# Verification of major events

Run at: 2026-10-06 11:18

Times in this report are UTC. 'Down' = Radar recorded the validator as not validating at that time.

## Summary

| Case | Time | Top tier organizations that lost their majority | Top tier validators down | Assessment |
|---|---|---|---|---|
| 2020-04-23 | 2020-04-24T01:00 | Stellar Development Foundation | 3/23 | real outage of 1 organization |
| 2020-04-23 | 2020-04-24T05:00 | Stellar Development Foundation | 3/23 | real outage of 1 organization |
| 2020-05-22 | 2020-05-23T12:00 | - | 0/23 | no organization lost its majority; CONFIGURATION CHANGE (see details) |
| 2020-05-22 | 2020-05-27T12:00 | - | 0/23 | no organization lost its majority; CONFIGURATION CHANGE (see details) |
| 2021-04-06 | 2021-04-06T10:00 | - | 0/23 | no organization lost its majority and the configuration is unchanged: the drop is not explained by this snapshot |
| 2021-04-06 | 2021-04-06T16:00 | LOBSTR, Stellar Development Foundation | 8/23 | real outage, 2 organizations down simultaneously |
| 2021-04-06 | 2021-04-07T12:00 | - | 0/23 | no organization lost its majority; CONFIGURATION CHANGE (see details) |
| 2022-07-26 | 2022-07-26T20:00 | Wirex Limited | 2/23 | real outage of 1 organization |
| 2022-07-26 | 2022-07-27T08:00 | Wirex Limited | 3/23 | real outage of 1 organization |
| 2022-12-13 | 2022-12-13T20:00 | Wirex Limited | 3/26 | real outage of 1 organization |
| 2022-12-13 | 2022-12-15T12:00 | Wirex Limited | 3/26 | real outage of 1 organization |
| 2023-09-14 | 2023-09-14T05:00 | Blockdaemon Inc., COINQVEST LLC, Franklin Templeton, LOBSTR, Public Node, SatoshiPay, Stellar Development Foundation, lobstr.co | 24/24 | 8 organizations 'down' at once (100% of validators): SUSPECTED CRAWLER OUTAGE |
| 2023-09-14 | 2023-09-14T10:58 | Public Node, SatoshiPay, lobstr.co | 8/24 | real outage, 3 organizations down simultaneously |
| 2023-09-14 | 2023-09-16T12:00 | lobstr.co | 1/24 | real outage of 1 organization |
| 2024-10-03 | 2024-10-05T12:00 | - | 0/23 | no organization lost its majority; CONFIGURATION CHANGE (see details) |
| 2025-08-22 | 2025-08-23T12:00 | SatoshiPay | 3/21 | real outage of 1 organization |
| 2025-08-22 | 2025-08-25T06:00 | SatoshiPay | 3/21 | real outage of 1 organization |
| 2026-10-01 | 2026-10-01T09:00 | - | 0/30 | no organization lost its majority and the configuration is unchanged: the drop is not explained by this snapshot |
| 2026-10-01 | 2026-10-01T23:00 | - | 0/30 | no organization lost its majority and the configuration is unchanged: the drop is not explained by this snapshot |

How to read the assessment column:
- 'real outage of 1 organization': the kind of event the SDF reviewers suggested (contacting node operators preemptively).
- 'SUSPECTED CRAWLER OUTAGE': more than half of the top tier validators down at once, unlikely to be a real outage; exclude from the analysis.
- 'CONFIGURATION CHANGE': the margin dropped because a quorum set or the top tier membership changed, not because a node failed.
- The top tier here is the transitive quorum set computed by Radar at the reference time (an approximation).


## 2020-04-23: Effective margin down to 1 organization for 7.7 hours

**Reference 2020-04-23T18:00** (snapshot 2020-04-23T17:58:45.726Z): top tier 23 validators, 7 organizations.

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2020-04-24T01:00** (snapshot 2020-04-24T00:57:26.005Z): real outage of 1 organization

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST Limited: 3/3 validating
- Keybase: 3/3 validating
- LOBSTR: 5/5 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 0/3 validating (down: SDF 3, SDF 1, SDF 2)  <-- MAJORITY LOST
- Wirex Limited: 3/3 validating

**2020-04-24T05:00** (snapshot 2020-04-24T04:57:01.738Z): real outage of 1 organization

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST Limited: 3/3 validating
- Keybase: 3/3 validating
- LOBSTR: 5/5 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 0/3 validating (down: SDF 3, SDF 1, SDF 2)  <-- MAJORITY LOST
- Wirex Limited: 3/3 validating


## 2020-05-22: Nominal margin reduced (blocking set 6 -> 4) for 7.5 days

**Reference 2020-05-21T12:00** (snapshot 2020-05-21T11:57:16.058Z): top tier 23 validators, 7 organizations.

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2020-05-23T12:00** (snapshot 2020-05-23T11:57:43.300Z): no organization lost its majority; CONFIGURATION CHANGE (see details)

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=4, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=2, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST Limited: 3/3 validating
- Keybase: 3/3 validating
- LOBSTR: 5/5 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 3/3 validating
- Wirex Limited: 3/3 validating
- Top tier validators that CHANGED quorum set since the reference: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3

**2020-05-27T12:00** (snapshot 2020-05-27T11:57:34.756Z): no organization lost its majority; CONFIGURATION CHANGE (see details)

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=4, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=2, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST Limited: 3/3 validating
- Keybase: 3/3 validating
- LOBSTR: 5/5 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 3/3 validating
- Wirex Limited: 3/3 validating
- Top tier validators that CHANGED quorum set since the reference: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3


## 2021-04-06: SDF validators halted (publicly reported); margin down to 1 organization from 14:34 for 3.9 hours

**Reference 2021-04-05T12:00** (snapshot 2021-04-05T11:59:36.929Z): top tier 23 validators, 7 organizations.

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2021-04-06T10:00** (snapshot 2021-04-06T09:58:18.206Z): no organization lost its majority and the configuration is unchanged: the drop is not explained by this snapshot

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST OÜ: 3/3 validating
- Keybase: 3/3 validating
- LOBSTR: 5/5 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 3/3 validating
- Wirex Limited: 3/3 validating

**2021-04-06T16:00** (snapshot 2021-04-06T15:59:23.775Z): real outage, 2 organizations down simultaneously

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=2, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=1, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST OÜ: 3/3 validating
- Keybase: 3/3 validating
- LOBSTR: 0/5 validating (down: LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 5 (Australia))  <-- MAJORITY LOST
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 0/3 validating (down: SDF 3, SDF 1, SDF 2)  <-- MAJORITY LOST
- Wirex Limited: 3/3 validating

**2021-04-07T12:00** (snapshot 2021-04-07T11:57:48.250Z): no organization lost its majority; CONFIGURATION CHANGE (see details)

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=4, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=2, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST OÜ: 3/3 validating
- Keybase: 3/3 validating
- LOBSTR: 5/5 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 3/3 validating
- Wirex Limited: 3/3 validating
- Top tier validators that CHANGED quorum set since the reference: SDF 1, SDF 2, SDF 3


## 2022-07-26: Thin effective margin for 1.2 days, at times down to 1 organization

**Reference 2022-07-26T08:00** (snapshot 2022-07-26T07:58:51.547Z): top tier 23 validators, 7 organizations.

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=5, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

Already down beforehand: Wirex Limited: Wirex United Kingdom

**2022-07-26T20:00** (snapshot 2022-07-26T19:57:49.344Z): real outage of 1 organization

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST LLC: 3/3 validating
- LOBSTR: 5/5 validating
- Public Node: 3/3 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 3/3 validating
- Wirex Limited: 1/3 validating (down: Wirex United Kingdom, Wirex Singapore)  <-- MAJORITY LOST

**2022-07-27T08:00** (snapshot 2022-07-27T07:57:50.357Z): real outage of 1 organization

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST LLC: 3/3 validating
- LOBSTR: 5/5 validating
- Public Node: 3/3 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 3/3 validating
- Wirex Limited: 0/3 validating (down: Wirex United States, Wirex United Kingdom, Wirex Singapore)  <-- MAJORITY LOST


## 2022-12-13: Thin margin for 1.1 days, then top tier from 8 to 7 organizations

**Reference 2022-12-13T06:00** (snapshot 2022-12-13T05:59:12.772Z): top tier 26 validators, 8 organizations.

Metrics: topTierSize=26, topTierOrgsSize=8, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=4, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2022-12-13T20:00** (snapshot 2022-12-13T19:58:40.851Z): real outage of 1 organization

Metrics: topTierSize=26, topTierOrgsSize=8, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=4, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST LLC: 3/3 validating
- Franklin Templeton: 3/3 validating
- LOBSTR: 5/5 validating
- Public Node: 3/3 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 3/3 validating
- Wirex Limited: 0/3 validating (down: Wirex United States, Wirex United Kingdom, Wirex Singapore)  <-- MAJORITY LOST
- Top tier validators that CHANGED quorum set since the reference: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong), SDF 1, SDF 2, SDF 3

**2022-12-15T12:00** (snapshot 2022-12-15T11:59:44.766Z): real outage of 1 organization

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST LLC: 3/3 validating
- Franklin Templeton: 3/3 validating
- LOBSTR: 5/5 validating
- Public Node: 3/3 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 3/3 validating
- Wirex Limited: 0/3 validating (down: Wirex United States, Wirex United Kingdom, Wirex Singapore)  <-- MAJORITY LOST
- Left the transitive quorum set since the reference: Wirex Singapore, Wirex United Kingdom, Wirex United States
- Top tier validators that CHANGED quorum set since the reference: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3, Boötes, COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong), FT SCV 1, FT SCV 2, FT SCV 3, Hercules, LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (India), Lyra by BP Ventures, SDF 1, SDF 2, SDF 3, SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)


## 2023-09-14: Effective margin at 0 several times within 9 hours (suspected measurement error)

**Reference 2023-09-13T18:00** (snapshot 2023-09-13T17:57:38.527Z): top tier 24 validators, 8 organizations.

Metrics: topTierSize=24, topTierOrgsSize=8, minBlockingSetSize=6, minBlockingSetFilteredSize=5, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

Already down beforehand: Public Node: Lyra by BP Ventures; lobstr.co: LOBSTR 2 (Europe)

**2023-09-14T05:00** (snapshot 2023-09-14T04:59:12.091Z): 8 organizations 'down' at once (100% of validators): SUSPECTED CRAWLER OUTAGE

Metrics: topTierSize=24, topTierOrgsSize=8, minBlockingSetSize=6, minBlockingSetFilteredSize=0, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=0, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 0/3 validating (down: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3)  <-- MAJORITY LOST
- COINQVEST LLC: 0/3 validating (down: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong))  <-- MAJORITY LOST
- Franklin Templeton: 0/3 validating (down: FT SCV 2, FT SCV 1, FT SCV 3)  <-- MAJORITY LOST
- LOBSTR: 0/5 validating (down: LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 5 (India))  <-- MAJORITY LOST
- Public Node: 0/3 validating (down: Lyra by BP Ventures, Hercules by OG Technologies, Boötes)  <-- MAJORITY LOST
- SatoshiPay: 0/3 validating (down: SatoshiPay Singapore, SatoshiPay Frankfurt, SatoshiPay Iowa)  <-- MAJORITY LOST
- Stellar Development Foundation: 0/3 validating (down: SDF 3, SDF 1, SDF 2)  <-- MAJORITY LOST
- lobstr.co: 0/1 validating (down: LOBSTR 2 (Europe))  <-- MAJORITY LOST

**2023-09-14T10:58** (snapshot 2023-09-14T10:56:13.115Z): real outage, 3 organizations down simultaneously

Metrics: topTierSize=24, topTierOrgsSize=8, minBlockingSetSize=6, minBlockingSetFilteredSize=1, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=1, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST LLC: 3/3 validating
- Franklin Templeton: 3/3 validating
- LOBSTR: 5/5 validating
- Public Node: 0/3 validating (down: Lyra by BP Ventures, Hercules by OG Technologies, Boötes)  <-- MAJORITY LOST
- SatoshiPay: 0/3 validating (down: SatoshiPay Singapore, SatoshiPay Frankfurt, SatoshiPay Iowa)  <-- MAJORITY LOST
- Stellar Development Foundation: 2/3 validating (down: SDF 2)
- lobstr.co: 0/1 validating (down: LOBSTR 2 (Europe))  <-- MAJORITY LOST

**2023-09-16T12:00** (snapshot 2023-09-16T11:57:40.620Z): real outage of 1 organization

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- COINQVEST LLC: 3/3 validating
- Franklin Templeton: 3/3 validating
- LOBSTR: 5/5 validating
- Public Node: 3/3 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 3/3 validating
- lobstr.co: 0/1 validating (down: LOBSTR 2 (Europe))  <-- MAJORITY LOST
- Left the transitive quorum set since the reference: LOBSTR 2 (Europe)
- Top tier validators that CHANGED quorum set since the reference: FT SCV 1, FT SCV 2, FT SCV 3


## 2024-10-03: Nominal blocking set 6 -> 5 for 4.6 days

**Reference 2024-10-03T10:00** (snapshot 2024-10-03T09:57:08.972Z): top tier 23 validators, 7 organizations.

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2024-10-05T12:00** (snapshot 2024-10-05T11:59:45.217Z): no organization lost its majority; CONFIGURATION CHANGE (see details)

Metrics: topTierSize=23, topTierOrgsSize=7, minBlockingSetSize=5, minBlockingSetFilteredSize=5, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- Franklin Templeton: 3/3 validating
- LOBSTR: 5/5 validating
- Public Node: 3/3 validating
- SatoshiPay: 3/3 validating
- Stellar Development Foundation: 3/3 validating
- Whalestack LLC: 3/3 validating
- Top tier validators that CHANGED quorum set since the reference: FT SCV 2


## 2025-08-22: Thin effective margin for 3.1 days

**Reference 2025-08-22T08:00** (snapshot 2025-08-22T07:56:58.960Z): top tier 21 validators, 7 organizations.

Metrics: topTierSize=21, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=6, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=3, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

**2025-08-23T12:00** (snapshot 2025-08-23T11:56:59.279Z): real outage of 1 organization

Metrics: topTierSize=21, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- Creit Technologies LLP: 3/3 validating
- Franklin Templeton: 3/3 validating
- LOBSTR: 3/3 validating
- Public Node: 3/3 validating
- SatoshiPay: 0/3 validating (down: SatoshiPay Singapore, SatoshiPay Frankfurt, SatoshiPay Iowa)  <-- MAJORITY LOST
- Stellar Development Foundation: 3/3 validating

**2025-08-25T06:00** (snapshot 2025-08-25T05:55:40.056Z): real outage of 1 organization

Metrics: topTierSize=21, topTierOrgsSize=7, minBlockingSetSize=6, minBlockingSetFilteredSize=4, minBlockingSetOrgsSize=3, minBlockingSetOrgsFilteredSize=2, minSplittingSetSize=3, minSplittingSetOrgsSize=3, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- Creit Technologies LLP: 3/3 validating
- Franklin Templeton: 3/3 validating
- LOBSTR: 3/3 validating
- Public Node: 3/3 validating
- SatoshiPay: 0/3 validating (down: SatoshiPay Singapore, SatoshiPay Frankfurt, SatoshiPay Iowa)  <-- MAJORITY LOST
- Stellar Development Foundation: 3/3 validating


## 2026-10-01: Organization splitting set 4 -> 0 -> 1 (suspected change of analyzer in Radar)

**Reference 2026-09-30T12:00** (snapshot 2026-09-30T11:56:35.166Z): top tier 30 validators, 10 organizations.

Metrics: topTierSize=30, topTierOrgsSize=10, minBlockingSetSize=8, minBlockingSetFilteredSize=8, minBlockingSetOrgsSize=4, minBlockingSetOrgsFilteredSize=4, minSplittingSetSize=4, minSplittingSetOrgsSize=4, hasQuorumIntersection=True

**2026-10-01T09:00** (snapshot 2026-10-01T08:59:03.964Z): no organization lost its majority and the configuration is unchanged: the drop is not explained by this snapshot

Metrics: topTierSize=30, topTierOrgsSize=10, minBlockingSetSize=8, minBlockingSetFilteredSize=8, minBlockingSetOrgsSize=4, minBlockingSetOrgsFilteredSize=4, minSplittingSetSize=4, minSplittingSetOrgsSize=1, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- Creit Technologies LLP: 3/3 validating
- Figure Certificate Company: 3/3 validating
- Franklin Templeton: 3/3 validating
- LOBSTR: 3/3 validating
- MoneyGram: 3/3 validating
- OBSRVR: 3/3 validating
- Public Node: 3/3 validating
- Range: 3/3 validating
- Stellar Development Foundation: 3/3 validating

**2026-10-01T23:00** (snapshot 2026-10-01T22:57:29.805Z): no organization lost its majority and the configuration is unchanged: the drop is not explained by this snapshot

Metrics: topTierSize=30, topTierOrgsSize=10, minBlockingSetSize=8, minBlockingSetFilteredSize=8, minBlockingSetOrgsSize=4, minBlockingSetOrgsFilteredSize=4, minSplittingSetSize=4, minSplittingSetOrgsSize=4, hasQuorumIntersection=True

- Blockdaemon Inc.: 3/3 validating
- Creit Technologies LLP: 3/3 validating
- Figure Certificate Company: 3/3 validating
- Franklin Templeton: 3/3 validating
- LOBSTR: 3/3 validating
- MoneyGram: 3/3 validating
- OBSRVR: 3/3 validating
- Public Node: 3/3 validating
- Range: 3/3 validating
- Stellar Development Foundation: 3/3 validating

