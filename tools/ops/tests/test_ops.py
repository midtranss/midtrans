#!/usr/bin/env python3
"""
Tests for the Phase 07 operating checks.

The market gate's whole purpose is to refuse a market that has not passed it, so most of this
suite is the refusals. The one that matters most is the demand-evidence rule: a gate that
accepts "there is clear demand from Turkey" is not a gate, it is the sentence someone writes on
the way to doing what they had already decided.

Run:  python3 tools/ops/tests/test_ops.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import market_gate as mg  # noqa: E402

failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        failures.append(name)


GOOD_DEMAND = ("9 RFQs and 14 MIRA conversations originated in Turkey between January and "
               "June 2026, per the D3 method")
GOOD_OPS = ("We run weekly consolidations through Mersin with a partner we have used since "
            "2019 and can name")
GOOD_CAPACITY = ("One writer for six weeks and a Turkish reviewer confirmed available without "
                 "pausing the Syria cluster")
GOOD_OWNER = ("Khaldoun Alhaj owns the market's content and its enquiries, confirmed at the "
              "September management review")


def market(**overrides):
    base = {
        "market": "turkey-to-syria",
        "status": "open",
        "owner": "Khaldoun Alhaj",
        "target": "12 qualified RFQs from Turkey in the first two quarters",
        "opened_at": "2026-09-16",
        "decision_recorded_by": "Khaldoun Alhaj",
        "decision_recorded_at": "2026-09-16",
        "gate": {
            "demand_evidence": {"passed": True, "evidence": GOOD_DEMAND},
            "operational_reality": {"passed": True, "evidence": GOOD_OPS},
            "capacity": {"passed": True, "evidence": GOOD_CAPACITY},
            "named_owner": {"passed": True, "evidence": GOOD_OWNER},
        },
    }
    for key, value in overrides.items():
        if key.startswith("gate."):
            _, test, field = key.split(".", 2)
            base["gate"][test][field] = value
        else:
            base[key] = value
    return base


# --------------------------------------------------------------------------------------
print("\n=== a complete record passes ===")

check("fully recorded open market has no problems", not mg.check_market(market()),
      str(mg.check_market(market())))
check("a candidate needs nothing", not mg.check_market(market(status="candidate")))
check("a retired market needs nothing", not mg.check_market(market(status="retired")))

# --------------------------------------------------------------------------------------
print("\n=== the demand-evidence rule ===")

problems = mg.check_market(market(**{
    "gate.demand_evidence.evidence":
        "There is clear and growing demand from the Turkish market for our services"}))
check("evidence without a number is refused",
      any("no number" in p for p in problems), str(problems))

problems = mg.check_market(market(**{"gate.demand_evidence.evidence": "9 RFQs"}))
check("a number alone is too short to be evidence",
      any("words of evidence" in p for p in problems), str(problems))

check("a real count and period passes", not mg.check_market(market()))

# --------------------------------------------------------------------------------------
print("\n=== each gate test must actually be passed ===")

for test in mg.TESTS:
    problems = mg.check_market(market(**{f"gate.{test}.passed": False}))
    check(f"'{test}' not passed blocks", any(test in p for p in problems), str(problems))

    problems = mg.check_market(market(**{f"gate.{test}.evidence": "yes"}))
    check(f"'{test}' passed on no evidence blocks",
          any(test in p and "words of evidence" in p for p in problems), str(problems))

# --------------------------------------------------------------------------------------
print("\n=== owner, target, dates ===")

check("no owner blocks", any("no owner" in p for p in mg.check_market(market(owner=None))))
check("a team is not an owner",
      any("not accountable" in p for p in mg.check_market(market(owner="Operations"))))
check("no target blocks",
      any("no target" in p for p in mg.check_market(market(target=""))))
check("target must predate opening — the rule is stated",
      any("BEFORE" in p for p in mg.check_market(market(target=""))))
check("no opened_at blocks",
      any("opened_at" in p for p in mg.check_market(market(opened_at=None))))
check("a loose date blocks",
      any("YYYY-MM-DD" in p for p in mg.check_market(market(opened_at="Sept 2026"))))
check("no signatory blocks",
      any("decision_recorded_by" in p for p in mg.check_market(market(decision_recorded_by=""))))

# --------------------------------------------------------------------------------------
print("\n=== one market at a time ===")

two_open = [market(), market(market="uae-to-syria")]
_, register = mg.check_register(two_open)
check("two open markets is a register error",
      any("More than one market is open" in r for r in register), str(register))

one_open = [market(), market(market="uae-to-syria", status="candidate")]
_, register = mg.check_register(one_open)
check("one open and one candidate is fine", not register, str(register))

live_and_open = [market(status="live"), market(market="uae-to-syria", status="open")]
_, register = mg.check_register(live_and_open)
check("a live market does not block the next one opening", not register, str(register))

_, register = mg.check_register([market(), market(market="turkey-to-syria", status="candidate")])
check("duplicate entries are caught",
      any("Duplicate" in r for r in register), str(register))

_, register = mg.check_register([market(status="live", opened_at=None)])
check("live without ever being opened is caught",
      any("never opened" in r for r in register), str(register))

# --------------------------------------------------------------------------------------
print("\n=== the register ships in the correct state ===")

real = mg.load(mg.DEFAULT_FILE)
check("register parses", len(real) == 4, f"{len(real)} markets")
per_market, register = mg.check_register(real)
check("register is consistent as shipped", not any(per_market.values()) and not register,
      str(per_market))
check("no market is open yet",
      all((m.get("status") or "") == "candidate" for m in real),
      str([(m.get("market"), m.get("status")) for m in real]))

# The fallback parser must produce the same verdict as PyYAML, because the one machine that
# lacks PyYAML is the one where the check silently stops working.
with open(mg.DEFAULT_FILE, encoding="utf-8") as fh:
    fallback = mg._load_fallback(fh.read())
check("fallback parser finds the same markets",
      [m.get("market") for m in fallback] == [m.get("market") for m in real],
      str([m.get("market") for m in fallback]))
check("fallback parser reads the gate structure",
      all(set(m.get("gate", {})) == set(mg.TESTS) for m in fallback),
      str([set(m.get("gate", {})) for m in fallback][:1]))
fb_per_market, fb_register = mg.check_register(fallback)
check("fallback reaches the same verdict",
      not any(fb_per_market.values()) and not fb_register, str(fb_per_market))

# An empty register agreeing proves little. Compare the two parsers on a FILLED record with
# real failures in it — that is where a structural parser diverges.
FILLED = """markets:
  - market: turkey-to-syria
    status: open
    owner: Khaldoun Alhaj
    target: "12 qualified RFQs in two quarters"
    opened_at: 2026-09-16
    decision_recorded_by: Khaldoun Alhaj
    decision_recorded_at: 2026-09-16
    gate:
      demand_evidence:
        passed: true
        evidence: "9 RFQs and 14 MIRA conversations originated in Turkey between Jan and Jun 2026"
      operational_reality:
        passed: true
        evidence: "Weekly consolidation through Mersin with a partner used since 2019, nameable"
      capacity:
        passed: true
        evidence: "One writer for six weeks and a Turkish reviewer, without pausing Syria work"
      named_owner:
        passed: true
        evidence: "Khaldoun Alhaj owns the content and the enquiries, confirmed in September"
  - market: uae-to-syria
    status: open
    owner: null
    target: ""
    opened_at: null
    decision_recorded_by: null
    decision_recorded_at: null
    gate:
      demand_evidence:
        passed: true
        evidence: "There is clear demand from the UAE market"
      operational_reality:
        passed: false
        evidence: ""
      capacity:
        passed: false
        evidence: ""
      named_owner:
        passed: false
        evidence: ""
"""


def verdict(markets):
    per, reg = mg.check_register(markets)
    return sorted(i for v in per.values() for i in v) + sorted(reg)


fallback_verdict = verdict(mg._load_fallback(FILLED))
check("fallback finds the failures in a filled record", len(fallback_verdict) == 11,
      f"{len(fallback_verdict)} issues")
check("fallback catches the unnumbered demand claim",
      any("no number" in i for i in fallback_verdict))
check("fallback catches two markets open at once",
      any("More than one market is open" in i for i in fallback_verdict))

try:
    import yaml  # type: ignore
    yaml_verdict = verdict(yaml.safe_load(FILLED)["markets"])
    check("both parsers reach an identical verdict", yaml_verdict == fallback_verdict,
          f"yaml {len(yaml_verdict)} vs fallback {len(fallback_verdict)}")
except ImportError:
    print("  note PyYAML absent — the equivalence check could not run here")

# --------------------------------------------------------------------------------------
print("\n=== health check ===")

HC = os.path.join(os.path.dirname(HERE), "health_check.py")
result = subprocess.run([sys.executable, HC, "--skip-suites"], capture_output=True, text=True)
check("health check runs", result.returncode in (0, 1), result.stderr[-200:])
check("reports the knowledge base", "MIRA knowledge base" in result.stdout)
check("reports unconfirmed calculator data", "unconfirmed" in result.stdout)
check("reports the market register", "Market expansion register" in result.stdout)
check("refuses to overclaim", "whether a page is still TRUE" in result.stdout)

# Expired content is a failure, not a note.
content = tempfile.mkdtemp()
with open(os.path.join(content, "stale.md"), "w", encoding="utf-8") as fh:
    fh.write("---\ntitle: Old\nlanguage: en\nowner: Khaldoun Alhaj\n"
             "reviewed_at: 2024-01-01\nexpires_at: 2025-01-01\n---\n\n# Old\n\nText.\n")
result = subprocess.run([sys.executable, HC, "--skip-suites", "--content-root", content],
                        capture_output=True, text=True)
check("expired content exits non-zero", result.returncode == 1, result.stdout[-300:])
check("expired content named", "EXPIRED 2025-01-01" in result.stdout)

with open(os.path.join(content, "stale.md"), "w", encoding="utf-8") as fh:
    fh.write("---\ntitle: Fresh\nlanguage: en\nowner: Khaldoun Alhaj\n"
             "reviewed_at: 2026-09-01\nexpires_at: 2099-01-01\n---\n\n# Fresh\n\nText.\n")
result = subprocess.run([sys.executable, HC, "--skip-suites", "--content-root", content],
                        capture_output=True, text=True)
check("fresh content exits zero", result.returncode == 0, result.stdout[-300:])

with open(os.path.join(content, "noowner.md"), "w", encoding="utf-8") as fh:
    fh.write("---\ntitle: Orphan\nlanguage: en\nexpires_at: 2099-01-01\n---\n\n# Orphan\n\nText.\n")
result = subprocess.run([sys.executable, HC, "--skip-suites", "--content-root", content],
                        capture_output=True, text=True)
check("a page with no owner fails", result.returncode == 1 and "no owner" in result.stdout)

# --------------------------------------------------------------------------------------
print()
if failures:
    print(f"Operating checks suite: {len(failures)} FAILED — {', '.join(failures[:4])}")
    sys.exit(1)
print("Operating checks suite: all checks passed")
