# Activating Meridian on the platform

A staged rollout. After step 3 the theme exists on the server and **nobody can
see it**. After step 5 exactly one group can: super admins, each for their own
account. Customers and ordinary users are never offered the choice and never
render the theme, even by accident.

This guide is deliberately stack-agnostic: it states the contract, not the
framework. Every placeholder is written `«like this»`.

If an agent is doing the wiring, copy `app-CLAUDE.md` (beside this file) into
the platform repository root as `CLAUDE.md` first. It carries the rules below
plus the standing ones — production safety, additive-only, Arabic, and the
figures that are never generated — so they apply to every turn rather than
only the first instruction.

---

## What decides the appearance

One attribute on the root element:

```html
<html data-skin="meridian">   <!-- the new system -->
<html>                        <!-- everything as it is today -->
```

`data-theme` (light/dark) is a separate axis and is not touched by any of this.

The attribute is the **only** switch. That is what makes the rollout reversible:
nothing else in the app changes.

---

## Step 0 — Get the package

The design system lives on a branch, not on `master`. Clone that branch:

```sh
git clone -b claude/design-system-extraction-onzs1r \
    https://github.com/midtranss/midtrans /tmp/mt-ds
```

Once the branch is merged, a plain `git clone` will do. Until then a plain
clone gives an empty directory.

## Step 1 — Serve the files

Copy `meridian/` into the app's public assets:

```
«public»/meridian/meridian.css
«public»/meridian/fonts/cairo.woff2
«public»/meridian/midtrans-icons.svg
```

Keep the directory shape. `meridian.css` references the font at
`fonts/cairo.woff2` relative to itself.

## Step 2 — Link it

One line in the layout, **after** the app's existing stylesheets:

```html
<link rel="stylesheet" href="/meridian/meridian.css">
```

Deploy this on its own and stop. Nothing renders differently — every rule in the
file is scoped to `[data-skin="meridian"]`, and no element carries that
attribute yet. This step is safe to ship to production with users on it, and it
is worth shipping alone: if anything at all changes visually, the problem is
visible before any switch exists.

## Step 3 — Store the preference

One nullable column, on the users table:

```sql
ALTER TABLE «users» ADD COLUMN ui_skin VARCHAR(16) NULL;
```

Nullable with no default, so every existing row keeps the current appearance
without being written to. Rollback is `DROP COLUMN ui_skin`.

Accepted values: `'meridian'`, or `NULL`/`'default'` for the current
appearance. Reject anything else at the write endpoint — this value is
interpolated into an HTML attribute.

## Step 4 — Render it

Wherever the layout emits `<html>`:

```
if «current_user» is authenticated
   and «current_user».is_super_admin
   and «current_user».ui_skin == 'meridian':
       emit  <html data-skin="meridian" …>
else:
       emit  <html …>          # unchanged
```

**The role is checked at render, not only at save.** If a super admin is later
demoted, their stored preference stops applying on the next page load without
anyone having to clean up the column.

No JavaScript is involved in this step, which is the point: the attribute is in
the first byte of HTML, so there is no flash of the old theme.

## Step 5 — The control

In the appearance section of settings, for super admins only:

```
Appearance
( ) Current            ← the platform as it is today
( ) Meridian           ← the new design system
```

Two independent gates, both required:

1. **Render gate** — the control is only emitted for super admins. A user who
   is not a super admin never receives this markup.
2. **Authorization gate** — the endpoint that saves it authorizes super admin
   and returns `403` otherwise.

Gate 1 alone is not a permission. A hidden control is still reachable by anyone
who can send a request; gate 2 is what actually restricts the feature.

```
POST «/settings/appearance»
  authorize: «current_user».is_super_admin      → else 403
  accept:    skin ∈ { 'meridian', 'default' }   → else 422
  persist:   «current_user».ui_skin = (skin == 'meridian' ? 'meridian' : NULL)
```

### Flipping it live

Optional. Without it the choice applies on the next page load, which is
perfectly acceptable. With it, the page changes under the user immediately:

```html
<script src="/meridian/install/meridian-theme.js" defer></script>
```

```js
// in the settings screen, after the save succeeds
const res = await fetch('«/settings/appearance»', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', «…CSRF…» },
  body: JSON.stringify({ skin })
});
if (res.ok) MidtransTheme.preview(skin);
```

`MidtransTheme.preview()` only touches the attribute on the live page. It does
not persist and it does not authorize — the server did both, above. Calling it
before the save succeeds would show a user a state the server rejected.

---

## Scope: whose appearance changes

As written, a super admin's choice changes **their own** rendering. Everyone
else is unaffected. This is the safe default and the one to ship: the blast
radius is a single account, and you can evaluate the theme against real data,
in production, with no one else exposed.

To make it a platform-wide default later, move `ui_skin` from the user row to
the settings table and read it in step 4 for every session instead of the
current user's own value. That is a deliberate second decision, not an
accident of this one — and it is the point at which customers see the change.

---

## Rolling back

| Undo | How | Effect |
| --- | --- | --- |
| One account | Set its `ui_skin` to `NULL` | That account is back on the next load |
| The feature | Remove the control and the render condition | Nobody can reach it; CSS still inert |
| Everything | Delete the `<link>` and the `meridian/` directory | The app is byte-for-byte what it was |

No migration is needed to roll back, and no data is lost by rolling back: the
column holds a preference, not a record.

---

## Validating it

Run these against a super-admin account and an ordinary account.

**Isolation — the step that matters most.** With the `<link>` deployed and no
attribute set:

- Open any existing screen and compare it against the same screen before the
  deploy. It must be identical, not merely similar.
- Check a screen with the app's own animations, and one with Arabic content.

**The gate:**

- An ordinary user's settings page does not contain the control.
- `POST «/settings/appearance»` as an ordinary user returns `403`, and their
  `ui_skin` is unchanged in the database.
- An invalid value returns `422` and persists nothing.
- A super admin who sets `meridian`, then has the role removed, renders the
  **current** appearance on the next load.

**The theme:**

- Light and dark both render, and `data-theme` still switches them.
- Arabic pages render in Cairo and mirror to RTL.
- A dashboard screen has the same structure, order and behaviour as before —
  only colour, type and size differ. Anything moving is a bug, not a theme.

---

## The rules that travel with the theme

Unchanged from `../README.md`, repeated because they are binding on whoever
wires this in:

- **The dashboard changes in three ways only: colour, type, size.**
- **No rate, transit time, duty or acceptance is displayed unless operations
  confirmed it.** Render the condition instead.
- **Mira always carries her label**: "Mira · MIDTRANS logistics assistant".
- **Arabic is Cairo**, bound by `lang="ar"`, RTL by logical properties. Never
  add a second stylesheet for RTL.
