# Bitbucket Pull Request Commenter
A simple docker image for making a comment on a bitbucket pull request

## Usage
### Variables
- BITBUCKET_API - The API of bitbucket.
- BITBUCKET_USERNAME - Username of the commenter.
- BITBUCKET_PASSWORD - Password of the commenter.
- OIDC_CLIENT_ID - Client ID of the Bitbucket commenting app (https://confluence.atlassian.com/bitbucket/oauth-on-bitbucket-cloud-238027431.html).
- OIDC_CLIENT_SECRET - Client secret of the Bitbucket commenting app (https://confluence.atlassian.com/bitbucket/oauth-on-bitbucket-cloud-238027431.html).
- BITBUCKET_PR_ID - The ID of the PR to comment on. This will be available for bitbucket pipelines.
- BITBUCKET_PROJECT_KEY - The project name. This will be available for bitbucket pipelines.
- BITBUCKET_REPO_SLUG - The repository name. This will be available for bitbucket pipelines.
- PR_COMMENT - The markdown comment to make.

### Example usage
```bash
docker run \
    -e BITBUCKET_API=https://api.bitbucket.org \
    -e BITBUCKET_USERNAME=commenter-bot@domain.com \
    -e BITBUCKET_PASSWORD=password \
    -e OIDC_CLIENT_ID=<client_id> \
    -e OIDC_CLIENT_SECRET=<client_secret> \
    -e BITBUCKET_PR_ID=1 \
    -e BITBUCKET_PROJECT_KEY=project \
    -e BITBUCKET_REPO_SLUG=<repo> \
    -e PR_COMMENT="My PR comment" \
    benjjefferies/bitbucket-pull-request-commenter
```