# AppShell

The frame every operational screen sits in: a sticky header with back and title, the content, and navigation that is a bottom bar on a phone and a side rail from tablet up.

Compose `mt-shell` → `mt-shell__header` (`mt-shell__back`, `mt-shell__title`, optional trailing StatusBadge or action), `mt-shell__main`, and `mt-shell__nav` of `mt-shell__nav-item` anchors.

**You provide:** the title, the navigation items with `aria-current="page"` on the active one, and the back destination.

## Back

**The back button is a real control, not a decoration.** It carries an `aria-label` naming where it returns to — "Back to shipments" — because "Back" alone tells a screen-reader user nothing.

**It navigates, it does not call `history.back()` blindly.** A user who arrived from a link, a notification or a bookmark has no history to pop, and the browser's back would leave the app. Give it an `href` to the parent screen and let it behave like a link; intercept it only when you know the previous screen was yours.

**It mirrors under `dir="rtl"`** — the arrow flips, and the button moves to the right edge, both handled by the stylesheet.

**It never replaces the browser's own back.** On a phone the system gesture, on a desktop the mouse's fourth button and the browser chrome must all still work. That means every screen has a real URL: a detail view opened over a list is a route, not a state variable, or back closes the whole app instead of the panel.

**From 900px up the back button gives way to the side rail** — with a mouse and visible browser chrome, a second back control is noise.

## Layout and the screen

`min-height: 100svh`, not `100vh`. On a mobile browser `100vh` includes chrome that is not there, which pushes the bottom bar below the fold; `svh` does not. When the on-screen keyboard opens, the sticky bottom bar must not cover the focused field — scroll the field into view on focus.

**Safe areas are respected on all four edges** through `env(safe-area-inset-*)`, folded into `--mt-gutter`. That is what keeps the header clear of a camera cutout and the bottom bar clear of a home indicator, on any device with either, including ones not yet released.

**Foldables** are handled by viewport segments, not by device width. Where two horizontal segments are reported, the shell exposes `--mt-fold-gap` so a two-column layout puts its gutter on the hinge instead of straddling it. Nothing interactive is ever placed on the crease.

## Input

Every target in the shell clears 44px on a coarse pointer. Hover styles apply only where `hover: hover` — without that, a tap leaves a button stuck in its hover state until the next tap, which reads as a bug.

**Do not** hide the navigation behind a hamburger on a phone if there are four items or fewer — a bottom bar is one tap, a menu is two. **Do not** put more than five items in the bottom bar. **Do not** make the header taller than it needs to be: on a 320px-tall cover screen the header and bar already spend half the height.
