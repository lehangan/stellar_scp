#!/usr/bin/env python3
"""
What one operator's removal of one organization would do to the current top tier.

Reads one archived OBSRVR Radar snapshot, rebuilds the top tier (transitive quorum set),
reports whether it is symmetric (every validator has the same quorum set), and recomputes
the organization level margin (minimal blocking set, crash failures) for:
  - the configuration as archived;
  - every operator X and every other organization Y, when j = 1, 2 or all of X's
    validators drop Y and take stellar-core's automatic threshold for the shorter list.

Standard library only. Usage (from the repository root):
  python3 current_tier_removals.py sdf_feasibility/verify/raw/snap_2026-10-01T2300.json
"""

import collections
import itertools
import json
import sys


def t_auto(s):
    return s - (s - 1) // 3


def compile_qset(q, idx):
    mask = 0
    for pk in q.get("validators") or []:
        if pk in idx:
            mask |= 1 << idx[pk]
    return (int(q.get("threshold") or 0), mask,
            [compile_qset(i, idx) for i in q.get("innerQuorumSets") or []])


def sat(c, S):
    t, mask, inner = c
    n = bin(mask & S).count("1")
    if n >= t:
        return True
    for i in inner:
        if sat(i, S):
            n += 1
            if n >= t:
                return True
    return False


def greatest_quorum(S, qs):
    while True:
        T, i, m = S, 0, S
        while m:
            if m & 1 and not sat(qs[i], S):
                T &= ~(1 << i)
            m >>= 1
            i += 1
        if T == S:
            return S
        S = T


def org_margin(qs, groups, full):
    for k in range(0, len(groups) + 1):
        for combo in itertools.combinations(groups, k):
            B = 0
            for g in combo:
                B |= g
            if greatest_quorum(full & ~B, qs) == 0:
                return k
    return None


def main(path):
    net = json.load(open(path, encoding="utf-8"))
    tier = sorted(net["transitiveQuorumSet"])
    idx = {pk: i for i, pk in enumerate(tier)}
    full = (1 << len(tier)) - 1
    orgof = {}
    for o in net.get("organizations") or []:
        for pk in o.get("validators") or []:
            orgof[pk] = o.get("name")
    qsets = {n["publicKey"]: n.get("quorumSet") or {} for n in net["nodes"]}
    orgs = collections.OrderedDict()
    for pk in tier:
        orgs.setdefault(orgof.get(pk, "(unknown)"), []).append(pk)
    groups = []
    for o, pks in orgs.items():
        m = 0
        for pk in pks:
            m |= 1 << idx[pk]
        groups.append(m)

    canon = {json.dumps(qsets[pk], sort_keys=True) for pk in tier}
    q = qsets[tier[0]]
    print(f"snapshot {net.get('time')}: {len(tier)} validators in {len(orgs)} organizations "
          f"({', '.join(f'{o} {len(v)}' for o, v in orgs.items())})")
    print(f"distinct quorum sets in the top tier: {len(canon)}; first one: threshold {q.get('threshold')} of "
          f"{len(q.get('innerQuorumSets') or []) + len(q.get('validators') or [])} entries, inner thresholds "
          f"{sorted({i.get('threshold') for i in q.get('innerQuorumSets') or []})}")

    base_qs = [compile_qset(qsets[pk], idx) for pk in tier]
    base = org_margin(base_qs, groups, full)
    print(f"organization margin as archived: {base}")

    names = list(orgs)
    results = collections.Counter()
    for x in names:
        for y in names:
            if y == x:
                continue
            ymembers = set(orgs[y])
            for j in (1, 2, len(orgs[x])):
                changed = dict(qsets)
                for pk in orgs[x][:j]:
                    q0 = qsets[pk]
                    inner = [i for i in q0.get("innerQuorumSets") or []
                             if not set(i.get("validators") or []) <= ymembers]
                    s = len(inner) + len(q0.get("validators") or [])
                    changed[pk] = dict(q0, innerQuorumSets=inner, threshold=t_auto(s))
                qs = [compile_qset(changed[pk], idx) for pk in tier]
                results[(min(j, 3), org_margin(qs, groups, full))] += 1
    for (j, m), cnt in sorted(results.items()):
        label = "all" if j == 3 else str(j)
        print(f"  {label} of an operator's validators drop one organization: margin {m} "
              f"organizations in {cnt} of {len(names) * (len(names) - 1)} operator/organization pairs")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
