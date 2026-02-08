import requests

GITHUB_API = "https://api.github.com"

class GitHubClient:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }

    def get_pr_files(self, owner: str, repo: str, pr_number: int):
        url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post_pr_comment(self, owner: str, repo: str, pr_number: int, body: str):
        url = f"{GITHUB_API}/repos/{owner}/{repo}/issues/{pr_number}/comments"
        response = requests.post(
            url,
            headers=self.headers,
            json={"body": body}
        )
        response.raise_for_status()
