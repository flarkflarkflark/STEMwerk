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
from pathlib import Path

def emit_progress(percent:  float, stage: str = ""):
    """Output progress in machine-readable format for C++ to parse."""
    sys.stdout.write(f"PROGRESS:{int(percent)}:{stage}\n")
    sys.stdout.flush()

def get_available_devices():
    """Get list of available compute devices."""
    devices = [{"id": "cpu", "name": "CPU", "type": "cpu"}]
    
    try:
        import torch
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                name = torch.cuda.get_device_name(i)
                devices.append({
                    "id": f"cuda:{i}",
                    "name": name,
                    "type": "cuda"
                })
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
    
    if requested_device == "auto":
        # Prefer GPU over CPU
        for dev in available:
            if dev["type"] in ["cuda", "directml"]:
                return dev["id"], dev["name"]
        return "cpu", "CPU"
    
    elif requested_device == "cpu":
        return "cpu", "CPU"
    
    elif requested_device in available_ids:
        for dev in available:
            if dev["id"] == requested_device:
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
            separator_device = "cpu"
            print("WARNING: DirectML requested but torch-directml not installed, using CPU", file=sys.stderr)
    else:
        # cuda:N or rocm:N format - pass through as-is
        separator_device = device

    # Initialize separator
    separator = Separator(
        output_dir=output_dir,
        output_format="WAV",
        normalization_threshold=0.9,
        log_level=10,  # DEBUG
        mdx_params={"device": separator_device},
        demucs_params={"device": separator_device}
    )

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
                    eta_str = f" | ETA {mins_remaining}:{secs_remaining: 02d}"
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

    args = parser.parse_args()

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

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__": 
    main()