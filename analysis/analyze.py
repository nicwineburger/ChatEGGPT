#!/usr/bin/env python3
"""Categorize subscribed channels on several axes, cluster them on text
similarity, and dump enriched CSV + cluster summaries."""
import json, re, sys, csv, math
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from overrides import OVERRIDES

JSONL = sys.argv[1]
OUT_CSV = sys.argv[2]
OUT_CLUSTERS = sys.argv[3]

rows = [json.loads(l) for l in open(JSONL)]

# ---------------------------------------------------------------- axes ----
DOMAINS = {
    "science": ["science", "physics", "chemistry", "biology", "astronomy", "space",
                "experiment", "scientist", "quantum", "laser", "microscope", "veritasium",
                "chemist", "nasa", "geology", "medicine", "medical", "brain", "neuro"],
    "math": ["math", "mathematics", "mathematical", "geometry", "number theory",
             "calculus", "puzzle", "mathematician", "topology"],
    "engineering_making": ["engineering", "engineer", "build", "maker", "diy", "3d print",
                           "robot", "invention", "workshop", "machining", "welding",
                           "electronics", "circuit", "arduino", "solder"],
    "programming_tech": ["programming", "software", "developer", "code", "coding", "linux",
                         "computer science", "hacking", "hacker", "security", "reverse engineer",
                         "tech", "technology", "gadget", "smartphone", "pc ", "gpu", "cpu",
                         "server", "raspberry pi", "web dev", "javascript", "ai ", "machine learning"],
    "retro_tech": ["retro", "vintage", "vhs", "cassette", "crt", "console mod", "gameboy",
                   "game boy", "restoration", "old computer", "obsolete", "walkman", "ipod",
                   "nostalgia tech", "dos ", "amiga", "commodore"],
    "gaming": ["gaming", "gameplay", "playthrough", "let's play", "lets play", "video game",
               "videogame", "games", "gamer", "nintendo", "playstation", "xbox", "steam",
               "minecraft", "mario", "zelda", "dark souls", "elden ring", "pokemon", "rpg",
               "fps", "esports", "twitch"],
    "speedrun_glitch": ["speedrun", "speedrunning", "glitch", "tas ", "world record",
                        "any%", "out of bounds", "boundary break", "a press", "randomizer"],
    "game_design_analysis": ["game design", "game dev", "gamedev", "game development",
                             "game analysis", "game criticism", "level design", "game music",
                             "game audio", "game soundtrack", "ludo"],
    "video_essay_media": ["video essay", "essay", "analysis", "criticism", "critique", "media",
                          "film analysis", "cinema", "movie", "film", "review", "trope",
                          "storytelling", "screenplay", "documentary", "deep dive"],
    "politics_society": ["politics", "political", "leftist", "socialism", "capitalism",
                         "philosophy", "gender", "race", "class", "fascism", "anarchism",
                         "feminist", "feminism", "queer", "trans", "lgbt", "breadtube",
                         "social justice", "labor", "marxis"],
    "urbanism_transit": ["urban", "urbanism", "city", "cities", "transit", "train", "bike",
                         "bicycle", "cars", "traffic", "zoning", "housing", "infrastructure",
                         "walkable", "public transport"],
    "comedy_sketch": ["comedy", "sketch", "funny", "humor", "parody", "satire", "improv",
                      "stand up", "standup", "comedian", "sitcom", "prank", "meme", "shitpost",
                      "abridged", "dub"],
    "music": ["music", "musician", "song", "songs", "album", "band", "guitar", "piano",
              "cover", "acapella", "a cappella", "remix", "producer", "composer", "soundtrack",
              "hip hop", "rap", "synth", "vocal"],
    "animation": ["animation", "animated", "animator", "cartoon", "anime", "manga",
                  "stop motion", "flash animation"],
    "food": ["cooking", "food", "recipe", "baking", "chef", "cuisine", "kitchen", "eating"],
    "nature_bio": ["animals", "wildlife", "nature", "plants", "botany", "birds", "insects",
                   "creatures", "beasts", "survival", "outdoors", "ecology"],
    "wrestling_sports": ["wrestling", "wrestler", "wwe", "sports", "football", "basketball",
                         "baseball", "olympics"],
    "podcast_actualplay": ["podcast", "actual play", "dungeons and dragons", "d&d", "ttrpg",
                           "tabletop", "campaign", "dice"],
}

# Priority when scores tie / overlap: more specific domains first.
DOMAIN_PRIORITY = ["speedrun_glitch", "retro_tech", "urbanism_transit", "math",
                   "game_design_analysis", "wrestling_sports", "podcast_actualplay",
                   "animation", "food", "nature_bio", "politics_society", "music",
                   "engineering_making", "science", "programming_tech", "comedy_sketch",
                   "video_essay_media", "gaming"]

ORG_HINTS = ["official", "productions", "studios", "team", "network", "channel of",
             "we are", "we make", "our ", "pbs", "university", "corporation", "company",
             "inc.", "llc", "games", "software", "records"]


BOILERPLATE = re.compile(
    r"https?://\S+|www\.\S+|\S+@\S+|\b(patreon|twitter|instagram|facebook|tiktok|"
    r"discord|twitch|reddit|merch|store|shop|business|inquiries|inquires|email|"
    r"subscribe|channel|youtube|official|videos?|content|new|check|follow|link|"
    r"links|bio|contact|welcome|hi|hello|thanks|watch)\b",
    re.IGNORECASE)


def text_of(r):
    return " ".join([r.get("title") or "", r.get("keywords") or "",
                     r.get("description") or ""]).lower()


def clean_text(r):
    # domain label is appended as a token so curated knowledge guides clustering
    t = BOILERPLATE.sub(" ", text_of(r))
    return t + (" " + r["domain"]) * 3


def classify_domain(r):
    t = " " + text_of(r) + " "
    scores = {}
    for dom, kws in DOMAINS.items():
        s = sum(t.count(" " + kw) + t.count(kw + " ") for kw in kws)
        if s:
            scores[dom] = s
    if not scores:
        return "unknown"
    best = max(scores.values())
    top = [d for d, s in scores.items() if s >= best * 0.75]
    for d in DOMAIN_PRIORITY:
        if d in top:
            return d
    return max(scores, key=scores.get)


def scale_tier(subs):
    if subs is None:
        return "unknown"
    if subs < 10_000:
        return "1_micro(<10K)"
    if subs < 100_000:
        return "2_small(10K-100K)"
    if subs < 1_000_000:
        return "3_mid(100K-1M)"
    if subs < 10_000_000:
        return "4_large(1M-10M)"
    return "5_mega(>10M)"


def volume_tier(v):
    if v is None:
        return "unknown"
    if v < 50:
        return "1_sparse(<50)"
    if v < 200:
        return "2_moderate(50-200)"
    if v < 1000:
        return "3_prolific(200-1K)"
    return "4_firehose(>1K)"


def creator_type(r):
    t = (r.get("title") or "").lower() + " " + (r.get("description") or "").lower()[:400]
    if any(h in t for h in ORG_HINTS):
        return "org/brand"
    if re.search(r"\b(i|my|me)\b", (r.get("description") or "").lower()):
        return "individual"
    return "individual?"


for r in rows:
    title = (r.get("title") or r.get("csvTitle") or "").strip()
    ov = OVERRIDES.get(r.get("title") or "") or OVERRIDES.get(title)
    r["domain"] = ov if ov else classify_domain(r)
    r["domainSource"] = "curated" if ov else "lexicon"
    r["scaleTier"] = scale_tier(r.get("subscribers"))
    r["volumeTier"] = volume_tier(r.get("videoCount"))
    r["creatorType"] = creator_type(r)
    s, v = r.get("subscribers"), r.get("videoCount")
    r["subsPerVideo"] = round(s / v, 1) if (s and v) else None

# ---------------------------------------------------------- clustering ----
docs = [clean_text(r) for r in rows]
vec = TfidfVectorizer(stop_words="english", max_features=6000, min_df=2,
                      ngram_range=(1, 2), sublinear_tf=True)
X = vec.fit_transform(docs)

best_k, best_score, best_labels = None, -1, None
for k in range(8, 21):
    km = KMeans(n_clusters=k, n_init=10, random_state=42)
    labels = km.fit_predict(X)
    sc = silhouette_score(X, labels, sample_size=min(600, X.shape[0]), random_state=42)
    if sc > best_score:
        best_k, best_score, best_labels, best_km = k, sc, labels, km
print(f"chose k={best_k} (silhouette={best_score:.3f})")

terms = np.array(vec.get_feature_names_out())
order = best_km.cluster_centers_.argsort(axis=1)[:, ::-1]
clusters = []
for c in range(best_k):
    members = [rows[i] for i in range(len(rows)) if best_labels[i] == c]
    for m in members:
        m["cluster"] = c
    top_terms = [t for t in terms[order[c][:15]]]
    subs = [m["subscribers"] for m in members if m.get("subscribers")]
    clusters.append({
        "cluster": c,
        "size": len(members),
        "topTerms": top_terms,
        "medianSubs": int(np.median(subs)) if subs else None,
        "domains": Counter(m["domain"] for m in members).most_common(5),
        "examples": [m["title"] for m in sorted(members, key=lambda m: -(m.get("subscribers") or 0))[:8]],
    })

with open(OUT_CLUSTERS, "w") as f:
    json.dump({"k": best_k, "silhouette": best_score, "clusters": clusters}, f,
              indent=2, ensure_ascii=False)

fields = ["channelId", "title", "handle", "subscribers", "videoCount", "domain",
          "domainSource", "scaleTier", "volumeTier", "creatorType", "subsPerVideo",
          "isFamilySafe", "cluster", "keywords", "description"]
with open(OUT_CSV, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    for r in sorted(rows, key=lambda r: (r.get("cluster", -1), -(r.get("subscribers") or 0))):
        rr = dict(r)
        rr["description"] = (rr.get("description") or "").replace("\n", " ")[:300]
        w.writerow(rr)

# ------------------------------------------------------------- summary ----
print("\n=== domain distribution ===")
for d, n in Counter(r["domain"] for r in rows).most_common():
    print(f"  {d:24s} {n}")
print("\n=== scale tiers ===")
for t, n in sorted(Counter(r["scaleTier"] for r in rows).items()):
    print(f"  {t:24s} {n}")
print("\n=== volume tiers ===")
for t, n in sorted(Counter(r["volumeTier"] for r in rows).items()):
    print(f"  {t:24s} {n}")
subs = [r["subscribers"] for r in rows if r.get("subscribers")]
print(f"\nsubs: median={int(np.median(subs)):,} mean={int(np.mean(subs)):,} "
      f"min={min(subs)} max={max(subs):,}")
print("\n=== clusters ===")
for c in clusters:
    print(f"[{c['cluster']:2d}] n={c['size']:3d} med_subs={c['medianSubs'] or 0:>10,} "
          f"terms={', '.join(c['topTerms'][:6])}")
    print(f"     e.g. {', '.join(c['examples'][:5])}")
