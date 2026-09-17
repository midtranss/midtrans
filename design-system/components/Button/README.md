# Button

Triggers an action; a link that navigates is an `<a>` carrying the same classes.

Use `mt-btn` plus exactly one variant class. One `mt-btn--primary` per view — the single action the page exists for. `mt-btn--secondary` takes every other committed action, `mt-btn--quiet` takes navigation and low-weight actions inside tables and cards, and `mt-btn--danger` takes destructive actions such as cancelling a booking or voiding an invoice. Add `mt-btn--sm` inside table rows and toolbars.

**You provide:** the element (`<button type="button">`, `<button type="submit">` or `<a href>`), the label, and `disabled` or `aria-disabled="true"` where the action is unavailable.

**Label it with a verb and its object** in sentence case — "Request a quotation", "Attach packing list" — never "Submit", "OK" or "Click here". Keep the label to four words; the locale with the longest translation sets the width, so test the German and Turkish strings.

Focus draws a 2px `border-focus` ring at a 2px offset. Do not remove it. Hover on the primary variant deepens the fill to `surface-inverse` and moves nothing.

A disabled button never stands alone: put the reason beside it in `body-sm` `ink-muted` ("Attach the packing list to continue"). Do not disable a submit button to express a validation failure — show the Field error instead.

**On a link, `aria-disabled` is not enough.** ARIA describes state; it does not suppress behaviour. An `<a href>` marked `aria-disabled="true"` still navigates on click and on Enter, so a control that looks unavailable stays fully operable. The stylesheet stops the pointer, which the keyboard walks straight past. Either **drop the `href`** — a link with nowhere to go is inert, and `role="link"` with `aria-disabled` keeps it in the reading order — or cancel activation in the handler. Prefer a `<button disabled>` wherever the action is not really navigation: the platform already does all of this.

**Do not** put two primary buttons side by side, do not colour a button with `brand-accent` (white on it measures 4.43:1), and do not use a button where a link is meant.
