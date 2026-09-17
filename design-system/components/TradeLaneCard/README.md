# TradeLaneCard

A corridor MIDTRANS operates: origin, destination, modes, equipment.

Compose `mt-lane` → `mt-lane__route` (two `mt-lane__place` spans with `mt-lane__arrow` between), `mt-lane__modes`, a `KeyValue` of lane facts, and one quiet action.

**You provide:** the places as "City, CC", the modes, the equipment, and the link.

**Transit time and rate are never printed here.** They carry `data-pending` — "Per carrier schedule", "Quoted on request" — because a lane page is read by people deciding whether to ship, and a transit time on a marketing page is read as a commitment. Both depend on the sailing, the season and the booking. This is the rule that makes lane pages safe to publish at scale.

**Equipment and modes are facts and do belong here**: 20GP, 40GP, 40HC, LCL, groupage, sea-plus-land. They say what MIDTRANS can actually move without promising when.

**The arrow is `arrow-end` and it mirrors under `dir="rtl"`** — the route must read origin-first in both directions, so this is the one icon in the set that flips.

**One card is one lane in one direction.** A lane operated both ways is two cards, because the equipment, the clearance and the documentation differ.

**Do not** add a flag graphic, a map thumbnail, or a "from $X" figure. Do not list a lane the company has not actually moved cargo on.
