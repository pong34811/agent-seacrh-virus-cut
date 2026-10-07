import json,pathlib,subprocess,concurrent.futures
from PIL import Image,ImageDraw
base=pathlib.Path(r'C:\Users\warit\Desktop\agent-seacrh-virus-cut\analysis');out=base/'soul_review'
inv=json.loads((base/'resolve_inventory.json').read_text(encoding='utf-8-sig'))
windows={'004':[(9104,9134),(9234,9264)],'003':[(7848,7868),(7924,7946),(5628,5660),(5754,5790)]}
for key,ranges in windows.items():
 c=next(c for c in inv['clips'] if 'Soul Walker - '+key in c['name']);slug='soul'+key
 for a,b in ranges:
  d=out/(slug+'_'+str(a));d.mkdir(exist_ok=True);frames=[]
  for t in range(a,b,2):
   dest=d/(str(t).zfill(5)+'.jpg')
   subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',c['path'],'-frames:v','1','-vf','scale=426:240','-q:v','3','-y',str(dest)],check=True);frames.append((t,dest))
  sheet=Image.new('RGB',(1704,266*((len(frames)+3)//4)),(25,25,25));draw=ImageDraw.Draw(sheet)
  for k,(t,dest) in enumerate(frames):
   x=k%4*426;y=k//4*266;sheet.paste(Image.open(dest),(x,y));draw.text((x+5,y+243),f'{slug} {t//3600:02}:{t//60%60:02}:{t%60:02} ({t}s)',fill='white')
  sheet.save(out/(slug+f'_{a}_fine.jpg'));print(slug,a,b,flush=True)
