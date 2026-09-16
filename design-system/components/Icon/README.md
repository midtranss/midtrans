# Icon

The MIDTRANS icon set: sixteen line marks drawn for freight operations, at 24px on a 1.5px stroke.

Every icon is a 24×24 viewBox, `fill="none"`, `stroke="currentColor"`, `stroke-width="1.5"`, with round caps and joins. Because the stroke is `currentColor`, an icon takes the colour of the text beside it — put it inside an element carrying `ink-body`, `ink-muted`, `brand-link` or a `status-*` colour and it follows.

**Use it inline, not as an image.** The set ships as an SVG sprite at `assets/Icons/midtrans-icons.svg` with one `<symbol>` per icon, id `mt-<name>`. Inline the sprite once per document, then reference an icon:

```html
<svg class="mt-icon" aria-hidden="true"><use href="#mt-ship" /></svg>
```

An `<img>` pointing at the sprite cannot inherit colour and will render black. That is the one thing to avoid.

**The set**

| Group | Icons |
| --- | --- |
| Modes | `ship`, `aircraft`, `truck` |
| Cargo and facilities | `container`, `package`, `warehouse`, `scale` |
| Documents and customs | `document`, `customs-stamp`, `shield-check` |
| Operations | `route`, `dashboard`, `clock`, `search`, `calculator` |
| Direction | `arrow-end` |

**Sizing.** 24px is the only size for interface icons. 20px is allowed inside a table row or a `mt-btn--sm`; nothing smaller, because a 1.5px stroke breaks up below 20px. For a hero or an empty state, scale to 32 or 40px and raise the stroke to 2 so the weight still reads.

**Meaning, not decoration.** An icon appears where it saves reading — a mode column, a document state, a service card — never as an ornament beside every heading. An icon that carries meaning on its own needs 3:1 against its ground; `ink-body`, `ink-muted`, `brand-link` and every `status-*` colour hold that in both themes. An icon that repeats the adjacent label is decorative: mark it `aria-hidden="true"`. An icon that stands alone needs an accessible name on the control that holds it.

**Never pair an icon with colour alone to express a status.** The word comes too — that rule is in StatusBadge and it applies here.

**Direction.** `arrow-end` is directional and mirrors under `dir="rtl"`, which it does automatically when drawn inline in an RTL container only if you transform it — so flip it with `transform: scaleX(-1)` in an `:dir(rtl)` rule, or use a separate start-pointing symbol. Every other icon in this set is non-directional and must not mirror: `ship`, `aircraft` and `truck` point the way they are drawn in both directions, exactly as the logo does.

**This set is new, not inherited.** No MIDTRANS icon library existed when it was drawn, so these were made for this system against the subjects the brand's own design direction names. If a licensed set is adopted later, replace the sprite and keep the names.
