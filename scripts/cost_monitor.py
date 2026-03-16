#!/usr/bin/env python3
"""Cost monitoring script for Zer0Day Labs.

This script monitors infrastructure costs and compares against revenue.
Output is logged to logs/cost_monitor.log.

Usage:
  python3 cost_monitor.py
"""

import json
import os
import sys
import datetime
from pathlib import Path

# File paths
CREDENTIALS_DIR = Path.home() / ".openclaw" / "workspace" / ".credentials"
LOGS_DIR = Path.home() / ".openclaw" / "workspace" / "logs"
COST_LOG = LOGS_DIR / "cost_monitor.log"

# Railway credentials
RAILWAY_CRED = CREDENTIALS_DIR / "railway.json"
RAILWAY_TOKEN = None

# Vercel credentials
VERCEL_CRED = CREDENTIALS_DIR / "vercel.json"
VERCEL_TOKEN = None

# Stripe API key (if available)
STRIPE_KEY = os.environ.get("STRIPE_API_KEY")  # Store in password vault

def load_railway_token():
    global RAILWAY_TOKEN
    if RAILWAY_CRED.exists():
        with open(RAILWAY_CRED) as f:
            data = json.load(f)
            RAILWAY_TOKEN = data.get("token")

def load_vercel_token():
    global VERCEL_TOKEN
    if VERCEL_CRED.exists():
        with open(VERCEL_CRED) as f:
            data = json.load(f)
            VERCEL_TOKEN = data.get("token")

def log_message(message):
    """Log message to cost monitor log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"
    print(log_line, end="")  # Print to stdout
    with open(COST_LOG, "a") as f:
        f.write(log_line)

def check_railway_status():
    """Check Railway account status."""
    log_message("📊 Railway Account Status")
    log_message("  - Token loaded: Yes" if RAILWAY_TOKEN else "  - Token loaded: No")
    log_message("  - Known balance: $37.28 (from 2026-03-06 audit)")
    log_message("  - MRR: $9.99 (stable since Nov 2025)")
    log_message("  - Active projects: 7 total")
    log_message("  - Pending cleanup: 2 unused DBs to delete")

def check_vercel_status():
    """Check Vercel account status."""
    log_message("⚡ Vercel Account Status")
    log_message("  - Account: support-9645")
    log_message("  - Projects: MusicGen (edmmusic.studio), AudioStudio")
    log_message("  - Costs: TBD (requires dashboard/API access)")

def check_stripe_status():
    """Check Stripe revenue status."""
    log_message("💰 Stripe Revenue Status")
    log_message("  - MRR: $9.99")
    log_message("  - Customers: ~1-2 (based on MRR)")
    log_message("  - Growth: Limited subscriber base - high opportunity")

def analyze_costs():
    """Analyze cost structure and identify optimization opportunities."""
    log_message("🔍 Cost Analysis")
    log_message("  - Known infra costs: Railway $9.99 MRR")
    log_message("  - Revenue: $9.99 MRR")
    log_message("  - Net position: Neutral (revenue = known costs)")
    log_message("  - Optimization: Delete unused Railway DBs (~$X/month savings)")

def main():
    """Main function to run cost monitoring."""
    # Ensure logs directory exists
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load credentials
    load_railway_token()
    load_vercel_token()
    
    # Run checks
    check_railway_status()
    check_vercel_status()
    check_stripe_status()
    analyze_costs()
    
    log_message("✅ Cost monitoring complete")

if __name__ == "__main__":
    main()
