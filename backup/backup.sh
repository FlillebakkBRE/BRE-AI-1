#!/bin/bash
# backup/backup.sh — Spor 1 backup av "hele løsningen" (uten hemmeligheter) til privat GitHub.
# Regenererer redigert config, kopierer memory-notater + persona, committer og pusher.
set -euo pipefail

WS="$HOME/.openclaw/workspace"
MEM="$HOME/.claude/projects/-Users-breai1--openclaw-workspace/memory"
cd "$WS"

mkdir -p backup/memory

# 1) Redigert config (hemmeligheter fjernet)
python3 backup/redact.py "$HOME/.openclaw/openclaw.json" > backup/openclaw.redacted.json

# 2) Memory-notater (kunnskap/persona-hukommelse)
if [ -d "$MEM" ]; then
  rm -f backup/memory/*.md 2>/dev/null || true
  cp "$MEM"/*.md backup/memory/ 2>/dev/null || true
fi

# 3) Sikkerhetsnett: avbryt hvis en kjent hemmelighet skulle dukke opp i det som skal committes
if grep -rIlE "BSA3ZX52|-----BEGIN (RSA|OPENSSH|EC) PRIVATE|ssh-ed25519 AAAA" backup/ --exclude=backup.sh 2>/dev/null | grep -q .; then
  echo "ADVARSEL: mulig hemmelighet i backup/ — avbryter push" >&2
  exit 1
fi

# 4) Commit kun det trygge settet
git add insider-radar lead-radar backup \
        AGENTS.md SOUL.md USER.md TOOLS.md IDENTITY.md HEARTBEAT.md 2>/dev/null || true

if git diff --cached --quiet; then
  echo "ingen endringer — hopper over commit"
else
  git commit -q -m "Backup-snapshot $(date +%F): config (redigert) + memory + persona + skript"
  echo "committet"
fi

git push -q origin main && echo "pushet til origin/main"
