import json, subprocess, pathlib, concurrent.futures
from PIL import Image,ImageDraw
BASE=pathlib.Path(__file__).parent
INV=json.loads((BASE.parent/'resolve_inventory.json').read_text(encoding='utf8'))
RANGES={'terraria':[(900,2220),(2940,4020),(4200,6600),(6900,8190)],'monster_hunter':[(1700,2150),(3400,4650),(4800,5070),(5400,6450),(6780,7560),(7950,8450)]}
def run(slug):
    c=next(c for c in INV['clips'] if ('Terraria' if slug=='terraria' else 'Monster Hunter') in c['name'])
    out=BASE/slug/'dense';out.mkdir(exist_ok=True,parents=True)
    for block,(a,b) in enumerate(RANGES[slug],1):
        tiles=[]
        for t in range(a,b+1,30):
            f=out/f'{t:05d}.jpg'
            if not f.exists():subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',c['path'],'-frames:v','1','-vf','scale=480:-1','-q:v','3','-threads','2','-y',str(f)],check=True,stdout=subprocess.DEVNULL)
            tile=Image.new('RGB',(480,296),(15,15,15));tile.paste(Image.open(f).convert('RGB'),(0,26));ImageDraw.Draw(tile).text((10,5),f'{t//3600:02d}:{t//60%60:02d}:{t%60:02d} ({t}s)',fill='white');tiles.append(tile)
        for n in range(0,len(tiles),20):
            chunk=tiles[n:n+20];sheet=Image.new('RGB',(1920,296*((len(chunk)+3)//4)),(30,30,30))
            for i,im in enumerate(chunk):sheet.paste(im,((i%4)*480,(i//4)*296))
            sheet.save(out/f'block{block}_{n//20+1}.jpg',quality=90)
        print(slug,block,a,b,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,RANGES))
