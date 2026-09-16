# Document

The print-ready commercial document: quotation, invoice, credit note, statement of account.

Compose `mt-doc` → `mt-doc__head` (letterhead and `mt-doc__ident`), `mt-doc__parties`, a `KeyValue` for the shipment terms, an `mt-table` of charge lines, `mt-doc__total`, then `mt-doc__note` blocks.

**You provide:** the document kind and number, the issue and validity dates, both parties, the charge lines, and the totals — all from the accounting record, never computed in the template.

**Every charge line carries its basis.** The `Basis` column ("Per container", "Per kg", "Per CBM", "Per shipment", "Per assessment") is not optional: a figure without its unit basis is not a quotation, and the line does not render without one. Amounts are `mt-table__num`, which sets tabular figures aligned on the digit.

**Currency is named once in the total label and again on each line.** Never show a bare number.

**What is excluded is written, not implied.** The closing note lists excluded charges explicitly — duties, taxes, storage, demurrage, inspection. An excluded line may also appear in the table with "Excluded" in `ink-muted` where the customer is likely to expect it, as import duties do.

**Unconfirmed figures never appear as numbers.** Use the `data-pending` treatment from `KeyValue` — "Confirmed on booking", "Pending customs assessment" — in `ink-muted`, in the position the figure will occupy. Never `0`, `—` or an estimate.

**Expired documents keep their figures.** Mark the header with a `neutral` StatusBadge reading "Expired"; do not blank, grey out or recompute the amounts. The document is a record.

**Print.** The stylesheet drops the border, radius and padding at `@media print`, and outlines the total in `border-strong` instead of filling it, so it survives a mono printer. Print with the real letterhead: `midtrans-logo-blue.png` as `mt-doc__logo`.

**Arabic.** `mt-doc__ident` is aligned with `text-align: end`, so it moves to the left edge under `dir="rtl"` without a change. Amounts and document numbers stay in Western digits in every locale.
