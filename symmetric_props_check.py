#!/usr/bin/env python3
"""
Exhaustive checks of the propositions in symmetric_model_proofs.pdf.

Model. Organizations with k validators each; an organization counts toward a list when
at least m = k//2 + 1 of its validators are in the quorum (majority inner threshold).
Each validator lists organizations and requires t(s) = s - (s-1)//3 of the s it lists
(the automatic threshold of stellar-core). Crash failures. The margin is the minimal
blocking set: the fewest organizations (organization level) or validators (node level)
whose failure leaves no quorum among the remaining validators of the top tier.

P1  t(s) = t(s-1) exactly when s = 1 (mod 3).
P2  symmetric top tier of n: margins f(n)+1 organizations and (f(n)+1)c validators,
    with f(n) = (n-1)//3 and c = k - m + 1.
P3  j of one operator's k validators drop one organization: at n = 1 (mod 3) the node
    margin falls by min(j, c) and the organization margin falls by one iff j >= c;
    otherwise neither falls.
P4  every validator, including those of newcomers and departing organizations, lists a set
    M with L0 <= M <= L0|L1 or L1 <= M <= L0|L1 (any interleaving, validator by validator,
    of changes that add before they remove): both margins stay at or above the smaller
    endpoint. Removing first can lose one organization (P3 with j = k).
Scope of the checks: P1 to P3 are checked exhaustively over failure patterns; P4 at
organization level over every stage assignment, and at validator level on random samples;
all P4 checks use k = 3.

Standard library only.  Usage:  python3 symmetric_props_check.py [--quick]
"""

import itertools
import random
import sys
import time


def t(s):
    return s - (s - 1) // 3


def f(s):
    return (s - 1) // 3


# ------------------------------------------------------------------ class level engine
# A configuration is a list of classes; a class is a group of interchangeable validators:
# (org, size, frozenset of listed orgs). Thresholds follow t(len(list)).

def survives(classes, alive, kof):
    """True if a nonempty quorum remains; alive[i] = validators of class i still up."""
    n_cls = len(classes)
    active = [alive[i] > 0 for i in range(n_cls)]
    while True:
        cnt = {}
        for i in range(n_cls):
            if active[i]:
                o = classes[i][0]
                cnt[o] = cnt.get(o, 0) + alive[i]
        ok = {o for o, v in cnt.items() if v >= kof[o] // 2 + 1}
        changed = False
        for i in range(n_cls):
            if active[i]:
                lst = classes[i][2]
                if sum(1 for e in lst if e in ok) < t(len(lst)):
                    active[i] = False
                    changed = True
        if not changed:
            return any(active)


def tier_classes(classes, seed_org):
    """Restrict to the transitive closure of listed organizations from seed_org."""
    lists = {}
    for o, size, lst in classes:
        lists.setdefault(o, set()).update(lst)
    seen, todo = set(), [seed_org]
    while todo:
        o = todo.pop()
        if o not in seen:
            seen.add(o)
            todo.extend(lists.get(o, ()))
    return [c for c in classes if c[0] in seen]


def org_margin(classes, kof):
    orgs = sorted({c[0] for c in classes})
    for r in range(0, len(orgs) + 1):
        for down in itertools.combinations(orgs, r):
            alive = [0 if c[0] in down else c[1] for c in classes]
            if not survives(classes, alive, kof):
                return r
    return None


def patterns_with_total(sizes, total, linked=None, prev=None):
    """Failure-count vectors with the given total, each entry capped by its class size.
    linked[i] = True when class i is interchangeable with class i-1 (whole organizations
    with the same size and a symmetric role); such runs are generated non-increasing only,
    which skips patterns that are permutations of one another."""
    if linked is None:
        linked = [False] * len(sizes)
    if not sizes:
        if total == 0:
            yield ()
        return
    head, rest = sizes[0], sizes[1:]
    cap_rest = sum(rest)
    hi = min(head, total)
    if linked[0] and prev is not None:
        hi = min(hi, prev)
    for x in range(max(0, total - cap_rest), hi + 1):
        for tail in patterns_with_total(rest, total - x, linked[1:], x):
            yield (x,) + tail


def blocks_with(classes, kof, total, linked=None):
    sizes = [c[1] for c in classes]
    for p in patterns_with_total(sizes, total, linked):
        alive = [s - x for s, x in zip(sizes, p)]
        if not survives(classes, alive, kof):
            return True
    return False


def node_margin(classes, kof, hint=None, linked=None):
    """Exact node margin. Blocking is monotone (more failures never create a quorum), so
    the margin is the smallest total for which some failure pattern blocks; 'hint' starts
    the search near the answer after checking that hint - 1 does not block."""
    sizes = [c[1] for c in classes]
    lo = 0
    if hint is not None and hint > 0 and not blocks_with(classes, kof, hint - 1, linked):
        lo = hint
    for total in range(lo, sum(sizes) + 1):
        if blocks_with(classes, kof, total, linked):
            return total
    return None


# ------------------------------------------------------------------ P1, P2, P3

def check_p1(limit=1000):
    for s in range(2, limit):
        assert (t(s) == t(s - 1)) == (s % 3 == 1), s
        assert t(s) - t(s - 1) in (0, 1)
    return f"P1 holds for 2 <= s < {limit}"


def symmetric(n, k):
    O = frozenset(range(n))
    return [(o, k, O) for o in range(n)], {o: k for o in range(n)}, [False] + [True] * (n - 1)


def partial_drop(n, k, j):
    """Operator 0 has j validators that drop organization X = n-1; the rest are unchanged.
    Organizations 1..n-2 are interchangeable."""
    O = frozenset(range(n))
    head = [c for c in [(0, j, O - {n - 1}), (0, k - j, O)] if c[1] > 0]
    classes = head + [(o, k, O) for o in range(1, n)]
    linked = [False] * len(head) + [False] + [True] * (n - 3) + [False]
    return classes, {o: k for o in range(n)}, linked


def check_p2_p3(ns, ks):
    lines = []
    for k in ks:
        m = k // 2 + 1
        c = k - m + 1
        for n in ns:
            cl, kof, ln = symmetric(n, k)
            om, nm = org_margin(cl, kof), node_margin(cl, kof, hint=(f(n) + 1) * c, linked=ln)
            assert (om, nm) == (f(n) + 1, (f(n) + 1) * c), (n, k, om, nm)
            for j in range(1, k + 1):
                cl, kof, ln = partial_drop(n, k, j)
                om, nm = org_margin(cl, kof), node_margin(cl, kof, hint=(f(n) + 1) * c - min(j, c), linked=ln)
                if n % 3 == 1:
                    exp = (f(n) + 1 - (1 if j >= c else 0), (f(n) + 1) * c - min(j, c))
                else:
                    exp = (f(n) + 1, (f(n) + 1) * c)
                assert (om, nm) == exp, (n, k, j, om, nm, exp)
            lines.append(f"  k={k} n={n}: symmetric {f(n)+1}|{(f(n)+1)*c}; partial drops j=1..{k} as predicted")
    return lines


# ------------------------------------------------------------------ P4 interleavings

def p4_replacement_org_level(n):
    """Replace organization X = n-1 by newcomer N = n; whole organizations move together.
    Stages: S0 = O, S1 = O + N, S2 = O - X + N (add first); R = O - X (remove first)."""
    O = frozenset(range(n))
    X, N = n - 1, n
    S0, S1, S2, R = O, O | {N}, (O - {X}) | {N}, O - {X}
    kof = {o: 3 for o in range(n + 1)}
    target = f(n) + 1
    states = 0
    old = list(range(n - 1))                      # interchangeable old organizations
    for a in range(len(old) + 1):                 # counts at S0, S1, S2
        for b in range(len(old) + 1 - a):
            cnt = (a, b, len(old) - a - b)
            stage_of_old = [S0] * cnt[0] + [S1] * cnt[1] + [S2] * cnt[2]
            for sx in (S0, S1, S2):
                for sn in (S1, S2):
                    cl = [(o, 3, stage_of_old[o]) for o in old] + [(X, 3, sx), (N, 3, sn)]
                    cl = tier_classes(cl, 0)
                    om = org_margin(cl, kof)
                    assert om >= target, (n, cnt, sx, sn, om)
                    states += 1
    # remove first: one operator at R, everybody else at S0 (Proposition 3 with j = k)
    cl = [(0, 3, R)] + [(o, 3, S0) for o in range(1, n)]
    rf = org_margin(tier_classes(cl, 0), kof)
    assert rf == target - (1 if n % 3 == 1 else 0), (n, rf)
    return states, target, rf


def p4_expansion_org_level(n0=7, n1=10):
    """Expansion from n0 to n1 organizations; every operator adds the newcomers one at a
    time in the same order (any operator may be at any stage)."""
    old = list(range(n0))
    new = list(range(n0, n1))
    stages = [frozenset(old) | frozenset(new[:i]) for i in range(len(new) + 1)]
    kof = {o: 3 for o in range(n1)}
    target = min(f(n0), f(n1)) + 1
    states = 0
    for combo in itertools.combinations_with_replacement(range(len(stages)), n0):
        cl = [(o, 3, stages[s]) for o, s in zip(old, combo)] + [(o, 3, stages[-1]) for o in new]
        cl = tier_classes(cl, 0)
        assert org_margin(cl, kof) >= target, combo
        states += 1
    return states, target


def p4_newcomer_hypothesis_needed():
    """The hypothesis of P4 also binds newcomers: at n = 4, with the old organizations
    listing O + N and the newcomer N listing only {N, 0, 1}, one organization blocks."""
    n, N = 4, 4
    O = frozenset(range(n))
    kof = {o: 3 for o in range(n + 1)}
    cl = [(o, 3, O | {N}) for o in range(n)] + [(N, 3, frozenset({N, 0, 1}))]
    m = org_margin(tier_classes(cl, 0), kof)
    assert m == 1, m
    return m


def p4_replacement_node_level(n, samples, rng):
    """Validator by validator: each validator independently at S0, S1 or S2 (X too; N at S1
    or S2). Checks that no failure of (g+1)c - 1 validators blocks."""
    O = frozenset(range(n))
    X, N = n - 1, n
    S0, S1, S2 = O, O | {N}, (O - {X}) | {N}
    kof = {o: 3 for o in range(n + 1)}
    c = 2
    bound = (f(n) + 1) * c
    checked = 0
    for _ in range(samples):
        cl = []
        for o in range(n + 1):
            choices = (S1, S2) if o == N else (S0, S1, S2)
            picks = [rng.choice(choices) for _ in range(3)]
            for st in set(picks):
                cl.append((o, picks.count(st), st))
        cl = tier_classes(cl, 0)
        assert not blocks_with(cl, kof, bound - 1), cl
        checked += 1
    return checked, bound


def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    print(check_p1())
    print("P2, P3 (organization and node margins, exhaustive over failure patterns):")
    for line in check_p2_p3(range(4, 11 if quick else 14), (3,)):
        print(line)
    for line in check_p2_p3(range(4, 8), (4, 5)):
        print(line)
    print("P4 (add before remove keeps the smaller endpoint):")
    for n in range(4, 9 if quick else 11):
        states, target, rf = p4_replacement_org_level(n)
        print(f"  replacement at n={n}: {states} organization level states, all >= {target};"
              f" remove first gives {rf}")
    states, target = p4_expansion_org_level()
    print(f"  expansion 7 -> 10, newcomers added one at a time: {states} states, all >= {target}")
    print(f"  newcomer listing only itself and two organizations at n=4: margin {p4_newcomer_hypothesis_needed()}"
          " (endpoints 2), so the hypothesis on newcomers is needed")
    rng = random.Random(20261025)
    for n, s in ((4, 400 if quick else 3000), (7, 30 if quick else 200)):
        checked, bound = p4_replacement_node_level(n, s, rng)
        print(f"  replacement at n={n}, validator level: {checked} random states, none blocked by {bound - 1} validators")
    print(f"all checks passed in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
