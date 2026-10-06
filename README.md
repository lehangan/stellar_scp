# Quorum configuration changes and liveness margin in the Stellar network, 2019–2026

Scripts, data and results behind the technical report `Stellar_Liveness_TechReport.pdf`
(Tra Nguyen and Binh Minh Nguyen, Hanoi University of Science and Technology, October 2026).

All data come from the public API of OBSRVR Radar (formerly Stellarbeat), `https://radar.withobsrvr.com/api`.
Every script is standard-library Python 3 and caches what it downloads, so a second run is instant.
Run them from the repository root, in this order.

| Script | What it does | Outputs (in `sdf_feasibility/`) | Numbers in the report |
|---|---|---|---|
| `full_scan.py` | Downloads the per-scan network statistics (May 2019 to October 2026, about 1.2 million scans) and detects configuration events (stable states, reconfiguration episodes) and degradation events (effective margin below nominal). | `full_scan/config_steps.csv`, `reconfig_episodes.csv`, `thin_margin.csv`, `no_quorum_intersection.csv`, `report.md` | Scan count; quorum intersection; splitting set history; the 52 stable states and 19 episodes; the 32 degradation periods of an hour or more; the 115 runs at or below one organization |
| `verify_case.py` | Fetches full network snapshots before and inside each event and reports which validators were down, which quorum sets changed and which organizations joined or left the top tier. | `verify/report.md`, `verify/cases.csv`, `verify/raw/snap_*.json` | Attribution of every event (Tables 1 and 2); SatoshiPay's removal on 15 July 2026; the August 2026 expansion; the 14 September 2023 crawler outage |
| `analysis.py` | For each configuration event, prints the quorum sets before and after, recomputes the minimal blocking set by exhaustive enumeration and runs the counterfactual (only the changed quorum sets replaced). Also the daily availability timelines of Wirex and SatoshiPay. | `mechanism/report.md`, `mechanism/timeline_*.csv` | Mechanism and counterfactual of the four configuration events (Table 1) |
| `tier1_availability.py` | Daily availability of every organization that was ever in the top tier, membership over time, and the scoring of the early warning rules S1, S2 and S3 against verified outages and removals. `--offline` uses cached files only. | `availability/report.md`, `membership.csv`, `availability_daily.csv`, `episodes.csv` | Table 3; lead times; the share of warnings due to SatoshiPay |

`cases_to_add.py` holds the extra cases that were appended to `verify_case.py` and `analysis.py`
(the thin margin periods of an hour or more and the configuration episodes attributed in October 2026).

Two checks in the report use sources outside Radar: ledger close times on 13 and 14 September 2023 from the
StellarExpert ledger API (`https://api.stellar.expert/explorer/public/ledger/<sequence>`, ledgers 48092100,
48092600, 48106500, 48106600, 48106700, 48107000), and SDF's statement on the halt of 6 April 2021.

Definitions used throughout (see the report, Section 1): the liveness margin is the minimal blocking set in
organizations; the nominal margin is computed from configurations, the effective margin discounts validators
not validating at the time; both are top tier figures. Membership is sampled at the start of every stable
configuration state; validators are dropped from the availability computation after their last day with any
validating time.
