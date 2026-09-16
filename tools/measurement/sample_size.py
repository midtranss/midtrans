#!/usr/bin/env python3
"""
Sample-size and minimum-detectable-effect tables for the Phase 01 gate.

Generates the three tables in docs/phases/PHASE-01-MEASUREMENT-FRAMEWORK.md §6-§7.
Standard library only. Re-run with the real baseline before the gate is used —
the numbers printed with the defaults are illustrative, the method is not.

    python3 tools/measurement/sample_size.py
    python3 tools/measurement/sample_size.py --baseline 34
"""

import argparse
from math import sqrt

Z_ALPHA = 1.959964   # two-sided, alpha = 0.05
Z_BETA = 0.841621    # 80% power


def count_mde(lam0):
    """Minimum detectable rate for a Poisson count, baseline vs test period of equal length.

    sqrt(X) ~ N(sqrt(lambda), 1/4), so sqrt(X1) - sqrt(X0) ~ N(sqrt(l1) - sqrt(l0), 1/2).
    Setting power to 80%: sqrt(l1) = sqrt(l0) + (Z_ALPHA + Z_BETA) * sqrt(0.5).
    """
    return (sqrt(lam0) + (Z_ALPHA + Z_BETA) * sqrt(0.5)) ** 2


def proportion_n(p0, p1):
    """Observations needed per period to detect p0 -> p1 in a two-proportion comparison."""
    pbar = (p0 + p1) / 2
    numerator = (
        Z_ALPHA * sqrt(2 * pbar * (1 - pbar))
        + Z_BETA * sqrt(p0 * (1 - p0) + p1 * (1 - p1))
    ) ** 2
    return numerator / (p1 - p0) ** 2


def table_counts(baselines):
    print("§6 — count metric: actionable RFQ per 4 weeks")
    print(f"{'baseline':>10} | {'must reach':>10} | {'increase':>9} | {'relative':>9}")
    print("-" * 46)
    for lam0 in baselines:
        lam1 = count_mde(lam0)
        print(f"{lam0:>10} | {lam1:>10.0f} | {lam1 - lam0:>9.0f} | {(lam1 / lam0 - 1) * 100:>8.0f}%")
    print()


def table_completion():
    print("§6 — completion rate: wizard starts needed per period")
    lifts = (0.05, 0.10, 0.15, 0.20)
    print(f"{'baseline':>10} |" + "".join(f"{f'+{int(d*100)} pts':>10}" for d in lifts))
    print("-" * (11 + 10 * len(lifts)))
    for p0 in (0.20, 0.30, 0.40, 0.50):
        row = f"{p0 * 100:>9.0f}% |"
        for d in lifts:
            p1 = p0 + d
            row += f"{proportion_n(p0, p1):>10.0f}" if p1 < 1 else f"{'-':>10}"
        print(row)
    print()


def table_followup():
    print("§7 — follow-up rate: submissions needed per period")
    targets = (0.50, 0.40, 0.30, 0.20, 0.10)
    print(f"{'from':>10} |" + "".join(f"{f'to {int(t*100)}%':>9}" for t in targets))
    print("-" * (11 + 9 * len(targets)))
    for p0 in (0.90, 0.80, 0.70, 0.60):
        row = f"{p0 * 100:>9.0f}% |"
        for p1 in targets:
            row += f"{proportion_n(p0, p1):>9.0f}" if p1 < p0 else f"{'-':>9}"
        print(row)
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        type=float,
        help="Real actionable-RFQ baseline per 4 weeks. Adds the row that actually applies.",
    )
    args = parser.parse_args()

    baselines = [5, 10, 20, 30, 50, 80, 120, 200]
    if args.baseline:
        baselines = sorted(set(baselines + [args.baseline]))

    table_counts(baselines)
    table_completion()
    table_followup()

    if args.baseline:
        lam1 = count_mde(args.baseline)
        print(
            f"At a baseline of {args.baseline:.0f} per 4 weeks, the count metric needs "
            f"{lam1:.0f} ({(lam1 / args.baseline - 1) * 100:.0f}% higher) to be detectable.\n"
            "If that is implausible, the gate decision belongs to the follow-up rate — see §7."
        )


if __name__ == "__main__":
    main()
