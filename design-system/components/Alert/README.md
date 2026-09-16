# Alert

A notice about the page or the record in front of the user, placed where the consequence is.

Use `mt-alert` with `--info`, `--success`, `--warning` or `--danger`, containing `mt-alert__body` with an `mt-alert__title` and an `mt-alert__text`.

**You provide:** the role — `role="alert"` for errors that interrupt, `role="status"` for everything else — the copy, and any action, as an `mt-btn--quiet` after the text.

Variants carry the same meanings as StatusBadge: `--info` is running, `--warning` is waiting on someone, `--success` is closed as intended, `--danger` is closed unintentionally or failed.

**The title states what happened and names the record**; the text says what to do next: "The Turkish authority requested the certificate of origin. Attach it to release the shipment." Never publish a reason you do not have — if the carrier gave no cause, say the response gave none rather than guessing one.

Place the alert directly above the content it concerns: at the top of the form it blocks, or inside the card for the record it names. A page-wide error above the header, far from the field that caused it, is not actionable.

**Do not** use an Alert for a permanent explanation — that is help text on the Field. Do not stack more than two, and do not auto-dismiss a `--danger` alert.
