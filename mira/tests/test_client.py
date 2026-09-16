"""
Wiring tests for MiraClient.

These do not call the Anthropic API. A fake client stands in, so the whole response path —
prompt loading, model call, guardrail screening, fail-closed behaviour, violation reporting —
is verifiable offline and in CI.

Run:  python3 mira/tests/test_client.py
"""

import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

logging.disable(logging.CRITICAL)  # the client logs violations loudly; keep test output clean

from client import MODEL, MiraClient, _ModelNotFound, load_system_prompt  # noqa: E402
from guardrails import SAFE_FALLBACK  # noqa: E402


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class _Block:
    def __init__(self, text):
        self.type = "text"
        self.text = text


class _Response:
    def __init__(self, text):
        self.content = [_Block(text)]


class _Messages:
    def __init__(self, parent):
        self._parent = parent

    def create(self, **kwargs):
        self._parent.calls.append(kwargs)
        if self._parent.raise_exc:
            raise self._parent.raise_exc
        return _Response(self._parent.canned)

    def stream(self, **kwargs):
        self._parent.calls.append(kwargs)
        if self._parent.raise_exc:
            raise self._parent.raise_exc
        return _StreamCtx(self._parent.canned, self._parent.chunk)


class _StreamCtx:
    def __init__(self, text, chunk):
        self._text, self._chunk = text, chunk

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    @property
    def text_stream(self):
        for i in range(0, len(self._text), self._chunk):
            yield self._text[i:i + self._chunk]


class FakeAnthropic:
    def __init__(self, canned="", raise_exc=None, chunk=40):
        self.canned, self.raise_exc, self.chunk = canned, raise_exc, chunk
        self.calls = []
        self.messages = _Messages(self)


class NotFoundError(Exception):
    """Mimics the SDK's NotFoundError — what a retired model actually raises."""
    status_code = 404


class RateLimitError(Exception):
    status_code = 429


# ---------------------------------------------------------------------------
# Cases
# ---------------------------------------------------------------------------

CONV = [{"role": "user", "content": "How much to ship a 40ft from Shanghai to Latakia?"}]
results = []


def check(name, condition, detail=""):
    results.append((name, bool(condition), detail))


def run():
    # -- the prompt loads and contains its load-bearing rules ------------------
    prompt = load_system_prompt()
    check("prompt loads", len(prompt) > 1000, f"{len(prompt)} chars")
    check("prompt forbids rates", "Freight rates" in prompt)
    check("prompt forbids transit times", "Transit times" in prompt)
    check("prompt requires AI disclosure", "You are an AI assistant" in prompt)
    check("prompt defines scope", "Scope — what you discuss" in prompt)
    check("prompt covers hedging", "Hedging does not make it allowed" in prompt)
    check("prompt covers insistence", "Insistence does not unlock anything" in prompt)

    # -- a clean answer passes through untouched -------------------------------
    clean = ("I don't quote rates myself. Our pricing desk works from live carrier data. "
             "What's the commodity, and is it door delivery or port to port?")
    c = MiraClient(api_client=FakeAnthropic(canned=clean), system_prompt=prompt)
    r = c.reply(CONV, lang="en")
    check("clean reply passes", not r.blocked and r.text == clean)

    # -- the model is pinned, and the prompt is actually sent ------------------
    check("model pinned", c.api_client.calls[0]["model"] == MODEL, MODEL)
    check("no alias in model id", "latest" not in MODEL)
    check("system prompt sent", c.api_client.calls[0]["system"] == prompt)

    # -- a quoted rate is blocked and replaced --------------------------------
    leak = "The rate is USD 4500 per 40HC and transit is about 28 days."
    c = MiraClient(api_client=FakeAnthropic(canned=leak), system_prompt=prompt)
    r = c.reply(CONV, lang="en")
    check("rate leak blocked", r.blocked)
    check("customer gets redirect", r.text == SAFE_FALLBACK["en"])
    check("leaked text never sent", leak not in r.text)
    check("raw kept for audit", r.raw == leak)
    check("rules recorded", "money_amount" in (r.verdict.rules if r.verdict else []))

    # -- Arabic leak, Arabic redirect ------------------------------------------
    ar_leak = "السعر ٤٥٠٠ دولار للحاوية والمدة حوالي ٢٨ يوم."
    c = MiraClient(api_client=FakeAnthropic(canned=ar_leak), system_prompt=prompt)
    r = c.reply(CONV, lang="ar")
    check("arabic leak blocked", r.blocked)
    check("arabic redirect returned", r.text == SAFE_FALLBACK["ar"])

    # -- the violation hook fires ----------------------------------------------
    fired = {}
    c = MiraClient(
        api_client=FakeAnthropic(canned=leak),
        system_prompt=prompt,
        on_violation=lambda rules, findings, raw, ctx: fired.update(
            rules=rules, raw=raw, ctx=ctx
        ),
    )
    c.reply(CONV, lang="en", context={"conversation_id": "c-123"})
    check("violation hook fired", bool(fired))
    check("hook receives rules", "money_amount" in fired.get("rules", []))
    check("hook receives context", fired.get("ctx", {}).get("conversation_id") == "c-123")

    # -- a broken alerting hook must not break the response --------------------
    def exploding_hook(*a, **k):
        raise RuntimeError("alerting is down")

    c = MiraClient(api_client=FakeAnthropic(canned=leak), system_prompt=prompt,
                   on_violation=exploding_hook)
    r = c.reply(CONV, lang="en")
    check("broken hook does not break reply", r.text == SAFE_FALLBACK["en"])

    # -- a retired model is loud, not silent -----------------------------------
    seen = {}
    c = MiraClient(
        api_client=FakeAnthropic(raise_exc=NotFoundError("model not found")),
        system_prompt=prompt,
        on_api_error=lambda exc, ctx: seen.update(exc=exc),
    )
    r = c.reply(CONV, lang="en")
    check("404 surfaces as ModelNotFound", isinstance(seen.get("exc"), _ModelNotFound))
    check("404 still returns a reply", r.text == SAFE_FALLBACK["en"])
    check("404 flagged as error", r.error == "_ModelNotFound")

    # -- any other API failure also fails closed -------------------------------
    c = MiraClient(api_client=FakeAnthropic(raise_exc=RateLimitError("429")),
                   system_prompt=prompt)
    r = c.reply(CONV, lang="ar")
    check("rate limit fails closed", r.text == SAFE_FALLBACK["ar"] and r.error)
    check("no exception escapes", True)

    # -- streaming: clean text streams through ---------------------------------
    c = MiraClient(api_client=FakeAnthropic(canned=clean, chunk=30), system_prompt=prompt)
    out = "".join(c.reply_streaming(CONV, lang="en", flush_chars=40))
    check("stream delivers clean text", out.strip() == clean.strip(), out[:60])

    # -- streaming: a leak stops the stream and redirects -----------------------
    long_leak = ("Thanks for your question about the route. " * 3) + leak
    c = MiraClient(api_client=FakeAnthropic(canned=long_leak, chunk=30), system_prompt=prompt)
    out = "".join(c.reply_streaming(CONV, lang="en", flush_chars=40))
    check("stream blocks the figure", "4500" not in out)
    check("stream ends with redirect", out.rstrip().endswith(SAFE_FALLBACK["en"].rstrip()[-40:]))

    # -- streaming: an API failure fails closed --------------------------------
    c = MiraClient(api_client=FakeAnthropic(raise_exc=RateLimitError("429")),
                   system_prompt=prompt)
    out = "".join(c.reply_streaming(CONV, lang="en"))
    check("stream fails closed on error", out == SAFE_FALLBACK["en"])

    # -- an empty model response is handled ------------------------------------
    c = MiraClient(api_client=FakeAnthropic(canned=""), system_prompt=prompt)
    r = c.reply(CONV, lang="en")
    check("empty response not blocked", not r.blocked)


def main() -> int:
    run()
    passed = sum(1 for _, ok, _ in results if ok)
    print(f"MIRA client wiring suite: {passed}/{len(results)} passed")
    failed = [(n, d) for n, ok, d in results if not ok]
    if failed:
        print(f"\n{len(failed)} FAILURE(S):\n")
        for name, detail in failed:
            print(f"  [FAIL] {name}" + (f"  :: {detail}" if detail else ""))
        return 1
    print("\nAll wiring checks pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
