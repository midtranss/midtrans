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

| Channel | Owner | Deputy |
|---|---|---|
| `info@mid-trans.com` | | |
| `info@midtrans.org` | | |
| `admin@midtrans.org` | | |
| RFQ wizard (`QREQ-` references) | | |
| Website chat / MIRA handover | | |
| WhatsApp — Dubai | | |
| WhatsApp — Damascus | | |
| Phone — Dubai | | |
| Phone — Damascus | | |

**Fill this table before anything else in Phase 01 is built.** An empty row is a channel where
the September pattern can recur, and there is no tooling that compensates for it.

Rules:

- **The owner is a person, not a team.** "Operations" is not accountable; a name is. This is the
  same rule the knowledge base and the market register apply, for the same reason.
- **Every channel has a deputy**, and the deputy is named too. Ownership that lapses on leave is
  not ownership.
- **Ownership means the enquiry is logged and acknowledged**, not that the owner answers it
  personally. Routing is a valid action. Silence is not.

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

## 5. Nobody invents a response time

The acknowledgement window is set **by MIDTRANS management, in writing**, and recorded here:

> **Acknowledgement window: ______ hours** · agreed by ____________ on __________

`enquiry_log.py` takes it as a required argument and **has no default**. The same discipline as
the volumetric divisor in `../../tools/calc/freight_math.py`: a number nobody chose, silently
inherited, is worse than no number.

Two rules follow from `WRITING-STANDARDS.md` §4:

- **The window is internal.** It is what MIDTRANS holds itself to, not something published on
  the website or promised in a reply. Publishing a response time operations has not committed to
  is prohibited, and `PHASE-06` D6 says the same about the incident contact route.
- **Acknowledging is not quoting.** An acknowledgement says the enquiry arrived, names who has
  it, and asks for what is missing. It does not need a price to be sent, and waiting for one is
  how four days pass. **`REPLY-PATTERNS.md` is what goes inside the window** — five patterns
  covering what actually arrives, and the rule that comes before all of them: the acknowledgement
  does not wait for the price.

---

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

- [ ] §2 filled — every channel has a named owner and a named deputy
- [ ] The acknowledgement window agreed by management and written into §5
- [ ] `enquiries.csv` in use, with every enquiry logged **on arrival**
- [ ] `enquiry_log.py --window N` exits 0 — nothing genuine is past the window
- [ ] The WhatsApp handover rule in §7 is understood by everyone who answers enquiries
- [ ] The check runs weekly, and its output is kept
- [ ] The ten enquiries in `D3` §8b–§8c are answered or explicitly closed, by name and date
