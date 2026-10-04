import gpu_env; gpu_env.setup()
import pathlib, subprocess, time, sys
import numpy as np
FF=r"C:\Users\warit\AppData\Local\hermes\tools\ffmpeg-9.0.1-win32-x64\bin\ffmpeg.exe"
src=[p for p in pathlib.Path(r"Z:\hoshi\2026-10-03").glob("*.mp4") if "roblox" in p.name][0]
raw=subprocess.run([FF,"-v","error","-ss","1500","-t","60","-i",str(src),"-vn","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
a=np.frombuffer(raw,dtype=np.float32); print("samples",a.size,flush=True)
from faster_whisper import WhisperModel
for ct in ["float16","int8_float16"]:
    try:
        t=time.time(); m=WhisperModel("large-v3",device="cuda",compute_type=ct); print("loaded",ct,round(time.time()-t,1),flush=True)
        t=time.time(); segs,_=m.transcribe(a,language="th",vad_filter=True,beam_size=1); out=[s.text for s in segs]
        print("OK",ct,"secs",round(time.time()-t,1),"|"," ".join(out)[:300]); sys.exit(0)
    except Exception as e: print("FAIL",ct,repr(e)[:300],flush=True)
