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
    print("Successfully authenticated")
    access_token = auth_token_response.json()['access_token']

    pr_id = os.getenv('BITBUCKET_PR_ID')
    if not pr_id:
        print("BITBUCKET_PR_ID must be set")
        exit(1)

    owner = os.getenv('BITBUCKET_REPO_OWNER')
    if not owner:
        print("BITBUCKET_REPO_OWNER must be set")
        exit(1)

    repo_slug = os.getenv('BITBUCKET_REPO_SLUG')
    if not repo_slug:
        print("BITBUCKET_REPO_SLUG must be set")
        exit(1)

    if os.getenv('PR_COMMENT'):
        comment = os.getenv('PR_COMMENT')
    elif os.getenv('PR_COMMENT_FILE'):
        comment_file = os.getenv('PR_COMMENT_FILE')
        with open(comment_file, 'r') as file:
            comment = file.read()
    else:
        print("PR_COMMENT or PR_COMMENT_FILE must be set")
        exit(1)

    content = {'content': {'raw': f"Automated PR comment\n\n```\n{comment}\n```"}}
    url = f"{bitbucket_api}/2.0/repositories/{owner}/{repo_slug}/pullrequests/{pr_id}/comments"
    print(f"Adding comment: {url}")
    print(f"{content}")
    post = requests.post(
        url,
        json=content,
        headers={'Authorization': f"Bearer {access_token}"})
    if post.status_code != 201:
        print("Failed to post comment")
        print(f"{post.status_code} {post.text}")
        exit(1)
    else:
        print("Successfully posted comment")


if __name__ == '__main__':
    comment_on_pr()
