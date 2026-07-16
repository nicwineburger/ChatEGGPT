#!/usr/bin/env python3
"""Remove sleep-autoplay tails from watch history.

Rule: sessionize with a 45-minute gap threshold. Once a session enters the
sleep window (23:30-07:00), keep the next 2 events (the videos deliberately
put on to fall asleep to) and drop the remainder of that session entirely —
including any autoplay that runs past 07:00 because the TV sleep timer was
forgotten.
"""
import json, sys
from datetime import datetime, time as dtime

rows = [json.loads(l) for l in open(sys.argv[1])]
for r in rows:
    r["dt"] = datetime.strptime(r["date"] + " " + r["time"], "%Y-%m-%d %H:%M:%S")
rows.sort(key=lambda r: r["dt"])

GAP_MIN = 45
SLEEP_START = dtime(23, 30)
SLEEP_END = dtime(7, 0)

def in_sleep_window(dt):
    t = dt.time()
    return t >= SLEEP_START or t < SLEEP_END

# sessionize
sessions, cur = [], []
for r in rows:
    if cur and (r["dt"] - cur[-1]["dt"]).total_seconds() > GAP_MIN * 60:
        sessions.append(cur)
        cur = []
    cur.append(r)
if cur:
    sessions.append(cur)

kept, dropped = [], []
for s in sessions:
    allowance = None  # None until session enters sleep window
    session_dead = False
    for r in s:
        if session_dead:
            dropped.append(r)
            continue
        if in_sleep_window(r["dt"]):
            if allowance is None:
                allowance = 2
            if allowance > 0:
                allowance -= 1
                kept.append(r)
            else:
                session_dead = True
                dropped.append(r)
        else:
            kept.append(r)

for r in kept:
    del r["dt"]
with open(sys.argv[2], "w") as f:
    for r in kept:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

n = len(rows)
print(f"sessions: {len(sessions)}")
print(f"kept {len(kept)}/{n} ({100*len(kept)/n:.1f}%), dropped {len(dropped)} autoplay-tail events")
from collections import Counter
dd = Counter(r["channelName"] for r in dropped if r["channelName"])
print("most-dropped channels:", dd.most_common(12))
dy = Counter(r["date"][:4] for r in dropped)
print("dropped by year:", sorted(dy.items()))
