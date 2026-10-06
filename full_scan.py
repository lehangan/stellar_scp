#!/usr/bin/env python3
"""
Scan the full history of the Stellar network (May 2019 -> today) to answer two questions:

  A. Did any configuration change pass through an INTERMEDIATE STATE WEAKER than both
     its starting and its final configuration?
     (motivation for the "safe reconfiguration" direction)
  B. How many periods of THIN LIVENESS MARGIN lasted >= 1 hour, and did the margin ever
     drop to <= 1?
     (motivation for the "early warning" direction)

Run:    python full_scan.py
Place it in the same directory as the earlier scripts. Days already downloaded are reused.
The first run takes about 15-40 minutes (~2,700 days of data). If interrupted, run it
again and it resumes where it stopped.

Output in ./sdf_feasibility/full_scan/
  report.md                 read this first; the VERDICT is at the top
  config_steps.csv          every stable configuration state over the seven years
  reconfig_episodes.csv     reconfiguration episodes (transitions close in time, grouped)
  thin_margin.csv           every thin margin period >= 15 minutes
  no_quorum_intersection.csv
  run.log
Standard library only.
"""

import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ----------------------------- CONFIGURATION -----------------------------

BASE = "https://radar.withobsrvr.com/api"
START = "2019-05-20"
END = "2026-10-02"               # None = today
RAW = Path("sdf_feasibility") / "events" / "raw"     # cache shared with the earlier script
OUT = Path("sdf_feasibility") / "full_scan"

THREADS = 3                     # parallel requests (kept low to be polite)
TIMEOUT = 120

CFG = ["topTierSize", "topTierOrgsSize", "minBlockingSetSize",
       "minBlockingSetOrgsSize", "minSplittingSetSize", "minSplittingSetOrgsSize"]
RESILIENCE = ["minBlockingSetSize", "minBlockingSetOrgsSize",
              "minSplittingSetSize", "minSplittingSetOrgsSize"]
REAL, NOMINAL = "minBlockingSetOrgsFilteredSize", "minBlockingSetOrgsSize"

MIN_STEP_SCANS = 5              # states shorter than this many scans are treated as noise
EPISODE_QUIET_DAYS = 14         # transitions closer than this many days belong to the same reconfiguration episode
GAP_MINUTES = 30                # thin margin periods closer than this are merged into one
THIN_MIN_MINUTES = 15           # only thin margin periods at least this long are written out

# Thresholds of the stopping rule
RULE_WEAK_TRANSITIONS = 1       # >= 1 reconfiguration episode with a weak intermediate state lasting >= 1 hour
RULE_MARGIN1_MINUTES = 60       # or >= 1 period with effective margin <= 1 lasting >= 60 minutes

# --------------------------------------------------------------------

LOG = []


def log(msg):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    LOG.append(line)


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "hust-fbas-research/0.3 (academic feasibility check)",
        "Accept": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.status, json.loads(r.read().decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            return e.code, None
        except Exception:
            if attempt < 3:
                time.sleep(10 * (attempt + 1))
                continue
            return 0, None
    return 0, None


def pt(s):
    return datetime.fromisoformat(str(s).replace("Z", "+00:00"))


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def dur(minutes):
    if minutes < 60:
        return f"{minutes:.0f} min"
    if minutes < 1440:
        return f"{minutes / 60:.1f} h"
    return f"{minutes / 1440:.1f} days"


def minutes_between(a, b):
    return (pt(b) - pt(a)).total_seconds() / 60


# ------------------------- download -------------------------

def download_day(day):
    f = RAW / f"stats_{day.strftime('%Y-%m-%d')}.json"
    if f.exists():
        return day, True
    q = urllib.parse.urlencode({"from": iso(day), "to": iso(day + timedelta(days=1))})
    status, data = fetch(f"{BASE}/v1/statistics?{q}")
    if isinstance(data, list):
        f.write_text(json.dumps(data), encoding="utf-8")
        return day, True
    LOG.append(f"download ERROR {day.strftime('%Y-%m-%d')}: HTTP {status}")
    return day, False


def download_all(days):
    todo = [d for d in days if not (RAW / f"stats_{d.strftime('%Y-%m-%d')}.json").exists()]
    log(f"{len(days)} days in total, {len(days) - len(todo)} already cached, {len(todo)} to download")
    failed, done, t0 = [], 0, time.time()
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for day, ok in ex.map(download_day, todo):
            done += 1
            if not ok:
                failed.append(day.strftime("%Y-%m-%d"))
            if done % 100 == 0 or done == len(todo):
                rate = done / max(time.time() - t0, 1)
                left = (len(todo) - done) / max(rate, 0.01) / 60
                log(f"  downloaded {done}/{len(todo)} days, {len(failed)} failed, about {left:.0f} min left")
    return failed


def load_all(days):
    """Returns a list of compact tuples: (time, cfg..., real, nominal, qi). Failed scans are dropped."""
    rows, total, seen_last = [], 0, ""
    for d in days:
        f = RAW / f"stats_{d.strftime('%Y-%m-%d')}.json"
        if not f.exists():
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        data = [r for r in data if isinstance(r, dict) and r.get("time")]
        data.sort(key=lambda r: r["time"])
        for r in data:
            total += 1
            if r["time"] <= seen_last:
                continue
            seen_last = r["time"]
            tt = r.get("topTierSize")
            if not isinstance(tt, (int, float)) or tt <= 0:
                continue
            rows.append((r["time"],) + tuple(r.get(k) for k in CFG)
                        + (r.get(REAL), r.get(NOMINAL), r.get("hasQuorumIntersection")))
    return rows, total


# ------------------------- analysis -------------------------

NC = len(CFG)


def config_steps(rows):
    segs = []
    for r in rows:
        key = r[1:1 + NC]
        if segs and segs[-1]["key"] == key:
            segs[-1]["end"] = r[0]
            segs[-1]["n"] += 1
        else:
            segs.append({"key": key, "start": r[0], "end": r[0], "n": 1})
    noise = [s for s in segs if s["n"] < MIN_STEP_SCANS]
    kept = []
    for s in segs:
        if s["n"] < MIN_STEP_SCANS:
            continue
        if kept and kept[-1]["key"] == s["key"]:
            kept[-1]["end"] = s["end"]
            kept[-1]["n"] += s["n"]
        else:
            kept.append(dict(s))
    return kept, len(noise)


def reconfig_episodes(steps):
    """Group transitions that are close in time. Each episode: the starting state (stable before),
    the intermediate states, and the final state (stable after)."""
    eps, i = [], 0
    quiet = EPISODE_QUIET_DAYS * 1440
    while i < len(steps) - 1:
        j = i + 1
        # extend the episode until a state that stays stable long enough (or the data ends)
        while j < len(steps) - 1 and minutes_between(steps[j]["start"], steps[j]["end"]) < quiet:
            j += 1
        first, last, mid = steps[i], steps[j], steps[i + 1:j]
        weak = []
        for m in mid:
            for k in RESILIENCE:
                idx = CFG.index(k)
                a, b, v = first["key"][idx], last["key"][idx], m["key"][idx]
                if None in (a, b, v):
                    continue
                if v < min(a, b):
                    weak.append({"metric": k, "value": v, "from": a, "to": b,
                                 "start": m["start"], "minutes": minutes_between(m["start"], m["end"]) + 5})
        eps.append({"start": steps[i + 1]["start"], "end": last["start"], "first": first["key"],
                    "last": last["key"], "n_mid": len(mid), "weak": weak,
                    "weak_minutes": max((w["minutes"] for w in weak), default=0)})
        i = j
    return eps


def thin_margin(rows):
    raw, cur = [], None
    for r in rows:
        t, real, nom = r[0], r[1 + NC], r[2 + NC]
        thin = isinstance(real, (int, float)) and isinstance(nom, (int, float)) and real < nom
        if thin:
            if cur is None:
                cur = {"start": t, "end": t, "n": 0, "min_real": real, "nominal": nom}
            cur["end"] = t
            cur["n"] += 1
            cur["min_real"] = min(cur["min_real"], real)
        elif cur:
            raw.append(cur)
            cur = None
    if cur:
        raw.append(cur)
    merged = []
    for e in raw:      # merge periods less than GAP_MINUTES apart (flapping nodes)
        if merged and minutes_between(merged[-1]["end"], e["start"]) < GAP_MINUTES:
            m = merged[-1]
            m["end"] = e["end"]
            m["n"] += e["n"]
            m["min_real"] = min(m["min_real"], e["min_real"])
        else:
            merged.append(dict(e))
    for e in merged:
        e["minutes"] = minutes_between(e["start"], e["end"]) + 5
    return merged, len(raw)


def margin_le1_runs(rows):
    """Contiguous periods in which the effective margin (organizations) is <= 1."""
    runs, cur = [], None
    for r in rows:
        real = r[1 + NC]
        if isinstance(real, (int, float)) and real <= 1:
            if cur is None:
                cur = {"start": r[0], "end": r[0], "min": real, "nominal": r[2 + NC]}
            cur["end"] = r[0]
            cur["min"] = min(cur["min"], real)
        elif cur:
            runs.append(cur)
            cur = None
    if cur:
        runs.append(cur)
    for e in runs:
        e["minutes"] = minutes_between(e["start"], e["end"]) + 5
    return runs


def no_qi_runs(rows):
    runs, cur = [], None
    for r in rows:
        if r[3 + NC] is False:
            if cur is None:
                cur = {"start": r[0], "end": r[0], "n": 0}
            cur["end"] = r[0]
            cur["n"] += 1
        elif cur:
            runs.append(cur)
            cur = None
    if cur:
        runs.append(cur)
    for e in runs:
        e["minutes"] = minutes_between(e["start"], e["end"]) + 5
    return runs


def write_csv(name, head, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(head)
        w.writerows(rows)


def keystr(k):
    return "/".join("-" if v is None else str(v) for v in k)


# ------------------------------ main ------------------------------

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    start = datetime.fromisoformat(START).replace(tzinfo=timezone.utc)
    end = (datetime.fromisoformat(END).replace(tzinfo=timezone.utc) if END
           else datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0))
    days = [start + timedelta(days=i) for i in range((end - start).days)]

    failed = download_all(days)
    log("Reading data...")
    rows, total = load_all(days)
    log(f"{total} scans, {len(rows)} valid")
    if not rows:
        log("NO DATA. See run.log.")
        (OUT / "run.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
        return

    steps, noise = config_steps(rows)
    eps = reconfig_episodes(steps)
    thin, thin_raw = thin_margin(rows)
    le1 = margin_le1_runs(rows)
    noqi = no_qi_runs(rows)

    write_csv("config_steps.csv", ["start", "end", "minutes", "scans"] + CFG,
              [[s["start"], s["end"], round(minutes_between(s["start"], s["end"])), s["n"]] + list(s["key"])
               for s in steps])
    write_csv("reconfig_episodes.csv",
              ["start", "end", "intermediate_states", "first(" + "/".join(CFG) + ")", "last",
               "has_weak_state", "weak_state_details"],
              [[e["start"], e["end"], e["n_mid"], keystr(e["first"]), keystr(e["last"]),
                "YES" if e["weak"] else "no",
                "; ".join(f"{w['metric']}={w['value']} (first {w['from']}, last {w['to']}) from {w['start'][:16]} for {dur(w['minutes'])}"
                          for w in e["weak"])] for e in eps])
    thin15 = [e for e in thin if e["minutes"] >= THIN_MIN_MINUTES]
    write_csv("thin_margin.csv", ["start", "end", "minutes", "scans", "min_effective_margin", "nominal_margin"],
              [[e["start"], e["end"], round(e["minutes"]), e["n"], e["min_real"], e["nominal"]] for e in thin15])
    write_csv("no_quorum_intersection.csv", ["start", "end", "minutes", "scans"],
              [[e["start"], e["end"], round(e["minutes"]), e["n"]] for e in noqi])

    # ---- figures for the stopping rule
    weak_eps = [e for e in eps if e["weak_minutes"] >= 60]
    weak_short = [e for e in eps if e["weak"] and e["weak_minutes"] < 60]
    le1_long = [e for e in le1 if e["minutes"] >= RULE_MARGIN1_MINUTES]
    thin_1h = [e for e in thin if e["minutes"] >= 60]
    thin_6h = [e for e in thin if e["minutes"] >= 360]
    thin_24h = [e for e in thin if e["minutes"] >= 1440]
    noqi_long = [e for e in noqi if e["minutes"] >= 60]

    go_a = len(weak_eps) >= RULE_WEAK_TRANSITIONS
    go_b = len(le1_long) >= 1

    R = ["# Full history scan of the Stellar network", "",
         f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
         f"Data: {rows[0][0][:10]} to {rows[-1][0][:10]}, {len(rows)} valid scans "
         f"({total} in total), {len(failed)} days failed to download.", "",
         "## VERDICT UNDER THE STOPPING RULE", "",
         f"- A. Reconfiguration episodes with a weak intermediate state lasting >= 1 hour: **{len(weak_eps)}** "
         f"(out of {len(eps)} episodes; {len(weak_short)} more have a weak state shorter than 1 hour)",
         f"- B. Periods with effective margin <= 1 organization lasting >= {RULE_MARGIN1_MINUTES} minutes: **{len(le1_long)}** "
         f"(periods with margin <= 1 of any length: {len(le1)})",
         f"- For reference: thin margin periods (effective < nominal) >= 1 hour: {len(thin_1h)}; >= 6 hours: {len(thin_6h)}; "
         f">= 24 hours: {len(thin_24h)}",
         f"- For reference: periods without quorum intersection >= 1 hour: {len(noqi_long)} ({len(noqi)} periods of any length)", ""]
    if go_a or go_b:
        why = []
        if go_a:
            why.append("there is historical evidence for the reconfiguration ordering problem")
        if go_b:
            why.append("there is a sustained period with the liveness margin at a dangerous level")
        R.append("**=> Threshold MET: " + " and ".join(why) + ".** Inspect each case below before relying on this.")
    else:
        R.append("**=> Threshold NOT met.** No configuration change passed through a sustained weak state, and the liveness margin "
                 "never stayed at <= 1 for more than 1 hour. The data say the network ran well.")
    if failed:
        R += ["", f"Note: {len(failed)} days failed to download (see run.log). Run the script again to fetch them before relying on the verdict."]

    R += ["", "## A. Reconfiguration episodes", "",
          f"{len(steps)} stable configuration states, {len(eps)} reconfiguration episodes, {noise} noise segments "
          f"shorter than {MIN_STEP_SCANS} scans dropped.", "",
          "Order of metrics: " + " / ".join(CFG), "",
          "| Start | End | Intermediate | First | Last | Weak state |", "|---|---|---|---|---|---|"]
    for e in eps:
        wk = "; ".join(f"{w['metric']}={w['value']} for {dur(w['minutes'])}" for w in e["weak"]) or "none"
        R.append(f"| {e['start'][:16]} | {e['end'][:16]} | {e['n_mid']} | {keystr(e['first'])} | {keystr(e['last'])} | {wk} |")

    R += ["", "## B. Thin liveness margin", "",
          f"{len(thin)} periods after merging ({thin_raw} raw periods). Distribution by length:", ""]
    for label, lo, hi in [("under 15 minutes", 0, 15), ("15 minutes - 1 hour", 15, 60), ("1 - 6 hours", 60, 360),
                          ("6 - 24 hours", 360, 1440), ("over 24 hours", 1440, 10 ** 9)]:
        R.append(f"- {label}: {sum(1 for e in thin if lo <= e['minutes'] < hi)} periods")
    R += ["", "By year (periods >= 1 hour only):", ""]
    years = sorted({e["start"][:4] for e in thin_1h})
    for y in years:
        ys = [e for e in thin_1h if e["start"][:4] == y]
        R.append(f"- {y}: {len(ys)} periods, total {dur(sum(e['minutes'] for e in ys))}, lowest margin {min(e['min_real'] for e in ys)}")
    R += ["", "30 longest periods:", "", "| Start | Length | Lowest effective margin | Nominal margin |", "|---|---|---|---|"]
    for e in sorted(thin, key=lambda e: -e["minutes"])[:30]:
        R.append(f"| {e['start'][:16]} | {dur(e['minutes'])} | {e['min_real']} | {e['nominal']} |")

    R += ["", "### Periods with effective margin <= 1 organization (20 longest)", "",
          "| Start | Length | Lowest | Nominal margin at the time |", "|---|---|---|---|"]
    for e in sorted(le1, key=lambda e: -e["minutes"])[:20]:
        R.append(f"| {e['start'][:16]} | {dur(e['minutes'])} | {e['min']} | {e['nominal']} |")

    R += ["", "## C. Loss of quorum intersection", ""]
    if noqi:
        R += ["| Start | Length | Scans |", "|---|---|---|"]
        for e in sorted(noqi, key=lambda e: -e["minutes"])[:20]:
            R.append(f"| {e['start'][:16]} | {dur(e['minutes'])} | {e['n']} |")
    else:
        R.append("No scan without quorum intersection.")

    R += ["", "## Limitations of this analysis", "",
          "- Only the four resilience metrics precomputed by Radar are used; states that are 'weak' by another metric do not show up.",
          f"- States that last fewer than {MIN_STEP_SCANS} scans are treated as noise and dropped.",
          "- The low nominal margin in 2019 (organization blocking set = 2) inflates the number of periods with margin <= 1 for that year.",
          "- The data come from Radar's crawler; a crawler that loses connectivity can create spurious thin margin periods.", ""]
    (OUT / "report.md").write_text("\n".join(R) + "\n", encoding="utf-8")
    (OUT / "run.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    print("\n" + "\n".join(R[:14]))
    print(f"\nDone. Report written to {OUT / 'report.md'}.")


if __name__ == "__main__":
    main()