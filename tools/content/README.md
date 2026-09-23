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

## check_cluster.py

```bash
python3 tools/content/check_cluster.py drafts/representation/*.md
python3 tools/content/tests/test_check_cluster.py
```

Near-duplicate detection across a cluster — the doorway-page pattern that `SEO-STANDARDS` §2 says
is assessed at site level, and that a per-page check cannot see. It masks the subject terms of
both pages and compares what remains, which is the standard's own find-and-replace test.

Measured separation: three templated pages score 100%; this repository's 14 phase documents, 91
pairs, score at most 1.5%. Defaults are 0.35 blocking, 0.20 warning. Recalibrate on the real
cluster — see `../../docs/phases/PHASE-05-CLAIMS-AND-DUPLICATION.md` §4.
