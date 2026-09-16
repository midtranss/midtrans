# Assistant

Mira: the MIDTRANS logistics assistant, her identity block, the conversation, and the point where she hands over to a person.

Compose `mt-assistant__id` (the `mt-avatar` image plus `mt-assistant__name` and `mt-assistant__role`) above a `mt-chat` of `mt-msg` items, with `mt-composer` pinned at the foot.

**You provide:** the portrait file, the messages, and the handoff action.

## The portrait

Mira's avatar is a **photographic portrait supplied by MIDTRANS** — square, head and shoulders, navy blazer over a white blouse, a small blue lapel pin, on a light blue-grey background. It is used as delivered and is never redrawn, filtered, cartooned or replaced with an initial, a robot mark or an emoji.

`mt-avatar` crops it to a circle with `object-position: center 22%`, because the head sits above the centre of the frame; a plain `center` crop cuts the chin. Sizes are 32, 40, 64 and 96px — the identity block uses `--lg`, message rows use the 40px default.

The file lives in the **Mira** asset group and is referenced from there, so every surface loads the same crop and a change reaches all of them at once.

## The label is mandatory

**A photographic human face beside a message reads as a person.** This was weighed against an illustrated avatar and the portrait was chosen deliberately; the label is the condition that makes that choice safe.

Wherever Mira is introduced — the conversation header, her first message, a notification she sends, the chat launcher — the name **Mira** and the role **MIDTRANS logistics assistant** appear with the portrait, in `mt-assistant__id`. Use `mt-assistant__id--inline` where space is tight; **never drop the role**.

This is enforced, not trusted: the stylesheet prints a visible error under any `mt-assistant__id` that has no `mt-assistant__role`, so a surface missing it fails in review instead of shipping.

Where the avatar repeats on each message row, it carries `alt="Mira, MIDTRANS logistics assistant"` rather than repeating the visible label every time.

Mira never claims to be a person, never signs off with a human name, and never says "I've booked it" for something a person has to confirm.

## What Mira may answer, and what she may not

She answers on **services, coverage, documentation, process, and arithmetic she can show her working for** — volume, volumetric weight, container fill, HS classification candidates.

She does **not** state a rate, a transit time, a duty or customs cost, space availability, or acceptance of a shipment. Those come from operations, and the claims section governs her replies exactly as it governs a page. Her refusal is useful, not a wall: she says why, gives what she does know, names what is still missing, and offers the handoff.

**The handoff is a real control**, not a phrase. `mt-handoff` carries the remaining gap in words and a button that sends the thread to the team. A conversation that reaches the boundary and stops there has failed.

**She asks only what the quotation needs** — commodity, origin and destination, incoterm, weight and dimensions, ready date, special handling. Not one question more.

## The conversation

Messages from Mira carry her avatar and sit on `surface-card`; the customer's sit on `brand-soft` and reverse direction, which mirrors correctly under `dir="rtl"` because the row uses `row-reverse` on the inline axis.

**The typing indicator is three dots at 1.4s**, under the flash threshold, and it stops entirely under `prefers-reduced-motion`. It carries an `aria-label`, because a screen reader gets nothing from three animated dots.

**The composer is sticky at the foot** with safe-area padding, and the focused input must not end up behind it when the on-screen keyboard opens.

**Arabic:** Mira replies in the customer's language, using the `ar-*` styles, and the formal plural. Reference numbers stay in Western digits.
