---
name: data-handling-prinsipp
description: "Frodes datahåndterings-/eksponeringsprinsipp — M365 som fasit, samle i workspace mot DGX-migrering, unngå dobbeltlagring i Claude"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

Frode (2026-07-08) om dataeksponering og fillagring:

**Retning:** Samle BRE-filer i OpenClaw-workspace («her») nå, som **staging mot fremtidig DGX-migrering** (lokal modell = full suverenitet, «forlater aldri huset»). Migrerer da plassering, ikke hele arbeidsflyten.

**Prinsipp for hvor data skal ligge:**
- **M365-tenant (SharePoint/OneDrive) = fasit** for forretningsfiler (kalkyler, BOM, tilbud) — EU-residens, egen leverandør, DPA.
- **Ikke dupliser** kunde-/forretningsdata inn i **Claude.ai-prosjektmapper** (legger ekstra kopi hos Anthropic/USA → større angrepsflate).
- **Mest sensitivt** (helse/[[diakonhjemmet-mcp]], NIS2-kundedata) → **DGX lokalt** (se [[kundeportal-dgx]]).

**Why:** Frode vil være minst mulig eksponert. Færre lagringssteder + egen tenant + lokal kjøring for det følsomme = lavere risiko.

**How to apply:** Når jeg foreslår lagring/opplasting: anbefal M365 eller workspace, ikke Claude-prosjekt for forretnings-/kundedata. Vær ærlig på at workspace i dag git-backes til privat GitHub OG at innhold jeg behandler sendes til Anthropic i turen — full suverenitet først på DGX. For sensitivt: styr mot DGX. Minn om DPA (Microsoft + Anthropic) ved forretningsdata.
