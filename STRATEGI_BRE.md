# BRE Digital — Strategi

_Levende dokument. Sist oppdatert: 2026-08-03. Eier: Frode Lillebakk._

Dette er ett samlet, oppdaterbart strategibilde for BRE Digital. Detaljerte tall (lønn, kundeøkonomi) holdes **utenfor** dette dokumentet — de lever i PowerOffice/M365 (fasit). Her: retning, initiativer og status.

---

## 1. Overordnet retning (forretningsstrategi)

1. 🔄 **Fra timesalg → gjentakende inntekt (ARR/abonnement).** BRE Cloud (SaaS, 599/mnd) er kjernen. Mål: bygge forutsigbar, skalerbar tilbakevendende omsetning i stedet for å være avhengig av fakturerbare timer.
2. 📦 **Produktisere AI + IoT.** Gå fra skreddersøm til gjenbrukbare produkter: agentbasert overvåking, kundevendt IoT-overvåkingsagent, interne dokument-/tilbuds-RAG.
3. 🛡️ **NIS2 / digitalsikkerhetsloven som salgsvinkel.** BRE selger sikkerhet — og skal selv være et forbilde (leverandørkjede-sikkerhet, ryddig IT-drift).
4. 🖥️ **Privat lokal AI på DGX.** Todelt: Mac mini = pilot/læring nå → 2× NVIDIA DGX Spark = produksjon. Prinsipp: **data forlater ikke selskapet** (Ollama/vLLM + RAG lokalt).

**Markedsfokus:** landbasert industri + offentlig sektor (ikke havbruk). Stack: IXON / Efento / Zegeba + BRE Cloud.

**Finansiering:** SkatteFUNN + Innovasjon Norge på plass. Neste steg vurderes: EIC / Horizon / Eurostars.

---

## 2. Salgs-/pipelinestrategi (aktiv siden 2026-07-05)

**Diagnose:** Flaskehalsen er ikke leads — det er **oppfølging og lukking**. Se detaljert roadmap og status i minne-notatet `salg-pipeline`.

| # | Tiltak | Status |
|---|---|---|
| 1 | Pipeline-helse i morgenbrief (9b) | ✅ live |
| 2 | Lead→deal auto-fangst + ICP-scoring (Doffin) | ✅ live |
| 3 | Oppfølgings-radar (man 07:30, kladd) | ✅ live |
| 4 | Møtereferat Notably → HubSpot (daglig 07:45) | ✅ live |
| 5 | Tilbuds-generator (AI-utkast fra mal + deal) | 🔧 bygges |
| 6 | E-signering | ⛔ blokkert → beslutning |

**Åpne beslutninger:**
- **E-signering:** Adobe småbedrift mangler API. Velg: (A) Adobe Integrasjonsnøkkel-vei, eller (B) bytt til norsk BankID-leverandør (Verified / Signere / Penneo).
- **Fil-opplasting til HubSpot:** bygg Files-API, eller last via SharePoint (O365) og lim delingslenke i deal.

---

## 3. Produktlinjer under utvikling

- **BRE Cloud** — IoT-overvåking som SaaS (ARR-motor). Sterk vekst YoY (følges som fast KPI i morgenbriefen).
- **BRE Lysstyring / DALI** — tunnel-/veilysstyring (Phoenix Contact PLCnext / DALI / Lumgate). Produktark-generator i workspace.
- **Kundeportal på DGX** — privat kunde-AI der kunden spør på egne IoT-data (Fase 1 query-lag bygget).

---

## 4. Intern drift / AI-assistent (muliggjør strategien)

- OpenClaw-agent «main» = Frodes AI-assistent (morgenbrief, lead-/insider-radar, oppfølging, møtereferat, Cloud ARR-KPI).
- Integrasjoner live: O365, HubSpot, PowerOffice Go (les), Homey, weather. Se `topologi-bre-ai.html`.
- Herdet drift (API-nøkkel-auth, SecretRefs, watchdog, lokal minne-embedding).

---

## 5. Neste strategiske steg (kort liste)

- [ ] Beslutte e-signeringsvei (A vs B) → fullføre salgs-lukkings-kjeden
- [ ] Ferdigstille tilbuds-generator som gjenbrukbar kommando
- [ ] DGX fra pilot → produksjon (privat AI, kundeportal)
- [ ] Sette IT-drift ut eksternt med GDAP + retained ownership (break-glass hos Frode)
- [ ] Vurdere EIC/Horizon/Eurostars-søknad

---

_Relaterte minne-notater: `bre-digital-profile`, `salg-pipeline`, `tilbud-maler`, `bre-lysstyring-dali`, `kundeportal-dgx`, `data-handling-prinsipp`._
