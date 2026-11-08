"""Phrase chunking and two basic caption styles, written as an .ass subtitle file.

Styles:
  bold     white, heavy outline, lower third
  karaoke  the same, but each word fills yellow as it is spoken
"""
from __future__ import annotations

PUNCT_END = (".", "?", "!", ",")


def chunk(words: list[dict], max_words: int = 4, max_chars: int = 20, max_pause: float = 0.4) -> list[list[dict]]:
    """Split words into short on-screen phrases."""
    chunks: list[list[dict]] = []
    cur: list[dict] = []
    for w in words:
        if cur:
            text_len = len(" ".join(x["word"] for x in cur + [w]))
            pause = w["start"] - cur[-1]["end"]
            if len(cur) >= max_words or text_len > max_chars or pause > max_pause or cur[-1]["word"].endswith(PUNCT_END):
                chunks.append(cur)
                cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    return chunks


def _ts(t: float) -> str:
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: bold,Arial,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,2,2,80,80,560,1
Style: karaoke,Arial,86,&H0000E5FF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,2,2,80,80,560,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def to_ass(words: list[dict], style: str = "bold", upper: bool = True) -> str:
    lines = [HEADER]
    for c in chunk(words):
        start, end = c[0]["start"], c[-1]["end"]
        shown = [w["word"].upper() if upper else w["word"] for w in c]
        if style == "karaoke":
            parts = []
            for i, w in enumerate(c):
                nxt = c[i + 1]["start"] if i + 1 < len(c) else w["end"]
                k = max(1, int(round((nxt - w["start"]) * 100)))
                parts.append(f"{{\\k{k}}}{shown[i]}")
            text = " ".join(parts)
        else:
            text = " ".join(shown)
        lines.append(f"Dialogue: 0,{_ts(start)},{_ts(end)},{style},,0,0,0,,{text}\n")
    return "".join(lines)
