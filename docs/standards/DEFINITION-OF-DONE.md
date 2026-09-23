# Definition of Done

**Status:** BINDING. Nothing ships without passing the applicable checklist.

---

## نبذة بالعربية

ثلاثة مستويات من "مُنجَز": لكل صفحة، لكل ميزة تقنية، ولكل مرحلة.

القاعدة الحاكمة: **المرحلة لا تُعتبر منجَزة بتسليم المخرجات، بل بتحقيق الرقم.** إن سُلّمت كل
المخرجات ولم يتحرّك المقياس، فالمرحلة لم تنجح — والقرار الصحيح هو التوقف وإعادة التشخيص، لا
الانتقال إلى المرحلة التالية.

---

## Level 1 — Page Done

Every published page, in every language:

**Content**
- [ ] Passes `WRITING-STANDARDS.md` review checklist
- [ ] Forbidden words absent; no unsupported claims
- [ ] No rate, transit time, customs cost, acceptance or capacity figure — including hedged
- [ ] Contains at least one insight a competitor could not have written
- [ ] Passes the uniqueness test in `SEO-STANDARDS.md` §2
- [ ] Reviewed and approved by a named human, with date recorded

**Technical**
- [ ] Correct parent, breadcrumbs, ≥3 relevant inbound internal links, no orphan
- [ ] Schema implemented, validated, matches visible content
- [ ] `canonical` self-referencing; `hreflang` complete and reciprocal
- [ ] Core Web Vitals pass on mobile
- [ ] Images optimised with meaningful alt text
- [ ] Indexation decision deliberate and recorded
- [ ] Renders correctly on mobile at 360px width
- [ ] Arabic version RTL-correct and set in Cairo

**Conversion**
- [ ] Carries the CTA set defined in Phase 01
- [ ] MIRA accessible from the page (from Phase 02 onward)
- [ ] Conversion events firing and verified in analytics

---

## Level 2 — Feature Done

Every technical deliverable:

- [ ] Works on mobile, tablet and desktop
- [ ] Works in all languages in its assigned tier, including RTL
- [ ] Keyboard accessible; meets WCAG 2.1 AA for contrast and focus
- [ ] Degrades gracefully when JavaScript fails
- [ ] Error states handled and tested, not only the happy path
- [ ] Forms validate server-side, not only client-side
- [ ] Personal data handled per the consent and retention policy
- [ ] Analytics events fire correctly and are verified in the reporting tool
- [ ] No regression in existing functionality — verified, not assumed
- [ ] Rollback path documented before deployment
- [ ] Lint, type check, build and available tests pass

---

## Level 3 — Phase Done

A phase is complete only when **all four** hold:

1. **All deliverables shipped** and each passes Level 1 or Level 2 as applicable
2. **Exit gate metric met** — the number defined in that phase's file has actually moved
3. **No regression** in any prior phase's metric
4. **Retrospective recorded** — what worked, what did not, what changes for the next phase

### The gate rule

> **Delivering the outputs is not the same as passing the phase.**

If every deliverable shipped and the metric did not move, the phase **did not succeed**. The
correct response is to stop and re-diagnose — not to proceed.

Proceeding builds phase N+1 on an assumption that phase N just disproved. That is how programmes
fail slowly and expensively while appearing to be on schedule.

### Gate decision record

Each gate produces a short written record:

| Field | Content |
|---|---|
| Phase | Which phase |
| Baseline | The metric at phase start |
| Result | The metric at phase end |
| Verdict | Pass / Fail |
| Decision | Proceed / Re-diagnose / Re-scope |
| Owner | Who decided |
| Date | When |

---

## What is explicitly not a completion criterion

- Number of pages published
- Number of words written
- Number of keywords ranked
- Number of features shipped
- Percentage of the roadmap completed

These measure activity. The programme is measured on **qualified RFQ volume**.
