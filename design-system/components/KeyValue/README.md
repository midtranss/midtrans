# KeyValue

Presents the fields of one record — a shipment, a quotation, an account — as term and value pairs.

Use a real `<dl class="mt-kv">` with `<dt>` terms and `<dd>` values. Add `data-mono` to any value that is a reference number or a figure, and `data-pending` to a value that is not yet confirmed.

**You provide:** the field order, the labels per locale, and the values already formatted for the locale — except reference numbers, which are reproduced exactly as issued, in Western digits, in every locale.

Order fields as the operator reads them off the document: identifiers, route, commercial terms, cargo, then figures. Keep it to what fits on one screen; anything longer is a Card per group.

`data-pending` is how an unknown figure is shown: the state word in `ink-muted` at `body-sm`, in the position the value will occupy, so nothing shifts when the real figure arrives. Never put `0`, `—`, `TBD` or an estimate there.

Below 600px the grid becomes a single column with the term above its value. The terms use the `label` style and are uppercased by the stylesheet, so pass them in sentence case.

**Do not** build this from `<div>`s — the `<dl>` association is what lets a screen reader pair a value with its term. Do not put interactive controls inside a `<dd>`; actions belong in the surrounding Card's footer.
