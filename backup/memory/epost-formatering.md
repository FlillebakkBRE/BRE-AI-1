---
name: epost-formatering
description: Alle e-postkladder skal ha ordentlig struktur (avsnitt/linjeskift/punktlister) — aldri komprimert til én linje
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

Alle e-poster/kladder jeg lager for Frode skal ha **ryddig struktur**: egne avsnitt, linjeskift, og punktlister der det passer. Aldri komprimert til én lang linje.

**Why:** Frode påpekte 2026-07-06 at både SHM-svaret og Kjell Ove-svaret ble komprimert/lite ryddig. Han vil ha samme pene struktur på ALLE e-poster fremover.

**How to apply (teknisk):** O365-verktøyenes `Comment`-parameter (create-reply-draft / create-reply-all-draft) flater ut linjeskift til én linje. Derfor: opprett kladden, og **sett deretter kroppen med `update-mail-message` som `contentType: html`** — med `<p>`-avsnitt, `<br>` og `<ul><li>` der relevant, og behold den siterte originaltråden under en `<hr>` (Fra/Sendt/Til/Kopi/Emne + original tekst). Referanse-eksempel: SHM-svaret «RE: Forecast -skapbygging 2026/2027» (pent formatert). **Standard e-postsignatur (Frode 2026-07-07 — bruk denne på alle kladder):**
```
Frode Lillebakk | CEO
M: +47 469 14 750
E : frode.lillebakk@bredigital.no
W: www.bredigital.no
Eidetorget 1
6490 Eide
```
I HTML: hver linje med `<br>`. Kan innledes med «Med vennlig hilsen,» over blokka. NB: Outlook kan legge på egen signatur ved åpning — hvis dobbel, er den manuelt satte overflødig.

**Vedlegg til kladd — AUTOMATISK (verifisert 2026-07-07):** `add-mail-attachment` krever base64 inline (upraktisk for store filer). Bruk i stedet: (1) `create-mail-attachment-upload-session` med `{AttachmentItem:{attachmentType:"file", name, size, contentType}}` → returnerer ferdig-autentisert `uploadUrl` (embedded authtoken, gyldig ~3t). (2) Last opp bytene med `curl -X PUT "<uploadUrl>" -H "Content-Length: <sz>" -H "Content-Range: bytes 0-<sz-1>/<sz>" -H "Content-Type: <mime>" --data-binary @fil`. HTTP 201 = ferdig. Funker også for filer <3 MB (ikke bare 3–150 MB). Ingen Graph-token trengs i shell — uploadUrl er selvautentiserende. Verifiser med hasAttachments=true. Slik slipper Frode manuell dra-og-slipp.
