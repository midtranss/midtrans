# Hero

The opening block of a public page: one headline, one sentence, one primary action.

Compose `mt-hero` → `mt-hero__copy` (`mt-hero__eyebrow`, `mt-hero__title`, `mt-hero__lede`, `mt-hero__actions`) with an optional `mt-hero__aside`.

**You provide:** the copy per locale, and the aside content — a KeyValue of verifiable facts, or an image.

**The eyebrow names the page's subject**, not a slogan: "Sea freight", "Jebel Ali", "Customs clearance". It is the `label` style and is uppercased by the stylesheet, so pass it in sentence case.

**The headline states what MIDTRANS does and where.** "Container shipping from Syria to Europe and the Gulf" — a service and a geography, which is also what makes the page findable. Never a claim: no "fastest", "leading", "best rates". One `mt-hero__title` per page, and it is the page's only `<h1>`.

**The lede is one sentence that adds a fact the headline did not carry** — the ports, the equipment, that clearance is in-house. Not a restatement.

**Actions: one primary, one secondary, never more.** The primary is the conversion for that page.

**The aside is proof, not decoration.** Verifiable facts in a KeyValue read better and load faster than a photograph. If it is an image, it is real freight operations, and it is dropped below 768px rather than scaled — `mt-hero__aside` is `display: none` there. Mobile performance outranks the picture.

**Do not** put a quotation form in the hero, do not stack two heroes on a page, and do not add a gradient, a globe graphic or a network animation behind it.
