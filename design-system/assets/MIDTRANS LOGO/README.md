# MIDTRANS LOGO

The MIDTRANS identity: a ship's wheel with wings, above the "Midtrans" wordmark in its own script face, with the line "Shipping & Services" beneath it on the full lock-up.

Each file has one job. Pick by the ground it lands on — never recolour a file to make it fit.

| File | Ground | Use |
| --- | --- | --- |
| `midtrans-logo-blue.png` | Light | Blue mark on transparency. On `surface-page`, `surface-card` and `surface-sunken`: site header, documents, light email templates. |
| `midtrans-logo-white.png` | Dark | White mark on transparency. On `surface-inverse`, on a `brand-accent` or `brand-primary` field, and over photography. |
| `midtrans-app-icon-512.png` | Its own | Solid blue field with the white mark. The browser and app icon: favicon, tab icon, PWA icon, touch icon, social profile. |
| `midtrans-app-icon-1024.png` | Its own | The same icon at 1024px, for store listings and any icon slot above 512px. |

**Light and dark.** In a dark theme, swap the file — do not filter, invert or fade the blue one. In HTML use a `<picture>` with a `prefers-color-scheme` source, or swap the `src` on the same `data-theme` attribute the tokens use, so the mark follows the theme with the rest of the interface.

**The icon is not the lock-up.** The app icon carries its own blue background and drops the "Shipping & Services" line; it is never placed inside the page as a logo, and the lock-up is never squeezed into a favicon. The full lock-up is not used below 120px wide — use the icon there.

**Ink.** These are flat PNGs on transparency (the icon on a solid field) and carry their ink in the file, so an `<img>` cannot inherit a text colour and CSS must not recolour them. Three different blues are measurable across the set — the stated brand `#007DC5`, the lock-up's ink `#007DC6`, and the icon field's `#027AC8`. None of the differences is visible in use, but whoever re-cuts the artwork should settle all three on `#007DC5`. The "Shipping & Services" line is near-black `#050708` in the blue lock-up.

**Clear space and size.** Keep `space-4` clear on all four sides of the lock-up, measured from the widest point of the wings. The icon files already carry their own padding inside the blue field: do not add more, and do not crop it.

**Do not** rotate, stretch, outline, add a shadow to, or recolour the mark; place the lock-up on a busy photograph without a `surface-inverse` scrim; or re-set the wordmark in another typeface. The mark is non-directional: it does **not** mirror on Arabic RTL pages.

**Format.** PNG raster only. Vector artwork is needed before print, large-format or crisp favicon production; record it here when it is available.
