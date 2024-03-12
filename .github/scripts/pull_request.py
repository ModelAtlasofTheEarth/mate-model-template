import os
from github import Github, Auth

# Environment variables
token = os.environ.get("GITHUB_TOKEN")
repo_name = os.environ.get("REPO_NAME")
pr_title = os.environ.get("PR_TITLE")
# event_path = os.environ.get("PR_BODY")
head_branch = os.environ.get("HEAD_BRANCH")
base_branch = os.environ.get("BASE_BRANCH")

# Get repo
auth = Auth.Token(token)
g = Github(auth=auth)
repo = g.get_repo(repo_name)

# PR body was a is passed in as a list of commits, change it into a string of commit messages
# pr_body = '\n'.join(['- '+ commit.message for commit in pr_body])
pr_body = "Temp"

# Existing PRs
existing_prs = repo.get_pulls(state='open', sort='created', base='main')

pr_exists = False

for pr in existing_prs:
    if pr.title == pr_title:
        pr_exists = True
        existing_pr = pr

        # Edit existing PR
        existing_pr_body = existing_pr.body
        updated_pr_body = existing_pr_body + '\n' + pr_body
        existing_pr.edit(body=updated_pr_body)

        print(f"Pull request body updated: {existing_pr.html_url}")
        break
    
if pr_exists == False:
    # Make new pull request
    new_pr = repo.create_pull(
        title = pr_title,
        body = "*Commits*\n\n" + pr_body,
        head = head_branch,
        base = base_branch
    )

    print(f"Pull request created: {new_pr.html_url}")

    