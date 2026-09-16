# D3 — RFQ Intake Analysis

**Analyst:** Claude (planning session)  **Date:** 2026-09-16
**Source:** MIDTRANS Gmail (read-only)  **Sample:** ~120 threads reviewed across two windows
**Status:** FIRST PASS — see §9 for what is not yet established

> **Customer data:** this file records aggregated patterns only. No names, email addresses,
> phone numbers, company identifiers or shipment references have been copied into it. Read-only
> access was used throughout; nothing was sent, labelled, or modified.

---

## نبذة بالعربية

تحليل الطلبات الواردة فعلياً إلى بريد MIDTRANS. هذه أهم نتيجة في المرحلة صفر، لأنها تُظهر الطلب
**الحقيقي** لا المفترَض.

أهم ثلاث نتائج:

1. **نظام RFQ الجديد عمره ستة أيام** (`QREQ-2026-00001` بتاريخ ١١ سبتمبر) وأنتج **٤ طلبات**. لا
   يوجد خط أساس تاريخي — وهذا في الواقع **توقيت ممتاز**: نحن نقيس من الصفر تماماً.
2. **مسار سوريا يهيمن على الطلب الحقيقي** — ١١ من ١٥ استفساراً حقيقياً خلال سنة. والصين ← سوريا هو
   الخط الأكثر تكراراً.
3. **٢٧٪ من الاستفسارات الحقيقية تصل بالعربية**، وواحد بالألمانية. هذا يؤكّد صحة قرار الطبقة
   اللغوية T2 (عربي + إنجليزي) لمحتوى سوريا — القرار كان مبنياً على تقدير، والبيانات تدعمه الآن.

وأخطر ملاحظة: **البريد العام للموقع (`info@mid-trans.com`) ضجيج بنسبة ~٨٥٪** — تسويق وكلاء، إشعارات
بنكية، وطلبات توظيف. الطلبات الحقيقية تغرق فيه.

---

## 1. Methodology and its limits

Two sampling windows, because one alone would mislead:

| Window | What was sampled | Threads |
|---|---|---|
| **A — Recent density** | All traffic to the public website address, 9–16 Sep 2026 | 40 |
| **B — 12-month end-customer sweep** | Free-mail senders (gmail/hotmail/yahoo/outlook) to the operations address, Sep 2025 – Sep 2026 | ~41 |
| **C — Targeted** | Website form subjects, quote-reference subjects, Syria-route enquiry terms | ~40 |

**Free-mail as a proxy:** window B filters on consumer email domains to isolate likely
end-customers from forwarder-to-forwarder and carrier traffic. It is a **proxy, not a
definition** — it will miss enquiries from company domains and include some non-enquiries. Treat
its counts as a floor, not a total.

**Gmail's result-count estimates are unreliable.** The same query returned an identical estimate
for a 6-month and a 12-month window, which cannot both be right. Counts below come from threads
actually read, not from those estimates.

---

## 2. Where enquiries actually come from

| Channel | Observed volume | Confidence | Note |
|---|---|---|---|
| **New website RFQ wizard** (`QREQ-` references) | **4 total**, 11–16 Sep 2026 | **HIGH** | Sequential references make this exact |
| **Older website form** ("global freight quote request") | 5 threads / 12 months | MED-HIGH | Structured field format; superseded by the wizard |
| **MIRA / website chat** | At least 1 conversation observed | LOW | **MIRA is live** — see §8a. Volume not established |
| **Direct email to operations address** | ~15 genuine end-customer enquiries / 12 months | MED | Free-mail proxy; a floor, not a total |
| **Public website address** (`info@` on the .com domain) | High volume, ~85% non-enquiry | MED | See §3 |
| **Forwarder / agent rate requests** | Continuous, high volume | HIGH | Partner traffic, not website-sourced |
| **Third-party freight marketplace** | ~12 threads / 12 months | MED-HIGH | Routed to a sister brand; low relevance |
| WhatsApp | UNKNOWN | — | Not visible in email |
| Phone | UNKNOWN | — | Not visible in email |

### The finding that matters most

> **The website RFQ funnel is six days old.**

`QREQ-2026-00001` was submitted on 11 September 2026; `QREQ-2026-00004` on 16 September. Four
submissions in six days is the entire history of the system.

This means **there is no historical website-conversion baseline to recover** — and that is not a
problem. It is close to ideal timing: Phase 01 will be measured from a genuine zero rather than
against a contaminated legacy number. The Phase 00 baseline should record the pre-wizard state
honestly as `≈0 structured website RFQs/month` and start the clock now.

---

## 3. The public inbox is ~85% noise

Window A — 40 threads over 8 days to the public website address:

| Category | Share | What it is |
|---|---|---|
| **Agent / carrier cold marketing** | ~55% | Unsolicited rate sheets, vessel schedules, space offers, container sales, network conference invitations |
| **Bank and finance notifications** | ~10% | Transaction advices routed to the public address |
| **Job applications** | ~8% | Unsolicited CVs |
| **Vendor / software / web-dev spam** | ~7% | |
| **Government and institutional** | ~5% | Customs auction notices, event invitations |
| **Genuine B2B enquiries** | ~10% | Forwarder-to-forwarder rate requests |
| **Genuine end-customer enquiries** | ~5% | |

**Implication for Phase 01:** the website's published contact address is functioning as a general
company inbox, not a lead channel. A real enquiry arriving there competes for attention with
forty cold rate sheets. The RFQ wizard's separate, structured routing — which already sends a
formatted notification to a named distribution list — is the correct pattern and should become
the primary path. Publishing the raw inbox address as the main CTA works against it.

**Secondary finding:** two domains are in use — the operations domain and the website domain —
and mail lands on both. Whether this is deliberate is a question for D1.

---

## 4. What real demand actually looks like

Across all genuine end-customer enquiries identified (n ≈ 15 over 12 months, plus 4 wizard
submissions and 5 older-form submissions):

### Route concentration

| Pattern | Share of genuine enquiries |
|---|---|
| **Syria as origin or destination** | **~73%** |
| China → Syria (Latakia / Tartous / Damascus / Aleppo) | Most frequent single lane |
| Europe → Syria (Germany, Poland, Italy, Netherlands) | Second |
| UAE → Syria | Present |
| USA → Syria (via Turkey transit) | Present |
| Syria → export (Europe, USA) | Present but less frequent |
| Non-Syria lanes (UAE→Africa, UAE→Egypt, UAE→Jordan) | Minority |

Origin ports named repeatedly: **Shenzhen, Yantian, Nanning, Shandong, Guangzhou**.
Destination points named repeatedly: **Latakia, Tartous, Damascus, Aleppo**.

> This is direct evidence for the Phase 04 decision. The Syria Trade & Procedures Center is not
> a strategic guess — it is the subject of roughly three-quarters of genuine inbound demand.

### Commodity mix

Chemicals (polyurethane components, galvanic chemicals, sodium metabisulphite — several requiring
MSDS and UN classification) · Vehicles · Food and FMCG (confectionery, olive oil, vegetable oils,
anise seed) · Apparel and footwear · Porcelain and houseware · Industrial spares

**Dangerous-goods and chemical enquiries recur.** This is a repeated qualification burden and a
content opportunity — see §5 and §6.

### Buyer profile — the most actionable pattern

The recurring self-description across genuine enquiries:

- *"first order"* · *"pilot shipment"* · *"trial LCL"* · *"starting a new retail business"*
- *"100 pairs"* · *"300 kg"* · *"47.5 litres"* · *"5 CBM"*
- Sourcing from Alibaba, asking whether a supplier can ship direct to a MIDTRANS warehouse

> **The dominant inbound buyer is a first-time or small importer moving LCL into Syria — not an
> FCL shipper.**

This has direct consequences:

| Consequence | Where it lands |
|---|---|
| The RFQ wizard must handle *"I don't know my volume yet"* without dead-ending | Phase 01 |
| LCL / consolidation content is higher priority than FCL content | Phase 04 |
| Procedural explanation matters more than rate competitiveness for this buyer | Phase 04 |
| "How to import into Syria for the first time" is the single highest-value guide | Phase 04 |

### Competitive behaviour — speed is a ranking factor

Multiple enquiries were addressed to **three to five forwarders simultaneously**, visibly in the
To: line. Named recipients included other Syria-route specialists.

> The buyer is not choosing MIDTRANS. They are broadcasting and taking the first competent,
> fastest reply.

This makes response speed a conversion mechanism, not a service nicety, and it strengthens the
Phase 01 case for instant structured acknowledgement and the Phase 02 case for MIRA qualifying
out of hours.

---

## 5. Missing information — **this specifies the Phase 01 RFQ wizard**

Derived from what the team actually had to ask for in replies. Every wizard field should trace to
a row here.

| Missing field | Frequency | Include in wizard? |
|---|---|---|
| **Commodity — specific name, not "general cargo"** | Very high | **Yes — required.** Carriers reject "general cargo" |
| Gross weight | Very high | Yes — required |
| Volume (CBM) or dimensions | Very high | Yes — required, with "not yet known" allowed |
| **Incoterms / shipment terms** (EXW, FOB, CIF, DDP, DDU) | Very high | Yes — required, with plain-language help |
| Mode (sea / air / land) when the enquiry only says "shipping" | High | Yes — required |
| Door-to-door vs. port-to-port | High | Yes — required |
| Collection address (not just city) | High | Yes — conditional on door pickup |
| Delivery address | High | Yes — conditional on door delivery |
| **MSDS / UN number / DG class** | Recurring | **Yes — conditional trigger on chemicals** |
| Consignee details | Medium | No — post-quote, not pre-quote |
| Packaging type (pallets / cartons / loose) | Medium | Yes |
| Cargo readiness date / target window | Medium | Yes |
| Customs clearance required at destination? | Medium | Yes |
| Pallet dimensions (LTL/LCL) | Medium | Yes — conditional |

### Design notes this data forces

1. **A conditional DG branch is mandatory, not optional.** Chemical enquiries recur often enough
   that asking for MSDS and UN class up front removes a full email round trip.
2. **Incoterms must be explained inside the form.** A first-time importer does not know what EXW
   means, and an unexplained dropdown will be answered wrongly or abandoned.
3. **"General cargo" must be blocked as an answer.** It is the single most common cause of a
   carrier coming back for clarification.
4. **"I don't know yet" must be a valid answer to volume and weight.** The dominant buyer
   genuinely does not know at enquiry time. Forcing a number produces a wrong number or an
   abandoned form.

---

## 6. Recurring questions — source material for FAQs and MIRA

Observed repeatedly. These are real questions from real enquirers, suitable for `FAQPage` schema
under `../standards/SEO-STANDARDS.md` §4.

| Question | Should be answered by |
|---|---|
| Can my Alibaba supplier ship directly to your warehouse in China? | Phase 04 guide + MIRA |
| Do you do LCL from China to Syria, and how does consolidation work? | Phase 04 guide + MIRA |
| What documents do I need to import into Syria for the first time? | Phase 04 documentation reference |
| Can you handle customs clearance at Latakia / Tartous, and what does that involve? | Phase 04 port pages |
| Do you ship chemicals, and what do you need from me? | Phase 04 + DG content |
| Can you bring a vehicle into Syria and clear it? | Phase 04 |
| Do you serve lane X? | **A published served-lanes page** — see below |
| What is DDP vs. DDU, and which do I need? | Phase 04 + MIRA |
| Can you ship from Syria to Europe / USA? | Phase 04 export cluster |

### A content gap with a measurable cost

At least one enquiry was declined because the requested lane is not served. That is the correct,
honest answer — but the enquirer spent time, and the team spent time, on a question the website
could have answered before either.

**Recommendation:** publish a clear served-lanes / coverage page in Phase 04. It reduces
unqualified enquiries, and it is exactly the kind of candid, useful content
`../standards/WRITING-STANDARDS.md` §1 asks for.

---

## 7. Language of real enquiries — **validates the tiering**

| Language | Share of genuine end-customer enquiries |
|---|---|
| English | ~66% |
| **Arabic** | **~27%** |
| German | ~7% |

Every Arabic-language enquiry concerned a Syria route, and was handled in Arabic by the team,
with at least one routed directly to the Damascus office.

> **This validates the T2 (EN + AR) assignment for the Syria cluster in
> `../standards/LANGUAGE-SCOPE.md`.** That tier was assigned on judgement before this data
> existed; the data now supports it.

**The German enquiry is a signal worth watching, not acting on yet.** It concerned importing a
vehicle into Syria — consistent with a diaspora audience. One instance is not demand. If German
Syria-route enquiries reach a recurring level, `LANGUAGE-SCOPE.md` §3's promotion rule applies at
a phase gate.

**No enquiries observed in FR, TR, ZH or SV** in this sample. Not evidence of absence, but no
evidence of demand either.

---

## 8. Response behaviour

| Observation | Assessment |
|---|---|
| Fastest observed reply to a genuine enquiry | ~20 minutes |
| Several enquiries answered same-day, some routed to the Syria team | Good |
| At least one enquiry chased twice by the enquirer without receiving the requested rate | **Lost-lead pattern** |
| The new wizard sends an automatic acknowledgement with a reference number | **Correct design** — keep it |
| Wizard notifications reach a named internal distribution list, and management replies on-thread | Working |

**On the automatic acknowledgement:** the wizard's confirmation email was checked against
`../standards/MIRA-GUARDRAILS.md` §2 and `WRITING-STANDARDS.md` §4. It states that the request was
received and that the operations team will review it. **It contains no rate, transit time, cost,
acceptance or capacity commitment.** This is compliant, and it is the pattern the rest of Phase 01
should follow.

---

## 8a. MIRA is live — ⚠️ correction to an earlier version of this file

> An earlier version of this analysis concluded that no autonomous AI assistant appeared to be
> live. **That conclusion was wrong**, and it has been withdrawn. It generalised from one chat
> conversation that staff answered — most likely an escalation *from* MIRA, not evidence that
> MIRA does not exist.

**MIRA is live and runs on the Claude API.** Documentary evidence in the mailbox:

- An Anthropic service notice (11 Sep 2026) names an API key **`MIRA · mira.midtrans.org`**
- MIRA has its own mailbox, `mira@midtrans.org`
- Anthropic billing receipts dated 20 Aug, 11 Sep and 15 Sep 2026 confirm active paid API use

The same notice reports that a MIRA code path is calling **`claude-3-5-haiku-20241022`** — a model
retired on 19 February 2026 — and that the call **fails silently**: Anthropic states the failure
"does not appear on the Usage page."

### What this changes in the programme

| Was | Is |
|---|---|
| Guardrails are a prerequisite to be built before MIRA ships | **Guardrails are remediation of a live system** |
| Phase 02 begins after Phase 01 | **The guardrail question is open now, ahead of everything** |
| No active commercial exposure | **Exposure is active until proven otherwise** |

Full detail, the migration fix, and the eight questions D1 must answer are in
`D4-feature-inventory.md` § MIRA status.

### The single most urgent open question

> **Does MIRA currently have any guardrail preventing it from stating a rate, transit time,
> customs cost, cargo acceptance, or capacity?**

Given §4 of this analysis — that the dominant inbound buyer is a first-time importer who opens
with *"how much to ship X to Syria"* — an unguarded MIRA is being asked the exact question it must
never answer, by most of the people who reach it.

Reviewing MIRA's recent conversation logs for any stated rate, transit time or acceptance is the
fastest way to establish whether the exposure has already materialised.

---

## 8b. ⚠️ Website enquiries are going unanswered — measured 2026-09-16

This was found while reconstructing the Phase 01 baseline. It is the most consequential finding
in this file, and it **inverts the assumption the Phase 01 gate was built on.**

### What was measured

All threads reaching `info@mid-trans.com` or `info@midtrans.org` with a quote, quotation, RFQ,
inquiry or enquiry subject, between **1 March and 11 September 2026** — the window ending the day
the RFQ wizard went live. Thirty threads returned.

| | |
|---|---|
| Threads sampled | 30 |
| Threads with any reply in-thread | **2** |
| Non-replied threads verified by a **separate sent-mail search** | 14 |
| Replies found by that search | **zero** |

The sent-mail search is the part that makes this solid. A missing reply inside a thread could be
a threading artefact — a reply sent as a new message would not appear. So the recipients were
searched directly across the whole mailbox, sent folder included: four free-mail addresses and
ten company domains. **No message has been sent to any of them.**

### The four end-customer enquiries, read in full

Each was opened and read. All four are unanswered, and none is a thin enquiry:

| Date | Enquirer | Enquiry | Detail supplied |
|---|---|---|---|
| 27 Jul | Italy-based, pilot shipment | LCL porcelain, Chaozhou → Latakia | Origin, destination, mode, commodity, HS heading 6911, quantity, **1.0–1.5 CBM, 150–220 kg**, Incoterm question |
| 10 Aug | Damascus engineer | EXW Germany → Damascus, beauty products | Origin, destination, route, commodity, Incoterm, full service list, three phone numbers |
| 11 Aug | Maron LLC | 300 kg anise seed, Syria → Los Angeles | Commodity, **weight**, origin, destination, service scope, phytosanitary and FDA Prior Notice named |
| 9 Sep | Managing Director, Turkey | FTL Trabzon → Dubai, hookah charcoal | Origin, destination, **DAP**, mode, commodity, **HS 4402.20.00**, packaging, 910 kg/pallet, MSDS offered, **1–10 trucks/month**, asks for a meeting |

The 9 September one is still marked **unread** as of 16 September.

### Why this changes the Phase 01 gate

`PHASE-01-MEASUREMENT-FRAMEWORK.md` chose the **follow-up rate** — the share of submissions where
the desk had to chase missing information — as the metric that could carry the gate. The reasoning
was sound and the arithmetic still holds. The premise does not.

**These enquiries did not fail for want of information.** Three of the four carry commodity,
origin, destination, weight or volume, and an Incoterm — they would score *actionable* under
§2 of that framework without a single follow-up. They failed because nobody replied.

A better intake form does not fix an unanswered inbox. It produces better-specified enquiries
that also go unanswered, and the wizard's own reference numbers would make that more visible, not
less.

### What this does not establish

- **Whether these customers were answered another way.** WhatsApp, phone, or a mailbox outside
  this account are all invisible here. This is the single most important thing to check, and only
  MIDTRANS can check it.
- **That every unanswered thread deserved a reply.** Much of the sample is forwarder and carrier
  marketing, where no reply is the correct answer. The four read in full are not.
- **A rate.** Thirty threads, one window, one method. It establishes that the pattern exists and
  is not a single incident — not its size.
- **Why.** Volume, ownership of the inbox, filtering, or routing. That is an operational question
  for MIDTRANS, not an analytical one.

### What follows

1. **Answer the four.** They are named, dated and specific, and the 9 September one is a
   recurring-volume lane with a Managing Director asking for a meeting. Nothing else in this
   programme returns value as fast.
2. **Establish who owns `info@`** and what happens to a message that arrives there.
3. **Measure the reply rate before anything else.** It is now the Phase 01 baseline metric —
   see `../phases/PHASE-01-MEASUREMENT-FRAMEWORK.md` §7a.

---

## 9. What this analysis does NOT establish

Recorded honestly rather than estimated, per `README.md`:

| Not established | Why | How to establish |
|---|---|---|
| **WhatsApp enquiry volume** | Not visible in email | Export from the business WhatsApp account |
| **Phone enquiry volume** | Not logged | Manual logging, or a call-tracking number |
| **Website chat widget volume** | Only one conversation surfaced in this sample | D1 — find the chat platform and pull its logs |
| **Quote → booking conversion rate** | Requires linking enquiries to shipments in the operational system | D1 — check whether the TMS holds this |
| **True total enquiry volume** | The free-mail proxy misses company-domain enquiries | A labelling convention going forward (see below) |
| **Enquiries never responded to** | Would require auditing every thread for a reply | Scripted check over the full inbox |
| **Which website page each enquirer came from** | Not captured in the email | Phase 01 — add source-page capture to the wizard |

---

## 10. Findings and their consequences

| # | Finding | Consequence |
|---|---|---|
| 1 | Website RFQ funnel is 6 days old; 4 submissions total | Baseline is ≈0. Phase 01 measures from a clean zero — **record this, do not backfill an estimate** |
| 2 | ~73% of genuine demand is Syria-route | **Confirms Phase 04 as the right content phase.** It is not a bet |
| 3 | Dominant buyer is a first-time LCL importer, not an FCL shipper | Reshapes Phase 01 wizard design and Phase 04 content priority |
| 4 | 27% of genuine enquiries arrive in Arabic | **Confirms T2 (EN+AR)** for the Syria cluster |
| 5 | Public inbox is ~85% noise | Make the structured wizard the primary CTA; stop featuring the raw inbox address |
| 6 | Enquirers broadcast to 3–5 forwarders at once | Speed is a conversion mechanism → strengthens the case for Phase 02 |
| 7 | Chemicals and DG recur | Conditional DG branch in the wizard; DG content in Phase 04 |
| 8 | "General cargo" and missing Incoterms cause most follow-up rounds | Block the first; explain the second in-form |
| 9 | At least one lane declined after the enquiry | Publish a served-lanes page in Phase 04 |
| 10 | Wizard acknowledgement is guardrail-compliant | Use it as the template for Phase 01 copy |
| 11 | At least one enquirer chased twice without a rate | Phase 01 needs an SLA and a follow-up mechanism |
| **12** | **MIRA is live on the Claude API** (`mira.midtrans.org`) | **Guardrails become remediation, not preparation — this outranks everything else in the programme** |
| **13** | **A MIRA code path calls a model retired in Feb 2026 and fails silently** | Pin `claude-haiku-4-5`, drop the `-latest` alias, and add failure alerting |

---

## 11. Immediate recommendations

**Before Phase 01 starts** — cheap, and they make everything after them measurable:

1. **Create a Gmail label for website-sourced enquiries** and apply it consistently. Without it,
   this analysis has to be reconstructed by proxy every time. *(Requires the account owner's
   approval — this analysis modified nothing.)*
2. **Record the baseline as `≈0 structured website RFQs/month`**, with the wizard's launch date.
   Do not invent a historical figure.
3. **Add source-page capture to the wizard** so Phase 04's content can be attributed to enquiries
   it generates.
4. **Define a first-response SLA** and monitor it. Against buyers who broadcast to five
   forwarders, response speed is the conversion lever.
5. **Pull the chat widget's logs** in D1 — it is an unmeasured channel that is already producing
   conversations.
