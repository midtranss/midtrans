"""
MIRA client — the two guardrail layers wired together.

This is the whole response path in one place: pinned model, system prompt, the independent
output check, violation logging, and fail-closed behaviour. Import it and call `reply()`.

    from mira.client import MiraClient

    mira = MiraClient()
    result = mira.reply(conversation, lang="ar")
    send_to_customer(result.text)

Design decisions worth knowing before you change anything:

  * The model ID is PINNED, never an alias. The `-latest` alias is what turned a model
    retirement into a silent production failure in Feb 2026 — the call started returning
    not_found_error and, per Anthropic's own notice, the failure did not even appear on the
    Usage page. `_ModelNotFound` below makes that loud.

  * Responses are BUFFERED before the guardrail runs. Streaming tokens to a customer means
    they have already read the number by the time a post-hoc check fires. Streaming is
    available via `reply_streaming()`, which checks each flush boundary and fails closed.

  * On any guardrail violation the customer gets the redirect, never the model's text, and
    never an error message. A blocked response still collects the enquiry.

  * On any API failure the customer gets the redirect too. MIRA going down must not produce a
    broken widget or a stack trace.

Requires: `anthropic` (official SDK). The SDK is imported lazily so the module can be unit
tested without it.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

import escalation
from guardrails import SAFE_FALLBACK, Verdict, check_response

log = logging.getLogger("mira")

# --------------------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------------------

#: Pinned model. Do NOT replace with an alias such as `claude-haiku-4-5-latest`.
#: Changing this is a deliberate decision that should be reviewed, not an automatic upgrade.
MODEL = "claude-haiku-4-5"

MAX_TOKENS = 2048

#: Where the layer-1 prompt lives. The text between the HTML markers is extracted.
PROMPT_PATH = Path(__file__).parent / "SYSTEM-PROMPT.md"

_PROMPT_START = "<!-- ===== BEGIN SYSTEM PROMPT ===== -->"
_PROMPT_END = "<!-- ===== END SYSTEM PROMPT ===== -->"


def load_system_prompt(path: Path | None = None) -> str:
    """Extract the system prompt from SYSTEM-PROMPT.md, between its markers."""
    path = path or PROMPT_PATH
    text = path.read_text(encoding="utf-8")
    try:
        body = text.split(_PROMPT_START, 1)[1].split(_PROMPT_END, 1)[0]
    except IndexError as exc:
        raise RuntimeError(
            f"{path} is missing its BEGIN/END system prompt markers — refusing to start "
            f"with an unknown prompt."
        ) from exc
    body = body.strip()
    if not body:
        raise RuntimeError(f"{path} contains an empty system prompt — refusing to start.")
    return body


# --------------------------------------------------------------------------------------
# Result
# --------------------------------------------------------------------------------------


def _last_user_text(messages: Sequence[dict]) -> str:
    """The most recent user turn, so the guardrail knows what the reply is answering.

    A reply like "we can definitely handle that" carries no cargo word of its own; the subject
    lives in the question. The user's text is never scanned for violations — see
    `guardrails.check_response`.
    """
    for message in reversed(list(messages or [])):
        if message.get("role") != "user":
            continue
        content = message.get("content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return "\n".join(
                block.get("text", "")
                for block in content
                if isinstance(block, dict) and block.get("type") == "text"
            )
    return ""


@dataclass
class MiraResult:
    """What to send, and what happened."""

    text: str
    blocked: bool = False
    error: str | None = None
    verdict: Verdict | None = None
    raw: str | None = None  #: the model's original text when blocked — for the audit log only

    #: Set when GUARDRAILS.md §6 says a human must take over. `text` is then the handover
    #: message and the model was never called — routing is the caller's job.
    escalation: Any = None

    @property
    def safe_to_send(self) -> bool:
        return bool(self.text)

    @property
    def needs_human(self) -> bool:
        return bool(self.escalation)


class _ModelNotFound(RuntimeError):
    """The pinned model was rejected by the API — usually a retirement. Never silent."""


# --------------------------------------------------------------------------------------
# Client
# --------------------------------------------------------------------------------------


@dataclass
class MiraClient:
    """MIRA's response path, with both guardrail layers in place."""

    api_client: Any = None
    system_prompt: str = field(default_factory=load_system_prompt)
    model: str = MODEL
    max_tokens: int = MAX_TOKENS

    #: Called with (rules, findings, raw_text, context) on every blocked response.
    #: Wire this to your alerting — a violation is a stop-the-line event, see GUARDRAILS.md §7.
    on_violation: Callable[[list[str], list[Any], str, dict], None] | None = None

    #: Called with (exception, context) when the model call fails. Wire to alerting:
    #: a _ModelNotFound here means the pinned model is gone and MIRA is silently broken.
    on_api_error: Callable[[Exception, dict], None] | None = None

    #: Called with (escalation, context) when §6 routes a conversation to a human. Wire this
    #: to whatever actually reaches a person — an escalation nobody receives is not one.
    on_escalation: Callable[[Any, dict], None] | None = None

    def __post_init__(self) -> None:
        if self.api_client is None:
            self.api_client = self._default_client()

    @staticmethod
    def _default_client() -> Any:
        try:
            from anthropic import Anthropic
        except ImportError as exc:  # pragma: no cover - depends on the deployment env
            raise RuntimeError(
                "The `anthropic` package is not installed. Install it, or pass an api_client."
            ) from exc
        return Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # -- public ------------------------------------------------------------------------

    def reply(
        self,
        messages: Sequence[dict],
        lang: str = "en",
        context: dict | None = None,
    ) -> MiraResult:
        """Produce a customer-safe reply. Never raises; always returns something sendable."""
        context = context or {}
        fallback = SAFE_FALLBACK.get(lang, SAFE_FALLBACK["en"])

        # GUARDRAILS.md §6 is checked BEFORE the model is called. A claims or incident
        # conversation is one MIRA must not hold at all, so screening its answer afterwards is
        # the wrong shape — the answer should never be generated. It also saves the call.
        routed = escalation.detect(messages)
        if routed:
            self._report_escalation(routed, context)
            return MiraResult(text=escalation.handover(lang), escalation=routed)

        try:
            candidate = self._call_model(messages)
        except Exception as exc:  # noqa: BLE001 - deliberate: never surface an error to a customer
            self._report_api_error(exc, context)
            return MiraResult(text=fallback, error=type(exc).__name__)

        return self._screen(
            candidate, lang=lang, context=context, fallback=fallback,
            user_said=_last_user_text(messages),
        )

    def reply_streaming(
        self,
        messages: Sequence[dict],
        lang: str = "en",
        context: dict | None = None,
        flush_chars: int = 120,
    ) -> Iterable[str]:
        """
        Stream, checking at flush boundaries and failing closed.

        Yields chunks only once the text accumulated so far passes the guardrail. On a
        violation it stops the stream and yields a marker plus the redirect — the customer
        may have seen a partial sentence, but never a figure.

        Buffered `reply()` remains the safer default. Use this only when perceived latency
        genuinely matters, and accept that a partial sentence can reach the screen.
        """
        context = context or {}
        fallback = SAFE_FALLBACK.get(lang, SAFE_FALLBACK["en"])

        routed = escalation.detect(messages)
        if routed:
            self._report_escalation(routed, context)
            yield escalation.handover(lang)
            return

        user_said = _last_user_text(messages)
        accumulated = ""
        released = 0

        try:
            for delta in self._stream_model(messages):
                accumulated += delta
                if len(accumulated) - released < flush_chars:
                    continue
                verdict = check_response(accumulated, lang=lang, context=user_said)
                if verdict.blocked:
                    self._report_violation(verdict, accumulated, context)
                    yield "\n\n"
                    yield fallback
                    return
                yield accumulated[released:]
                released = len(accumulated)
        except Exception as exc:  # noqa: BLE001
            self._report_api_error(exc, context)
            yield fallback
            return

        verdict = check_response(accumulated, lang=lang, context=user_said)
        if verdict.blocked:
            self._report_violation(verdict, accumulated, context)
            yield "\n\n"
            yield fallback
            return
        if released < len(accumulated):
            yield accumulated[released:]

    # -- internals ---------------------------------------------------------------------

    def _screen(
        self, candidate: str, lang: str, context: dict, fallback: str, user_said: str = ""
    ) -> MiraResult:
        verdict = check_response(candidate, lang=lang, context=user_said)
        if verdict.blocked:
            self._report_violation(verdict, candidate, context)
            return MiraResult(text=fallback, blocked=True, verdict=verdict, raw=candidate)
        return MiraResult(text=candidate, verdict=verdict)

    def _call_model(self, messages: Sequence[dict]) -> str:
        try:
            response = self.api_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                messages=list(messages),
            )
        except Exception as exc:  # noqa: BLE001
            raise self._classify(exc) from exc
        return self._extract_text(response)

    def _stream_model(self, messages: Sequence[dict]) -> Iterable[str]:
        try:
            with self.api_client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.system_prompt,
                messages=list(messages),
            ) as stream:
                yield from stream.text_stream
        except Exception as exc:  # noqa: BLE001
            raise self._classify(exc) from exc

    @staticmethod
    def _classify(exc: Exception) -> Exception:
        """Turn a model-not-found into a distinct, loud error instead of a generic failure."""
        name = type(exc).__name__
        status = getattr(exc, "status_code", None)
        if name == "NotFoundError" or status == 404:
            return _ModelNotFound(
                "The pinned model was rejected (404). It has most likely been retired. "
                "This is the failure mode that went unnoticed for months in early 2026 — "
                "it does not appear on the API Usage page. Update MODEL in mira/client.py."
            )
        return exc

    @staticmethod
    def _extract_text(response: Any) -> str:
        """Join the text blocks of a Messages API response."""
        parts = []
        for block in getattr(response, "content", []) or []:
            if getattr(block, "type", None) == "text":
                parts.append(getattr(block, "text", ""))
        return "".join(parts).strip()

    def _report_violation(self, verdict: Verdict, raw: str, context: dict) -> None:
        log.error(
            "MIRA GUARDRAIL VIOLATION rules=%s context=%s",
            verdict.rules,
            {k: v for k, v in context.items() if k != "raw"},
        )
        for finding in verdict.findings:
            log.error("  %s @%d :: %s", finding.rule, finding.position, finding.excerpt)
        if self.on_violation:
            try:
                self.on_violation(verdict.rules, verdict.findings, raw, context)
            except Exception:  # noqa: BLE001 - alerting must never break the response path
                log.exception("on_violation handler raised")

    def _report_escalation(self, routed, context: dict) -> None:
        logging.getLogger("mira").warning(
            "MIRA escalation: %s | %s", ",".join(routed.names), context)
        if self.on_escalation:
            try:
                self.on_escalation(routed, context)
            except Exception:  # noqa: BLE001 - a broken hook must not break the reply
                logging.getLogger("mira").exception("on_escalation hook failed")

    def _report_api_error(self, exc: Exception, context: dict) -> None:
        if isinstance(exc, _ModelNotFound):
            log.critical("MIRA MODEL UNAVAILABLE :: %s", exc)
        else:
            log.error("MIRA API call failed: %s: %s", type(exc).__name__, exc)
        if self.on_api_error:
            try:
                self.on_api_error(exc, context)
            except Exception:  # noqa: BLE001
                log.exception("on_api_error handler raised")
