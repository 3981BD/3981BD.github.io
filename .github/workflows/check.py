import subprocess
import os
import json
from urllib.request import urlopen
github_sha = os.environ['GITHUB_SHA']
github_repository = os.environ['GITHUB_REPOSITORY']
pages_build_version = urlopen('https://subdomain.func.host/pages-build-version').read().decode()
response = subprocess.getoutput(f'gh api repos/{github_repository}/compare/{pages_build_version}...{github_sha}')
print(f"::notice::response: {response}")
comparison = json.loads(response)
print(f"::notice::comparison['status']: {comparison['status']}")
print(f"::notice::GITHUB_SHA: {github_sha}")
print(f"::notice::pages_build_version: {pages_build_version}")
