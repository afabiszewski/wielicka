#!/usr/bin/env bash
set -euo pipefail

readonly GITHUB_REMOTE_URL="https://github.com/afabiszewski/wielicka.git"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if git -C "$ROOT_DIR" remote get-url origin >/dev/null 2>&1; then
  git -C "$ROOT_DIR" remote set-url origin "$GITHUB_REMOTE_URL"
else
  git -C "$ROOT_DIR" remote add origin "$GITHUB_REMOTE_URL"
fi
