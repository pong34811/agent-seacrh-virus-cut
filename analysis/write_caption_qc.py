from pathlib import Path
import json
root=Path.cwd()
review=json.loads((root/'analysis'/'captions'/'K404_29_SW005_HellCityClear_TH_review.json').read_text(encoding='utf-8'))
out=root/'analysis'/'captions'/'K404_29_SW005_HellCityClear_TH_QC.md'
lines=[
'# Transcript และ QC — K404_29_SW005_HellCityClear',
'',
'- Timeline: 16:9, 1920×1080, 60 fps; ช่วงต้นฉบับ 01:49:30–01:50:50',
'- Subtitle track: `TH` (เปิดใช้งาน)',
'- Subtitle: 39 cues; readback จาก Resolve ตรงกับจำนวนและข้อความใน SRT; ไม่ซ้อน; อยู่ในขอบเขต Timeline',
'- Timing: คลาดจาก SRT สูงสุด 0.007 วินาที; ระยะต่อ cue 0.70–1.77 วินาที',
'- Project `KT404_2026-09-29` บันทึกแล้ว',
'',
'## Transcript ตาม cue',
'',
'| # | เวลาในคลิป | ข้อความ |',
'|---:|:---|:---|',
]
for c in review['cues']:
    s=c['start_seconds']; e=c['end_seconds']; t=c['text'].replace('\n',' / ').replace('|','\\|')
    def tc(v):
        msec=round(v*1000); mm,ms=divmod(msec,60000); ss,ms=divmod(ms,1000)
        return f'{mm:02}:{ss:02}.{ms:03}'
    lines.append(f"| {c['index']} | {tc(s)}–{tc(e)} | {t} |")
lines += [
'',
'## จุดที่ควรฟังยืนยันก่อนเผยแพร่',
'',
'ถอดเทียบด้วย faster-whisper large-v3-turbo และ large-v3 แล้ว แต่ทั้งสองรอบยังเห็นคำไม่ตรงกันหรือความเชื่อต่ำในช่วงเหล่านี้: 01:49:30–31, 01:49:35–38, 01:49:44–01:50:00, 01:50:08–14, 01:50:16–25 และ 01:50:33–40 โดยเฉพาะคำว่า `Security Tank`, `Security Armored`, ชื่อ `คุณเคน` และวลีช่วงเสียงเกมกลบ คำบรรยายที่ใส่ไว้เป็นร่างที่ดีที่สุดจากผลถอดเสียงสองรอบ ไม่ควรถือว่าได้ยืนยันทุกพยางค์ด้วยการฟังมนุษย์แล้ว',
'',
'## รูปแบบตัวอักษรและข้อจำกัดการตรวจภาพ',
'',
'SRT ที่นำเข้าใส่ markup สำหรับ Mitr, ตัวหนา และสีขาว และ Resolve อ่านกลับเป็นข้อความสะอาด อย่างไรก็ตาม Scripting API ของ Resolve 21.1 ไม่เปิดให้อ่าน/เขียน outline สีดำหรือตำแหน่ง subtitle ต่อ track ได้ จึงยังยืนยัน stroke และตำแหน่ง lower-safe ด้วยภาพ preview ไม่ได้',
'',
'ไฟล์ SRT: `K404_29_SW005_HellCityClear_TH.srt`',
'ไฟล์ transcript machine-readable: `K404_29_SW005_HellCityClear_TH_review.json`',
]
out.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(out)
