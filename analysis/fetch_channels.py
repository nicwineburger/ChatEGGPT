#!/usr/bin/env python3
"""Fetch YouTube channel metadata via Google's InnerTube API (youtubei.googleapis.com)."""
import csv, json, sys, time, re
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request

API = "https://youtubei.googleapis.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
CTX = {"context": {"client": {"clientName": "WEB", "clientVersion": "2.20240101.00.00"}}}

CSV_IN = sys.argv[1]
JSONL_OUT = sys.argv[2]


def parse_count(text):
    """'7.03M subscribers' -> 7030000; '195 videos' -> 195."""
    if not text:
        return None
    m = re.search(r"([\d.,]+)\s*([KMB]?)", text.replace(",", ""))
    if not m:
        return None
    val = float(m.group(1))
    mult = {"K": 1e3, "M": 1e6, "B": 1e9}.get(m.group(2), 1)
    return int(val * mult)


def fetch(cid, title):
    body = dict(CTX, browseId=cid)
    req = urllib.request.Request(API, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                d = json.load(r)
            break
        except Exception as e:
            if attempt == 3:
                return {"channelId": cid, "csvTitle": title, "error": str(e)}
            time.sleep(2 * (attempt + 1))
    md = d.get("metadata", {}).get("channelMetadataRenderer", {})
    subs_text = videos_text = None
    try:
        rows = (d["header"]["pageHeaderRenderer"]["content"]["pageHeaderViewModel"]
                 ["metadata"]["contentMetadataViewModel"]["metadataRows"])
        parts = [p.get("text", {}).get("content", "") for row in rows
                 for p in row.get("metadataParts", [])]
        for p in parts:
            if "subscriber" in p:
                subs_text = p
            elif "video" in p:
                videos_text = p
    except (KeyError, IndexError, TypeError):
        pass
    return {
        "channelId": cid,
        "csvTitle": title,
        "title": md.get("title", title),
        "description": md.get("description", ""),
        "keywords": md.get("keywords", ""),
        "isFamilySafe": md.get("isFamilySafe"),
        "handle": (md.get("vanityChannelUrl") or "").split("/")[-1],
        "subscribers": parse_count(subs_text),
        "subscribersText": subs_text,
        "videoCount": parse_count(videos_text),
        "videoCountText": videos_text,
        "terminated": md == {},
    }


rows = list(csv.DictReader(open(CSV_IN)))
print(f"fetching {len(rows)} channels...")
results = []
with ThreadPoolExecutor(max_workers=10) as ex:
    futs = {ex.submit(fetch, r["Channel Id"], r["Channel Title"]): r for r in rows}
    for i, f in enumerate(as_completed(futs)):
        results.append(f.result())
        if (i + 1) % 50 == 0:
            print(f"  {i+1}/{len(rows)}")

with open(JSONL_OUT, "w") as f:
    for r in results:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

errs = [r for r in results if r.get("error")]
dead = [r for r in results if r.get("terminated")]
print(f"done: {len(results)} fetched, {len(errs)} errors, {len(dead)} terminated/empty")
for r in errs[:10]:
    print("  ERR", r["csvTitle"], r["error"])
