#!/usr/bin/env python3
"""Player-endpoint pass for videos still lacking exact durations."""
import json, threading, time, urllib.request

API = "https://youtubei.googleapis.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"

have = set()
for l in open("durations.jsonl"):
    d = json.loads(l)
    if d["seconds"]:
        have.add(d["videoId"])
for f in ("channel_durations.jsonl", "missing_durations.jsonl"):
    for l in open(f):
        d = json.loads(l)
        have.update(d["videos"])
        have.update(d.get("shorts", []))

todo, seen = [], set()
for l in open("watch_filtered.jsonl"):
    v = json.loads(l)["videoId"]
    if v not in have and v not in seen:
        seen.add(v)
        todo.append(v)
print(f"{len(todo)} videos to try", flush=True)

lock = threading.Lock()
out = open("durations.jsonl", "a")
streak = [0]
count = [0]
stop = threading.Event()

def fetch(vid):
    if stop.is_set():
        return
    body = json.dumps({"context": {"client": {
        "clientName": "MWEB", "clientVersion": "2.20250311.03.00", "hl": "en"}},
        "videoId": vid}).encode()
    try:
        req = urllib.request.Request(API, data=body,
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
        vd = d.get("videoDetails", {})
        secs = vd.get("lengthSeconds")
        status = d.get("playabilityStatus", {}).get("status")
        with lock:
            if secs:
                out.write(json.dumps({"videoId": vid, "seconds": int(secs),
                                      "status": status, "pass": 2}) + "\n")
                streak[0] = 0
            elif status == "LOGIN_REQUIRED":
                streak[0] += 1
                if streak[0] >= 40:
                    stop.set()
                    print("bot-blocked again, stopping", flush=True)
            else:
                out.write(json.dumps({"videoId": vid, "seconds": None,
                                      "status": status, "pass": 2}) + "\n")
            count[0] += 1
            if count[0] % 400 == 0:
                out.flush()
                print(f"{count[0]}/{len(todo)}", flush=True)
    except Exception:
        pass
    time.sleep(0.15)

from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=4) as ex:
    list(ex.map(fetch, todo))
out.close()
print(f"done ({count[0]} attempted, stopped={stop.is_set()})", flush=True)
