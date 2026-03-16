# Graphiti Knowledge Graph Fix

**Date:** 2026-03-15  
**Issue:** Neo4j embedding dimension mismatch causing search failures  
**Status:** REQUIRES MANUAL INTERVENTION

---

## Problem Analysis

**Root Cause:**
The Neo4j database has vector embeddings with different dimensions (likely 512 vs 768), causing Graphiti's vector similarity search to fail with:

```
Neo.ClientError.Statement.ArgumentError: Invalid input for 'vector.similarity.cosine()': 
The supplied vectors do not have the same number of dimensions.
```

**Why This Happened:**
- Graphiti uses BERT-based embeddings for knowledge graphs
- Different BERT models produce different vector dimensions (BERT-base=512, BERT-large=768)
- Some facts were likely added with one model version, others with another
- The graph now contains mixed-dimension vectors, making similarity search impossible

**Impact:**
- ❌ Search endpoint fails (Internal Server Error)
- ❌ Cannot query knowledge graph programmatically
- ✅ Episodes listing still works (doesn't use vectors)
- ✅ Adding new messages works (queued for processing)

---

## Solution Options

### Option 1: Wipe and Rebuild (RECOMMENDED) ⭐
**Pros:**
- Clean slate, no dimension mismatches
- Fresh start with consistent embeddings
- Quick to implement

**Cons:**
- Loses historical data (facts from Mar 6-15)
- Need to re-add important facts manually

**Estimated Time:** 15-20 minutes

### Option 2: Partial Recovery (Complex)
**Pros:**
- Retains some historical data

**Cons:**
- Requires complex Neo4j queries
- Uncertain success rate
- May leave orphaned nodes/edges
- Time-consuming to implement

**Estimated Time:** 2-4 hours

### Option 3: Continue with Workaround (Temporary)
**Pros:**
- No data loss
- Can still add new facts

**Cons:**
- Search will continue to fail
- Cannot leverage historical knowledge
- Technical debt accumulates

**Estimated Time:** Ongoing maintenance

---

## Recommended: Option 1 - Wipe and Rebuild

### Step 1: Backup Important Facts (5 min)
Extract all important knowledge from current state:

```bash
# List all ZER0DAY episodes
curl -sf "http://localhost:8001/episodes/ZER0DAY?last_n=100" > /tmp/graphiti_backup.json

# Extract important lessons from daily logs
cat ~/.openclaw/workspace/memory/*.md | grep -E "^\*|^- (Lesson|Decision|Milestone):" > /tmp/facts.txt

# Extract important decisions from MEMORY.md
cat ~/.openclaw/workspace/memory/MEMORY.md | grep -E "^\d+\.|^##|^---" > /tmp/decisions.txt
```

### Step 2: Stop and Wipe Neo4j (2 min)

```bash
# Stop Graphiti service
docker stop graphiti

# Wipe Neo4j database
docker exec neo4j-graphiti neo4j-admin db clear

# Start Graphiti service
docker start graphiti
```

### Step 3: Re-add Important Facts (5 min)
Add the most critical facts from backups:

```bash
# Add lessons learned
curl -s -X POST "http://localhost:8001/messages" \
  -H "Content-Type: application/json" \
  -d '{"group_id": "ZER0DAY", "messages": [{"role": "user", "role_type": "user", "content": "Lesson: Never keep mental notes, always write to files for session continuity"}]}'

curl -s -X POST "http://localhost:8001/messages" \
  -H "Content-Type: application/json" \
  -d '{"group_id": "ZER0DAY", "messages": [{"role": "user", "role_type": "user", "content": "Lesson: Resourceful before asking - try to figure it out before requesting help"}]}'

curl -s -X POST "http://localhost:8001/messages" \
  -H "Content-Type: application/json" \
  -d '{"group_id": "ZER0DAY", "messages": [{"role": "user", "role_type": "user", "content": "Lesson: Quality > quantity in group chats - one thoughtful response beats three fragments"}]}'

# Add decision records
curl -s -X POST "http://localhost:8001/messages" \
  -H "Content-Type: application/json" \
  -d '{"group_id": "ZER0DAY", "messages": [{"role": "user", "role_type": "user", "content": "Decision 2026-03-06: Implemented heartbeat batching pattern to reduce API calls by 60%. Instead of separate cron jobs, check all 2-4 times daily in single turn."}]}'
```

### Step 4: Verify Fix (3 min)

```bash
# Test search endpoint
curl -s -X POST "http://localhost:8001/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "lessons about memory management", "max_facts": 5}' | jq .

# Verify it returns results without errors
```

---

## Implementation Script

Create `scripts/fix_graphiti.sh`:

```bash
#!/bin/bash
set -e

GRAPHTI_URL="http://localhost:8001"

# Step 1: Backup current state
mkdir -p ~/.openclaw/workspace/graphiti-backup
BACKUP_DATE=$(date +%Y%m%d_%H%M)
echo "Creating backup..."
curl -sf "$GRAPHTI_URL/episodes/ZER0DAY?last_n=100" > "~/.openclaw/workspace/graphiti-backup/$BACKUP_DATE_ZER0DAY.json" || echo "No data to backup"

# Step 2: Stop and wipe
echo "Stopping Graphiti..."
docker stop graphiti 2>/dev/null || true

echo "Wiping Neo4j database..."
docker exec neo4j-graphiti neo4j-admin db clear 2>/dev/null || true

# Step 3: Restart Graphiti
echo "Restarting Graphiti..."
docker start graphiti

sleep 10

# Step 4: Re-add important facts from MEMORY.md
echo "Re-adding important facts..."

# Extract lessons from MEMORY.md
LESSONS=$(grep -E "^\d+\. " ~/.openclaw/workspace/memory/MEMORY.md | head -20 | sed 's/^\d+\. //' | sed 's/^/Lesson: /')

for lesson in $LESSONS; do
  content=$(echo "$lesson" | sed "s/'/\\'/g")
  curl -s -X POST "$GRAPHTI_URL/messages" \
    -H "Content-Type: application/json" \
    -d '{"group_id": "ZER0DAY", "messages": [{"role": "user", "role_type": "user", "content": "'$content'"}]}' \
    >/dev/null 2>&1
  sleep 1
done

# Step 5: Test search endpoint
echo "Testing search endpoint..."
result=$(curl -s -X POST "$GRAPHTI_URL/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "lessons about memory management", "max_facts": 5}' 2>&1)

if echo "$result" | grep -q "Internal Server Error"; then
  echo "❌ Search endpoint still failing"
  exit 1
else
  echo "✅ Search endpoint working!"
  echo "$result" | jq '.facts[] | .fact' | head -5
fi

echo ""
echo "Graphiti knowledge graph fix complete!"
```

---

## Risk Assessment

**Low Risk:**
- Graphiti will continue to add new messages (queued for processing)
- All agent tasks continue unaffected
- No production systems depend on Graphiti search

**Medium Risk:**
- Loss of historical knowledge graph data (facts from Mar 6-15)
- May need to re-add important facts manually

**Mitigation:**
- Backup current state before wiping
- Document critical facts from daily logs before wiping
- Re-add important lessons and decisions after wipe

---

## Execution Checklist

- [ ] Stop Graphiti service: `docker stop graphiti`
- [ ] Backup current episodes: `curl -sf "http://localhost:8001/episodes/ZER0DAY?last_n=100" > backup.json`
- [ ] Wipe Neo4j database: `docker exec neo4j-graphiti neo4j-admin db clear`
- [ ] Start Graphiti service: `docker start graphiti`
- [ ] Wait 10 seconds for service to initialize
- [ ] Re-add important facts from daily logs and MEMORY.md
- [ ] Test search endpoint: `curl -s -X POST "http://localhost:8001/search" -H "Content-Type: application/json" -d '{"query": "lessons", "max_facts": 5}'`
- [ ] Verify search returns results without errors
- [ ] Update MEMORY.md with this fix documentation

---

## Post-Fix: Important Facts to Re-add

1. **Agent Identity:** CB - Co-pilot at Zer0Day Labs, mission-oriented, trusted partner
2. **Core Truths:** Resourceful, documented, opinionated, earned trust
3. **Memory System:** Daily logs + MEMORY.md curation
4. **Agent Tools:** agent-autopilot, agent-orchestrator, task-orchestra, agent-autonomy
5. **Communication:** Slack preferred, quality over quantity, emoji reactions
6. **Security:** Local vault for API keys, never exfiltrate private data
7. **Task Management:** Never idle, always have next step, skip blocked tasks
8. **Graphiti:** Use for facts, lessons, decisions - not routine updates

---

**Author:** CB - Zer0Day Labs AI Partner  
**Status:** Ready for execution (15-20 min)
