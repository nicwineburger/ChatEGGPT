# Watch History × Subscriptions: Cross-Analysis

> **Superseded by [WATCH_REPORT_V2.md](WATCH_REPORT_V2.md).** Ground-truth
> feedback revealed that the overnight watching here is a TV sleep timer
> left running (autoplay), and the recent non-subscribed growth is largely a
> second household viewer. Finding 2 (sleep-aid volume) and Finding 5
> (algorithmic drift) are substantially artifacts; v2 re-runs everything
> with autoplay tails removed.

Correlates 7.2 years of watch history (Google Takeout, May 2019 → July 2026:
**31,547 watch events**, 30,977 attributable to a channel, across **4,675
distinct channels**) against the 629-channel subscription analysis in
[REPORT.md](REPORT.md).

Pipeline: `parse_watch.py` extracts events from Takeout's
`watch-history.html`; `correlate.py` joins them to `channels_enriched.csv` by
channel ID and emits `watch_analysis.json`. Raw watch history is deliberately
**not** committed — only aggregates.

## Headline numbers

- **66%** of attributable watches are on subscribed channels; the other 34%
  spread across ~4,000 never-subscribed channels.
- **138 subscriptions (22%) are fully dormant** — zero watches in 7.2 years.
- Top 10 subscribed channels = **44%** of all subscribed watching.
- **30.4% of all watch events are rewatches** of a video already seen.

## Finding 1: You subscribe like a curator, watch like a comfort-seeker

The subscription report called this "thinky YouTube" with mid-tail loyalty.
Watching tells a different story on both axes:

**Domain watch-index** (share of watching ÷ share of subscriptions):

| domain | subs share | watch share | index |
|---|---|---|---|
| general education | 4.0% | **33.1%** | **×8.3** |
| programming/tech | 10.0% | 10.9% | ×1.1 |
| science | 9.5% | 9.6% | ×1.0 |
| video essays | 14.6% | 11.5% | ×0.8 |
| comedy/sketch | 11.1% | 7.2% | ×0.6 |
| speedrun/glitch | 3.0% | 1.3% | ×0.4 |
| math | 2.2% | 0.8% | ×0.4 |
| animation | 5.6% | 1.7% | ×0.3 |
| politics (BreadTube) | 4.5% | 1.1% | ×0.3 |
| music | 6.4% | 0.9% | ×0.15 |
| urbanism | 1.0% | 0.1% | ×0.15 |

The 25 edutainment-generalist channels (4% of subscriptions) absorb a third of
all subscribed watching. Meanwhile the distinctive collector niches from the
subscription report — BreadTube, math, speedrunning, animation, urbanism —
are watched at a quarter of their subscription weight or less. Much of the
subscription list is *aspirational identity*; the watching is Technology
Connections and Tom Scott.

**Scale**: channels with 1M–10M subs are 21% of subscriptions but **69% of
watching**. Micro+small channels (<100K) are 38% of subscriptions but under
8% of watching. The "mid-tail loyalty" in the subscription list is real as
patronage, not as attention.

## Finding 2: Technology Connections is functionally a sleep aid

The single most striking pattern in the whole dataset:

- **2,412 watches** of Technology Connections — 7.8% of *all* attributable
  watching, 11.8% of subscribed watching, more than the next two channels
  combined (Tom Scott 1,951, Chris Remo 742).
- **88% of those watches fall between 11 PM and 5 AM** (vs 32% baseline).
- **111 different TC videos have been watched 10+ times each.** All 15 of the
  most-rewatched videos in the entire history are TC episodes (25–34 plays
  each: the fridge video, drip coffee makers, laundry detergent, lava lamps,
  smoke alarms…), plus CGP Grey's 2½-hour unedited garlic-bread flight footage
  (33 plays) — the canonical "fall asleep to this" video.
- The overall hourly histogram peaks at midnight–1 AM.

A familiar, evenly-narrated back catalog on loop at midnight is comfort/sleep
listening, and it single-handedly explains the ×8.3 general-education index.

## Finding 3: The dormant 22% is the fossil record, confirmed

The subscription report guessed that the 2008–2014-era channels were
preserved relics. The watch data proves it: dormant subscriptions skew
heavily comedy/sketch (26), video essays (21), and music (15). The largest
never-watched subscriptions — Bad Lip Reading, Lorde, Nice Peter, OneyNG,
Marble Hornets, PBS Idea Channel — are almost all from that era. Comedy's
watch share collapsed from 18% (2019) to ~4% (2023+): taste moved on;
the subscriptions stayed.

Music looks dormant but is really *displaced*: musician subscriptions get
0.9% of watching, yet there are 381 plays on auto-generated "— Topic"
channels and whole binge days of Odesza and Coldplay — music listening moved
to autoplay/mixes where subscriptions don't matter.

## Finding 4: The unsubscribed 34% reveals two hidden appetites

Top never-subscribed channels watched: IGN (304), Vox (227), **Weird History
Food (168)**, Nintendo (140), Bob Ross (124), PlayStation (123), Veritasium
(114), **Tasting History with Max Miller (109)**, Netflix (100), dunkey (91),
Chapo Trap House (56), Internet Historian (45), Binging with Babish (40).

1. **Food is massively under-subscribed.** Only 6 food subscriptions (1%),
   but ~1,800 watches of food-history/cooking channels, nearly all
   unsubscribed. Weird History Food + Tasting History alone outdraw most of
   the subscribed niches.
2. **Trailer-and-coverage snacking** (IGN, Nintendo, PlayStation, Netflix,
   Marvel, HBO Max) is a steady diet that never converts to subscriptions —
   consistent with the subscription list's creator-first character: brands
   get watched, people get subscribed.

Oddities: **Veritasium — 114 watches, yet only the dead second channel
(2veritasium) is subscribed**, and the main channel never was. And the #3
most-watched channel overall is Chris Remo… doing daily NYT crossword streams
— a daily-ritual channel the subscription report had filed under "gaming."

## Finding 5: Algorithmic drift is accelerating

Share of watching on subscribed channels by year:

| year | events | subscribed share |
|---|---|---|
| 2019 | 2,729 | 56.6% |
| 2021 | 4,213 | 71.8% |
| 2022 | 4,023 | **75.0%** |
| 2024 | 4,266 | 67.6% |
| 2025 | 5,422 | 65.0% |
| 2026 | 2,743 | **54.3%** |

2021–2023 was peak subscription-driven viewing; since then volume is up
(2025 is the biggest year) but the subscribed share has slid 20 points —
more feed, less follow. 2026 also shows a video-essay resurgence (27% of
subscribed watching, highest since 2019) driven by Defunctland — including a
146-video New Year's Day 2026 marathon, the biggest single day on record.

## Finding 6: Rhythm

- **Night owl**: watching peaks 11 PM–1 AM; the 3–6 AM trough is shallow.
- Weekdays out-watch weekends (Mon highest, Sat lowest) — YouTube as
  background/wind-down, not weekend event.
- Signature binges: 79 ProZD skits in one day (Feb 2021), 36-video IGN
  session (Dec 2023), 30 CGP Grey videos in a day (Aug 2023), Odesza music
  marathon (Apr 2025), Defunctland New Year's marathons two years running.

## Files

| file | contents |
|---|---|
| `parse_watch.py` | Takeout `watch-history.html` → JSONL parser |
| `correlate.py` | joins watch events to `channels_enriched.csv`, prints all stats |
| `watch_analysis.json` | aggregated results (top channels, domain indices, dormant list) |

Reproduce: `python3 parse_watch.py watch-history.html watch.jsonl && python3 correlate.py watch.jsonl channels_enriched.csv`
