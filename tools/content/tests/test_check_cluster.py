#!/usr/bin/env python3
"""
Tests for the cluster duplication check.

The measurement only earns its thresholds if the two populations separate cleanly, so the suite
checks both ends: templated pages must score near 1.0, and genuinely distinct pages written by
the same author in the same voice must score near 0. The repository's own phase documents serve
as the real-world negative control — 14 documents, 91 pairs, all under 2%.

Run:  python3 tools/content/tests/test_check_cluster.py
"""

import glob
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.dirname(HERE))

import check_cluster as cc  # noqa: E402

failures = []


def check(name, condition, detail=""):
    if condition:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name}  {detail}")
        failures.append(name)


FRONT = """---
title: {title}
language: en
owner: Khaldoun Alhaj
reviewed_at: 2026-09-16
expires_at: 2027-03-16
uniqueness: {uniq}
uniqueness_reviewed_by: Khaldoun Alhaj
---
"""

TEMPLATE_BODY = """
# {service} services from MIDTRANS

MIDTRANS provides {service} for international companies operating in the Syrian market. Our team
works with you to understand your requirements and deliver a service matched to your objectives.

## How the engagement works

We begin with a scoping conversation to understand your objectives. We then prepare a proposal
setting out the scope, the reporting cadence, and what you are responsible for.

## What you are responsible for

You provide the commercial objectives, the product information, and a point of contact who can
make decisions. We handle the in-market execution and the reporting.

## Why MIDTRANS

We have operated in the Syrian market since 1998, with offices in Damascus and Dubai. That
presence is what makes {service} workable rather than theoretical.
"""

DISTINCT_A = """
# Tender monitoring in Syria

Syrian public tenders are published across four channels that do not mirror each other, and the
shortest gives eleven days from publication to submission. Missing a tender is almost never a
decision — it is a channel nobody was watching.

## Where tenders appear

Ministry bulletins carry the majority, but municipal tenders frequently appear only in local
print, and some are posted physically at the issuing authority.

## Bid documentation

Submissions are routinely rejected on documentation before the commercial offer is read. The
authority does not usually explain which document failed.
"""

DISTINCT_B = """
# Distributor search in Syria

A distributor who already carries a competing line will take your agency and shelve it. That is
the single outcome worth designing the search to avoid, and it is why we start from the
distributor's existing portfolio rather than from their stated coverage.

## What we check first

Warehouse and cold-chain capacity where the product needs it, and whether the sales team is
actually theirs or subcontracted. A distributor with a hired sales force behaves differently
under a slow quarter.

## What you decide

Territory, exclusivity, and the review point at which the agreement ends if volumes do not
appear. We will not recommend an open-ended exclusive.
"""


def write(body, title, uniq="Twelve words at minimum recording what only MIDTRANS could have written here."):
    fh = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8",
                                     dir=tempfile.mkdtemp())
    fh.write(FRONT.format(title=title, uniq=uniq) + body)
    fh.close()
    return fh.name


# --------------------------------------------------------------------------------------
print("\n=== templated pages are caught ===")

paths = [
    write(TEMPLATE_BODY.format(service="business representation"), "Business representation"),
    write(TEMPLATE_BODY.format(service="commercial representation"), "Commercial representation"),
    write(TEMPLATE_BODY.format(service="local representation"), "Local representation"),
]
pairs = cc.analyse(paths, cc.BLOCK_AT, cc.WARN_AT)
check("all three pairs flagged", len(pairs) == 3, f"got {len(pairs)}")
check("flagged as blockers", all(p.level == "BLOCKER" for p in pairs),
      str([p.level for p in pairs]))
check("similarity near total", all(p.similarity > 0.9 for p in pairs),
      str([round(p.similarity, 3) for p in pairs]))
check("shared text is reported", all(p.shared for p in pairs))
check("masked subject shown as a blank", any("___" in s for p in pairs for s in p.shared),
      str(pairs[0].shared))

# Shared examples must be the same on every run. They were sliced from a set, so they were not:
# the suite failed on roughly half of all hash seeds before this was fixed.
first = [tuple(p.shared) for p in cc.analyse(paths, cc.BLOCK_AT, cc.WARN_AT)]
second = [tuple(p.shared) for p in cc.analyse(paths, cc.BLOCK_AT, cc.WARN_AT)]
check("examples are deterministic within a run", first == second)
check("masked examples come first",
      all("___" in p.shared[0] for p in pairs if p.shared), str([p.shared[0] for p in pairs]))

# --------------------------------------------------------------------------------------
print("\n=== genuinely distinct pages are not ===")

distinct = [
    write(DISTINCT_A, "Tender monitoring in Syria"),
    write(DISTINCT_B, "Distributor search in Syria"),
]
similarity, _ = cc.compare(cc.load(distinct[0]), cc.load(distinct[1]))
check("two real pages score near zero", similarity < 0.05, f"{similarity:.3f}")
check("not flagged at default thresholds",
      not cc.analyse(distinct, cc.BLOCK_AT, cc.WARN_AT))

# One templated page among distinct ones is found, and only against its own kind.
mixed = distinct + [paths[0], paths[1]]
pairs = cc.analyse(mixed, cc.BLOCK_AT, cc.WARN_AT)
check("only the templated pair flagged in a mixed set", len(pairs) == 1, f"got {len(pairs)}")
check("the right pair", {pairs[0].a, pairs[0].b} == {paths[0], paths[1]} if pairs else False)

# --------------------------------------------------------------------------------------
print("\n=== masking is what makes the test work ===")

a, b = cc.load(paths[0]), cc.load(paths[1])
masked, _ = cc.compare(a, b)
unmasked_a = cc.shingles(a.words, set())
unmasked_b = cc.shingles(b.words, set())
unmasked = len(unmasked_a & unmasked_b) / len(unmasked_a | unmasked_b)
check("masking raises the score for templated pages", masked > unmasked,
      f"masked {masked:.2f} vs unmasked {unmasked:.2f}")
check("unmasked alone would under-report", unmasked < 0.9, f"{unmasked:.2f}")

# --------------------------------------------------------------------------------------
print("\n=== real-world negative control ===")

real = sorted(glob.glob(os.path.join(ROOT, "docs", "phases", "PHASE-0*.md")))
check("control corpus found", len(real) >= 10, f"{len(real)} documents")
if len(real) >= 10:
    worst = 0.0
    pages = [cc.load(p) for p in real]
    for i, a in enumerate(pages):
        for b in pages[i + 1:]:
            worst = max(worst, cc.compare(a, b)[0])
    check(f"no real pair exceeds the warn threshold (worst {worst:.3f})", worst < cc.WARN_AT)
    check("and the margin is wide, not marginal", worst < 0.10, f"worst {worst:.3f}")

# --------------------------------------------------------------------------------------
print("\n=== exit codes ===")

import subprocess  # noqa: E402

CLI = os.path.join(os.path.dirname(HERE), "check_cluster.py")


def run(*args):
    return subprocess.run([sys.executable, CLI, *args], capture_output=True, text=True)

res = run(*distinct)
check("exit 0 when clean", res.returncode == 0, res.stdout[-200:])
check("output refuses to overclaim", "evidence, not a verdict" in res.stdout)

res = run(*paths)
check("exit 1 on a blocking pair", res.returncode == 1)

res = run(distinct[0])
check("exit 2 with a single page", res.returncode == 2, res.stderr[:120])

# --------------------------------------------------------------------------------------
print()
if failures:
    print(f"Cluster duplication suite: {len(failures)} FAILED — {', '.join(failures)}")
    sys.exit(1)
print("Cluster duplication suite: all checks passed")
