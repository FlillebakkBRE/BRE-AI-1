---
name: git-backup
description: Workspace-skript backes opp til privat GitHub-repo via SSH deploy key
metadata: 
  node_type: memory
  type: reference
  originSessionId: 96ba557a-abbb-400d-8f36-e8ba50c62760
---

Satt opp 2026-07-05. Radar-skriptene ([[insider-radar]], [[lead-radar-doffin]]) i workspace er versjonert i git og pushes til privat GitHub-repo for off-site backup.

- **Remote:** `origin` = `git@github-bre:FlillebakkBRE/BRE-AI-1.git` (privat repo, Frodes GitHub-bruker FlillebakkBRE)
- **Auth:** SSH deploy key (write) — privat nøkkel `~/.ssh/id_ed25519_bre_backup`, host-alias `github-bre` i `~/.ssh/config` (IdentitiesOnly). Nøkkelen gir kun tilgang til dette ene repoet.
- **Push:** `cd ~/.openclaw/workspace && git push` (main tracker origin/main). Kun kode + `.gitignore` er sporet; genererte data (`insider-radar/data/`, `seen*.json`) er ignorert. Ingen hemmeligheter i repoet (Brave-nøkkel bor i OpenClaw-config).
- **Rutine:** push manuelt etter endringer i radar-skriptene så backupen holdes fersk.

**Spor 1 — full løsnings-backup (satt opp 2026-07-05):** Repoet inneholder nå hele løsningen UTEN hemmeligheter:
- `backup/openclaw.redacted.json` — hele configen med hemmeligheter erstattet av `<REDACTED>` (generert av `backup/redact.py`)
- `backup/cron-jobs.json` — eksport av cron-definisjonene (morgenbrief + insider-radar); OBS må re-eksporteres manuelt når en cron endres (crons bor i state/openclaw.sqlite, ikke i openclaw.json)
- `backup/memory/*.md` — kopi av memory-notatene
- persona: AGENTS/SOUL/USER/TOOLS/IDENTITY/HEARTBEAT.md
- `backup/RESTORE.md` — gjenopprettings-runbook (hvor hemmeligheter hører hjemme + hvordan skaffe på nytt)
- `backup/backup.sh` — regenererer redigert config + kopierer memory + committer + pusher; har sikkerhetsnett som avbryter hvis en hemmelighet dukker opp i backup/
- **Automatikk:** cron `e2a6cdf2-6d36-4d82-ad01-4ac923c6f8dc` «Ukentlig backup (Spor 1)» — søndager 03:00, systemEvent til main (som har exec), kjører backup.sh, stille med mindre noe feiler.
- **Spor 2 (kryptert hemmelighets-backup): IKKE satt opp** — venter på at Frode vil ha det (krever passordfrase).

