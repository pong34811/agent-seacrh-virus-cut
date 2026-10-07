import json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(r'C:\Users\warit\Desktop\agent-seacrh-virus-cut\analysis\transcripts')/(sys.argv[1]+'.json')
if not p.exists(): print('not ready');raise SystemExit()
d=json.loads(p.read_text(encoding='utf-8'));print('COVERED',d['covered_until'],'COMPLETE',d['complete'])
a=float(sys.argv[2]) if len(sys.argv)>2 else 0;b=float(sys.argv[3]) if len(sys.argv)>3 else 100000
for i,s in enumerate(d['segments']):
 if s['end']>=a and s['start']<b: print(f"{i}: {s['start']:.2f}–{s['end']:.2f}: {s['text']}")
