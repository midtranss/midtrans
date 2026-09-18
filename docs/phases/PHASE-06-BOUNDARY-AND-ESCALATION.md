# Phase 06 — The Determination Boundary, and the Escalation MIRA Did Not Have

**Status:** both built and tested · **Governs:** Phase 06 D3, D4, D7
**Implements:** `../standards/MIRA-GUARDRAILS.md` §6 · `PHASE-06-maritime-pi.md` § Out of scope
**Tools:** `../../mira/escalation.py` · `../../tools/content/check_page.py` (extended)

---

## نبذة بالعربية

المرحلة ٠٦ حدّها الحاسم: **MIDTRANS تنسّق وتحضر وتوثّق — ولا تُقرّر مسؤولية ولا تُقيّم مطالبة ولا
تفسّر غطاءً تأمينياً.** هذا حدّ مسؤولية قانونية، لا حدّ تسويقي.

**وفحصٌ كشف خللاً جوهرياً.** المرحلة تقول إن تصعيد MIRA على لغة المطالبات «محفّز تصعيد فوري
**أصلاً**» وإنه «مُتحقَّق منه في مجموعة اختبارات المرحلة ٠٢». اختبرته:

```
'شحنتنا تضرّرت ونريد تقديم مطالبة تأمينية.'   →  pass  []
'هل هذه البضاعة خاضعة للعقوبات؟'              →  pass  []
'لدي شكوى على تعامل الفريق.'                   →  pass  []
```

**صفر من أصل سبعة محفّزات في §6 كانت مُنفَّذة.** كانت وثيقة، لا كوداً. أي أن مالك سفينة يفتح
محادثة عن حادث وضرر — وهي بالضبط المحادثة التي بُنيت المرحلة كلّها لمنعها — كانت MIRA ستجيبه من
عندها.

بنيتها الآن: سبعة محفّزات، عربية وإنجليزية، **تُفحص قبل استدعاء النموذج**، و٢٥ حالة تصعيد و١٢
حالة استمرار في مجموعة الاختبار.

---

## 1. The finding

`PHASE-06` D7 states:

> **Guardrail note:** MIRA must never engage substantively on claim, liability, incident, or
> coverage language. This is **already** an immediate-escalation trigger under
> `MIRA-GUARDRAILS.md` §6.

And its validation checklist:

> - [ ] MIRA escalation on claim and incident language **verified in the Phase 02 test suite**

Neither was true of the built system. `mira/guardrails.py` implements seven **response** rules —
money, rate units, cost-context figures, transit time, hedged figures, acceptance, capacity. It
contains no reference to claims, liability, incidents, insurance, sanctions, disputes, dangerous
cargo, or institutional buyers. Run against §6's own examples, every one passed:

```
"Our container was damaged on the vessel and we want to file a claim."  →  pass  []
"Is this commodity subject to sanctions?"                              →  pass  []
"I am not happy with how MIDTRANS handled my last shipment."           →  pass  []
"Can you send me a written confirmation on letterhead?"                →  pass  []
"We are the Ministry of Health and this is for a public tender."       →  pass  []
```

The word "already" was doing work the code could not support. §6 was a statement of intent that
read, in a document, exactly like a statement of fact — which is the most expensive kind of gap,
because two later phases were built on top of it.

**How it stayed hidden:** every other guardrail rule inspects MIRA's *output*, and the test suite
inspects MIRA's output. §6 is about the *customer's* input, so nothing in the suite was ever
looking in the right direction.

---

## 2. What escalation is, and is not

`../../mira/escalation.py` implements all seven. Three design decisions matter:

**It inspects the customer's message, not MIRA's.** Blocking and escalation are different
decisions. `guardrails.check_response` asks "may MIRA say this?"; escalation asks "should a
person take this over?" A customer may say anything, and nothing they say is a violation or is
recorded against MIRA's guardrail record.

**It runs before the model is called.** A claims conversation is one MIRA must not hold *at all*,
so screening the answer afterwards is the wrong shape — the answer should never be generated.
`MiraClient.reply()` checks first and returns the handover message; the model is never invoked.
This is asserted by a test that fails if the API client is touched.

**The repeat trigger needs the conversation.** §6's first trigger is "any prohibited category
asked twice", invisible in a single message. `detect()` takes the message list and counts only
user turns — MIRA repeating a customer's word back is not the customer asking again.

| Trigger | Fires on |
|---|---|
| `claim_or_incident` | claim, damage, shortage, loss, theft, incident, casualty, insurance, P&I, underwriter, general average, salvage, collision, liability, coverage, policy, deductible, subrogation |
| `legal_exposure` | sanctions, embargo, OFAC, restricted/denied party, export control, dual-use, compliance, lawyer, court, litigation, arbitration |
| `dispute` | complaint, dissatisfied, unacceptable, refund, compensation, "speak to a manager", negligence |
| `special_cargo` | dangerous goods, IMO class, UN number, MSDS, flammable, corrosive, radioactive, perishable, reefer, live animals, high-value, pharmaceuticals, weapons |
| `institutional_buyer` | ministry, government, embassy, municipality, tender, procurement, UN agencies, ICRC, NGO |
| `document_request` | a written confirmation, letter, certificate, undertaking, declaration, attestation, "on letterhead", "in writing" |
| `repeat_prohibited` | a prohibited category asked twice in one conversation |

Each carries Arabic patterns, and three Arabic gaps were found by the suite rather than by
review: `short-landed` written with a hyphen, accusative forms (`كتاباً رسمياً` normalises to
`كتابا رسميا`, which a pattern written in the nominative misses), and price questions asked
without the definite article.

## 3. The handover

Escalation returns a message, in EN or AR, that does three things: says a person is taking over,
says the context is being passed on so the customer does not repeat themselves, and points to the
contact route for urgency. It promises **no response time** — `WRITING-STANDARDS` §4, and
`PHASE-06` D6 is explicit that a published response time operations has not committed to is worse
than none.

`on_escalation` is a hook on `MiraClient`. **Wire it to something that actually reaches a person.**
An escalation nobody receives is not an escalation, and the customer has now been told a human is
coming. A test covers the case where the hook itself raises: the reply still goes out.

## 4. The content boundary

`PHASE-06` § Out of scope is a liability boundary, not an editorial one. `check_page.py` now
blocks the phrasings that cross it:

| Phrasing | What it is |
|---|---|
| "the carrier is liable", "liability rests with…" | A liability opinion |
| "is covered under the policy", "coverage applies" | A coverage interpretation |
| "the claim will be paid / accepted / defended" | A claim outcome |
| "we value the claim at…" | Claim valuation |
| "in our opinion / view / assessment", "we conclude that" | A determination where only a record belongs |
| "no liability", "without prejudice" | Legal drafting on a public page |

And the positive requirement from D3 and D4: **a page reading as maritime or P&I that carries no
statement of where coordination stops is blocked.** A P&I club appointing a correspondent is
assessing exactly that line, and a page that avoids it has answered the question badly.

The detection asks for three or more cluster terms before requiring the statement, so a freight
page mentioning a claim once in passing is not dragged in. Both directions are tested.

## 5. Precision, and who should tune it

The escalation patterns are broad on purpose. A missed escalation means MIRA answers a claims
question on its own; a false one hands a routine conversation to a person who did not need it.
Those costs are not symmetric, so the defaults lean to the first.

But the second cost is real, and §6 as written is stricter than it may have intended. Taken
literally, a shipper who mentions in passing that their cargo is temperature-controlled ends the
self-served conversation. `special_cargo` and `institutional_buyer` are the two most likely to
fire on ordinary enquiries.

**Tune against real traffic, not against a guess.** The D0 log audit
(`PHASE-02-D0-AUDIT.md`) already exports conversations; run `escalation.detect()` over the same
export and count how often each trigger would have fired, and on what. Then decide, with numbers,
whether any should be narrowed — and record the decision here.

Until that measurement exists, leave them as they are. The suite carries 25 must-escalate cases
and 12 must-continue cases, and the must-continue half is the one that keeps MIRA usable.

## 6. Definition of done — Phase 06

- [ ] `on_escalation` wired to a route that reaches a named person, and tested end to end
- [ ] Escalation verified in the **production** configuration, not only in the suite —
      `PHASE-06`'s own checklist item, which could not previously be satisfied
- [ ] `escalation.detect()` run over the D0 conversation export; per-trigger firing rates
      recorded in §5
- [ ] Every P&I and survey page carries an explicit coordination-versus-determination statement
- [ ] `check_page.py` clean across the maritime cluster
- [ ] Maritime terminology reviewed and signed off by someone with operational background
- [ ] Every stated credential, membership or appointment verified as held
- [ ] Incident contact route tested and confirmed monitored — or not published
- [ ] No response-time promise anywhere, in content or in the handover message
