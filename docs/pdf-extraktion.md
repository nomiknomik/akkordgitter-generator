# Akkorde und Songs aus einem PDF übernehmen

Die Gypsy-Jazz-Chord-eBooks enthalten Griffbilder **nur als Grafik**. Der
PDF-Textlayer liefert bestenfalls die Akkordnamen, nie die Bünde. Verlässlich ist
die Pixelanalyse. Der folgende Weg ist erprobt (v1.3, an *All Of Me* verifiziert).

## Werkzeuge im Repo

| Werkzeug | Zweck |
|---|---|
| `tools/griffbild_lesen.py` | liest ein Griffbild aus einem Bildausschnitt → Bundliste |
| `tools/voicing_pruefen.py` | rechnet eine Bundliste gegen die Akkordtöne |

Beide brauchen nur `numpy`, `Pillow`, `scipy`.

## Ablauf: neue Griffe in die Datenbank

### 1. Seite als Bild besorgen
PDF-Seite als PNG exportieren (mind. 150 dpi, besser 300). In claude.ai reicht es,
den relevanten Ausschnitt als Screenshot hochzuladen — genau so wurden die
Korrekturen in v1.3 gemacht.

### 2. Ausschnitt je Diagramm bestimmen
```bash
python3 -c "from PIL import Image; im=Image.open('seite.png'); print(im.size)"
```
Dann grob in gleich breite Spalten teilen und **großzügig** schneiden — lieber zu
viel Rand als eine abgeschnittene Saite. Genau daran ist der erste Versuch bei
`G7+` gescheitert: der Ausschnitt endete auf der hohen E-Saite, ein Punkt fehlte.

### 3. Auslesen
```bash
python3 tools/griffbild_lesen.py seite.png --x0 470 --x1 880 --lage 7 --debug
# -> Bünde: [7, 'x', 6, 7, 'x', 'x']
```
`--lage` ist die Ziffer links neben dem Gitter, die **von Hand abgelesen** wird
(kein OCR). Das Skript erkennt selbst, neben welcher Bundzeile sie steht, und
rechnet die übrigen Punkte relativ dazu um.

`--debug` zeigt erkannte Saitenspalten, Bundzeilen und Punktschwerpunkte. Wenn die
Zahl der Spalten nicht zur Saitenzahl passt, stimmt der Ausschnitt nicht.

### 4. Gegenrechnen (Pflicht)
```bash
python3 tools/voicing_pruefen.py E7 7 x 6 7 x x
```
Meldet akkordfremde und fehlende Töne. **Wichtig:**
- Ein fehlender **Grundton** ist nur ein Hinweis, kein Fehler — Rootless-Voicings
  sind im Gypsy Jazz normal, besonders bei Slash-Akkorden, wo der Bass die Lage trägt.
- Eine fehlende **Terz** oder **Septime/Sexte** ist ein echter Fehler.

### 5. Sichtprüfung
Ausschnitt stark vergrößern und ansehen:
```bash
python3 -c "
from PIL import Image
im=Image.open('seite.png').convert('RGB')
im.crop((470,60,880,480)).resize((1640,1680)).save('zoom.png')"
```
Diesen Schritt nicht überspringen. Der Tonartcheck erkennt *falsche Töne*, aber
nicht *das falsche Voicing* — siehe unten.

### 6. In `SHAPES` eintragen
Absolute Bünde in Offsets zum Ankerbund umrechnen (siehe
[`griffbibliothek.md`](griffbibliothek.md)), eintragen, Versionsnummer und
`archiv/CHANGELOG.md` pflegen.

## Die wichtigste Lektion

> Der Akkordton-Check und die Quelltreue sind **zwei verschiedene Prüfungen**.

Das ursprünglich falsche `E7/B` (`7,7,9,7,9,x`) besteht den Tonartcheck fehlerfrei —
alle Töne gehören zu E7. Trotzdem war es das falsche Voicing, weil das Original ein
Rootless-Voicing mit stummer A- und H-Saite vorgibt. Wer ein Buch nachbaut, muss die
Griffe **Punkt für Punkt mit dem Bild vergleichen**, nicht nur harmonisch prüfen.

Umgekehrt fielen `7/4` und `m7/3` erst beim systematischen Gegenrechnen **aller**
Slash-Voicings auf — die enthielten tatsächlich akkordfremde Töne. Also: beides tun.

## Ablauf: neuen Song übernehmen

1. **Akkordfolge abtippen** statt automatisch extrahieren. Die Gitter sind grafisch,
   OCR über Akkordsymbole mit Hoch- und Tiefstellungen ist fehleranfälliger als
   Abtippen. Format siehe [`syntax.md`](syntax.md).
2. **Taktaufteilung** aus der Diagonalen im Original ablesen und über Beat-Suffixe
   abbilden (`C6:2 Bb7:1 A7:1`), siehe [`taktaufteilung.md`](taktaufteilung.md).
3. **Lagenangaben** aus den Ecken der Original-Takte übernehmen — nur dort, wo sie
   von der automatischen Wahl abweichen, per `@Bund` erzwingen.
4. Als JSON unter `charts/` ablegen (Export-Knopf der App erzeugt das Format).
5. Gegenprobe: App öffnen, Analyse einblenden, Stufen mit dem Original vergleichen.

## Verschiedene Interpretationen desselben Songs

Mehrere Fassungen als getrennte Dateien ablegen, Herkunft im Titel führen:

```
charts/all-of-me-djangosolos.json
charts/all-of-me-realbook.json
```

So bleibt vergleichbar, welche Substitutionen aus welcher Quelle stammen. Die
Analysefunktion der App eignet sich gut, um die Unterschiede zu beschreiben:
gleiche Tonart einstellen und die Stufenfolgen je Formteil nebeneinanderlegen.
