# Phase 07 — Operating Checks

**Status:** both built and tested · **Governs:** Phase 07 Part B and ongoing operations
**Tools:** `../../tools/ops/market_gate.py` · `../../tools/ops/health_check.py`
**Register:** `../../tools/ops/markets.yaml`

---

## نبذة بالعربية

المرحلة ٠٧ لا تنتهي — **تُدار**. وخطرها الأول مكتوب في سجلّ مخاطرها نفسه: «تجاوز بوّابات الأسواق
تحت ضغط تجاري»، وعلاجه المقترح «قرار مُسجَّل كتابةً». لكنّ قراراً مكتوباً نثراً قرار **لا يستطيع
أحد فحصه**.

جعلته سجلّاً مُهيكلاً وبوّابة ميكانيكية. والقاعدة التي تحمل معظم الوزن:

> **دليل الطلب يجب أن يحتوي رقماً.**

«هناك طلب واضح من السوق التركية» رأي. «٩ طلبات عروض و١٤ محادثة ميرا مصدرها تركيا بين كانون
الثاني وحزيران ٢٠٢٦» دليل. بوّابة تقبل الأولى **ليست بوّابة** — هي الجملة التي يكتبها المرء في
طريقه إلى ما قرّره سلفاً.

والثاني: **فحص صحّة البرنامج**. المرحلة تُدرج مراجعة أسبوعية وشهرية وثلاث فصلية — كلّها «شخص
يتذكّر أن ينظر». هذا يحمل الجزء الذي تحمله الآلة: ما انتهت صلاحيته، وما بلا مالك، وما لم يؤكَّد،
وحالة السجلّ، وكل مجموعات الاختبار.

**وما لا يراه، يقوله في كل تشغيل:** لا يعرف إن كانت الصفحة ما تزال **صحيحة**. صفحة سارية تصف
إجراءً تغيّر الشهر الماضي تجتاز كل فحص هنا.

---

## 1. The market gate, as a register

`PHASE-07` Part B states the rule clearly — four tests, all four, one market at a time — and then
mitigates the risk of bypass with "decision recorded in writing by the programme owner". Writing
is where the rule leaks. A paragraph in a document cannot be checked, cannot be counted, and
cannot refuse anything.

`tools/ops/markets.yaml` holds one record per market. `market_gate.py` refuses:

| Refusal | Why |
|---|---|
| A market marked `open` or `live` with any of the four tests not passed | The gate is all four |
| A test marked passed on under ten words of evidence | "Yes" is not a finding |
| **Demand evidence with no number in it** | §2 |
| No owner, or an owner like "Operations" | Test 4 is a named person; a team is not accountable |
| No `target` | Phase 07's own gate is "against a target agreed **before** the market opened" |
| Missing or malformed `opened_at`, `decision_recorded_at` | A decision without a date is not a record |
| No `decision_recorded_by` | Somebody signs it |
| **More than one market `open`** | Part B: one at a time |
| `live` with no `opened_at` | A market cannot skip the gate by being published |
| `rejected` with no reason | It will be re-litigated next quarter otherwise |

Run it:

```bash
python3 tools/ops/market_gate.py
```

As shipped, all four candidate markets are `candidate` and the register is consistent. **No market
is open, which is the correct state** until one has evidence behind it.

---

## 2. The rule that does the work

> Demand evidence must contain a number.

This single constraint is the difference between a gate and a formality.

**Fails:** *"There is clear and growing demand from the Turkish market for our services."*
Unfalsifiable, and it will be written with complete sincerity by someone who has already decided.

**Passes:** *"9 RFQs and 14 MIRA conversations originated in Turkey between January and June
2026, per the D3 method."* A count, a period, and a method — which means it can be wrong, checked,
and argued with.

Phase 07's test 1 is "organic search demand, inbound RFQs, or MIRA conversations originating from
that market". Every one of those is a countable thing. If the number cannot be produced, the
honest reading is that the evidence does not exist yet — which is a finding, not an obstacle.

The other three tests require ten words of evidence but no number, because operational reality,
capacity and ownership are properly described in sentences.

### What the gate does not do

It checks that a decision was **recorded**, not that it was **right**. Whether nine RFQs justify a
market is a commercial judgement belonging to the programme owner. The tool insists only that the
number exists and that somebody put their name to it — and it says so on every run.

---

## 3. The health check

```bash
python3 tools/ops/health_check.py
python3 tools/ops/health_check.py --content-root drafts --days 60
```

Phase 07's cadence table lists a weekly metric review, a monthly MIRA audit, and three quarterly
reviews. Each is a person remembering to look. This holds the part a machine can hold, and tells
the person which pages to read first.

| Section | Reports |
|---|---|
| Content freshness | Pages past `expires_at`, pages expiring inside the horizon, pages with no valid expiry, pages with **no owner** |
| MIRA knowledge base | Entries, how many are servable, how many still await a named owner, and any validation error |
| Calculator reference data | Container capacities and volumetric divisors still `unconfirmed` — the calculators must not go live while any remain |
| Market register | The §1 checks, summarised |
| Suites | All seven test suites, run |

**Expired content and ownerless pages exit non-zero.** Those are not opinions: a published page
whose review date has passed is either still true and needs re-dating, or is no longer true and is
misleading someone. Everything else reports and lets a person decide.

Run it in CI, or as the first act of each quarterly review.

---

## 4. What none of this can see

Stated because a check that appears to cover more than it does is worse than no check, and the
health check prints this on every run:

> **Whether a page is still TRUE.** An unexpired page describing a procedure that changed last
> month passes every check here.

Also invisible:

- **Whether a market met its target.** The register holds the target; measuring against it is the
  Phase 01 measurement framework and a person reading the numbers.
- **Whether a case study is accurate.** `PHASE-07` D1 forbids embellished outcomes and unmeasured
  figures. Nothing mechanical can tell a real outcome from a flattering one — only the written
  client permission and a factual review can.
- **Whether a Trust Center claim is held.** A certification that MIDTRANS does not hold looks
  exactly like one it does. Verification is per claim, before publish, by a person.
- **Whether imagery is authentic.** Stock photography of an unrelated port is the single fastest
  way to undo the credibility Phases 04–06 build, and no check here will notice it.

The quarterly review is a person reading the content. This tells them where to start.

---

## 5. Opening a market — the sequence

1. **Evidence first.** Produce the number: RFQs, MIRA conversations, or organic sessions from
   that market, with a period and a method. If it cannot be produced, stop — the market is not
   ready, and that is the gate working.
2. **Fill the record** in `markets.yaml`: all four tests, the owner by name, the target, the
   signatory, the dates.
3. **Run the gate.** `python3 tools/ops/market_gate.py` must exit 0.
4. **Confirm nothing else is open.** The tool refuses two, but the discipline is the point, not
   the refusal.
5. **Set status to `open`** and build, at T3 scope — market hub, lane content, corridor detail.
   Not a replica of the Syria cluster; the Syria cluster is the depth asset and market pages
   route into it.
6. **Publish, set `live`,** and measure against the target that was written down in step 2.
7. **At the review:** met the target → consider the next market. Missed it → the content is
   reviewed for retirement, not extended in hope. `PHASE-07` is explicit about this, and it is
   the hardest part of the phase to actually do.

---

## 6. Definition of done — Phase 07 operations

- [ ] `market_gate.py` exits 0 — no market open on an incomplete record, never two at once
- [ ] Every open or live market's demand evidence carries a real count and period
- [ ] Every market's target was written down **before** it opened
- [ ] `health_check.py` run at each quarterly review, with the output kept
- [ ] Nothing expired; every page carries a named owner and a valid `expires_at`
- [ ] `unconfirmed_rows()` empty before any calculator goes live
- [ ] Case studies: written client permission held; no unmeasured or embellished figures
- [ ] Trust Center: every certification, membership and appointment verified as held
- [ ] Imagery authentic; no stock photography of facilities MIDTRANS does not operate
- [ ] A rejected market carries its reason, so it is not re-argued every quarter
