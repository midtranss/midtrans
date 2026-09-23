# MIDTRANS design system — handoff

Everything a session needs to continue this work without re-deriving it. Facts
here were read out of the files in this repository, not recalled.

Last updated against `master` at the merge of #3.

---

## 1 · What is in this repository

```
design-system/     tokens.json, 34 components, 5 guideline sections
meridian/          the installable theme package + install/ kit
drafts/            website, cover, shipments, quotation, tools, Mira, theme
tools/audit/       eight checks and four generators
```

`design-system/components/` holds one directory per component with a
`preview.html` and a `README.md`, plus `bundle.css` — the single ~68 KB
stylesheet every component consumes.

**Generated files are never hand-edited**: `tokens.css`, `api/`,
`manifest.json`. Run the generators in `tools/audit/` instead.

## 2 · The decided values

These were argued and settled. Changing one is a decision, not a preference.

| Token | Light | Dark | Why this value |
| --- | --- | --- | --- |
| `brand-primary` | `#0074b7` | `#3ea7e4` | Fills carrying small white text; `#007DC5` fails 4.5:1 there |
| `brand-accent` | `#007dc5` | `#007dc5` | The brand colour itself, for large areas and marks |
| `brand-link` | `#0069a8` | `#67c0f2` | 5.14:1 on `brand-soft` |
| `status-info` | `#0070b0` | `#67c0f2` | 4.67:1 |
| `border-focus` | `#007dc5` | `#007dc5` | Same in both: the lighter dark value reached only 1.73:1 on an inverse panel |
| `surface-page` | `#ffffff` | `#050d1a` | Dark surfaces taken from the running app, not invented |
| `surface-inverse` | `#0a2440` | `#e8eef4` | Footer, hero bands, print letterhead |
| `ink-strong` | `#0a2440` | `#f0f5fb` | |

Radii **4 / 8 / 12 / 999**. Spacing on a 4px grid: 4, 8, 12, 16, 24, 32, 48, 64.

Type: `"Helvetica Neue", Helvetica, Arial, "Liberation Sans", system-ui,
sans-serif`. Arabic is **Cairo, exclusively**.

Contrast floors: **4.5:1** body, **3:1** large text, borders and focus rings.
Large means ≥24px, or ≥18.66px bold.

### The Arabic binding

Components declare their own `font-family`, so setting it on `[lang="ar"]` is
not enough — it loses to the component's own rule. The variable is rebound:

```css
[lang="ar"], [lang^="ar-"] {
  --font-sans: var(--font-arabic);
  font-family: var(--font-arabic);
}
```

Without the first line, 108 checks fail. That was measured, by removing it.

RTL is handled by **logical properties only** (`margin-inline-start`,
`inset-inline-end`, …). There is no second stylesheet for RTL and there must
never be one.

## 3 · Company facts — never paraphrase these

Freight forwarding and logistics. Founded in **Damascus, 1998**; head office in
**Dubai**.

The name has three exact forms — `MIDTRANS SHIPPING AND SERVICES` for legal and
commercial documents, `Midtrans Shipping And Services` for running text, titles
and metadata (the capital **A** is part of the name), and
`المتوسط للشحن و الخدمات - ميدترانس` for all Arabic. **It is "AND", never "&"**:
the ampersand exists only in the drawn logo artwork. Short reference: MIDTRANS,
or ميدترانس.

| Office | Address | Numbers |
| --- | --- | --- |
| Head office — Dubai, UAE | Deira, Port Saeed, Al Makateb Building, Office No 611 | Tel `+971 4 271 4480 / 4481` · Mob `+971 55 292 8560` |
| Syrian office — Damascus | Halponi, Mouslam Al Baroudi Street, 2nd Floor | Tel `+963 11 9067` · Mob `+963 933 383 858` |

WhatsApp `+963 944 334 338`.

Sample data in previews uses reserved fictional values — `ABC Trading Co.`,
`+963 11 555 0101`, `@abctrading.example`. Those are deliberately not real and
must stay that way.

## 4 · Meridian and its switch

One attribute on the root element:

```html
<html data-skin="meridian">   <!-- the new system -->
<html>                        <!-- everything as it is today -->
```

`data-theme` (light/dark) is a separate axis and is untouched.

Package: `meridian.css` 87 KB / 17 KB gzipped, `fonts/cairo.woff2` 114 KB,
`midtrans-icons.svg` 4 KB. The full wiring contract is
`meridian/install/INSTALL.md`.

Three properties that make it safe, verified rather than assumed:

- Every rule is scoped to `[data-skin="meridian"]`. No bare `:root`, `html` or
  `body` rule exists in the file.
- Every `@keyframes` is namespaced `meridian-*`.
- The font is declared `"Meridian Cairo"`, so it cannot override a `Cairo` face
  the host already loads.

The acceptance test: a legacy component measured **byte-identical** with the
skin off, on, and on in dark.

### The gate

- The control is rendered only for super admins, **and** the save endpoint
  authorizes super admin and returns 403 otherwise. A hidden control is not a
  permission.
- The role is checked **at render**, not only at save, so a demoted admin falls
  back on the next page load.
- Scope is **per account**. Making it platform-wide is a separate decision and
  the point at which customers see it.

### Switching it live

`meridian/install/meridian-theme.js` exposes `MidtransTheme.preview(skin)`. It
suppresses transitions for one frame during the flip. That freeze is not
cosmetic: without it, `background-color` is caught mid-transition and reads as
the *previous* colour while radius and font have already changed.

## 5 · The checks

```sh
sh tools/audit/run-all.sh          # needs a server on :8000 for the browser checks
```

| Check | What it proves |
| --- | --- |
| `static.py` | Raw hex, undefined vars, physical properties, decided values, radii, Arabic binding, flash rate, ink contrast against the surfaces its own usage text names |
| `doc_totals.py` | Every document total against the column its label names, plus `closing = opening + debits − credits` |
| `contract_check.js` | 23 claims, each quoting a card sentence verbatim; the quote must still be in the card |
| `live.js` | Fonts, contrast, tap targets, focus rings, Arabic subtree, rail/launcher gap |
| `meridian_proof.js` | The skin's isolation |
| `theme_switch.js` | Turning the skin on and off again is lossless |
| `veneer_check.js` | The website veneer paints without moving a box, under both box models |
| `bidi_check.js` | Every data run - weight, date, amount, phone, reference - reads left-to-right inside a right-to-left page |

All eight exit non-zero on failure. They used to print counts and exit 0, which
let regressions through.

Every check has a **negative control**: it was proven to fail when its defect
was reintroduced. A check that has never failed has never been tested.

In this container the browser checks need:

```sh
PW=/opt/node22/lib/node_modules/playwright \
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
```

## 6 · Standing constraints

- **Do not touch the live app, the website, or their modules** — loading
  calculator, HS code, invoice builder, accounting, invoices, footer. Work
  locally.
- **Old themes and designs stay unchanged.** Meridian is additive and opt-in.
- **The dashboard changes in three ways only: colour, type, size.** Structure,
  order, elements and behaviour stay. Anything moving is a bug.
- **Invoice templates take the app's existing templates**, not new ones.
- **No rate, transit time, duty, route, capacity, acceptance or delivery date**
  is ever displayed unless operations confirmed it — including in placeholder
  and demo content. Render the condition instead: "Confirmed on booking",
  "Subject to carrier schedule", "Pending customs assessment". Never `0`, `—`,
  `TBD` or a greyed sample figure.
- **No superlatives** in any locale: best, largest, cheapest, fastest,
  guaranteed, number one.
- **Mira is synthetic, and the illustrated mark is her image.** The
  photographic portrait is retired: a human face beside a reply presents a
  synthetic persona as a member of staff. `mira-avatar.svg` is the `mt-avatar`
  source everywhere; `mt-avatar` carries no border, no fill and
  `object-position: center`, because the mark is already a disc. She is
  **never presented as an employee** — no team page, no staff directory, no
  signature, no named contact.
- **Mira always carries her label**: "Mira · MIDTRANS logistics assistant".
  The mark makes her nature legible; the label states it. Both, not either.
- Locales in parity: EN, AR, FR, DE, TR, ZH, SV.
- `trustbycompass.com` is a different project and out of scope.

## 7 · Mistakes already made here — do not repeat them

Each of these shipped, was caught, and was fixed. They are listed because the
next session is likelier to repeat them than to invent new ones.

| What went wrong | The lesson |
| --- | --- |
| A Damascus phone number was invented | The canonical number is `+963 11 9067`. Read it from `Contact/preview.html` |
| Freight rates were illustrated in document previews | Amounts are masked `0 000.00`. A specimen document says so in an alert |
| A packing list's totals did not add up (12,026 vs 7,026) | `doc_totals.py` now checks every total against its named column |
| The totals check accepted **any** column, and silently skipped money totals | A regex stopped at the first `</span>`. Four totals reported PASS while never being checked |
| Em-dashes filled empty ledger cells | A blank cell is blank |
| The auditor read styles mid-transition | It invented 23 contrast failures. Bake `data-theme` into the markup and freeze transitions before measuring |
| Arabic rendered in Helvetica | Every component declaring its own family beat the `[lang="ar"]` rule. Rebind `--font-sans` |
| Six of seven Meridian keyframes were dead | The generator prefixed at-rules like selectors. At-rules are handled by kind |
| A hover fix never worked | A reset at line 619 lost to real rules at 1100 by source order at equal specificity |
| `.mt-doc__main` became focusable with no focus ring | Adding `tabindex` adds a focus obligation |
| The README claimed 72 KB / 12 KB | It was 87 KB / 17 KB. Measure, do not estimate |
| An install guide told readers to clone a branch | The merge made it false. Instructions about the repo go stale when the repo changes |
| Arabic scrambled every number in the system | No rule anywhere isolated a data run, so in RTL "12 500 KG" drew as "KG 500 12" and both offices' phones reversed - 57 runs in 34 components. `direction:ltr` fixed the order but flipped column alignment; unprefixed `match-parent` does nothing in Chromium; `-webkit-match-parent` does. Measured each |
| A check reported PASS having measured nothing | `bidi_check.js` skipped pages that failed to load - the server was down - and passed on zero runs. A failed load is now a failure, and fewer than 20 runs is a failure |
| Mira shipped with a photographic portrait | She is synthetic. A human face beside a reply presents her as staff, whatever the label says. Reversed to the illustrated mark, which also removed the resolution limit and reads better at 32px |

## 8 · Not yet decided

- Dashboard chrome from the reference pack: header row, top nav, More menu,
  Quick Action, sidebar, notifications, chat dock, mobile bottom nav, KPI grid,
  needs-now, freight cycle. All under "colour, type, size only".
- PR #1 (`Add MIDTRANS office contact pages`) is an open draft from June: a
  static site for `www.mid-trans.com`, English only, carrying its own design
  direction that predates this system. Its contact data is correct and matches
  section 3.
