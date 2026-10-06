# Daily availability of all top tier organizations and early warning scoring

Run at: 2026-10-06 17:55

14 organizations were in the top tier at some point; 52 membership samples; 18592 organization-days; 0 crawler outage days excluded.

## Organizations

| Organization | In top tier | Days | Validators | Verified outages | Outcomes (merged) |
|---|---|---|---|---|---|
| Keybase | 2019-05-31 to 2022-03-13 | 1018 | 3 | 0 | REMOVAL 2022-03-13 |
| LOBSTR | 2019-05-31 to 2026-10-06 | 2686 | 6 | 1 | OUTAGE 2021-04-06 |
| Stellar Development Foundation | 2019-05-31 to 2026-10-06 | 2686 | 3 | 3 | OUTAGE 2020-04-23; OUTAGE 2020-05-10; OUTAGE 2021-04-06 |
| SatoshiPay | 2019-05-31 to 2026-07-14 | 2602 | 3 | 8 | OUTAGE 2020-05-31; OUTAGE 2021-09-01; OUTAGE 2021-10-13; OUTAGE 2024-02-14; OUTAGE 2025-02-18; OUTAGE 2025-08-22; REMOVAL 2026-07-14 |
| Whalestack LLC (also COINQVEST LLC) | 2019-05-31 to 2025-01-09 | 2051 | 3 | 0 | REMOVAL 2025-01-09 |
| Blockdaemon Inc. | 2019-10-30 to 2026-10-06 | 2534 | 3 | 0 | none |
| Wirex Limited | 2020-01-31 to 2022-12-13 | 1048 | 3 | 3 | OUTAGE 2022-07-13; OUTAGE 2022-07-26; OUTAGE+REMOVAL 2022-12-13 |
| Public Node | 2022-03-08 to 2026-10-06 | 1674 | 3 | 0 | none |
| Franklin Templeton | 2022-10-19 to 2026-10-06 | 1449 | 3 | 0 | none |
| Creit Technologies LLP | 2025-01-08 to 2026-10-06 | 637 | 3 | 0 | none |
| OBSRVR | 2026-07-15 to 2026-10-06 | 84 | 3 | 0 | none |
| Figure Certificate Company | 2026-08-27 to 2026-10-06 | 41 | 3 | 0 | none |
| MoneyGram | 2026-08-27 to 2026-10-06 | 41 | 3 | 0 | none |
| Range | 2026-08-27 to 2026-10-06 | 41 | 3 | 0 | none |

## Scoring of the three signals

An episode is a WARNING if an outcome of the same organization follows between 7 and W days later, an INCIDENT if an outcome falls within a day before to 7 days after its start (the episode is the incident itself or too late to help), and a FALSE ALARM otherwise. Precision = warnings / (warnings + false alarms). Recall = outcomes preceded by a warning. Lead time from the earliest warning.

### S1: any validator < 90% or organization < 99%

110 episodes across 12 organizations.

| Window W | Warning | Incident (within a day before to 7 days after) | False alarm | Precision | Outcomes | Preceded by a warning | Recall | Lead time (days, median / min / max) |
|---|---|---|---|---|---|---|---|---|
| 180 | 31 | 5 | 74 | 30% | 16 | 13 | 81% | 153 / 61 / 176 |
| 365 | 47 | 3 | 60 | 44% | 16 | 16 | 100% | 252 / 61 / 356 |

### S2: organization < 99% on 3 of the trailing 7 days

15 episodes across 4 organizations.

| Window W | Warning | Incident (within a day before to 7 days after) | False alarm | Precision | Outcomes | Preceded by a warning | Recall | Lead time (days, median / min / max) |
|---|---|---|---|---|---|---|---|---|
| 180 | 10 | 2 | 3 | 77% | 16 | 5 | 31% | 131 / 22 / 174 |
| 365 | 13 | 0 | 2 | 87% | 16 | 7 | 44% | 174 / 22 / 334 |

### S3: a validator at <= 10% for a day or organization < 90%

32 episodes across 8 organizations.

| Window W | Warning | Incident (within a day before to 7 days after) | False alarm | Precision | Outcomes | Preceded by a warning | Recall | Lead time (days, median / min / max) |
|---|---|---|---|---|---|---|---|---|
| 180 | 16 | 4 | 12 | 57% | 16 | 9 | 56% | 153 / 15 / 178 |
| 365 | 18 | 3 | 11 | 62% | 16 | 10 | 62% | 174 / 15 / 347 |

## Outcomes and the earliest signal before each (within 365 days)

| Organization | Date | Kind | S1 first signal, lead days | S3 first signal, lead days |
|---|---|---|---|---|
| Keybase | 2022-03-13 | REMOVAL | 2021-08-26, 199 | 2021-10-11, 153 |
| LOBSTR | 2021-04-06 | OUTAGE | 2020-07-09, 271 | 2021-04-06, 0 |
| SatoshiPay | 2020-05-31 | OUTAGE | 2020-01-02, 150 | none |
| SatoshiPay | 2021-09-01 | OUTAGE | 2020-12-23, 252 | 2021-04-22, 132 |
| SatoshiPay | 2021-10-13 | OUTAGE | 2020-12-23, 294 | 2021-04-22, 174 |
| SatoshiPay | 2024-02-14 | OUTAGE | 2023-08-16, 182 | 2023-08-21, 177 |
| SatoshiPay | 2025-02-18 | OUTAGE | 2024-02-28, 356 | none |
| SatoshiPay | 2025-08-22 | OUTAGE | 2024-12-17, 248 | 2025-02-25, 178 |
| SatoshiPay | 2026-07-14 | REMOVAL | 2025-08-22, 326 | 2025-08-22, 326 |
| Stellar Development Foundation | 2020-04-23 | OUTAGE | 2020-02-22, 61 | none |
| Stellar Development Foundation | 2020-05-10 | OUTAGE | 2020-02-22, 78 | 2020-04-24, 16 |
| Stellar Development Foundation | 2021-04-06 | OUTAGE | 2020-04-23, 348 | 2020-04-24, 347 |
| Whalestack LLC | 2025-01-09 | REMOVAL | 2024-04-06, 278 | none |
| Wirex Limited | 2022-07-13 | OUTAGE | 2021-11-03, 252 | 2022-07-11, 2 |
| Wirex Limited | 2022-07-26 | OUTAGE | 2021-11-03, 265 | 2022-07-11, 15 |
| Wirex Limited | 2022-12-13 | OUTAGE+REMOVAL | 2022-04-30, 227 | 2022-07-11, 155 |

## Notes

- Membership is sampled once per stable configuration state, so an organization that joined and left between two samples is missed.
- A REMOVAL is counted whenever an organization's last membership day is more than 3 days before the data end, whatever the reason (failure or voluntary exit). Organizations that share a validator key are merged, so a change of organization id is not a removal.
- Organization availability is Radar's isSubQuorumAvailableCount / crawlCount; validator availability is isValidatingCount / crawlCount.
- Thresholds (90%, 99%, 10%, 7 day gap, 7 day minimum lead) are starting points. The proposal should report the score of the rule finally chosen, with thresholds picked on 2019-2023 and tested on 2024-2026.

