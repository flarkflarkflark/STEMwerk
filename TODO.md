# STEMwerk TODO

This file is intentionally tracked in git so "what's next" survives VS Code / Copilot chat sessions.

## Current

- [x] Run pytest + i18n checks
- [x] Verify CI workflow passes (replicated locally)
- [x] Align Lua @version with APP_VERSION
- [x] Decide default DEBUG_MODE behavior
- [x] Sanity-check Python path auto-detect
- [ ] Re-test REAPER UI scaling/status
- [ ] Confirm DirectML/device options docs

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

- OS-level installer for non-REAPER / inexperienced users (guided install outside REAPER)
	- Windows: .msi or .exe installer
	- macOS: .pkg installer
	- Linux: distro-friendly package (e.g. .deb/.rpm) or AppImage
