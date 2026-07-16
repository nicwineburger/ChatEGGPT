#!/usr/bin/env python3
"""Estimate engaged watch time from filtered history + video durations.

Per event: credit = min(duration, gap to next event in session).
Session-final events: credit = min(duration, 45 min).
Sleep-window events (>=23:30 or <07:00): credit capped at 15 min ("sleep
onset") and tallied separately from engaged time.
"""
import json, csv, statistics, sys
from datetime import datetime, time as dtime
from collections import Counter, defaultdict

watch = [json.loads(l) for l in open("watch_filtered.jsonl")]
durs = {}
for l in open("durations.jsonl"):
    d = json.loads(l)
    if d["seconds"]:
        durs[d["videoId"]] = d["seconds"]
# durations scraped from channel video listings; also per-channel library medians
lib_med = {}
try:
    for l in open("channel_durations.jsonl"):
        d = json.loads(l)
        for v, s in d["videos"].items():
            durs.setdefault(v, s)
        if d["videos"]:
            lib_med[d["channelId"]] = statistics.median(d["videos"].values())
except FileNotFoundError:
    pass
subs = list(csv.DictReader(open("channels_enriched.csv")))
by_id = {r["channelId"]: r for r in subs}

for r in watch:
    r["dt"] = datetime.strptime(r["date"] + " " + r["time"], "%Y-%m-%d %H:%M:%S")
watch.sort(key=lambda r: r["dt"])

# impute missing: median of channel's watched videos, else channel library
# median, else global median of watched videos
ch_durs = defaultdict(list)
for r in watch:
    if r["videoId"] in durs and r["channelId"]:
        ch_durs[r["channelId"]].append(durs[r["videoId"]])
ch_med = {c: statistics.median(v) for c, v in ch_durs.items()}
glob_med = statistics.median(durs[r["videoId"]] for r in watch if r["videoId"] in durs)
n_missing = 0
for r in watch:
    d = durs.get(r["videoId"])
    if not d:
        n_missing += 1
        d = ch_med.get(r["channelId"]) or lib_med.get(r["channelId"]) or glob_med
    r["dur"] = d
n_exact = len(watch) - n_missing
print(f"exact durations: {n_exact}/{len(watch)} events ({100*n_exact/len(watch):.0f}%)")

GAP_MIN, TERMINAL_CAP, SLEEP_CAP = 45, 45 * 60, 15 * 60
SLEEP_START, SLEEP_END = dtime(23, 30), dtime(7, 0)
def asleep(dt):
    return dt.time() >= SLEEP_START or dt.time() < SLEEP_END

# sessionize and credit
sessions, cur = [], []
for r in watch:
    if cur and (r["dt"] - cur[-1]["dt"]).total_seconds() > GAP_MIN * 60:
        sessions.append(cur); cur = []
    cur.append(r)
if cur: sessions.append(cur)

for s in sessions:
    for i, r in enumerate(s):
        gap = (s[i+1]["dt"] - r["dt"]).total_seconds() if i+1 < len(s) else None
        credit = min(r["dur"], gap) if gap is not None else min(r["dur"], TERMINAL_CAP)
        if asleep(r["dt"]):
            r["credit"], r["sleep"] = min(credit, SLEEP_CAP), True
        else:
            r["credit"], r["sleep"] = credit, False

eng = [r for r in watch if not r["sleep"]]
slp = [r for r in watch if r["sleep"]]
H = 3600
tot_e = sum(r["credit"] for r in eng) / H
tot_s = sum(r["credit"] for r in slp) / H
days = (watch[-1]["dt"] - watch[0]["dt"]).days
print(f"missing durations imputed: {n_missing}/{len(watch)} events")
print(f"\nENGAGED time: {tot_e:,.0f} h over {days} days "
      f"({60*tot_e/days:.1f} min/day, {tot_e/days*7:.1f} h/wk)")
print(f"sleep-onset time (capped 15min/event): {tot_s:,.0f} h")
print(f"median video length watched: {statistics.median(r['dur'] for r in eng)/60:.1f} min; "
      f"median credited: {statistics.median(r['credit'] for r in eng)/60:.1f} min")

print("\n=== engaged hours by year ===")
by_y = defaultdict(float)
for r in eng: by_y[r["date"][:4]] += r["credit"]
yr_days = {"2019": 227, "2026": 197}
for y in sorted(by_y):
    d = yr_days.get(y, 365)
    print(f"  {y}: {by_y[y]/H:6.0f} h  ({60*by_y[y]/H/d:.0f} min/day)")

print("\n=== top 25 channels by ENGAGED hours (rank by count in brackets) ===")
ch_h = defaultdict(float); ch_n = Counter()
for r in eng:
    if r["channelId"]:
        ch_h[r["channelId"]] += r["credit"]; ch_n[r["channelId"]] += 1
names = {}
for r in watch:
    if r["channelId"]: names[r["channelId"]] = r["channelName"]
cnt_rank = {c: i+1 for i, (c, _) in enumerate(ch_n.most_common())}
for c, sec in sorted(ch_h.items(), key=lambda x: -x[1])[:25]:
    sub = "sub" if c in by_id else "   "
    print(f"  {sec/H:6.0f} h  [{cnt_rank[c]:4d} by count] {sub}  {names[c][:40]}")

print("\n=== engaged hours: domain share (vs watch-count share) ===")
dom_h = defaultdict(float); dom_n = Counter(); tot_sub_h = 0
for r in eng:
    if r["channelId"] in by_id:
        d = by_id[r["channelId"]]["domain"]
        dom_h[d] += r["credit"]; dom_n[d] += 1; tot_sub_h += r["credit"]
for d, sec in sorted(dom_h.items(), key=lambda x: -x[1]):
    print(f"  {d:24s} {100*sec/tot_sub_h:5.1f}% of hours  ({100*dom_n[d]/sum(dom_n.values()):5.1f}% of counts)")

sub_h = sum(r["credit"] for r in eng if r["channelId"] in by_id)
att_h = sum(r["credit"] for r in eng if r["channelId"])
print(f"\nsubscribed share of engaged hours: {100*sub_h/att_h:.1f}%")

# rewatch time
seen, rew = set(), 0.0
for r in eng:
    if r["videoId"] in seen: rew += r["credit"]
    seen.add(r["videoId"])
print(f"rewatch share of engaged hours: {100*(rew/H)/tot_e:.1f}%")

# sessions
es = [[r for r in s if not r["sleep"]] for s in sessions]
es = [s for s in es if s]
slens = [sum(r["credit"] for r in s) / 60 for s in es]
print(f"\nsessions: {len(es)}, median {statistics.median(slens):.0f} min, "
      f"mean {statistics.mean(slens):.0f} min; {len(es)/days:.1f} sessions/day")
print("longest sessions:")
for s in sorted(es, key=lambda s: -sum(r['credit'] for r in s))[:5]:
    hrs = sum(r["credit"] for r in s) / H
    top = Counter(r["channelName"] for r in s if r["channelName"]).most_common(2)
    print(f"  {s[0]['date']} {s[0]['time'][:5]}: {hrs:.1f} h, {len(s)} videos — {top}")

# hours-by-hour-of-day (engaged)
hh = defaultdict(float)
for r in eng: hh[r["dt"].hour] += r["credit"]
print("\nengaged hours by clock hour:")
mx = max(hh.values())
for h in range(24):
    v = hh.get(h, 0) / H
    print(f"  {h:02d}  {'#' * int(40 * hh.get(h,0) / mx)} {v:.0f}h")

json.dump({
    "engagedHours": round(tot_e), "sleepOnsetHours": round(tot_s),
    "minPerDay": round(60 * tot_e / days, 1),
    "hoursByYear": {y: round(v / H) for y, v in sorted(by_y.items())},
    "topChannelsByHours": [
        {"name": names[c], "hours": round(sec / H, 1), "watches": ch_n[c],
         "countRank": cnt_rank[c], "subscribed": c in by_id}
        for c, sec in sorted(ch_h.items(), key=lambda x: -x[1])[:40]],
    "domainHoursShare": {d: round(100 * sec / tot_sub_h, 2)
                         for d, sec in sorted(dom_h.items(), key=lambda x: -x[1])},
    "subscribedShareOfHours": round(100 * sub_h / att_h, 1),
}, open("time_analysis.json", "w"), indent=2, ensure_ascii=False)
print("\nwrote time_analysis.json")
