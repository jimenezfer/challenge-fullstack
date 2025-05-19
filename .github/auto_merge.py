# auto_merge.py
import os
import requests

def create_pull_request():
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Create a pull request
    pr_data = {
        'title': 'Auto PR: Merge test-branch into main',
        'body': 'This PR is automatically created to merge changes from test-branch to main.',
        'head': 'test-branch',
        'base': 'main'
    }

    pr_url = f'https://api.github.com/repos/{repo}/pulls'
    response = requests.post(pr_url, headers=headers, json=pr_data)

    if response.status_code == 201:
        print('Pull request created successfully.')
        return response.json()['url']
    else:
        print(f'Failed to create pull request: {response.json()}')
        return None

def merge_pull_request(pr_url):
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    pull_request_number = pr_url.split('/')[-1]
    merge_url = f'https://api.github.com/repos/{repo}/pulls/{pull_request_number}/merge'

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.put(merge_url, headers=headers, json={'merge_method': 'squash'})

    if response.status_code == 200:
        print('Pull request merged successfully.')
    else:
        print(f'Failed to merge pull request: {response.json()}')

if __name__ == '__main__':
    pr_url = create_pull_request()
    if pr_url:
        merge_pull_request(pr_url)
