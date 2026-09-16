# Writing Standards

**Status:** BINDING. Applies to every published word — website copy, guides, FAQs, MIRA
responses, meta descriptions, alt text, and email templates.

---

## نبذة بالعربية

قواعد الكتابة لكل محتوى MIDTRANS المنشور.

الصوت: تنفيذي أمريكي في الشحن الدولي بخبرة تتجاوز ٢٥ سنة — عملي، استشاري، واثق بلا مبالغة.

ممنوع: المبالغة، الادعاءات غير المدعومة، الحشو التسويقي، أسلوب الذكاء الاصطناعي العام،
وأي رقم تشغيلي مخترَع (سعر، مدة، تكلفة جمركية، قبول شحنة).

هذه القواعد مأخوذة من الوثيقة الأصلية ومُبقاة كما هي لأنها كانت أقوى جزء فيها.

---

## 1. Voice

Write as a highly experienced American logistics executive with 25+ years in international
freight forwarding, maritime operations, global trade, business development, and market-entry
consulting.

**Tone:** professional, authoritative, practical, consultative, commercially intelligent, human,
helpful.

The reader should finish a page thinking:

> "This company understands my business."

Not:

> "This website is trying to sell me something."

### The practical test

Before publishing any page, ask: **could a competent competitor have written this exact page?**

If yes, it is not finished. Every page must carry something specific that comes from MIDTRANS
having operated in Damascus, Latakia, Tartous, Dubai and Jebel Ali since 1998 — a procedural
detail, a sequencing insight, a common failure mode, a documentation nuance.

Generic is the failure state. Not wrong — generic.

---

## 2. Forbidden words and claims

### Never use

`Best` · `Largest` · `Number One` · `World Class` · `Industry Leading` · `Premier` ·
`Revolutionary` · `Cutting Edge` · `Guaranteed` · `Unmatched` · `Leading provider` ·
`One-stop shop` · `Seamless` · `Hassle-free`

### Never claim

- Market leadership, ranking, or size superiority of any kind
- Guarantees of outcome, delivery, clearance, or acceptance
- Certifications, memberships, or partnerships that are not held and verifiable
- Client names or case details without written permission
- Coverage, capacity, or capability that MIDTRANS does not actually have

### Why this is enforced strictly

Unsupported superlatives do three kinds of damage at once: they are legally exposed, they are
invisible to a professional buyer who has read the same words on forty other freight websites,
and they are actively down-weighted by search engines and AI systems assessing content quality.

There is no upside to trade off against.

> **Note:** the source document that preceded this programme contained the phrase *"one of the
> largest specialised websites"* in its own closing section, in direct violation of its own
> forbidden-word list. This is a normal drift pattern. Copy review must check the list explicitly
> rather than relying on the writer remembering it.

---

## 2a. Never draw a line between "human" and "artificial"

**Decided by MIDTRANS, 2026-09-16.** In anything a customer reads, and in the Arabic prose of
this programme, work is reviewed, checked, or taken over by **فريق العمل — the team**. Not by
"a human", not "after human review", not "a human colleague will take over".

| Do not write | Write |
|---|---|
| بعد مراجعة بشرية | **بعد مراجعة فريق العمل** |
| حكم بشري | **حكم فريق العمل** |
| A human will review this | **A colleague from the team will review this** |
| Handed to a human | **Handed to the team** |

**Why.** The distinction is ours, not the customer's. A customer asking about a shipment does not
want to be told which side of an internal boundary their question has crossed; they want to know
someone is dealing with it. Naming the boundary also makes the assistant the subject of the
sentence, and MIDTRANS is what should be the subject.

### The line this does *not* cross

This is a rule about **which word to use for the people who do the work.** It is not permission
to let MIRA present itself as a person, and the two are easy to confuse.

`D4-feature-inventory.md` finding 1 records — as a High-severity finding, observed in live output
— that MIRA describes itself as a member of the MIDTRANS team with no disclosure. That finding
stands. So all of the following remain in force and are **not** relaxed by this section:

- `../../mira/SYSTEM-PROMPT.md`: never sign off with a personal name or a job title
- `kb-seed.yaml` `never_say`: not a member of staff, not a name, not a title
- `MIRA-GUARDRAILS.md` §6: the seven triggers still hand the conversation over

"The team is looking at this" is true, says nothing false about who is typing, and is what a
customer actually needs. "I'll ask my colleague in the Damascus office" — said by software about
itself, as though it were sitting next to them — is the thing finding 1 is about. The first is
required; the second is still prohibited.

**Internal engineering language is exempt.** Function names, code comments, and the escalation
standards may say `human` where the distinction is the whole point of the sentence — the rule is
about what is read, not about what is implemented.

---

## 3. Anti-AI-writing rules

Content must not read as machine-generated. Specifically prohibited:

| Pattern | Example of the failure |
|---|---|
| Triadic filler | "efficient, reliable, and cost-effective solutions" |
| Empty transitions | "In today's fast-paced global economy…" |
| Self-referential structure | "In this article, we will explore…" |
| Hollow conclusions | "In conclusion, choosing the right partner is essential." |
| Restating the heading | A section that spends its first paragraph rephrasing its own title |
| Uniform paragraph rhythm | Every paragraph three sentences long |
| Keyword stuffing | The target phrase repeated past the point of natural use |
| Hedge-everything | Copy so qualified it commits to nothing and teaches nothing |

### Required instead

- Open with the substance. No throat-clearing.
- Vary sentence and paragraph length. Real expertise has rhythm.
- Prefer the concrete over the abstract: name the port, the document, the step, the failure mode.
- Say the useful thing even when it is inconvenient — that is what earns trust from a buyer.
- Use short sentences for the points that matter most.

---

## 4. Factual limits — hard boundary

**Never publish, state, estimate, or imply:**

- Freight rates or price ranges of any kind
- Transit times, sailing schedules, or ETAs
- Customs duties, taxes, or clearance costs
- Acceptance of any specific cargo, route, or commodity
- Space, equipment, or capacity availability
- Any operational commitment or delivery promise
- Regulatory determinations for a specific shipment

This applies to hedged phrasing exactly as it applies to direct statements. "Typically around",
"usually takes about", and "expect roughly" are all violations.

**What to publish instead:** explain the *factors* that determine the answer. A page that
explains what drives a rate is more useful to a professional buyer than a number that is out of
date the week after publication — and it converts better, because it demonstrates competence.

See `MIRA-GUARDRAILS.md` for how this rule applies to conversational surfaces.

---

## 5. Structure

| Element | Requirement |
|---|---|
| H1 | One per page, describing the page's actual subject |
| Heading depth | H2 for major sections, H3 beneath. No skipped levels. |
| Opening | Answer the page's core question within the first 100 words |
| Paragraphs | 2–5 sentences. Break up anything longer. |
| Tables | Use for anything comparative or procedural |
| Lists | Use for sequences and requirements — not as a substitute for explanation |
| Closing | A clear, specific next step. Never a generic "contact us today". |

---

## 6. Arabic content

- Proper RTL layout throughout — not a mirrored English page
- Font: **Cairo**
- Arabic is **written**, not translated. A machine-translated Arabic page fails this standard.
- Terminology must match what Syrian and Gulf trade professionals actually use in the field
- Numerals, dates, and units follow the conventions of the target audience
- Bidirectional text (Latin terms, port codes, HS codes inside Arabic sentences) must render
  correctly — this is a QA checklist item, not an assumption

### Other languages

English is the source of record. FR, DE, TR, ZH and SV are localisations of approved English
content — reviewed by a speaker with domain familiarity, never published raw from machine
translation. See `LANGUAGE-SCOPE.md` for which content gets which languages.

---

## 7. Review checklist

Every page, before publish:

- [ ] Forbidden-word list checked explicitly against the copy
- [ ] No unsupported claim of leadership, size, or guarantee
- [ ] No rate, transit time, customs cost, acceptance, or capacity figure — including hedged
- [ ] Every factual claim traceable to a verifiable source
- [ ] Contains at least one insight a competitor could not have written
- [ ] Anti-AI-writing patterns from §3 absent
- [ ] Opens with substance; closes with a specific next step
- [ ] Arabic version is written, RTL-correct, and set in Cairo
- [ ] Reviewed by a named human, recorded with date
