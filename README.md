# STEMwerk

STEMwerk is a REAPER script that runs **Demucs-based stem separation** via a Python worker, with a REAPER-native UI, progress windows, debug logging, and **capability-driven device selection** (CPU / CUDA / ROCm / DirectML / MPS when available).

## Python interpreter: cross-platform & fallback

STEMwerk automatically looks for a suitable Python interpreter. For best compatibility on Windows, Linux, and macOS:

1. **Recommended:** Create a virtual environment in the repo root:
   - Windows: `.venv\Scripts\python.exe`
   - Linux/macOS: `.venv/bin/python3`
2. **Set the interpreter path explicitly** via the STEMwerk UI or config (pythonPath override). This avoids using a global Python by accident.
3. **Fallback order:**
   - First: user-configured pythonPath (config/ExtState)
   - Then: local .venv (platform-specific path)
   - Finally: `python3` or `python` on the system PATH

**Example detection logic:**
```lua
if user_configured_python then
  use(user_configured_python)
elseif os_is_windows then
  use(project_dir .. "\\.venv\\Scripts\\python.exe")
else
  use(project_dir .. "/.venv/bin/python3")
end
-- fallback:
use("python3")
```

**Note:**
Make sure all required Python packages are installed in the selected environment. See the install section below.

## Install / update in REAPER

### 1) Python environment (repo-local venv)
From repo root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements-ci.txt
```

Optional: verify backends:

```bash
python tools/gpu_check.py
```

### 2) Sync scripts into REAPER

```bash
bash scripts/reaper/sync_to_reaper.sh
```

### 3) Run in REAPER
- Run `STEMwerk.lua`
- Optional debug:
  - `STEMwerk_Enable_Debug.lua`
  - `STEMwerk_Disable_Debug.lua`

Logs:
- `/tmp/STEMwerk_debug.log` (when debug enabled)
- Per-run `separation_log.txt` inside the run folder (shown in the UI + written next to outputs)

## Testing guides (stability-first)
- `docs/TESTING_current_system_linux_amd_rocm.md`
- `docs/TESTING_nvidia_rtx3060_win11_arch_bazzite.md`
- `docs/TESTING_macbookpro11_2_ventura_oclp_arch.md`

## ROCm
- `docs/ROCm.md`

## Benchmarks
Benchmark notes live here:
- `tests/bench_results/README.md`