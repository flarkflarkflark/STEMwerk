#!/usr/bin/env bash
set -euo pipefail

# Sync the repo versions of the REAPER scripts into the user's REAPER Scripts folder.
# This is useful because REAPER often runs the copies under its config directory,
# not the files inside this git repo.
#
# Linux:  ~/.config/REAPER/Scripts/STEMwerk/scripts/reaper/
# macOS:  ~/Library/Application Support/REAPER/Scripts/STEMwerk/scripts/reaper/
#
# Usage (from repo root):
#   bash scripts/reaper/sync_to_reaper.sh

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
src_dir="${repo_root}/scripts/reaper"

linux_dest="${HOME}/.config/REAPER/Scripts/STEMwerk/scripts/reaper"
mac_dest="${HOME}/Library/Application Support/REAPER/Scripts/STEMwerk/scripts/reaper"

dest=""
if [[ -d "${HOME}/.config/REAPER" ]]; then
  dest="${linux_dest}"
elif [[ -d "${HOME}/Library/Application Support/REAPER" ]]; then
  dest="${mac_dest}"
else
  echo "Could not find a REAPER config directory in HOME."
  echo "Expected either:"
  echo "  ${HOME}/.config/REAPER"
  echo "  ${HOME}/Library/Application Support/REAPER"
  exit 1
fi

mkdir -p "${dest}"

cp -v "${src_dir}/STEMwerk.lua" "${dest}/STEMwerk.lua"
cp -v "${src_dir}/audio_separator_process.py" "${dest}/audio_separator_process.py"

echo
echo "Synced STEMwerk scripts to: ${dest}"
echo "Restart REAPER (or re-run the script) to pick up changes."


