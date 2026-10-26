#!/usr/bin/env python3
"""
Counterfactual alternatives to Blockdaemon's quorum set change of 22 May 2020.

Reads two archived OBSRVR Radar snapshots (one before the change, one during it),
rebuilds the top tier (transitive quorum set) and recomputes, for each configuration:

  margin     minimal blocking set, in organizations and in nodes (liveness margin)
  split      minimal splitting set, in organizations (safety margin)
  QI         quorum intersection (no two disjoint quorums)
  own        peer organizations whose failure blocks Blockdaemon's validators
  one down   the organization margin left when one organization is down

Configurations (only the quorum sets named are changed; all others as archived):
  A0  before the change: Blockdaemon trusts the seven organizations, 5 of 7
  A1  the actual change: SatoshiPay removed, automatic threshold 5 of 6
  A2  SatoshiPay removed, explicit threshold 4 of 6
  R1  replacement, step 1: Blockdaemon adds a newcomer Z first, 6 of 8
  R2  replacement, step 2: Blockdaemon then removes SatoshiPay, 5 of 7
  A3  every top tier operator removes SatoshiPay, automatic threshold 5 of 6
  A4  every top tier operator removes SatoshiPay, threshold 4 of 6
Z is synthetic: three always validating validators (keys ZNEWCOMER1..3) with a two of
three inner set, listing the same seven organizations as Blockdaemon after step 2, 5 of 7.
Each configuration is also checked against stellar-core's minimum threshold: a quorum set
with s top level entries must have threshold >= s - (s-1)//3 (Config::validateConfig);
lower thresholds are refused unless UNSAFE_QUORUM=true.

Semantics: crash failures for blocking sets (a failed node satisfies nobody);
Byzantine failures for splitting sets (a faulty node counts as satisfied for everyone).
A set B is blocking if no quorum remains among the other top tier validators.

Standard library only. Usage (from the repository root):
  python3 blockdaemon_alternatives.py \
      sdf_feasibility/verify/raw/snap_2020-05-21T1200.json \
      sdf_feasibility/verify/raw/snap_2020-05-23T1200.json
"""

import copy
import itertools
import json
import sys

BLOCKDAEMON, SATOSHIPAY = "Blockdaemon", "SatoshiPay"


# ------------------------------------------------------------------ loading

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def org_names(net):
    name = {}
    for o in net.get("organizations") or []:
        for pk in o.get("validators") or []:
            name[pk] = o.get("name") or o.get("homeDomain") or o.get("id")
    return name


def members(q, acc):
    if isinstance(q, dict):
        acc.update(q.get("validators") or [])
        for i in q.get("innerQuorumSets") or []:
            members(i, acc)


def transitive_closure(seeds, qsets):
    seen, todo = set(), list(seeds)
    while todo:
        pk = todo.pop()
        if pk in seen:
            continue
        seen.add(pk)
        acc = set()
        members(qsets.get(pk), acc)
        todo.extend(acc - seen)
    return sorted(seen)


# ------------------------------------------------------------------ FBAS core

def compile_qset(q, idx):
    """-> (threshold, bitmask of member validators, [compiled inner sets]).
    Validators outside the tier are kept as unsatisfiable (they never count)."""
    mask = 0
    for pk in q.get("validators") or []:
        if pk in idx:
            mask |= 1 << idx[pk]
    inner = [compile_qset(i, idx) for i in q.get("innerQuorumSets") or []]
    return (int(q.get("threshold") or 0), mask, inner)


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


def greatest_quorum(S, qs, present=0):
    """Greatest quorum inside S. 'present' = Byzantine nodes that count as satisfied
    for everyone but are not members of the quorum."""
    while True:
        T, i, m = S, 0, S
        while m:
            if m & 1 and not sat(qs[i], S | present):
                T &= ~(1 << i)
            m >>= 1
            i += 1
        if T == S:
            return S
        S = T


class Config:
    def __init__(self, label, qsets, orgof, seeds):
        self.label = label
        self.tier = transitive_closure(seeds, qsets)
        self.idx = {pk: i for i, pk in enumerate(self.tier)}
        self.qs = [compile_qset(qsets[pk], self.idx) for pk in self.tier]
        self.full = (1 << len(self.tier)) - 1
        self.orgs = {}
        for pk in self.tier:
            o = orgof.get(pk, "(unknown)")
            self.orgs[o] = self.orgs.get(o, 0) | (1 << self.idx[pk])

    def org(self, part):
        return next(o for o in self.orgs if part in o)

    def min_blocking(self, groups, base=None, stop=None, limit=8):
        """Smallest number of groups whose crash leaves no quorum (or, if 'stop' is
        given, leaves no member of 'stop' in the greatest quorum)."""
        base = self.full if base is None else base
        for k in range(0, min(limit, len(groups)) + 1):
            for combo in itertools.combinations(groups, k):
                B = 0
                for g in combo:
                    B |= g
                q = greatest_quorum(base & ~B, self.qs)
                if (q == 0) if stop is None else (q & stop == 0):
                    return k
        return None

    def margin(self, down=0):
        base = self.full & ~down
        og = [m for m in self.orgs.values() if m & base]
        nodes = [1 << i for i in range(len(self.tier)) if (base >> i) & 1]
        return self.min_blocking(og, base), self.min_blocking(nodes, base)

    def split_orgs(self):
        """Smallest number of organizations whose (Byzantine) failure allows two
        disjoint quorums among the remaining validators."""
        names = list(self.orgs)
        for k in range(0, len(names) + 1):
            for faulty in itertools.combinations(names, k):
                S = 0
                for o in faulty:
                    S |= self.orgs[o]
                honest = [o for o in names if o not in faulty]
                for r in range(1, len(honest)):
                    for left in itertools.combinations(honest, r):
                        L = 0
                        for o in left:
                            L |= self.orgs[o]
                        R = self.full & ~S & ~L
                        if greatest_quorum(L, self.qs, S) and greatest_quorum(R, self.qs, S):
                            return k
        return None

    def quorum_intersection(self):
        names = list(self.orgs)
        for r in range(1, len(names)):
            for left in itertools.combinations(names, r):
                L = 0
                for o in left:
                    L |= self.orgs[o]
                if greatest_quorum(L, self.qs) and greatest_quorum(self.full & ~L, self.qs):
                    return False
        return True

    def own_tolerance(self, who, down=0):
        mine = self.orgs[self.org(who)]
        base = self.full & ~down
        peers = [m for o, m in self.orgs.items() if who not in o and m & base]
        return self.min_blocking(peers, base=base, stop=mine)


# ------------------------------------------------------------------ alternatives

def drop_org(q, victims):
    """Copy of q without inner sets made only of the victim validators."""
    q = copy.deepcopy(q)
    q["innerQuorumSets"] = [i for i in q.get("innerQuorumSets") or []
                            if not set(i.get("validators") or []) <= victims]
    q["validators"] = [v for v in q.get("validators") or [] if v not in victims]
    return q


def min_threshold(s):
    """stellar-core's minimum top level threshold for s entries (Byzantine level)."""
    return s - (s - 1) // 3


def unsafe_validators(qsets, tier):
    """Validators whose top level threshold is below stellar-core's minimum."""
    bad = []
    for pk in tier:
        q = qsets[pk]
        s = len(q.get("validators") or []) + len(q.get("innerQuorumSets") or [])
        if s and int(q.get("threshold") or 0) < min_threshold(s):
            bad.append(pk)
    return bad


def describe(q, orgof):
    parts = []
    for i in q.get("innerQuorumSets") or []:
        names = {orgof.get(v, v[:6]) for v in i.get("validators") or []}
        parts.append("/".join(sorted(names)))
    return f"{q.get('threshold')} of {len(parts) + len(q.get('validators') or [])} [{', '.join(sorted(parts))}]"


def main(before_path, during_path):
    before, during = load(before_path), load(during_path)
    orgof = org_names(before)
    orgof.update({k: v for k, v in org_names(during).items() if k not in orgof})
    q0 = {n["publicKey"]: n.get("quorumSet") or {} for n in before["nodes"]}
    qd = {n["publicKey"]: n.get("quorumSet") or {} for n in during["nodes"]}
    tier0 = before.get("transitiveQuorumSet") or []
    bd = sorted(pk for pk in tier0 if BLOCKDAEMON in orgof.get(pk, ""))
    sp = {pk for pk in tier0 if SATOSHIPAY in orgof.get(pk, "")}
    seeds = [pk for pk in tier0 if "Stellar Development Foundation" in orgof.get(pk, "")]

    print(f"before: {before.get('time')}   during: {during.get('time')}")
    print(f"top tier before: {len(tier0)} validators; Blockdaemon validators: {len(bd)}; SatoshiPay validators: {len(sp)}")
    print("Blockdaemon quorum set before:", describe(q0[bd[0]], orgof))
    print("Blockdaemon quorum set during:", describe(qd[bd[0]], orgof))
    same = all(json.dumps(qd[pk], sort_keys=True) == json.dumps(qd[bd[0]], sort_keys=True) for pk in bd)
    print("all Blockdaemon validators share the 'during' quorum set:", same)
    expected = drop_org(q0[bd[0]], sp)
    print("'during' set = 'before' set without SatoshiPay, threshold kept at",
          expected["threshold"], ":",
          json.dumps({k: v for k, v in qd[bd[0]].items() if k in ("threshold", "validators", "innerQuorumSets")}, sort_keys=True)
          == json.dumps({k: v for k, v in expected.items() if k in ("threshold", "validators", "innerQuorumSets")}, sort_keys=True))

    configs = []
    a0 = dict(q0)
    configs.append(("A0 before the change (5 of 7, trusts SatoshiPay)", a0))
    a1 = dict(q0)
    for pk in bd:
        a1[pk] = qd[pk]
    configs.append(("A1 actual change (5 of 6 without SatoshiPay)", a1))
    a2 = dict(a1)
    for pk in bd:
        a2[pk] = dict(qd[pk], threshold=4)
    configs.append(("A2 same six, explicit 4 of 6", a2))
    # replacement by a synthetic newcomer Z, adding Z before removing SatoshiPay
    zkeys = ["ZNEWCOMER1", "ZNEWCOMER2", "ZNEWCOMER3"]
    for z in zkeys:
        orgof[z] = "Newcomer Z (synthetic)"
    z_inner = {"threshold": 2, "validators": list(zkeys), "innerQuorumSets": []}
    b0, b1 = q0[bd[0]], qd[bd[0]]
    assert not (b0.get("validators") or []) and not (b1.get("validators") or [])
    z_list = {"threshold": 5, "validators": [], "innerQuorumSets": list(b1["innerQuorumSets"]) + [z_inner]}
    r1, r2 = dict(q0), dict(q0)
    for pk in bd:
        r1[pk] = {"threshold": 6, "validators": [], "innerQuorumSets": list(b0["innerQuorumSets"]) + [z_inner]}
        r2[pk] = z_list
    for z in zkeys:
        r1[z] = z_list
        r2[z] = z_list
    configs.append(("R1 replace, step 1: add Z first (6 of 8)", r1))
    configs.append(("R2 replace, step 2: then remove SatoshiPay (5 of 7 with Z)", r2))
    a3, a4 = dict(q0), dict(q0)
    for pk in tier0:
        if pk in sp:
            continue
        a3[pk] = drop_org(q0[pk], sp)
        a4[pk] = dict(drop_org(q0[pk], sp), threshold=4)
        assert int(q0[pk].get("threshold")) == 5 and len(a3[pk]["innerQuorumSets"]) == 6, pk
    configs.append(("A3 all operators drop SatoshiPay, automatic 5 of 6", a3))
    configs.append(("A4 all operators drop SatoshiPay, 4 of 6", a4))

    print()
    rows = []
    for label, qs in configs:
        c = Config(label, qs, orgof, seeds)
        mo, mn = c.margin()
        res = {
            "label": label, "tier": f"{len(c.tier)}/{len(c.orgs)}",
            "margin": f"{mo}|{mn}", "split": c.split_orgs(), "QI": c.quorum_intersection(),
            "own": c.own_tolerance(BLOCKDAEMON),
            "own_sp_down": c.own_tolerance(BLOCKDAEMON, down=c.orgs[c.org(SATOSHIPAY)])
            if any(SATOSHIPAY in o for o in c.orgs) else None,
            "unsafe": len(unsafe_validators(qs, c.tier)),
        }
        one_down = {}
        for o, m in sorted(c.orgs.items()):
            one_down[o] = c.margin(down=m)[0]
        res["one_down"] = one_down
        rows.append(res)
        print(f"{label}")
        print(f"   top tier {res['tier']} (validators/organizations); margin orgs|nodes {res['margin']}; "
              f"splitting set {res['split']} orgs; quorum intersection {res['QI']}; "
              f"peer organizations whose failure blocks Blockdaemon: {res['own']}"
              + (f" (with SatoshiPay down: {res['own_sp_down']} more)" if res['own_sp_down'] is not None else ""))
        print(f"   validators below stellar-core's minimum threshold (need UNSAFE_QUORUM): {res['unsafe']}")
        print("   organization margin left with one organization down:")
        for o, v in one_down.items():
            print(f"      {o:35s} {v}")
    return rows


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
