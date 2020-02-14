#!/usr/bin/env python
import os

import requests


def comment_on_pr():
    bitbucket_api = os.getenv('BITBUCKET_API', 'https://api.bitbucket.org')
    username, password = os.getenv('BITBUCKET_USERNAME'), os.getenv('BITBUCKET_PASSWORD')
    if not username or not password:
        print("BITBUCKET_USERNAME and BITBUCKET_PASSWORD must be set")
        exit(1)
    client_id, client_secret = os.getenv('OIDC_CLIENT_ID'), os.getenv('OIDC_CLIENT_SECRET')
    if not client_id or not client_secret:
        print("OIDC_CLIENT_ID and OIDC_CLIENT_SECRET must be set")
        exit(1)
    auth_token_response = requests.post(f"{bitbucket_api.replace('api.', '')}/site/oauth2/access_token",
                                        data=[('grant_type', 'password'), ('username', username), ('password', password)],
                                        auth=(client_id, client_secret))
    if 'access_token' not in auth_token_response.json():
        print("Could not get access token")
        exit(1)
    access_token = auth_token_response.json()['access_token']

    pr_id = os.getenv('BITBUCKET_PR_ID')
    if not pr_id:
        print("BITBUCKET_PR_ID must be set")
        exit(1)

    project = os.getenv('BITBUCKET_PROJECT_KEY')
    if not project:
        print("BITBUCKET_PROJECT_KEY must be set")
        exit(1)

    repo_slug = os.getenv('BITBUCKET_REPO_SLUG')
    if not repo_slug:
        print("BITBUCKET_PR_ID must be set")
        exit(1)

    comment = os.getenv('PR_COMMENT')
    if not comment:
        print("PR_COMMENT must be set")
        exit(1)

    content = {'content': {'raw': f"Automated PR comment\n\n{comment}", 'markup': 'markdown'}}
    post = requests.post(
        f"{bitbucket_api}/2.0/repositories/{project}/{repo_slug}/pullrequests/{pr_id}/comments",
        json=content,
        headers={'Authorization': f"Bearer {access_token}"})
    print(post)


if __name__ == '__main__':
    comment_on_pr()
