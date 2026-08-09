---
name: poweroffice-go
description: "PowerOffice Go API v2 — BRE forretningssystem; LIVE PROD 2026-07-20, klient poweroffice.py"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
  modified: 2026-08-05T13:27:39.135Z
---

PowerOffice Go = BRE Digitals forretningssystem (økonomi/regnskap/lønn). Integrasjon under oppsett (Frode 2026-07-06).

- **Swagger UI:** https://prdm0go0stor0apiv20eurw.z6.web.core.windows.net/
- **Base-URL:** `https://goapi.poweroffice.net/v2` · OpenAPI 3.0.4 · auth = Bearer JWT (`bearerAuth`).
- **Underlag lagret lokalt:** `workspace/poweroffice/` — README.md (indeks) + `openapispecs/*.json` (39 områder, 184 paths, 297 operasjoner, lastet ned 2026-07-06).
- **Token/auth (VERIFISERT):** OAuth2 client credentials. `Authorization: Basic base64(ApplicationKey:ClientKey)` + header `Ocp-Apim-Subscription-Key: <subscription>` mot token-endpoint. Alle kall trenger BÅDE Bearer-token OG subscription-header (APIM). Token demo: `https://goapi.poweroffice.net/Demo/OAuth/Token`, base demo: `.../Demo/v2`. Prod: uten `/Demo`. Application key=client_id, Client key=client_secret. Subscription key er hex u/bindestreker (IKKE GUID); Client ID er egen GUID som ikke brukes i auth.
- **STATUS: ✅ LIVE PROD 2026-07-20.** Klient `workspace/poweroffice/poweroffice.py`, `environment=prod` → base `https://goapi.poweroffice.net/v2`. Nøkler i `config.json` (gitignorert; nå også `config.json.bak-*` — ALDRI i memory/backup). Prod-utvidelse = «POGO BRE» (starter-prod-abonnement). Verifisert mot ekte klient **BRE Digital AS** (ClientId 41de3a7e-1228-4dce-8f31-6c3d5ce94045). Bruk: `python3 poweroffice.py --smoke` eller `... GET /<path>`.
  - **Aktive abonnement:** Accounting, TimeTracking, Payroll, TravelExpense, HolidayAndLeave.
  - **Gyldige privilegier (les):** AccountTransaction, Budget, GeneralLedgerAccount, IncomingInvoice, JournalEntryVoucher, Enterprises, Location, ClientBankAccount, ContactBankAccount, Employee + Employment/lønn-felter, PayItem, PayrollSettings, CommonServices.
  - **Salg/Faktura åpnet 2026-08-05 ✅:** PowerOffice ga lese-tilgang til **Customers, OutgoingInvoices, SalesOrders** (etter Frodes e-post s.d.). Verifisert live. NB: filtrering — SalesOrders bruker `salesOrderNos` (ikke orderNos); OutgoingInvoices bruker `orderNos`/`invoiceNos` + krever fromDate/toDate. Klient trunkerer print på 4000 tegn → bruk `import poweroffice as po; po.api('GET',path)` for store svar. Fortsatt 403: Voucher-GET, Products, Projects (ikke kritisk). InvalidPrivileges: ClientAdmin + Quality*.
  - Testcase løst: SalesOrder 2107 = Snarkjøp Gruppen (kundenr 10031), 54× Efento Cloud 5-års lisens, netto 21 924 / totalt 27 405 kr.
  - **API-teknisk:** paging = `PageNumber`/`PageSize` (IKKE OData `$top`). Klient trunkerer print på 4000 tegn — for store svar: `import poweroffice as po; po.api("GET",path)`. Lønn: `/Employees/Employments/{id}/Salaries` (felt AnnualSalary, FromDate) — nyeste FromDate = gjeldende. AccountTransactions bærer `ProjectCode`/`ProjectId` (kan skille kunde-prosjekt via bilagstekst når Customer=403).
  - Demo-config bevart i `config.json.bak-20260720-134024` (subscription «BreDigitalAs-Demo»).
  - ⚠️ Prod = ekte regnskapsdata → hold på **lesing**; ingen skriv/bilag uten eksplisitt OK fra Frode.
  - **BRE Cloud-inntekt** = konti **3610 + 3613 + 3615** (BRE IoT Cloud). Script `poweroffice/cloud_arr.py` (JSON ytd/priorTotal/runRate) — LAGT INN som fast KPI-linje «10b» i morgenbrief-cron (2026-07-20). 2026 YTD ≈ 1,44 MNOK vs 1,14 MNOK helår 2025 (≈dobling, årstakt ~2,6 MNOK).
- **PROD-TILGANG (prosess, oppgitt av PowerOffice 2026-07-06):** kontakt `go-api@poweroffice.no`. De trenger info om appen (formål, v2 vs v1, bruksmønster, forventet trafikkvolum), org-info og formell **signering av vilkår**; noen ganger et kort møte før lansering. Tidslinje typisk **live innen 1–2 uker**. Bygg/test ferdig mot Demo først; bytt kun environment+nøkler ved prod.
- **Mest relevant for BRE:** Customers/Customer Ledger, Projects (deal→prosjekt), Outgoing Invoices/Sales Orders, Trial Balance/Account Transactions (nøkkeltall i morgenbrief), Products (→ tilbud-generator). Kobles mot [[salg-pipeline]] (HubSpot vunnet deal → kunde/prosjekt i PowerOffice).
