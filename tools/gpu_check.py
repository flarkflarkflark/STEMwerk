#!/usr/bin/env python3
"""
Lightweight GPU/runtime detection and quick tensor benchmark.
Writes results to stdout and `gpu_check.json`.

Run inside your project's venv: `python tools/gpu_check.py`
"""
import json
import platform
import subprocess
import sys
import os
import time


def run_cmd(cmd):
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True, text=True)
        return out.strip()
    except Exception:
        return None


info = {
    "platform": platform.system(),
    "platform_release": platform.release(),
    "python": platform.python_version(),
    "torch": None,
    "cuda_available": False,
    "cuda_version": None,
    "nvidia_smi": None,
    "rocm_detected": False,
    "mps_available": False,
    "directml_possible": False,
    "quick_benchmark": {},
}

# Try import torch
try:
    import torch
    info["torch"] = getattr(torch, "__version__", str(torch))
    try:
        info["cuda_available"] = torch.cuda.is_available()
    except Exception:
        info["cuda_available"] = False
    try:
        info["cuda_version"] = torch.version.cuda
    except Exception:
        info["cuda_version"] = None
    try:
        info["mps_available"] = getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available()
    except Exception:
        info["mps_available"] = False
except Exception as e:
    info["torch_error"] = str(e)

# nvidia-smi
n = run_cmd("nvidia-smi -L") or run_cmd("nvidia-smi --query-gpu=name --format=csv,noheader")
if n:
    info["nvidia_smi"] = n

# ROCm hint
if os.path.exists("/opt/rocm") or os.environ.get("ROCM_PATH"):
    info["rocm_detected"] = True

# DirectML hint (torch-directml)
try:
    import importlib
    info["directml_possible"] = importlib.util.find_spec("torch_directml") is not None
except Exception:
    info["directml_possible"] = False


def try_benchmark(device):
    res = {"device": device, "ok": False}
    try:
        import torch
        dtype = torch.float32
        # handle DirectML device object via torch_directml
        if device == "dml":
            try:
                import torch_directml
                d = torch_directml.device()
            except Exception as e:
                res["error"] = f"torch_directml import/device error: {e}"
                return res
            a = torch.randn((1024, 1024), device=d, dtype=dtype)
            b = torch.randn((1024, 1024), device=d, dtype=dtype)
            # run and time; DirectML may not expose a synchronize API similar to CUDA
            t0 = time.time()
            c = torch.matmul(a, b)
            # best-effort wait briefly to let compute dispatch
            time.sleep(0.05)
            t1 = time.time()
        else:
            # device may be 'cpu', 'mps' or 'cuda:0'
            a = torch.randn((1024, 1024), device=device, dtype=dtype)
            b = torch.randn((1024, 1024), device=device, dtype=dtype)
            if isinstance(device, str) and device.startswith("cuda"):
                torch.cuda.synchronize()
            t0 = time.time()
            c = torch.matmul(a, b)
            if isinstance(device, str) and device.startswith("cuda"):
                torch.cuda.synchronize()
            t1 = time.time()

        res["time_s"] = t1 - t0
        res["ok"] = True
    except Exception as e:
        res["error"] = str(e)
    return res


# device priority for quick benchmark
devices = []
if info.get("cuda_available"):
    devices.append("cuda:0")
if info.get("mps_available"):
    devices.append("mps")
if info.get("directml_possible"):
    devices.append("dml")
# always include cpu
devices.append("cpu")

for d in devices:
    bench = try_benchmark(d)
    info["quick_benchmark"][d] = bench
    if bench.get("ok"):
        # stop after first working device benchmark
        break

print(json.dumps(info, indent=2))
try:
    with open("gpu_check.json", "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)
except Exception:
    pass
