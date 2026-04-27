CI: Rebuild Project Dashboards

This repository includes a GitHub Actions workflow that regenerates the Dev Hub project dashboards automatically.

Workflow: .github/workflows/regen-projects.yml

Behavior:
- Runs on push and pull_request to the main (or master) branch.
- Executes: make -C dev_hub regen-projects
- If generated files change, commits and pushes them back using the workflow's token.

Local testing:
- From repo root:
    cd /home/hn3t/dev_hub
    make regen-projects

To force discovery (merge new sibling repos into projects.json):
    make regen-projects-discover

Disable: remove or rename the workflow file under .github/workflows/regen-projects.yml

Approval gate:
- The workflow now requires manual approval before committing generated files. Create a GitHub Environment named 'regen-approve' and add reviewers (maintainers) to require approval.
- When a run produces changes, the 'commit' job will pause and wait for an environment approval before it performs the commit and push.

Auto-create environment (optional):
- A helper script is provided to create the GitHub environment via the REST API:
    scripts/create_github_env.sh <owner> <repo> <environment>
  Example:
    export GITHUB_TOKEN="<token-with-repo-scope>"
    ./scripts/create_github_env.sh hn3t hn3tdevops-jpg regen-approve
- The script performs a simple PUT to the environments API. It does not set reviewers; add required reviewers via the GitHub UI (recommended) or extend the script to configure protection rules via the API.

