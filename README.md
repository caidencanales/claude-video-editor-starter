# claude-video-editor-starter

Edit videos with [Claude Code](https://claude.com/claude-code). Point Claude at a long video and it finds the best
moment, cuts the dead air, reframes it to vertical 9:16 and burns in captions. Then it grows into the editor you
want: Claude plans with you and builds new features into this repo as you go.

## Get started

1. Install Python 3.10+ and [ffmpeg](https://ffmpeg.org/) (on PATH).
2. `pip install -r requirements.txt`
3. Open this folder in Claude Code, switch to plan mode, and paste the prompt from **[PROMPT.md](PROMPT.md)**. Claude
   interviews you, studies your example videos and footage, plans, and then builds your editor with you step by step.

Have a GPU? An NVIDIA card makes transcription much faster; it's used automatically when CUDA is set up, with a CPU
fallback otherwise.

## What's in it

| step | file | how |
|---|---|---|
| transcribe | `editor/transcribe.py` | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) word timestamps |
| cut dead air | `editor/cut.py` | removes pauses longer than 0.6 s |
| vertical reframe | `editor/make_short.py` | 1080x1920 output |
| captions | `editor/captions.py` | phrase-by-phrase captions in two styles, `bold` and `karaoke` (each word fills as it's spoken) |

Run it directly:

```bash
python -m editor.make_short input.mp4 --start 60 --end 105 --style karaoke --out out/short.mp4
```

## What you can build next with Claude

- face tracking for the reframe;
- punch-in zooms;
- b-roll;
- motion graphics;
- music and sound effects;
- colour grading;
- more caption styles;
- smarter moment picking;
- a review page.

Ask Claude for any of these; `CLAUDE.md` tells it how to plan and build them into this repo.

## Licence

MIT. Bring your own footage, and respect the rights of anything you edit or publish.
