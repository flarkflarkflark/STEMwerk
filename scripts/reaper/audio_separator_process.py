#!/usr/bin/env python3 -u
"""
Audio Separator Script for STEMwerk
Uses audio-separator library for high-quality AI stem separation.

NOTE: The -u flag enables unbuffered stdout for real-time progress output.

Usage:
    python audio_separator_process.py <input.wav> <output_dir> [--model htdemucs] [--device auto|cpu|cuda: 0|cuda:1]

Models:
    - htdemucs (default): Facebook's Hybrid Transformer Demucs
    - htdemucs_ft: Fine-tuned version (better quality, slower)
    - htdemucs_6s: 6-stem model (adds guitar, piano)
    - UVR-MDX-NET-Voc_FT: Best for vocal isolation
    - Kim_Vocal_2:  Alternative vocal model

Device options:
    - auto:  Automatically select best available GPU (default)
    - cpu: Force CPU processing
    - cuda: 0: Use first GPU (e.g., RX 9070)
    - cuda: 1: Use second GPU (e.g., 780M)

Outputs:
    <output_dir>/vocals.wav
    <output_dir>/drums.wav
    <output_dir>/bass.wav
    <output_dir>/other.wav

Progress output (stdout):
    PROGRESS: <percent>: <stage>
    Example: PROGRESS:45:Processing chunk 3/8
"""

import sys
import os
import argparse
import json
import importlib
import platform
import subprocess
from pathlib import Path

_DEVICE_SKIPS = []


class _TeeTextIO:
    def __init__(self, *streams):
        self._streams = [s for s in streams if s is not None]

    def write(self, s):
        for st in self._streams:
            try:
                st.write(s)
            except Exception:
                pass
        return len(s)

    def flush(self):
        for st in self._streams:
            try:
                st.flush()
            except Exception:
                pass


_progress_file = None


def _setup_reaper_io(output_dir: str | None):
    """If output_dir is set, write progress/log/done markers into that folder.

    This lets REAPER launch Python without shell redirection (no console windows)
    while still providing real-time progress via stdout.txt.
    """
    global _progress_file
    if not output_dir:
        return None

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stdout_path = out / "stdout.txt"
    stderr_path = out / "separation_log.txt"
    done_path = out / "done.txt"

    # Truncate on each run so REAPER always reads fresh progress.
    stdout_f = open(stdout_path, "w", encoding="utf-8", buffering=1)
    stderr_f = open(stderr_path, "w", encoding="utf-8", buffering=1)
    _progress_file = stdout_f

    # Tee stderr so CLI users still see output.
    sys.stderr = _TeeTextIO(sys.stderr, stderr_f)

    def write_done(status: str):
        try:
            done_path.write_text(status + "\n", encoding="utf-8")
        except Exception:
            pass

    return write_done

def emit_progress(percent:  float, stage: str = ""):
    """Output progress in machine-readable format for C++ to parse."""
    line = f"PROGRESS:{int(percent)}:{stage}\n"
    # Write to REAPER progress file if configured.
    global _progress_file
    if _progress_file is not None:
        try:
            _progress_file.write(line)
            _progress_file.flush()
        except Exception:
            pass
    # Also write to stdout for normal CLI usage.
    try:
        sys.stdout.write(line)
        sys.stdout.flush()
    except Exception:
        pass

def get_available_devices():
    """Get list of available compute devices."""
    global _DEVICE_SKIPS
    _DEVICE_SKIPS = []
    # Always include stable choices so UIs can offer consistent selections.
    devices = [
        {"id": "auto", "name": "Auto", "type": "auto"},
        {"id": "cpu", "name": "CPU", "type": "cpu"},
    ]
    
    try:
        import torch
        is_linux = platform.system() == "Linux"
        torch_hip = None
        try:
            torch_hip = getattr(getattr(torch, "version", None), "hip", None)
        except Exception:
            torch_hip = None
        is_rocm = bool(is_linux and torch_hip)
        rocblas_lib_dir = Path("/opt/rocm/lib/rocblas/library")

        def _rocm_arches_from_rocminfo():
            """Best-effort list of GPU arch names (gfx...) in enumeration order."""
            try:
                p = subprocess.run(
                    ["rocminfo"],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=3.0,
                )
                txt = (p.stdout or "") + "\n" + (p.stderr or "")
            except Exception:
                return []

            arches = []
            in_agent = False
            is_gpu = False
            arch = None
            for raw in txt.splitlines():
                line = raw.strip()
                if line.startswith("Agent "):
                    # Flush previous agent
                    if in_agent and is_gpu and arch and isinstance(arch, str) and arch.startswith("gfx"):
                        arches.append(arch)
                    in_agent = True
                    is_gpu = False
                    arch = None
                    continue
                if not in_agent:
                    continue
                if line.startswith("Device Type:"):
                    # "Device Type: GPU"
                    is_gpu = ("GPU" in line)
                elif line.startswith("Name:"):
                    # "Name: gfx1103"
                    val = line.split(":", 1)[1].strip() if ":" in line else ""
                    if val:
                        arch = val
            # Flush last
            if in_agent and is_gpu and arch and isinstance(arch, str) and arch.startswith("gfx"):
                arches.append(arch)
            return arches

        def _device_rocm_arch(idx: int):
            # Prefer rocminfo ordering (most reliable), then fall back to torch properties if present.
            try:
                if not hasattr(_device_rocm_arch, "_rocminfo_arches"):
                    setattr(_device_rocm_arch, "_rocminfo_arches", _rocm_arches_from_rocminfo())
                arches = getattr(_device_rocm_arch, "_rocminfo_arches", []) or []
                if idx < len(arches):
                    return arches[idx]
            except Exception:
                pass
            try:
                props = torch.cuda.get_device_properties(idx)
                return getattr(props, "gcnArchName", None) or getattr(props, "gcnArch", None)
            except Exception:
                return None

        def _rocblas_has_tensile_for_arch(arch: str | None) -> bool:
            if not arch or not isinstance(arch, str):
                return True  # unknown -> don't block
            arch = arch.split(":", 1)[0].strip()
            if not arch.startswith("gfx"):
                return True
            try:
                if not rocblas_lib_dir.exists():
                    return True  # can't validate
                # If any Tensile library mentions this arch, assume supported.
                matches = list(rocblas_lib_dir.glob(f"*{arch}*.dat"))
                return len(matches) > 0
            except Exception:
                return True

        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                name = torch.cuda.get_device_name(i)
                if is_rocm:
                    arch = _device_rocm_arch(i)
                    if not _rocblas_has_tensile_for_arch(arch):
                        _DEVICE_SKIPS.append({
                            "id": f"cuda:{i}",
                            "name": name,
                            "reason": f"ROCm rocBLAS Tensile library missing for arch {arch} (see /opt/rocm/lib/rocblas/library).",
                        })
                        continue
                devices.append({
                    "id": f"cuda:{i}",
                    "name": name,
                    "type": "cuda"
                })

        # Apple MPS (macOS)
        try:
            if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
                devices.append({
                    "id": "mps",
                    "name": "Apple MPS",
                    "type": "mps"
                })
        except Exception:
            pass

        # Check for DirectML (AMD on Windows)
        try:
            import torch_directml
            # DirectML can have multiple devices (e.g., RX 9070 and 780M)
            dml_device_count = torch_directml.device_count()
            for i in range(dml_device_count):
                dml_device = torch_directml.device(i)
                device_name = f"DirectML GPU {i}"
                # Try to get device name if available
                try:
                    # DirectML doesn't always expose device names, but we can try
                    device_name = f"DirectML GPU {i}"
                except:
                    pass
                devices.append({
                    "id": f"directml:{i}" if dml_device_count > 1 else "directml",
                    "name": device_name,
                    "type": "directml"
                })
        except ImportError:
            pass
        except Exception:
            pass
            
        # Check for ROCm (AMD on Linux)
        if hasattr(torch, 'hip') or 'rocm' in torch.__version__.lower():
            # ROCm uses cuda-like interface
            pass  # Already captured above via cuda.is_available()
            
    except ImportError:
        pass
    
    return devices

def select_device(requested_device:  str = "auto"):
    """Select the compute device based on user preference."""
    import torch
    
    available = get_available_devices()
    available_ids = [d["id"] for d in available]
    skipped_ids = set([d.get("id") for d in (_DEVICE_SKIPS or []) if d.get("id")])
    
    if requested_device == "auto":
        # Prefer GPU over CPU
        for dev in available:
            if dev["type"] in ["cuda", "directml", "mps"]:
                return dev["id"], dev["name"]
        return "cpu", "CPU"
    
    elif requested_device == "cpu":
        return "cpu", "CPU"

    elif requested_device == "mps":
        try:
            if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
                return "mps", "Apple MPS"
        except Exception:
            pass
        print("WARNING:  MPS requested but not available, using CPU", file=sys.stderr)
        return "cpu", "CPU"
    
    elif requested_device in available_ids:
        for dev in available:
            if dev["id"] == requested_device:
                return dev["id"], dev["name"]

    # If user requested a specific CUDA/ROCm device but it is unavailable, fall back to the first usable CUDA device if any.
    if isinstance(requested_device, str) and requested_device.startswith("cuda:"):
        if requested_device in skipped_ids:
            # Provide extra hint for ROCm library issues.
            for s in (_DEVICE_SKIPS or []):
                if s.get("id") == requested_device:
                    print(f"WARNING: Requested device '{requested_device}' is not usable: {s.get('reason')}", file=sys.stderr)
                    break
        for dev in available:
            if dev.get("type") == "cuda" and isinstance(dev.get("id"), str) and dev["id"].startswith("cuda:"):
                print(f"WARNING: Requested device '{requested_device}' not available; falling back to {dev['id']}", file=sys.stderr)
                return dev["id"], dev["name"]

    # Fallback to CPU if requested device not found
    print(f"WARNING:  Requested device '{requested_device}' not available, using CPU", file=sys.stderr)
    return "cpu", "CPU"

def separate_stems(input_file: str, output_dir: str, model_name: str = "htdemucs", device_preference: str = "auto"):
    """
    Separate audio into stems using audio-separator.

    Args:
        input_file: Path to input audio file
        output_dir: Directory to write output stems
        model_name: Model to use for separation (htdemucs, htdemucs_ft, htdemucs_6s)
        device_preference: Device to use (auto, cpu, cuda:0, cuda:1, directml)

    Returns:
        dict: Paths to output stem files
    """
    from audio_separator.separator import Separator
    import threading
    import time

    # Map short names to full model names used by audio-separator
    model_mapping = {
        'htdemucs':  'htdemucs.yaml',
        'htdemucs_ft': 'htdemucs_ft.yaml',
        'htdemucs_6s': 'htdemucs_6s.yaml',
        'hdemucs_mmi': 'hdemucs_mmi.yaml',
    }

    full_model_name = model_mapping.get(model_name, model_name)
    os.makedirs(output_dir, exist_ok=True)

    emit_progress(0, "Initializing")
    print(f"Loading model: {full_model_name} (from {model_name})", file=sys.stderr)
    print(f"Input:  {input_file}", file=sys.stderr)
    print(f"Output:  {output_dir}", file=sys.stderr)

    # Select device
    import torch
    device, device_name = select_device(device_preference)
    print(f"Device preference: {device_preference}", file=sys.stderr)
    print(f"Selected device: {device} ({device_name})", file=sys.stderr)

    # IMPORTANT: Some downstream libs default to cuda:0 unless the process default device is set.
    # Enforce the requested CUDA/ROCm device index here so "cuda:1" really means device 1.
    if isinstance(device, str) and device.startswith("cuda:"):
        try:
            idx = int(device.split(":")[1])
            torch.cuda.set_device(idx)
            try:
                cur = torch.cuda.current_device()
                cur_name = torch.cuda.get_device_name(cur) if torch.cuda.is_available() else "n/a"
                print(f"STEMWERK: torch.cuda.set_device({idx}) -> current_device={cur} ({cur_name})", file=sys.stderr)
            except Exception:
                print(f"STEMWERK: torch.cuda.set_device({idx})", file=sys.stderr)
        except Exception as e:
            print(f"WARNING: Failed to set CUDA device '{device}': {e}", file=sys.stderr)
    
    # Show available devices
    available = get_available_devices()
    print(f"Available devices:", file=sys.stderr)
    for dev in available:
        marker = " <-- SELECTED" if dev["id"] == device else ""
        print(f"  - {dev['id']}:  {dev['name']}{marker}", file=sys.stderr)

    # Progress emitter thread for model loading phase
    loading_done = threading.Event()
    loading_progress = [0]

    def loading_progress_thread():
        start_time = time.time()
        while not loading_done.is_set():
            elapsed = time.time() - start_time
            progress_ratio = 1 - (0.5 ** (elapsed / 15))
            percent = int(1 + progress_ratio * 9)
            percent = min(10, percent)
            loading_progress[0] = percent

            if elapsed < 60:
                emit_progress(percent, f"Loading model ({elapsed:.0f}s) [{device_name}]")
            else: 
                mins = int(elapsed) // 60
                secs = int(elapsed) % 60
                emit_progress(percent, f"Loading model ({mins}:{secs:02d}) [{device_name}]")

            loading_done.wait(0.4)

    loading_worker = threading.Thread(target=loading_progress_thread, daemon=True)
    loading_worker.start()

    emit_progress(1, f"Initializing [{device_name}]")

    # Determine device parameters for separator
    # Handle different device types
    if device == "cpu":
        separator_device = "cpu"
    elif device == "mps":
        separator_device = "mps"
    elif device == "directml" or device.startswith("directml:"):
        # DirectML uses special handling for audio-separator
        # audio-separator expects "privateuseone:0" for DirectML
        try:
            import torch_directml
            if device == "directml":
                separator_device = "privateuseone:0"
            elif device.startswith("directml:"):
                # Extract device index: directml:0 -> privateuseone:0
                device_idx = device.split(":")[1]
                separator_device = f"privateuseone:{device_idx}"
            else:
                separator_device = "privateuseone:0"
        except ImportError:
            # If torch_directml is not installed, check whether ONNX Runtime DirectML is available
            try:
                ort_dml = _pkg_version("onnxruntime-directml") or _pkg_version("onnxruntime-gpu") or _pkg_version("onnxruntime")
            except Exception:
                ort_dml = None
            if ort_dml:
                # audio-separator will use ONNX Runtime + DirectML where available.
                # Use the privateuseone: namespace so downstream libs that look for DirectML
                # device strings still get a DirectML device reference.
                if device == "directml":
                    separator_device = "privateuseone:0"
                else:
                    device_idx = device.split(":")[1] if ":" in device else "0"
                    separator_device = f"privateuseone:{device_idx}"
                print(f"DirectML requested but torch-directml not installed; using ONNX Runtime DirectML (detected {ort_dml})", file=sys.stderr)
            else:
                separator_device = "cpu"
                print("WARNING: DirectML requested but neither torch-directml nor onnxruntime-directml are installed; using CPU", file=sys.stderr)
    else:
        # cuda:N or rocm:N format - pass through as-is
        separator_device = device

    # Initialize separator
    use_directml = isinstance(device, str) and device.startswith("directml")

    # Hint to ONNX Runtime which DirectML device to pick when multiple GPUs are present.
    if use_directml:
        try:
            os.environ["ORT_DML_DEFAULT_DEVICE_ID"] = str(int(device.split(":")[1])) if ":" in device else "0"
        except Exception:
            os.environ["ORT_DML_DEFAULT_DEVICE_ID"] = "0"

    separator = Separator(
        output_dir=output_dir,
        output_format="WAV",
        normalization_threshold=0.9,
        log_level=10,  # DEBUG
        use_directml=use_directml,
        mdx_params={"device": separator_device},
        demucs_params={"device": separator_device}
    )

    # Force the selected DirectML device index because audio-separator defaults to device 0.
    if use_directml:
        try:
            import torch_directml
            try:
                dml_index = int(device.split(":")[1]) if ":" in device else 0
            except Exception:
                dml_index = 0
            separator.torch_device = torch_directml.device(dml_index)
            separator.torch_device_dml = separator.torch_device
            print(f"STEMWERK: Forced DirectML device index {dml_index}", file=sys.stderr)
        except Exception as e:
            print(f"WARNING: Failed to force DirectML device: {e}", file=sys.stderr)

    # Report chosen backend for clarity (helps UIs show accurate tooltips)
    try:
        backend = "cpu"
        try:
            import torch_directml
            backend = "torch_directml"
        except Exception:
            # prefer ONNX/DirectML if available
            if _pkg_version("onnxruntime-directml") or _pkg_version("onnxruntime-gpu"):
                backend = "onnxruntime-directml"
        print(f"Backend selected: {backend}", file=sys.stderr)
    except Exception:
        pass

    emit_progress(3, f"Loading AI model [{device_name}]")

    # Load model
    separator.load_model(full_model_name)

    loading_done.set()
    loading_worker.join(timeout=1.0)

    emit_progress(11, f"Starting separation [{device_name}]")

    # Get audio duration for progress estimation
    duration_seconds = 0
    try:
        import soundfile as sf
        info = sf.info(input_file)
        duration_seconds = info.duration
        print(f"Audio duration: {duration_seconds:.1f}s", file=sys.stderr)
    except Exception: 
        duration_seconds = 180

    # Estimate processing time based on device
    if device == "cpu":
        estimated_time = duration_seconds * 4.0  # CPU is slower
        print("Using CPU - processing will be slower", file=sys.stderr)
    else:
        estimated_time = duration_seconds * 0.5  # GPU is faster
        print(f"Using GPU:  {device_name}", file=sys.stderr)

    print(f"Estimated processing time: {estimated_time:.0f}s", file=sys.stderr)

    # Progress emitter thread
    processing_done = threading.Event()

    def progress_thread():
        start_time = time.time()
        last_percent = 11

        while not processing_done.is_set():
            elapsed = time.time() - start_time
            if estimated_time > 0:
                progress_ratio = 1 - (0.5 ** (elapsed / estimated_time))
                percent = int(12 + progress_ratio * 76)
            else:
                percent = min(88, int(12 + elapsed * 2))

            percent = min(88, max(last_percent, percent))
            last_percent = percent

            mins_elapsed = int(elapsed) // 60
            secs_elapsed = int(elapsed) % 60

            if percent > 15:
                progress_fraction = (percent - 12) / 78.0
                if progress_fraction > 0.05:
                    total_est = elapsed / progress_fraction
                    remaining = max(0, total_est - elapsed)
                    mins_remaining = int(remaining) // 60
                    secs_remaining = int(remaining) % 60
                    eta_str = f" | ETA {mins_remaining}:{secs_remaining:02d}"
                else:
                    eta_str = ""
            else:
                eta_str = ""

            emit_progress(percent, f"Processing ({mins_elapsed}:{secs_elapsed:02d}{eta_str}) [{device_name}]")
            processing_done.wait(0.3)

    progress_worker = threading.Thread(target=progress_thread, daemon=True)
    progress_worker.start()

    print("Processing...", file=sys.stderr)
    try:
        output_files = separator.separate(input_file)
    finally:
        processing_done.set()
        progress_worker.join(timeout=1.0)

    emit_progress(92, "Writing stems")

    print(f"Raw output files: {output_files}", file=sys.stderr)

    # Rename outputs to standard names
    result = {}
    stem_mapping = {
        'vocals': ['vocals', 'vocal', 'Vocals'],
        'drums':  ['drums', 'drum', 'Drums'],
        'bass': ['bass', 'Bass'],
        'other': ['other', 'Other', 'no_vocals', 'instrumental', 'Instrumental'],
        'guitar': ['guitar', 'Guitar'],
        'piano': ['piano', 'Piano', 'keys', 'Keys']
    }

    for output_file in output_files: 
        if not os.path.isabs(output_file):
            output_file = os.path.join(output_dir, output_file)

        filename = Path(output_file).stem.lower()

        for stem_name, patterns in stem_mapping.items():
            for pattern in patterns: 
                if pattern.lower() in filename:
                    new_path = os.path.join(output_dir, f"{stem_name}.wav")
                    if output_file != new_path:
                        if os.path.exists(new_path):
                            os.remove(new_path)
                        import shutil
                        shutil.move(output_file, new_path)
                    result[stem_name] = new_path
                    print(f"  {stem_name}:  {new_path}", file=sys.stderr)
                    break

    emit_progress(100, "Complete")
    return result

def check_installation():
    """Check if audio-separator is properly installed."""
    try:
        from audio_separator.separator import Separator
        import torch

        print(f"audio-separator:  OK", file=sys.stderr)
        print(f"PyTorch: {torch.__version__}", file=sys.stderr)
        print(f"CUDA available: {torch.cuda.is_available()}", file=sys.stderr)

        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                print(f"GPU {i}:  {torch.cuda.get_device_name(i)}", file=sys.stderr)
        
        # Check DirectML
        try:
            import torch_directml
            print(f"DirectML:  Available", file=sys.stderr)
        except ImportError: 
            print(f"DirectML: Not installed (pip install torch-directml)", file=sys.stderr)

        return True
    except ImportError as e: 
        print(f"ERROR: {e}", file=sys.stderr)
        print("\nInstall with: pip install audio-separator[gpu]", file=sys.stderr)
        return False

def list_devices():
    """List all available compute devices."""
    devices = get_available_devices()
    print("Available devices:")
    for dev in devices:
        print(f"  {dev['id']}:  {dev['name']} ({dev['type']})")
    return devices


def _pkg_version(dist_name: str):
    """Return installed version for a distribution name (best-effort)."""
    try:
        try:
            from importlib.metadata import version  # py3.8+
        except Exception:
            from importlib_metadata import version  # type: ignore
        return version(dist_name)
    except Exception:
        return None


def list_devices_machine():
    """Machine-readable dump for REAPER/Lua UIs (no JSON parser needed on Lua side)."""
    devices = get_available_devices()
    print("STEMWERK_DEVICES_BEGIN")
    for d in devices:
        # Tab-separated: id, name, type
        print(f"STEMWERK_DEVICE\t{d.get('id','')}\t{d.get('name','')}\t{d.get('type','')}")
    # Report skipped devices (e.g. ROCm GPU arch unsupported by installed rocBLAS).
    for s in (_DEVICE_SKIPS or []):
        sid = s.get("id", "")
        sname = s.get("name", "")
        reason = s.get("reason", "")
        # Keep it parse-safe: no tabs.
        reason = str(reason).replace("\t", " ")
        print(f"STEMWERK_DEVICE_SKIPPED\t{sid}\t{sname}\t{reason}")

    env = {
        "platform": platform.system(),
        "python": platform.python_version(),
        "sys_executable": sys.executable,
        "pythonpath_env": os.environ.get("PYTHONPATH"),
        "ld_library_path_env": os.environ.get("LD_LIBRARY_PATH"),
        "torch": None,
        "torch_file": None,
        "cuda_available": False,
        "cuda_count": 0,
        "mps_available": False,
        "directml_possible": importlib.util.find_spec("torch_directml") is not None,
        "rocm_path_exists": False,
        "torch_hip": None,
        # ORT packages (audio-separator checks these)
        "onnxruntime": _pkg_version("onnxruntime"),
        "onnxruntime-gpu": _pkg_version("onnxruntime-gpu"),
        "onnxruntime-directml": _pkg_version("onnxruntime-directml"),
        "onnxruntime-silicon": _pkg_version("onnxruntime-silicon"),
    }
    try:
        env["rocm_path_exists"] = bool(os.path.exists("/opt/rocm") or os.environ.get("ROCM_PATH"))
    except Exception:
        env["rocm_path_exists"] = False
    try:
        import torch
        env["torch"] = getattr(torch, "__version__", str(torch))
        try:
            env["torch_file"] = getattr(torch, "__file__", None)
        except Exception:
            env["torch_file"] = None
        try:
            env["torch_hip"] = getattr(getattr(torch, "version", None), "hip", None)
        except Exception:
            env["torch_hip"] = None
        try:
            env["cuda_available"] = bool(torch.cuda.is_available())
        except Exception:
            env["cuda_available"] = False
        try:
            env["cuda_count"] = int(torch.cuda.device_count()) if env["cuda_available"] else 0
        except Exception:
            env["cuda_count"] = 0
        try:
            env["mps_available"] = bool(getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available())
        except Exception:
            env["mps_available"] = False
    except Exception:
        pass

    print("STEMWERK_ENV_JSON " + json.dumps(env, ensure_ascii=False))
    print("STEMWERK_DEVICES_END")

def main():
    parser = argparse.ArgumentParser(description="Audio Separator for STEMwerk")
    parser.add_argument("input", nargs="?", help="Input audio file")
    parser.add_argument("output_dir", nargs="?", help="Output directory for stems")
    parser.add_argument("--model", default="htdemucs",
                        help="Model to use (htdemucs, htdemucs_ft, htdemucs_6s, etc.)")
    parser.add_argument("--device", default="auto",
                        help="Device to use:  auto, cpu, cuda:0, cuda: 1, directml")
    parser.add_argument("--check", action="store_true",
                        help="Only check installation, don't process")
    parser.add_argument("--list-models", action="store_true",
                        help="List available models")
    parser.add_argument("--list-devices", action="store_true",
                        help="List available compute devices")
    parser.add_argument("--list-devices-machine", action="store_true",
                        help="List available devices in a machine-readable format (for REAPER UIs)")

    args = parser.parse_args()

    # If called from REAPER, we want progress/log/done markers in output_dir.
    # Do this early so any diagnostic prints are captured into separation_log.txt.
    write_done = _setup_reaper_io(args.output_dir if args.output_dir else None)

    # If the user explicitly requests CPU, make that a hard requirement by hiding GPU devices
    # BEFORE any torch import happens. This avoids "CPU selected but torch still uses GPU"
    # behavior in downstream libs on ROCm/CUDA setups.
    if str(getattr(args, "device", "auto")).lower() == "cpu":
        for k in ("CUDA_VISIBLE_DEVICES", "HIP_VISIBLE_DEVICES", "ROCR_VISIBLE_DEVICES"):
            os.environ[k] = ""
        print("STEMWERK: CPU mode requested; masked GPU visibility via CUDA_VISIBLE_DEVICES/HIP_VISIBLE_DEVICES/ROCR_VISIBLE_DEVICES", file=sys.stderr)

    if args.check:
        if check_installation():
            print("\nInstallation OK!")
            list_devices()
            sys.exit(0)
        else:
            sys.exit(1)

    if args.list_devices:
        list_devices()
        sys.exit(0)
    if args.list_devices_machine:
        list_devices_machine()
        sys.exit(0)

    if args.list_models: 
        print("Popular models:")
        print("  htdemucs - Hybrid Transformer Demucs (default, fast)")
        print("  htdemucs_ft - Fine-tuned Demucs (better quality)")
        print("  htdemucs_6s - 6-stem model (guitar, piano)")
        print("  UVR-MDX-NET-Voc_FT - Best vocal isolation")
        print("  Kim_Vocal_2 - Alternative vocal model")
        sys.exit(0)

    if not args.input or not args.output_dir:
        parser.print_help()
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        output_files = separate_stems(args.input, args.output_dir, args.model, args.device)
        print(json.dumps(output_files))

        if write_done:
            write_done("DONE")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        if write_done:
            # Ensure REAPER doesn't hang on errors.
            write_done("ERROR")
        sys.exit(1)

if __name__ == "__main__": 
    main()
