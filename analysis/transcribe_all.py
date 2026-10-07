import json, re, time, subprocess, traceback, os
from pathlib import Path
import numpy as np
import torch
TORCH_LIB = str(Path(torch.__file__).parent/'lib')
os.environ['PATH'] = TORCH_LIB + os.pathsep + os.environ.get('PATH','')
DLL_HANDLE = os.add_dll_directory(TORCH_LIB)
from faster_whisper import WhisperModel, BatchedInferencePipeline

ROOT = Path(__file__).resolve().parent
CLIPS = json.loads((ROOT/'resolve_inventory.json').read_text(encoding='utf-8'))['clips']
OUT = ROOT/'transcripts'
OUT.mkdir(exist_ok=True)
MODEL = r'C:\Users\warit\.cache\huggingface\hub\models--mobiuslabsgmbh--faster-whisper-large-v3-turbo\snapshots\0a363e9161cbc7ed1431c9597a8ceaf0c4f78fcf'
def slug(c):
    n=c['name']
    if 'Minecraft' in n: return 'minecraft_'+re.search(r'Minecraft - (\d+)',n).group(1)
    if 'Soul Walker' in n: return 'soul_'+re.search(r'Soul Walker - (\d+)',n).group(1)
    return 'terraria' if 'Terraria' in n else 'monster_hunter'

def save(path,data):
    temp=path.with_suffix('.tmp')
    temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    os.replace(temp,path)

print('Loading cached large-v3-turbo CUDA int8_float16',flush=True)
model=WhisperModel(MODEL,device='cuda',compute_type='int8_float16',cpu_threads=4,num_workers=1)
pipe=BatchedInferencePipeline(model=model)
order=['minecraft_002','soul_003','terraria','monster_hunter','minecraft_003','soul_004','soul_005']
clips=sorted(CLIPS,key=lambda c:order.index(slug(c)))
for c in clips:
    key=slug(c); duration=int(c['frames'])/float(c['fps']); path=OUT/(key+'.json')
    data=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'slug':key,'source':c,'duration':duration,'covered_until':0,'complete':False,'segments':[],'chunks':[],'model':'faster-whisper-large-v3-turbo','language':'th','limitations':'ASR rough transcript; game/multiple-speaker audio can be inaccurate. Timings are source seconds.'}
    for start in range(int(data['covered_until']),int(np.ceil(duration)),600):
        length=min(600,duration-start)
        t=time.time()
        try:
            cmd=['ffmpeg','-v','error','-ss',str(start),'-i',c['path'],'-t',str(length),'-vn','-ac','1','-ar','16000','-f','f32le','pipe:1']
            audio=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
            arr=np.frombuffer(audio,dtype=np.float32)
            segments,info=pipe.transcribe(arr,batch_size=8,language='th',beam_size=3,vad_filter=True,without_timestamps=False,word_timestamps=True,condition_on_previous_text=False,repetition_penalty=1.1)
            count=0
            for s in segments:
                data['segments'].append({'start':round(start+s.start,2),'end':round(start+s.end,2),'text':s.text.strip(),'avg_logprob':round(s.avg_logprob,3),'no_speech_prob':round(s.no_speech_prob,3),'words':[{'start':round(start+w.start,2),'end':round(start+w.end,2),'word':w.word,'probability':round(w.probability,3)} for w in (s.words or [])]})
                count+=1
            data['covered_until']=round(start+length,3)
            data['complete']=data['covered_until']>=duration-0.05
            data['chunks'].append({'start':start,'end':data['covered_until'],'segments':count,'wall_seconds':round(time.time()-t,2)})
            save(path,data)
            print(json.dumps({'slug':key,'covered':data['covered_until'],'duration':duration,'segments':len(data['segments']),'chunk_wall':round(time.time()-t,1),'complete':data['complete']}),flush=True)
        except Exception as e:
            print(json.dumps({'slug':key,'start':start,'error':str(e)}),flush=True)
            traceback.print_exc()
            raise
    save(path,data)
print('ALL_COMPLETE',flush=True)
