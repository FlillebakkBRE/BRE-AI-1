---
name: bre-lysstyring-dali
description: BRE produktlinje for tunnel-/infrastruktur-lysstyring (DALI-2/Lumgate); produktark generert i workspace/bre-lysstyring/
metadata: 
  node_type: memory
  type: project
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

BRE-produktlinje: **lysstyring for tunnel & infrastruktur** — BRE er norsk systemintegrator for Phoenix Contact PLCnext-basert løsning (DALI-2 + Lumgate). Egen produktlinje ved siden av IoT/automasjon. Radaren fanger nå lys/DALI-anbud (se [[lead-radar-doffin]]).

**Teknisk (fra kundens underlag, Phoenix Contact C250252 / TLA-DALI):** Kontroller = AXC F 2152 (PLCnext, 16 DI/DO, 4 AI, webserver, IEC 62443, OPC UA/Modbus TCP/PROFINET). Komponenter: CTRL-CAB / CTRL-CAB-HMI (skap, 10,1″ HMI), MODULAR-BOX-2 (4 DALI-segm.) / MODULAR-BOX-1 (2 segm.) tunnelbokser IP65, AI-CAMERA INPUT (Modbus TCP, 4–20 mA luminanskamera). Lumgate V4 = universell LED-driver-gateway (1–10 V + DALI-2), leverandøruavhengig. 1 skap → 8 DALI-bokser, 64 drivere/master. Referanser: Hvalfjörður (Island), Færøyene 11,3 km, Bjørum–Skaret, Mælefjelltunnelen, Hundvåg.

**Produktark laget 2026-07-08:** `workspace/bre-lysstyring/` — `gen_produktark.py` (python-docx → docx, konverter til PDF med `soffice --headless --convert-to pdf`). Output `Produktark_BRE_Lysstyring_DALI.pdf` (2 sider, BRE-brand: logo BRE_logo_liten.png, farger #005689/#0092D2/#59C2EA/#FAE100). Egen BRE-tegnet arkitekturskisse i `img/arkitektur_bre.svg` (rsvg-convert → png) som navngir komponentene. Referanse-galleri bruker bilder trukket ut av kundens PDF-er med `pdfimages` (i `img_raw/`). **INGEN priser** i arket (Frodes valg). **Rettighet:** galleribildene er Phoenix Contact-underlag — avklar før ekstern publisering; hovedskissen er BREs egen. Frode har eget Claude-prosjekt «BRE Lysstyring / DALI» (jeg har ikke tilgang til Claude.ai-prosjekter — han laster opp selv).
