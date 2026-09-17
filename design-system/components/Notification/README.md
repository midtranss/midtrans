# Notification

The notification centre: what happened, to which record, and when.

Use `mt-notes` as a `<ul>` of `mt-note` items with `mt-note--info`, `--success`, `--warning` or `--danger`, each holding an icon, `mt-note__body` (title, text, `mt-note__ref`) and `mt-note__time`.

**You provide:** the events, the reference, the relative time, and `data-unread="true"` while unread.

**Every notification names its record.** `mt-note__ref` carries the booking, quotation or invoice number in `mono` — a notification an operator cannot trace to a record is noise.

**Variants mean what they mean everywhere in this system:** info is running, warning is waiting on someone, success is closed as intended, danger is closed unintentionally or overdue. Use the same icons as the matching StatusBadge state.

**The title is what happened, in three or four words.** The text adds the one fact needed to decide whether to act now. Neither restates the other.

**Unread is a `brand-soft` background, not a dot alone** — a dot at the edge of a dense list is missed.

**Time is relative up to a week** ("12 min", "2 h", "3 d"), then absolute. Never "just now" for something an hour old.

**Do not notify what the user did themselves.** A confirmation of your own action is a Toast that disappears; a notification is for something that happened while you were elsewhere.

**Never put a rate, a duty or a transit time in a notification.** The claims rules apply here exactly as on a page — notifications are forwarded and screenshotted more than any other surface.
