---
name: diakonhjemmet-mcp
description: "Diakonhjemmet MCP — BRE Cloud InfluxDB tidsserie-kilde (kunde-IoT), OAuth, 3+ verktøy"
metadata: 
  node_type: memory
  type: project
  originSessionId: 7598b5ee-a839-4a70-8f7f-6da31ab876bf
---

Diakonhjemmet MCP — egen BRE Cloud-tjeneste, IKKE åpen data.
- **URL:** `https://mcp.diakonhjemmet.brecloud.no/mcp` · transport streamable-http · auth OAuth (scope `mcp:access offline_access`). Config i openclaw.json under `mcp.servers.diakonhjemmet`. OAuth-token: `~/.openclaw/mcp-oauth/diakonhjemmet-*.json`.
- **Hva den er:** grensesnitt mot en **InfluxDB** (tidsseriedata) — sannsynligvis IoT-/sensordata fra BRE-installasjon hos kunden Diakonhjemmet. Ekte kundedata, ikke offentlig.
- **Verktøy:** `diakonhjemmet__query_influx` (spør InfluxDB), `diakonhjemmet__describe_schema` (measurements/felter), `diakonhjemmet__resources_list`, `diakonhjemmet__resources_read`, `diakonhjemmet__whoami`.
- **Hendelse 2026-07-06 (natt):** var konfigurert men manglet i aktiv MCP-liste i økten. `openclaw mcp doctor` = ok, `openclaw mcp probe diakonhjemmet` = 3 tools + resources (OAuth funker). Root cause: ikke lastet i kjørende runtime → fikset med `openclaw mcp reload` (tar effekt ved neste runtime-bygg). Token-fila så tom ut ved rask inspeksjon (kun state/codeVerifier), men probe beviste at auth virker — så ikke stol blindt på token-fil-innhold; bruk `probe` for sannhet.
- **Nyttige CLI:** `openclaw mcp probe <navn> [--json]`, `openclaw mcp reload`, `openclaw mcp login <navn>`, `openclaw mcp list`, `openclaw mcp doctor`.
