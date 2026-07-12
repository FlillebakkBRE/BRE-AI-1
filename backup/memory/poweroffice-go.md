---
name: poweroffice-go
description: "PowerOffice Go API v2 — BRE forretningssystem; LIVE Demo 2026-07-06, klient poweroffice.py"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

PowerOffice Go = BRE Digitals forretningssystem (økonomi/regnskap/lønn). Integrasjon under oppsett (Frode 2026-07-06).

- **Swagger UI:** https://prdm0go0stor0apiv20eurw.z6.web.core.windows.net/
- **Base-URL:** `https://goapi.poweroffice.net/v2` · OpenAPI 3.0.4 · auth = Bearer JWT (`bearerAuth`).
- **Underlag lagret lokalt:** `workspace/poweroffice/` — README.md (indeks) + `openapispecs/*.json` (39 områder, 184 paths, 297 operasjoner, lastet ned 2026-07-06).
- **Token/auth (VERIFISERT):** OAuth2 client credentials. `Authorization: Basic base64(ApplicationKey:ClientKey)` + header `Ocp-Apim-Subscription-Key: <subscription>` mot token-endpoint. Alle kall trenger BÅDE Bearer-token OG subscription-header (APIM). Token demo: `https://goapi.poweroffice.net/Demo/OAuth/Token`, base demo: `.../Demo/v2`. Prod: uten `/Demo`. Application key=client_id, Client key=client_secret. Subscription key er hex u/bindestreker (IKKE GUID); Client ID er egen GUID som ikke brukes i auth.
- **STATUS: ✅ LIVE (Demo) 2026-07-06.** Klient `workspace/poweroffice/poweroffice.py` (token-cache i .token_cache.json, gitignorert). Nøkler i `workspace/poweroffice/config.json` (gitignorert, chmod 600 — ALDRI i memory/backup). Subscription «BreDigitalAs-Demo». Klient = BRE Digital AS, full tilgang (Customer/Project/OutgoingInvoice/Product/TrialBalance/Voucher/Supplier/Employee/Payroll). Demo-klient er tom for data foreløpig. Bruk: `python3 poweroffice.py --smoke` eller `... GET /Projects`. Prod-nøkler byttes inn senere (sett environment=prod + nye nøkler).
- **PROD-TILGANG (prosess, oppgitt av PowerOffice 2026-07-06):** kontakt `go-api@poweroffice.no`. De trenger info om appen (formål, v2 vs v1, bruksmønster, forventet trafikkvolum), org-info og formell **signering av vilkår**; noen ganger et kort møte før lansering. Tidslinje typisk **live innen 1–2 uker**. Bygg/test ferdig mot Demo først; bytt kun environment+nøkler ved prod.
- **Mest relevant for BRE:** Customers/Customer Ledger, Projects (deal→prosjekt), Outgoing Invoices/Sales Orders, Trial Balance/Account Transactions (nøkkeltall i morgenbrief), Products (→ tilbud-generator). Kobles mot [[salg-pipeline]] (HubSpot vunnet deal → kunde/prosjekt i PowerOffice).
