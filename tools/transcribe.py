#!/usr/bin/env python3
"""Transcribe an MP4 to timestamped markdown via faster-whisper.

Usage:
  python tools/transcribe.py INPUT.mp4 --output raw/transcripts/foo.md
"""
import argparse
import sys
import time
from pathlib import Path

from faster_whisper import WhisperModel


def fmt_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--model", default="small.en")
    ap.add_argument("--compute-type", default="int8")
    ap.add_argument("--device", default="cpu")
    args = ap.parse_args()

    print(f"[transcribe] loading model={args.model} compute={args.compute_type} device={args.device}", flush=True)
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute_type)
    print(f"[transcribe] model loaded; transcribing {args.input}", flush=True)

    t0 = time.time()
    segments, info = model.transcribe(
        str(args.input),
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
    )
    print(f"[transcribe] language={info.language} prob={info.language_probability:.2f} duration={info.duration:.0f}s ({info.duration/60:.1f} min)", flush=True)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        f.write(f"# Transcript — {args.input.name}\n\n")
        f.write(f"**Source file:** `{args.input}`  \n")
        f.write(f"**Language:** {info.language} (prob {info.language_probability:.2f})  \n")
        f.write(f"**Duration:** {info.duration:.0f}s ({info.duration/60:.1f} min)  \n")
        f.write(f"**Model:** faster-whisper `{args.model}` ({args.device}, {args.compute_type})  \n")
        f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}  \n\n")
        f.write("---\n\n")
        last_status = t0
        for i, seg in enumerate(segments):
            ts = fmt_ts(seg.start)
            text = seg.text.strip()
            f.write(f"**[{ts}]** {text}\n\n")
            f.flush()
            now = time.time()
            if now - last_status > 30:
                pct = (seg.end / info.duration) * 100 if info.duration else 0
                print(f"[progress] {ts} (~{pct:.1f}%) elapsed={now-t0:.0f}s", flush=True)
                last_status = now

    elapsed = time.time() - t0
    realtime_x = info.duration / elapsed if elapsed > 0 else 0
    print(f"[transcribe] done in {elapsed:.1f}s ({realtime_x:.1f}x realtime); output -> {args.output}", flush=True)


if __name__ == "__main__":
    main()
