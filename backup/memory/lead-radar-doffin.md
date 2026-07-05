---
name: lead-radar-doffin
description: Doffin IoT-lead-søk bygget inn i morgenbriefen — eget skript mot Doffins ekte søke-API
metadata: 
  node_type: memory
  type: project
  originSessionId: 96ba557a-abbb-400d-8f36-e8ba50c62760
---

Bygget 2026-07-04. Erstatter upålitelig web_search for Doffin i morgenbriefens LEAD-RADAR.

**Datakilde:** Doffins ekte søke-API: `POST https://api.doffin.no/webclient/api/v2/search-api/search` med body `{"searchString": <term>, "numHitsPerPage": N, "page": 1}` (page må være ≥ 1). Fant basen i frontend-bundle (variabel zs). Hit-felt: id, buyer[], heading, description, status (ACTIVE m.fl.), estimatedValue, deadline, publicationDate, type. Notice-URL: `https://doffin.no/nb/notices/{id}`.

**Kode:** `workspace/lead-radar/doffin.py` — søker ~17 BRE-relevante termer (IoT, sensor, sensorikk, tilstandsovervåking, fjernovervåking, energiovervåking, byggautomasjon, SD-anlegg, VA telemetri, SCADA, automasjon, digital tvilling m.fl.), dedup på id, klassifiserer i `new` (publisert siste N dager, dedup mot `seen_doffin.json`, default 4d) og `active` (status ACTIVE eller frist frem i tid). Printer JSON {totalScanned, newCount, new[], activeCount, active[]}. Flagg `--newdays N`. Ingen LLM.

**Integrasjon:** Morgenbrief-cron (jobId 93c12194-521e-45a4-a8a5-0955519c4348) seksjon 1 kjører nå skriptet som autoritativ Doffin-kilde; web_search brukes kun for Mercell/LinkedIn. Se [[daglig-morgen-brief]].

**Status ved bygging:** 318 unike treff skannet, 9 aktive muligheter (bl.a. Asker NB-IoT vannmålere 40M, Lillestrøm byggautomasjon-rammeavtale, Fredrikstad + Digi Rogaland DPS-er, Nissedal SD-anlegg). seen_doffin.json primet, så kun ekte nye flagges heretter. Samme mønster som [[insider-radar]].
