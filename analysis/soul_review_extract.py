import json, pathlib, subprocess, concurrent.futures
from PIL import Image,ImageDraw
base=pathlib.Path(r'C:\Users\warit\Desktop\agent-seacrh-virus-cut\analysis')
out=base/'soul_review';out.mkdir(exist_ok=True)
inventory=json.loads((base/'resolve_inventory.json').read_text(encoding='utf-8-sig'))
clips=[c for c in inventory['clips'] if 'Soul Walker - 003' in c['name'] or 'Soul Walker - 004' in c['name']]
for c in clips:
 slug='soul003' if '003' in c['name'] else 'soul004'
 p=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',c['path']],text=True,encoding='utf-8'))
 (out/(slug+'_probe.json')).write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
 dur=float(p['format']['duration']);d=out/slug;d.mkdir(exist_ok=True)
 def extract(t):
  dest=d/(str(int(t)).zfill(5)+'.jpg')
  if not dest.exists():
   subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i',c['path'],'-frames:v','1','-vf','scale=426:240','-q:v','4','-y',str(dest)],check=True)
  return t,dest
 times=list(range(0,int(dur),120))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  frames=list(ex.map(extract,times))
 for j in range(0,len(frames),24):
  batch=frames[j:j+24];sheet=Image.new('RGB',(426*4,266*6),(25,25,25));draw=ImageDraw.Draw(sheet)
  for k,(t,dest) in enumerate(batch):
   x=k%4*426;y=k//4*266;sheet.paste(Image.open(dest),(x,y));draw.text((x+5,y+243),f'{slug}  {t//3600:02}:{t//60%60:02}:{t%60:02}',fill='white')
  sheet.save(out/(slug+f'_overview_{j//24+1}.jpg'))
 print(slug,'duration',dur,'frames',len(frames),flush=True)
