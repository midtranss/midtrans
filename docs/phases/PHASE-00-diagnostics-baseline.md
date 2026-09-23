# Phase 00 — Diagnostics & Baseline

**Duration:** 2 weeks
**Prerequisite for:** every other phase
**Status:** not started

---

## نبذة بالعربية

مرحلة التشخيص — وهي **غير موجودة إطلاقاً في الخطة الأصلية، وهي أهم مرحلة في المشروع كله**.

الهدف: معرفة أين نحن فعلاً قبل أن نقرّر إلى أين نذهب. فحص الكود الحقيقي، واستخراج أرقام اثني عشر
شهراً، وتحليل طلبات العروض الواردة، وجرد صادق لما هو موجود فعلاً مقابل ما نظنه موجوداً.

بدون هذه المرحلة، كل ما يليها إيمان لا إدارة — ولن نستطيع بعد ستة أشهر أن نقول إن نجحنا أم لا،
لأننا لا نعرف من أين بدأنا.

**تحذير مقصود:** قد تكشف هذه المرحلة أن مصدر عملائك الحقيقي ليس الموقع أصلاً. إن حدث ذلك، تتغيّر
الخطة كلها — وهذا نجاح للمرحلة، لا فشل لها.

---

## Mission

Establish what is actually true about the MIDTRANS website — its code, its traffic, its funnel,
and its existing features — before committing budget to changing it.

## Why this phase exists

The roadmap this programme replaces contained no current-state data. Not one figure about
traffic, enquiries, conversion rate, or the real state of the codebase.

A plan built without a baseline is a coordinated guess. Worse, it is unfalsifiable: six months
later nobody can say whether it worked, because nobody recorded where it started.

This phase is deliberately short and deliberately blocking.

---

## Scope

### In scope

- Technical audit of the production codebase
- Twelve months of analytics extraction and analysis
- Inbound RFQ analysis (Gmail and any other intake channel)
- Honest inventory of existing features and tools
- Competitive and SERP position check for the target topic clusters
- Baseline document with the metrics the whole programme will be judged against

### Out of scope

- Any code change beyond what is needed to instrument measurement
- Any content change
- Any design change

**This phase changes nothing. It only finds out.**

---

## Deliverables

### D1 — Technical audit

| Item | What to record |
|---|---|
| Stack | Framework, language, versions, hosting, build and deploy pipeline |
| Repository | Location, branch model, who has access, CI state |
| Routing | Full route map; how pages are defined and added |
| i18n | How the 7 languages are implemented; where translations live; how a new language version is created |
| URL scheme | Current language URL pattern; whether it is consistent |
| CMS | What exists, who can edit, what requires a developer |
| Data layer | Database, schema, what customer data is stored and where |
| Performance | Core Web Vitals on mobile for the top 20 pages by traffic |
| Accessibility | Baseline check on the main templates |
| Technical SEO | hreflang correctness, canonicals, sitemap, robots.txt, indexation state, redirect chains |
| Dependencies | Outdated or unmaintained packages; known vulnerabilities |
| Integrations | Analytics, forms, email, WhatsApp, chat, tracking, anything third-party |

**Sensitive-data rule:** this is a read-only audit. Do not modify, export, or copy production
customer data. Record schema and volumes, not records.

### D2 — Traffic and conversion baseline

Twelve months, segmented by language and by country:

- Sessions, users, entrances
- Top entry pages
- Traffic by source and medium
- Bounce and engagement by page cluster
- Existing goal or conversion configuration — and whether it is trustworthy
- Current form submissions: volume, source page, completion rate
- Device split, with mobile isolated

**If conversion tracking is absent or unreliable, say so plainly.** Installing it becomes the
first task of Phase 01, and the baseline is established from the first clean month instead.

### D3 — RFQ intake analysis

Sample a minimum of 100 recent inbound enquiries (or all of them, if fewer):

- Where did each come from — website form, email, WhatsApp, phone, referral, existing client?
- Which are qualified (actionable by the pricing desk) vs. unqualified?
- What is the actual origin/destination and service mix of real demand?
- What information is routinely missing, forcing a follow-up email?
- What questions recur? These become FAQ and MIRA knowledge-base source material.
- Which languages do real enquiries arrive in?

> **This is the highest-value deliverable in the phase.** It shows what demand actually exists,
> as opposed to what the roadmap assumed. The "information routinely missing" list directly
> specifies the Phase 01 RFQ wizard fields.

**Handling:** this involves customer data. Work from aggregates and anonymised summaries. Do not
copy customer records into any planning document.

### D4 — Feature inventory

For every tool and feature the roadmap assumes exists:

| Feature | Exists? | Works? | Traffic | Produces enquiries? | Verdict |
|---|---|---|---|---|---|
| Loading Calculator | | | | | |
| Container Calculator | | | | | |
| CBM Calculator | | | | | |
| Volumetric Calculator | | | | | |
| Commercial Invoice Builder | | | | | |
| Shipment Tracker | | | | | |
| MIRA | | | | | |
| RFQ / quote form | | | | | |
| WhatsApp contact | | | | | |

Verdict is one of: **Keep** · **Fix** · **Rebuild** · **Retire**.

Nothing is retired without explicit written approval.

### D5 — Position check

- Where does MIDTRANS currently appear for its core topic clusters, by language?
- Who ranks for Syria trade, Syria customs, and Syria market entry queries — and what do their
  pages actually contain?
- What does an AI assistant currently say when asked about shipping to Syria, and is MIDTRANS
  cited?
- Which existing MIDTRANS pages already rank and convert? **These are assets — Phase 01 protects
  and strengthens them rather than replacing them.**

### D6 — Baseline document

The single artefact every later gate is measured against:

| Metric | Value | Period | Source | Confidence |
|---|---|---|---|---|
| Qualified RFQ / month | | | | |
| Total enquiries / month | | | | |
| Website-sourced enquiries / month | | | | |
| Organic sessions / month | | | | |
| RFQ form completion rate | | | | |
| Mobile share of traffic | | | | |
| Indexed pages | | | | |
| Mobile CWV pass rate | | | | |

Confidence is recorded explicitly. A number nobody trusts must be labelled as such, not quietly
carried forward.

---

## Technical requirements

- Read-only access to the production repository
- Read access to analytics for 12 months
- Access to the RFQ intake channel for the sample
- No production data modified, exported, or copied
- Findings recorded in this repository under `docs/baseline/`

---

## Risks

| Risk | Mitigation |
|---|---|
| No usable historical analytics | Install clean tracking as the first Phase 01 task; baseline from first clean month; state the gap explicitly |
| Codebase not accessible | **Blocking.** Programme cannot start. Escalate to programme owner. |
| Audit reveals the website is not the main lead source | This is a finding, not a failure. Re-scope the programme accordingly. |
| Feature inventory contradicts roadmap assumptions | Expected. Update plan before Phase 01. |
| Temptation to start fixing during the audit | Explicitly out of scope. Log findings; do not act. |

## Rollback

Nothing changes in this phase, so there is nothing to roll back. If measurement instrumentation
is added, it is additive and independently removable.

---

## Validation

- [ ] Every deliverable D1–D6 produced and reviewed
- [ ] Baseline numbers reconciled across at least two independent sources where possible
- [ ] Confidence level recorded for every metric
- [ ] Feature inventory verdicts agreed with the programme owner
- [ ] Open decisions from `00-MASTER-PLAN.md` §10 closed
- [ ] No production data modified or copied

## Exit gate

> **Baseline document signed off by the programme owner, with a stated qualified-RFQ-per-month
> figure and a recorded confidence level.**

Additionally, before Phase 01 starts:

- Phase 01 duration estimate re-confirmed against the real codebase
- Roles from `00-MASTER-PLAN.md` §8 assigned by name
- Any finding that invalidates the plan escalated and resolved

**If the baseline cannot be established, Phase 01 does not start.**
