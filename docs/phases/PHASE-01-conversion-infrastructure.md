# Phase 01 — Conversion Infrastructure

**Duration:** 4–6 weeks (re-confirm at Phase 00 gate)
**Prerequisite:** Phase 00 baseline signed off
**Replaces:** original Phase 01

---

## نبذة بالعربية

بناء آلة التحويل. هذه المرحلة هي قلب المشروع كله.

الفكرة: كل ما يأتي بعدها — ميرا، الأدوات، المحتوى — يصبّ في هذا المسار. إن كان المسار مكسوراً،
فكل زائر إضافي نجلبه هو زائر مهدور.

المخرج الأساسي: **RFQ Wizard متعدد الخطوات** مصمَّم بناءً على تحليل الطلبات الواردة الفعلي من
المرحلة صفر — لا على تخمين.

قاعدة صارمة: لا يُحذف أي نموذج أو مسار تواصل يعمل حالياً قبل أن يثبت البديل تفوّقه بالأرقام.

---

## Mission

Build the lead-capture system that every later phase feeds into, and prove it converts better
than what exists today.

## Why this is first

Traffic sent into a funnel that does not convert is wasted twice: the visit is lost, and the
experiment teaches nothing about whether the content was any good.

The RFQ funnel is the heart of the system. MIRA (Phase 02), the tools (Phase 03), and all content
(Phases 04–06) exist to feed it. Building it first means everything after it is measurable.

---

## Scope

### In scope

- RFQ wizard (multi-step, qualification-driven)
- Consultation booking path
- WhatsApp path
- Callback request path
- Unified CTA framework across all service pages
- Conversion tracking with consent governance

### Out of scope

- MIRA integration (Phase 02 — the funnel must work standalone first)
- New content pages
- Visual redesign beyond what the CTA framework requires

### Preservation rule

**No existing form, contact route, or conversion path is removed in this phase.** New paths run
alongside old ones until data shows the replacement performs better. Removal then requires
explicit written approval.

---

## Deliverables

### D1 — RFQ Wizard

The central deliverable.

**Field set is derived from Phase 00 / D3**, specifically the "information routinely missing"
list — the data the pricing desk actually has to chase by follow-up email. It is not designed
from assumption.

**Design rules:**

| Rule | Detail |
|---|---|
| Progressive disclosure | Ask the easy, low-commitment questions first. Contact details last. |
| Partial submission is a lead | An abandoned wizard with an email captured is still routed. Do not discard it. |
| Save and resume | A returning user does not start over |
| Branching | Sea / air / road / customs / project cargo paths ask different questions |
| Mobile-first | Built for a phone. Mobile is the primary device, not an adaptation. |
| Honest about what happens next | Tell the user a human will respond. Do not promise a response time that is not guaranteed. |
| Field count | Minimum that lets the pricing desk act without a follow-up email |

**Hard constraint:** the wizard must never display, estimate, or imply a rate, transit time,
customs cost, acceptance, or capacity — including as a "preliminary indication". See
`../standards/WRITING-STANDARDS.md` §4.

**Routing:** submissions reach the pricing desk in a structured, consistent format, with the
source page and language recorded.

### D2 — Consultation funnel

For enquiries that are not yet a shipment — market entry, representation, maritime. A different
intent from an RFQ, and it needs a different path: a scheduled conversation, not a quote request.

### D3 — WhatsApp path

- Present on every service page and in the site header or a persistent element
- Pre-filled context message identifying the page the user came from
- Click tracked as a conversion event
- Mobile behaviour verified on real devices, not only in an emulator

### D4 — Callback request

A short form — name, number, preferred window, topic. For users who will not type a full enquiry
but will take a call.

**Do not state a callback time that operations has not committed to.**

### D5 — Unified CTA framework

Every service page carries a consistent CTA set:

`Request a Quote` · `WhatsApp` · `Book a Consultation` · `Contact`

Rules:
- Consistent placement and hierarchy across all pages
- Contextual labelling — the CTA on the customs page references customs, not generic "get
  started"
- One primary action per page; the others secondary
- Present and usable in every language in the page's tier, including RTL
- No CTA promises anything operations has not committed to

### D6 — Measurement and consent

- Conversion events for every path in D1–D5, verified firing in the reporting tool
- Funnel visualisation: entry → step → submission → qualified
- Source attribution: which page, which language, which country
- **Consent management** covering EU visitors — Phase 07 targets Germany, France, Netherlands and
  Sweden, so this is built now, not retrofitted
- Documented data retention policy for enquiry data
- Server-side validation on every form

---

## Technical requirements

- Mobile-first; verified at 360px width on real devices
- Server-side validation, not client-side only
- Works with JavaScript degraded — at minimum a functional fallback contact route
- WCAG 2.1 AA: keyboard navigation, focus states, contrast, form labels, error announcement
- All languages in tier, RTL-correct for Arabic (Cairo)
- Spam protection that does not degrade accessibility (no CAPTCHA that blocks screen readers)
- Personal data encrypted in transit and at rest
- Error states designed and tested — a failed submission must never silently lose a lead
- Submission retry / queue so a backend outage does not drop enquiries

## SEO requirements

- Wizard steps are not separate indexable URLs, or are `noindex`
- No layout shift from CTA elements (CWV)
- Structured data unaffected
- No change to existing ranking URLs without a 301

## CRO requirements

- A/B or before-after measurement against the Phase 00 baseline
- Abandonment tracked per step, so the weak step is identifiable
- Minimum two weeks of clean data before drawing conclusions

## Language scope

**T1 — all seven languages.** This is the commercial core; a broken funnel in any language is a
lost market.

## Capacity estimate

| Work | Estimate |
|---|---|
| RFQ wizard (design, build, routing, test) | 2–3 weeks |
| Consultation, WhatsApp, callback paths | 1 week |
| CTA framework rollout | 1 week |
| Measurement, consent, QA across 7 languages | 1 week |

Concurrent work assumed. Sequential execution extends this materially.

---

## Risks and rollback

| Risk | Mitigation |
|---|---|
| New wizard converts worse than the existing form | Run both in parallel; route by split; keep the old form until the new one wins on data |
| Enquiries lost during cutover | Submission queue + retry; monitor volume daily against baseline for the first two weeks |
| Wizard too long; abandonment rises | Per-step abandonment tracking; partial submissions still routed as leads |
| Consent implementation suppresses analytics | Test consent and measurement together before launch, not after |
| RTL breakage in the wizard | Arabic QA is a named checklist item, not a final glance |
| Pricing desk overwhelmed by volume | Confirm intake capacity with operations before launch |

**Rollback:** every new path is additive and independently disableable by feature flag. The
existing contact routes remain live throughout. Rolling back is turning off the new path, not
restoring a backup.

---

## Validation

- [ ] Every path tested end to end in all 7 languages, including RTL
- [ ] Submissions verified arriving at the pricing desk, correctly formatted
- [ ] Conversion events verified in the analytics tool — not assumed from code
- [ ] Mobile tested on real devices
- [ ] Accessibility audit passed
- [ ] No rate, transit time, cost, acceptance or capacity anywhere in the flow
- [ ] Existing contact routes still functional
- [ ] Rollback verified by actually exercising the feature flag
- [ ] Lint, type check, build, and available tests pass
- [ ] Level 2 checklist in `../standards/DEFINITION-OF-DONE.md` passed

## Exit gate

> **Qualified RFQ submissions per month measurably higher than the Phase 00 baseline, over a
> minimum of four weeks of clean data.**

Also required:
- Zero enquiries lost during cutover
- Funnel measurement trustworthy enough to evaluate Phases 02–06 against

**If qualified RFQ volume did not move:** stop. Do not start Phase 02. Re-diagnose — the problem
is upstream of the funnel (traffic quality, audience, or offer), and building MIRA on top of a
funnel that does not convert will not fix it.
