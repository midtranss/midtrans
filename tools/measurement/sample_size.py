#!/usr/bin/env python3
"""
Sample-size and minimum-detectable-effect tables for the Phase 01 gate.

Generates the tables in docs/phases/PHASE-01-MEASUREMENT-FRAMEWORK.md §6-§7 and the
zero-violation bounds in docs/phases/PHASE-02-D0-AUDIT.md §5.
Standard library only. Re-run with the real baseline before the gate is used —
the numbers printed with the defaults are illustrative, the method is not.

    python3 tools/measurement/sample_size.py
    python3 tools/measurement/sample_size.py --baseline 34
    python3 tools/measurement/sample_size.py --zero-events 140
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


def zero_event_bound(n):
    """Upper 95% bound on an event rate after n observations with zero events.

    Exact: the largest p for which observing zero in n has probability >= 0.05,
    i.e. (1-p)^n = 0.05. (The familiar 3/n is this, approximated.)
    """
    return 1 - 0.05 ** (1 / n)


def table_zero_events(extra=None):
    print("§5 (Phase 02) — what zero observed violations supports")
    print(f"{'conversations':>14} | {'upper 95% bound':>16} | {'i.e. as often as':>20}")
    print("-" * 56)
    sizes = [30, 50, 100, 200, 300, 500, 1000, 2000]
    if extra:
        sizes = sorted(set(sizes + [int(extra)]))
    for n in sizes:
        p = zero_event_bound(n)
        print(f"{n:>14} | {p * 100:>15.2f}% | 1 in {1 / p:>14,.0f}")
    print()
    print("  Zero observed is never zero. It bounds the rate; it does not establish it.")
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
    parser.add_argument(
        "--zero-events",
        type=int,
        help="Conversations audited with zero violations. Adds the row that actually applies.",
    )
    args = parser.parse_args()

    baselines = [5, 10, 20, 30, 50, 80, 120, 200]
    if args.baseline:
        baselines = sorted(set(baselines + [args.baseline]))

    table_counts(baselines)
    table_completion()
    table_followup()
    table_zero_events(args.zero_events)

    if args.zero_events:
        p = zero_event_bound(args.zero_events)
        print(
            f"{args.zero_events} conversations with zero violations bounds the rate at "
            f"{p * 100:.2f}% — about 1 in {1 / p:,.0f} conversations.\n"
            "State it that way in the gate decision. Do not write \"MIRA does not quote\".\n"
        )

    if args.baseline:
        lam1 = count_mde(args.baseline)
        print(
            f"At a baseline of {args.baseline:.0f} per 4 weeks, the count metric needs "
            f"{lam1:.0f} ({(lam1 / args.baseline - 1) * 100:.0f}% higher) to be detectable.\n"
            "If that is implausible, the gate decision belongs to the follow-up rate — see §7."
        )


if __name__ == "__main__":
    main()
