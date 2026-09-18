#!/usr/bin/env python3
"""
Calculation core for the Phase 03 tools.

Scope, and the reason it is drawn here: these functions compute **physical and documentary
facts** — volume, weight, chargeable basis, whether a consignment could physically fit. They do
not compute, estimate, or imply a price, a rate, a transit time, a duty, a customs cost, or an
acceptance decision. That boundary is enforced by a test, not only by intention.

Two design choices carry most of the safety:

1. `volumetric_weight()` takes the divisor as a **required argument with no default.** A divisor
   is a commercial convention that differs by carrier, mode and contract. A default would be a
   number nobody chose, silently inherited into every quote.

2. `container_feasibility()` never returns "it fits". Volumetric fit is not stowability: cargo
   shape, stacking, pallet footprint and door aperture all decide the real answer, and a
   calculator that says "fits" has made an operational claim on MIDTRANS's behalf. It returns
   EXCEEDS, REVIEW, or LIKELY_FITS — and LIKELY_FITS still means "send it to the team".

See ../../docs/phases/PHASE-03-TOOL-CALCULATION-SPEC.md.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from enum import Enum

_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "equipment.json")


class CalcError(ValueError):
    """An input that cannot produce a meaningful answer. Never swallowed."""


# --------------------------------------------------------------------------------------
# Validation — a wrong answer is worse than a refusal
# --------------------------------------------------------------------------------------

# Cargo dimensions arrive from a web form, and the two errors that actually occur are a unit
# mix-up (metres typed into a centimetres field) and a transposed decimal. Both produce a
# plausible-looking number, which is why they are caught here rather than trusted.
_MAX_DIM_CM = 2000.0     # 20 m — longer than any standard container
_MAX_WEIGHT_KG = 100000.0


# An Arabic-language form submits Arabic-Indic digits. Rejecting them as "not a number" would
# make the calculator unusable in Arabic while appearing to work — the same fold guardrails.py
# applies to MIRA's output.
_DIGITS = {ord(c): str(i % 10) for i, c in enumerate("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹")}
_DECIMAL_MARKS = {ord("٫"): ".", ord("،"): "", ord(","): ""}


def _to_number(value):
    """Parse a number, accepting Arabic-Indic digits and Arabic separators."""
    if isinstance(value, str):
        value = value.strip().translate(_DIGITS).translate(_DECIMAL_MARKS)
    return float(value)


def _positive(value, name: str, limit: float) -> float:
    try:
        number = _to_number(value)
    except (TypeError, ValueError):
        raise CalcError(f"{name} must be a number, got {value!r}") from None
    if number != number or number in (float("inf"), float("-inf")):
        raise CalcError(f"{name} must be a real number")
    if number <= 0:
        raise CalcError(f"{name} must be greater than zero, got {number}")
    if number > limit:
        raise CalcError(
            f"{name} of {number} exceeds the plausible limit of {limit:g}. "
            "Check the unit — centimetres and kilograms are expected."
        )
    return number


def _count(value, name: str = "quantity") -> int:
    try:
        number = int(_to_number(value))
    except (TypeError, ValueError, OverflowError):
        raise CalcError(f"{name} must be a whole number, got {value!r}") from None
    if number < 1:
        raise CalcError(f"{name} must be at least 1, got {number}")
    return number


# --------------------------------------------------------------------------------------
# Volume and weight
# --------------------------------------------------------------------------------------

def cbm(length_cm, width_cm, height_cm, quantity=1) -> float:
    """Volume in cubic metres. Dimensions in centimetres."""
    length = _positive(length_cm, "length_cm", _MAX_DIM_CM)
    width = _positive(width_cm, "width_cm", _MAX_DIM_CM)
    height = _positive(height_cm, "height_cm", _MAX_DIM_CM)
    return length * width * height * _count(quantity) / 1_000_000.0


def volumetric_weight(length_cm, width_cm, height_cm, divisor_cm3_per_kg, quantity=1) -> float:
    """Volumetric weight in kilograms.

    `divisor_cm3_per_kg` is required and has no default, deliberately. Air is conventionally
    6000 and express 5000, but conventions differ by carrier and by account — see
    equipment.json, where both are recorded as unconfirmed. Pass the value operations has
    confirmed for the mode and partner in question.
    """
    divisor = _positive(divisor_cm3_per_kg, "divisor_cm3_per_kg", 100_000.0)
    length = _positive(length_cm, "length_cm", _MAX_DIM_CM)
    width = _positive(width_cm, "width_cm", _MAX_DIM_CM)
    height = _positive(height_cm, "height_cm", _MAX_DIM_CM)
    return length * width * height * _count(quantity) / divisor


@dataclass(frozen=True)
class ChargeableWeight:
    kg: float
    basis: str            # "gross" or "volumetric"
    gross_kg: float
    volumetric_kg: float

    @property
    def is_volumetric(self) -> bool:
        return self.basis == "volumetric"


def chargeable_weight(gross_kg, volumetric_kg) -> ChargeableWeight:
    """The higher of gross and volumetric, and which one it was.

    The basis is returned because it is the part that changes a customer's decision: light,
    bulky cargo charged on volume is the single most common surprise in air freight, and a
    tool that reports only a number teaches the customer nothing.
    """
    gross = _positive(gross_kg, "gross_kg", _MAX_WEIGHT_KG)
    volumetric = _positive(volumetric_kg, "volumetric_kg", _MAX_WEIGHT_KG)
    if volumetric > gross:
        return ChargeableWeight(volumetric, "volumetric", gross, volumetric)
    return ChargeableWeight(gross, "gross", gross, volumetric)


# --------------------------------------------------------------------------------------
# Consignments
# --------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Line:
    length_cm: float
    width_cm: float
    height_cm: float
    # Per piece. `None` means NOT SUPPLIED YET — which is different from wrong, and the
    # distinction is the point. Zero is still an error: zero is a wrong number, None is an
    # absent one. Half the enquiries in the register arrive with dimensions and no weight
    # (2026-09-16-sprinters gives dimensions per vehicle for six vehicles and no weight at
    # all), and a tool that refuses to compute anything without it teaches the desk to type a
    # weight in to make the tool run. An invented weight is worse than a missing one.
    weight_kg: float | None
    quantity: int = 1
    description: str = ""


@dataclass(frozen=True)
class Totals:
    pieces: int
    total_cbm: float
    total_gross_kg: float | None       # None when any line's weight was not supplied
    heaviest_piece_kg: float | None
    longest_dimension_cm: float
    density_kg_per_m3: float | None

    @property
    def weight_known(self) -> bool:
        return self.total_gross_kg is not None


def consignment_totals(lines) -> Totals:
    """Roll up mixed cargo lines.

    Reports the longest single dimension and the heaviest single piece alongside the totals,
    because those — not the total — are what make a consignment awkward. Cargo that fits by
    volume and fails at the door is a real and expensive outcome.
    """
    if not lines:
        raise CalcError("A consignment needs at least one line")

    pieces = 0
    volume = 0.0
    weight = 0.0
    heaviest = 0.0
    longest = 0.0
    # One line without a weight makes every weight-derived total unknown. It is not summed as
    # zero and it is not skipped: either would report a total that reads as complete.
    any_weight_missing = False

    for index, line in enumerate(lines, start=1):
        quantity = _count(line.quantity, f"line {index} quantity")
        volume += cbm(line.length_cm, line.width_cm, line.height_cm, quantity)
        pieces += quantity
        longest = max(longest, line.length_cm, line.width_cm, line.height_cm)

        if line.weight_kg is None:
            any_weight_missing = True
            continue
        per_piece_kg = _positive(line.weight_kg, f"line {index} weight_kg", _MAX_WEIGHT_KG)
        weight += per_piece_kg * quantity
        heaviest = max(heaviest, per_piece_kg)

    return Totals(
        pieces=pieces,
        total_cbm=volume,
        total_gross_kg=None if any_weight_missing else weight,
        heaviest_piece_kg=None if any_weight_missing else heaviest,
        longest_dimension_cm=float(longest),
        density_kg_per_m3=None if (any_weight_missing or not volume) else weight / volume,
    )


# --------------------------------------------------------------------------------------
# Container feasibility — deliberately not "does it fit"
# --------------------------------------------------------------------------------------

class Fit(Enum):
    EXCEEDS = "exceeds"          # over capacity on volume, payload, or a single dimension
    REVIEW = "review"            # inside capacity but close enough that stowage decides
    LIKELY_FITS = "likely_fits"  # comfortable margin — still not a promise


# Real container utilisation is well below 100%: cartons do not tessellate, pallets waste the
# space above them, and stacking limits apply. The default margin is intentionally conservative
# and is a parameter, so operations can set what their own loading experience supports.
DEFAULT_USABLE_FRACTION = 0.80


@dataclass(frozen=True)
class Feasibility:
    verdict: Fit
    container: str
    volume_utilisation: float        # of usable volume, not nominal
    payload_utilisation: float | None   # None when the gross weight was not supplied
    reasons: list = field(default_factory=list)
    data_status: str = "unconfirmed"

    @property
    def needs_human(self) -> bool:
        return self.verdict is not Fit.LIKELY_FITS


def container_feasibility(totals: Totals, container: dict,
                          usable_fraction: float = DEFAULT_USABLE_FRACTION) -> Feasibility:
    """Whether a consignment could physically go in one container of this type.

    Never returns a yes. `LIKELY_FITS` means the numbers leave room; it does not mean the cargo
    is stowable, and the tool must say so wherever this is displayed.
    """
    fraction = _positive(usable_fraction, "usable_fraction", 1.0)
    usable_volume = float(container["internal_volume_m3"]) * fraction
    payload = float(container["max_payload_kg"])

    volume_use = totals.total_cbm / usable_volume if usable_volume else float("inf")
    payload_use = (None if not totals.weight_known
                   else (totals.total_gross_kg / payload if payload else float("inf")))

    reasons = []
    verdict = Fit.LIKELY_FITS

    if totals.total_cbm > usable_volume:
        verdict = Fit.EXCEEDS
        reasons.append(
            f"Volume {totals.total_cbm:.2f} m³ exceeds the usable "
            f"{usable_volume:.2f} m³ ({fraction:.0%} of nominal)."
        )
    if totals.weight_known and totals.total_gross_kg > payload:
        verdict = Fit.EXCEEDS
        reasons.append(
            f"Weight {totals.total_gross_kg:,.0f} kg exceeds the payload {payload:,.0f} kg."
        )

    door_limit = min(float(container["door_width_cm"]), float(container["door_height_cm"]))
    if totals.longest_dimension_cm > float(container["internal_length_cm"]):
        verdict = Fit.EXCEEDS
        reasons.append(
            f"A piece measuring {totals.longest_dimension_cm:.0f} cm is longer than the "
            f"container interior."
        )
    elif totals.longest_dimension_cm > door_limit:
        verdict = Fit.EXCEEDS if verdict is Fit.EXCEEDS else Fit.REVIEW
        reasons.append(
            f"A piece measuring {totals.longest_dimension_cm:.0f} cm is wider than the door "
            f"aperture ({door_limit:.0f} cm). It may still load, but not through the door "
            "in that orientation."
        )

    if verdict is Fit.LIKELY_FITS and (volume_use > 0.9 or (payload_use or 0) > 0.9):
        verdict = Fit.REVIEW
        reasons.append(
            "Above 90% of usable capacity. At this level stowage, not arithmetic, decides."
        )

    # An unsupplied weight can never produce a comfortable verdict. Volume alone is a real and
    # useful answer — "will six vehicles physically go in one box" is decided by dimensions —
    # but a container is limited by payload as well, and reporting LIKELY_FITS while half the
    # constraint is unmeasured would be a yes the data does not support. REVIEW is the most
    # this can say, and the reason names exactly what is missing.
    if not totals.weight_known:
        verdict = Fit.EXCEEDS if verdict is Fit.EXCEEDS else Fit.REVIEW
        reasons.append(
            "Gross weight was not supplied, so the payload limit could not be checked. This "
            "verdict covers volume and dimensions only."
        )

    if container.get("status") != "confirmed":
        reasons.append(
            "Container capacities are UNCONFIRMED — nominal published figures, not verified "
            "against the equipment MIDTRANS books. Operations must confirm before this is shown "
            "to a customer."
        )

    return Feasibility(
        verdict=verdict,
        container=container.get("code", "?"),
        volume_utilisation=volume_use,
        payload_utilisation=payload_use,
        reasons=reasons,
        data_status=container.get("status", "unconfirmed"),
    )


# --------------------------------------------------------------------------------------
# Reference data
# --------------------------------------------------------------------------------------

def load_equipment(path: str = _DATA) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def containers(path: str = _DATA) -> dict:
    return {c["code"]: c for c in load_equipment(path)["containers"]}


def divisor(mode: str, path: str = _DATA) -> dict:
    """Look up a volumetric divisor. Returns the whole row so the caller sees its status."""
    for row in load_equipment(path)["volumetric_divisors"]["rows"]:
        if row["mode"] == mode:
            return row
    raise CalcError(
        f"No divisor recorded for mode {mode!r}. Add it to equipment.json with a source, "
        "rather than passing a number from memory."
    )


def unconfirmed_rows(path: str = _DATA) -> list:
    """Every reference row still awaiting an owner's confirmation."""
    data = load_equipment(path)
    rows = [("container", c["code"]) for c in data["containers"] if c.get("status") != "confirmed"]
    rows += [("divisor", r["mode"]) for r in data["volumetric_divisors"]["rows"]
             if r.get("status") != "confirmed"]
    return rows
