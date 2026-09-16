# Reply patterns — the first response to a new enquiry

**Status:** ready to use · **Added 2026-09-16**
**Derived from:** `../baseline/D3-REPLY-DRAFTS.md` and `D3-rfq-analysis.md` §5, §8c
**Works with:** `ENQUIRY-INTAKE.md` · checked against `../../mira/guardrails.py`

---

## نبذة بالعربية

المسوّدات الستّ عالجت ستّ حالات. **هذا الملف يعالج ما يأتي.**

قرار الإدارة: لا نلاحق المتأخّرات، بل نأخذ منها الدرس. فحوّلتُ المسوّدات من رسائل إلى **أنماط** —
لأن الرسالة تُستهلك مرّة، والنمط يعمل في كل مرّة.

الأنماط خمسة، مستخرَجة ممّا يصل فعلاً لا ممّا نتوقّعه. ومعها **قاعدة واحدة تسبقها جميعاً**:

> **الإشعار بالاستلام لا ينتظر السعر.**

هذا هو الدرس كلّه في سطر. الاستفسارات العشرة لم تفشل لأن أحداً رفضها — بل لأن الردّ انتظر جواباً
لم يجهز، فمرّ يوم ثم أسبوع. الإشعار يقول: وصلت، وفلان يتابعها، وهذا ما ينقصنا. **لا يحتاج سعراً.**

---

## 0. The rule that comes before all five

> **The acknowledgement does not wait for the price.**

That is the whole lesson in one line. None of the ten unanswered enquiries was refused. Each was
waiting on an answer that was not ready, and a day passed, then a week.

An acknowledgement says three things and needs no figure to say them:

1. It arrived, and here is who has it — **by name**
2. Here is what we still need from you, and why each item is needed
3. Here is how to reach that person directly

`ENQUIRY-INTAKE.md` §5 puts a window on this. This file is what goes inside it.

### Two things that make any first reply work

**Never ask for what they already sent.** `D3` §5 shows the desk chasing commodity, weight,
volume, Incoterms and mode. Three of the six September enquiries carried all of those. Asking
again tells a well-prepared enquirer that nobody read their email, and it is the most common
reason a good enquiry goes quiet.

**Every question carries its reason.** *"Gross weight per vehicle — RoRo bookings are confirmed
against weight as well as dimensions, and the carrier will ask before holding space."* The reason
converts a demand into a collaboration, and a reader who understands why answers faster.

---

## 1 · Well-specified enquiry — answer inside the window

**Recognise it by:** commodity, origin, destination, and a weight or volume already present.
Roughly half of what arrives. The Poland, Lörrach and Arabic LCL enquiries were all this shape.

**What it needs:** a named owner, an acknowledgement, and the two or three items genuinely
missing. Nothing more.

> Thank you — [name the specific thing they supplied: dimensions per unit / the SDS / the two
> volumes to compare]. That is more than we usually receive and it lets our pricing desk start
> straight away.
>
> To put firm numbers against it, [two or three] things are still needed:
>
> 1. **[Item].** [Why — who will ask for it and at what stage.]
> 2. **[Item].** [Why.]
>
> [Named person] has this and will come back with [what, in the form they asked for].
> If it is quicker, they are on [direct number].

**Do not** restate their own enquiry back to them. They know what they sent.

---

## 2 · Under-specified enquiry — the same window, a different body

**Recognise it by:** an intent without the facts. *"I want to import from China, how much?"*

**The mistake to avoid:** a checklist of twelve fields. It reads as a form and it gets abandoned.
Ask for **four at most**, and say that "not known yet" is acceptable — `D3` §5 is explicit that
forcing a number from someone who does not have one produces a wrong number or silence.

> Happy to help. Four things and our team can work on it properly:
>
> 1. **What exactly is the cargo?** The specific product, not a general description — the carrier
>    will not accept a general one, and it changes what is possible.
> 2. **Roughly how much?** Weight, or volume, or the number of cartons or pallets. **"Not known
>    yet" is a fine answer** — tell us and we will work against a range.
> 3. **From where, to where?** The supplier's city, and the destination city or port.
> 4. **When is it ready?**
>
> [Named person] will take it from there.

---

## 3 · Regulated category — vehicles, chemicals, food

**Recognise it by:** the enquirer is asking whether the thing is *possible*, not what it costs.
Four of the six September enquiries were this shape, and vehicles have now arrived three times.

**The rule that matters:** MIDTRANS does not state a customs or regulatory rule from memory.
Someone buys a vehicle on that answer.

> On [the admissibility / the requirements / the classification]: I will be direct — we will not
> give you that from memory. The rules are set by [the destination authority] and they change. An
> emailed answer that you then base a [purchase / order] on would not be responsible.
>
> What we will do instead is put the specific details in front of our clearing agent and come
> back with what he confirms, together with what that confirmation rests on and how long it is
> likely to hold.
>
> To do that we need: [the precise data points — the registration document fields, the SDS, the
> product specification].

**Why this wins rather than loses the enquiry:** the German vehicle enquirer sent the same five
questions to three forwarders. Two will answer from memory. The one who says *"we will confirm and
tell you what it rests on"* is the one a careful buyer keeps.

**Where the answer comes back:** into `../../mira/knowledge/kb-seed.yaml` with a named owner —
`kb-008` vehicles, `kb-004` chemicals, `kb-014` food. It is asked repeatedly; answer it once.

---

## 4 · Sent to several forwarders at once

**Recognise it by:** multiple recipients in the To or Cc line. Two of the six.

**What changes:** speed is the whole competition. A reply measured in days is a loss by default,
and the enquirer never tells you that you lost.

**What to do:** reply first, briefly, the same day. Answer the question they actually asked —
usually *"can you do this route at all?"* — and say when the detail follows.

> Thank you. You asked first whether this routing and this cargo are workable, so let me answer
> that rather than send you a form.
>
> We are checking [the specific thing] now with [our correspondent on that leg]. **We will come
> back with a clear yes or no, not a maybe.**
>
> So pricing can run in parallel: [one or two facts].

**Never** claim the route is available before operations confirms it. A fast wrong answer loses
the customer later and more expensively than a slow one loses them now.

---

## 5 · A recurring lane, not one shipment

**Recognise it by:** *"1 to 10 trucks per month"*, *"we are establishing a regular lane"*, a
company rather than an individual, an offer to meet. One of the six.

**What changes:** this is not a quote request. It is the beginning of a commercial relationship,
and `ENQUIRY-INTAKE.md` §8 escalates it to management rather than merely assigning it.

> Thank you — a regular lane is a different conversation from a single shipment, and worth having
> properly.
>
> [Senior person, by name] handles this side and will contact you directly. In the meantime, so
> the first quotation is real rather than indicative: [the two or three facts].

**Do not** bury a recurring-volume enquiry in the ordinary quote queue. It arrives looking like an
RFQ and it is not one.

---

## 6 · What must never appear in a first reply

Same list as everywhere else in this programme, and it is the reason these are patterns rather
than finished letters:

`rate` · `price` · `transit time` · `duty` · `customs cost` · `acceptance` ·
`space availability` · `a regulatory determination` · `a response-time promise`

A hedge does not create an exception. *"Roughly", "approximately", "indicative", "for guidance
only"* produce a quote with a disclaimer, which is still a quote.

**Check a new pattern before adding it here:**

```bash
python3 -c "import sys;sys.path.insert(0,'mira');import guardrails as g;
print(g.check_response(open('draft.txt').read()).rules)"
```

The six drafts that produced this file were checked that way, and the check itself turned out to
be wrong — see `../baseline/D3-REPLY-DRAFTS.md`. Run it anyway; a wrong check that gets fixed is
worth more than no check.

---

## 7 · Arabic

Two of the six September enquiries arrived in Arabic and one in German. The reply goes out in the
language the enquirer used — not as a courtesy, but because a reply in another language moves the
effort of translation onto the person you are trying to win.

The patterns above translate directly. What does not translate is tone: `WRITING-STANDARDS.md` §6
applies, and an Arabic reply that reads as translated English reads as unserious to a Syrian or
Gulf trader.

---

## 8 · Definition of done

- [ ] Every channel owner in `ENQUIRY-INTAKE.md` §2 has read this file
- [ ] The acknowledgement window in §5 is set, and acknowledgements are sent inside it **without
      waiting for a price**
- [ ] Recurring-lane enquiries are escalated, not queued
- [ ] Multi-forwarder enquiries are answered the same day
- [ ] Regulated-category answers, once the clearing agent confirms them, are written back into the
      knowledge base with a named owner — so the next one is answered from record, not from scratch
