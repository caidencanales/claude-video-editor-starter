"""Word-level transcription with faster-whisper.

    python -m editor.transcribe input.mp4 --out words.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_audio(path: str | Path, sr: int = 16000):
    """Decode any media file to 16 kHz mono float32 with ffmpeg (no PyAV version issues)."""
    import subprocess

    import numpy as np

    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", str(sr), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def _run(audio, model: str, device: str, compute_type: str) -> list[dict]:
    from faster_whisper import WhisperModel

    m = WhisperModel(model, device=device, compute_type=compute_type)
    segments, _info = m.transcribe(audio, word_timestamps=True, vad_filter=True)
    words = []
    for seg in segments:
        for w in seg.words or []:
            text = w.word.strip()
            if text:
                words.append({"word": text, "start": round(w.start, 3), "end": round(w.end, 3)})
    return words


def transcribe(path: str | Path, model: str = "small", device: str = "auto") -> list[dict]:
    """Return [{"word", "start", "end"}, ...] in seconds. Falls back to CPU if the GPU libraries are missing."""
    audio = load_audio(path)
    try:
        return _run(audio, model, device, "default")
    except RuntimeError as e:
        if device == "cpu" or not any(k in str(e).lower() for k in ("cuda", "cublas", "cudnn")):
            raise
        print("GPU libraries not available, transcribing on CPU (slower)")
        return _run(audio, model, "cpu", "int8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="small")
    a = ap.parse_args()
    words = transcribe(a.input, a.model)
    Path(a.out).write_text(json.dumps(words, indent=1), encoding="utf-8")
    print(f"{len(words)} words -> {a.out}")


if __name__ == "__main__":
    main()
