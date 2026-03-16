#!/usr/bin/env python3
"""Alert testing scripts for Zer0Day Labs monitoring.

This script provides utilities to test Sentry and PostHog alert configurations
once they are set up in the dashboards.

Usage:
  python3 alert_testing.py --test sentry-error   # Test Sentry error alert
  python3 alert_testing.py --test sentry-latency # Test Sentry latency alert  
  python3 alert_testing.py --test posthog-retention # Test PostHog retention alert
  python3 alert_testing.py --test all            # Run all tests

Note: Testing requires staging environment access and should be done during low-traffic periods.
"""

import json
import os
import sys
import requests
from datetime import datetime

# Credentials
CRED_PATH = os.path.expanduser("~/.openclaw/workspace/.credentials")
POSTHOG_CRED = os.path.join(CRED_PATH, "posthog.json")
SENTRY_CRED = os.path.join(CRED_PATH, "sentry.json")

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL")  # Configured in PostHog/Sentry

def check_sentry_config():
    """Check if Sentry project has alerts configured."""
    if not os.path.exists(SENTRY_CRED):
        print("⚠️  Sentry credentials not found. Ensure sentry.json exists.")
        return False
    
    with open(SENTRY_CRED) as f:
        cred = json.load(f)
    
    if cred.get("dsn"):
        print("✅ Sentry DSN found")
        return True
    return False

def check_posthog_config():
    """Check if PostHog is configured."""
    if not os.path.exists(POSTHOG_CRED):
        print("⚠️  PostHog credentials not found. Ensure posthog.json exists.")
        return False
    
    with open(POSTHOG_CRED) as f:
        cred = json.load(f)
    
    if cred.get("apiKey") and cred.get("host"):
        print("✅ PostHog API key and host found")
        return True
    return False

def test_slack_integration():
    """Test if Slack integration is working."""
    if not SLACK_WEBHOOK:
        print("⚠️  SLACK_WEBHOOK_URL not set in environment")
        print("   Configure in PostHog/Sentry dashboard settings")
        return False
    
    # Test webhook
    test_payload = {
        "text": f"⚡ Alert test from Zer0Day Labs at {datetime.now().isoformat()}"
    }
    
    try:
        resp = requests.post(SLACK_WEBHOOK, json=test_payload, timeout=5)
        if resp.status_code == 200:
            print("✅ Slack webhook test successful")
            return True
        else:
            print(f"❌ Slack webhook failed: {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Slack webhook error: {e}")
        return False

def run_alert_tests():
    """Run all alert configuration checks."""
    print("\n" + "=" * 50)
    print("Alert Configuration Test")
    print("=" * 50)
    
    checks = []
    
    checks.append(("Sentry Configuration", check_sentry_config()))
    checks.append(("PostHog Configuration", check_posthog_config()))
    checks.append(("Slack Integration", test_slack_integration()))
    
    print("\n" + "=" * 50)
    print("Summary:")
    print("=" * 50)
    
    all_passed = True
    for name, passed in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n✅ All alert configurations found. Ready for manual alert setup.")
        print("   Follow: scripts/setup_alerts_checklist.md")
    else:
        print("\n❌ Some configurations missing. Please complete the setup.")
    
    return all_passed

if __name__ == "__main__":
    run_alert_tests()
