# RESTORE — gjenoppbygging av BRE AI-løsningen

Dette repoet er **Spor 1**-backup: all logikk og kunnskap, men **ingen hemmeligheter**
(de er bevisst holdt ute). Med denne runbooken kan hele løsningen gjenreises.

## Hva som ligger her
- `insider-radar/` — Oslo Børs innsidehandel-radar (fetch.py, watchlist.json)
- `lead-radar/` — Doffin IoT-lead-radar (doffin.py)
- `backup/openclaw.redacted.json` — hele OpenClaw-configen med hemmeligheter = `<REDACTED>`
- `backup/cron-jobs.json` — cron-definisjoner (morgenbrief 07:00, insider-radar 07:10)
- `backup/memory/` — assistentens langtidshukommelse (MEMORY.md + notater)
- `AGENTS.md / SOUL.md / USER.md / TOOLS.md / IDENTITY.md / HEARTBEAT.md` — persona/oppsett

## Hva som IKKE ligger her (må skaffes på nytt ved gjenoppretting)
| Hemmelighet | Hvor den hører hjemme | Hvordan skaffe på nytt |
|---|---|---|
| Brave Search API-nøkkel | `tools.web.search` i openclaw.json | brave.com/search/api → ny nøkkel |
| HubSpot OAuth | `mcp.servers.hubspot` / mcp-oauth | `openclaw mcp login hubspot` |
| Diakonhjemmet OAuth | `~/.openclaw/mcp-oauth/` | `openclaw mcp login diakonhjemmet` |
| Telegram-paring | `~/.openclaw/credentials/` | par bot på nytt via OpenClaw |
| SSH deploy key | `~/.ssh/id_ed25519_bre_backup` | ny nøkkel + legg til som deploy key på GitHub (se [[git-backup]]) |

## Gjenopprettingssteg
1. **Installer OpenClaw** på ny maskin (se docs.openclaw.ai).
2. **Config:** kopier `backup/openclaw.redacted.json` → `~/.openclaw/openclaw.json`, og fyll inn de `<REDACTED>`-verdiene (Brave-nøkkel, tokens) på nytt.
3. **Skript:** klon dette repoet inn i `~/.openclaw/workspace/` (insider-radar/ + lead-radar/ ligger klare). Genererte data (`data/`, `seen*.json`) bygges opp av seg selv ved neste kjøring.
4. **Cron:** gjenopprett de to jobbene fra `backup/cron-jobs.json` med cron-verktøyet (`action=add`). Merk: den *kanoniske* fulle payloaden ligger i live-jobben; JSON-en her er et fyldig sammendrag som virker, men sjekk mot behov.
5. **MCP-innlogging:** `openclaw mcp login hubspot` (+ diakonhjemmet når den er oppe).
6. **Memory:** kopier `backup/memory/*.md` → `~/.claude/projects/-Users-breai1--openclaw-workspace/memory/`.
7. **Verifiser:** kjør begge radar-skriptene manuelt, og `cron run` for å teste briefene.

## Automatikk
`backup/backup.sh` regenererer redigert config + kopierer memory + committer + pusher.
Kjøres ukentlig av en OpenClaw cron-jobb (isolert). Sikkerhetsnett i skriptet avbryter
push hvis en kjent hemmelighet skulle dukke opp i `backup/`.

## Full katastrofe-backup (Spor 2 — ikke satt opp ennå)
For backup *med* hemmeligheter: kryptert snapshot av `~/.openclaw/openclaw.json`,
`~/.openclaw/credentials/`, `~/.openclaw/mcp-oauth/` og `~/.ssh/id_ed25519_bre_backup`
med en passordfrase Frode eier. Be assistenten sette dette opp ved behov.
