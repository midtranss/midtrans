# ServiceCard

A capability the company sells, in a grid of three: mode, service, or specialism.

Use `mt-service` on an `<a>`, holding `mt-service__icon` (an inline icon from the set), `mt-service__title` and `mt-service__text`.

**You provide:** the link, the icon symbol, and the copy per locale.

**The whole card is the link** — this is the one place that rule is inverted from Card, because the card carries a single destination and no inner actions. Keep it an `<a>` so it is one tab stop with one accessible name.

**The icon is the service's mode or subject**, from the MIDTRANS set: `ship`, `aircraft`, `truck` for modes, `customs-stamp` for clearance, `warehouse` for storage, `document` for documentation, `shield-check` for verification. It inherits `brand-link` from the card, so it is never given its own colour.

**The text says what is actually operated** — ports, equipment, whether clearance is in-house, whether door delivery exists. Two lines. It is not a slogan and it is not a list of adjectives.

**Three per row on desktop, one below 768px.** A grid of six services is two rows of three, not a scroller.

**Do not** add a "Learn more →" line: the whole card is the link and the arrow is noise. Do not vary the card heights by writing longer copy for some services — the grid stretches them to match, and ragged text lengths are what make a service grid look unplanned.
