# Watch Time: How Much, and On What

Extends [WATCH_REPORT_V2.md](WATCH_REPORT_V2.md) from watch *counts* to watch
*time*. Counts overweight 4-minute videos and sleep starts; time is the honest
measure of attention.

## Method

Takeout only records when each video **started**, so time is estimated:

- **Durations**: fetched for 20,155 distinct videos via YouTube's InnerTube
  API — `player` endpoint until bot detection cut it off (~1,900 videos), then
  by paging 767 channels' upload tabs (`fetch_channel_durations.py`, 85,960
  library videos scraped). **66% of events have exact durations**; the rest
  are imputed from the median length of that channel's watched or library
  videos.
- **Credit per event**: `min(duration, gap to next video in the session)` —
  so skipping early credits only the gap; session-final videos capped at
  45 min.
- **Sleep starts**: any video started 23:30–07:00 is capped at **15 min** and
  tallied separately ("sleep onset"), reflecting that these are started
  deliberately but not finished awake. Autoplay tails were already removed in
  v2.

Known biases: Shorts aren't in channel video tabs, so short-heavy channels
impute slightly high; the 2024–26 numbers include the second household
viewer; nothing before May 2019 exists in the export at all.

## The headline

> **≈ 4,200 hours of engaged watching since May 2019 — 97 minutes per day,
> every day, for 7.2 years.** Plus ~800 hours of sleep-onset starts.

Ways to hold that number:

- **≈ 10% of waking life** (assuming 16 waking hours/day) from age 25 to 32.
- **≈ 2 years of full-time work** (at 2,080 h/yr).
- It's remarkably steady: every year lands between 85 and 116 min/day. The
  2025 peak (116) is partly the second viewer; the 2019 figure (112) is the
  young tail of the record.
- And it's the *floor* for lifetime: the 2007–2019 YouTube years — ages 13
  to 25 — are invisible.

## Attention is not what the counts said

Top channels by engaged hours (count-rank in brackets):

| hours | channel | rank by count |
|---|---|---|
| 202 h | Chris Remo (NYT crossword streams) | [2] |
| 128 h | Tom Scott | [1] |
| 99 h | Technology Connections | [9] |
| 86 h | Marques Brownlee | [5] |
| 86 h | hbomberguy | [22] |
| 82 h | Secret Base | [19] |
| 80 h | Noah Caldwell-Gervais | [25] |
| 75 h | Folding Ideas | [17] |
| 54 h | A More Civilized Age (podcast) | [38] |
| 54 h | Captain Disillusion | [6] |

- **The #1 use of your YouTube attention is doing the NYT crossword with
  Chris Remo** — 202 hours, a daily ritual that neither the subscription
  analysis nor the count ranking surfaced as what it is.
- **The long-form essayists are the real second tier.** hbomberguy, Secret
  Base, Noah Caldwell-Gervais, Folding Ideas, and Jenny Nicholson all leap
  20+ ranks when measured in hours. Action Button (rank 49 by count, 40 h)
  and A More Civilized Age (rank 38, 54 h) are the extreme cases: a handful
  of plays, each hours long.
- By domain, **video essays (16.8%) pull essentially even with general
  education (17.0%)** — by counts it was 10% vs 26%. The "×7 edutainment
  over-index" was largely a short-video counting artifact; by attention
  you're as much an essay/documentary viewer as a Tom Scott snacker.
- Comedy collapses further (8.8% of counts → 3.9% of hours); podcasts and
  wrestling/sports documentary (Secret Base) double their apparent weight.

## Texture of the habit

- **3.4 sessions per day, median 20 minutes.** This is grazing, not
  marathoning — the longest session in 7 years is 4.2 hours, and days like
  that are rare. YouTube fills interstitial time: the midday plateau
  (10 AM–1 PM) and the 6–10 PM evening ramp, peaking at 8 PM once sleep
  starts are excluded.
- **Rewatching is 22% of engaged hours** even with every sleep start capped
  at 15 minutes — nearly a quarter of attention goes to videos already seen.
  Combined with 70% of hours on subscribed channels (higher than the 64% of
  counts — subscribed content runs longer), the picture is strongly
  return-to-the-familiar: about half of all engaged time is either a repeat
  viewing or a Chris Remo/TC/Tom Scott staple.
- **Sleep onset is its own budget**: ~800 hours of drift-off starts across
  7 years (~13 min/night on nights it happens) — before counting the
  autoplay the TV kept playing to an empty room, which was another ~5,000
  events discarded in v2.

## Files

| file | contents |
|---|---|
| `fetch_durations.py` | InnerTube player-endpoint duration fetcher (rate-limited fate documented above) |
| `browse_lib.py` + `fetch_channel_durations.py` | channel videos-tab duration scraper |
| `estimate_time.py` | credit model + all statistics |
| `time_analysis.json` | aggregated results |

Reproduce: run the two fetchers, then `python3 estimate_time.py` (expects
`watch_filtered.jsonl` from the v2 pipeline alongside).
