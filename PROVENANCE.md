# Data provenance

**Source.** All network data come from the public API of OBSRVR Radar (formerly Stellarbeat), `https://radar.withobsrvr.com/api`:
`/v1/statistics` (per scan network statistics, used by `full_scan.py`), `/v1?at=<time>` (full network snapshots, used by `verify_case.py` and `analysis.py`), and `/v1/node/<key>/day-statistics` and `/v1/organization/<id>/day-statistics` (daily availability, used by `tier1_availability.py`). Radar inherited the Stellarbeat database, so the record starts on 31 May 2019.

**Collection.** The scan record was downloaded in early October 2026 and ends on 1 October 2026; snapshots and daily availability were downloaded between 2 and 6 October 2026 (exact timestamps in `sdf_feasibility/*/run.log`). Every downloaded response is cached under `sdf_feasibility/*/raw`; the cached snapshots (159) and availability files are committed, the scan cache (about 1.2 million records) is not, and `full_scan.py` rebuilds it.

**Versions.** Release v1.0.0 of this repository is archived at Zenodo, doi:10.5281/zenodo.23186634 (concept DOI 10.5281/zenodo.23186596). The technical report in the repository was built from that release.

**Known limitations of the data.**
- Single vantage point: a validator recorded as not validating or unreachable may have been invisible to Radar's crawler only.
- Radar's nominal margins respond to reachability as well as to configuration; configuration changes are established only by snapshot diffs.
- Membership is sampled at the start of each stable configuration state (52 snapshots); an organization that joined and left between samples would be missed.
- Radar's analysis backend changed over the period (its own code, then fbas_analyzer, now python-fbas), and PR #65 of the Radar repository (merged 1 October 2026) records that its quorum intersection parser previously inferred safety from the absence of one substring. Quorum intersection and the degradation series are Radar's figures; the blocking sets of the four configuration events were recomputed independently.
- Organization availability is Radar's `isSubQuorumAvailableCount / crawlCount`; validator availability is `isValidatingCount / crawlCount`.

**Licenses.** Code and report: MIT License (see `LICENSE`). The cached API responses are redistributed unchanged for reproducibility; OBSRVR Radar's own terms apply to the underlying data.
