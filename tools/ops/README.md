# Operating checks

Phase 07 does not end; it is operated. These hold the parts a machine can hold.

```bash
python3 tools/ops/market_gate.py
python3 tools/ops/health_check.py --content-root drafts
python3 tools/ops/tests/test_ops.py
```

| File | Purpose |
|---|---|
| `markets.yaml` | The market expansion register — one record per market, four gate tests each |
| `market_gate.py` | Refuses a market open on an incomplete record, and two open at once |
| `health_check.py` | Expired content, ownerless pages, unconfirmed data, register state, every suite |
| `enquiries.csv` | The enquiry register — one row per enquiry, logged on arrival |
| `enquiry_log.py` | Reports genuine enquiries past the acknowledgement window, oldest first |

Full process: `../../docs/phases/PHASE-07-OPERATING-CHECKS.md` and, for the enquiry
register, `../../docs/standards/ENQUIRY-INTAKE.md`.

```bash
python3 tools/ops/enquiry_log.py --window 24
```

`--window` is required and has no default. A response time nobody chose, silently
inherited, is worse than none — the same rule the volumetric divisor follows. The register
ships loaded with the ten unanswered enquiries found in `D3` §8b–§8c, so it starts from
the real backlog rather than from zero.

**The rule that does the work:** demand evidence must contain a number. "There is clear demand
from Turkey" is an opinion. "9 RFQs and 14 MIRA conversations originated in Turkey between January
and June 2026" is evidence. A gate that accepts the first is not a gate.

**What the health check cannot see** — and says so on every run — is whether a page is still
*true*. An unexpired page describing a procedure that changed last month passes every check here.
It tells a reviewer where to start, not what to conclude.

Both work without PyYAML: `market_gate.py` carries a fallback parser, and the suite asserts it
reaches a verdict identical to PyYAML's on a filled record with real failures in it. An earlier
version read only the first gate test and would have passed an incomplete record in silence.
