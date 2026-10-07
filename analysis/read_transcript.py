import argparse, json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('slug')
p.add_argument('--start',type=float,default=0)
p.add_argument('--end',type=float,default=999999)
p.add_argument('--search',default='')
p.add_argument('--max',type=int,default=60)
a=p.parse_args()
d=json.loads((Path(__file__).resolve().parent/'transcripts'/f'{a.slug}.json').read_text(encoding='utf-8'))
print('COVERED',d['covered_until'],'OF',d['duration'],'COMPLETE',d['complete'])
count=0
for s in d['segments']:
    if s['end']<a.start or s['start']>a.end or (a.search and a.search not in s['text']):continue
    def t(x): return f'{int(x//3600):02}:{int(x//60)%60:02}:{x%60:05.2f}'
    print(t(s['start']),t(s['end']),s['text'])
    count+=1
    if count>=a.max:break
