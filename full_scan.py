#!/usr/bin/env python3
"""
Quet toan bo lich su mang Stellar (5/2019 -> nay) de tra loi 2 cau hoi:

  A. Co lan doi cau hinh nao di qua TRANG THAI TRUNG GIAN YEU hon ca diem dau va diem cuoi?
     (dong luc cho huong "tai cau hinh an toan")
  B. Co bao nhieu dot BIEN AN TOAN MONG keo dai >= 1 gio, va co lan nao bien xuong <= 1?
     (dong luc cho huong "canh bao som")

Chay:   python full_scan.py
Dat cung thu muc voi cac script truoc. Ngay nao da tai (boi event_deep_dive.py) se duoc dung lai.
Lan dau mat khoang 15-40 phut (~2.700 ngay du lieu). Bi ngat thi chay lai, no tiep tuc tu cho dung.

Ket qua trong ./sdf_feasibility/full_scan/
  report.md                 doc file nay, phan KET LUAN o dau
  config_steps.csv          moi trang thai cau hinh on dinh trong 7 nam
  reconfig_episodes.csv     cac dot tai cau hinh (nhom cac lan chuyen gan nhau)
  thin_margin.csv           moi dot bien mong >= 15 phut
  no_quorum_intersection.csv
  run.log
Chi dung thu vien chuan.
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

# ----------------------------- CAU HINH -----------------------------

BASE = "https://radar.withobsrvr.com/api"
START = "2019-05-20"
END = None                      # None = hom nay
RAW = Path("sdf_feasibility") / "events" / "raw"     # dung chung cache voi script truoc
OUT = Path("sdf_feasibility") / "full_scan"

THREADS = 3                     # so request song song (giu thap cho lich su)
TIMEOUT = 120

CFG = ["topTierSize", "topTierOrgsSize", "minBlockingSetSize",
       "minBlockingSetOrgsSize", "minSplittingSetSize", "minSplittingSetOrgsSize"]
RESILIENCE = ["minBlockingSetSize", "minBlockingSetOrgsSize",
              "minSplittingSetSize", "minSplittingSetOrgsSize"]
REAL, NOMINAL = "minBlockingSetOrgsFilteredSize", "minBlockingSetOrgsSize"

MIN_STEP_SCANS = 5              # trang thai ngan hon so lan quet nay coi la nhieu
EPISODE_QUIET_DAYS = 14         # 2 lan chuyen cach nhau duoi so ngay nay thuoc cung 1 dot tai cau hinh
GAP_MINUTES = 30                # 2 dot bien mong cach nhau duoi muc nay thi gop lam mot
THIN_MIN_MINUTES = 15           # chi ghi cac dot bien mong tu muc nay tro len

# Nguong cua quy tac dung
RULE_WEAK_TRANSITIONS = 1       # >= 1 dot tai cau hinh co trang thai trung gian yeu keo dai >= 1 gio
RULE_MARGIN1_MINUTES = 60       # hoac >= 1 dot bien thuc te <= 1 keo dai >= 60 phut

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
        return f"{minutes:.0f} phut"
    if minutes < 1440:
        return f"{minutes / 60:.1f} gio"
    return f"{minutes / 1440:.1f} ngay"


def minutes_between(a, b):
    return (pt(b) - pt(a)).total_seconds() / 60


# ------------------------- tai du lieu -------------------------

def download_day(day):
    f = RAW / f"stats_{day.strftime('%Y-%m-%d')}.json"
    if f.exists():
        return day, True
    q = urllib.parse.urlencode({"from": iso(day), "to": iso(day + timedelta(days=1))})
    status, data = fetch(f"{BASE}/v1/statistics?{q}")
    if isinstance(data, list):
        f.write_text(json.dumps(data), encoding="utf-8")
        return day, True
    LOG.append(f"LOI tai {day.strftime('%Y-%m-%d')}: HTTP {status}")
    return day, False


def download_all(days):
    todo = [d for d in days if not (RAW / f"stats_{d.strftime('%Y-%m-%d')}.json").exists()]
    log(f"Tong {len(days)} ngay, da co {len(days) - len(todo)}, can tai {len(todo)}")
    failed, done, t0 = [], 0, time.time()
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for day, ok in ex.map(download_day, todo):
            done += 1
            if not ok:
                failed.append(day.strftime("%Y-%m-%d"))
            if done % 100 == 0 or done == len(todo):
                rate = done / max(time.time() - t0, 1)
                left = (len(todo) - done) / max(rate, 0.01) / 60
                log(f"  da tai {done}/{len(todo)} ngay, loi {len(failed)}, con khoang {left:.0f} phut")
    return failed


def load_all(days):
    """Tra ve list tuple gon: (time, cfg..., real, nominal, qi). Bo lan quet loi."""
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


# ------------------------- phan tich -------------------------

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
    """Nhom cac lan chuyen gan nhau. Moi dot: trang thai dau (on dinh truoc do),
    cac trang thai trung gian, trang thai cuoi (on dinh sau do)."""
    eps, i = [], 0
    quiet = EPISODE_QUIET_DAYS * 1440
    while i < len(steps) - 1:
        j = i + 1
        # keo dai dot cho den khi gap trang thai on dinh du lau (hoac het du lieu)
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
    for e in raw:      # gop cac dot cach nhau duoi GAP_MINUTES (node chap chon)
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
    """Cac dot lien tuc ma bien thuc te (to chuc) <= 1."""
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


# ------------------------------ chinh ------------------------------

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    start = datetime.fromisoformat(START).replace(tzinfo=timezone.utc)
    end = (datetime.fromisoformat(END).replace(tzinfo=timezone.utc) if END
           else datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0))
    days = [start + timedelta(days=i) for i in range((end - start).days)]

    failed = download_all(days)
    log("Dang doc du lieu...")
    rows, total = load_all(days)
    log(f"{total} lan quet, hop le {len(rows)}")
    if not rows:
        log("KHONG CO DU LIEU. Xem run.log.")
        (OUT / "run.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
        return

    steps, noise = config_steps(rows)
    eps = reconfig_episodes(steps)
    thin, thin_raw = thin_margin(rows)
    le1 = margin_le1_runs(rows)
    noqi = no_qi_runs(rows)

    write_csv("config_steps.csv", ["bat_dau", "ket_thuc", "phut", "so_lan_quet"] + CFG,
              [[s["start"], s["end"], round(minutes_between(s["start"], s["end"])), s["n"]] + list(s["key"])
               for s in steps])
    write_csv("reconfig_episodes.csv",
              ["bat_dau", "ket_thuc", "so_trang_thai_trung_gian", "dau(" + "/".join(CFG) + ")", "cuoi",
               "co_trang_thai_yeu", "chi_tiet_yeu"],
              [[e["start"], e["end"], e["n_mid"], keystr(e["first"]), keystr(e["last"]),
                "CO" if e["weak"] else "khong",
                "; ".join(f"{w['metric']}={w['value']} (dau {w['from']}, cuoi {w['to']}) tu {w['start'][:16]} trong {dur(w['minutes'])}"
                          for w in e["weak"])] for e in eps])
    thin15 = [e for e in thin if e["minutes"] >= THIN_MIN_MINUTES]
    write_csv("thin_margin.csv", ["bat_dau", "ket_thuc", "phut", "so_lan_quet", "bien_thuc_te_min", "bien_danh_nghia"],
              [[e["start"], e["end"], round(e["minutes"]), e["n"], e["min_real"], e["nominal"]] for e in thin15])
    write_csv("no_quorum_intersection.csv", ["bat_dau", "ket_thuc", "phut", "so_lan_quet"],
              [[e["start"], e["end"], round(e["minutes"]), e["n"]] for e in noqi])

    # ---- so lieu cho quy tac dung
    weak_eps = [e for e in eps if e["weak_minutes"] >= 60]
    weak_short = [e for e in eps if e["weak"] and e["weak_minutes"] < 60]
    le1_long = [e for e in le1 if e["minutes"] >= RULE_MARGIN1_MINUTES]
    thin_1h = [e for e in thin if e["minutes"] >= 60]
    thin_6h = [e for e in thin if e["minutes"] >= 360]
    thin_24h = [e for e in thin if e["minutes"] >= 1440]
    noqi_long = [e for e in noqi if e["minutes"] >= 60]

    go_a = len(weak_eps) >= RULE_WEAK_TRANSITIONS
    go_b = len(le1_long) >= 1

    R = ["# Quet toan bo lich su mang Stellar", "",
         f"Chay luc: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
         f"Du lieu: {rows[0][0][:10]} den {rows[-1][0][:10]}, {len(rows)} lan quet hop le "
         f"(tong {total}), {len(failed)} ngay tai loi.", "",
         "## KET LUAN THEO QUY TAC DUNG", "",
         f"- A. Dot tai cau hinh co trang thai trung gian yeu keo dai >= 1 gio: **{len(weak_eps)}** "
         f"(tren tong {len(eps)} dot; them {len(weak_short)} dot co trang thai yeu nhung duoi 1 gio)",
         f"- B. Dot bien thuc te <= 1 to chuc keo dai >= {RULE_MARGIN1_MINUTES} phut: **{len(le1_long)}** "
         f"(tong so dot bien <= 1 bat ky do dai: {len(le1)})",
         f"- Tham khao: dot bien mong (thuc te < danh nghia) >= 1 gio: {len(thin_1h)}; >= 6 gio: {len(thin_6h)}; "
         f">= 24 gio: {len(thin_24h)}",
         f"- Tham khao: dot mat quorum intersection >= 1 gio: {len(noqi_long)} (tong {len(noqi)} dot bat ky do dai)", ""]
    if go_a or go_b:
        why = []
        if go_a:
            why.append("co bang chung lich su cho bai toan thu tu tai cau hinh")
        if go_b:
            why.append("co ca bien an toan xuong muc nguy hiem keo dai")
        R.append("**=> DAT nguong di tiep: " + " va ".join(why) + ".** Can doc ky tung ca ben duoi truoc khi tin.")
    else:
        R.append("**=> KHONG dat nguong.** Khong co lan chuyen cau hinh nao di qua trang thai yeu keo dai, va bien an toan "
                 "chua lan nao xuong <= 1 qua 1 gio. Du lieu noi rang mang van hanh on; de xuat thieu dong luc thuc tien.")
    if failed:
        R += ["", f"Luu y: {len(failed)} ngay tai loi (xem run.log). Chay lai script de tai bu truoc khi tin ket luan."]

    R += ["", "## A. Cac dot tai cau hinh", "",
          f"{len(steps)} trang thai cau hinh on dinh, {len(eps)} dot tai cau hinh, bo {noise} doan nhieu "
          f"ngan hon {MIN_STEP_SCANS} lan quet.", "",
          "Thu tu chi so: " + " / ".join(CFG), "",
          "| Bat dau | Ket thuc | Trung gian | Dau | Cuoi | Trang thai yeu |", "|---|---|---|---|---|---|"]
    for e in eps:
        wk = "; ".join(f"{w['metric']}={w['value']} trong {dur(w['minutes'])}" for w in e["weak"]) or "khong"
        R.append(f"| {e['start'][:16]} | {e['end'][:16]} | {e['n_mid']} | {keystr(e['first'])} | {keystr(e['last'])} | {wk} |")

    R += ["", "## B. Bien an toan mong", "",
          f"Tong {len(thin)} dot sau khi gop ({thin_raw} dot tho). Phan bo theo do dai:", ""]
    for label, lo, hi in [("duoi 15 phut", 0, 15), ("15 phut - 1 gio", 15, 60), ("1 - 6 gio", 60, 360),
                          ("6 - 24 gio", 360, 1440), ("tren 24 gio", 1440, 10 ** 9)]:
        R.append(f"- {label}: {sum(1 for e in thin if lo <= e['minutes'] < hi)} dot")
    R += ["", "Theo nam (chi tinh dot >= 1 gio):", ""]
    years = sorted({e["start"][:4] for e in thin_1h})
    for y in years:
        ys = [e for e in thin_1h if e["start"][:4] == y]
        R.append(f"- {y}: {len(ys)} dot, tong {dur(sum(e['minutes'] for e in ys))}, bien thap nhat {min(e['min_real'] for e in ys)}")
    R += ["", "30 dot dai nhat:", "", "| Bat dau | Do dai | Bien thuc te thap nhat | Bien danh nghia |", "|---|---|---|---|"]
    for e in sorted(thin, key=lambda e: -e["minutes"])[:30]:
        R.append(f"| {e['start'][:16]} | {dur(e['minutes'])} | {e['min_real']} | {e['nominal']} |")

    R += ["", "### Cac dot bien thuc te <= 1 to chuc (20 dot dai nhat)", "",
          "| Bat dau | Do dai | Thap nhat | Bien danh nghia luc do |", "|---|---|---|---|"]
    for e in sorted(le1, key=lambda e: -e["minutes"])[:20]:
        R.append(f"| {e['start'][:16]} | {dur(e['minutes'])} | {e['min']} | {e['nominal']} |")

    R += ["", "## C. Mat quorum intersection", ""]
    if noqi:
        R += ["| Bat dau | Do dai | So lan quet |", "|---|---|---|"]
        for e in sorted(noqi, key=lambda e: -e["minutes"])[:20]:
            R.append(f"| {e['start'][:16]} | {dur(e['minutes'])} | {e['n']} |")
    else:
        R.append("Khong co lan quet nao mat quorum intersection.")

    R += ["", "## Gioi han cua phan tich nay", "",
          "- Chi dung 4 chi so resilience ma Radar tinh san; trang thai 'yeu' theo chi so khac se khong hien ra.",
          f"- Trang thai ton tai duoi {MIN_STEP_SCANS} lan quet bi coi la nhieu va bo qua.",
          "- Bien danh nghia thap o giai doan 2019 (blocking set to chuc = 2) lam tang so dot bien <= 1 cua nam do.",
          "- So lieu la cua crawler Radar; node crawler mat ket noi co the tao dot bien mong gia.", ""]
    (OUT / "report.md").write_text("\n".join(R) + "\n", encoding="utf-8")
    (OUT / "run.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    print("\n" + "\n".join(R[:14]))
    print(f"\nXong. Gui file {OUT / 'report.md'} de doc tiep.")


if __name__ == "__main__":
    main()