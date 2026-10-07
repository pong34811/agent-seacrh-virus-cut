import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'resolve_inventory.json').read_text(encoding='utf-8'))
out=ROOT/'root_review'; out.mkdir(exist_ok=True)
c=next(c for c in data['clips'] if 'Soul Walker - 005' in c['name'])
probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',c['path']],capture_output=True,check=True).stdout)
(out/'soul005_probe.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2),encoding='utf-8')
images=[]
for sec in range(120,int(c['frames'])//int(c['fps']),240):
    p=out/f'soul005_{sec:05}.jpg'
    subprocess.run(['ffmpeg','-v','error','-ss',str(sec),'-i',c['path'],'-frames:v','1','-vf','scale=480:-1','-q:v','3','-y',str(p)],check=True)
    images.append((sec,p))
for k in range(0,len(images),16):
    subset=images[k:k+16]; sheet=Image.new('RGB',(1920,4*300),'#111111'); d=ImageDraw.Draw(sheet)
    for j,(sec,p) in enumerate(subset):
        x=(j%4)*480;y=(j//4)*300
        sheet.paste(Image.open(p),(x,y+24));d.text((x+8,y+3),f'{sec//3600:02}:{sec//60%60:02}:{sec%60:02}',fill='white')
    sheet.save(out/f'soul005_sheet_{k//16+1}.jpg')
print('Soul005 overview saved',flush=True)
