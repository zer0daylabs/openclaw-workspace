#!/usr/bin/env python3
"""Railway cleanup automation script.

This script uses the Railway GraphQL API to:
  1. List all projects in the workspace.
  2. Delete specified projects (if the API supports deletion).
  3. Rename projects.

Prerequisites:
  - Railway CLI authenticated as support@zer0daylabs.com.
  - The following credentials file is present: ~/.openclaw/workspace/.credentials/railway.json

Usage:
  python3 railway_cleanup.py list
  python3 railway_cleanup.py delete <project_id>
  python3 railway_cleanup.py rename <project_id> <new_name>

The script will read the credentials file for the API token and endpoint.

Note: Deleting a Railway project is a destructive operation.  Use with
caution.  This script does not confirm deletion; you must confirm via
command line arguments.
"""

import json
import os
import sys
import requests

CRED_PATH = os.path.expanduser("~/.openclaw/workspace/.credentials/railway.json")

# Load credentials
try:
    with open(CRED_PATH) as f:
        creds = json.load(f)
except Exception as e:
    print(f"Error loading credentials: {e}")
    sys.exit(1)

TOKEN = creds.get("token")
API_URL = creds.get("api")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

QUERY_PROJECTS = """
query {
  projects {
    edges {
      node {
        id
        name
        services {
          edges {
            node {
              id
              name
            }
          }
        }
      }
    }
  }
}
"""

def list_projects():
    resp = requests.post(API_URL, headers=HEADERS, json={"query": QUERY_PROJECTS})
    data = resp.json()
    if "errors" in data:
        print("GraphQL errors:", data["errors"])
        return
    projects = data["data"]["projects"]["edges"]
    print("Projects in workspace:\n")
    for p in projects:
        node = p["node"]
        print(f"- {node['name']} (ID: {node['id']})")

DELETE_MUTATION = """
mutation DeleteProject($projectId: ID!) {
  deleteProject(projectId: $projectId) {
    success
  }
}
"""

def delete_project(project_id):
    resp = requests.post(API_URL, headers=HEADERS, json={
        "query": DELETE_MUTATION,
        "variables": {"projectId": project_id},
    })
    data = resp.json()
    if "errors" in data:
        print("GraphQL errors:", data["errors"])
        return
    success = data["data"]["deleteProject"]["success"]
    print(f"Delete project {project_id} success: {success}")

RENAME_MUTATION = """
mutation RenameProject($projectId: ID!, $name: String!) {
  renameProject(projectId: $projectId, name: $name) {
    success
  }
}
"""

def rename_project(project_id, new_name):
    resp = requests.post(API_URL, headers=HEADERS, json={
        "query": RENAME_MUTATION,
        "variables": {"projectId": project_id, "name": new_name},
    })
    data = resp.json()
    if "errors" in data:
        print("GraphQL errors:", data["errors"])
        return
    success = data["data"]["renameProject"]["success"]
    print(f"Rename project {project_id} to '{new_name}' success: {success}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: railway_cleanup.py <command> [args]")
        print("Commands: list, delete <id>, rename <id> <new_name>")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "list":
        list_projects()
    elif cmd == "delete" and len(sys.argv) == 3:
        delete_project(sys.argv[2])
    elif cmd == "rename" and len(sys.argv) == 4:
        rename_project(sys.argv[2], sys.argv[3])
    else:
        print("Invalid command or arguments.")
        sys.exit(1)
