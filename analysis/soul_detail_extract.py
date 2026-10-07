import json,pathlib,subprocess,concurrent.futures
from PIL import Image,ImageDraw
base=pathlib.Path(r'C:\Users\warit\Desktop\agent-seacrh-virus-cut\analysis');out=base/'soul_review'
inv=json.loads((base/'resolve_inventory.json').read_text(encoding='utf-8-sig'))
windows={'003':[(0,120),(330,490),(1860,2010),(5570,5800),(6840,7010),(7820,8000)],'004':[(430,530),(2580,2730),(6440,6570),(7500,7680),(8070,8300),(9000,9470)]}
for key,ranges in windows.items():
 c=next(c for c in inv['clips'] if 'Soul Walker - '+key in c['name']);slug='soul'+key
 for a,b in ranges:
  times=list(range(a,b,10));d=out/(slug+'_'+str(a));d.mkdir(exist_ok=True)
  def extract(t):
   dest=d/(str(t).zfill(5)+'.jpg')
   if not dest.exists(): subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',c['path'],'-frames:v','1','-vf','scale=426:240','-q:v','3','-y',str(dest)],check=True)
   return t,dest
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: frames=list(ex.map(extract,times))
  for j in range(0,len(frames),24):
   batch=frames[j:j+24];rows=(len(batch)+3)//4;sheet=Image.new('RGB',(1704,266*rows),(25,25,25));draw=ImageDraw.Draw(sheet)
   for k,(t,dest) in enumerate(batch):
    x=k%4*426;y=k//4*266;sheet.paste(Image.open(dest),(x,y));draw.text((x+5,y+243),f'{slug} {t//3600:02}:{t//60%60:02}:{t%60:02} ({t}s)',fill='white')
   sheet.save(out/(slug+f'_{a}_detail_{j//24+1}.jpg'))
  print(slug,a,b,flush=True)
