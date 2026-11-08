# Instructions for Claude: editing videos with this repo

You edit videos from longer footage, and you grow this repo into the editor the user wants.

## First session: plan, then build

1. **Plan mode first.** Interview the user before writing code: what they make, who it's for, their footage, the
   look they want, and 2-3 example videos they love. Ask multiple-choice questions where you can.
2. **Look at the footage and the examples.** Transcribe, pull stills, and note what the examples do that this repo
   can't do yet (captions, zooms, b-roll, graphics, sound, colour, pacing).
3. **Propose a plan:** the first video to make together, then the features to build, in order of visible impact.
   Wait for approval.
4. **Build step by step.**
   - Add each feature as its own module under `editor/`, with tests.
   - After each step, render and show the user stills or the clip.
   - Ask what to improve, and repeat.

## Making a video

1. **Transcribe:** `python -m editor.transcribe input.mp4 --out words.json`
2. **Pick the moment.** Read `words.json` and choose a span with:
   - a strong first sentence (the hook);
   - one clear idea;
   - a payoff at the end.
   Start on the hook, not on filler.
3. **Render:** `python -m editor.make_short input.mp4 --start S --end E --style karaoke --out out/short.mp4`
4. **Check it with your own eyes:**
   `ffmpeg -i out/short.mp4 -vf fps=1,scale=270:-1,tile=6x4 -frames:v 1 out/sheet.jpg`
   Are the captions readable? Is the face in frame? Are the edges clean?
5. **Fix and re-run:** widen spans that cut words, shorten caption phrases (`editor/captions.py`), improve the
   reframe.

## Rules

- Never overwrite the user's footage. Write to `out/`.
- Run `pytest -q` after changing code.
- Keep functions small and pure where you can (see `editor/cut.py`), so they stay testable.
- Respect the rights of any music, footage or assets you add.
