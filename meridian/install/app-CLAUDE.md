<!--
  Copy this file to the ROOT of the MIDTRANS platform repository, named
  CLAUDE.md, before starting work there. Claude Code reads it on every turn,
  so these rules hold for the whole job rather than only the first prompt.

  If that repository already has a CLAUDE.md, append the sections below to it
  instead of replacing it.
-->

# MIDTRANS platform — working rules

## Production is live

`app.midtrans.net` serves real shipments, real customers and real money.

- Never deploy, never run a migration against a live database, never edit data.
- Work on a branch. Stop and report before any step that leaves this machine.
- Prefer a dry run, a backup and a written rollback over a fast fix.
- If something looks risky, stop and explain the risk instead of proceeding.

## Additive only

Do not remove or rename an existing route, page, template, column, translation,
asset, link, widget or behaviour unless I have explicitly approved that removal
in this conversation. If a feature already exists, read it first, then fix it;
do not rebuild it beside itself.

Do not copy code from older versions of this project. Use them as references
for appearance, workflow and behaviour only.

## The Meridian theme

One attribute on the root element decides the appearance:

```html
<html data-skin="meridian">   <!-- the new design system -->
<html>                        <!-- everything as it is today -->
```

`data-theme` (light/dark) is a separate axis and is not touched by this work.

The full contract is in `meridian/install/INSTALL.md`. Two points are not
negotiable:

- **The control is gated twice**: it is only rendered for super admins, AND
  the endpoint that saves it authorizes super admin and returns 403 otherwise.
  A control hidden in the UI is not a permission.
- **The role is checked at render, not only at save**, so a demoted admin falls
  back to the current appearance on the next page load.

The preference is per-account. A super admin's choice changes their own
rendering and nobody else's. Making it platform-wide is a separate decision
and needs my explicit approval — that is the point at which customers see it.

## The dashboard changes in three ways only

Colour, type, size. Structure, order, elements and behaviour stay exactly as
they are. If something moves, that is a bug, not a theme.

## Arabic

Cairo, exclusively, bound by `lang="ar"`. RTL is handled by logical properties
(`margin-inline-start`, `inset-inline-end`, …). Never add a second stylesheet
for RTL and never mirror by overriding physical properties.

Locales in parity: EN, AR, FR, DE, TR, ZH, SV. The language switcher keeps its
context across a switch.

## Figures are sourced, never generated

No rate, transit time, customs or duty cost, route, schedule, capacity,
acceptance or delivery date is displayed unless it came from a confirmed
operational source. This includes placeholder, demo and seed data.

Where a value is not yet known, render the condition in its place —
"Confirmed on booking", "Subject to carrier schedule", "Pending customs
assessment" — never `0`, `—`, `TBD` or a sample figure.

No superlatives anywhere, in any locale: best, largest, cheapest, fastest,
guaranteed, number one.

## Mira

The assistant always carries her label: "Mira · MIDTRANS logistics assistant".

## Reporting

After every change, run the relevant tests, build, lint and type checks, and
verify the routes and pages you touched. Report exactly what passed, what
failed, and what you did not test. Do not report completion without evidence
from code, logs, tests or files.
