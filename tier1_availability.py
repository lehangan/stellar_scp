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
     Outcomes (one list, used for every signal):
       OUTAGE   a verified organization outage of one hour or more, from verify_case.py / verify/report.md
                (listed in VERIFIED_OUTAGES below)
       REMOVAL  the organization leaves the top tier (last day of membership, if before data end)
       Outcomes of one organization closer than 7 days are merged into one.
     Signal days are merged into episodes (gap of 7 days or less). Each episode is classified against
     the outcomes of its organization within a window W: WARNING if an outcome follows between 7 and W
     days later; INCIDENT if an outcome falls within a day before to 7 days after the episode start
     (the episode is the incident itself or too late to help); FALSE ALARM otherwise.
       precision = WARNING / (WARNING + FALSE ALARM)
       recall    = share of outcomes preceded by a WARNING episode
       lead time = days from the earliest WARNING episode to the outcome
     Validators are dropped from the computation after their last day with any validating time
     (retired validators that stay listed in quorum sets would otherwise read as 0% forever).

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
WINDOWS = (180, 365)
EPISODE_GAP_DAYS = 7
MIN_LEAD = 7                                               # an episode counts as EARLY warning only if it starts this many days before the outcome
# Verified organization outages of one hour or more (verify/report.md): (organization name contains, day)
VERIFIED_OUTAGES = [
    ("Stellar Development Foundation", "2020-04-23"), ("Stellar Development Foundation", "2020-05-10"),
    ("Stellar Development Foundation", "2021-04-06"), ("LOBSTR", "2021-04-06"),
    ("Wirex", "2022-07-13"), ("Wirex", "2022-07-26"), ("Wirex", "2022-12-13"),
    ("SatoshiPay", "2020-05-31"), ("SatoshiPay", "2021-09-01"), ("SatoshiPay", "2021-10-13"),
    ("SatoshiPay", "2024-02-14"), ("SatoshiPay", "2025-02-18"), ("SatoshiPay", "2025-02-25"),
    ("SatoshiPay", "2025-02-26"), ("SatoshiPay", "2025-08-22"),
]
MIN_DAYS = 30                                              # organizations in the top tier for fewer days are transient and not scored
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
    """-> orgs: {org_id: {"name", "validators": {pk: name}, "days": set of 'YYYY-MM-DD'}}
    Organizations that share a validator public key (renamed organizations, mis-attributed validators)
    are merged into one record."""
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
            o = orgs.setdefault(oid, {"name": onames.get(oid, oid[:8]), "validators": {}, "days": set(), "day_pks": {}})
            o["name"] = onames.get(oid, o["name"])
            o["validators"][pk] = n.get("name") or pk[:8]
            present.setdefault(oid, set()).add(pk)
        samples.append((t, present))
    samples.sort(key=lambda x: x[0])
    # merge organizations that share a validator (same organization under a new id or name)
    parent = {oid: oid for oid in orgs}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    owner = {}
    for oid, o in orgs.items():
        for pk in o["validators"]:
            if pk in owner and find(owner[pk]) != find(oid):
                parent[find(owner[pk])] = find(oid)
            owner[pk] = oid
    # the representative of a group is the real organization id seen most recently (never a node: id)
    groups = {}
    for oid in orgs:
        groups.setdefault(find(oid), []).append(oid)
    last_seen = {}
    for t, present in samples:
        for oid in present:
            last_seen[oid] = t
    rep = {}
    for root, ids in groups.items():
        realids = [i for i in ids if not i.startswith("node:")]
        key = max(realids, key=lambda i: last_seen.get(i, "")) if realids else root
        for i in ids:
            rep[i] = key
    merged = {}
    for oid, o in orgs.items():
        key = rep[oid]
        m = merged.setdefault(key, {"name": orgs[key]["name"], "validators": {}, "days": set(), "day_pks": {}, "ids": []})
        m["validators"].update(o["validators"])
        m["ids"].append(oid)
    msamples = []
    for t, present in samples:
        mp = {}
        for oid, pks in present.items():
            mp.setdefault(rep[oid], set()).update(pks)
        msamples.append((t, mp))
    samples = msamples
    for key, m in merged.items():
        names = [orgs[i]["name"] for i in m["ids"] if not i.startswith("node:")]
        m["aliases"] = sorted(set(names) - {m["name"]})
    # membership days: a day belongs to the latest sample taken at or before the end of that day
    end = datetime.strptime(END_DAY or datetime.now(timezone.utc).strftime("%Y-%m-%d"), "%Y-%m-%d")
    first = datetime.strptime(samples[0][0][:10], "%Y-%m-%d")
    cur, i = first, 0
    while cur <= end:
        day_end = cur.strftime("%Y-%m-%dT23:59")
        while i + 1 < len(samples) and samples[i + 1][0] <= day_end:
            i += 1
        for root, pks in samples[i][1].items():
            d = cur.strftime("%Y-%m-%d")
            merged[root]["days"].add(d)
            merged[root]["day_pks"][d] = pks
        cur += timedelta(days=1)
    return merged, samples


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
        for src in o.get("ids", [oid]):
            if src.startswith("node:"):
                continue
            for y in years:
                for r in day_stats("organization", src, y):
                    d, v = str(r.get("time"))[:10], ratio(r, "isSubQuorumAvailableCount")
                    cur = org_av.setdefault(oid, {}).get(d)
                    if v is not None and (cur is None or v > cur):
                        org_av[oid][d] = v
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
    last_up = {}                      # last day on which the validator validated at all
    for pk, days in node_av.items():
        ups = [d for d, v in days.items() if v]
        last_up[pk] = max(ups) if ups else None
    table = {}
    for oid, o in orgs.items():
        if oid.startswith("node:") or len(o["days"]) < MIN_DAYS:
            continue
        hist = []
        for d in daterange(min(o["days"]), min(max(o["days"]), end)):
            if d not in o["days"]:
                continue
            oa = org_av.get(oid, {}).get(d)
            vs = [node_av.get(pk, {}).get(d) for pk in o.get("day_pks", {}).get(d, o["validators"])
                  if last_up.get(pk) is not None and d <= last_up[pk]]
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
    """-> {oid: [(day, kind)]}: verified outages of an hour or more plus removals, merged within 7 days."""
    end = END_DAY or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    res = {}
    for oid, o in orgs.items():
        if oid.startswith("node:") or len(o["days"]) < MIN_DAYS:
            continue
        ev = [(d, "OUTAGE") for name, d in VERIFIED_OUTAGES if name.lower() in o["name"].lower()]
        last = max(o["days"])
        if days_between(last, end) > 3:
            ev.append((last, "REMOVAL"))
        ev.sort()
        merged, last_d = [], None
        for d, k in ev:
            if merged and days_between(last_d, d) <= EPISODE_GAP_DAYS:
                if k not in merged[-1][1]:
                    merged[-1] = (merged[-1][0], merged[-1][1] + "+" + k)
            else:
                merged.append((d, k))
            last_d = d
        res[oid] = merged
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


def classify(eps, outs, W):
    """-> {(oid, start): 'WARNING' | 'INCIDENT' | 'FALSE ALARM'} for window W."""
    cls = {}
    for oid, lst in eps.items():
        for st, e, n in lst:
            gaps = [days_between(st, od) for od, _ in outs.get(oid, [])]
            if any(MIN_LEAD <= g <= W for g in gaps):
                cls[(oid, st)] = "WARNING"
            elif any(-1 <= g < MIN_LEAD for g in gaps):
                cls[(oid, st)] = "INCIDENT"
            else:
                cls[(oid, st)] = "FALSE ALARM"
    return cls


def score(eps, outs, W):
    """precision over warning and false alarm episodes, recall over outcomes, lead times from the earliest warning."""
    cls = classify(eps, outs, W)
    warn = sum(1 for v in cls.values() if v == "WARNING")
    inc = sum(1 for v in cls.values() if v == "INCIDENT")
    fa = sum(1 for v in cls.values() if v == "FALSE ALARM")
    n_out = hit = 0
    leads = []
    for oid, lst in outs.items():
        for od, kind in lst:
            n_out += 1
            prior = [st for st, e, n in eps.get(oid, []) if MIN_LEAD <= days_between(st, od) <= W]
            if prior:
                hit += 1
                leads.append(days_between(min(prior), od))
    prec = warn / (warn + fa) if (warn + fa) else None
    rec = hit / n_out if n_out else None
    return warn, inc, fa, prec, n_out, hit, rec, leads


def pct(x):
    return "-" if x is None else f"{100 * x:.0f}%"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    SNAP.mkdir(parents=True, exist_ok=True)

    orgs, samples = membership()
    real = {k: v for k, v in orgs.items() if not k.startswith("node:") and v["days"]}
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
         "## Organizations", "", "| Organization | In top tier | Days | Validators | Verified outages | Outcomes (merged) |", "|---|---|---|---|---|---|"]
    for oid, o in sorted(real.items(), key=lambda kv: min(kv[1]["days"]) if kv[1]["days"] else ""):
        if not o["days"]:
            continue
        od = sum(1 for name, d in VERIFIED_OUTAGES if name.lower() in o["name"].lower())
        ev = "; ".join(f"{k} {d}" for d, k in outs.get(oid, [])) or "none"
        nm = o["name"] + (f" (also {', '.join(o.get('aliases', []))})" if o.get("aliases") else "")
        if len(o["days"]) < MIN_DAYS:
            ev = "transient, not scored"
        R.append(f"| {nm} | {min(o['days'])} to {max(o['days'])} | {len(o['days'])} | {len(o['validators'])} | {od} | {ev} |")

    R += ["", "## Scoring of the three signals", "",
          "An episode is a WARNING if an outcome of the same organization follows between 7 and W days later, an INCIDENT if an outcome "
          "falls within a day before to 7 days after its start (the episode is the incident itself or too late to help), and a FALSE ALARM otherwise. "
          "Precision = warnings / (warnings + false alarms). Recall = outcomes preceded by a warning. Lead time from the earliest warning.", ""]
    ep_rows = []
    for sig, desc in (("S1", "any validator < 90% or organization < 99%"),
                      ("S2", "organization < 99% on 3 of the trailing 7 days"),
                      ("S3", "a validator at <= 10% for a day or organization < 90%")):
        eps = episodes(table, bad, sig)
        n_eps = sum(len(v) for v in eps.values())
        R += [f"### {sig}: {desc}", "", f"{n_eps} episodes across {len(eps)} organizations.", "",
              "| Window W | Warning | Incident (within a day before to 7 days after) | False alarm | Precision | Outcomes | Preceded by a warning | Recall | Lead time (days, median / min / max) |",
              "|---|---|---|---|---|---|---|---|---|"]
        for W in WINDOWS:
            warn, inc, fa, prec, n_out, hit, rec, leads = score(eps, outs, W)
            lt = "-"
            if leads:
                s = sorted(leads)
                lt = f"{s[len(s) // 2]} / {s[0]} / {s[-1]}"
            R.append(f"| {W} | {warn} | {inc} | {fa} | {pct(prec)} | {n_out} | {hit} | {pct(rec)} | {lt} |")
        R.append("")
        cls = classify(eps, outs, 365)
        for oid, lst in eps.items():
            for s, e, n in lst:
                nxt = [od for od, _ in outs.get(oid, []) if days_between(s, od) >= -1]
                ep_rows.append([sig, real[oid]["name"], s, e, n, min(nxt) if nxt else "", days_between(s, min(nxt)) if nxt else "", cls[(oid, s)]])

    R += ["## Outcomes and the earliest signal before each (within 365 days)", "",
          "| Organization | Date | Kind | S1 first signal, lead days | S3 first signal, lead days |", "|---|---|---|---|---|"]
    eps1, eps3 = episodes(table, bad, "S1"), episodes(table, bad, "S3")
    for oid, lst in sorted(outs.items(), key=lambda kv: real[kv[0]]["name"]):
        for d, k in lst:
            cells = []
            for eps in (eps1, eps3):
                prior = [st for st, e, n in eps.get(oid, []) if 0 <= days_between(st, d) <= 365]
                cells.append(f"{min(prior)}, {days_between(min(prior), d)}" if prior else "none")
            R.append(f"| {real[oid]['name']} | {d} | {k} | {cells[0]} | {cells[1]} |")
    R += ["", "## Notes", "",
          "- Membership is sampled once per stable configuration state, so an organization that joined and left between two samples is missed.",
          "- A REMOVAL is counted whenever an organization's last membership day is more than 3 days before the data end, whatever the reason "
          "(failure or voluntary exit). Organizations that share a validator key are merged, so a change of organization id is not a removal.",
          "- Organization availability is Radar's isSubQuorumAvailableCount / crawlCount; validator availability is isValidatingCount / crawlCount.",
          "- Thresholds (90%, 99%, 10%, 7 day gap, 7 day minimum lead) are starting points. The proposal should report the score of the rule finally chosen, "
          "with thresholds picked on 2019-2023 and tested on 2024-2026.", ""]
    with open(OUT / "episodes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["signal", "organization", "episode_start", "episode_end", "signal_days", "next_outcome", "days_to_outcome", "class_at_365_days"])
        w.writerows(ep_rows)
    (OUT / "report.md").write_text("\n".join(R) + "\n", encoding="utf-8")
    (OUT / "run.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    print("\n" + "\n".join(R[:60]))
    print(f"\nDone. Report written to {OUT / 'report.md'}.")


if __name__ == "__main__":
    main()
