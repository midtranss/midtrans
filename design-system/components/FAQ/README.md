# FAQ

Questions customers actually ask, answered without promising anything unconfirmed.

Use `mt-faq` of `mt-faq__item`, each a `<button class="mt-faq__q">` with `aria-expanded` and `aria-controls`, followed by the `mt-faq__a` panel it names.

**You provide:** the questions and answers per locale, and the toggle handler. The stylesheet hides a panel whose button reads `aria-expanded="false"`, so the state lives on the button and the markup stays honest.

**The question is the customer's words, not the company's.** "How long does shipping take?", not "Transit time policy". That is also what matches a search query.

**One question per item, phrased as a question, ending in a question mark.**

**The first item may open by default; the rest are closed.** Never open all of them — an accordion with everything expanded is a page, and the reader loses the map.

**Answers obey the claims rules exactly.** A question about price or transit time is answered with the process, not a number: "Transit time depends on the sailing, the season and clearance at destination. We confirm it against the carrier's schedule at booking." Never an average, never a range, never "typically 20–25 days".

**Two to three sentences.** A longer answer is a page, and the FAQ links to it.

## Structured data

Every FAQ block ships a matching `FAQPage` JSON-LD with one `Question` per item, the answer text identical to what is rendered. Two rules:

- **Do not mark up an answer the page does not display.** Search engines treat a mismatch as cloaking.
- **The structured data is per locale** and sits on that locale's page, with the same `inLanguage` as the document.

This is what puts MIDTRANS answers into search results and AI answers directly, which is the reason the block exists and the reason its answers must be accurate.

**Keyboard and assistive technology:** the question is a real `<button>`, so it is reachable and operable by keyboard, and `aria-expanded` announces the state. The plus/minus sign is `aria-hidden` — it is decoration on top of the state the button already carries. Never build this from `<div>`s with click handlers.
