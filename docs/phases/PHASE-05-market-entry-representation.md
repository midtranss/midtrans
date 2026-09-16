# Phase 05 — Market Entry & Business Representation

**Duration:** 8–10 weeks
**Prerequisite:** Phase 04 gate passed
**Merges:** original Phases 08, 09 and 13 — with Phase 13 substantially reduced

---

## نبذة بالعربية

محورا دخول السوق السورية والتمثيل التجاري — وهما أعلى قيمة لكل عميل في محفظة MIDTRANS كلها.

الجمهور هنا مختلف جذرياً: شركة دولية تدرس دخول السوق السورية، لا شاحن يبحث عن سعر حاوية. الصفقة
أكبر، ودورة القرار أطول، والمحتوى يجب أن يخاطب مديراً تنفيذياً يقيّم المخاطر — لا مشتري شحن.

**القرار الأهم في هذه المرحلة: حذف صفحات الولايات والمدن الأمريكية** (تكساس، هيوستن، كاليفورنيا،
لوس أنجلوس، نيويورك، نيوجيرسي، فلوريدا، أتلانتا، شيكاغو). السبب: صفحات موقعية متشابهة بلا جوهر
تشغيلي فريد تُقيَّم على **مستوى النطاق كله**، والخطر هو خنق الصفحات العميقة التي بنيناها في
المرحلة الرابعة. المكسب هامشي، والخسارة قد تطال الموقع بأكمله.

البديل: **صفحة أمريكية واحدة قوية جداً** للشركات الأمريكية الداخلة إلى سوريا.

---

## Mission

Build the market-entry and business-representation hubs that serve MIDTRANS's highest-value
client type: an international company evaluating entry into the Syrian market.

## Why this audience is different

A freight buyer wants a rate and a sailing. A company evaluating market entry wants to know
whether the move is viable at all — and is making a decision worth far more than a shipment.

The content must speak to an executive assessing risk, not a shipper comparing quotes. That means
it must be candid about difficulty. Content that oversells the opportunity loses exactly the
serious, well-advised buyer it is meant to attract.

---

## The US location-page decision

**The nine US state and city pages from the original roadmap are removed.**

| | |
|---|---|
| **Proposed** | Texas, Houston, California, Los Angeles, New York, New Jersey, Florida, Atlanta, Chicago |
| **Decision** | Removed |
| **Replaced by** | One strong page: *US companies entering Syria* |

### Reasoning

Templated location pages without unique operational substance are assessed by search engines at
**site level**, not page level. The failure mode is not that the nine pages fail to rank — it is
that a doorway-page pattern can suppress the deep Syria content built in Phase 04, which is the
programme's most valuable asset.

The risk is asymmetric: marginal upside on nine templated pages, material risk to the entire
domain. Stating in a plan that the pages "are not doorway pages" offers no protection; only the
pages' actual content does, and there is no distinct operational reality for MIDTRANS in Atlanta
versus Chicago.

### The reopening condition

US city or state pages may be reconsidered **only** when all three hold:

1. Phase 00 or later data shows genuine search demand at city level for this service
2. MIDTRANS has genuinely city-specific operational substance — a corridor, a partner, a handled
   case, a documented constraint
3. Each page independently passes the uniqueness test in `../standards/SEO-STANDARDS.md` §2

Absent all three, the answer is no.

---

## Scope

### In scope

- Syria market entry hub
- Business and commercial representation hub
- Partner and distributor search services
- Sales representation and tender monitoring
- One US-focused page: US companies entering Syria
- Consultation funnel tuned for this audience

### Out of scope

- US state and city pages (see above)
- Europe, China and UAE market content — deferred to Phase 07, gated per market
- Legal, tax, or regulatory advice
- Any claim about market size, opportunity value, or expected return that is not sourced and
  cited

### Page budget

**20–30 pages.** Depth over spread, as in Phase 04.

---

## Deliverables

### D1 — Syria Market Entry hub

- Market entry services: what MIDTRANS actually does, concretely
- How foreign companies enter the Syrian market — the real sequence
- What to establish before committing: entity questions, local presence, logistics
- Practical constraints a foreign company should plan for
- Market research and assessment services

**Editorial rule:** this content must be candid about difficulty. Entry into any market carries
real constraints. A page that acknowledges them earns the trust of a serious buyer; a page that
presents only upside is dismissed by the exact reader it needs.

**Sourcing rule:** any market-condition or opportunity statement must be sourced and cited, or it
is not published. No invented market sizes, growth figures, or opportunity values.

**Enforced:** `../../tools/content/check_page.py` blocks any market size, valuation or growth
figure without a citation **in the same paragraph**. A cited figure is exempted from the rate rule
and recorded for review — without that exemption this rule and Phase 04's gate contradicted each
other, and D1 was unsatisfiable. See `PHASE-05-CLAIMS-AND-DUPLICATION.md` §2.

### D2 — Business Representation hub

- Business representation — what the service actually covers
- Commercial representation
- Local representation and in-market presence
- Partner search
- Distributor search
- Sales representation
- Tender monitoring

Each page answers the three questions this buyer actually has: **what MIDTRANS does, how the
engagement works, and what the client is responsible for.** Scope clarity is the selling point —
this is a service category where vagueness reads as inexperience.

> **⚠️ This hub carries the same doorway risk as the US pages this phase removed.**
> *Business*, *commercial* and *local* representation are not obviously different services to a
> reader, and a page each is one template with a substituted noun — the pattern this phase
> rejects, wearing a name that does not look like it. Nothing in a per-page review would notice:
> each page has a title, an owner and real sentences.
>
> Before drafting, answer in one sentence per page: **what does a client get here that they do
> not get from the page next to it?** If the answer needs the page's own name to make sense, the
> pages are one page — merge and write once. Then run
> `../../tools/content/check_cluster.py` over the hub.
> See `PHASE-05-CLAIMS-AND-DUPLICATION.md` §3.

### D3 — US companies entering Syria

One page, built properly: what a US company must consider, how the process works, what MIDTRANS
provides, and what the company handles itself.

**Compliance boundary:** this page explains MIDTRANS's logistics and representation services. It
does not make sanctions, export-control, or compliance determinations, and it says so explicitly,
directing the reader to qualified specialist advice.

### D4 — Consultation funnel for this audience

The Phase 01 consultation path, tuned:

- Qualification questions relevant to market entry, not shipment details
- Longer decision cycle acknowledged — a follow-up sequence, not a single touch
- A route to a senior MIDTRANS contact, because this buyer expects one

### D5 — MIRA integration

MIRA recognises representation and market-entry intent (Phase 02 / D5 trigger list) and routes to
the consultation funnel rather than the RFQ wizard — different intent, different path.

Knowledge-base entries added per `../standards/MIRA-GUARDRAILS.md` §5.

---

## Technical requirements

- Hub, pillar, cluster structure; breadcrumbs; no orphans
- `Service`, `Article`, `FAQPage`, `BreadcrumbList` schema, translated per language tier
- Consultation booking integrated with a real calendar and confirmed to reach a person
- Mobile CWV pass
- All per `../standards/DEFINITION-OF-DONE.md` Level 1 and Level 2

## SEO requirements

- Every page passes the uniqueness test
- No templated location or industry pages
- Answer-first structure; self-contained sections
- Entity consistency across the hub
- Cross-linking to Phase 04 Syria content in both directions — a market-entry reader needs the
  procedural detail, and a procedural reader may be a market-entry buyer

## CRO requirements

- Consultation requests tracked separately from RFQs — different value, different cycle
- Longer attribution window, matching the real decision cycle
- Content-to-consultation progression measured per page

## Language scope

| Content | Tier |
|---|---|
| Market entry hub | **T3** — EN + AR, plus the language of any market actively targeted |
| Representation hub | **T3** — same basis |
| US companies entering Syria | **T4** — EN only |

## Capacity estimate

| Work | Estimate |
|---|---|
| Content: 20–30 pages, EN | 4–5 weeks |
| Localisation and review | 2 weeks |
| Consultation funnel tuning | 1 week |
| Technical implementation, schema, linking | 1 week |
| MIRA integration, QA | 0.5 week |

This content requires commercial and market judgement, not only logistics knowledge. Expect
review cycles with MIDTRANS senior management, and schedule for them.

---

## Risks and rollback

| Risk | Mitigation |
|---|---|
| **Pressure to reinstate US city pages** | Reopening condition documented above; decision sits with the programme owner, on evidence |
| Overselling the opportunity | Candour requirement; senior management editorial review |
| Unsourced market claims | Sourcing rule: cited or not published, **blocked mechanically** by `check_page.py` |
| **Representation pages become a template of each other** | `check_cluster.py` over the hub, and the differentiation question answered before drafting. The risk the removed US pages made obvious, in a form that does not look like it |
| Straying into legal, tax or compliance advice | Explicit boundary statement on relevant pages; route to specialists |
| Consultation requests with no capacity to service them | Confirm senior availability with management before launch |
| Content thin because the service is not yet fully defined | Define the service scope first. Do not publish a page describing a service MIDTRANS cannot yet deliver consistently. |
| Long sales cycle makes the gate hard to read | Longer measurement window agreed at phase start |

**Rollback:** additive content; individual pages unpublishable with a 301 to the parent hub.
Consultation funnel changes are feature-flagged and revert to the Phase 01 configuration.

---

## Validation

- [ ] Every page passes the uniqueness test, recorded
- [ ] No templated location or industry page published
- [ ] `check_cluster.py` clean across the representation hub and the market-entry hub
- [ ] Every market claim sourced and cited, **and every cited source followed by a named reviewer**
- [ ] No legal, tax, sanctions or compliance determination
- [ ] Service scope statements reviewed and confirmed deliverable by operations
- [ ] Consultation booking tested end to end; confirmed reaching a real person
- [ ] Cross-linking with Phase 04 content complete in both directions
- [ ] Schema validated and translated
- [ ] Language tiers correctly applied; hreflang reciprocal
- [ ] Level 1 and Level 2 checklists passed

## Exit gate

> **Market entry and representation hubs live, and producing qualified consultation requests from
> the target audience at a rate agreed at phase start.**

Also required:
- No regression in Phases 01–04 metrics — in particular, no ranking loss on the Phase 04 Syria
  cluster, which would indicate a content-quality problem introduced here
- Senior MIDTRANS capacity confirmed available to service the enquiries generated
