The packing list: the same template as Document, with no money column anywhere.

It answers what is in the shipment, how many pieces, how heavy and how large — for the warehouse, the carrier and the customs officer. It never answers what it cost.

## What differs from Document

| | |
| --- | --- |
| `mt-doc__kind` and footer | `Packing list` |
| Meta rows | No · Job No · Date |
| Table columns | Mark · Description · Pkgs · Gross kg · Net kg · CBM — **six, and none of them money** |
| Totals | Gross weight · Net weight · Volume · **Total packages** as the grand row |
| Side column | Consignee · QR · shipment card (B/L, container, seal, vessel) |
| Terms card | Handling instructions, not payment terms |

## No value, deliberately

There is no `mt-doc__money`, no currency and no amount on this document, and the closing note says so:

> No commercial value is stated on this document. It lists contents, counts and measurements for handling and customs presentation. Values are on the commercial invoice for the same job number.

A packing list that carries prices invites the wrong conversation at the border and exposes commercial terms to everyone who handles the box. The job number is what ties it to the invoice.

## The grand row is a count

`mt-doc__total-row--grand` is the only filled row here as everywhere else, but it carries **Total packages** — the number the warehouse and the carrier actually check. Weights and volume sit in the plain rows above it.

Figures are set in the mono face with tabular figures, so gross, net and volume columns align on the digit down the page.

## Marks

The mark column is mono (`data-mono`) and holds the range as it is written on the cartons — `1–12`, not `1 to 12` and not `12 pcs`. It is matched character by character against what is physically on the pallet.

## What you provide

The issuing office, the consignee, the piece list with its marks, the weights and measurements, the B/L, container and seal numbers, and the QR payload. Where the vessel is not yet confirmed, write the condition — "Per carrier schedule" — not a guess.
