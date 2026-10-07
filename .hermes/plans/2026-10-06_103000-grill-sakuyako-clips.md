# Grill Review — Sakuyako-Cheris Highlight Selection

> **Mode:** PLAN MODE — no implementation, no file edits, no Resolve mutations.
> **Skill:** `grill-me` (adversarial plan interview). This plan maps the clip-selection plan as a design tree and grills every branch before the selects are locked.
> **Existing plan:** `.hermes/plans/2026-10-05_151500-sakuyako-cheris-highlights.md` (Tasks 1–4 in progress; timelines not yet created).
> **Review data:** `work/Sakuyako-Cheris/sakuyako-2026-09/review/` — 19 briefs, 19 packets, 72 candidates, 89.59 min.

## Goal

Stress-test the Sakuyako-Cheris clip selection through adversarial questioning: are the selected candidates genuinely interesting, and do they resemble the kind of highlight clips that perform on YouTube, before Resolve timelines are created.

## Current context / assumptions

- 19 source MP4s, all 1280×720 30fps H.264/Opus, from `G:\My Drive\Projects\Sakuyako-Cheris\sakuyako-2026-09`.
- 72 candidates (v01–v19), scores 0.70–0.78, categories: gameplay / fun / meme.
- ASR uncertainty flagged on most candidates — dialogue claims are unverified.
- `video_analyze` failed on source previews (Codex Responses does not accept video_url).
- v05 has no evidence-rich segment; dropped candidates: v03-06 (out of bounds), v03-03 (ASR-only, no visual support).
- Test pass status is not a reliable indicator for this task; verify after any change.
- Resolve project `sakuyako-2026-09` created (ID `7b43f381-...`), playback FPS still 24 in UI — timelines blocked pending user UI confirmation.

## Architecture / proposed approach

Run the `grill-me` frontier-rounds interview against the clip-selection plan, using the review JSON/packet data as evidence. Round 1 settles scope definitions (what "interesting" and "YouTube-similar" mean); subsequent rounds probe each design-tree branch: candidate quality, category balance, ASR-reliance risk, deduplication, and YouTube-fit. No code or media mutation until the frontier is empty and the user confirms alignment.

## Step-by-step tasks

### Round 1 — Frontier: define "interesting" and "YouTube-similar"

❓ Q1 — What does "interesting" mean for this stream? Options:
  (a) High-energy gameplay moments only (kills, fights, WIPED OUT)
  (b) Reactions / chat interaction (fun category, ASR-drawn banter)
  (c) Story/context clips with setup-payoff (fun + gameplay mixed)
  (d) Personal preference — user lists 3–5 reference YouTube VTuber highlight clips
➡️ Recommendation: (d) — ask for 3–5 reference clips. "Interesting" is subjective; anchors from the user's own taste prevent the selector from guessing.

❓ Q2 — What does "คลิปวิดีโอใน YouTube" (YouTube video clips) mean here? Options:
  (a) Clips that look like YouTube Shorts (fast-cut, 15–60s, punchy)
  (b) Clips that look like YouTube long-form highlights (3–10 min, narrative)
  (c) Clips similar to other VTuber highlight channels (comp style)
  (d) Not sure — needs examples
➡️ Recommendation: (d) — ask for 2–3 reference URLs or channel names before judging similarity.

❓ Q3 — How many total clips does the user want? Current 72 candidates across 19 sources (~3.8/source). Options:
  (a) Keep all 72 (dense selection)
  (b) Tighten to 3–4 per source (~57–76)
  (c) Tighten to 1–2 per source (~19–38), only the strongest
➡️ Recommendation: (c) — tighter set forces evidence-only keeps; weak candidates surface faster.

### Round 2 — Frontier: candidate quality (after Q1–3 settle)

❓ Q4 — Score threshold: current min 0.70. Raise to 0.75? Drop candidates below?
❓ Q5 — Category balance: current split gameplay/fun/meme — does the user want more of one?
❓ Q6 — ASR-unverified candidates (most of them): reject all below a confidence floor, or keep and flag for manual listen?
❓ Q7 — v05 (no evidence-rich segment): drop entirely or keep the best-of-bad-options?

### Round 3 — Frontier: dedup & overlap

❓ Q8 — Overlapping story beats (e.g., v03-01/v03-02 both LaoLan fight): keep both or merge to one?
❓ Q9 — Cross-source duplicates (same moment referenced from different vNN): keep one, mark others as derived?

### Round 4 — Frontier: YouTube-fit check

❓ Q10 — After selects are locked, sample 5 clips: do they look like YouTube highlights? If not, what's the gap (pacing, audio, content type)?

## Tests / validation

- No code tests apply (media selection, not code). Validation is evidence-based:
  - Every surviving candidate must have source-verified frame evidence (contact sheet + packet), not ASR-only.
  - Category/duration/bounds re-validated against `review/<vNN>.json` schema after each round.
  - Count of selects matches user's chosen per-source target.
  - Reference clips provided by user are compared visually/thematically, not by hash.

## Risks, tradeoffs, and open questions

- **ASR unreliability:** Thai ASR hallucination is the largest risk. Any candidate whose title/reason depends on ASR dialogue must be listen-verified before committing to a timeline.
- **video_analyze failure:** Codex Responses cannot ingest video — visual QC must be manual (contact sheets + frames), not automated.
- **Score heuristic non-predictive:** `score` is a discovery ranking, not a quality guarantee. Do not cite scores as evidence of YouTube performance.
- **Reference clips missing:** Rounds 1–2 cannot answer Q1/Q2 without user examples. Block on this — do not guess.
- **Resolve playback FPS:** Project is 30 fps but UI playback is 24. Timelines remain blocked until user confirms in Project Settings.
- **Scope creep:** "grill-with-docs" skill name suggests documentation review, but the installed skill is `grill-me` (plan interview). If the user intended docs review (e.g., `llm_wiki/`), that's a separate frontier round.

## Open questions to user (Round 1)

1. What does "interesting" mean for this stream? (a/b/c/d above)
2. What does "คลิปวิดีโอใน YouTube" mean here? (a/b/c/d above)
3. How many total clips desired? (a/b/c above)
4. Any reference YouTube clips/channels to compare against?

--

Plan written in plan mode only. No files created, no media mutated, no Resolve changes.