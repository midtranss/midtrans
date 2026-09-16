# Claims and figures

This section is binding on the website, the platform, quotation and email templates, and the logistics chatbot. It exists because a freight forwarder's published numbers are read as commitments.

## Never generated, only sourced

Prices, transit times, customs and duty costs, routes, schedules, capacity, acceptance decisions and delivery dates are shown only when they come from a confirmed operational source — a rate sheet, a carrier schedule, a booking, a signed quotation. No interface, template or chatbot reply may estimate, interpolate or illustrate one of these figures, including in placeholder or demo content.

Where a value is not yet known:

- Show the state, not a number: "Confirmed on booking", "Subject to carrier schedule", "Pending customs assessment".
- Set that text in `ink-muted` at `body-sm`, in the position the value will occupy, so the layout does not shift once the figure arrives.
- Never show `0`, `—`, `TBD` or a greyed sample figure in place of a real one.

## Quotations

- Every quoted figure carries its currency, its unit basis (per shipment, per kg, per CBM, per container type) and a validity date. A figure without all three is incomplete and does not render.
- Charges excluded from the quotation are listed explicitly rather than implied.
- A quotation that has expired is shown with `status-neutral` and the word "Expired", and its figures remain visible and unaltered for the record.

## The chatbot and RFQ replies

- The chatbot answers about services, coverage, documentation and process. For anything in the list above it collects the request and hands off; it does not answer with a figure.
- It asks only the questions the quotation actually needs — commodity, origin and destination, incoterm, weight and dimensions, ready date, special handling — and not one more.
- It never states or implies acceptance of a shipment.

## Superlatives

"Best", "largest", "cheapest", "fastest", "guaranteed", "number one" and unsupported market-leadership claims do not appear in any locale, in any channel, including meta descriptions and structured data. State the verifiable fact instead: the founding year, the services operated, the lanes served, the certifications held.
