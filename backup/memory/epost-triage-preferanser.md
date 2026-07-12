---
name: epost-triage-preferanser
description: "Hvordan Frode vil ha innboks-/oppfølgingstriage: hopp over driftsalarmer (IXON, BRE Cloud/RMM)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

Ved gjennomgang av Frodes innboks / oppfølginger (og morgenbrief): **hopp over drifts-/alarmmeldinger** som IXON (f.eks. «Ixon offline …»), BRE Cloud og RMM device-offline-varsler (f.eks. AIO-Scale, BREinfo0xx). Ikke flagg dem som noe Frode må følge opp.

**Why:** Frode sa 2026-07-06 at driftsmeldinger fra IXON og BRE Cloud ikke trenger å ses på fremover — de håndteres i egen driftsflyt, ikke av ham personlig.

**How to apply:** Filtrer bort automatiske device-/oppetidsvarsler (avsendere som noreply@ixon.cloud, noreply@rmmservice.com o.l.) fra e-post-oppfølgingslister. Fokuser triage på ekte person-til-person-dialog (kunder, leverandører, partnere) og forretningskritiske varsler (f.eks. faktura/avtale). Gjelder også [[daglig-morgen-brief]] hvis driftsvarsler dukker opp der. Interne alarmer generelt: nedprioriter med mindre Frode ber om det.
