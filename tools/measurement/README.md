# Measurement tools

Small, dependency-free scripts supporting the measurement framework. Standard library only —
they must run anywhere, including on a laptop with no project setup.

| Script | Purpose |
|---|---|
| `sample_size.py` | Generates the minimum-detectable-effect and sample-size tables in `../../docs/phases/PHASE-01-MEASUREMENT-FRAMEWORK.md` §6–§7 |

## sample_size.py

```
python3 tools/measurement/sample_size.py
python3 tools/measurement/sample_size.py --baseline 34
```

Pass `--baseline` the real actionable-RFQ count per 4 weeks from `D6-BASELINE.md`. The script adds
the row that actually applies and says plainly whether the count metric can carry the gate
decision at that volume.

All tables assume 80% power and α = 0.05 two-sided, comparing a baseline period against a test
period of equal length.

**These are planning figures, not results.** They say what a comparison would be capable of
detecting — never what it found.
