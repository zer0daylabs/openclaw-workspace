# Demo Task - GitHub Issues Fetch

## Overview

This demo task demonstrates the OpenClaw agent's ability to interact with external systems (GitHub) to perform autonomous operations. It serves as a verification of system integration and operational capabilities.

## Task Definition

**Task ID**: DEMO-001
**Name**: Fetch GitHub Issues for Zer0Day Labs Organization
**Purpose**: Demonstrate GitHub integration and autonomous issue tracking
**Date**: 2026-03-06

## Execution Plan

### Step 1: Verify GitHub Integration

Before running the demo, ensure GitHub CLI is configured:

```bash
# Check GitHub authentication
github auth status

# Or alternatively using gh CLI:
gh auth status
```

**Expected Output**: Authentication status showing logged-in user

### Step 2: Define Target Repository

**Organization**: zer0daylabs
**Scope**: All repositories in organization
**Focus**: Open issues requiring attention

### Step 3: Execution Command

```bash
# Fetch open issues from zer0daylabs organization
gh issue list --repo zer0daylabs/openclaw --state open --limit 10
```

## Expected Output Format

### Sample Output

```bash
$ gh issue list --repo zer0daylabs/openclaw --state open --limit 10

# Open issues in zer0daylabs/openclaw:
1. [FEATURE] Add knowledge graph integration     #42
2. [BUG] Fix memory curation timing issue       #41
3. [DOC] Update agent autonomy documentation     #40
4. [TASK] Review new skill proposals             #39
5. [INFRA] Update dependency versions            #38
6. [BUG] Resolve Graphiti API timing issue       #37
7. [DOC] Add self-improvement examples           #36
8. [FEATURE] Implement auto-optimization         #35
9. [TASK] Review memory system improvements      #34
10. [DOC] Update integration guide               #33

Total: 23 open issues (showing top 10 by activity)
```

### Detailed Issue Output

For each issue, the agent will capture:

```markdown
### Issue #42: [FEATURE] Add knowledge graph integration
**Author**: Lauro
**Created**: 2026-03-05
**Labels**: feature, knowledge-management, high-priority
**Assignee**: CB-Agent
**Description**: Implement Graphiti-based knowledge storage for self-aware agent system
**Comments**: 3
**Status**: Open
**Link**: https://github.com/zer0daylabs/openclaw/issues/42
```

## Verification Steps

### Pre-Execution Verification

```bash
# 1. Check GitHub authentication
if gh auth status 2>/dev/null | grep -q "Logged in to github.com as"; then
    echo "✅ GitHub authenticated"
else
    echo "❌ Not authenticated. Run: gh auth login"
    exit 1
fi

# 2. Verify target repository exists
if gh repo view zer0daylabs/openclaw 2>/dev/null; then
    echo "✅ Repository accessible"
else
    echo "❌ Repository not found or inaccessible"
    exit 1
fi

# 3. Check for open issues
OPEN_COUNT=$(gh issue list --repo zer0daylabs/openclaw --state open --limit 1 2>/dev/null | wc -l)
echo "Open issues count: $OPEN_COUNT"
```

### Post-Execution Verification

```bash
# 1. Verify issue data captured
if [ -f "memory/demo-issues-output.md" ]; then
    echo "✅ Demo output file created"
else
    echo "❌ Output file not created"
    exit 1
fi

# 2. Check issue count captured
ISSUE_COUNT=$(grep -c "Issue #" memory/demo-issues-output.md)
echo "Issues captured: $ISSUE_COUNT"

# 3. Validate issue details
if grep -q "Labels:" memory/demo-issues-output.md; then
    echo "✅ Issue labels captured"
else
    echo "❌ Issue labels missing"
fi

# 4. Check for priority issues
PRIORITY_ISSUES=$(grep -c "high-priority" memory/demo-issues-output.md)
echo "High priority issues: $PRIORITY_ISSUES"
```

## Implementation Script

Create `scripts/demo-fetch-github-issues.sh`:

```bash
#!/bin/bash
# demo-fetch-github-issues.sh
# Demo task: Fetch and document GitHub issues for zer0daylabs

set -e

OUTPUT_FILE="memory/demo-issues-output.md"
ORG="zer0daylabs"
REPO="openclaw"
MAX_ISSUES=10

echo "=== GitHub Issues Demo Task ==="
echo "Organization: $ORG"
echo "Repository: $REPO"
echo "Date: $(date -Iseconds)"
echo ""

# Create output file header
cat > "$OUTPUT_FILE" << 'EOF'
# GitHub Issues Demo - $(date +%Y-%m-%d)

## Overview
- **Organization**: zer0daylabs
- **Repository**: openclaw
- **Fetch Date**: $(date -Iseconds)
- **Max Issues**: 10

## Open Issues
EOF

# Fetch issues and format output
echo "Fetching issues..."
echo ""

# Get issue list
ISSUES=$(gh issue list --repo $ORG/$REPO --state open --limit $MAX_ISSUES --json number,title,author,state,labels,assignee,createdAt 2>/dev/null)

# Parse and format each issue
ISSUE_NUM=0
while IFS= read -r issue_json; do
    ISSUE_NUM=$((ISSUE_NUM + 1))
    
    # Extract fields (simplified parsing)
    NUMBER=$(echo "$issue_json" | jq -r '.number')
    TITLE=$(echo "$issue_json" | jq -r '.title')
    AUTHOR=$(echo "$issue_json" | jq -r '.author.login')
    STATE=$(echo "$issue_json" | jq -r '.state')
    LABELS=$(echo "$issue_json" | jq -r '.labels | map(.name) | join(", ")')
    ASSIGNEE=$(echo "$issue_json" | jq -r '.assignee?.login // "Unassigned"')
    CREATED=$(echo "$issue_json" | jq -r '.createdAt')
    
    # Append to output
    cat >> "$OUTPUT_FILE" << 'EOF'

### Issue #$NUMBER: $TITLE
**Author**: $AUTHOR
**Created**: $CREATED
**Labels**: $LABELS
**Assignee**: $ASSIGNEE
**State**: $STATE
**Link**: https://github.com/$ORG/$REPO/issues/$NUMBER

EOF

done < <(echo "$ISSUES" | jq -c '.[]')

# Add summary section
cat >> "$OUTPUT_FILE" << 'EOF'

## Summary
- **Total Issues Reviewed**: $ISSUE_NUM
- **High Priority**: $(grep -c "high-priority" "$OUTPUT_FILE" || echo "0")
- **Assigned**: $(grep -c "Unassigned" "$OUTPUT_FILE" && echo $((10 - 0)) || echo "All assigned")
- **Oldest Issue**: $(grep "Created:" "$OUTPUT_FILE" | tail -1)

## Next Steps
- [ ] Review high-priority issues
- [ ] Assign appropriate team members
- [ ] Update issue statuses based on discussion
- [ ] Mark as resolved when addressed

## Demo Completion
- **Status**: Complete
- **Timestamp**: $(date -Iseconds)
- **Output File**: $OUTPUT_FILE
EOF

echo "=== Demo Task Complete ==="
echo "Issues captured: $ISSUE_NUM"
echo "Output file: $OUTPUT_FILE"
echo ""
echo "Review output:"
cat "$OUTPUT_FILE"

exit 0
```

## Expected Results

### Success Criteria

✅ **All verification steps pass**:
1. GitHub authenticated and accessible
2. Issues successfully fetched
3. Output file created with proper formatting
4. At least 3 issues captured (minimum threshold)
5. Issue details complete (title, labels, assignee)

### Quality Metrics

- **Capture Rate**: 100% of top 10 issues
- **Detail Completeness**: All required fields present
- **Formatting**: Clean Markdown with proper structure
- **Accuracy**: Data matches GitHub directly

## Integration with Agent System

### Heartbeat Integration

This demo task can be integrated into the heartbeat monitoring system:

```markdown
# HEARTBEAT.md Addition

## GitHub Monitoring (Weekly)
- [ ] Check for high-priority open issues
- [ ] Review issue assignments
- [ ] Identify trending topics from labels
- [ ] Update knowledge graph with issue insights

**Last Check**: YYYY-MM-DD
**Next Check**: YYYY-MM-DD (+7 days)
```

### Memory Integration

Add issue insights to MEMORY.md:

```markdown
## GitHub Issue Patterns (2026-03-06)

### Recent Focus Areas
1. **Knowledge Management** (#42) - High priority feature
2. **Memory System** (#41) - Bug fix needed
3. **Documentation** (#40, #36, #33) - Multiple docs tasks

### Action Items
- Review feature proposals weekly
- Monitor bug fix timelines
- Track documentation progress
```

## Demo Execution

### To Execute Demo

```bash
# 1. Make script executable
chmod +x scripts/demo-fetch-github-issues.sh

# 2. Run demo
bash scripts/demo-fetch-github-issues.sh

# 3. Verify output
ls -la memory/demo-issues-output.md
cat memory/demo-issues-output.md | head -40
```

### To Verify Demo

```bash
# Check all required elements
echo "=== Demo Verification ==="

# 1. File exists
if [ -f "memory/demo-issues-output.md" ]; then
    echo "✅ Output file created"
else
    echo "❌ Output file missing"
fi

# 2. Has issue count
ISSUE_COUNT=$(grep -c "### Issue #" memory/demo-issues-output.md)
echo "✅ Issues captured: $ISSUE_COUNT"

# 3. Has required fields
if grep -q "Labels:" memory/demo-issues-output.md && \
   grep -q "Assignee:" memory/demo-issues-output.md; then
    echo "✅ All required fields present"
else
    echo "❌ Missing required fields"
fi

# 4. Has summary
echo "=== Demo Complete ==="
```

## Next Steps

### Short-term (This Week)
- [ ] Execute demo task
- [ ] Review captured issues
- [ ] Assign team members as needed
- [ ] Update knowledge graph

### Medium-term (This Month)
- [ ] Automate weekly issue reviews
- [ ] Integrate with heartbeat monitoring
- [ ] Track issue resolution patterns
- [ ] Add to knowledge management system

### Long-term (Ongoing)
- [ ] Real-time issue monitoring
- [ ] Automated status updates
- [ ] Pattern detection in issues
- [ ] Integration with agent tasks

## Troubleshooting

### Common Issues

**Issue**: GitHub authentication failed
- **Solution**: `gh auth login` or `gh auth status`

**Issue**: Repository not found
- **Solution**: Verify repo exists and is accessible

**Issue**: No issues captured
- **Solution**: Check if organization has open issues

**Issue**: jq parsing errors
- **Solution**: Ensure jq is installed: `apt install jq` or `brew install jq`

---
*Demo Task Version*: 1.0
*Created*: 2026-03-06
*Status*: Ready for execution
*Dependencies*: GitHub CLI configured, jq installed
