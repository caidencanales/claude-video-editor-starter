"""Remove dead air: keep spans of speech, drop long pauses between words.

Pure functions, so they're easy to test and build on.
"""
from __future__ import annotations


def keep_spans(words: list[dict], max_gap: float = 0.6, pad: float = 0.08) -> list[tuple[float, float]]:
    """Group words into spans; a pause longer than max_gap starts a new span."""
    spans: list[list[float]] = []
    for w in words:
        if spans and w["start"] - spans[-1][1] <= max_gap:
            spans[-1][1] = w["end"]
        else:
            spans.append([w["start"], w["end"]])
    out = []
    for a, b in spans:
        a, b = max(0.0, a - pad), b + pad
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], b)
        else:
            out.append((a, b))
    return out


def remap_words(words: list[dict], spans: list[tuple[float, float]]) -> list[dict]:
    """Move word times onto the cut timeline (spans placed back to back)."""
    out, offset = [], 0.0
    for a, b in spans:
        for w in words:
            if w["start"] >= a and w["end"] <= b:
                out.append({**w, "start": round(w["start"] - a + offset, 3), "end": round(w["end"] - a + offset, 3)})
        offset += b - a
    return out
