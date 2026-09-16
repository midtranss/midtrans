# Phase 01 / D1 — RFQ Wizard Specification

**Status:** ready to implement · **Derived from:** `../baseline/D3-rfq-analysis.md`
**Governed by:** `../standards/WRITING-STANDARDS.md` §4, `../standards/DEFINITION-OF-DONE.md` L2

---

## نبذة بالعربية

مواصفة الـ RFQ Wizard كاملة وجاهزة للتنفيذ.

**كل حقل هنا يعود إلى سطر في جدول «المعلومات الناقصة» في D3** — أي إلى جولة بريد اضطر فريقك فعلاً
لإجرائها. لا حقل مبني على تخمين، ولا حقل «لأننا قد نحتاجه».

أربعة قرارات تصميم تفرضها البيانات:
١. فرع بضائع خطرة شرطي — استفسارات الكيماويات متكرّرة
٢. شرح Incoterms داخل النموذج — المستورد لأول مرة لا يعرف EXW
٣. منع «General cargo» كإجابة — السبب الأول لعودة الناقل بالاستفسار
٤. «لا أعرف بعد» إجابة صالحة — إجبار رقم يُنتج رقماً خاطئاً أو نموذجاً مهجوراً

---

## 0. Correction — this replaces a live page (2026-09-16)

This spec was first written as a new build. Repository evidence says otherwise:
`config/protected-pages.json` on `midtranss/midtrans` lists **`/get-quote/`** among
the pages that must not be lost, so a quote page is already live and ranking.
See `../baseline/D1-technical-audit.md` § repository findings.

Three consequences, all binding:

1. **Measure before touching.** Record the current `/get-quote/` sessions, submissions
   and submission rate for a full 28 days first. Without that number there is no way to
   prove the wizard helped, and Phase 01's exit gate is a comparison.
2. **Keep the URL.** The new wizard ships *at* `/get-quote/`. No new slug, no redirect
   chain, no `/request-a-quote/`. The page's existing authority is an asset.
3. **Rollback is restoration, not removal.** Keep a byte-exact copy of the current page
   and its server config before deployment. The rollback step is "put the old page back",
   and it must be tested once on staging before launch — not discovered under pressure.

Nothing else in this spec changes. The field set below is still derived from D3.

---

## 1. The rule that governs every field

> **A field exists only if a row in `D3-rfq-analysis.md` §5 shows the pricing desk had to chase it
> by follow-up email.**

Every field below carries its justification. A field without one is a field nobody needed, and it
costs completion rate for nothing.

**Hard constraint:** the wizard must never display, calculate, estimate or imply a rate, transit
time, customs cost, acceptance or capacity — including as a "preliminary indication". Not on any
screen, not in the confirmation, not in a tooltip.

---

## 2. Who this is actually for

From D3 §4, the dominant inbound buyer is **a first-time or small importer moving LCL into
Syria** — not an FCL shipper. The recurring self-description: *"first order"*, *"pilot shipment"*,
*"trial LCL"*, *"100 pairs"*, *"sourcing from Alibaba"*.

This has to shape the wizard, not just sit in a persona document:

| Because the buyer is… | The wizard must… |
|---|---|
| Shipping for the first time | Explain Incoterms in the form, not link away to a glossary |
| Often unsure of volume/weight | Accept "I don't know yet" without dead-ending |
| Comparing 3–5 forwarders at once (D3 §4) | Be fast, and acknowledge instantly |
| Frequently moving chemicals (D3 §4) | Branch to DG questions automatically |
| Writing in Arabic ~27% of the time (D3 §7) | Be fully RTL, natively written |

---

## 3. Flow

Five steps. Contact details last — the commitment ask comes after the user has invested effort.

```
1. Route          →  2. Cargo      →  3. Service     →  4. Timing    →  5. Contact
   origin            what it is       door/port         readiness       name, email
   destination       weight/volume    clearance?        target window   phone/WhatsApp
   mode              packaging        Incoterms                         preferred channel
                     ↓
                  [DG branch if chemical/hazardous]
```

**Progress is shown** ("Step 2 of 5"), and every step is reversible without data loss.

---

## 4. Fields

Legend: **R** required · **O** optional · **C** conditional

### Step 1 — Route

| Field | Type | R/O | Justification (D3 §5) |
|---|---|---|---|
| Origin country | select, searchable | R | Always needed |
| Origin port / city | select + free text | R | "Other city / address" must be an option — seen in live submissions |
| Destination country | select | R | Always needed |
| Destination port / city | select + free text | R | Same |
| Mode | radio: Sea · Air · Road · **Not sure** | R | **High frequency** — many enquiries say only "shipping" |

**"Not sure" is a first-class option on mode.** A first-time importer genuinely does not know
whether their 300kg should fly or sail. Forcing a choice produces a wrong one, and the pricing
desk then quotes the wrong thing.

Pre-fill origin/destination from the page the user came from where possible (a China–Syria trade
lane page pre-fills that lane).

### Step 2 — Cargo

| Field | Type | R/O | Justification |
|---|---|---|---|
| Commodity | free text | **R** | **Very high** — carriers reject "general cargo"; the single most common cause of a clarification round |
| Commodity category | select | R | Drives the DG branch |
| Gross weight | number + unit + **"Not known yet"** | R | Very high |
| Volume (CBM) or dimensions | number + unit + **"Not known yet"** | R | Very high |
| Packaging | select: pallets · cartons · loose · crates · other | R | Medium |
| Number of packages | number | O | Helps LCL pricing |
| Stackable? | yes/no/unknown | O | Affects LCL rating |

#### The "general cargo" block

If the commodity field contains only a generic term — *general cargo, goods, merchandise, various,
بضاعة عامة, بضائع, مواد* — **do not accept it**. Show inline, without blocking the form:

> *Carriers need the actual commodity to quote and to accept the booking — "general cargo" will
> come back to you as a question. What is it, roughly? (e.g. "cotton t-shirts", "PVC pipe
> fittings", "ceramic tiles")*

Match on a maintained list, case-insensitive, both languages. **Soft-block**: the user can proceed
after a second attempt, but the enquiry is flagged `commodity_vague` so the desk knows to ask.

Hard-blocking here would cost more leads than it saves.

#### "Not known yet"

Selecting it on weight or volume is valid and does not block submission. It sets
`weight_unknown` / `volume_unknown` on the enquiry, and the confirmation says the team may come
back with a question.

**Rationale (D3 §4):** the dominant buyer genuinely does not know at enquiry time. Forcing a
number produces a fabricated one — which is worse than a flagged unknown — or an abandoned form.

### Step 2b — Dangerous goods (conditional)

**Triggered when:** commodity category is chemical/industrial, **or** the commodity text matches a
DG term list (acid, chemical, battery, paint, solvent, aerosol, flammable, كيماوي, حمض, بطارية,
دهان, مذيب).

| Field | Type | R/O | Justification |
|---|---|---|---|
| Is this classified as dangerous goods? | yes / no / **not sure** | R | |
| UN number | text | C | Required if "yes" |
| Class / division | select | C | Required if "yes" |
| MSDS upload | file | C | Requested if "yes" or "not sure" |
| Packing group | select | O | |

**This branch is mandatory, not a nice-to-have.** D3 §4 found chemical and DG enquiries recurring
often enough that asking here removes a guaranteed email round trip — and a DG enquiry without an
MSDS cannot be priced at all.

If "not sure": *"No problem — if you can upload the safety data sheet (MSDS) from your supplier,
our team will classify it."* Never tell the user whether their cargo is dangerous.

### Step 3 — Service

| Field | Type | R/O | Justification |
|---|---|---|---|
| Collection | select: **Door pickup** · Port/airport · Not sure | R | High |
| Collection address | text | C | High — required when door pickup; "not just the city" |
| Delivery | select: **Door delivery** · Port/airport · Not sure | R | High |
| Delivery address | text | C | High — required when door delivery |
| Customs clearance needed? | origin / destination / both / neither / not sure | R | Medium |
| Incoterms | select + **inline explainer** | R | **Very high** |

#### Incoterms in the form

A dropdown of EXW / FOB / CIF / DDP / DDU answered by someone who does not know what they mean
produces a wrong answer that silently misprices the enquiry.

Each option carries one plain line, in the user's language:

| Option | Inline text |
|---|---|
| **EXW** | Your supplier hands the goods over at their factory. Everything after that is on you. |
| **FOB** | Your supplier delivers to the origin port and handles export clearance. You take it from there. |
| **CIF** | Your supplier covers freight and insurance to the destination port. You handle import. |
| **DDP** | Delivered to your door, all duties and taxes paid by the seller. |
| **DDU / DAP** | Delivered to your door, but you pay import duties and taxes. |
| **I'm not sure** | We'll work it out with you — pick this and our team will ask. |

**"I'm not sure" must be present.** It is a better outcome than a confidently wrong FOB.

### Step 4 — Timing

| Field | Type | R/O | Justification |
|---|---|---|---|
| Cargo readiness date | date + "as soon as possible" + "not fixed yet" | R | Medium |
| Target arrival window | month/quarter picker | O | Medium |
| Is this a one-off or recurring? | select | O | Recurring flows are higher value and should reach the desk flagged |

**Never state or imply a transit time on this screen** — including a date picker that suggests or
greys out "realistic" arrival dates. A greyed-out calendar is a transit-time statement.

### Step 5 — Contact

| Field | Type | R/O |
|---|---|---|
| Full name | text | R |
| Company | text | O |
| Email | email | R |
| Phone / WhatsApp | tel, with country code | R |
| Preferred channel | Email · WhatsApp · Phone call | R |
| Anything else? | textarea | O |

**Placed last, deliberately.** Steps 1–4 are low-commitment and build investment; asking for
contact details first raises abandonment on exactly the audience least willing to commit.

---

## 5. Partial submissions are leads

**The single highest-value mechanic in this wizard.**

Capture the email as soon as it is entered and valid. If the user then abandons, the enquiry is
**still routed** — marked `partial`, with whatever was completed.

An abandoned wizard with an email is a lead. Discarding it is discarding the marketing spend that
produced the visit.

Implementation: persist on each step transition; a partial older than 30 minutes with a valid
email is forwarded to the desk with a `PARTIAL` marker and the last step reached.

---

## 6. Notification to the pricing desk

Match the format already in production (D3 §8 found it working — structured, sent to a named
distribution list, with management replying on-thread). Do not redesign what works.

Required in the notification:

- Reference number (`QREQ-YYYY-NNNNN`, continuing the existing sequence)
- Every field the user completed, in flow order
- **Flags, prominently:** `DG` · `commodity_vague` · `weight_unknown` · `volume_unknown` ·
  `PARTIAL` · `RECURRING`
- **Source page** the user started from — currently not captured, and D3 §9 names it as a gap that
  blocks attributing Phase 04 content to the enquiries it generates
- Language of submission
- Timestamp and user's timezone if available

---

## 7. Acknowledgement to the customer

The existing acknowledgement was checked against the guardrails in D3 §8 and **is compliant** —
it states the request was received and that the operations team will review it, with no rate,
transit time, cost, acceptance or capacity. Keep it, and keep its shape as the template.

Two additions:

1. **A realistic next step**, without a promised time: *"Our team will review this and come back
   to you."* Never "within 24 hours" unless operations has committed to it and staffs it.
2. **What happens if something is missing:** *"If we need anything else to price this accurately,
   we'll ask."* This makes the `not known yet` path feel deliberate rather than broken.

Send in the language of the submission.

---

## 8. Technical requirements

| Area | Requirement |
|---|---|
| Mobile | Built mobile-first; verified at 360px on real devices |
| Validation | Server-side as well as client-side |
| Persistence | Save on every step transition; resumable via emailed link |
| No-JS | A functional fallback contact route must exist |
| Accessibility | WCAG 2.1 AA — keyboard, labels, focus, error announcement |
| RTL | Full RTL for Arabic including the progress indicator and date picker; Cairo font |
| Spam | Protection that does not block screen readers — no image CAPTCHA |
| Uploads | MSDS: PDF/image, size-capped, virus-scanned, not publicly addressable |
| Reliability | Queue + retry so a backend outage never drops an enquiry |
| Data | Encrypted in transit and at rest; retention policy documented; consent captured for EU visitors |

## 9. Analytics

Per step: entrances, completions, abandonment, time on step, error rate per field.
Plus: partial-capture rate, DG branch trigger rate, `commodity_vague` rate, `not known yet` usage,
and language of submission.

**The per-step abandonment chart is the point.** It identifies which question is costing enquiries,
which is the only way to iterate on this with evidence rather than opinion.

## 10. Language scope

**T1 — all seven languages** (`../standards/LANGUAGE-SCOPE.md`). This is the commercial core; a
broken funnel in any language is a lost market.

Arabic is authored natively, not translated — D3 §7 found ~27% of genuine enquiries arrive in
Arabic, all Syria-route.

## 11. Definition of Done

- [ ] Every field traces to a row in `D3-rfq-analysis.md` §5
- [ ] No rate, transit time, cost, acceptance or capacity anywhere in the flow, including tooltips
      and the date picker
- [ ] `general cargo` soft-block live in both languages
- [ ] "Not known yet" accepted on weight and volume without blocking
- [ ] DG branch triggers on category **and** on commodity text
- [ ] Incoterms explained inline, with "I'm not sure" present
- [ ] Partial submissions captured and routed
- [ ] Source page captured on every submission
- [ ] Notification format verified with the pricing desk before launch
- [ ] Acknowledgement re-checked against `MIRA-GUARDRAILS.md` §2 in every language
- [ ] Tested end to end in all 7 languages, RTL verified on mobile
- [ ] Existing contact routes still live and untouched
- [ ] Rollback verified by exercising the feature flag
