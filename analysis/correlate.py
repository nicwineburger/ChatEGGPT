#!/usr/bin/env python3
"""Cross-analyze watch history against the enriched subscription data."""
import json, csv, sys
from collections import Counter, defaultdict
import numpy as np

WATCH, SUBS = sys.argv[1], sys.argv[2]

watch = [json.loads(l) for l in open(WATCH)]
subs = list(csv.DictReader(open(SUBS)))
by_id = {r["channelId"]: r for r in subs}

events = [w for w in watch if not w["ad"]]
with_ch = [w for w in events if w["channelId"]]
sub_events = [w for w in with_ch if w["channelId"] in by_id]

print(f"watch events: {len(events)} ({len(with_ch)} attributable to a channel)")
print(f"on subscribed channels: {len(sub_events)} "
      f"({100*len(sub_events)/len(with_ch):.1f}% of attributable)")
print(f"distinct channels watched: {len(set(w['channelId'] for w in with_ch))}")

# --- per-subscription watch counts ------------------------------------
cnt = Counter(w["channelId"] for w in sub_events)
print("\n=== top 25 most-watched subscriptions ===")
for cid, n in cnt.most_common(25):
    r = by_id[cid]
    print(f"  {n:5d}  {r['title'][:36]:36s} {r['domain']}")

watched_ids = set(cnt)
dormant = [r for r in subs if r["channelId"] not in watched_ids]
print(f"\ndormant subscriptions (0 watches in 7.2 yrs): {len(dormant)}/{len(subs)}")
print("dormant by domain:", Counter(r["domain"] for r in dormant).most_common(10))
notable_dormant = sorted(dormant, key=lambda r: -(int(r["subscribers"] or 0)))[:15]
print("largest dormant:", [r["title"] for r in notable_dormant])

# concentration
top = cnt.most_common()
tot = sum(cnt.values())
for k in (10, 25, 50):
    print(f"top {k} subs channels = {100*sum(n for _,n in top[:k])/tot:.1f}% of subscribed watching")

# --- domain: subscription share vs watch share ------------------------
dom_subs = Counter(r["domain"] for r in subs)
dom_watch = Counter(by_id[w["channelId"]]["domain"] for w in sub_events)
print("\n=== domain | subs share | watch share | index ===")
rows_out = []
for d in sorted(dom_subs, key=lambda d: -dom_watch.get(d, 0)):
    ss = dom_subs[d] / len(subs)
    ws = dom_watch.get(d, 0) / max(1, sum(dom_watch.values()))
    idx = ws / ss if ss else 0
    rows_out.append((d, dom_subs[d], dom_watch.get(d, 0), ss, ws, idx))
    print(f"  {d:24s} {100*ss:5.1f}% {100*ws:5.1f}%  x{idx:4.2f}")

# --- most watched NON-subscribed channels ------------------------------
nonsub = Counter((w["channelId"], w["channelName"]) for w in with_ch
                 if w["channelId"] not in by_id)
print("\n=== top 30 non-subscribed channels watched ===")
for (cid, name), n in nonsub.most_common(30):
    print(f"  {n:5d}  {name}")

# --- temporal ----------------------------------------------------------
print("\n=== per year: events, subscribed-share ===")
by_year = defaultdict(list)
for w in with_ch:
    by_year[w["date"][:4]].append(w)
for y in sorted(by_year):
    ws = by_year[y]
    s = sum(1 for w in ws if w["channelId"] in by_id)
    print(f"  {y}: {len(ws):5d} events, {100*s/len(ws):4.1f}% subscribed")

print("\n=== domain mix by year (top 6 domains, % of attributable+subscribed) ===")
doms = [d for d, _ in dom_watch.most_common(8)]
hdr = "  year " + "".join(f"{d[:14]:>16s}" for d in doms)
print(hdr)
for y in sorted(by_year):
    ws = [w for w in by_year[y] if w["channelId"] in by_id]
    c = Counter(by_id[w["channelId"]]["domain"] for w in ws)
    print(f"  {y} " + "".join(f"{100*c.get(d,0)/max(1,len(ws)):15.1f}%" for d in doms))

# --- time of day / weekday --------------------------------------------
import datetime
hours = Counter(int(w["time"][:2]) for w in events)
print("\n=== watches by hour (local) ===")
for h in range(24):
    print(f"  {h:02d}:00 {'#'*(hours.get(h,0)//60)} {hours.get(h,0)}")
wd = Counter(datetime.date(*map(int, w["date"].split("-"))).strftime("%a") for w in events)
print("weekday:", [(d, wd[d]) for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]])

# --- binges & rewatches -------------------------------------------------
per_day = Counter(w["date"] for w in events)
print("\n=== biggest days ===")
for d, n in per_day.most_common(8):
    ws = [w for w in events if w["date"] == d and w["channelId"]]
    chans = Counter(w["channelName"] for w in ws).most_common(3)
    print(f"  {d}: {n} videos — {chans}")

vids = Counter((w["videoId"], w["videoTitle"]) for w in events)
print("\n=== most-rewatched videos ===")
for (vid, t), n in vids.most_common(15):
    print(f"  {n:3d}x  {t[:70]}")

# --- scale tier of watching vs subscribing ------------------------------
tier_subs = Counter(r["scaleTier"] for r in subs)
tier_watch = Counter(by_id[w["channelId"]]["scaleTier"] for w in sub_events)
print("\n=== scale tier | subs share | watch share ===")
for t in sorted(tier_subs):
    ss = tier_subs[t] / len(subs)
    ws = tier_watch.get(t, 0) / max(1, sum(tier_watch.values()))
    print(f"  {t:22s} {100*ss:5.1f}% {100*ws:5.1f}%")

json.dump({
    "totals": {"events": len(events), "attributable": len(with_ch),
               "subscribedEvents": len(sub_events),
               "distinctChannels": len(set(w["channelId"] for w in with_ch)),
               "dormantSubs": len(dormant)},
    "topSubscribed": [{"title": by_id[c]["title"], "watches": n,
                       "domain": by_id[c]["domain"]} for c, n in top[:50]],
    "topNonSubscribed": [{"name": name, "watches": n}
                         for (cid, name), n in nonsub.most_common(50)],
    "domainIndex": [{"domain": d, "subs": s, "watches": w,
                     "subsShare": round(ss, 4), "watchShare": round(ws, 4),
                     "index": round(idx, 3)}
                    for d, s, w, ss, ws, idx in rows_out],
    "dormant": [{"title": r["title"], "subscribers": r["subscribers"],
                 "domain": r["domain"]} for r in dormant],
}, open("watch_analysis.json", "w"), indent=2, ensure_ascii=False)
print("\nwrote watch_analysis.json")
