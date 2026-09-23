# Phase 05 — Market Claims and Cluster Duplication

**Status:** both checks built and tested · **Governs:** Phase 05 D1, D2, D3
**Tools:** `../../tools/content/check_page.py` (extended) · `../../tools/content/check_cluster.py`
**Enforces:** `PHASE-05-market-entry-representation.md` § sourcing rule,
`../standards/SEO-STANDARDS.md` §2

---

## نبذة بالعربية

المرحلة ٠٥ تحمل خطرين لا تلتقطهما بوّابة المرحلة ٠٤:

**الأول — ادّعاءات السوق.** المرحلة تشترط: «كل عبارة عن وضع السوق أو حجم الفرصة **موثّقة
بمصدر، وإلا لا تُنشر**». أضفت هذا إلى الفاحص: كل حجم سوق أو نسبة نموّ يُحجب ما لم يوجد مصدر
**في الفقرة نفسها**.

وعالجت تعارضاً حقيقياً: فاحص المرحلة ٠٤ كان يحجب «سوق بقيمة ٤.٢ مليار دولار (البنك الدولي)»
بوصفه سعراً — ممّا يجعل شرط المرحلة ٠٥ مستحيل التنفيذ. الآن الرقم **الموثَّق** داخل ادّعاء سوق
يُستثنى من قاعدة السعر، ويُسجَّل كملاحظة للمراجع.

**الثاني، وهو الأخطر — التشابه داخل العنقود نفسه.** المرحلة تحذف تسع صفحات مدن أمريكية بحقّ. لكن
**مركز التمثيل التجاري نفسه يحمل الخطر ذاته**: «تمثيل تجاري» و«تمثيل أعمال» و«تمثيل محلّي» —
ثلاث صفحات قد تكون نسخاً من بعضها بأسماء مختلفة. وهذا لا تراه مراجعة صفحة-بصفحة أبداً.

بنيت فاحصاً للعنقود يُنفّذ اختبار المعيار حرفياً: **يُخفي أسماء موضوع الصفحتين، ثم يقارن الباقي.**
النتيجة على عيّنة حقيقية: ثلاث صفحات قالبية = **١٠٠٪ تطابق**؛ و١٤ وثيقة حقيقية مختلفة، ٩١ زوجاً =
**أقلّ من ٢٪**. الفصل حادّ، لا رمادي فيه.

---

## 1. The sourcing rule, enforced

`PHASE-05` D1 is unambiguous:

> Any market-condition or opportunity statement must be sourced and cited, or it is not
> published. No invented market sizes, growth figures, or opportunity values.

`check_page.py` now detects market and opportunity claims — a size, a valuation, a growth rate, a
"fastest-growing", and their Arabic equivalents — and decides on one rule:

| Situation | Result |
|---|---|
| A citation in the **same paragraph** | `NOTE` — recorded for the reviewer |
| No citation in that paragraph | **`BLOCKER`** — the page does not publish |

A citation is a link, a footnote marker, "Source:", "according to", a parenthetical attribution
with a year, or the Arabic equivalents. The detection is deliberately generous: the tool sees
that a source is present, and the reviewer judges whether it supports the claim. Those are
different jobs and only one of them is automatable.

### Why the paragraph, not a character window

The first implementation searched a 220-character window either side. On a realistic draft, an
uncited *"the sector is growing at 8% annually"* two paragraphs below a properly cited market
size **inherited that citation and passed**. The paragraph is the unit a reader treats as one
statement, so it is the unit the check uses. The case is in the suite.

---

## 2. ⚠️ A conflict that made D1 unsatisfiable

Phase 04's gate blocks figures in a cost context, using `mira/guardrails.py`. Run it on a Phase 05
page and:

```
"The Syrian construction market was valued at $4.2 billion in 2024 (World Bank, 2025)."
  → BLOCKED  prohibited:money_amount
```

Phase 05 **requires** sourced market figures. Phase 04's gate **blocks all figures**. As built,
the two phases contradicted each other, and a writer meeting D1 would have been unable to publish.

**Resolution:** a figure inside a *cited* market claim is exempted from the rate rule and recorded
as `rate_rule_exempted` — a note asking the reviewer to confirm it is a market statistic and not a
price. An **uncited** figure gets no exemption: it is blocked twice over, as an unsourced claim
and as a figure.

The exemption is narrow by construction. It requires a market-claim pattern *and* a citation in
the same paragraph, both of which a price quotation would fail.

---

## 3. The risk inside Phase 05's own hub

Phase 05 removes nine templated US location pages, for the right reason: a doorway pattern is
assessed at site level and can suppress the Phase 04 Syria cluster.

**The same risk sits inside D2, and the phase document does not flag it.** The Business
Representation hub lists:

> business representation · commercial representation · local representation · partner search ·
> distributor search · sales representation · tender monitoring

The first three are not obviously different services to a reader, and a page each is the same
pattern as a page per US city — one template, one substituted noun. The difference is that
"Texas" and "Chicago" look like a doorway pattern at a glance, and "commercial representation"
versus "business representation" does not.

**This is not a prediction that the pages will be templated. It is the observation that nothing
in the phase would notice if they were**, because every per-page check passes: each has a title,
an owner, a uniqueness field, real sentences.

### Before writing these pages

For each, answer in one sentence: **what does a client get here that they do not get from the page
next to it?** If the answer needs the page's own name to make sense, the pages are one page. Merge
first and write once — `SEO-STANDARDS` §2's own preference, and far cheaper than merging after
publication and carrying the redirects.

---

## 4. The cluster check

```bash
python3 tools/content/check_cluster.py drafts/representation/*.md
python3 tools/content/check_cluster.py drafts/*.md --block 0.35 --warn 0.20
```

It implements `SEO-STANDARDS` §2's own test:

> If the page would survive find-and-replace of its location or industry name with another and
> still read correctly, it does not pass.

For every pair, the subject terms of **both** pages are masked — title words, the filename, and
any `entities:` in front matter — and the remaining text is compared as 5-word shingles (Jaccard
similarity). Two pages about genuinely different things diverge once their subject names are
removed. Two templated pages do not.

Masking is what makes it work, and the suite proves it: on templated pages, masking **raises** the
score, because the substituted noun was the only thing making them look different.

### Calibration — measured, not assumed

| Population | Pairs | Similarity |
|---|---|---|
| Three templated representation pages | 3 | **100%** |
| This repository's own phase documents | 91 | **worst 1.5%** |

The negative control is the honest half: 14 documents written by the same author, in the same
voice, on adjacent subjects, with shared structure and shared vocabulary — exactly the population
most likely to produce false positives. The worst pair scores 1.5%.

Defaults are therefore **0.35 blocking, 0.20 warning**, with an order of magnitude of clear space
on either side. Both are flags, not constants: recalibrate against the real cluster once a dozen
pages exist, and record the numbers here.

### What it is not

Similarity is evidence, not a verdict, and the tool says so on every run. Two genuinely distinct
pages can share structure — a common H2 skeleton across a service hub is good practice, not
duplication. **Read the pair before acting.** The failure mode to avoid is a writer who starts
varying sentences to move a number, which produces worse prose and the same page.

---

## 5. Where these sit in the workflow

Phase 04's gate runs per page. This one runs per **cluster**, and it runs at three moments:

| When | Why |
|---|---|
| Before writing the cluster | §3 — answer the differentiation question first, on an outline |
| When the third page in a cluster is drafted | Early enough that merging is cheap |
| Before the phase gate, over every page | A page that passed in week 2 may have been edited in week 8 |

Run both:

```bash
python3 tools/content/check_page.py    drafts/**/*.md
python3 tools/content/check_cluster.py drafts/representation/*.md
```

Cluster the invocation the way a reader would — the representation pages against each other, the
market-entry pages against each other. Comparing every page in the phase against every other
mostly produces pairs nobody would confuse.

---

## 6. What neither check can do

- **Judge whether a source supports its claim.** It sees that a citation is present. A citation
  to a blog post repeating a figure nobody can trace is still a citation.
- **Notice an invented figure that carries a fabricated source.** Only a reviewer following the
  link catches that, and on a market-entry page aimed at an executive assessing risk, it is worth
  following every one.
- **Decide that two similar pages should nonetheless both exist.** That is a commercial judgement.
- **Catch a market claim phrased without numbers.** *"Demand is strong and growing"* is an
  unsourced claim that no pattern will flag. `WRITING-STANDARDS` §4 covers it; a human enforces it.
- **Apply the uniqueness test.** Unchanged from Phase 04's gate: recorded, not automated.

---

## 7. Definition of done — Phase 05 content

- [ ] Every market, growth or opportunity claim carries a source in its own paragraph
- [ ] Every `rate_rule_exempted` note reviewed — confirmed a market statistic, not a price
- [ ] Every cited source followed and confirmed to support the claim, by a named reviewer
- [ ] §3's differentiation question answered in writing for each representation page, **before**
      drafting
- [ ] `check_cluster.py` clean across the representation hub and the market-entry hub
- [ ] Thresholds recalibrated against the real cluster, and the numbers recorded in §4
- [ ] The US page carries its compliance boundary statement explicitly (Phase 05 D3)
- [ ] No legal, tax, sanctions or compliance determination anywhere — `check_page.py` blocks the
      phrasings it knows; a reviewer covers the rest
- [ ] Phase 04 gate checklist also passed for every page
