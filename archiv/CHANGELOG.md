# Changelog

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
