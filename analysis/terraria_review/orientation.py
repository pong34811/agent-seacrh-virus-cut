import json, subprocess, pathlib, concurrent.futures
from PIL import Image,ImageDraw
BASE=pathlib.Path(__file__).parent
INV=json.loads((BASE.parent/'resolve_inventory.json').read_text(encoding='utf8'))
clips=[c for c in INV['clips'] if 'Terraria' in c['name'] or 'Monster Hunter' in c['name']]
def run(c):
    slug='terraria' if 'Terraria' in c['name'] else 'monster_hunter'
    out=BASE/slug; out.mkdir(exist_ok=True,parents=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',c['path']],text=True,encoding='utf8'))
    (out/'probe.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2),encoding='utf8')
    dur=float(probe['format']['duration'])
    times=list(range(120,int(dur)-10,300))
    ims=[]
    for t in times:
        f=out/f'{t:05d}.jpg'
        if not f.exists():
            subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',c['path'],'-frames:v','1','-vf','scale=480:-1','-q:v','3','-threads','2','-y',str(f)],check=True,stdout=subprocess.DEVNULL)
        im=Image.open(f).convert('RGB')
        tile=Image.new('RGB',(480,296),(15,15,15));tile.paste(im,(0,26))
        draw=ImageDraw.Draw(tile);draw.text((10,5),f'{slug} {t//3600:02d}:{t//60%60:02d}:{t%60:02d} ({t}s)',fill='white')
        ims.append(tile)
    for n in range(0,len(ims),20):
        chunk=ims[n:n+20];sheet=Image.new('RGB',(480*4,296*((len(chunk)+3)//4)),(30,30,30))
        for i,im in enumerate(chunk):sheet.paste(im,((i%4)*480,(i//4)*296))
        sheet.save(out/f'sheet_{n//20+1}.jpg',quality=90)
    print(json.dumps({'slug':slug,'duration':dur,'fps':next(s.get('avg_frame_rate') for s in probe['streams'] if s['codec_type']=='video'),'samples':len(ims)},ensure_ascii=False),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(run,clips))
