# Phase 03 — Tool Calculation Specification

**Status:** reference implementation built and tested · **Governs:** Phase 03 / D1
**Reference implementation:** `../../tools/calc/freight_math.py`
**Reference data:** `../../tools/calc/equipment.json`
**Binds:** `../standards/WRITING-STANDARDS.md` §4, `../standards/MIRA-GUARDRAILS.md` §2

---

## نبذة بالعربية

هذا الملف يحدّد بدقّة **ما تحسبه كل أداة وما لا تحسبه**، ويأتي معه تنفيذ مرجعي مُختبَر
(`tools/calc/freight_math.py`) تُبنى عليه الأدوات بدل إعادة اشتقاق الحساب في كل واجهة.

ثلاثة قرارات تصميم تحمل معظم الأمان:

**١. معامل الوزن الحجمي مطلوب إجبارياً، بلا قيمة افتراضية.** الرقم ٦٠٠٠ للجوّ و٥٠٠٠ للبريد السريع
عُرف تجاري يختلف بين ناقل وآخر وبين حساب وآخر — لا قانون فيزيائي. القيمة الافتراضية رقم لم يخترْه
أحد، ثم يُورَّث بصمت إلى كل عرض سعر.

**٢. الحاسبة لا تقول «تتّسع» أبداً.** الاتّساع الحجمي ليس قابلية تستيف: شكل البضاعة، والتستيف فوق
بعضها، وقاعدة الطبلية، وفتحة الباب — كلّها تقرّر الجواب الحقيقي. حاسبة تقول «تتّسع» تكون قد أعطت
التزاماً تشغيلياً باسم MIDTRANS. المخرجات ثلاثة: **تتجاوز** / **تحتاج مراجعة** / **الأرجح أنها
تتّسع** — والأخيرة تعني «أرسلها للفريق» لا «مضمونة».

**٣. بيانات الحاويات غير مؤكَّدة حتى يوقّع عليها أحد بالاسم.** الأرقام المنشورة تختلف بين
المصنّعين والملّاك والناقلين. كل نتيجة تحمل `data_status: unconfirmed`، والأداة **لا تُنشر** بهذه
الحالة.

---

## 1. The boundary, stated once

The tools compute **physical and documentary facts**: volume, weight, chargeable basis,
dimensional feasibility, document completeness.

They do not compute, estimate, indicate, or imply:

`price` · `rate` · `transit time` · `duty` · `customs cost` · `clearance fee` · `acceptance` ·
`space availability` · `booking confirmation`

There is no hedged version of this. "Approximate", "indicative", "typically", "starting from" and
"for guidance only" do not create an exception — they create a quote with a disclaimer, which is
still a quote. A rate estimator is a quote wearing an engineering costume.

**This boundary is enforced by a test.** `tools/calc/tests/test_freight_math.py` runs every string
the calculation core can emit — verdicts, reasons, error messages — through the MIRA guardrail
check from `../../mira/guardrails.py`. The tools and the assistant are held to one standard,
because the customer does not distinguish between them.

Any new calculator added to this module inherits that test automatically. Adding one that emits a
figure in a cost context will fail the suite.

---

## 2. What each function computes

All implemented in `tools/calc/freight_math.py`, all pure, no network, no dependencies.

| Function | Computes | Notes |
|---|---|---|
| `cbm(l, w, h, qty)` | Volume in m³ from centimetres | The base of everything downstream |
| `volumetric_weight(l, w, h, divisor, qty)` | Volumetric weight in kg | **Divisor is required** — see §3 |
| `chargeable_weight(gross, volumetric)` | The higher of the two, **and which** | The basis is the part that changes a decision |
| `consignment_totals(lines)` | Pieces, total CBM, total gross, heaviest piece, longest dimension, density | Rolls up mixed cargo |
| `container_feasibility(totals, container, usable_fraction)` | `EXCEEDS` / `REVIEW` / `LIKELY_FITS` with reasons | **Never "fits"** — see §4 |

### Why `chargeable_weight` returns the basis, not just a number

Light, bulky cargo charged on volume rather than weight is the most common surprise in air
freight, and the customer who understands *why* stops arguing and starts packing better. A tool
that reports `166.67 kg` teaches nothing. A tool that reports `166.67 kg, charged on volume
because the cargo is light for its size` is the expertise `PHASE-03` §D3 says the guides should
carry — delivered at the moment it is useful.

### Why `consignment_totals` reports the extremes

The heaviest single piece and the longest single dimension are returned alongside the totals
because **they, not the totals, are what make a consignment awkward.** Cargo that fits by volume
and fails at the door is a real and expensive outcome, and a calculator that reports only totals
cannot see it coming.

---

## 3. The volumetric divisor has no default, deliberately

```python
volumetric_weight(120, 80, 100, divisor_cm3_per_kg=6000, quantity=4)
```

Calling it without a divisor raises `TypeError`. That is the design, and it is tested.

A divisor is a **commercial convention**, not physics. 6000 cm³/kg is the widespread IATA air
convention and 5000 the common courier one, but both differ by carrier, by mode, and by
negotiated account. A default value is a number nobody at MIDTRANS chose, inherited silently into
every calculation a customer sees.

`equipment.json` records both conventions with a `source` and `status: unconfirmed`. They are the
starting point for a conversation with operations, not an answer. `divisor("sea")` raises rather
than guessing — because there is no sea equivalent, and a tool that invents one is worse than a
tool that says it does not know.

**Before any air or express calculator goes live:** operations confirms the divisor each partner
actually applies, sets `confirmed_by` and `confirmed_at`, and changes `status` to `confirmed`.

---

## 4. Feasibility, not fit

`container_feasibility()` returns one of three verdicts. None of them is "yes".

| Verdict | Meaning | What the UI must say |
|---|---|---|
| `EXCEEDS` | Over usable volume, over payload, or a piece too large for the interior | Clear: this will not go in one of these |
| `REVIEW` | Inside capacity, but stowage decides — above 90% utilisation, or a piece wider than the door | "Our team needs to look at this" |
| `LIKELY_FITS` | Comfortable margin on every check | "The numbers leave room. Send it to our team to confirm." |

**`LIKELY_FITS` is not a promise and the interface must never present it as one.** Displaying it
as a green tick with the word "Fits" converts a calculation into an operational commitment, which
is prohibited by `../standards/WRITING-STANDARDS.md` §4 and is exactly the risk `PHASE-03`'s
register names.

### Usable volume, not nominal

The default `usable_fraction` is **0.80**. Cartons do not tessellate, pallets waste the space
above them, and stacking limits apply. Computing against nominal volume is the single most common
error in public container calculators, and it produces a confident wrong answer: the customer is
told 67 m³ of cargo goes into a 40ft, ships it, and discovers otherwise at the warehouse.

The fraction is a parameter, not a constant, so operations can set what MIDTRANS's own loading
experience supports rather than inheriting a guess.

### The door check

A piece can be inside the container's interior dimensions and still not go through the door. The
function checks the longest dimension against the door aperture and returns `REVIEW` with an
explanation, rather than silently passing it.

---

## 5. Reference data: unconfirmed until someone owns it

`equipment.json` carries three containers and two divisors. **Every row is
`status: unconfirmed`**, with `confirmed_by: null` and `confirmed_at: null`, and this is asserted
by a test — so nobody can quietly flip a row without the ritual that the field names imply.

The figures are nominal ISO / carrier-published values. They differ between builds, owners and
carriers. A calculator that tells a customer their cargo fits, using a capacity nobody checked,
has made an operational claim on numbers it does not own.

Every `Feasibility` result therefore carries `data_status`, and while it reads `unconfirmed` the
reasons list says so in plain words.

### Closing the loop

For each row, operations:

1. Checks the figure against the equipment MIDTRANS actually books on its lanes
2. Corrects it where it differs
3. Sets `confirmed_by` to **a person's name** — not "operations", not a team
4. Sets `confirmed_at` to the date
5. Sets `status: confirmed`

```bash
python3 -c "import sys; sys.path.insert(0,'tools/calc'); import freight_math as f; print(f.unconfirmed_rows())"
```

The tool does not go live while that list is non-empty. This mirrors the knowledge-base rule in
`../../mira/knowledge/README.md`: **a fact without a named owner is not a fact MIDTRANS stands
behind.**

---

## 6. Input validation — a refusal beats a plausible wrong answer

Two input errors actually occur in production forms, and both produce numbers that look fine:

- **A unit mix-up** — metres typed into a centimetres field. `1.2` becomes `1.2 cm`, or `5000`
  appears where `500` was meant.
- **A transposed decimal** — `12.0` for `1.20`.

The core rejects any dimension above **2,000 cm** (longer than any standard container) and any
weight above **100,000 kg**, with an error naming the expected unit. It also rejects zero,
negative, non-numeric, `NaN` and infinity.

Every one of these is tested. The principle: **a calculator that refuses is annoying; a calculator
that returns a plausible wrong number costs a shipment.**

The UI must surface these messages rather than swallowing them into a generic "invalid input" —
the message says which field and which unit, and that is what lets the user fix it.

---

## 7. Worked examples — the operations review

`PHASE-03` requires calculations "verified against worked examples reviewed by MIDTRANS
operations". The suite contains the arithmetic cases. What it cannot contain is MIDTRANS's
judgement.

Before the tools go live, operations supplies **at least five real consignments** already shipped,
with the actual outcome:

| Field | Why |
|---|---|
| The cargo lines as the customer originally described them | Including the vagueness |
| What was actually loaded, and into what | The ground truth |
| Whether it went in one container or needed another | The feasibility check's real test |
| Anything that went wrong at loading | The cases the arithmetic cannot see |

Each becomes a test case. Where the reference implementation disagrees with what happened, **the
implementation is wrong** — the parameters, most likely `usable_fraction`, need setting from
experience rather than from a default.

This is the step that converts a correct calculator into a MIDTRANS calculator, and it is the one
most likely to be skipped under schedule pressure.

---

## 8. Running it

```bash
python3 tools/calc/tests/test_freight_math.py
```

Standard library only. No API key, no network, no build step. The prohibition cross-check imports
`mira/guardrails.py`; if that import fails, the suite fails rather than skipping — a silently
skipped safety test is not a safety test.

---

## 9. Definition of done — for the calculation layer

- [ ] Every UI calculator calls `freight_math.py` rather than re-deriving the arithmetic
- [ ] No calculator emits, displays, or links to a price, rate, transit time, duty or acceptance
- [ ] `LIKELY_FITS` is never rendered as "Fits" or a bare green tick
- [ ] Every result displaying container capacity shows its `data_status` while unconfirmed
- [ ] `unconfirmed_rows()` returns empty — every row confirmed by a **named** person
- [ ] `usable_fraction` set from MIDTRANS loading experience, not left at the default
- [ ] Volumetric divisors confirmed per partner and mode; no default anywhere in the UI layer
- [ ] At least five operations-supplied real consignments added as test cases, and passing
- [ ] Validation messages surfaced to the user, naming the field and the unit
- [ ] Arabic interface: numeric input accepts Arabic-Indic digits and renders RTL correctly
- [ ] Level 1 and Level 2 checklists in `../standards/DEFINITION-OF-DONE.md` passed
