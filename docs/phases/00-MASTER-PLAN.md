# MIDTRANS Website Development — Master Plan

**Version:** 1.0
**Date:** 2026-09-16
**Supersedes:** the 25-phase "MIDTRANS VISION 2030" roadmap (see `../reference/ORIGINAL-25-PHASE-MAP.md`)

---

## نبذة بالعربية

الخطة الرئيسية لتطوير موقع MIDTRANS: سبع مراحل تنفيذية تسبقها مرحلة تشخيص إلزامية.

**السؤال الحاكم للمشروع كله:** ما الذي يمنع زائراً مؤهلاً اليوم من أن يصبح شحنة؟ وكل عمل لا يجيب
على هذا السؤال يُؤجَّل.

المبادئ الأربعة: العمق قبل العرض · لا مرحلة تبدأ قبل أن تُثبت سابقتها رقماً · اللغة قرار تجاري ·
MIRA أصل محكوم لا شات بوت.

المقياس الوحيد: **عدد طلبات عروض الأسعار المؤهّلة شهرياً** — وليس عدد الصفحات.

---

## 1. The question this programme answers

> **What stops a qualified visitor today from becoming a shipment?**

Everything in this plan exists to answer that question. Work that does not answer it is deferred,
regardless of how attractive it looks on a roadmap.

### What changed from the previous roadmap

The earlier roadmap was built on an untested assumption: *MIDTRANS is not visible enough, and the
answer is more content.*

Its own closing section contradicted that assumption — "the site already has good content but
needs higher conversion more than more pages" — yet nineteen content-expansion phases remained in
the plan.

This programme takes that conclusion seriously and restructures around it.

| | Previous roadmap | This plan |
|---|---|---|
| Phases | 25, parallel, open-ended | 7 sequential + 1 diagnostic prerequisite |
| Year-1 page target | ~500 | **150–200** |
| Two-year page target | 1,500–2,000 | **400–500** |
| Governing metric | Page count | **Qualified RFQ / month** |
| Language planning | Absent | Tiered per content type |
| MIRA constraints | Absent | Blocking prerequisite |
| Baseline measurement | Absent | Phase 00, mandatory |
| US location pages | 9 state/city pages | **Removed** — doorway-page risk |

Page count is not a goal. It is a by-product of having useful things to say.

---

## 2. Governing principles

### Principle 1 — Depth before breadth

One page on customs clearance at Latakia, written from 27 years of doing it, beats fifty generic
city pages. It also cannot be copied by a competitor. Generic content is the failure state — not
incorrect, just worthless and replaceable.

### Principle 2 — No phase starts until the previous one produced a number

Every phase has an exit gate expressed as a metric. If the metric does not move, the programme
stops and re-diagnoses. It does not proceed.

This is the single most important rule in this document. It is what separates a plan from a wish
list.

### Principle 3 — Language is a commercial decision, not a technical one

Seven languages applied naively to a 1,500-page target produces 10,500 URLs and a project that
never finishes. Coverage is assigned per content type by expected return, before writing starts.
See `../standards/LANGUAGE-SCOPE.md`.

### Principle 4 — MIRA is a governed commercial asset, not a chatbot

MIRA qualifies; it does not quote. No rate, transit time, customs cost, acceptance, capacity, or
operational commitment — ever, in any phrasing. Guardrails are a prerequisite for Phase 02, not a
deliverable of it. See `../standards/MIRA-GUARDRAILS.md`.

---

## 3. The programme

| # | Phase | Est. duration | Exit gate |
|---|---|---|---|
| **00** | Diagnostics & Baseline | 2 weeks | Baseline document signed off |
| **01** | Conversion Infrastructure | 4–6 weeks | Qualified RFQ volume measurably up vs. baseline |
| **02** | MIRA as a Controlled Asset | 4–6 weeks | MIRA produces qualified leads; zero commitments given |
| **03** | Tools as a Lead Engine | 4 weeks | Every tool shows a measurable conversion path |
| **04** | Syria Trade & Procedures Center | 6–8 weeks | 25–40 deep pages live; originality verified |
| **05** | Market Entry & Representation | 8–10 weeks | Hubs live and producing qualified enquiries |
| **06** | Maritime & P&I | 6 weeks | Hubs live; qualified enquiries from the target audience |
| **07** | Trust & Conditional Expansion | Continuous | Per-market gates, opened one at a time |

**Estimated to first content phase:** ~4 months. **Estimated through Phase 06:** ~12 months.

All durations assume an assigned, available team. They are estimates made **before** Phase 00 has
run, and must be re-confirmed against the real codebase and the real baseline at the Phase 00
gate.

---

## 4. Sequencing logic

Phases 00–03 build and prove the **conversion machine**. Phases 04–06 feed it with content that
only MIDTRANS can write. Phase 07 expands, one gated market at a time.

```
00 Diagnostics ─── mandatory prerequisite for everything
        │
01 Conversion ──── the RFQ funnel is the heart of the system
        │
02 MIRA ────────── feeds the funnel; guardrails first
        │
03 Tools ───────── strongest lead magnets; feed funnel + MIRA
        │
04 Syria Center ── the defensible content moat begins here
        │
   ┌────┴────┐
05 Market    06 Maritime
   Entry &      & P&I
   Represen-
   tation
   └────┬────┘
        │
07 Trust & Conditional Expansion (continuous)
```

**Why content comes fourth, not first:** sending traffic to a funnel that does not convert wastes
the traffic and, worse, teaches nothing. Fix the funnel, then fill it.

**Why Phase 04 is where content starts:** Syrian trade procedure is the one subject where
MIDTRANS has knowledge no competitor can replicate. If content is going to be written, it starts
where the advantage is absolute.

---

## 5. Sizing

| Horizon | Target | Composition |
|---|---|---|
| Months 0–12 | **150–200 pages** | Conversion, MIRA, tools, Syria center |
| Months 12–24 | **400–500 pages** | Representation, maritime, P&I, gated markets |
| Steady state | Growth follows demand, not a target | |

At roughly 400 pages of unique content under the tiering in `LANGUAGE-SCOPE.md`, the site carries
approximately **1,050 URLs** — against ~2,800 if everything were translated into all seven
languages.

200 pages nobody else can write beat 2,000 generic ones. That is not encouragement; it is the
documented direction of both search ranking systems and AI citation behaviour.

---

## 6. Measurement

### Primary metric

**Qualified RFQ submissions per month.**

A qualified RFQ carries enough information for the pricing desk to act: origin, destination,
commodity, approximate volume or weight, and a contactable requester.

### Supporting metrics

- RFQ completion rate (started → submitted)
- MIRA conversations producing a qualified lead
- Tool usage → RFQ progression
- Assisted conversions by content cluster
- Organic entrances to converting pages

### Explicitly not success metrics

Page count · word count · keywords ranked · features shipped · percentage of roadmap completed.

These measure activity. The business is paid for shipments.

---

## 7. What was deliberately removed, and why

Nothing was discarded silently. Full mapping in `../reference/ORIGINAL-25-PHASE-MAP.md`.

| Removed | Reason |
|---|---|
| **US state and city pages** (Texas, Houston, California, LA, NY, NJ, Florida, Atlanta, Chicago) | Templated location pages without unique operational substance are assessed at **site level**. The risk is suppression of the entire domain; the upside is marginal. Replaced by one strong "US companies entering Syria" page in Phase 05. |
| **"500 pages in 6 months"** | At the stated quality bar (4,500–6,000 words, 12 FAQs, schema) across seven languages, this is ~3 reference pages per day. It produces either poor content or no content. |
| **"50 case studies"** | Replaced by 10 excellent ones in Phase 07. Fifty thin case studies is fifty thin pages. |
| **Parallel execution of 25 phases** | Nobody executes 25 things. Executing 25 things finishes none. |
| **Unconstrained proactive MIRA** | Direct commercial and legal exposure. Reinstated in Phase 02 with guardrails. |

### Retained unchanged

- The writing standards, including the forbidden-word list — the strongest part of the original
  document, kept verbatim in `../standards/WRITING-STANDARDS.md`
- The specialist positioning: Syria Trade + Maritime + Business Representation
- The revised sequencing conclusion: conversion before expansion

---

## 8. Governance

### Roles to assign before Phase 00

| Role | Responsibility |
|---|---|
| **Programme owner** | Gate decisions. Authority to stop the programme. |
| **Technical lead** | Codebase, implementation, technical DoD |
| **Content lead** | Editorial standards, factual accuracy, originality |
| **MIRA owner** | Knowledge base accuracy, guardrail enforcement, review cadence |
| **Measurement owner** | Baseline integrity, metric reporting, gate evidence |

A phase without a named owner does not start.

### Cadence

| When | What |
|---|---|
| Weekly | Progress against the current phase's exit metric |
| Phase end | Gate review, written decision record, retrospective |
| Monthly | MIRA audit (see `MIRA-GUARDRAILS.md` §7) |
| Quarterly | Language tier review — promote or demote based on data |

---

## 9. Risk register

| Risk | Impact | Mitigation |
|---|---|---|
| **MIRA invents a rate or transit time — ACTIVE, not hypothetical: MIRA is already live** | Commercial and legal exposure; loss of trust | **Audit live conversation logs now**; treat as unguarded until proven otherwise; then guardrails, independent output check, stop-the-line |
| A MIRA model call fails silently in production | Broken behaviour nobody sees | Pin model IDs, never use `-latest`; alert on failed model calls |
| Thin or templated content triggers site-level suppression | Loss of ranking across the whole domain | Uniqueness test mandatory per page; US location pages removed |
| Content capacity below plan | Phases stall; half-finished sections go live | Language tiering; conservative page targets; no partial publication |
| Phase gates bypassed under schedule pressure | Compounding a failed assumption | Gate rule in `DEFINITION-OF-DONE.md`; written gate decision record |
| Baseline never established | Success becomes unmeasurable | Phase 00 is a hard prerequisite |
| Translation debt | Half-translated site; hreflang errors | Tiering; no partial publication rule |
| Regression in existing working features | Loss of current conversions | No removal without explicit approval; rollback path per deliverable |
| Personal data handling (EU markets targeted) | Regulatory exposure | Consent and retention policy in Phase 01 |
| Key-person dependency on MIDTRANS operational knowledge | Content moat cannot be built | Structured knowledge capture sessions scheduled in Phase 04 |

---

## 10. Open decisions

These must be closed at the Phase 00 gate:

1. **Where does the production website codebase live?** Not yet identified. Phase 00 cannot start
   without it.
2. **Current stack, CMS, and i18n implementation** — unknown until Phase 00.
3. **Which tools already exist and work** — partially answered. **MIRA is confirmed live** at
   `mira.midtrans.org`, and the RFQ wizard launched 11 Sep 2026. Calculator and Invoice Builder
   status remains unverified. See `../baseline/D4-feature-inventory.md`.
3b. **Does the live MIRA have any guardrails?** — the highest-priority open question in the
   programme.
4. **Team capacity and budget** — determines whether the estimates in §3 hold.
5. **Analytics and consent tooling currently in place.**
6. **URL scheme for languages** — to be decided once, against the existing codebase, then frozen.
