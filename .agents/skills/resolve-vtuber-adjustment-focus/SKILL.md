---
name: resolve-vtuber-adjustment-focus
description: Use when zoom-focusing VTubers with Adjustment Clips.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Resolve, VTuber, Adjustment-Clip, Framing, Safety]
---

# VTuber Adjustment Clip focus

## When to Use

Use for subtitle-led avatar close-ups using existing or newly approved Adjustment Clips on dedicated video tracks.

Use only for authorized live edits. Read project house style/operating notes and preserve approved raster/FPS, underlying clips and source media.

## Discovery and recovery

- Verify project/timeline IDs, exact build, per-timeline record FPS, playback FPS, raster, every video/audio/subtitle/overlay range, source metadata and enable/lock states.
- Treat selected/current-item fallback as ambiguous. If the tool returns a GIF under the playhead with a selection-unavailable warning, it is not an approved Adjustment template. Ask to identify the template or approve a new Adjustment Clip.
- Work on verified variants. Reject destination original ID and mismatched variant names on every mutation/render. Save/export DRP and check ZIP integrity/hash; distinguish archive validation from a restore test.
- Compare all protected item names/record/source ranges, properties, audio/fades, subtitle text, media paths and metadata. Ignore only a proven read-only reference counter such as Usage, increased by DuplicateTimeline. Original audits also require exact track count and item IDs.
- Capture UI/marks/locks freshly; put duplication inside try/finally. Run independent cleanup callbacks even after an activation/lock failure so original restoration is still attempted. Collect errors and publish PASS only after exact original readback succeeds.

## Insertion and Fusion

- Lock all original video/audio/subtitle tracks; add a dedicated named video track and leave only it unlocked. Space structural mutations around 1.2s.
- For [start,end), set marks start/end-1 and playhead at start, insert Adjustment Clip, then clear marks. The insertion API has no destination-track argument: require exact actual track/range and audit all protected tracks immediately. Locks alone do not prove absence of ripple.
- On observed Studio21.1.0.17, a source-less Adjustment generator can use AddFusionComp: MediaIn -> Transform -> MediaOut. Probe current build; set numeric Size and point Center outside comp.Lock. Inspector Pan/Tilt are not Fusion Center coordinates.
- Verify clip enabled, comp count, node count, bypass state, actual Input connections and values. On the observed build GetInputList entries with INPS_ID=Input and GetConnectedOutput().GetTool() exposed wiring. Numeric readback alone cannot prove the effect is in the image path.
- Persist exact-prefix progress. Resume existing adjustments without duplicating. Repair only an unambiguous task-owned partial comp; refuse valid graphs with unexpected values or unrelated comps.

## Framing and QC

- Use subtitles as cue candidates, not proof of emotion. If video/audio understanding is unavailable, report it rather than inventing listening results. Avoid focus overlapping unrelated GIFs that an upper adjustment would also transform.
- Calibrate each distinct avatar layout and problem cue. Preserve head/hair/accessories/face, important fingers/hands/controller, small headroom and near-central placement. A baked-in corner avatar constrains pure-transform centering; never force a crop.
- Inspect Resolve-rendered beginning/middle/end per cue. Contact sheets decoded from sources and property values are not Fusion visual proof.
- Native stills may omit subtitles. Inspect real burn-in/viewer output. Long captions can cover fingers despite safe head framing: adjust only the approved Adjustment Clip or defer the cue; never silently move/restyle captions.
- Canvas must have no uncovered pixels. Wrap/Duplicate/Mirror may repeat scenery or avatars; inspect actual exports before accepting.

## Rendering and handoff

- Save render state as a uniquely named temporary preset; pin a live available base preset and explicit codec/range/video/audio/subtitle settings. Restore preset/format/codec/mode/queue and UI separately.
- Use tracked background terminal+notification for renders exceeding foreground/RPC timeouts. A killed foreground caller can orphan rendering and skip finally. Identify exact own job/preset, stop only that operation, then restore/read back. Never kill by ResolvePython image name: the MCP server can use that interpreter.
- Discover hardware codecs; available H.264 NVIDIA can avoid a slow software re-render. Require Complete, nonempty file and ffprobe video/audio/raster/FPS/frame-count checks.
- Seek individual frames from completed previews instead of re-decoding a long movie for each contact sheet. Count/persist a frame manifest and resume missing outputs after timeouts.
- Save and read back every planned adjustment and protected target, export final DRP, restore original UI/locks, and report sampled visual QC separately from unperformed listening or backup restore tests.
