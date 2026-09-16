# Card

Groups one record — a quotation, a shipment, a service, an account — into a bordered panel.

Compose `mt-card` from `mt-card__head` (holding `mt-card__title` and optional `mt-card__meta`, with a StatusBadge on the opposite side), `mt-card__body`, and `mt-card__foot` for actions.

**You provide:** the heading level that fits the page outline — `mt-card__title` styles the text, it does not choose the tag — the content, and any Button or StatusBadge inside it.

A card at rest carries `border-subtle` and no shadow; it is separated from the page by its border, not by a fill. Cards sit on `surface-sunken` where a page needs them distinguished from the background. Padding is `space-5`, dropping to `space-4` below 768px.

Put the record's identifier in `mt-card__meta` and the state in a badge in the head, so a grid of cards can be scanned down one edge.

**One card is one record.** If the content is a form, a table or a page section, it is not a card — use the page's own layout. Nesting cards inside cards means the hierarchy is wrong.

**Do not** make the whole card a link. Give it explicit actions in `mt-card__foot`, so keyboard users get real targets and the card's text stays selectable.
