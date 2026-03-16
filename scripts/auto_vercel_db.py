#!/usr/bin/env python3
"""Automate Vercel ↔ Railway DB integration.

This script reads a mapping of project names to DATABASE_URLs from a JSON file
(`railway_db.json`) and updates the corresponding Vercel environment variables.

Requirements:
  - Vercel API token stored in ~/.openclaw/workspace/.credentials/vercel.json
  - JSON file with the structure:
        {
          "MusicGen": "postgres://user:pw@host:port/dbname?sslmode=require",
          "AudioStudio": "postgres://user:pw@host:port/dbname?sslmode=require"
        }
  - Vercel projects must be named exactly as the keys in the JSON file.

Usage:
  python3 auto_vercel_db.py --config railway_db.json
"""

import json
import os
import sys
import argparse
import requests

# Load Vercel credentials
CRED_PATH = os.path.expanduser("~/.openclaw/workspace/.credentials/vercel.json")
try:
    with open(CRED_PATH) as f:
        cred = json.load(f)
except Exception as e:
    print(f"Error loading Vercel credentials: {e}")
    sys.exit(1)

TOKEN = cred.get("token")
ACCOUNT_ID = cred.get("account")
API_URL = f"https://api.vercel.com/v1"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

def load_config(path):
    with open(path) as f:
        return json.load(f)

def set_env_var(project_id, key, value):
    url = f"{API_URL}/projects/{project_id}/env"
    payload = {
        "key": key,
        "value": value,
        "type": "encrypted",
        "target": ["production"],
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    if resp.status_code in (200, 201):
        print(f"✅ Updated {key} for project {project_id}")
    else:
        print(f"❌ Failed to update {key} for project {project_id}: {resp.status_code} {resp.text}")

def main():
    parser = argparse.ArgumentParser(description="Update Vercel env vars with Railway DB URLs")
    parser.add_argument("--config", required=True, help="Path to JSON mapping of project names to DATABASE_URLs")
    args = parser.parse_args()

    db_map = load_config(args.config)

    # Get list of Vercel projects
    projects_resp = requests.get(f"{API_URL}/accounts/{ACCOUNT_ID}/projects", headers=HEADERS)
    if projects_resp.status_code != 200:
        print(f"❌ Failed to fetch Vercel projects: {projects_resp.status_code} {projects_resp.text}")
        sys.exit(1)
    projects = projects_resp.json().get("projects", [])
    project_lookup = {p["name"]: p["id"] for p in projects}

    for proj_name, db_url in db_map.items():
        proj_id = project_lookup.get(proj_name)
        if not proj_id:
            print(f"❌ Vercel project '{proj_name}' not found. Skipping.")
            continue
        set_env_var(proj_id, "DATABASE_URL", db_url)

if __name__ == "__main__":
    main()
