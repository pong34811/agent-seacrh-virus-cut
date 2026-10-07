import json, os, subprocess, sys
from pathlib import Path
import numpy as np
import torch
from faster_whisper import WhisperModel

root = Path.cwd()
inventory = json.loads((Path.cwd()/'analysis'/'resolve_inventory.json').read_text(encoding='utf-8'))
src = Path(next(c['path'] for c in inventory['clips'] if 'Soul Walker - 005' in c['name']))
start, duration = 6570.0, 80.0
model_path = r"C:\Users\warit\.cache\huggingface\hub\models--mobiuslabsgmbh--faster-whisper-large-v3-turbo\snapshots\0a363e9161cbc7ed1431c9597a8ceaf0c4f78fcf"
torch_lib = str(Path(torch.__file__).parent / 'lib')
os.environ['PATH'] = torch_lib + os.pathsep + os.environ.get('PATH', '')
if os.name == 'nt':
    dll_handle = os.add_dll_directory(torch_lib)
cmd = ['ffmpeg', '-v', 'error', '-ss', str(start), '-i', str(src), '-t', str(duration), '-vn', '-ac', '1', '-ar', '16000', '-f', 'f32le', 'pipe:1']
proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
audio = np.frombuffer(proc.stdout, dtype=np.float32)
model = WhisperModel(model_path, device='cuda', compute_type='int8_float16', cpu_threads=4, num_workers=1)
segments, info = model.transcribe(audio, language='th', beam_size=8, vad_filter=True, word_timestamps=True, condition_on_previous_text=False, repetition_penalty=1.1, initial_prompt='ภาษาไทย ชื่อเกม Soul Walker, Hell City, EX, Hotkey, i-frame, raid, เคน')
rows=[]
for seg in segments:
    rows.append({'start': round(start+seg.start,3), 'end': round(start+seg.end,3), 'text': seg.text.strip(), 'avg_logprob': round(seg.avg_logprob,3), 'no_speech_prob': round(seg.no_speech_prob,3), 'words':[{'start':round(start+w.start,3),'end':round(start+w.end,3),'word':w.word,'probability':round(w.probability,3)} for w in (seg.words or [])]})
out = root/'analysis'/'transcripts'/'soul_005_active_6570_6650_review.json'
out.write_text(json.dumps({'source':str(src),'source_range_seconds':[start,start+duration],'model':'faster-whisper-large-v3-turbo','language':info.language,'segments':rows},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'language':info.language,'segments':len(rows),'output':str(out)},ensure_ascii=False))
for row in rows:
    print(json.dumps({k:row[k] for k in ('start','end','text','avg_logprob','no_speech_prob')},ensure_ascii=False))

