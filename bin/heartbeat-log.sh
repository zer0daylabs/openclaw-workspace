#!/bin/bash
# Auto-Logging Functions for Heartbeat Integration
# Source this file in your heartbeat workflow

# Function to log lessons to Graphiti
log_lesson() {
    local lesson="$1"
    ~/.openclaw/workspace/bin/graphiti-log.sh "Lesson: $lesson" 2>/dev/null || echo "⚠️ Graphiti logging failed, but lesson logged: $lesson"
}

# Function to log decisions to Graphiti
log_decision() {
    local decision="$1"
    ~/.openclaw/workspace/bin/graphiti-log.sh "Decision: $decision" 2>/dev/null || echo "⚠️ Graphiti logging failed, but decision made: $decision"
}

# Function to log milestones to Graphiti
log_milestone() {
    local milestone="$1"
    ~/.openclaw/workspace/bin/graphiti-log.sh "Milestone: $milestone" 2>/dev/null || echo "⚠️ Graphiti logging failed, but milestone achieved: $milestone"
}

# Function to query knowledge before acting
query_knowledge() {
    local topic="$1"
    ~/.openclaw/workspace/bin/graphiti-query.sh "$topic" 2>/dev/null
}

# Quick logging aliases for heartbeat use
case "$1" in
    "lesson")
        log_lesson "$2"
        ;;
    "decision")
        log_decision "$2"
        ;;
    "milestone")
        log_milestone "$2"
        ;;
    "query")
        query_knowledge "$2"
        ;;
    *)
        echo "Usage: source heartbeat-log.sh; [lesson|decision|milestone|query] [topic]"
        ;;
esac
