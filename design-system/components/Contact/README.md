# Contact

The offices, and the persistent rail that keeps contact one tap away on every page.

## Offices

Use `mt-offices` of `mt-office` cards, each with `mt-office__label`, `mt-office__city`, an `<address>`, and `mt-office__lines`.

**Both offices are always shown.** MIDTRANS has a head office in **Dubai** and a Syrian office in **Damascus** — a page, footer or letterhead that names only one city is wrong. The details below are the ones published in the live site's structured data:

| Office | Address | Telephone |
| --- | --- | --- |
| Head office — Dubai, AE | Deira, Port Saeed, Al Makateb Building, Office No 611 | +971 4 271 4480 / 1 · mobile +971 55 292 8560 |
| Syrian office — Damascus, SY | Halponi, Mouslam Al Baroudi Street, 2nd Floor | +963 11 9067 · mobile +963 933 383 858 |
| WhatsApp | — | +963 944 334 338 |

**Every number is a `tel:` link** in the `mono` face with tabular figures, so it dials on a phone and can be checked digit by digit on a desk. Numbers stay in Western digits in Arabic, and the `+` stays at the start of the number — wrap them so the bidirectional algorithm cannot move it.

**The city heading is the place, not the role.** "Dubai, United Arab Emirates", with "Head office" as the label above it.

## The rail

`mt-rail` is the persistent strip of contact actions pinned to the page edge: WhatsApp, call, request a quotation. Each `mt-rail__item` is 44px minimum and carries an `aria-label` naming the action and its target — an icon alone is not a name.

**Three items, at most.** The rail is a shortcut, not a second navigation. It sits on `surface-inverse` so it reads against any page section, and turns `brand-primary` on hover.

**On a phone it moves to the bottom-end corner**, clear of the home indicator through `--mt-safe-bottom`, and it must never overlap an AppShell bottom bar — a page that has one does not also carry the rail.

**WhatsApp is green in most brands; here it is not.** The rail is one colour, because three differently-coloured floating buttons read as an advertisement. The WhatsApp icon carries the recognition.

**Do not** add a chat bubble, a callback form or a cookie banner to the rail, and do not animate it into view on scroll.
