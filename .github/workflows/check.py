import subprocess
import os
import json
from urllib.request import urlopen, Request

github_sha = os.environ.get('GITHUB_SHA')
github_repository = os.environ.get('GITHUB_REPOSITORY')

if not github_repository:
    raise ValueError("Missing GITHUB_REPOSITORY environment variable")
if not github_sha:
    raise ValueError("Missing GITHUB_SHA environment variable")

pages_build_version = urlopen('https://subdomain.func.host/pages-build-version').read().decode()

url = f"https://api.github.com/repos/{github_repository}/compare/{pages_build_version}...{github_sha}"
headers = {
    "Authorization": f"Bearer {os.environ.get('GH_TOKEN')}"
}

req = Request(url, headers=headers)
try:
    response = urlopen(req).read().decode()
except Exception as e:
    print(f"::error::Failed to fetch comparison data: {e}")
    raise

print(f"::notice::response: {response}")
data = json.loads(response)
# check if data contains an error response
if 'message' in data:
    print(f"::warning::errors: {data['message']}")
    raise ValueError(f"GitHub API returned an error: {data['message']}")

print(f"::notice::comparison['status']: {data['status']}")
print(f"::notice::GITHUB_SHA: {github_sha}")
print(f"::notice::pages_build_version: {pages_build_version}")
