#!/usr/bin/env python3
"""
Rechnet ein Voicing gegen die Akkordtöne — Pflichtschritt vor jedem Eintrag
in die SHAPES-Bibliothek.

    python3 tools/voicing_pruefen.py C6 3 3 2 2 x x
    python3 tools/voicing_pruefen.py E7 7 x 6 7 x x
    python3 tools/voicing_pruefen.py --stimmung ukulele C6 0 0 0 0

Gibt die klingenden Tonhöhenklassen aus und meldet fehlende bzw. akkordfremde Töne.
"""
import sys

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
FLATS = {'Db': 1, 'Eb': 3, 'Gb': 6, 'Ab': 8, 'Bb': 10, 'Cb': 11, 'Fb': 4}

STIMMUNGEN = {
    'gitarre':   [4, 9, 2, 7, 11, 4],
    'dropd':     [2, 9, 2, 7, 11, 4],
    'ukulele':   [7, 0, 4, 9],
    'bariton':   [2, 7, 11, 4],
    'mandoline': [7, 2, 9, 4],
    'banjo':     [0, 7, 2, 9],
    'bass':      [4, 9, 2, 7],
}

# identisch zu CHORD_TONES in index.html — bei Änderungen beide Stellen pflegen
TONE = {
    'maj': [0, 4, 7], '6': [0, 4, 7, 9], '69': [0, 2, 4, 9],
    'maj7': [0, 4, 7, 11], 'maj9': [0, 2, 4, 7, 11],
    '7': [0, 4, 7, 10], '9': [0, 2, 4, 7, 10], '13': [0, 4, 7, 9, 10],
    '11': [0, 5, 7, 10], '7b5': [0, 4, 6, 10], '7b9': [0, 1, 4, 10],
    '7#9': [0, 3, 4, 10], '7#5': [0, 4, 8, 10], 'aug': [0, 4, 8],
    'm': [0, 3, 7], 'm6': [0, 3, 7, 9], 'm7': [0, 3, 7, 10],
    'm9': [0, 2, 3, 7, 10], 'dim': [0, 3, 6, 9], 'm7b5': [0, 3, 6, 10],
}
WESENTLICH = {
    'maj': [0, 4], '6': [0, 4, 9], '69': [0, 4, 9], 'maj7': [0, 4, 11],
    'maj9': [0, 4, 11], '7': [0, 4, 10], '9': [0, 4, 10], '13': [0, 4, 9, 10],
    '11': [0, 5, 10], '7b5': [0, 4, 6, 10], '7b9': [0, 4, 10, 1],
    '7#9': [0, 4, 10, 3], '7#5': [0, 4, 8, 10], 'aug': [0, 4, 8],
    'm': [0, 3], 'm6': [0, 3, 9], 'm7': [0, 3, 10], 'm9': [0, 3, 10],
    'dim': [0, 3, 6, 9], 'm7b5': [0, 3, 6, 10],
}
ALIAS = {'': 'maj', 'M': 'maj', 'M6': '6', '6/9': '69', 'M7': 'maj7',
         'M9': 'maj9', '7+': '7#5', '-': 'm', '-6': 'm6', '-7': 'm7',
         '-9': 'm9', '°': 'dim', 'o': 'dim', 'ø': 'm7b5', '0': 'm7b5'}


def tonhoehe(name):
    return FLATS[name] if name in FLATS else NOTES.index(name)


def zerlege(symbol):
    i = 1
    if len(symbol) > 1 and symbol[1] in '#b':
        i = 2
    grundton, rest = symbol[:i], symbol[i:]
    qual = ALIAS.get(rest, rest)
    if qual not in TONE:
        raise SystemExit(f"Unbekannte Qualität '{rest}'. Bekannt: {sorted(TONE)}")
    return tonhoehe(grundton), qual, grundton


def main():
    args = sys.argv[1:]
    stimmung = 'gitarre'
    if args and args[0] == '--stimmung':
        stimmung = args[1]
        args = args[2:]
    if len(args) < 2:
        raise SystemExit(__doc__)

    symbol, buende_roh = args[0], args[1:]
    wurzel, qual, grundname = zerlege(symbol)
    offen = STIMMUNGEN[stimmung]
    if len(buende_roh) != len(offen):
        raise SystemExit(f"{stimmung} hat {len(offen)} Saiten, {len(buende_roh)} Bünde angegeben.")

    klingend, details = set(), []
    for saite, b in enumerate(buende_roh):
        if b.lower() in ('x', '-', 'none'):
            details.append('  x')
            continue
        pc = (offen[saite] + int(b)) % 12
        klingend.add(pc)
        details.append(f"  Bund {b:>2} = {NOTES[pc]}")

    soll = {(wurzel + t) % 12 for t in TONE[qual]}
    # Grundton gesondert behandeln: Rootless-Voicings sind im Gypsy Jazz üblich,
    # besonders bei Slash-Akkorden, wo der Bass die Lage bestimmt.
    pflicht = {(wurzel + t) % 12 for t in WESENTLICH[qual] if t != 0}
    fremd = klingend - soll
    fehlt = pflicht - klingend
    grundton_fehlt = wurzel not in klingend

    print(f"{symbol}  ({stimmung})")
    for d in details:
        print(d)
    print("  klingende Töne:", ', '.join(NOTES[p] for p in sorted(klingend)))
    print("  Akkordtöne soll:", ', '.join(NOTES[p] for p in sorted(soll)))
    if fremd:
        print("  FEHLER akkordfremd:", ', '.join(NOTES[p] for p in sorted(fremd)))
    if fehlt:
        print("  FEHLER fehlt (charakterbildend):", ', '.join(NOTES[p] for p in sorted(fehlt)))
    if grundton_fehlt and not fehlt and not fremd:
        print(f"  HINWEIS: Grundton {NOTES[wurzel]} fehlt — als Rootless-Voicing in Ordnung,")
        print( "           sonst prüfen. Bei Slash-Akkorden trägt der Bass die Lage.")
    if not fremd and not fehlt:
        gespielt = [int(b) for b in buende_roh if b.lower() not in ('x', '-', 'none') and int(b) > 0]
        spanne = (max(gespielt) - min(gespielt)) if gespielt else 0
        print(f"  OK — Spanne {spanne} Bünde")


if __name__ == "__main__":
    main()
