import os, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
# tests need a job to load; config.py has no default. Explicit HIGHLIGHT_JOB still wins.
os.environ.setdefault("HIGHLIGHT_JOB", str(pathlib.Path(__file__).parent / "hoshi" / "2026-10-03" / "job.json"))
