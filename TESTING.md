# STEMwerk Testing Guide

Comprehensive testing documentation for REAPER scripts and audio separation workflows across Windows, macOS, and Linux.

## Overview

STEMwerk includes automated test infrastructure to validate:
- REAPER script integration
- Audio separation quality (vocals, drums, bass, other, guitar, piano)
- Time selection and media item handling
- Cross-platform compatibility
- Model performance (htdemucs, htdemucs_ft, htdemucs_6s)

## Quick Start

### Prerequisites

- Python 3.9+ with `numpy` and `soundfile`
- REAPER installed (for local testing)
- ffmpeg (for separation backend)

```bash
# Install test dependencies
pip install numpy soundfile pytest

# Generate test assets
python tests/reaper/generate_test_audio.py
```

### Run Local Tests

**Windows:**
```powershell
# Quick smoke tests (2 scenarios)
.\scripts\test\run-reaper-test.ps1 quick

# Full test suite (4 scenarios)
.\scripts\test\run-reaper-test.ps1 full

# Heavy tests with 6-stem model
.\scripts\test\run-reaper-test.ps1 heavy

# Or run directly
python tests/reaper/run_reaper_test.py --reaper-path "C:\Program Files\REAPER\reaper.exe" --filter quick
```

**Linux/macOS:**
```bash
# Make launcher executable
chmod +x scripts/test/run-reaper-test.sh

# Run tests
./scripts/test/run-reaper-test.sh quick
./scripts/test/run-reaper-test.sh full

# Or run directly
python3 tests/reaper/run_reaper_test.py --reaper-path "/opt/REAPER/reaper" --filter quick
```

## Test Scenarios

### Quick Smoke Tests (CI-friendly)

#### 1. Karaoke (Full Item)
- **Goal:** Remove vocals from complete media item
- **Expected stems:** drums, bass, other
- **Selection:** Full media item (10s)
- **Validates:** Stem count, duration, sample rate, RMS levels

#### 2. Vocals Only (Time Selection)
- **Goal:** Extract vocals from 4-bar time selection
- **Expected stems:** vocals
- **Selection:** Time range 2.0s - 6.0s
- **Validates:** Precise time-based extraction

### Full Test Suite

Includes quick tests plus:

#### 3. Drums Only
- **Goal:** Isolate drums for reference or sampling
- **Expected stems:** drums
- **Use case:** Extract drum loop from full mix

#### 4. All Stems (htdemucs)
- **Goal:** Complete 4-stem separation
- **Expected stems:** vocals, drums, bass, other
- **Model:** htdemucs (balanced speed/quality)

### Heavy Tests (Manual/Scheduled)

#### 5. Six-Stem (htdemucs_6s)
- **Goal:** Detailed separation with guitar and piano
- **Expected stems:** vocals, drums, bass, other, guitar, piano
- **Model:** htdemucs_6s (slower, more detailed)

#### 6. Intersection (Surgical Edit)
- **Goal:** Extract bass from specific 2-second region
- **Selection:** Time + item intersection (3.0s - 5.0s)
- **Use case:** Remove unwanted bass bleed from sample

## Test Architecture

### Components

```
tests/reaper/
 test_scenarios.json        # Test definitions with validation rules
 generate_test_audio.py     # Creates synthetic multi-stem audio
 generate_rpp.py            # Creates REAPER project files
 run_reaper_test.py         # Main test harness
 assets/                    # Generated test audio (ignored)
    test_mix_10s.wav
    test_mix_5s.wav
 output/                    # Test results (ignored)
     <scenario_name>/
         test_mix_10s_vocals.wav
         test_mix_10s_drums.wav
         ...

scripts/test/
 run-reaper-test.ps1        # Windows launcher
 run-reaper-test.sh         # Linux/macOS launcher
```

### Test Flow

1. **Load scenarios** from `test_scenarios.json`
2. **Generate test assets** (synthetic audio with known components)
3. **Create REAPER projects** with media items and time selections
4. **Invoke separation** (simulated or actual backend)
5. **Validate outputs:**
   - File existence
   - Stem count matches expected
   - Duration within tolerance (0.2s)
   - Sample rate matches source
   - RMS above silence threshold (-60dB)

## CI/CD Integration

### GitHub Actions Workflows

#### 1. REAPER Cross-Platform Tests (`ci-reaper.yml`)
- **Trigger:** Push to main, pull requests
- **Platforms:** ubuntu-latest, macos-latest, windows-latest
- **Validates:**
  - Test scenarios JSON structure
  - Asset generation (synthetic audio)
  - .rpp project generation
  - Test infrastructure integrity
- **Note:** Does NOT run full separation (REAPER not installed on runners)

#### 2. CI Full (`ci-full.yml`)
- **Trigger:** Push, pull requests
- **Tests:** Python unit tests for separation backend
- **Fast:** Installs only pytest, soundfile (no heavy ML packages)

#### 3. CI Heavy (`ci-heavy.yml`)
- **Trigger:** Manual dispatch, weekly schedule
- **Tests:** Full `audio-separator[cpu]` install with model checks
- **Heavy:** Downloads ~2GB models

### Artifacts

CI uploads test assets for inspection:
- `test-assets-windows-latest.zip`
- `test-assets-ubuntu-latest.zip`
- `test-assets-macos-latest.zip`

Contains:
- Generated .wav files
- .rpp project files
- Separation outputs (if available)

## Adding New Tests

### 1. Define Scenario

Edit `tests/reaper/test_scenarios.json`:

```json
{
  "name": "bass_only_time_selection",
  "description": "Extract bass from 2-bar section",
  "script": "STEMwerk_AI_Separate.lua",
  "args": ["--stem", "bass"],
  "selection_type": "time_selection",
  "time_range": [4.0, 6.0],
  "expected_stems": ["bass"],
  "duration_sec": 2,
  "validate": {
    "stem_count": 1,
    "min_duration_sec": 1.8,
    "max_duration_sec": 2.2,
    "min_rms_db": -60,
    "check_sample_rate": 44100
  }
}
```

### 2. Add to Test Sets

Update `quick_smoke_tests`, `full_tests`, or `heavy_tests` arrays:

```json
"quick_smoke_tests": ["karaoke_full_item", "vocals_only_time_selection", "bass_only_time_selection"]
```

### 3. Run Locally

```bash
python tests/reaper/run_reaper_test.py --filter quick
```

### 4. Commit and Push

```bash
git add tests/reaper/test_scenarios.json
git commit -m "Add bass-only time selection test"
git push
```

## Validation Rules

### Required Fields

- `stem_count`: Expected number of output files
- `min_duration_sec` / `max_duration_sec`: Duration tolerance
- `min_rms_db`: Minimum RMS level (detects silence/errors)

### Optional Fields

- `check_sample_rate`: Verify output sample rate
- `max_file_size_mb`: Detect runaway file sizes
- `min_snr_db`: Signal-to-noise ratio (if reference available)

## Troubleshooting

### Test Failures

**"REAPER not found"**
```bash
# Specify path explicitly
python tests/reaper/run_reaper_test.py --reaper-path "/path/to/reaper.exe"
```

**"Test asset missing"**
```bash
# Regenerate assets
python tests/reaper/generate_test_audio.py
```

**"Validation failed: duration outside range"**
- Check if separation respects time selections
- Verify .rpp project has correct SELECTION markers
- Inspect output files: `tests/reaper/output/<scenario_name>/`

**"RMS below threshold"**
- Output file is silent or corrupted
- Check separation backend logs
- Verify input audio has content

### CI Failures

**"No artifacts uploaded"**
- Normal if test outputs not generated (REAPER not on CI)
- Check that infrastructure validation passed

**"Module not found"**
- Add missing dependency to workflow's pip install step
- Or add to `requirements-ci.txt`

### Performance Issues

**Slow separation (>60s for 10s audio)**
- Use CPU for CI: `--device cpu`
- GPU tests require self-hosted runners
- Consider smaller test assets for quick tests

**Out of memory**
- Reduce test audio length (use 5s instead of 10s)
- Use htdemucs instead of htdemucs_ft
- Split heavy tests into separate runs

## Manual Testing Workflows

### Test Karaoke Feature

```bash
# Generate test project
python tests/reaper/generate_rpp.py test_karaoke.rpp tests/reaper/assets/test_mix_10s.wav

# Open in REAPER
reaper test_karaoke.rpp

# In REAPER:
# 1. Select media item
# 2. Run: Actions > STEMwerk: Karaoke
# 3. Verify: 3 stems created (drums, bass, other)
```

### Test Time Selection

```bash
# Generate project with time selection
python tests/reaper/generate_rpp.py test_timesel.rpp tests/reaper/assets/test_mix_10s.wav --time-selection 2.0 6.0

# Open in REAPER
reaper test_timesel.rpp

# In REAPER:
# 1. Verify time selection is active (2s - 6s)
# 2. Run: Actions > STEMwerk: Vocals Only
# 3. Verify: Vocal stem is exactly 4 seconds
```

### Test All Models

```bash
# Quick test all models
for model in htdemucs htdemucs_ft htdemucs_6s; do
  echo "Testing $model..."
  python scripts/reaper/audio_separator_process.py \
    tests/reaper/assets/test_mix_5s.wav \
    tests/reaper/output/$model/ \
    --model $model --device cpu
done
```

## Advanced Topics

### Self-Hosted GPU Runners

For real-time separation testing with GPU acceleration:

1. Set up self-hosted runner on machine with NVIDIA/AMD GPU
2. Install REAPER, Python, ffmpeg, audio-separator[gpu]
3. Update workflow to use `runs-on: self-hosted`
4. Enable GPU device in test scenarios: `--device cuda:0`

### Model Performance Benchmarking

```python
# Add timing to test harness
import time
start = time.time()
# ... separation ...
elapsed = time.time() - start
print(f"Separation took {elapsed:.1f}s")
```

### Quality Metrics

To add SNR/SDR validation (requires reference stems):

1. Generate reference stems offline
2. Store in `tests/reaper/references/`
3. Add validation logic to compare outputs
4. Update scenarios with `min_snr_db` or `min_sdr_db`

## Resources

- [REAPER scripting docs](https://www.reaper.fm/sdk/reascript/reascript.php)
- [audio-separator](https://github.com/nomadkaraoke/python-audio-separator)
- [Demucs models](https://github.com/facebookresearch/demucs)
- [CI workflow examples](.github/workflows/)

## Support

Issues or questions? Open an issue at:
https://github.com/flarkflarkflark/STEMwerk/issues