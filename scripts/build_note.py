#!/usr/bin/env python3
"""Build static Nekoweb diary from posts.json and a versioned HTML template."""
import json, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
source=ROOT/'public/note/posts.json'
template=ROOT/'scripts/note-template.html'
out=ROOT/'public/note/index.html'
posts=json.loads(source.read_text(encoding='utf-8'))
if not isinstance(posts,list): raise SystemExit('posts.json must be an array')
clean=[]
for i,p in enumerate(posts):
    if not isinstance(p,dict): raise SystemExit(f'post {i}: invalid object')
    if p.get('destination','nekoweb')!='nekoweb': continue
    for k in ('id','created'):
        if not isinstance(p.get(k),str) or not p[k]: raise SystemExit(f'post {i}: missing {k}')
    q={k:p.get(k,'') for k in ('id','created','title','content','category')}
    if not all(isinstance(v,str) for v in q.values()): raise SystemExit(f'post {i}: invalid text field')
    q['tags']=p.get('tags',[])
    q['images']=p.get('images',[])
    if not isinstance(q['tags'],list) or not all(isinstance(x,str) for x in q['tags']):raise SystemExit(f'post {i}: invalid tags')
    if not isinstance(q['images'],list) or not all(isinstance(x,str) and re.fullmatch(r'images/[a-zA-Z0-9._-]+\.(?:png|jpg|jpeg|webp|gif)',x,re.I) and (ROOT/'public/note'/x).is_file() for x in q['images']):raise SystemExit(f'post {i}: image file missing or unsafe path')
    clean.append(q)
clean.sort(key=lambda x:x['created'],reverse=True)
serialized=json.dumps(clean,ensure_ascii=False,separators=(',',':')).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
html=template.read_text(encoding='utf-8')
needle='<script type="application/json" id="post-data">[]</script>'
if html.count(needle)!=1:raise SystemExit('template data placeholder missing')
html=html.replace(needle,f'<script type="application/json" id="post-data">{serialized}</script>')
out.write_text(html,encoding='utf-8')
print(f'Generated {out.relative_to(ROOT)} ({len(clean)} posts, {out.stat().st_size} bytes)')
