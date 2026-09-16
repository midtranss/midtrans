# Meridian

An **additive** theme for MIDTRANS. It adds one option; it changes nothing that already exists.

## Install

Three files, and one `<link>` after your existing stylesheets:

```
meridian/
├── meridian.css          72 KB · 12 KB gzipped
├── fonts/cairo.woff2     114 KB · Cairo, subset to Arabic + Latin, SIL OFL
└── midtrans-icons.svg    4 KB · the 16-mark logistics sprite
```

```html
<link rel="stylesheet" href="/meridian/meridian.css">
```

Loading it does nothing on its own. Nothing renders differently until the attribute is set.

## Switch it on

```html
<html data-skin="meridian" data-theme="dark">
          ↑ which design system    ↑ light or dark, your existing control
```

Two independent axes. `data-theme` is yours and is untouched. `data-skin` is the new one, and it has exactly two values:

| `data-skin` | Result |
| --- | --- |
| absent, or anything else | The current appearance, unchanged |
| `meridian` | The new system |

Wire it to a setting, default it to off, and let people opt in.

```js
// remember the choice
document.documentElement.setAttribute('data-skin', pref);  // 'meridian' or remove
```

## Why it cannot leak

Verified in a browser, not assumed:

- **Every rule is scoped to `[data-skin="meridian"]`.** There is no bare `:root`, `html` or `body` rule anywhere in the file.
- **Every `@keyframes` is namespaced** `meridian-*`, so an animation name cannot collide with one of yours.
- **The font is declared as `"Meridian Cairo"`**, not `Cairo`, so it cannot override a Cairo face you already load.
- **Nothing is renamed or removed.** Your classes, variables and cascade are exactly as they were.

The acceptance test: with `meridian.css` loaded, a legacy component measured **byte-identical** in all three states — skin off, skin on, and skin on in dark. Backing out is deleting the `<link>`.

## What it brings

31 colour tokens across light and dark, 15 text styles, a 4px spacing grid, the 4/8/12 radius scale, 27 components, 16 logistics icons, and Cairo for Arabic.

The values are the app's own where the app had them: `#007DC5` brand, `#0074B7` for fills carrying small white text, and the production dark surfaces `#050D1A`, `#0E1B2E`, `#22334C`, `#F0F5FB`.

## Rules that travel with it

- **The dashboard changes in three ways only: colour, type, size.** Structure, order, elements and behaviour stay exactly as they are.
- **No rate, transit time, duty or acceptance is ever displayed unless operations confirmed it.** Render the condition instead — "Confirmed on booking", "Per carrier schedule".
- **Mira always carries her label**: "Mira · MIDTRANS logistics assistant". The stylesheet prints a visible error if it is missing.
- **Arabic is Cairo, bound by `lang="ar"`**, and RTL is handled by logical properties. Never add a second stylesheet for RTL.

Full documentation: https://claude.ai/artifact/G8bBKTVonv2Z4Xca7xN9fe
