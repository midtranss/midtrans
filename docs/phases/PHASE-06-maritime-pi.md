# Phase 06 — Maritime & P&I

**Duration:** 6 weeks
**Prerequisite:** Phase 05 gate passed
**Merges:** original Phases 10 and 11

---

## نبذة بالعربية

المحور البحري ومراسل P&I.

الجمهور هنا ضيق جداً وعالي القيمة: ملاك السفن، المشغّلون، المسّاحون، نوادي P&I، ومؤمّنو النقل
البحري. عددهم بالمئات لا بالملايين — والجودة هنا تهزم الكمية بلا منافسة.

هذا جمهور محترف يقرأ بعين ناقدة: أي صفحة فيها لغة تسويقية عامة أو مصطلح بحري مستخدم خطأً تُرفض
فوراً. المصطلحات يجب أن تكون دقيقة تماماً، والصفحة يجب أن تُقرأ وكأن من كتبها حضر عمليات موانئ
فعلية.

**حدّ حاسم:** ممنوع تماماً تقديم أي رأي في مسؤولية، أو تقييم مطالبة، أو تفسير غطاء تأميني. MIDTRANS
تنسّق وتحضر وتوثّق — ولا تُقرّر مسؤولية ولا تُقيّم مطالبات.

**ملاحظة:** المحتوى بالإنجليزية فقط — لغة العمل في القطاع البحري الدولي.

---

## Mission

Establish MIDTRANS as a credible maritime services and P&I correspondent presence for shipowners,
operators, surveyors, and marine insurers.

## Why this audience justifies a dedicated phase

The maritime and P&I audience is small — hundreds of relevant decision-makers worldwide, not
millions. But each relationship is high-value and durable, and the buying decision is made almost
entirely on demonstrated competence.

This is the phase where quality beats volume by the widest margin in the entire programme. Ten
pages that read as written by someone who has attended port operations will outperform a hundred
pages that do not.

## The credibility bar

This audience reads critically. Two things get a page dismissed immediately:

1. **Generic marketing language.** A P&I claims handler has read a thousand "trusted partner"
   pages.
2. **Imprecise terminology.** Terms of art must be used exactly. A single misused maritime term
   signals that the writer has not done the work, and the reader stops.

Terminology review by someone with genuine maritime operational background is a **required
deliverable**, not an optional check.

---

## Scope

### In scope

- Maritime representation
- Ship agency support
- Port call coordination
- Vessel support services
- Marine survey coordination
- Cargo survey coordination
- P&I correspondent services
- Claims support coordination
- Marine incident support

### Out of scope — hard boundary

MIDTRANS **coordinates, attends, and documents**. It does not:

- Give an opinion on liability
- Assess, value, or adjust a claim
- Interpret insurance coverage
- Provide legal advice
- Act as a surveyor where independent appointment is required
- State that a claim will be accepted, paid, or defended

Every page in the P&I cluster must make the distinction between coordination and determination
explicit. Blurring it is both a professional credibility failure and a liability exposure.

### Page budget

**15–25 pages.** The audience is small; the content must be excellent. Fewer, better.

---

## Deliverables

### D1 — Maritime hub

The entry point, organised the way this audience thinks about services — by operational need, not
by MIDTRANS's internal service taxonomy.

### D2 — Representation and port call cluster

- Maritime representation — scope, responsibilities, the client's responsibilities
- Ship agency support
- Port call coordination: what MIDTRANS handles, at which ports, and the sequence
- Vessel support services
- Port-specific operational detail for Latakia and Tartous, cross-linked to Phase 04

The port call pages are where MIDTRANS's actual presence shows. Generic port call descriptions are
available everywhere; what happens at Latakia and Tartous specifically is not.

### D3 — Survey coordination cluster

- Marine survey coordination
- Cargo survey coordination
- Vessel attendance
- Damage and condition survey attendance

**Boundary, stated on each page:** MIDTRANS coordinates and attends. Where an independent surveyor
appointment is required, MIDTRANS facilitates it and does not substitute for it.

### D4 — P&I correspondent cluster

- P&I correspondent services — the scope precisely defined
- Claims support coordination
- Marine incident support and attendance
- Insurance liaison

**The precision requirement is highest here.** A P&I club evaluating a correspondent is assessing
exactly where the correspondent's role starts and stops. Vague scope is disqualifying.

### D5 — Credentials and coverage

- Which ports MIDTRANS covers, and what coverage means operationally
- Response capability and escalation structure
- Relevant experience, described without claiming certifications or memberships not held

**No invented credentials.** Per `../standards/WRITING-STANDARDS.md` §2, memberships,
appointments and certifications are stated only if held and verifiable.

### D6 — Enquiry path for this audience

This audience does not fill in an RFQ wizard. They need:

- Direct contact for a named responsible person
- A clearly published emergency or incident contact route, with an honest statement of
  availability — **do not publish a response time operations has not committed to**
- A short enquiry form appropriate to the professional context

### D7 — MIRA integration

MIRA recognises maritime and P&I intent (Phase 02 / D5 trigger list) and routes to the maritime
contact path, not the freight RFQ.

**Guardrail note:** MIRA must never engage substantively on claim, liability, incident, or
coverage language.

> **⚠️ Correction, 2026-09-16.** This previously read "this is **already** an immediate-escalation
> trigger". It was not. §6 listed seven triggers and **none of them existed in code** — tested
> against §6's own examples, every one passed through. A shipowner opening a conversation about
> damage and a claim, the exact conversation this phase exists to prevent, would have been
> answered by MIRA on its own.
>
> Now implemented in `../../mira/escalation.py`, checked **before the model is called**, with 25
> must-escalate and 12 must-continue cases. See `PHASE-06-BOUNDARY-AND-ESCALATION.md`.

---

## Technical requirements

- Hub and cluster structure; breadcrumbs; no orphans
- `Service`, `Article`, `BreadcrumbList`, `LocalBusiness` where accurate
- Incident contact route works and is monitored — a published emergency contact that does not
  answer is worse than none
- Mobile CWV pass
- Level 1 and Level 2 per `../standards/DEFINITION-OF-DONE.md`

## SEO requirements

- Every page passes the uniqueness test
- Precise maritime terminology used consistently as entity names
- Cross-linked with Phase 04 port content in both directions
- Low search volume expected and accepted — this cluster is judged on enquiry quality, not
  traffic

## CRO requirements

- Maritime and P&I enquiries tracked separately from freight enquiries
- Enquiry source tracked by cluster page
- Measured on **qualified enquiries from the target audience**, not volume

## Language scope

**T4 — English only.**

International maritime and P&I operate in English as the working language. Adding six
translations here would be pure cost against an audience that reads English professionally.

## Capacity estimate

| Work | Estimate |
|---|---|
| Content: 15–25 pages, EN | 3 weeks |
| Maritime terminology and factual review | 1 week |
| Technical implementation, schema, linking | 1 week |
| Contact routing, MIRA integration, QA | 1 week |

Requires a writer with genuine maritime domain knowledge, or close collaboration with someone who
has it. **A general content writer will not clear the credibility bar in this sector** — this is
the most common failure mode for maritime content.

---

## Risks and rollback

| Risk | Mitigation |
|---|---|
| **Imprecise terminology destroys credibility** | Mandatory terminology review by someone with maritime operational background |
| A page implies liability assessment or coverage interpretation | Explicit boundary statement on every P&I page; legal-sensitivity review before publish |
| Claimed credentials or appointments not held | Verification required before publish; no exceptions |
| Published emergency contact goes unanswered | Confirm monitoring and escalation with operations before publishing any incident route |
| Content written generically by a non-specialist | Domain-competent writer required; terminology review is a gate, not a courtesy |
| Low traffic read as phase failure | Gate is enquiry quality, not volume — agreed explicitly at phase start |
| MIRA engages on a claim or liability question | Escalation triggers **now implemented** (`mira/escalation.py`) and checked before the model is called. They did not exist until 2026-09-16 — see `PHASE-06-BOUNDARY-AND-ESCALATION.md` §1 |
| An escalation is raised and nobody receives it | `on_escalation` wired to a route that reaches a named person, tested end to end. The customer has been told a human is coming |

**Rollback:** additive content, unpublishable per page with a 301 to the hub. The incident contact
route is separately disableable if monitoring cannot be sustained — and should be disabled rather
than left unanswered.

---

## Validation

- [ ] Maritime terminology reviewed by someone with operational background, and signed off
- [ ] Every P&I page carries an explicit coordination-versus-determination boundary statement
- [ ] No liability opinion, claim assessment, or coverage interpretation anywhere
- [ ] Every stated credential, membership or appointment verified as held
- [ ] Emergency and incident contact route tested and confirmed monitored
- [ ] No response-time promise that operations has not committed to
- [ ] MIRA escalation on claim and incident language verified in production configuration
- [ ] `check_page.py` clean across the maritime cluster — it blocks liability, coverage and
      claim-outcome phrasings, and blocks a P&I page carrying no boundary statement
- [ ] Per-trigger firing rates measured against the D0 conversation export before any tuning
- [ ] Cross-linking with Phase 04 port content complete
- [ ] Every page passes the uniqueness test
- [ ] Level 1 and Level 2 checklists passed

## Exit gate

> **Maritime and P&I hubs live, credibility-reviewed, and producing qualified enquiries from the
> target audience — shipowners, operators, surveyors, P&I clubs, or marine insurers.**

Measured on **quality and source of enquiry, not volume**. A small number of enquiries from the
right organisations passes this gate. A large number from freight shippers does not.

Also required: no regression in Phases 01–05 metrics.
