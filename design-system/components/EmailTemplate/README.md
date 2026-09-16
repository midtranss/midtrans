# EmailTemplate

Transactional email: departure and arrival notices, quotations sent, payment reminders, document requests.

**Email is not the web, and this is the one component that cannot use the design system's stylesheet.** Mail clients strip `<link>`, ignore most external CSS, and — critically — **do not support CSS custom properties**. `var(--brand-primary)` renders as nothing, which means an unstyled email.

So the rules invert:

- **Table layout**, `role="presentation"`, `cellpadding="0" cellspacing="0" border="0"`. Not flexbox, not grid.
- **Every style inline** on the element.
- **Token values hardcoded as hex**, copied from the table below. When a token changes, this template is updated by hand — it is the one place the system does not propagate automatically, and that is a known, accepted cost.
- **600px maximum width**, single column.
- **Buttons are a table cell with a background and a padded `<a>`** inside. A styled `<button>` does not render in Outlook.
- **Helvetica, Arial, sans-serif** written out. No webfont: Cairo will not load in most clients, so **Arabic email uses the client's own Arabic face** — set `dir="rtl"` on the table and accept the fallback.

## The values to inline

| Role | Hex | Token it mirrors |
| --- | --- | --- |
| Letterhead band | `#0a2440` | `surface-inverse` |
| Text on that band | `#ffffff` | `ink-inverse` |
| Secondary on that band | `#a8bccd` | `ink-inverse-muted` |
| Page / card | `#ffffff` | `surface-card` |
| Footer band | `#f2f5f8` | `surface-sunken` |
| Heading | `#0a2440` | `ink-strong` |
| Body | `#1f3448` | `ink-body` |
| Secondary | `#52657a` | `ink-muted` |
| Rules | `#dde4ea` | `border-subtle` |
| Button fill | `#0069a8` | `brand-primary` |
| Button label | `#ffffff` | `ink-on-brand` |

**Dark mode is not controlled here.** Some clients auto-invert. Keep the design readable when inverted: do not rely on a white background for legibility, and never place dark text on a transparent image.

## Content

**The subject line and the first heading say the same thing.** "Your shipment has departed", not "Update regarding your booking".

**Every email names its record** in `mono` in the first sentence, and the record's key facts follow as label/value rows.

**One action, as one button.** Everything else is a text link.

**Unconfirmed figures follow the claims rules exactly**: "Per carrier schedule" in `#52657a`, never a date the carrier has not published. Email is forwarded, printed and produced in disputes — it is the least forgiving surface in the system for an invented figure.

**No tracking pixels in operational mail**, and no marketing content in a transactional message.
