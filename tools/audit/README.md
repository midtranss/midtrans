# Conformance checks

Three checks, run against the design system as it stands. They exist because
reading the CSS is not the same as seeing what a browser computes from it —
several of the defects they caught were invisible in the source.

## Running them

    python3 -m http.server 8000 &          # from the repository root
    python3 tools/audit/gen_tokens.py      # tokens.json -> audit-tokens.css
    python3 tools/audit/gen_mounts.py      # previews -> loadable pages
    python3 tools/audit/static.py          # the source text
    node    tools/audit/live.js            # what the browser computes
    node    tools/audit/meridian_proof.js  # the skin's isolation

`live.js` and `meridian_proof.js` take `PW` (the Playwright module path) and
`CHROME` (a browser binary) from the environment when the defaults do not
resolve. In this container:

    PW=/opt/node22/lib/node_modules/playwright \
    CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome node tools/audit/live.js

`gen_tokens.py` writes `audit-tokens.css` at the repository root and `live.js`
mounts each `components/*/preview.html` under `.audit-mounts/`. Both are
throwaway harness files; delete them when you are done.

## static.py — the source

Raw hex outside `tokens.json`; `var()` references that resolve to nothing;
physical (non-logical) properties that would break RTL; the decided values for
`brand-accent`, `brand-primary`, `border-focus` and `status-info`; the radius
scale; Arabic bound to Cairo; the alert flash under the 3Hz seizure threshold;
and every text-bearing component root declaring its own `font-family`.

## live.js — what the browser computes

Every component preview, in both themes, at desktop and phone widths:

- **fonts** — the resolved family on every element holding text
- **contrast** — 4.5:1 body, 3:1 large, against the real composited background
- **taps** — 44px on a coarse pointer
- **focus** — a 2px ring at 3:1 on every focusable element
- **Arabic** — every element holding Arabic text resolves to Cairo

Two things this harness got wrong at first, both worth knowing:

1. It set `data-theme` after load and read styles while the 120ms colour
   transition was still running, which invented 23 contrast failures. The theme
   is now baked into the mount page and transitions are frozen before measuring.
2. Its Arabic check only looked at elements carrying `lang="ar"`, so it missed
   Arabic rendering in Helvetica inside buttons, badges, table headers and
   labels. It now walks the whole subtree. Removing the fix in `bundle.css`
   turns up 108 failures, which is how we know the check is not vacuous.

## meridian_proof.js — the skin

Snapshots a legacy component's computed style with the skin off, on, and on in
dark, and fails on any difference; confirms the skin styles its own components
and that `meridian-mt-flash` is actually running.

## gen_meridian.py

Regenerates `meridian/meridian.css` from `tokens.json` and `bundle.css`. Run it
after any change to either, or the skin will keep serving the old values.
At-rules are handled by kind, never by string prefixing: `[data-skin="meridian"]
@keyframes ...` is invalid CSS, and it cost six of the seven animations.
