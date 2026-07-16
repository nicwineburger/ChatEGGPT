# YouTube Subscription Analysis

Analysis of 629 subscribed channels (from a Google Takeout `subscriptions.csv`),
enriched with live metadata from Google's InnerTube API
(`youtubei.googleapis.com` — the same backend youtube.com uses), categorized on
five axes, then clustered on text similarity.

## Method

1. **Fetch** (`fetch_channels.py`): one InnerTube `browse` call per channel ID →
   title, description, keywords, subscriber count, video count, family-safe flag.
   629/629 fetched; 6 channels returned empty metadata (terminated/deleted).
2. **Categorize** (`analyze.py` + `overrides.py`): each channel labeled on
   - **domain** (21 topic categories; 605 hand-curated labels + keyword-lexicon fallback)
   - **scale tier** (subscriber count buckets)
   - **volume tier** (video count buckets)
   - **creator type** (individual vs. org/brand, heuristic)
   - **subs-per-video** ("reach efficiency")
3. **Cluster**: TF-IDF over cleaned title+keywords+description (URLs and social
   boilerplate stripped, domain label injected as a token), KMeans with k chosen
   by silhouette score over k=8..20 → **k=19, silhouette 0.124**.

Outputs: `channels_enriched.csv` (every channel with all axes + cluster
assignment), `clusters.json` (per-cluster terms, sizes, examples).

## The axes at a glance

**Domain** (top 10 of 21):

| domain | n | median subs |
|---|---|---|
| video essays / media criticism | 92 | 293K |
| comedy / sketch | 70 | 136K |
| programming / tech | 63 | 224K |
| science | 60 | 670K |
| gaming | 54 | 72K |
| music | 40 | 208K |
| animation | 35 | 61K |
| engineering / making | 30 | **1.32M** |
| politics / society | 28 | 127K |
| general education | 25 | 515K |

**Scale**: micro <10K: 91 · small 10K–100K: 146 · mid 100K–1M: 243 ·
large 1M–10M: 132 · mega >10M: 11. Median 230K, mean 1.18M —
the mean is 5× the median, i.e. a handful of megachannels
(Mark Rober 79.8M, Zach King 43.1M, Kurzgesagt 25.3M, Vsauce 24.9M,
MKBHD 21.1M) sit atop a long mid-tail. Combined reach of all
subscriptions: ~738M subscribers.

**Volume**: 200 channels have fewer than 50 videos; only 30 have >1,000.

## The 19 clusters

| # | n | theme | flagship examples |
|---|---|---|---|
| 9 | 61 | mainstream science | Kurzgesagt, Vsauce, SmarterEveryDay, NileRed |
| 1 | 92 | video essays / film & culture | Every Frame a Painting, hbomberguy, Defunctland |
| 3 | 70 | comedy & sketch | Dropout, Bad Lip Reading, TomSka, RDCworld1 |
| 18 | 63 | programming & consumer tech | Fireship, Computerphile, MKBHD, Gamers Nexus |
| 5 | 53 | gaming (play & coverage) | Iron Pineapple, Digital Foundry, Polygon |
| 2 | 40 | music & musicians | Lorde, alyankovic, Adam Neely, Smooth McGroove |
| 13 | 35 | animation | TerminalMontage, Egoraptor, OneyNG |
| 15 | 30 | engineering & making | Mark Rober, colinfurze, ElectroBOOM, DIY Perks |
| 11 | 28 | politics / philosophy (BreadTube) | ContraPoints, Philosophy Tube, Shaun |
| 4 | 25 | edutainment generalists | CGP Grey, Tom Scott, CrashCourse, Wendover |
| 0 | 23 | retro tech & hardware | LGR, Techmoan, Gaming Historian |
| 12 | 21 | game design & criticism | GMTK, Joseph Anderson, NakeyJakey, Ahoy |
| 14 | 19 | speedrunning & glitch archaeology | Summoning Salt, pannenkoek2012, Zullie the Witch |
| 7 | 15 | podcasts & actual play | McElroys, Dimension 20, Friends at the Table |
| 6 | 14 | mathematics | 3Blue1Brown, Numberphile, Mathologer, Vihart |
| 10 | 13 | food (+ misc) | Kenji López-Alt, MinuteFood |
| 8 | 12 | nature / bio (+ sports storytelling) | PBS Eons, Microcosmos, Secret Base |
| 17 | 9 | personality vlogs | WheezyWaiter, yourharto |
| 16 | 6 | urbanism & transit | Not Just Bikes, donoteat01 |

## Interesting patterns

1. **This is "thinky YouTube."** Analysis-oriented domains — video essays,
   science, math, programming, game criticism, general education, politics —
   account for well over half the subscriptions. Pure entertainment (comedy,
   animation, music) is the other big block, but even there it skews toward
   craft (music theory, animation analysis, abridged parody) over passive viewing.

2. **Mid-tail loyalty, not megachannel chasing.** 38% of channels (237) have
   under 100K subscribers and 91 are under 10K — including channels with 9, 13,
   and 64 subscribers (friends' channels, most likely). Only 1.8% are >10M.
   The subscription list actively supports small creators rather than mirroring
   the YouTube front page.

3. **Quality-over-quantity auteurs are over-represented.** Ten channels have
   >1M subs on fewer than 60 videos (Every Frame a Painting: 64K subs *per
   video*; boburnham: 98K; Stuff Made Here: 119K; ContraPoints: 55K). At the
   other extreme sit daily-upload firehoses followed anyway (hankgames: 106
   subs/video across 1,500 videos). The subs-per-video axis spans four orders
   of magnitude — a taste for slow, dense, essayistic output.

4. **Engineering/science is the mainstream anchor; niches go deep.** Median
   subs by domain: engineering/making 1.3M, science 670K — these are followed
   at their biggest names. Meanwhile speedrunning (19 channels, including
   *both* pannenkoek2012 accounts), retro tech (23), urbanism (6), and actual-play
   podcasts (15) are deep vertical dives where median channel size drops to
   18K–250K. The profile: mainstream STEM + hyper-specific hobby rabbit holes.

5. **Superfan behavior: ~25 second channels.** CGPGrey2, 2veritasium,
   Numberphile2, The Slow Mo Guys 2, Stuff Made Here 2, Tom Scott plus,
   ContraPointsLive, Nightshift (Kurzgesagt After Dark), Defunctland After Dark,
   Cathode Ray Dude Gaiden, Technology Connextras, Beyond Fireship, D!NG,
   CGP Play, styro pyro 2, hankgames, ProZD Eats Food, Suede's Pokémon Journey…
   When this viewer likes a creator, they subscribe to the *whole* creator.

6. **A visible BreadTube → urbanism pipeline.** The politics cluster
   (ContraPoints, Philosophy Tube, Shaun, Innuendo Studios, F.D Signifier, Zoe
   Baker, CCK Philosophy) coexists with the urbanism cluster (Not Just Bikes,
   donoteat01, Car Free Keith) and adjacent media-criticism channels (Folding
   Ideas, Citations Needed) — the classic late-2010s leftist-explainer
   ecosystem, all present. Even a political campaign channel (Zohran Mamdani
   for NYC) made the list.

7. **Fossil record of 2008–2014 YouTube.** potterpuppetpals, homestarrunner,
   TeamFourStar, Little Kuriboh (subscribed *twice* — the only duplicate),
   GanXingba, Egoraptor, Glove and Boots, Nice Peter, RocketJump, Marble
   Hornets: the abridged-series/sketch era is preserved intact. Six channels
   are now terminated or empty (Vihart, Little Kuriboh, Faulerro, PurpleEyesWTF,
   Skull, ShadyVox) — subscriptions outliving their channels.

8. **Creator-first, not brand-first.** Roughly 70% of channels are individual
   creators. The orgs that do appear are creator-collectives or PBS-adjacent
   (Complexly/SciShow/CrashCourse, Dropout, Polygon/Secret Base, PBS Space
   Time/Eons/Infinite Series) rather than corporate media. Notably, the Green
   brothers' network alone accounts for 9+ subscriptions (vlogbrothers, Hank
   Green, hankgames, John Green, CrashCourse, Complexly, SciShow, SciShow Space,
   dftbarecords, thebrainscoop-adjacent).

9. **100% family-safe.** Not a single channel is flagged `isFamilySafe: false`
   by YouTube — remarkable for 629 subscriptions and consistent with the
   educational skew.

## Files

| file | contents |
|---|---|
| `subscriptions.csv` | original Takeout export (629 channels) |
| `fetch_channels.py` | InnerTube metadata fetcher |
| `analyze.py` | axis categorization + TF-IDF/KMeans clustering |
| `overrides.py` | 615 hand-curated domain labels |
| `channels.jsonl` | raw fetched metadata |
| `channels_enriched.csv` | every channel × all axes × cluster |
| `clusters.json` | cluster sizes, top terms, examples |

Reproduce with:

```sh
python3 fetch_channels.py subscriptions.csv channels.jsonl
pip install scikit-learn
python3 analyze.py channels.jsonl channels_enriched.csv clusters.json
```
