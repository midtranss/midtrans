# Assistant

Mira: the MIDTRANS logistics assistant, her identity block, the conversation, and the point where she hands over to a person.

Compose `mt-assistant__id` (the `mt-avatar` image plus `mt-assistant__name` and `mt-assistant__role`) above a `mt-chat` of `mt-msg` items, with `mt-composer` pinned at the foot.

**You provide:** the portrait file, the messages, and the handoff action.

## The mark

Mira's avatar is the **illustrated mark** — a blue disc, a headset, simple eyes and a smile. `mira-avatar.svg` is the source on every surface; it is vector, so it is crisp at every size. Use it as delivered: never recoloured, never cropped into, never redrawn, never replaced with an initial, a robot glyph or an emoji.

`mt-avatar` sets `object-fit: contain`, `object-position: center`, and **no border and no fill**. The mark is already a disc on a transparent ground, so a border or a background draws a second ring around it. Sizes are 32, 40, 64 and 96px — the identity block uses `--lg`, message rows use the 40px default.

Prefer the SVG over `mira-avatar.png`: the PNG carries a transparent margin, so the same box renders the disc visibly smaller.

A photographic portrait was used first and has been **retired**. Mira is synthetic, and a photographic human face beside a reply presents a synthetic persona as a member of staff. `assets/Mira/README.md` records the reversal and what followed from it.

The file lives in the **Mira** asset group and is referenced from there, so every surface loads the same mark and a change reaches all of them at once.

## The label is mandatory

The illustrated mark makes Mira's nature legible; the label states it. Both, not either — the mark alone still leaves "who am I talking to" to inference, and inference is what a customer acts on.

Wherever Mira is introduced — the conversation header, her first message, a notification she sends, the chat launcher — the name **Mira** and the role **MIDTRANS logistics assistant** appear with the portrait, in `mt-assistant__id`. Use `mt-assistant__id--inline` where space is tight; **never drop the role**.

This is enforced, not trusted: the stylesheet prints a visible error under any `mt-assistant__id` that has no `mt-assistant__role`, so a surface missing it fails in review instead of shipping.

Where the avatar repeats on each message row, it carries `alt="Mira, MIDTRANS logistics assistant"` rather than repeating the visible label every time.

Mira never claims to be a person, never signs off with a human name, and never says "I've booked it" for something a person has to confirm. **She is never presented as an employee** — not on a team page, not in a staff directory, not in a signature, not as a named contact.

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
