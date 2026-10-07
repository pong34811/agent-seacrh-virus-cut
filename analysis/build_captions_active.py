from pathlib import Path
import json

root = Path.cwd()
out_dir = root / 'analysis' / 'captions'
out_dir.mkdir(parents=True, exist_ok=True)
cues = [
    (0.25, 1.45, 'แกไปเครื่องสองเว้ย\nให้ฉันซัก'),
    (4.92, 5.84, 'โอ้โห เสียใจว่ะ'),
    (5.92, 6.72, 'คนดู ผมขอโทษนะ'),
    (6.74, 7.72, 'ถ้าผมข้ามคัทซีนไปอ่ะ'),
    (8.22, 9.42, 'ผมจะเซ็ต Hotkey\nไม่ใช่อะไร'),
    (11.56, 12.70, 'เปิด EX แม่งเลย'),
    (14.48, 15.28, 'ไอ้เหี้ย เอ๊ย'),
    (15.36, 16.30, 'แล้ว Security Tank ไม่ได้'),
    (16.30, 17.10, 'Search เป็น Security Armored'),
    (17.10, 18.40, 'ตอนลงเรดนะ'),
    (27.44, 28.50, 'จะต้องพึ่งคุณเคน'),
    (28.50, 29.55, 'หนักเลยล่ะ'),
    (29.66, 31.30, 'อัด Key มาเยอะมาก'),
    (31.30, 32.58, 'อ่ะไอ้เหี้ย'),
    (34.08, 35.12, 'ถ้าแพ้อีกก็แดก'),
    (35.12, 36.18, 'วิตามินซีเหมือนเดิม'),
    (38.28, 39.44, 'บอกเลยว่าเล่นจนชิน'),
    (39.44, 40.66, 'อะไอ้เหี้ย บอกเลย'),
    (41.80, 43.20, 'อยู่เปล่า'),
    (43.20, 44.22, 'เจออีกแล้ว'),
    (44.54, 45.42, 'เอาไปเลย'),
    (45.42, 46.28, 'ไอ้เหี้ย'),
    (46.28, 47.16, 'ขอ'),
    (47.16, 48.28, 'อ้าว ชิบหายเรื่อง'),
    (48.56, 49.55, 'เอาไปแล้ว'),
    (49.55, 50.35, 'ลาฟี่กู'),
    (50.35, 51.78, 'โดนจับไป ไอ้เหี้ย'),
    (53.08, 54.00, 'ไอ้เหี้ย'),
    (54.00, 55.50, 'โอ๊ย'),
    (62.82, 63.80, 'ทีวิตน้ำปันอยู่ยาก'),
    (63.80, 64.50, 'ไอ้เหี้ย โดนจับ'),
    (64.50, 65.48, 'เป็นบ้าเล่นเลยคนดู'),
    (65.92, 67.10, 'โดนจับเป็นเรื่องธรรมดา'),
    (67.10, 68.10, 'คุณเค'),
    (68.34, 69.10, 'ไอ้มอนตัวนี้'),
    (69.10, 69.90, 'ไอ้บอสตัวนี้มันจับได้'),
    (72.12, 73.88, 'นี่คือหนึ่งในเหตุผลที่'),
    (73.88, 75.10, 'ผมต้องใช้ EX สองที'),
    (75.10, 76.60, 'ไงแหละ เพราะมัน i-frame'),
]

def ts(value):
    ms = round(value * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1_000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

srt_lines=[]
for i, (start, end, text) in enumerate(cues, 1):
    markup = f'<font face="Mitr" color="#FFFFFF"><b>{text}</b></font>'
    srt_lines.extend([str(i), f'{ts(start)} --> {ts(end)}', markup, ''])
srt_path = out_dir / 'K404_29_SW005_HellCityClear_TH.srt'
srt_path.write_text('\n'.join(srt_lines), encoding='utf-8-sig')
review = {
    'timeline': 'K404_29_SW005_HellCityClear',
    'timeline_fps': 60,
    'source_start_seconds': 6570,
    'source_end_seconds': 6650,
    'transcription_models': ['faster-whisper-large-v3-turbo', 'faster-whisper-large-v3'],
    'cue_count': len(cues),
    'cues': [{'index': i, 'start_seconds': s, 'end_seconds': e, 'text': t} for i, (s,e,t) in enumerate(cues,1)],
    'low_confidence_source_ranges_seconds': [[6570.25,6571.45],[6574.92,6577.72],[6584.48,6587.1],[6587.1,6599.55],[6608.28,6614.22],[6616.55,6625.5],[6632.82,6640.0]],
    'notes': [
        'คำในช่วงที่ระบุมีผล ASR ต่างกันหรือความเชื่อต่ำ; ต้องตรวจฟังซ้ำก่อนเผยแพร่เพื่อยืนยันคำเฉพาะและประโยคที่ไม่ชัด',
        'ไฟล์ SRT ใช้ markup มาตรฐานสำหรับ Mitr/ตัวหนา/สีขาว; Resolve API ไม่เปิดให้ตั้ง stroke และตำแหน่ง track ผ่านสคริปต์',
        'เวลาเป็น offset เทียบกับต้นคลิปที่ 6570 วินาที; ไม่มีการเขียนหรือแปลงไฟล์วิดีโอต้นฉบับ',
    ]
}
review_path = out_dir / 'K404_29_SW005_HellCityClear_TH_review.json'
review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'srt':str(srt_path),'review':str(review_path),'cue_count':len(cues),'min_duration':round(min(e-s for s,e,_ in cues),3),'max_duration':round(max(e-s for s,e,_ in cues),3),'total_overlaps':sum(cues[i][0] < cues[i-1][1] for i in range(1,len(cues)))},ensure_ascii=False))

