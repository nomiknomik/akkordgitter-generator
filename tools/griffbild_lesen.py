#!/usr/bin/env python3
"""
Liest Griffbilder (Chord-Boxes) aus einem Bild eines Gypsy-Jazz-Chord-eBooks aus.

Hintergrund: Die PDFs enthalten die Griffe nur als Grafik. Aus dem PDF-Textlayer
kommt nichts Brauchbares. Verlässlich ist die Pixelanalyse: Gitterlinien über
Spalten-/Zeilensummen finden, Punkte über Connected Components, x/o-Marker im
Kopfbereich über der Nullbund-Linie.

Verwendung:
    python3 tools/griffbild_lesen.py bild.png                 # ganzes Bild
    python3 tools/griffbild_lesen.py bild.png --x0 470 --x1 880   # ein Diagramm
    python3 tools/griffbild_lesen.py bild.png --saiten 4      # Ukulele/Mandoline

Ausgabe: Bundliste in der Reihenfolge [E,A,D,G,B,e] (tiefste Saite zuerst),
None = stumme Saite, 0 = Leersaite. Die Lagenzahl (Ziffer links neben dem
Gitter) wird NICHT per OCR gelesen — die muss man ablesen und mit --lage angeben.

WICHTIG: Das Ergebnis immer mit tools/voicing_pruefen.py gegenrechnen und
zusätzlich das vergrößerte Bild ansehen. Die Automatik erkennt Punkte gut,
kann aber bei überlappender Beschriftung danebenliegen.
"""
import argparse
import numpy as np
from PIL import Image

try:
    from scipy import ndimage
except ImportError:
    raise SystemExit("scipy fehlt:  pip install scipy --break-system-packages")


def gruppiere(indices, abstand=3):
    """Benachbarte Indizes zu einer Linie zusammenfassen."""
    gruppen = []
    for i in indices:
        if gruppen and i - gruppen[-1][-1] <= abstand:
            gruppen[-1].append(i)
        else:
            gruppen.append([i])
    return [int(np.mean(g)) for g in gruppen]


def finde_linien(binaer, achse, mindest):
    """Spalten- (achse=0) bzw. Zeilensummen (achse=1) mit vielen dunklen Pixeln."""
    summe = binaer.sum(axis=achse)
    kandidaten = [i for i in range(1, len(summe) - 1)
                  if summe[i] > mindest
                  and summe[i] >= summe[i - 1] and summe[i] >= summe[i + 1]]
    return gruppiere(kandidaten)


def lies_griffbild(pfad, x0=0, x1=None, y0=0, y1=None, saiten=6, lage=None, debug=False):
    arr = np.array(Image.open(pfad).convert("L"))
    arr = arr[y0:(y1 or arr.shape[0]), x0:(x1 or arr.shape[1])]
    binaer = arr < 100

    hoehe, breite = binaer.shape
    # Saitenlinien: senkrecht, laufen über einen Großteil der Gitterhöhe
    spalten = finde_linien(binaer, 0, mindest=hoehe * 0.28)
    # Bundlinien: waagerecht
    zeilen = finde_linien(binaer, 1, mindest=breite * 0.35)

    if debug:
        print(f"  Saitenspalten: {spalten}")
        print(f"  Bundzeilen:    {zeilen}")

    if len(spalten) < saiten or len(zeilen) < 2:
        raise ValueError(f"Gitter nicht erkannt (Spalten={len(spalten)}, Zeilen={len(zeilen)}). "
                         f"Bildausschnitt mit --x0/--x1/--y0/--y1 enger setzen.")

    # Falls Textreste mitgezählt wurden: die {saiten} gleichmäßigsten Spalten nehmen
    if len(spalten) > saiten:
        abstaende = [spalten[i + 1] - spalten[i] for i in range(len(spalten) - 1)]
        median = np.median(abstaende)
        beste, lauf = [], [spalten[0]]
        for i, d in enumerate(abstaende):
            if abs(d - median) <= median * 0.35:
                lauf.append(spalten[i + 1])
            else:
                if len(lauf) > len(beste):
                    beste = lauf
                lauf = [spalten[i + 1]]
        beste = lauf if len(lauf) > len(beste) else beste
        spalten = beste[:saiten]

    nullbund = zeilen[0]

    # Punkte: Connected Components, ungefähr rund und deutlich größer als Linien
    lbl, n = ndimage.label(binaer)
    punkte = []
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        h, w, flaeche = ys.max() - ys.min(), xs.max() - xs.min(), len(ys)
        if flaeche < 60 or h < 8 or w < 8:
            continue
        if not (0.6 < (w + 1) / (h + 1) < 1.7):     # grob rund
            continue
        if flaeche / ((w + 1) * (h + 1)) < 0.55:    # gefüllt, kein Buchstabe
            continue
        punkte.append((ys.mean(), xs.mean(), flaeche))

    # Lagenziffer: Textkomponente links vom Gitter. Ihre Zeile bestimmt, fuer
    # welches Bundfeld die angegebene Bundzahl gilt (im eBook steht die Ziffer
    # neben der betreffenden Zeile, nicht zwingend neben der obersten).
    referenzfeld = 1
    links = []
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        if xs.max() >= spalten[0] - 6:
            continue
        if ys.min() < nullbund - 5:
            continue
        if len(ys) < 25:
            continue
        links.append(ys.mean())
    if links:
        cy = float(np.mean(links))
        referenzfeld = max(1, sum(1 for z in zeilen if z < cy))

    if debug:
        print(f"  Punkte (y,x,Fläche): {[(round(a), round(b), c) for a, b, c in punkte]}")
        print(f"  Lagenziffer steht neben Bundfeld {referenzfeld}")

    buende = [None] * saiten
    offen = [False] * saiten
    for cy, cx, _ in punkte:
        saite = int(np.argmin([abs(cx - s) for s in spalten]))
        if cy < nullbund:                      # oberhalb der Nullbundlinie = o-Marker
            offen[saite] = True
            continue
        # in welchem Bundfeld liegt der Punkt?
        feld = sum(1 for z in zeilen if z < cy)
        buende[saite] = feld

    # x-Marker: dunkle Pixel im Kopfbereich, aber kein runder Punkt
    kopf = binaer[max(0, nullbund - 60):max(1, nullbund - 4), :]
    stumm = []
    for idx, s in enumerate(spalten):
        band = kopf[:, max(0, s - 10):s + 11]
        stumm.append(band.sum() > 25)

    ergebnis = []
    for i in range(saiten):
        if buende[i] is not None:
            ergebnis.append(buende[i] + (lage - referenzfeld if lage else 0))
        elif offen[i]:
            ergebnis.append(0)
        elif stumm[i]:
            ergebnis.append(None)
        else:
            ergebnis.append(None)   # nichts erkannt -> vorsichtshalber stumm
    return ergebnis, {"spalten": spalten, "zeilen": zeilen, "stumm": stumm,
                      "offen": offen, "referenzfeld": referenzfeld}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("bild")
    ap.add_argument("--x0", type=int, default=0)
    ap.add_argument("--x1", type=int, default=None)
    ap.add_argument("--y0", type=int, default=0)
    ap.add_argument("--y1", type=int, default=None)
    ap.add_argument("--saiten", type=int, default=6)
    ap.add_argument("--lage", type=int, default=None,
                    help="Bundzahl links neben dem Gitter (aus dem Bild ablesen)")
    ap.add_argument("--debug", action="store_true")
    a = ap.parse_args()

    buende, info = lies_griffbild(a.bild, a.x0, a.x1, a.y0, a.y1, a.saiten, a.lage, a.debug)
    print("Bünde:", ["x" if b is None else b for b in buende])
    print("Als SHAPES-Eintrag (Ankerbund abziehen!):", buende)
