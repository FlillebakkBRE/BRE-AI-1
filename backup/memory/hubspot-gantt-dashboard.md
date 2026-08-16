---
name: hubspot-gantt-dashboard
description: "BRE Prosjekt-Gantt web-dashboard (gantt_server.py) — LAN-tilgang, Basic Auth, launchd, Fagområde-filter"
metadata: 
  node_type: memory
  type: project
  originSessionId: e4fa5993-9781-463d-ae3d-b23c107ccf0f
  modified: 2026-08-14T07:52:08.278Z
---

Web-Gantt over HubSpot-prosjekter (0-970) + oppgaver: `workspace/hubspot-gantt/gantt_server.py` (henter live via pat-token som aldri forlater serveren). **Ikke lenger read-only (2026-08-13): kan redigere tilbake til HubSpot.**

- **Redigering fra brettet (2026-08-13):** POST-endepunkter bak samme Basic Auth:
  - `/move` — dra stolpe = flytt; dra kant = juster start/forfall. Lagrer `hs_timestamp` (forfall, kl 12:00Z) + `bre_start_date` (ny date-property «Startdato (BRE)», gruppe `taskinformation`). Stolpe = start→forfall når startdato satt, ellers 1-dag ved forfall.
  - `/owner` — klikk eier-navn i venstremeny → nedtrekk (alle eiere fra `/crm/v3/owners`) → setter `hubspot_owner_id` («» = fjern).
  - `/status` — klikk status-brikke (farget prikk + etikett) → setter `hs_task_status` (NOT_STARTED/IN_PROGRESS/WAITING/DEFERRED/COMPLETED).
  - `/prio` — klikk prioritet-flagg ⚑ → setter `hs_task_priority` (NONE/LOW/MEDIUM/HIGH).
  - `/utforende` — klikk utførende-kolonne → setter enumeration-property `bre_utforende` (**«Utførende (BRE)»**, seedet med teamet). Egen fra eier.
  - Forfalt-markering (åpen forbi forfall = rød ramme+⚠️), «i dag»-linje, eier-filter (nedtrekk), uke/måned-skillelinjer (`.tick`/`.tick.thick`). Overstyrings-lag (`remember_override`, 5 min TTL) mot HubSpot liste-etterslep — ellers hoppet endringer «tilbake» ved Oppdater.
  - **↶ Angre**-knapp i topp: klient-stakk, sender revers til samme endepunkt + `location.reload()`. Dekker move/owner/status.
- **Visnings-detaljer:** frappe sin lilla progress-overlay (`.bar-progress #a3a3ff`) nøytralisert (`fill:transparent`) — fullførte = grå, ikke lilla. Venstremeny låst til 30px rad-pitch + 56px topp-offset + 1:1 scroll-synk for å ligge rad-for-rad med stolpene. Rad-kolonner: emne (forkortes, `min-width:0`) · status · eier.

- **URL på kontornett:** `http://192.168.50.126:8787` (Mac-ens LAN-IP; kan endre seg ved DHCP → vurder fast reservasjon/Tailscale). Binder til `HOST=0.0.0.0`.
- **Innlogging:** Basic Auth, bruker/passord i **gitignorert** `hubspot-gantt/gantt_auth.json` (`{"user","pass"}`). Mangler fila → ingen auth. Bruker i dag: `bre`.
- **Autostart:** launchd `~/Library/LaunchAgents/ai.openclaw.gantt.plist` (versjonert kopi i `hubspot-gantt/`), RunAtLoad+KeepAlive, `/usr/bin/python3`. Styr: `launchctl bootout/bootstrap gui/$(id -u) <plist>`. (Samme mønster som [[bre-homey]] varmestyring.)
- **Fagområde-filter (2026-08-10):** egendefinert oppgave-property `bre_fagomrade` (enum: tavleverksted/utvikling/installasjon/drift_leveranse/salg, gruppe `taskinformation`). Gantt har filter-lenker `?fag=<verdi>` + fargelegging + legend. HubSpot native: filtrer oppgavelister på «Fagområde».
- **Fagområde-tagging (2026-08-12/13):** ~175/390 oppgaver tagget manuelt/regelbasert. Gjenstår bl.a. Foodman Kjellingmoen, Diakonhjemmet, Redox, Foodman Myrfaret. Relatert: [[hubspot-prosjekt-kobling]].
