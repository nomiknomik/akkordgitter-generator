# Instrumente und Griffgenerator

Die Instrumentenauswahl (Kopfbereich links) betrifft **Griffbilder und Wiedergabe-Tonhöhen**,
nicht die Notation des Gitters.

| Kennung | Instrument | Stimmung (tiefste Saite zuerst) |
|---|---|---|
| `gitarre` | Gitarre | E A D G B E |
| `dropd` | Gitarre Drop D | D A D G B E |
| `ukulele` | Ukulele | G C E A (re-entrant) |
| `ukuleleLow` | Ukulele Low-G | G C E A |
| `bariton` | Baritonukulele | D G B E |
| `mandoline` | Mandoline | G D A E |
| `banjo` | Tenorbanjo | C G D A |
| `bass` | Bass | E A D G |

Neues Instrument = eine Zeile in `INSTRUMENTS`:

```js
banjo5: {n:'Banjo offen G', midi:[62,55,62,67,74], lab:['D','G','D','G','B']}
```

`midi` sind die MIDI-Nummern der Leersaiten (bestimmen Stimmung **und** Klanghöhe),
`lab` nur die Beschriftung. `shapes:true` schaltet die kuratierte Gypsy-Griffbibliothek
frei — das gilt ausschließlich für die Standardgitarre.

## Woher die Griffe kommen

- **Gitarre:** kuratierte Voicings aus `SHAPES` (authentische Gypsy-Formen).
  Fehlt für eine Qualität eine Form, springt der Generator ein.
- **Alle anderen Instrumente:** `genVoicings()` berechnet die Griffe aus den Akkordtönen.

### So arbeitet `genVoicings()`

1. Akkordtöne aus `CHORD_TONES`, unverzichtbare Töne aus `ESSENTIAL`
   (die Quinte darf entfallen, Terz und Septime/Sexte nicht).
2. Für jedes Bundfenster (0–13, Spanne standardmäßig 4 Bünde) je Saite die
   passenden Bünde sammeln, Leersaiten immer erlaubt.
3. Alle Kombinationen durchgehen und bewerten. Strafpunkte für: große Spanne,
   hohe Lage, stumme Saiten, Lücken zwischen klingenden Saiten, fehlender
   Grundton, falscher Basston. Bonus für viele klingende Saiten.
4. Pro Lage bleibt der beste Griff, sortiert nach Bund — im Griffbild per
   „andere Lage“ durchschaltbar.

Eine `0` als Lagenangabe bedeutet wie in der Originalvorlage: **offener Akkord**.
