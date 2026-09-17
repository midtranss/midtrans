# Devices and input

MIDTRANS interfaces are used on a desk with a mouse, on a warehouse tablet with gloves, and on a phone at a port gate. The system is built against **capabilities**, never against device names — that is what lets it work on hardware released after it was written.

## Verified device viewports

Measured CSS viewport widths, not physical resolutions — these are the numbers a media query sees.

| Device | CSS viewport | Falls in |
| --- | --- | --- |
| Galaxy Z Fold 7, unfolded | 984 × 1092 (DPR 2.0) | Side-rail layout |
| Galaxy Z Fold 8, unfolded | 4:3 inner display — wider and shorter than the Fold 7 | Side-rail layout |
| Galaxy Z Fold 8, cover | 5.5in cover, narrower than the Fold 7's 6.5in | Narrow band |
| iPhone Air | 420 × 912 (DPR 3) | Phone band |
| iPhone 17 | 402 × 874 (DPR 3) | Phone band |

Two of these drive real decisions. **984px unfolded** is why the side rail starts at 900px and not at 1024px: a Fold 7 opened must get the desk layout, not a stretched phone layout. **The Fold 8's cover screen is narrower than the Fold 7's**, which is why the narrow band below is not an edge case — it is a shipping flagship, and the layout is checked there first, not last.

The Fold 8's inner display is 4:3 — wider and shorter than the Fold 7's. A layout that assumed a tall narrow window when unfolded will run out of height before it runs out of width, so vertical rhythm is what to watch there, not horizontal.

The current mobile platforms as of September 2026 are **iOS 26.6.2** and **Android 17** — the latter ships on the Fold 8. There is no iOS 27.

## Sizes

One layout, five behaviours. Widths, not devices.

| Width | What it is in practice | Behaviour |
| --- | --- | --- |
| ≤ 359px | The Fold 8 cover screen, small phones, a split-screen pane, a browser window dragged narrow | Single column, actions full width, padding drops to `space-3`, hero title to 26px, tables restate as stacked records |
| 360–599px | Phones, including iPhone 17 at 402px and iPhone Air at 420px | Single column, bottom navigation bar, tables stacked |
| 600–899px | Tablets in portrait, a small folding phone opened | Two-column pairs return, cards go two across |
| 900–1199px | Tablets in landscape, small laptops, **a Fold 7 or Fold 8 unfolded** | Side rail replaces the bottom bar, tables return as tables |
| ≥ 1200px | Desktop | Full layout, 1200px content maximum |

Test at **280px** as well. It is not a phone; it is a split-screen pane and a resized browser window, and it is where a layout that assumed 360px breaks.

## Foldables

Folding devices are detected by **viewport segments**, not by width or user agent:

- `@media (horizontal-viewport-segments: 2)` — two panes side by side with a hinge between. Two-column layouts put their gutter on the hinge, using `env(viewport-segment-*)` to measure it. A card, a table row or an image never straddles the fold.
- `@media (vertical-viewport-segments: 2)` — a book fold laid flat. Nothing interactive sits on the crease: the primary action moves above it.

The same rules serve any folding device, of any generation, because nothing here names one.

## Safe areas

Every full-bleed surface — the app header, the bottom bar, the footer, a modal — pads with `env(safe-area-inset-*)`. The system exposes `--mt-gutter`, which is `space-4` or the inset, whichever is larger, so a rounded corner, a camera cutout or a home indicator never clips content. This is applied to all four edges, because in landscape the inset is on the sides.

## Viewport height

Use `100svh` for a full-height shell. `100vh` counts browser chrome that may not be displayed and pushes fixed bottom elements below the fold. When the on-screen keyboard opens, the layout must not trap the focused field behind a sticky bar — scroll it into view on focus.

## Touch and pointer

- **44px minimum** for every interactive target where `pointer: coarse`, applied by the stylesheet. Where a target cannot grow — a link inside a paragraph — the spacing around it grows instead.
- **24px minimum** spacing between adjacent targets on touch, so a mis-tap costs nothing.
- **Hover styles live inside `@media (hover: hover)`.** On a touch device a tap otherwise leaves the hover state stuck until the next tap, which users read as a broken button.
- `touch-action: manipulation` on controls removes the 300ms double-tap-zoom delay; `-webkit-tap-highlight-color: transparent` removes the grey flash, and the focus ring replaces it.
- **Focus is for keyboards.** `:focus-visible` shows the ring for keyboard and switch users and hides it for taps. Never remove it for everyone.
- **A mouse still needs the same layout.** Nothing in this system requires hover to be discoverable: a control that only appears on hover does not exist on a tablet.

## Going back

- **Every screen has a URL.** A detail view, a filter, an open modal that a user would expect back to close — each is a route. Where they are not, the system back gesture closes the whole application instead of the panel, which is the single most common failure on a phone.
- The in-app back control is a link to the parent screen with a label naming the destination. It never calls `history.back()` unconditionally: a user arriving from a notification or a bookmark has nothing to go back to.
- It mirrors under RTL; the system gesture and the mouse's back button keep working alongside it.
- **Unsaved work warns before back discards it** — a quotation being drafted, a form partly filled.

## Motion

All motion is short and functional: 120ms on colour, no movement on hover. `prefers-reduced-motion: reduce` collapses every transition and animation to near zero, which the stylesheet applies globally — motion is never the only way a change is communicated.

## What is verified and what is not

The viewport figures above are published device specifications. The rules themselves are built on web platform features — viewport segments, safe-area insets, pointer and hover queries, `svh`, reduced motion — so they also cover devices that have not shipped yet, because none of them names a device.

**Nothing here has been run on physical hardware.** Before launch, verify on: a folding phone opened and closed, a tablet in both orientations, a phone with a home indicator, and a desktop browser at 280px, 768px, 984px and 1440px. The 984px check is the one most likely to be skipped and the one most likely to fail.

## Motion

Motion in this system marks a change an operator must not miss. It is never decorative.

- **Nothing flashes more than three times per second.** The Alert flash runs at 1.67Hz, twice, then stops — half the WCAG 2.3.1 seizure threshold. This is a hard limit, not a preference: a faster flash can trigger a seizure.
- **Nothing loops forever** except the loading skeleton, which stops when its content arrives.
- **Motion is never the only signal.** Remove every animation and each state is still expressed in colour, icon and words.
- **`prefers-reduced-motion: reduce` disables all of it**, globally, from one rule. A person who asked their device for less motion gets an interface that does not move.
- **Durations:** 180–320ms for a change of state, 1.2s for the alert flash, 120ms for a colour transition. Nothing slower — an operator clearing a hundred shipments should never wait on an animation.
- **Nothing moves on hover.** A row that shifts under the cursor is a mis-click waiting to happen.
