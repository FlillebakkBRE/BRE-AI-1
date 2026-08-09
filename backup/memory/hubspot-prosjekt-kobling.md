---
name: hubspot-prosjekt-kobling
description: HubSpot auto-kobling av avtaler/oppgaver/tickets til prosjekt (navn=selskap); daglig cron + skript
metadata: 
  node_type: memory
  type: project
  originSessionId: e4fa5993-9781-463d-ae3d-b23c107ccf0f
  modified: 2026-08-06T20:26:54.283Z
---

BRE vil at alle avtaler, oppgaver og tickets i HubSpot skal ha et **prosjekt** tilknyttet, der prosjektnavn = selskapsnavn (én prosjekt-record per selskap). Etablert 2026-08-05.

**Metodikk (samme for alle 3 objekttyper):** for objekt uten prosjekt → finn selskapets prosjekt via normalisert navnematch (strip " AS"/" IS", spaceless-fallback), opprett prosjekt (=selskapsnavn) hvis mangler, knytt objekt→prosjekt. Hopp over: objekter uten selskap, selskap uten navn, og «BRE Digital» (oss selv). **Avtaler** ekskluderer i tillegg steg Fakturert (4973680889), Klar til fakturering (4973840579), Salg tapt (closedlost).

**Nøkkel-IDer:** prosjekt-objekt `0-970`; Project Pipeline `139663aa-09ee-418e-b67d-c8cfcd3e5ce3`, steg Planning `acc364b5-d367-49f4-a957-cc4fbf7e8e4b`. Assoc-typeId (HUBSPOT_DEFINED): deal→prosjekt **1239**, task→prosjekt **1247**, ticket→prosjekt **1241**. Alias-kart: imenco→«Imenco Aqua», foodman→«Foodman - Generelt».

**Skript:** `workspace/hubspot/hubspot_project_linker.py` (idempotent — rører kun objekter uten prosjekt). `--dry-run` for rapport uten skriv. Leser HubSpot pat-token fra `~/.openclaw/openclaw.json` (mcp.servers.hubspot.env). Logger til `hubspot/project_linker.log`. Direkte REST mot api.hubapi.com (ikke MCP).

**Daglig cron:** «HubSpot prosjekt-kobling (daglig)» id `0dc91b72-794b-42b6-92dc-4b57577857f7`, 06:55 Europe/Oslo, systemEvent→hovedsesjon; sender ALLTID kort statuslinje (endret 2026-08-05 fra «stille ved 0» til fast dagsrapport).

**Prosjekt-flagg for Gantt-filter (2026-08-05):** custom bool-egenskap på prosjekt `har_oppgave_eller_ticket` (label «Har oppgave/ticket», gruppe project_information). Skriptet har `refresh_project_flags()` som kjører sist i hver runde. **Regel (justert 2026-08-05 kveld): true = ≥1 ÅPEN oppgave (status≠COMPLETED) ELLER ≥1 åpen ticket.** **Fiks 2026-08-06 kveld:** lukket-ticket-steg hentes nå DYNAMISK via `closed_ticket_stages()` (isClosed=true fra `/crm/v3/pipelines/tickets`) — tidligere hardkodet `"4"` som bare gjaldt Support Pipeline. BRE har 4 ticket-pipelines (Support=0, Leveranse=3624190191, Utvikling=3624190192, Alle=3659094223) med egne lukket-steg. Korrigerte 4 prosjekter true→false (Alotta, BOS Power, Fagkaup IS, Drågen Smokehouse) som kun hadde lukkede tickets. Task-sekvenser (blokkert-flagg) er skissert i `hubspot/task_sequencer.py` (ikke i cron ennå; venter på spor/parallell-håndtering). Fullførte/lukkede teller ikke — ellers vises prosjekter med bare ferdige oppgaver som «tomme» i Gantt (f.eks. 4subsea hadde 2 COMPLETED tasks → skal være Nei). Frode filtrerer Gantt/prosjektvisning på dette = Ja for å skjule deal-only-prosjekter — i stedet for å slette dem. Init 2026-08-05: 46 Ja / 15 Nei av 61 prosjekter. (HubSpot Projects støtter ikke direkte «har assosiert task/ticket»-filter, derfor flagget.)

**Førstegangs-opprydning 2026-08-05:** 290 koblinger (avtaler 53, oppgaver 138, tickets 99) + 36 nye prosjekter. Full logg: `workspace/hubspot-prosjekt-kobling-20260805.md`. Krevde at tickets-scope (crm.objects.tickets.read/write) ble lagt til i HubSpot private app. Relatert: [[hubspot-pipeline-steg]], [[salg-pipeline]].
