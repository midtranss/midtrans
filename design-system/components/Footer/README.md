# Footer

The site footer: a navy band closing every public page, carrying navigation, the locale row and the legal line.

Compose `mt-footer` → `mt-footer__inner` → `mt-footer__top` (brand block and `mt-footer__cols` of link groups), then `mt-footer__langs`, then `mt-footer__legal`.

**You provide:** the link groups and their labels per locale, the locale list with `aria-current="true"` on the active one, and the legal line.

**The logo.** Production uses `midtrans-logo-white.png` from the MIDTRANS LOGO group, as `<img class="mt-footer__logo">`, because the band is `surface-inverse`. The preview beside this shows the text fallback only — previews fetch nothing. Never place the blue lock-up here.

**Text colour on the navy band is `ink-inverse` for headings and links on hover, and `ink-inverse-muted` for the rest.** Do not use `ink-muted` here: it measures 2.6:1 on `surface-inverse` and fails. That is the one mistake this component exists to prevent.

**The locale row is the language switcher's second home** and follows the same rule as the header switcher: each link goes to the *same page* in the target locale, never to the home page. Each anchor carries its own `lang`, and the Arabic one carries `dir="rtl"` so the label renders correctly inside an English page.

Link groups are named after what the user is looking for — Services, Tools, Company — not after the site's internal structure. Keep to three or four groups; a footer that lists every page is a sitemap, not navigation.

**Do not** put a newsletter form, social wall, or marketing banner in the footer, and do not repeat the full main navigation.
