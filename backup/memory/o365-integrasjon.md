---
name: o365-integrasjon
description: O365/Microsoft Graph-integrasjon FERDIG — kalender-lesing + e-post (les + kladd, Mail.ReadWrite) live; «Dagens kalender» i morgenbriefen (cron 93c12194)
metadata: 
  node_type: memory
  type: project
  originSessionId: 96ba557a-abbb-400d-8f36-e8ba50c62760
---

Besluttet 2026-07-04. Neste integrasjon i stacken: koble Frodes O365 (Outlook kalender + e-post) inn i OpenClaw via en Microsoft Graph MCP-server, så morgenbriefen åpner med «dagens kalender». Status: **venter på IT** (Frode må ta Entra-app-registrering + admin-consent med IT).

**Valgt tilnærming:** MCP-server med DELEGERT OAuth (agenten ser kun Frodes egne data, ikke hele tenanten). Rekkefølge: kalender først, deretter e-post (lese + lage KLADD). Frode vil ha kladd-funksjon. Nøkkel-sikring: gi `Mail.ReadWrite` (les innboks + opprett kladd i Utkast-mappe) men BEVISST IKKE `Mail.Send` — da kan agenten teknisk ikke sende, kun lage utkast Frode godkjenner og sender selv.

**Anbefalt server:** `ms-365-mcp-server` (Softeria) — laget for Outlook kalender/e-post/filer. Alternativer: Lokka (merill, mer tenant-admin) eller Microsofts offisielle Graph-MCP. Kobles via `openclaw mcp add` (HTTP/OAuth eller stdio) + `openclaw mcp login`, tool-filter til kalender-lesing i start. Se OpenClaw-dok `cli/mcp.md`.

**Venter på fra IT/Frode:** (1) Entra app-registrering «OpenClaw Assistent» (single tenant), (2) Allow public client flows = ja (device-code), (3) Delegated Graph-permissions med admin-consent: Calendars.Read + Mail.ReadWrite + offline_access — IKKE Mail.Send (kladd, ikke send), (4) Tenant ID + Client ID til Frode. Når disse er klare: jeg registrerer MCP-en, kjører login (Frode logger inn i nettleser én gang), og legger «📅 Dagens kalender» øverst i morgenbriefen (cron 93c12194...). Se [[daglig-morgen-brief]].

**STATUS 2026-07-05:** Entra-app «Openclaw Assistent» opprettet. TenantID `90a3d4f8-dbbf-4159-bb17-0326d34bfdc2`, ClientID `cb4af444-bca3-48a0-8a18-5bb641a82a5a`. Device-code login mot Softeria-serveren (`npx -y @softeria/ms-365-mcp-server --login` med env MS365_MCP_TENANT_ID/MS365_MCP_CLIENT_ID) fungerer pålogging OK, men blokkeres av **Conditional Access 53003**. Frode ekskluderte bruker fra Microsoft-managed «Block device code flow» — men 53003 vedvarer med `Enhetstilstand: Unregistered` (macOS-server, IP 85.93.226.154). Konklusjon: egen device-compliance grant-control («krev kompatibel/hybrid-tilknyttet enhet») blokkerer. **Venter på IT:** enten (B) ekskluder app/bruker fra device-compliance-policyen, eller (C) bytt til app-only/client-credentials (client secret + Application-permissions + admin-consent, scopet til Frodes postboks via Application Access Policy) — sjekk om Softeria støtter app-only. MCP ikke registrert i openclaw.json ennå (venter på fungerende token).

**✅ STATUS 2026-07-05 (FERDIG):** O365 er LIVE og koblet inn i morgenbriefen. IT løste blokkeringen i to steg: (1) ekskluderte bruker fra «Block device code flow», (2) ga admin-consent på appen. Device-code login mot Softeria (`@softeria/ms-365-mcp-server`) gikk gjennom. `o365`-MCP er koblet til gateway og verktøy tilgjengelig (verify-login bekrefter `frode.lillebakk@bredigital.no`; get-calendar-view leser kalenderen live — verifisert med reelle avtaler uke 28). Login-scope trimmet til KUN kalender (Calendars.Read + User.Read) — ikke mail/filer. Tips til fremtidig re-login: kjør device-code-prosessen DETACHED så den overlever gateway-restart og fanger token. **GJORT 2026-07-05:** «📅 DAGENS KALENDER» lagt inn som seksjon 0 (øverst) i morgenbrief-cron `93c12194-521e-45a4-a8a5-0955519c4348` — henter dagens avtaler via mcp__o365__get-calendar-view, kun lesing. Se [[daglig-morgen-brief]]. **EVT. SENERE:** utvide scope til Mail.ReadWrite for kladd-funksjon (bevisst utsatt).

**✅ STATUS 2026-07-05 (E-POST KLADD FERDIG):** Scope utvidet til `Mail.ReadWrite`. Ny device-code login gikk gjennom uten CA-sperre (IT hadde alt ryddet). Verifisert ende-til-ende: list-mail-messages leser innboksen live, create-draft-email lager ekte utkast i Outlook (testkladd opprettet + slettet igjen). BEVISST IKKE Mail.Send — agenten lager kun kladd Frode selv sender. O365 nå fullt operativt: kalender (les) + e-post (les + kladd). Verktøy: mcp__o365__list-mail-messages, get-mail-message, create-draft-email, create-reply-draft, create-reply-all-draft, create-forward-draft, delete-mail-message m.fl.

**Andre ventende stack-saker:** committe/backup radar-skriptene til git; hardne investor/leverandør/konkurrent-radarene mot ekte kilder (investor via Newsweb navne-watchlist som [[insider-radar]]); Diakonhjemmet-MCP cross-runtime.
