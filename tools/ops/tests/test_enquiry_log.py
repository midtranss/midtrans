#!/usr/bin/env python3
"""
Tests for the enquiry register check — ENQUIRY-INTAKE.md.

The register exists because ten real enquiries went unanswered without anyone intending it. So
the cases that matter most are the ones where a check could look clean while the register is
broken: an unparseable file, a duplicate id, a missing arrival time. Each of those must fail
loudly, because a register that cannot be trusted reads exactly like a register with nothing in
it.

Run:  python3 tools/ops/tests/test_enquiry_log.py
"""

import datetime as dt
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import enquiry_log as el  # noqa: E402

failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        failures.append(name)


HEAD = "id,received_at,channel,owner,genuine,acknowledged_at,closed_at,note\n"
NOW = dt.datetime(2026, 9, 16, 12, 0)


def write(body, head=HEAD):
    fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
    fh.write(head + body)
    fh.close()
    return fh.name


def rows(*lines):
    return "".join(l if l.endswith("\n") else l + "\n" for l in lines)


# --------------------------------------------------------------------------------------
print("\n=== the basic accounting ===")

path = write(rows(
    "a,2026-09-16 09:00,info@,Khaldoun,yes,2026-09-16 09:20,,answered fast",
    "b,2026-09-14,info@,Khaldoun,yes,,,two days and nothing",
    "c,2026-09-16 11:00,info@,Khaldoun,yes,,,just arrived",
    "d,2026-09-10,info@,Khaldoun,no,,,carrier marketing",
))
r = el.analyse(el.load(path), window_hours=24, now=NOW)
check("non-genuine excluded", len(r.genuine) == 3, len(r.genuine))
check("acknowledged counted", len(r.acknowledged) == 1)
check("overdue found", [e.id for e in r.overdue] == ["b"], [e.id for e in r.overdue])
check("inside the window is not overdue", [e.id for e in r.waiting] == ["c"])
check("reply rate", abs(r.reply_rate - 1 / 3) < 1e-9, r.reply_rate)
check("median measured on acknowledged only", abs(r.median_hours - (20 / 60)) < 0.01,
      r.median_hours)

# --------------------------------------------------------------------------------------
print("\n=== §4: unsure counts as genuine ===")

path = write(rows("u,2026-09-10,info@,Khaldoun,unsure,,,ambiguous"))
r = el.analyse(el.load(path), 24, NOW)
check("unsure is genuine", len(r.genuine) == 1 and len(r.overdue) == 1)

path = write(rows("n,2026-09-10,info@,Khaldoun,no,,,job application"))
r = el.analyse(el.load(path), 24, NOW)
check("no is excluded entirely", not r.genuine and not r.overdue)

# --------------------------------------------------------------------------------------
print("\n=== §2: an owner is a person ===")

for label, owner in [("blank", ""), ("a team", "Operations"), ("a department", "ops"),
                     ("the company", "MIDTRANS"), ("a placeholder", "TBD")]:
    path = write(rows(f"x,2026-09-16 11:00,info@,{owner},yes,,,note"))
    r = el.analyse(el.load(path), 24, NOW)
    check(f"{label} is not an owner", len(r.ownerless) == 1, owner)

path = write(rows("x,2026-09-16 11:00,info@,Khaldoun Alhaj,yes,,,note"))
check("a name is an owner", not el.analyse(el.load(path), 24, NOW).ownerless)

# --------------------------------------------------------------------------------------
print("\n=== a broken register must not read as a clean one ===")

for label, body, head in [
    ("a missing column", rows("a,2026-09-16,info@,K,yes,,"), "id,received_at,channel,owner\n"),
    ("a blank arrival time", rows("a,,info@,K,yes,,,note"), HEAD),
    ("an unparseable date", rows("a,September 2026,info@,K,yes,,,note"), HEAD),
    ("an unknown genuine value", rows("a,2026-09-16,info@,K,maybe,,,note"), HEAD),
    ("a duplicate id", rows("a,2026-09-16,info@,K,yes,,,one",
                            "a,2026-09-15,info@,K,yes,,,two"), HEAD),
]:
    try:
        el.load(write(body, head))
        check(f"{label} raises", False, "no RegisterError")
    except el.RegisterError:
        check(f"{label} raises", True)

try:
    el.load(write("", ""))
    check("an empty file raises", False)
except el.RegisterError:
    check("an empty file raises", True)

# Comment lines and blank ids are skipped, not treated as errors.
path = write(rows("# a note about the register", "", "a,2026-09-16 11:00,info@,K,yes,,,note"))
check("comments and blank rows skipped", len(el.load(path)) == 1, len(el.load(path)))

# Commas inside a note must survive.
path = write('a,2026-09-16 11:00,info@,K,yes,,,"HS 6911, 1.0-1.5 CBM, 150-220 kg"\n')
check("a quoted note keeps its commas", el.load(path)[0].note.count(",") == 2,
      el.load(path)[0].note)

# --------------------------------------------------------------------------------------
print("\n=== §5: nobody invents a response time ===")

CLI = os.path.join(os.path.dirname(HERE), "enquiry_log.py")


def run(*args):
    return subprocess.run([sys.executable, CLI, *args], capture_output=True, text=True)

res = run("--file", write(rows("a,2026-09-16 11:00,info@,K,yes,,,note")))
check("--window is required", res.returncode != 0 and "window" in res.stderr.lower(),
      res.stderr[:120])

res = run("--window", "0", "--file", write(rows("a,2026-09-16,info@,K,yes,,,n")))
check("a zero window is refused", res.returncode == 2)

# --------------------------------------------------------------------------------------
print("\n=== exit codes ===")

overdue = write(rows("a,2026-09-10,info@,Khaldoun,yes,,,waited six days"))
res = run("--window", "24", "--now", "2026-09-16", "--file", overdue)
check("exit 1 when something is overdue", res.returncode == 1, res.stdout[-200:])
check("the overdue enquiry is named", "a " in res.stdout and "PAST THE WINDOW" in res.stdout)

clean = write(rows("a,2026-09-16 09:00,info@,Khaldoun,yes,2026-09-16 09:20,,answered"))
res = run("--window", "24", "--now", "2026-09-16 12:00", "--file", clean)
check("exit 0 when nothing is overdue", res.returncode == 0, res.stdout[-200:])
check("output refuses to overclaim", "invisible here" in res.stdout)

res = run("--window", "24", "--file", "/tmp/definitely-not-here-9482.csv")
check("exit 2 on an unreadable file", res.returncode == 2)

res = run("--window", "24", "--file", write(rows("a,not-a-date,info@,K,yes,,,n")))
check("exit 2 on a broken register", res.returncode == 2)
check("and it says why", "not usable" in res.stderr, res.stderr[:120])

# --------------------------------------------------------------------------------------
print("\n=== the register ships loaded with the real backlog ===")

real = el.load(el.DEFAULT_FILE)
check("ten enquiries pre-loaded", len(real) == 10, len(real))
check("all genuine", all(e.genuine for e in real))
check("none acknowledged yet", all(e.open for e in real))
check("none has an owner yet", all(e.owner == "" for e in real))
check("the oldest is the July porcelain enquiry",
      min(real, key=lambda e: e.received).id == "2026-07-27-porcelain")
check("notes survived the CSV",
      any("HS 6911" in e.note for e in real), [e.note[:40] for e in real][:1])

# --------------------------------------------------------------------------------------
print()
if failures:
    print(f"Enquiry register suite: {len(failures)} FAILED — {', '.join(failures[:4])}")
    sys.exit(1)
print("Enquiry register suite: all checks passed")
