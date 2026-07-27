#!/usr/bin/env python3
"""
Schreibt einen Chart aus charts/*.json als Vorgabe in index.html.

Die App muss auch ohne Server laufen (Doppelklick, file://). Dort ist fetch()
gesperrt, der Vorgabe-Chart muss also im HTML stehen. Damit die eingebettete
Fassung nicht von der Datei abweicht, wird sie mit diesem Skript erzeugt statt
von Hand gepflegt.

    python3 tools/chart_einbetten.py charts/all-of-me-holovaty.json

Ohne Argument wird der aktuell eingebettete Chart nur angezeigt.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
HTML = ROOT / 'index.html'
ANF = '/* >>> VORGABE-CHART, erzeugt von tools/chart_einbetten.py <<< */'
END = '/* >>> ENDE VORGABE-CHART <<< */'

s = HTML.read_text(encoding='utf-8')
if ANF not in s or END not in s:
    sys.exit('Markierungen fehlen in index.html — bitte ANF/END prüfen.')

if len(sys.argv) < 2:
    block = s.split(ANF, 1)[1].split(END, 1)[0]
    m = re.search(r'"title"\s*:\s*"([^"]*)"', block)
    q = re.search(r'"quelle"\s*:\s*"([^"]*)"', block)
    print('Eingebettet:', m.group(1) if m else '?', '—', q.group(1) if q else 'ohne Quellenangabe')
    sys.exit()

src = pathlib.Path(sys.argv[1])
d = json.loads(src.read_text(encoding='utf-8'))
for feld in ('title', 'src'):
    if feld not in d:
        sys.exit(f'Feld "{feld}" fehlt in {src}')

neu = (ANF + '\nconst EXAMPLE = '
       + json.dumps(d, ensure_ascii=False, indent=2) + ';\n' + END)
s = s[:s.index(ANF)] + neu + s[s.index(END) + len(END):]
HTML.write_text(s, encoding='utf-8')
print(f'{src.name} als Vorgabe eingebettet ({d["title"]}).')
