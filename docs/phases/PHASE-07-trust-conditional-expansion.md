# Phase 07 — Trust & Conditional Expansion

**Duration:** continuous
**Prerequisite:** Phase 06 gate passed
**Merges:** original Phases 14–20 and 22–25, plus 17, 18 and 19

---

## نبذة بالعربية

المرحلة المستمرة: بناء الثقة، ثم التوسع **المشروط** — سوق واحد في كل مرة، وكل سوق ببوابة قرار
مبنية على طلب حقيقي وارد، لا على افتراض.

الفرق الجوهري عن الخطة الأصلية: المراحل ١٤–٢٥ كانت مفتوحة ومتوازية. هنا كل سوق لا يُفتح إلا إذا
أثبتت البيانات طلباً فعلياً — بحث عضوي، أو طلبات عروض واردة، أو محادثات ميرا من ذلك السوق.

**الحالات الدراسية: عشر ممتازة، لا خمسون متوسطة.** خمسون حالة سطحية هي خمسون صفحة ضعيفة، وهي
بالضبط ما تتجنّبه هذه الخطة كلها.

هذه المرحلة لا "تنتهي" — تُدار.

---

## Mission

Deepen trust with what MIDTRANS has actually done, then expand into new markets **one at a time,
each gated on evidence of real demand.**

## Why the original phases 14–25 were collapsed into one gated phase

The earlier roadmap listed Europe, China, UAE, industry verticals, case studies, trust expansion,
visual programme, video programme, AI search optimisation, schema expansion, and knowledge graph
as eleven separate phases, all open-ended and all assumed.

They are not eleven projects. They are one continuous operating programme, plus a set of market
expansions that should each be justified individually before any work starts.

Treating them as a queue of guaranteed phases is how a programme commits budget to a German
market presence before checking whether a single German enquiry has ever arrived.

---

## Part A — Trust deepening (continuous, ungated)

### D1 — Case studies: 10 excellent, not 50 adequate

**This is a deliberate reversal of the original target of 50.**

Fifty thin case studies are fifty thin pages that dilute the site and pass no uniqueness test. Ten
substantial ones, each documenting a real engagement, carry more commercial weight than all fifty
would.

Structure per case study:

| Section | Content |
|---|---|
| Challenge | The actual operational or commercial problem |
| Constraints | What made it genuinely difficult |
| Approach | What MIDTRANS did, specifically and in sequence |
| Outcome | What actually happened |

**Rules:**
- Client permission in writing before any identifying detail is published
- Where permission is not granted, anonymise the client but keep the operational specifics — the
  specifics are the value
- **No invented or embellished outcomes.** A case study with a softened or improved result is a
  fabricated reference.
- No performance figures that were not measured
- Prioritise cases relevant to Phases 04–06 clusters: Syria trade, market entry, maritime

### D2 — Trust Center expansion

- Company history and timeline from 1998
- Certifications, memberships and accreditations — **only those actually held and verifiable**
- Network and partnerships, with permission
- Team and expertise, where the individuals consent
- Offices and physical presence

Every claim here must be verifiable. The Trust Center is where an unsupported claim does the most
damage, because it is the page a cautious buyer reads specifically to check.

### D3 — Visual programme

Derived from the original Phases 20 and 21 image audit, re-prioritised to match this programme.

Priority order:
1. Pages that already convert — protect and strengthen them first
2. Phase 04 Syria content — ports, corridors, procedures, documentation
3. Trust Center, Locations, About
4. Tool pages — usage and process visuals
5. Maritime and representation hubs

**Requirements:**
- Authentic MIDTRANS operations imagery wherever possible. Stock imagery of unrelated ports
  actively undermines the credibility the rest of the programme builds.
- Process diagrams where a diagram genuinely explains better than text
- Meaningful alt text — descriptive, not keyword-stuffed
- Optimised: modern formats, responsive sizes, explicit dimensions, lazy-loaded below the fold
- **Mobile performance takes priority over decoration.** Heavy decorative imagery may be dropped
  on mobile.
- No image published that misrepresents MIDTRANS facilities, equipment, or scale

### D4 — Video programme

Started only after the visual programme is complete and the content clusters are stable.

Priority: explainer content for the highest-traffic guides, tool walkthroughs, and procedural
explanations from Phase 04.

`VideoObject` schema; transcripts published (accessibility, and indexable content).

### D5 — AI search and schema (continuous)

Per `../standards/SEO-STANDARDS.md` §§4 and 6, run as an ongoing discipline rather than a phase:

- Schema coverage extended as new content types ship
- Entity naming consistency audited across the site
- Contradictions between pages found and resolved — procedural facts single-sourced
- Periodic check: what do AI assistants say about shipping to Syria, and is MIDTRANS cited
  accurately?
- Content gaps identified from MIRA's unanswered-question log

---

## Part B — Conditional market expansion (gated, one at a time)

### The gate

**No market opens until it passes all four tests:**

| # | Test |
|---|---|
| 1 | **Demand evidence** — organic search demand, inbound RFQs, or MIRA conversations originating from that market |
| 2 | **Operational reality** — MIDTRANS has genuine corridor, partner, or handling capability for that market |
| 3 | **Capacity** — content and translation capacity available without degrading existing clusters |
| 4 | **Owner** — a named person accountable for the market's content and its enquiries |

All four, or the market does not open.

### The queue

Candidate markets, in no fixed order — order is decided by evidence, not by this list:

- Turkey → Syria
- UAE → Syria
- China → Syria
- Germany, France, Netherlands, Sweden → Syria

### The rule

**One market at a time.** A market is opened, built, measured against its own gate, and only then
is the next considered.

Parallel market expansion is how translation debt, half-finished clusters, and unmaintained
content accumulate — and it is precisely the pattern this programme was restructured to avoid.

### Per-market scope

Deliberately small: a market hub, the trade lane content, the practical corridor detail, and
language per `../standards/LANGUAGE-SCOPE.md` T3 — market language + English.

**Not** a replica of the full Syria cluster. The Syria cluster is the depth asset; market pages
route qualified traffic into it.

### Industry verticals

Same gate, same rule. An industry page opens only when MIDTRANS has genuine sector-specific
operational substance — handled cargo types, sector documentation knowledge, real constraints.

Generic industry pages are the same doorway-page risk as generic location pages, and are
prohibited on the same basis.

---

## Ongoing operations (permanent)

| Cadence | Activity |
|---|---|
| Weekly | Metric review against the current focus |
| Monthly | MIRA audit per `../standards/MIRA-GUARDRAILS.md` §7 |
| Quarterly | Content freshness review; pages past `expires_at` re-reviewed or retired |
| Quarterly | Language tier review — promote or demote on data |
| Quarterly | Zero-entrance page review — merge or retire |
| Continuous | Technical SEO monitoring: CWV, indexation, hreflang, redirects, 404s |

### Content retirement

A page with zero organic entrances and zero assisted conversions after two quarterly reviews is
merged into a stronger parent or retired with a 301.

**Retirement requires explicit approval** and is never automatic. But a site that only ever grows
accumulates maintenance debt until the good content is buried in it.

---

## Language scope

Per `../standards/LANGUAGE-SCOPE.md`. Market content is **T3** — market language plus English.
Case studies start at **T4** and are promoted on demand.

## Capacity estimate

Continuous. Each market expansion is scoped and estimated individually at its gate, against
available capacity at that time — not against a figure written in advance in this document.

---

## Risks and rollback

| Risk | Mitigation |
|---|---|
| **Market gates bypassed under commercial pressure** | Four-test gate; decision recorded in writing by the programme owner |
| Case studies embellished or invented | Written client permission; no unmeasured figures; factual review |
| Stock imagery undermines credibility | Authentic operations imagery required wherever possible |
| Visual programme degrades mobile performance | Performance budget enforced; decorative imagery dropped on mobile |
| Parallel market expansion resumes informally | One-market-at-a-time rule; owner named per market |
| Content decays across an expanding site | Quarterly freshness review; expiry dates; retirement process |
| Unverifiable Trust Center claims | Verification required per claim before publish |
| Generic industry pages introduced | Same gate and same uniqueness test as location pages |

**Rollback:** every element is additive and independently reversible. A market that fails its own
gate after launch is unpublished with 301s to the relevant Syria cluster pages, not left to decay.

---

## Validation

Per item, continuously:

- [ ] Case studies: written client permission held; no unmeasured or embellished figures
- [ ] Trust Center: every claim verified
- [ ] Images: authentic, optimised, meaningful alt text, no misrepresentation
- [ ] Mobile performance budget held after every visual addition
- [ ] Market expansions: all four gate tests documented as passed before work started
- [ ] No market opened while another is still in progress
- [ ] Quarterly reviews actually run, with written outcomes
- [ ] No contradiction introduced between pages
- [ ] Level 1 and Level 2 checklists passed per item

## Exit gate

This phase does not end. It is **operated**.

Each market expansion has its own gate:

> **Qualified enquiries from the target market, sufficient to justify the content investment —
> assessed against a target agreed before the market opened.**

A market that does not meet its gate is not expanded further, and its content is reviewed for
retirement rather than extended in the hope of improvement.
