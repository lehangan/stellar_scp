# Daily availability of all top tier organizations and early warning scoring

Run at: 2026-10-06 14:06

17 organizations were in the top tier at some point; 52 membership samples; 18598 organization-days; 0 crawler outage days excluded.

## Organizations

| Organization | In top tier | Days | Validators | Outage days | Outcomes |
|---|---|---|---|---|---|
| LOBSTR | 2019-06-10 to 2026-10-06 | 2676 | 6 | 0 | none |
| Keybase | 2019-06-10 to 2022-03-13 | 1008 | 3 | 0 | REMOVAL 2022-03-13 |
| SatoshiPay | 2019-06-10 to 2026-08-27 | 2636 | 3 | 39 | OUTAGE 2025-08-23; OUTAGE 2026-07-23; REMOVAL 2026-08-27 |
| COINQVEST LLC | 2019-06-10 to 2024-10-02 | 1942 | 3 | 0 | REMOVAL 2024-10-02 |
| Stellar Development Foundation | 2019-06-10 to 2026-10-06 | 2676 | 3 | 0 | none |
| Blockdaemon Inc. | 2019-10-30 to 2026-10-06 | 2534 | 3 | 0 | none |
| Wirex Limited | 2020-01-31 to 2022-12-13 | 1048 | 3 | 2 | OUTAGE 2022-07-13; OUTAGE 2022-07-27; REMOVAL 2022-12-13 |
| Muyu Network | 2021-04-13 to 2021-04-18 | 6 | 4 | 0 | REMOVAL 2021-04-18 |
| SAKKEX OÜ | 2021-04-13 to 2021-04-18 | 6 | 3 | 0 | REMOVAL 2021-04-18 |
| Public Node | 2022-03-08 to 2026-10-06 | 1674 | 3 | 0 | none |
| Franklin Templeton | 2022-10-19 to 2026-10-06 | 1449 | 3 | 0 | none |
| Whalestack LLC | 2024-10-03 to 2025-01-09 | 99 | 3 | 0 | REMOVAL 2025-01-09 |
| Creit Technologies LLP | 2025-01-08 to 2026-10-06 | 637 | 3 | 0 | none |
| OBSRVR | 2026-07-15 to 2026-10-06 | 84 | 3 | 0 | none |
| Range | 2026-08-27 to 2026-10-06 | 41 | 3 | 0 | none |
| Figure Certificate Company | 2026-08-27 to 2026-10-06 | 41 | 3 | 0 | none |
| MoneyGram | 2026-08-27 to 2026-10-06 | 41 | 3 | 0 | none |

## Scoring of the three signals

Precision: share of signal episodes followed by an outage or removal of the same organization within W days. Recall: share of outcomes preceded by a signal episode within W days. Lead time: days from the first such episode to the outcome.

### S1: any validator < 90% or organization < 99%

105 episodes across 13 organizations.

| Window W | Episodes | Followed by outcome | Precision | Outcomes | Preceded by episode | Recall | Lead time (days, median / min / max) |
|---|---|---|---|---|---|---|---|
| 30 | 105 | 6 | 6% | 11 | 6 | 55% | 9 / 1 / 17 |
| 90 | 105 | 11 | 10% | 11 | 7 | 64% | 74 / 1 / 89 |
| 180 | 105 | 15 | 14% | 11 | 9 | 82% | 116 / 1 / 179 |
| 365 | 105 | 23 | 22% | 11 | 9 | 82% | 249 / 2 / 345 |

### S2: organization < 99% on 3 of the trailing 7 days

16 episodes across 4 organizations.

| Window W | Episodes | Followed by outcome | Precision | Outcomes | Preceded by episode | Recall | Lead time (days, median / min / max) |
|---|---|---|---|---|---|---|---|
| 30 | 16 | 0 | 0% | 11 | 0 | 0% | - |
| 90 | 16 | 2 | 12% | 11 | 2 | 18% | 71 / 36 / 71 |
| 180 | 16 | 2 | 12% | 11 | 2 | 18% | 71 / 36 / 71 |
| 365 | 16 | 4 | 25% | 11 | 3 | 27% | 190 / 71 / 333 |

### S3: a validator at <= 10% for a day or organization < 90%

35 episodes across 9 organizations.

| Window W | Episodes | Followed by outcome | Precision | Outcomes | Preceded by episode | Recall | Lead time (days, median / min / max) |
|---|---|---|---|---|---|---|---|
| 30 | 35 | 7 | 20% | 11 | 7 | 64% | 2 / 1 / 21 |
| 90 | 35 | 11 | 31% | 11 | 8 | 73% | 16 / 1 / 84 |
| 180 | 35 | 14 | 40% | 11 | 8 | 73% | 153 / 1 / 179 |
| 365 | 35 | 15 | 43% | 11 | 8 | 73% | 155 / 1 / 335 |

## Outcomes

| Organization | Date | Kind |
|---|---|---|
| COINQVEST LLC | 2024-10-02 | REMOVAL |
| Keybase | 2022-03-13 | REMOVAL |
| Muyu Network | 2021-04-18 | REMOVAL |
| SAKKEX OÜ | 2021-04-18 | REMOVAL |
| SatoshiPay | 2025-08-23 | OUTAGE |
| SatoshiPay | 2026-07-23 | OUTAGE |
| SatoshiPay | 2026-08-27 | REMOVAL |
| Whalestack LLC | 2025-01-09 | REMOVAL |
| Wirex Limited | 2022-07-13 | OUTAGE |
| Wirex Limited | 2022-07-27 | OUTAGE |
| Wirex Limited | 2022-12-13 | REMOVAL |

## Notes

- Membership is sampled once per stable configuration state, so an organization that joined and left between two samples is missed.
- A REMOVAL is counted whenever an organization's last membership day is more than 3 days before the data end, whatever the reason (failure, voluntary exit, or a change of organization id in Radar). Check each against membership.csv.
- Organization availability is Radar's isSubQuorumAvailableCount / crawlCount; validator availability is isValidatingCount / crawlCount.
- Thresholds (90%, 99%, 10%, 50%, 7 day gap) are starting points. The proposal should report the score of the rule finally chosen, with thresholds picked on 2019-2023 and tested on 2024-2026.

