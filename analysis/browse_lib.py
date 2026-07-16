"""InnerTube browse helpers: channel videos tab -> {videoId: seconds}."""
import json, re, urllib.request

API = "https://youtubei.googleapis.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
CTX = {"client": {"clientName": "WEB", "clientVersion": "2.20250101.00.00", "hl": "en"}}
TIME_RE = re.compile(r'^(\d{1,2}:)?\d{1,2}:\d{2}$')

def _post(body):
    req = urllib.request.Request(API, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def _to_secs(t):
    p = [int(x) for x in t.split(":")]
    s = 0
    for x in p:
        s = s * 60 + x
    return s

def _walk(o, lockups, conts):
    if isinstance(o, dict):
        if "lockupViewModel" in o:
            lockups.append(o["lockupViewModel"])
        if "continuationCommand" in o and isinstance(o["continuationCommand"], dict):
            tok = o["continuationCommand"].get("token")
            if tok:
                conts.append(tok)
        for v in o.values():
            _walk(v, lockups, conts)
    elif isinstance(o, list):
        for v in o:
            _walk(v, lockups, conts)

def _badge_time(lockup):
    found = []
    def w(o):
        if isinstance(o, dict):
            t = o.get("text")
            if isinstance(t, str) and TIME_RE.match(t):
                found.append(t)
            for v in o.values():
                w(v)
        elif isinstance(o, list):
            for v in o:
                w(v)
    w(lockup.get("contentImage", {}))
    return found[0] if found else None

def parse_page(resp):
    lockups, conts = [], []
    _walk(resp, lockups, conts)
    out = {}
    for l in lockups:
        vid = l.get("contentId")
        t = _badge_time(l)
        if vid and t:
            out[vid] = _to_secs(t)
    return out, (conts[0] if conts else None)

def channel_videos(channel_id, max_pages=5, stop_ids=None):
    """Return {videoId: seconds} from a channel's videos tab.
    Stops early once all stop_ids are found (if given)."""
    vids = {}
    resp = _post({"context": CTX, "browseId": channel_id,
                  "params": "EgZ2aWRlb3PyBgQKAjoA"})
    page, cont = parse_page(resp)
    vids.update(page)
    pages = 1
    while cont and pages < max_pages:
        if stop_ids and stop_ids <= set(vids):
            break
        if not page:  # empty page, don't loop
            break
        resp = _post({"context": CTX, "continuation": cont})
        page, cont = parse_page(resp)
        vids.update(page)
        pages += 1
    return vids
