# StatusBadge

Names the state of a shipment, quotation, invoice or document, as a word and a colour together.

Use `mt-badge` with one of `mt-badge--neutral`, `--info`, `--warning`, `--success` or `--danger`, and always include the `mt-badge__dot` span and a text label.

**You provide:** the state word, in sentence case, translated per locale.

Map states by what the operator must do, not by sentiment:

| Variant | Means | Shipment | Quotation / invoice |
| --- | --- | --- | --- |
| `--neutral` | Nothing is running | Draft, Archived | Draft, Expired |
| `--info` | Running, nothing owed | Booked, In transit | Sent |
| `--warning` | Waiting on someone | Awaiting documents, Customs hold | Payment due |
| `--success` | Closed as intended | Delivered, Cleared | Paid |
| `--danger` | Closed unintentionally | Cancelled, Failed | Rejected, Overdue |

**The word is never optional.** `status-success` and `status-danger` are told apart by their labels, which is what keeps the set readable for a colour-blind operator; a bare dot or a colour-only cell is not a status. The dot inherits the badge's text colour, so it is decoration, not information.

Keep one badge per record per column. A shipment that is both in transit and awaiting documents shows the state that blocks progress — the warning.

**Do not** invent variants for new states, and do not use a badge as a button; if the state is changeable, put a Button beside it.
