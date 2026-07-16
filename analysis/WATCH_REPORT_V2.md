# Watch Habits v2: Sleep-Autoplay Removed

Revision of [WATCH_REPORT.md](WATCH_REPORT.md) after ground-truth feedback:
the overnight watching was a sleep timer left running (fall asleep to 1–2
videos, autoplay continues), and a second household viewer — who doesn't
subscribe — ramped up in the last two years.

## The filter

`filter_sleep.py` sessionizes the history (events ≤45 min apart = one
session). Once a session crosses into the sleep window (23:30–07:00) it keeps
the next **2** events — the videos deliberately put on to fall asleep to —
and drops the remainder of the session, including autoplay that runs past
morning.

Result: **4,974 of 31,547 events (15.8%) removed as autoplay.** Sanity checks
line up with the ground truth: the most-dropped channels are exactly the
sleep-content suspects (Technology Connections −1,220, Tom Scott −401,
Defunctland −233), dropped volume grows year over year (37 in 2019 → 1,230 in
2025) as the TV habit grew, and the filtered hourly curve now looks human —
the midnight–5 AM plateau collapses (32% → 19% of events, and most of the
remainder is the kept pre-sleep picks).

Remaining events: **26,573** (26,034 attributable, 4,213 distinct channels).

## What actually changed

| metric | raw | filtered |
|---|---|---|
| #1 channel | Technology Connections (2,412) | **Tom Scott (1,550)** |
| Technology Connections | 2,412 (7.8% of everything) | 1,192 |
| top-10 concentration | 44.0% | 40.5% |
| rewatch share | 30.4% | 24.5% |
| most-rewatched video | 34 plays | 19 plays |
| general-education index | ×8.3 | ×7.3 |
| night share (11 PM–5 AM) | 32% | 19% |

**What was an artifact:** TC's #1 spot, roughly half its play count, and the
extreme rewatch numbers. The all-TC top-15 rewatch list was the fridge video
looping at 3 AM.

**What survives:** more than you might expect.

- TC is still #2 with ~1,200 *deliberate* plays, and 78% of them are still
  the late-evening wind-down picks — it genuinely is the fall-asleep channel,
  just at half the apparent volume.
- General education still over-indexes ×7.3: awake-you really does watch Tom
  Scott, vlogbrothers, and CGP Grey far out of proportion to their 4%
  subscription share. The curator-vs-comfort gap is real, not an autoplay
  artifact.
- Rewatching is still a quarter of all viewing, but the filtered rewatch list
  is more honest: comfort *video essays* — Folding Ideas' "This is Financial
  Advice" (18×) and "Line Goes Up" (15×), Jenny Nicholson's Vampire Diaries
  video (17×), Defunctland's EPCOT (17×), Captain Disillusion (16×) — with TC
  favorites (detergent, smoke alarms, turn signals) at 17–19 plays each.
- The dormant-22% fossil record, the large-channel attention skew (1M–10M
  channels: 21% of subs, 65% of watching), and the domain indices (music
  ×0.16, politics ×0.30, animation ×0.34) barely move. Those conclusions
  stand.

## Your actual daily shape

With autoplay gone, the rhythm is: a **late-morning/lunch block**
(10 AM–1 PM, the biggest sustained plateau of the day), an **evening ramp**
from 6 PM peaking at 10–11 PM, then 1–2 wind-down videos, and sleep. Monday
is the heaviest day, Friday–Sunday the lightest — YouTube is a weekday
routine, not a weekend event.

The real binge days are also more flattering: music marathons (Odesza,
Coldplay/Fray nostalgia day, a Luke Combs day), a 46-video ProZD skit run,
and 36 Tom Scott videos in a day when he wound down the channel (May 2025).

## The second viewer is visible in the data

Non-subscribed channels with ≥12 watches concentrated ≥90% in 2024–2026 form
a coherent cluster that doesn't match the subscriber's taste profile at all:

- **Food history/cooking**: Weird History Food (162, all 2025–26), Tasting
  History (102), Epicurious (23)
- **Ambient/TV-adjacent**: Bob Ross (65, all 2025), The CW Network (36),
  YouTube Movies (23)
- **True-crime/animals**: Scary Interesting (28), Girl With The Dogs (23)
- **Toddler content**, 2023–24: Ms Rachel (17), Super Simple Songs (12)

That cluster alone is ~500 watches — 53 in 2024, 285 in 2025, 152 in the
first half of 2026 — and accounts for **18% of all 2025–26 non-subscribed
watching**. Excluding it, the 2025 subscribed share goes back up to ~70%,
right at the 2021–2023 plateau. So the "algorithmic drift" in v1 was mostly
misattribution: **the subscriber's own habits didn't drift; the household
got a second viewer.** (2026 still dips to ~58% excluding the cluster —
either more of her watching than the heuristic catches, or a genuine recent
shift.)

This also reassigns v1's "hidden food appetite": the food-history watching is
essentially all in the second-viewer cluster and era. The subscriber's own
under-subscribed blind spots are more modest: Veritasium (98 deliberate
watches, still only subscribed to the dead second channel), dunkey (88),
Internet Historian (42), Man Carrying Thing (48, mostly 2026).

Meanwhile some 2024+ non-subscribed channels *do* match the subscriber's
profile and are just unconverted subscriptions: Low Level, Snazzy Labs,
Austin John Plays, The B1M, fern.

## Revised one-paragraph profile

A weekday-rhythm viewer who watches lunch-and-evening, almost two-thirds
from a subscription list built years ago, concentrated on a stable core of
edutainment anchors (Tom Scott, Technology Connections, vlogbrothers, CGP
Grey) plus a daily crossword ritual (Chris Remo, #3 overall). A quarter of
viewing is deliberate rewatching of comfort essays and TC classics. The
subscription list's long tail is patronage, not attention; its niches
(music, politics, animation, math) are identity more than habit. The
apparent late-night binge persona was a sleep timer, and the apparent recent
surrender to the algorithm was mostly someone else on the couch.

## Files

| file | contents |
|---|---|
| `filter_sleep.py` | sessionization + sleep-autoplay filter |
| `watch_analysis_filtered.json` | aggregated stats on filtered data |

Reproduce: `python3 parse_watch.py watch-history.html watch.jsonl && python3 filter_sleep.py watch.jsonl watch_filtered.jsonl && python3 correlate.py watch_filtered.jsonl channels_enriched.csv`
