#!/usr/bin/env python3
"""Complete duration coverage: deep-page Videos, then Live, then Shorts tabs
for every channel that still has watched videos without a known duration."""
import json, threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from browse_lib import channel_videos, TAB_VIDEOS, TAB_LIVE, TAB_SHORTS

watch = [json.loads(l) for l in open("watch_filtered.jsonl")]
have = set()
for l in open("durations.jsonl"):
    d = json.loads(l)
    if d["seconds"]:
        have.add(d["videoId"])
for l in open("channel_durations.jsonl"):
    d = json.loads(l)
    have.update(d["videos"])
try:
    for l in open("missing_durations.jsonl"):
        d = json.loads(l)
        have.update(d["videos"])
        have.update(d["shorts"])
except FileNotFoundError:
    pass

need = defaultdict(set)
evc = Counter()
for w in watch:
    if w["channelId"] and w["videoId"] not in have:
        need[w["channelId"]].add(w["videoId"])
        evc[w["channelId"]] += 1

targets = list(evc)
targets.sort(key=lambda c: -evc[c])
print(f"{len(targets)} channels, {sum(len(v) for v in need.values())} videos, "
      f"{sum(evc.values())} events to resolve", flush=True)

def depth(n):
    if n >= 200: return 150
    if n >= 50: return 60
    if n >= 10: return 30
    if n >= 3: return 15
    return 6

lock = threading.Lock()
out = open("missing_durations.jsonl", "a")
count = [0]

def job(cid):
    want = set(need[cid])
    found, shorts = {}, set()
    try:
        for params in (TAB_VIDEOS, TAB_LIVE, TAB_SHORTS):
            if not (want - set(found) - shorts):
                break
            v, unb = channel_videos(cid, max_pages=depth(evc[cid]),
                                    stop_ids=want, params=params)
            found.update(v)
            if params == TAB_SHORTS:
                shorts |= (unb & want)
        rec = {"channelId": cid,
               "videos": {k: v for k, v in found.items() if k in want or True},
               "shorts": sorted(shorts),
               "matched": len(want & (set(found) | shorts)),
               "wanted": len(want)}
    except Exception as e:
        rec = {"channelId": cid, "videos": found, "shorts": sorted(shorts),
               "matched": len(want & set(found)), "wanted": len(want),
               "error": str(e)[:120]}
    with lock:
        out.write(json.dumps(rec) + "\n")
        count[0] += 1
        if count[0] % 100 == 0:
            out.flush()
            print(f"{count[0]}/{len(targets)} channels", flush=True)

with ThreadPoolExecutor(max_workers=8) as ex:
    list(ex.map(job, targets))
out.close()
print("done", flush=True)
