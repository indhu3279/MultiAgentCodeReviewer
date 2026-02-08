import os
import json
from github_int.client import GitHubClient
from github_int.utils import extract_code_from_pr
from graph.workflow import build_review_graph
from dotenv import load_dotenv

load_dotenv(".gitignore/.env")

def review_pull_request(owner: str, repo: str, pr_number: int):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN not set in environment")

    client = GitHubClient(token)

    print("Fetching PR files...")
    files = client.get_pr_files(owner, repo, pr_number)

    print(f"Fetched {len(files)} files from PR")

    code = extract_code_from_pr(files)

    if not code.strip():
        print("No code diff found in PR. Skipping review.")
        return

    print("Running LangGraph multi-agent review...")
    graph = build_review_graph()

    initial_state = {
        "code": code,
        "bug_report": None,
        "security_report": None,
        "performance_report": None,
        "final_review": None,
    }

    result = graph.invoke(initial_state)
    final_review = result["final_review"]

    # Format comment nicely
    comment_body = (
        "### 🤖 AI Code Review (Multi-Agent)\n\n"
        "Here is an automated review of this PR:\n\n"
        "```json\n"
        f"{json.dumps(final_review, indent=2)}\n"
        "```"
    )

    print("Posting review as PR comment...")
    client.post_pr_comment(owner, repo, pr_number, comment_body)

    print("✅ Review posted successfully!")


if __name__ == "__main__":
    # CHANGE THESE
    OWNER = "indhu3279"
    REPO = "RAG_LEARNING_DOC_Q-A"
    PR_NUMBER = 1

    review_pull_request(OWNER, REPO, PR_NUMBER)
