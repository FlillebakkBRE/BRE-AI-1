#!/usr/bin/env python3
"""
lead-radar / doffin.py
Søker Doffin (offisielle søke-API) etter IoT/digitaliserings-relevante utlysninger for BRE Digital.
Dumt og robust: POST mot search-api, dedup på tvers av søkeord, klassifiserer i NYE (nylig
publisert, dedup mot seen.json) og AKTIVE muligheter (status ACTIVE / frist frem i tid).
Printer JSON til stdout for brief-laget. Ingen LLM her.

Bruk: python3 doffin.py [--newdays N]   (default 4 dager for "nye")
"""
import json, sys, os, datetime, urllib.request

API = "https://api.doffin.no/webclient/api/v2/search-api/search"
HERE = os.path.dirname(os.path.abspath(__file__))
SEEN_FILE = os.path.join(HERE, "seen_doffin.json")
UA = "Mozilla/5.0 (lead-radar; privat/bedrift BRE Digital)"

# BRE Digitals fokusområder — landbasert industri + offentlig sektor, IoT/digitalisering
TERMS = [
    "IoT", "sensor", "sensorikk", "tilstandsovervåking", "fjernovervåking",
    "sensorovervåking", "energiovervåking", "energiledelse", "energioppfølging",
    "trådløse sensorer", "SD-anlegg", "byggautomasjon", "prediktivt vedlikehold",
    "SCADA", "automasjon", "fjernavlesning", "smart bygg",
    # VA/automasjon-vokabular (norske kommuner) — lagt til 2026-07-08
    "driftskontroll", "toppsystem", "PLS", "NB-IoT", "vannmåler", "digitalisering bygg",
    "temperaturovervåking",
    # Lysstyring/DALI — BRE produktlinje (lagt til 2026-07-08)
    "lysstyring", "belysningsanlegg", "veibelysning", "lysanlegg", "smart belysning", "KNX",
]

def _search(term):
    req = urllib.request.Request(API,
        data=json.dumps({"searchString": term, "numHitsPerPage": 30, "page": 1}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r).get("hits", [])
        except Exception:
            if attempt == 2:
                return []

def load_seen():
    try:
        return set(json.load(open(SEEN_FILE)))
    except Exception:
        return set()

def save_seen(seen):
    json.dump(sorted(seen), open(SEEN_FILE, "w"))

ICP_THRESHOLD = 70  # score >= dette => foreslå auto-fangst som deal

# BRE Digital ICP: landbasert industri + offentlig sektor, IoT/sensor/automasjon/energi/VA
ICP_KEYWORDS = ["iot", "sensor", "sensorikk", "tilstandsovervåking", "fjernovervåking",
    "sensorovervåking", "energiovervåking", "energiledelse", "energioppfølging", "eos",
    "trådløse sensorer", "sd-anlegg", "byggautomasjon", "va-telemetri", "vannmåler",
    "telemetri", "scada", "automasjon", "prediktivt vedlikehold",
    "overvåking", "fjernavlesning", "smart bygg",
    # VA/automasjon (norske kommuner) — 2026-07-08
    "driftskontroll", "toppsystem", "pls", "nb-iot", "digitalisering",
    # Lysstyring/DALI-produktlinje — 2026-07-08 (dali/knx booster scoring, ikke retrieval)
    "lysstyring", "belysning", "belysningsanlegg", "veibelysning", "lysanlegg",
    "dali", "knx"]
PUBLIC_HINTS = ["kommune", "fylkeskommune", "sykehus", "helse", "interkommunal",
    "innkjøpssamarbeid", "statsbygg", "etat", "direktorat", "universitet", "høgskole"]
NEGATIVE = ["fluorometer", "forskningsinstrument", "instrument til forskning",
    "matvarer", "renhold", "kantine", "møbler", "transporttjenester", "vikartjenester"]

def score_icp(h):
    hay = ((h.get("heading") or "") + " " + (h.get("description") or "")).lower()
    buyer = ((h.get("buyer") or [{}])[0].get("name") or "").lower()
    score, reasons = 0, []
    kw = [k for k in ICP_KEYWORDS if k in hay]
    if kw:
        pts = min(45, 15 * len(kw)); score += pts
        reasons.append(f"nøkkelord: {', '.join(kw[:4])} (+{pts})")
    if any(p in buyer for p in PUBLIC_HINTS):
        score += 25; reasons.append("offentlig oppdragsgiver (+25)")
    else:
        score += 10; reasons.append("privat/industri (+10)")
    val = (h.get("estimatedValue") or {}).get("amount")
    if isinstance(val, (int, float)):
        if val >= 5_000_000: score += 15; reasons.append("verdi ≥5M (+15)")
        elif val >= 1_000_000: score += 10; reasons.append("verdi 1–5M (+10)")
        else: score += 5; reasons.append("verdi <1M (+5)")
    t = (h.get("type") or "").lower()
    if any(w in (t + " " + hay) for w in ["rammeavtale", "dynamisk", "dps"]):
        score += 15; reasons.append("rammeavtale/DPS (+15)")
    if any(n in hay for n in NEGATIVE):
        score -= 30; reasons.append("mulig irrelevant (−30)")
    score = max(0, min(100, score))
    return score, reasons

def slim(h):
    val = h.get("estimatedValue") or {}
    icp, reasons = score_icp(h)
    return {
        "id": h.get("id"),
        "heading": h.get("heading"),
        "buyer": (h.get("buyer") or [{}])[0].get("name"),
        "status": h.get("status"),
        "publicationDate": (h.get("publicationDate") or "")[:10],
        "deadline": (h.get("deadline") or "")[:10],
        "value": val.get("amount"),
        "currency": val.get("currencyCode"),
        "type": h.get("type"),
        "url": f"https://doffin.no/nb/notices/{h.get('id')}",
        "icpScore": icp,
        "icpReasons": reasons,
        "capture": icp >= ICP_THRESHOLD,
    }

def main():
    newdays = 4
    if "--newdays" in sys.argv:
        try: newdays = int(sys.argv[sys.argv.index("--newdays")+1])
        except Exception: pass

    seen = load_seen()
    hits = {}
    for t in TERMS:
        for h in _search(t):
            if h.get("id"):
                hits[h["id"]] = h

    today = datetime.date.today()
    cutoff = (today - datetime.timedelta(days=newdays)).isoformat()
    today_s = today.isoformat()

    new_items, active = [], []
    for h in hits.values():
        s = slim(h)
        pub = s["publicationDate"]
        dl = s["deadline"]
        # NYE: publisert i vinduet OG ikke sett før
        if pub and pub >= cutoff and s["id"] not in seen:
            new_items.append(s)
        # AKTIVE muligheter: status ACTIVE eller frist frem i tid
        if (h.get("status") == "ACTIVE") or (dl and dl >= today_s):
            active.append(s)

    # oppdater seen med ALT vi har sett nå (så "nye" kun trigger én gang)
    seen |= set(hits.keys())
    save_seen(seen)

    new_items.sort(key=lambda x: x["publicationDate"], reverse=True)
    active.sort(key=lambda x: x["deadline"] or "9999")

    out = {
        "totalScanned": len(hits),
        "newCount": len(new_items),
        "captureCount": sum(1 for x in new_items if x["capture"]),
        "new": new_items,
        "activeCount": len(active),
        "active": active[:15],
    }
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
