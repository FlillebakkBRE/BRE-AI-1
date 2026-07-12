---
name: kundeportal-dgx
description: Privat kunde-AI på DGX — kundeportal der kunde spør på egne IoT-data; Fase 1 query-lag bygget
metadata: 
  node_type: memory
  type: project
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

Produktidé (Frode 2026-07-07): la kunder (f.eks. Diakonhjemmet) spørre på **sine egne** IoT-data i naturlig språk, kjørt på **lokal modell på DGX Spark** — data forlater aldri BRE/kundens infra. Sterk mot helse/offentlig + NIS2/personvern. Differensiator: «privat AI på egne data».

**Avklart arkitektur:** IKKE kundebrukere på BREs Claude-konto (tenant-blanding/GDPR/kost). Behold Claude-connector til BRE-intern bruk. Kundevendt = egen portal på DGX: Open WebUI (chat) → Ollama (lokal LLM) → `query_layer.py` (tenant-scoped, read-only) → InfluxDB (BRE Cloud). Alternativ B = Anthropic API server-side m/ DPA hvis sky aksepteres.

**Fase 1 bygget 2026-07-07** i `workspace/kundeportal/`:
- `query_layer.py` — 2 verktøy: `list_metrics(tenant_id)` + `query_timeseries(tenant_id, measurement, field, start, stop, aggregate, every)`. Modellen sender KUN strukturerte parametre; laget bygger Flux med bucket LÅST til kundens bucket. Read-only, injeksjonssikret (validerer identifikator/tid/aggregat), ukjent tenant avvises. Mock-modus (token="MOCK") for demo uten creds — verifisert kjørende + guardrails testet.
- `tools_schema.json` (LLM function-calling), `config.example.json` (tenant→bucket+read-only-token), README m/ DGX deploy-guide (Ollama + Open WebUI + Caddy/TLS). config.json gitignorert.
- **Sikkerhetsprinsipp:** tenant_id settes av backend fra innlogget bruker, ALDRI av modellen; per-kunde read-only InfluxDB-token + egen bucket.

**Gjenstår:** (1) ekte schema fra Diakonhjemmet-bucket (via [[diakonhjemmet-mcp]] / InfluxDB read-token) for å bekrefte målingsnavn; (2) Ollama+Open WebUI på DGX; (3) tenant-innlogging → tool-binding server-side. Estimat: Fase 1 ~2–4 dagsverk (query-lag ✅ ferdig), Fase 2 flerkunde-produkt +1–2 uker.
