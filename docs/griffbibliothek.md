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
| `q` | **Quelle** — Schlüssel in `QUELLEN`, z. B. `cosimini`, `holovaty` |

Der **Ankerbund** ist die Zahl, die im Gitter links oben im Takt und im Griffbild
links neben dem Diagramm steht. `f[s]` muss deshalb immer `0` sein.

## Quelle mitschreiben — Pflicht

Jedes Voicing stammt von einem konkreten Gitarristen; das ist der Wert dieser
Sammlung gegenüber rechnerisch erzeugten Griffen. Die Herkunft lässt sich
nachträglich **nicht** rekonstruieren, deshalb wird `q` bei jedem neuen Eintrag
gesetzt und in `QUELLEN` ein Klartextname hinterlegt:

```js
const QUELLEN = {
  cosimini: {n:'DjangoSolos / Colin Cosimini', j:'2009'},
  holovaty: {n:'Adrian Holovaty, „All Of Me“',  j:'Arrangement'}
};
```

Nachträge einer neuen Quelle stehen in `SHAPES_ADD` und werden beim Laden an
`SHAPES` angehängt — so bleibt der Grundbestand als Block lesbar. Die Auswahl
„Griffe bevorzugt aus“ sortiert Voicings der gewählten Quelle nach vorn; das
wirkt auch auf `@n`, sodass ein Chart die Griffe eines bestimmten Buchs
bundgenau reproduziert.

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

## Herkunft der Voicings

Die Einträge in `SHAPES` stammen aus dem Gypsy-Jazz-Chord-eBook (DjangoSolos,
Colin Cosimini). Sie sind **nicht** beliebige gültige Griffe, sondern die
stilistisch gemeinten Formen. Wer sie ändert, ändert den Klang des Buches —
also nur mit Vorlage.

Kommen Voicings aus einer **zweiten Quelle** dazu, siehe
[`roadmap.md`](roadmap.md), Arbeitspaket 1: dort steht die offene Entwurfsfrage
zur Herkunftskennzeichnung.

## Voicing gegenrechnen

Vor dem Einchecken prüfen, ob die Töne stimmen:

```
Halbton = (OPEN[saite] + bund) % 12      OPEN = [4, 9, 2, 7, 11, 4]   // E A D G B e
```

Beispiel `C6` A-Form, Ankerbund 3 → Bünde `x 3 2 2 1 x`
→ `(9+3)%12=0` C, `(2+2)%12=4` E, `(7+2)%12=9` A, `(11+1)%12=0` C → C·E·A = C6 ✓

Bequemer mit dem Werkzeug:

```bash
python3 tools/voicing_pruefen.py C6 x 3 2 2 1 x
```

Es meldet akkordfremde und fehlende Töne und gibt die Spanne aus. Ein fehlender
**Grundton** ist nur ein Hinweis (Rootless-Voicings sind üblich), eine fehlende
**Terz** oder **Septime/Sexte** dagegen ein echter Fehler.

## Achtung: Töne prüfen ≠ Vorlage treffen

Die Tonprüfung findet falsche Töne — aber nicht das falsche Voicing. Das bis v1.2
hinterlegte `E7/B` (`7,7,9,7,9,x`) bestand sie fehlerfrei, war aber trotzdem falsch:
Das Original schreibt ein Rootless-Voicing mit stummer A- und H-Saite vor
(`7,x,6,7,x,x`). **Immer zusätzlich das Bild vergleichen**, Vorgehen in
[`pdf-extraktion.md`](pdf-extraktion.md).

## Korrekturhistorie

| Version | Shape | Was war falsch |
|---|---|---|
| v1.3 | `6/7` (`C6/G`) | Zusatznote auf der H-Saite, im Original stumm |
| v1.3 | `7/7` (`E7/B`) | war nicht als Rootless-Voicing angelegt |
| v1.3 | `7/4` | akkordfremde Töne (beim Nachrechnen gefunden) |
| v1.3 | `m7/3` | akkordfremde Töne (beim Nachrechnen gefunden) |
| v1.3 | `7#5` (`G7+`) | hohe E-Saite fehlte gegenüber dem Original |
