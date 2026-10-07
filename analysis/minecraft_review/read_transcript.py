import sys,json,pathlib
sys.stdout.reconfigure(encoding='utf-8')
p=pathlib.Path(__file__).parent.parent/'transcripts'/(sys.argv[1]+'.json')
d=json.loads(p.read_text(encoding='utf-8'))
start=float(sys.argv[2]) if len(sys.argv)>2 else 0
end=float(sys.argv[3]) if len(sys.argv)>3 else 99999
print('COVERAGE',d['covered_until'])
for s in d['segments']:
    if s['end']>=start and s['start']<=end:
        print('{start:.2f}-{end:.2f} {text}'.format(**s))
