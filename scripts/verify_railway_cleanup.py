#!/usr/bin/env python3
"""Verify Railway manual cleanup completion.

This script checks if the manual Railway cleanup task has been completed by:
1. Verifying project count is reduced from 7 to 5
2. Confirming cryptic names were replaced
3. Ensuring unused DBs were deleted

Usage:
    python3 verify_railway_cleanup.py
"""

import subprocess
import json
import sys
from pathlib import Path

def run_railway_cmd(cmd):
    """Run Railway CLI command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return None, str(e), 1

def verify_cleanup():
    """Verify Railway cleanup was completed."""
    print("🔍 Railway Cleanup Verification\n")
    
    # Get project list
    stdout, stderr, rc = run_railway_cmd("railway project ls --json")
    
    if rc != 0:
        print("❌ Railway CLI authentication failed")
        print(f"   Error: {stderr}")
        return False
    
    try:
        projects = json.loads(stdout)
    except json.JSONDecodeError:
        print("❌ Failed to parse Railway project list")
        return False
    
    project_count = len(projects.get("projects", []))
    print(f"📦 Total Railway projects: {project_count}")
    
    # Expected count after cleanup: 5 (from 7)
    if project_count == 5:
        print("✅ Project count correct (5 projects remaining)")
    elif project_count == 7:
        print("⏳ Cleanup not yet completed (7 projects still present)")
        return False
    else:
        print(f"⚠️ Unexpected project count: {project_count}")
    
    # Check for cryptic names
    cryptic_names = ["lucky-playfulness", "truthful-warmth", "appealing-laughter"]
    new_names = ["MusicGen-DB", "AudioStudio-DB", "musicgen-db", "audiostudio-db"]
    
    project_names = [p.get("name", "").lower() for p in projects.get("projects", [])]
    
    has_cryptic = any(name in project_names for name in [n.lower() for n in cryptic_names])
    has_renamed = any(name in project_names for name in [n.lower() for n in new_names])
    
    if has_cryptic:
        print("❌ Cryptic project names still present")
        print("   Remaining: lucky-playfulness, truthful-warmth, appealing-laughter")
    else:
        print("✅ No cryptic project names found")
    
    if has_renamed:
        print("✅ Project names appear to be renamed")
    else:
        print("⏳ Renamed projects not yet detected")
    
    print()
    if project_count == 5 and not has_cryptic:
        print("✅ Railway cleanup VERIFIED")
        return True
    else:
        print("⏳ Railway cleanup IN PROGRESS or PENDING")
        print("   Next: Lauro must complete manual dashboard cleanup")
        return False

if __name__ == "__main__":
    verify_cleanup()
