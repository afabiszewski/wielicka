#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
VENV_DIR="$ROOT_DIR/deps/.venv"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  printf 'Python 3 is required. Set PYTHON to a Python 3.11+ executable.\n' >&2
  exit 1
fi

"$PYTHON" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r "$ROOT_DIR/deps/requirements.txt"

printf 'Environment ready: %s\n' "$VENV_DIR"
