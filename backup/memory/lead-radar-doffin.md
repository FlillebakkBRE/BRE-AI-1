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

**Kode:** `workspace/lead-radar/doffin.py` — søker ~28 BRE-relevante termer, dedup på id, klassifiserer i `new` (publisert siste N dager, dedup mot `seen_doffin.json`, default 4d) og `active` (status ACTIVE eller frist frem i tid). Printer JSON {totalScanned, newCount, new[], activeCount, active[]}. Flagg `--newdays N`. Ingen LLM.

**Søkeord utvidet 2026-07-08:** la til VA/automasjon-vokabular (driftskontroll, toppsystem, PLS, NB-IoT, vannmåler, digitalisering bygg, temperaturovervåking, energioppfølging) + **lysstyring/DALI-produktlinje** (lysstyring, belysningsanlegg, veibelysning, lysanlegg, smart belysning, KNX). Fjernet «VA telemetri» + «digital tvilling» (~0 norske treff). VIKTIG bug-fiks: samme ord lagt i BÅDE TERMS (retrieval) OG ICP_KEYWORDS (scoring) — før scoret nye retrieval-treff 0 og nådde aldri terskel. `dali`/`knx` ligger KUN i ICP_KEYWORDS (booster lys-treff) — ikke i TERMS, fordi bar «DALI» matcher «Daling»/kulvert i fulltekst (støy). Verifisert: fanget «Belysning Stordalstunnelen» (Møre og Romsdal, 20M, ICP 70) + Bærum lysanlegg (27M, ICP 85); Øvre Romerike PLS→ICP 85, Asker NB-IoT→ICP 100.

**ICP-scoring + auto-fangst (2026-07-05):** doffin.py scorer hver lead 0-100 (score_icp, ICP_THRESHOLD=70) → felt icpScore, icpReasons, capture. Output har også captureCount. Morgenbriefen (seksjon 1b) auto-oppretter HubSpot-deal for 'new'-leads med capture=true (dealname '[Doffin] <heading>', pipeline default, stage appointmentscheduled, owner 89064005, dedup via søk på Doffin-id). Se [[salg-pipeline]].

**Integrasjon:** Morgenbrief-cron (jobId 93c12194-521e-45a4-a8a5-0955519c4348) seksjon 1 kjører nå skriptet som autoritativ Doffin-kilde; web_search brukes kun for Mercell/LinkedIn. Mercell-søket i cron-prompten (seksjon 1c) fikk lys/DALI + VA-ord 2026-07-08. Se [[daglig-morgen-brief]].

**📋 BACKLOG — ekte Mercell-integrasjon (ønsket av Frode 2026-07-08):** I dag dekkes Mercell KUN via web_search i morgenbriefen (upålitelig, ingen ICP-scoring/auto-fangst). Frode vil ha en ordentlig Mercell-kobling på nivå med Doffin-scriptet — eget script mot Mercell/Visma/TendSign-API (mange norske DPS-er og konkurranser ligger der, bl.a. Digi Rogaland). Å utrede: har Mercell et åpent/gratis søke-API (à la Doffin webclient), eller krever det leverandør-innlogging/betalt tilgang? Bygg doffin.py-mønsteret på nytt for Mercell hvis API finnes.

**Status ved bygging:** 318 unike treff skannet, 9 aktive muligheter (bl.a. Asker NB-IoT vannmålere 40M, Lillestrøm byggautomasjon-rammeavtale, Fredrikstad + Digi Rogaland DPS-er, Nissedal SD-anlegg). seen_doffin.json primet, så kun ekte nye flagges heretter. Samme mønster som [[insider-radar]].
