# Icons

The MIDTRANS logistics icon set: sixteen line marks at 24×24, `fill="none"`, 1.5px stroke, round caps and joins.

**One file: `midtrans-icons.svg`** — an SVG sprite holding one `<symbol>` per icon, with ids `mt-ship`, `mt-aircraft`, `mt-truck`, `mt-container`, `mt-package`, `mt-warehouse`, `mt-scale`, `mt-document`, `mt-customs-stamp`, `mt-shield-check`, `mt-route`, `mt-dashboard`, `mt-clock`, `mt-search`, `mt-calculator`, `mt-arrow-end`.

**Ink.** Every symbol strokes in `currentColor` and has no fill, so an icon takes the colour of the text around it. That only works when the sprite is **inlined into the document** and referenced with `<use href="#mt-ship">`. Loaded through an `<img>` it renders black and cannot be themed — that is the one wrong way to use this file.

**Sizing.** 24px in the interface, 20px inside a table row or small button, 32–40px at stroke 2 for a service card or empty state. Nothing below 20px: the 1.5px stroke breaks up.

**Direction.** `mt-arrow-end` is the only directional mark and mirrors under `dir="rtl"`. The modes — ship, aircraft, truck — and every other icon are non-directional and must never be flipped, exactly like the logo.

These were drawn for this system against the subjects MIDTRANS's own design direction names. No licensed icon library was in use. If one is adopted later, replace this sprite and keep the ids.

## The checksum in the index is not the checksum of this file

`design-system.json` records this sprite as 4,506 bytes with sha256 `ca373e92…`,
while the file here is 4,241 bytes with `202346d3…`. They are the same sixteen
symbols with the same geometry: the asset store serialises SVG on upload, so
`<path … />` comes back as `<path …></path>`. Re-uploading this exact file
returns that same 4,506-byte blob, which is how we know the pair is consistent
rather than stale — the index describes what the store holds, and this file is
the source before that normalisation. Nothing to reconcile; edit this file and
re-upload if the set changes.
