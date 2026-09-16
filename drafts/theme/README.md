# MIDTRANS theme

The built theme layer for every MIDTRANS property: the website, the platform, the ERP, the desk and the assistants. It is CSS and one font. It contains no application logic, no framework and no build step.

## Files

| File | Size | What it is |
| --- | --- | --- |
| `tokens.css` | 5 KB | Colour, type, spacing, radius and shadow as CSS custom properties, in light and dark, plus the `@font-face` for Cairo. Generated from the design system — never edit by hand. |
| `midtrans.css` | 31 KB | The components, and the device and input foundations. |
| `fonts/cairo.woff2` | 114 KB | Cairo, variable, weights 200–1000, subset to Arabic and Latin. SIL Open Font License. |
| `midtrans-icons.svg` | 4 KB | The 16-mark logistics icon sprite. |
| `index.html` | — | A verification harness. Not for production. |

## Install

Copy the files, then in every page's `<head>`, in this order:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="preload" href="/theme/fonts/cairo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/theme/tokens.css">
<link rel="stylesheet" href="/theme/midtrans.css">
```

`viewport-fit=cover` is required, or `env(safe-area-inset-*)` returns zero and the layout will clip on any device with a notch or a home indicator.

Preload the font only on pages that render Arabic.

## Theme

Set `data-theme="light"` or `data-theme="dark"` on `<html>`. With neither, the theme follows the operating system through `prefers-color-scheme`.

```html
<html lang="ar" dir="rtl" data-theme="dark">
```

## Direction

Set `dir="rtl"` on `<html>` for Arabic. One stylesheet serves both directions — everything is written with logical properties. Do not add an RTL stylesheet.

## Icons

Inline the sprite once per document, then reference a symbol:

```html
<svg class="mt-icon" aria-hidden="true"><use href="#mt-ship"/></svg>
```

Loading the sprite through `<img>` renders it black and it cannot follow the theme.

## Rules that are not negotiable

1. **No raw hex in application code.** Every colour is `var(--token)`. This is what lets one change reach every property.
2. **Never recolour the logo with CSS.** Swap the file: blue on light grounds, white on dark, the blue-field icon as the favicon.
3. **No price, transit time, duty, customs cost or acceptance is rendered unless it came from a confirmed operational source.** Where the value is unknown, render the condition — "Confirmed on booking", "Per carrier schedule" — using `data-pending`.
4. **Every screen has a URL**, so the system back gesture and the browser's back button work.

## Verify

Open `index.html` and check: both themes, both directions, tab focus rings, and the window at 280px, 402px, 768px, 984px and 1440px. The 984px width is a folding phone opened — it is the check most often skipped.

## Updating

This directory is generated from the MIDTRANS design system. Change the system, regenerate, replace these files. Do not patch them in place — an edit here is lost at the next regeneration.
