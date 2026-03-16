#!/usr/bin/env python3
"""Collect DATABASE_URLs from Railway projects."""

import json
import os
import sys
import requests
import argparse

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

QUERY = """
query GetEnvironmentVariables($projectId: ID!, $environmentId: ID!) {
  project(projectId: $projectId) {
    environment(id: $environmentId) {
      environmentVariables {
        edges {
          node {
            key
            value
          }
        }
      }
    }
  }
}
"""

def fetch_env_vars(project_id, env_id="production"):
    resp = requests.post(
        API_URL,
        headers=HEADERS,
        json={"query": QUERY, "variables": {"projectId": project_id, "environmentId": env_id}}
    )
    data = resp.json()
    if "errors" in data:
        return None
    return data

def main():
    parser = argparse.ArgumentParser(description="Collect DATABASE_URLs from Railway")
    parser.add_argument("--project-id", action="append", required=True)
    parser.add_argument("--label", action="append")
    args = parser.parse_args()
    
    print("📊 Railway DATABASE_URL Collector\n")
    results = {}
    
    for i, pid in enumerate(args.project_id):
        label = args.label[i] if i < len(args.label or []) else "Unknown"
        print(f"🔍 Project: {label} ({pid})")
        result = fetch_env_vars(pid)
        
        if result and "data" in result:
            data = result["data"]
            env = data.get("project", {}).get("environment", {})
            for edge in env.get("environmentVariables", {}).get("edges", []):
                node = edge.get("node", {})
                if node.get("key") == "DATABASE_URL":
                    results[label] = node.get("value")
                    print(f"   ✅ {node.get('value')[:50]}...")
                    break
            else:
                print(f"   ❌ No DATABASE_URL")
        else:
            print(f"   ❌ Query failed")
    
    if results:
        print("\n📝 Output:")
        for label, url in results.items():
            print(f'  "{label}": "{url}",')

if __name__ == "__main__":
    main()
