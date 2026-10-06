# Daily availability of all top tier organizations and early warning scoring

Run at: 2026-10-06 16:22

14 organizations were in the top tier at some point; 52 membership samples; 18592 organization-days; 0 crawler outage days excluded.

## Organizations

| Organization | In top tier | Days | Validators | Outage days | Outcomes |
|---|---|---|---|---|---|
| LOBSTR | 2019-05-31 to 2026-10-06 | 2686 | 6 | 0 | none |
| SatoshiPay | 2019-05-31 to 2026-07-14 | 2602 | 3 | 5 | OUTAGE 2021-09-01; OUTAGE 2025-08-22; REMOVAL 2026-07-14 |
| Whalestack LLC (also COINQVEST LLC) | 2019-05-31 to 2025-01-09 | 2051 | 3 | 1 | OUTAGE 2023-11-08; REMOVAL 2025-01-09 |
| Stellar Development Foundation | 2019-05-31 to 2026-10-06 | 2686 | 3 | 1 | OUTAGE 2020-04-24 |
| Keybase | 2019-05-31 to 2022-03-13 | 1018 | 3 | 0 | REMOVAL 2022-03-13 |
| Blockdaemon Inc. | 2019-10-30 to 2026-10-06 | 2534 | 3 | 0 | none |
| Wirex Limited | 2020-01-31 to 2022-12-13 | 1048 | 3 | 4 | OUTAGE 2022-07-13; OUTAGE 2022-07-26; OUTAGE 2022-12-13; REMOVAL 2022-12-13 |
| Public Node | 2022-03-08 to 2026-10-06 | 1674 | 3 | 0 | none |
| Franklin Templeton | 2022-10-19 to 2026-10-06 | 1449 | 3 | 0 | none |
| Creit Technologies LLP | 2025-01-08 to 2026-10-06 | 637 | 3 | 0 | none |
| OBSRVR | 2026-07-15 to 2026-10-06 | 84 | 3 | 0 | none |
| Range | 2026-08-27 to 2026-10-06 | 41 | 3 | 0 | none |
| Figure Certificate Company | 2026-08-27 to 2026-10-06 | 41 | 3 | 0 | none |
| MoneyGram | 2026-08-27 to 2026-10-06 | 41 | 3 | 0 | none |

## Scoring of the three signals

Precision: share of signal episodes followed by an outage or removal of the same organization within W days. Recall: share of outcomes preceded by a signal episode within W days. Lead time: days from the first such episode to the outcome.

### S1: any validator < 90% or organization < 99%

108 episodes across 12 organizations.

| Window W | Min lead | Episodes | Followed by outcome | Precision | Outcomes | Preceded by episode | Recall | Lead time (days, median / min / max) |
|---|---|---|---|---|---|---|---|---|
| 30 | 0 | 108 | 8 | 7% | 11 | 9 | 82% | 3 / 0 / 16 |
| 90 | 0 | 108 | 16 | 15% | 11 | 9 | 82% | 42 / 0 / 87 |
| 180 | 0 | 108 | 22 | 20% | 11 | 10 | 91% | 153 / 0 / 165 |
| 365 | 0 | 108 | 34 | 31% | 11 | 11 | 100% | 248 / 0 / 326 |
| 30 | 7 | 108 | 3 | 3% | 11 | 4 | 36% | 11 / 7 / 16 |
| 90 | 7 | 108 | 11 | 10% | 11 | 7 | 64% | 62 / 11 / 87 |
| 180 | 7 | 108 | 18 | 17% | 11 | 8 | 73% | 156 / 62 / 165 |
| 365 | 7 | 108 | 31 | 29% | 11 | 10 | 91% | 252 / 62 / 326 |

### S2: organization < 99% on 3 of the trailing 7 days

15 episodes across 4 organizations.

| Window W | Min lead | Episodes | Followed by outcome | Precision | Outcomes | Preceded by episode | Recall | Lead time (days, median / min / max) |
|---|---|---|---|---|---|---|---|---|
| 30 | 0 | 15 | 2 | 13% | 11 | 2 | 18% | 28 / 27 / 28 |
| 90 | 0 | 15 | 3 | 20% | 11 | 2 | 18% | 83 / 27 / 83 |
| 180 | 0 | 15 | 5 | 33% | 11 | 2 | 18% | 131 / 27 / 131 |
| 365 | 0 | 15 | 7 | 47% | 11 | 3 | 27% | 189 / 131 / 324 |
| 30 | 7 | 15 | 2 | 13% | 11 | 2 | 18% | 28 / 27 / 28 |
| 90 | 7 | 15 | 3 | 20% | 11 | 2 | 18% | 83 / 27 / 83 |
| 180 | 7 | 15 | 5 | 33% | 11 | 2 | 18% | 131 / 27 / 131 |
| 365 | 7 | 15 | 7 | 47% | 11 | 3 | 27% | 189 / 131 / 324 |

### S3: a validator at <= 10% for a day or organization < 90%

35 episodes across 9 organizations.

| Window W | Min lead | Episodes | Followed by outcome | Precision | Outcomes | Preceded by episode | Recall | Lead time (days, median / min / max) |
|---|---|---|---|---|---|---|---|---|
| 30 | 0 | 35 | 9 | 26% | 11 | 10 | 91% | 7 / 0 / 29 |
| 90 | 0 | 35 | 12 | 34% | 11 | 10 | 91% | 7 / 0 / 71 |
| 180 | 0 | 35 | 16 | 46% | 11 | 10 | 91% | 149 / 0 / 178 |
| 365 | 0 | 35 | 17 | 49% | 11 | 10 | 91% | 153 / 0 / 326 |
| 30 | 7 | 35 | 4 | 11% | 11 | 5 | 45% | 15 / 7 / 29 |
| 90 | 7 | 35 | 7 | 20% | 11 | 5 | 45% | 15 / 7 / 71 |
| 180 | 7 | 35 | 12 | 34% | 11 | 7 | 64% | 153 / 15 / 178 |
| 365 | 7 | 35 | 14 | 40% | 11 | 7 | 64% | 155 / 15 / 326 |

## Outcomes and the earliest signal before each (within 365 days)

| Organization | Date | Kind | S1 first signal, lead days | S3 first signal, lead days |
|---|---|---|---|---|
| Keybase | 2022-03-13 | REMOVAL | 2021-08-26, 199 | 2021-10-11, 153 |
| SatoshiPay | 2021-09-01 | OUTAGE | 2020-12-23, 252 | 2021-04-22, 132 |
| SatoshiPay | 2025-08-22 | OUTAGE | 2024-12-17, 248 | 2025-02-25, 178 |
| SatoshiPay | 2026-07-14 | REMOVAL | 2025-08-22, 326 | 2025-08-22, 326 |
| Stellar Development Foundation | 2020-04-24 | OUTAGE | 2020-02-22, 62 | 2020-04-24, 0 |
| Whalestack LLC | 2023-11-08 | OUTAGE | 2023-11-08, 0 | 2023-11-08, 0 |
| Whalestack LLC | 2025-01-09 | REMOVAL | 2024-04-06, 278 | none |
| Wirex Limited | 2022-07-13 | OUTAGE | 2021-11-03, 252 | 2022-07-11, 2 |
| Wirex Limited | 2022-07-26 | OUTAGE | 2021-11-03, 265 | 2022-07-11, 15 |
| Wirex Limited | 2022-12-13 | OUTAGE | 2022-04-30, 227 | 2022-07-11, 155 |
| Wirex Limited | 2022-12-13 | REMOVAL | 2022-04-30, 227 | 2022-07-11, 155 |

## Notes

- Membership is sampled once per stable configuration state, so an organization that joined and left between two samples is missed.
- A REMOVAL is counted whenever an organization's last membership day is more than 3 days before the data end, whatever the reason (failure, voluntary exit, or a change of organization id in Radar). Check each against membership.csv.
- Organization availability is Radar's isSubQuorumAvailableCount / crawlCount; validator availability is isValidatingCount / crawlCount.
- Thresholds (90%, 99%, 10%, 75%, 7 day gap, 7 day minimum lead) are starting points. The proposal should report the score of the rule finally chosen, with thresholds picked on 2019-2023 and tested on 2024-2026.

