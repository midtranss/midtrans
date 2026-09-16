# Multilingual and RTL

MIDTRANS publishes in seven languages: English, Arabic, French, German, Turkish, Chinese and Swedish. Arabic is a first-class locale, not a translation layer.

## Parity

- Every page, route, form, error message, email template and structured-data block exists in all seven locales, or the locale is not offered for that page. A partial locale is worse than an absent one.
- The language switcher preserves context: it moves to the same page in the target locale, keeping path parameters, query state and scroll position. It never returns the user to the home page.
- Each locale carries its own `hreflang` alternate, its own canonical URL and its own localised metadata. The `lang` attribute is set on `<html>` for every locale.
- Numbers, dates, weights and currencies are formatted per locale, but the digits in a reference number never are: a booking or AWB number is reproduced exactly as issued, in Western digits, in every locale including Arabic.

## Arabic and direction

- Arabic pages set `dir="rtl"` on `<html>`, not on a wrapper. Everything below inherits it.
- Set Arabic text in the `arabic` family through `ar-heading-1`, `ar-body` and `ar-body-sm`. These carry taller leading than the Latin styles because Cairo's ascenders and descenders need it; using `body` for Arabic produces crowded lines.
- Write every layout with logical CSS properties — `margin-inline-start`, `padding-inline-end`, `inset-inline-start`, `border-inline-start`, `text-align: start` — so that one stylesheet serves both directions. Never write a separate RTL stylesheet and never mirror with `transform: scaleX(-1)`.
- Directional icons mirror: back and forward arrows, breadcrumb chevrons, progress and shipment-timeline direction. Non-directional icons do not: clocks, checkmarks, warnings, the vessel, aircraft and truck marks, and any logo.
- Tables in RTL keep the reference column first in reading order, which places it at the right edge. Numeric columns stay aligned on the digit, which means `text-align: end` in both directions.
- Latin runs inside Arabic text — a port code, a container number, an email address — are wrapped so the bidirectional algorithm cannot reorder them, and are set in the `mono` family where they are reference numbers.
- Test every Arabic page at 320px width. Cairo at `ar-body` with its 30px leading is the case that breaks a layout tuned for 15px Helvetica.
