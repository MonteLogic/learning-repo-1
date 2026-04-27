# JCMNS Vol 40 — Audiobook Generator

Converts the audiobook markdown script into a high-quality MP3 using
[edge-tts](https://github.com/rany2/edge-tts) (Microsoft Neural TTS, free, no API key).

## Files

| File | Description |
|---|---|
| `BiberianJPjcondensedzm.pdf` | Source academic journal (JCMNS Vol 40, 2025) |
| `audiobook_JCMNS_Vol40.md` | 5,000-word audiobook script (edit this to change content) |
| `generate_audiobook.py` | Pipeline script: MD → clean text → MP3 |
| `requirements.txt` | Python dependency (`edge-tts`) |
| `Makefile` | Convenience targets |

## Quick Start

### Option A — Make (recommended)

```bash
# First time: creates a virtualenv and installs edge-tts
make

# Re-generate with a different voice
make mp3 VOICE=en-US-JennyNeural

# Wipe generated files and start fresh
make clean-audio && make
```

### Option B — Python directly (if edge-tts is already installed)

```bash
pip install -r requirements.txt
python3 generate_audiobook.py
```

### Options

```
python3 generate_audiobook.py --help

  --voice   en-US-GuyNeural    edge-tts voice (default: GuyNeural)
  --rate    +10%               Speech rate offset  (e.g. +15%, -5%)
  --pitch   -2Hz               Pitch offset        (e.g. -5Hz, +3Hz)
  --skip-clean                 Skip MD cleaning; reuse existing audiobook_clean.txt
```

### Listing all available voices

```bash
edge-tts --list-voices
```

## Output

| File | Description |
|---|---|
| `audiobook_clean.txt` | Intermediate plain-text (auto-generated, safe to delete) |
| `audiobook_JCMNS_Vol40.mp3` | Final MP3, ~11 MB, ~29 min at natural pace, ~12 min at 2.5x |

## Dependencies

- Python 3.8+
- `edge-tts` (installed via `requirements.txt`)
- `ffmpeg` (optional, used only for the duration report)
- Internet connection (edge-tts streams audio from Microsoft servers)

## Changing the Script

Edit `audiobook_JCMNS_Vol40.md` then re-run `make`. The pipeline automatically
strips all markdown formatting and `[PAUSE]` markers before synthesis.

## Recommended Playback

Listen at **2.5x speed** in any podcast app (Pocket Casts, Overcast, Apple Podcasts).
The voice (`en-US-GuyNeural`) is a neural TTS voice that articulates clearly at
high speeds with no distortion.
