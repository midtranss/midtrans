#!/usr/bin/env python3
"""
Market expansion gate — PHASE-07 Part B.

Phase 07's first risk is "market gates bypassed under commercial pressure", mitigated by "a
decision recorded in writing by the programme owner". A decision recorded in prose is a decision
nobody can check. This makes the record structured and the gate mechanical.

    python3 tools/ops/market_gate.py
    python3 tools/ops/market_gate.py --file tools/ops/markets.yaml

The rule that does most of the work: **demand evidence must contain a number.** "There is clear
demand from Turkey" is an opinion. "9 RFQs and 14 MIRA conversations originated in Turkey between
January and June 2026" is evidence. A gate that accepts the first is not a gate — it is the
sentence someone writes on the way to doing what they had already decided.

Exit 0 when the register is consistent, 1 when a market is open on an incomplete record or more
than one is open, 2 when the file cannot be read.
"""

from __future__ import annotations

import argparse
import os
import re
import sys

DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "markets.yaml")

TESTS = ("demand_evidence", "operational_reality", "capacity", "named_owner")
ACTIVE = ("open", "live")
STATUSES = ("candidate", "open", "live", "retired", "rejected")

# Minimum words for a piece of evidence to be an answer rather than a restatement. Same
# discipline as the uniqueness field in the Phase 04 editorial gate.
MIN_EVIDENCE_WORDS = 10

NOT_A_PERSON = {
    "operations", "ops", "team", "the team", "marketing", "midtrans", "management",
    "tbd", "n/a", "none", "sales",
}


def load(path: str) -> list:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        return data.get("markets", []) if isinstance(data, dict) else []
    except ImportError:
        return _load_fallback(text)


def _load_fallback(text: str) -> list:
    """Structural parse sufficient for validation when PyYAML is absent.

    Mirrors mira/knowledge/validate_kb.py: the checks must run on a machine with nothing
    installed, because the one time they are skipped is the time they were needed. The suite
    asserts this parser reaches the same verdict as PyYAML — an earlier version read only the
    first gate test and would have passed an incomplete record in silence.
    """
    markets: list = []
    current: dict | None = None
    in_gate = False
    test: str | None = None

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()

        if line.startswith("- market:"):
            current = {"gate": {}}
            markets.append(current)
            current["market"] = _value(line.split(":", 1)[1])
            in_gate, test = False, None
            continue
        if current is None:
            continue

        key = line.split(":", 1)[0].strip().lstrip("- ")

        # A gate test header: two levels in, no value, and a name we recognise.
        if in_gate and key in TESTS and line.rstrip().endswith(":"):
            test = key
            current["gate"][test] = {}
            continue

        if key == "gate" and line.rstrip().endswith(":"):
            in_gate, test = True, None
            continue

        # Any other top-level key ends the gate block.
        if indent <= 4 and not line.rstrip().endswith(":"):
            in_gate, test = False, None

        if ":" not in line:
            continue
        _, _, value = line.partition(":")
        value = _value(value)

        if test is not None and indent >= 8:
            current["gate"][test][key] = value
        elif not in_gate:
            current[key] = value

    return markets


def _value(raw: str):
    value = raw.strip().strip('"').strip("'")
    if value in ("null", "~", ""):
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    return value


def _evidence_of(market: dict, test: str) -> str:
    block = (market.get("gate") or {}).get(test) or {}
    return str(block.get("evidence") or "")


def _passed(market: dict, test: str) -> bool:
    block = (market.get("gate") or {}).get(test) or {}
    return block.get("passed") is True


def check_market(market: dict) -> list:
    name = market.get("market", "?")
    status = (market.get("status") or "").strip()
    problems = []

    if status not in STATUSES:
        problems.append(f"status {status!r} is not one of {', '.join(STATUSES)}")
    if status not in ACTIVE:
        # A candidate, retired or rejected market needs nothing more. A rejected one should
        # carry its reason so it is not re-argued every quarter, but that is advice, not a gate.
        if status == "rejected" and not _evidence_of(market, "demand_evidence"):
            problems.append(
                "rejected with no reason recorded — it will be re-litigated next quarter")
        return problems

    for test in TESTS:
        if not _passed(market, test):
            problems.append(f"{status} but gate test '{test}' is not marked passed")
            continue
        evidence = _evidence_of(market, test)
        if len(evidence.split()) < MIN_EVIDENCE_WORDS:
            problems.append(
                f"'{test}' is marked passed with {len(evidence.split())} words of evidence. "
                f"At least {MIN_EVIDENCE_WORDS} — state what was observed, not that it was")

    # The rule that separates evidence from assertion.
    demand = _evidence_of(market, "demand_evidence")
    if _passed(market, "demand_evidence") and not re.search(r"\d", demand):
        problems.append(
            "demand evidence contains no number. Enquiries, sessions or conversations from "
            "that market — a count and a period. Without one this is an opinion")

    owner = (market.get("owner") or "").strip()
    if not owner:
        problems.append(f"{status} with no owner. Test 4 is a named person")
    elif owner.lower() in NOT_A_PERSON:
        problems.append(f"owner is {owner!r}. A team is not accountable; a person is")

    if not (market.get("target") or "").strip():
        problems.append(
            "no target recorded. PHASE-07's own gate is 'assessed against a target agreed "
            "BEFORE the market opened' — set after the fact, it is a description, not a gate")

    for field in ("opened_at", "decision_recorded_at"):
        value = market.get(field)
        if not value:
            problems.append(f"{status} with no {field}")
        elif not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(value)):
            problems.append(f"{field} must be YYYY-MM-DD, got {value!r}")

    if not (market.get("decision_recorded_by") or "").strip():
        problems.append("no decision_recorded_by — the programme owner signs the gate decision")

    return problems


def check_register(markets: list) -> tuple[dict, list]:
    per_market = {m.get("market", f"#{i}"): check_market(m) for i, m in enumerate(markets)}

    register = []
    open_markets = [m.get("market") for m in markets if (m.get("status") or "") == "open"]
    if len(open_markets) > 1:
        register.append(
            "More than one market is open: " + ", ".join(open_markets) + ". PHASE-07 Part B: "
            "one at a time. Parallel expansion is how translation debt and half-finished "
            "clusters accumulate")

    names = [m.get("market") for m in markets]
    duplicates = {n for n in names if names.count(n) > 1 and n}
    if duplicates:
        register.append("Duplicate market entries: " + ", ".join(sorted(duplicates)))

    for market in markets:
        if (market.get("status") or "") == "live" and not market.get("opened_at"):
            register.append(
                f"{market.get('market')} is live but was never opened — a market cannot skip "
                "the gate by being published")

    return per_market, register


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--file", default=DEFAULT_FILE)
    args = parser.parse_args()

    try:
        markets = load(args.file)
    except OSError as exc:
        print(f"Could not read {args.file}: {exc}", file=sys.stderr)
        return 2

    per_market, register = check_register(markets)

    print("\nMARKET EXPANSION GATE")
    print("=" * 72)

    by_status: dict = {}
    for market in markets:
        by_status.setdefault(market.get("status") or "?", []).append(market.get("market"))
    for status in STATUSES:
        if by_status.get(status):
            print(f"  {status:<10} {', '.join(by_status[status])}")
    print()

    problems = 0
    for name, issues in per_market.items():
        if not issues:
            continue
        problems += len(issues)
        print(f"  {name}")
        for issue in issues:
            print(f"    - {issue}")
        print()

    for issue in register:
        problems += 1
        print(f"  REGISTER: {issue}\n")

    print("-" * 72)
    if not problems:
        active = by_status.get("open", []) + by_status.get("live", [])
        if active:
            print(f"  Register consistent. Active: {', '.join(active)}")
        else:
            print("  Register consistent. No market is open — which is a valid state, and the")
            print("  correct one until a market has evidence behind it.")
    else:
        print(f"  {problems} problem(s). A market on an incomplete record is not through the")
        print("  gate, whatever the file says its status is.")

    print("\n  This checks that a decision was recorded, not that it was right. Whether 9 RFQs")
    print("  justify a market is a commercial judgement — the gate only insists the number")
    print("  exists and that somebody put their name to the decision.")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
