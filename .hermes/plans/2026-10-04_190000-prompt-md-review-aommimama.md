# Review of prompt.md for the Aommimama job — Plan

## Goal
Make `prompt.md` and the code it relies on consistent for job `Aommimama / 2026-09-aomimama`, and get the open questions below answered before any footage work starts.

## Current context (read-only review, 2026-10-04)
- `prompt.md` variables now: `INPUT_DIR=Z:\Aommi-mama\2026-09-aomimama`, `CHANNEL=Aommimama`, `JOB=2026-09-aomimama`, `RESOLVE_PROJECT=ยังไม่ระบุ`, `PLAYBACK_FPS_USER_CONFIRMED=ยังไม่ยืนยัน`. File uses CRLF line endings (keep them).
- `INPUT_DIR` exists: 13 `.mp4` files (dated 20260906..20260926) plus a stray `downloaded.txt` (not a video, must be ignored by inventory). Games visible in filenames: alien shooter, Minecraft Dreamlight, League of Legends, strinova, Becastled, plus one talk video ("หงุดหงิด ฉุนเฉียว"). Filenames are NOT reliable evidence of the game (AGENTS.md).
- `work/Aommimama/` does not exist yet. The only job.json is `work/hoshi_1489/2026-09/job.json`.
- The user typed "promt.md"; the real file is `prompt.md`.

## Findings (things in prompt.md / code that look wrong or doubtful)

1. No job.json for this job. AGENTS.md says `work/<channel>/<job>/job.json` mirrors the prompt table and `HIGHLIGHT_JOB` selects it. Without `work/Aommimama/2026-09-aomimama/job.json`, `config.py` falls back to its default (hoshi) and would write into the wrong folder.
2. `GAME_NAME` and `TIMELINE_NAME_FORMAT` exist in the hoshi job.json but are NOT in the prompt.md table, while deliverable 3 (line 98) requires `{ชื่อคลิป}-{ชื่อเกม}-vdo`. A single `GAME_NAME` is wrong for this job: 13 videos cover at least 5 games and one talk video. Game name must be per video (or asked per clip).
3. `work/build_timelines.py:11` `timeline_name()` still returns `{id}_{category}_{title}`. That contradicts prompt line 98 (no id, no category). The rename done for hoshi was manual in Resolve; shared code was never fixed.
4. `work/build_timelines.py:5` `to_clip_infos(..., fps=60)` hardcodes 60 fps. Prompt says fps must come only from `ffprobe`/`inventory.json`, and Aommimama footage fps is unknown.
5. Skills list (line 38-47) omits `long-video-highlight-clipping`, which AGENTS.md says to load first.
6. `CATEGORIES`/definitions (`gameplay`, `fun`, `meme`) and `CLIPS_PER_VIDEO=4-8` were inherited from hoshi and never confirmed for Aommimama. 13 videos x 4-8 = 52-104 clips, and 13 > 8 so subagents must run in 2 rounds (line 62).
7. Line 34 still cites `HBD`/`Backrooms` as examples; harmless history but hoshi-specific. Line 55 plan file is named `...hoshi-...-v2.md` although it claims to be channel-neutral (the body has no hoshi references; only the filename does).
8. Line 98 limits names to 60 characters; Thai names plus a game name plus `-vdo` can exceed that. Truncation rule is undefined (current code just slices).

## Proposed approach
Fix the prompt table and create the job.json first (cheap, no footage), then fix the two code defects with TDD, then run the normal Task 0 of plan v2. Do not start inventory/transcribe until the open questions are answered.

## Tasks

### Task 1 — Add missing rows to prompt.md (edit only the table)
File: `prompt.md`, after the `RESOLVE_PROJECT` row add:
```
| `GAME_NAME` | `ถามรายวิดีโอ` | งานนี้มีหลายเกม: ใช้ชื่อเกมที่ผู้ใช้ยืนยันต่อวิดีโอ ห้ามเดาจากชื่อไฟล์ |
| `TIMELINE_NAME_FORMAT` | `{ชื่อคลิป}-{ชื่อเกม}-vdo` | ผู้ใช้กำหนด 2026-10-04 ไม่ใส่ id/category |
```
Also add `long-video-highlight-clipping` as the first bullet under "Skills ที่ต้องโหลดก่อนเริ่ม". Preserve CRLF.
Verify: `git diff --check` prints nothing; `python -c "print(open('prompt.md','rb').read().count(b'\n')==open('prompt.md','rb').read().count(b'\r\n'))"` prints `True`.

### Task 2 — Create the job file
File: `work/Aommimama/2026-09-aomimama/job.json` (copy keys from `work/hoshi_1489/2026-09/job.json`):
```
{
  "INPUT_DIR": "Z:\\Aommi-mama\\2026-09-aomimama",
  "CHANNEL": "Aommimama",
  "JOB": "2026-09-aomimama",
  "CLIP_MIN_S": 30, "CLIP_MAX_S": 180,
  "CATEGORIES": ["gameplay", "fun", "meme"],
  "CLIPS_PER_VIDEO": "4-8",
  "ASPECT": "16:9", "LANGUAGE": "th", "APPROVAL": "auto",
  "RESOLVE_PROJECT": null,
  "PLAYBACK_FPS_USER_CONFIRMED": null,
  "TRANSCRIBE_PAD_S": 90,
  "TIMELINE_NAME_FORMAT": "{ชื่อคลิป}-{ชื่อเกม}-vdo"
}
```
(Values for CATEGORIES/CLIPS_PER_VIDEO/ASPECT/APPROVAL stay provisional until Q2 is answered.)
Verify: `HIGHLIGHT_JOB=D:/agent-seacrh-virus-cut/work/Aommimama/2026-09-aomimama/job.json work/.venv/Scripts/python.exe -c "import sys; sys.path.insert(0,'work'); import config; print(config.WORK_DIR)"` ends with `Aommimama\2026-09-aomimama`.

### Task 3 — TDD: timeline name format (`work/build_timelines.py`)
1. Write failing test in `work/tests/test_timeline_name.py`:
```
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from build_timelines import timeline_name

def test_name_is_title_game_vdo():
    c = {"id": "c01", "category": "fun", "title_th": "ชื่อคลิป", "game": "Backrooms"}
    assert timeline_name(c) == "ชื่อคลิป-Backrooms-vdo"

def test_name_strips_illegal_chars_and_limit():
    c = {"id": "c01", "category": "fun", "title_th": 'a/b:c' + "ก" * 80, "game": "G"}
    n = timeline_name(c)
    assert len(n) <= 60 and n.endswith("-G-vdo") and "/" not in n
```
2. Run `work/.venv/Scripts/python.exe -m pytest work/tests/test_timeline_name.py -q` -> expect FAIL.
3. Implement: truncate the title (not the suffix) so the whole name is <= 60 chars; require `c["game"]` (raise `KeyError` if missing so a guessed game never slips in). Check `work/tests/test_candidates_schema.py` and the review schema in `work/templates/reviewer_brief.md` to add an optional `game` field (null = ask user).
4. Re-run -> expect `2 passed`, then run full `work/.venv/Scripts/python.exe -m pytest work/tests -q` with `HIGHLIGHT_JOB` set to the hoshi job (33 tests passed previously).
5. Commit to `main` only.

### Task 4 — TDD: fps from inventory (`work/build_timelines.py`)
Failing test: `to_clip_infos(c, "id", fps=30)` already works; add test that `main()` reads fps from `WORK_DIR/inventory.json` and errors when missing instead of defaulting to 60. Implement lookup per `source_id`, remove the `fps=60` default. Verify with pytest as in Task 3. Commit.

### Task 5 — Start the job (only after Q1-Q4 answered)
Follow `.hermes/plans/2026-10-04_013000-hoshi-highlight-timelines-v2.md` from Task 0 with `HIGHLIGHT_JOB` pointing to the new job.json. Run `python pipeline.py inventory` from `work/`; expected: `inventory.json` lists 13 videos, `downloaded.txt` excluded; report any mixed fps before Resolve.

## Risks / tradeoffs
- Changing `timeline_name` affects the already-finished hoshi job only if it is rebuilt; its `timeline_plan.json` is a saved artifact and is not regenerated.
- Per-video game names require user input; `APPROVAL=auto` conflicts with that unless names are collected up front.
- 52-104 clips means many Resolve timelines; long Resolve calls should be batched (`build_timelines.py calls <start> <end>`).

## Open questions for the user
1. RESOLVED 2026-10-04 (user): take the game name from the file name. Mapping re-read from the folder (no subfolders; `downloaded.txt` is the only non-video):
   - "alien shooter Last Hope" (own game, user-confirmed): 20260906 "alien shooter last hope"
   - "alien shooter" (separate game, user-confirmed): 20260906 "alien shooter", 20260910 "alien shooter 2"
   - Minecraft (Server Dreamlight 001/002/003)
   - League of Legends (003)
   - strinova (005, 006)
   - Becastled (001, 002, 003)
   - League of Legends: also 20260911 "หงุดหงิด ฉุนเฉียว" (user-confirmed: it is a League of Legends stream; the name has no game, so it needs a per-video override in job.json)
   This overrides the "do not guess game from filename" rule for this job only; derive it in code from the title between `【LIVE】` and ` - NNN`/` #tag`, with a per-video override in job.json, not hardcoded.
2. UPDATE 2026-10-04: user confirmed Q2 (settings OK). Q3 (Resolve): user wants 2 projects; recommendation below.
   Live facts: 13 files, 42.46 h total, all h264 1920x1080; 12 files at 60 fps, `Becastled - 002` at 30 fps (mixed fps; needs user decision). Resolve scripting API was NOT reachable (SCRIPTING_UNAVAILABLE; Studio: Preferences > General > External scripting using = Local) so the open project/project list could not be read.
   Proposed split by date (balanced, each <=8 videos so one subagent round each):
   - Project 1 `aomimama-2026-09-p1`: 20260906 alien shooter Last Hope, 20260906 alien shooter, 20260907 Minecraft 001, 20260910 alien shooter 2, 20260911 LoL stream, 20260914 Minecraft 002, 20260915 LoL 003 (7 files, 21.97 h)
   - Project 2 `aomimama-2026-09-p2`: 20260919 strinova 005, 20260920 strinova 006, 20260921 Minecraft 003, 20260922/24/26 Becastled 001/002/003 (6 files, 20.49 h)
   Implementation: one job/WORK_DIR, `RESOLVE_PROJECTS` mapping source_id -> project in job.json, run `build_timelines.py calls` per range.
2b. (original Q2) Are `gameplay/fun/meme`, 30-180 s clips, `4-8` per video, `16:9`, and `APPROVAL=auto` correct for Aommimama, or should I use `ask`/fewer clips?
3. Resolve: reuse the open project or create a new one (name)? Which one is currently open is checked live at job start.
4. Please confirm Playback frame rate in Project Settings after I report the footage fps.
5. OK to fix `timeline_name` and the 60 fps default in shared code (Tasks 3-4) and commit to `main`?
