
import base64
import json
import urllib.request
import urllib.error
import sys
import os

TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_OWNER = "ZheWang-stack"
REPO_NAME = "FairProp-AI"
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
    "User-Agent": "FairProp-Doc-Updater"
}

def call_api(url, data=None, method='GET'):
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8') if data else None, 
            headers=HEADERS, 
            method=method
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def upload_file(filename):
    print(f"Uploading {filename} to GitHub...")
    local_path = os.path.join(r"c:\Users\86187\Desktop\ease", filename)
    
    if not os.path.exists(local_path):
        print(f"Local file not found: {local_path}")
        return

    try:
        with open(local_path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        print(f"Error reading local file: {e}")
        return
    
    # Handle windows path separators for API
    api_path = filename.replace("\\", "/")
    url = f"{BASE_URL}/contents/{api_path}"
    
    res = call_api(url)
    sha = res['sha'] if res and 'sha' in res else None
    
    data = {"message": f"Professionalize docs: {os.path.basename(filename)}", "content": content}
    if sha: data["sha"] = sha
    
    res = call_api(url, data=data, method='PUT')
    if res:
        print(f"✅ {filename} uploaded successfully.")
    else:
        print(f"❌ Failed to upload {filename}.")

if __name__ == "__main__":
    files = [
        "README.md",
        "LEGAL_NOTICE.md",
        "docs\\evaluation.md",
        "docs\\jurisdiction_coverage.md",
        "docs\\rules_engine.md"
    ]
    for f in files:
        upload_file(f)
