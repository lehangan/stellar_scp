#!/usr/bin/env python3
"""
Daily availability of EVERY organization that was ever in the top tier (2019 -> today), and a
first scoring of early warning signals: lead time, precision and recall.

Why: so far daily availability was pulled only for Wirex and SatoshiPay, the two organizations
already known to have failed. A lead time measured that way says nothing about false alarms.
This script pulls the same data for all top tier organizations and scores three candidate
signals against two outcomes.

Steps
  1. Membership. One snapshot at the start of every stable configuration state listed in
     sdf_feasibility/full_scan/config_steps.csv (written by full_scan.py). From each snapshot:
     which organizations and validators were in the transitive quorum set. (~50 requests, cached)
  2. Daily availability. node and organization day-statistics for every validator and
     organization ever in the top tier, per calendar year. (~400 requests, cached)
  3. Signals and outcomes, per organization and day, counted only on days when the organization
     was in the top tier and the day is not a crawler outage day (half or more of the top tier
     organizations below 50% on the same day).
       S1  any validator below 90%, or the organization below 99%      (rule used so far)
       S2  the organization below 99% on at least 3 of the trailing 7 days
       S3  any validator at 10% or less for the whole day, or the organization below 90%
     Outcomes:
       OUTAGE   the organization below 50% for a day while in the top tier
       REMOVAL  the organization leaves the top tier (last day of membership, if before data end)
     Signal days are merged into episodes (gap of 7 days or less). For each signal and each
     window W in {30, 90, 180, 365} days: precision = share of episodes followed by an outcome of
     that organization within W days; recall = share of outcomes preceded by an episode within W
     days; lead time = days from the first such episode to the outcome.

Run:    python tier1_availability.py            from the directory that contains sdf_feasibility/
        python tier1_availability.py --offline  use only cached files (no network), for testing
Output: sdf_feasibility/availability/report.md, membership.csv, availability_daily.csv,
        episodes.csv, run.log
Standard library only. A second run reuses everything already downloaded.
"""

import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = "https://radar.withobsrvr.com/api"
STEPS = Path("sdf_feasibility") / "full_scan" / "config_steps.csv"
SNAP = Path("sdf_feasibility") / "verify" / "raw"          # snapshot cache shared with verify_case.py
MECH = Path("sdf_feasibility") / "mechanism" / "raw"       # day statistics already pulled for Wirex and SatoshiPay
OUT = Path("sdf_feasibility") / "availability"
RAW = OUT / "raw"
TIMEOUT = 120
FIRST_DAY = "2019-05-31"
END_DAY = None                                             # None = today (UTC)
WINDOWS = (30, 90, 180, 365)
EPISODE_GAP_DAYS = 7
OFFLINE = "--offline" in sys.argv

LOG = []


def log(m):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {m}"
    print(line, flush=True)
    LOG.append(line)


def get(url):
    if OFFLINE:
        return 0, None
    req = urllib.request.Request(url, headers={
        "User-Agent": "hust-fbas-research/0.6 (academic feasibility check)", "Accept": "application/json"})
    last = None
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
        time.sleep(5 * (attempt + 1))
    log(f"ERROR {last}  {url}")
    return 0, None


# ------------------------------------------------------------------ step 1: membership

def snapshot(t):
    """t = 'YYYY-MM-DDTHH:MM' (UTC). Cached in the shared snapshot directory."""
    f = SNAP / ("snap_" + t.replace(":", "") + ".json")
    if f.exists():
        try:
            return json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            pass
    status, data = get(f"{BASE}/v1?{urllib.parse.urlencode({'at': t + ':00.000Z'})}")
    time.sleep(0.5)
    if isinstance(data, dict) and "nodes" in data:
        f.write_text(json.dumps(data), encoding="utf-8")
        log(f"downloaded snapshot {t} -> {data.get('time')}")
        return data
    log(f"could NOT download snapshot {t} (HTTP {status})")
    return None


def walk(q, acc):
    if isinstance(q, dict):
        acc.update(q.get("validators") or [])
        for i in q.get("innerQuorumSets") or []:
            walk(i, acc)


def top_tier(net):
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
        if pk not in seen:
            seen.add(pk)
            acc = set()
            walk(nodes.get(pk, {}).get("quorumSet"), acc)
            todo.extend(acc - seen)
    return seen


def step_times():
    """Snapshot times: the start of every stable configuration state (plus the data end)."""
    if OFFLINE or not STEPS.exists():
        times = sorted(f.name[5:-5] for f in SNAP.glob("snap_*.json"))
        return [t[:11] + t[11:13] + ":" + t[13:15] for t in times]
    ts = []
    with open(STEPS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = datetime.fromisoformat(r["start"].replace("Z", "+00:00")) + timedelta(minutes=10)
            ts.append(d.strftime("%Y-%m-%dT%H:%M"))
    return ts


def membership():
    """-> orgs: {org_id: {"name", "validators": {pk: name}, "days": set of 'YYYY-MM-DD'}}"""
    times = step_times()
    log(f"{len(times)} snapshot times for membership")
    orgs, samples = {}, []
    for t in times:
        net = snapshot(t)
        if not net:
            continue
        tier = top_tier(net)
        nodes = {n["publicKey"]: n for n in net.get("nodes") or []}
        onames = {o.get("id"): (o.get("name") or o.get("homeDomain") or str(o.get("id"))[:8])
                  for o in net.get("organizations") or []}
        present = {}
        for pk in tier:
            n = nodes.get(pk)
            if not n:
                continue
            oid = n.get("organizationId") or ("node:" + pk)
            o = orgs.setdefault(oid, {"name": onames.get(oid, oid[:8]), "validators": {}, "days": set()})
            o["name"] = onames.get(oid, o["name"])
            o["validators"][pk] = n.get("name") or pk[:8]
            present[oid] = True
        samples.append((t[:10], set(present)))
    # membership days: an organization is in the top tier from one sample to the next
    samples.sort()
    end = datetime.strptime(END_DAY or datetime.now(timezone.utc).strftime("%Y-%m-%d"), "%Y-%m-%d")
    for i, (d, present) in enumerate(samples):
        d0 = datetime.strptime(d, "%Y-%m-%d")
        d1 = datetime.strptime(samples[i + 1][0], "%Y-%m-%d") if i + 1 < len(samples) else end + timedelta(days=1)
        cur = d0
        while cur < d1:
            for oid in present:
                orgs[oid]["days"].add(cur.strftime("%Y-%m-%d"))
            cur += timedelta(days=1)
    return orgs, samples


# ------------------------------------------------------------------ step 2: daily availability

def day_stats(kind, ident, year):
    """Daily records of one node or organization for one calendar year. Cached per year;
    falls back to the files mechanism_analysis.py already downloaded (any date range)."""
    f = RAW / f"{kind}_{ident[:12]}_{year}.json"
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    for g in MECH.glob(f"{kind}_{ident[:12]}_*.json"):
        try:
            data = [r for r in json.loads(g.read_text(encoding="utf-8")) if str(r.get("time", ""))[:4] == str(year)]
        except Exception:
            data = []
        if data:
            return data
    d1, d2 = f"{year}-01-01", f"{year + 1}-01-01"
    q = urllib.parse.urlencode({"from": d1 + "T00:00:00.000Z", "to": d2 + "T00:00:00.000Z"})
    status, data = get(f"{BASE}/v1/{kind}/{urllib.parse.quote(ident)}/day-statistics?{q}")
    time.sleep(0.4)
    if isinstance(data, list):
        f.write_text(json.dumps(data), encoding="utf-8")
        return data
    if not OFFLINE:
        log(f"could NOT download day-statistics {kind} {ident[:12]} {year} (HTTP {status})")
    return []


def ratio(rec, key):
    c = rec.get("crawlCount") or 0
    return (rec.get(key) or 0) / c if c else None


def pull_availability(orgs):
    end = END_DAY or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    years = range(int(FIRST_DAY[:4]), int(end[:4]) + 1)
    node_av, org_av = {}, {}       # node_av[pk][day] = ratio ; org_av[oid][day] = ratio
    todo = sum(len(o["validators"]) + 1 for o in orgs.values()) * len(years)
    log(f"pulling daily availability: about {todo} year-chunks (cached ones are instant)")
    for oid, o in orgs.items():
        if oid.startswith("node:"):
            continue
        for y in years:
            for r in day_stats("organization", oid, y):
                org_av.setdefault(oid, {})[str(r.get("time"))[:10]] = ratio(r, "isSubQuorumAvailableCount")
        for pk in o["validators"]:
            for y in years:
                for r in day_stats("node", pk, y):
                    node_av.setdefault(pk, {})[str(r.get("time"))[:10]] = ratio(r, "isValidatingCount")
    return node_av, org_av


# ------------------------------------------------------------------ step 3: signals and outcomes

def daterange(d1, d2):
    cur = datetime.strptime(d1, "%Y-%m-%d")
    stop = datetime.strptime(d2, "%Y-%m-%d")
    while cur <= stop:
        yield cur.strftime("%Y-%m-%d")
        cur += timedelta(days=1)


def days_between(a, b):
    return (datetime.strptime(b, "%Y-%m-%d") - datetime.strptime(a, "%Y-%m-%d")).days


def build_table(orgs, node_av, org_av):
    """-> rows per (org, day in top tier): dict with org availability, min validator availability, signals."""
    end = END_DAY or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    table = {}
    for oid, o in orgs.items():
        if oid.startswith("node:") or not o["days"]:
            continue
        hist = []
        for d in daterange(min(o["days"]), min(max(o["days"]), end)):
            if d not in o["days"]:
                continue
            oa = org_av.get(oid, {}).get(d)
            vs = [node_av.get(pk, {}).get(d) for pk in o["validators"]]
            vs = [v for v in vs if v is not None]
            mn = min(vs) if vs else None
            hist.append(oa)
            trailing = [x for x in hist[-7:] if x is not None]
            s1 = (mn is not None and mn < 0.90) or (oa is not None and oa < 0.99)
            s2 = sum(1 for x in trailing if x < 0.99) >= 3
            s3 = (mn is not None and mn <= 0.10) or (oa is not None and oa < 0.90)
            table[(oid, d)] = {"org": oa, "min_val": mn, "n_val": len(vs), "S1": s1, "S2": s2, "S3": s3}
    return table


def crawler_days(table, orgs):
    """Days on which half or more of the top tier organizations were below 50%: measurement problem."""
    per_day = {}
    for (oid, d), r in table.items():
        per_day.setdefault(d, []).append(r["org"])
    bad = set()
    for d, xs in per_day.items():
        known = [x for x in xs if x is not None]
        if known and sum(1 for x in known if x < 0.5) * 2 >= len(known) and len(known) >= 3:
            bad.add(d)
    return bad


def outcomes(table, orgs, bad_days):
    """-> {oid: [(day, kind)]} with kind OUTAGE or REMOVAL."""
    end = END_DAY or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    res = {}
    for oid, o in orgs.items():
        if oid.startswith("node:") or not o["days"]:
            continue
        ev = []
        prev_out = None
        for d in sorted(o["days"]):
            r = table.get((oid, d))
            if not r or d in bad_days or r["org"] is None:
                continue
            if r["org"] < 0.5:
                if prev_out is None or days_between(prev_out, d) > EPISODE_GAP_DAYS:
                    ev.append((d, "OUTAGE"))
                prev_out = d
        last = max(o["days"])
        if days_between(last, end) > 3:
            ev.append((last, "REMOVAL"))
        res[oid] = ev
    return res


def episodes(table, bad_days, signal):
    """-> {oid: [(start_day, end_day, n_days)]}"""
    res = {}
    for (oid, d), r in sorted(table.items()):
        if not r[signal] or d in bad_days:
            continue
        eps = res.setdefault(oid, [])
        if eps and days_between(eps[-1][1], d) <= EPISODE_GAP_DAYS:
            eps[-1] = (eps[-1][0], d, eps[-1][2] + 1)
        else:
            eps.append((d, d, 1))
    return res


def score(eps, outs, W):
    """precision, recall, lead times for window W (days)."""
    n_ep = tp = 0
    for oid, lst in eps.items():
        for s, e, n in lst:
            n_ep += 1
            if any(0 <= days_between(s, od) <= W for od, _ in outs.get(oid, [])):
                tp += 1
    n_out = hit = 0
    leads = []
    for oid, lst in outs.items():
        for od, kind in lst:
            n_out += 1
            prior = [s for s, e, n in eps.get(oid, []) if 0 <= days_between(s, od) <= W]
            if prior:
                hit += 1
                leads.append(days_between(min(prior), od))
    prec = tp / n_ep if n_ep else None
    rec = hit / n_out if n_out else None
    return n_ep, tp, prec, n_out, hit, rec, leads


def pct(x):
    return "-" if x is None else f"{100 * x:.0f}%"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    SNAP.mkdir(parents=True, exist_ok=True)

    orgs, samples = membership()
    real = {k: v for k, v in orgs.items() if not k.startswith("node:")}
    log(f"{len(real)} organizations ever in the top tier")
    with open(OUT / "membership.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["org_id", "name", "first_day", "last_day", "days_in_top_tier", "validators"])
        for oid, o in sorted(real.items(), key=lambda kv: min(kv[1]["days"]) if kv[1]["days"] else ""):
            if o["days"]:
                w.writerow([oid, o["name"], min(o["days"]), max(o["days"]), len(o["days"]),
                            "; ".join(sorted(o["validators"].values()))])

    node_av, org_av = pull_availability(real)
    table = build_table(real, node_av, org_av)
    bad = crawler_days(table, real)
    outs = outcomes(table, real, bad)
    log(f"{len(table)} organization-days, {len(bad)} crawler outage days excluded")

    with open(OUT / "availability_daily.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "organization", "org_available", "min_validator_validating", "validators_with_data",
                    "S1", "S2", "S3", "crawler_day"])
        for (oid, d), r in sorted(table.items(), key=lambda kv: (kv[0][1], real[kv[0][0]]["name"])):
            w.writerow([d, real[oid]["name"], "" if r["org"] is None else round(r["org"], 4),
                        "" if r["min_val"] is None else round(r["min_val"], 4), r["n_val"],
                        int(r["S1"]), int(r["S2"]), int(r["S3"]), int(d in bad)])

    R = ["# Daily availability of all top tier organizations and early warning scoring", "",
         f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M')}" + ("  (OFFLINE: cached files only)" if OFFLINE else ""), "",
         f"{len(real)} organizations were in the top tier at some point; {len(samples)} membership samples; "
         f"{len(table)} organization-days; {len(bad)} crawler outage days excluded.", "",
         "## Organizations", "", "| Organization | In top tier | Days | Validators | Outage days | Outcomes |", "|---|---|---|---|---|---|"]
    for oid, o in sorted(real.items(), key=lambda kv: min(kv[1]["days"]) if kv[1]["days"] else ""):
        if not o["days"]:
            continue
        od = sum(1 for d in o["days"] if table.get((oid, d), {}).get("org") is not None
                 and table[(oid, d)]["org"] < 0.5 and d not in bad)
        ev = "; ".join(f"{k} {d}" for d, k in outs.get(oid, [])) or "none"
        R.append(f"| {o['name']} | {min(o['days'])} to {max(o['days'])} | {len(o['days'])} | {len(o['validators'])} | {od} | {ev} |")

    R += ["", "## Scoring of the three signals", "",
          "Precision: share of signal episodes followed by an outage or removal of the same organization within W days. "
          "Recall: share of outcomes preceded by a signal episode within W days. Lead time: days from the first such episode to the outcome.", ""]
    ep_rows = []
    for sig, desc in (("S1", "any validator < 90% or organization < 99%"),
                      ("S2", "organization < 99% on 3 of the trailing 7 days"),
                      ("S3", "a validator at <= 10% for a day or organization < 90%")):
        eps = episodes(table, bad, sig)
        n_eps = sum(len(v) for v in eps.values())
        R += [f"### {sig}: {desc}", "", f"{n_eps} episodes across {len(eps)} organizations.", "",
              "| Window W | Episodes | Followed by outcome | Precision | Outcomes | Preceded by episode | Recall | Lead time (days, median / min / max) |",
              "|---|---|---|---|---|---|---|---|"]
        for W in WINDOWS:
            n_ep, tp, prec, n_out, hit, rec, leads = score(eps, outs, W)
            lt = "-"
            if leads:
                s = sorted(leads)
                lt = f"{s[len(s) // 2]} / {s[0]} / {s[-1]}"
            R.append(f"| {W} | {n_ep} | {tp} | {pct(prec)} | {n_out} | {hit} | {pct(rec)} | {lt} |")
        R.append("")
        for oid, lst in eps.items():
            for s, e, n in lst:
                nxt = [od for od, _ in outs.get(oid, []) if days_between(s, od) >= 0]
                ep_rows.append([sig, real[oid]["name"], s, e, n, min(nxt) if nxt else "", days_between(s, min(nxt)) if nxt else ""])

    R += ["## Outcomes", "", "| Organization | Date | Kind |", "|---|---|---|"]
    for oid, lst in sorted(outs.items(), key=lambda kv: real[kv[0]]["name"]):
        for d, k in lst:
            R.append(f"| {real[oid]['name']} | {d} | {k} |")
    R += ["", "## Notes", "",
          "- Membership is sampled once per stable configuration state, so an organization that joined and left between two samples is missed.",
          "- A REMOVAL is counted whenever an organization's last membership day is more than 3 days before the data end, whatever the reason "
          "(failure, voluntary exit, or a change of organization id in Radar). Check each against membership.csv.",
          "- Organization availability is Radar's isSubQuorumAvailableCount / crawlCount; validator availability is isValidatingCount / crawlCount.",
          "- Thresholds (90%, 99%, 10%, 50%, 7 day gap) are starting points. The proposal should report the score of the rule finally chosen, "
          "with thresholds picked on 2019-2023 and tested on 2024-2026.", ""]
    with open(OUT / "episodes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["signal", "organization", "episode_start", "episode_end", "signal_days", "next_outcome", "days_to_outcome"])
        w.writerows(ep_rows)
    (OUT / "report.md").write_text("\n".join(R) + "\n", encoding="utf-8")
    (OUT / "run.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    print("\n" + "\n".join(R[:60]))
    print(f"\nDone. Report written to {OUT / 'report.md'}.")


if __name__ == "__main__":
    main()
