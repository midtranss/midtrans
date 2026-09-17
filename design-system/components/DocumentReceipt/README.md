The payment receipt: the same template as Document, confirming what was received. It never asks for anything.

## What differs from Document

| | |
| --- | --- |
| `mt-doc__kind` and footer | `Payment receipt` |
| Meta rows | No · **Invoice** · Date |
| Above the table | An `Alert--success` confirming receipt and stating it is not an invoice |
| Table | Allocated to · Invoice · Amount — what the money was applied against |
| Totals | Invoice total · Balance after this receipt · **Amount received** as the grand row |
| Side column | Received from · QR · method card (instrument, reference, value date) |
| Terms card | Settlement, not payment terms |

## It confirms, it does not demand

The `Alert--success` and the `Settlement` card exist so this document cannot be read as a request for money. Keep both. A receipt that looks like an invoice gets paid twice.

## The grand row is what was received

`Amount received` is the filled row — the fact this document certifies. `Invoice total` and `Balance after this receipt` sit above it as context. When the amount received differs from the invoice, **the balance is not adjusted here**: it carries on the account statement, and the settlement card says so. A receipt is a record of an event, and events are not recomputed.

## Allocation is provisional

Bank transfers clear after the value date and finance allocates against invoices on its own cycle. The settlement card states that allocation is subject to finance review and bank clearing, so the receipt stays true even when the allocation later moves.

## What you provide

The issuing office, the payer, the instrument and its reference, the value date, the invoice the payment is allocated against, the amount, and the QR payload — all from the accounting record. The invoice number in the meta row and in the table must be the same record.
