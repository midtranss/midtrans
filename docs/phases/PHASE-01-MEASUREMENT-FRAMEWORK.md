# Phase 01 — Measurement Framework

**Status:** ready to implement · **Governs:** the Phase 01 exit gate
**Depends on:** `../baseline/D3-rfq-analysis.md` §5, §8 · `../baseline/D6-BASELINE.md`
**Binds:** `PHASE-01-conversion-infrastructure.md` D6, `PHASE-01-RFQ-WIZARD-SPEC.md`

---

## نبذة بالعربية

بوابة المرحلة ٠١ مكتوبة حالياً هكذا: «طلبات عروض أسعار مؤهّلة شهرياً **أعلى بشكل قابل للقياس** من
خطّ الأساس». هذه الجملة غير قابلة للتنفيذ كما هي — «قابل للقياس» غير معرّف، ولا أحد يستطيع أن يحكم
بها.

والأخطر: **بحجمكم الحالي، لا يمكن إثبات ذلك إحصائياً في أربعة أسابيع.** حسبتُ الرقم. عند عشرين طلباً
في الشهر، تحتاجون أن يرتفع العدد إلى اثنين وأربعين — أي أكثر من الضعف — قبل أن يصبح الفرق قابلاً
للتمييز عن التذبذب الطبيعي. أي تحسّن واقعي (٢٠٪ أو ٣٠٪) سيبدو كصدفة، وسيُقرأ خطأً في الاتجاهين.

هذا لا يعني ترك القياس. يعني اختيار **مقياس يعمل عند حجمكم**.

المقياس الذي يعمل هو: **نسبة الطلبات التي اضطرّ فيها قسم التسعير لمراسلة العميل ليسأل عن معلومة
ناقصة.** كل طلب يعطي ملاحظة واحدة، والفرق المتوقّع كبير جداً. عشرة طلبات فقط تكفي لإثبات انخفاض
من ٨٠٪ إلى ٢٠٪. هذا هو بالضبط ما صُمّم الـ Wizard ليفعله، وهو ما يوفّر وقت فريقكم فعلياً.

خلاصة الإطار: العدد الشهري يبقى مقياس الأعمال، لكن **قرار البوابة يُتّخذ بنسبة المراسلات
الاستدراكية**، مع مقاييس حراسة تمنع تحسين الرقم على حساب فقدان عملاء.

---

## 1. Why this document exists

The Phase 01 exit gate currently reads:

> Qualified RFQ submissions per month measurably higher than the Phase 00 baseline, over a
> minimum of four weeks of clean data.

Three words in that sentence are not implementable: **qualified**, **measurably**, and **clean**.
Until each is a rule a person can apply without judgement, the gate cannot be passed or failed —
it can only be argued about, and it will be argued about by whoever has the most at stake.

This document defines all three, and then says something uncomfortable that the arithmetic forces:
at MIDTRANS's enquiry volume, **the primary metric cannot carry the gate decision.** §6 shows why,
and §7 gives the gate that can.

---

## 2. The primary metric, defined mechanically

The master plan defines a qualified RFQ as one carrying "origin, destination, commodity,
approximate volume or weight, and a contactable requester."

That definition collides with the wizard spec. `D3` §5 establishes that **"I don't know yet" must
be a valid answer to volume and weight** — the dominant buyer genuinely does not know at enquiry
time, and forcing a number produces either a wrong number or an abandoned form. So a submission the
wizard is deliberately designed to accept would be scored unqualified.

Both are right. They are measuring different things, and they need different names.

### Two tiers, both computed from the submission record

| Tier | Rule | What it means |
|---|---|---|
| **Actionable RFQ** | origin **and** destination **and** specific commodity **and** (gross weight **or** volume **or** dimensions) **and** mode **and** Incoterm **and** a contactable requester | The desk can approach a carrier without asking the customer anything first |
| **Qualified lead** | origin **and** destination **and** specific commodity **and** a contactable requester | Real demand, real person, enough to start work |

"Specific commodity" means the `commodity` field is populated and is **not** one of the blocked
generic values (`general cargo`, `goods`, `cargo`, `products`, `items`, and their Arabic
equivalents) — the block list the wizard already enforces per `PHASE-01-RFQ-WIZARD-SPEC.md`.

"Contactable requester" means a syntactically valid email **or** a phone number in E.164 form.

Every term above is a field on the submission record. **No human judgement is applied**, which
means the number cannot drift as the person computing it changes.

### Which is primary

**Actionable RFQ per 4 weeks is the business metric.** It is what converts into quoting work.

**Qualified lead per 4 weeks is a guardrail** (§8). It exists so that nobody improves the first
number by making the form stricter and quietly losing the customers who do not yet know their
volumes.

---

## 3. Event schema

Events are named and propertied here so instrumentation is implementable, testable, and identical
across languages. Names are fixed; adding properties later is fine, renaming is not.

| Event | Fires when | Required properties |
|---|---|---|
| `rfq_view` | The wizard's first step renders | `page_path`, `language`, `referrer_type`, `device` |
| `rfq_start` | The user changes or confirms any field on step 1 | + `entry_step` |
| `rfq_step_complete` | A step is passed | + `step_index`, `step_name`, `ms_on_step` |
| `rfq_step_error` | Validation blocks progression | + `step_index`, `field`, `error_type` |
| `rfq_abandon` | Session ends with a start and no submit | + `last_step_index`, `had_contact` |
| `rfq_submit` | The submission is accepted server-side | + `reference` (`QREQ-…`), `steps_completed`, `total_ms`, `tier` |
| `rfq_submit_failed` | Server rejects or errors | + `failure_type` |
| `whatsapp_click` | The WhatsApp path is opened | `page_path`, `language`, `device` |
| `callback_submit` | Callback form accepted | `page_path`, `language` |
| `consult_submit` | Consultation booking accepted | `page_path`, `language` |

Three rules that decide whether this data is worth anything:

1. **`rfq_submit` fires server-side, on acceptance.** A client-side submit event counts requests
   that never arrived. The reference number is the proof the record exists.
2. **`tier` is computed server-side** by the §2 rules at the moment of acceptance, and stored on
   the record. Recomputing it later from an evolved rule silently rewrites history.
3. **`language` is the page's language, not the browser's.** Attribution by browser locale will
   misreport every Arabic speaker browsing an English page, and `D3` §7 shows that is a real and
   common pattern in this business.

### The field that makes §7 possible

Add one field to the submission record, set by the pricing desk, not by the website:

| Field | Set by | Values |
|---|---|---|
| `followup_required` | The person who picks up the submission | `none` · `one_round` · `multiple_rounds` |

It is set once, when the desk first sends the enquiry onward or first replies to the customer. It
answers one question: **did we have to go back and ask for something before we could quote?**

This is the single most valuable number in the framework. §7 explains why.

---

## 4. Verifying the instrumentation

`PHASE-01` D6 requires events "verified firing in the reporting tool — not assumed from code". That
verification is this procedure, and its output is a signed-off table, not a memory.

For every event in §3, in **every language in tier, including Arabic**:

1. Trigger it manually on a real device.
2. Confirm it arrives in the reporting tool, with every required property populated and correctly
   typed.
3. Record: event, language, device, timestamp, verified by whom.

Then three checks that catch what per-event testing does not:

- **Consent interaction.** Run the whole procedure once with consent granted and once with consent
  refused. Record what is lost under refusal. A framework that silently loses half its data to a
  consent banner produces confident wrong answers. This is a known failure mode, listed in
  `PHASE-01` risks.
- **Reconciliation.** For a full week, compare `rfq_submit` event count against `QREQ-` references
  actually issued. They must match exactly. A gap means events are being dropped; a surplus means
  they are being double-counted. **Do not begin the measurement period until they match**, and
  re-run this check weekly thereafter.
- **Deduplication.** Confirm a double-click, a page refresh on the confirmation screen, and the
  browser back button do not each produce an extra `rfq_submit`.

---

## 5. What "clean data" means

A 4-week measurement period is clean only if all of the following hold. Any breach restarts the
period; it does not shorten it.

| Condition | Why |
|---|---|
| No change to the wizard, its fields, its validation, or its routing during the period | Changing the thing being measured mid-measurement |
| The §4 reconciliation matched every week of the period | Otherwise the count is unknown, not just uncertain |
| No paid campaign started, stopped, or materially changed budget | Traffic mix change masquerades as a funnel change |
| No site-wide outage longer than 4 hours | A lost day is a lost ~3.5% of the period |
| Consent configuration unchanged | Changes what is observable, not what happened |
| No bulk or test submissions in the data | They are not customers |

Also record, without treating them as disqualifying: Ramadan, Eid, Chinese New Year, and the
European August. `D3` §4 shows route concentration through China and the Gulf, so these move real
volume. A period spanning one is still usable — but the comparison period must span the same one,
or the conclusion is about the calendar, not the funnel.

---

## 6. The arithmetic that changes the gate

`D3` §2 gives the only hard volume number available: **4 wizard submissions in the 6 days**
11–16 Sep 2026 (`QREQ-2026-00001` … `00004`, sequential, so exact). Sustained, that is roughly
**20 per 4 weeks** — and it is 4 observations, so treat 20 as an order of magnitude, not a figure.

For a count metric, comparing a baseline 4-week period against a test 4-week period of equal
length, at 80% power and α = 0.05 two-sided:

| Baseline / 4 wks | Must reach | Increase of | Relative |
|---|---|---|---|
| 5 | 18 | +13 | +256% |
| 10 | 26 | +16 | +165% |
| 20 | 42 | +22 | **+108%** |
| 30 | 56 | +26 | +85% |
| 50 | 82 | +32 | +64% |
| 80 | 119 | +39 | +49% |
| 120 | 167 | +47 | +39% |
| 200 | 260 | +60 | +30% |

*(Two Poisson counts, equal exposure, variance-stabilising √ transform: √λ₁ = √λ₀ + 1.981.
Computation is reproducible — see the note at the end of this section.)*

**Read the row that applies.** At ~20 submissions per 4 weeks, the funnel must **more than double**
before the increase can be distinguished from ordinary month-to-month variation. A genuine,
valuable 25% improvement would be statistically invisible — and, worse, a random quiet month would
look like failure and a random busy one like success.

Extending to 8 weeks helps, but less than hoped: it roughly halves the required relative effect,
which at this volume still means needing something near +70%.

The completion-rate metric is no better. Detecting a 10-point lift needs ~300 wizard starts in each
period:

| Baseline completion | +5 pts | +10 pts | +15 pts | +20 pts |
|---|---|---|---|---|
| 20% | 1,094 | 293 | 138 | 81 |
| 30% | 1,376 | 356 | 162 | 93 |
| 40% | 1,533 | 387 | 173 | 97 |
| 50% | 1,565 | 387 | 169 | 93 |

*(Starts needed per period. Two-proportion test, 80% power, α = 0.05 two-sided.)*

**The honest conclusion: significance testing is the wrong instrument for this decision at this
volume.** Pretending otherwise produces false confidence in both directions, which is worse than
having no test at all.

> Reproducibility: every table in §6 and §7 is generated by `../../tools/measurement/sample_size.py`
> (standard library only). Before this framework is used, re-run it with the real baseline —
> `python3 tools/measurement/sample_size.py --baseline <actionable RFQ per 4 weeks>` — and read the
> row that actually applies. The method, not the illustrative numbers, is what this section
> contributes.

---

## 7. The gate that works at this volume

Use the metric where **every submission is an observation and the expected effect is large.**

### The follow-up rate

Of submissions received, the share where the pricing desk had to go back to the customer for
missing information before it could quote — the `followup_required` field from §3.

`D3` §5 establishes that commodity, weight, volume, Incoterms, mode and door-vs-port were **each
missing at "very high" or "high" frequency** before the wizard. The pre-wizard follow-up rate was
therefore close to universal. The entire purpose of the wizard's field set is to collapse it.

That is a large expected effect on a per-submission metric, and large effects need small samples:

| Follow-up rate falls from | to 50% | to 40% | to 30% | to 20% | to 10% |
|---|---|---|---|---|---|
| 90% | 19 | 13 | 9 | **7** | 5 |
| 80% | 38 | 22 | 14 | **10** | 7 |
| 70% | 93 | 42 | 23 | 14 | 9 |
| 60% | 387 | 97 | 42 | 22 | 13 |

*(Submissions needed per period, 80% power, α = 0.05 two-sided.)*

**Ten submissions per period are enough to prove an 80% → 20% drop.** That is within reach at the
observed volume — unlike every row in §6.

It is also the better metric on its merits. It measures what Phase 01 is actually for: a funnel
that collects what the desk needs, first time. And it maps directly to money, because each avoided
round trip is desk hours saved and, per `D3` §8, one fewer chance to lose a lead that was chased
twice and never answered.

### ⚠️ 7a. Correction — the binding constraint is upstream of this (2026-09-16)

Everything in §7 is arithmetically sound and its premise is wrong.

The follow-up rate was chosen because §6 showed the count metric cannot carry the gate at this
volume, and because `D3` §5 showed information was missing from nearly every enquiry. While
reconstructing the baseline from the mailbox, thirty quote-subject threads to the public
addresses between 1 March and 11 September 2026 were sampled: **two had any reply.** Fourteen of
the rest were checked by a separate sent-mail search against the recipients themselves — the test
that does not depend on threading — and **no message had been sent to any of them.**

Four end-customer enquiries were read in full. All four are unanswered, and all four are
well-specified: three carry commodity, origin, destination, weight or volume and an Incoterm, so
they would score **actionable** under §2 without a single follow-up. The most recent — a
Managing Director proposing one to ten trucks a month, with HS code, packaging and pallet weight
— was still unread a week later.

`D3` §8b has the detail.

**The consequence for this framework:** a better intake form cannot raise a number that is being
lost after intake. Improving specification quality on enquiries nobody answers produces
better-specified unanswered enquiries — and the wizard's sequential references make that more
visible, not less.

### The metric that now comes first

**Reply rate: of enquiries received, the share that received any human reply, and the time to it.**

It sits above the follow-up rate because it is upstream of it. An enquiry that is never answered
has no follow-up round to count, so it silently leaves the denominator of §7's metric — which
means the follow-up rate can *improve* while the business loses more customers. That is the worst
property a gate metric can have.

| | Reply rate | Follow-up rate (§7) |
|---|---|---|
| Measures | Whether anyone responded | Whether the form collected enough |
| Owner | Operations — inbox ownership and routing | Phase 01 — the wizard's field set |
| Sample needed | Every enquiry is an observation; the effect is large | ~10 submissions per period |
| Fixed by | A person and a process | A better form |

Both are tracked. The **reply rate gates Phase 01**, and the follow-up rate measures whether the
wizard did its own job. A wizard that halves the follow-up rate while the reply rate stays where
it is has not moved the business, and the gate should say so.

**Baseline to establish first, before any wizard work:** of enquiries arriving in the 90 days
before 11 September 2026, how many received a reply, and how long did it take? The §8b sample is
a starting point and explicitly not a rate.

**Before drawing any conclusion from it:** confirm whether these enquirers were answered by
WhatsApp or phone. Email is the only channel visible from here, and `D3` §2 records both other
channels as UNKNOWN. If they were answered elsewhere, this correction narrows to a measurement
problem rather than a lost-lead one — which is still worth knowing, and is a different problem.

---

### The revised exit gate

Replace the current gate with this. All four conditions, none optional:

1. **Reply rate is at or above the target agreed at phase start**, and no enquiry in the period
   went unanswered beyond the agreed window. **This is now the first condition** — see §7a.
   Until the reply rate is known, nothing below is meaningful.
2. **Follow-up rate on wizard submissions is significantly lower than the pre-wizard baseline**,
   over at least 4 weeks of clean data (§5) and at least the sample size the table above requires
   for the observed effect. This measures whether the wizard did its own job.
3. **Actionable RFQ per 4 weeks is not lower than baseline.** Directional, not significance-tested
   — §6 says it cannot be. It is a floor, not a target.
4. **Zero enquiries lost during cutover**, evidenced by the §4 weekly reconciliation matching every
   week, with no unexplained gap.
5. **No guardrail in §8 has breached its threshold.**

### Pre-registration

Before the measurement period opens, write down and have the phase owner countersign: the baseline
value, the period start and end dates, the expected effect size, and what decision each outcome
triggers. File it in `../baseline/D6-BASELINE.md` § gate decision.

This is the cheapest protection available against the failure mode that actually destroys
programmes like this one — deciding what the number meant after seeing it.

---

## 8. Guardrail metrics

Each has a threshold that, if breached, blocks the gate **regardless of the primary result**. They
exist because every one of them can be traded away to improve the headline number.

| Guardrail | Threshold | What it prevents |
|---|---|---|
| Qualified leads / 4 wks (§2 tier 2) | Not below baseline | Tightening the form to raise "actionable", losing the buyer who does not yet know their volumes — the dominant buyer in `D3` §4 |
| Wizard completion rate | Not more than 5 points below baseline | Adding fields until only the most determined finish |
| `rfq_submit_failed` rate | < 1% of attempts | A lead dropped by a backend error is invisible in every other metric |
| Total enquiries across **all** routes (wizard + email + WhatsApp + phone) | Not below baseline | Moving volume between channels and calling it growth |
| **Reply rate** | 100% of genuine enquiries answered within the agreed window | §7a. Measured as a guardrail as well as the primary gate, because it is the one number that can fail silently |
| Median desk response time | Not worse than baseline | Volume arriving faster than the desk can absorb it. `PHASE-01` names this risk; this is how it is detected |
| Spam / non-genuine share of submissions | Not materially above baseline | Inflating counts with junk. `D3` §3 found the public inbox ~85% noise — the risk is real and precedented |

Guardrails are reviewed **weekly during the period**, not at the end. A breach caught in week 1 is a
fixable problem; the same breach found in week 4 has cost the whole period.

---

## 9. Rules against gaming

Not because anyone intends to cheat, but because metrics under pressure drift, and the drift is
always in the flattering direction.

1. **The §2 definitions are frozen for the duration of the measurement period.** Changing them
   mid-period voids the period. If a definition is wrong, fix it and restart.
2. **`tier` is stored at acceptance, never recomputed.**
3. **Internal, test, and known-partner submissions are excluded**, by a rule written before the
   period opens, not by inspection afterwards.
4. **The person computing the number is not the person whose phase is being gated.**
5. **A failed gate is a valid, expected outcome.** `PHASE-01`'s own instruction is to stop and
   re-diagnose if volume does not move. A framework that cannot return "no" measures nothing.

---

## 10. ⚠️ The baseline problem — act on this first

**The wizard went live on 11 September 2026.** Today is 16 September 2026. Phase 00's baseline was
supposed to be measured before Phase 01 shipped, and part of Phase 01 has already shipped.

There is no forward path to a clean pre-wizard baseline. It must be **reconstructed from history**,
and the sources are finite and decaying:

| Baseline needed | Source | Risk |
|---|---|---|
| Pre-wizard enquiry volume | Mailbox, Sep 2025 – Sep 2026, per `D3` §1 method | Deletions, archiving, mailbox retention policy |
| Pre-wizard follow-up rate | The same threads: count those where the team had to ask for missing information before quoting | Same, plus this requires reading threads, which takes time |
| Pre-wizard `/get-quote/` sessions and submissions | Analytics history | Retention window may already have expired |
| Traffic and source mix | Analytics history | Same |

**Do this before anything else in Phase 01.** Every day that passes makes the reconstruction harder
and the eventual conclusion weaker. The follow-up rate in particular — the one metric §7 shows can
actually carry the gate — exists only inside email threads that nobody is currently preserving for
this purpose.

Reconstruct it over a window matched to the test period: same length, and spanning comparable
seasonality per §5.

If any of it proves unrecoverable, record that in `D6-BASELINE.md` § gaps, and say plainly in the
gate decision that the comparison is weaker for it. **An acknowledged weak baseline is usable. An
unacknowledged one silently corrupts every phase gate that follows.**

---

## 11. Weekly review

Thirty minutes, same day each week, during the measurement period. Not a meeting about the
website — a check that the measurement is still valid.

```
Week __ of __ · Period __________ to __________

RECONCILIATION
  rfq_submit events ____   QREQ- references issued ____   Match? Y/N
  If N: stop. The period is not clean until this is resolved.

PRIMARY
  Submissions this week ____   Of those, followup_required = none ____
  Running follow-up rate ____%   Baseline ____%

GUARDRAILS                              breach?
  Qualified leads (tier 2)      ____      Y/N
  Completion rate               ____%     Y/N
  Submit failure rate           ____%     Y/N
  Total enquiries, all routes   ____      Y/N
  Median desk response time     ____      Y/N
  Spam share                    ____%     Y/N

CLEAN-DATA BREACHES THIS WEEK (§5)
  ____________________________________________

ACTIONS
  ____________________________________________
```

Keep every completed sheet. They are the evidence the gate decision rests on, and they are what
makes a disputed result re-examinable rather than re-arguable.

---

## 12. Definition of done — for this framework

- [ ] Every §3 event implemented and verified per §4, in every language in tier, on real devices
- [ ] Consent-granted and consent-refused both tested; what is lost under refusal is documented
- [ ] Reconciliation matched for one full week before the period opens
- [ ] `followup_required` field exists, and the pricing desk has been shown how and when to set it
- [ ] §2 definitions implemented server-side, with `tier` stored at acceptance
- [ ] Baseline reconstructed per §10, with gaps explicitly recorded in `D6-BASELINE.md`
- [ ] §6 tables re-run against the real baseline and the applicable row identified
- [ ] Pre-registration written and countersigned before the period opens
- [ ] Weekly review scheduled, with a named owner
- [ ] Level 2 checklist in `../standards/DEFINITION-OF-DONE.md` passed
