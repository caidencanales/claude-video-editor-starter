"""Make a vertical short: trim -> transcribe -> cut dead air -> centre-crop 9:16 -> burn captions.

    python -m editor.make_short input.mp4 --start 60 --end 105 --style karaoke --out short.mp4
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from editor.captions import to_ass
from editor.cut import keep_spans, remap_words
from editor.transcribe import transcribe

VERTICAL = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1"


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, check=True, cwd=cwd)


def make_short(src: Path, out: Path, start: float | None, end: float | None, style: str, model: str) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    # work files sit next to the output (same drive, easy to inspect, nothing written to the system temp folder)
    work = Path(tempfile.mkdtemp(prefix=f".work-{out.stem}-", dir=out.parent))
    clip = work / "clip.mp4"
    trim = (["-ss", str(start)] if start is not None else []) + (["-to", str(end)] if end is not None else [])
    run(["ffmpeg", "-v", "error", "-y", *trim, "-i", str(src), "-c:v", "libx264", "-crf", "18", "-c:a", "aac", str(clip)])

    words = transcribe(clip, model)
    (work / "words.json").write_text(json.dumps(words, indent=1), encoding="utf-8")
    spans = keep_spans(words)
    if not spans:
        raise SystemExit("no speech found")

    parts = "".join(
        f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];"
        for i, (a, b) in enumerate(spans)
    )
    joins = "".join(f"[v{i}][a{i}]" for i in range(len(spans)))
    graph = f"{parts}{joins}concat=n={len(spans)}:v=1:a=1[v][a];[v]{VERTICAL}[vo]"
    cut = work / "cut.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-filter_complex", graph, "-map", "[vo]", "-map", "[a]",
         "-c:v", "libx264", "-crf", "18", "-c:a", "aac", str(cut)])

    (work / "captions.ass").write_text(to_ass(remap_words(words, spans), style), encoding="utf-8")
    # run inside the work dir so the ass filter gets a plain relative path (avoids Windows escaping)
    run(["ffmpeg", "-v", "error", "-y", "-i", "cut.mp4", "-vf", "ass=captions.ass", "-c:v", "libx264", "-crf", "18",
         "-c:a", "copy", "final.mp4"], cwd=work)
    (work / "final.mp4").replace(out)
    print(f"{out}  ({len(spans)} spans kept, work files in {work})")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--start", type=float)
    ap.add_argument("--end", type=float)
    ap.add_argument("--style", choices=["bold", "karaoke"], default="bold")
    ap.add_argument("--model", default="small")
    a = ap.parse_args()
    make_short(a.input, a.out, a.start, a.end, a.style, a.model)


if __name__ == "__main__":
    main()
