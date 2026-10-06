# Kiem chung cac ca lon

Chay luc: 2026-10-02 11:24

Gio trong bao cao la UTC. 'Ngung' = Radar ghi validator do khong validating tai thoi diem do.

## Tom tat

| Ca | Thoi diem | To chuc top tier mat da so validator | Tong validator top tier ngung | Nhan dinh |
|---|---|---|---|---|
| 2020-04-23 | 2020-04-24T01:00 | Stellar Development Foundation | 3/23 | su co that o 1 to chuc |
| 2020-04-23 | 2020-04-24T05:00 | Stellar Development Foundation | 3/23 | su co that o 1 to chuc |
| 2020-05-22 | 2020-05-23T12:00 | - | 0/23 | khong to chuc nao mat da so; co THAY DOI CAU HINH (xem chi tiet) |
| 2020-05-22 | 2020-05-27T12:00 | - | 0/23 | khong to chuc nao mat da so; co THAY DOI CAU HINH (xem chi tiet) |
| 2021-04-06 | 2021-04-06T10:00 | - | 0/23 | khong to chuc nao mat da so, cau hinh khong doi: chi so giam khong giai thich duoc bang snapshot nay |
| 2021-04-06 | 2021-04-06T16:00 | LOBSTR, Stellar Development Foundation | 8/23 | su co that, 2 to chuc ngung dong thoi |
| 2021-04-06 | 2021-04-07T12:00 | - | 0/23 | khong to chuc nao mat da so; co THAY DOI CAU HINH (xem chi tiet) |
| 2022-07-26 | 2022-07-26T20:00 | Wirex Limited | 2/23 | su co that o 1 to chuc |
| 2022-07-26 | 2022-07-27T08:00 | Wirex Limited | 3/23 | su co that o 1 to chuc |
| 2022-12-13 | 2022-12-13T20:00 | Wirex Limited | 3/26 | su co that o 1 to chuc |
| 2022-12-13 | 2022-12-15T12:00 | Wirex Limited | 3/26 | su co that o 1 to chuc |
| 2023-09-14 | 2023-09-14T05:00 | Blockdaemon Inc., COINQVEST LLC, Franklin Templeton, LOBSTR, Public Node, SatoshiPay, Stellar Development Foundation, lobstr.co | 24/24 | 8 to chuc 'ngung' cung luc (100% validator): NGHI LOI CRAWLER |
| 2023-09-14 | 2023-09-14T10:58 | Public Node, SatoshiPay, lobstr.co | 8/24 | su co that, 3 to chuc ngung dong thoi |
| 2023-09-14 | 2023-09-16T12:00 | lobstr.co | 1/24 | su co that o 1 to chuc |
| 2024-10-03 | 2024-10-05T12:00 | - | 0/23 | khong to chuc nao mat da so; co THAY DOI CAU HINH (xem chi tiet) |
| 2025-08-22 | 2025-08-23T12:00 | SatoshiPay | 3/21 | su co that o 1 to chuc |
| 2025-08-22 | 2025-08-25T06:00 | SatoshiPay | 3/21 | su co that o 1 to chuc |
| 2026-10-01 | 2026-10-01T09:00 | - | 0/30 | khong to chuc nao mat da so, cau hinh khong doi: chi so giam khong giai thich duoc bang snapshot nay |
| 2026-10-01 | 2026-10-01T23:00 | - | 0/30 | khong to chuc nao mat da so, cau hinh khong doi: chi so giam khong giai thich duoc bang snapshot nay |

Cach doc cot nhan dinh:
- 'su co that o 1 to chuc': dung kieu su kien SDF goi y (bao truoc cho node operator).
- 'NGHI LOI CRAWLER': qua nua validator top tier cung ngung, kho la su co that; khong nen dua vao proposal.
- 'THAY DOI CAU HINH': bien giam do quorum set hoac thanh vien top tier doi, khong phai do node hong.
- Top tier o day la transitive quorum set do Radar tinh tai thoi diem doi chung (xap xi).


## 2020-04-23: Bien thuc te con 1 to chuc trong 7,7 gio

**Doi chung 2020-04-23T18:00** (snapshot 2020-04-23T17:58:45.726Z): top tier 23 validator, 7 to chuc.

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2020-04-24T01:00** (snapshot 2020-04-24T00:57:26.005Z): su co that o 1 to chuc

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST Limited: 3/3 dang validating
- Keybase: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 0/3 dang validating (ngung: SDF 2, SDF 1, SDF 3)  <-- MAT DA SO
- Wirex Limited: 3/3 dang validating

**2020-04-24T05:00** (snapshot 2020-04-24T04:57:01.738Z): su co that o 1 to chuc

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST Limited: 3/3 dang validating
- Keybase: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 0/3 dang validating (ngung: SDF 2, SDF 1, SDF 3)  <-- MAT DA SO
- Wirex Limited: 3/3 dang validating


## 2020-05-22: Bien danh nghia giam (blocking set 6 -> 4) trong 7,5 ngay

**Doi chung 2020-05-21T12:00** (snapshot 2020-05-21T11:57:16.058Z): top tier 23 validator, 7 to chuc.

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2020-05-23T12:00** (snapshot 2020-05-23T11:57:43.300Z): khong to chuc nao mat da so; co THAY DOI CAU HINH (xem chi tiet)

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=4, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=2, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST Limited: 3/3 dang validating
- Keybase: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating
- Wirex Limited: 3/3 dang validating
- Validator top tier DOI quorum set so voi doi chung: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3

**2020-05-27T12:00** (snapshot 2020-05-27T11:57:34.756Z): khong to chuc nao mat da so; co THAY DOI CAU HINH (xem chi tiet)

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=4, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=2, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST Limited: 3/3 dang validating
- Keybase: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating
- Wirex Limited: 3/3 dang validating
- Validator top tier DOI quorum set so voi doi chung: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3


## 2021-04-06: SDF dung validator (da co thong cao); bien con 1 to chuc tu 14:34 trong 3,9 gio

**Doi chung 2021-04-05T12:00** (snapshot 2021-04-05T11:59:36.929Z): top tier 23 validator, 7 to chuc.

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2021-04-06T10:00** (snapshot 2021-04-06T09:58:18.206Z): khong to chuc nao mat da so, cau hinh khong doi: chi so giam khong giai thich duoc bang snapshot nay

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST OÜ: 3/3 dang validating
- Keybase: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating
- Wirex Limited: 3/3 dang validating

**2021-04-06T16:00** (snapshot 2021-04-06T15:59:23.775Z): su co that, 2 to chuc ngung dong thoi

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=2, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=1, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST OÜ: 3/3 dang validating
- Keybase: 3/3 dang validating
- LOBSTR: 0/5 dang validating (ngung: LOBSTR 2 (Europe), LOBSTR 5 (Australia), LOBSTR 3 (North America), LOBSTR 1 (Europe), LOBSTR 4 (Asia))  <-- MAT DA SO
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 0/3 dang validating (ngung: SDF 2, SDF 1, SDF 3)  <-- MAT DA SO
- Wirex Limited: 3/3 dang validating

**2021-04-07T12:00** (snapshot 2021-04-07T11:57:48.250Z): khong to chuc nao mat da so; co THAY DOI CAU HINH (xem chi tiet)

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=4, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=2, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST OÜ: 3/3 dang validating
- Keybase: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating
- Wirex Limited: 3/3 dang validating
- Validator top tier DOI quorum set so voi doi chung: SDF 1, SDF 2, SDF 3


## 2022-07-26: Bien thuc te mong 1,2 ngay, co luc con 1 to chuc

**Doi chung 2022-07-26T08:00** (snapshot 2022-07-26T07:58:51.547Z): top tier 23 validator, 7 to chuc.

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=5, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

Da ngung tu truoc: Wirex Limited: Wirex United Kingdom

**2022-07-26T20:00** (snapshot 2022-07-26T19:57:49.344Z): su co that o 1 to chuc

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST LLC: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- Public Node: 3/3 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating
- Wirex Limited: 1/3 dang validating (ngung: Wirex United Kingdom, Wirex Singapore)  <-- MAT DA SO

**2022-07-27T08:00** (snapshot 2022-07-27T07:57:50.357Z): su co that o 1 to chuc

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST LLC: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- Public Node: 3/3 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating
- Wirex Limited: 0/3 dang validating (ngung: Wirex United Kingdom, Wirex Singapore, Wirex United States)  <-- MAT DA SO


## 2022-12-13: Bien mong 1,1 ngay roi top tier tu 8 ve 7 to chuc

**Doi chung 2022-12-13T06:00** (snapshot 2022-12-13T05:59:12.772Z): top tier 26 validator, 8 to chuc.

Chi so: topTierSize=26, topTierOrgsSize=8, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=4, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2022-12-13T20:00** (snapshot 2022-12-13T19:58:40.851Z): su co that o 1 to chuc

Chi so: topTierSize=26, topTierOrgsSize=8, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=4, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST LLC: 3/3 dang validating
- Franklin Templeton: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- Public Node: 3/3 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating
- Wirex Limited: 0/3 dang validating (ngung: Wirex United Kingdom, Wirex Singapore, Wirex United States)  <-- MAT DA SO
- Validator top tier DOI quorum set so voi doi chung: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong), SDF 1, SDF 2, SDF 3

**2022-12-15T12:00** (snapshot 2022-12-15T11:59:44.766Z): su co that o 1 to chuc

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST LLC: 3/3 dang validating
- Franklin Templeton: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- Public Node: 3/3 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating
- Wirex Limited: 0/3 dang validating (ngung: Wirex United Kingdom, Wirex Singapore, Wirex United States)  <-- MAT DA SO
- Roi transitive quorum set so voi doi chung: Wirex Singapore, Wirex United Kingdom, Wirex United States
- Validator top tier DOI quorum set so voi doi chung: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3, Boötes, COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong), FT SCV 1, FT SCV 2, FT SCV 3, Hercules, LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (India), Lyra by BP Ventures, SDF 1, SDF 2, SDF 3, SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)


## 2023-09-14: Bien thuc te ve 0 nhieu lan trong 9 gio (nghi loi do)

**Doi chung 2023-09-13T18:00** (snapshot 2023-09-13T17:57:38.527Z): top tier 24 validator, 8 to chuc.

Chi so: topTierSize=24, topTierOrgsSize=8, minBlockingSetSize=6, minBlockingSetFilteredSize=5, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

Da ngung tu truoc: Public Node: Lyra by BP Ventures; lobstr.co: LOBSTR 2 (Europe)

**2023-09-14T05:00** (snapshot 2023-09-14T04:59:12.091Z): 8 to chuc 'ngung' cung luc (100% validator): NGHI LOI CRAWLER

Chi so: topTierSize=24, topTierOrgsSize=8, minBlockingSetSize=6, minBlockingSetFilteredSize=0, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=0, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 0/3 dang validating (ngung: Blockdaemon Validator 2, Blockdaemon Validator 3, Blockdaemon Validator 1)  <-- MAT DA SO
- COINQVEST LLC: 0/3 dang validating (ngung: COINQVEST (Hong Kong), COINQVEST (Germany), COINQVEST (Finland))  <-- MAT DA SO
- Franklin Templeton: 0/3 dang validating (ngung: FT SCV 1, FT SCV 3, FT SCV 2)  <-- MAT DA SO
- LOBSTR: 0/5 dang validating (ngung: LOBSTR 5 (India), LOBSTR 3 (North America), LOBSTR 1 (Europe), LOBSTR 4 (Asia), LOBSTR 2 (Europe))  <-- MAT DA SO
- Public Node: 0/3 dang validating (ngung: Hercules by OG Technologies, Lyra by BP Ventures, Boötes)  <-- MAT DA SO
- SatoshiPay: 0/3 dang validating (ngung: SatoshiPay Frankfurt, SatoshiPay Singapore, SatoshiPay Iowa)  <-- MAT DA SO
- Stellar Development Foundation: 0/3 dang validating (ngung: SDF 1, SDF 2, SDF 3)  <-- MAT DA SO
- lobstr.co: 0/1 dang validating (ngung: LOBSTR 2 (Europe))  <-- MAT DA SO

**2023-09-14T10:58** (snapshot 2023-09-14T10:56:13.115Z): su co that, 3 to chuc ngung dong thoi

Chi so: topTierSize=24, topTierOrgsSize=8, minBlockingSetSize=6, minBlockingSetFilteredSize=1, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=1, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST LLC: 3/3 dang validating
- Franklin Templeton: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- Public Node: 0/3 dang validating (ngung: Hercules by OG Technologies, Lyra by BP Ventures, Boötes)  <-- MAT DA SO
- SatoshiPay: 0/3 dang validating (ngung: SatoshiPay Frankfurt, SatoshiPay Singapore, SatoshiPay Iowa)  <-- MAT DA SO
- Stellar Development Foundation: 2/3 dang validating (ngung: SDF 2)
- lobstr.co: 0/1 dang validating (ngung: LOBSTR 2 (Europe))  <-- MAT DA SO

**2023-09-16T12:00** (snapshot 2023-09-16T11:57:40.620Z): su co that o 1 to chuc

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- COINQVEST LLC: 3/3 dang validating
- Franklin Templeton: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- Public Node: 3/3 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating
- lobstr.co: 0/1 dang validating (ngung: LOBSTR 2 (Europe))  <-- MAT DA SO
- Roi transitive quorum set so voi doi chung: LOBSTR 2 (Europe)
- Validator top tier DOI quorum set so voi doi chung: FT SCV 1, FT SCV 2, FT SCV 3


## 2024-10-03: Blocking set danh nghia 6 -> 5 trong 4,6 ngay

**Doi chung 2024-10-03T10:00** (snapshot 2024-10-03T09:57:08.972Z): top tier 23 validator, 7 to chuc.

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2024-10-05T12:00** (snapshot 2024-10-05T11:59:45.217Z): khong to chuc nao mat da so; co THAY DOI CAU HINH (xem chi tiet)

Chi so: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=5, minBlockingSetFilteredSize=5, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- Franklin Templeton: 3/3 dang validating
- LOBSTR: 5/5 dang validating
- Public Node: 3/3 dang validating
- SatoshiPay: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating
- Whalestack LLC: 3/3 dang validating
- Validator top tier DOI quorum set so voi doi chung: FT SCV 2


## 2025-08-22: Bien thuc te mong 3,1 ngay

**Doi chung 2025-08-22T08:00** (snapshot 2025-08-22T07:56:58.960Z): top tier 21 validator, 7 to chuc.

Chi so: topTierSize=21, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2025-08-23T12:00** (snapshot 2025-08-23T11:56:59.279Z): su co that o 1 to chuc

Chi so: topTierSize=21, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- Creit Technologies LLP: 3/3 dang validating
- Franklin Templeton: 3/3 dang validating
- LOBSTR: 3/3 dang validating
- Public Node: 3/3 dang validating
- SatoshiPay: 0/3 dang validating (ngung: SatoshiPay Frankfurt, SatoshiPay Singapore, SatoshiPay Iowa)  <-- MAT DA SO
- Stellar Development Foundation: 3/3 dang validating

**2025-08-25T06:00** (snapshot 2025-08-25T05:55:40.056Z): su co that o 1 to chuc

Chi so: topTierSize=21, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- Creit Technologies LLP: 3/3 dang validating
- Franklin Templeton: 3/3 dang validating
- LOBSTR: 3/3 dang validating
- Public Node: 3/3 dang validating
- SatoshiPay: 0/3 dang validating (ngung: SatoshiPay Frankfurt, SatoshiPay Singapore, SatoshiPay Iowa)  <-- MAT DA SO
- Stellar Development Foundation: 3/3 dang validating


## 2026-10-01: Splitting set to chuc 4 -> 0 -> 1 (nghi do Radar doi bo phan tich)

**Doi chung 2026-09-30T12:00** (snapshot 2026-09-30T11:56:35.166Z): top tier 30 validator, 10 to chuc.

Chi so: topTierSize=30, topTierOrgsSize=10, minBlockingSetSize=8, minBlockingSetFilteredSize=8, minBlockingSetOrgsSize=4, minBlockingSetOrgsFilteredSize=4, minSplittingSetSize=4, minSplittingSetOrgsSize=4, hasQuorumIntersection=True

**2026-10-01T09:00** (snapshot 2026-10-01T08:59:03.964Z): khong to chuc nao mat da so, cau hinh khong doi: chi so giam khong giai thich duoc bang snapshot nay

Chi so: topTierSize=30, topTierOrgsSize=10, minBlockingSetSize=8, minBlockingSetFilteredSize=8, minBlockingSetOrgsSize=4, minBlockingSetOrgsFilteredSize=4, minSplittingSetSize=4, minSplittingSetOrgsSize=1, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- Creit Technologies LLP: 3/3 dang validating
- Figure Certificate Company: 3/3 dang validating
- Franklin Templeton: 3/3 dang validating
- LOBSTR: 3/3 dang validating
- MoneyGram: 3/3 dang validating
- OBSRVR: 3/3 dang validating
- Public Node: 3/3 dang validating
- Range: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating

**2026-10-01T23:00** (snapshot 2026-10-01T22:57:29.805Z): khong to chuc nao mat da so, cau hinh khong doi: chi so giam khong giai thich duoc bang snapshot nay

Chi so: topTierSize=30, topTierOrgsSize=10, minBlockingSetSize=8, minBlockingSetFilteredSize=8, minBlockingSetOrgsSize=4, minBlockingSetOrgsFilteredSize=4, minSplittingSetSize=4, minSplittingSetOrgsSize=4, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 dang validating
- Creit Technologies LLP: 3/3 dang validating
- Figure Certificate Company: 3/3 dang validating
- Franklin Templeton: 3/3 dang validating
- LOBSTR: 3/3 dang validating
- MoneyGram: 3/3 dang validating
- OBSRVR: 3/3 dang validating
- Public Node: 3/3 dang validating
- Range: 3/3 dang validating
- Stellar Development Foundation: 3/3 dang validating

