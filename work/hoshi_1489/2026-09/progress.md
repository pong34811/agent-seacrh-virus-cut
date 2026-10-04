# Job ledger — plan: D:\agent-seacrh-virus-cut\.hermes\plans\2026-10-04_013000-hoshi-highlight-timelines-v2.md

Spec: prompt.md ปัจจุบัน; งานนี้แยกจากรอบก่อนทั้งหมด

Task 0: in progress — พบ source หนึ่งไฟล์; Resolve Studio 21.1.0.17 / MCP 4.8.26; source AV1 Online 60 fps; โปรเจกต์ hoshi-2026-09 ไม่มี Timeline; ยืนยันค่า user แล้ว

Ruling: ใช้ main ไม่สร้าง worktree/branch — คำสั่งผู้ใช้ใน AGENTS.md มีลำดับเหนือ skill — งานนี้ไม่แยก branch
Ruling: ใช้ pipeline และ tests ที่มีอยู่แทนสร้างซ้ำ Task 1–6 — งานนี้เป็นการรันกับ input ใหม่ ไม่ใช่ implement โค้ดเดิมอีกครั้ง — จะทดสอบและตรวจ artifacts ของ job นี้ใหม่
Ruling: ใช้โปรเจกต์ hoshi-2026-09 แม้ชื่อไม่ตรง JOB — ผู้ใช้เลือกโดยตรง; ไม่เปลี่ยน JOB ซึ่งเป็นชื่อโฟลเดอร์งาน — ไม่สลับโปรเจกต์และไม่ import ซ้ำ
Ruling: เก็บ ledger ใน WORK_DIR ต่อ job แทน ledger ของแผนร่วม — แผนเดียวถูกใช้หลายงาน; completion ของงานเก่าไม่พิสูจน์งานใหม่

Pre-flight interfaces:
| Producer -> Consumer | Checked contract | Finding |
| --- | --- | --- |
| job.json -> config -> inventory | per-job INPUT_DIR and WORK_DIR, sorted source mapping | HIGHLIGHT_JOB ต้องเลือก job นี้อย่างชัดเจน |
| inventory -> features -> shortlist | source_id, duration, untouched WAV, RMS/peak | ใช้ outputs ของ job นี้เท่านั้น |
| shortlist -> transcribe -> packets | absolute seconds and padded spans | live prompt กำหนด padding 90 s แต่ code default 60 s; ต้อง override ตอนรันและวัด coverage ก่อน |
| sheets + transcript -> packets + briefs -> review | one packet/brief per source, verified visual evidence | ASR ไม่ใช่คำพูดที่ยืนยัน |
| review -> schema -> build -> Resolve | bounds, nonoverlap, live clip IDs, exclusive end frames | schema test ชื่อจริงต้องตรวจ; tests ในแผนบางชื่อเก่า |

Task 0: complete — GPU float16 smoke exited 0; model loaded 4.7 s; source AV1 Online; user confirmed decisions
Task 1: complete — inventory.json/md หนึ่ง source, ffprobe 12359.014 s, 60/1 r/avg fps, AV1 + Opus
Task 2: complete — existing pipeline tests: 32 passed, 1 schema gate deselected; full run failed only missing review as expected
Task 3: complete — untouched WAV/features produced, extraction 59.2 s; initial shortlist 27 windows
Ruling: ใช้ per_hour=14 ตามแผนแทน code default 20 — เมื่อ pad ±90 s ค่า 20 ครอบคลุม 50.97%, ค่า 14 ครอบคลุม 39.08% และได้ 20 windows — อาจพลาดมุกเสียงเรียบ; รายงานข้อจำกัดนี้
Ruling: transcribe.spans ใช้ functools.partial(pad=90) ตอนรัน — รักษา live prompt โดยไม่เปลี่ยน shared code default ของงานอื่น — reviewer packet default บริบท 60 s แต่ transcript มีบริบท 90 s
Task 4: in progress — GPU shortlist transcription
Tasks 5–10: pending
