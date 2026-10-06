# Mechanism analysis

Run at: 2026-10-06 13:48

## Summary of part A (configuration changes)

- 2020-05 Blockdaemon: CONFIRMED: this change alone is sufficient to lower the organization level margin from 3 to 2.
- 2021-04 SDF: CONFIRMED: this change alone is sufficient to lower the organization level margin from 3 to 2.
- 2024-10 Franklin Templeton: CONFIRMED (node level): this change alone lowers the blocking set from 6 to 5 nodes.
- 2022-02 unexplained: No top tier validator changed its quorum set between the two snapshots.
- 2022-07 Wirex period: No top tier validator changed its quorum set between the two snapshots.
- 2022-07-13 organizations 2: No top tier validator changed its quorum set between the two snapshots.
- 2021-04-13 transient: CONFIRMED (node level): this change alone lowers the blocking set from 6 to 5 nodes.

How to read: 'CONFIRMED' means that replacing only that organization's quorum sets in the earlier configuration lowers the network wide margin exactly as observed. This is the direct counterfactual for the claim that a check run before the change would have detected it.
Limitation: the script considers top tier validators only and uses its own blocking set computation; values may differ from Radar in edge cases.

## 2020-05 Blockdaemon: Blocking set 6 -> 4 (organizations 3 -> 2) for 7.5 days

Top tier at the reference time: 23 validators. Validators that changed quorum set: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3

### Quorum set of: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3

BEFORE:
```
- requires 5 of 7 elements
  [Keybase] requires 2 of 3: Keybase 0, Keybase 1, Keybase 2
  [LOBSTR] requires 3 of 5: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (Australia)
  [Blockdaemon Inc.] requires 2 of 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Wirex Limited] requires 2 of 3: Wirex Singapore, Wirex United Kingdom, Wirex United States
  [Stellar Development Foundation] requires 2 of 3: SDF 1, SDF 2, SDF 3
  [COINQVEST Limited] requires 2 of 3: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong)
  [SatoshiPay] requires 2 of 3: SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)
```
AFTER:
```
- requires 5 of 6 elements
  [Keybase] requires 2 of 3: Keybase 0, Keybase 1, Keybase 2
  [LOBSTR] requires 3 of 5: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (Australia)
  [Blockdaemon Inc.] requires 2 of 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Wirex Limited] requires 2 of 3: Wirex Singapore, Wirex United Kingdom, Wirex United States
  [Stellar Development Foundation] requires 2 of 3: SDF 1, SDF 2, SDF 3
  [COINQVEST Limited] requires 2 of 3: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong)
```
Difference: outer threshold 5 -> 5; outer elements 7 -> 6; removed: SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)

### Recomputed liveness margin (top tier only)

| Configuration | Min blocking set (organizations) | (nodes) | Recorded by Radar (organizations / nodes) | Smallest groups of organizations that block the network |
|---|---|---|---|---|
| Before the change | 3 | 6 | 3 / 6 | Blockdaemon Inc. + COINQVEST Limited + Keybase; Blockdaemon Inc. + COINQVEST Limited + LOBSTR; Blockdaemon Inc. + COINQVEST Limited + SatoshiPay; Blockdaemon Inc. + COINQVEST Limited + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST Limited + Wirex Limited; Blockdaemon Inc. + Keybase + LOBSTR |
| Actual, after the change | 2 | 4 | 2 / 4 | COINQVEST Limited + Keybase; COINQVEST Limited + LOBSTR; COINQVEST Limited + Stellar Development Foundation; COINQVEST Limited + Wirex Limited; Keybase + LOBSTR; Keybase + Stellar Development Foundation |
| COUNTERFACTUAL: only the quorum sets of the validators above replaced | 2 | 4 | - | COINQVEST Limited + Keybase; COINQVEST Limited + LOBSTR; COINQVEST Limited + Stellar Development Foundation; COINQVEST Limited + Wirex Limited; Keybase + LOBSTR; Keybase + Stellar Development Foundation |

**Mechanism verdict: CONFIRMED: this change alone is sufficient to lower the organization level margin from 3 to 2.**
Afterwards (2020-05-30T12:00): 3/3 validators had returned to the earlier quorum set; Radar records blocking set organizations/nodes = 3/6.

## 2021-04 SDF: After the 6 April 2021 incident, blocking set 6 -> 4 for 1.3 days

Top tier at the reference time: 23 validators. Validators that changed quorum set: SDF 3, SDF 1, SDF 2

### Quorum set of: SDF 3, SDF 1, SDF 2

BEFORE:
```
- requires 5 of 7 elements
  [Keybase] requires 2 of 3: Keybase 0, Keybase 1, Keybase 2
  [LOBSTR] requires 3 of 5: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (Australia)
  [Blockdaemon Inc.] requires 2 of 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Wirex Limited] requires 2 of 3: Wirex Singapore, Wirex United Kingdom, Wirex United States
  [Stellar Development Foundation] requires 2 of 3: SDF 1, SDF 2, SDF 3
  [COINQVEST OÜ] requires 2 of 3: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong)
  [SatoshiPay] requires 2 of 3: SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)
```
AFTER:
```
- requires 5 of 6 elements
  [Keybase] requires 2 of 3: Keybase 0, Keybase 1, Keybase 2
  [Blockdaemon Inc.] requires 2 of 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Wirex Limited] requires 2 of 3: Wirex Singapore, Wirex United Kingdom, Wirex United States
  [Stellar Development Foundation] requires 2 of 3: SDF 1, SDF 2, SDF 3
  [COINQVEST OÜ] requires 2 of 3: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong)
  [SatoshiPay] requires 2 of 3: SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)
```
Difference: outer threshold 5 -> 5; outer elements 7 -> 6; removed: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (Australia)

### Recomputed liveness margin (top tier only)

| Configuration | Min blocking set (organizations) | (nodes) | Recorded by Radar (organizations / nodes) | Smallest groups of organizations that block the network |
|---|---|---|---|---|
| Before the change | 3 | 6 | 3 / 6 | Blockdaemon Inc. + COINQVEST OÜ + Keybase; Blockdaemon Inc. + COINQVEST OÜ + LOBSTR; Blockdaemon Inc. + COINQVEST OÜ + SatoshiPay; Blockdaemon Inc. + COINQVEST OÜ + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST OÜ + Wirex Limited; Blockdaemon Inc. + Keybase + LOBSTR |
| Actual, after the change | 2 | 4 | 2 / 4 | Blockdaemon Inc. + COINQVEST OÜ; Blockdaemon Inc. + Keybase; Blockdaemon Inc. + SatoshiPay; Blockdaemon Inc. + Wirex Limited; COINQVEST OÜ + Keybase; COINQVEST OÜ + SatoshiPay |
| COUNTERFACTUAL: only the quorum sets of the validators above replaced | 2 | 4 | - | Blockdaemon Inc. + COINQVEST OÜ; Blockdaemon Inc. + Keybase; Blockdaemon Inc. + SatoshiPay; Blockdaemon Inc. + Wirex Limited; COINQVEST OÜ + Keybase; COINQVEST OÜ + SatoshiPay |

**Mechanism verdict: CONFIRMED: this change alone is sufficient to lower the organization level margin from 3 to 2.**
Afterwards (2021-04-20T12:00): 3/3 validators had returned to the earlier quorum set; Radar records blocking set organizations/nodes = 3/6.

## 2024-10 Franklin Templeton: Blocking set 6 -> 5 for 4.6 days

Top tier at the reference time: 23 validators. Validators that changed quorum set: FT SCV 2

### Quorum set of: FT SCV 2

BEFORE:
```
- requires 5 of 7 elements
  [LOBSTR] requires 3 of 5: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (India)
  [Franklin Templeton] requires 2 of 3: FT SCV 1, FT SCV 2, FT SCV 3
  [Blockdaemon Inc.] requires 2 of 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Stellar Development Foundation] requires 2 of 3: SDF 1, SDF 2, SDF 3
  [Whalestack LLC] requires 2 of 3: Whalestack (Finland), Whalestack (Germany), Whalestack (Hong Kong)
  [SatoshiPay] requires 2 of 3: SatoshiPay Frankfurt, SatoshiPay Iowa, SatoshiPay Singapore
  [Public Node] requires 2 of 3: Boötes, Hercules by OG Technologies, Lyra by BP Ventures
```
AFTER:
```
- requires 5 of 6 elements
  [Franklin Templeton] requires 2 of 3: FT SCV 1, FT SCV 2, FT SCV 3
  [Blockdaemon Inc.] requires 2 of 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Stellar Development Foundation] requires 2 of 3: SDF 1, SDF 2, SDF 3
  [Whalestack LLC] requires 2 of 3: Whalestack (Finland), Whalestack (Germany), Whalestack (Hong Kong)
  [SatoshiPay] requires 2 of 3: SatoshiPay Frankfurt, SatoshiPay Iowa, SatoshiPay Singapore
  [Public Node] requires 2 of 3: Boötes, Hercules by OG Technologies, Lyra by BP Ventures
```
Difference: outer threshold 5 -> 5; outer elements 7 -> 6; removed: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (India)

### Recomputed liveness margin (top tier only)

| Configuration | Min blocking set (organizations) | (nodes) | Recorded by Radar (organizations / nodes) | Smallest groups of organizations that block the network |
|---|---|---|---|---|
| Before the change | 3 | 6 | 3 / 6 | Blockdaemon Inc. + Franklin Templeton + LOBSTR; Blockdaemon Inc. + Franklin Templeton + Public Node; Blockdaemon Inc. + Franklin Templeton + SatoshiPay; Blockdaemon Inc. + Franklin Templeton + Stellar Development Foundation; Blockdaemon Inc. + Franklin Templeton + Whalestack LLC; Blockdaemon Inc. + LOBSTR + Public Node |
| Actual, after the change | 3 | 5 | 3 / 5 | Blockdaemon Inc. + Franklin Templeton + LOBSTR; Blockdaemon Inc. + Franklin Templeton + Public Node; Blockdaemon Inc. + Franklin Templeton + SatoshiPay; Blockdaemon Inc. + Franklin Templeton + Stellar Development Foundation; Blockdaemon Inc. + Franklin Templeton + Whalestack LLC; Blockdaemon Inc. + LOBSTR + Public Node |
| COUNTERFACTUAL: only the quorum sets of the validators above replaced | 3 | 5 | - | Blockdaemon Inc. + Franklin Templeton + LOBSTR; Blockdaemon Inc. + Franklin Templeton + Public Node; Blockdaemon Inc. + Franklin Templeton + SatoshiPay; Blockdaemon Inc. + Franklin Templeton + Stellar Development Foundation; Blockdaemon Inc. + Franklin Templeton + Whalestack LLC; Blockdaemon Inc. + LOBSTR + Public Node |

**Mechanism verdict: CONFIRMED (node level): this change alone lowers the blocking set from 6 to 5 nodes.**
Afterwards (2024-10-09T12:00): 1/1 validators had returned to the earlier quorum set; Radar records blocking set organizations/nodes = 3/6.

## 2022-02 unexplained: Node blocking set 6 -> 5 for 2.4 days

Top tier at the reference time: 23 validators. Validators that changed quorum set: NONE

### Recomputed liveness margin (top tier only)

| Configuration | Min blocking set (organizations) | (nodes) | Recorded by Radar (organizations / nodes) | Smallest groups of organizations that block the network |
|---|---|---|---|---|
| Before the change | 3 | 6 | 3 / 6 | Blockdaemon Inc. + COINQVEST OÜ + Keybase; Blockdaemon Inc. + COINQVEST OÜ + LOBSTR; Blockdaemon Inc. + COINQVEST OÜ + SatoshiPay; Blockdaemon Inc. + COINQVEST OÜ + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST OÜ + Wirex Limited; Blockdaemon Inc. + Keybase + LOBSTR |
| Actual, after the change | 3 | 6 | 3 / 5 | Blockdaemon Inc. + COINQVEST OÜ + Keybase; Blockdaemon Inc. + COINQVEST OÜ + LOBSTR; Blockdaemon Inc. + COINQVEST OÜ + SatoshiPay; Blockdaemon Inc. + COINQVEST OÜ + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST OÜ + Wirex Limited; Blockdaemon Inc. + Keybase + LOBSTR |

**Mechanism verdict: No top tier validator changed its quorum set between the two snapshots.**
Afterwards (2022-03-01T12:00): 0/0 validators had returned to the earlier quorum set; Radar records blocking set organizations/nodes = 3/6.

## 2022-07 Wirex period: Nominal blocking set 6 -> 5 for 3 days during the Wirex trouble

Top tier at the reference time: 23 validators. Validators that changed quorum set: NONE

### Recomputed liveness margin (top tier only)

| Configuration | Min blocking set (organizations) | (nodes) | Recorded by Radar (organizations / nodes) | Smallest groups of organizations that block the network |
|---|---|---|---|---|
| Before the change | 3 | 6 | 3 / 6 | Blockdaemon Inc. + COINQVEST LLC + LOBSTR; Blockdaemon Inc. + COINQVEST LLC + Public Node; Blockdaemon Inc. + COINQVEST LLC + SatoshiPay; Blockdaemon Inc. + COINQVEST LLC + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST LLC + Wirex Limited; Blockdaemon Inc. + LOBSTR + Public Node |
| Actual, after the change | 3 | 6 | 3 / 5 | Blockdaemon Inc. + COINQVEST LLC + LOBSTR; Blockdaemon Inc. + COINQVEST LLC + Public Node; Blockdaemon Inc. + COINQVEST LLC + SatoshiPay; Blockdaemon Inc. + COINQVEST LLC + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST LLC + Wirex Limited; Blockdaemon Inc. + LOBSTR + Public Node |

**Mechanism verdict: No top tier validator changed its quorum set between the two snapshots.**
Afterwards (2022-07-25T12:00): 0/0 validators had returned to the earlier quorum set; Radar records blocking set organizations/nodes = 3/6.

## 2022-07-13 organizations 2: Nominal blocking set 4 (organizations 2) for 12.6 h

Top tier at the reference time: 23 validators. Validators that changed quorum set: NONE

### Recomputed liveness margin (top tier only)

| Configuration | Min blocking set (organizations) | (nodes) | Recorded by Radar (organizations / nodes) | Smallest groups of organizations that block the network |
|---|---|---|---|---|
| Before the change | 3 | 6 | 3 / 6 | Blockdaemon Inc. + COINQVEST LLC + LOBSTR; Blockdaemon Inc. + COINQVEST LLC + Public Node; Blockdaemon Inc. + COINQVEST LLC + SatoshiPay; Blockdaemon Inc. + COINQVEST LLC + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST LLC + Wirex Limited; Blockdaemon Inc. + LOBSTR + Public Node |
| Actual, after the change | 3 | 6 | 2 / 4 | Blockdaemon Inc. + COINQVEST LLC + LOBSTR; Blockdaemon Inc. + COINQVEST LLC + Public Node; Blockdaemon Inc. + COINQVEST LLC + SatoshiPay; Blockdaemon Inc. + COINQVEST LLC + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST LLC + Wirex Limited; Blockdaemon Inc. + LOBSTR + Public Node |

**Mechanism verdict: No top tier validator changed its quorum set between the two snapshots.**
Afterwards (2022-07-25T12:00): 0/0 validators had returned to the earlier quorum set; Radar records blocking set organizations/nodes = 3/6.

## 2021-04-13 transient: Node blocking set 5 for 5.4 h with a 30/9 top tier

Top tier at the reference time: 23 validators. Validators that changed quorum set: LOBSTR 5 (Australia), LOBSTR 2 (Europe)

### Quorum set of: LOBSTR 5 (Australia), LOBSTR 2 (Europe)

BEFORE:
```
- requires 5 of 7 elements
  [Keybase] requires 2 of 3: Keybase 0, Keybase 1, Keybase 2
  [LOBSTR] requires 3 of 5: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (Australia)
  [Blockdaemon Inc.] requires 2 of 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
  [Wirex Limited] requires 2 of 3: Wirex Singapore, Wirex United Kingdom, Wirex United States
  [Stellar Development Foundation] requires 2 of 3: SDF 1, SDF 2, SDF 3
  [COINQVEST OÜ] requires 2 of 3: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong)
  [SatoshiPay] requires 2 of 3: SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)
```
AFTER:
```
- requires 5 of 7 elements
  [Keybase] requires 2 of 3: Keybase 0, Keybase 1, Keybase 2
  [LOBSTR] requires 3 of 5: LOBSTR 1 (Europe), LOBSTR 2 (Europe), LOBSTR 3 (North America), LOBSTR 4 (Asia), LOBSTR 5 (Australia)
  [Wirex Limited] requires 2 of 3: Wirex Singapore, Wirex United Kingdom, Wirex United States
  [Stellar Development Foundation] requires 2 of 3: SDF 1, SDF 2, SDF 3
  [COINQVEST OÜ] requires 2 of 3: COINQVEST (Finland), COINQVEST (Germany), COINQVEST (Hong Kong)
  [SatoshiPay] requires 2 of 3: SatoshiPay (DE, Frankfurt), SatoshiPay (SG, Singapore), SatoshiPay (US, Iowa)
  - requires 3 of 3 elements
    [Blockdaemon Inc.] requires 2 of 3: Blockdaemon Validator 1, Blockdaemon Validator 2, Blockdaemon Validator 3
    [Muyu Network] requires 3 of 4: fchain core1, fchain core2, fchain core3, fchain core4
    [SAKKEX OÜ] requires 2 of 3: GBTNFYOZ, Sakkex Singapore, Sakkex United Kingdom
```
Difference: outer threshold 5 -> 5; outer elements 7 -> 7; added: GBTNFYOZ, Sakkex Singapore, Sakkex United Kingdom, fchain core1, fchain core2, fchain core3, fchain core4

### Recomputed liveness margin (top tier only)

| Configuration | Min blocking set (organizations) | (nodes) | Recorded by Radar (organizations / nodes) | Smallest groups of organizations that block the network |
|---|---|---|---|---|
| Before the change | 3 | 6 | 3 / 6 | Blockdaemon Inc. + COINQVEST OÜ + Keybase; Blockdaemon Inc. + COINQVEST OÜ + LOBSTR; Blockdaemon Inc. + COINQVEST OÜ + SatoshiPay; Blockdaemon Inc. + COINQVEST OÜ + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST OÜ + Wirex Limited; Blockdaemon Inc. + Keybase + LOBSTR |
| Actual, after the change | 3 | 5 | 3 / 5 | Blockdaemon Inc. + COINQVEST OÜ + Keybase; Blockdaemon Inc. + COINQVEST OÜ + LOBSTR; Blockdaemon Inc. + COINQVEST OÜ + SatoshiPay; Blockdaemon Inc. + COINQVEST OÜ + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST OÜ + Wirex Limited; Blockdaemon Inc. + Keybase + LOBSTR |
| COUNTERFACTUAL: only the quorum sets of the validators above replaced | 3 | 5 | - | Blockdaemon Inc. + COINQVEST OÜ + Keybase; Blockdaemon Inc. + COINQVEST OÜ + LOBSTR; Blockdaemon Inc. + COINQVEST OÜ + SatoshiPay; Blockdaemon Inc. + COINQVEST OÜ + Stellar Development Foundation; Blockdaemon Inc. + COINQVEST OÜ + Wirex Limited; Blockdaemon Inc. + Keybase + LOBSTR |

**Mechanism verdict: CONFIRMED (node level): this change alone lowers the blocking set from 6 to 5 nodes.**
Afterwards (2021-04-14T12:00): 2/2 validators had returned to the earlier quorum set; Radar records blocking set organizations/nodes = 3/6.

## Timeline of Wirex: 2022-01-01 to 2022-12-31 (milestone: 2022-12-14, left the top tier)

Validators: Wirex Singapore, Wirex United Kingdom, Wirex United States. Days with data: 365. Days with signs of degradation (a validator below 90% or the organization below 99%): 46.

- First day with signs: **2022-04-30**, 228 days before the milestone 2022-12-14 (left the top tier).
- Days on which THE ORGANIZATION was partly unavailable (below 99%): 25, first on 2022-04-30.

By month:

| Month | Days with signs | Wirex Singapore | Wirex United Kingdom | Wirex United States | Organization |
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

First 40 days with signs:

| Date | Wirex Singapore | Wirex United Kingdom | Wirex United States | Organization |
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

## Timeline of SatoshiPay: 2025-01-01 to 2026-09-30 (milestone: 2025-08-22, all 3 validators down for more than 3 days)

Validators: SatoshiPay Iowa, SatoshiPay Singapore, SatoshiPay Frankfurt. Days with data: 638. Days with signs of degradation (a validator below 90% or the organization below 99%): 157.

- First day with signs: **2025-01-20**, 214 days before the milestone 2025-08-22 (all 3 validators down for more than 3 days).
- Days on which THE ORGANIZATION was partly unavailable (below 99%): 109, first on 2025-01-20.

By month:

| Month | Days with signs | SatoshiPay Iowa | SatoshiPay Singapore | SatoshiPay Frankfurt | Organization |
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

First 40 days with signs:

| Date | SatoshiPay Iowa | SatoshiPay Singapore | SatoshiPay Frankfurt | Organization |
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
