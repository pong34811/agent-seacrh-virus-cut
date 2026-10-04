# Project knowledge entry point

This repository supports selecting and assembling Thai VTuber livestream highlights for YouTube. The maintained project wiki is in `llm_wiki/`.

Before a clip-selection or editing task:

1. Read the current user brief and `prompt.md` for current job variables and permissions.
2. Read `llm_wiki/wiki/index.md`, `llm_wiki/wiki/overview.md`, and relevant pages, especially `llm_wiki/wiki/analyses/skill-integration.md` and `llm_wiki/wiki/concepts/clip-selection.md`.
3. Read `.agents/skills/house-style/SKILL.md` and the applicable installed skills. Wiki summaries supplement actual skills; they do not substitute for them.
4. Inspect current footage and tool state. Historical wiki entries and raw snapshots cannot establish current input paths, file inventories, frame rates, approvals, or Resolve state.

Use the wiki to reuse sourced preferences, candidate-selection criteria, and recorded feedback. Treat experimental ranking criteria as unvalidated heuristics, never predictions of views. Require a real source file and verifiable timestamps for each candidate; do not invent observations from a transcript alone.

For wiki-only requests, maintain the wiki without starting footage processing, Resolve operations, rendering, or uploads. Explicit current user instructions take precedence over older documents. If a live task document conflicts with the wiki, inspect the current document and preserve the discrepancy as dated knowledge rather than silently choosing stale instructions.

When maintaining the vault, read and follow `llm_wiki/AGENTS.md`. Keep raw originals and footage immutable. Save derived job artifacts under the current `WORK_DIR`; the wiki stores source-backed summaries and reusable learning. Do not upload to YouTube unless explicitly requested.

## Skills

Hermes skills live outside this repo (`~/.../hermes/skills`); `house-style` is also kept in `.agents/skills/`. Load the ones that apply before a job:

- `long-video-highlight-clipping` (media): the full funnel and the pitfalls learned from real runs. Load first. `livestream-highlight-clipping` is its shorter order-of-work view.
- `house-style`: the user's editing preferences. Timelines are assembly only: no titles, captions, effects, music or grading unless the user asks.
- `resolve-rough-cut`, `resolve-media-pool`, `resolve-session`: Resolve MCP rules (end-frame exclusivity, current-folder import, session setup).
- `llm-wiki` (research): maintaining `llm_wiki/`; includes `scripts/lint_vault.py`.

## Pipeline code

Code lives in `work/` (`config.py`, `pipeline.py`, `inventory.py`, `features.py`, `shortlist.py`, `transcribe.py`, `contact_sheet.py`, `packets.py`, `briefs.py`, `snap.py`, `windows.py`, `resolve_clips.py`, `build_timelines.py`, `gpu_env.py`; helpers in `work/tools/`, the reviewer prompt in `work/templates/reviewer_brief.md`) with pytest tests in `work/tests/`. Never hardcode a channel, folder or file list: job variables are in `work/<channel>/<job>/job.json` (mirrored by the `prompt.md` variables table), selected with the `HIGHLIGHT_JOB` environment variable (path to a `job.json`; `config.py` has a default). Per-job artifacts stay in that job folder (`audio/`, `scores/`, `transcripts/`, `frames/`, `review/`, `inventory.json`, `candidates.json`, `timeline_plan.json`).

Setup and checks (run through the `terminal` tool):

- Create the venv: `python -m venv work/.venv`, then install `numpy faster-whisper pillow pytest` (Windows NVIDIA GPUs also `nvidia-cublas-cu12 nvidia-cudnn-cu12`; `gpu_env.setup()` makes the DLLs visible).
- Tests: `work/.venv/Scripts/python.exe -m pytest work/tests`. `test_review_files_match_schema` fails by design until every video has a `review/vNN.json`.
- Stages: `python pipeline.py inventory|features|shortlist|transcribe|sheets|packets|briefs` (run from `work/`; outputs are cached). Run long stages as background processes. Before `transcribe`, smoke-test the GPU with `python tools/gpu_smoke.py`.
- `briefs` writes `review/<id>.brief.md` per video from the template; pass each file's text as the `context` of one `delegate_task` task (one subagent per video, writes `review/<id>.json`). The schema test is the gate.
- Resolve: save the MCP `media_pool probe_media_pool` JSON to a file, run `python resolve_clips.py <probe.json>` (writes `resolve_clips.json`, fails if a video is missing), then `python build_timelines.py` (writes `candidates.json`, `timeline_plan.json`) and `python build_timelines.py calls <start> <end>` to print ready MCP payloads for `create_timeline_from_clips`.
- Wiki lint: `python tools/lint_vault.py ../llm_wiki` (a copy of the `llm-wiki` skill script).
- Config: ffmpeg/ffprobe come from `HIGHLIGHT_FFMPEG` / `HIGHLIGHT_FFPROBE`, else the bundled Hermes copy, else `PATH`.

## Working rules

- Footage folders are read-only. Re-read footage, `ffprobe` facts, Resolve project state and clip ids at the start of every job; never reuse them from an old job or from the wiki.
- Ask all open questions once up front (aspect, clips per video, approval pause, Resolve project) and skip any the user already answered.
- Whisper Thai text is unverified: treat quotes and punchlines from it as unconfirmed, have reviewers flag low-confidence clips, and surface those ids in the report. Filenames do not reliably tell the game or topic.
- Verify subagent output with the schema pytest, not their summaries.
- Playback frame rate cannot be set or checked through the API: ask the user to confirm it in Project Settings.
- Use `main` only: commit and push directly to `main`, no feature branches (user instruction, 2026-10-04). Do not auto-commit `llm_wiki/` changes if its rules forbid it. Check a claim (hash, file read) before writing it into the append-only wiki log.

## Current state (dated 2026-10-04; verify before relying on it)

The first job (`work/hoshi/2026-10-03/`) produced 31 clips and 31 Resolve timelines in project `2026-10-03`; the user approved the set without per-clip reasons (see `llm_wiki/wiki/analyses/hoshi-2026-10-03-run.md`). No published-video analytics exist yet.
