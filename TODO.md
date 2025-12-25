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
- [ ] Help: add "Reaper" menu entry with a page for temp files + settings

- [ ] REAPER progress/complete UI polish
	- [x] Progress: model badge aligned with progress bar (no overflow)
	- [x] Progress: ETA parsing tolerant of stray spaces (no more "ETA: 2:")
	- [x] Progress: device indicator reflects actual runtime device (no "GPU: DirectML" on Linux)
	- [x] Progress: CPU not highlighted as GPU; ETA not always green
	- [x] Progress: Nerd Mode button moved so it doesn't overlap "Elapsed:"
	- [x] Complete: add FX icon toggle near theme icon
	- [x] Complete: remove Space as a close/OK key
	- [x] i18n: Nerd Mode tooltip strings
	- [ ] Complete: verify all header tooltips consistent with main/progress windows

- [ ] REAPER time-selection workflow correctness
	- [x] Fix multi-track render producing empty `input.wav` (ffmpeg log + AudioAccessor fallback)
	- [x] Multi-track: refuse to launch job when per-track `input.wav` is empty
	- [x] Time selection + "Mute sel": if nothing is selected, operate on overlapping items (auto semantics)

- [ ] REAPER UI: merge language/day-night/FX into 1 icon + add TT (tooltips) toggle

- [ ] Linux AMD GPUs: ROCm support (if hardware/driver supports it)
	- Detect ROCm availability (e.g. `/opt/rocm`, `torch.version.hip`, `rocminfo`)
	- Install/guide correct ROCm-enabled PyTorch wheels for the user’s distro/ROCm version
	- Ensure `audio_separator_process.py` reports usable GPU devices under ROCm (often via `torch.cuda`)
	- Update device UI/tooltips to explain ROCm requirements + fallback behavior

- [ ] Test matrix: NVIDIA RTX 3060 laptop (Windows + Linux)
	- Fresh clone + venv setup
	- Install GPU backend (CUDA torch) and verify via `python tools/gpu_check.py`
	- Install REAPER scripts + verify device probe shows `cuda:0`
	- Run short separation test (time selection) and confirm log says `Using GPU`
	- Validate multi-track mode + cancel behavior
	- Validate tooltips + i18n + window placement on both OSes

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
