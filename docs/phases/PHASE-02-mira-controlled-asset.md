# Phase 02 — MIRA as a Controlled Asset

**Duration:** 4–6 weeks
**Prerequisites:** Phase 01 gate passed **and** `../standards/MIRA-GUARDRAILS.md` fully implemented
**Merges:** original Phases 02, 03, 04

---

## نبذة بالعربية

تحويل MIRA من شات بوت دعم إلى أصل تجاري محكوم يولّد عملاء مؤهّلين.

**الشرط المانع:** لا يبدأ تنفيذ هذه المرحلة قبل تطبيق ملف الضوابط `MIRA-GUARDRAILS.md` كاملاً
واجتياز مجموعة الاختبارات فيه. هذا ليس تشدّداً زائداً — MIRA استباقية بلا ضوابط ستعطي عاجلاً أو
آجلاً سعراً أو زمن ترانزيت من عندها، وذلك التزام تجاري وقانوني على الشركة.

القاعدة: **MIRA تؤهّل العميل، ولا تُسعّر له.** المحادثة الناجحة تنتهي بطلب مكتمل يصل إلى فريق
التسعير — لا برقم يُعطى للعميل.

دمجنا هنا ثلاث مراحل أصلية (02 التكامل، 03 الصيانة، 04 التفاعل) لأن نشر MIRA بلا دورة مراجعة
وتحسين هو نشر مؤجَّل الفشل.

---

## Mission

Turn MIRA into a governed commercial asset that qualifies visitors and routes them into the
Phase 01 funnel — without ever making a commitment on behalf of MIDTRANS.

## Why these three original phases are merged

The original roadmap separated MIRA deployment (02), maintenance (03), and engagement (04).
Deploying a proactive assistant without the review loop already running is deferred failure: the
errors accumulate in production while the maintenance phase waits its turn.

Deployment, review cadence, and proactive engagement ship together or not at all.

---

## ⚠️ Status changed — MIRA is already live

**Established 2026-09-16** (`../baseline/D4-feature-inventory.md` § MIRA status): MIRA is in
production on the Claude API at `mira.midtrans.org`. It is talking to visitors now.

This phase was written as "build MIRA properly". It is now **"bring a live MIRA under control"** —
a different job with a different urgency.

| Consequence | Detail |
|---|---|
| **Guardrail work is no longer gated behind Phase 01** | The audit question in `../standards/MIRA-GUARDRAILS.md` §0 is open immediately |
| **Two production defects are already known** | An unanswered guardrail question, and a code path calling a model retired in Feb 2026 that fails silently |
| **D5 (proactive engagement) moves to the end** | Do not make a possibly-unguarded assistant *more* proactive |
| **A new D0 is required** | Audit what MIRA does today before changing it |

### D0 — Audit the live MIRA (new; comes first)

1. Review recent conversation logs for any stated rate, transit time, customs cost, acceptance or
   capacity. **This establishes whether the exposure has already materialised.**
2. Record what constraints exist today — system prompt only, output check, or nothing.
3. Identify every model reference, and fix the retired-model call: pin `claude-haiku-4-5`, drop
   the `-latest` alias, add alerting so a failed model call is never silent again.
4. Establish what MIRA is grounded in, and which languages it answers in.

Only then proceed to D1 below.

---

## Blocking prerequisite

**No expansion of MIRA's reach or proactivity happens until every box in `../standards/MIRA-GUARDRAILS.md` §9 is ticked**,
including the full test suite in §8 — with its Arabic and indirect-phrasing variants passing.

This is the single hardest gate in the programme, and it is deliberate. One invented rate that
reaches a customer costs more than a month of delay.

---

## Scope

### In scope

- Guardrail implementation and independent output enforcement
- Knowledge base built from real MIDTRANS operational knowledge
- MIRA available on every page
- MIRA → RFQ handoff
- Contextual and proactive engagement, within guardrails
- Review dashboard and the daily / weekly / monthly cadence

### Out of scope

- Any capability to quote, estimate, confirm, or commit — permanently out of scope
- Autonomous email sending
- Access to customer financial or shipment records without a separate security review

---

## Deliverables

### D1 — Guardrails in force

Two independent layers, because a single layer is a single point of failure:

1. **System prompt** carrying the full prohibition set
2. **Output check independent of the model** that blocks a response containing a prohibited
   pattern before it reaches the user

A model instructed not to quote will, under sufficient user pressure or unusual phrasing,
sometimes quote. The output check exists for exactly that case.

Plus: escalation routing that reaches a real person, logging of every guardrail trigger, and the
documented stop-the-line procedure.

### D2 — Knowledge base

Built from MIDTRANS's actual operational knowledge, not generic freight content. Primary sources:

- Published MIDTRANS website content
- The recurring-questions list from Phase 00 / D3
- Structured knowledge capture sessions with MIDTRANS operations staff

**Every entry carries:** `source`, `owner`, `reviewed_at`, `expires_at`. Entries without a named
owner do not enter the knowledge base.

**Content boundary:** the knowledge base holds procedures, requirements, document sets, process
sequences, and service descriptions. It holds **no** rates, transit times, costs, or acceptance
rules — not even internally, so that none can leak into a response.

### D3 — MIRA everywhere

- Persistent, non-intrusive entry point on every page
- Dedicated MIRA landing page (T1, all seven languages)
- Context awareness: MIRA knows which page the user is on and what it covers
- Conversation continuity across page navigation
- Full functionality in Arabic with correct RTL rendering

### D4 — MIRA → RFQ handoff

The commercial point of the whole phase.

- MIRA recognises shipment intent and collects the qualification fields from the Phase 01 wizard
- Handoff carries the context over — the user does not re-enter what they already told MIRA
- A conversation that ends without a handoff but with contact details is still routed as a lead
- The pricing desk receives the transcript alongside the structured enquiry

### D5 — Proactive engagement, within guardrails

MIRA may introduce relevant tools and resources — this was the useful core of the original
Phase 04, and it is retained with limits.

| Trigger | MIRA may suggest |
|---|---|
| Dimensions, weight, pallets, containers mentioned | Loading Calculator — explaining *why* utilisation affects cost, with no figures |
| Invoice, export documentation, customs paperwork | Commercial Invoice Builder |
| Syria import / export / customs / ports | The relevant Syria guide (Phase 04) |
| Partner, agent, distributor, representative, market entry | Business Representation services (Phase 05) |
| Vessel, survey, port call, P&I, claims | Maritime / P&I services (Phase 06) |

**Constraints on proactivity:**
- Contextual only. Never interrupt with an unrelated suggestion.
- One suggestion per conversation turn, at most.
- Never suggest a tool or page that does not exist yet.
- Never pressure. A declined suggestion is not repeated.
- The suggestion must be genuinely useful at that moment, or it is noise that trains users to
  dismiss MIRA.

### D6 — Review dashboard and cadence

Dashboard surfacing:

- Conversations, by language and by entry page
- Unanswered and low-confidence answers
- Abandoned conversations, with the last turn before abandonment
- Guardrail triggers, by rule
- Escalations and their outcomes
- Qualified leads generated
- Knowledge-base entries approaching `expires_at`

Cadence per `MIRA-GUARDRAILS.md` §7 — daily scan, weekly review, monthly audit — each with a
named owner.

---

## Technical requirements

- Guardrail output check runs independently of the model
- Full conversation logging with retention policy and consent handling
- Knowledge base versioned; changes reviewable and revertible
- Graceful degradation: if MIRA is unavailable, the page shows the standard contact routes, never
  a broken widget
- Response latency budget defined and monitored
- Mobile-first; usable one-handed on a phone
- Arabic RTL correct, including mixed Latin/Arabic text in a single message
- Accessible: keyboard navigable, screen-reader compatible, announced correctly
- Rate limiting and abuse protection
- No customer PII stored beyond the documented retention period

## SEO requirements

- MIRA landing page is a proper indexable page with real content, not an empty widget shell
- The widget does not block rendering or degrade mobile CWV
- Conversation content is not injected into the DOM in a way that creates duplicate or spurious
  indexable text

## CRO requirements

- Engagement rate, handoff rate, and qualified-lead rate tracked separately
- Proactive suggestions measured for acceptance — a suggestion type with a low acceptance rate is
  removed, not tuned indefinitely

## Language scope

**T1** for the MIRA landing page and interface. Conversational capability in **EN and AR at full
depth**; other languages at the depth the knowledge base supports.

**Do not claim a language capability that is not backed by reviewed knowledge-base content.** An
assistant that answers confidently but shallowly in German is worse than one that routes German
enquiries to a human.

## Capacity estimate

| Work | Estimate |
|---|---|
| Guardrails + independent output check + test suite | 1.5 weeks |
| Knowledge base (capture sessions, authoring, review) | 2 weeks |
| Site-wide deployment + RFQ handoff | 1 week |
| Proactive engagement layer | 0.5 week |
| Dashboard + cadence setup | 1 week |

Knowledge capture depends on MIDTRANS operations staff availability. **This is the most likely
source of slippage in the phase** — schedule the sessions before the phase starts.

---

## Risks and rollback

| Risk | Mitigation |
|---|---|
| **MIRA states a rate, transit time, or acceptance** | Two independent guardrail layers; full test suite including Arabic and indirect phrasing; stop-the-line on any confirmed violation |
| Knowledge base becomes stale; MIRA states outdated procedure | `expires_at` on every entry; monthly audit; named owner per entry |
| Proactive suggestions perceived as intrusive | One per turn; contextual only; acceptance measured; low-acceptance types removed |
| MIRA cannibalises the RFQ form without converting | Handoff rate and qualified-lead rate tracked separately from engagement |
| Arabic quality materially below English | Arabic tested as a first-class language, not as a translation check |
| Conversation logs create a data-protection exposure | Retention policy, consent, access control defined before launch |
| Knowledge capture sessions do not happen | Schedule and confirm before the phase starts; it is the critical path |

**Rollback:** MIRA is behind a feature flag, per-surface. Proactive engagement is a separate flag
from core MIRA, so proactivity can be disabled without removing the assistant. Disabling MIRA
entirely restores the Phase 01 contact routes, which remain live throughout.

---

## Validation

- [ ] `MIRA-GUARDRAILS.md` §9 fully ticked **before** any production exposure
- [ ] Full §8 test suite passing, including Arabic and indirect-phrasing variants
- [ ] Independent output check verified to block a prohibited response the model attempted
- [ ] Every knowledge-base entry has source, owner, reviewed_at, expires_at
- [ ] Handoff to RFQ tested end to end; pricing desk confirms usable output
- [ ] Escalation routing confirmed to reach a real person
- [ ] Arabic RTL verified on mobile, including mixed-script messages
- [ ] Degradation tested: MIRA offline leaves a usable page
- [ ] Dashboard live; daily/weekly/monthly owners named and briefed
- [ ] Level 2 checklist in `../standards/DEFINITION-OF-DONE.md` passed

## Exit gate

> **MIRA produces qualified leads at a measurable rate, with zero confirmed guardrail violations
> over four weeks of production traffic.**

Also required:
- Handoff rate meets the target set at phase start
- Review cadence has run at least one full monthly cycle
- No regression in the Phase 01 RFQ baseline

**A single confirmed guardrail violation fails the gate**, regardless of lead performance. Fix,
add a regression test, and re-run the four-week window.
