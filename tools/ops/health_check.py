#!/usr/bin/env python3
"""
Programme health check — PHASE-07's recurring reviews, in one command.

Phase 07 does not end; it is operated. Its cadence table lists a weekly metric review, a monthly
MIRA audit, and three quarterly reviews. Each of those is a person remembering to look. This is
the part a machine can hold: the state of the programme's own artefacts, on the day it is run.

    python3 tools/ops/health_check.py
    python3 tools/ops/health_check.py --content-root drafts --days 60

It reports rather than judges, with one exception: anything already expired, or published with
no owner, exits non-zero. Those are not opinions.

What it cannot see is the half that matters most — whether the content is true, whether a page
still reflects how the port actually works, whether a market's target was met. Section 3 of
../../docs/phases/PHASE-07-OPERATING-CHECKS.md says so at more length.
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

sys.path.insert(0, os.path.join(ROOT, "tools", "content"))
sys.path.insert(0, os.path.join(ROOT, "tools", "calc"))
sys.path.insert(0, HERE)

OK, WARN, FAIL = "ok", "warn", "FAIL"


class Section:
    def __init__(self, title: str):
        self.title = title
        self.lines: list = []
        self.worst = OK

    def add(self, level: str, text: str) -> None:
        self.lines.append((level, text))
        if level == FAIL or (level == WARN and self.worst == OK):
            self.worst = level

    def render(self) -> None:
        marker = {OK: "  ", WARN: "! ", FAIL: "X "}[self.worst]
        print(f"\n{marker}{self.title}")
        for level, text in self.lines:
            prefix = {OK: "    ", WARN: "  ! ", FAIL: "  X "}[level]
            print(f"{prefix}{text}")


# --------------------------------------------------------------------------------------

def content_freshness(root: str, horizon_days: int) -> Section:
    """Quarterly content freshness review — PHASE-07 ongoing operations."""
    section = Section(f"Content freshness  ({root or 'no content root given'})")
    if not root or not os.path.isdir(root):
        section.add(OK, "No content directory yet. Pass --content-root once pages exist.")
        return section

    try:
        from check_page import split_front_matter
    except ImportError:
        section.add(FAIL, "tools/content/check_page.py not importable — cannot read front matter")
        return section

    today = dt.date.today()
    horizon = today + dt.timedelta(days=horizon_days)
    pages = sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True))
    if not pages:
        section.add(OK, f"No pages under {root}.")
        return section

    expired, soon, ownerless, undated = [], [], [], []
    for path in pages:
        with open(path, encoding="utf-8") as fh:
            fields, _, _ = split_front_matter(fh.read())
        owner = (fields.get("owner") or "").strip()
        if not owner:
            ownerless.append(path)
        raw = (fields.get("expires_at") or "").strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
            undated.append(path)
            continue
        expiry = dt.date.fromisoformat(raw)
        if expiry < today:
            expired.append((path, expiry))
        elif expiry <= horizon:
            soon.append((path, expiry))

    section.add(OK, f"{len(pages)} page(s) scanned")
    for path, expiry in sorted(expired, key=lambda p: p[1]):
        section.add(FAIL, f"EXPIRED {expiry} — {path}")
    for path, expiry in sorted(soon, key=lambda p: p[1]):
        section.add(WARN, f"expires {expiry} — {path}")
    for path in undated:
        section.add(FAIL, f"no valid expires_at — {path}")
    for path in ownerless:
        section.add(FAIL, f"no owner — {path}")
    if not (expired or soon or undated or ownerless):
        section.add(OK, f"Nothing expired or expiring within {horizon_days} days.")
    return section


def enquiry_register(window_hours, path=None) -> Section:
    """ENQUIRY-INTAKE.md §6 — is anything genuine sitting past the acknowledgement window?"""
    section = Section("Enquiry register")
    try:
        import enquiry_log
    except Exception as exc:  # noqa: BLE001
        section.add(FAIL, f"tools/ops/enquiry_log.py could not be imported: {exc}")
        return section

    if not window_hours:
        section.add(WARN,
                    "No acknowledgement window given, so nothing can be judged overdue. "
                    "Management sets it (ENQUIRY-INTAKE.md §5), then pass --enquiry-window N.")
        # The register is still worth reporting on, even without a window.
        window_hours = None

    try:
        enquiries = enquiry_log.load(path or enquiry_log.DEFAULT_FILE)
    except enquiry_log.RegisterError as exc:
        section.add(FAIL, f"register is not usable — {exc}")
        section.add(FAIL, "A register that cannot be parsed reads exactly like a clean one.")
        return section
    except OSError as exc:
        section.add(FAIL, f"register could not be read: {exc}")
        return section

    report = enquiry_log.analyse(enquiries, window_hours or float("inf"), dt.datetime.now())
    section.add(OK, f"{len(report.genuine)} genuine · {len(report.acknowledged)} acknowledged")
    if report.reply_rate is not None:
        section.add(OK if report.reply_rate > 0 else WARN,
                    f"reply rate {report.reply_rate:.0%}")
    for e in report.overdue:
        owner = e.owner or "NO OWNER"
        section.add(FAIL,
                    f"{_age(e.waiting_hours(dt.datetime.now()))} overdue — {e.id} ({owner})")
    if report.ownerless:
        section.add(FAIL,
                    f"{len(report.ownerless)} enquiry(ies) with no named owner — §2")
    if not report.genuine:
        section.add(WARN, "Nothing logged. If that is not true, the register is not in use.")
    return section


def _age(hours: float) -> str:
    return f"{hours:.0f}h" if hours < 48 else f"{hours / 24:.0f}d"


def knowledge_base() -> Section:
    """MIRA knowledge base: how much of it MIDTRANS has actually confirmed."""
    section = Section("MIRA knowledge base")
    path = os.path.join(ROOT, "mira", "knowledge", "kb-seed.yaml")
    if not os.path.exists(path):
        section.add(OK, "No knowledge base file yet.")
        return section

    sys.path.insert(0, os.path.join(ROOT, "mira", "knowledge"))
    try:
        import validate_kb
        entries = validate_kb._load()
        servable = validate_kb.servable_entries()
        errors, _ = validate_kb.validate(entries)
    except Exception as exc:  # noqa: BLE001
        section.add(FAIL, f"validate_kb.py could not run: {exc}")
        return section

    drafts = len(entries) - len(servable)
    section.add(OK, f"{len(entries)} entries, {len(servable)} servable, {drafts} draft")
    for error in errors:
        section.add(FAIL, f"validation: {error}")
    if drafts:
        section.add(WARN,
                    f"{drafts} entry(ies) still await a named owner's answer. Until then MIRA "
                    "has nothing to say on them — which is correct, and also a content gap.")
    return section


def reference_data() -> Section:
    """Phase 03 equipment data — unconfirmed rows block the calculators from going live."""
    section = Section("Calculator reference data")
    try:
        import freight_math
        pending = freight_math.unconfirmed_rows()
    except Exception as exc:  # noqa: BLE001
        section.add(FAIL, f"tools/calc/freight_math.py could not run: {exc}")
        return section

    if not pending:
        section.add(OK, "Every container capacity and divisor confirmed by a named person.")
    else:
        section.add(WARN, f"{len(pending)} row(s) unconfirmed — the calculators must not go live:")
        for kind, name in pending:
            section.add(WARN, f"  {kind}: {name}")
    return section


def market_register() -> Section:
    """PHASE-07 Part B — is the expansion register consistent?"""
    section = Section("Market expansion register")
    try:
        import market_gate
        markets = market_gate.load(market_gate.DEFAULT_FILE)
        per_market, register = market_gate.check_register(markets)
    except Exception as exc:  # noqa: BLE001
        section.add(FAIL, f"market_gate.py could not run: {exc}")
        return section

    counts: dict = {}
    for market in markets:
        counts[market.get("status") or "?"] = counts.get(market.get("status") or "?", 0) + 1
    section.add(OK, ", ".join(f"{n} {s}" for s, n in sorted(counts.items())) or "empty register")

    for name, issues in per_market.items():
        for issue in issues:
            section.add(FAIL, f"{name}: {issue}")
    for issue in register:
        section.add(FAIL, issue)
    if not any(per_market.values()) and not register:
        section.add(OK, "Register consistent.")
    return section


def guardrail_suites() -> Section:
    """The safety suites must pass. A suite nobody runs is documentation."""
    section = Section("Guardrail and tool suites")
    import subprocess

    suites = [
        ("MIRA guardrails", "mira/tests/test_guardrails.py"),
        ("MIRA client wiring", "mira/tests/test_client.py"),
        ("MIRA escalation", "mira/tests/test_escalation.py"),
        ("MIRA log auditor", "mira/tests/test_audit_logs.py"),
        ("Freight calculations", "tools/calc/tests/test_freight_math.py"),
        ("Content gate", "tools/content/tests/test_check_page.py"),
        ("Cluster duplication", "tools/content/tests/test_check_cluster.py"),
        ("Operating checks", "tools/ops/tests/test_ops.py"),
        ("Enquiry register", "tools/ops/tests/test_enquiry_log.py"),
    ]
    for label, path in suites:
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            section.add(FAIL, f"{label}: missing ({path})")
            continue
        result = subprocess.run([sys.executable, full], capture_output=True, text=True, cwd=ROOT)
        if result.returncode == 0:
            section.add(OK, f"{label}: pass")
        else:
            section.add(FAIL, f"{label}: FAIL — {result.stdout.strip().splitlines()[-1:]}")
    return section


# --------------------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--content-root", default="",
                        help="Directory of published or draft pages with front matter")
    parser.add_argument("--days", type=int, default=90,
                        help="Warn on content expiring within this many days (default 90)")
    parser.add_argument("--enquiry-window", type=float, default=None,
                        help="Acknowledgement window in hours (ENQUIRY-INTAKE.md §5). "
                             "No default — management sets it")
    parser.add_argument("--enquiry-file", default=None,
                        help="Enquiry register to read (default: tools/ops/enquiries.csv)")
    parser.add_argument("--skip-suites", action="store_true",
                        help="Skip running the test suites (faster, less useful)")
    args = parser.parse_args()

    print("=" * 72)
    print(f"  MIDTRANS PROGRAMME HEALTH CHECK   {dt.date.today()}")
    print("=" * 72)

    sections = [
        enquiry_register(args.enquiry_window, args.enquiry_file),
        content_freshness(args.content_root, args.days),
        knowledge_base(),
        reference_data(),
        market_register(),
    ]
    if not args.skip_suites:
        sections.append(guardrail_suites())

    for section in sections:
        section.render()

    failures = [s for s in sections if s.worst == FAIL]
    warnings = [s for s in sections if s.worst == WARN]

    print("\n" + "=" * 72)
    if failures:
        print(f"  {len(failures)} section(s) need action: "
              + ", ".join(s.title.split("  ")[0] for s in failures))
    elif warnings:
        print(f"  Nothing broken. {len(warnings)} section(s) carry open items.")
    else:
        print("  All clear.")

    print("\n  What this cannot see: whether a page is still TRUE. An unexpired page describing")
    print("  a procedure that changed last month passes every check here. The quarterly review")
    print("  is a person reading the content — this only tells you which pages to read first.")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
