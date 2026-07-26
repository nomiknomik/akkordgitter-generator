# Griffbibliothek erweitern

Alle Voicings stehen im Objekt `SHAPES` (Abschnitt 2 im `<script>` von `index.html`).

## Format

```js
'm11': [
  {s:1, a:0, f:[null,0,-2,0,0,null], n:'A-Form'}
]
```

| Feld | Bedeutung |
|---|---|
| `s` | Ankersaite: `0` = tiefe E-Saite, `1` = A-Saite |
| `a` | Halbtonabstand des Ankertons zum Grundton (Default `0`) |
| `f` | sechs Bundabstände zum Ankerbund, Reihenfolge `[E, A, D, G, B, e]`, `null` = Saite nicht anschlagen |
| `n` | Anzeigename der Form |

Der **Ankerbund** ist die Zahl, die im Gitter links oben im Takt und im Griffbild
links neben dem Diagramm steht. `f[s]` muss deshalb immer `0` sein.

Mehrere Einträge pro Qualität = mehrere Lagen. `allVoicings()` berechnet daraus
alle spielbaren Positionen (Bund 1–15) und sortiert sie aufsteigend; im Griffbild
lässt sich mit „andere Lage“ durchschalten.

## Slash-Akkorde

Umkehrungen liegen unter dem Schlüssel `<qualität>/<halbtonintervall des Basstons>`:

| Schlüssel | Bedeutung |
|---|---|
| `maj/4` | Durakkord mit Terz im Bass (`G/B`) |
| `maj/7` | Durakkord mit Quinte im Bass (`C/G`) |
| `6/7` | Sextakkord mit Quinte im Bass (`C6/G`) |
| `7/7`, `7/4` | Dominantseptakkord mit Quinte bzw. Terz im Bass |
| `m7/3` | Moll-Sept mit kleiner Terz im Bass |

Fehlt der passende Eintrag, greift automatisch die Grundstellung — der Bass wird
dann nur im Akkordnamen angezeigt.

## Neue Akkordschreibweise

Drei Stellen anpassen:

1. `SHAPES` — Voicing(s) hinterlegen
2. `QMAP` — Eingabetext → Bibliotheksschlüssel (mehrere Aliasse erlaubt)
3. `QFAMILY` — Bibliotheksschlüssel → `maj` | `dom` | `min` | `dim` | `hdim` | `aug`
   (steuert Groß-/Kleinschreibung und Suffix der Stufenangabe)

## Voicing gegenrechnen

Vor dem Einchecken prüfen, ob die Töne stimmen:

```
Halbton = (OPEN[saite] + bund) % 12      OPEN = [4, 9, 2, 7, 11, 4]   // E A D G B e
```

Beispiel `C6` A-Form, Ankerbund 3 → Bünde `x 3 2 2 1 x`
→ `(9+3)%12=0` C, `(2+2)%12=4` E, `(7+2)%12=9` A, `(11+1)%12=0` C → C·E·A = C6 ✓
