"""Exhaustive check of the symmetric top tier arithmetic quoted in the proposal (objective O2).

Model. n organizations with three validators each. Every validator's quorum set lists every
organization as an inner set with threshold 2 of 3, and the outer threshold follows the
stellar-core automatic rule t(n) = n - floor((n - 1) / 3). A change is made by one operator
only: either all three of its validators, or a single one of them, remove one organization
from their list (the threshold is recomputed by the rule).

Quantity. The liveness margin in organizations: the smallest set of organizations whose
failure (all validators down) leaves no quorum among the remaining validators. A quorum is a
non-empty set of validators each of whose quorum sets is satisfied inside the set; the greatest
quorum inside a set of live validators is found by repeatedly discarding validators whose
quorum set cannot be met.

Claims checked (see the proposal, O2):
  1. t(n) = t(n - 1) exactly when n = 1 (mod 3).
  2. When all validators of one operator drop one organization, the margin falls from f + 1 to f
     if n = 3f + 1, and is unchanged if n = 3f + 2 or 3f + 3.
  3. When a single validator of one operator makes the same change, the organization level
     margin is unchanged (the loss is at node level only).
  4. At n = 3f + 1, one operator replacing an organization by a newcomer keeps the margin if it
     adds the newcomer first and loses one organization of margin if it removes the old one first.

Standard library only. Runs in well under a minute for n up to 13.
"""
from itertools import combinations

K = 3  # validators per organization
INNER = 2  # inner threshold, 2 of 3


def threshold(n):
    return n - (n - 1) // 3


def greatest_quorum(alive, qsets):
    alive = set(alive)
    changed = True
    while changed:
        changed = False
        for v in list(alive):
            t, orgs = qsets[v]
            met = sum(1 for o in orgs if sum(1 for i in range(K) if (o, i) in alive) >= INNER)
            if met < t:
                alive.remove(v)
                changed = True
    return alive


def margin(orgs_all, qsets):
    """Smallest number of organizations whose failure leaves no quorum."""
    vals = list(qsets)
    for size in range(0, len(orgs_all) + 1):
        for failed in combinations(orgs_all, size):
            alive = [v for v in vals if v[0] not in failed]
            if not greatest_quorum(alive, qsets):
                return size
    return None


def network(n_orgs, trust):
    """trust: dict validator -> list of organizations it trusts; validators not listed trust
    the organizations in `trust['default']`."""
    qsets = {}
    for o in range(n_orgs):
        for i in range(K):
            orgs = trust.get((o, i), trust['default'])
            qsets[(o, i)] = (threshold(len(orgs)), orgs)
    return qsets


def main():
    print("Claim 1: t(n) == t(n-1) exactly when n = 1 (mod 3)")
    for n in range(4, 14):
        same = threshold(n) == threshold(n - 1)
        assert same == (n % 3 == 1), n
    print("  holds for n = 4..13")

    print("\nClaims 2 and 3: one operator (org 0) removes org 1")
    print("  n  n mod 3  t(n)  margin before -> after, whole operator | one validator")
    for n in range(4, 14):
        orgs = list(range(n))
        base = margin(orgs, network(n, {'default': orgs}))
        without = [o for o in orgs if o != 1]
        whole_trust = {'default': orgs}
        for i in range(K):
            whole_trust[(0, i)] = without
        whole = network(n, whole_trust)
        single = network(n, {'default': orgs, (0, 0): without})
        a, b = margin(orgs, whole), margin(orgs, single)
        f = (n - 1) // 3
        if n % 3 == 1:
            assert (base, a) == (f + 1, f), (n, base, a)
        else:
            assert a == base, (n, base, a)
        assert b == base, (n, base, b)
        print(f"  {n:2d}  {n % 3}        {threshold(n):2d}    {base} -> {a} | {b}")
    print("  claims 2 and 3 hold for n = 4..13")

    print("\nClaim 4: replacement by one operator at n = 7 (newcomer is org 7)")
    n = 7
    old = list(range(n))            # what the incumbents trust
    orgs_all = list(range(n + 1))   # includes the newcomer
    base = {'default': old}
    for i in range(K):
        base[(7, i)] = orgs_all  # the newcomer trusts everyone, nobody trusts it yet

    def variant(operator_trusts):
        trust = dict(base)
        for i in range(K):
            trust[(0, i)] = operator_trusts
        return margin(orgs_all, network(n + 1, trust))

    before = margin(orgs_all, network(n + 1, base))
    after_add = variant(orgs_all)
    after_add_remove = variant([o for o in orgs_all if o != 1])
    after_remove = variant([o for o in old if o != 1])
    print(f"  before {before}; add newcomer first {after_add}; then remove old {after_add_remove}; "
          f"remove old first {after_remove}")
    assert before == after_add == after_add_remove == 3 and after_remove == 2
    print("  claim 4 holds")


if __name__ == "__main__":
    main()
