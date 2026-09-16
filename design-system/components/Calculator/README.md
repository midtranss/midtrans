# Calculator

Inputs beside a live readout: the loading calculator, volumetric and chargeable weight, container fill.

Compose `mt-calc` → `mt-calc__inputs` (Fields, paired in `mt-calc__row`) and `mt-calc__out` (a stack of `mt-calc__figure` blocks and an optional `mt-calc__meter`). It collapses to one column below 900px, readout last.

**You provide:** the fields, the arithmetic, and the formatted figures. The component formats nothing.

**Add `data-mono` to every dimension and quantity input** so digits are checkable against a packing list.

**Every figure states its unit and how it was derived.** `mt-calc__figure-sub` carries the working — "18 × 1.392 CBM" — so an operator can verify the result instead of trusting it.

**The meter shows fill against a named equipment type**, never a bare percentage. Past 100% add `mt-calc__meter--over` to the meter: the fill turns `status-danger` and the text goes bold — because over-capacity is a decision, not a warning to be missed. The wording carries the meaning too: "108% of a 40HC by volume — exceeds one container".

**Geometry is calculable; commerce is not.** Volume, volumetric weight, chargeable weight against a declared rate basis, and container fill are arithmetic and may be shown. **Freight cost, duties, transit time, customs charges and space availability are never computed or estimated here** — they render with `data-pending` as "Quoted after review" or "Confirmed on booking". A calculator that returns a price the operations team has not confirmed creates a commitment MIDTRANS did not make.

**Do not** put a "Get instant price" call to action on this component, and do not show a result before the required inputs are valid — show the field error instead.
