#!/usr/bin/env bash
set -euo pipefail

# Usage: ./create_github_env.sh <owner> <repo> <environment> [users_csv] [teams_csv]
# users_csv: optional comma-separated GitHub usernames to require as reviewers
# teams_csv: optional comma-separated team slugs (within the org) to require as reviewers
# Requires GITHUB_TOKEN in env with repo scope

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <owner> <repo> <environment> [users_csv] [teams_csv]"
  exit 2
fi
OWNER=$1
REPO=$2
ENV=$3
USERS_CSV=${4-}
TEAMS_CSV=${5-}

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "Error: GITHUB_TOKEN env var is required. Create a token with repo scope and export GITHUB_TOKEN=..."
  exit 1
fi

API_BASE="https://api.github.com/repos/$OWNER/$REPO"
ENV_URL="$API_BASE/environments/$ENV"
PROT_URL="$ENV_URL/protection"

echo "Creating environment '$ENV' in $OWNER/$REPO..."

resp=$(curl -sS -X PUT -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" "$ENV_URL" -d '{"wait_timer":0}')

if echo "$resp" | grep -q 'created_at\|updated_at'; then
  echo "Environment '$ENV' created or updated successfully." 
else
  echo "Unexpected response from GitHub API when creating environment:" >&2
  echo "$resp" >&2
  exit 1
fi

# Build reviewers list after validation
entries=()

validate_user() {
  local user=$1
  local url="https://api.github.com/users/$user"
  if curl -sS -f -H "Authorization: token $GITHUB_TOKEN" "$url" >/dev/null 2>&1; then
    echo "ok"
  else
    echo "missing"
  fi
}

validate_team() {
  local team=$1
  # team slug expected without org prefix; use OWNER as org
  local url="https://api.github.com/orgs/$OWNER/teams/$team"
  if curl -sS -f -H "Authorization: token $GITHUB_TOKEN" "$url" >/dev/null 2>&1; then
    echo "ok"
  else
    echo "missing"
  fi
}

# collect user entries
if [ -n "$USERS_CSV" ]; then
  IFS=',' read -r -a users <<< "$USERS_CSV"
  for u in "${users[@]}"; do
    u_trim=$(echo "$u" | xargs)
    if [ -z "$u_trim" ]; then
      continue
    fi
    if [ "$(validate_user "$u_trim")" = "ok" ]; then
      entries+=("{\"type\":\"User\",\"login\":\"$u_trim\"}")
      echo "Validated user: $u_trim"
    else
      echo "Warning: user '$u_trim' not found or inaccessible. Skipping." >&2
    fi
  done
fi

# collect team entries
if [ -n "$TEAMS_CSV" ]; then
  IFS=',' read -r -a teams <<< "$TEAMS_CSV"
  for t in "${teams[@]}"; do
    t_trim=$(echo "$t" | xargs)
    if [ -z "$t_trim" ]; then
      continue
    fi
    if [ "$(validate_team "$t_trim")" = "ok" ]; then
      entries+=("{\"type\":\"Team\",\"slug\":\"$t_trim\"}")
      echo "Validated team: $t_trim"
    else
      echo "Warning: team '$t_trim' not found in org '$OWNER' or inaccessible. Skipping." >&2
    fi
  done
fi

# Apply protection rules if we have any entries
if [ ${#entries[@]} -gt 0 ]; then
  reviewers_entries=$(IFS=,; echo "${entries[*]}")
  payload=$(cat <<JSON
{
  "rules": [
    {
      "type": "required_reviewers",
      "required_reviewers": [${reviewers_entries}],
      "required_approving_review_count": 1
    }
  ],
  "wait_timer": 0
}
JSON
)
  echo "Applying protection rules to environment (requires reviewers):"
  echo "$payload"
  prot_resp=$(curl -sS -X PUT -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" "$PROT_URL" -d "$payload")
  if echo "$prot_resp" | grep -q 'rules\|required_reviewers'; then
    echo "Protection updated (response includes rules)."
    echo "$prot_resp" | jq -r '.rules[]?.type' 2>/dev/null || true
  else
    echo "Protection API response (may still be OK):" >&2
    echo "$prot_resp" >&2
    echo "Note: The protection API format may vary by GitHub version. If the script cannot set protection, configure reviewers in the GitHub UI: Settings → Environments → $ENV."
  fi
else
  echo "No valid users or teams provided — skipping protection configuration."
fi

exit 0
