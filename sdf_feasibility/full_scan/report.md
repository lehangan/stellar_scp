# Quet toan bo lich su mang Stellar

Chay luc: 2026-10-02 11:09

Du lieu: 2019-05-31 den 2026-10-01, 1214403 lan quet hop le (tong 1214403), 0 ngay tai loi.

## KET LUAN THEO QUY TAC DUNG

- A. Dot tai cau hinh co trang thai trung gian yeu keo dai >= 1 gio: **6** (tren tong 19 dot; them 0 dot co trang thai yeu nhung duoi 1 gio)
- B. Dot bien thuc te <= 1 to chuc keo dai >= 60 phut: **1** (tong so dot bien <= 1 bat ky do dai: 115)
- Tham khao: dot bien mong (thuc te < danh nghia) >= 1 gio: 32; >= 6 gio: 4; >= 24 gio: 3
- Tham khao: dot mat quorum intersection >= 1 gio: 0 (tong 0 dot bat ky do dai)

**=> DAT nguong di tiep: co bang chung lich su cho bai toan thu tu tai cau hinh va co ca bien an toan xuong muc nguy hiem keo dai.** Can doc ky tung ca ben duoi truoc khi tin.

## A. Cac dot tai cau hinh

52 trang thai cau hinh on dinh, 19 dot tai cau hinh, bo 236 doan nhieu ngan hon 5 lan quet.

Thu tu chi so: topTierSize / topTierOrgsSize / minBlockingSetSize / minBlockingSetOrgsSize / minSplittingSetSize / minSplittingSetOrgsSize

| Bat dau | Ket thuc | Trung gian | Dau | Cuoi | Trang thai yeu |
|---|---|---|---|---|---|
| 2019-06-04T11:06 | 2019-06-10T06:42 | 1 | 17/17/4/4/2/2 | 17/5/4/2/3/3 | khong |
| 2019-10-30T15:52 | 2019-10-30T16:15 | 1 | 17/5/4/2/3/3 | 20/6/4/2/4/4 | khong |
| 2020-01-31T23:25 | 2020-02-05T14:09 | 1 | 20/6/4/2/4/4 | 23/7/6/3/3/3 | khong |
| 2020-05-22T07:24 | 2020-05-29T18:29 | 1 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | minBlockingSetSize=4 trong 7.5 ngay; minBlockingSetOrgsSize=2 trong 7.5 ngay |
| 2021-04-06T17:04 | 2021-04-19T08:20 | 7 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | minBlockingSetSize=5 trong 20 phut; minBlockingSetSize=4 trong 1.3 ngay; minBlockingSetOrgsSize=2 trong 1.3 ngay; minBlockingSetSize=5 trong 5.4 gio; minBlockingSetSize=5 trong 23 phut |
| 2022-02-26T00:03 | 2022-03-22T00:33 | 5 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | minBlockingSetSize=5 trong 2.4 ngay |
| 2022-06-24T06:40 | 2022-06-24T07:15 | 1 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | khong |
| 2022-07-10T04:46 | 2022-07-25T09:52 | 4 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | minBlockingSetSize=5 trong 3.1 ngay; minBlockingSetSize=4 trong 12.6 gio; minBlockingSetOrgsSize=2 trong 12.6 gio; minBlockingSetSize=5 trong 17.6 gio |
| 2022-10-19T21:59 | 2022-10-19T21:59 | 0 | 23/7/6/3/3/3 | 26/8/6/3/3/3 | khong |
| 2022-11-04T18:20 | 2022-11-04T18:20 | 0 | 26/8/6/3/3/3 | 26/8/6/3/4/3 | khong |
| 2022-12-13T23:25 | 2022-12-14T15:46 | 1 | 26/8/6/3/4/3 | 23/7/6/3/3/3 | khong |
| 2023-07-03T09:14 | 2023-07-03T09:14 | 0 | 23/7/6/3/3/3 | 24/8/6/3/3/3 | khong |
| 2023-09-15T16:21 | 2023-09-15T16:21 | 0 | 24/8/6/3/3/3 | 23/7/6/3/3/3 | khong |
| 2024-10-03T18:03 | 2024-10-08T09:20 | 1 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | minBlockingSetSize=5 trong 4.6 ngay |
| 2025-01-08T17:48 | 2025-01-10T14:08 | 1 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | khong |
| 2025-04-23T12:22 | 2025-04-23T18:32 | 1 | 23/7/6/3/3/3 | 21/7/6/3/3/3 | khong |
| 2026-07-15T10:16 | 2026-07-15T21:06 | 1 | 21/7/6/3/3/3 | 21/7/6/3/3/3 | khong |
| 2026-08-27T09:23 | 2026-08-28T08:26 | 4 | 21/7/6/3/3/3 | 30/10/8/4/4/4 | khong |
| 2026-10-01T08:09 | 2026-10-01T21:24 | 2 | 30/10/8/4/4/4 | 30/10/8/4/4/1 | minSplittingSetOrgsSize=0 trong 1.2 gio |

## B. Bien an toan mong

Tong 1487 dot sau khi gop (1886 dot tho). Phan bo theo do dai:

- duoi 15 phut: 1247 dot
- 15 phut - 1 gio: 208 dot
- 1 - 6 gio: 28 dot
- 6 - 24 gio: 1 dot
- tren 24 gio: 3 dot

Theo nam (chi tinh dot >= 1 gio):

- 2019: 1 dot, tong 1.3 gio, bien thap nhat 3
- 2020: 6 dot, tong 16.2 gio, bien thap nhat 1
- 2021: 5 dot, tong 15.2 gio, bien thap nhat 1
- 2022: 3 dot, tong 2.5 ngay, bien thap nhat 1
- 2023: 4 dot, tong 8.9 gio, bien thap nhat 0
- 2024: 2 dot, tong 6.0 gio, bien thap nhat 2
- 2025: 11 dot, tong 3.8 ngay, bien thap nhat 2

30 dot dai nhat:

| Bat dau | Do dai | Bien thuc te thap nhat | Bien danh nghia |
|---|---|---|---|
| 2025-08-22T15:51 | 3.1 ngay | 2 | 3 |
| 2022-07-26T14:09 | 1.2 ngay | 1 | 3 |
| 2022-12-13T13:26 | 1.1 ngay | 2 | 3 |
| 2020-04-23T23:33 | 7.7 gio | 1 | 3 |
| 2021-09-01T09:48 | 5.1 gio | 2 | 3 |
| 2022-07-13T19:03 | 4.9 gio | 2 | 3 |
| 2021-04-06T14:34 | 3.9 gio | 1 | 3 |
| 2024-02-14T06:52 | 3.9 gio | 2 | 3 |
| 2021-09-01T04:47 | 3.8 gio | 2 | 3 |
| 2023-09-14T01:59 | 3.2 gio | 0 | 3 |
| 2025-03-02T15:00 | 3.1 gio | 2 | 3 |
| 2020-05-31T11:20 | 2.5 gio | 2 | 3 |
| 2023-09-14T09:11 | 2.4 gio | 0 | 3 |
| 2025-02-25T03:00 | 2.4 gio | 2 | 3 |
| 2025-09-18T01:55 | 2.3 gio | 2 | 3 |
| 2024-10-04T12:34 | 2.1 gio | 2 | 3 |
| 2020-06-02T14:47 | 2.0 gio | 1 | 3 |
| 2023-09-14T06:35 | 1.8 gio | 1 | 3 |
| 2020-05-10T16:43 | 1.5 gio | 1 | 3 |
| 2025-02-26T14:02 | 1.5 gio | 2 | 3 |
| 2020-05-21T13:31 | 1.4 gio | 2 | 3 |
| 2025-02-18T13:48 | 1.4 gio | 2 | 3 |
| 2023-08-24T12:17 | 1.4 gio | 2 | 3 |
| 2019-06-05T17:07 | 1.3 gio | 3 | 4 |
| 2025-02-28T15:02 | 1.2 gio | 2 | 3 |
| 2021-10-13T07:26 | 1.2 gio | 2 | 3 |
| 2025-02-28T01:29 | 1.2 gio | 2 | 3 |
| 2021-09-13T23:12 | 1.2 gio | 2 | 3 |
| 2025-02-26T18:17 | 1.1 gio | 2 | 3 |
| 2020-05-15T19:44 | 1.1 gio | 1 | 3 |

### Cac dot bien thuc te <= 1 to chuc (20 dot dai nhat)

| Bat dau | Do dai | Thap nhat | Bien danh nghia luc do |
|---|---|---|---|
| 2021-04-06T14:34 | 3.9 gio | 1 | 3 |
| 2023-09-14T04:56 | 14 phut | 0 | 3 |
| 2019-12-18T12:41 | 8 phut | 1 | 2 |
| 2023-09-14T11:08 | 8 phut | 1 | 3 |
| 2023-09-14T10:56 | 8 phut | 0 | 3 |
| 2023-09-14T10:44 | 8 phut | 1 | 3 |
| 2023-09-14T03:41 | 8 phut | 1 | 3 |
| 2023-09-14T09:53 | 8 phut | 1 | 3 |
| 2023-09-14T10:35 | 8 phut | 0 | 3 |
| 2019-06-28T12:57 | 5 phut | 1 | 2 |
| 2019-07-09T07:48 | 5 phut | 1 | 2 |
| 2019-10-06T13:17 | 5 phut | 1 | 2 |
| 2019-10-08T01:18 | 5 phut | 1 | 2 |
| 2019-10-08T15:15 | 5 phut | 1 | 2 |
| 2019-10-08T16:25 | 5 phut | 1 | 2 |
| 2019-10-12T16:31 | 5 phut | 1 | 2 |
| 2019-10-17T12:44 | 5 phut | 1 | 2 |
| 2019-10-17T12:50 | 5 phut | 1 | 2 |
| 2019-10-17T13:38 | 5 phut | 1 | 2 |
| 2019-10-18T08:56 | 5 phut | 1 | 2 |

## C. Mat quorum intersection

Khong co lan quet nao mat quorum intersection.

## Gioi han cua phan tich nay

- Chi dung 4 chi so resilience ma Radar tinh san; trang thai 'yeu' theo chi so khac se khong hien ra.
- Trang thai ton tai duoi 5 lan quet bi coi la nhieu va bo qua.
- Bien danh nghia thap o giai doan 2019 (blocking set to chuc = 2) lam tang so dot bien <= 1 cua nam do.
- So lieu la cua crawler Radar; node crawler mat ket noi co the tao dot bien mong gia.

