"""Independent check of quorum intersection and the organization level blocking set
on archived OBSRVR Radar snapshots (top tier = transitive quorum set from SDF's validators).

Usage: python3 -I qi_check.py <snapshot.json> [...]
Quorum intersection is decided with z3 (search for two disjoint nonempty quorums).
The blocking set is computed by brute force over organization subsets, using the
greatest quorum of the surviving validators (iterative pruning).
"""
import json
import sys
import itertools
import z3


def refs(qs, acc):
    for v in qs.get("validators", []) or []:
        acc.add(v)
    for inner in qs.get("innerQuorumSets", []) or []:
        refs(inner, acc)
    return acc


def closure(nodes, roots):
    seen = set()
    frontier = list(roots)
    while frontier:
        k = frontier.pop()
        if k in seen or k not in nodes:
            continue
        seen.add(k)
        qs = nodes[k].get("quorumSet") or {}
        for r in refs(qs, set()):
            if r not in seen:
                frontier.append(r)
    return seen


def qs_formula(qs, lit):
    """z3 formula: quorum set satisfied by the set described by lit(key) -> BoolRef/False."""
    terms = [lit(v) for v in qs.get("validators", []) or []]
    terms += [qs_formula(inner, lit) for inner in qs.get("innerQuorumSets", []) or []]
    t = qs.get("threshold", 0)
    if t <= 0:
        return z3.BoolVal(True)
    if len(terms) < t:
        return z3.BoolVal(False)
    return z3.AtLeast(*terms, t) if len(terms) > 1 else terms[0]


def has_intersection(nodes, tier):
    x = {k: z3.Bool("x_" + k[:8] + str(i)) for i, k in enumerate(tier)}
    y = {k: z3.Bool("y_" + k[:8] + str(i)) for i, k in enumerate(tier)}
    s = z3.Solver()

    def lit(d):
        return lambda v: d[v] if v in d else z3.BoolVal(False)

    for k in tier:
        qs = nodes[k].get("quorumSet")
        if not qs or not refs(qs, set()):
            s.add(z3.Not(x[k]), z3.Not(y[k]))
            continue
        s.add(z3.Implies(x[k], qs_formula(qs, lit(x))))
        s.add(z3.Implies(y[k], qs_formula(qs, lit(y))))
        s.add(z3.Not(z3.And(x[k], y[k])))
    s.add(z3.Or(*[x[k] for k in tier]))
    s.add(z3.Or(*[y[k] for k in tier]))
    r = s.check()
    if r == z3.unsat:
        return True, None
    m = s.model()
    q1 = [k for k in tier if z3.is_true(m.eval(x[k], model_completion=True))]
    q2 = [k for k in tier if z3.is_true(m.eval(y[k], model_completion=True))]
    return False, (q1, q2)


def satisfied(qs, alive):
    terms = [1 if v in alive else 0 for v in qs.get("validators", []) or []]
    terms += [1 if satisfied(inner, alive) else 0 for inner in qs.get("innerQuorumSets", []) or []]
    return sum(terms) >= qs.get("threshold", 0) and qs.get("threshold", 0) > 0


def greatest_quorum(nodes, candidates):
    alive = set(k for k in candidates if nodes[k].get("quorumSet"))
    changed = True
    while changed:
        changed = False
        for k in list(alive):
            if not satisfied(nodes[k]["quorumSet"], alive):
                alive.discard(k)
                changed = True
    return alive


def org_blocking_set(nodes, tier, org_of, failed_nodes=frozenset()):
    orgs = sorted(set(org_of[k] for k in tier))
    base = set(tier) - set(failed_nodes)
    if not greatest_quorum(nodes, base):
        return 0, ()
    for size in range(1, len(orgs) + 1):
        for combo in itertools.combinations(orgs, size):
            alive = set(k for k in base if org_of[k] not in combo)
            if not greatest_quorum(nodes, alive):
                return size, combo
    return len(orgs), tuple(orgs)


def main(paths):
    print("snapshot,time,tier_size,tier_matches_radar,qi_ours,qi_radar,blocking_orgs_ours,blocking_orgs_radar,eff_blocking_orgs_ours,eff_blocking_orgs_radar,note")
    for p in paths:
        d = json.load(open(p))
        nodes = {n["publicKey"]: n for n in d["nodes"]}
        orgs = {o["id"]: o for o in d.get("organizations", [])}

        def org_name(k):
            n = nodes[k]
            oid = n.get("organizationId")
            if oid in orgs:
                return orgs[oid]["name"]
            return n.get("homeDomain") or k[:6]

        roots = [k for k, n in nodes.items() if n.get("organizationId") in orgs
                 and orgs[n["organizationId"]]["name"].startswith("Stellar Development Foundation")]
        if not roots:
            roots = [k for k, n in nodes.items() if (n.get("homeDomain") or "").endswith("stellar.org") and n.get("quorumSet")]
        tier = sorted(closure(nodes, roots))
        radar_tier = sorted(d.get("transitiveQuorumSet") or [])
        tier_ok = tier == radar_tier
        qi, witness = has_intersection(nodes, tier)
        st = d.get("statistics") or {}
        org_of = {k: org_name(k) for k in tier}
        b, _ = org_blocking_set(nodes, tier, org_of)
        down = frozenset(k for k in tier if not nodes[k].get("isValidating"))
        eb, _ = org_blocking_set(nodes, tier, org_of, down)
        note = ""
        if not qi:
            q1, q2 = witness
            note = "disjoint quorums: " + "|".join(sorted(set(org_of[k] for k in q1))) + " vs " + "|".join(sorted(set(org_of[k] for k in q2)))
        if not tier_ok:
            note += (" " if note else "") + f"closure {len(tier)} vs radar {len(radar_tier)}"
        print(",".join(str(v) for v in [p.split("/")[-1], d.get("time"), len(tier), tier_ok, qi,
                                        st.get("hasQuorumIntersection"), b, st.get("minBlockingSetOrgsSize"),
                                        eb, st.get("minBlockingSetOrgsFilteredSize"), note]))


if __name__ == "__main__":
    main(sys.argv[1:])
