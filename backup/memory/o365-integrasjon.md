---
name: o365-integrasjon
description: Planlagt O365/Microsoft Graph-integrasjon (kalender→e-post) i morgenbriefen — venter på IT/Entra-oppsett
metadata: 
  node_type: memory
  type: project
  originSessionId: 96ba557a-abbb-400d-8f36-e8ba50c62760
---

Besluttet 2026-07-04. Neste integrasjon i stacken: koble Frodes O365 (Outlook kalender + e-post) inn i OpenClaw via en Microsoft Graph MCP-server, så morgenbriefen åpner med «dagens kalender». Status: **venter på IT** (Frode må ta Entra-app-registrering + admin-consent med IT).

**Valgt tilnærming:** MCP-server med DELEGERT OAuth (agenten ser kun Frodes egne data, ikke hele tenanten). Rekkefølge: kalender først, deretter e-post (lese + lage KLADD). Frode vil ha kladd-funksjon. Nøkkel-sikring: gi `Mail.ReadWrite` (les innboks + opprett kladd i Utkast-mappe) men BEVISST IKKE `Mail.Send` — da kan agenten teknisk ikke sende, kun lage utkast Frode godkjenner og sender selv.

**Anbefalt server:** `ms-365-mcp-server` (Softeria) — laget for Outlook kalender/e-post/filer. Alternativer: Lokka (merill, mer tenant-admin) eller Microsofts offisielle Graph-MCP. Kobles via `openclaw mcp add` (HTTP/OAuth eller stdio) + `openclaw mcp login`, tool-filter til kalender-lesing i start. Se OpenClaw-dok `cli/mcp.md`.

**Venter på fra IT/Frode:** (1) Entra app-registrering «OpenClaw Assistent» (single tenant), (2) Allow public client flows = ja (device-code), (3) Delegated Graph-permissions med admin-consent: Calendars.Read + Mail.ReadWrite + offline_access — IKKE Mail.Send (kladd, ikke send), (4) Tenant ID + Client ID til Frode. Når disse er klare: jeg registrerer MCP-en, kjører login (Frode logger inn i nettleser én gang), og legger «📅 Dagens kalender» øverst i morgenbriefen (cron 93c12194...). Se [[daglig-morgen-brief]].

**Andre ventende stack-saker:** committe/backup radar-skriptene til git; hardne investor/leverandør/konkurrent-radarene mot ekte kilder (investor via Newsweb navne-watchlist som [[insider-radar]]); Diakonhjemmet-MCP cross-runtime.
