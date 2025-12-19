# STEMwerk

STEMwerk is a REAPER script that runs **Demucs-based stem separation** via a Python worker, with a REAPER-native UI, progress windows, debug logging, and **capability-driven device selection** (CPU / CUDA / ROCm / DirectML / MPS when available).

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

