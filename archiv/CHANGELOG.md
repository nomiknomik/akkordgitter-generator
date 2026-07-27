# Changelog

## v1.7 — 2026-07-27
- **Taktversatz in der Video-Synchronisation behoben.** `data-bar` ist 0-basiert,
  die Taktnummern im Gitter sind 1-basiert — die Markierung lag deshalb einen
  Takt daneben, und ein Klick sprang um einen Takt zu früh. Beides betraf nur
  die in v1.6 neu hinzugekommene Synchronisation, nicht die eigene Wiedergabe
  (die rechnet direkt mit `idx`). Von Alexander Zabelyshenskiy bemerkt.
- **Kalibrierung als zwei nummerierte Schritte** dargestellt, mit erklärendem
  Vorspann und Rückmeldung nach jedem Schritt. Hinweis ergänzt, dass ein
  größerer Abstand zwischen den beiden Stützstellen das Tempo genauer macht.
- **Vorgabe-Chart ist jetzt die Holovaty-Fassung** (mit Video-ID, La Pompe und
  Quellpräferenz). Sie steht eingebettet in `index.html`, damit die App auch
  per Doppelklick ohne Server startet; `tools/chart_einbetten.py` erzeugt den
  Block aus `charts/*.json`, damit beide Fassungen nicht auseinanderlaufen.

## v1.6 — 2026-07-27
- **Video-Synchronisation.** Ein YouTube-Video lässt sich einbetten und das
  Gitter mitlaufen lassen: über zwei Stützstellen (Beginn von Takt 1 und Beginn
  eines späteren Taktes) ergeben sich Startzeit und Sekunden je Takt, daraus
  das Tempo. Bei aktivem „Video folgen“ springt ein Klick auf einen Takt an die
  passende Stelle. Eingebettet über `youtube-nocookie.com`; die eigene Wiedergabe
  wird dabei angehalten. Die Zuordnung ist linear und trägt so weit, wie das
  Tempo der Aufnahme gleichmäßig bleibt. Video-ID und Kalibrierung stehen im
  Chart-JSON unter `video`.
- **Korrektur Takt 16 und 48** im Holovaty-Chart: statt `Ab°` im 4. Bund steht
  dort jetzt `Bb°` im 6. Bund. Es ist derselbe Griff, zwei Bünde höher. Die
  Bassnote auf der tiefen E-Saite läuft damit F/A (5) – B♭° (6) – G/B (7) –
  C6 (8), also chromatisch aufwärts; die Vorlage bricht diese Linie. Beide sind
  für sich gültige dim7-Griffe, die Vorlage ist also in sich stimmig, im
  Zusammenhang aber unplausibel. Vermerkt im Chart unter `abweichungen`; die
  Griffbibliothek bleibt unverändert.

## v1.5 — 2026-07-27
- **Zweite Quelle in der Griffbibliothek.** Aus dem Chord-Melody-Arrangement von
  Adrian Holovaty zu *All Of Me* wurden 67 Griffbilder ausgelesen; daraus
  11 verschiedene Voicings, davon 8 neu gegenüber der bisherigen Bibliothek.
  Jeder Griff ist gegen die Akkordtöne gegengerechnet, ein Testlauf prüft, dass
  die App alle 20 vorkommenden Symbole bundgenau reproduziert.
- **Quellenkennzeichnung**: jedes Shape trägt jetzt ein Feld `q` (`cosimini` |
  `holovaty`), Register in `QUELLEN`. Neue Auswahl „Griffe bevorzugt aus“
  sortiert die Voicings entsprechend; die Quelle steht unter jedem Griffbild.
  Damit bleibt nachvollziehbar, von welchem Gitarristen ein Voicing stammt.
- **Neuer Extraktionsweg**: die Griffbilder lassen sich direkt aus der
  **Vektorebene** des PDF lesen — exakt und ohne Pixelanalyse. Zwei Fallen sind
  dokumentiert: geteilte Lagenziffern bei Doppeldiagrammen und der verdickte
  **Sattelbalken** als Kennzeichen der offenen Lage. Siehe `docs/pdf-extraktion.md`.
- **Griffbilder farbcodiert**: Punktfarbe und Beschriftung geben die Tonfunktion
  an (Grundton, Terz, Quinte, Septime, Sexte, None, alteriert), Grundton
  zusätzlich umrandet. Diagramme etwas größer, Farblegende über der Grifftabelle.
- **Automatische Tonarterkennung** (Schaltfläche „Tonart erkennen“): bewertet
  alle 24 Tonarten nach Leitereigenheit, charakteristischen Funktionen sowie
  Anfangs- und Schlussakkord.
- **La-Pompe-Rhythmus** in der Wiedergabe: auf 1 und 3 gedämpfter Grundschlag mit
  Auftakt, auf 2 und 4 der betonte Schlag; alle Anschläge werden sofort
  abgedämpft. Umschaltbar über „Rhythmus“.
- **Stufenangabe im Gitter deutlich größer** (bis 21 px statt 15 px, halbfett).
- **Hintergrund aufgehellt** (`#14181f` → `#2f3540`), Eingabefelder angepasst.
- **Fußzeile** mit Version, Autor und Link auf das GitHub-Repository.
- **Kürzere Zeilen behalten die Kachelgröße.** Bisher wurde jede Zeile auf die
  volle Blattbreite gestreckt; da `.bar` quadratisch ist, wurden Takte einer
  angebrochenen Zeile entsprechend größer. Solche Zeilen nehmen jetzt nur den
  ihnen zustehenden Anteil ein (z. B. 6 von 8 Takten = 75 % Breite).
- **Charts**: `all-of-me.json` aufgeteilt in `all-of-me-cosimini.json` und
  `all-of-me-holovaty.json`; neuer Umschalter lädt Charts direkt aus
  `charts/index.json` (nur über http/https, bei `file://` ausgeblendet).

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
