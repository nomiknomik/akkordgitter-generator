# Akkordgitter-Generator

Einzeldatei-Webapp (`index.html`, kein Build, keine Abhängigkeiten), die eine
Akkordfolge in ein Akkordgitter im Stil der *Gypsy Jazz Chord eBooks*
(DjangoSolos / Colin Cosimini) setzt.

- **Lage** (Bundangabe) links oben in jedem Takt — automatisch aus der Griffbibliothek berechnet
- **Stufe in der Tonart** als Randnotiz rechts oben (inkl. Zwischendominanten `V7/x`)
- **Griffbilder** aller vorkommenden Akkorde unterhalb des Gitters, mit umschaltbaren Lagen
- **Quadratische Taktboxen** mit den Aufteilungen der Vorlage (4 · 2+2 · 1+1+2 · 2+1+1 · 1+1+1+1
  sowie die Keilformen „nur 1. Beat“ / „nur letzter Beat“)
- **Instrumente**: Gitarre, Drop D, Ukulele, Baritonukulele, Mandoline, Tenorbanjo, Bass —
  Griffe werden für fremde Stimmungen aus den Akkordtönen berechnet
- **Harmonische Analyse** unter dem Gitter: ii–V, Zwischendominanten, Tritonussubstitution,
  verminderte Durchgänge, Modal Interchange, Schlusswendung
- **Wiedergabe** mit stufenlosem Tempo (40–300 BPM), sechs Klangfarben, Metronom, Loop,
  Einzähler und mitlaufendem Playhead
- **Undo/Redo** (Strg+Z / Strg+Shift+Z), Leertaste startet und stoppt
- Takte direkt im Gitter anklickbar/editierbar, Rückschreiben in die Textquelle
- Export/Import als JSON, Druck-/PDF-Layout via `@media print`

## Projektstruktur

```
index.html            die App (alles in einer Datei)
CLAUDE.md             Projektkontext für neue Claude-Chats
docs/syntax.md        Eingabesyntax
docs/griffbibliothek.md   Griffe ergänzen
docs/taktaufteilung.md    Geometrie der Taktunterteilungen
docs/instrumente.md       Stimmungen, Griffgenerator
docs/analyse.md           Regeln der harmonischen Analyse
archiv/CHANGELOG.md   Versionshistorie
archiv/v1.0/          eingefrorene Vorversion
charts/               gespeicherte Charts (JSON)
```

## Eingabesyntax

| Schreibweise | Bedeutung |
|---|---|
| `\|` | Taktstrich |
| `%` | Takt wiederholen |
| `C6 Bb7` | zwei Akkorde in einem Takt (Splitbox mit Diagonale) |
| `[A]` | Formteil-Marke |
| `C6/G` | Bassnote (Slash-Akkord) |
| `C6@8` | Lage erzwingen (Ankerton in Bund 8) |
| `C6:2` | Dauer in Beats (steuert Taktaufteilung und Wiedergabe) |
| `>C6` / `<C6` | nur 1. bzw. nur letzter Beat des Taktes |
| `-` | Moll (`D-9` = Dm9) |
| `°` / `o` | vermindert |
| `0` / `ø` | halbvermindert |
| `7+` | 7#5 |

## Erweitern

**Neue Griffe** → Objekt `SHAPES` (Abschnitt 2 im `<script>`):

```js
'm11': [{s:1, f:[null,0,-2,0,0,null], n:'A-Form'}]
```

- `s` = Ankersaite (`0` = tiefe E-Saite, `1` = A-Saite)
- `a` = Halbtonabstand des Ankertons zum Grundton (Default `0`; für Umkehrungen
  z. B. `4` = Terz im Bass, `7` = Quinte im Bass)
- `f` = sechs Bundabstände zum Ankerbund `[E,A,D,G,B,e]`, `null` = Saite nicht anschlagen
- Slash-Akkorde werden unter dem Schlüssel `<qualität>/<halbtonintervall>` gesucht,
  z. B. `maj/4` (Terz im Bass), `7/7` (Quinte im Bass); fehlt der Eintrag,
  greift automatisch die Grundstellung.

**Neue Akkordschreibweisen** → `QMAP` (Eingabe → Bibliotheksschlüssel) und
`QFAMILY` (Bibliotheksschlüssel → Klanggeschlecht für die Stufenanalyse).

**Stufenlogik** → `degreeOf()`; diatonische Referenz in `DIATONIC_MAJ` / `DIATONIC_MIN`.

Ausführlich: [`docs/syntax.md`](docs/syntax.md)

## Nächste Ideen

- Transponieren der ganzen Nummer (Tonart wechseln → Akkorde mitziehen)
- Mehrere Songs in einer Datei / Songbook-Export als PDF
- Playback (Tone.js) und Metronom
- Alternative Voicings automatisch nach kleinster Lagenbewegung wählen
