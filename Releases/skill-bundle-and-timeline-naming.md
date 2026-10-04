# Release notes — Project skill bundle และรูปแบบชื่อ Timeline

สาขา: `main` | ฐานก่อน commit นี้: `378f49b`

บันทึกการเปลี่ยนแปลงใน repository เท่านั้น เอกสารนี้ไม่ใช่การสร้าง Git tag หรือเผยแพร่ GitHub Release

## สิ่งที่เพิ่ม

- เพิ่มสำเนา skills ที่เกี่ยวข้องกับงานโปรเจกต์ 37 skills ใน `.agents/skills/` รวม `house-style` เดิมเป็น 38 skills
- ครอบคลุม highlight clipping, vertical reframing, Resolve, wiki, code/GitHub และ workflow Superpowers พร้อมไฟล์ประกอบภายใน skill directories
- เก็บเอกสาร Resolve ที่ SKILL.md อ้างโดยตรงใน `.agents/skills/_references/resolve/` และ LICENSE ที่พบจากต้นทาง
- เพิ่ม `.agents/skills/README.md` อธิบายรายการ ขอบเขต การใช้สำเนา และลำดับความสำคัญของกฎโปรเจกต์
- เพิ่ม `.agents/skills/manifest.json` บันทึก provenance, SHA-256 และขนาดไฟล์ที่คัดลอก 139 ไฟล์; house-style ฉบับโปรเจกต์ไม่ถูกทับ

## รูปแบบชื่อ Timeline

- ผู้ใช้กำหนดชื่อเป็น `{ชื่อคลิป}-{ชื่อเกม}-vdo` เท่านั้น ไม่ใส่ candidate ID หรือ category prefix
- ผู้ใช้ยืนยันชื่อเกม `Backrooms`; เปลี่ยนชื่อครบ 7 Timeline ในโปรเจกต์ `hoshi-2026-09` โดยไม่สร้าง Timeline ใหม่หรือเปลี่ยนจุดตัด
- บันทึก Resolve แล้วอ่านรายชื่อกลับ: `exec_034e7ed855b0` (save), `exec_9fcc9464f223` (list readback)
- อัปเดต `.agents/skills/house-style/SKILL.md`, `prompt.md`, job config, `timeline_plan.json` และ report ให้ตรงกับชื่อใหม่
- เพิ่ม `work/hoshi_1489/2026-09/rename_verification.json` เป็นหลักฐานการเปลี่ยนชื่อ

## การตรวจที่รันจริงก่อน commit

- `HIGHLIGHT_JOB=work/hoshi_1489/2026-09/job.json` แล้วรัน pytest: `33 passed in 1.85s`
- ตรวจ SHA-256 ของไฟล์ที่คัดลอกครบ 139 ไฟล์ตรง manifest; จำนวน skills 37 เพิ่มใหม่ / 38 รวมเดิม
- ตรวจแผน Timeline ครบ 7 รายการ ลงท้าย `-Backrooms-vdo`
- ตรวจ `git diff --check` ผ่าน

## ข้อจำกัดและประเด็นเปิด

- runtime ปฏิเสธโหลด project skill `github` และ `long-video-highlight-clipping` เพราะ security scanner quarantine; เก็บคำเตือนนี้ไว้ ไม่ปลด quarantine หรือเลี่ยง scanner ไม่รับรองว่า skills ทุกตัวโหลดผ่าน runtime แล้ว
- ตรวจสำเนา skill ด้วย hashes/โครงสร้าง ไม่ได้รัน scripts ที่คัดลอกครบทุกตัว และไม่ใช่การติดตั้ง plugin/MCP server
- คำสั่งผู้ใช้, AGENTS.md, prompt.md และ house-style ชนะข้อแนะนำทั่วไปในสำเนา เช่น main-only และ assembly-only
- shared pipeline `work/build_timelines.py` ยังมี naming function รูปแบบเก่า; ครั้งนี้เปลี่ยนชื่อจริงและ job artifacts ไม่ได้แก้ shared code ให้สร้างชื่อรูปแบบใหม่อัตโนมัติ ต้องทำ code change พร้อม tests แยกก่อนอ้างว่ารองรับแล้ว
- ชื่อเกมที่ผู้ใช้ระบุเป็น label ของชุดงาน ไม่ใช่ผลพิสูจน์เนื้อหาเกมทุกคลิปจาก ASR
- ข้อจำกัดการคัดคลิปเดิมยังคงอยู่: exact dialogue/payoff และ sentence-complete cuts ของทั้ง 7 คลิปไม่ได้ฟังยืนยัน
- เครื่องมือจับภาพ QC ก่อนหน้านี้คืน render format เดิมไม่สำเร็จ; ตาม report ปัจจุบัน JPG/YUV420_8 ต้องเลือก delivery preset ก่อน render
- ไม่เปลี่ยน footage, ไม่ render วิดีโอส่งออก, ไม่ upload YouTube, ไม่เปลี่ยน `llm_wiki/`, ไม่ push, ไม่สร้าง tag และไม่เผยแพร่ GitHub Release ในขั้นนี้

## ไฟล์อ้างอิง

- [Skill bundle](../.agents/skills/README.md)
- [Manifest](../.agents/skills/manifest.json)
- [รายงานงาน](../work/hoshi_1489/2026-09/report.md)
- [หลักฐานเปลี่ยนชื่อ](../work/hoshi_1489/2026-09/rename_verification.json)
