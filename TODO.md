# STEMwerk TODO

This file is intentionally tracked in git so "what's next" survives VS Code / Copilot chat sessions.

## Current

- [x] Run pytest + i18n checks
- [x] Verify CI workflow passes (replicated locally)
- [x] Align Lua @version with APP_VERSION
- [x] Decide default DEBUG_MODE behavior
- [x] Sanity-check Python path auto-detect
- [ ] Re-test REAPER UI scaling/status
- [x] Confirm DirectML/device options docs

- [ ] ASAP: Build downloadable installers for testing on macOS + Windows + Linux
	- Goal: download from GitHub (Releases/Artifacts), install, and run setup + REAPER scripts
	- Windows: .msi or .exe
	- macOS: .pkg
	- Linux: AppImage and/or .deb

### REAPER UI scaling/status checklist

- [ ] Open `Stemwerk: Main` and resize the window (corners + edges)
- [ ] Verify all controls scale and remain clickable (checkboxes, presets, device/model dropdowns)
- [ ] Verify text does not overlap or clip at small + large sizes
- [ ] Verify progress/status area stays visible during separation
- [ ] Verify reopening restores last window size/position (ExtState)
- [ ] Verify focus behavior: running script again focuses existing window (unless quick preset)
- [ ] Verify quick presets from toolbar run without showing dialog (Karaoke/Vocals/Drums/Bass/All)

## TODO

Toolbar + Icons + Toolbarscripts:

| Script | Description |
|--------|-------------|
| **Stemwerk:** | Main dialog - full control over model, stems, and options |
| **Stemwerk: Karaoke** | One-click vocal removal (keeps drums, bass, other) |
| **Stemwerk: Vocals Only** | Extract vocals to new track |
| **Stemwerk: Drums Only** | Extract drums to new track |
| **Stemwerk: Bass Only** | Extract bass to new track |
| **Stemwerk: All Stems** | Extract all stems to separate tracks |
| **Stemwerk: Setup Toolbar** | Add quick-access toolbar buttons |

## Future

- (After installers exist) Add “novice mode” UX: guided install outside REAPER, minimal prompts, clear GPU choice
