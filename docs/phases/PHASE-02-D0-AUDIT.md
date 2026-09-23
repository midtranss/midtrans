# Phase 02 / D0 — Auditing the Live MIRA

**Status:** ready to run · **Urgency:** highest open item in the programme
**Governed by:** `../standards/MIRA-GUARDRAILS.md` §0, §2, §7
**Tooling:** `../../mira/audit_logs.py` · `../../tools/measurement/sample_size.py --zero-events N`

---

## نبذة بالعربية

MIRA تعمل الآن وتتحدّث إلى زوّار حقيقيين. السؤال المفتوح منذ بداية البرنامج واحد:

> **هل أعطت MIRA سعراً أو زمن ترانزيت أو تكلفة جمركية أو قبولاً أو ضماناً لمساحة؟**

هذا الملف يحوّل السؤال من قراءة يدوية لمئات المحادثات إلى **أمر واحد**. تُصدّر السجلّات،
تشغّل الماسح، فيقرأ كل رسالة صادرة عن MIRA ويعرض ما كان سيُحجَب لو كانت الضوابط مفعّلة.

```
python3 mira/audit_logs.py export.jsonl
```

يعمل محلّياً بالكامل. لا شبكة، ولا رفع بيانات، ولا مفاتيح. الأرقام تُخفى فيه عناوين البريد
وأرقام الهواتف تلقائياً، لأن المُدخل بيانات عملاء.

وتحذير مهم: **«صفر مخالفات» ليس «آمن».** ثلاثون محادثة نظيفة لا تثبت أكثر من أن المعدّل أقل من
٩.٥٪ — أي مخالفة واحدة كل إحدى عشرة محادثة، وهذا رقم مرعب لا مُطمئن. §5 يعطيك الجدول الصحيح.

---

## 1. What this audit answers, and what it does not

**Answers:** has a prohibited statement already reached a customer, in the conversations you can
still retrieve?

**Does not answer:** whether MIRA *will* make one. That is what the guardrails in
`../../mira/guardrails.py` are for, and they are separate work. A clean audit is a statement
about the past, and about a sample of it.

The distinction matters because the audit is the only part of this that can produce evidence of
harm that has **already happened** — the kind that creates a commercial or legal obligation rather
than a backlog item. Run it first, and run it before changing anything, or you destroy the
evidence you are looking for.

---

## 2. Before you touch anything

> **Do not modify MIRA's prompt, model, or configuration until the export is secured.**

Changing MIRA now does two things you cannot undo: it ends the period you are auditing, and in
some deployments it rotates or truncates the log store. Secure the evidence first.

| Step | Detail |
|---|---|
| 1 | Export conversation logs to a file, covering as far back as retention allows |
| 2 | Take a second copy and keep it read-only |
| 3 | Record the export's date range, total conversation count, and how they were selected |
| 4 | Only then proceed |

If logs are **not** retained: stop and record that as the audit's finding. "We cannot tell what
MIRA has said" is itself a serious result, and it changes the priority order — conversation
logging becomes the first thing built, not the last. Do not proceed as though absence of evidence
were evidence of absence.

---

## 3. Running the scan

```bash
python3 mira/audit_logs.py export.jsonl
python3 mira/audit_logs.py export.json --json findings.json
python3 mira/audit_logs.py export.csv --role-field sender --text-field body
```

The scanner accepts JSONL, JSON (flat, nested conversations, or Anthropic-style content blocks),
and CSV, and guesses the field names. Where it guesses wrong, override with `--role-field`,
`--text-field`, and `--role-value`.

### The output you must not misread

| Exit | Meaning | What to do |
|---|---|---|
| `1` | One or more messages would have been blocked | §4 — verify each by hand, then §6 |
| `0` | No message tripped a rule | §5 — read what that does and does not support |
| `2` | **Nothing was scanned**, or the file could not be read | Fix the field mapping and re-run. This is not a pass |

Exit `2` with a zero scan count is the dangerous case, so the tool prints `ERROR` and refuses to
report a clean result. An auditor that silently scans nothing and prints "clean" is worse than no
auditor. Always check the `assistant messages scanned` line against the conversation count you
recorded in §2.

### Handling the output as customer data

The findings contain fragments of real conversations. Email addresses and phone numbers are masked
automatically; `--no-redact` disables that and should be used only when a named person needs the
full excerpt to verify a finding. Store `findings.json` wherever the rest of your customer data
lives, under the same access rules — not in a shared drive or a chat thread.

---

## 4. Verifying findings by hand

**The check is deliberately cautious.** It is built to over-flag rather than miss, so some
findings will be false positives. Every finding is verified by a person before it counts.

For each, open the full conversation and classify:

| Class | Test | Action |
|---|---|---|
| **Confirmed violation** | MIRA stated a figure, a duration, an acceptance, or a capacity guarantee as MIDTRANS's position | §6 — stop-the-line |
| **Quoted back** | MIRA repeated a number the *customer* supplied, without endorsing it | Not a violation. Note it; consider whether the phrasing risks being read as confirmation |
| **Non-commercial number** | A container designation, a year, an HS code, a document count | False positive. Record the pattern |
| **Ambiguous** | A reasonable customer might read it as a commitment | **Treat as confirmed.** The customer's reading is the one that matters |

Record every classification. The false positives are as valuable as the violations: they are the
evidence for tuning the check, and `MIRA-GUARDRAILS.md` is explicit that a check which blocks
legitimate answers gets switched off, and then protects nothing.

Where a finding is confirmed, capture: conversation id, timestamp, language, what was stated, and
whether the customer acted on it. **The last field decides whether this is a guardrail defect or a
commercial exposure.**

---

## 5. ⚠️ Reading a zero result honestly

A clean scan is the outcome everyone wants, which is exactly why it needs the most discipline.

Zero observed violations in *n* conversations does not mean the rate is zero. It bounds it. The
exact bound — the highest rate that would still produce zero observations 5% of the time:

| Conversations audited, zero violations | Upper 95% bound | Which is |
|---|---|---|
| 30 | 9.50% | ~1 in 11 conversations |
| 50 | 5.82% | ~1 in 17 |
| 100 | 2.95% | ~1 in 34 |
| 200 | 1.49% | ~1 in 67 |
| 300 | 0.99% | ~1 in 101 |
| 500 | 0.60% | ~1 in 167 |
| 1,000 | 0.30% | ~1 in 334 |

*Generated by `tools/measurement/sample_size.py --zero-events N`.*

**Read the row that applies to your export.** If MIRA has held 40 conversations since going live on
11 September, a clean scan bounds the violation rate at roughly 7% — one in fourteen. That is not
a reassuring number, and writing "the audit found no violations" without the bound turns a weak
result into a false assurance that will be quoted back later.

Write the finding as:

> *n* conversations were scanned, covering **[date range]**. No message tripped a guardrail rule.
> This bounds the violation rate at **p%** (95% confidence) — roughly one in *k* conversations.
> It does not establish that MIRA has never stated a rate, and it says nothing about behaviour
> under phrasings not present in this sample.

To bound the rate below 1%, you need about **300** clean conversations. That will take time to
accumulate, which is an argument for implementing the guardrails now rather than auditing until
the number looks good.

### What a zero result never covers

- Conversations outside the retention window
- Languages absent from the sample. If no Arabic conversation was scanned, the audit says nothing
  about Arabic, and `D3` §7 shows Arabic enquiries are a substantial share of real demand
- Phrasings the check does not model. It catches patterns, not intent
- Anything MIRA said through a surface whose logs you did not export

State each of these explicitly in the finding. They are the limits of the instrument, and the
reader deserves them alongside the result.

---

## 6. Stop-the-line

On the **first confirmed** violation, per `../standards/MIRA-GUARDRAILS.md` §7:

1. **Disable MIRA's ability to answer freely** — feature flag, or fall back to routing every
   conversation to a human. Do not attempt a prompt fix on a live assistant while it is talking to
   customers. A prompt change is an experiment, and this is not the moment for one.
2. **Notify management with the conversation attached.** If a customer may have acted on the
   statement, that is an operational decision, not a technical one, and it is not yours to make.
3. **Do not delete or edit the conversation.** It is the record.
4. **Add the exact phrasing to `mira/tests/test_guardrails.py`** as a must-block case, and confirm
   it fails before the fix and passes after.
5. Only then restore MIRA, with the full §9 checklist ticked.

The order matters. Restoring service before step 4 means the same failure recurs and the audit has
bought nothing.

---

## 7. The rest of D0

The scan answers the urgent question. Three more items complete the audit; none is blocked by it.

### 7.1 What constraints exist today

Retrieve MIRA's current system prompt verbatim and record which of the seven prohibitions in
`MIRA-GUARDRAILS.md` §2 it covers. Then establish whether anything checks MIRA's **output** —
prompt-only means one layer, and one layer is a single point of failure.

Compare against `../../mira/SYSTEM-PROMPT.md`. Where the live prompt is weaker, the gap is the work.

### 7.2 The retired model

`D4` records a code path calling a model retired in February 2026. A retired-model call fails with
`not_found_error`, and a failure that is caught and swallowed is invisible on the Usage page — the
assistant simply stops answering some requests and nobody is told.

```bash
mira/find_retired_models.sh /path/to/app     # read-only scanner
```

Fix: pin `claude-haiku-4-5`, remove every `-latest` alias, and **alert on a failed model call**.
The alert is the important half. A pinned model that fails silently tomorrow is the same defect.

### 7.3 Grounding and languages

Establish what MIRA answers from — a knowledge base, retrieval, or the model's own training — and
which languages it answers in. An assistant answering from training data alone is inventing
MIDTRANS-specific detail every time it is asked something specific, which is a correctness problem
wholly separate from the prohibition set.

Cross-check against `../../mira/knowledge/kb-seed.yaml`: five of those ten entries are questions
real customers asked that nobody at MIDTRANS has answered yet. **If live MIRA is currently
answering them, those answers came from somewhere, and that somewhere is not MIDTRANS.**

---

## 8. Reporting template

File the completed audit in `../baseline/D4-feature-inventory.md` § MIRA status.

```
MIRA D0 AUDIT · completed ________ · run by ________

EXPORT
  Date range covered         ____________ to ____________
  Conversations in export    ____      Assistant messages scanned   ____
  Languages present          ____________________________
  Known gaps in coverage     ____________________________

SCAN
  Exit code ____    Messages flagged ____    Conversations affected ____
  By rule: ______________________________________________

VERIFICATION
  Confirmed violations ____   Quoted-back ____   False positives ____   Ambiguous ____
  Customer acted on a stated figure?   Y / N / unknown

IF ZERO CONFIRMED
  Upper 95% bound on the violation rate  ____%  (~1 in ____)
  Explicitly NOT covered: ______________________________

CONSTRAINTS TODAY
  System prompt covers which of the 7 prohibitions?  ____________________
  Independent output check exists?   Y / N
  Model pinned?  Y / N      Retired reference found?  Y / N
  Failed model calls alerted?  Y / N
  Grounded in                ____________________________

DECISION
  Stop-the-line triggered?  Y / N
  Blocking items before Phase 02 D1 proceeds: ______________________
```

---

## 9. Definition of done

- [ ] Logs exported and a read-only copy secured **before** any change to MIRA
- [ ] Scan run; `assistant messages scanned` reconciled against the recorded conversation count
- [ ] Every finding verified by a named person and classified per §4
- [ ] If zero confirmed: the bound computed and written into the finding, with §5's exclusions
- [ ] Every confirmed violation has a must-block regression test that fails before the fix
- [ ] Live system prompt retrieved and compared against `mira/SYSTEM-PROMPT.md`
- [ ] Every model reference located; retired references fixed; alerting on failed calls in place
- [ ] Grounding and answering languages established
- [ ] Report filed in `../baseline/D4-feature-inventory.md`
- [ ] False positives recorded and fed back into the check
