#!/usr/bin/env python3
"""
Kiem chung cac ca lon: tai thoi diem do, validator cua TO CHUC NAO khong hoat dong?

  - Dung mot to chuc co da so validator ngung  -> su co that, biet luon to chuc nao.
  - Nhieu to chuc cung "ngung" mot luc          -> nghi crawler cua Radar mat ket noi.
  - Khong to chuc nao ngung nhung chi so giam    -> thay doi cau hinh (quorum set) hoac loi tinh toan.

Chay:   python verify_cases.py          (khoang 25 request, 1-2 phut)
Ket qua trong ./sdf_feasibility/verify/
  report.md          doc file nay
  cases.csv          moi dong la mot (ca, thoi diem, to chuc)
  raw/snap_*.json    snapshot goc
Chi dung thu vien chuan. Chay lai se dung lai snapshot da tai.
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

# (ten ca, mo ta, thoi diem doi chung truoc su kien, [cac thoi diem trong su kien])  -- gio UTC
CASES = [
    ("2020-04-23", "Bien thuc te con 1 to chuc trong 7,7 gio",
     "2020-04-23T18:00", ["2020-04-24T01:00", "2020-04-24T05:00"]),
    ("2020-05-22", "Bien danh nghia giam (blocking set 6 -> 4) trong 7,5 ngay",
     "2020-05-21T12:00", ["2020-05-23T12:00", "2020-05-27T12:00"]),
    ("2021-04-06", "SDF dung validator (da co thong cao); bien con 1 to chuc tu 14:34 trong 3,9 gio",
     "2021-04-05T12:00", ["2021-04-06T10:00", "2021-04-06T16:00", "2021-04-07T12:00"]),
    ("2022-07-26", "Bien thuc te mong 1,2 ngay, co luc con 1 to chuc",
     "2022-07-26T08:00", ["2022-07-26T20:00", "2022-07-27T08:00"]),
    ("2022-12-13", "Bien mong 1,1 ngay roi top tier tu 8 ve 7 to chuc",
     "2022-12-13T06:00", ["2022-12-13T20:00", "2022-12-15T12:00"]),
    ("2023-09-14", "Bien thuc te ve 0 nhieu lan trong 9 gio (nghi loi do)",
     "2023-09-13T18:00", ["2023-09-14T05:00", "2023-09-14T10:58", "2023-09-16T12:00"]),
    ("2024-10-03", "Blocking set danh nghia 6 -> 5 trong 4,6 ngay",
     "2024-10-03T10:00", ["2024-10-05T12:00"]),
    ("2025-08-22", "Bien thuc te mong 3,1 ngay",
     "2025-08-22T08:00", ["2025-08-23T12:00", "2025-08-25T06:00"]),
    ("2026-10-01", "Splitting set to chuc 4 -> 0 -> 1 (nghi do Radar doi bo phan tich)",
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
                log(f"OK   {t} -> snapshot luc {data.get('time')}")
                time.sleep(0.5)
                return data
        except urllib.error.HTTPError as e:
            log(f"HTTP {e.code} {t}")
            if e.code == 404:
                return None
        except Exception as e:
            log(f"LOI {type(e).__name__} {t}")
        time.sleep(5)
    return None


def walk(q, acc):
    if isinstance(q, dict):
        acc.update(q.get("validators") or [])
        for i in q.get("innerQuorumSets") or []:
            walk(i, acc)


def top_tier(net):
    """Xap xi top tier = transitive quorum set cua mang (Radar tinh san).
    Neu snapshot khong co truong nay: lay bao dong tin cay tu validator duoc tin nhieu nhat."""
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
    """{ten to chuc: [(ten node, isValidating, quorumSetHashKey)]} cho cac validator trong tier."""
    nodes = {n["publicKey"]: n for n in net.get("nodes") or []}
    orgname = {}
    for o in net.get("organizations") or []:
        for pk in o.get("validators") or []:
            orgname[pk] = o.get("name") or o.get("homeDomain") or o.get("id")
    view = {}
    for pk in tier:
        n = nodes.get(pk)
        org = orgname.get(pk) or (n or {}).get("homeDomain") or "(khong ro to chuc)"
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
    R = ["# Kiem chung cac ca lon", "", f"Chay luc: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
         "Gio trong bao cao la UTC. 'Ngung' = Radar ghi validator do khong validating tai thoi diem do.", "",
         "## Tom tat", "", "| Ca | Thoi diem | To chuc top tier mat da so validator | Tong validator top tier ngung | Nhan dinh |",
         "|---|---|---|---|---|"]
    detail, rows = [], []

    for name, desc, base_t, probes in CASES:
        detail += ["", f"## {name}: {desc}", ""]
        base = snapshot(base_t)
        if not base:
            detail.append(f"Khong tai duoc snapshot doi chung {base_t}.")
            R.append(f"| {name} | {base_t} | - | - | khong tai duoc snapshot |")
            continue
        tier = top_tier(base)
        bview = org_view(base, tier)
        bq = {pk: n.get("quorumSetHashKey") for pk, n in ((n["publicKey"], n) for n in base.get("nodes") or [])}
        detail += [f"**Doi chung {base_t}** (snapshot {base.get('time')}): top tier {len(tier)} validator, "
                   f"{len(bview)} to chuc.", "", f"Chi so: {stats_line(base)}", ""]
        bdown = [f"{o}: {', '.join(n for n, v, _ in vs if not v)}" for o, vs in sorted(bview.items())
                 if any(not v for _, v, _ in vs)]
        if bdown:
            detail += ["Da ngung tu truoc: " + "; ".join(bdown), ""]

        for t in probes:
            net = snapshot(t)
            if not net:
                detail.append(f"**{t}**: khong tai duoc snapshot.")
                R.append(f"| {name} | {t} | - | - | khong tai duoc snapshot |")
                continue
            # dung top tier cua DOI CHUNG de thay ai bien mat; ghi them thay doi thanh vien
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
                majority_lost = up * 2 <= len(vs)          # con <= mot nua: to chuc khong con du da so
                flag = "  <-- MAT DA SO" if majority_lost else ""
                if majority_lost:
                    down_orgs.append(org)
                off = [n for n, v, _ in vs if not v]
                lines.append(f"- {org}: {up}/{len(vs)} dang validating"
                             + (f" (ngung: {', '.join(off)})" if off else "") + flag)
                rows.append([name, t, org, len(vs), up, "; ".join(off), "x" if majority_lost else ""])
            joined = sorted(names.get(pk, pk[:8]) for pk in now_tier - tier)
            left = sorted(names.get(pk, pk[:8]) for pk in tier - now_tier)
            qchanged = sorted(names.get(pk, pk[:8]) for pk in tier
                              if pk in nq and bq.get(pk) and nq[pk] and nq[pk] != bq[pk])

            frac = down_nodes / total if total else 0
            if len(down_orgs) == 0 and not (joined or left or qchanged):
                verdict = "khong to chuc nao mat da so, cau hinh khong doi: chi so giam khong giai thich duoc bang snapshot nay"
            elif len(down_orgs) == 0:
                verdict = "khong to chuc nao mat da so; co THAY DOI CAU HINH (xem chi tiet)"
            elif frac > 0.5:
                verdict = f"{len(down_orgs)} to chuc 'ngung' cung luc ({frac:.0%} validator): NGHI LOI CRAWLER"
            elif len(down_orgs) == 1:
                verdict = "su co that o 1 to chuc"
            else:
                verdict = f"su co that, {len(down_orgs)} to chuc ngung dong thoi"
            R.append(f"| {name} | {t} | {', '.join(down_orgs) or '-'} | {down_nodes}/{total} | {verdict} |")

            detail += [f"**{t}** (snapshot {net.get('time')}): {verdict}", "", f"Chi so: {stats_line(net)}", ""] + lines
            if joined:
                detail.append(f"- Vao transitive quorum set so voi doi chung: {', '.join(joined)}")
            if left:
                detail.append(f"- Roi transitive quorum set so voi doi chung: {', '.join(left)}")
            if qchanged:
                detail.append(f"- Validator top tier DOI quorum set so voi doi chung: {', '.join(qchanged)}")
            detail.append("")

    R += ["", "Cach doc cot nhan dinh:",
          "- 'su co that o 1 to chuc': dung kieu su kien SDF goi y (bao truoc cho node operator).",
          "- 'NGHI LOI CRAWLER': qua nua validator top tier cung ngung, kho la su co that; khong nen dua vao proposal.",
          "- 'THAY DOI CAU HINH': bien giam do quorum set hoac thanh vien top tier doi, khong phai do node hong.",
          "- Top tier o day la transitive quorum set do Radar tinh tai thoi diem doi chung (xap xi).", ""]
    with open(OUT / "cases.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ca", "thoi_diem_utc", "to_chuc", "so_validator", "dang_validating", "validator_ngung", "mat_da_so"])
        w.writerows(rows)
    (OUT / "report.md").write_text("\n".join(R + detail) + "\n", encoding="utf-8")
    (OUT / "run.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    print("\n" + "\n".join(R))
    print(f"Xong. Gui file {OUT / 'report.md'}.")


if __name__ == "__main__":
    main()