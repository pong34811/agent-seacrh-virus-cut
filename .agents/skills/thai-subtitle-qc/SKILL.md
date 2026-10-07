---
name: thai-subtitle-qc
description: Use only when the user asks for Thai subtitles or captions on a clip, to generate and QC them.
---

# Thai subtitle QC

House style forbids captions unless the user asks. When asked:
1. Load `thai-speech-to-text` for transcription and SRT/ASS generation.
2. Whisper Thai text is unverified. Check each line against the actual audio at its timestamp; flag low-confidence lines, collapse hallucinated repeated characters.
3. Write a QC report next to the subtitle file (see `analysis/captions/*_QC.md` for the format) listing checked lines, corrections and unresolved lines.
4. Tell the user which lines remain unverified before publishing.
