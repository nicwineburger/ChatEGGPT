#!/usr/bin/env python3
"""Fetch video durations via InnerTube MWEB player endpoint (metadata only)."""
import json, sys, time, threading, urllib.request
from concurrent.futures import ThreadPoolExecutor

WATCH, OUT = sys.argv[1], sys.argv[2]
API = "https://youtubei.googleapis.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"

ids = []
seen = set()
for l in open(WATCH):
    v = json.loads(l)["videoId"]
    if v not in seen:
        seen.add(v)
        ids.append(v)

done = set()
try:
    for l in open(OUT):
        done.add(json.loads(l)["videoId"])
except FileNotFoundError:
    pass
todo = [v for v in ids if v not in done]
print(f"{len(ids)} distinct, {len(done)} cached, {len(todo)} to fetch", flush=True)

lock = threading.Lock()
out = open(OUT, "a")
counter = [0]

def fetch(vid):
    body = json.dumps({"context": {"client": {
        "clientName": "MWEB", "clientVersion": "2.20250311.03.00", "hl": "en"}},
        "videoId": vid}).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request(API, data=body,
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                d = json.load(r)
            vd = d.get("videoDetails", {})
            secs = vd.get("lengthSeconds")
            rec = {"videoId": vid,
                   "seconds": int(secs) if secs else None,
                   "status": d.get("playabilityStatus", {}).get("status")}
            with lock:
                out.write(json.dumps(rec) + "\n")
                counter[0] += 1
                if counter[0] % 500 == 0:
                    out.flush()
                    print(f"fetched {counter[0]}/{len(todo)}", flush=True)
            return
        except Exception as e:
            time.sleep(2 ** attempt)
    with lock:
        out.write(json.dumps({"videoId": vid, "seconds": None,
                              "status": "FETCH_FAILED"}) + "\n")
        counter[0] += 1

with ThreadPoolExecutor(max_workers=16) as ex:
    list(ex.map(fetch, todo))
out.close()
print("done", flush=True)
