from editor.captions import chunk, to_ass
from editor.cut import keep_spans, remap_words

WORDS = [
    {"word": "This", "start": 0.0, "end": 0.2},
    {"word": "is", "start": 0.25, "end": 0.35},
    {"word": "great.", "start": 0.4, "end": 0.8},
    {"word": "Really", "start": 2.5, "end": 2.8},
    {"word": "great", "start": 2.85, "end": 3.2},
]


def test_long_pause_splits_spans():
    spans = keep_spans(WORDS, max_gap=0.6, pad=0.0)
    assert spans == [(0.0, 0.8), (2.5, 3.2)]


def test_remap_closes_the_gap():
    spans = keep_spans(WORDS, max_gap=0.6, pad=0.0)
    moved = remap_words(WORDS, spans)
    assert moved[3]["start"] == 0.8  # "Really" now follows "great." directly


def test_chunks_break_on_punctuation():
    assert [len(c) for c in chunk(WORDS)] == [3, 2]


def test_karaoke_tags_stay_lowercase():
    ass = to_ass(WORDS, "karaoke")
    assert "\\k" in ass and "\\K" not in ass and "GREAT" in ass
