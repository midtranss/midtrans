The account statement: the opening position, what moved during the period, and the closing position.

It restates what the account already holds. Payment is requested on an invoice and confirmed by a receipt; a statement does neither.

## What differs from Document

| | |
| --- | --- |
| `mt-doc__kind` and footer | `Account statement` |
| Meta rows | No · **Period** — a statement covers a span, not a date |
| Table columns | Date · Reference · Description · Debit · Credit · Balance |
| Totals | Opening balance · Total debits · Total credits · **Closing balance** as the grand row |
| Side column | Account (with the account number) · QR · terms |
| Terms card | How to read the statement, not payment terms |

## The balance column carries the running position

Each row shows the balance **after** that movement, which is what lets a customer find the line where two records diverged. It is the one column that is not a sum of anything.

An invoice appears on issue, not on payment. A receipt appears on the value date its bank confirmed — which is why a payment made late in the period can land in the next one, and why the terms card says so before anyone telephones about it.

## The closing balance is a relation, not a column

```
closing = opening + debits − credits
```

No column sum can express that, so `tools/audit/doc_totals.py` states it as its own rule and checks it on this document specifically. The other totals are checked against the columns they name.

## Nothing is recomputed after issue

A statement is a position at a moment. Where a figure is disputed, the reference in its row identifies the record, and the correction appears as a later movement — the issued statement keeps its figures. This is the same rule the Document card states for every kind.

## The amounts here are masked

Every figure on this preview is a placeholder. The claims guideline forbids illustrating a price "including in placeholder or demo content", and a balance is arithmetic over invoices, which are arithmetic over rates — so a specimen balance illustrates a rate at one remove. The masking keeps the column alignment visible, which is what a design card needs to show, and carries no number a reader could act on. **A statement's real arithmetic is proved in the accounting system; this component governs the visual layer only.**

## What you provide

The issuing office, the account and its number, the period, every movement with its date, reference, description and amount, the opening balance, and the QR payload — all from the accounting record.
