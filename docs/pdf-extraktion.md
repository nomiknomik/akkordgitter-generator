# Akkorde und Songs aus einem PDF übernehmen

Es gibt **zwei Wege**. Welcher taugt, hängt davon ab, wie das PDF gebaut ist —
das prüft man in einer Zeile:

```bash
python3 -c "import fitz; d=fitz.open('buch.pdf'); print(len(d[0].get_drawings()),'Zeichenobjekte')"
```

| Ergebnis | Weg |
|---|---|
| viele Zeichenobjekte (Rechtecke + Kreise) | **A — Vektorebene**, exakt, immer zuerst versuchen |
| kaum oder keine (Seite ist ein Bild) | **B — Pixelanalyse** mit `tools/griffbild_lesen.py` |

---

# Weg A — direkt aus der Vektorebene (empfohlen)

Erprobt an *All Of Me* (Adrian Holovaty), v1.5: 67 Griffbilder, alle korrekt,
ohne eine einzige Handkorrektur.

Griffbilder solcher PDFs sind keine Grafik, sondern gezeichnete Primitive:
Gitterlinien als dünne **Rechtecke**, Punkte als gefüllte **Kreise**. Beides
lässt sich mit PyMuPDF punktgenau abgreifen — kein OCR, keine Schwellenwerte,
keine Ausschnitte von Hand.

## Ablauf

1. **Objekte einsammeln** (`page.get_drawings()`):
   - `('re',)`, breit und flach → waagerechte Bundlinie
   - `('re',)`, schmal und hoch → senkrechte Saitenlinie
   - `('re',)`, breit **und** hoch → Rahmen eines Griffbilds
   - `('c','c')` → Punkt
2. **Boxen bilden**: je Rahmen die sechs Saitenlinien und die Bundlinien darin
   sammeln. Sechs senkrechte Linien = ein Griffbild.
3. **Beschriftung zuordnen** über den Textlayer, unterschieden nach Schriftgrad:
   Akkordname ≈ 11 pt, Lagenziffer und `X`-Marker ≈ 8 pt.
4. **Bünde ausrechnen**: Reihenmitte jedes Punktes bestimmen, Reihe der
   Lagenziffer als Bezug nehmen, Differenz aufaddieren.
5. **Gegenrechnen** — Pflicht, siehe unten.

## Zwei Fallen, die Zeit kosten

**Geteilte Lagenziffer.** Stehen zwei Griffbilder nebeneinander, ist die Ziffer
oft nur einmal gedruckt und steht *zwischen* beiden. Sucht man sie „irgendwo
links“, greift man auf das Nachbardiagramm über und liegt um mehrere Bünde
daneben. Richtig ist: nur die **unmittelbar** links angrenzende Ziffer nehmen
(Abstand < 14 pt) und ihre senkrechte Lage gegen die Reihenmitten prüfen.

**Sattelbalken statt Ziffer.** Diagramme ohne Lagenziffer sind nicht
fehlerhaft — sie stehen in **offener Lage**. Erkennbar an einem verdickten,
über den Rahmen hinausragenden Balken am oberen Rand (Rechteck, dessen `x0`
kleiner und `x1` größer ist als der Rahmen). Dann gilt: erste Reihe = 1. Bund.
Genau hieran scheiterten anfangs alle `Dm6`-Griffe und das schließende `C6/9`.

## Gegenrechnen

Auch bei exakter Geometrie gilt die Prüfpflicht — sie fängt falsch zugeordnete
Namen und Lagen ab:

```bash
python3 tools/voicing_pruefen.py Dm6 x 2 3 2 3 x
```

Bewährte Zusatzprobe: die fertige Akkordfolge gegen die bekannte Form des
Stücks halten. Bei *All Of Me* ergab sich lückenlos ABAC mit `F | Fm | C | A7`
in Takt 25–28 — eine unabhängige Bestätigung, dass Takt- und Griffzuordnung
stimmen. Zuletzt prüft ein Testlauf, ob die App mit `@n` bundgenau dieselben
Griffe liefert wie das Buch.

## Fehlerbild deuten

- fehlender **Grundton** → kein Fehler, Rootless-Voicings sind normal
- fehlende **Terz** oder **Septime/Sexte** → echter Fehler, Ausschnitt prüfen
- dreitönige `dim`-Griffe ohne Quinte → normal, es sind `dim7`-Ausschnitte
- Buchbezeichnung weicht ab (`Am/C` klingt als `Am7/C`) → Bezeichnung des
  Autors beibehalten, das Voicing aber unter dem tatsächlichen Schlüssel ablegen

---

# Weg B — Pixelanalyse



| Werkzeug | Zweck |
|---|---|
| `tools/griffbild_lesen.py` | liest ein Griffbild aus einem Bildausschnitt → Bundliste |
| `tools/voicing_pruefen.py` | rechnet eine Bundliste gegen die Akkordtöne |

Beide brauchen nur `numpy`, `Pillow`, `scipy`.

## Werkzeuge im Repo

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
