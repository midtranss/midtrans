Proves that Arabic renders in Cairo and reads right-to-left in every component, not only in the ones that happen to be tested.

Arabic is bound by language, not by a class: mark the subtree `lang="ar" dir="rtl"` and everything inside follows. The binding does two things, and the second is the one that matters:

```css
[lang="ar"], [lang^="ar-"] {
  --font-sans: var(--font-arabic);   /* rebinds the variable */
  font-family: var(--font-arabic);   /* and the property */
}
```

Setting `font-family` alone is not enough. Every component declares `font-family: var(--font-sans)` on itself, and a declaration on the element beats a family inherited from an ancestor — so buttons, badges, alert titles, card titles, table headers, field labels and timeline titles all kept rendering their Arabic in Helvetica while the surrounding prose was correctly in Cairo. Pointing `--font-sans` at the Arabic face inside the subtree makes every component resolve to Cairo with no per-component rules.

`--font-mono` is deliberately left alone. A booking, AWB, B/L or container number is checked character by character against a paper document and is written in Western digits in every locale, so it stays in the mono face inside Arabic:

```css
[lang="ar"] .mt-table__ref,
[lang="ar"] .mt-doc__no,
[lang="ar"] .data,
[lang="ar"] .data-sm,
[lang="ar"] [data-mono] { font-family: var(--font-mono); }
```

## What this preview covers

Hero copy, the four button variants, all five badges, an alert, a card with a data table, a field with label and help text, a timeline, an office block with a telephone link, and a reference number set inside a sentence of Arabic.

## Using it

Set `lang` and `dir` on the highest element whose content is Arabic — usually `<html>` on a fully Arabic page, or the section wrapper where a page mixes languages. Do not set `dir="rtl"` without `lang="ar"`: direction alone does not bring the font with it.

Arabic block copy uses the `ar-*` type styles rather than the Latin ones. They carry the taller leading Cairo needs — `ar-body` is 16px/30px against `body` at 15px/23px — because Cairo reads smaller than Helvetica at the same size.

Every inline axis in `bundle.css` uses logical properties, so one stylesheet serves both directions and nothing needs mirroring by hand. The logo is non-directional and does not flip.
