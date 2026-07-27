#!/usr/bin/env python3
"""
Liest Griffbilder aus einem PDF über die VEKTOREBENE aus – exakt, ohne OCR
und ohne Pixelanalyse.

Voraussetzung: Das PDF enthält die Griffbilder als gezeichnete Primitive
(Gitterlinien = dünne Rechtecke, Punkte = gefüllte Kreise). Das prüft man mit

    python3 -c "import fitz; d=fitz.open('buch.pdf'); print(len(d[0].get_drawings()))"

Sind es nur wenige Objekte, ist die Seite ein Bild – dann tools/griffbild_lesen.py
verwenden.

Verwendung:
    python3 tools/griffbild_vektor.py buch.pdf            # alle Seiten, JSON
    python3 tools/griffbild_vektor.py buch.pdf --lesbar   # Tabelle statt JSON

Ausgabe je Griffbild: Akkordname, Lage und die Bundliste in der Reihenfolge
[E,A,D,G,B,e]; null = Saite nicht anschlagen.

Zwei Besonderheiten, die das Skript selbst behandelt:
  * Stehen zwei Diagramme nebeneinander, ist die Lagenziffer oft nur einmal
    gedruckt. Es wird nur die UNMITTELBAR links angrenzende Ziffer verwendet.
  * Diagramme ohne Lagenziffer haben stattdessen einen verdickten SATTELBALKEN
    am oberen Rand und stehen damit in offener Lage (erste Reihe = 1. Bund).

Das Ergebnis IMMER mit tools/voicing_pruefen.py gegenrechnen.
"""
import fitz, json, re, sys, argparse

ap = argparse.ArgumentParser()
ap.add_argument('pdf')
ap.add_argument('--lesbar', action='store_true', help='Tabelle statt JSON')
args = ap.parse_args()

PDF = args.pdf
doc = fitz.open(PDF)
boxes = []

for pno, page in enumerate(doc):
    rects, circles = [], []
    for x in page.get_drawings():
        r = x['rect']; t = tuple(i[0] for i in x['items'])
        if t == ('re',):
            rects.append((r.x0, r.y0, r.x1, r.y1))
        elif t in (('c','c'), ('c',)):
            circles.append(((r.x0+r.x1)/2, (r.y0+r.y1)/2, x['type']))

    names, small = [], []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                t = s['text'].strip()
                if not t: continue
                if 10.5 < s['size'] < 12.0: names.append((*s['bbox'], t))
                elif 7.5 < s['size'] < 9.0:  small.append((*s['bbox'], t))

    hor = [r for r in rects if (r[2]-r[0]) > 12 and (r[3]-r[1]) < 2.5]
    ver = [r for r in rects if (r[3]-r[1]) > 12 and (r[2]-r[0]) < 2.5]
    outer = [r for r in rects if (r[2]-r[0]) > 12 and (r[3]-r[1]) > 12]

    for o in outer:
        x0, y0, x1, y1 = o
        xs = sorted(set(round((v[0]+v[2])/2, 1) for v in ver
                        if x0-2 <= v[0] and v[2] <= x1+2 and abs(v[1]-y0) < 3))
        if len(xs) != 6: continue
        fl = sorted(set(round((h[1]+h[3])/2, 1) for h in hor
                        if x0-2 <= h[0] and h[2] <= x1+2 and y0+2 < (h[1]+h[3])/2 < y1-2))
        bounds = fl + [y1]                       # Untergrenzen der Reihen
        rowc = [( (fl[i-1] if i else fl[0]-10) + bounds[i])/2 for i in range(len(bounds))]
        nut = any(r[0] < x0-1 and r[2] > x1+1 and (r[3]-r[1]) < 4 and abs(r[1]-y0) < 4
                  for r in rects)
        boxes.append(dict(page=pno, x0=x0, y0=y0, x1=x1, y1=y1, xs=xs, rowc=rowc, nut=nut,
            circ=[c for c in circles if x0-2 <= c[0] <= x1+2 and y0-2 <= c[1] <= y1+2],
            mark=[s for s in small if x0-4 <= s[0] <= x1+4 and y0-14 <= s[1] < y0],
            lage=sorted([s for s in small if s[2] <= x0+1 and x0-s[2] < 14
                  and y0-4 < (s[1]+s[3])/2 < y1+4
                  and re.fullmatch(r'\d+', s[4])], key=lambda s: -s[2]),
            name=[n for n in names if x0-16 <= n[0] <= x1+16 and y0-32 <= n[3] <= y0+2]))

boxes.sort(key=lambda b: (b['page'], round(b['y0']/28), b['x0']))

STR = ['E','A','D','G','B','e']
out = []
for b in boxes:
    if not b['name']:
        out.append(dict(err='Name fehlt', **{k: b[k] for k in ('page','x0','y0')})); continue
    rows = [None]*6
    for cx, cy, _ in b['circ']:
        si = min(range(6), key=lambda i: abs(b['xs'][i]-cx))
        rows[si] = min(range(len(b['rowc'])), key=lambda i: abs(b['rowc'][i]-cy))
    xs_mark = [None]*6
    for m in b['mark']:
        mx = (m[0]+m[2])/2
        si = min(range(6), key=lambda i: abs(b['xs'][i]-mx))
        xs_mark[si] = m[4]
    if b['lage']:
        lg = b['lage'][0]; lgf = int(lg[4]); lgy = (lg[1]+lg[3])/2
        ri = min(range(len(b['rowc'])), key=lambda i: abs(b['rowc'][i]-lgy))
    elif b['nut']:
        lgf, ri = 1, 0
    else:
        lgf = ri = None
    frets = None if lgf is None else [None if r is None else lgf + (r-ri) for r in rows]
    out.append(dict(page=b['page'], y=round(b['y0']), x=round(b['x0']), nut=b['nut'],
                    name=b['name'][0][4], lage=(int(b['lage'][0][4]) if b['lage'] else lgf),
                    rows=rows, frets=frets, mark=xs_mark))

if args.lesbar:
    for i, b in enumerate(out):
        if 'err' in b:
            print(f"{i:3}  {b}"); continue
        fs = ' '.join('x' if v is None else str(v) for v in (b['frets'] or []))
        print(f"{i:3}  S{b['page']+1}  {b['name']:10} Lage {b['lage']:>2}"
              f"{'  (Sattel)' if b['nut'] else '':10}  [{fs}]")
else:
    print(json.dumps(out, ensure_ascii=False, indent=1))
