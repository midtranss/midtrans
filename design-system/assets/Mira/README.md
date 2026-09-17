# Mira

The assistant's avatar and the chat mark.

| File | What it is |
| --- | --- |
| `mira-avatar.png` | The avatar running in the app today: a blue disc, a headset, simple eyes and a smile. 800×800, transparent margin. |
| `mira-avatar.svg` | The same mark as vector, and the source the PNG was drawn from. Scales to any size. |
| `midtrans-chat-mark.png` | The company mark — the wings and the wheel — on a transparent ground, used on the team-chat launcher disc. |

## The decision

**The photographic portrait is Mira's image.** The owner chose it over the illustrated avatar, and the trade-offs were put to them before the choice: that a photographic face becomes unreadable at 24–32px, that it is a raster at one resolution rather than vector, and that a human face beside a reply reads as a person replying.

**The label is therefore mandatory, not recommended.** Wherever Mira is introduced — the conversation header, her first message, a notification she sends, the launcher — the name **Mira** and the role **MIDTRANS logistics assistant** appear with the portrait. This is not a footnote to be trimmed for space: it is the thing that stops a customer believing an operator promised them a rate or a date. The stylesheet prints a visible error under any identity block that omits the role, so a surface cannot ship without it by accident.

Where the avatar repeats inside a conversation, it carries `alt="Mira, MIDTRANS logistics assistant"` rather than repeating the visible label on every row.

### Files

| File | Status |
| --- | --- |
| `mira-portrait.jpg` | **Mira's avatar.** 256 × 256, the portrait as supplied. This is the `mt-avatar` source on every surface. |
| `mira-avatar.png` / `.svg` | The illustrated headset avatar the app ships today. Kept as the record of what is currently live, and as the fallback for any surface the portrait cannot serve. |
| `midtrans-chat-mark.png` | The company wings-and-wheel mark, for the **team** chat launcher — not Mira's. |

### Still to settle before launch

- **Provenance.** If the portrait is a real employee, her agreement to have her face used for automated replies. If it is synthetic, it must not be presented anywhere as a named member of staff.
- **Resolution.** The file is 256 × 256. That covers every avatar size the system uses at 2× — 32, 40, 64 and 96px need 192px at most — with 64px to spare. It does **not** cover a larger use: a profile header, a press page or print. Supply a 512px or 1024px original before any of those.
- **Small sizes.** At 24–32px a photographic face carries far less than an illustrated mark. The portrait is still legible there, but if a surface needs to be read at a glance in a dense list, the illustrated avatar remains the better mark and is kept for exactly that case.

## Ink and use

The illustrated avatar carries its own colours — a blue gradient disc with `#EAF6FF` headset and `#0B2B45` features — and is used as delivered on any ground in either theme. It is never recoloured, never cropped into, and never redrawn.

`midtrans-chat-mark.png` is the company wings-and-wheel mark and belongs to the **team** chat launcher, not to Mira. Do not use the two marks interchangeably: one is the company, one is the assistant.
