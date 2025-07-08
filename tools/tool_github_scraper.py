# tools/tool_github_scraper.py

import requests

def fetch_github_readme(repo_url: str) -> str:
    if "github.com" not in repo_url:
        return "Invalid GitHub URL."

    parts = repo_url.rstrip('/').split('/')
    if len(parts) < 2:
        return "Could not parse GitHub repo."

    user, repo = parts[-2], parts[-1]
    url = f"https://raw.githubusercontent.com/{user}/{repo}/main/README.md"
    
    res = requests.get(url)
    return res.text if res.status_code == 200 else "README not found."
