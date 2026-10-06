# Cases to ADD to the existing scripts (copy and paste; nothing else changes).
#
# 1. Append CASES_EXTRA to the CASES list in verify_case.py, then run:  python verify_case.py
#    (about 35 new snapshots, 3-5 minutes; the ones already cached are reused)
# 2. Append CONFIG_CASES_EXTRA to CONFIG_CASES in analysis.py, then run:  python analysis.py
#    (reuses the snapshots downloaded in step 1)
#
# Times are UTC. Format of each tuple is the same as in the scripts.

# ---------------------------------------------------------------- verify_case.py : CASES

CASES_EXTRA = [
    # (a) The configuration episodes from full_scan that have NOT been attributed yet.
    #     Reference = just before the episode; probes = inside each intermediate state.
    ("2021-04-13", "Inside the April 2021 episode: top tier 30/9 for 6 hours, then node blocking set 5",
     "2021-04-12T12:00", ["2021-04-13T11:50", "2021-04-13T15:00", "2021-04-19T08:10"]),
    ("2022-02-26", "Node blocking set 6 -> 5 for 2.4 days (unexplained; Keybase to Public Node transition?)",
     "2022-02-25T12:00", ["2022-02-27T12:00", "2022-03-01T12:00", "2022-03-10T12:00", "2022-03-22T00:15"]),
    ("2022-06-24", "Brief 23/8/7/4 state for 30 minutes",
     "2022-06-23T12:00", ["2022-06-24T06:55"]),
    ("2022-07-10", "Nominal blocking set 6 -> 5 for 3 days, then 4 (organizations 2) for 12.6 h, during the Wirex trouble",
     "2022-07-09T12:00", ["2022-07-11T12:00", "2022-07-13T12:00", "2022-07-24T20:00"]),
    ("2025-01-08", "Top tier 26/8 for 1.8 days, then back to 23/7",
     "2025-01-07T12:00", ["2025-01-09T12:00"]),
    ("2025-04-23", "Top tier 23 -> 21 validators (which organization shrank?)",
     "2025-04-22T12:00", ["2025-04-24T12:00"]),
    ("2026-07-15", "Top tier 24/8 for 10.7 h, then 21/7 (an organization added early, then removed?)",
     "2026-07-14T12:00", ["2026-07-15T15:00", "2026-07-16T12:00"]),
    ("2026-08-27", "The August 2026 expansion: 21/7 -> 33/11 -> 30/10; which organization left?",
     "2026-08-26T12:00", ["2026-08-27T10:00", "2026-08-27T11:30", "2026-08-27T15:00", "2026-08-28T12:00"]),

    # (b) Thin margin periods of one hour or more that have not been verified against a snapshot.
    #     Probe = midpoint of the period; reference = 6 hours before its start.
    ("2019-06-05", "Thin margin for 1.3 h, lowest effective margin 3 (nominal 4)",
     "2019-06-05T11:00", ["2019-06-05T17:45"]),
    ("2020-05-10", "Thin margin for 1.5 h, lowest effective margin 1 (nominal 3)",
     "2020-05-10T10:00", ["2020-05-10T17:25"]),
    ("2020-05-15", "Thin margin for 1.1 h, lowest effective margin 1 (nominal 3)",
     "2020-05-15T13:00", ["2020-05-15T20:15"]),
    ("2020-05-21", "Thin margin for 1.4 h, lowest effective margin 2 (nominal 3)",
     "2020-05-21T07:00", ["2020-05-21T14:12"]),
    ("2020-05-31", "Thin margin for 2.5 h, lowest effective margin 2 (nominal 3)",
     "2020-05-31T05:00", ["2020-05-31T12:33"]),
    ("2020-06-02", "Thin margin for 2.0 h, lowest effective margin 1 (nominal 3)",
     "2020-06-02T08:00", ["2020-06-02T15:44"]),
    ("2021-09-01a", "Thin margin for 3.8 h, lowest effective margin 2 (nominal 3)",
     "2021-08-31T22:00", ["2021-09-01T06:38"]),
    ("2021-09-01b", "Thin margin for 5.1 h, lowest effective margin 2 (nominal 3)",
     "2021-09-01T03:00", ["2021-09-01T12:18"]),
    ("2021-09-13", "Thin margin for 1.2 h, lowest effective margin 2 (nominal 3)",
     "2021-09-13T17:00", ["2021-09-13T23:44"]),
    ("2021-10-13", "Thin margin for 1.2 h, lowest effective margin 2 (nominal 3)",
     "2021-10-13T01:00", ["2021-10-13T08:00"]),
    ("2022-07-13", "Thin margin for 4.9 h, lowest effective margin 2 (nominal 3)",
     "2022-07-13T13:00", ["2022-07-13T21:29"]),
    ("2023-08-24", "Thin margin for 1.4 h, lowest effective margin 2 (nominal 3)",
     "2023-08-24T06:00", ["2023-08-24T12:56"]),
    ("2024-02-14", "Thin margin for 3.9 h, lowest effective margin 2 (nominal 3)",
     "2024-02-14T00:00", ["2024-02-14T08:46"]),
    ("2024-10-04", "Thin margin for 2.1 h, lowest effective margin 2 (nominal 3)",
     "2024-10-04T06:00", ["2024-10-04T13:34"]),
    ("2025-02-18", "Thin margin for 1.4 h, lowest effective margin 2 (nominal 3)",
     "2025-02-18T07:00", ["2025-02-18T14:28"]),
    ("2025-02-25a", "Thin margin for 2.4 h, lowest effective margin 2 (nominal 3)",
     "2025-02-24T21:00", ["2025-02-25T04:10"]),
    ("2025-02-25b", "Thin margin for 1.1 h, lowest effective margin 2 (nominal 3)",
     "2025-02-25T05:00", ["2025-02-25T11:36"]),
    ("2025-02-25c", "Thin margin for 1.0 h, lowest effective margin 2 (nominal 3)",
     "2025-02-25T15:00", ["2025-02-25T21:58"]),
    ("2025-02-26a", "Thin margin for 1.5 h, lowest effective margin 2 (nominal 3)",
     "2025-02-26T08:00", ["2025-02-26T14:44"]),
    ("2025-02-26b", "Thin margin for 1.1 h, lowest effective margin 2 (nominal 3)",
     "2025-02-26T12:00", ["2025-02-26T18:49"]),
    ("2025-02-28a", "Thin margin for 1.2 h, lowest effective margin 2 (nominal 3)",
     "2025-02-27T19:00", ["2025-02-28T02:02"]),
    ("2025-02-28b", "Thin margin for 1.2 h, lowest effective margin 2 (nominal 3)",
     "2025-02-28T09:00", ["2025-02-28T15:37"]),
    ("2025-03-02", "Thin margin for 3.1 h, lowest effective margin 2 (nominal 3)",
     "2025-03-02T09:00", ["2025-03-02T16:30"]),
    ("2025-09-18", "Thin margin for 2.3 h, lowest effective margin 2 (nominal 3)",
     "2025-09-17T19:00", ["2025-09-18T03:03"]),
]

# ---------------------------------------------------------------- analysis.py : CONFIG_CASES
# (name, description, before, during, after recovery). The script prints which validators changed
# quorum set, the diff, and the counterfactual recomputation of the blocking set.

CONFIG_CASES_EXTRA = [
    ("2022-02 unexplained", "Node blocking set 6 -> 5 for 2.4 days",
     "2022-02-25T12:00", "2022-02-27T12:00", "2022-03-01T12:00"),
    ("2022-07 Wirex period", "Nominal blocking set 6 -> 5 for 3 days during the Wirex trouble",
     "2022-07-09T12:00", "2022-07-11T12:00", "2022-07-25T12:00"),
    ("2022-07-13 organizations 2", "Nominal blocking set 4 (organizations 2) for 12.6 h",
     "2022-07-09T12:00", "2022-07-13T12:00", "2022-07-25T12:00"),
    ("2021-04-13 transient", "Node blocking set 5 for 5.4 h with a 30/9 top tier",
     "2021-04-12T12:00", "2021-04-13T15:00", "2021-04-14T12:00"),
]
