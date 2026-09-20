# The veneer

The MIDTRANS design system's **appearance**, applied to an existing site
without touching its markup, its words, or the order of anything on a page.

```
veneer/
├── midtrans-veneer.css      13 KB · 4 KB gzipped
├── fonts/cairo.woff2        114 KB · Cairo, SIL OFL
└── fonts/Cairo-OFL.txt
```

## The one rule

**It may paint. It may not move.**

| Permitted | Forbidden |
| --- | --- |
| `color` `background` `border` `border-radius` `box-shadow` `outline` | `display` `position` `float` `order` `flex-*` `grid-*` |
| `font-family` `font-size` `line-height` `font-weight` `letter-spacing` | `width` / `height` on layout containers |
| `transition` | `content`, and any `::before`/`::after` that adds text |

No rule in this file names a class the site owns. It targets elements, which
is why it survives a redesign of the markup.

## Install

One line, **after** every stylesheet the site already has:

```html
<link rel="stylesheet" href="/veneer/midtrans-veneer.css">
```

Keep `fonts/` beside the CSS — the Arabic face is fetched relative to it.

**Loading it changes nothing.** Every rule is behind an attribute on `<html>`
that is not there yet. Deploy this alone, look at the site, and confirm it is
identical. That is the safest step in the process and it is worth taking by
itself.

## Turn it on, a layer at a time

```html
<html data-mt="colour">                 colours only          moves nothing
<html data-mt="colour surface">         + borders, radii, shadows   moves nothing
<html data-mt="colour surface type">    + fonts and sizes      reflows
```

The order matters. The first two are free: **measured against a page with its
own stylesheet, every box stayed at exactly the same x, y, width and height.**
Ship them, look, live with them for a day.

`type` is different and it is honest to say so. Changing a font size changes
how tall a paragraph is, and on inline layouts it changes how wide things sit
— in the test fixture the submit button shifted sideways, because the
whitespace between form controls is sized by the parent's font. That is not a
defect to fix; it is what changing the type *means*. Take that layer on
purpose, on staging, and look at every template before it goes live.

Removing a layer is deleting a word from the attribute. Removing the whole
thing is deleting the `<link>`.

## What each layer does

**colour** — body and heading ink, link colour and hover, muted text, form
control ink and placeholders, selection, `mark`, table ink, and a visible
focus ring on everything interactive. The focus ring is the one that matters
most: it meets the 3:1 floor whatever the site did before.

**surface** — the 4/8/12 radius scale on images, inputs and buttons; the
subtle border colour on rules and tables; the brand rule on blockquotes; the
sunken fill behind code.

The input ring is painted with `box-shadow: inset`, **not** a border. A border
occupies space: on a site that has not set `box-sizing: border-box`, and whose
inputs carry no border of their own, adding one grows every field by 2px in
each direction. That was measured on exactly that case before it was changed.

**type** — the design system's scale: `h1` 32/38, `h2` 26/32, `h3` 21/28,
`h4` 17/24, body 15/23, small 13/20. Arabic gets its own metrics, which are
looser: 26/40 for a heading and 16/30 for body, because Cairo needs the room.

**Arabic applies under every layer**, not just `type`. A wrong font in Arabic
is not a refinement. The face is declared as `"MIDTRANS Cairo"` so it cannot
override a `Cairo` the site already loads, and the variable is rebound as well
as the property — an element whose own rule reads `var(--mt-sans)` resolves it
to Cairo too.

## What element selectors cannot reach

This is the veneer's real limit, and it is worth knowing before you judge the
result.

Naming no class the site owns is what makes the file survive a markup
redesign — but it also means a `<div class="card">` is **invisible** to it.
Element selectors reach `body`, headings, links, `img`, `input`, `select`,
`textarea`, `button`, `table`, `th`, `td`, `hr`, `blockquote` and `code`. They
do not reach the site's cards, panels, bands, nav or footer, and those carry
most of a site's visual character.

So expect this from the base file alone: **text, links, form controls, tables
and focus rings take the system's appearance; the site's own containers keep
theirs.** On a content-heavy page that is most of what you see. On a page built
from custom cards it is not.

The last block in the stylesheet, `THE SITE'S OWN CLASSES`, is where you close
that gap — one block, clearly marked, with the same paint-never-move rule and
a template to copy. Filling it needs the site's real class names, which means
reading its stylesheet first.

## Maintenance

**The veneer is always last.** If a build step concatenates stylesheets, it
goes at the end. If it stops being last, it stops working, silently.

**Never edit the site's own CSS to make the veneer fit.** If a rule does not
land, the answer is a more specific selector inside the veneer, never a change
to the site. The two files must stay separable, because that separation is
what makes this reversible.

**Never add a moving property.** Not padding, not margin, not width — not even
"just this once, on one card". The check below exists because that is the
temptation, and it fails the moment anyone gives in.

**A new page needs no work.** The veneer targets elements, so a page published
next year is styled the day it ships. That is the whole reason it does not
name the site's classes.

**When the site changes its own colours**, nothing here needs touching: the
veneer sets the colour last and wins. When the site changes its *layout*, also
nothing — the veneer never had an opinion about layout.

**When a token changes in the design system**, change it here too, in the
`:root` block. Those values are copied, not imported, because the site does
not load `tokens.css`. `HANDOFF.md` §2 is the source of truth; the block here
must match it exactly.

**Check before every deploy:**

```sh
node tools/audit/veneer_check.js
```

It renders a page that has its own stylesheet, applies each layer, and fails
if `colour` or `surface` moved a single box by more than half a pixel, or if
turning the veneer off does not return the page to exactly what it was. It is
proven to fail: adding one `padding` rule to the colour layer moves 11 boxes
and the check reports all of them.

## What this is not

It does not change a word, a heading, a link, an image or the order of
anything. It does not add or remove a page. It does not redirect. It has no
opinion about content, and the content rules in `website-CLAUDE.md` still
govern every word on the site independently of it.
