#!/usr/bin/env python3
"""
Enquiry register check — ENQUIRY-INTAKE.md §6.

Between March and September 2026, ten well-specified customer enquiries reached MIDTRANS and
none was answered; four were never opened. In the same period another was answered in twenty
minutes. The capability was never the problem — whether an enquiry got picked up was chance.

This makes that visible on demand instead of six months later.

    python3 tools/ops/enquiry_log.py --window 24
    python3 tools/ops/enquiry_log.py --window 24 --file tools/ops/enquiries.csv --json out.json

`--window` is the acknowledgement window in hours, and it is **required with no default** —
the same rule as the volumetric divisor in tools/calc/freight_math.py. A response time nobody
chose, silently inherited, is worse than none, and WRITING-STANDARDS §4 forbids publishing one
that operations has not committed to. Management sets it; this tool only holds them to it.

Exit 0 when nothing genuine is past the window, 1 when something is, 2 when the register cannot
be read or is malformed.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
from dataclasses import dataclass, field

DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "enquiries.csv")

FIELDS = ("id", "received_at", "channel", "owner", "genuine",
          "acknowledged_at", "closed_at", "note")

# §4: "unsure" counts as genuine. The failure this register exists to prevent is an enquiry
# quietly reclassified as noise, so an honest mistake should fall towards answering someone.
GENUINE = {"yes", "y", "true", "1", "unsure", "?"}
NOT_GENUINE = {"no", "n", "false", "0"}

NOT_A_PERSON = {"operations", "ops", "team", "the team", "midtrans", "info", "tbd", "n/a", ""}


class RegisterError(ValueError):
    """The register cannot be trusted. Never worked around — a bad register reads as a clean one."""


@dataclass
class Enquiry:
    id: str
    received: dt.datetime
    channel: str
    owner: str
    genuine: bool
    acknowledged: dt.datetime | None
    closed: dt.datetime | None
    note: str

    @property
    def open(self) -> bool:
        return self.acknowledged is None

    def waiting_hours(self, now: dt.datetime) -> float:
        end = self.acknowledged or now
        return (end - self.received).total_seconds() / 3600.0


def _parse_time(value: str, field_name: str, row_id: str) -> dt.datetime | None:
    value = (value or "").strip()
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            return dt.datetime.strptime(value[:len(fmt) + 2].strip(), fmt)
        except ValueError:
            continue
    try:
        return dt.datetime.fromisoformat(value.replace("Z", ""))
    except ValueError:
        raise RegisterError(
            f"row {row_id!r}: {field_name} is {value!r}. Expected YYYY-MM-DD or an ISO timestamp"
        ) from None


def load(path: str) -> list:
    with open(path, encoding="utf-8") as fh:
        lines = [line for line in fh if not line.lstrip().startswith("#")]

    reader = csv.DictReader(lines)
    if reader.fieldnames is None:
        raise RegisterError("the register is empty — not even a header row")
    missing = [f for f in FIELDS if f not in reader.fieldnames]
    if missing:
        raise RegisterError("header is missing: " + ", ".join(missing))

    enquiries = []
    for index, row in enumerate(reader, start=2):
        if not (row.get("id") or "").strip():
            continue
        row_id = row["id"].strip()

        received = _parse_time(row.get("received_at", ""), "received_at", row_id)
        if received is None:
            raise RegisterError(f"row {row_id!r}: received_at is blank. When did it arrive?")

        flag = (row.get("genuine") or "").strip().lower()
        if flag not in GENUINE and flag not in NOT_GENUINE:
            raise RegisterError(
                f"row {row_id!r}: genuine is {flag!r}. Use yes, no or unsure — see §4")

        enquiries.append(Enquiry(
            id=row_id,
            received=received,
            channel=(row.get("channel") or "").strip(),
            owner=(row.get("owner") or "").strip(),
            genuine=flag in GENUINE,
            acknowledged=_parse_time(row.get("acknowledged_at", ""), "acknowledged_at", row_id),
            closed=_parse_time(row.get("closed_at", ""), "closed_at", row_id),
            note=(row.get("note") or "").strip(),
        ))

    ids = [e.id for e in enquiries]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        raise RegisterError("duplicate ids: " + ", ".join(duplicates))
    return enquiries


@dataclass
class Report:
    genuine: list = field(default_factory=list)
    overdue: list = field(default_factory=list)
    waiting: list = field(default_factory=list)
    ownerless: list = field(default_factory=list)
    acknowledged: list = field(default_factory=list)

    @property
    def reply_rate(self) -> float | None:
        if not self.genuine:
            return None
        return len(self.acknowledged) / len(self.genuine)

    @property
    def median_hours(self) -> float | None:
        times = sorted(e for e in self.acknowledged_hours)
        if not times:
            return None
        mid = len(times) // 2
        return times[mid] if len(times) % 2 else (times[mid - 1] + times[mid]) / 2

    acknowledged_hours: list = field(default_factory=list)


def analyse(enquiries: list, window_hours: float, now: dt.datetime) -> Report:
    report = Report()
    for e in enquiries:
        if not e.genuine:
            continue
        report.genuine.append(e)
        if e.owner.lower() in NOT_A_PERSON:
            report.ownerless.append(e)
        if e.acknowledged is not None:
            report.acknowledged.append(e)
            report.acknowledged_hours.append(e.waiting_hours(now))
        elif e.waiting_hours(now) > window_hours:
            report.overdue.append(e)
        else:
            report.waiting.append(e)

    report.overdue.sort(key=lambda e: e.received)     # oldest first — that is the action list
    report.waiting.sort(key=lambda e: e.received)
    return report


def _age(hours: float) -> str:
    if hours < 48:
        return f"{hours:.0f}h"
    return f"{hours / 24:.0f}d"


def print_report(report: Report, window: float, now: dt.datetime) -> None:
    print("\nENQUIRY REGISTER")
    print("=" * 74)
    print(f"  as at {now:%Y-%m-%d %H:%M} · acknowledgement window {window:g}h")
    print(f"  {len(report.genuine)} genuine enquiries · {len(report.acknowledged)} acknowledged "
          f"· {len(report.waiting)} waiting · {len(report.overdue)} overdue")

    rate = report.reply_rate
    if rate is not None:
        print(f"  reply rate {rate:.0%}", end="")
        median = report.median_hours
        print(f" · median time to acknowledge {_age(median)}" if median is not None else "")
    print()

    if report.overdue:
        print("  PAST THE WINDOW — oldest first")
        for e in report.overdue:
            owner = e.owner or "NO OWNER"
            print(f"    {_age(e.waiting_hours(now)):>5}  {e.id:<28} {owner:<18} {e.channel}")
            if e.note:
                print(f"           {e.note[:88]}")
        print()

    if report.waiting:
        print("  Waiting, inside the window")
        for e in report.waiting:
            print(f"    {_age(e.waiting_hours(now)):>5}  {e.id:<28} {e.owner or 'NO OWNER'}")
        print()

    if report.ownerless:
        print(f"  NO NAMED OWNER — {len(report.ownerless)} enquiry(ies)")
        print("    ENQUIRY-INTAKE.md §2: a team is not accountable, a person is.")
        for e in report.ownerless:
            print(f"    {e.id:<28} {e.channel}")
        print()

    by_channel: dict = {}
    for e in report.genuine:
        entry = by_channel.setdefault(e.channel or "(unset)", [0, 0])
        entry[0] += 1
        if e.acknowledged is not None:
            entry[1] += 1
    if by_channel:
        print("  By channel")
        for channel, (total, done) in sorted(by_channel.items(), key=lambda kv: -kv[1][0]):
            share = f"{done / total:.0%}" if total else "—"
            print(f"    {channel:<32} {done}/{total} acknowledged  {share}")
        print()

    print("-" * 74)
    if report.overdue:
        print("  An enquiry past the window is not a backlog item. Two of the ten found in")
        print("  September had been sent to several forwarders at once — there, a reply")
        print("  measured in days is a loss by default, and nobody tells you that you lost.")
    elif not report.genuine:
        print("  No genuine enquiries logged. If that is not true, the register is not in use —")
        print("  which is the state that produced D3 §8b in the first place.")
    else:
        print("  Nothing past the window.")

    print("\n  This counts what is logged. An enquiry nobody recorded is invisible here, and")
    print("  that is exactly how ten of them went unanswered without anyone intending it.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--window", type=float, required=True,
                        help="Acknowledgement window in hours, agreed by management (§5). "
                             "Required — there is deliberately no default")
    parser.add_argument("--file", default=DEFAULT_FILE)
    parser.add_argument("--json", dest="json_out")
    parser.add_argument("--now", help="Override the current time, as YYYY-MM-DD or ISO")
    args = parser.parse_args()

    if args.window <= 0:
        print("--window must be greater than zero", file=sys.stderr)
        return 2

    now = dt.datetime.now()
    if args.now:
        try:
            now = _parse_time(args.now, "--now", "argument") or now
        except RegisterError as exc:
            print(str(exc), file=sys.stderr)
            return 2

    try:
        enquiries = load(args.file)
    except OSError as exc:
        print(f"Could not read {args.file}: {exc}", file=sys.stderr)
        return 2
    except RegisterError as exc:
        print(f"Register is not usable — {exc}", file=sys.stderr)
        print("A register that cannot be parsed reads exactly like a clean one. Fix it first.",
              file=sys.stderr)
        return 2

    report = analyse(enquiries, args.window, now)
    print_report(report, args.window, now)

    if args.json_out:
        payload = {
            "as_at": now.isoformat(timespec="minutes"),
            "window_hours": args.window,
            "genuine": len(report.genuine),
            "acknowledged": len(report.acknowledged),
            "reply_rate": report.reply_rate,
            "median_hours_to_acknowledge": report.median_hours,
            "overdue": [
                {"id": e.id, "owner": e.owner, "channel": e.channel,
                 "hours": round(e.waiting_hours(now), 1), "note": e.note}
                for e in report.overdue
            ],
        }
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
        print(f"\n  written to {args.json_out}")

    return 1 if report.overdue else 0


if __name__ == "__main__":
    sys.exit(main())
