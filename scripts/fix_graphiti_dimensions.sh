#!/bin/bash
# Fix Graphiti Neo4j embedding dimension mismatch
# This script queries Neo4j to find vector properties with different dimensions
# and creates a script to fix or remove them

set -e

DOCKER_NAME="neo4j-graphiti"
NEO4J_USER="neo4j"
NEO4J_PASS="testpassword"
NEO4J_PORT="7474"

# Get list of entities with vector properties
QUERY="MATCH (n {has_embedding: true}) WITH n, n.embedding as vec RETURN labels(n)[0] as type, size(vec) as dimensions, count(*) as count GROUP BY type, dimensions ORDER BY dimensions"

# Check if the graphiti service is responding
GRAPHTI_URL="http://localhost:8001"

if curl -sf "$GRAPHTI_URL/health" >/dev/null 2>&1; then
  echo "✅ Graphiti API is responding"
else
  echo "❌ Graphiti API is NOT responding"
  echo "Attempting to diagnose..."
  
  # Get recent error logs
  echo ""
  echo "Recent Graphiti errors:"
  docker logs graphiti --tail 50 2>/dev/null | grep -i "error\|exception\|dimension" || echo "No recent errors found"
  
  echo ""
  echo "Next steps to fix:"
  echo "1. Stop Graphiti: docker stop graphiti"
  echo "2. Wipe Neo4j database: docker exec $DOCKER_NAME neo4j-admin dbms set-initial-password <newpassword>"
  echo "3. Restart Graphiti: docker restart graphiti"
  echo "4. Re-add important facts from memory files"
  exit 1
fi
