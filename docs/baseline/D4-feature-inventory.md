# D4 — Feature Inventory

**Owner:** _________  **Date:** _________

> Verdict is one of: **Keep** · **Fix** · **Rebuild** · **Retire**.
> **Nothing is retired without explicit written approval.**

| Feature | Exists? | Works? | Monthly usage | Produces enquiries? | Verdict | Notes |
|---|---|---|---|---|---|---|
| Loading Calculator | | | | | | |
| Container Calculator | | | | | | |
| CBM Calculator | | | | | | |
| Volumetric Weight Calculator | | | | | | |
| Commercial Invoice Builder | | | | | | |
| Shipment Tracker | | | | | | |
| MIRA chatbot | | | | | | |
| RFQ / quote form | | | | | | |
| WhatsApp contact | | | | | | |
| Consultation booking | | | | | | |
| Language switcher | | | | | | |
| Blog / knowledge center | | | | | | |

## Pages that already rank and convert — **protect these**

| Page | Language | Organic entrances | Conversions | Note |
|---|---|---|---|---|
| | | | | |

> Phase 01 strengthens these pages. It does not replace or restructure them without evidence.

## MIRA current state (if deployed)

| Item | Finding |
|---|---|
| Deployed? On which pages? | |
| Underlying model / platform | |
| Knowledge source | |
| **Any guardrails currently in place?** | |
| **Has it ever stated a rate, transit time, or acceptance?** | |
| Conversation logs available? | |
| Languages supported | |

> If MIRA is live with no guardrails, that is an **active commercial exposure**, not a Phase 02
> item. Report it immediately to the programme owner.

---

## Partial findings from D3 (2026-09-16) — email evidence only, not verified in code

These came out of the D3 mailbox analysis. They are **indirect evidence** and must be confirmed
against the codebase in D1 before being treated as established.

| Feature | Evidence | Provisional verdict |
|---|---|---|
| **RFQ wizard** | Live. Sequential `QREQ-` references, auto-acknowledgement to the enquirer, structured notification to a named internal list. First submission 11 Sep 2026. | **Keep** — this is the Phase 01 foundation, not a rebuild |
| **Website chat widget** | Live. Observed relaying a visitor message to email, answered manually by named MIDTRANS staff in English and Arabic. | Keep; instrument it |
| **Older website form** | Superseded by the wizard. Structured-field format, ~5 submissions in 12 months. | Retire **only** after the wizard proves itself — needs approval |
| **Customer account / login** | Live. A password-reset flow was observed, including a bilingual EN/AR notice. | Investigate in D1 — scope and purpose unknown |
| Loading / Container / CBM / Volumetric calculators | No evidence either way in email | UNKNOWN — D1 must check |
| Commercial Invoice Builder | No evidence either way in email | UNKNOWN — D1 must check |
| Shipment Tracker | No evidence either way in email | UNKNOWN — D1 must check |

### MIRA status — ⚠️ CORRECTED 2026-09-16

> **An earlier version of this file stated that no autonomous AI assistant appeared to be live.
> That was wrong.** It generalised from a single chat conversation that humans answered — which
> was most likely an escalation *from* MIRA, not evidence of its absence. The corrected finding
> below is based on direct documentary evidence.

**MIRA is live and runs on the Claude API.** Evidence, from an Anthropic service notice dated
11 September 2026 (in the MIDTRANS mailbox):

| Fact | Source |
|---|---|
| MIRA has its own API key, named `MIRA · mira.midtrans.org` | Anthropic notice, verbatim |
| MIRA therefore has its own subdomain: `mira.midtrans.org` | Same |
| MIRA has its own mailbox: `mira@midtrans.org` | Password-reset mail addressed to it, 15 Sep 2026 |
| Anthropic API is in paid, active use | Billing receipts: 20 Aug, 11 Sep, 15 Sep 2026 |

### ⚠️ Two open issues, both requiring action

**Issue 1 — a MIRA code path calls a retired model and fails silently.**

- Model called: `claude-3-5-haiku-20241022`, via the alias `claude-3-5-haiku-latest`
- That model was **retired on 19 February 2026** and is no longer served
- The call returns `not_found_error`
- **Anthropic's notice states explicitly: the failure "does not appear on the Usage page"**

The volume reported is low (1 failed request on 10 September), which suggests a secondary code
path rather than MIRA's main conversation loop — a fallback, a classifier, a summariser, a title
generator. But **a silent failure is worse than a loud one**: nothing surfaces it, so it can
persist indefinitely. Whatever that path does, it has been doing nothing since February.

**Fix:** change the model ID to `claude-haiku-4-5`.

Migration notes for this specific change:
- Use the plain ID `claude-haiku-4-5` — do **not** append a date suffix.
- Replace the `-latest` alias with the pinned ID. The alias is what turned a model retirement
  into a silent production failure; pinning makes the next retirement a deliberate, visible
  decision instead of an outage.
- Haiku 4.5 context window is 200K.
- Extended thinking on Haiku 4.5 still uses `thinking: {type: "enabled", budget_tokens: N}`; the
  newer `adaptive` mode and the `effort` parameter are **not** supported on this model and will
  error.
- Search the application logs for the old model string to find every call site — there may be
  more than one.

**Issue 2 — MIRA is live, so the guardrail exposure is ACTIVE, not hypothetical.**

`../standards/MIRA-GUARDRAILS.md` was written on the assumption that guardrails would be built
before MIRA went live. That assumption no longer holds. MIRA is already talking to visitors.

**This inverts the Phase 02 sequencing.** Guardrails are no longer a prerequisite for future
work — they are **remediation of a live system**, and they come before anything else in the
programme.

### Questions D1 must answer, in priority order

1. **Does MIRA currently have ANY guardrail preventing it from stating a rate, transit time,
   customs cost, cargo acceptance, or capacity?** This is the single most urgent question in the
   entire audit.
2. Is there an output check independent of the model, or only a system prompt?
3. Which model does MIRA's **main** conversation loop use? (The failing call is a side path.)
4. Where is the retired model ID referenced — how many call sites?
5. Are MIRA's conversations logged and retrievable? Where?
6. What is MIRA grounded in — published content, a knowledge base, or an unconstrained prompt?
7. What does `mira.midtrans.org` serve, and is it publicly reachable?
8. Which languages does MIRA answer in, and is quality equivalent across them?

### Immediate recommendation

**Until question 1 is answered, treat MIRA as an unguarded live assistant** and apply
`MIRA-GUARDRAILS.md` §7's stop-the-line posture: if it can quote, it should not be proactive.

Reviewing MIRA's recent conversation logs for any stated rate, transit time, or acceptance is the
fastest way to establish whether the exposure has already materialised — and it is the first
thing to do.

### Operational software

A freight-forwarding platform and a separate accounting/ERP tool both appear in the mailbox as
active vendor relationships. **D1 must establish what is actually in use, what data it holds, and
whether it can report quote-to-booking conversion** — which D3 could not establish and which the
programme needs for its primary metric.
