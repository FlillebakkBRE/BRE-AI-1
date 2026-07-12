# MEMORY

- [BRE Digital profile](bre-digital-profile.md) — Frode's company: IoT/digitalisering, stack (IXON/Efento/Zegeba), fokus landbasert industri + offentlig sektor (ikke havbruk), 2× DGX Spark privat AI
- [Daglig morgen-brief](daglig-morgen-brief.md) — cron: hverdager 07:00 Telegram, industri/offentlig + IoT + NIS2 + nøkkelord
- [Insider-radar](insider-radar.md) — Oslo Børs meldepliktig handel, daglig brief 07:10 hverdager, Newsweb kat.1102, terskel 500k kjøp, læringsfokus
- [Lead-radar Doffin](lead-radar-doffin.md) — Doffin IoT-søk (ekte API) bygget inn i morgenbriefen, script i workspace/lead-radar/doffin.py
- [O365-integrasjon](o365-integrasjon.md) — LIVE 2026-07-05: Graph MCP kalender (les) + e-post (les/kladd), aldri auto-send; kalender i morgenbrief
- [Git-backup](git-backup.md) — workspace-skript pushes til privat GitHub FlillebakkBRE/BRE-AI-1 via SSH deploy key
- [Salg-pipeline](salg-pipeline.md) — salgsdiagnose + roadmap; pipeline-helse + oppfølgings-radar (mandag 07:30, kladd) gjort, neste: e-sign, tilbud-gen
- [BRE-brand](bre-brand.md) — visuell profil: farger (#005689/#0092D2/#59C2EA/#FAE100), Proxima Nova-font, logo/brevmal-filer i workspace/brand/
- [Tilbud-maler](tilbud-maler.md) — 3 BRE-tilbudsmodeller (dagrate/BOM/enhetspris+abo) fra Foodman, underlag for tilbuds-generator, filer i workspace/tilbud-maler/
- [Homey](bre-homey.md) — LIVE 2026-07-06: Homey Pro-integrasjon via sky-proxy, script homey/homey.py, 56 enheter, nøkkel gitignorert
- [Diakonhjemmet MCP](diakonhjemmet-mcp.md) — BRE Cloud InfluxDB tidsserie (kunde-IoT), OAuth; fikset med `openclaw mcp reload` 2026-07-06
- [PowerOffice Go](poweroffice-go.md) — BRE forretningssystem, API v2 LIVE (Demo) 2026-07-06, klient workspace/poweroffice/poweroffice.py, nøkler gitignorert
- [E-post-triage](epost-triage-preferanser.md) — hopp over driftsalarmer (IXON/BRE Cloud/RMM device-offline) i innboks-oppfølging + morgenbrief
- [E-post-formatering](epost-formatering.md) — alle kladder skal ha struktur (HTML avsnitt/punkt), sett body via update-mail-message (ikke flat Comment)
- [Kundeportal DGX](kundeportal-dgx.md) — privat kunde-AI på DGX (kunde spør på egne IoT-data); Fase 1 query-lag bygget i workspace/kundeportal/
- [HubSpot pipeline-steg](hubspot-pipeline-steg.md) — deal-steg mapping: presentationscheduled=«Tilbud sendt», contractsent=⚠️Won-felle (ikke bruk for tilbud sendt)
- [BRE Lysstyring/DALI](bre-lysstyring-dali.md) — produktlinje tunnel-lysstyring (Phoenix Contact PLCnext/DALI/Lumgate); produktark-generator i workspace/bre-lysstyring/
- [Data-håndteringsprinsipp](data-handling-prinsipp.md) — M365=fasit, samle i workspace mot DGX-migrering, ikke dupliser forretningsdata i Claude-prosjekt, sensitivt→DGX
