import json, subprocess, pathlib, concurrent.futures
from PIL import Image,ImageDraw
BASE=pathlib.Path(__file__).parent
INV=json.loads((BASE.parent/'resolve_inventory.json').read_text(encoding='utf8'))
RANGES={'terraria':[(1910,1950),(3800,3850),(5040,5110),(5510,5570)],'monster_hunter':[(1940,2010),(4320,4400),(5610,5670),(6050,6130),(7340,7400),(8350,8400)]}
def run(slug):
    c=next(c for c in INV['clips'] if ('Terraria' if slug=='terraria' else 'Monster Hunter') in c['name'])
    out=BASE/slug/'boundaries';out.mkdir(exist_ok=True,parents=True)
    for block,(a,b) in enumerate(RANGES[slug],1):
        tiles=[]
        for t in range(a,b+1,5):
            f=out/f'{t:05d}.jpg'
            if not f.exists():subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',c['path'],'-frames:v','1','-vf','scale=640:-1','-q:v','2','-threads','2','-y',str(f)],check=True,stdout=subprocess.DEVNULL)
            tile=Image.new('RGB',(640,386),(15,15,15));tile.paste(Image.open(f).convert('RGB'),(0,26));ImageDraw.Draw(tile).text((10,5),f'{t//3600:02d}:{t//60%60:02d}:{t%60:02d} ({t}s)',fill='white');tiles.append(tile)
        for n in range(0,len(tiles),12):
            chunk=tiles[n:n+12];sheet=Image.new('RGB',(1920,386*((len(chunk)+2)//3)),(30,30,30))
            for i,im in enumerate(chunk):sheet.paste(im,((i%3)*640,(i//3)*386))
            sheet.save(out/f'block{block}_{n//12+1}.jpg',quality=93)
        print(slug,block,a,b,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,RANGES))
