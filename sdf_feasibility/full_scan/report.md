# Full history scan of the Stellar network

Run at: 2026-10-06 11:18

Data: 2019-05-31 to 2026-10-01, 1214403 valid scans (1214403 in total), 0 days failed to download.

## VERDICT UNDER THE STOPPING RULE

- A. Reconfiguration episodes with a weak intermediate state lasting >= 1 hour: **6** (out of 19 episodes; 0 more have a weak state shorter than 1 hour)
- B. Periods with effective margin <= 1 organization lasting >= 60 minutes: **1** (periods with margin <= 1 of any length: 115)
- For reference: thin margin periods (effective < nominal) >= 1 hour: 32; >= 6 hours: 4; >= 24 hours: 3
- For reference: periods without quorum intersection >= 1 hour: 0 (0 periods of any length)

**=> Threshold MET: there is historical evidence for the reconfiguration ordering problem and there is a sustained period with the liveness margin at a dangerous level.** Inspect each case below before relying on this.

## A. Reconfiguration episodes

52 stable configuration states, 19 reconfiguration episodes, 236 noise segments shorter than 5 scans dropped.

Order of metrics: topTierSize / topTierOrgsSize / minBlockingSetSize / minBlockingSetOrgsSize / minSplittingSetSize / minSplittingSetOrgsSize

| Start | End | Intermediate | First | Last | Weak state |
|---|---|---|---|---|---|
| 2019-06-04T11:06 | 2019-06-10T06:42 | 1 | 17/17/4/4/2/2 | 17/5/4/2/3/3 | none |
| 2019-10-30T15:52 | 2019-10-30T16:15 | 1 | 17/5/4/2/3/3 | 20/6/4/2/4/4 | none |
| 2020-01-31T23:25 | 2020-02-05T14:09 | 1 | 20/6/4/2/4/4 | 23/7/6/3/3/3 | none |
| 2020-05-22T07:24 | 2020-05-29T18:29 | 1 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | minBlockingSetSize=4 for 7.5 days; minBlockingSetOrgsSize=2 for 7.5 days |
| 2021-04-06T17:04 | 2021-04-19T08:20 | 7 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | minBlockingSetSize=5 for 20 min; minBlockingSetSize=4 for 1.3 days; minBlockingSetOrgsSize=2 for 1.3 days; minBlockingSetSize=5 for 5.4 h; minBlockingSetSize=5 for 23 min |
| 2022-02-26T00:03 | 2022-03-22T00:33 | 5 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | minBlockingSetSize=5 for 2.4 days |
| 2022-06-24T06:40 | 2022-06-24T07:15 | 1 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | none |
| 2022-07-10T04:46 | 2022-07-25T09:52 | 4 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | minBlockingSetSize=5 for 3.1 days; minBlockingSetSize=4 for 12.6 h; minBlockingSetOrgsSize=2 for 12.6 h; minBlockingSetSize=5 for 17.6 h |
| 2022-10-19T21:59 | 2022-10-19T21:59 | 0 | 23/7/6/3/3/3 | 26/8/6/3/3/3 | none |
| 2022-11-04T18:20 | 2022-11-04T18:20 | 0 | 26/8/6/3/3/3 | 26/8/6/3/4/3 | none |
| 2022-12-13T23:25 | 2022-12-14T15:46 | 1 | 26/8/6/3/4/3 | 23/7/6/3/3/3 | none |
| 2023-07-03T09:14 | 2023-07-03T09:14 | 0 | 23/7/6/3/3/3 | 24/8/6/3/3/3 | none |
| 2023-09-15T16:21 | 2023-09-15T16:21 | 0 | 24/8/6/3/3/3 | 23/7/6/3/3/3 | none |
| 2024-10-03T18:03 | 2024-10-08T09:20 | 1 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | minBlockingSetSize=5 for 4.6 days |
| 2025-01-08T17:48 | 2025-01-10T14:08 | 1 | 23/7/6/3/3/3 | 23/7/6/3/3/3 | none |
| 2025-04-23T12:22 | 2025-04-23T18:32 | 1 | 23/7/6/3/3/3 | 21/7/6/3/3/3 | none |
| 2026-07-15T10:16 | 2026-07-15T21:06 | 1 | 21/7/6/3/3/3 | 21/7/6/3/3/3 | none |
| 2026-08-27T09:23 | 2026-08-28T08:26 | 4 | 21/7/6/3/3/3 | 30/10/8/4/4/4 | none |
| 2026-10-01T08:09 | 2026-10-01T21:24 | 2 | 30/10/8/4/4/4 | 30/10/8/4/4/1 | minSplittingSetOrgsSize=0 for 1.2 h |

## B. Thin liveness margin

1487 periods after merging (1886 raw periods). Distribution by length:

- under 15 minutes: 1247 periods
- 15 minutes - 1 hour: 208 periods
- 1 - 6 hours: 28 periods
- 6 - 24 hours: 1 periods
- over 24 hours: 3 periods

By year (periods >= 1 hour only):

- 2019: 1 periods, total 1.3 h, lowest margin 3
- 2020: 6 periods, total 16.2 h, lowest margin 1
- 2021: 5 periods, total 15.2 h, lowest margin 1
- 2022: 3 periods, total 2.5 days, lowest margin 1
- 2023: 4 periods, total 8.9 h, lowest margin 0
- 2024: 2 periods, total 6.0 h, lowest margin 2
- 2025: 11 periods, total 3.8 days, lowest margin 2

30 longest periods:

| Start | Length | Lowest effective margin | Nominal margin |
|---|---|---|---|
| 2025-08-22T15:51 | 3.1 days | 2 | 3 |
| 2022-07-26T14:09 | 1.2 days | 1 | 3 |
| 2022-12-13T13:26 | 1.1 days | 2 | 3 |
| 2020-04-23T23:33 | 7.7 h | 1 | 3 |
| 2021-09-01T09:48 | 5.1 h | 2 | 3 |
| 2022-07-13T19:03 | 4.9 h | 2 | 3 |
| 2021-04-06T14:34 | 3.9 h | 1 | 3 |
| 2024-02-14T06:52 | 3.9 h | 2 | 3 |
| 2021-09-01T04:47 | 3.8 h | 2 | 3 |
| 2023-09-14T01:59 | 3.2 h | 0 | 3 |
| 2025-03-02T15:00 | 3.1 h | 2 | 3 |
| 2020-05-31T11:20 | 2.5 h | 2 | 3 |
| 2023-09-14T09:11 | 2.4 h | 0 | 3 |
| 2025-02-25T03:00 | 2.4 h | 2 | 3 |
| 2025-09-18T01:55 | 2.3 h | 2 | 3 |
| 2024-10-04T12:34 | 2.1 h | 2 | 3 |
| 2020-06-02T14:47 | 2.0 h | 1 | 3 |
| 2023-09-14T06:35 | 1.8 h | 1 | 3 |
| 2020-05-10T16:43 | 1.5 h | 1 | 3 |
| 2025-02-26T14:02 | 1.5 h | 2 | 3 |
| 2020-05-21T13:31 | 1.4 h | 2 | 3 |
| 2025-02-18T13:48 | 1.4 h | 2 | 3 |
| 2023-08-24T12:17 | 1.4 h | 2 | 3 |
| 2019-06-05T17:07 | 1.3 h | 3 | 4 |
| 2025-02-28T15:02 | 1.2 h | 2 | 3 |
| 2021-10-13T07:26 | 1.2 h | 2 | 3 |
| 2025-02-28T01:29 | 1.2 h | 2 | 3 |
| 2021-09-13T23:12 | 1.2 h | 2 | 3 |
| 2025-02-26T18:17 | 1.1 h | 2 | 3 |
| 2020-05-15T19:44 | 1.1 h | 1 | 3 |

### Periods with effective margin <= 1 organization (20 longest)

| Start | Length | Lowest | Nominal margin at the time |
|---|---|---|---|
| 2021-04-06T14:34 | 3.9 h | 1 | 3 |
| 2023-09-14T04:56 | 14 min | 0 | 3 |
| 2019-12-18T12:41 | 8 min | 1 | 2 |
| 2023-09-14T11:08 | 8 min | 1 | 3 |
| 2023-09-14T10:56 | 8 min | 0 | 3 |
| 2023-09-14T10:44 | 8 min | 1 | 3 |
| 2023-09-14T03:41 | 8 min | 1 | 3 |
| 2023-09-14T09:53 | 8 min | 1 | 3 |
| 2023-09-14T10:35 | 8 min | 0 | 3 |
| 2019-06-28T12:57 | 5 min | 1 | 2 |
| 2019-07-09T07:48 | 5 min | 1 | 2 |
| 2019-10-06T13:17 | 5 min | 1 | 2 |
| 2019-10-08T01:18 | 5 min | 1 | 2 |
| 2019-10-08T15:15 | 5 min | 1 | 2 |
| 2019-10-08T16:25 | 5 min | 1 | 2 |
| 2019-10-12T16:31 | 5 min | 1 | 2 |
| 2019-10-17T12:44 | 5 min | 1 | 2 |
| 2019-10-17T12:50 | 5 min | 1 | 2 |
| 2019-10-17T13:38 | 5 min | 1 | 2 |
| 2019-10-18T08:56 | 5 min | 1 | 2 |

## C. Loss of quorum intersection

No scan without quorum intersection.

## Limitations of this analysis

- Only the four resilience metrics precomputed by Radar are used; states that are 'weak' by another metric do not show up.
- States that last fewer than 5 scans are treated as noise and dropped.
- The low nominal margin in 2019 (organization blocking set = 2) inflates the number of periods with margin <= 1 for that year.
- The data come from Radar's crawler; a crawler that loses connectivity can create spurious thin margin periods.

