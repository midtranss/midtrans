# MIDTRANS Website Development Programme

**Owner:** MIDTRANS Shipping & Services
**Status:** Planning package — approved structure, pending Phase 00 execution
**Last revised:** 2026-09-16

---

## نبذة بالعربية

هذه حزمة تخطيط تطوير موقع MIDTRANS. تتكوّن من سبع مراحل تنفيذية (بالإضافة إلى مرحلة تشخيص إلزامية تسبقها)،
وكل مرحلة لا تبدأ إلا بعد أن تُثبت المرحلة التي قبلها نتيجة قابلة للقياس.

المبدأ الحاكم: **رفع التحويلات قبل رفع عدد الصفحات.** المقياس الوحيد الذي نحكم به على نجاح أي مرحلة هو
عدد طلبات عروض الأسعار المؤهّلة شهرياً — وليس عدد الصفحات المنشورة.

قبل تنفيذ أي مرحلة، اقرأ ملفات `standards/` أولاً. هي ملزمة وليست اختيارية.

---

## How to use this package

Read in this order. Do not skip.

1. **`standards/`** — binding rules that apply to every phase. Read all five before writing a
   single line of content or code.
2. **`phases/00-MASTER-PLAN.md`** — the programme: sequencing, gates, sizing, governance.
3. **`phases/PHASE-00` … `PHASE-07`** — one self-contained package per phase.
4. **`reference/`** — where the earlier 25-phase map went, and why.

Each phase file is written to be handed directly to an implementer — a developer, a content
writer, or a coding agent — without further briefing.

---

## Contents

### Standards (binding, apply everywhere)

| File | What it governs |
|---|---|
| `standards/WRITING-STANDARDS.md` | Voice, forbidden words, factual limits on all published copy |
| `standards/MIRA-GUARDRAILS.md` | What MIRA may and may not say. **Blocking prerequisite for Phase 02.** |
| `standards/LANGUAGE-SCOPE.md` | Which content gets which of the 7 languages, and why |
| `standards/SEO-STANDARDS.md` | Technical SEO, structured data, internal linking, thin-content rules |
| `standards/DEFINITION-OF-DONE.md` | The checklist every page and every phase must pass |

### Phases

| # | File | Duration (est.) | Exit gate |
|---|---|---|---|
| 00 | `PHASE-00-diagnostics-baseline.md` | 2 weeks | Baseline document signed off |
| 01 | `PHASE-01-conversion-infrastructure.md` | 4–6 weeks | Follow-up rate down; RFQ volume not down |
| 01 | `PHASE-01-RFQ-WIZARD-SPEC.md` | — | Implementation spec for Phase 01 / D1 |
| 01 | `PHASE-01-MEASUREMENT-FRAMEWORK.md` | — | Defines the Phase 01 gate: metrics, events, guardrails |
| 02 | `PHASE-02-D0-AUDIT.md` | — | Executable now: audit what the live MIRA has already said |
| 02 | `PHASE-02-mira-controlled-asset.md` | 4–6 weeks | MIRA generates qualified leads, zero commitments given |
| 03 | `PHASE-03-tools-lead-engine.md` | 4 weeks | Each tool produces a measurable conversion path |
| 03 | `PHASE-03-TOOL-CALCULATION-SPEC.md` | — | What each tool computes, and what it must never compute |
| 04 | `PHASE-04-syria-trade-center.md` | 6–8 weeks | 25–40 deep pages live, originality verified |
| 04 | `PHASE-04-KNOWLEDGE-CAPTURE.md` | — | Interview guides — the critical path for Phase 04 |
| 04 | `PHASE-04-EDITORIAL-GATE.md` | — | Pre-publication check for every content page |
| 05 | `PHASE-05-market-entry-representation.md` | 8–10 weeks | Representation + market-entry hubs live and converting |
| 05 | `PHASE-05-CLAIMS-AND-DUPLICATION.md` | — | Market-claim sourcing, and the cluster duplication test |
| 06 | `PHASE-06-maritime-pi.md` | 6 weeks | Maritime and P&I hubs live, qualified enquiries received |
| 06 | `PHASE-06-BOUNDARY-AND-ESCALATION.md` | — | The liability boundary, and the escalation §6 lacked |
| 07 | `PHASE-07-trust-conditional-expansion.md` | Continuous | Per-market gates, opened one at a time |
| 07 | `PHASE-07-OPERATING-CHECKS.md` | — | The market gate as a register, and the recurring health check |

### Baseline workspace

| File | Purpose |
|---|---|
| `baseline/` | Phase 00 worksheets — fill in as the audit runs. `D6-BASELINE.md` is the document every later gate is measured against. |
| `briefs/` | Paste-ready execution briefs for agents or developers with access this planning session lacks. |

### Reference

| File | Purpose |
|---|---|
| `reference/ORIGINAL-25-PHASE-MAP.md` | Full mapping of the original 25-phase roadmap onto this programme. Nothing was discarded silently. |

---

## The one rule that matters most

> **No phase starts until the phase before it has produced a number.**

If a phase does not move its metric, the correct action is to stop and re-diagnose — not to
proceed to the next phase. Building phase N+1 on top of a phase N that did not work compounds
the error instead of correcting it.

---

## Estimates: read this before quoting any date

Every duration in this package is an **estimate made before Phase 00 has run**. Phase 00 exists
precisely because the current state of the codebase, the traffic, and the conversion funnel are
not yet known in detail.

Durations assume a working team is assigned and available. They are not commitments, and they
must be re-confirmed at the end of Phase 00 against the real codebase and the real baseline.

No figure in this package describes freight rates, transit times, customs costs, capacity, or
any operational commitment. See `standards/WRITING-STANDARDS.md` §4.
