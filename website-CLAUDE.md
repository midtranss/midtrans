<!--
  Copy this file to the ROOT of the MIDTRANS website repository, named
  CLAUDE.md, before starting work there. Claude Code reads it on every turn,
  so these rules hold for the whole job rather than only the first prompt.

  If that repository already has a CLAUDE.md, append the sections below.

  The design system itself is a clone away:
      git clone https://github.com/midtranss/midtrans /tmp/mt-ds
  Read /tmp/mt-ds/design-system/README.md and the five files in
  /tmp/mt-ds/design-system/guidelines/ before writing anything.
-->

# MIDTRANS website — working rules

Scope: the public web properties. `mid-trans.com` is the canonical host;
`midtrans.org` is the corporate site on the same server. The platform
(`app.midtrans.net`) is a different job with its own rules.

## Production is live

- Never deploy, never edit a live database, never work straight on production.
  Staging first, always.
- Work on a branch. Stop and report before any step that leaves this machine.
- If something looks risky, stop and explain the risk instead of proceeding.

## Additive only — this one is absolute

- **No page, route, path, text, translation, image or asset is ever deleted.**
  An old URL is 301-redirected, never removed.
- **No redirect chains.** Every redirect is a single hop.
- **No bulk redirect to the home page.** A redirect goes to the page that
  replaces it, or it does not exist.
- Do not rebuild a feature beside itself. Read it first, then fix it.

## The design system

Every property loads the same three files and nothing below that layer is
re-themed per property:

```
tokens.css
components/bundle.css
fonts/Cairo-Variable.ttf
```

What differs between properties is **which components they use**, never what
those components look like. A button on the corporate site and a button in the
ERP are the same button. Public sites lead with the marketing set (Hero,
ServiceCard, TradeLaneCard, CTABlock, Footer, Contact) and carry at most one
`surface-inverse` band per screen.

Key values — the full table is in `/tmp/mt-ds/HANDOFF.md` §2:

| | |
| --- | --- |
| Brand | `brand-accent` `#007dc5` for graphics, rules and display type ≥24px |
| Fills under small white text | `brand-primary` `#0074b7` — `#007DC5` measures 4.43:1 and fails |
| Links | `brand-link` `#0069a8` |
| Radii | 4 / 8 / 12 / 999 |
| Spacing | 4px grid: 4 8 12 16 24 32 48 64 |
| Latin type | `"Helvetica Neue", Helvetica, Arial, "Liberation Sans", system-ui, sans-serif` |
| Arabic type | Cairo, exclusively |
| Contrast | 4.5:1 body · 3:1 large text, borders, focus rings (large = ≥24px, or ≥18.66px bold) |
| Favicon | `midtrans-app-icon-512.png`, `theme_color: "#007DC5"` |

Never write a raw hex value. Every colour comes from a token.

## The company name

Three forms, reproduced exactly — letters, capitals and spacing are all part of
the name:

| Form | Where |
| --- | --- |
| `MIDTRANS SHIPPING AND SERVICES` | Legal and commercial documents, letterhead, the footer's legal line |
| `Midtrans Shipping And Services` | Running text, page titles, email signatures, metadata. The capital **A** in "And" is part of the name |
| `المتوسط للشحن و الخدمات - ميدترانس` | All Arabic content, in full, including the hyphen and the transliteration |

**It is "AND", never "&".** The ampersand exists in the drawn logo artwork,
which is historic and stays; written text never copies it. Two of the four
forms currently live on the site use "&" and are wrong on that ground alone.

Short references: **MIDTRANS** in capitals, or **ميدترانس**. Never "Midtrans
Shipping", never "MTS", never an invented abbreviation, and never the name
translated into French, German, Turkish, Chinese or Swedish — Arabic is the
only translated form there is.

> **Open decision — do not settle it yourself.** An SEO brief proposes that
> every `<title>` end in `| MIDTRANS`. The card above assigns page titles to
> `Midtrans Shipping And Services`. These conflict. Khaled decides, and the
> card is edited first; until then the card stands.

## Figures are sourced, never generated

No rate, transit time, customs or duty cost, route, schedule, capacity,
acceptance or delivery date appears unless operations confirmed it — including
in placeholder, demo and seed content.

Where a value is unknown, render the condition in its place: "Confirmed on
booking", "Subject to carrier schedule", "Pending customs assessment". Never
`0`, `—`, `TBD`, or a greyed sample figure.

**No superlatives**, in any locale, in any channel, including meta
descriptions and structured data: best, largest, cheapest, fastest,
guaranteed, number one, world-leading. State the verifiable fact instead —
the founding year, the services operated, the lanes served, the offices held.

## Seven locales, and Arabic

EN · AR · FR · DE · TR · ZH · SV. Arabic is a first-class locale, not a
translation layer.

- Every page, route, form, error, email template and structured-data block
  exists in all seven locales, **or the locale is not offered for that page**.
  A partial locale is worse than an absent one.
- The language switcher **preserves context**: same page in the target locale,
  keeping path parameters, query state and scroll position. It never drops the
  user on the home page.
- Each locale carries its own `hreflang` alternate, its own canonical and its
  own localised metadata. `lang` is set on `<html>` for every locale.
- Arabic sets `dir="rtl"` on `<html>`, not on a wrapper.
- **Logical properties only** — `margin-inline-start`, `inset-inline-end`,
  `padding-block`. Never a second stylesheet for RTL, and never mirroring by
  overriding `left`/`right`. The system's own `bundle.css` has 101 logical
  properties and zero physical ones; keep it that way.
- Numbers, dates, weights and currencies are formatted per locale — but the
  digits of a reference number never are. A booking, AWB, B/L or container
  number is reproduced exactly as issued, in Western digits, in every locale
  including Arabic.

## Domains and canonical

`midtrans.org` and `mid-trans.com` resolve to the same IP.

**The choice is already made in the code**: the live `index.html` declares
`https://www.mid-trans.com/` as canonical and its `hreflang` alternates point
there. So `mid-trans.com` is the canonical host, and `midtrans.org` must
301-redirect to it or serve its own distinct content. It cannot serve the same
pages.

Canonical and `hreflang` are set once at the server, not per page.

`trustbycompass.com` is a separate project, excluded by the owner. It never
loads this system.

Three named properties have **no DNS record** — `chat.midtrans.org`,
`desk.midtrans.net`, `mira.midtrans.net`. Design for them if asked, but never
write copy or documentation implying they exist.

## Company facts — never paraphrase

Founded in **Damascus, 1998**. Head office in **Dubai**.

| Office | Address | Numbers |
| --- | --- | --- |
| Head office — Dubai, AE | Deira, Port Saeed, Al Makateb Building, Office No 611 | Tel `+971 4 271 4480 / 1` · Mob `+971 55 292 8560` |
| Syrian office — Damascus, SY | Halponi, Mouslam Al Baroudi Street, 2nd Floor | Tel `+963 11 9067` · Mob `+963 933 383 858` |

WhatsApp `+963 944 334 338`.

A footer, letterhead or contact page naming only one city is wrong. Print both.
Telephone numbers are `tel:` links on every surface and stay in Western digits
in Arabic.

> **Open decision.** The live site states the founding year three different
> ways — 1998, 1960 (family heritage) and "since 1970". This system says 1998
> throughout. Do not invent a reconciling phrasing: Khaled decides, and the
> site follows.

## Mira on the website

Mira is **synthetic**, and the illustrated mark `mira-avatar.svg` is her image
— never a photograph. `mt-avatar` carries no border, no fill and
`object-position: center`; the mark is already a disc.

Wherever she appears, including the launcher, the name **Mira** and the role
**MIDTRANS logistics assistant** appear together. The stylesheet prints a
visible error under any identity block missing the role.

She is **never presented as an employee** — no team page, no staff directory,
no signature, no named contact. She never states a rate, transit time, duty or
acceptance; the claims rules govern her replies exactly as they govern a page.

## Reporting

After every change, run the repo's own checks — build, lint, typecheck — and
verify the routes and pages you touched. Report exactly what passed, what
failed, and what you did not test. Do not report completion without evidence
from code, logs, tests or files.

"Not tested" is a legitimate answer. A guess is not.
