---
name: salg-pipeline
description: "Salgseffektivisering BRE Digital — pipeline-diagnose + roadmap (pipeline-helse, e-sign, tilbud-gen, lead-capture)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 96ba557a-abbb-400d-8f36-e8ba50c62760
---

Diagnose 2026-07-05 (fra HubSpot, owner Frode 89064005): ~42 åpne deals, ~9,5 MNOK samlet, men ~30 hadde PASSERT closedate og stod fortsatt åpne (noen fra mars). Flaskehalsen er IKKE leads — det er **oppfølging og lukking**. 8 deals stod på 'decisionmakerboughtin' (kjøpsklare, ~2 MNOK) uten å lukkes. NB: PTG Compact skap = 2,5 MNOK i deal-kortet (oppgavetittel sa feilaktig 5 MNOK).

Salgsstegene vurdert: Lead ✅ (radar, men ikke auto→CRM/scoring) · Tilbud ❌ (manuelt) · Oppfølging 🔴 (svakest) · Forhandling ⚠️ (ingen møteforb.) · Signering ❌ (ingen e-sign).

**Roadmap (prioritert):**
1. ✅ GJORT 2026-07-05: **Pipeline-helse i morgenbriefen** (seksjon 9b) — flagger åpne deals som er forbi frist / stille 14+ dager / kjøpsklare-men-ikke-lukket, sortert på beløp, med handlingsforslag. Bygger på HubSpot MCP (ingen ny integrasjon). Se [[daglig-morgen-brief]].
2. **E-signering** (neste, størst utslag): nordisk e-sign (Verified/Scrive/Penneo/GetAccept) + kontraktmaler → de 8 kjøpsklare lukkes raskt.
3. **Tilbuds-generator:** AI-norsk tilbudsutkast fra mal + HubSpot deal/line-items → Frode redigerer/sender.
4. ✅ GJORT 2026-07-05: **Lead→deal auto-fangst + ICP-scoring.** `doffin.py` scorer hver lead 0-100 (ICP_THRESHOLD=70) med icpReasons + capture-bool (nøkkelord + offentlig/industri + verdi + rammeavtale/DPS, minus irrelevant). Morgenbriefen auto-oppretter deal i HubSpot for 'new'-leads med capture=true: dealname '[Doffin] <heading>', pipeline default, stage appointmentscheduled, owner 89064005, dedup ved å søke Doffin-id først. Testkalibrering: NB-IoT vannmålere 85, byggautomasjon/sensorovervåking/DPS-er 70 (fanges); PLS/ren-VA 40-55 (fanges ikke). Se [[lead-radar-doffin]].
5. Forhandling: AI møte-brief per deal (historikk, stakeholders, siste kontakt) — særlig når [[o365-integrasjon]] (kalender) er oppe.
