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

    comment = os.getenv('PR_COMMENT')
    if not comment:
        print("PR_COMMENT must be set")
        exit(1)

    content = {'content': {'raw': 'Automated PR comment\n\n\x1b[0m\x1b[1mRefreshing Terraform state in-memory prior to plan...\x1b[0m\nThe refreshed state will be used to calculate this plan, but will not be\npersisted to local or remote state storage.\n\x1b[0m\n\x1b[0m\x1b[1mmodule.terraform_state.aws_dynamodb_table.terraform_locks: Refreshing state... [id=terraform-locks]\x1b[0m\n\x1b[0m\x1b[1mmodule.terraform_state.aws_s3_bucket.terraform_state: Refreshing state... [id=terraform-state-071021110864]\x1b[0m\n\n------------------------------------------------------------------------\n\n\x1b[0m\x1b[1m\x1b[32mNo changes. Infrastructure is up-to-date.\x1b[0m\x1b[32m\n\nThis means that Terraform did not detect any differences between your\nconfiguration and real physical resources that exist. As a result, no\nactions need to be performed.\x1b[0m\nReleasing state lock. This may take a few moments...', 'markup': 'markdown'}}
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
