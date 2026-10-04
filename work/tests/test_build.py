import build_timelines as b

def test_to_clip_infos_frames_at_60fps():
    c = {"start_s": 10, "end_s": 70}
    assert b.to_clip_infos(c, "CID", fps=60) == [{"clip_id": "CID", "start_frame": 600, "end_frame": 4200, "record_frame": 0}]

def test_to_clip_infos_rounds_fractional_seconds():
    out = b.to_clip_infos({"start_s": 10.504, "end_s": 71.0}, "X", fps=60)[0]
    assert out["start_frame"] == 630 and out["end_frame"] == 630 + round(60.496 * 60)

def test_timeline_name_sanitized_and_max_60():
    c = {"id": "v01-03", "category": "meme", "title_th": "จดชื่อ/ไว้ใน:เดธโน้ต" + "ก" * 80}
    n = b.timeline_name(c)
    assert len(n) <= 60 and n.startswith("v01-03_meme_") and not any(ch in n for ch in '\/:*?"<>|')

def test_merge_reviews_orders_and_counts(tmp_path):
    import json
    (tmp_path / "v02.json").write_text(json.dumps([{"id": "v02-01", "start_s": 5}]), encoding="utf-8")
    (tmp_path / "v01.json").write_text(json.dumps([{"id": "v01-02", "start_s": 9}, {"id": "v01-01", "start_s": 1}]), encoding="utf-8")
    merged = b.merge_reviews(tmp_path)
    assert [c["id"] for c in merged] == ["v01-01", "v01-02", "v02-01"]
