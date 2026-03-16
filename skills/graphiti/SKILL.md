---
name: graphiti
description: Knowledge graph operations via Graphiti API. Search facts, add episodes, and extract entities/relationships.
homepage: https://github.com/getzep/graphiti
metadata: {"clawdbot":{"emoji":"🕸️","requires":{"services":["neo4j","qdrant","graphiti"]},"install":[{"id":"docker","kind":"docker-compose","label":"Install Graphiti stack (Docker)"}]}}
---

# Graphiti Knowledge Graph

Query and manage your knowledge graph using Graphiti's REST API with dynamic service discovery.

## Prerequisites

- Neo4j database (graph storage)
- Qdrant (vector search)
- Graphiti service running (default: http://localhost:8001)

## Tools

### graphiti_search
Search the knowledge graph for relevant facts.

**Usage:**
```bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/search" \
  -H 'Content-Type: application/json' \
  -d '{"query": "YOUR_QUERY", "max_facts": 10}' | jq .
```

### graphiti_add
Add a new episode/memory to the knowledge graph.

**Usage:**
```bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/messages" \
  -H 'Content-Type: application/json' \
  -d '{"group_id": "ZER0DAY", "messages": [{"role": "user", "role_type": "user", "content": "EPISODE_CONTENT"}]}' | jq .
```

### graphiti_list_episodes
List episodes for a group.

**Usage:**
```bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -sf "$GRAPHITI_URL/episodes/ZER0DAY?last_n=10" | jq .
```

### graphiti_entity_node
Add an entity node to the knowledge graph.

**Usage:**
```bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/entity-node" \
  -H 'Content-Type: application/json' \
  -d '{"name": "Node Name", "type": "category", "description": "Description"}' | jq .
```

## Dynamic Configuration

The skill uses environment discovery to find Graphiti automatically:

1. **Clawdbot config**: `clawdbot config get skills.graphiti.baseUrl`
2. **Environment variable**: `$GRAPHITI_URL`
3. **Default fallback**: `http://localhost:8001`

To change the Graphiti URL:
```bash
export GRAPHITI_URL="http://10.0.0.10:8001"
# OR
clawdbot config set skills.graphiti.baseUrl "http://10.0.0.10:8001"
```

## Examples

Search for information:
```bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/search" \
  -H 'Content-Type: application/json' \
  -d '{"query": "Zer0Day Labs", "max_facts": 5}'
```

Add a memory:
```bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/messages" \
  -H 'Content-Type: application/json' \
  -d '{"group_id": "ZER0DAY", "messages": [{"role": "user", "role_type": "user", "content": "Project Update: Completed Phase 1 of Clawdbot integration"}]}'
```

List episodes:
```bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -sf "$GRAPHITI_URL/episodes/ZER0DAY?last_n=10"
```

Add entity node:
```bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/entity-node" \
  -H 'Content-Type: application/json' \
  -d '{"name": "OpenClaw", "type": "system", "description": "AI agent framework for Zer0Day Labs"}'
```

## Endpoint Details

### Search
- **URL**: `/search`
- **Method**: POST
- **Body**: `{"query": "string", "max_facts": 10}`
- **Returns**: `{"facts": [...]}`

### Add Episode
- **URL**: `/messages`
- **Method**: POST
- **Body**: `{"group_id": "string", "messages": [{"role": "user", "role_type": "user", "content": "string"}]}`
- **Returns**: `{"message": "Messages added to processing queue", "success": true}`

### List Episodes
- **URL**: `/episodes/{group_id}`
- **Method**: GET
- **Params**: `last_n=10`
- **Returns**: Episodes list

### Add Entity Node
- **URL**: `/entity-node`
- **Method**: POST
- **Body**: `{"name": "string", "type": "string", "description": "string"}`
- **Returns**: Node UUID and status

## Valid Role Types
- `user` - User input
- `assistant` - AI response
- `system` - System instructions

## Group ID Convention
Use organization/project identifier as group_id:
- `ZER0DAY` - Zer0Day Labs data
- `TEAM` - Team collaboration
- `PERSONAL` - Personal notes

---
*Updated*: 2026-03-07 01:30 MST
*Status*: All endpoints verified operational ✅
