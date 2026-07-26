# Taktaufteilung („broken chord boxes“)

Übernommen aus dem Gypsy-Jazz-Chord-eBook (DjangoSolos, Colin Cosimini),
Abschnitt *The Chord Boxes*.

## Prinzip

Die **Hauptdiagonale von unten links nach oben rechts** trennt die erste von der
zweiten Takthälfte. Zusatzlinien von einer Ecke zur Feldmitte unterteilen die
jeweilige Hälfte weiter:

- Linie von **oben links** zur Mitte → teilt die erste Hälfte in *links* und *oben*
- Linie von **unten rechts** zur Mitte → teilt die zweite Hälfte in *unten* und *rechts*

Spielreihenfolge: **links → oben → unten → rechts**.

## Die fünf Grundformen (4/4)

| Beats | Linien | Felder |
|---|---|---|
| `4` | keine | ganzes Feld |
| `2 + 2` | Diagonale | oben links, unten rechts |
| `1 + 1 + 2` | Diagonale + oben links | links, oben, unten rechts |
| `2 + 1 + 1` | Diagonale + unten rechts | oben links, unten, rechts |
| `1 + 1 + 1 + 1` | beide Diagonalen | links, oben, unten, rechts |

## Sonderformen

| Zeichen im Feld | Bedeutung | Syntax |
|---|---|---|
| Keil `>` (Linien von den beiden linken Ecken zur Mitte) | nur den 1. Beat des Taktes spielen | `>C6` |
| Keil `<` (Linien von den beiden rechten Ecken zur Mitte) | nur den letzten Beat spielen | `<C6` |

## Implementierung

`LAYOUTS` in Abschnitt 6 von `index.html` bildet Beat-Muster auf Geometrie ab:

```js
const DIAG=[0,100,100,0], SPLIT_UL=[0,0,50,50], SPLIT_LR=[100,100,50,50];
'1,1,2': {lines:[DIAG,SPLIT_UL], regions:[[25,55],[57,21],[70,72]]}
```

`lines` sind Strecken in Prozentkoordinaten `[x1,y1,x2,y2]` des quadratischen Feldes,
`regions` die Mittelpunkte der Beschriftungen in derselben Einheit.
Neue Muster einfach als weiteren Schlüssel (`'3,1'` o. ä.) ergänzen; für unbekannte
Muster fällt `layoutFor()` auf die Standardform mit passender Feldanzahl zurück,
ab fünf Akkorden auf senkrechte Streifen.
