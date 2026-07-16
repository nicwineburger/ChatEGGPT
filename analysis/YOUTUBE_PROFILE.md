# The Complete YouTube Profile

The capstone of the full analysis chain — subscriptions ([REPORT.md](REPORT.md)),
watch history ([WATCH_REPORT.md](WATCH_REPORT.md), [v2](WATCH_REPORT_V2.md)),
and watch time ([WATCH_TIME_REPORT.md](WATCH_TIME_REPORT.md)) — corrected by
ground truth from the subject: overnight events are a forgotten TV sleep
timer; a second household viewer (who never subscribes) ramped up in 2024+;
the account is also signed in at the subject's parents' house; born 1994,
on YouTube since 2007.

**Data**: 629 subscriptions · 31,547 watch events (May 2019 – Jul 2026) ·
6,383 searches (Oct 2011 – Jul 2026) · durations for 26,000+ videos fetched
from YouTube's InnerTube API (player endpoint + channel Videos/Live/Shorts
tab paging).

**Confidence**: after removing 4,974 autoplay events, **89.3% of the
remaining 26,573 events carry exact video durations**; 10.7% are imputed
from channel medians (deleted/private videos — the irreducible floor).
Time credited per event is `min(duration, gap to next video)`, 45-min cap on
session-final videos, 15-min cap on sleep-window (23:30–07:00) starts.
Headline totals moved less than ±2% across the last two coverage upgrades —
they are stable.

---

## 1. The scale

> **≈ 4,350 hours of engaged watching in 7.2 years — 100 minutes a day,
> every single day** — plus ≈ 800 hours of fall-asleep starts, plus an
> unknowable amount the TV played to an empty room (≈ 5,000 discarded
> autoplay events).

- **YouTube happened on 2,592 of 2,616 days (99.1%).** The longest break
  since May 2019 is **four days**. There is no vacation, illness, or life
  event in seven years that produced a YouTube-free week.
- That's ≈ 10% of waking life from age 25 to 32, or 2.1 years of full-time
  work.
- It is strikingly stable: every year lands between 89 and 121 min/day.
  The 2025 high (121) includes the second viewer's share.
- And it's a floor. The record begins at age 25; YouTube began at age 13.
  The first twelve years — more than half the YouTube life — exist only as
  fossils (§5).

## 2. The shape of a day

Three-and-a-half sessions a day, median 23 minutes. YouTube is mortar, not
brick: a midday block (10 AM–1 PM), an evening ramp from 6 PM peaking at
8–9 PM, then one or two wind-down videos after 11:30. Mondays are the
heaviest day, weekends the lightest — this is a weekday-routine medium, not
weekend entertainment. Marathons are vanishingly rare: the longest engaged
session in seven years is 4.5 hours, and most "binge days" in the raw data
were the sleep timer.

## 3. The cast

**The ritual.** The single largest object in the attention budget is
**Chris Remo's daily New York Times crossword stream: 278 hours across 667
distinct days** — every other day for five years, 6.4% of all engaged
watching. No other lens (subscriptions, counts) revealed it; only time did.

**The anchors.** Tom Scott (127 h — #1 by count at 1,550 plays),
Technology Connections (99 h engaged, *plus* the crown as sleep aid),
Marques Brownlee (86 h), vlogbrothers (50 h).

**The essayists.** The real second tier by attention, invisible by count:
hbomberguy (84 h), Noah Caldwell-Gervais (80 h), Secret Base (77 h),
Folding Ideas (75 h), Jenny Nicholson (48 h), Defunctland (43 h), Action
Button (39 h from just ~30 plays). A Star Wars podcast (A More Civilized
Age, 54 h) and Cathode Ray Dude (52 h) round out a top tier that is
overwhelmingly **long-form, single-author, analytical**.

**The evergreens.** 48 channels were watched in *every* calendar year of
the record — vlogbrothers, CGP Grey, Jenny Nicholson, RedLetterMedia,
Summoning Salt, ProZD, Captain Disillusion… The core cast has near-zero
turnover across seven years.

**The loyalty is to people.** 70% of engaged hours go to subscribed
channels. Brand channels (IGN, Nintendo, Netflix, PlayStation) get watched
— trailers and coverage, ~2,000 events — but almost never subscribed.
When a *person* earns trust, the whole person gets subscribed: ~25 second
channels (Technology Connextras, 2veritasium, CGPGrey2, Defunctland After
Dark…). The Green brothers alone hold 9+ subscription slots and ~130 hours.

## 4. Three lenses, three different viewers

| lens | apparent profile |
|---|---|
| **subscriptions** (629) | a curator: video essays 15%, comedy 11%, programming 10%, science 10%, music 6%, BreadTube 4.5% — "thinky YouTube" with a long mid-tail of small creators |
| **watch counts** | an edutainment snacker: general education ×7 over-index, Tom Scott #1, comfort rewatching everywhere |
| **watch hours** | a long-form listener: video essays and general education tied at 16.4%, gaming 13%, a daily crossword ritual on top, essays and podcasts doubled in weight |

All three are real, but they describe different behaviors: **subscribing is
identity, counting is habit, hours are attention.** The distinctive
subscription niches — music, animation, math, politics, urbanism — get
1–2% of hours each. They are patronage and past selves, not viewing. The
BreadTube shelf is the clearest case: ContraPoints was the single
most-searched term of 2015–2018 (a genuinely watched former habit) and is
still watched every year, but politics now takes 2.4% of hours.

**Comfort is the signature mode.** 22% of engaged hours are rewatches even
with every sleep start capped at 15 minutes. The comfort canon: Folding
Ideas ("This is Financial Advice", "Line Goes Up"), Jenny Nicholson's
Vampire Diaries video, Defunctland's EPCOT, Captain Disillusion, and the
Technology Connections classics (detergent, smoke alarms, turn signals).
Add the ritual and the evergreen anchors, and **roughly half of all
attention is return visits to the known** — YouTube functioning as a
familiar radio station with pictures.

## 5. The deep past (2007–2019), reconstructed

The watch log begins abruptly on May 19, 2019 — a settings artifact (watch
history was off or cleared; search history survives from October 2011).
Ages 13–25 are reconstructed from two proxies:

- **Search archaeology.** 2011–2014 (high school → college): Crash Course,
  Vsauce, vlogbrothers, Clone High, Mountain Goats songs — peak
  nerdfighter, watching Crash Course *while taking the classes*. 2015–2018
  (early 20s): ContraPoints, Game Grumps, vine compilations, Persona 5
  soundtracks. vlogbrothers appears in the top searches of **every era
  across 15 years** — the single longest thread in the data.
- **The fossil record.** 138 subscriptions (22%) have zero watches since
  2019, skewed exactly toward 2008–2014 YouTube: Bad Lip Reading, Nice
  Peter, potterpuppetpals, TeamFourStar, Marble Hornets, OneyNG. Six are
  dead channels kept anyway. The subscription list is archaeological strata:
  each era's taste preserved where it stopped.

The record we do have starts *fully formed* — day one is Kurzgesagt, Tom
Scott, MKBHD, ContraPoints — confirming the core cast predates the log by
years.

## 6. The household in the data

One account, at least four viewers, all separable:

- **The subject**: everything above.
- **The spouse** (2024+, doesn't subscribe): a coherent non-subscribed
  cluster — Weird History Food (162 plays / 32 h), Tasting History, Bob
  Ross, The CW, Girl With The Dogs, Scary Interesting, Epicurious — ~500
  events, 18% of recent non-subscribed viewing. Excluding it, the
  subject's subscribed share holds at ~70%, unchanged since 2021: **the
  apparent "algorithmic drift" of 2024–26 was mostly another person.**
- **The parents' house TV**: Bill Maher / Club Random — and a search
  pattern of "bill maher full episode" with few resulting watches
  (searching for something YouTube doesn't legally have).
- **The grandkids** (via the parents' TV, 2023+): Ms Rachel, Super Simple
  Songs, Blippi, Peppa Pig — ~80 events timed to their ages.
- **The sleep timer**: ~5,000 discarded overnight autoplay events, growing
  yearly — the "phantom fifth viewer" that inflated every naive metric.

## 7. Oddities and blind spots

- **Veritasium**: 98 engaged watches, watched every year — but only the
  dead second channel (2veritasium) is subscribed. The main channel
  subscription was apparently never made (or was lost).
- **Unconverted regulars** matching the subject's own taste: dunkey,
  Internet Historian, Man Carrying Thing, Low Level, Snazzy Labs — watched
  like subscriptions, never subscribed.
- **Music is displaced, not dead**: musician subscriptions get ~1% of
  hours, but auto-generated "— Topic" channels host real listening binges
  (an Odesza marathon, a Coldplay/Fray/Script nostalgia day, a Luke Combs
  day). Music moved to autoplay mixes where subscribing is meaningless.
- **Shorts are nearly absent**: 245 events (<1%) — for a 2020s account, an
  almost total non-adoption of the format.
- **The one duplicate subscription** in 629: Little Kuriboh, twice — a
  2008-era abridged-series creator subscribed so early the follow itself
  got fossilized and re-made.

## 8. One-paragraph portrait

A 32-year-old who has watched YouTube for 100 minutes a day, every day,
since the record began — not as event television but as ambient
infrastructure: the lunch hour, the evening wind-down, the crossword
companion, the voice falling asleep to. The taste is long-form, single-author,
analytical — video essays, edutainment, technology post-mortems, game
criticism — delivered almost entirely by a cast of ~50 creators that has
barely changed since college, several of whom have been there since high
school. Half of all attention is re-visitation: rewatched essays, the daily
ritual, the same explainer channels. The subscription list is a museum of
every self since 2007 — nerdfighter, abridged-series fan, BreadTube-era
leftist, tech enthusiast — maintained but not curated, while the actual
watching flows through a much narrower, warmer channel: familiar voices,
returned to daily, one of which is just a man doing the crossword.

---

## Appendix: headline numbers

| metric | value |
|---|---|
| engaged watch time | 4,351 h (99.9 min/day; 11.7 h/wk) |
| sleep-onset starts | 794 h (capped 15 min/event) |
| discarded sleep-timer autoplay | 4,974 events |
| active days | 2,592 / 2,616 (99.1%); longest gap 4 days |
| sessions | 8,976 · 3.4/day · median 23 min · max 4.5 h |
| distinct videos / channels | 20,155 / 4,675 |
| exact-duration coverage | 89.3% of events |
| subscribed share | 70.3% of hours (64% of counts) |
| rewatch share | 22.0% of hours |
| #1 channel by hours | Chris Remo, 278 h (667 days) |
| evergreen channels (all 8 years) | 48 |
| dormant subscriptions | 138/629 (22%) |
| spouse cluster | ~500 events / ~60 h, 2024+ |
| grandkid + grandparent cluster | ~100 events |
| busiest engaged year | 2025 (737 h — includes spouse) |

Pipeline: `parse_watch.py` → `filter_sleep.py` → `fetch_durations.py` +
`fetch_channel_durations.py` + `fetch_missing.py` + `fetch_remaining.py` →
`estimate_time.py` → `time_analysis.json`.
