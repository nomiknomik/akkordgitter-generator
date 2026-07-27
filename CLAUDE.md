# CLAUDE.md — Projektkontext Akkordgitter-Generator

> **Einstiegspunkt für jeden neuen Chat.** Repo: `nomiknomik/akkordgitter-generator`
> (öffentlich). Dateien per GitHub-API lesen (`github-push`-Skill) oder Repo klonen,
> dann hier weiterlesen. Aktuelle Version: **v1.8**.
>
> Was als Nächstes geplant ist, steht in [`docs/roadmap.md`](docs/roadmap.md).

## Was das ist

Einzeldatei-Webapp (`index.html`) — kein Build, keine Abhängigkeiten, läuft per
Doppelklick, als Artefakt in claude.ai und auf GitHub Pages.

Sie setzt eine getippte Akkordfolge in ein **Akkordgitter im Stil der
Gypsy-Jazz-Chord-eBooks** (DjangoSolos / Colin Cosimini, © 2009) und ergänzt
Stufenanalyse, Griffbilder, harmonische Deutung und Wiedergabe.

**Live:** https://nomiknomik.github.io/akkordgitter-generator/

Nutzer: Alex — Gitarrist und Arzt, baut sich gerne wiederverwendbare Werkzeuge,
kommuniziert deutsch, mag knappe Antworten und achtet auf Token-Effizienz.

## Dateien

| Pfad | Inhalt |
|---|---|
| `index.html` | die komplette App (HTML + CSS + JS in einer Datei) |
| `README.md` | Kurzbeschreibung, Feature-Liste |
| `CLAUDE.md` | diese Datei — Kontext, Architektur, Konventionen |
| `docs/roadmap.md` | **geplante Arbeitspakete** — hier zuerst schauen |
| `docs/syntax.md` | vollständige Eingabesyntax |
| `docs/griffbibliothek.md` | Format der `SHAPES`, wie neue Griffe ergänzt werden |
| `docs/instrumente.md` | Stimmungen und Funktionsweise des Griffgenerators |
| `docs/taktaufteilung.md` | Geometrie der Taktunterteilungen (Original-Vorlage) |
| `docs/analyse.md` | Regeln der harmonischen Analyse und ihre Grenzen |
| `docs/pdf-extraktion.md` | **Griffe und Songs aus einem PDF übernehmen** |
| `docs/skill-ideen.md` | was sich als eigener Skill lohnt — und was nicht |
| `docs/entwicklungslog.md` | Entscheidungen, Fehler, Prüfvorgehen |
| `tools/chart_einbetten.py` | schreibt einen Chart aus `charts/` als Vorgabe in `index.html` (nicht von Hand pflegen) |
| `tools/griffbild_vektor.py` | **liest Griffbilder aus der PDF-Vektorebene → Bundliste (exakt, zuerst versuchen)** |
| `tools/griffbild_lesen.py` | liest Griffbilder aus Bildern → Bundliste (Rückfall, wenn die Seite ein Bild ist) |
| `tools/voicing_pruefen.py` | rechnet Bundlisten gegen die Akkordtöne |
| `archiv/CHANGELOG.md` | Versionshistorie |
| `archiv/v1.0…v1.2/` | eingefrorene Vorversionen |
| `charts/*.json` | gespeicherte Charts (Export-Format der App) |
| `charts/index.json` | Verzeichnis der Charts für das Auswahlmenü |

## Architektur von `index.html`

Das `<script>` ist in nummerierte Abschnitte gegliedert — beim Bearbeiten
**gezielt per `str_replace`**, nicht die Datei neu schreiben.

1. **Musik-Grundlagen** — `NOTES`, `FLATS`, `INSTRUMENTS` (Stimmungen),
   `OPEN()` / `OPEN_MIDI()`, `pitchOf()`
2. **Griff-Bibliothek** — `SHAPES` (kuratierte Gitarrenvoicings aus dem Buch),
   `QMAP` (Schreibweise → Qualität), `QSHORT` (kanonische Kurzform),
   `QFAMILY` (Klanggeschlecht), `CHORD_TONES` + `ESSENTIAL` (für den Generator)
3. **Parser** — `parseChord()` (Grundton, Qualität, Bassnote, `@Lage`, `:Beats`),
   `parseSource()` (Zeilen → Takte, `[Formteil]`, Umbruch nach Takte/Zeile)
4. **Stufenanalyse** — `degreeOf()`, `ROMAN`, `DIATONIC_MAJ/MIN`
5. **4b. Harmonische Analyse** — `analyzeChart()`: Quintfallketten, ii–V,
   Zwischendominanten, Tritonussubstitution vs. chromatische Rückung,
   verminderte Durchgänge, Modal Interchange, Schlusswendung
6. **Griffberechnung** — `shapesFor()`, `genVoicings()` (Griffe aus Akkordtönen
   für beliebige Stimmungen), `allVoicings()`, `bestVoicing()`, `diagramSVG()`
7. **Rendering** — `render()` baut das Blatt **und** `state.bars` (Grundlage der
   Wiedergabe); `buildBar()`, `defaultBeats()`, `LAYOUTS`, `layoutFor()`,
   `renderBar()`, `bindSheet()` (Inline-Edit + Lagenwechsel), `writeBack()`
8. **Wiedergabe** — Web Audio: `buildBeatMap()`, `SOUNDS` (Klangfarben), `voice()`,
   `strum()`, `click()`, `scheduler()` (25-ms-Timer, 200-ms-Lookahead),
   `highlight()` (rAF-Playhead)
9. **Undo/Redo** — `hist`-Stack über JSON-Snapshots von `currentData()`
10. **Beispiel + I/O** — `EXAMPLE` (All Of Me), `loadData()`, `currentData()`, Init

### Wichtige Datenstrukturen

```js
// Akkord (aus parseChord)
{raw, rootName, rootPitch, quality, qtext, bassName, bassPitch, pos?, beats,
 name,    // wie geschrieben, z. B. "CM6"
 short,   // kanonisch, z. B. "C6"
 canon,   // Identität "pitch|quality|bass" – C6 und CM6 sind gleich
 err?}

// Takt (aus buildBar) — liegt in state.bars, Reihenfolge = Spielreihenfolge
{raw, line, tok, idx, section, wedge:null|'first'|'last', repeat:bool, chords:[Akkord]}

// Griff-Shape (SHAPES)
{s:0|1,        // Ankersaite: 0 = tiefe E, 1 = A
 a:0,          // Halbtonabstand Ankerton→Grundton (4 = Terz im Bass usw.)
 f:[6 Werte],  // Bundabstände zum Ankerbund [E,A,D,G,B,e], null = X
 n:'A-Form'}   // Anzeigename
```

## Konventionen

- **Deutsch** in UI, Kommentaren und Doku.
- Kein Framework, kein Build, **kein `localStorage`** (in claude.ai-Artefakten
  verboten) — Persistenz über JSON-Export/-Import.
- Die **Textquelle im Eingabefeld ist führend**; Klicks im Gitter schreiben dorthin
  zurück. Nie einen zweiten Zustand danebenlegen.
- Neue Akkordqualität = **fünf** Stellen: `SHAPES`, `QMAP`, `QSHORT`, `QFAMILY`,
  `CHORD_TONES` + `ESSENTIAL`. Zusätzlich `TONE`/`WESENTLICH` in
  `tools/voicing_pruefen.py` synchron halten.
- `state.variants` ist nach `canon` verschlüsselt, nicht nach Schreibweise.
- Voicings **vor dem Einchecken gegenrechnen** (`tools/voicing_pruefen.py`) **und**
  mit dem Bild vergleichen. Beides, siehe unten.
- Versionsnummer bei jeder inhaltlichen Änderung in `archiv/CHANGELOG.md`
  fortschreiben, Vorversion nach `archiv/vX.Y/` einfrieren.

## Die beiden wichtigsten Lektionen

1. **Akkordton-Prüfung und Quelltreue sind zwei verschiedene Dinge.** Ein Voicing
   kann harmonisch fehlerfrei und trotzdem das falsche sein. Genau so entstanden die
   Fehler in `C6/G` und `E7/B`, die bis v1.2 unbemerkt blieben. Wer eine Vorlage
   nachbaut: Punkt für Punkt vergleichen.
2. **Bei einem gefundenen Fehler die ganze Kategorie prüfen.** Das systematische
   Nachrechnen aller Slash-Voicings förderte zwei weitere Fehler zutage, nach denen
   niemand gefragt hatte.

## Testen ohne Browserfenster

```python
# Playwright ist in der Claude-Sandbox verfügbar
pg.goto('file:///.../index.html')
pg.evaluate("()=>state.bars.map(b=>b.chords.map(c=>c.name+'/'+c.beats))")
pg.evaluate("()=>buildBeatMap().map(s=>s?s.ch.name:'-')")
pg.evaluate("()=>bestVoicing(parseChord('C6/G'),0).frets")
```

Reine Musiklogik in Node testen: Abschnitte 1–6 aus dem `<script>` schneiden,
`module.exports` anhängen. Syntaxprüfung mit `node --check`.

**Nicht prüfbar in der Sandbox:** Klang der Wiedergabe (keine Audioausgabe),
Druckbild auf A4, die Live-Seite selbst (github.io nicht in der Netzwerk-Freigabe —
nur der Build-Status über die API).

## Infrastruktur

Öffentliches Repo, GitHub Pages aus `main`, Pfad `/`. Push über die REST-API
(`github-push`-Skill), kein git-CLI. Nach einem Push braucht der Pages-Build
etwa 15–30 Sekunden; ein zwischenzeitliches `errored` bei `/pages/builds/latest`
kann noch in `built` umschlagen.
