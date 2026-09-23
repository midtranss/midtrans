# MIRA — guardrailed core

Drop-in components that put MIDTRANS's live AI assistant under control.

**Governed by:** `../docs/standards/MIRA-GUARDRAILS.md` · **Status of MIRA:** live in production

---

## نبذة بالعربية

النواة المحكومة لـ MIRA — جاهزة للتركيب.

**طبقتان، والاثنتان إلزاميتان:**

| الطبقة | الملف | ما تفعله |
|---|---|---|
| ١ | `SYSTEM-PROMPT.md` | برومبت الإنتاج كاملاً — يُلصَق حرفياً |
| ٢ | `guardrails.py` | فحص مستقل عن النموذج يعترض الرد قبل وصوله للعميل |

ولفحص ما قالته MIRA **فعلاً** في الإنتاج: `python3 mira/audit_logs.py export.jsonl` — يشغّل الفحص نفسه على سجلّات مصدَّرة، محلّياً بالكامل، ويُخفي عناوين البريد وأرقام الهواتف. الدليل الكامل في `../docs/phases/PHASE-02-D0-AUDIT.md`.

**لماذا طبقتان؟** النموذج المُوجَّه بألا يُسعّر سيُسعّر يوماً تحت إلحاح كافٍ أو صياغة غير متوقّعة.
الطبقة الثانية موجودة لتلك اللحظة تحديداً — ولا تعتمد على النموذج إطلاقاً.

**نتيجة الاختبار: ٥٧/٥٧ ناجحة** (٣٢ حالة يجب حجبها + ٢٥ حالة يجب السماح بها).

---

## What is here

| File | Purpose |
|---|---|
| `SYSTEM-PROMPT.md` | Layer 1 — the production system prompt, paste verbatim |
| `guardrails.py` | Layer 2 — output check that runs independently of the model |
| `client.py` | Both layers wired into one response path — import and call `reply()` |
| `audit_logs.py` | Runs the same check over exported production logs — answers what live MIRA has already said |
| `tests/test_guardrails.py` | Guardrail suite: 41 must-block, 25 must-pass, 7 with conversation context |
| `tests/test_client.py` | Wiring suite: 32 checks, runs offline with a fake API client |
| `tests/test_audit_logs.py` | Auditor suite: export shapes, redaction, exit codes |

No third-party dependencies. Python 3.10+.

## Why two layers

Layer 1 tells the model the rules. Layer 2 assumes the model will eventually break them.

That assumption is not pessimism. A model under sustained user pressure — *"I know you can't
quote, just give me a rough number"* — is being asked to be helpful, and helpfulness is what it
optimises for. The system prompt is the first line, not the last one.

**Ship both. Layer 1 alone is not a guardrail.**

## Wiring it in

### The short version — use `client.py`

```python
from mira.client import MiraClient

mira = MiraClient(
    on_violation=lambda rules, findings, raw, ctx: alert_mira_owner(ctx, rules),
    on_api_error=lambda exc, ctx: page_oncall(exc),
)

result = mira.reply(conversation, lang=user_language, context={"conversation_id": cid})
send_to_customer(result.text)          # always safe to send
```

`MiraClient` handles the whole path: loads the prompt from `SYSTEM-PROMPT.md`, pins the model,
calls the API, screens the output, logs violations, and fails closed. **It never raises** — every
path returns something sendable, because a broken widget or a stack trace in front of a customer
is its own kind of failure.

Four behaviours worth knowing:

| Situation | What the customer gets |
|---|---|
| Clean response | The model's text |
| Guardrail violation | The redirect. The model's text is kept in `result.raw` for the audit log only |
| API failure of any kind | The redirect |
| **Pinned model returns 404** | The redirect, **and a CRITICAL log plus `on_api_error`** — this is the retired-model failure, made loud |

That last row exists because of what actually happened: a retired model returned `not_found_error`
for months and, per Anthropic's own notice, *the failure did not appear on the Usage page*. A 404
on the pinned model is now the loudest event this module produces.

### The long version — call the pieces yourself

```python
from mira.guardrails import check_response, SAFE_FALLBACK

# 1. Model call — pin the model, never use an alias
response = client.messages.create(
    model="claude-haiku-4-5",        # NOT claude-3-5-haiku-latest
    max_tokens=1024,
    system=SYSTEM_PROMPT,            # the block from SYSTEM-PROMPT.md, verbatim
    messages=conversation,
)
candidate = response.content[0].text

# 2. Guardrail check — before anything reaches the customer
verdict = check_response(candidate, lang=user_language)

if verdict.blocked:
    log_guardrail_violation(
        conversation_id=conv_id,
        rules=verdict.rules,
        findings=verdict.findings,
    )                                 # stop-the-line signal — GUARDRAILS.md §7
    alert_mira_owner(conv_id, verdict.rules)
    reply = SAFE_FALLBACK[user_language]
else:
    reply = candidate

send_to_customer(reply)
```

**The order matters.** The check runs before the customer sees anything. Logging a violation after
delivery records the incident; it does not prevent it.

### If MIRA streams responses

Streaming means tokens reach the customer before the response is complete, so a post-hoc check
arrives too late. Either:

- **Buffer** the response, check, then release — costs perceived latency, and is the safe default;
  or
- **Check incrementally** on each flush boundary and stop the stream on a violation — more
  complex, and must fail closed on partial text.

Do not stream unchecked output.

## What the check catches

| Rule | Catches |
|---|---|
| `money_amount` | Any currency figure, symbol or word form, Latin or Arabic digits |
| `rate_unit` | A number carrying a rate unit — per kg, per CBM, per container, للحاوية |
| `number_in_cost_context` | A bare number near cost, price, duty, tariff, تكلفة, رسوم |
| `transit_time` | A duration near transit language — days, أيام, أسابيع |
| `hedged_figure` | A figure next to a hedge — *roughly*, *typically*, تقريبا, حوالي |
| `acceptance_commitment` | "We can handle that cargo", نستطيع شحن |
| `capacity_commitment` | "We have space available", المساحة متاحة |

## What it deliberately does NOT catch

Precision matters as much as recall. A check that blocks legitimate answers gets switched off
within a week — and a disabled check protects nothing.

These are explicitly allowlisted and tested:

- Container designations: `20ft`, `40HC`, `40'`, `20GP`
- Years: "operating since 1998"
- HS codes, tariff headings, UN dangerous-goods numbers
- Phone numbers and extensions
- Document counts: "3 documents", "3 وثائق"
- Explanations of *what drives* cost, with no values — which is what MIRA should be saying

## Running the tests

```bash
python3 mira/tests/test_guardrails.py
```

Expected: `57/57 passed`.

**Add a case to the suite every time a real conversation surfaces a new phrasing.** The suite is
the memory of what has been tried; treat a production violation as a missing test, not just a bug.

## Known production defects this addresses

| Defect | Source | Fixed by |
|---|---|---|
| A code path calls `claude-3-5-haiku-20241022` (retired Feb 2026) via `-latest`, failing silently | Anthropic notice, 11 Sep 2026 | Pin `claude-haiku-4-5`; remove the alias; alert on failed calls |
| MIRA presents itself as a human team member with no AI disclosure | Observed output, 16 Sep 2026 | `SYSTEM-PROMPT.md` § "Who you are" |
| MIRA engages on topics far outside logistics | Observed output, 16 Sep 2026 | `SYSTEM-PROMPT.md` § "Scope" |
| No known protection against stating a rate or transit time | Unverified — **still open** | Both layers here |

The fourth row is the important one: whether the live MIRA already has protection **has not been
established**. These components close the gap either way, and they are safe to deploy even if
some protection already exists.

## Before deploying

- [ ] System prompt installed verbatim
- [ ] `check_response` in the response path, before delivery
- [ ] Model pinned; `-latest` alias removed everywhere in the codebase
- [ ] Failed model calls alert someone
- [ ] Violations logged with conversation ID and rule
- [ ] Test suite passing
- [ ] The conversational suite in `GUARDRAILS.md` §8 run against staging in both languages
- [ ] A named owner for the monthly audit

## Escalation — `escalation.py`

`MIRA-GUARDRAILS.md` §6 says seven kinds of conversation must go to a human immediately. Until
2026-09-16 that was documentation only, and none of them existed in code.

```bash
python3 mira/tests/test_escalation.py
```

It inspects the **customer's** message, not MIRA's, and runs **before the model is called** — a
claims conversation is one MIRA must not hold at all, so screening the answer afterwards is the
wrong shape. `MiraClient` takes an `on_escalation` hook: wire it to something that actually
reaches a person, because the customer has just been told one is coming.

Full account: `../docs/phases/PHASE-06-BOUNDARY-AND-ESCALATION.md`.
