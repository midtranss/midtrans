MIDTRANS is an international freight forwarding and logistics company operating from Damascus since 1998. Everything built with this system — the public website, the platform, ERP, CRM, quotations, the logistics chatbot and printed documents — should read as enterprise operational software: organised, specific, and answerable. Not a consumer app, and not generic SaaS.

## Content fundamentals

Write in the operator's voice: calm, precise, and accountable for what it states.

- **Be specific or be silent.** Never publish a price, transit time, customs cost, route, capacity, acceptance or delivery commitment that has not been confirmed operationally. Where a figure is not yet known, write "Confirmed on booking" and set it in `ink-muted`, not a placeholder number.
- **No superlatives.** "Best", "largest", "fastest", "guaranteed", "world-leading" and unsupported market-leadership claims do not appear in any locale. Replace the claim with the fact behind it: "Operating from Damascus since 1998", "Sea, air and land freight with in-house customs clearance".
- **Sentence case for everything a person reads** — headings, buttons, table headers, notification titles. Uppercase belongs only to the `label` style, which the component applies with `text-transform`.
- **Say what happens next.** Every empty state, error and confirmation names the next action: "Attach the packing list to continue", not "Missing document".
- **Address the reader as "you"; MIDTRANS is "we".** In Arabic use the formal plural.
- **No emoji** in product UI, transactional email or documents.
- **Reference numbers are never reflowed.** Booking, AWB, B/L, container and invoice numbers are set in `data` or `data-sm` with `font-variant-numeric: tabular-nums`, and are selectable as one run.

## Visual foundations

### Colour

- Set page backgrounds in `surface-page`, panels and tables in `surface-card`, and recessed bands, table headers and sidebar rails in `surface-sunken`.
- `brand-accent` is the identity blue `#007DC5`, exact in both themes. Spend it on graphics, rules, chart marks and display type at 24px or larger. White on it measures 4.43:1, so it never fills a button or any surface carrying body-size text.
- Fill primary actions with `brand-primary` and label them `ink-on-brand`. `brand-primary` is the identity blue darkened for light and lightened for dark, which is what keeps the label legible in both.
- Use `surface-inverse` with `ink-inverse` for deep-navy bands: the site footer, a hero, a letterhead. One such band per screen.
- Keep body copy in `ink-body`, headings and figures in `ink-strong`, and secondary text in `ink-muted`. Every text token's note names the grounds it is cleared for; do not put text on a ground its note does not list.
- Draw meaning-carrying edges — input outlines, secondary button borders, checkbox edges — in `border-strong`. `border-subtle` is decorative only: card outlines, table rules, dividers.

### Type

- Latin copy is set in the `sans` family — Helvetica first, with Arial and Liberation Sans behind it. No webfont is loaded for Latin text: the stack is resident on every platform MIDTRANS serves, which is what keeps the first paint fast on mobile.
- Arabic copy is set in the `arabic` family, Cairo first. Use the `ar-*` styles rather than the Latin ones: they carry the taller leading Cairo needs.
- Reference numbers and aligned figures use the `mono` family through `data` and `data-sm`.
- One `display-1` per page at most. Inside the platform, start pages at `heading-1`.

### Spacing, radius and elevation

- Lay everything out on the 4px grid in `spacing`. Page gutters are `space-8` on desktop, `space-4` on mobile; cards are padded `space-5` on desktop and `space-4` below 768px.
- Radii stay small: `radius-sm` for inputs and badges, `radius-md` for buttons, cards and modals, `radius-lg` only for hero and media blocks. `radius-pill` is reserved for the status dot and dismissible filter chips.
- A card at rest carries `border-subtle` and no shadow. Shadow means the element floats above the page: `shadow-md` for dropdowns and popovers, `shadow-lg` for modals.

### States

- Focus is a solid 2px `border-focus` ring with a 2px offset, on every interactive element, in both themes. Never remove it and never replace it with a background change alone.
- Hover darkens a fill by one step and never moves the element.
- Disabled controls drop to 55% opacity and keep their text legible; they are never the only explanation for why an action is unavailable — say why in adjacent `body-sm` text.
- Status colour never carries meaning alone. Every status is a colour **and** a word, which is what makes the set readable for colour-blind operators. `status-success` and `status-danger` are told apart by their labels, not by hue.

### Imagery

Photography shows real freight operations — vessels, aircraft cargo holds, container yards, trucks, warehouse handling, documentation. No stock handshakes, no abstract network graphics, no globes with glowing arcs. Heavy hero imagery is dropped or replaced with a `surface-inverse` band below 768px rather than scaled down; mobile performance outranks the picture.

### Logo and marks

No MIDTRANS logo file was available when this system was built, so none is included here and none has been drawn. Until the real artwork is added under an `assets/Logos` group, set the company name as plain type: `display-2` in `ink-strong`, or `ink-inverse` on `surface-inverse`, with the word MIDTRANS in full capitals and no letter-spacing change.

### Iconography

No MIDTRANS icon set was available either. Until one is chosen, use a single open outline set at 24px on a 24px box with a 1.5px stroke, drawn in `currentColor` so it inherits the text token beside it, and record the choice here. Do not mix two icon sets, and do not use emoji as icons. Icons that carry meaning on their own need 3:1 against their ground, which `ink-body`, `ink-muted`, `brand-link` and the `status-*` colours all hold.

## Layout

- The platform runs at a 1280px content maximum with a fixed left rail; the website runs at 1200px centred.
- Tables are the primary surface for shipments, quotations and invoices. Freeze the header, keep the reference number column first and left-aligned, and right-align every numeric column.
- Forms are single-column. Two columns only for values that are read as a pair — origin and destination, gross weight and volume.

## Reading this system

Foundations are in `tokens.json`. Component markup contracts are in `components/<Name>/README.md`, with a live example beside each one, and the classes they use are defined in `components/bundle.css`. Multilingual and RTL rules, and the rules on claims and figures, are the two sections that follow this one.
