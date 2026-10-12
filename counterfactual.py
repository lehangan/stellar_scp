"""Operational counterfactual for the three single operator removals in Table 1 of the report.

For each case, on the cached snapshot before the change and the one inside it, this prints:
  nominal      the organization level minimal blocking set of the top tier (the liveness margin);
  removed down the number of further organization failures that leave no quorum once the
               organization the operator removed is already down (its liveness tolerance in the
               degraded state is that number minus one);
  other down   the same number when one other organization is down instead (minimum over them).

Reading the output for Blockdaemon, May 2020: with SatoshiPay down, the previous configuration
(5 of 7) and the new one (5 of 6) tolerate the same number of further failures, so the change
gained the operator nothing while SatoshiPay was down; with any other organization down, the new
configuration leaves the top tier one failure from a halt where the previous one left two.

Uses the cached snapshots in sdf_feasibility/verify/raw (downloaded by verify_case.py) and the
quorum set machinery of analysis.py. Run from the repository root. Standard library only.
"""
import importlib.util
import itertools
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("analysis", HERE / "analysis.py")
an = importlib.util.module_from_spec(spec)
spec.loader.exec_module(an)

# (label, operator, removed organization (substring of the Radar name), snapshot before, snapshot inside)
CASES = [
    ("Blockdaemon, May 2020", "Blockdaemon", "SatoshiPay", "2020-05-21T12:00", "2020-05-23T12:00"),
    ("SDF, April 2021", "Stellar Development Foundation", "LOBSTR", "2021-04-05T12:00", "2021-04-07T12:00"),
    ("Franklin Templeton, October 2024", "Franklin Templeton", "LOBSTR", "2024-10-03T10:00", "2024-10-05T12:00"),
]


def remaining_margin(net, tier, qs, og, failed):
    """Smallest number of further organization failures (beyond `failed`) that leave no quorum."""
    full = (1 << len(tier)) - 1
    down = 0
    for o in failed:
        down |= og[o]
    alive = full & ~down
    groups = [og[n] for n in sorted(og) if n not in failed]
    for k in range(0, len(groups) + 1):
        for combo in itertools.combinations(range(len(groups)), k):
            B = 0
            for g in combo:
                B |= groups[g]
            if an.greatest_quorum(alive & ~B, qs) == 0:
                return k
    return None


def analyse(t, operator, removed):
    net = an.snapshot(t)
    if net is None:
        raise SystemExit(f"snapshot {t} is not in the cache; run verify_case.py first")
    tier = an.tier_of(net)
    idx, qs = an.build(net, tier)
    og = an.org_groups(net, tier)
    names = sorted(og)
    rem = [n for n in names if removed.lower() in n.lower()]
    assert len(rem) == 1, (t, removed, names)
    nominal = an.analyse_config(net, tier)["orgs"]
    with_removed_down = remaining_margin(net, tier, qs, og, rem)
    others = {n: remaining_margin(net, tier, qs, og, [n]) for n in names if n != rem[0]}
    worst = min(others.values())
    return nominal, with_removed_down, worst, others


def main():
    print(f"{'case':34s} {'snapshot':18s} nominal  removed down  other down (worst)")
    for label, operator, removed, t_before, t_inside in CASES:
        for tag, t in (("before", t_before), ("inside", t_inside)):
            nominal, rd, worst, others = analyse(t, operator, removed)
            print(f"{label:34s} {tag + ' ' + t:18s}   {nominal}          {rd}             {worst}")
            if tag == "inside":
                low = [n for n, v in others.items() if v == worst]
                print(f"{'':34s} organizations whose failure leaves the margin at {worst}: {', '.join(low)}")
        print()


if __name__ == "__main__":
    main()
