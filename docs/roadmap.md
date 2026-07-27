# Geplante Arbeitspakete

Stand v1.5.

---

## Erledigt in v1.5 / v1.6

- **Solo-Chorus + erweitertes Tag im Holovaty-Chart** (v1.10, Takt 33–68 aus
  der PDF ergänzt). Formteile umbenannt (`Solo A/B/A2/C`) statt eigener Namen,
  damit akkordgleiche Abschnitte erkennbar bleiben.

- **Zweite Quelle in der Bibliothek** (Holovaty, *All Of Me*) — die in v1.3
  offene Entwurfsfrage ist entschieden: jedes Shape trägt ein Feld `q`, dazu
  gibt es einen Quellenfilter. Rückwirkend wäre die Herkunft nicht mehr
  rekonstruierbar gewesen.
- **Zweite Interpretation als Chart** (`charts/all-of-me-holovaty.json`) samt
  Auswahlmenü, das die Dateien aus `charts/index.json` direkt anbietet.
- **La Pompe**, **automatische Tonarterkennung**, farbcodierte Griffbilder.
- **Video-Synchronisation** mit YouTube (v1.6), lineare Zuordnung über zwei
  Stützstellen.

---

## 1. Weitere Akkorde aus einer dritten Quelle

**Vorgehen:** [`pdf-extraktion.md`](pdf-extraktion.md), **Weg A** zuerst
versuchen — die Vektorebene liefert exakte Werte ohne Handarbeit.

**Nicht vergessen:**
- `q` setzen und `QUELLEN` ergänzen.
- Bei neuen Akkordqualitäten sind **fünf** Stellen zu pflegen: `SHAPES` bzw.
  `SHAPES_ADD`, `QMAP`, `QSHORT`, `QFAMILY`, `CHORD_TONES` + `ESSENTIAL`.
- `TONE`/`WESENTLICH` in `tools/voicing_pruefen.py` spiegeln
  `CHORD_TONES`/`ESSENTIAL` aus `index.html`. Beide Stellen synchron halten.

## 2. Skills aus diesem Projekt ableiten

Details in [`skill-ideen.md`](skill-ideen.md). Nach v1.5 ist die klarste
Kandidatin schärfer geworden:

1. **`griffbild-extraktion`** — jetzt mit zwei Wegen (Vektor zuerst, Pixel als
   Rückfall) und den beiden dokumentierten Fallen. Abgeschlossene Aufgabe,
   erprobte Werkzeuge, nicht-offensichtliche Methode, außerhalb dieses Projekts
   nutzbar. Zweimal gebraucht — damit kein Einzelfall mehr.
2. **`harmonische-analyse`** — Stufenanalyse in Textform, Regelwerk in
   `analyse.md`.
3. **`akkord-voicing-pruefung`** — klein; ginge auch als Teil von (1).

## Kleinere offene Punkte

- **Transponieren**: Tonart wechseln → Akkorde mitziehen. Nicht implementiert.
- **Lagenwahl nach Griffnähe**: aktuell wird die tiefste spielbare Lage gewählt,
  ohne den Vorgängerakkord zu berücksichtigen.
- **Songbook-PDF** über mehrere Charts.
- **Druckbild**: bei 8 Takten/Zeile noch nicht auf A4 gegengeprüft.
- **La Pompe verfeinern**: derzeit ein festes Muster; Varianten (halbe Zeit,
  Walzer, „à la Django“ mit Bassläufen) wären hörbar besser.
- **Melodiestimme**: die Arrangements enthalten TAB, die App nicht. Bewusst
  ausgeklammert — hier geht es um Akkordgitter.
- **Video-Synchronisation bei schwankendem Tempo**: die Zuordnung ist eine
  Gerade durch alle Bezugspunkte. Für Aufnahmen mit ziehendem Tempo wäre
  abschnittsweise Interpolation zwischen den Punkten nötig statt einer
  gemeinsamen Geraden.
- **Automatische Beat-Erkennung** ist für YouTube ausgeschlossen: der Player
  läuft in einem iframe fremder Herkunft, Web Audio erhält keinen Zugriff auf
  dessen Tondaten. Denkbar wäre sie nur für lokal geladene Audiodateien
  (`createMediaElementSource` + Onset-Erkennung) oder über eine
  Tab-Tonaufnahme via `getDisplayMedia({audio:true})` — beides ein anderer
  Eingabeweg, kein Ersatz für die jetzige Kalibrierung.
- **Video über mehrere Chorusse**: der Chart umfasst einen Durchgang, die
  Aufnahme mehrere. Derzeit kalibriert man auf den Durchgang, den man braucht;
  ein Umlauf über die Formlänge wäre die naheliegende Erweiterung.
- **Formteil-Referenzsyntax**: `[...]`-Marken sind reine Anzeigetexte
  (`parseSource()`), keine Verweise. Akkordgleiche Wiederholungen (z. B. ein
  Solo-Chorus identisch zu A-B-A2) müssen komplett ausgeschrieben werden. Eine
  Syntax wie `[Solo A]=A` (Formteil übernimmt Takte eines vorherigen) würde das
  vermeiden — betrifft Datenhaltung und Rendering, kein kleiner Eingriff.
