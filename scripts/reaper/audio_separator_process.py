#!/home/flark/STEMwerk/.venv/bin/python -u
"""
Audio Separator Script for STEMwerk
Thin wrapper around stemwerk-core for REAPER.

Progress output (stdout):
    PROGRESS:<percent>:<stage>
    Example: PROGRESS:45:Processing chunk 3/8
"""

import argparse
import importlib
import importlib.util
import json
import os
import platform
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

from stemwerk_core import StemSeparator, get_available_devices
from stemwerk_core import devices as core_devices


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


def _setup_reaper_io(output_dir: Optional[str]):
    """If output_dir is set, write progress/log/done markers into that folder."""
    global _progress_file
    if not output_dir:
        return None

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stdout_path = out / "stdout.txt"
    stderr_path = out / "separation_log.txt"
    done_path = out / "done.txt"

    stdout_f = open(stdout_path, "w", encoding="utf-8", buffering=1)
    stderr_f = open(stderr_path, "w", encoding="utf-8", buffering=1)
    _progress_file = stdout_f

    sys.stderr = _TeeTextIO(sys.stderr, stderr_f)

    def write_done(status: str):
        try:
            done_path.write_text(status + "\n", encoding="utf-8")
        except Exception:
            pass

    return write_done


def emit_progress(percent: float, stage: str = ""):
    """Output progress in machine-readable format for Lua to parse."""
    line = f"PROGRESS:{int(percent)}:{stage}\n"
    global _progress_file
    if _progress_file is not None:
        try:
            _progress_file.write(line)
            _progress_file.flush()
        except Exception:
            pass
    try:
        sys.stdout.write(line)
        sys.stdout.flush()
    except Exception:
        pass


def _split_list(value: Optional[str]) -> List[str]:
    if not value:
        return []
    text = str(value)
    for sep in (";", "\n", "\t", " "):
        text = text.replace(sep, ",")
    return [part.strip() for part in text.split(",") if part.strip()]


def _get_device_skips() -> List[Dict[str, str]]:
    skips = getattr(core_devices, "_DEVICE_SKIPS", None)
    if not skips:
        return []
    return [dict(item) for item in skips]


def _build_env_json() -> Dict[str, object]:
    env: Dict[str, object] = {
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
        "onnxruntime": None,
        "onnxruntime-gpu": None,
        "onnxruntime-directml": None,
        "onnxruntime-silicon": None,
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
            env["mps_available"] = bool(
                getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available()
            )
        except Exception:
            env["mps_available"] = False
    except Exception:
        pass

    try:
        try:
            from importlib.metadata import version as dist_version
        except Exception:
            from importlib_metadata import version as dist_version  # type: ignore

        def _dist(name: str) -> Optional[str]:
            try:
                return dist_version(name)
            except Exception:
                return None

        env["onnxruntime"] = _dist("onnxruntime")
        env["onnxruntime-gpu"] = _dist("onnxruntime-gpu")
        env["onnxruntime-directml"] = _dist("onnxruntime-directml")
        env["onnxruntime-silicon"] = _dist("onnxruntime-silicon")
    except Exception:
        pass

    return env


def list_devices_machine(skip_devices: Optional[Set[str]] = None):
    """Machine-readable dump for REAPER/Lua UIs (no JSON parser needed on Lua side)."""
    devices = get_available_devices()
    if skip_devices:
        devices = [d for d in devices if d.get("id") not in skip_devices]

    print("STEMWERK_DEVICES_BEGIN")
    for d in devices:
        print(f"STEMWERK_DEVICE\t{d.get('id','')}\t{d.get('name','')}\t{d.get('type','')}")

    for s in _get_device_skips():
        sid = s.get("id", "")
        sname = s.get("name", "")
        reason = s.get("reason", "")
        reason = str(reason).replace("\t", " ")
        print(f"STEMWERK_DEVICE_SKIPPED\t{sid}\t{sname}\t{reason}")

    env = _build_env_json()
    print("STEMWERK_ENV_JSON " + json.dumps(env, ensure_ascii=False))
    print("STEMWERK_DEVICES_END")


def list_devices(skip_devices: Optional[Set[str]] = None):
    """List all available compute devices."""
    devices = get_available_devices()
    if skip_devices:
        devices = [d for d in devices if d.get("id") not in skip_devices]
    print("Available devices:")
    for dev in devices:
        print(f"  {dev['id']}:  {dev['name']} ({dev['type']})")
    return devices


def check_installation():
    """Check if stemwerk-core and audio-separator are properly installed."""
    try:
        from audio_separator.separator import Separator  # noqa: F401
        import torch

        print("audio-separator:  OK", file=sys.stderr)
        print(f"PyTorch: {torch.__version__}", file=sys.stderr)
        print(f"CUDA available: {torch.cuda.is_available()}", file=sys.stderr)

        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                print(f"GPU {i}:  {torch.cuda.get_device_name(i)}", file=sys.stderr)

        try:
            import torch_directml
            print("DirectML:  Available", file=sys.stderr)
        except ImportError:
            print("DirectML: Not installed (pip install torch-directml)", file=sys.stderr)

        return True
    except ImportError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("\nInstall with: pip install stemwerk-core", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Audio Separator for STEMwerk")
    parser.add_argument("input", nargs="?", help="Input audio file")
    parser.add_argument("output_dir", nargs="?", help="Output directory for stems")
    parser.add_argument("--model", default="htdemucs",
                        help="Model to use (htdemucs, htdemucs_ft, htdemucs_6s, etc.)")
    parser.add_argument("--device", default="auto",
                        help="Device to use:  auto, cpu, cuda:0, cuda: 1, directml")
    parser.add_argument("--stems", default="",
                        help="Optional comma-separated stems (vocals, drums, bass, other, guitar, piano)")
    parser.add_argument("--env-json", action="store_true",
                        help="Emit STEMWERK_ENV_JSON and device list for Lua")
    parser.add_argument("--skip-devices", default="",
                        help="Comma-separated device ids to skip")
    parser.add_argument("--check", action="store_true",
                        help="Only check installation, don't process")
    parser.add_argument("--list-models", action="store_true",
                        help="List available models")
    parser.add_argument("--list-devices", action="store_true",
                        help="List available compute devices")
    parser.add_argument("--list-devices-machine", action="store_true",
                        help="List available devices in a machine-readable format (for REAPER UIs)")

    args = parser.parse_args()

    write_done = _setup_reaper_io(args.output_dir if args.output_dir else None)

    skip_devices = set(_split_list(args.skip_devices))

    if args.env_json or args.list_devices_machine:
        list_devices_machine(skip_devices)
        return 0

    if args.check:
        if check_installation():
            print("\nInstallation OK!")
            list_devices(skip_devices)
            return 0
        return 1

    if args.list_devices:
        list_devices(skip_devices)
        return 0

    if args.list_models:
        print("Popular models:")
        print("  htdemucs - Hybrid Transformer Demucs (default, fast)")
        print("  htdemucs_ft - Fine-tuned Demucs (better quality)")
        print("  htdemucs_6s - 6-stem model (guitar, piano)")
        print("  UVR-MDX-NET-Voc_FT - Best vocal isolation")
        print("  Kim_Vocal_2 - Alternative vocal model")
        return 0

    if not args.input or not args.output_dir:
        parser.print_help()
        return 1

    if not os.path.exists(args.input):
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        return 1

    device_preference = args.device
    if device_preference in skip_devices:
        print(f"WARNING: Device '{device_preference}' skipped; using auto", file=sys.stderr)
        device_preference = "auto"

    stems = _split_list(args.stems)

    try:
        sep = StemSeparator(model=args.model, device=device_preference)

        def reaper_progress(pct: float, msg: str):
            emit_progress(pct, msg)

        sep.on_progress = reaper_progress

        result = sep.separate(args.input, args.output_dir, stems=stems or None)
        output_files = {name: str(path) for name, path in result.stems.items()}
        print(json.dumps(output_files))

        if write_done:
            write_done("DONE")

        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        if write_done:
            write_done("ERROR")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
