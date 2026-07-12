---
name: hubspot-pipeline-steg
description: "HubSpot deal-steg (pipeline \"default\") for BRE — mapping stegnavn→intern-ID, incl. contractsent-fella"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

BRE HubSpot (hubId 147931170, EU1, valuta NOK). Deals bruker pipeline **"default"**. Steg-etiketter er IKKE lesbare via API-et (dealstage-property har externalOptions=tom, ingen pipeline-ressurs). Kartlagt via eksempel-deals 2026-07-07:

- **`presentationscheduled` = «Tilbud sendt»** ✅ (bekreftet: «Foodman – Datafangst og visualisering» lå her). Åpent steg. Bruk DENNE når noe skal settes til tilbud sendt.
- **`contractsent` = ⚠️ et CLOSED WON-steg** hos BRE (ikke «kontrakt sendt»!). Å sette dealstage=contractsent markerer dealen som **vunnet** med lukkedato. IKKE bruk for «tilbud sendt».
- `qualifiedtobuy` = åpent tidlig-steg.
- `closedlost` = tapt.
- Egendefinerte tallsteg: `4973680889` (mest brukt — Automasjonskap/Redox/Quartz/Diakonhjemmet), `4973840579` (Foodman Løklinje/Infoskjermer). Etiketter ukjent — spør Frode ved behov.

Ny deal opprettes uten dealstage → havner i default første steg. Sett steg eksplisitt etterpå. Ved feil Won: sett tilbake til åpent steg + nullstill `closedate` (send "" ) for å fjerne lukkedato-rest.

Se også [[salg-pipeline]].
