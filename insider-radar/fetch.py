#!/usr/bin/env python3
"""
insider-radar / fetch.py
Poller Oslo Børs Newsweb for meldepliktig handel (primærinnsidere, kategori 1102).
Dumt og robust: henter ren JSON fra det offisielle Newsweb-endepunktet, dedup mot
seen.json, skriver hver nye melding som data/<messageId>.json, og printer et
maskinlesbart sammendrag av NYE meldinger til stdout (for LLM-brief-laget).

Ingen LLM her. Ingen beslutninger. Bare henting.
Bruk: python3 fetch.py [--days N] [--all]
  --days N : hvor mange dager bakover å hente liste for (default 3)
  --all    : ignorer seen.json, print alle (for test/backfill-visning)
"""
import json, sys, os, re, time, datetime, urllib.request, urllib.parse

BASE = "https://api3.oslo.oslobors.no/v1/newsreader"
CATEGORY = 1102  # MELDEPLIKTIG HANDEL FOR PRIMÆRINNSIDERE / MANAGERS' TRANSACTION
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
SEEN_FILE = os.path.join(HERE, "seen.json")
WATCHLIST_FILE = os.path.join(HERE, "watchlist.json")
UA = "Mozilla/5.0 (insider-radar; privat bruk)"

def _get(path, params):
    qs = urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    url = f"{BASE}/{path}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))

def load_seen():
    if os.path.exists(SEEN_FILE):
        try:
            return set(json.load(open(SEEN_FILE)))
        except Exception:
            return set()
    return set()

def save_seen(seen):
    json.dump(sorted(seen), open(SEEN_FILE, "w"))

def strip_html(html):
    return " ".join(re.sub(r"<[^>]+>", " ", html or "").split())

def load_watchlist():
    try:
        w = json.load(open(WATCHLIST_FILE))
        return [t.upper() for t in w.get("tickers", [])], [n.lower() for n in w.get("names", [])]
    except Exception:
        return [], []

def watchlist_hits(item, tickers, names):
    hits = []
    if (item.get("issuerSign") or "").upper() in tickers:
        hits.append(item.get("issuerSign"))
    hay = ((item.get("title") or "") + " " + (item.get("body") or "")).lower()
    hits += [n for n in names if n and n in hay]
    # bevar original-casing for navn ved å slå opp igjen er unødvendig; returner unike treff
    return sorted(set(h for h in hits if h))

def guess_lang(item):
    t = ((item.get("title") or "") + " " + (item.get("body") or "")).lower()
    no = sum(w in t for w in ("meldepliktig", "kjøpt", "solgt", "aksjer", "egenkapitalbevis", "primærinnsider", "nærstående"))
    en = sum(w in t for w in ("mandatory notification", "purchased", "bought", "shares", "primary insider", "equity certificates"))
    return "no" if no >= en else "en"

def collapse_translations(items):
    """Slå sammen NO/EN-dubletter: samme selskap + samme tidsstempel + ulikt språk.
    Konservativt: kun par (2 stk) med ulike språk kollapses; ellers beholdes alt."""
    groups, order = {}, []
    for it in items:
        # minutt-granularitet: NO/EN-par skiller ofte på sekund/ms
        key = (it.get("issuerSign"), (it.get("publishedTime") or "")[:16])
        if key not in groups:
            groups[key] = []; order.append(key)
        groups[key].append(it)
    out, removed = [], 0
    for key in order:
        grp = groups[key]
        if len(grp) == 2 and guess_lang(grp[0]) != guess_lang(grp[1]):
            rep = next((g for g in grp if guess_lang(g) == "no"), grp[0])
            rep = dict(rep); rep["duplicateOf"] = [g["messageId"] for g in grp if g["messageId"] != rep["messageId"]]
            out.append(rep); removed += 1
        else:
            out.extend(grp)
    return out, removed

def main():
    days = 3
    take_all = "--all" in sys.argv
    if "--days" in sys.argv:
        try:
            days = int(sys.argv[sys.argv.index("--days") + 1])
        except Exception:
            pass

    # VIKTIG: uten datovindu returnerer endepunktet bare siste melding.
    today = datetime.date.today()
    from_date = (today - datetime.timedelta(days=days)).isoformat()
    to_date = today.isoformat()
    lst = _get("list", {"category": CATEGORY, "fromDate": from_date, "toDate": to_date})
    msgs = lst.get("data", {}).get("messages", [])
    seen = set() if take_all else load_seen()

    new_items = []
    for m in msgs:
        mid = m.get("messageId")
        if mid is None:
            continue
        if not take_all and mid in seen:
            continue
        # hent full tekst
        try:
            detail = _get("message", {"messageId": mid})
            body = strip_html(detail.get("data", {}).get("message", {}).get("body", ""))
        except Exception:
            body = ""
        item = {
            "messageId": mid,
            "publishedTime": m.get("publishedTime"),
            "issuerSign": m.get("issuerSign"),
            "issuerName": m.get("issuerName"),
            "title": m.get("title"),
            "url": f"https://newsweb.oslobors.no/message/{mid}",
            "body": body[:4000],
        }
        # lagre rå melding til disk
        json.dump(item, open(os.path.join(DATA_DIR, f"{mid}.json"), "w"), ensure_ascii=False, indent=2)
        new_items.append(item)
        seen.add(mid)

    if not take_all:
        save_seen(seen)

    # slå sammen NO/EN-oversettelser av samme handel
    deduped, removed = collapse_translations(new_items)

    # flagg watchlist-treff (varsler uansett beløp)
    tickers, names = load_watchlist()
    for it in deduped:
        hits = watchlist_hits(it, tickers, names)
        if hits:
            it["watchlist"] = hits

    wl_count = sum(1 for it in deduped if it.get("watchlist"))

    # maskinlesbart sammendrag for brief-laget
    out = {"count": len(deduped), "rawCount": len(new_items), "duplicatesCollapsed": removed,
           "watchlistHits": wl_count, "items": deduped}
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
