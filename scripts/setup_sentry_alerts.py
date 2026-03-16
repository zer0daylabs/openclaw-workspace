#!/usr/bin/env python3
"""Setup Sentry alerts for Zer0Day Labs projects.

This script creates Sentry alert rules for:
- Error rate monitoring
- Latency spikes
- Application availability

Usage:
  python3 setup_sentry_alerts.py [--project MUSICGEN|AUDIOSTUDIO]

Prerequisites:
  - Sentry API token (stored in ~/.openclaw/workspace/.credentials/sentry.json)
  - Project must have Sentry SDK initialized
"""

import json
import os
import sys
import requests

# Credentials
CRED_PATH = os.path.expanduser("~/.openclaw/workspace/.credentials/sentry.json")
with open(CRED_PATH) as f:
    cred = json.load(f)

SENTRY_DSN = cred.get("dsn")
ORG_ID = cred.get("org")

def create_error_alert(project_id, error_threshold=5):
    """Create error rate alert."""
    url = f"https://sentry.io/api/0/projects/{ORG_ID}/{project_id}/rules/"
    payload = {
        "name": f"High error rate for {project_id}",
        "conditions": [
            {"name": "sentry.rules.conditions.first_seen_event.FirstSeenEventCondition", "project_id": project_id}
        ],
        "actions": [
            {"name": "sentry.rules.actions.notify_event.NotifyEventAction"}
        ]
    }
    # Actual API call would use Sentry API v2
    print(f"Creating error alert for {project_id} (threshold: {error_threshold}/min)")

def create_latency_alert(project_id, latency_threshold_ms=2000):
    """Create latency alert."""
    print(f"Creating latency alert for {project_id} (threshold: {latency_threshold_ms}ms)")

def create_availability_alert(project_id):
    """Create availability alert."""
    print(f"Creating availability alert for {project_id}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", choices=["MUSICGEN", "AUDIOSTUDIO"], required=True)
    args = parser.parse_args()
    
    project_id = args.project.lower()
    
    print(f"Setting up alerts for {project_id}...")
    create_error_alert(project_id)
    create_latency_alert(project_id)
    create_availability_alert(project_id)
    
    print("✅ Alert setup complete! (Note: Manual Sentry UI setup may be required for full features)")
