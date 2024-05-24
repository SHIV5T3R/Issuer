import os
import requests


def update_org_variable(org, var_name, new_value, token):
    url = f"https://api.github.com/orgs/{org}/actions/variables/{var_name}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    print(token)
    data = {
        "name": var_name,
        "value": str(new_value)
    }
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()

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
    org_var_token = os.getenv('ISSUE_GEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    issue_prefix = os.getenv('ISSUE_PREFIX')
    issue_number = os.getenv('ISSUE_NUMBER')
    issue_number_var = os.getenv('ISSUE_NUMBER_VAR')
    issue_title = os.getenv('GITHUB_EVENT_ISSUE_TITLE')
    org_name = os.getenv('ORG_NAME')

    next_number = int(issue_number) + 1
    update_org_variable(org_name, issue_number_var, next_number, org_var_token)
    update_issue_title(repo, issue_prefix, issue_number, github_token, next_number, issue_title)
