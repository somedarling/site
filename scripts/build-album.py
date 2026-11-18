#!/usr/bin/env python3
"""Generate a safe, static Neocities album page from items.json."""
import json, html, pathlib
root=pathlib.Path(__file__).resolve().parents[1]
out=root/'public/album'
items=json.loads((out/'items.json').read_text(encoding='utf-8'))
if not isinstance(items,list): raise ValueError('items.json must be an array')
def e(s): return html.escape(str(s or ''),quote=True)
cards=[]
for item in reversed(items):
    path=str(item.get('path',''))
    if not path.startswith('images/') or '/' in path[7:] or not path.lower().endswith(('.png','.jpg','.jpeg','.gif','.webp')): continue
    title=e(item.get('title') or '無題の一枚')
    desc=e(item.get('description') or '')
    cards.append(f'<article class="tile"><a href="{e(path)}" target="_blank" rel="noopener"><img loading="lazy" src="{e(path)}" alt="{title}"></a><div class="caption"><strong>{title}</strong>{f"<p>{desc}</p>" if desc else ""}</div></article>')
page='''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>画像置き場 | 4ki</title><style>
:root{font-family:"Yu Mincho","Hiragino Mincho ProN",Georgia,serif;color:#625a55;background:#efe6d9}*{box-sizing:border-box}body{margin:0;min-height:100vh;background-color:#efe6d9;background-image:radial-gradient(circle at 17% 13%,#b4a99a44 0 1px,transparent 1.5px),radial-gradient(circle at 79% 61%,#97b5b744 0 1px,transparent 1.6px);background-size:131px 149px,197px 223px}header{text-align:center;padding:40px 15px 20px}h1{font-size:clamp(1.7rem,5vw,2.3rem);letter-spacing:.12em;margin:0 0 12px}header p{font-size:.88rem;color:#77706c}main{max-width:1100px;margin:auto;padding:20px 20px 80px}.gallery{columns:3 230px;column-gap:18px}.tile{display:inline-block;width:100%;break-inside:avoid;background:#fffaf0c9;margin:0 0 18px;padding:12px}.tile img{display:block;width:100%;height:auto}.caption{padding:10px 5px 4px;overflow-wrap:anywhere}.caption strong{font-size:.95rem}.caption p{font-size:.88rem;white-space:pre-wrap;line-height:1.7;margin:7px 0}.empty{text-align:center;background:#fffaf0b8;padding:55px 20px;color:#7b716c}a{color:inherit}footer{text-align:center;padding:10px 0 35px;font-size:.82rem;color:#7b716c}@media(max-width:520px){main{padding:10px 16px 60px}.tile{padding:9px}}
</style></head><body><header><h1><a href="/album/" style="text-decoration:none">画像置き場</a></h1><p>描いたもの、見つけたもの、日々のかけら。</p></header><main><div class="gallery">'''+(''.join(cards) if cards else '<p class="empty">まだ画像はありません。</p>')+'''</div></main><footer>4ki · album</footer></body></html>'''
(out/'index.html').write_text(page,encoding='utf-8')
print('Generated',out/'index.html','with',len(cards),'images')
