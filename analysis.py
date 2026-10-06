#!/usr/bin/env python3
"""
Mechanism analysis for the Stellar quorum configuration study. Two parts:

PART A - Three CONFIGURATION CHANGES (Blockdaemon May 2020, SDF April 2021, Franklin Templeton October 2024)
  1. Print the quorum set BEFORE and AFTER for the validators that changed.
  2. Recompute the liveness margin (minimal blocking set) for three configurations:
        - before the change
        - actual, after the change
        - COUNTERFACTUAL: the earlier configuration with only the quorum sets of the
          changed validators replaced
     If the counterfactual reproduces the drop, the change made by that one organization
     is the CAUSE, and a check run before the change would have shown it.

PART B - Daily timeline of Wirex (2022) and SatoshiPay (2025)
  Daily uptime per validator and for the organization, the first day with signs of
  degradation, and the distance to the removal / major outage.

Run:    python mechanism_analysis.py      (about 15 requests, 1-3 minutes)
Place it in the same directory as the earlier scripts; downloaded snapshots are reused.
Output: ./sdf_feasibility/mechanism/report.md
Standard library only.
"""

import csv
import itertools
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "https://radar.withobsrvr.com/api"
SNAP = Path("sdf_feasibility") / "verify" / "raw"       # snapshot cache shared with the earlier script
OUT = Path("sdf_feasibility") / "mechanism"
TIMEOUT = 120
MAX_COMBOS = 600_000        # cap on combinations for node level exhaustive search

# (name, description, before, during, after recovery)  -- UTC times
CONFIG_CASES = [
    ("2020-05 Blockdaemon", "Blocking set 6 -> 4 (organizations 3 -> 2) for 7.5 days",
     "2020-05-21T12:00", "2020-05-23T12:00", "2020-05-30T12:00"),
    ("2021-04 SDF", "After the 6 April 2021 incident, blocking set 6 -> 4 for 1.3 days",
     "2021-04-05T12:00", "2021-04-07T12:00", "2021-04-20T12:00"),
    ("2024-10 Franklin Templeton", "Blocking set 6 -> 5 for 4.6 days",
     "2024-10-03T10:00", "2024-10-05T12:00", "2024-10-09T12:00"),
    ("2022-02 unexplained", "Node blocking set 6 -> 5 for 2.4 days",
     "2022-02-25T12:00", "2022-02-27T12:00", "2022-03-01T12:00"),
    ("2022-07 Wirex period", "Nominal blocking set 6 -> 5 for 3 days during the Wirex trouble",
     "2022-07-09T12:00", "2022-07-11T12:00", "2022-07-25T12:00"),
    ("2022-07-13 organizations 2", "Nominal blocking set 4 (organizations 2) for 12.6 h",
     "2022-07-09T12:00", "2022-07-13T12:00", "2022-07-25T12:00"),
    ("2021-04-13 transient", "Node blocking set 5 for 5.4 h with a 30/9 top tier",
     "2021-04-12T12:00", "2021-04-13T15:00", "2021-04-14T12:00"),
]

# (organization name contains this string, snapshot used to get public keys, from, to, milestone date, milestone description)
ORG_TIMELINES = [
    ("Wirex", "2022-07-26T08:00", "2022-01-01", "2022-12-31", "2022-12-14", "left the top tier"),
    ("SatoshiPay", "2025-08-22T08:00", "2025-01-01", "2026-09-30", "2025-08-22", "all 3 validators down for more than 3 days"),
]

LOG = []


def log(m):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {m}"
    print(line, flush=True)
    LOG.append(line)


def get(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "hust-fbas-research/0.5 (academic feasibility check)", "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.status, json.loads(r.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404, None
            last = e.code
        except Exception as e:
            last = type(e).__name__
        time.sleep(5)
    log(f"ERROR {last}  {url}")
    return 0, None


def snapshot(t):
    f = SNAP / ("snap_" + t.replace(":", "") + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    status, data = get(f"{BASE}/v1?{urllib.parse.urlencode({'at': t + ':00.000Z'})}")
    time.sleep(0.5)
    if isinstance(data, dict) and "nodes" in data:
        f.write_text(json.dumps(data), encoding="utf-8")
        log(f"downloaded snapshot {t} -> {data.get('time')}")
        return data
    log(f"could NOT download snapshot {t} (HTTP {status})")
    return None


# ---------------------------------------------------------------- FBAS

def walk(q, acc):
    if isinstance(q, dict):
        acc.update(q.get("validators") or [])
        for i in q.get("innerQuorumSets") or []:
            walk(i, acc)


def tier_of(net):
    tq = net.get("transitiveQuorumSet")
    if tq:
        return sorted(tq)
    nodes = {n["publicKey"]: n for n in net.get("nodes") or []}
    cnt = {}
    for n in nodes.values():
        acc = set()
        walk(n.get("quorumSet"), acc)
        for pk in acc:
            cnt[pk] = cnt.get(pk, 0) + 1
    seed = max(cnt, key=cnt.get)
    seen, todo = set(), [seed]
    while todo:
        pk = todo.pop()
        if pk not in seen:
            seen.add(pk)
            acc = set()
            walk(nodes.get(pk, {}).get("quorumSet"), acc)
            todo.extend(acc - seen)
    return sorted(seen)


def compile_qset(q, idx):
    """-> (threshold, bitmask of validators in the tier, [inner...])"""
    if not isinstance(q, dict):
        return None
    mask = 0
    for pk in q.get("validators") or []:
        if pk in idx:
            mask |= 1 << idx[pk]
    inner = [c for c in (compile_qset(i, idx) for i in q.get("innerQuorumSets") or []) if c]
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


def greatest_quorum(S, qs):
    """Greatest quorum contained in the set S (bitmask). 0 = no quorum left."""
    while True:
        T, i, m = S, 0, S
        while m:
            if m & 1:
                c = qs[i]
                if c is None or not sat(c, S):
                    T &= ~(1 << i)
            m >>= 1
            i += 1
        if T == S:
            return S
        S = T


def min_blocking(groups, full, qs):
    """groups: list of bitmasks (each element is one node or one organization).
    Returns (minimal size, the sets of that size [at most 12], search_completed)."""
    n, done = len(groups), 0
    for k in range(0, n + 1):
        found = []
        for combo in itertools.combinations(range(n), k):
            done += 1
            if done > MAX_COMBOS:
                return None, [], False
            B = 0
            for g in combo:
                B |= groups[g]
            if greatest_quorum(full & ~B, qs) == 0:
                found.append(combo)
        if found:
            return k, found[:12], True
    return None, [], True


def build(net, tier, override=None):
    """override: {publicKey: quorumSet} used instead of the quorum set in net."""
    idx = {pk: i for i, pk in enumerate(tier)}
    nodes = {n["publicKey"]: n for n in net.get("nodes") or []}
    qs = []
    for pk in tier:
        q = (override or {}).get(pk) or nodes.get(pk, {}).get("quorumSet")
        qs.append(compile_qset(q, idx))
    return idx, qs


def org_groups(net, tier):
    orgname = {}
    for o in net.get("organizations") or []:
        for pk in o.get("validators") or []:
            orgname[pk] = o.get("name") or o.get("homeDomain") or o.get("id")
    nodes = {n["publicKey"]: n for n in net.get("nodes") or []}
    groups = {}
    for i, pk in enumerate(tier):
        org = orgname.get(pk) or nodes.get(pk, {}).get("homeDomain") or "(unknown)"
        groups[org] = groups.get(org, 0) | (1 << i)
    return groups


def analyse_config(net, tier, override=None):
    idx, qs = build(net, tier, override)
    full = (1 << len(tier)) - 1
    og = org_groups(net, tier)
    names = sorted(og)
    ko, sets_o, _ = min_blocking([og[n] for n in names], full, qs)
    kn, _, complete = min_blocking([1 << i for i in range(len(tier))], full, qs)
    has_q = greatest_quorum(full, qs) != 0
    return {"orgs": ko, "org_sets": [[names[i] for i in c] for c in sets_o],
            "nodes": kn if complete else None, "has_quorum": has_q}


def fmt_qset(q, names, orgof, depth=0):
    if not isinstance(q, dict):
        return ["(no quorum set)"]
    vals = q.get("validators") or []
    inner = q.get("innerQuorumSets") or []
    pad = "  " * depth
    out = [f"{pad}- requires {q.get('threshold')} of {len(vals) + len(inner)} elements"]
    if vals:
        out.append(f"{pad}  direct validators: " + ", ".join(sorted(names.get(v, v[:8]) for v in vals)))
    for i in sorted(inner, key=lambda x: str(sorted(x.get("validators") or []))):
        iv = i.get("validators") or []
        orgs = sorted({orgof.get(v, "?") for v in iv})
        if not i.get("innerQuorumSets"):
            out.append(f"{pad}  [{'/'.join(orgs)}] requires {i.get('threshold')} of {len(iv)}: "
                       + ", ".join(sorted(names.get(v, v[:8]) for v in iv)))
        else:
            out += fmt_qset(i, names, orgof, depth + 1)
    return out


def canon(q):
    if not isinstance(q, dict):
        return None
    return (q.get("threshold"), tuple(sorted(q.get("validators") or [])),
            tuple(sorted((canon(i) for i in q.get("innerQuorumSets") or []), key=str)))


def config_case(name, desc, t_before, t_during, t_after):
    R = ["", f"## {name}: {desc}", ""]
    a, b = snapshot(t_before), snapshot(t_during)
    if not a or not b:
        return R + ["Could not download the snapshots."], None
    tier = tier_of(a)
    na = {n["publicKey"]: n for n in a.get("nodes") or []}
    nb = {n["publicKey"]: n for n in b.get("nodes") or []}
    names = {pk: (n.get("name") or pk[:8]) for pk, n in list(nb.items()) + list(na.items())}
    orgof = {}
    for net in (b, a):
        for o in net.get("organizations") or []:
            for pk in o.get("validators") or []:
                orgof[pk] = o.get("name") or o.get("id")

    changed = [pk for pk in tier if pk in nb and canon(na.get(pk, {}).get("quorumSet")) != canon(nb[pk].get("quorumSet"))]
    R.append(f"Top tier at the reference time: {len(tier)} validators. Validators that changed quorum set: "
             + (", ".join(names[pk] for pk in changed) or "NONE"))
    # group validators that share the same (before, after) pair
    seen = {}
    for pk in changed:
        key = (canon(na[pk].get("quorumSet")), canon(nb[pk].get("quorumSet")))
        seen.setdefault(key, []).append(pk)
    for pks in seen.values():
        pk = pks[0]
        R += ["", f"### Quorum set of: {', '.join(names[p] for p in pks)}", "", "BEFORE:", "```"]
        R += fmt_qset(na[pk].get("quorumSet"), names, orgof) + ["```", "AFTER:", "```"]
        R += fmt_qset(nb[pk].get("quorumSet"), names, orgof) + ["```"]
        qa, qb = na[pk].get("quorumSet") or {}, nb[pk].get("quorumSet") or {}
        sa, sb = set(), set()
        walk(qa, sa)
        walk(qb, sb)
        diff = [f"outer threshold {qa.get('threshold')} -> {qb.get('threshold')}",
                f"outer elements {len(qa.get('validators') or []) + len(qa.get('innerQuorumSets') or [])} -> "
                f"{len(qb.get('validators') or []) + len(qb.get('innerQuorumSets') or [])}"]
        if sb - sa:
            diff.append("added: " + ", ".join(sorted(names.get(v, v[:8]) for v in sb - sa)))
        if sa - sb:
            diff.append("removed: " + ", ".join(sorted(names.get(v, v[:8]) for v in sa - sb)))
        R.append("Difference: " + "; ".join(diff))

    log(f"{name}: computing blocking sets (may take 1-2 minutes)...")
    before = analyse_config(a, tier)
    actual = analyse_config(b, tier)
    cf = analyse_config(a, tier, {pk: nb[pk].get("quorumSet") for pk in changed}) if changed else None
    sa_, sb_ = a.get("statistics") or {}, b.get("statistics") or {}

    def row(label, r, radar=None):
        sets = "; ".join(" + ".join(s) for s in r["org_sets"][:6]) if r["org_sets"] else "-"
        rd = f"{radar.get('minBlockingSetOrgsSize')} / {radar.get('minBlockingSetSize')}" if radar else "-"
        return f"| {label} | {r['orgs']} | {r['nodes'] if r['nodes'] is not None else 'not computed'} | {rd} | {sets} |"

    R += ["", "### Recomputed liveness margin (top tier only)", "",
          "| Configuration | Min blocking set (organizations) | (nodes) | Recorded by Radar (organizations / nodes) | Smallest groups of organizations that block the network |",
          "|---|---|---|---|---|",
          row("Before the change", before, sa_), row("Actual, after the change", actual, sb_)]
    verdict = None
    if cf:
        R.append(row("COUNTERFACTUAL: only the quorum sets of the validators above replaced", cf))
        if cf["orgs"] == actual["orgs"] and (cf["orgs"] or 0) < (before["orgs"] or 0):
            verdict = "CONFIRMED: this change alone is sufficient to lower the organization level margin from %s to %s." % (before["orgs"], cf["orgs"])
        elif cf["nodes"] is not None and before["nodes"] is not None and cf["nodes"] < before["nodes"] and cf["nodes"] == actual["nodes"]:
            verdict = "CONFIRMED (node level): this change alone lowers the blocking set from %s to %s nodes." % (before["nodes"], cf["nodes"])
        elif cf["orgs"] == before["orgs"] and cf["nodes"] == before["nodes"]:
            verdict = "NOT CONFIRMED: replacing only these quorum sets does not lower the margin; the cause lies elsewhere."
        else:
            verdict = "PARTIAL: the counterfactual differs from both the before and the after configuration; inspect manually."
    else:
        verdict = "No top tier validator changed its quorum set between the two snapshots."
    R += ["", f"**Mechanism verdict: {verdict}**"]
    if before["orgs"] != sa_.get("minBlockingSetOrgsSize"):
        R.append(f"(Note: the recomputed value for the earlier configuration ({before['orgs']}) differs from the value recorded by Radar "
                 f"({sa_.get('minBlockingSetOrgsSize')}); this script's computation may not match Radar exactly.)")

    c = snapshot(t_after)
    if c:
        nc = {n["publicKey"]: n for n in c.get("nodes") or []}
        back = [names[pk] for pk in changed if pk in nc and canon(nc[pk].get("quorumSet")) == canon(na[pk].get("quorumSet"))]
        sc = c.get("statistics") or {}
        R.append(f"Afterwards ({t_after}): {len(back)}/{len(changed)} validators had returned to the earlier quorum set; "
                 f"Radar records blocking set organizations/nodes = {sc.get('minBlockingSetOrgsSize')}/{sc.get('minBlockingSetSize')}.")
    return R, verdict


# ---------------------------------------------------------------- organization timelines

def day_stats(kind, ident, d1, d2):
    f = OUT / "raw" / f"{kind}_{ident[:12]}_{d1}_{d2}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    q = urllib.parse.urlencode({"from": d1 + "T00:00:00.000Z", "to": d2 + "T00:00:00.000Z"})
    status, data = get(f"{BASE}/v1/{kind}/{urllib.parse.quote(ident)}/day-statistics?{q}")
    time.sleep(0.5)
    if isinstance(data, list):
        f.write_text(json.dumps(data), encoding="utf-8")
        return data
    log(f"could NOT download day-statistics {kind} {ident[:12]} (HTTP {status})")
    return []


def ratio(rec, key):
    c = rec.get("crawlCount") or 0
    return (rec.get(key) or 0) / c if c else None


def org_timeline(match, snap_t, d1, d2, milestone, mdesc):
    R = ["", f"## Timeline of {match}: {d1} to {d2} (milestone: {milestone}, {mdesc})", ""]
    net = snapshot(snap_t)
    if not net:
        return R + ["Could not download the snapshot needed for the public keys."]
    org = next((o for o in net.get("organizations") or [] if match.lower() in (o.get("name") or "").lower()), None)
    if not org:
        return R + [f"No organization found whose name contains '{match}'."]
    nodes = {n["publicKey"]: n for n in net.get("nodes") or []}
    vals = [(pk, nodes.get(pk, {}).get("name") or pk[:8]) for pk in org.get("validators") or []]

    per = {}
    for pk, nm in vals:
        data = day_stats("node", pk, d1, d2)
        if data and "isValidatingCount" not in data[0]:
            R.append(f"(Node data fields differ from expected: {sorted(data[0].keys())})")
        for r in data:
            per.setdefault(str(r.get("time"))[:10], {})[nm] = ratio(r, "isValidatingCount")
    odata = day_stats("organization", org["id"], d1, d2)
    okey = "isSubQuorumAvailableCount"
    if odata and okey not in odata[0]:
        R.append(f"(Organization data fields differ from expected: {sorted(odata[0].keys())})")
    oday = {str(r.get("time"))[:10]: ratio(r, okey) for r in odata}

    days = sorted(set(per) | set(oday))
    if not days:
        return R + ["No daily data available."]
    names = [nm for _, nm in vals]
    rows, bad = [], []
    for d in days:
        vs = [per.get(d, {}).get(nm) for nm in names]
        o = oday.get(d)
        rows.append([d] + [("" if v is None else round(100 * v, 1)) for v in vs] + ["" if o is None else round(100 * o, 1)])
        degraded = [v for v in vs if v is not None and v < 0.9]
        if degraded or (o is not None and o < 0.99):
            bad.append((d, vs, o))
    with open(OUT / f"timeline_{match}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date"] + [f"{nm} % validating" for nm in names] + ["organization % available"])
        w.writerows(rows)

    def pct(v):
        return "-" if v is None else f"{100 * v:.0f}%"

    R.append(f"Validators: {', '.join(names)}. Days with data: {len(days)}. "
             f"Days with signs of degradation (a validator below 90% or the organization below 99%): {len(bad)}.")
    if bad:
        first = bad[0][0]
        gap = (datetime.fromisoformat(milestone) - datetime.fromisoformat(first)).days
        org_bad = [b for b in bad if b[2] is not None and b[2] < 0.99]
        R += ["", f"- First day with signs: **{first}**, {gap} days before the milestone {milestone} ({mdesc}).",
              f"- Days on which THE ORGANIZATION was partly unavailable (below 99%): {len(org_bad)}"
              + (f", first on {org_bad[0][0]}" if org_bad else "") + ".", "",
              "By month:", "", "| Month | Days with signs | " + " | ".join(names) + " | Organization |",
              "|---|---|" + "---|" * (len(names) + 1)]
        for m in sorted({d[:7] for d in days}):
            md = [d for d in days if d[:7] == m]
            avg = []
            for nm in names:
                xs = [per.get(d, {}).get(nm) for d in md]
                xs = [x for x in xs if x is not None]
                avg.append(sum(xs) / len(xs) if xs else None)
            xo = [oday[d] for d in md if oday.get(d) is not None]
            R.append(f"| {m} | {sum(1 for b in bad if b[0][:7] == m)} | " + " | ".join(pct(x) for x in avg)
                     + f" | {pct(sum(xo) / len(xo) if xo else None)} |")
        R += ["", "First 40 days with signs:", "", "| Date | " + " | ".join(names) + " | Organization |",
              "|---|" + "---|" * (len(names) + 1)]
        for d, vs, o in bad[:40]:
            R.append(f"| {d} | " + " | ".join(pct(v) for v in vs) + f" | {pct(o)} |")
    return R


def main():
    (OUT / "raw").mkdir(parents=True, exist_ok=True)
    SNAP.mkdir(parents=True, exist_ok=True)
    body, summ = [], []
    for case in CONFIG_CASES:
        r, v = config_case(*case)
        body += r
        summ.append(f"- {case[0]}: {v or 'no data'}")
    for tl in ORG_TIMELINES:
        body += org_timeline(*tl)
    head = ["# Mechanism analysis", "", f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
            "## Summary of part A (configuration changes)", ""] + summ + [
            "", "How to read: 'CONFIRMED' means that replacing only that organization's quorum sets in the earlier configuration "
                "lowers the network wide margin exactly as observed. This is the direct counterfactual for the claim that "
                "a check run before the change would have detected it.",
            "Limitation: the script considers top tier validators only and uses its own blocking set computation; "
            "values may differ from Radar in edge cases."]
    (OUT / "report.md").write_text("\n".join(head + body) + "\n", encoding="utf-8")
    (OUT / "run.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    print("\n" + "\n".join(head))
    print(f"\nDone. Report written to {OUT / 'report.md'}.")


if __name__ == "__main__":
    main()