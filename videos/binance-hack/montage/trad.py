# Version anglaise : traduit le texte affiché dans les pages capturées juste avant chaque capture (dictionnaire code/trad_en.json
# + règles de format des nombres : 6,3 → 6.3 · 6 300 → 6,300 · 6,3 Md$ → $6.3B). Usage : if trad.EN: trad.brancher(pg)
import os, json
EN = os.environ.get('LANGUE') == 'en'
CODE = '/home/claude/true_stories/videos/binance-hack/code/'
D = json.load(open(CODE + 'trad_en.json'))
JS = r"""D => { const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n; const L = [];
  while (n = w.nextNode()) L.push(n);
  for (const n of L) { const s = n.nodeValue, k = s.trim(); if (!k) continue;
    if (k in D) { n.nodeValue = s.replace(k, D[k]); continue; }
    if (!/\d/.test(k)) continue;
    let t = s.replace(/(\d),(\d{1,2})(?!\d)/g, '$1.$2');
    for (let i = 0; i < 4; i++) t = t.replace(/(\d)[   ](\d{3})(?!\d)/g, '$1,$2');
    t = t.replace(/([\d.,]+)\s*Md\$/g, '$$$1B').replace(/([\d.,]+)\s*M\$/g, '$$$1M').replace(/([\d][\d.,]*)\s*\$/g, '$$$1');
    n.nodeValue = t; } }"""
def brancher(pg):
    orig = pg.screenshot
    def capture(*a, **k):
        pg.evaluate(JS, D); return orig(*a, **k)
    pg.screenshot = capture
def suf(): return '_en' if EN else ''
