# Document

The MIDTRANS commercial document: quotation, invoice, proforma, payment receipt, delivery advice, packing list, account statement.

**This is the app's own template, not a replacement for it.** The anatomy below was taken element for element from the templates running in `app.midtrans.net` — the 6px brand rule, the letterhead row, the document box with its meta list and verified badge, the 250px side column of cards, the line table, the terms card beside the totals, the brand-filled grand-total row, and the document kind repeated in the footer. Only colour, type and size come from this system. **Do not rearrange it.**

## Anatomy

```
mt-doc                                  6px brand-accent rule on top
├── mt-doc__top
│   ├── mt-doc__brand                   company name + full issuing-office address
│   ├── mt-doc__box                     mt-doc__kind · mt-doc__meta rows · mt-doc__badge
│   └── mt-doc__logo
├── mt-doc__content
│   ├── mt-doc__side  (250px)           party card · QR card · route / location card
│   └── mt-doc__main
│       ├── mt-doc__table               the lines
│       ├── mt-doc__close               terms card | mt-doc__totals
│       └── mt-doc__note                exclusions
└── mt-doc__foot                        the kind, again
```

**You provide:** the issuing office, the parties, the lines, the totals, the QR payload, and the document number — all from the accounting record.

## The kinds

One component, one `mt-doc__kind` line, one footer label. A receipt is not a different layout from a quotation.

| Kind | Meta rows | Totals label | Notes |
| --- | --- | --- | --- |
| Quotation | No · Job No · Valid | Quotation total | Terms card states it is subject to space and review |
| Proforma invoice | No · Job No · Valid | Proforma total | Marked clearly as **not** a tax invoice or a demand for payment |
| Invoice | No · Job No · Due | Invoice total | Payment terms and bank details in the terms card |
| Payment receipt | No · Invoice · Date | Amount received | Confirms receipt only — never a demand; settlement note says allocation is subject to finance review |
| Delivery advice | No · Job No · Date | Delivery status | Cargo/reference/qty/status table; instructions card |
| Packing list | No · Job No · Date | Total packages / weight / volume | No money column at all |
| Account statement | No · Period | Closing balance | Opening balance, movements, closing balance |

## The rules that do not move

**The issuing office is chosen, not assumed.** MIDTRANS issues from Dubai and from Damascus, and the letterhead prints the address and telephone of the office that issued *this* document. Never a blended or generic address.

**Money is two aligned columns** — currency, then amount — in `mono` with tabular figures, exactly as the app sets it. A column of amounts lines up on the digit and the currency never drifts. An amount without its currency does not render.

**The grand total row is the only filled row**, in `brand-primary` with `ink-on-brand`. In print it becomes an outline in `border-strong`, because a tinted fill flattens to grey on a mono printer and the most important number on the page must not be the least legible.

**The QR card verifies the document**, and stays even when the value is long. It is `brand-accent` on the page and pure black when printed.

**Every unconfirmed figure renders as its condition**, in `ink-muted`: "Confirmed on booking", "Pending customs assessment", "Assessed on the declaration". Never `0`, never `—`.

**Nothing is recomputed after issue.** An expired quotation keeps its figures and gains a `neutral` StatusBadge reading "Expired".

**Arabic** sets `dir="rtl"` on the article; every axis in this component is logical, so the side column moves to the right and the totals to the left with no second stylesheet. Document numbers and amounts stay in Western digits.

## Still to reconcile

The numbering schemes, tax lines, legal text and bank details in the app's live templates are business artefacts. Where this card and the app differ on any of them, **the app is right** — this component governs the visual layer only.
