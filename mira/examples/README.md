# What to ask for when exporting MIRA's conversations

`../audit_logs.py` answers the one question nothing else in this programme can:
**has the live MIRA already quoted a rate, a transit time, a customs cost, an acceptance or a
capacity commitment to a real customer?** It cannot answer it without a log export.

The two files here are **synthetic examples, not real conversations.** They exist so the person
doing the export can see the shape and check their file against it before sending anything.

## What is actually needed

One row or object per message, with three things. Nothing else is required:

| Needed | Accepted field names |
|---|---|
| **Who spoke** | `role`, `sender`, `author`, `from`, `speaker`, `type`, `direction` |
| **What was said** — the full text | `content`, `text`, `message`, `body`, `response`, `output`, `answer` |
| **Which conversation** | `conversation_id`, `session_id`, `thread_id`, `chat_id`, `sid` |

Helpful but optional: `timestamp` (or `created_at`, `time`, `date`) and `language` (`lang`).

MIRA's own messages are recognised from `assistant`, `mira`, `bot`, `ai`, `agent`, `outbound`.
Any other word works too — pass it with `--role-value`.

**Customer messages must be included, not stripped.** The check reads the customer's preceding
turn as context so it does not blame MIRA for a word the customer used — "can you *guarantee*
space?" in a question is not a capacity commitment in the answer. They are never scanned for
violations themselves.

## Formats

JSONL, JSON, or CSV — detected automatically, including a CSV saved as `.log` or `.txt`.

```bash
python3 mira/audit_logs.py export.jsonl
python3 mira/audit_logs.py export.csv
python3 mira/audit_logs.py export.csv --role-field sender --text-field body   # if auto-detect misses
```

## Before sending the file anywhere

This is **customer conversation data**. It is sensitive, and the tool treats it that way:

- It runs **entirely locally**. No network call is made and nothing is uploaded.
- Email addresses and phone numbers in printed excerpts are **masked by default**.
- Full message bodies are never printed — only short excerpts around a match.

Names and company details will still be inside the file itself. Handle it as you would any
customer record.

## What the output means

```
  ⚠  MESSAGES THAT WOULD BE BLOCKED   3  (60.0%)
```

That is **what the guardrail would stop today**, not a count of proven mistakes. The check is
deliberately cautious and some findings are false positives — §8a of `MIRA-GUARDRAILS.md` records
four real ones. Verify by hand before acting.

Exit codes: `0` nothing blocked · `1` something blocked · **`2` nothing was scanned** — an
explicit error, because a silent zero on a file that was never read is the dangerous outcome.
