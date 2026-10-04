"""Single source of truth for job parameters. Reads job.json (see prompt.md variables table)."""
import json, os, pathlib

CODE_DIR = pathlib.Path(__file__).parent
JOB_FILE = pathlib.Path(os.environ.get("HIGHLIGHT_JOB", CODE_DIR / "hoshi" / "2026-10-03" / "job.json"))
_job = json.loads(JOB_FILE.read_text(encoding="utf-8"))

FFBIN = pathlib.Path(r"C:\Users\warit\AppData\Local\hermes\tools\ffmpeg-9.0.1-win32-x64\bin")
FFMPEG = str(FFBIN / "ffmpeg.exe")
FFPROBE = str(FFBIN / "ffprobe.exe")

INPUT_DIR = pathlib.Path(_job["INPUT_DIR"])
CHANNEL = _job["CHANNEL"]
JOB = _job["JOB"]
WORK_DIR = JOB_FILE.parent
CLIP_MIN_S = _job["CLIP_MIN_S"]
CLIP_MAX_S = _job["CLIP_MAX_S"]
CATEGORIES = _job["CATEGORIES"]
LANGUAGE = _job["LANGUAGE"]
VIDEO_EXTS = {".mp4", ".mkv", ".mov", ".webm", ".ts", ".m4v"}
