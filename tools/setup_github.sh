#!/usr/bin/env bash
set -euo pipefail

readonly GITHUB_REPOSITORY="afabiszewski/wielicka"
readonly GITHUB_REMOTE_URL="https://github.com/${GITHUB_REPOSITORY}.git"

ensure_github_cli() {
  if command -v gh >/dev/null 2>&1; then
    return 0
  fi

  if command -v apt-get >/dev/null 2>&1; then
    apt-get update -y -qq
    apt-get install -y -qq gh
    return 0
  fi

  printf 'GitHub CLI (gh) not found and no supported package manager is available.\n' >&2
  return 1
}

configure_github_remote() {
  if git -C "$ROOT_DIR" remote get-url origin >/dev/null 2>&1; then
    git -C "$ROOT_DIR" remote set-url origin "$GITHUB_REMOTE_URL"
  else
    git -C "$ROOT_DIR" remote add origin "$GITHUB_REMOTE_URL"
  fi
}

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ensure_github_cli
configure_github_remote

if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  github_token="$GITHUB_TOKEN"
  unset GITHUB_TOKEN
  printf '%s' "$github_token" | gh auth login --hostname github.com --with-token
  gh auth setup-git
elif [[ -n "${GH_TOKEN:-}" ]]; then
  printf '%s' "$GH_TOKEN" | env -u GH_TOKEN gh auth login --hostname github.com --with-token
  env -u GH_TOKEN gh auth setup-git
else
  printf 'GitHub remote configured; set GITHUB_TOKEN or GH_TOKEN to authenticate gh.\n'
fi
