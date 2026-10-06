# Phan tich co che

Chay luc: 2026-10-02 11:37

## Tom tat phan A (doi cau hinh)

- 2020-05 Blockdaemon: XAC NHAN: rieng thay doi nay da du de lam bien to chuc giam tu 3 xuong 2.
- 2021-04 SDF: XAC NHAN: rieng thay doi nay da du de lam bien to chuc giam tu 3 xuong 2.
- 2024-10 Franklin Templeton: XAC NHAN (cap node): rieng thay doi nay lam blocking set giam tu 6 xuong 5 node.

Cach doc: 'XAC NHAN' nghia la chi can thay quorum set cua dung to chuc do vao cau hinh cu la bien an toan toan mang giam dung nhu thuc te. Day la phan thuc truc tiep cho cau 'cong cu kiem tra truoc khi doi se phat hien duoc'.
Gioi han: script chi xet cac validator trong top tier va tu cai dat phep tinh blocking set; so co the lech voi Radar o truong hop bien.

## 2020-05 Blockdaemon: Blocking set 6 -> 4 (to chuc 3 -> 2) trong 7,5 ngay

Top tier luc doi chung: 23 validator. Validator doi quorum set: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3

### Quorum set cua: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3

TRUOC:
```
- can 5 trong 7 phan tu
  [Keybase] can 2 trong 3: Keybase 0, Keybase 1, Keybase 2
  [LOBSTR] can 3 trong 5: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (Australia)
  [Blockdaemon Inc.] can 2 trong 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Wirex Limited] can 2 trong 3: Wirex Singapore, Wirex United Kingdom, Wirex United States
  [Stellar Development Foundation] can 2 trong 3: SDF 1, SDF 2, SDF 3
  [COINQVEST Limited] can 2 trong 3: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong)
  [SatoshiPay] can 2 trong 3: SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)
```
SAU:
```
- can 5 trong 6 phan tu
  [Keybase] can 2 trong 3: Keybase 0, Keybase 1, Keybase 2
  [LOBSTR] can 3 trong 5: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (Australia)
  [Blockdaemon Inc.] can 2 trong 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Wirex Limited] can 2 trong 3: Wirex Singapore, Wirex United Kingdom, Wirex United States
  [Stellar Development Foundation] can 2 trong 3: SDF 1, SDF 2, SDF 3
  [COINQVEST Limited] can 2 trong 3: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong)
```
Khac biet: nguong ngoai 5 -> 5; so phan tu ngoai 7 -> 6; bo: SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)

### Bien an toan tu tinh lai (chi xet top tier)

| Cau hinh | Min blocking set (to chuc) | (node) | Radar ghi (to chuc / node) | Cac nhom to chuc nho nhat du de chan mang |
|---|---|---|---|---|
| Truoc khi doi | 3 | 6 | 3 / 6 | Blockdaemon Inc. + COINQVEST Limited + Keybase; Blockdaemon Inc. + COINQVEST Limited + LOBSTR; Blockdaemon Inc. + COINQVEST Limited + SatoshiPay; Blockdaemon Inc. + COINQVEST Limited + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST Limited + Wirex Limited; Blockdaemon Inc. + Keybase + LOBSTR |
| Thuc te sau khi doi | 2 | 4 | 2 / 4 | COINQVEST Limited + Keybase; COINQVEST Limited + LOBSTR; COINQVEST Limited + Stellar Development Foundation; COINQVEST Limited + Wirex Limited; Keybase + LOBSTR; Keybase + Stellar Development Foundation |
| PHAN THUC: chi doi quorum set cua cac validator tren | 2 | 4 | - | COINQVEST Limited + Keybase; COINQVEST Limited + LOBSTR; COINQVEST Limited + Stellar Development Foundation; COINQVEST Limited + Wirex Limited; Keybase + LOBSTR; Keybase + Stellar Development Foundation |

**Ket luan co che: XAC NHAN: rieng thay doi nay da du de lam bien to chuc giam tu 3 xuong 2.**
Sau do (2020-05-30T12:00): 3/3 validator da quay ve quorum set cu; Radar ghi blocking set to chuc/node = 3/6.

## 2021-04 SDF: Sau su co 6/4/2021, blocking set 6 -> 4 trong 1,3 ngay

Top tier luc doi chung: 23 validator. Validator doi quorum set: SDF 3, SDF 1, SDF 2

### Quorum set cua: SDF 3, SDF 1, SDF 2

TRUOC:
```
- can 5 trong 7 phan tu
  [Keybase] can 2 trong 3: Keybase 0, Keybase 1, Keybase 2
  [LOBSTR] can 3 trong 5: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (Australia)
  [Blockdaemon Inc.] can 2 trong 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Wirex Limited] can 2 trong 3: Wirex Singapore, Wirex United Kingdom, Wirex United States
  [Stellar Development Foundation] can 2 trong 3: SDF 1, SDF 2, SDF 3
  [COINQVEST OÜ] can 2 trong 3: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong)
  [SatoshiPay] can 2 trong 3: SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)
```
SAU:
```
- can 5 trong 6 phan tu
  [Keybase] can 2 trong 3: Keybase 0, Keybase 1, Keybase 2
  [Blockdaemon Inc.] can 2 trong 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Wirex Limited] can 2 trong 3: Wirex Singapore, Wirex United Kingdom, Wirex United States
  [Stellar Development Foundation] can 2 trong 3: SDF 1, SDF 2, SDF 3
  [COINQVEST OÜ] can 2 trong 3: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong)
  [SatoshiPay] can 2 trong 3: SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)
```
Khac biet: nguong ngoai 5 -> 5; so phan tu ngoai 7 -> 6; bo: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (Australia)

### Bien an toan tu tinh lai (chi xet top tier)

| Cau hinh | Min blocking set (to chuc) | (node) | Radar ghi (to chuc / node) | Cac nhom to chuc nho nhat du de chan mang |
|---|---|---|---|---|
| Truoc khi doi | 3 | 6 | 3 / 6 | Blockdaemon Inc. + COINQVEST OÜ + Keybase; Blockdaemon Inc. + COINQVEST OÜ + LOBSTR; Blockdaemon Inc. + COINQVEST OÜ + SatoshiPay; Blockdaemon Inc. + COINQVEST OÜ + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST OÜ + Wirex Limited; Blockdaemon Inc. + Keybase + LOBSTR |
| Thuc te sau khi doi | 2 | 4 | 2 / 4 | Blockdaemon Inc. + COINQVEST OÜ; Blockdaemon Inc. + Keybase; Blockdaemon Inc. + SatoshiPay; Blockdaemon Inc. + Wirex Limited; COINQVEST OÜ + Keybase; COINQVEST OÜ + SatoshiPay |
| PHAN THUC: chi doi quorum set cua cac validator tren | 2 | 4 | - | Blockdaemon Inc. + COINQVEST OÜ; Blockdaemon Inc. + Keybase; Blockdaemon Inc. + SatoshiPay; Blockdaemon Inc. + Wirex Limited; COINQVEST OÜ + Keybase; COINQVEST OÜ + SatoshiPay |

**Ket luan co che: XAC NHAN: rieng thay doi nay da du de lam bien to chuc giam tu 3 xuong 2.**
Sau do (2021-04-20T12:00): 3/3 validator da quay ve quorum set cu; Radar ghi blocking set to chuc/node = 3/6.

## 2024-10 Franklin Templeton: Blocking set 6 -> 5 trong 4,6 ngay

Top tier luc doi chung: 23 validator. Validator doi quorum set: FT SCV 2

### Quorum set cua: FT SCV 2

TRUOC:
```
- can 5 trong 7 phan tu
  [LOBSTR] can 3 trong 5: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (India)
  [Franklin Templeton] can 2 trong 3: FT SCV 1, FT SCV 2, FT SCV 3
  [Blockdaemon Inc.] can 2 trong 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Stellar Development Foundation] can 2 trong 3: SDF 1, SDF 2, SDF 3
  [Whalestack LLC] can 2 trong 3: Whalestack (Finland), Whalestack (Germany), Whalestack (Hong Kong)
  [SatoshiPay] can 2 trong 3: SatoshiPay Frankfurt, SatoshiPay Iowa, SatoshiPay Singapore
  [Public Node] can 2 trong 3: Boötes, Hercules by OG Technologies, Lyra by BP Ventures
```
SAU:
```
- can 5 trong 6 phan tu
  [Franklin Templeton] can 2 trong 3: FT SCV 1, FT SCV 2, FT SCV 3
  [Blockdaemon Inc.] can 2 trong 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Stellar Development Foundation] can 2 trong 3: SDF 1, SDF 2, SDF 3
  [Whalestack LLC] can 2 trong 3: Whalestack (Finland), Whalestack (Germany), Whalestack (Hong Kong)
  [SatoshiPay] can 2 trong 3: SatoshiPay Frankfurt, SatoshiPay Iowa, SatoshiPay Singapore
  [Public Node] can 2 trong 3: Boötes, Hercules by OG Technologies, Lyra by BP Ventures
```
Khac biet: nguong ngoai 5 -> 5; so phan tu ngoai 7 -> 6; bo: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (India)

### Bien an toan tu tinh lai (chi xet top tier)

| Cau hinh | Min blocking set (to chuc) | (node) | Radar ghi (to chuc / node) | Cac nhom to chuc nho nhat du de chan mang |
|---|---|---|---|---|
| Truoc khi doi | 3 | 6 | 3 / 6 | Blockdaemon Inc. + Franklin Templeton + LOBSTR; Blockdaemon Inc. + Franklin Templeton + Public Node; Blockdaemon Inc. + Franklin Templeton + SatoshiPay; Blockdaemon Inc. + Franklin Templeton + Stellar Development Foundation; Blockdaemon Inc. + Franklin Templeton + Whalestack LLC; Blockdaemon Inc. + LOBSTR + Public Node |
| Thuc te sau khi doi | 3 | 5 | 3 / 5 | Blockdaemon Inc. + Franklin Templeton + LOBSTR; Blockdaemon Inc. + Franklin Templeton + Public Node; Blockdaemon Inc. + Franklin Templeton + SatoshiPay; Blockdaemon Inc. + Franklin Templeton + Stellar Development Foundation; Blockdaemon Inc. + Franklin Templeton + Whalestack LLC; Blockdaemon Inc. + LOBSTR + Public Node |
| PHAN THUC: chi doi quorum set cua cac validator tren | 3 | 5 | - | Blockdaemon Inc. + Franklin Templeton + LOBSTR; Blockdaemon Inc. + Franklin Templeton + Public Node; Blockdaemon Inc. + Franklin Templeton + SatoshiPay; Blockdaemon Inc. + Franklin Templeton + Stellar Development Foundation; Blockdaemon Inc. + Franklin Templeton + Whalestack LLC; Blockdaemon Inc. + LOBSTR + Public Node |

**Ket luan co che: XAC NHAN (cap node): rieng thay doi nay lam blocking set giam tu 6 xuong 5 node.**
Sau do (2024-10-09T12:00): 1/1 validator da quay ve quorum set cu; Radar ghi blocking set to chuc/node = 3/6.

## Dien bien Wirex: 2022-01-01 den 2022-12-31 (moc: 2022-12-14, roi top tier)

Validator: Wirex Singapore, Wirex United Kingdom, Wirex United States. So ngay co du lieu: 365. So ngay co dau hieu (mot validator duoi 90% hoac to chuc duoi 99%): 46.

- Ngay dau tien co dau hieu: **2022-04-30**, tuc 228 ngay truoc moc 2022-12-14 (roi top tier).
- So ngay CA TO CHUC khong kha dung mot phan (duoi 99%): 25, dau tien 2022-04-30.

Theo thang:

| Thang | Ngay co dau hieu | Wirex Singapore | Wirex United Kingdom | Wirex United States | To chuc |
|---|---|---|---|---|---|
| 2022-01 | 0 | 100% | 100% | 100% | 100% |
| 2022-02 | 0 | 100% | 100% | 100% | 100% |
| 2022-03 | 0 | 100% | 100% | 100% | 100% |
| 2022-04 | 1 | 100% | 100% | 100% | 100% |
| 2022-05 | 2 | 100% | 99% | 100% | 100% |
| 2022-06 | 1 | 100% | 100% | 100% | 100% |
| 2022-07 | 12 | 94% | 82% | 82% | 94% |
| 2022-08 | 5 | 98% | 99% | 96% | 100% |
| 2022-09 | 0 | 100% | 100% | 100% | 100% |
| 2022-10 | 0 | 100% | 100% | 100% | 100% |
| 2022-11 | 0 | 100% | 100% | 100% | 100% |
| 2022-12 | 25 | 40% | 28% | 40% | 41% |

40 ngay co dau hieu dau tien:

| Ngay | Wirex Singapore | Wirex United Kingdom | Wirex United States | To chuc |
|---|---|---|---|---|
| 2022-04-30 | 100% | 98% | 99% | 99% |
| 2022-05-04 | 100% | 86% | 100% | 100% |
| 2022-05-18 | 99% | 97% | 98% | 98% |
| 2022-06-07 | 91% | 95% | 95% | 95% |
| 2022-07-10 | 100% | 100% | 20% | 100% |
| 2022-07-11 | 100% | 100% | 0% | 100% |
| 2022-07-12 | 100% | 100% | 0% | 100% |
| 2022-07-13 | 25% | 41% | 0% | 25% |
| 2022-07-14 | 100% | 100% | 0% | 100% |
| 2022-07-15 | 100% | 100% | 36% | 100% |
| 2022-07-24 | 100% | 68% | 100% | 100% |
| 2022-07-25 | 100% | 0% | 100% | 100% |
| 2022-07-26 | 59% | 0% | 100% | 59% |
| 2022-07-27 | 22% | 0% | 91% | 22% |
| 2022-07-28 | 100% | 0% | 100% | 100% |
| 2022-07-29 | 100% | 47% | 100% | 100% |
| 2022-08-01 | 100% | 100% | 57% | 100% |
| 2022-08-02 | 100% | 100% | 59% | 100% |
| 2022-08-03 | 100% | 100% | 76% | 100% |
| 2022-08-05 | 100% | 64% | 99% | 100% |
| 2022-08-08 | 50% | 99% | 100% | 100% |
| 2022-12-02 | 82% | 100% | 100% | 100% |
| 2022-12-06 | 100% | 3% | 100% | 100% |
| 2022-12-07 | 100% | 0% | 100% | 100% |
| 2022-12-08 | 100% | 0% | 100% | 100% |
| 2022-12-09 | 100% | 0% | 100% | 100% |
| 2022-12-10 | 100% | 94% | 76% | 100% |
| 2022-12-13 | 57% | 57% | 57% | 57% |
| 2022-12-14 | 0% | 0% | 0% | 0% |
| 2022-12-15 | 0% | 0% | 0% | 0% |
| 2022-12-16 | 0% | 0% | 0% | 0% |
| 2022-12-17 | 0% | 0% | 0% | 0% |
| 2022-12-18 | 0% | 0% | 0% | 0% |
| 2022-12-19 | 0% | 0% | 0% | 0% |
| 2022-12-20 | 0% | 0% | 0% | 0% |
| 2022-12-21 | 0% | 0% | 0% | 0% |
| 2022-12-22 | 0% | 0% | 0% | 0% |
| 2022-12-23 | 0% | 0% | 0% | 0% |
| 2022-12-24 | 0% | 0% | 0% | 0% |
| 2022-12-25 | 0% | 0% | 0% | 0% |

## Dien bien SatoshiPay: 2025-01-01 den 2026-09-30 (moc: 2025-08-22, ngung ca 3 validator hon 3 ngay)

Validator: SatoshiPay Iowa, SatoshiPay Singapore, SatoshiPay Frankfurt. So ngay co du lieu: 638. So ngay co dau hieu (mot validator duoi 90% hoac to chuc duoi 99%): 157.

- Ngay dau tien co dau hieu: **2025-01-20**, tuc 214 ngay truoc moc 2025-08-22 (ngung ca 3 validator hon 3 ngay).
- So ngay CA TO CHUC khong kha dung mot phan (duoi 99%): 109, dau tien 2025-01-20.

Theo thang:

| Thang | Ngay co dau hieu | SatoshiPay Iowa | SatoshiPay Singapore | SatoshiPay Frankfurt | To chuc |
|---|---|---|---|---|---|
| 2025-01 | 9 | 100% | 93% | 98% | 100% |
| 2025-02 | 17 | 91% | 92% | 99% | 97% |
| 2025-03 | 10 | 93% | 99% | 100% | 100% |
| 2025-04 | 0 | 100% | 100% | 100% | 100% |
| 2025-05 | 0 | 99% | 100% | 100% | 100% |
| 2025-06 | 0 | 100% | 100% | 100% | 100% |
| 2025-07 | 0 | 100% | 100% | 100% | 100% |
| 2025-08 | 4 | 90% | 90% | 89% | 90% |
| 2025-09 | 1 | 100% | 100% | 99% | 100% |
| 2025-10 | 0 | 100% | 100% | 99% | 100% |
| 2025-11 | 0 | 100% | 100% | 99% | 100% |
| 2025-12 | 7 | 80% | 100% | 100% | 100% |
| 2026-01 | 5 | 98% | 96% | 100% | 100% |
| 2026-02 | 12 | 65% | 100% | 100% | 100% |
| 2026-03 | 0 | 100% | 100% | 100% | 100% |
| 2026-04 | 0 | 100% | 100% | 100% | 100% |
| 2026-05 | 6 | 99% | 100% | 88% | 100% |
| 2026-06 | 13 | 97% | 100% | 81% | 99% |
| 2026-07 | 12 | 69% | 70% | 68% | 70% |
| 2026-08 | 31 | 0% | 0% | 0% | 0% |
| 2026-09 | 30 | 0% | 0% | 0% | 0% |

40 ngay co dau hieu dau tien:

| Ngay | SatoshiPay Iowa | SatoshiPay Singapore | SatoshiPay Frankfurt | To chuc |
|---|---|---|---|---|
| 2025-01-20 | 100% | 64% | 99% | 99% |
| 2025-01-21 | 100% | 65% | 100% | 100% |
| 2025-01-22 | 100% | 68% | 100% | 100% |
| 2025-01-23 | 100% | 82% | 87% | 92% |
| 2025-01-24 | 100% | 89% | 99% | 99% |
| 2025-01-26 | 100% | 85% | 100% | 100% |
| 2025-01-27 | 100% | 75% | 100% | 100% |
| 2025-01-29 | 100% | 88% | 99% | 100% |
| 2025-01-30 | 100% | 97% | 98% | 99% |
| 2025-02-03 | 100% | 83% | 90% | 92% |
| 2025-02-12 | 85% | 98% | 96% | 95% |
| 2025-02-13 | 89% | 99% | 98% | 98% |
| 2025-02-14 | 89% | 99% | 98% | 98% |
| 2025-02-16 | 89% | 90% | 100% | 97% |
| 2025-02-17 | 87% | 91% | 100% | 97% |
| 2025-02-18 | 75% | 85% | 100% | 92% |
| 2025-02-19 | 84% | 86% | 100% | 97% |
| 2025-02-20 | 81% | 92% | 100% | 97% |
| 2025-02-21 | 80% | 95% | 98% | 97% |
| 2025-02-22 | 87% | 93% | 100% | 99% |
| 2025-02-23 | 92% | 92% | 100% | 98% |
| 2025-02-24 | 86% | 86% | 100% | 93% |
| 2025-02-25 | 75% | 58% | 96% | 83% |
| 2025-02-26 | 77% | 84% | 99% | 91% |
| 2025-02-27 | 90% | 85% | 100% | 97% |
| 2025-02-28 | 83% | 80% | 100% | 90% |
| 2025-03-02 | 81% | 83% | 100% | 91% |
| 2025-03-03 | 84% | 81% | 100% | 97% |
| 2025-03-04 | 85% | 100% | 100% | 100% |
| 2025-03-06 | 83% | 100% | 100% | 100% |
| 2025-03-07 | 77% | 100% | 100% | 100% |
| 2025-03-08 | 80% | 100% | 100% | 100% |
| 2025-03-09 | 81% | 100% | 100% | 100% |
| 2025-03-10 | 81% | 100% | 100% | 100% |
| 2025-03-12 | 90% | 100% | 100% | 100% |
| 2025-03-15 | 88% | 100% | 100% | 100% |
| 2025-08-22 | 66% | 66% | 65% | 66% |
| 2025-08-23 | 0% | 0% | 0% | 0% |
| 2025-08-24 | 0% | 0% | 0% | 0% |
| 2025-08-25 | 20% | 41% | 5% | 20% |
