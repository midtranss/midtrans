#!/usr/bin/env python3
"""
Tests for the Phase 03 calculation core.

Three groups, and the third is the one that makes this more than an arithmetic suite:

  * correctness against worked examples
  * refusal on inputs that would produce a plausible wrong answer
  * the prohibition property — no function may emit anything the MIRA guardrail would block

The third reuses mira/guardrails.py, so the tools and the assistant are held to one standard.
A tool that says "fits" or prints a figure in a cost context is the same failure as MIRA doing
it; the surface differs, the customer's reading does not.

Run:  python3 tools/calc/tests/test_freight_math.py
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))       # tools/calc/tests
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))   # repository root
sys.path.insert(0, os.path.dirname(HERE))              # tools/calc
sys.path.insert(0, os.path.join(ROOT, "mira"))         # for the prohibition cross-check

import freight_math as fm  # noqa: E402

failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        failures.append(name)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


# --------------------------------------------------------------------------------------
print("\n=== volume ===")

# 100 x 100 x 100 cm is exactly 1 m3. If this is wrong, everything downstream is.
check("cbm: unit cube", close(fm.cbm(100, 100, 100), 1.0), fm.cbm(100, 100, 100))
check("cbm: quantity multiplies", close(fm.cbm(100, 100, 100, 7), 7.0))
check("cbm: carton 120x80x100", close(fm.cbm(120, 80, 100), 0.96), fm.cbm(120, 80, 100))
check("cbm: order independent",
      close(fm.cbm(120, 80, 100), fm.cbm(100, 120, 80)))

# --------------------------------------------------------------------------------------
print("\n=== volumetric and chargeable weight ===")

# 100x100x100 at the 6000 convention = 1,000,000 / 6000 = 166.67 kg
check("volumetric: divisor 6000", close(fm.volumetric_weight(100, 100, 100, 6000), 1e6 / 6000))
check("volumetric: divisor 5000", close(fm.volumetric_weight(100, 100, 100, 5000), 200.0))
check("volumetric: quantity multiplies",
      close(fm.volumetric_weight(100, 100, 100, 5000, 3), 600.0))

try:
    fm.volumetric_weight(100, 100, 100)  # type: ignore[call-arg]
    check("volumetric: divisor is required", False, "no TypeError raised")
except TypeError:
    check("volumetric: divisor is required", True)

# Light and bulky: volumetric wins, and the tool must say which basis applied.
cw = fm.chargeable_weight(gross_kg=40, volumetric_kg=166.67)
check("chargeable: takes the higher", close(cw.kg, 166.67, 1e-2))
check("chargeable: basis reported", cw.basis == "volumetric" and cw.is_volumetric, cw.basis)

# Dense cargo: gross wins.
cw = fm.chargeable_weight(gross_kg=900, volumetric_kg=166.67)
check("chargeable: gross when denser", cw.basis == "gross" and close(cw.kg, 900.0))
check("chargeable: both figures retained",
      close(cw.gross_kg, 900.0) and close(cw.volumetric_kg, 166.67, 1e-2))

# --------------------------------------------------------------------------------------
print("\n=== consignments ===")

lines = [
    fm.Line(120, 100, 110, weight_kg=180, quantity=10, description="pallets"),
    fm.Line(60, 40, 40, weight_kg=12, quantity=25, description="cartons"),
]
totals = fm.consignment_totals(lines)
check("totals: pieces", totals.pieces == 35, totals.pieces)
check("totals: volume", close(totals.total_cbm, 13.2 + 2.4, 1e-6), totals.total_cbm)
check("totals: weight", close(totals.total_gross_kg, 1800 + 300))
check("totals: heaviest piece", close(totals.heaviest_piece_kg, 180.0))
check("totals: longest dimension", close(totals.longest_dimension_cm, 120.0))
check("totals: density computed", totals.density_kg_per_m3 > 0)

try:
    fm.consignment_totals([])
    check("totals: empty consignment refused", False)
except fm.CalcError:
    check("totals: empty consignment refused", True)

# --------------------------------------------------------------------------------------
print("\n=== inputs that would produce a plausible wrong answer ===")

for bad, label in [
    (0, "zero"),
    (-5, "negative"),
    ("abc", "non-numeric"),
    (float("nan"), "NaN"),
    (float("inf"), "infinity"),
    (5000, "metres typed as centimetres"),
]:
    try:
        fm.cbm(bad, 100, 100)
        check(f"refuses {label}", False, "no CalcError")
    except fm.CalcError:
        check(f"refuses {label}", True)

try:
    fm.cbm(100, 100, 100, 0)
    check("refuses zero quantity", False)
except fm.CalcError:
    check("refuses zero quantity", True)

# --------------------------------------------------------------------------------------
print("\n=== Arabic-Indic input ===")

# An Arabic form submits these. Rejecting them makes the calculator unusable in Arabic while
# still appearing to work in English, which is the worst of both.
check("accepts Arabic-Indic digits", close(fm.cbm("١٠٠", "١٠٠", "١٠٠"), 1.0),
      fm.cbm("١٠٠", "١٠٠", "١٠٠"))
check("accepts Persian digits", close(fm.cbm("۱۰۰", 100, 100), 1.0))
check("accepts Arabic decimal mark", close(fm.cbm("١٢٠٫٥", 100, 100), 1.205, 1e-9),
      fm.cbm("١٢٠٫٥", 100, 100))
check("accepts Arabic thousands separator", close(fm.cbm("1,200", 100, 100), 12.0))
check("Arabic quantity counted", close(fm.cbm(100, 100, 100, "٥"), 5.0))
check("mixed script still validated",
      close(fm.volumetric_weight("١٠٠", 100, 100, "٦٠٠٠"), 1e6 / 6000))

try:
    fm.cbm("١٠٠٠٠", 100, 100)   # 10,000 cm — over the plausible limit
    check("Arabic digits still range-checked", False)
except fm.CalcError:
    check("Arabic digits still range-checked", True)

# --------------------------------------------------------------------------------------
print("\n=== container feasibility never promises ===")

boxes = fm.containers()
check("equipment: three containers loaded", set(boxes) == {"20GP", "40GP", "40HC"}, str(set(boxes)))

small = fm.consignment_totals([fm.Line(100, 100, 100, weight_kg=200, quantity=5)])
verdict = fm.container_feasibility(small, boxes["40HC"])
check("feasibility: comfortable load is LIKELY_FITS", verdict.verdict is fm.Fit.LIKELY_FITS,
      verdict.verdict)
check("feasibility: never uses the word 'fits' as a promise",
      verdict.verdict.value != "fits")

over = fm.consignment_totals([fm.Line(100, 100, 100, weight_kg=200, quantity=70)])
verdict = fm.container_feasibility(over, boxes["40HC"])
check("feasibility: over volume is EXCEEDS", verdict.verdict is fm.Fit.EXCEEDS, verdict.verdict)
check("feasibility: reason given", any("Volume" in r for r in verdict.reasons), str(verdict.reasons))

heavy = fm.consignment_totals([fm.Line(100, 100, 100, weight_kg=2000, quantity=20)])
verdict = fm.container_feasibility(heavy, boxes["20GP"])
check("feasibility: over payload is EXCEEDS", verdict.verdict is fm.Fit.EXCEEDS)
check("feasibility: payload reason given", any("payload" in r for r in verdict.reasons))

# A piece wider than the door: inside the volume, still a problem. This is the case a naive
# CBM calculator gets wrong and a customer discovers at the warehouse.
wide = fm.consignment_totals([fm.Line(400, 250, 100, weight_kg=500, quantity=1)])
verdict = fm.container_feasibility(wide, boxes["40HC"])
check("feasibility: door aperture considered", verdict.verdict is not fm.Fit.LIKELY_FITS,
      verdict.verdict)
check("feasibility: door reason given", any("door" in r for r in verdict.reasons),
      str(verdict.reasons))

# Near the limit: arithmetic says yes, stowage decides.
near = fm.consignment_totals([fm.Line(100, 100, 100, weight_kg=100, quantity=58)])
verdict = fm.container_feasibility(near, boxes["40HC"])
check("feasibility: near capacity needs review", verdict.verdict is fm.Fit.REVIEW,
      f"{verdict.verdict} at {verdict.volume_utilisation:.2f}")
check("feasibility: needs_human set", verdict.needs_human)

# --------------------------------------------------------------------------------------
print("\n=== reference data is unconfirmed until someone owns it ===")

pending = fm.unconfirmed_rows()
check("every reference row is unconfirmed", len(pending) == 5, str(pending))
check("results carry data_status",
      fm.container_feasibility(small, boxes["40HC"]).data_status == "unconfirmed")
check("unconfirmed data is stated in the reasons",
      any("UNCONFIRMED" in r for r in fm.container_feasibility(small, boxes["40HC"]).reasons))

air = fm.divisor("air")
check("divisor lookup returns the whole row", air["status"] == "unconfirmed" and "source" in air)
try:
    fm.divisor("sea")
    check("unknown mode refused, not guessed", False)
except fm.CalcError:
    check("unknown mode refused, not guessed", True)

# --------------------------------------------------------------------------------------
print("\n=== the prohibition property ===")

try:
    import guardrails  # noqa: E402
    have_guardrails = True
except ImportError:
    have_guardrails = False

if not have_guardrails:
    check("guardrails importable for the cross-check", False, "mira/guardrails.py not found")
else:
    # Everything these functions can say to a user, in one place.
    emitted = []
    for box in boxes.values():
        for totals_case in (small, over, heavy, wide, near):
            v = fm.container_feasibility(totals_case, box)
            emitted.extend(v.reasons)
            emitted.append(v.verdict.value)
    for bad_input in (0, -5, "abc", 5000):
        try:
            fm.cbm(bad_input, 100, 100)
        except fm.CalcError as exc:
            emitted.append(str(exc))
    try:
        fm.divisor("sea")
    except fm.CalcError as exc:
        emitted.append(str(exc))

    blocked = [(t, guardrails.check_response(t).rules)
               for t in emitted if guardrails.check_response(t).blocked]
    check(f"no tool output trips a guardrail rule ({len(emitted)} strings checked)",
          not blocked, str(blocked[:2]))

    # And the inverse: the guardrail would catch it if a rate ever crept in here.
    check("the cross-check has teeth",
          guardrails.check_response("The rate is USD 4500 per 40HC.").blocked)

# --------------------------------------------------------------------------------------
print()
if failures:
    print(f"Freight calculation suite: {len(failures)} FAILED — {', '.join(failures)}")
    sys.exit(1)
print("Freight calculation suite: all checks passed")
