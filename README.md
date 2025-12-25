# STEMwerk

STEMwerk is a REAPER script that runs **Demucs-based stem separation** via a Python worker, with a REAPER-native UI, progress windows, debug logging, and **capability-driven device selection** (CPU / CUDA / ROCm / DirectML / MPS when available).


## Python interpreter: cross-platform & fallback

STEMwerk zoekt automatisch naar een geschikte Python-interpreter. Voor maximale compatibiliteit op Windows, Linux en macOS:

1. **Aanbevolen:** Maak een virtuele omgeving aan in de repo-root:
   - Windows: `.venv\Scripts\python.exe`
   - Linux/macOS: `.venv/bin/python3`
2. **Stel het pad naar de interpreter expliciet in** via de STEMwerk UI of config (pythonPath override). Dit voorkomt dat een globale Python wordt gebruikt.
3. **Fallback-volgorde:**
   - Eerst: expliciet opgegeven pythonPath (config/ExtState)
   - Dan: lokale .venv (platformspecifiek pad)
   - Daarna: `python3` of `python` in het systeem-PATH

**Voorbeeld detectielogica:**
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

**Let op:**
Zorg dat alle benodigde Python-pakketten in de gekozen omgeving zijn geïnstalleerd. Zie ook de sectie hieronder voor installatie-instructies.

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

