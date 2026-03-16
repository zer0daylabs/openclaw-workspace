#!/usr/bin/env python3
"""Collect DATABASE_URLs from Railway projects using GraphQL API.

This script fetches DATABASE_URL environment variables from specified Railway projects.

Usage:
    python3 collect_railway_db_urls.py --project-id <id> --project-id <id> ...
    
Reads credentials from: ~/.openclaw/workspace/.credentials/railway.json

Requires Railway project IDs (from `railway project ls` output).
"""

import json
import os
import sys
import requests
import argparse

# Load credentials
CRED_PATH = os.path.expanduser("~/.openclaw/workspace/.credentials/railway.json")
try:
    with open(CRED_PATH) as f:
        cred = json.load(f)
except Exception as e:
    print(f"Error loading credentials: {e}")
    sys.exit(1)

TOKEN = cred.get("token")
API_URL = cred.get("api")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# GraphQL query to get environment variables from a project
ENV_QUERY = """
query GetProjectEnv($projectId: ID!) {
  serviceInstance(projectId: $projectId, environmentId: "production") {
    envVars {
      edges {
        node {
          key
          value
        }
      }
    }
  }
}
"""

def fetch_env_vars(project_id):
    """Fetch environment variables for a project."""
    resp = requests.post(
        API_URL,
        headers=HEADERS,
        json={"query": ENV_QUERY, "variables": {"projectId": project_id}}
    )
    data = resp.json()
    if "errors" in data:
        print(f"❌ GraphQL error for project {project_id}: {data['errors']}")
        return {}
    return data.get("data", {}).get("serviceInstance", {}).get("envVars", {}).get("edges", [])

def find_db_url(env_edges):
    """Extract DATABASE_URL from environment variables."""
    for edge in env_edges:
        node = edge.get("node", {})
        if node.get("key") == "DATABASE_URL":
            return node.get("value")
    return None

def main():
    parser = argparse.ArgumentParser(description="Collect DATABASE_URLs from Railway projects")
    parser.add_argument("--project-id", action="append", required=True, help="Railway project ID")
    args = parser.parse_args()
    
    print("📊 Railway DATABASE_URL Collector\n")
    
    db_urls = {}
    for project_id in args.project_id:
        print(f"📦 Project: {project_id}")
        env_vars = fetch_env_vars(project_id)
        db_url = find_db_url(env_vars)
        
        if db_url:
            db_urls[project_id] = db_url
            print(f"   ✅ DATABASE_URL: {db_url[:50]}...")
        else:
            print(f"   ❌ No DATABASE_URL found in project environment")
        print()
    
    if db_urls:
        print("📝 Output (paste into docs/railway_db_urls_template.json):")
        print("\n{")
        for pid, url in db_urls.items():
            # Extract project name from ID (simplified)
            print(f'  "{pid}": "{url}",')
        print("}")

if __name__ == "__main__":
    main()
