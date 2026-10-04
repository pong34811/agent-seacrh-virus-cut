# Hoshi Livestream Highlights -> Resolve Timelines Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Steps use checkbox syntax. Also load the `resolve-rough-cut`, `resolve-media-pool`, `resolve-session` skills before Phase 4.

**Goal:** Inventory the 4 livestream VODs in `Z:\hoshi\2026-10-03`, find 30s-3min highlight moments (gameplay / fun / meme), then build one DaVinci Resolve timeline per clip.

**Architecture:** Cheap signal first, expensive review second. ffmpeg/Python extract audio and score every 30s window (loudness spikes + transcript keywords + laughter-like energy); a subagent per VOD reviews the top windows via transcripts and contact sheets and writes `candidates.json`; a final script converts approved candidates into Resolve `clip_infos` and creates timelines via the Resolve MCP. Source files are never modified or transcoded.

**Tech Stack:** ffmpeg/ffprobe 9.0.1 (`C:\Users\warit\AppData\Local\hermes\tools\ffmpeg-9.0.1-win32-x64\bin`), Python 3 (+ pytest), faster-whisper (to install in a venv), Pillow (contact sheets), Resolve MCP (`D:\davinci-resolve-mcp`).

**Spec:** the user request (Thai): list all footage; find interesting moments ~30s-3min in 3 categories (gameplay, fun, meme); then create a Timeline per clip.

## Global Constraints

- Source folder is READ-ONLY: `Z:\hoshi\2026-10-03`. Never write beside it.
- All work output goes under `D:\agent-seacrh-virus-cut\work\` (gitignored: `frames/`, `audio/`, `transcripts/`; tracked: `inventory.json`, `candidates.json`, scripts, tests).
- Clip length: min 30 s, max 180 s, target 45-120 s.
- Categories are exactly: `gameplay`, `fun`, `meme`.
- Timelines: deliverable is an assembled timeline only. NO titles, captions, music, effects, grading (resolve-rough-cut contract).
- Timeline fps 60 (all sources 60/1 CFR). Resolution per Open Question 1 (default 1920x1080).
- User communicates in Thai: final report in Thai.
- Be careful with filenames: they contain `【】`, Thai text and full-width `｜` / `⧸`. Always glob/list from Python (`pathlib`), never hand-type paths.

## Review Focus

1. AV1 source (3 of 4 files) may not decode in the installed Resolve edition -> import yields offline/black clips. Task 2 checks this before any analysis.
2. Streams are 2.3-3 h each: transcript/score steps must be resumable and chunked, or a timeout loses everything.
3. Quiet or music-only stretches (BRB screens, waiting rooms) score high on nothing but also can be flagged by loudness spikes (game jumpscares in Backrooms are legitimately great; BGM stingers are not). Review step must reject windows with no speech.
4. Overlapping candidate windows must be merged, not emitted twice.
5. A candidate crossing a sentence boundary: snap start/end to nearest silence (<-35 dB, >=0.4 s) within +-3 s.

## File Structure

- `work/config.py` – paths, clip limits, category names (single source of truth)
- `work/inventory.py` – ffprobe all files -> `work/inventory.json` + `work/inventory.md`
- `work/extract_audio.py` – 16 kHz mono wav per VOD in `work/audio/`
- `work/transcribe.py` – faster-whisper (Thai, `large-v3` or `medium` if no GPU) -> `work/transcripts/<id>.json`, resumable per 10-min chunk
- `work/score.py` – 30 s hop windows, loudness/peak/speech-rate/keyword features -> `work/scores/<id>.json`
- `work/windows.py` – pure functions: `merge_windows`, `snap_to_silence`, `clamp_duration` (unit tested)
- `work/contact_sheet.py` – frame grid for a time range
- `work/candidates.json` – reviewed output (schema below)
- `work/build_timelines.py` – candidates -> `clip_infos` -> Resolve MCP calls
- `work/tests/test_windows.py`, `test_inventory.py`, `test_candidates_schema.py`

`candidates.json` schema (list):
```json
{"id":"roblox-01","source_id":"roblox","start_s":1234.5,"end_s":1320.0,
 "category":"fun","title_th":"สั้นๆ บรรยายไทย","reason":"why interesting","score":0.0-1.0}
```
`source_id` in {`hbd`,`backrooms`,`drawing`,`roblox`} (mapping in `config.py`).

## Known facts (probed 2026-10-04, read-only)

| source_id | file (prefix) | codec | duration |
|---|---|---|---|
| hbd | 【HBD】ไลฟ์สุขสันต์วันเกิด Hoshi_1489 (20/08/2026) | AV1 1080p60 | 8119 s (2h15m) |
| backrooms | 【LIVE】Backrooms (08/08/2026) | AV1 1080p60 | 10274 s (2h51m) |
| drawing | 【LIVE】วาดรูปกับคุณเปอร์ (15/08/2026) | AV1 1080p60 | 10821 s (3h00m) |
| roblox | 【กองโจร】เล่นroblox (23/08/2026) | H.264 1080p60 | 8740 s (2h26m) |

All: opus stereo audio, 16:9, ~12.1 GB total, ~10.5 h of footage. Landscape, so no rotation flag. Mapping of category hints: backrooms/roblox -> mostly `gameplay`; hbd/drawing -> mostly `fun`; `meme` can come from any.

## Tasks

### Task 1: Scaffold + inventory (TDD)

**Files:** Create `work/config.py`, `work/inventory.py`, `work/tests/test_inventory.py`, `work/.gitignore` (`audio/ frames/ transcripts/ scores/`).

**Interfaces:** Produces `config.SOURCE_DIR: Path`, `config.FFPROBE: str`, `inventory.probe(path: Path) -> dict` (keys `file, source_id, codec, width, height, fps, duration_s, size_bytes, audio_codec`), `inventory.build() -> list[dict]`.

- [ ] Step 1: Write failing test `test_build_lists_four_sources`: `rows = inventory.build(); assert len(rows)==4; assert {r["source_id"] for r in rows}=={"hbd","backrooms","drawing","roblox"}; assert all(r["fps"]==60 and r["duration_s"]>7000 for r in rows)`.
- [ ] Step 2: `cd D:/agent-seacrh-virus-cut/work && python -m pytest tests/test_inventory.py -v` -> Expected FAIL (module missing).
- [ ] Step 3: Implement. `source_id` derived by substring match: "HBD"->hbd, "Backrooms"->backrooms, "วาดรูป"->drawing, "roblox"->roblox. `probe` uses `ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate -of json`. fps = eval of fraction via `fractions.Fraction`. `__main__` writes `inventory.json` and a markdown table `inventory.md` (the human-readable footage list requested).
- [ ] Step 4: Re-run pytest -> Expected `1 passed`. Run `python inventory.py` -> prints 4 rows; `inventory.md` exists.
- [ ] Step 5: `git add work && git commit -m "feat: footage inventory"`

### Task 2: Resolve compatibility gate (AV1) — decision point

**Files:** none created. Uses Resolve MCP (see skills `resolve-session`, `resolve-media-pool`).

- [ ] Step 1: Confirm Resolve is running: `resolve_control get_version` -> returns edition/version.
- [ ] Step 2: Check project list (`project_manager list`). Per resolve-rough-cut: add timelines to an existing series project if one fits, otherwise create `Hoshi-2026-10` and BEFORE creating any timeline set `timelineFrameRate=60` and ask the user to set Playback frame rate in the UI (Project Settings -> Master Settings -> Playback frame rate; quote exactly, do not elaborate).
- [ ] Step 3: `media_pool add_subfolder "2026-10-03"`, `set_current_folder` to it, THEN `media_storage` import the 4 files (current-folder rule).
- [ ] Step 4: For each clip read `media_pool_item` properties; Expected: `Video Codec` populated, `Resolution` 1920x1080, FPS 60, no "media offline". If an AV1 clip is offline/zero-length -> STOP and ask user (options: install AV1 decoder / Resolve Studio, or transcode proxies to H.264 into `work/proxy/` — transcoding is out of scope unless approved since "never transcode source" applies to the originals only).
- [ ] Step 5: Save the 4 `clip_id`s to `work/resolve_clips.json` as `{source_id: clip_id}`. Commit.

### Task 3: Audio extraction + transcription (resumable)

**Files:** Create `work/extract_audio.py`, `work/transcribe.py`.

**Interfaces:** Produces `work/audio/<source_id>.wav` (16 kHz mono) and `work/transcripts/<source_id>.json` = `[{"start":float,"end":float,"text":str}, ...]`.

- [ ] Step 1: `python -m venv work/.venv && work/.venv/Scripts/pip install faster-whisper pillow numpy pytest`. Expected: installs succeed. (Needs network; flag to user if GPU absent -> use `medium` model, expect hours on CPU; fall back to `small`.)
- [ ] Step 2: `extract_audio.py`: for each inventory row run `ffmpeg -y -i <file> -vn -ac 1 -ar 16000 -c:a pcm_s16le work/audio/<id>.wav`. Skip if the wav exists. Run it; Expected: 4 wavs, durations within 1 s of inventory (verify with ffprobe).
- [ ] Step 3: `transcribe.py <source_id>`: transcribe in 600 s chunks (`language="th"`, `vad_filter=True`), append each chunk to `transcripts/<id>.partial.json`, rename to `.json` when done; on rerun resume from the last chunk end. Offset segment times by chunk start.
- [ ] Step 4: Run per source as background process with notify (not a foreground call; >5 min). Verify: `python -c "import json;t=json.load(open('work/transcripts/roblox.json',encoding='utf-8'));print(len(t),t[-1]['end'])"` -> segments > 500, last end within 60 s of 8740.
- [ ] Step 5: Commit scripts only.

### Task 4: Window utilities (TDD)

**Files:** Create `work/windows.py`, `work/tests/test_windows.py`.

**Interfaces:** `merge_windows(ws: list[tuple[float,float,float]], gap_s: float=15) -> list[tuple[float,float,float]]` (start,end,score; overlapping or within gap merged, score=max); `clamp_duration(start,end,min_s=30,max_s=180,center=None)->tuple[float,float]`; `snap_to_silence(t: float, silences: list[tuple[float,float]], radius: float=3.0) -> float` (returns the silence midpoint nearest t within radius, else t).

- [ ] Step 1: Tests: `merge_windows([(0,40,.5),(35,80,.9),(200,240,.3)])==[(0,80,.9),(200,240,.3)]`; `clamp_duration(100,110)` returns length 30 centered; `clamp_duration(0,500)` returns length 180; `snap_to_silence(100,[(101,101.6)])==101.3`; `snap_to_silence(100,[(110,111)])==100`.
- [ ] Step 2: run pytest -> FAIL. Step 3: implement. Step 4: pytest -> `5 passed`. Step 5: commit.

### Task 5: Candidate scoring

**Files:** Create `work/score.py`, `work/keywords.py` (Thai lists: laughter `ฮ่าๆ|555|ขำ|ตลก`, shock `เฮ้ย|อ๊าก|ตายแล้ว|กรี๊ด|ว้าย|โอ้โห`, meme `มีม|meme|เพลงนี้|ซ้ำ|ปัง|ไอ้|เสียงนี้`, tune later from transcripts).

**Interfaces:** Consumes `audio/<id>.wav`, `transcripts/<id>.json`. Produces `scores/<id>.json` = list of `{"start","end","score","loud_z","peak_z","kw_hits","speech_ratio"}` for 60 s windows at 30 s hop, plus top-N (`N = duration_h*12`) written to `scores/<id>.top.json` after `merge_windows`.

- [ ] Step 1: Score = 0.4*loud_z + 0.2*peak_z + 0.3*min(kw_hits,5)/5 + 0.1*speech_ratio, normalized 0-1 per VOD. Windows with speech_ratio<0.2 get score*0.3 (review-focus 3).
- [ ] Step 2: Run `python score.py roblox`. Expected: `scores/roblox.top.json` has ~29 windows, none overlapping (assert in script).
- [ ] Step 3: Run for all four. Commit.

### Task 6: Subagent review per VOD (parallel, 4 children)

**Files:** Produces `work/review/<id>.json` (candidate list per schema) per child.

- [ ] Step 1: `delegate_task` with 4 tasks (one per source_id). Context for each child must include: Global Constraints, candidate schema, category definitions (gameplay = skilled/tense/funny gameplay moments with commentary; fun = banter, birthday, drawing reactions, chat interaction; meme = quotable lines, running gags, absurd/clip-worthy reactions), paths to `transcripts/<id>.json`, `scores/<id>.top.json`, `contact_sheet.py` usage, and the rule: read transcript text for each top window +-60 s, view at most 1 contact sheet per window, choose 4-8 clips per VOD, set start/end on topic boundaries (snap with `snap_to_silence` using `ffmpeg silencedetect -af silencedetect=n=-35dB:d=0.4`), length 30-180 s, write Thai `title_th` and `reason`. Children write only to `work/review/<id>.json`; they cannot ask questions.
- [ ] Step 2: Verify each returned file yourself: `python -m pytest tests/test_candidates_schema.py -v`, where the test loads all `work/review/*.json` and asserts: required keys, category in the allowed set, `30<=end_s-start_s<=180`, `end_s<=duration_s` from inventory, no overlaps within a source. Expected: all pass. Reject/redo any child whose file fails (child summaries are self-reports).
- [ ] Step 3: Merge to `work/candidates.json`, ordered by source then start, ids `<source_id>-NN`. Commit.

### Task 7: USER CHECKPOINT — approve candidates

- [ ] Step 1: Print a table (id, source, hh:mm:ss start-end, duration, category, title_th) from `candidates.json` and ask the user (in Thai) to approve / drop / adjust. Do NOT create timelines before approval (timelines are cheap but cleanup of archived versions is annoying).
- [ ] Step 2: Apply edits to `candidates.json`; re-run schema test; commit.

### Task 8: Build timelines in Resolve

**Files:** Create `work/build_timelines.py` (generates `work/timeline_plan.json`), then executes via MCP.

**Interfaces:** `to_clip_infos(c: dict, clip_id: str, fps: int=60) -> list[dict]` returns one item `{"clip_id","start_frame":round(start_s*fps),"end_frame":start_frame+round(dur*fps),"record_frame":0}` (end exclusive; source fps == timeline fps 60 so no mixed-fps floor issue). Unit test: 60 s clip at start 10 s -> `start_frame 600, end_frame 4200`.

- [ ] Step 1: TDD `to_clip_infos` (write test, see fail, implement, pass). Commit.
- [ ] Step 2: For each approved candidate: `media_pool set_current_folder` to the `2026-10-03` bin, then `media_pool create_timeline_from_clips` name `<id>_<category>_<title_th>` (<=60 chars) with the `clip_infos`. Single-clip timelines include audio automatically.
- [ ] Step 3: Verify per timeline: `timeline detect_gaps_overlaps` -> 0 gaps, 0 overlaps; duration frames == `round(dur*60)` (±0); count of timelines created == count in `candidates.json`.
- [ ] Step 4: `project_manager`/`media_pool` list timelines; delete any `*_archived_vNN`. Save project.
- [ ] Step 5: Optional spot check: `timeline_frame` capture the first frame of 3 random timelines; confirm picture is not black.

### Task 9: Report

- [ ] Final report in Thai: the footage list (inventory.md), the candidate table, timeline names, and what was NOT done (no titles/captions/grading; no renders unless asked).

## Risks / Tradeoffs

- Transcription time: ~10.5 h of audio. On GPU ~15-30 min total; CPU `medium` could take 10+ h. Check `nvidia-smi` in Task 3; else downgrade model or transcribe only top-scored windows (loudness-only prefilter) — acceptable fallback, note it in the report.
- Whisper Thai accuracy is mediocre on game noise; keywords are a weak signal, so loudness + human-like review of contact sheets carries weight. Fun/meme judgements are subjective -> the Task 7 checkpoint is the quality gate.
- Chat/superchat overlays are not in the VOD; no chat-based signals.
- Disk: audio wavs ~1.2 GB total (16 kHz mono) in `work/audio/`.

## Open Questions (ask the user in Thai before Task 8; defaults in brackets)

1. Timeline format: keep 16:9 1920x1080 [default], or vertical 1080x1920 for Shorts/TikTok (adds a reframe step with face/game-region crop; would be a new task)?
2. Number of clips: 4-8 per VOD (~16-32 total) [default] — or fewer, best-only?
3. Resolve project: use an existing project or create `Hoshi-2026-10` [default]?
4. If AV1 is not decodable: approve H.264 proxy generation in `work/proxy/`?
