---
name: insider-radar
description: "Frodes innsidehandel-radar for Oslo Børs (meldepliktig handel primærinnsidere), daglig brief, læringsfokus"
metadata: 
  node_type: memory
  type: project
  originSessionId: 96ba557a-abbb-400d-8f36-e8ba50c62760
---

Bygget 2026-07-03. Signal-/varslingsagent (INGEN megler-integrasjon, ingen auto-trading) som overvåker meldepliktig handel fra primærinnsidere på Oslo Børs. Mål: lære mest mulig om «smart money»-signaler.

**Datakilde:** Newsweb JSON-endepunkt `https://api3.oslo.oslobors.no/v1/newsreader/list?category=1102&fromDate=YYYY-MM-DD&toDate=YYYY-MM-DD` (kategori 1102 = MELDEPLIKTIG HANDEL FOR PRIMÆRINNSIDERE / MANAGERS' TRANSACTION). Full melding: `.../message?messageId=<id>`. VIKTIG: uten datovindu returnerer lista bare siste melding — datofilter er obligatorisk. Newsweb-data er opphavsrettsbeskyttet = kun privat bruk, ikke republiser/videreselg.

**Kode:** `workspace/insider-radar/fetch.py` — poller kategori 1102, dedup mot `seen.json`, skriver hver melding til `data/<id>.json`, printer JSON {count, items[]} til stdout. Ren henter, ingen LLM. Flagg: `--days N` (default 3), `--all` (ignorer dedup, for test).

**Brief-lag:** LLM parser fritekst-body → kjøp/salg, navn, rolle, antall, kurs, verdi. Terskel: fremhev KJØP > 500 000 kr (justerbar). Filtrer bort opsjons-/RSU-tildelinger, gaver, emisjoner/tegningsretter, mandatory-offer-aksepter.

**Watchlist:** `watchlist.json` (tickers + names) → treff varsler ALLTID uansett beløp, vist øverst i briefen. Match: ticker mot issuerSign, navn som delstreng i tekst. Seed 2026-07-03: ticker DNB; navn Gro Bakstad, Lars Røsæg, Jøtul Invest (DNB-styremedlemmer som kjøpte mai/juni 2026), Tore Tønseth, Ronja Capital (SALME styreleder). NB: DNB-ticker fanger også ansatte-aksjeprogram (støy) — briefen skiller konviksjonskjøp fra program/opsjon.

**Cron:** jobId `47b0755d-5237-453c-8873-250fce4aae62`, «Insider-radar Oslo Børs», hverdager 07:10 Europe/Oslo, sessionTarget main, Telegram-tråd til Frode. Egen jobb, atskilt fra [[daglig-morgen-brief]].

**Mulige neste steg:** watchlist på spesifikke bjellesau-navn (Spetalen/Fredly/Tveitereid), justere terskel etter volum, evt. sanntidsvarsel for store kjøp, senere US-marked (SEC Form 4) + Dataroma-superinvestorer. Se [[bre-digital-profile]] for eier-kontekst.
