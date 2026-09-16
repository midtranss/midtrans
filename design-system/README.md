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
- `brand-accent` is the official identity blue `#007DC5`, exact in both themes. It supersedes the `#0a5a9c` used by the current public site stylesheet, which is legacy and is not carried forward. Spend it on graphics, rules, chart marks and display type at 24px or larger. White on it measures 4.43:1, so it never fills a button or any surface carrying body-size text.
- Fill primary actions with `brand-primary` and label them `ink-on-brand`. `brand-primary` is the identity blue darkened for light and lightened for dark, which is what keeps the label legible in both.
- Use `surface-inverse` with `ink-inverse` for deep-navy bands: the site footer, a hero, a letterhead. One such band per screen.
- Keep body copy in `ink-body`, headings and figures in `ink-strong`, and secondary text in `ink-muted`. Every text token's note names the grounds it is cleared for; do not put text on a ground its note does not list.
- Draw meaning-carrying edges — input outlines, secondary button borders, checkbox edges — in `border-strong`. `border-subtle` is decorative only: card outlines, table rules, dividers.

### Type

- Latin copy is set in the `sans` family — Helvetica first, with Arial and Liberation Sans behind it. No webfont is loaded for Latin text: the stack is resident on every platform MIDTRANS serves, which is what keeps the first paint fast on mobile.
- Arabic copy is set in the `arabic` family, which is **Cairo and nothing else** — no system fallback is declared. The variable font ships with this system at `fonts/Cairo-Variable.ttf` (weights 200–1000, SIL Open Font License, licence beside it), so Arabic renders in Cairo on every device without a call to a font CDN. Use the `ar-*` styles rather than the Latin ones: they carry the taller leading Cairo needs.
- Reference numbers and aligned figures use the `mono` family through `data` and `data-sm`.
- One `display-1` per page at most. Inside the platform, start pages at `heading-1`.

### Spacing, radius and elevation

- Lay everything out on the 4px grid in `spacing`. Page gutters are `space-8` on desktop, `space-4` on mobile; cards are padded `space-5` on desktop and `space-4` below 768px.
- Radii follow the international enterprise band: `radius-sm` (4px) for inputs and badges, `radius-md` (8px) for buttons, cards, panels and modals, `radius-lg` (12px) for hero blocks, media frames and document letterheads. `radius-pill` is reserved for status dots, meters and dismissible filter chips — never a button.
- A card at rest carries `border-subtle` and no shadow. Shadow means the element floats above the page: `shadow-md` for dropdowns and popovers, `shadow-lg` for modals.

### States

- Focus is a solid 2px `border-focus` ring with a 2px offset, on every interactive element, in both themes. Never remove it and never replace it with a background change alone.
- Hover darkens a fill by one step and never moves the element.
- Disabled controls drop to 55% opacity and keep their text legible; they are never the only explanation for why an action is unavailable — say why in adjacent `body-sm` text.
- Status colour never carries meaning alone. Every status is a colour **and** a word, which is what makes the set readable for colour-blind operators. `status-success` and `status-danger` are told apart by their labels, not by hue.

### Imagery

Photography shows real freight operations — vessels, aircraft cargo holds, container yards, trucks, warehouse handling, documentation. No stock handshakes, no abstract network graphics, no globes with glowing arcs. Heavy hero imagery is dropped or replaced with a `surface-inverse` band below 768px rather than scaled down; mobile performance outranks the picture.

### Logo and marks

The mark is a ship's wheel with wings, above the "Midtrans" wordmark and the line "Shipping & Services". Four files sit in the **MIDTRANS LOGO** asset group, and each has one job — pick by the ground, never recolour a file to fit:

- `midtrans-logo-blue.png` — blue on transparency, for light grounds: `surface-page`, `surface-card`, `surface-sunken`.
- `midtrans-logo-white.png` — white on transparency, for dark grounds: `surface-inverse`, a `brand-accent` or `brand-primary` field, and photography.
- `midtrans-app-icon-512.png` and `midtrans-app-icon-1024.png` — the white mark on a solid blue field, used as the browser and app icon: favicon, tab icon, PWA and touch icon, social profile. Never placed inside a page as a logo.

In a dark theme, swap the file rather than filtering or inverting the blue one; drive the swap from the same `data-theme` attribute the tokens use so the mark follows the interface.

- The artwork is flat and carries its own ink, so it does not inherit `currentColor` and CSS must not recolour it. Three blues are measurable across the set — the stated brand `#007DC5`, the lock-up's ink `#007DC6`, the icon field's `#027AC8`; none is visibly different, but re-cut artwork should settle all three on `#007DC5`. The "Shipping & Services" line is near-black `#050708`.
- Clear space around the lock-up is `space-4` on all four sides, from the widest point of the wings. Minimum width for the lock-up is 120px; below that use the icon. The icon files carry their own padding — do not add to it or crop it.
- Never recolour, rotate, stretch, outline or shadow the mark. The wordmark is part of the artwork in its own script face: never re-set "Midtrans" in `sans` and never uppercase it. Where only text is possible, set MIDTRANS in `display-2` `ink-strong`, full capitals, no letter-spacing change.
- The mark is non-directional: it does not mirror on Arabic RTL pages.
- Only PNG raster is available; obtain vector artwork before print, large-format or crisp favicon work.

### Iconography

No MIDTRANS icon set was available either. Until one is chosen, use a single open outline set at 24px on a 24px box with a 1.5px stroke, drawn in `currentColor` so it inherits the text token beside it, and record the choice here. Do not mix two icon sets, and do not use emoji as icons. Icons that carry meaning on their own need 3:1 against their ground, which `ink-body`, `ink-muted`, `brand-link` and the `status-*` colours all hold.

## Layout

- The platform runs at a 1280px content maximum with a fixed left rail; the website runs at 1200px centred.
- Tables are the primary surface for shipments, quotations and invoices. Freeze the header, keep the reference number column first and left-aligned, and right-align every numeric column.
- Forms are single-column. Two columns only for values that are read as a pair — origin and destination, gross weight and volume.

## Reading this system

Foundations are in `tokens.json`. Component markup contracts are in `components/<Name>/README.md`, with a live example beside each one, and the classes they use are defined in `components/bundle.css`. Multilingual and RTL rules, and the rules on claims and figures, are the two sections that follow this one.
