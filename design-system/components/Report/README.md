# Report

An operational summary: headline figures as stat tiles, and one figure showing a breakdown.

Compose `mt-stats` of `mt-stat` blocks (`mt-stat__label`, `mt-stat__value`, optional `mt-stat__note`), then a `<figure class="mt-figure">` with a `<figcaption>`, `mt-figure__rows`, and `mt-figure__legend`.

**You provide:** the numbers, already aggregated, and the bar widths as percentages of the largest value.

## A number is not always a chart

A single headline figure is a stat tile, not a chart. Reach for the bar figure only when the job is comparing magnitudes across a handful of named categories. Four modes is a figure; one total is a tile.

**Values are `mono` with tabular figures**, so a column of numbers aligns on the digit and a changing value does not shift the layout.

**A figure the accounting system owns is never estimated here.** Revenue, margin and outstanding balances render with `data-pending` — "From accounting only" — unless the report is generated from the accounting record itself.

## The figure

**Horizontal bars, because the category names are words.** Vertical bars force the labels to rotate, and rotated labels are slower to read.

**Bars are anchored to the baseline with a 4px rounded data-end**; the start edge stays square. A 2px surface ring separates adjacent fills so two bars never read as one mark.

**Colour carries identity, never magnitude.** Length is the measure. The four categorical colours are `chart-1` to `chart-4` and they are assigned **in fixed order, never cycled** — a fifth mode folds into "Other", it does not get a generated hue.

These colours were validated, not chosen by eye: worst adjacent colour-blind separation is ΔE 16.2 in light and 13.6 in dark, against a target of 8, and every one clears 3:1 against its surface in both themes. **Do not substitute a colour here without re-running that validation** — a palette that looks distinct to you can collapse into one colour for a deuteranopic operator.

**Status colours are reserved and never used as series colours.** `status-warning` means a shipment needs attention; it does not mean "air freight".

**Identity is never colour alone.** Every row is named in text beside its bar, and the legend repeats the mapping. Remove all colour and the figure still reads.

**Every bar is directly labelled with its value.** No axis, no gridlines — at five rows they are noise.

**Never two scales in one figure.** Counts and amounts are two figures, or one indexed to a common base.

## Print

Tiles and tracks gain a `border-strong` outline and bars drop their ring, so the report survives a mono printer where the fills flatten to grey.
