---
name: bre-homey
description: Homey (Athom) integrasjon — LIVE via sky-proxy; script homey/homey.py leser enheter/sensorer
metadata: 
  node_type: memory
  type: project
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
  modified: 2026-08-12T12:21:49.968Z
---

LIVE 2026-07-06 (natt): Homey-integrasjon virker. Frodes Homey Pro (v13.3.0).
- **Homey ID / cloudId:** `653e4b878a5393d15177f28c` → base-URL `https://653e4b878a5393d15177f28c.connect.athom.com`
- **API-nøkkel:** lokal Homey Pro API-key (3-delt `uuid:uuid:hex`), lagret i `workspace/homey/config.json` (GITIGNORERT — kommer ikke i GitHub-backup). Brukes som `Authorization: Bearer <key>`. Roter ved behov via tools.developer.homey.app.
- **Virker fra ekstern server** via sky-proxyen (connect.athom.com) — trengte Homey-ID (kunne ikke utledes av nøkkelen; `*.connect.athom.com` er wildcard som 400-er uten gyldig id). Nøkkelen er IKKE et Athom-sky-OAuth-token (401 mot api.athom.com).
- **Script:** `workspace/homey/homey.py` — `python3 homey.py` gir lesbar oppsummering (enheter per klasse, temperatur, effekt, aktive alarmer); `--json` for maskinlesbart. Endepunkt: `/api/manager/system/`, `/api/manager/devices/device`, `/api/manager/zones/zone`, `/api/manager/flow/flow`.
- **Status ved oppsett:** 56 enheter (44 lys/Hue, 7 sensorer, 4 stikk, 1 ovn). Flows kom tomt — nøkkelens scope manglet trolig `flow` (utvid nøkkel-scope for å trigge scener/styre).
- **SKRIVING VIRKER (2026-08-09):** `PUT /api/manager/devices/device/{id}/capability/{cap}` body `{"value":X}` setter kapabilitet. Retur 200 med `{transactionTime,value}`.
- **Varmestyring FL Varmovn (Frodes kontor) — LIVE 2026-08-09:** enhet-id `b7696811-0800-44fe-ae4c-b7d85faa6962` (class heater, termostat target_temperature 4–35°C, PID). VIKTIG: må sette `individual_control=true` FØR `target_temperature` kan endres (ellers 400 «Individuell kontroll er deaktivert»). Også `onoff=true`.
  - `homey/set_heater.py comfort|eco|<temp>` — engangs-setter (comfort=22°C, eco=17°C).
  - `homey/heater_scheduler.py` — daemon, poller hvert 5. min, idempotent/selv-helbredende. Regel (oppdatert 2026-08-10): komfort **22°C man–fre 07:30–16:00** (varmt kontor før 08), ellers spar 17°C (helg = spar hele tiden). Logg: `homey/heater.log`. **Multi-device:** styrer nå flere ovner via `DEVICES`-lista — FL Varmovn (Frode, b7696811…), EO Varmovn (Erlend, f48fc127…), **AHB Varmovn (Alf Helge, 46772c70…) + Verksted Ovn (10bf35b7-1af0-4dc1-ae8c-39156b6300ea) lagt til 2026-08-12** (nattsenking = samme regel). Styrer nå 4 ovner. «Kontor 1 Ovn» (4f7880b0…) finnes men styres ikke. `set_heater.py` gjelder fortsatt kun FL.
  - **crontab virker IKKE headless** (macOS Full Disk Access-sperre → henger). OpenClaw isolerte cron-økter mangler `exec`-verktøy (toolsAllow strippet). Derfor daemon-mønster.
  - **launchd LaunchAgent på plass 2026-08-10:** `~/Library/LaunchAgents/ai.openclaw.homey-heater.plist` (versjonert kopi i `homey/`). RunAtLoad + KeepAlive → starter ved innlogging og restartes ved kræsj/reboot (verifisert). Kjør `/usr/bin/python3`. Styr med `launchctl bootout/bootstrap gui/$(id -u) <plist>`.
- **Neste:** launchd auto-start for gantt_server (samme mønster, gjenstår); legge Homey-nøkkeltall i morgenbrief hvis ønsket; avklar bruk (hjemme vs. kunde-demo for BRE IoT-salg).
