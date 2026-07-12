---
name: tilbud-maler
description: "BRE Digital tilbudsmaler — tre modeller (dagrate/BOM/enhetspris+abo) fra Foodman-tilbud, underlag for tilbuds-generator"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

Frode sendte 2026-07-05 fire Foodman-tilbud som underlag for fremtidige tilbudsmaler. Lagret i `workspace/tilbud-maler/`. Tre distinkte tilbudsmodeller BRE Digital bruker:

1. **Dagrate-modell** (`01_dagrate_OT-commissioning_brevmal.docx`) — tjeneste/commissioning. Dagrate NOK 14 600/dag (8t, eks mva, reise/kost/opphold inkl.), estimerte dagsverk × rate, faktureres etter medgått tid. Har **scope-matrise** (ansvarsfordeling BRE/Kunde/Andre: Engineering / Leveranse / Tjenester på anlegg). Seksjoner 1–6: Innledning, Pris (estimert omfang + scope + dagrate), Betalingsbetingelser, Gyldighet, Fremdriftsplan, Standard salgs-/leveringsbetingelser. Matcher HubSpot-deal «Foodman – OT-skap comission».

2. **Produkt/BOM-modell** (`02_produkt-BOM_styreskap.docx`) — styreskap med full **stykkliste** (pos/antall/artikkelnr/beskrivelse/fabrikat). Typisk innhold: Rittal AX-kapsling, Phoenix Contact VL3 UPC industri-PC, Axioline-I/O, FL SWITCH, TRIO3 strømforsyning. Seksjoner: Innledning, Leveranseomfang, Stykkliste (BOM). Sendt til Tolcon (mellomledd/partner).

3. **Enhetspris + abonnement** (`03_enhetspris-abonnement_datafangst.docx`) — SaaS/datafangst. Standard 15 000 kr/enhet, 30 % volumrabatt ved 200 enheter → 10 500 kr/enhet = 2,1 MNOK engangs. Løpende BRE Cloud-abo 99 kr/enhet/mnd (200 → 19 800/mnd = 237 600/år). IEC 62443/NIS2, BRE Site Server + redundant fiberring, InfluxDB + Grafana. Matcher deal «Foodman – Datafangst og visualisering» (2,1 MNOK).

**Felles standardelementer (til generator):**
- Topp-blokk: kunde + kontaktpersoner, tilbudsnr (f.eks. 191068), dato, tilbudsfrist/gyldighet (30 dager), BRE-kontakt = Frode Lillebakk / frode.lillebakk@bredigital.no.
- Betalingsbetingelser (datafangst): 30 % ved bestilling, 60 % ved ferdig installasjon, 10 % ved godkjent idriftsettelse, netto 14 dager. Abo forskuddsvis pr. kvartal, 12 mnd binding.
- Standard forbehold: alle priser eks. mva; montasje ofte av andre (Laukas/kunde); grensesnitt avklares i oppstartsmøte.

**✅ Generator-mekanisme funker (2026-07-05):** python-docx (installert i ~/Library/Python/3.9) genererer tilbud i BRE-mal. NB: python-docx nekter å åpne `.dotx` direkte — brevmalen ble konvertert til `brand/_brevmal_as_docx.docx` (byttet content-type template.main→document.main i [Content_Types].xml); åpne DEN som template. Header/footer/logo (word/media image1+2 + footer1) og BRE-font bevares. Malen mangler «Table Grid»-stil → sett tabellkanter manuelt via w:tblBorders. Skript-eksempler i `workspace/tilbud-maler/`: gen_dragen.py (tilbud fra bunn), add_komm.py (sett inn seksjon i eksisterende docx via ref._p.addprevious), gen_vedlegg.py (Modbus-vedlegg). Første ekte leveranse: Drågen Smokehouse desinfiseringsanlegg (Tilbud_Dragen_Smokehouse_UTKAST_v2.docx + Vedlegg_A_Modbus_registerkart_UTKAST.docx).

**Prisregler (Frode 2026-07-06 — gjelder alle tilbud):**
- **Materiell:** kostpris + 15 % påslag.
- **Installasjon:** etter medgått tid, timesats **kr 970,-/time** (eks. mva.).
- **BRE Cloud (SaaS):** **kr 599,-/mnd** (7 188,-/år), **ingen bindingstid** (NB: eldre datafangst-mal hadde 99 kr/enhet/mnd + 12 mnd binding — dette er standard SaaS-linje for mindre anlegg).
- **Betalingsplan:** droppes for prosjekt **under kr 100 000** (da ingen 30/60/10-plan). Over 100k: bruk 30 % bestilling / 60 % installasjon / 10 % idriftsettelse.
- Struktur: samle ALL pris under kap. «4. Pris» (Frode foretrekker det ryddig).

**Drågen Smokehouse (levende eksempel):** siste versjon `Tilbud_Dragen_Smokehouse_UTKAST_v11.docx`. Prosess-/leveranseskisse `prosess_dragen.png/.svg` (fargekodet: grå=eksisterende pH+pumpe+ventil, blå=BRE styreskap/PLS+signalintegrasjon+ventilstyring 24VAC, gul=opsjon nivåmåler), generert via rsvg-convert (librsvg). Byggeskript `upd_tilbud_kap4.py`. Beløp 35k (deal closedwon).

**Åpne spørsmål til Frode før tilbuds-generator bygges (del av [[salg-pipeline]] roadmap #3):** (1) er disse 3 malene representative/komplette? (2) output som .docx eller Outlook-kladd m/vedlegg? (3) finnes fast logo/brevmal-fil (header/footer) som skal brukes?
