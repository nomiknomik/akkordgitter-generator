# Changelog

## v1.4 — 2026-07-26
- `G7+` (`7#5`, E-Form) um die hohe E-Saite ergänzt — Abweichung vom Original,
  gefunden beim Testen des neuen Extraktionswerkzeugs
- **Werkzeuge**: `tools/griffbild_lesen.py` (liest Griffbilder per Pixelanalyse
  aus Bildern aus, erkennt Saitenspalten, Bundzeilen, Punkte, x/o-Marker und die
  Bezugszeile der Lagenziffer) und `tools/voicing_pruefen.py` (rechnet Bundlisten
  gegen die Akkordtöne, behandelt Rootless-Voicings als Hinweis statt Fehler)
- **Dokumentation**: `docs/pdf-extraktion.md`, `docs/roadmap.md`,
  `docs/skill-ideen.md`, `docs/entwicklungslog.md`; `CLAUDE.md` als vollständiger
  Projekteinstieg neu gefasst; `griffbibliothek.md` um Prüf-Workflow und
  Korrekturhistorie erweitert

## v1.3 — 2026-07-26
- **Korrektur der Slash-Akkord-Voicings** gegen die Original-Griffbilder im PDF
  (pixelgenau nachvollzogen): `C6/G` und `E7/B` enthielten eine zusätzliche,
  im Original stummgeschaltete Note auf der H-Saite. `E7/B` ist jetzt korrekt
  als „rootless“ Voicing (Bass=Quinte, ohne Grundton) hinterlegt, wie im Original.
  Bei der Gelegenheit auch `7/4` und `m7/3` korrigiert, die zuvor
  akkordfremde Töne enthielten (unabhängig vom PDF entdeckt, beim Nachrechnen aller
  Slash-Voicings aufgefallen).
- **Schrift im Akkordgitter deutlich vergrößert** (Chordsymbole, Lage- und
  Stufenangabe), angelehnt an die Originalgröße im eBook.

## v1.2 — 2026-07-26
- Zeilenumbruch strikt nach „Takte/Zeile“ (Standard **8 Kästchen pro Reihe**);
  Schriftgrößen skalieren über Container-Queries mit der Boxbreite
- **Instrumentenauswahl**: Gitarre, Drop D, Ukulele (High-/Low-G), Baritonukulele,
  Mandoline, Tenorbanjo, Bass — Griffbilder und Wiedergabetonhöhen folgen der Stimmung
- **Griffgenerator** `genVoicings()`: berechnet Griffe aus den Akkordtönen für alle
  Instrumente ohne kuratierte Bibliothek und als Rückfallebene bei der Gitarre;
  Lagenangabe `0` = offener Akkord
- **Harmonische Analyse**: Quintfallketten, ii–V(–I), Zwischendominanten,
  Tritonussubstitution vs. chromatische Rückung, verminderte Durchgänge,
  Modal Interchange, Schlusswendung, Stufenfolge je Formteil
- **Klangfarben** für die Wiedergabe: Stahlsaite, Nylon/Jazz, Klavier, E-Piano,
  Vibraphon, Streicher
- Gleiche Akkorde werden in der Grifftabelle zusammengefasst: `C6` und `CM6`
  ergeben eine Karte mit Hinweis auf die andere Schreibweise

## v1.1 — 2026-07-26
- Taktboxen quadratisch (`aspect-ratio: 1/1`)
- Taktaufteilungen nach eBook-Vorlage: 4 · 2+2 · 1+1+2 · 2+1+1 · 1+1+1+1
  sowie die Keilformen „nur 1. Beat“ (`>`) und „nur letzter Beat“ (`<`)
- Beat-Dauer je Akkord über Suffix `:n`
- Wiedergabe (Web Audio): gestrummte Akkorde aus den berechneten Voicings,
  Metronom mit Taktakzent, Tempo 40–300 BPM stufenlos, Loop, Einzähler,
  mitlaufender Playhead (Takt- und Feldmarkierung)
- Undo/Redo über Snapshot-Stack, Tastenkürzel Strg+Z / Strg+Shift+Z, Leertaste = Play
- Stufenangabe je Feld auch in geteilten Takten (Lage + Stufe als Mikrozeile)
- Projektdoku: `CLAUDE.md`, `docs/`, `archiv/`, `charts/`

## v1.0 — 2026-07-26
- Erste Fassung: Akkordgitter im DjangoSolos-Format
- Parser für Akkordsymbole inkl. Bassnoten, `%`-Wiederholung, Formteile
- Stufenanalyse mit Zwischendominanten
- Griffbibliothek mit automatischer Lagenberechnung, SVG-Griffbilder
- Inline-Bearbeitung im Gitter, JSON-Export/-Import, Druckansicht
