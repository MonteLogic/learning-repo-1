#!/usr/bin/env python3
"""
generate_audiobook.py
---------------------
Pipeline: audiobook_JCMNS_Vol40.md  →  audiobook_clean.txt  →  audiobook_JCMNS_Vol40.mp3

Requirements:
    pip install edge-tts

Usage:
    python3 generate_audiobook.py [--voice VOICE] [--rate RATE] [--pitch PITCH]

Defaults:
    --voice  en-US-GuyNeural   (clear, neutral male; stays intelligible at 2.5x+)
    --rate   +10%              (slight speed boost at source; adjust to taste)
    --pitch  -2Hz              (slightly deeper; easier on ears at fast playback)

Available voices (run to list all):
    edge-tts --list-voices
"""

import argparse
import asyncio
import re
import subprocess
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
REPO_DIR    = Path(__file__).parent.resolve()
SCRIPT_MD   = REPO_DIR / "audiobook_JCMNS_Vol40.md"
CLEAN_TXT   = REPO_DIR / "audiobook_clean.txt"
OUTPUT_MP3  = REPO_DIR / "audiobook_JCMNS_Vol40.mp3"


# ── Step 1: clean the markdown script ─────────────────────────────────────────
def clean_markdown(src: Path, dst: Path) -> None:
    """Strip markdown syntax and [PAUSE] markers; write plain TTS-ready text."""
    print(f"[1/3] Cleaning  {src.name}  →  {dst.name}")
    text = src.read_text(encoding="utf-8")

    # Headings → keep text only
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Blockquote markers
    text = re.sub(r"^\s*>\s*", "", text, flags=re.MULTILINE)
    # Bold / italic / inline-code
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*",     r"\1", text)
    text = re.sub(r"`(.*?)`",       r"\1", text)
    # Horizontal rules
    text = re.sub(r"^-{3,}$", "", text, flags=re.MULTILINE)
    # Markdown tables (lines containing |)
    text = re.sub(r"^\|.*\|$", "", text, flags=re.MULTILINE)
    # [PAUSE] → comma (gives the TTS engine a natural micro-pause)
    text = re.sub(r"\[PAUSE\]", ",", text)
    # Italicised footnotes like *Word count: …*
    text = re.sub(r"^\*[^*]+\*$", "", text, flags=re.MULTILINE)
    # Collapse runs of blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    dst.write_text(text.strip() + "\n", encoding="utf-8")
    word_count = len(text.split())
    print(f"         {word_count:,} words written to {dst.name}")


# ── Step 2: synthesise with edge-tts ──────────────────────────────────────────
async def synthesise(voice: str, rate: str, pitch: str) -> None:
    """Use the edge_tts Python API directly to convert clean text to MP3."""
    print(f"[2/3] Synthesising  {CLEAN_TXT.name}  →  {OUTPUT_MP3.name}")
    print(f"         voice={voice}  rate={rate}  pitch={pitch}")

    try:
        import edge_tts  # noqa: PLC0415
    except ImportError:
        print("ERROR: edge-tts is not installed. Run: pip install edge-tts", file=sys.stderr)
        sys.exit(1)

    text = CLEAN_TXT.read_text(encoding="utf-8")
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(str(OUTPUT_MP3))


# ── Step 3: report ────────────────────────────────────────────────────────────
def report() -> None:
    """Print file size and duration using ffprobe if available."""
    print(f"[3/3] Done  →  {OUTPUT_MP3}")
    size_mb = OUTPUT_MP3.stat().st_size / 1_048_576
    print(f"         Size: {size_mb:.1f} MB")

    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1",
                str(OUTPUT_MP3),
            ],
            capture_output=True, text=True, check=True,
        )
        seconds = float(result.stdout.strip().split("=")[1])
        mins, secs = divmod(int(seconds), 60)
        print(f"         Duration: {mins}m {secs:02d}s at source rate")
        print(f"         At 2.5x playback: ~{mins//2}m {(secs + (mins % 2)*60)//2:02d}s")
    except Exception:
        pass  # ffprobe optional


# ── CLI ────────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the JCMNS Vol 40 audiobook MP3 from the markdown script.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--voice", default="en-US-GuyNeural",
                        help="edge-tts voice name (default: en-US-GuyNeural)")
    parser.add_argument("--rate",  default="+10%",
                        help="Speech rate offset, e.g. +10%% or -5%% (default: +10%%)")
    parser.add_argument("--pitch", default="-2Hz",
                        help="Pitch offset, e.g. -2Hz or +5Hz (default: -2Hz)")
    parser.add_argument("--skip-clean", action="store_true",
                        help="Skip markdown cleaning (use existing audiobook_clean.txt)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not SCRIPT_MD.exists():
        print(f"ERROR: source script not found: {SCRIPT_MD}", file=sys.stderr)
        sys.exit(1)

    if not args.skip_clean:
        clean_markdown(SCRIPT_MD, CLEAN_TXT)

    asyncio.run(synthesise(args.voice, args.rate, args.pitch))
    report()


if __name__ == "__main__":
    main()
