The proforma invoice: the same template as Document, marked so it cannot be mistaken for a tax invoice or a demand for payment.

A proforma exists so a buyer can open a letter of credit, pre-clear customs, or get an internal approval **before** the shipment is booked. Everything about it that differs from an invoice exists to stop it being treated as one.

## What differs from Document

| | |
| --- | --- |
| `mt-doc__kind` and footer | `Proforma invoice` |
| Meta rows | No · Job No · **Valid** (never "Due" — nothing is due) |
| Totals label | `Proforma total` |
| Above the table | An `Alert--info` stating it is not a tax invoice and not a demand for payment |
| Terms card | Says the figures are indicative and subject to space, final cargo details and operational review |

Everything else — the 6px rule, the letterhead, the 250px side column, the money columns, the single filled grand-total row, the footer label — is unchanged. **Do not rearrange it.**

## The notice is not optional

The `Alert--info` above the table is part of this document, not decoration. A proforma that reads like an invoice gets paid like one, and a payment against a proforma has no invoice to allocate against. Keep the two sentences: what it is not, and what follows it.

## Duties and taxes

Customs duties are assessed on the declaration, not by MIDTRANS, so they are never a figure here. The line renders its condition instead:

```html
<td class="num" data-unset>Assessed on the declaration</td>
```

`data-unset` drops the cell out of the mono/tabular treatment into `ink-muted` prose, so it reads as a condition rather than a number. Never `0`, never an em-dash. The same applies to any charge that is not yet known: "Confirmed on booking".

## What you provide

The issuing office, the consignee, the lines, the validity date, the QR payload and the document number — all from the accounting record. Never invent a rate, a transit time, a customs cost or a capacity commitment: if it is not confirmed operationally, it is a `data-unset` condition.
