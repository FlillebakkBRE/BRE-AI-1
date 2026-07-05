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
