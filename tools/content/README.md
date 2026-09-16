# Content gate

Pre-publication check for MIDTRANS content pages. Standard library only.

```bash
python3 tools/content/check_page.py drafts/*.md
python3 tools/content/tests/test_check_page.py
```

Full process: `../../docs/phases/PHASE-04-EDITORIAL-GATE.md`.

| Exit | Meaning |
|---|---|
| 0 | No blockers. Warnings may still be present |
| 1 | At least one blocker — the page does not publish |
| 2 | A file could not be read |

It enforces `WRITING-STANDARDS.md`, `SEO-STANDARDS.md` §2, and Phase 04's out-of-scope list, and
runs the prose through `mira/guardrails.py` so the content and the assistant are held to one
standard.

**It cannot apply the uniqueness test.** That is a human judgement. All the tool does is refuse to
pass a page whose reviewer has not recorded one, and say so on every run — including a clean one.
A clean run is a licence to review, not a licence to publish.
