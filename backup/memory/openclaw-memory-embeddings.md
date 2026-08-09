---
name: openclaw-memory-embeddings
description: "Minnesøk-embeddings: lokal Ollama (nomic-embed-text) + extraPaths-bro til Claude-minnestien; fikset 2026-08-03"
metadata: 
  node_type: memory
  type: project
  originSessionId: ad389e59-7604-4056-87d7-0ca39a783b1f
  modified: 2026-08-03T16:38:54.405Z
---

Fikset 2026-08-03: semantisk `memory_search` var pauset («index metadata missing»). To rotårsaker funnet og løst:

1. **Embedding-provider:** default var OpenAI, men da vi la om modell-auth til ren Anthropic-nøkkel ([[openclaw-modell-auth]]) forsvant OpenAI-nøkkelen → CLI feilet ved oppstart («No API key found for provider openai»). Løst ved å bytte til **lokal Ollama** — passer [[data-handling-prinsipp]] (minneinnhold forlater ikke maskinen, ingen API-kost). Modell: `nomic-embed-text` (hentet via `ollama pull`). Config: `agents.defaults.memorySearch.provider="ollama"`, `model="nomic-embed-text"` i `~/.openclaw/openclaw.json`.

2. **To frakoblede minne-lagre (viktig):** OpenClaws innebygde indeks ser i `~/.openclaw/workspace/memory` (fantes ikke), mens de faktiske 21 notatene ligger i Claude Code sitt lager: `~/.claude/projects/-Users-breai1--openclaw-workspace/memory/`. Symlink funker IKKE — builtin-indekseren hopper over symlinker (bekreftet i docs). Løst med **`memorySearch.extraPaths`** som peker absolutt på Claude-minnestien. Resultat: 21/21 filer · 63 chunks indeksert, søk gir treff (score ~0.76).

**Reindeksering ved endring:** `openclaw memory index --force --agent main`. **Status:** `openclaw memory status`.

Gjenstår (kosmetisk): doctor/status viser fortsatt «memory directory missing (~/.openclaw/workspace/memory)» — ufarlig, extraPaths bærer indekseringen. Kan lukkes ved å lage en tom workspace/memory-mappe hvis ønskelig.

Config-backup tatt før endring: `~/.openclaw/openclaw.json.bak-20260803-183509`.
