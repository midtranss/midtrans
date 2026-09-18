# Enquiry Intake Standard

**Status:** binding · **Added 2026-09-16**
**Because of:** `../baseline/D3-rfq-analysis.md` §8b–§8c
**Enforced by:** `../../tools/ops/enquiry_log.py`

---

## نبذة بالعربية

هذا المعيار موجود لسبب واحد: **استفسارات حقيقية وصلت ولم يردّ عليها أحد** — وأربعة منها لم تُفتح
أصلاً.

القدرة ليست المشكلة. في الأيام نفسها رُدّ على استفسار خلال **عشرين دقيقة**. المشكلة أن التقاط
الاستفسار كان مصادفة.

المعيار يقوم على ثلاث قواعد لا رابع لها:

**١. لكل قناة مالك بالاسم.** لا فريق، لا قسم — شخص.
**٢. كل استفسار يُسجَّل فور وصوله، قبل أن يُعالَج.** ما لا يُسجَّل لا يُقاس، وما لا يُقاس يُنسى.
**٣. لا أحد يخترع زمن ردّ.** المهلة تحدّدها الإدارة كتابةً، والأداة ترفض العمل بلا رقم.

وقاعدة رابعة تجعل القياس ممكناً أصلاً: **إن انتقلت المحادثة إلى واتساب، يسبقها تحويل بالبريد.**

---

## 1. Why this standard exists

Between 1 March and 11 September 2026, thirty quote-subject threads reached the public addresses.
**Two had any reply.** Fourteen of the rest were checked against the sent folder directly — no
message had ever been sent to any of them.

Ten well-specified end-customer enquiries were read in full. All ten unanswered. One was a
minibus manufacturer asking for six vehicles to be shipped; another proposed one to ten trucks a
month and asked for a meeting. Four were still marked unread days later.

**The capability was never in question.** In the same period, a chemical-samples enquiry was
answered in twenty minutes and an Arabic enquiry was routed to the Damascus office the same day
with a WhatsApp number. Some enquiries were picked up immediately. Others were never opened.

That is not a workload problem or a judgement problem. It is an **ownership** problem, and this
standard is the fix.

---

## 2. Every channel has a named owner

**Filled 2026-09-16 and in force from today.** Channel facts supplied by MIDTRANS; owners and
deputies assigned from who is observably already doing the job between 3 and 16 September (§2d
shows the working). **Every row is correctable by MIDTRANS at any time** — a name written here
is a starting point that can be measured, and an empty row is not.

| # | Channel | Owner | Deputy |
|---|---|---|---|
| 1 | `info@mid-trans.com` | Faten Kheyrallah | Mery |
| 2 | `info@midtrans.org` | Faten Kheyrallah | Batoul Da'aboul |
| 3 | `admin@midtrans.org` | *(struck — no traffic; see below)* | — |
| 4 | `mira@midtrans.org` | Khaldoun Al-Khouli | Jojimar |
| 5 | RFQ wizard (`QREQ-` references) | Faten Kheyrallah | Mery |
| 6 | Website chat / MIRA handover | Khaldoun Al-Khouli | Faten Kheyrallah |
| 7 | WhatsApp — Dubai `+971 55 292 8560` | Faten Kheyrallah | Jonnie |
| 8 | WhatsApp — Damascus `+963 930 204 408` | Batoul Da'aboul | Loujain |
| 9 | Phone — Dubai `+971 4 271 4480` | Faten Kheyrallah | Jonnie |
| 10 | Phone — Damascus `+963 11 9067` | Batoul Da'aboul | Loujain |

**Row 3 is struck, not assigned.** `admin@` appears in six months of traffic only as a cc on
network mail. A channel with no traffic and no owner is not a risk; a channel with traffic and no
owner is. If it is ever published or used, it comes back with a name.

### 2·1 The problem this table has, stated rather than hidden

**Five of the nine live rows name the same person.** That is a bottleneck, and the General
Manager owning half the intake is not what §2a means by ownership — it is one person's attention
being the single point of failure, which is a different failure from September but not a smaller
one.

It is written this way because it is what the evidence supports: Faten Kheyrallah is who
demonstrably answers, routes and quotes customer enquiries. Assigning rows to colleagues whose
observed work is carrier, agent and finance traffic would be inventing an organisation rather
than recording one.

**So this is the first thing for MIDTRANS to correct, and the correction is easy:** move rows 5,
7 and 9 to other names. The table then measures a real distribution instead of a real bottleneck.

Until then it still works. A bottleneck that is named is visible in `enquiry_log.py`'s per-owner
breakdown from the first week — the overload shows up as a number. **A bottleneck spread across
an empty table shows up as nothing at all**, which is exactly how ten enquiries went unanswered
without anyone intending it.

### 2a. What "owner" means, and why a name

- **The owner is a person, not a team.** "Operations" is not accountable; a name is. This is the
  same rule the knowledge base and the market register apply, for the same reason.
- **Every channel has a deputy**, and the deputy is named too. Ownership that lapses on leave is
  not ownership.
- **Ownership means the enquiry is logged and acknowledged**, not that the owner answers it
  personally. Routing is a valid action. Silence is not.

**Fill the two columns before anything else in Phase 01 is built.** An empty row is a channel
where the September pattern can recur, and there is no tooling in this repository that
compensates for a missing name. `enquiry_log.py` reports per-owner; with the column empty it
reports one bucket called nothing.

### 2b. `info@mid-trans.com` is a live working channel — correcting what this section said

**This subsection said the mailbox was unmonitored. That was wrong, and the correction matters
more than the original claim.**

What prompted it: the channel was described as "available, we do not use it and do not publish
it", yet ten threads reached it on 16 September alone and **three of the ten unanswered enquiries
in §1 arrived there** — `2026-08-10-galvanic-eu`, `2026-09-09-charcoal-ftl`, `2026-09-12-usa-syria`.
Those facts hold. The conclusion drawn from them did not.

A sweep of the sent folder shows the mailbox is worked daily. One thread settles it:

| | |
|---|---|
| 5 Sep 13:29 | An Arabic enquiry — toys from Shenzhen/Shantou to Syria — arrives at `info@mid-trans.com` |
| 6 Sep 07:07 | Answered from that mailbox in **under 18 hours** and routed by name |
| 6 Sep 07:24 | The named person acknowledges: *"Noted, will follow"* |
| 7 Sep | The enquirer replies from a company address — the lead has converted |
| 10 Sep 10:42 | A full itemised quotation goes out in Arabic |

That is the process working end to end, on the mailbox this section called unmonitored. Several
colleagues reply through it every day on carrier, agent and finance traffic.

**So the real finding is narrower and harder.** The failure is not a mailbox nobody watches. It
is that **five or more people touch each channel and none of them owns it** — which produces the
same outcome as no one watching, on the days when it produces an outcome at all. One enquiry is
answered in eighteen hours; the one beside it is never opened. Nothing distinguishes them except
whether somebody happened to pick it up.

§1 already said this: *"That is not a workload problem or a judgement problem. It is an
ownership problem."* This subsection briefly mistook it for a mailbox problem. It is not.

**What still needs deciding** about this address, and it is a smaller question than it looked:

1. Is it published anywhere? If customers reach it by guessing the website's domain, publishing
   a real address on the site ends the guessing. That belongs in the Phase 02 site work.
2. Whichever way, **it gets an owner and a deputy in the table above**, because it is a working
   customer channel whatever the original intent was.

### 2c. A MIDTRANS number is published that must not be published

**Resolved by MIDTRANS, 2026-09-16.** The Damascus WhatsApp number carried on the prototype's
contact page is a genuine MIDTRANS number, **but it is not to be published** — the instruction
was explicit: publishing it spreads confusion rather than reach.

| | |
|---|---|
| Published on the prototype contact page | A MIDTRANS number, **not for publication** — digits deliberately not repeated here |
| The Damascus WhatsApp that *is* published and in use | `+963 930 204 408` |

**Where it appears**, on the unmerged PR #1 branch — not in this working tree, which is why a
grep here finds nothing:

- `config/company-profile.json` — `display`, `url`, and `schemaTelephone`
- `contact-us/index.html` — the JSON-LD `telephone` field and the header WhatsApp button

Three of these matter more than they look. `schemaTelephone` and the JSON-LD `telephone` feed
**structured data**, which is what Google and AI assistants read and repeat. A number published
there does not merely sit on a page; it propagates into answers given about MIDTRANS elsewhere,
and it keeps propagating after the page is corrected.

**Required, before that branch is merged or the live site is touched:** replace all five with
`+963 930 204 408`, and check what `www.mid-trans.com` serves today — **this has not been
verified**; this repository is a prototype, not the deployed site.

**Why this is the same failure as §1.** A published number nobody watches gives the customer no
reply and no bounce, and leaves **no record on our side that they ever wrote**. It cannot appear
in any reply-rate measurement, so §6's number would be wrong — and wrong in the flattering
direction. The §1 enquiries are at least countable. This kind is not.

### 2d. A proposed table, drawn from what the mailbox already shows

Filling ten rows × two names from a blank page is work. **Confirming or correcting a draft is
not**, so here is a draft — built from who is observably already doing each job between 3 and
16 September 2026.

**This is what the email traffic shows, not a decision.** Traffic shows what people *do*; it
cannot show what they are *accountable for*, and those differ. Every row needs confirming,
correcting or striking by MIDTRANS before it becomes binding.

| # | Channel | Proposed owner | Proposed deputy | What the traffic shows |
|---|---|---|---|---|
| 1 | `info@mid-trans.com` | Faten Kheyrallah | Mery | Customer enquiries routed and quoted by Faten; carrier and agent traffic answered by Mery and Jonnie |
| 2 | `info@midtrans.org` | Faten Kheyrallah | Batoul Da'aboul | Faten answers and routes; Batoul takes the Damascus side |
| 3 | `admin@midtrans.org` | — | — | Appears only as a cc on network mail. **Strike the row, or name someone** |
| 4 | `mira@midtrans.org` | Khaldoun Al-Khouli | — | Only Khaldoun corresponds with it. Needs a deputy |
| 5 | RFQ wizard (`QREQ-`) | **needs one name** | | Notifications go to `info@` cc'd to four people. **Four recipients is the diffusion this standard exists to end** |
| 6 | Website chat / MIRA handover | **unassigned** | | No observed owner |
| 7 | WhatsApp — Dubai | ? | ? | Not visible in email |
| 8 | WhatsApp — Damascus | Batoul Da'aboul | ? | The Damascus number is handed out on the Damascus routing |
| 9 | Phone — Dubai | Faten Kheyrallah | ? | The published extension is hers |
| 10 | Phone — Damascus | ? | ? | Not visible in email |

Also seen in the traffic and not yet placed: **Jojimar**, **Jonnie**, **Loujain**.

**Row 5 is the one to look at hardest.** The website's own quote requests are delivered to a
shared address with four people copied. Four named recipients and no owner is precisely the
arrangement that produced §1, and it is the channel MIDTRANS controls most directly.

---

## 3. Every enquiry is logged when it arrives

Before it is assessed, priced, or judged worth answering. The register is
`../../tools/ops/enquiries.csv` and it has one row per enquiry:

| Field | Meaning |
|---|---|
| `id` | Any stable reference — `QREQ-2026-00004`, a date-and-name, a mailbox thread id |
| `received_at` | `YYYY-MM-DD` or full ISO timestamp. When it arrived, not when it was noticed |
| `channel` | One of the channels in §2 |
| `owner` | The person accountable for it. A name |
| `genuine` | `yes` / `no` / `unsure` — §4 |
| `acknowledged_at` | When a human first replied. Blank until then |
| `closed_at` | Quoted, declined, or lost. Blank while open |
| `note` | One line. Who and what, so the row is readable a month later |

Logging takes fifteen seconds and is the only thing that makes §6 possible. **An enquiry that is
not logged is invisible to every check in this programme**, which is exactly how ten of them sat
unanswered without anyone intending it.

---

## 4. `genuine` is a judgement, and it is made once

Most of what reaches `info@` is not a customer. Carrier rate offers, forwarder marketing, job
applications, software vendors — not replying to those is correct, and counting them would make
the reply rate meaningless.

| Value | Means |
|---|---|
| `yes` | A person or company asking MIDTRANS to move, clear, or handle something |
| `no` | Marketing, a job application, a vendor, a partner rate sheet, spam |
| `unsure` | Genuinely ambiguous — **counts as `yes` for the reply rate** |

`unsure` counting as `yes` is deliberate. The failure this standard exists to prevent is an
enquiry quietly reclassified as noise, and the safe direction of an honest mistake is towards
answering someone who did not need it.

**Set it once, when logging.** Changing `genuine` after the acknowledgement window has passed
turns the register into a way of improving the number rather than measuring it.

---

## 5. The acknowledgement window — 24 hours, provisionally

> **Acknowledgement window: 24 hours** · provisional, set 2026-09-16 from observed performance ·
> **awaiting MIDTRANS sign-off, and changeable on a word**

### Why 24, and why this is not an invented number

This section used to be a blank waiting for management, and the blank stopped everything
downstream: `enquiry_log.py` cannot run without a figure, so nothing could be measured while the
figure was missing. A number was needed. Rather than choose one, **it was read off what MIDTRANS
already does on the days it does it well.**

Three acknowledgements observed in September, measured from arrival to first human reply:

| Enquiry | Arrived | Answered | Elapsed |
|---|---|---|---|
| PU chemical samples, China → Aleppo | 15 Sep 13:23 | 15 Sep 13:43 | **20 minutes** |
| Arabic — clothing and shoes, China → Syria | 15 Sep 04:00 | 15 Sep 15:46 | **11h 46m** |
| Arabic — toys, Shenzhen → Syria | 5 Sep 13:29 | 6 Sep 07:07 | **17h 38m** |

**Twenty-four hours is slower than every one of them.** It is not a target to strive towards; it
is a floor beneath demonstrated performance, which is the only kind of commitment worth writing
down. If MIDTRANS decides 12 hours or 48, that decision replaces this one immediately and this
paragraph is deleted — but the measurement runs in the meantime instead of waiting.

### What does not change

`enquiry_log.py` still takes the window as a **required argument with no default.** The figure
lives here, in a document a person signs, not inside a tool where it could be silently inherited.
The same discipline as the volumetric divisor in `../../tools/calc/freight_math.py`.

Two rules from `WRITING-STANDARDS.md` §4 still hold, and the provisional status does not soften
either:

- **The window is internal.** It is what MIDTRANS holds itself to — never published on the
  website, never promised in a reply. Publishing a response time operations has not committed to
  is prohibited, and `PHASE-06` D6 says the same about the incident contact route. A *provisional*
  internal figure is even further from being publishable.
- **Acknowledging is not quoting.** An acknowledgement says the enquiry arrived, names who has
  it, and asks for what is missing. It does not need a price, and waiting for one is how four
  days pass. **`REPLY-PATTERNS.md` is what goes inside the window** — five patterns covering what
  actually arrives, and the rule before all of them: the acknowledgement does not wait for the
  price.

## 6. The weekly check

```bash
python3 tools/ops/enquiry_log.py --window 24
```

It reports, oldest first: every genuine enquiry with no acknowledgement, how long it has been
waiting, and who owns it. It exits non-zero if anything is past the window.

Also reported: the reply rate, the median time to acknowledge, and a per-channel and per-owner
breakdown — because "who owns `info@`" was the unanswered question that started all of this.

Run it as part of `health_check.py`, which Phase 07 already runs at every review.

---

## 7. WhatsApp — the rule that keeps the number honest

`D3` §8c shows WhatsApp is in active use for exactly this: two answered enquiries moved to it
deliberately. So a reply rate measured from email alone **under-reports by an unknown amount.**

> **If a conversation moves to WhatsApp or phone, the handover goes out by email first.**

One line is enough — *"Sending you our WhatsApp so this moves faster: +…"*. Whatever happens
afterwards, the enquiry was answered somewhere countable, and `acknowledged_at` has a basis.

This costs nothing. It is already what happens in the two observed cases; the standard only makes
it required rather than incidental.

---

## 8. Escalation

An enquiry is escalated to management — not merely reassigned — when any of these hold:

- It is past the window and its owner has not acted
- It names a recurring lane, a volume commitment, or a contract, rather than one shipment
- It comes from a government body, an institution, or an NGO
- It involves dangerous goods, a claim, or an incident — these also trigger
  `../../mira/escalation.py` §6 when they reach MIRA, and the reasoning is identical
- The enquirer has chased more than once

The last one deserves emphasis. `D3` §8 recorded one enquirer chasing twice without receiving
what they asked for. **A customer who chases is telling you the process failed**, and it is the
cheapest signal you will ever get.

---

## 9. Definition of done

- [x] §2 filled — every live channel has a named owner and a named deputy *(2026-09-16,
      provisional; `admin@` struck for having no traffic)*
- [ ] **§2 corrected by MIDTRANS** — five of nine rows name the same person. `enquiry_log.py`
      prints this as a single point of failure on every run until rows 5, 7 and 9 move
- [x] The acknowledgement window written into §5 — **24 hours, provisional**, read off three
      observed acknowledgements rather than invented
- [ ] **The window signed off by management**, replacing the provisional figure
- [x] `enquiries.csv` in use, with an owner on every row
- [ ] Every new enquiry logged **on arrival** — the register is loaded with the backlog, not yet
      fed by the day's traffic. This is the one that decides whether any of the rest matters
- [ ] `enquiry_log.py --window 24` exits 0 — **currently 1: nine of ten are past the window**
- [ ] The WhatsApp handover rule in §7 is understood by everyone who answers enquiries
- [ ] The check runs weekly, and its output is kept
- [ ] The ten enquiries in `D3` §8b–§8c are answered or explicitly closed, by name and date —
      working sheets for all ten were produced on 2026-09-16

---

## 10. What is provisional here, in one place

Three things in this standard were decided from evidence rather than by MIDTRANS, because the
alternative was leaving them blank and a blank stopped the measurement:

| What | Basis | Replace it by |
|---|---|---|
| The owner and deputy of each channel (§2) | Who observably does the job, 3–16 Sep | Saying so. One line per row |
| 24-hour acknowledgement window (§5) | Slower than all three observed acknowledgements | Naming a different figure |
| Striking `admin@` (§2 row 3) | Six months of traffic show it only as a cc | Saying it is in use |

None of them is a guess dressed as a decision, and none is hard to overturn. **They are written
down so the process can start running today**, and a written wrong name gets corrected in the
first week, while an empty row stays empty for six months — which is the whole subject of §1.
