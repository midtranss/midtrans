# Milestone

The shipment timeline: what has happened, what is happening, what has not been reached.

Use an ordered list `mt-timeline` of `mt-timeline__step` items, each carrying `data-state` of `done`, `current` or `pending`, and holding `mt-timeline__title` and `mt-timeline__meta`.

**You provide:** the steps in operational order, their states, and the dates.

**Three states, three treatments.** `done` is a filled `status-success` marker with the real date. `current` is a `brand-primary` marker, a bold title, and what is known now. `pending` is a hollow `border-strong` marker with `ink-muted` text — and no date, unless a carrier has published one.

**A pending step never carries an invented date.** Write the condition instead: "Per carrier schedule", "Pending arrival", "On document receipt". An estimated arrival shown as a date is read as a promise; this component is where that mistake would be most costly.

**Steps do not disappear when passed** and their dates are never recomputed. The timeline is the shipment's record, and a customer comparing it to an earlier screenshot must find the same dates.

**The rail runs on the inline-start edge** and is drawn with logical properties, so it moves to the right under `dir="rtl"` with no change. The marker is `radius-pill` — one of the few places that token is used.

**Do not** use this for a marketing "how we work" section — that is a numbered list, not a shipment. Do not collapse completed steps behind a "show more": the whole history is the point.
