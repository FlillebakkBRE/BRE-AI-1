---
name: openclaw-stabilitet
description: Gateway-watchdog (launchd) installert 2026-07-17 for å auto-restarte hengt gateway; MCP-flap er mistenkt rotårsak
metadata: 
  node_type: memory
  type: project
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

**Problem (2026-07-17):** Frode måtte restarte Mac mini for å få OpenClaw til å funke igjen. Diagnose: maskinvare frisk (92% ledig minne, 3% disk). Gateway kjører som LaunchAgent `ai.openclaw.gateway` (port 18789). Mistenkt rotårsak: **MCP-laget flapper** — 17 MCP-servere (o365, hubspot, diakonhjemmet + 14 åpne-data mount'et via felles `main.py`) hoppet av/på samtidig gjennom hele økter → tyder på én felles MCP-vert som henger/restarter. Når *gateway* henger (ikke krasjer) fanger ikke LaunchAgent det.

**GJORT — pkt 2 (watchdog):** Uavhengig launchd-watchdog installert:
- Skript: `~/.openclaw/watchdog/gateway_watchdog.sh` (sh). Sjekker `http://127.0.0.1:18789/` 3× (5s mellomrom, --max-time 8); ved 3 feil: `launchctl kickstart -k gui/501/ai.openclaw.gateway`. Logg: `~/.openclaw/watchdog/watchdog.log` (kun ved restart), + launchd.out/err.
- Tjeneste: `~/Library/LaunchAgents/ai.openclaw.gateway.watchdog.plist` — StartInterval 120s, RunAtLoad. Lastet med `launchctl bootstrap gui/501`. Verifisert active + testkjørt exit 0. Restart-pathen ikke force-testet (ville droppet live-økta).

**IKKE gjort ennå — pkt 1 (Frode vurderer):** slå av de 13 ubrukte åpne-data-MCP-ene (entsoe, ssb, stortinget, lovdata, vegvesen, geonorge, norgesbank, nve, statnett, strompris, luftkvalitet, postlister, firmafakta) i `~/.openclaw/openclaw.json` — behold o365/hubspot/diakonhjemmet/weather. Reduserer flap-flate/last. Reversibelt.

**GJORT — oppgradering (2026-07-18):** openclaw oppgradert `2026.6.9` → `2026.7.1-2` (nyeste stabile). Config/nøkler/minne urørt. Kan hjelpe på MCP-flap.

**GJORT — sikkerhetshardening (2026-07-18):** `openclaw security audit --deep` gikk fra 5→2 advarsler. Slått av `gateway.controlUi.allowInsecureAuth` (→false) og satt `tools.fs.workspaceOnly=true` (agentens filtilgang låst til workspace). Brave-plugin-advarselen forsvant av seg selv — pluginen er bundlet inn i openclaw-pakken (dist/), ikke separat npm-avhengighet, så den følger openclaw-versjonen. Gjenværende 2 advarsler er by-design for én-operatør: trusted_proxies (kun relevant ved reverse proxy; vi er loopback) + multi_user_heuristic (trigges av Telegram-allowlist).

**Neste ved behov:** grave i gateway/MCP-logger for å finne *hvorfor* main.py-verten faller (rotårsak, ikke bare symptom). Pkt 1 (slå av 13 ubrukte åpne-data-MCP) gjenstår fortsatt som egentlig flap-fiks.
