# Media and subtitle workflow boundaries

Source-safe speech transcription, Thai subtitle QC and build-aware Resolve scripting are separate steps. This guide is self-contained; the named Hermes skills below are optional integrations, not repository dependencies.

## Choose the requested operation

| Request | Optional Hermes skill | Deliverable |
|---|---|---|
| Probe, explicitly authorized trim/extract/transcode | `ffmpeg-media-ops` | Technical report or verified new media output |
| Whisper speech-to-text with FFmpeg preparation | `whisper-ffmpeg-transcription` | Raw transcript, DRAFT SRT and provenance |
| Thai wording, readability, cue and audio review | `thai-subtitle-qc` | Candidate SRT, change log and review coverage |
| API capability lookup or Python automation | `resolve-scripting` | Build-specific guidance or authorized changes with readback |

A probe request does not trigger transcription. An existing SRT can receive text-only QC without Whisper or Resolve. A transcription request does not implicitly authorize timeline changes or persisted intermediate audio. Do not route ordinary subtitle QC into SFX placement.

## Runtime and source safety

Discover executable and interpreter paths from the actual environment. Inspect installed packages and model cache before loading a model; named models can initiate downloads. If the current interpreter lacks Whisper, inspect the selected project environment before claiming it is absent from the machine. Never install packages, download weights or upload audio without permission.

Probe source duration and audio streams before choosing dialogue. Explicitly select the relevant stream/channel; the first audio stream is not necessarily speech. Preserve source files: no overwrite, proxy, relink, transcode or persisted media derivative unless the user authorized that exact operation. Scratch output is not an exemption. Decode into bounded memory/pipe for requested analysis when supported; ask before generating intermediate WAV files when required by a backend.

For authorized transformations use distinct output paths, check collisions and enable non-overwrite behavior. Inspect exit status and stderr, then probe the exact result. Stream-copy video cuts are not inherently frame exact. Preserve partial-job status and inspect state before retries rather than duplicating work.

## Transcribe to a draft

1. Identify the source, requested range, language and task. For Thai use a multilingual model and transcription rather than translation.
2. Verify backend-specific flags, local assets and device. OpenAI Whisper and faster-whisper are not interchangeable command interfaces. Faster-whisper may decode through PyAV without standalone FFmpeg; disclose backend changes rather than silently substituting them.
3. Run within the authorized scope. A pilot can establish runtime cost; CPU fallback needs suitable precision and an explicit speed trade-off, not a fabricated estimate.
4. Preserve raw segments and write new UTF-8 text/JSON/SRT sidecars. Label outputs DRAFT; ASR confidence and word timestamps are estimates.
5. Validate every cue structurally and report missing coverage, repeated phrases and suspected music/game-audio hallucination for review. Do not invent dialogue to fill gaps.

## Time and handoff contract

Each stage reports:

- `input`: source identity, authorized operation, selected stream and range.
- `time_basis`: seconds/frames, source vs timeline origin, actual FPS when needed, trim/start offsets, gaps and retime mapping.
- `artifacts`: actual paths with raw/draft/candidate/delivery roles.
- `runtime`: interpreter/executable, backend/model/language/task/device when used.
- `qc`: cue count, structural errors, text review, audio-reviewed and unresolved intervals.
- `verification`: actual evidence, tolerances, failures and blockers.

For unretimed material, map source event time relative to source-in onto record-in. Do not confuse source frames, timeline frames or start timecode. Unsupported reverse/variable retime or nested-clip mapping must be flagged; a source-time transcript must not masquerade as timeline-synced SRT.

## Thai text and audio QC

Read full context, preserve colloquial speech/particles/code-switching and avoid guessing proper names. Thai spaces are not reliable word boundaries; segment by readable phrases without detaching combining marks. Readability targets depend on delivery requirements, not a hardcoded FPS or universal words-per-line limit.

Parse all SRT blocks and check ordered unique indices, valid timestamps, nonnegative starts, positive durations, overlaps and nonempty text. Report invalid intervals before guessing corrections. Overlap may be intentional dialogue; an unverified rewrite is not an automatic fix.

Text-only review is not audio fidelity review. If audio or an audio-capable tool is unavailable, say so and retain unresolved wording. Multiple ASR models agreeing is not proof. Log the intervals actually heard; partial review stays partial. Suspected hallucinations must not be silently deleted from final captions without evidence.

Write a candidate to a new path and keep the original. Every change records cue ID, before/after, reason, evidence and uncertainty. Re-parse and compare counts/timecodes/text against the change log. A valid SRT alone does not prove synchronization, styling or delivery inside Resolve.

## Resolve API and Python boundaries

For plan-only/offline questions read documentation without connecting to or launching Resolve. For authorized live work identify product/edition, exact patch/build and current project/timeline before mutation. Distinguish native method names from MCP actions; inspect actual schemas and definitions.

Use the shipped documentation for the actual installation, the bundled text and typed reference, and versioned API truth. A recorded finding on another build is a prior, not universal support. Dynamic proxies may fabricate attributes: `hasattr` is not proof of method existence, and Fusion `dir()` can omit real methods. Unknown support remains unknown until safely established.

Native auto-caption uses Resolve's engine, not Whisper. Never invent a Thai language constant. The absence of a Thai constant in one reference does not establish every build's support. Some older subtitle limitations and later observations conflict; report the evidence/build instead of asserting universal impossibility or success.

Importing an SRT into the Media Pool is not proof of timeline placement. Protect existing subtitle tracks. Before writes establish recovery and exact target/track/FPS/start offsets, then verify cue count, text and positions where the build exposes them. If readback is incomplete report the gap. A workaround producing a new or nested timeline requires approval; do not substitute it for modifying the original. Do not promise scriptable subtitle styling from SRT alone or patch the project database as a silent fallback.

For Python, distinguish module discovery, native-library load, connection and current project availability. A successful import followed by `scriptapp` returning None is a connection failure, not authorization to create a project. Inspect the repo connection helper and report transport, including an existing bridge fallback. Do not start a bridge, change global `PYTHONHOME`, switch modes, or repeat a crashing import without diagnosing scope and runtime first.

## Existing analysis and creative workflows remain intact

This guide does not disable the repository's Resolve-target media-analysis defaults. When a user requests media analysis, follow the canonical analysis guide: visuals, transcription, persistence, metadata and Media Pool marker writeback remain enabled unless the user opts out; deferred host vision must reach commit. Transcription-only/text-QC requests are distinct workflows, not an excuse to downgrade requested full analysis.

Source-safety, recoverable edits and frame-first grading requirements in `AGENTS.md` still apply. No color or SFX change is implied by subtitle work.

## References

- [Canonical media analysis](media-analysis-guide.md)
- [Audio/Fairlight boundary](../kernels/audio-fairlight-kernel.md)
- [Bundled scripting text](../reference/resolve_scripting_api.txt)
- [Typed scripting API](../reference/DaVinciResolveScript.pyi)
- [Versioned limitations](../reference/api-limitations.md)
- API evidence source: `src/utils/api_truth.py`
- Connection implementation: `src/utils/resolve_connection.py`

Read the actual files and running-build context before applying method-specific advice. This guide supplies process, not a new API surface or a claim of live validation.
