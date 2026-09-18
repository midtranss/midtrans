# MIRA knowledge base

**Governed by:** `../../docs/standards/MIRA-GUARDRAILS.md` §5 (sourcing rule)

---

## نبذة بالعربية

قاعدة معرفة MIRA — الأسئلة مستخرَجة من **بريد MIDTRANS الحقيقي**، لا مخترَعة.

**قاعدة صارمة:** كل مُدخَل يحمل `source` و`owner` و`reviewed_at` و`expires_at`. **مُدخَل بلا مالك
مُسمّى لا يدخل القاعدة** — لأن معلومة بلا مالك هي معلومة غير مُصانة، والمعلومات غير المُصانة عن
الإجراءات الجمركية **تصبح خاطئة بصمت**.

**حدّ قاطع:** القاعدة تحوي إجراءات ووثائق وتسلسلات — **ولا تحوي أسعاراً ولا مدداً ولا رسوماً ولا
قواعد قبول، ولا حتى داخلياً**، كي لا يتسرّب شيء منها إلى رد.

---

## Where these questions come from

Every entry answers a question that **appeared in real MIDTRANS enquiries**, catalogued in
`../../docs/baseline/D3-rfq-analysis.md` §6. None was invented to fill a schema block or to look
complete.

That matters twice over: these are the questions MIRA will actually be asked, and under
`../../docs/standards/SEO-STANDARDS.md` §4 they are the only kind that may carry `FAQPage` schema
when the same content reaches the website.

## The rules that govern every entry

| Field | Why it is mandatory |
|---|---|
| `source` | Where the answer came from. An answer with no source cannot be verified or corrected. |
| `owner` | The named person accountable. **An entry without one does not enter the base** — an unowned fact is an unmaintained fact, and unmaintained facts about customs procedure go wrong quietly. |
| `reviewed_at` | When a human last confirmed it |
| `expires_at` | When it must be re-reviewed or retired |
| `status` | `draft` until an owner signs it off. **Draft entries must not be served.** |

## The content boundary

The knowledge base holds **procedures, document requirements, process sequences, and service
descriptions**.

It holds **no rates, no transit times, no costs, no acceptance rules** — not even as internal
notes, so that none can leak into a response. See `MIRA-GUARDRAILS.md` §2.

## Status of this set

Every entry below is **`draft`**. The questions are real and the structure is right, but the
*answers* were written from what is observable in the mailbox and from general trade practice —
**not from MIDTRANS's own documented procedure**, which this session has no access to.

> **They must be reviewed by MIDTRANS operations before any of them is served.** Serving an
> unreviewed answer about Syrian customs procedure is exactly the failure mode the sourcing rule
> exists to prevent.

The review is quick: each entry is short, and the reviewer only has to confirm or correct it, then
fill in `owner` and the dates.

---

## The validator

```bash
python3 mira/knowledge/validate_kb.py
```

It enforces the sourcing rule **mechanically**, so it cannot be forgotten under deadline
pressure. Verified against deliberately bad entries — it rejects:

| Case | Rejected because |
|---|---|
| Approved with no owner | An unowned fact is an unmaintained fact |
| Contains a currency amount | Forbidden by `MIRA-GUARDRAILS.md` §2 |
| Contains a transit time | Same |
| Approved with an unresolved source | "TO BE CONFIRMED" is not a source |
| Approved but past `expires_at` | Stale procedural facts go wrong quietly |

A clean procedural entry — including one mentioning "3 documents" — passes. Precision matters
here for the same reason it does in `guardrails.py`: a validator that rejects good entries gets
bypassed.

### Use `servable_entries()`, not the YAML

```python
from mira.knowledge.validate_kb import servable_entries
kb = servable_entries()      # only approved, unexpired, owned, clean entries
```

Loading `kb-seed.yaml` directly bypasses every check above. Don't.

### Current state: 0 servable, 10 draft

That is the correct state for a freshly seeded base, and the validator says so rather than
failing. Each entry needs MIDTRANS operations to confirm the answer and take ownership.

Four entries (`kb-003`, `kb-006`, `kb-007`, `kb-008`, `kb-009`) are deliberately left unanswered
rather than drafted: Syrian import documentation, served lanes, export compliance, vehicle
import, and port clearance procedure are all subjects where a plausible-sounding guess would be
worse than silence — and where MIDTRANS's own 27 years of experience is the only valid source.
