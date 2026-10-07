import json, subprocess, csv
from pathlib import Path
ROOT=Path(__file__).resolve().parent
inv=json.loads((ROOT/'resolve_inventory.json').read_text(encoding='utf-8'))
rows=[]
for c in inv['clips']:
    p=Path(c['path'])
    probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)],capture_output=True,check=True).stdout)
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    aud=[s for s in probe['streams'] if s['codec_type']=='audio']
    duration=float(probe['format']['duration']); hh=int(duration)//3600; mm=int(duration)//60%60;ss=duration%60
    rows.append({**c,'size_bytes':p.stat().st_size,'modified_ns':p.stat().st_mtime_ns,'duration_seconds':duration,'duration_hms':f'{hh:02}:{mm:02}:{ss:06.3f}','avg_frame_rate':v['avg_frame_rate'],'r_frame_rate':v['r_frame_rate'],'audio_streams':[{k:s.get(k) for k in ['codec_name','sample_rate','channels','channel_layout']} for s in aud],'probe':probe})
(ROOT/'footage_inventory.json').write_text(json.dumps({'project':inv['project'],'clips':rows},ensure_ascii=False,indent=2),encoding='utf-8')
with (ROOT/'footage_inventory.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f);writer.writerow(['Filename','Duration','GB','Resolution','FPS','Video codec','Audio','Path'])
    for c in rows: writer.writerow([c['name'],c['duration_hms'],round(c['size_bytes']/1e9,3),c['resolution'],c['fps'],c['codec'],c['audio'],c['path']])
total=sum(c['duration_seconds'] for c in rows); size=sum(c['size_bytes'] for c in rows)
lines=['# รายการฟุตเทจ Katy404 — 2026-09-29','',f'โปรเจกต์ Resolve: {inv["project"]}',f'ฟุตเทจ {len(rows)} ไฟล์ รวม {int(total)//3600:02}:{int(total)//60%60:02}:{int(total)%60:02} ชั่วโมง / {size/1e9:.2f} GB','', '| ไฟล์ | ความยาว | GB | ภาพ / FPS | Codec |','|---|---:|---:|---|---|']
for c in rows: lines.append(f'| {c["name"].replace("|","／")} | {c["duration_hms"]} | {c["size_bytes"]/1e9:.2f} | {c["resolution"]} / {c["fps"]} | {c["codec"]} |')
lines+=['','ทุกไฟล์มีเสียง Opus stereo 48 kHz และอยู่สถานะ Online ใน Media Pool','desktop.ini เป็นไฟล์ระบบ ไม่ใช่ฟุตเทจ','', 'วิธีวิเคราะห์: ตรวจทุกไฟล์ด้วย FFprobe; ถอดเสียงไทยเต็มช่วงด้วย faster-whisper large-v3-turbo; ดูภาพตัวอย่างทั่วทั้งไฟล์และเจาะภาพช่วงที่คัดเลือก การถอดเสียงอัตโนมัติอาจคลาดเคลื่อน โดยเฉพาะเสียงหลายคน/เสียงเกม ไม่ใช้เป็นซับสำเร็จรูป','', 'งานคัดคลิปเป็น rough selects: รักษาภาพเต็ม 16:9 และเสียงต้นฉบับ พร้อมเวลาต้นทางสำหรับย้อนตรวจ']
(ROOT/'FOOTAGE_INVENTORY.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'files':len(rows),'duration':total,'bytes':size}))
