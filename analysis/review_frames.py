import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
p=argparse.ArgumentParser()
p.add_argument('slug');p.add_argument('start',type=int);p.add_argument('end',type=int)
p.add_argument('--step',type=int,default=10);p.add_argument('--width',type=int,default=640)
a=p.parse_args()
root=Path(__file__).resolve().parent
clips=json.loads((root/'resolve_inventory.json').read_text(encoding='utf-8'))['clips']
def slug(c):
 n=c['name']
 if 'Minecraft' in n:return 'minecraft_'+n.split('Minecraft - ')[1][:3]
 if 'Soul Walker' in n:return 'soul_'+n.split('Soul Walker - ')[1][:3]
 return 'terraria' if 'Terraria' in n else 'monster_hunter'
c=next(x for x in clips if slug(x)==a.slug)
out=root/'root_review'/f'{a.slug}_{a.start}_{a.end}';out.mkdir(parents=True,exist_ok=True)
times=list(range(a.start,a.end+1,a.step))
for i,t in enumerate(times):
 f=out/f'{t:05}.jpg'
 if not f.exists():subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',c['path'],'-frames:v','1','-vf',f'scale={a.width}:-1','-q:v','3','-y',str(f)],check=True)
for k in range(0,len(times),12):
 subset=times[k:k+12];w=a.width;h=round(w*9/16)+24
 sheet=Image.new('RGB',(w*3,h*4),'#111');draw=ImageDraw.Draw(sheet)
 for i,t in enumerate(subset):
  x=i%3*w;y=i//3*h;sheet.paste(Image.open(out/f'{t:05}.jpg'),(x,y+24));draw.text((x+8,y+3),f'{t//3600:02}:{t//60%60:02}:{t%60:02}',fill='white')
 sheet.save(out/f'sheet_{k//12+1}.jpg')
print(out)
