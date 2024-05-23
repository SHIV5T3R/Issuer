import os
import requests
import subprocess

def get_next_issue_number(issue_counter_repo, token):
    subprocess.run(["git", "clone", f"https://x-access-token:{token}@github.com/{issue_counter_repo}.git", "issue-counter"], check=True)
    with open('issue-counter/counter.txt', 'r') as file:
        current_number = int(file.read().strip())
    next_number = current_number + 1
    with open('issue-counter/counter.txt', 'w') as file:
        file.write(str(next_number))
    return next_number

def update_issue_counter(next_number):
    subprocess.run(["git", "-C", "issue-counter", "config", "--global", "user.name", "Issue Number Assigner"], check=True)
    subprocess.run(["git", "-C", "issue-counter", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
    subprocess.run(["git", "-C", "issue-counter", "add", "counter.txt"], check=True)
    subprocess.run(["git", "-C", "issue-counter", "commit", "-m", f"Update issue counter to {next_number}"], check=True)
    subprocess.run(["git", "-C", "issue-counter", "push"], check=True)

def update_issue_title(repo, issue_prefix, issue_number, token, next_number, issue_title):
    issue_number_formatted = f"{issue_prefix}-{next_number:03d}"
    new_title = f"{issue_number_formatted} - {issue_title}"
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"title": new_title}
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Failed to update issue title: {response.json()}")

if __name__ == "__main__":
    github_token = os.getenv('GITHUB_TOKEN')
    issue_gen_token = os.getenv('ISSUE_GEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    issue_prefix = os.getenv('ISSUE_PREFIX')
    issue_number = os.getenv('GITHUB_EVENT_ISSUE_NUMBER')
    issue_title = os.getenv('GITHUB_EVENT_ISSUE_TITLE')
    issue_counter_repo = os.getenv('ISSUE_COUNTER_REPO')

    next_number = get_next_issue_number(issue_counter_repo, issue_gen_token)
    update_issue_counter(next_number)
    update_issue_title(repo, issue_prefix, issue_number, github_token, next_number, issue_title)
