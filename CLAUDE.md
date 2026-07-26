# CLAUDE.md — Projektkontext Akkordgitter-Generator

> Diese Datei ist der Einstiegspunkt für jeden neuen Chat. Repo klonen bzw. Dateien
> per GitHub-API lesen (`github-push`-Skill, Repo `nomiknomik/akkordgitter-generator`,
> **privat**), dann hier weiterlesen.

## Was das ist

Einzeldatei-Webapp (`index.html`) — kein Build, keine externen Abhängigkeiten,
läuft per Doppelklick im Browser und als Artefakt in claude.ai.
Sie setzt eine getippte Akkordfolge in ein **Akkordgitter im Stil der Gypsy-Jazz-Chord-eBooks**
(DjangoSolos / Colin Cosimini, Quelle: *All Of Me*, Key of C, 32 Bars) und ergänzt
Stufenanalyse, Griffbilder und Wiedergabe.

Nutzer: Alex — Gitarrist/Arzt, arbeitet gerne mit wiederverwendbaren Werkzeugen,
kommuniziert deutsch, mag knappe Antworten und Token-Effizienz.

## Dateien

| Pfad | Inhalt |
|---|---|
| `index.html` | die komplette App (HTML + CSS + JS in einer Datei) |
| `README.md` | Kurzbeschreibung, Feature-Liste |
| `CLAUDE.md` | diese Datei — Kontext, Architektur, Konventionen |
| `docs/syntax.md` | vollständige Eingabesyntax |
| `docs/griffbibliothek.md` | Format der `SHAPES`, wie neue Griffe ergänzt werden |
| `docs/taktaufteilung.md` | Geometrie der Taktunterteilungen (Original-Vorlage) |
| `archiv/CHANGELOG.md` | Versionshistorie |
| `archiv/v1.0/index.html` | eingefrorene Vorgängerversion |
| `charts/*.json` | gespeicherte Charts (Export-Format der App) |

## Architektur von `index.html`

Das `<script>` ist in nummerierte Abschnitte gegliedert — beim Bearbeiten
**gezielt per `str_replace`** arbeiten, nicht die Datei neu schreiben.

1. **Musik-Grundlagen** — `NOTES`, `FLATS`, `OPEN` (Leersaiten in Halbtönen), `pitchOf()`
2. **Griff-Bibliothek** — `SHAPES` (Voicings), `QMAP` (Schreibweise → Qualität),
   `QFAMILY` (Qualität → Klanggeschlecht für die Stufenanalyse)
3. **Parser** — `parseChord()` (Grundton, Qualität, Bassnote, `@Lage`, `:Beats`),
   `parseSource()` (Zeilen → Takte, `[Formteil]`, Zeilenumbruch)
4. **Stufenanalyse** — `degreeOf()`, `ROMAN`, `DIATONIC_MAJ/MIN`, Zwischendominanten
5. **Griffberechnung** — `shapesFor()`, `allVoicings()` (alle spielbaren Lagen,
   nach Bund sortiert), `bestVoicing()`, `diagramSVG()`
6. **Rendering** — `render()` baut das Blatt **und** `state.bars` (Grundlage der
   Wiedergabe); `buildBar()`, `defaultBeats()`, `LAYOUTS`, `layoutFor()`, `renderBar()`,
   `bindSheet()` (Inline-Edit + Lagenwechsel), `writeBack()`
7. **Wiedergabe** — Web Audio: `buildBeatMap()`, `strum()`, `click()`,
   `scheduler()` (25-ms-Timer, 200-ms-Lookahead), `highlight()` (rAF-Playhead)
8. **Undo/Redo** — `hist`-Stack über JSON-Snapshots von `currentData()`
9. **Beispiel + I/O** — `EXAMPLE` (All Of Me), `loadData()`, `currentData()`, Init

### Wichtige Datenstrukturen

```js
// Akkord (aus parseChord)
{raw, rootName, rootPitch, quality, qtext, bassName, bassPitch, pos?, beats, name, err?}

// Takt (aus buildBar) — liegt in state.bars, Reihenfolge = Spielreihenfolge
{raw, line, tok, idx, wedge:null|'first'|'last', repeat:bool, chords:[Akkord]}

// Griff-Shape (SHAPES)
{s:0|1,        // Ankersaite: 0 = tiefe E, 1 = A
 a:0,          // Halbtonabstand Ankerton→Grundton (4 = Terz im Bass usw.)
 f:[6 Werte],  // Bundabstände zum Ankerbund [E,A,D,G,B,e], null = X
 n:'A-Form'}   // Anzeigename
```

## Konventionen

- **Deutsch** in UI, Kommentaren und Doku.
- Kein Framework, kein Build, **kein `localStorage`** (in claude.ai-Artefakten verboten) —
  Persistenz läuft über JSON-Export/-Import.
- Neue Akkordqualität ergänzen = drei Stellen: `SHAPES`, `QMAP`, `QFAMILY`.
- Voicings vor dem Einchecken gegen die Akkordtöne rechnen
  (Halbton = `(OPEN[saite] + bund) % 12`), nicht aus dem Gedächtnis eintragen.
- Versionsnummer bei jeder inhaltlichen Änderung in `archiv/CHANGELOG.md` fortschreiben.

## Testen ohne Browserfenster

```python
# Playwright ist in der Claude-Sandbox verfügbar
pg.goto('file:///.../index.html')
pg.evaluate("()=>state.bars.map(b=>b.chords.map(c=>c.name+'/'+c.beats))")
pg.evaluate("()=>buildBeatMap().map(s=>s?s.ch.name:'-')")
```
Reine Musiklogik lässt sich auch in Node testen: Abschnitte 1–5 aus dem `<script>`
schneiden und `module.exports` anhängen.

## Offene Ideen

- Transponieren (Tonart wechseln → Akkorde mitziehen)
- Songbook: mehrere Charts in einer Datei, Sammel-PDF
- Bass-Line/„La Pompe“-Rhythmus statt gleichmäßiger Schläge
- Automatische Lagenwahl nach kleinster Griffbewegung zum Vorgängerakkord
- Import von iReal-Pro- oder ChordPro-Dateien
