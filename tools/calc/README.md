# Calculation core for the Phase 03 tools

Pure arithmetic for the MIDTRANS calculators. Standard library only — no dependencies, no
network, no build step.

| File | Purpose |
|---|---|
| `freight_math.py` | CBM, volumetric and chargeable weight, consignment totals, container feasibility |
| `equipment.json` | Container capacities and volumetric divisors — **every row unconfirmed** |
| `tests/test_freight_math.py` | Correctness, refusals, Arabic input, and the prohibition property |

Full specification: `../../docs/phases/PHASE-03-TOOL-CALCULATION-SPEC.md`.

```bash
python3 tools/calc/tests/test_freight_math.py
```

## The three things to know before using it

**The volumetric divisor is required.** `volumetric_weight()` has no default. A divisor is a
commercial convention that differs by carrier and account, not a physical constant, and a default
is a number nobody chose being inherited into every result a customer sees.

**It never says "fits".** `container_feasibility()` returns `EXCEEDS`, `REVIEW`, or `LIKELY_FITS`.
Volumetric fit is not stowability. Rendering `LIKELY_FITS` as a green tick reading "Fits" turns a
calculation into an operational commitment.

**The reference data is unconfirmed.** Container capacities are nominal published figures, not
verified against the equipment MIDTRANS books. Every result carries `data_status`, and the tool
must not go live while `unconfirmed_rows()` returns anything:

```bash
python3 -c "import sys; sys.path.insert(0,'tools/calc'); import freight_math as f; print(f.unconfirmed_rows())"
```

## The prohibition property

The test suite runs every string this module can emit through `mira/guardrails.py`. A calculator
that ever printed a figure in a cost context would fail the suite. The tools and MIRA are held to
one standard, because a customer does not distinguish between them.
