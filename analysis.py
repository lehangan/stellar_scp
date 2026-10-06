#!/usr/bin/env python3
"""
Phan tich co che cho proposal SDF. Hai phan:

PHAN A - Ba ca DOI CAU HINH (Blockdaemon 5/2020, SDF 4/2021, Franklin Templeton 10/2024)
  1. In quorum set TRUOC va SAU cua cac validator da doi.
  2. Tu tinh lai bien an toan (min blocking set) cho 3 cau hinh:
        - truoc khi doi
        - thuc te sau khi doi
        - PHAN THUC: cau hinh truoc, chi thay quorum set cua dung cac validator da doi
     Neu phan thuc tai tao duoc muc giam => thay doi cua rieng to chuc do la NGUYEN NHAN,
     va mot cong cu kiem tra truoc khi doi se thay duoc.

PHAN B - Dien bien theo ngay cua Wirex (2022) va SatoshiPay (2025)
  Uptime tung validator va cua ca to chuc theo ngay, ngay dau tien co dau hieu,
  khoang cach den luc bi loai / su co lon.

Chay:   python mechanism_analysis.py      (khoang 15 request, 1-3 phut)
Dat cung thu muc voi cac script truoc; snapshot da tai se duoc dung lai.
Ket qua: ./sdf_feasibility/mechanism/report.md   (gui file nay)
Chi dung thu vien chuan.
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
SNAP = Path("sdf_feasibility") / "verify" / "raw"       # cache snapshot cua script truoc
OUT = Path("sdf_feasibility") / "mechanism"
TIMEOUT = 120
MAX_COMBOS = 600_000        # gioi han so to hop khi vet can cap node

# (ten, mo ta, truoc, trong, sau khi hoi phuc)  -- gio UTC
CONFIG_CASES = [
    ("2020-05 Blockdaemon", "Blocking set 6 -> 4 (to chuc 3 -> 2) trong 7,5 ngay",
     "2020-05-21T12:00", "2020-05-23T12:00", "2020-05-30T12:00"),
    ("2021-04 SDF", "Sau su co 6/4/2021, blocking set 6 -> 4 trong 1,3 ngay",
     "2021-04-05T12:00", "2021-04-07T12:00", "2021-04-20T12:00"),
    ("2024-10 Franklin Templeton", "Blocking set 6 -> 5 trong 4,6 ngay",
     "2024-10-03T10:00", "2024-10-05T12:00", "2024-10-09T12:00"),
]

# (ten to chuc chua chuoi nay, snapshot de lay public key, tu ngay, den ngay, moc su kien, mo ta moc)
ORG_TIMELINES = [
    ("Wirex", "2022-07-26T08:00", "2022-01-01", "2022-12-31", "2022-12-14", "roi top tier"),
    ("SatoshiPay", "2025-08-22T08:00", "2025-01-01", "2026-09-30", "2025-08-22", "ngung ca 3 validator hon 3 ngay"),
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
    log(f"LOI {last}  {url}")
    return 0, None


def snapshot(t):
    f = SNAP / ("snap_" + t.replace(":", "") + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    status, data = get(f"{BASE}/v1?{urllib.parse.urlencode({'at': t + ':00.000Z'})}")
    time.sleep(0.5)
    if isinstance(data, dict) and "nodes" in data:
        f.write_text(json.dumps(data), encoding="utf-8")
        log(f"tai snapshot {t} -> {data.get('time')}")
        return data
    log(f"KHONG tai duoc snapshot {t} (HTTP {status})")
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
    """-> (threshold, bitmask validator trong tier, [inner...])"""
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
    """Quorum lon nhat nam trong tap S (bitmask). 0 = khong con quorum nao."""
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
    """groups: list bitmask (moi phan tu la 1 node hoac 1 to chuc).
    Tra ve (kich thuoc nho nhat, cac tap dat kich thuoc do [toi da 12], da_vet_het)."""
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
    """override: {publicKey: quorumSet} thay cho quorum set trong net."""
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
        org = orgname.get(pk) or nodes.get(pk, {}).get("homeDomain") or "(khong ro)"
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
        return ["(khong co quorum set)"]
    vals = q.get("validators") or []
    inner = q.get("innerQuorumSets") or []
    pad = "  " * depth
    out = [f"{pad}- can {q.get('threshold')} trong {len(vals) + len(inner)} phan tu"]
    if vals:
        out.append(f"{pad}  validator truc tiep: " + ", ".join(sorted(names.get(v, v[:8]) for v in vals)))
    for i in sorted(inner, key=lambda x: str(sorted(x.get("validators") or []))):
        iv = i.get("validators") or []
        orgs = sorted({orgof.get(v, "?") for v in iv})
        if not i.get("innerQuorumSets"):
            out.append(f"{pad}  [{'/'.join(orgs)}] can {i.get('threshold')} trong {len(iv)}: "
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
        return R + ["Khong tai duoc snapshot."], None
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
    R.append(f"Top tier luc doi chung: {len(tier)} validator. Validator doi quorum set: "
             + (", ".join(names[pk] for pk in changed) or "KHONG CO"))
    # nhom cac validator co cung cap (truoc, sau)
    seen = {}
    for pk in changed:
        key = (canon(na[pk].get("quorumSet")), canon(nb[pk].get("quorumSet")))
        seen.setdefault(key, []).append(pk)
    for pks in seen.values():
        pk = pks[0]
        R += ["", f"### Quorum set cua: {', '.join(names[p] for p in pks)}", "", "TRUOC:", "```"]
        R += fmt_qset(na[pk].get("quorumSet"), names, orgof) + ["```", "SAU:", "```"]
        R += fmt_qset(nb[pk].get("quorumSet"), names, orgof) + ["```"]
        qa, qb = na[pk].get("quorumSet") or {}, nb[pk].get("quorumSet") or {}
        sa, sb = set(), set()
        walk(qa, sa)
        walk(qb, sb)
        diff = [f"nguong ngoai {qa.get('threshold')} -> {qb.get('threshold')}",
                f"so phan tu ngoai {len(qa.get('validators') or []) + len(qa.get('innerQuorumSets') or [])} -> "
                f"{len(qb.get('validators') or []) + len(qb.get('innerQuorumSets') or [])}"]
        if sb - sa:
            diff.append("them: " + ", ".join(sorted(names.get(v, v[:8]) for v in sb - sa)))
        if sa - sb:
            diff.append("bo: " + ", ".join(sorted(names.get(v, v[:8]) for v in sa - sb)))
        R.append("Khac biet: " + "; ".join(diff))

    log(f"{name}: dang tinh blocking set (co the mat 1-2 phut)...")
    before = analyse_config(a, tier)
    actual = analyse_config(b, tier)
    cf = analyse_config(a, tier, {pk: nb[pk].get("quorumSet") for pk in changed}) if changed else None
    sa_, sb_ = a.get("statistics") or {}, b.get("statistics") or {}

    def row(label, r, radar=None):
        sets = "; ".join(" + ".join(s) for s in r["org_sets"][:6]) if r["org_sets"] else "-"
        rd = f"{radar.get('minBlockingSetOrgsSize')} / {radar.get('minBlockingSetSize')}" if radar else "-"
        return f"| {label} | {r['orgs']} | {r['nodes'] if r['nodes'] is not None else 'khong tinh'} | {rd} | {sets} |"

    R += ["", "### Bien an toan tu tinh lai (chi xet top tier)", "",
          "| Cau hinh | Min blocking set (to chuc) | (node) | Radar ghi (to chuc / node) | Cac nhom to chuc nho nhat du de chan mang |",
          "|---|---|---|---|---|",
          row("Truoc khi doi", before, sa_), row("Thuc te sau khi doi", actual, sb_)]
    verdict = None
    if cf:
        R.append(row("PHAN THUC: chi doi quorum set cua cac validator tren", cf))
        if cf["orgs"] == actual["orgs"] and (cf["orgs"] or 0) < (before["orgs"] or 0):
            verdict = "XAC NHAN: rieng thay doi nay da du de lam bien to chuc giam tu %s xuong %s." % (before["orgs"], cf["orgs"])
        elif cf["nodes"] is not None and before["nodes"] is not None and cf["nodes"] < before["nodes"] and cf["nodes"] == actual["nodes"]:
            verdict = "XAC NHAN (cap node): rieng thay doi nay lam blocking set giam tu %s xuong %s node." % (before["nodes"], cf["nodes"])
        elif cf["orgs"] == before["orgs"] and cf["nodes"] == before["nodes"]:
            verdict = "KHONG XAC NHAN: thay rieng quorum set nay khong lam bien giam; nguyen nhan nam o cho khac."
        else:
            verdict = "MOT PHAN: phan thuc cho ket qua khac ca truoc lan sau, can xem tay."
    else:
        verdict = "Khong thay validator top tier nao doi quorum set giua hai snapshot."
    R += ["", f"**Ket luan co che: {verdict}**"]
    if before["orgs"] != sa_.get("minBlockingSetOrgsSize"):
        R.append(f"(Luu y: so tu tinh cho cau hinh truoc ({before['orgs']}) khac so Radar ghi "
                 f"({sa_.get('minBlockingSetOrgsSize')}); cach tinh cua script co the khong khop hoan toan voi Radar.)")

    c = snapshot(t_after)
    if c:
        nc = {n["publicKey"]: n for n in c.get("nodes") or []}
        back = [names[pk] for pk in changed if pk in nc and canon(nc[pk].get("quorumSet")) == canon(na[pk].get("quorumSet"))]
        sc = c.get("statistics") or {}
        R.append(f"Sau do ({t_after}): {len(back)}/{len(changed)} validator da quay ve quorum set cu; "
                 f"Radar ghi blocking set to chuc/node = {sc.get('minBlockingSetOrgsSize')}/{sc.get('minBlockingSetSize')}.")
    return R, verdict


# ---------------------------------------------------------------- dien bien to chuc

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
    log(f"KHONG tai duoc day-statistics {kind} {ident[:12]} (HTTP {status})")
    return []


def ratio(rec, key):
    c = rec.get("crawlCount") or 0
    return (rec.get(key) or 0) / c if c else None


def org_timeline(match, snap_t, d1, d2, milestone, mdesc):
    R = ["", f"## Dien bien {match}: {d1} den {d2} (moc: {milestone}, {mdesc})", ""]
    net = snapshot(snap_t)
    if not net:
        return R + ["Khong tai duoc snapshot de lay public key."]
    org = next((o for o in net.get("organizations") or [] if match.lower() in (o.get("name") or "").lower()), None)
    if not org:
        return R + [f"Khong tim thay to chuc co ten chua '{match}'."]
    nodes = {n["publicKey"]: n for n in net.get("nodes") or []}
    vals = [(pk, nodes.get(pk, {}).get("name") or pk[:8]) for pk in org.get("validators") or []]

    per = {}
    for pk, nm in vals:
        data = day_stats("node", pk, d1, d2)
        if data and "isValidatingCount" not in data[0]:
            R.append(f"(Truong du lieu node khac du kien: {sorted(data[0].keys())})")
        for r in data:
            per.setdefault(str(r.get("time"))[:10], {})[nm] = ratio(r, "isValidatingCount")
    odata = day_stats("organization", org["id"], d1, d2)
    okey = "isSubQuorumAvailableCount"
    if odata and okey not in odata[0]:
        R.append(f"(Truong du lieu to chuc khac du kien: {sorted(odata[0].keys())})")
    oday = {str(r.get("time"))[:10]: ratio(r, okey) for r in odata}

    days = sorted(set(per) | set(oday))
    if not days:
        return R + ["Khong co du lieu theo ngay."]
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
        w.writerow(["ngay"] + [f"{nm} % validating" for nm in names] + ["to chuc % kha dung"])
        w.writerows(rows)

    def pct(v):
        return "-" if v is None else f"{100 * v:.0f}%"

    R.append(f"Validator: {', '.join(names)}. So ngay co du lieu: {len(days)}. "
             f"So ngay co dau hieu (mot validator duoi 90% hoac to chuc duoi 99%): {len(bad)}.")
    if bad:
        first = bad[0][0]
        gap = (datetime.fromisoformat(milestone) - datetime.fromisoformat(first)).days
        org_bad = [b for b in bad if b[2] is not None and b[2] < 0.99]
        R += ["", f"- Ngay dau tien co dau hieu: **{first}**, tuc {gap} ngay truoc moc {milestone} ({mdesc}).",
              f"- So ngay CA TO CHUC khong kha dung mot phan (duoi 99%): {len(org_bad)}"
              + (f", dau tien {org_bad[0][0]}" if org_bad else "") + ".", "",
              "Theo thang:", "", "| Thang | Ngay co dau hieu | " + " | ".join(names) + " | To chuc |",
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
        R += ["", "40 ngay co dau hieu dau tien:", "", "| Ngay | " + " | ".join(names) + " | To chuc |",
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
        summ.append(f"- {case[0]}: {v or 'khong co du lieu'}")
    for tl in ORG_TIMELINES:
        body += org_timeline(*tl)
    head = ["# Phan tich co che", "", f"Chay luc: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
            "## Tom tat phan A (doi cau hinh)", ""] + summ + [
            "", "Cach doc: 'XAC NHAN' nghia la chi can thay quorum set cua dung to chuc do vao cau hinh cu la bien an toan "
                "toan mang giam dung nhu thuc te. Day la phan thuc truc tiep cho cau 'cong cu kiem tra truoc khi doi "
                "se phat hien duoc'.",
            "Gioi han: script chi xet cac validator trong top tier va tu cai dat phep tinh blocking set; "
            "so co the lech voi Radar o truong hop bien."]
    (OUT / "report.md").write_text("\n".join(head + body) + "\n", encoding="utf-8")
    (OUT / "run.log").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    print("\n" + "\n".join(head))
    print(f"\nXong. Gui file {OUT / 'report.md'}.")


if __name__ == "__main__":
    main()