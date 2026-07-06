---
name: bre-homey
description: Homey (Athom) integrasjon — LIVE via sky-proxy; script homey/homey.py leser enheter/sensorer
metadata: 
  node_type: memory
  type: project
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

LIVE 2026-07-06 (natt): Homey-integrasjon virker. Frodes Homey Pro (v13.3.0).
- **Homey ID / cloudId:** `653e4b878a5393d15177f28c` → base-URL `https://653e4b878a5393d15177f28c.connect.athom.com`
- **API-nøkkel:** lokal Homey Pro API-key (3-delt `uuid:uuid:hex`), lagret i `workspace/homey/config.json` (GITIGNORERT — kommer ikke i GitHub-backup). Brukes som `Authorization: Bearer <key>`. Roter ved behov via tools.developer.homey.app.
- **Virker fra ekstern server** via sky-proxyen (connect.athom.com) — trengte Homey-ID (kunne ikke utledes av nøkkelen; `*.connect.athom.com` er wildcard som 400-er uten gyldig id). Nøkkelen er IKKE et Athom-sky-OAuth-token (401 mot api.athom.com).
- **Script:** `workspace/homey/homey.py` — `python3 homey.py` gir lesbar oppsummering (enheter per klasse, temperatur, effekt, aktive alarmer); `--json` for maskinlesbart. Endepunkt: `/api/manager/system/`, `/api/manager/devices/device`, `/api/manager/zones/zone`, `/api/manager/flow/flow`.
- **Status ved oppsett:** 56 enheter (44 lys/Hue, 7 sensorer, 4 stikk, 1 ovn). Flows kom tomt — nøkkelens scope manglet trolig `flow` (utvid nøkkel-scope for å trigge scener/styre).
- **Neste:** legge Homey-nøkkeltall i morgenbrief hvis ønsket; utvide scope for flow-trigging/enhetsstyring; avklar bruk (hjemme vs. kunde-demo for BRE IoT-salg).
