# HSCodeCard

One classification, packaged to be copied, shared or pasted into a message.

Compose `mt-hscard` → `mt-hscard__head` (brand and kind), `mt-hscard__code`, `mt-hscard__desc`, a `KeyValue` of chapter and heading, the actions, and `mt-hscard__foot`.

**You provide:** the tariff data, the copy-to-clipboard and share handlers, and the locale.

**The code is the hero**, at 32px in `mono` with tabular figures, in `brand-accent` — this is one of the few places the exact brand blue is used as type, and it qualifies because it is well above 24px.

**The description is the tariff's own wording**, not a paraphrase. The recipient compares it against a commercial invoice.

## Why the duty line says nothing

**The duty row always reads "Assessed on the declaration".** This card is built to leave MIDTRANS — it gets pasted into WhatsApp, forwarded to a supplier, attached to an email, screenshotted. A duty rate on it would travel with the MIDTRANS name attached and be read as a quoted customs cost, for a country, an origin and a valuation the card knows nothing about.

**The footer disclaimer is part of the card, not a caption.** It travels with the image and it is never removed to make the card tidier: the classification is indicative, and the authority of the country of import decides. The company name appears beside it so a forwarded card is attributable.

**When the card is rendered as an image for sharing**, the disclaimer and the company name must be inside the rendered area. A card cropped to just the code is not this component.

**Do not** put a price, a transit time or a "total landed cost" on this card, and do not let it be the input to a declaration without a person confirming the classification.
