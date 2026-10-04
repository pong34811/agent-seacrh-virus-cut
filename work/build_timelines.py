"""Candidates -> Resolve clip_infos / timeline names. Resolve calls themselves go through the Resolve MCP."""
import glob, json, pathlib, re
import config

def to_clip_infos(c: dict, clip_id: str, fps: float = 60) -> list[dict]:
    start = round(c["start_s"] * fps)
    return [{"clip_id": clip_id, "start_frame": start,
             "end_frame": start + round((c["end_s"] - c["start_s"]) * fps),   # end exclusive
             "record_frame": 0}]

def timeline_name(c: dict, limit: int = 60) -> str:
    title = re.sub(r'[\/:*?"<>|]', " ", c["title_th"]).strip()
    return f"{c['id']}_{c['category']}_{title}"[:limit].rstrip()

def merge_reviews(review_dir: pathlib.Path | None = None) -> list[dict]:
    review_dir = pathlib.Path(review_dir or config.WORK_DIR / "review")
    out = []
    for f in sorted(glob.glob(str(review_dir / "v??.json"))):
        out += sorted(json.loads(pathlib.Path(f).read_text(encoding="utf-8")), key=lambda c: c["start_s"])
    return out

def main() -> None:
    cands = merge_reviews()
    (config.WORK_DIR / "candidates.json").write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
    clips = json.loads((config.WORK_DIR / "resolve_clips.json").read_text(encoding="utf-8"))
    plan = [{"name": timeline_name(c), "clip_infos": to_clip_infos(c, clips[c["source_id"]]), "candidate": c["id"]} for c in cands]
    (config.WORK_DIR / "timeline_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(plan), "timelines planned")

if __name__ == "__main__":
    main()
