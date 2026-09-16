# Phase 03 — Tools as a Lead Engine

**Duration:** 4 weeks
**Prerequisite:** Phase 02 gate passed
**Merges:** original Phases 05 and 21

---

## نبذة بالعربية

الأدوات ليست زينة — هي أقوى مغناطيس عملاء لدى MIDTRANS، **لأن من يحسب حمولة حاوية لديه شحنة
فعلية**. هذه أعلى نيّة شرائية يمكن قياسها على الموقع.

الهدف: تحويل كل أداة من "خدمة مجانية" إلى مسار مُقاس ينتهي بطلب عرض سعر مؤهّل.

قاعدة صارمة: الأدوات تحسب أبعاداً وأحجاماً وأوزاناً — **ولا تحسب أسعاراً ولا مدداً ولا رسوماً
جمركية أبداً**. حاسبة تعطي تقديراً سعرياً هي عرض سعر بغطاء هندسي.

ملاحظة: الحالة الفعلية لكل أداة تتحدّد من جرد المرحلة صفر (D4)، لا من الافتراض.

---

## Mission

Turn the MIDTRANS tools into measurable lead generators feeding the Phase 01 funnel.

## Why tools rank this high

Someone calculating container loading has cargo. Someone building a commercial invoice has a
shipment. Someone checking volumetric weight is comparing options right now.

This is the highest-intent traffic on the site, and it arrives self-selected. A tool that is used
a thousand times and produces no enquiry is a measurement failure, not a traffic success.

## Starting point

The build/fix/rebuild decision for each tool comes from **Phase 00 / D4**, not from assumption.
Some tools may already exist and work; some may exist and not work; some may not exist. This
phase acts on the inventory verdicts.

---

## Scope

### In scope

| Tool | Purpose |
|---|---|
| Loading Calculator | Container utilisation — cartons, pallets, units into 20ft / 40ft / 40HC; LCL |
| Container Calculator | Container selection for a given cargo profile |
| CBM Calculator | Volume calculation |
| Volumetric Weight Calculator | Chargeable weight basis for air and express |
| Commercial Invoice Builder | Export documentation generation |
| Shipment Tracker | Status visibility |

Plus, for each: landing page, user guide, FAQ, MIRA integration, and a measured conversion path.

### Out of scope — permanently

**No tool produces a price, a rate, a transit time, a customs cost, a duty figure, or an
acceptance decision.**

This is enforced by a test, not only by intention: `tools/calc/tests/test_freight_math.py` runs
every string the calculation core can emit through the MIRA guardrail check in
`../../mira/guardrails.py`. The tools and the assistant are held to one standard, because the
customer does not distinguish between them.

The tools calculate physical and documentary facts: volume, weight, fit, utilisation, document
completeness. A "rate estimator" is a quote wearing an engineering costume, and it is prohibited
under `../standards/WRITING-STANDARDS.md` §4.

---

## Deliverables

### D1 — Tool functionality

**The calculation layer is specified and built: `PHASE-03-TOOL-CALCULATION-SPEC.md`, implemented
in `../../tools/calc/freight_math.py`.** Every UI calculator calls it rather than re-deriving the
arithmetic, so the boundary in §"Out of scope" is enforced in one place and tested there.

Three properties of that layer decide whether this phase's hard constraint actually holds:
the volumetric divisor is a required argument with no default; container feasibility returns
`EXCEEDS` / `REVIEW` / `LIKELY_FITS` and never "fits"; and every reference capacity is
`unconfirmed` until a named person at operations signs it off.

Per the Phase 00 verdicts. For each tool, whether built or fixed:

- Correct calculation, verified against worked examples reviewed by MIDTRANS operations
  (§7 of the spec defines what operations must supply, and why the suite cannot substitute for it)
- Mobile-first — these are used on phones, in warehouses and offices
- Clear, exportable output the user can act on or send onward
- Sensible input validation with useful error messages
- No registration wall. A tool behind a signup converts nothing.

### D2 — Conversion path per tool

Every tool ends with a contextual next step, not a generic CTA:

| Tool | Contextual next step |
|---|---|
| Loading Calculator | "Ready to move this? Send the plan to our team for a quote." — result pre-loads the RFQ wizard |
| Container Calculator | Same, with the recommended container type carried into the enquiry |
| CBM / Volumetric | Carry the computed figures into the RFQ |
| Invoice Builder | Offer document review and customs support |
| Shipment Tracker | Offer support on the tracked shipment; offer a quote for the next one |

**The mechanism that matters:** the tool result pre-populates the RFQ wizard. The user has already
done the work; do not make them do it twice.

### D3 — Content around each tool

For each tool, three pieces (per `../standards/SEO-STANDARDS.md`):

1. **Landing page** — what it does, who it is for, why it matters commercially
2. **User guide** — how to use it well, including the mistakes that produce wrong answers
3. **FAQ** — real questions, sourced from Phase 00 / D3 and MIRA transcripts

The guide is where MIDTRANS expertise shows. "How to measure cargo for accurate container
planning, and the four measurement errors that cause cargo to be rejected at loading" is a page a
competitor cannot copy. "How to use our calculator" is not.

### D4 — MIRA integration

- MIRA suggests the relevant tool when context warrants (per Phase 02 / D5)
- MIRA can explain how to use a tool and interpret its output
- MIRA can carry a tool result into a qualified enquiry
- MIRA never states what a tool would compute without the tool having computed it

### D5 — Measurement

Per tool: entrances, completions, completion rate, result → RFQ progression, qualified leads
produced, and mobile vs. desktop split.

**A tool with high usage and zero RFQ progression has a broken conversion path.** That is the
signal this deliverable exists to surface.

---

## Technical requirements

- Client-side calculation where possible — fast, works offline, no server round trip
- Mobile-first; verified on real devices at 360px
- Accessible: keyboard operable, labelled inputs, results announced to screen readers
- Results shareable via URL, and exportable (PDF or image) where meaningful
- Calculation logic unit-tested against operations-reviewed worked examples
- Invoice Builder: generated documents must not be stored server-side beyond the session unless a
  retention policy explicitly covers it
- Shipment Tracker: integration credentials never exposed client-side; rate limiting in place
- No CWV regression from tool JavaScript on the landing pages

## SEO requirements

- Each tool landing page targets its genuine topic cluster
- `SoftwareApplication` or `WebApplication` schema where accurate; `FAQPage` on real FAQs only
- Tool result URLs are `noindex` — they are user-specific, not content
- Internal links: landing ↔ guide ↔ FAQ ↔ relevant service pages, both directions
- Guides are genuinely useful standalone content, not thin wrappers around a link

## CRO requirements

- Tool result → RFQ progression is the primary tool metric
- Per-step abandonment tracked inside multi-step tools (notably the Invoice Builder)
- Pre-population verified to actually reduce RFQ abandonment, not just to exist

## Language scope

- Tool interfaces and landing pages: **T1** (all seven)
- Guides and FAQs: **T2** (EN + AR)

Rationale in `../standards/LANGUAGE-SCOPE.md`: the tool must be usable by anyone; the depth
content is read by the operating audience.

## Capacity estimate

| Work | Estimate |
|---|---|
| Tool build / fix (depends heavily on Phase 00 verdicts) | 2 weeks |
| Conversion paths + RFQ pre-population | 0.5 week |
| Content: 6 landing pages, 6 guides, 6 FAQs (EN + AR) | 1 week |
| MIRA integration, measurement, QA | 0.5 week |

**Widest uncertainty band in the programme.** If Phase 00 finds most tools need rebuilding rather
than fixing, this extends to 6–7 weeks.

---

## Risks and rollback

| Risk | Mitigation |
|---|---|
| A tool computes incorrectly and a customer acts on it | Unit tests against operations-reviewed worked examples; visible scope statement on each tool |
| A tool is read as giving a commercial commitment | Explicit, visible scope statement: what it calculates and what it does not |
| Pressure to add a "rate estimate" feature | Prohibited. Escalate to programme owner; the answer is no. |
| High usage, zero leads | Per-tool progression measurement makes this visible within days, not quarters |
| Tracker integration fails or exposes credentials | Server-side proxy; rate limiting; graceful failure with a contact route |
| Invoice Builder retains customer commercial data | Session-only by default; retention requires explicit policy and approval |
| Tool JavaScript degrades mobile CWV | Budget set and measured before launch |

**Rollback:** each tool is independently feature-flagged. Disabling one leaves the others and the
site unaffected. Existing tools are not removed until the replacement is proven.

---

## Validation

- [ ] Calculations verified against operations-reviewed worked examples
- [ ] No price, rate, transit time, duty, or acceptance output anywhere in any tool
- [ ] `PHASE-03-TOOL-CALCULATION-SPEC.md` §9 checklist passed — in particular
      `unconfirmed_rows()` empty, and `LIKELY_FITS` never rendered as "Fits"
- [ ] Every tool tested on real mobile devices
- [ ] Accessibility audit passed per tool
- [ ] RFQ pre-population verified end to end
- [ ] Conversion events verified firing in the analytics tool
- [ ] MIRA integration tested, including the "do not compute without the tool" constraint
- [ ] Arabic interfaces RTL-correct, including numeric input
- [ ] Guides and FAQs pass `../standards/SEO-STANDARDS.md` §2 uniqueness test
- [ ] Level 1 and Level 2 checklists passed

## Exit gate

> **Every live tool shows a measurable conversion path — usage, result, and RFQ progression — and
> the tools collectively produce qualified leads at a rate agreed at phase start.**

**A tool with usage but no progression does not pass.** Fix the path or retire the tool; do not
carry a lead generator that generates no leads into the next phase.
