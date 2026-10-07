# Sakuyako-Cheris Highlight Selection and Resolve Project Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to execute this plan task-by-task. Use `delegate_task` for parallel review work only after one controller has created immutable, ID-keyed review packets. This plan describes a media-editing job, not a code feature; do not invent code tests or commits for footage/Resolve operations. Verify each media artifact and each Resolve state change directly.

**Goal:** Review all video files in `G:\My Drive\Projects\Sakuyako-Cheris\sakuyako-2026-09`, identify evidence-backed, self-contained horizontal highlights, and create one editable Resolve timeline per selected candidate in a new project in the user-designated Resolve project library/folder, with timeline names `{ชื่อคลิป}-vdo`.

**Architecture:** Use the existing `work/` pipeline and a job-scoped directory under `work/Sakuyako-Cheris/sakuyako-2026-09/`, keeping the Google Drive source footage read-only and all derived analysis in that job directory. One controller inventories/transcribes/samples media and owns all Resolve changes; delegate independent candidate-review batches to agents using immutable per-video packets, then validate/merge their structured results before creating Resolve timelines. “Footer” was a typo for footage/video source: the confirmed source folder is `G:\My Drive\Projects\Sakuyako-Cheris\sakuyako-2026-09`. The supplied screenshot shows the connected Resolve library as `google drive` and breadcrumb `Projects / Sakuyako-Cheris / 2026-09`; confirm the Resolve project destination folder in the live library before project creation.

**Tech Stack:** Existing Python job pipeline, ffmpeg/ffprobe, faster-whisper/GPU if available, Hermes `delegate_task`, DaVinci Resolve and its already-verified scripting bridge. Do not install software, change the project, or mutate Resolve during planning.

**Spec:** User request in the current conversation; repository guidance in `AGENTS.md`, `prompt.md`, `.agents/skills/house-style/SKILL.md`, and `llm_wiki/wiki/concepts/clip-selection.md`.

## Global Constraints

- Treat `G:\My Drive\Projects\Sakuyako-Cheris\sakuyako-2026-09` as the confirmed video source folder. The user corrected the path; do not use the previously observed Desktop folder as source unless the user later explicitly redirects.
- Planning-time read-only inspection of the confirmed folder found 19 top-level `.mp4` files plus `desktop.ini` (20 files total), with no immediate subdirectories. Re-inventory and probe live contents at execution; `desktop.ini` is not footage.
- User asks to create the Resolve project in the screenshot location. It shows Resolve library `google drive` and breadcrumb `Projects / Sakuyako-Cheris / 2026-09`. MCP readback confirmed the active project-manager folder is `2026-09` and it was empty before creation.
- Resolve project `sakuyako-2026-09` has now been created and saved via the existing local DaVinci Resolve MCP; unique ID `7b43f381-5630-49f1-8d35-a13bf4d8a99e`. `timelineFrameRate` was set to `30` and read back as 30.0; resolution is 1920x1080.
- Resolve `timelinePlaybackFrameRate` read back as 24. User selected 30 fps, but project rules say playback frame rate cannot be set/verified via API; a visible Resolve UI control is required before timeline creation. Do not create timelines until playback is confirmed at 30 through Project Settings.

- User confirms horizontal 16:9, automatic continuation into timeline creation (no approval pause), one timeline per selected candidate, timeline names exactly `{ชื่อคลิป}-vdo`, and a target of 3–4 or more clips per source video (not a hard ceiling). Titles must be based on source-verified event content; never pad with weak moments to meet a target.
- “Footer” was the user's typo for footage/video source, not branding or overlay assets. The confirmed source folder is `G:\My Drive\Projects\Sakuyako-Cheris\sakuyako-2026-09`; no footer graphic is requested.
- Clip duration is the job's 30–180 second working bound; available categories are `gameplay`, `fun`, `meme`. All 19 sources were probed at 1280×720, 30 fps; the user approved 30 fps, and `timelineFrameRate` is set to 30. The reusable `prompt.md` table contains stale Aommimama/60-fps values; the Sakuyako-specific job and current user messages govern. Playback frame rate still needs UI confirmation at 30 before timelines.
- Respect `.agents/skills/house-style/SKILL.md`: Resolve timelines are assembly only; no titles, captions, text cards, transitions, effects, speed ramps, music, or grading unless the user explicitly requests them. “Footer” is a typo for footage, not a request for a graphic.
- Do not convert to 9:16, upload, publish, or modify source media without authorization. Do not infer exact quotes, visual events, or punchlines from ASR alone; inspect source media and flag uncertainty.
- Save and verify Resolve mutations. Do not switch away from an unsaved project; do not change playback FPS via API. Ask for UI confirmation if playback FPS must be set.
- Requested up-front skills: load `long-video-highlight-clipping` if available, `superpowers:brainstorming`, `superpowers:subagent-driven-development`, and `superpowers:executing-plans`; use `delegate_task` for candidate-review fanout. Also load applicable Resolve/house-style skills if available. If a skill is unavailable in the active profile, report that and follow checked-in project guidance rather than pretending it was loaded.

## Review Focus

- Source footage with variable or mixed frame rates: determine actual per-file FPS before choosing timeline FPS; do not make a mixed-FPS assumption.
- Whisper hallucination, repeated text, or overlapping voices: candidate must still be verified against source audio/video; ASR-only jokes remain unconfirmed.
- Best moment may be understated rather than loud: audio-energy shortlist is a discovery aid, not a completeness or quality guarantee.
- Multiple candidate clips may cover the same setup/payoff: track timestamp overlap and retain only genuinely distinct beats unless the user prefers otherwise.
- “Footer” was a typo for footage; no branding graphic is requested.

---

## Current context / assumptions

- User asks to find interesting clips from the specified directory and create a Resolve project because none has yet been created. The only visible target from the supplied screenshot is the `google drive` Project Library and breadcrumb `Projects / Sakuyako-Cheris / 2026-09`.
- “Footer” was a typo for footage/video source, not a visual overlay. The confirmed source folder is `G:\My Drive\Projects\Sakuyako-Cheris\sakuyako-2026-09`; there are 19 MP4s plus `desktop.ini` in the last read-only inventory. The number 22 is not a clip count or project count.
- User says “footer เป็นของช่องSakuyako-Cheris.” Interpreted only as a branding requirement to clarify; it does not authorize creating a logo/footer or placing a graphic on timelines by itself.
- User confirms horizontal 16:9, automatic continuation into timeline creation (no approval pause), one timeline per selected candidate, timeline names exactly `{ชื่อคลิป}-vdo`, and a target of 3–4 or more clips per source video (not a hard ceiling). Titles must be based on source-verified event content; never pad with weak moments to meet a target.
- The source folder, Resolve library folder, and job-work folder are distinct: source is `G:\My Drive\Projects\Sakuyako-Cheris\sakuyako-2026-09`; screenshot target is Resolve `google drive` > `Projects / Sakuyako-Cheris / 2026-09`; work artifacts are in the repository job folder.
- “Footer” was a typo for footage/video source, not a branding or overlay request. There is no graphic footer to create.
- Current working tree was `main` at `07686f7`, with an unrelated untracked `analysis/` directory. Leave it untouched. No code or media processing has been run for this job.
- Skill discovery showed the requested Superpowers skills available. `long-video-highlight-clipping`, `livestream-highlight-clipping`, and `resolve-rough-cut` / media-pool / session skills were not available by their plain names in the active profile at planning time. Check available skill sources at execution; do not claim to have loaded absent skills.

## Questions to resolve before execution

Ask only unresolved points in one compact follow-up; user has already confirmed the source folder, landscape output, automatic continuation to timeline creation, naming format, and flexible clip quantity:

3. Duration and categories: no clip duration was specified; use existing project default 30–180 seconds and `gameplay`, `fun`, `meme` as review guidelines, but keep only candidates that form complete, interesting beats. Do not stretch/cut a moment poorly to fit. If a strong candidate falls outside the range, report its actual duration rather than silently including it or altering it.
## File map (planned; no files created yet)

- Create `work/Sakuyako-Cheris/sakuyako-2026-09/job.json`: explicit source path `G:\My Drive\Projects\Sakuyako-Cheris\sakuyako-2026-09`, channel/job labels, approved duration/count/aspect/language/categories, approval mode, and confirmed Resolve project mapping.
- Create `work/Sakuyako-Cheris/sakuyako-2026-09/` generated pipeline artifacts only: `inventory.json`, `audio/`, `scores/`, `transcripts/`, `frames/`, `review/`, `candidates.json`, `timeline_plan.json`, `resolve_clips.json`, and `report.md` as produced by existing pipeline stages.
- Do not change shared pipeline code, `prompt.md`, the wiki, or house style for this one-off job unless a demonstrated bug blocks the work and the user approves the code-change scope.
- No test files are planned: acceptance is based on exact media inventory, schema/constraint validation of candidate data, and read-back verification of Resolve project/timelines. If shared pipeline code must change, create targeted tests first and run them RED→GREEN before applying it.

## Step-by-step tasks

### Task 1: Confirm scope and resolve target (2–5 min)

- Present no new scope questions; user has already confirmed input folder, horizontal 16:9, automatic timeline creation, exact naming pattern, and flexible 3–4+ clips per source. Inspect Resolve Project Manager to verify the exact project folder and whether a same-name project exists; if there is any destination mismatch, stop and report it rather than guessing.
- Confirmed media input is `G:\My Drive\Projects\Sakuyako-Cheris\sakuyako-2026-09`; inspect live contents and report current video count. At planning time it contained 19 top-level MP4s and `desktop.ini`; exclude `desktop.ini`.
- Verify current Resolve project/library state read-only. In Resolve, confirm the screenshot-designated `google drive` library and `Projects / Sakuyako-Cheris / 2026-09` folder; list projects before creating anything.
- Expected: source inventory verified; destination library/folder confirmed; no existing target project overwritten; any genuine ambiguity reported before mutation.

### Task 2: Prepare job configuration and baseline inventory (2–5 min)

- Create `work/Sakuyako-Cheris/sakuyako-2026-09/job.json` with source path `G:\My Drive\Projects\Sakuyako-Cheris\sakuyako-2026-09`, channel/job labels, duration/category policy, `ASPECT: 16:9`, `LANGUAGE: th`, and approval mode `auto` to proceed through timeline creation. Set `CLIPS_PER_VIDEO` to `4-8`: this satisfies the user's 3–4-or-more target and existing project review/test defaults. Select only evidence-backed clips; if a source does not contain enough distinct good moments, do not pad it, and report the shortfall. Record exact timeline naming policy `{ชื่อคลิป}-vdo`. Add Resolve project destination only after confirming the screenshot folder in the live library.
- From `work/`, set `HIGHLIGHT_JOB` to the absolute job JSON path and run `python inventory.py` per the existing `AGENTS.md` pipeline guidance.
- Expected: current supported source videos have stable `v01..vNN` IDs, exact filename, duration, dimensions, FPS, codec/audio information. Compare inventory with the live source folder contents; exclude `desktop.ini`, explain skipped unsupported files; do not hardcode the previous 19 count.

### Task 3: Probe all media and identify technical constraints (2–5 min plus tool runtime)

- Use `ffprobe` via the configured project tooling on every inventory source; preserve exact per-file stream facts in `inventory.json`.
- Compare dimensions and FPS across sources. If footage is mixed-FPS or mixed-aspect, stop before Resolve project creation and obtain a specific timeline policy rather than silently converting or mismatching.
- Expected: every inventoried file has probe evidence; no unreadable/corrupt source is omitted silently; any FPS/aspect conflict is surfaced before the first timeline is created.

### Task 4: Build audio discovery and transcript/frame evidence (2–5 min plus tool runtime)

- Run existing stages from `work/` with the job environment: `python pipeline.py features`, then `python pipeline.py shortlist`, `python pipeline.py transcribe`, `python pipeline.py sheets`, `python pipeline.py packets` (confirm actual CLI stage names via `python pipeline.py --help` before execution; do not execute guessed commands if the CLI differs).
- Run long CPU/GPU work with `terminal` background + `notify=true`; monitor completion and inspect error logs/output. Run GPU smoke test first if transcription uses GPU. Do not install dependencies or transcode source video without separate permission.
- Expected: deterministic per-source candidate windows, Thai ASR marked unverified, six-frame sheets/packets where the pipeline produces them, and no claims about moments based only on loudness/transcript.

### Task 5: Delegate candidate review in disjoint batches (2–5 min per batch + reviewer runtime)

- Write immutable per-video reviewer briefs/packets under `work/Sakuyako-Cheris/sakuyako-2026-09/review/` using the user's flexible target of 3–4 or more candidates per source video and the approved 30–180-second/category guidelines. Never pad with weak or duplicate clips just to reach the minimum. Ensure each packet references only its own source ID and exact available paths.
- Dispatch one `delegate_task` reviewer per video (19 independent units; batch at most 8 concurrent tasks, then continue with the remaining IDs). Require agents to inspect packet and visual evidence, return only the required JSON at the exact per-video path, label uncertainty, and never modify Resolve or the originals.
- Controller validates every returned JSON with the existing project schema/tests and verifies candidate IDs, source IDs, start/end ordering, duration limits, no overlaps per approved policy, source bounds, exact category values, and every required video has a result. Do not trust agent summaries in place of data/schema checks.
- Expected: verified coverage count equals number of inventoried videos; every candidate has traceable source ID and start/end timestamps; malformed/uncertain candidates are rejected or marked for manual review, not silently passed.

### Task 6: Controller evidence check and choose the final selects (2–5 min per review batch)

- Independently inspect source footage/audio around every proposed interval, including setup and payoff; correct cut points and names only when supported by source evidence. Keep the ranking heuristic non-predictive; no claim of viral performance.
- Deduplicate repeated/overlapping story beats and verify selected count against the user's chosen policy. If approval mode is `ask`, present the candidate slate and wait before Resolve timeline creation.
- Expected: `candidates.json` and `report.md` distinguish confirmed observations from ASR uncertainty, list exact source time ranges and rationales, and meet the confirmed count/duration rules; if user approval is required, no timelines have yet been created.

### Task 7: Create/confirm Resolve project in the specified library (2–5 min)

- Project `sakuyako-2026-09` has already been created and saved in the verified `google drive` library folder `Projects / Sakuyako-Cheris / 2026-09`; confirm by ID `7b43f381-5630-49f1-8d35-a13bf4d8a99e` before any further write.
- Use the confirmed technical settings: 1920x1080 project raster (16:9) and `timelineFrameRate=30` (same as all 19 probed source files). The project currently reports `timelinePlaybackFrameRate=24`; before creating any timeline, wait for the user to set Playback frame rate to 30 in the Resolve Project Settings UI and confirm it, because the scripting API cannot set/verify that field.
- Import only source files required by selected candidates and confirm they are online in Media Pool; if any are offline, stop before timeline assembly and report options rather than creating proxies unasked.
- Expected: project identity/folder/settings read back; media online; playback FPS confirmed 30 by user; no existing project overwritten.

### Task 8: Create one assembly-only timeline per selected clip (2–5 min per batch)

- Generate `timeline_plan.json` with exact source IDs, in/out frames/timecodes, project/timeline FPS, source FPS, and final timeline names using exactly `{ชื่อคลิป}-vdo`; derive concise Thai `{ชื่อคลิป}` from the verified segment and keep it unique without IDs/categories unless necessary to avoid a real collision (if collision, pause and ask rather than silently changing the requested format).
- Use the verified Resolve bridge/UI and one controller for all mutations. Create each timeline from the planned source range with original 16:9 aspect and source audio. No titles/captions/music/effects/grading/graphics. “Footer” is a typo for footage and does not request a visual overlay.
- Space serialized structural mutations, save at safe checkpoints, and read back timeline IDs, names, clip counts, exact ranges, track layout, and project folder.
- Expected: exactly one timeline per selected candidate; every timeline contains the right source/range and no unapproved embellishments; all created timelines are read back and match the plan.

### Task 9: Final QC and handoff (2–5 min)

- Re-read Resolve project/timeline list and compare against `timeline_plan.json` and candidate report. Play/inspect each selected interval in Resolve for source correctness, event context, audio sync, and clean in/out. Verify project saved and still in the designated library/folder.
- Record any skipped sources, uncertain candidates, offline files, and footer status in `work/Sakuyako-Cheris/sakuyako-2026-09/report.md`.
- Expected: counts match across approved candidates, plan, and actual Resolve timelines; all source intervals are valid; deliverable project is editable and saved. Report paths, verified timeline count, and any deferred issues; do not claim render/export/publication unless separately requested and completed.

## Tests / validation

- This is not a software implementation plan; do not invent TDD or commits for media processing. If a necessary code change emerges, stop and write a scoped code plan with the relevant tests before changing shared pipeline code.
- File-level validation: live inventory reconciliation, ffprobe output per source, JSON/schema checks, clip-count/category/duration/source-bound/non-overlap checks.
- Media validation: inspect actual audio/video around each candidate; ASR is a navigation aid only.
- Resolve validation: read back project/library/folder, exact project identity/settings, saved state, timeline count, names, source IDs, frame/time ranges, and playback QC.
- Preserve unrelated `analysis/` untracked content; no cleanup, commit, push, render, or upload is included.

## Risks, tradeoffs, and open questions

- **Remaining decisions:** footer meaning/files/placement and clip duration are not specified. The user has already confirmed input folder, horizontal format, automatic timeline creation, timeline naming, and flexible candidate quantity; do not ask those again. Confirm the Resolve destination folder in the live library using the supplied screenshot.
- The input folder is on Google Drive and currently has 19 MP4 files plus `desktop.ini`; duration/codecs and total derived-analysis storage are unknown until probed. Use job-scoped artifacts and check free space without deleting files.
- The Resolve screenshot's library breadcrumb is `Projects / Sakuyako-Cheris / 2026-09`, whereas the media source folder is `sakuyako-2026-09`; verify and keep the Resolve destination and source roles distinct.
- “22 footer items” is branding scope, not the number of footage files, candidates, or timelines. Ask what these are and how to apply them before making any graphic changes.
- Loudness/transcript screening can miss quiet comedy, and Thai ASR can hallucinate. Candidate selection requires visual/audio verification; delegated reviews reduce latency but can vary in judgment.
- Source frame rates may differ. Probe first; ask only if the verified media does not support a safe common timeline rate.
- Do not let repository assembly-only defaults imply footer use; footer creation/overlay requires actual supplied assets and clear placement instructions.
- Neither candidate scores nor edit quality guarantee YouTube reach, copyright clearance, or monetization.
