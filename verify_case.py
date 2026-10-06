#!/usr/bin/env python3
"""
Verify the major events: at that time, the validators of WHICH ORGANIZATION were not validating?

  - Exactly one organization lost the majority of its validators -> a real outage, and
    the organization is identified.
  - Many organizations "down" at the same moment                  -> Radar's crawler probably
    lost connectivity.
  - No organization down but the metric dropped                   -> a configuration change
    (quorum set) or a computation error.

Run:    python verify_cases.py          (about 25 requests, 1-2 minutes)
Output in ./sdf_feasibility/verify/
  report.md          read this file
  cases.csv          one row per (case, time, organization)
  raw/snap_*.json    original snapshots
Standard library only. A second run reuses the snapshots already downloaded.
"""

import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

BASE = "https://radar.withobsrvr.com/api"
OUT = Path("sdf_feasibility") / "verify"
RAW = OUT / "raw"
TIMEOUT = 120

# (case name, description, reference time before the event, [times during the event])  -- UTC times
CASES = [
    ("2020-04-23", "Effective margin down to 1 organization for 7.7 hours",
     "2020-04-23T18:00", ["2020-04-24T01:00", "2020-04-24T05:00"]),
    ("2020-05-22", "Nominal margin reduced (blocking set 6 -> 4) for 7.5 days",
     "2020-05-21T12:00", ["2020-05-23T12:00", "2020-05-27T12:00"]),
    ("2021-04-06", "SDF validators halted (publicly reported); margin down to 1 organization from 14:34 for 3.9 hours",
     "2021-04-05T12:00", ["2021-04-06T10:00", "2021-04-06T16:00", "2021-04-07T12:00"]),
    ("2022-07-26", "Thin effective margin for 1.2 days, at times down to 1 organization",
     "2022-07-26T08:00", ["2022-07-26T20:00", "2022-07-27T08:00"]),
    ("2022-12-13", "Thin margin for 1.1 days, then top tier from 8 to 7 organizations",
     "2022-12-13T06:00", ["2022-12-13T20:00", "2022-12-15T12:00"]),
    ("2023-09-14", "Effective margin at 0 several times within 9 hours (suspected measurement error)",
     "2023-09-13T18:00", ["2023-09-14T05:00", "2023-09-14T10:58", "2023-09-16T12:00"]),
    ("2024-10-03", "Nominal blocking set 6 -> 5 for 4.6 days",
     "2024-10-03T10:00", ["2024-10-05T12:00"]),
    ("2025-08-22", "Thin effective margin for 3.1 days",
     "2025-08-22T08:00", ["2025-08-23T12:00", "2025-08-25T06:00"]),
    ("2026-10-01", "Organization splitting set 4 -> 0 -> 1 (suspected change of analyzer in Radar)",
     "2026-09-30T12:00", ["2026-10-01T09:00", "2026-10-01T23:00"]),
]

STAT_KEYS = ["topTierSize", "topTierOrgsSize", "minBlockingSetSize", "minBlockingSetFilteredSize",
             "minBlockingSetOrgsSize", "minBlockingSetOrgsFilteredSize",
             "minSplittingSetSize", "minSplittingSetOrgsSize", "hasQuorumIntersection"]

LOG = []


def log(m):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {m}"
    print(line, flush=True)
    LOG.append(line)


def snapshot(t):
    at = t + ":00.000Z"
    f = RAW / ("snap_" + t.replace(":", "") + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    url = f"{BASE}/v1?{urllib.parse.urlencode({'at': at})}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "hust-fbas-research/0.4 (academic feasibility check)", "Accept": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                data = json.loads(r.read().decode("utf-8", errors="replace"))
            if isinstance(data, dict) and "nodes" in data:
                f.write_text(json.dumps(data), encoding="utf-8")
                log(f"OK   {t} -> snapshot at {data.get('time')}")
                time.sleep(0.5)
                return data
        except urllib.error.HTTPError as e:
            log(f"HTTP {e.code} {t}")
            if e.code == 404:
                return None
        except Exception as e:
            log(f"ERROR {type(e).__name__} {t}")
        time.sleep(5)
    return None


def walk(q, acc):
    if isinstance(q, dict):
        acc.update(q.get("validators") or [])
        for i in q.get("innerQuorumSets") or []:
            walk(i, acc)


def top_tier(net):
    """Approximate top tier = the transitive quorum set of the network (precomputed by Radar).
    If the snapshot lacks this field: take the trust closure from the most trusted validator."""
    tq = net.get("transitiveQuorumSet")
    if tq:
        return set(tq)
    nodes = {n["publicKey"]: n for n in net.get("nodes") or []}
    cnt = {}
    for n in nodes.values():
        acc = set()
        walk(n.get("quorumSet"), acc)
        for pk in acc:
            cnt[pk] = cnt.get(pk, 0) + 1
    if not cnt:
        return set()
    seed = max(cnt, key=cnt.get)
    seen, todo = set(), [seed]
    while todo:
        pk = todo.pop()
        if pk in seen:
            continue
        seen.add(pk)
        acc = set()
        walk(nodes.get(pk, {}).get("quorumSet"), acc)
        todo.extend(acc - seen)
    return seen


def org_view(net, tier):
    """{organization name: [(node name, isValidating, quorumSetHashKey)]} for the validators in the tier."""
    nodes = {n["publicKey"]: n for n in net.get("nodes") or []}
    orgname = {}
    for o in net.get("organizations") or []:
        for pk in o.get("validators") or []:
            orgname[pk] = o.get("name") or o.get("homeDomain") or o.get("id")
    view = {}
    for pk in tier:
        n = nodes.get(pk)
        org = orgname.get(pk) or (n or {}).get("homeDomain") or "(unknown organization)"
        if n is None:
            view.setdefault(org, []).append((pk[:8], None, None))
        else:
            view.setdefault(org, []).append((n.get("name") or pk[:8], bool(n.get("isValidating")),
                                             n.get("quorumSetHashKey")))
    return view


def stats_line(net):
    s = net.get("statistics") or {}
    return ", ".join(f"{k}={s.get(k)}" for k in STAT_KEYS)


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    R = ["# Verification of major events", "", f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
         "Times in this report are UTC. 'Down' = Radar recorded the validator as not validating at that time.", "",
         "## Summary", "", "| Case | Time | Top tier organizations that lost their majority | Top tier validators down | Assessment |",
         "|---|---|---|---|---|"]
    detail, rows = [], []

    for name, desc, base_t, probes in CASES:
        detail += ["", f"## {name}: {desc}", ""]
        base = snapshot(base_t)
        if not base:
            detail.append(f"Could not download the reference snapshot {base_t}.")
            R.append(f"| {name} | {base_t} | - | - | snapshot not available |")
            continue
        tier = top_tier(base)
        bview = org_view(base, tier)
        bq = {pk: n.get("quorumSetHashKey") for pk, n in ((n["publicKey"], n) for n in base.get("nodes") or [])}
        detail += [f"**Reference {base_t}** (snapshot {base.get('time')}): top tier {len(tier)} validators, "
                   f"{len(bview)} organizations.", "", f"Metrics: {stats_line(base)}", ""]
        bdown = [f"{o}: {', '.join(n for n, v, _ in vs if not v)}" for o, vs in sorted(bview.items())
                 if any(not v for _, v, _ in vs)]
        if bdown:
            detail += ["Already down beforehand: " + "; ".join(bdown), ""]

        for t in probes:
            net = snapshot(t)
            if not net:
                detail.append(f"**{t}**: snapshot not available.")
                R.append(f"| {name} | {t} | - | - | snapshot not available |")
                continue
            # use the top tier of the REFERENCE snapshot to see who disappeared; also record membership changes
            view = org_view(net, tier)
            now_tier = top_tier(net)
            nq = {n["publicKey"]: n.get("quorumSetHashKey") for n in net.get("nodes") or []}
            names = {n["publicKey"]: (n.get("name") or n["publicKey"][:8]) for n in
                     (base.get("nodes") or []) + (net.get("nodes") or [])}
            down_orgs, down_nodes, total = [], 0, 0
            lines = []
            for org, vs in sorted(view.items()):
                up = sum(1 for _, v, _ in vs if v)
                total += len(vs)
                down_nodes += len(vs) - up
                majority_lost = up * 2 <= len(vs)          # half or fewer left: the organization no longer has a majority
                flag = "  <-- MAJORITY LOST" if majority_lost else ""
                if majority_lost:
                    down_orgs.append(org)
                off = [n for n, v, _ in vs if not v]
                lines.append(f"- {org}: {up}/{len(vs)} validating"
                             + (f" (down: {', '.join(off)})" if off else "") + flag)
                rows.append([name, t, org, len(vs), up, "; ".join(off), "x" if majority_lost else ""])
            joined = sorted(names.get(pk, pk[:8]) for pk in now_tier - tier)
            left = sorted(names.get(pk, pk[:8]) for pk in tier - now_tier)
            qchanged = sorted(names.get(pk, pk[:8]) for pk in tier
                              if pk in nq and bq.get(pk) and nq[pk] and nq[pk] != bq[pk])

            frac = down_nodes / total if total else 0
            if len(down_orgs) == 0 and not (joined or left or qchanged):
                verdict = "no organization lost its majority and the configuration is unchanged: the drop is not explained by this snapshot"
            elif len(down_orgs) == 0:
                verdict = "no organization lost its majority; CONFIGURATION CHANGE (see details)"
            elif frac > 0.5:
                verdict = f"{len(down_orgs)} organizations 'down' at once ({frac:.0%} of validators): SUSPECTED CRAWLER OUTAGE"
            elif len(down_orgs) == 1:
                verdict = "real outage of 1 organization"
            else:
                verdict = f"real outage, {len(down_orgs)} organizations down simultaneously"
            R.append(f"| {name} | {t} | {', '.join(down_orgs) or '-'} | {down_nodes}/{total} | {verdict} |")

            detail += [f"**{t}** (snapshot {net.get('time')}): {verdict}", "", f"Metrics: {stats_line(net)}", ""] + lines
            if joined:
                detail.append(f"- Joined the transitive quorum set since the reference: {', '.join(joined)}")
            if left:
                detail.append(f"- Left the transitive quorum set since the reference: {', '.join(left)}")
            if qchanged:
                detail.append(f"- Top tier validators that CHANGED quorum set since the reference: {', '.join(qchanged)}")
            detail.append("")

    R += ["", "How to read the assessment column:",
          "- 'real outage of 1 organization': the kind of event the SDF reviewers suggested (contacting node operators preemptively).",
          "- 'SUSPECTED CRAWLER OUTAGE': more than half of the top tier validators down at once, unlikely to be a real outage; exclude from the analysis.",
          "- 'CONFIGURATION CHANGE': the margin dropped because a quorum set or the top tier membership changed, not because a node failed.",
          "- The top tier here is the transitive quorum set computed by Radar at the reference time (an approximation).", ""]
    with open(OUT / "cases.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["case", "time_utc", "organization", "validators", "validating", "validators_down", "majority_lost"])
        w.writerows(rows)
    (OUT / "report.md").write_text("\n".join(R + detail) + "\n", encoding="utf-8")
    (OUT / "run.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    print("\n" + "\n".join(R))
    print(f"Done. Report written to {OUT / 'report.md'}.")


if __name__ == "__main__":
    main()