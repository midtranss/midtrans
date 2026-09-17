The delivery advice: the consignment has arrived, this is what is in it, and this is what must happen before it is handed over.

It is not a receipt and not a release order. It tells the consignee that cargo is at the destination and states the conditions of collection — so it carries a status per line, and no money at all.

## What differs from Document

| | |
| --- | --- |
| `mt-doc__kind` and footer | `Delivery advice` |
| Meta rows | No · Job No · Date |
| Table columns | Mark · Description · Pkgs · Gross kg · **Status** — no money column |
| Totals | Gross weight · Released · **Total packages** as the grand row |
| Side column | Deliver to · QR · consignment card (B/L, container, seal, arrival) |
| Terms card | What to bring and what the signature covers |

## A status per line, because a consignment arrives in parts

The status column is a StatusBadge per row, and it is the reason this document exists: two packages held for inspection while eighteen are ready is the normal case, not the exception. A single status on the whole consignment would force the operator to telephone.

`Released` in the totals is the count that may actually be collected — it is deliberately not the same as `Total packages`, and where the two differ the terms card says why in words.

## What the signature covers

**The driver signs for the count and the condition of the packages, not for their contents.** That sentence is in the terms card of every delivery advice, because a signature on an advice is regularly produced later as proof that contents were accepted. Do not shorten it to "received in good order".

## Money is elsewhere

No amount appears here. Charges are on the invoice for the same job number, and the closing note says so. A consignee who reads an amount on a collection document treats it as payable at the counter, which is a conversation for the accounts desk and not for a driver.

## What you provide

The issuing office, the consignee, the piece list with its marks and statuses, the B/L, container and seal numbers, the arrival date, and the QR payload. Where a package is held, the reason belongs in the terms card, not in the status word.
