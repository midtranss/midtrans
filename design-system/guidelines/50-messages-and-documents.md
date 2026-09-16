# Messages and documents

Everything MIDTRANS sends or prints — email, notifications, quotations, invoices, receipts, statements, reports — is one family. Same tokens, same voice, same rules about figures. These are the rules that differ from a screen.

## The one gap, stated plainly

**The invoice and document templates already running in `app.midtrans.net` have not been read.** They are not in any repository reachable from here, so what this system provides is a design, not a replacement for them. Before anything ships, the app's existing templates must be placed beside these and reconciled field by field: the numbering scheme, the tax and charge lines, the legal text, the terms block and the signature area are business artefacts and **the app's version wins on every one of them**. This section changes the visual layer only.

## What each artefact is

| Artefact | Kind | Governs |
| --- | --- | --- |
| Quotation | Document | Offer to carry, with validity |
| Invoice | Document | Amount owed |
| Credit note | Document | Amount reversed |
| Payment receipt | Document | Amount received — never an offer or a demand |
| Account statement | Document | Ledger over a period, with an opening and closing balance |
| Report | Report | Operational summary, internal |
| Email | EmailTemplate | Anything sent to an address |
| Notification | Notification | Something that happened while the user was elsewhere |
| Toast | Toast | Confirmation of what the user just did |

Each uses the component of that name. A receipt is the Document component with a different kind line and total label — it is not a new layout.

## Rules common to all of them

- **Every artefact names its record** in `mono` with tabular figures, in the first block. A document without a traceable number is not a document.
- **Every amount carries its currency and its basis.** A bare number never renders.
- **An unknown figure renders as its condition**, in `ink-muted`: "Confirmed on booking", "Per carrier schedule", "Pending customs assessment". Never `0`, never `—`, never an estimate. This is the rule that matters most here, because these artefacts are forwarded, printed, and produced in disputes.
- **Nothing is recomputed after issue.** A sent quotation, a paid invoice, an expired offer — all keep the figures they were issued with, forever. An expired document is marked `neutral` and stays readable.
- **Arabic uses the full name** `المتوسط للشحن و الخدمات - ميدترانس` and `dir="rtl"`. Reference numbers stay in Western digits in every locale.
- **The letterhead is `midtrans-logo-blue.png`** on light, the white file on a navy band. Never a recoloured mark.

## Where each surface differs

**Print** — the Document and Report drop their interface at `@media print`: no buttons, no borders on the page, the total outlined in `border-strong` rather than filled, so it survives a mono printer where a tinted fill flattens to grey.

**Email** — no stylesheet, no CSS variables, no webfont. Table layout, inline hex, 600px. The hex table is in the EmailTemplate card, and it is the one place a token change does not propagate: it is updated by hand. Arabic email falls back to the client's own Arabic face, because Cairo will not load in most clients.

**Notification** — never carries a rate, a duty or a transit time. It is the most-screenshotted surface in the product.

**Report** — internal. Figures the accounting system owns are marked `data-pending` unless the report is generated from the accounting record itself. The categorical colours are validated, fixed in order, and never reused from the status palette.

## Numbering

Document numbers follow whatever `app.midtrans.net` already issues. Nothing in this system invents a scheme, and the examples in the previews — `MDT-2026-004182`, `MDT-Q-2026-0418`, `MDT-I-2026-0311` — are placeholders shaped to show the layout, not a proposal.
