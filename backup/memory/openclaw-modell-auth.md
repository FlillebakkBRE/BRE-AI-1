---
name: openclaw-modell-auth
description: Modell-auth byttet fra Claude-abonnement (OAuth) til Anthropic API-nøkkel 2026-08-03 for å fikse at cron/morgenbrief feilet headless
metadata: 
  node_type: memory
  type: project
  originSessionId: ae7cfad3-0a0c-47a5-9b81-f26ae0cdf38e
---

**Problem (2026-08-03):** Planlagte cron-jobber (morgenbrief 07:00 m.fl.) feilet hver morgen med «login expired», mens interaktiv chat alltid virket. Rotårsak: `anthropic:claude-cli` var en kortlivet OAuth-token (~8t) fra Claude-abonnementet — den fornyes kun ved interaksjon, ikke headless. Utløp om natta → morgen-cron traff utløpt token.

**LØST:** Byttet til Anthropic **API-nøkkel** (utløper aldri).
- Ny auth-profil `anthropic:api` (api_key) lagt inn via `openclaw models auth paste-api-key`.
- Order-override satt: `openclaw models auth order set --provider anthropic anthropic:api` → API-nøkkel foretrekkes.
- Default-modell er `anthropic/claude-opus-4-8` (uendret) → cron bruker denne → nå API-nøkkel.
- `anthropic:claude-cli` OAuth-profilen ligger urørt som fallback.
- **Verifisert 2026-08-03:** `openclaw infer model run` både lokalt og via `--gateway` → status 200 mot api.anthropic.com. Cron-pathen (gateway) bekreftet.

**Kostnad:** Går fra gratis abonnement til metered API-betaling (per token). Frode aksepterte dette bevisst for stabil 24/7-drift.

**Merk:** API-nøkkelen ble limt inn i chatten (Telegram-transcript) under oppsett — vurder rotasjon på console.anthropic.com hvis eksponering i chat-historikk er en bekymring. Se [[openclaw-stabilitet]].
