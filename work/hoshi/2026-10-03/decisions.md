# Decisions (Task 0, answered by user)
- ASPECT: 16:9 1920x1080 (project already 1920x1080 @ 60fps)
- CLIPS_PER_VIDEO: 4-8
- APPROVAL: auto (no pause before building timelines)
- Resolve: reuse open project `2026-10-03` (4 clips online incl. 3 AV1, 0 timelines)
- GPU: faster-whisper large-v3 float16 works after `gpu_env.setup()` (pip nvidia-cublas-cu12 + nvidia-cudnn-cu12 in venv)
- Ruling: code lives in `work/`, artifacts in `work/hoshi/2026-10-03/` (WORK_DIR); plan's `work/<artifact>` means WORK_DIR/<artifact>.
