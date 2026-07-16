#!/usr/bin/env python3
"""Parse Google Takeout watch-history.html into JSONL."""
import re, json, sys, html

src = open(sys.argv[1], encoding="utf-8").read()
out = open(sys.argv[2], "w")

# split into entry cells
cells = re.findall(
    r'<div class="content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1">(.*?)</div>',
    src, re.S)

entry_re = re.compile(
    r'Watched[\s\xa0]*(?:&nbsp;)?<a href="https://www\.youtube\.com/watch\?v=([^"&]+)[^"]*">(.*?)</a>'
    r'(?:<br\s*/?><a href="https://www\.youtube\.com/(?:channel/|user/|c/|@)?([^"]+)">(.*?)</a>)?'
    r'<br\s*/?>([A-Z][a-z]{2} \d{1,2}, \d{4}, [\d:]+[\s \xa0]*[AP]M [A-Z]+)', re.S)

months = {m: i+1 for i, m in enumerate(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}

n_parsed = n_skipped = 0
for c in cells:
    m = entry_re.search(c)
    if not m:
        n_skipped += 1
        continue
    vid, vtitle, churl, chname, ts = m.groups()
    dm = re.match(r'(\w{3}) (\d{1,2}), (\d{4}), (\d{1,2}):(\d{2}):(\d{2})[\s \xa0]*([AP])M', ts)
    mo, day, yr, hh, mm, ss, ap = dm.groups()
    hh = int(hh) % 12 + (12 if ap == "P" else 0)
    ad = "From Google Ads" in c
    cid = None
    if churl:
        churl = churl.split("/")[-1] if "/" in churl else churl
        if churl.startswith("UC"):
            cid = churl
    out.write(json.dumps({
        "videoId": vid,
        "videoTitle": html.unescape(vtitle),
        "channelId": cid,
        "channelUrlFrag": churl,
        "channelName": html.unescape(chname) if chname else None,
        "date": f"{yr}-{months[mo]:02d}-{int(day):02d}",
        "time": f"{hh:02d}:{mm}:{ss}",
        "ad": ad,
    }, ensure_ascii=False) + "\n")
    n_parsed += 1

print(f"cells={len(cells)} parsed={n_parsed} skipped={n_skipped}")
