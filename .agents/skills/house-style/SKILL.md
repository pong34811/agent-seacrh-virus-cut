---
name: house-style
description: Use when assembling, restructuring, or refining video edits for the user so established pacing, shot selection, caption, cut-point, and delivery preferences are applied consistently.
user-invocable: false
---

# House Style

This file records the user's established editorial preferences so they travel with this project and can be carried into other projects. Read it before any edit task. Append to it when the user gives a correction that should apply to future work.

## Capture protocol

When the user corrects an editorial decision—such as rejecting a cut, changing a shot choice, adjusting a duration, or saying a result does not match their intent—make the correction and capture the reusable rule here.

Each entry should state:

- **Rule:** a concrete instruction that can be checked in the edit.
- **Why:** the user's reason or intended viewing experience.
- **Trap:** the likely mistake that makes the preference easy to miss.

Keep rules falsifiable. For example, “cut on motion” can be checked; “make it feel dynamic” needs a concrete clarification before it can guide an edit. Add preferences that generalize to future work. Revise a rule if later feedback shows it is stale or too broad.

## Pacing and rhythm

For short-form Thai subtitle passes, keep each caption to at most three short words and about 14 Thai characters, with no more than 1.5 seconds on screen. Write Thai captions without spaces between Thai words; keep spaces only around Latin terms such as names. Shorten the hold when speech arrives faster. Group by natural phrase and spoken rhythm rather than splitting mechanically to meet a word count. The goal is quick mobile reading without unnatural spacing.

## Shot selection

_Not yet captured._

## Cut points

_Not yet captured._

## Structure and openings

_Not yet captured._

## Rejected by default

For rough-cut assembly tasks, do not add titles, captions, text cards, transitions, effects, speed ramps, music beds, or grading unless the brief asks for them. This default does not override an explicit request for any of those elements.

## Delivery conventions

- **Rule:** Name Resolve highlight timelines exactly `{ชื่อคลิป}-{ชื่อเกม}-vdo`, without candidate/source IDs or category prefixes. Preserve IDs in job metadata. Use a verified or user-supplied game label; ask about labels for non-game chat segments when unspecified.
- **Why:** The user wants only the clip title, game name, and `vdo` suffix in the timeline name.
- **Trap:** Reusing `<id>_<category>_<title>`, or assuming every segment contains the game named in the source filename.

### Apply and verify timeline names

1. Read the current brief and `prompt.md`. Use the exact game label the user confirms for the requested set, including chat segments when the user applies one label to the whole set. Do not hardcode a game name for future jobs or ask again after confirmation.
2. Build each name as `{ชื่อคลิป}-{ชื่อเกม}-vdo`, preserving the clip title and game label. Do not add IDs, categories, dates, or extra suffixes. Keep ID-to-timeline mappings in job artifacts, not the displayed name. Resolve duplicate names with the user rather than silently appending a number.
3. For existing timelines, read the live project and timeline list first. Select each target by its stable timeline ID, then call `timeline set_name` sequentially. Rename only: do not rebuild timelines or change clips, tracks, frame ranges, or source files.
4. Save the project, then read `timeline list` back. Verify every requested timeline ID has its exact planned name and the timeline count is unchanged. A successful rename call alone is not verification.
5. Update `timeline_plan.json` and the current job report to match the verified names. Preserve candidate IDs and source timestamps. Report the verified count and any unresolved names; do not claim the shared pipeline's naming code changed unless it was actually edited and tested.

## Color and look

This file does not define color-grading taste. Follow the active project's brief and references for color and look decisions.

## Portability

This is the user's preference file, intentionally kept with the project at the user's request so it can travel to other projects. Keep project-wide requirements in the project's own documentation. Add only preferences the user wants carried forward with this file.
