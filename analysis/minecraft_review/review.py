import json,subprocess,pathlib,sys,concurrent.futures
from PIL import Image,ImageDraw,ImageFont
ROOT=pathlib.Path(__file__).parent
INV=json.loads((ROOT.parent/'resolve_inventory.json').read_text(encoding='utf-8'))
CLIPS={('minecraft_003' if 'Minecraft - 003' in c['name'] else 'minecraft_002'):c for c in INV['clips'] if 'Minecraft' in c['name']}
def tc(t):
    t=int(t); return f'{t//3600:02}:{t//60%60:02}:{t%60:02}'
def probe(slug):
    c=CLIPS[slug]
    p=subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',c['path']],capture_output=True,text=True,encoding='utf-8',check=True)
    (ROOT/f'{slug}_probe.json').write_text(p.stdout,encoding='utf-8')
    return float(json.loads(p.stdout)['format']['duration'])
def frame(slug,t):
    fp=ROOT/f'{slug}_{int(t):05}.jpg'
    if not fp.exists():
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(t),'-i',CLIPS[slug]['path'],'-frames:v','1','-vf','scale=480:-1','-q:v','3','-y',str(fp)],capture_output=True,check=True)
    return fp
def sheet(slug,times,label):
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: files=list(pool.map(lambda t:frame(slug,t),times))
    out=Image.new('RGB',(1440,((len(times)+2)//3)*294),'#181818'); d=ImageDraw.Draw(out)
    font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    for i,(f,t) in enumerate(zip(files,times)):
        x=(i%3)*480;y=(i//3)*294
        out.paste(Image.open(f),(x,y));d.text((x+10,y+271),f'{slug} {tc(t)} ({t}s)',fill='white',font=font)
    outfile=ROOT/f'{slug}_{label}.jpg';out.save(outfile,quality=90);print(str(outfile),flush=True)
if __name__=='__main__':
    if len(sys.argv)>2: sheet(sys.argv[1],[float(x) for x in sys.argv[2].split(',')],sys.argv[3] if len(sys.argv)>3 else 'detail')
    else:
        for slug in CLIPS:
            duration=probe(slug);print(slug,duration,flush=True)
            times=list(range(300,int(duration),300));sheet(slug,times,'orientation')
