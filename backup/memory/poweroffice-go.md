---
name: poweroffice-go
description: "PowerOffice Go API v2 — BRE forretningssystem; OpenAPI-specs lastet ned, venter på nøkler"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

PowerOffice Go = BRE Digitals forretningssystem (økonomi/regnskap/lønn). Integrasjon under oppsett (Frode 2026-07-06).

- **Swagger UI:** https://prdm0go0stor0apiv20eurw.z6.web.core.windows.net/
- **Base-URL:** `https://goapi.poweroffice.net/v2` · OpenAPI 3.0.4 · auth = Bearer JWT (`bearerAuth`).
- **Underlag lagret lokalt:** `workspace/poweroffice/` — README.md (indeks) + `openapispecs/*.json` (39 områder, 184 paths, 297 operasjoner, lastet ned 2026-07-06).
- **Token/auth:** JWT via PowerOffice token-tjeneste (OAuth2 client credentials: Application key + Client key + Subscription key). Eksakt token-endpoint bekreftes når nøklene kommer — IKKE gjett i prod. Start mot Demo-miljø.
- **STATUS:** ⏳ venter på API-nøkler fra PowerOffice. Når de kommer: bygg klient/MCP (doffin.py/homey.py-mønster).
- **Mest relevant for BRE:** Customers/Customer Ledger, Projects (deal→prosjekt), Outgoing Invoices/Sales Orders, Trial Balance/Account Transactions (nøkkeltall i morgenbrief), Products (→ tilbud-generator). Kobles mot [[salg-pipeline]] (HubSpot vunnet deal → kunde/prosjekt i PowerOffice).
