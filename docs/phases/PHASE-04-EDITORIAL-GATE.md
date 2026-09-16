# Phase 04 — Editorial Gate

**Status:** checker built and tested · **Governs:** every page published in Phases 04–07
**Tool:** `../../tools/content/check_page.py`
**Enforces:** `../standards/WRITING-STANDARDS.md`, `../standards/SEO-STANDARDS.md` §2,
`PHASE-04-syria-trade-center.md` § Out of scope

---

## نبذة بالعربية

المرحلة ٠٤ تنشر ٢٥–٤٠ صفحة عن إجراءات التجارة السورية، يكتبها بشر، تحت قاعدة صارمة: **لا رسوم
جمركية، ولا مدد تخليص، ولا تكاليف، ولا أحكام قانونية.** زلّة واحدة تصل إلى العميل بوصفها موقف
MIDTRANS المنشور.

هذا الملف يضيف بوّابة تحريرية تعمل **قبل النشر**:

```
python3 tools/content/check_page.py drafts/*.md
```

تفحص ما يمكن للآلة أن تفحصه: العبارات التجارية الممنوعة (بنفس محرّك ضوابط MIRA)، مدد التخليص،
الأحكام القانونية، الكلمات الممنوعة، أنماط الكتابة الآلية، البنية، الروابط الداخلية، والعربية
المكتوبة مقابل المترجَمة.

**وما لا تستطيع، لا تتظاهر به.** اختبار التفرّد حكم لفريق العمل — كل ما تفعله الأداة أنها **ترفض تمرير
صفحة لم يسجّل مراجعها إجابته عليه**. التشغيل النظيف إذن **رخصة للمراجعة، لا رخصة للنشر.**

---

## 1. Why a gate, and why here

Phase 04 is the first phase where the deliverable is **prose written by people**. Everything
before it was a system with tests. Prose has no tests, and the failure mode is quiet: a duty
figure in a paragraph reads exactly like the rest of the paragraph.

The Phase 04 risk register names it — *"a cost or timing figure is published"* — and mitigates it
with "review checklist item; editorial sign-off". A checklist catches what the reviewer happens
to notice on the day. Twenty-five to forty pages, two languages, several reviewers, over six to
eight weeks: something will be noticed on page 3 and missed on page 31.

The gate makes the mechanical part mechanical, so human review can spend itself on the part only
humans can do.

---

## 2. What it checks

```bash
python3 tools/content/check_page.py drafts/syria-import-documents.md
python3 tools/content/check_page.py drafts/*.md --json report.json
python3 tools/content/check_page.py drafts/*.md --warnings-are-blocking
```

### Blockers — the page does not publish

| Check | Rule it enforces |
|---|---|
| Rate, cost figure, duration, acceptance, capacity | Runs `mira/guardrails.py` over the prose. The assistant and the content are held to one standard |
| Clearance duration | `PHASE-04` § Out of scope — explain the sequence and what drives it, never how long |
| Compliance or legal determination | Sanctions, licensing, legality. Out of scope on every page in this programme |
| Never-use words | `WRITING-STANDARDS` § Never use — *best*, *largest*, *guaranteed*, *seamless*, and the rest |
| Missing or vague front matter | Owner, review date, expiry, and the recorded uniqueness answer |
| An owner that is not a person | "Operations" is not an owner. Same rule as the knowledge base |
| A token uniqueness answer | Under twelve words is not an answer to §4 |
| Two H1s, or none | `WRITING-STANDARDS` §5 |
| A language outside T2 | Phase 04 is EN + AR (`../standards/LANGUAGE-SCOPE.md`) |
| An English body declared `language: ar` | The translated-shell tell |

### Warnings — a human decides

| Check | Why it is not a blocker |
|---|---|
| AI-writing patterns | *"In conclusion"*, *"in today's fast-paced"*, *"contact us today"*. Sometimes a stock phrase is the right phrase |
| Thin page (under 300 words) | `SEO-STANDARDS` §2 prefers merging — but a short reference page can be correct |
| No substance before the first H2 | Answer-first is a strong rule with real exceptions |
| Fewer than three internal links | The links may exist inbound rather than outbound |
| No next step found | The detection is crude; a real close may be phrased unusually |
| Heavily Latin text on an Arabic page | Technical terms are expected; English sentences are not |

Warnings do not block by default. Once the cluster's house style has settled, run with
`--warnings-are-blocking` and keep it there.

### What it deliberately ignores

Figures inside fenced code blocks and HTML tags. A rate shown as a worked example of a *document*
is not MIDTRANS stating a rate. This is tested, because the opposite behaviour would make the tool
unusable on exactly the documentation-reference pages Phase 04 D4 calls for.

---

## 3. Front matter

Every page carries it. The checker refuses a page without it, and the fields are the same
discipline the knowledge base applies — because these pages **become** knowledge-base entries
under Phase 04 D7.

```yaml
---
title: Documents required to import into Syria
language: en
owner: Khaldoun Alhaj
reviewed_at: 2026-09-16
expires_at: 2027-03-16
uniqueness: Records the three document errors our Latakia desk sees most often and what each
  costs the shipper in re-issuance, which no published guide states.
uniqueness_reviewed_by: Khaldoun Alhaj
---
```

| Field | Rule |
|---|---|
| `language` | `en` or `ar` — the language the file is **written in**, not translated into |
| `owner` | A person's name. Not a team, not a role, not "MIDTRANS" |
| `reviewed_at` | `YYYY-MM-DD`. When a human last checked the facts |
| `expires_at` | `YYYY-MM-DD`. When the procedure must be re-checked. Syrian procedure changes |
| `uniqueness` | §4 |
| `uniqueness_reviewed_by` | Who applied the test. Usually not the writer |

`expires_at` is the field that keeps this cluster from quietly rotting. Published procedure that
has drifted out of date is worse than no page, because a reader acts on it.

---

## 4. The uniqueness test is not automatable, and the tool says so

`SEO-STANDARDS` §2:

> If the page would survive find-and-replace of its location or industry name with another and
> still read correctly, **it does not pass.**

No checker can apply that. It requires knowing what a competitor could have written, which is a
judgement about the world, not about the text.

So the tool does the only honest thing: it **requires the answer to be recorded, by a named
person, in at least twelve words**, and blocks the page until it is. It then prints, on every run
including a clean one:

> This tool cannot apply the uniqueness test. It only refuses to pass a page whose reviewer has
> not recorded one. A clean run is a licence to review, not a licence to publish.

### What a real answer looks like

**Fails** — *"Covers Syrian import documentation comprehensively."* Survives find-and-replace with
any country. No MIDTRANS in it.

**Fails** — *"Unique content about Latakia port."* Asserts the conclusion instead of supplying it.

**Passes** — *"Records the three document errors our Latakia desk sees most often and what each
costs the shipper in re-issuance, which no published guide states."* Names the specific
operational knowledge, and it could not be written by someone who has not worked the port.

The test in `SEO-STANDARDS` §2 asks for one of: specific operational detail, procedural
requirements that genuinely differ from the generic case, or genuine MIDTRANS experience — a
handled case, a known constraint, a recurring failure mode. The recorded answer should name which.

---

## 5. Where the gate sits in the workflow

```
capture session  →  draft  →  check_page.py  →  human review  →  operations sign-off  →  publish
                               ↑______________________|
                                  blockers return it
```

1. **Knowledge capture** per `PHASE-04-KNOWLEDGE-CAPTURE.md`. The gate cannot create substance;
   it can only refuse to let its absence through quietly.
2. **Draft**, with front matter from the start — not added at the end, when `uniqueness` becomes
   a box to tick rather than a question to answer.
3. **`check_page.py`** — the writer runs it before submitting. Blockers come back to the writer.
4. **Human review** — the uniqueness test, the warnings, and everything the tool cannot see:
   is this true, is it useful, does it contradict another page, does it read like MIDTRANS.
5. **Operations sign-off** on factual accuracy. `PHASE-04` requires this per page, and it is the
   step that makes the content worth publishing.
6. **Publish**, and the page becomes a MIRA knowledge-base entry per D7, carrying the same owner
   and expiry.

Run the checker over the whole cluster again before the phase gate. A page that passed in week 2
may have been edited in week 6.

---

## 6. What the gate cannot catch

Stated plainly, because a tool that appears to cover more than it does is worse than no tool:

- **A factual error.** "The certificate is issued by the chamber of commerce" — if that is wrong,
  nothing here will know. Only operations sign-off catches it.
- **Content that is true, unique, and useless.** Uniqueness is necessary, not sufficient.
- **A contradiction with another page.** `PHASE-04` requires a reconciliation pass; the checker
  reads one page at a time.
- **Bad Arabic.** It measures script distribution, not quality. A native domain reviewer is
  required by `WRITING-STANDARDS` §6 and is not replaceable.
- **A commitment phrased in a way the patterns do not model.** The guardrail rules catch patterns,
  and language is larger than patterns. Every phrasing that slips through and is caught in review
  becomes a test case, the same loop the MIRA guardrails use.

---

## 7. Running the suite

```bash
python3 tools/content/tests/test_check_page.py
```

Standard library only. The suite carries as many must-pass cases as must-block ones, and that
balance is deliberate: **a checker that blocks good writing gets switched off, and then it
protects nothing.** A false blocker costs a writer five minutes; a missed rate reaches a customer.
Both failure modes are tested.

If `mira/guardrails.py` cannot be imported, the checker **blocks** rather than skipping the
commercial-statement check. A silently skipped safety check is not a safety check.

---

## 8. Definition of done — for the gate

- [ ] Every draft carries complete front matter from its first commit
- [ ] `check_page.py` runs clean on every page in the cluster, with no blockers
- [ ] Every `uniqueness` field answers §4 specifically, named, and is not the writer's own sign-off
- [ ] Warnings reviewed and either fixed or consciously accepted, recorded per page
- [ ] `--warnings-are-blocking` adopted once the house style has settled
- [ ] Operations sign-off recorded per page, by name and date
- [ ] Reconciliation pass done across the cluster — no page contradicts another
- [ ] Arabic pages reviewed by a native domain reviewer, recorded
- [ ] Every phrasing caught in human review that the checker missed has become a test case
- [ ] Checker re-run over the whole cluster immediately before the phase gate
