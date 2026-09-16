# Toast

A transient confirmation that an action succeeded or failed, and the motion patterns that draw attention without harming anyone.

Put a `mt-toast-region` once per page and append `mt-toast` elements to it, each with `mt-toast--success` or `mt-toast--danger`, an icon, the message, and a dismiss button.

**You provide:** the message, the timer, and the removal.

## When a toast, when an Alert

A **toast** confirms something the user just did, and it is safe to miss — "Quotation sent". It disappears. An **Alert** states a condition the user must act on, and it stays until the condition is resolved. A failed save is an Alert beside the form, not a toast that vanishes before it is read.

`role="status"` for success — the screen reader announces it when convenient. `role="alert"` for failure — it interrupts. Never the reverse.

**Dismiss must be reachable.** A toast that auto-hides in 4 seconds is unusable for someone reading with a magnifier: give every toast a close button, and do not auto-hide a `--danger` toast at all.

## The alert flash

Add `data-flash` to an Alert that arrives while the user is already on the page — a customs hold that came in, a booking that failed. It pulses a ring in the alert's own colour twice, over 1.2 seconds, and stops.

**It pulses at 1.67Hz — half the three-per-second seizure threshold in WCAG 2.3.1** — and it runs once, never on a loop. Do not shorten the duration to make it "snappier": that is what pushes the rate into the unsafe band.

**The flash is an addition, never the message.** Remove the animation and the alert still says everything: colour, icon, title and text. Under `prefers-reduced-motion: reduce` the flash does not run at all, and nothing is lost.

## The other motion in this system

| Pattern | What it marks | Duration |
| --- | --- | --- |
| `data-flash` on an Alert | A notice that just arrived | 1.2s, once |
| `data-changed` on a StatusBadge | A status that just changed | 200ms |
| `data-just-completed` on a timeline step | A milestone just reached | 320ms |
| `mt-toast` entrance | A confirmation appearing | 200ms |
| `mt-skeleton` | Content loading | Sweeps until content arrives |
| `mt-table--enter` | A register loading | 180ms, first 8 rows only |
| `:active` scale on touch | A tap landed | Instant |

**Only the first eight table rows animate.** Animating a hundred-row register turns an operational screen into a light show and delays the first readable frame.

**A skeleton, not a spinner.** A skeleton shows the shape of what is coming and keeps the layout from jumping. A spinner says only "wait".

**Everything here is switched off by `prefers-reduced-motion: reduce`**, globally, in the stylesheet. That is a promise: no MIDTRANS interface moves for a person who asked it not to.
