# STEMwerk (REAPER scripts)

**STEM separation for REAPER**

![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)
![ReaPack](https://img.shields.io/badge/ReaPack-compatible-green)
![License](https://img.shields.io/badge/license-MIT-blue)

![STEMwerk Hero](docs/images/STEMwerk-hero.png)

STEMwerk uses AI (Demucs/HTDemucs) as a tool to separate audio into individual stems. This repo focuses on REAPER scripts (via ReaPack). The former plugin/standalone is developed separately as STEMdropper; historical JUCE/VST files live in `legacy/`.

---

## Why STEMwerk?

**Stay in your DAW.** No more exporting, switching to external tools, and re-importing.

![Before and After](docs/images/STEMwerk-before-after.png)

STEMwerk integrates directly into REAPER, letting you:

- **Process time selections** - Select a 4-bar section and extract just the drums from that part
- **Edit in place** - Replace a media item with its separated stems instantly
- **Work non-destructively** - Original files are preserved, stems are created alongside
- **Be surgical** - Found a sample with an unwanted vocal bleed? Extract only what you need
- **Stay creative** - Remix, mashup, or repair audio without leaving your project

### Real-World Workflows

| Scenario | Traditional Approach | With STEMwerk |
|----------|---------------------|------------------|
| Remove vocal from a loop | Export → External tool → Re-import → Align | Select item → Karaoke → Done |
| Extract drums from reference track | Export → Separate → Import 4 files → Create tracks | Select → All Stems → Auto-routed tracks |
| Fix a sample with unwanted bass | Find alternate sample or EQ compromise | Select → Bass Only → Delete original bass |
| Create acapella from full mix | External software, manual export/import | Select → Vocals Only → New track |
| Isolate guitar solo for analysis | Complex EQ/phase tricks | Select region → Guitar Only |

---

## Quick Start (REAPER)

1. **Install AI Backend** (one time, ~5 minutes):

   **Windows** (PowerShell as Admin):
   ```powershell
   # Download and run installer
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/flarkflarkflark/STEMwerk/main/scripts/install.ps1" -OutFile install.ps1
   .\install.ps1
   ```

   **macOS/Linux** (Terminal):
   ```bash
   curl -sSL https://raw.githubusercontent.com/flarkflarkflark/STEMwerk/main/scripts/install.sh | bash
   ```

2. **Install REAPER Scripts**:
   - Open REAPER → Extensions → ReaPack → Import repositories
   - Paste: `https://raw.githubusercontent.com/flarkflarkflark/STEMwerk/main/scripts/reaper/index.xml`
   - Extensions → ReaPack → Browse packages → Search "STEMwerk" → Install

3. **Verify Setup**:
   - Actions → Run: "STEMwerk: Installation & Setup"
   - Should show all green checkmarks ✓

4. **Use It**:
   - Select audio item → Actions → "STEMwerk: AI Stem Separation"

---

## Features

### Internationalization

STEMwerk supports multiple languages:
- **English (EN)** - Default language
- **Dutch (NL)** - Nederlands
- **German (DE)** - Deutsch

All UI elements are translated including stem names, presets, tooltips, help text, and error messages. Language files are located in `i18n/languages.lua` with 152 translation keys per language.

To add a new language, copy the `en` block in `i18n/languages.lua` and translate all keys. See [TESTING.md](TESTING.md#internationalization-testing) for validation tools.

### Stem Types

| Model | Stems | Best For |
|-------|-------|----------|
| **htdemucs** (4-stem) | Vocals, Drums, Bass, Other | Fast, general use |
| **htdemucs_ft** (4-stem) | Vocals, Drums, Bass, Other | Highest quality |
| **htdemucs_6s** (6-stem) | Vocals, Drums, Bass, Other, Guitar, Piano | Detailed separation |

![6-Stem Model](docs/images/STEMwerk-6stem.png)

### Flexible Input Selection

STEMwerk works with whatever you have selected:

![Time Selection Feature](docs/images/STEMwerk-time-selection.png)

| Selection Type | What Gets Processed |
|----------------|---------------------|
| **Media item(s)** | Full item(s) - stems replace or appear alongside original |
| **Time selection** | Only the selected time range - perfect for surgical edits |
| **Time selection + item** | Intersection of both - maximum precision |

This means you can:
- Process an entire song by selecting the media item
- Extract stems from just a chorus by making a time selection
- Work on a specific 2-bar section without affecting the rest

### REAPER Scripts

![STEMwerk Dialog](docs/images/STEMwerk-dialog.png)

| Script | Description |
|--------|-------------|
| **STEMwerk: AI Stem Separation** | Main dialog - full control over model, stems, and options |
| **STEMwerk: Karaoke** | One-click vocal removal (keeps drums, bass, other) |
| **STEMwerk: Vocals Only** | Extract vocals to new track |
| **STEMwerk: Drums Only** | Extract drums to new track |
| **STEMwerk: Bass Only** | Extract bass to new track |
| **STEMwerk: All Stems** | Extract all stems to separate tracks |
| **STEMwerk: Explode Stems** | Route stems to individual tracks |
| **STEMwerk: Setup Toolbar** | Add quick-access toolbar buttons |

![Toolbar Icons](docs/images/STEMwerk-toolbar.png)

### Keyboard Shortcuts (in dialog)
- `1-6` - Toggle stems
- `K` - Karaoke preset
- `I` - Instrumental preset
- `A` - All stems
- `Enter` - Start separation
- `Esc` - Cancel

---

## Installation Details

### Requirements

- **Python 3.9+** (3.10-3.12 recommended)
- **ffmpeg** (for audio conversion)
- **~2GB disk space** (for AI models)

### Automatic Installation

The install scripts automatically:
1. Find or install Python
2. Create isolated virtual environment
3. Install PyTorch with GPU support (if available)
4. Install audio-separator package
5. Pre-download AI models

### GPU Acceleration

| GPU | Support | Speed Improvement |
|-----|---------|-------------------|
| NVIDIA (CUDA) | ✓ Full | 10-20x faster |
| AMD (ROCm) | ✓ Linux only | 10-15x faster |
| Apple Silicon (MPS) | ✓ Native | 5-10x faster |
| Intel/AMD (CPU) | ✓ Fallback | Baseline |

### Manual Installation

If automatic installation fails:

**Windows:**
```cmd
python -m pip install audio-separator[gpu]
winget install Gyan.FFmpeg
```

**macOS:**
```bash
pip3 install audio-separator[gpu]
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
pip3 install audio-separator[gpu]
sudo apt install ffmpeg
```

**Linux (Arch):**
```bash
pip install audio-separator[gpu]
sudo pacman -S ffmpeg
```

---

## Legacy plugin/standalone

The VST3/standalone implementation has moved to the **STEMdropper** project. Historical JUCE/VST code and resources remain in `legacy/` for reference.

---

## Processing Time

| Hardware | 3-minute song |
|----------|---------------|
| RTX 3080 / RX 6800 | 15-30 seconds |
| RTX 2070 / RX 5700 | 30-60 seconds |
| Apple M1/M2 | 45-90 seconds |
| Modern CPU (8 core) | 2-5 minutes |
| Older CPU | 5-15 minutes |

---

## Output

![REAPER with Stems](docs/images/reaper-stems.png)

Stems are saved as WAV files alongside your original audio (regardless of input format):
```
mysong.mp3           # Your original file (mp3, wav, flac, etc.)
mysong_vocals.wav    # Stems are always high-quality WAV
mysong_drums.wav
mysong_bass.wav
mysong_other.wav
mysong_guitar.wav    # 6-stem only
mysong_piano.wav     # 6-stem only
```

---

## Troubleshooting

### "Python not found"
Run the install script for your platform, or install Python 3.10+ manually.

### "audio-separator not found"
```bash
pip install audio-separator[gpu]
```

### "ffmpeg not found"
- Windows: `winget install Gyan.FFmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg` or `sudo pacman -S ffmpeg`

### Slow processing
- Ensure GPU drivers are up to date
- Use `htdemucs` model (faster than `htdemucs_ft`)
- Check GPU is being used (look for CUDA/ROCm/MPS in output)

### Out of memory
- Close other GPU-intensive applications
- Try `htdemucs` instead of `htdemucs_6s`
- Processing in smaller chunks (time selection)

---

## Credits

- **Demucs**: Meta AI Research (MIT License)
- **audio-separator**: Beverly Nguyen (MIT License)
- **JUCE**: RAL/ROLI (Commercial/GPL)

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Development

For the current project task list (tracked in git), see [TODO.md](TODO.md).

---

**flarkAUDIO** - Professional Audio Tools
## Script: `scripts/reaper/audio_separator_process.py`

Usage examples:

- Quick list of available models (safe for CI, no heavy installs):

```bash
python scripts/reaper/audio_separator_process.py --list-models
```

- Check installation (requires `audio-separator` and `torch`):

```bash
python scripts/reaper/audio_separator_process.py --check
```

- Run separation (example):

```bash
python scripts/reaper/audio_separator_process.py path/to/input.wav path/to/output_dir --model htdemucs --device auto
```

Notes:
- `--list-models` prints common model names and is useful for CI to validate the script is present and runnable.
- `--check` will import `audio-separator` and `torch` and may require GPU drivers and significant time to set up; use locally or in a dedicated CI job with caching.
