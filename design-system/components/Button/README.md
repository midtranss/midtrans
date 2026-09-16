# Button

Triggers an action; a link that navigates is an `<a>` carrying the same classes.

Use `mt-btn` plus exactly one variant class. One `mt-btn--primary` per view — the single action the page exists for. `mt-btn--secondary` takes every other committed action, `mt-btn--quiet` takes navigation and low-weight actions inside tables and cards, and `mt-btn--danger` takes destructive actions such as cancelling a booking or voiding an invoice. Add `mt-btn--sm` inside table rows and toolbars.

**You provide:** the element (`<button type="button">`, `<button type="submit">` or `<a href>`), the label, and `disabled` or `aria-disabled="true"` where the action is unavailable.

**Label it with a verb and its object** in sentence case — "Request a quotation", "Attach packing list" — never "Submit", "OK" or "Click here". Keep the label to four words; the locale with the longest translation sets the width, so test the German and Turkish strings.

Focus draws a 2px `border-focus` ring at a 2px offset. Do not remove it. Hover on the primary variant deepens the fill to `surface-inverse` and moves nothing.

A disabled button never stands alone: put the reason beside it in `body-sm` `ink-muted` ("Attach the packing list to continue"). Do not disable a submit button to express a validation failure — show the Field error instead.

**Do not** put two primary buttons side by side, do not colour a button with `brand-accent` (white on it measures 4.43:1), and do not use a button where a link is meant.
