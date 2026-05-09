#!/usr/bin/env bash
set -e

# This script is intentionally conservative.
# It only cleans known temp/cache folders inside this repo.
# Extend it manually once you're sure what is truly orphaned.

cd "$(dirname "$0")/.."

echo "[cleanup] Starting orphan cleanup inside ai-hanuman-tunnel..."

# Example: remove local temp/cache folders if they exist
for path in \
  ".pytest_cache" \
  ".mypy_cache" \
  ".ruff_cache" \
  "tmp" \
  "logs/tmp" \
  "__pycache__"
do
  if [ -e "$path" ]; then
    echo "[cleanup] Removing: $path"
    rm -rf "$path"
  fi
done

echo "[cleanup] Done. No system-wide paths were touched."
