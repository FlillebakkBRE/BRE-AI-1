---
name: bre-digital-profile
description: "Frode Lillebakk's company BRE Digital — profile, tech stack, and strategic focus"
metadata: 
  node_type: memory
  type: project
  originSessionId: cab12b21-5815-463f-83a6-c50ac6daf2cd
---

Frode Lillebakk is daglig leder (CEO) of **BRE Digital AS** (org.nr 921 244 541, Eidetorget 1, 6490 Eide; morselskap Lillebakk Holding AS). ~8 ansatte, IoT/digitaliseringskonsulent. Partner-/produktstack: **IXON** (sky/fjerntilgang), **Efento** (trådløse sensorer), **Zegeba** (digitale skjema/rapporter).

**Bransjefokus (bekreftet 2026-07-02):** landbasert industri (produksjon, prosess, energi, bygg/anlegg) og offentlig sektor. IKKE havbruk — jeg antok havbruk tidligere, men Frode korrigerte det.

Har allerede **SkatteFUNN + Innovasjon Norge** på plass. Interessert i EIC/Horizon/Eurostars som neste steg. Strategiske tema drøftet: vri fra timesalg til gjentakende inntekt (ARR/abonnement), productisere AI+IoT (agentbasert overvåking), NIS2/digitalsikkerhetsloven som salgsvinkel.

**AI-infra:** eier 2× NVIDIA DGX Spark (0005-000, 200GbE) — bygger privat lokal AI (Ollama/vLLM + Qwen3.6 + RAG/Qdrant + Open WebUI) så data ikke forlater selskapet. Vurderer interne agenter (tilbuds-/dokument-RAG først) og kundevendt IoT-overvåkingsagent.

**Beslutning 2026-07-02 (todelt strategi):** Mac mini brukes til PILOT/læring (kjører OpenClaw-gateway nå, agent «main» = Frode). DGX-løsningen settes opp SEPARAT som produksjons-/skaleringsmålbilde: dedikert Linux-host (DGX OS) med isolerte agenter per bruker/kunde + sandboxing (Docker) + lokal LLM-inferens. Vil ha flere isolerte agenter (egen Telegram-bot per agent) så andre ikke ser hans workspace. Pilot-agent-oppsett venter på at Frode gir agentnavn + ny BotFather-token.

**Leverandører:** Efento, IXON, Kunbus, Digital Matter, Phoenix Contact, Enless Wireless (+ Zegeba). **Konkurrenter (fra LinkedIn, 2026-07-03):** Etero AS, Piscada, Clarify, El-Watch AS, Axbit, Nivero AS, Gapit Nordics, Digel. Begge lister overvåkes i morgenbriefen.

Se [[daglig-morgen-brief]].
