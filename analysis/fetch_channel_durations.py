#!/usr/bin/env python3
"""Fetch video durations by paging channels' videos tabs via InnerTube browse."""
import json, threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from browse_lib import channel_videos

watch = [json.loads(l) for l in open("watch_filtered.jsonl")]
have = set()
for l in open("durations.jsonl"):
    d = json.loads(l)
    if d["seconds"]:
        have.add(d["videoId"])

need = defaultdict(set)   # channelId -> videoIds still needing duration
evc = Counter()           # channelId -> unmatched event count
for w in watch:
    if w["channelId"] and w["videoId"] not in have:
        need[w["channelId"]].add(w["videoId"])
        evc[w["channelId"]] += 1

targets = [c for c, n in evc.most_common() if n >= 3]
print(f"{len(targets)} channels with >=3 unmatched events "
      f"({sum(evc[c] for c in targets)} of {sum(evc.values())} unmatched events)", flush=True)

done_ch = set()
try:
    for l in open("channel_durations.jsonl"):
        done_ch.add(json.loads(l)["channelId"])
except FileNotFoundError:
    pass
targets = [c for c in targets if c not in done_ch]
print(f"{len(done_ch)} cached, {len(targets)} to fetch", flush=True)

lock = threading.Lock()
out = open("channel_durations.jsonl", "a")
count = [0]

def pages_for(n):
    if n >= 100: return 20
    if n >= 30: return 12
    if n >= 10: return 7
    return 3

def job(cid):
    try:
        vids = channel_videos(cid, max_pages=pages_for(evc[cid]), stop_ids=need[cid])
        rec = {"channelId": cid, "videos": vids,
               "matched": len(need[cid] & set(vids))}
    except Exception as e:
        rec = {"channelId": cid, "videos": {}, "matched": 0, "error": str(e)[:120]}
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
