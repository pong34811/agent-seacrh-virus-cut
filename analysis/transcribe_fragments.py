import json, os, subprocess
from pathlib import Path
import numpy as np, torch
from faster_whisper import WhisperModel
root=Path.cwd()
inv=json.loads((root/'analysis'/'resolve_inventory.json').read_text(encoding='utf-8'))
src=next(Path(c['path']) for c in inv['clips'] if 'Soul Walker - 005' in c['name'])
model_path=r"C:\Users\warit\.cache\huggingface\hub\models--Systran--faster-whisper-large-v3\snapshots\edaa852ec7e145841d8ffdb056a99866b5f0a478"
torch_lib=str(Path(torch.__file__).parent/'lib'); os.environ['PATH']=torch_lib+os.pathsep+os.environ.get('PATH','')
if os.name=='nt': dll_handle=os.add_dll_directory(torch_lib)
model=WhisperModel(model_path,device='cuda',compute_type='int8_float16',cpu_threads=4,num_workers=1)
windows=[(6574.5,6.0),(6583.5,4.5),(6608.0,17.0),(6632.0,15.0)]
rows=[]
for start,dur in windows:
    cmd=['ffmpeg','-v','error','-ss',str(start),'-i',str(src),'-t',str(dur),'-vn','-af','highpass=f=80,lowpass=f=7000','-ac','1','-ar','16000','-f','f32le','pipe:1']
    audio=np.frombuffer(subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout,dtype=np.float32)
    segs,info=model.transcribe(audio,language='th',beam_size=8,vad_filter=False,word_timestamps=True,condition_on_previous_text=False,repetition_penalty=1.05,initial_prompt='ภาษาไทย')
    for s in segs:
        rows.append({'start':round(start+s.start,3),'end':round(start+s.end,3),'text':s.text.strip(),'avg_logprob':round(s.avg_logprob,3),'words':[{'start':round(start+w.start,3),'end':round(start+w.end,3),'word':w.word,'probability':round(w.probability,3)} for w in (s.words or [])]})
out=root/'analysis'/'transcripts'/'soul_005_active_fragments_largev3.json'
out.write_text(json.dumps({'source':str(src),'windows':windows,'model':'faster-whisper-large-v3','language':'th','segments':rows},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'segments':len(rows),'output':str(out)},ensure_ascii=False))
for r in rows: print(json.dumps({k:r[k] for k in ('start','end','text','avg_logprob')},ensure_ascii=False))
