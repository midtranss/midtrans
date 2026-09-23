# Mira

The assistant's mark and the chat mark.

| File | What it is |
| --- | --- |
| `mira-avatar.svg` | **Mira's mark.** A blue disc, a headset, simple eyes and a smile. Vector, so it is crisp at every size. This is the `mt-avatar` source on every surface. |
| `mira-avatar.png` | The same mark at 800×800 with a transparent margin. Use only where an SVG cannot be served. |
| `mira-portrait.jpg` | A photographic portrait, 256×256. **Retired — see below.** Kept as the record of a decision that was reversed. |
| `midtrans-chat-mark.png` | The company mark — the wings and the wheel — for the **team** chat launcher. Not Mira's. |

## The decision, and why it was reversed

Mira was first given a photographic portrait. That has been reversed: **Mira is
synthetic, and the illustrated mark is her image.**

The reason is not aesthetic. A synthetic persona must never be presented as a
named member of staff, and a photographic human face does exactly that — it
reads as a person who works here, whatever the surrounding text says. The
illustrated mark makes the same point the label makes, in the image itself.

Three things followed from the reversal, all of them improvements:

- **The resolution question disappeared.** The portrait was 256×256, which
  covered the avatar sizes at 2× and nothing larger; a profile header, a press
  page or print needed an original nobody had. The mark is vector: there is no
  size it cannot serve.
- **Small sizes got better, not worse.** At 32px a photographic face is an
  indistinct blob. The mark's headset silhouette still reads. Measured side by
  side before the change.
- **No consent is owed.** No real person's face is being used to answer
  customers automatically.

`mira-portrait.jpg` stays in the repository because deleting it would erase the
record. It is not referenced by any surface and must not be.

## Using the mark

- **Prefer the SVG.** The PNG carries a transparent margin, so the same box
  renders the disc visibly smaller. Both are correct; the SVG is tighter and
  sharper.
- **No border and no fill.** `mt-avatar` sets neither. The mark is already a
  disc on a transparent ground, and either one draws a second ring around it.
- **`object-position: center`.** The `center 22%` crop existed because the
  portrait's head sat above the middle of its frame. The mark is centred, and
  the old crop clipped it.
- **Used as delivered on any ground, in either theme.** The mark carries its
  own colours — a blue gradient disc with `#EAF6FF` headset and `#0B2B45`
  features. Never recoloured, never cropped into, never redrawn.
- Sizes are 32, 40, 64 and 96px. The identity block uses `--lg`; message rows
  use the 40px default.

## The label is still mandatory

Wherever Mira is introduced — the conversation header, her first message, a
notification she sends, the launcher — the name **Mira** and the role
**MIDTRANS logistics assistant** appear with the mark.

The illustrated mark makes her nature legible; the label states it. Both, not
either. The stylesheet prints a visible error under any identity block that
omits the role, so a surface cannot ship without it by accident.

Where the mark repeats inside a conversation, it carries
`alt="Mira, MIDTRANS logistics assistant"` rather than repeating the visible
label on every row.

**Mira is never presented as an employee.** Not on a team page, not in a staff
directory, not in a signature, not as a named contact. She does not claim to be
a person, does not sign off with a human name, and does not say "I've booked
it" for something a person has to confirm.

`midtrans-chat-mark.png` is the company wings-and-wheel mark and belongs to the
**team** chat launcher. Do not use the two interchangeably: one is the company,
one is the assistant.
