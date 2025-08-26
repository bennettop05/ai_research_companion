import requests

def scrape_github_readme(repo_url: str) -> str:
    """
    Fetch README.md text from a public GitHub repository.
    """
    if repo_url.endswith("/"):
        repo_url = repo_url[:-1]

    api_url = repo_url.replace("https://github.com", "https://raw.githubusercontent.com") + "/main/README.md"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.text
    else:
        return f"⚠️ Failed to fetch README from {repo_url}"
