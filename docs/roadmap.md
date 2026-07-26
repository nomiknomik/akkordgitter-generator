# Geplante Arbeitspakete

Stand v1.3. Die drei folgenden Vorhaben sind angekündigt, aber noch nicht begonnen.
Jedes ist so beschrieben, dass ein neuer Chat direkt loslegen kann.

---

## 1. Weitere Akkorde aus einem anderen PDF in die Datenbank

**Ziel:** Die Griffbibliothek um Voicings aus einer weiteren Quelle erweitern.

**Vorgehen:** [`pdf-extraktion.md`](pdf-extraktion.md) Schritt für Schritt.
Kurzfassung: Ausschnitt bestimmen → `tools/griffbild_lesen.py` → 
`tools/voicing_pruefen.py` → Sichtprüfung → `SHAPES` ergänzen.

**Zu klärende Entwurfsfrage:** Die Bibliothek kennt bisher **eine** Quelle. Kommen
Voicings aus einem zweiten Buch dazu, stellt sich die Frage, ob sie
- einfach als weitere Lage-Variante an dieselbe Qualität gehängt werden
  (einfach, aber die Herkunft geht verloren), oder
- ein Feld `q:'quelle'` je Shape bekommen und die App einen Filter „nur Voicings aus
  Buch X" erhält (sauberer, etwas mehr Aufwand).

Empfehlung: das Feld `q` gleich mitschreiben, auch wenn der Filter erst später kommt.
Rückwirkend lässt sich die Herkunft nicht mehr rekonstruieren.

**Nicht vergessen:**
- Bei neuen Akkordqualitäten sind **fünf** Stellen zu pflegen: `SHAPES`, `QMAP`,
  `QSHORT`, `QFAMILY`, `CHORD_TONES` + `ESSENTIAL`.
- `TONE`/`WESENTLICH` in `tools/voicing_pruefen.py` spiegeln `CHORD_TONES`/`ESSENTIAL`
  aus `index.html`. Beide Stellen synchron halten.

---

## 2. Neuen Song oder andere Interpretation übernehmen

**Ziel:** Weitere Charts unter `charts/`, ggf. mehrere Fassungen desselben Stücks.

**Vorgehen:** [`pdf-extraktion.md`](pdf-extraktion.md), Abschnitt „Ablauf: neuen Song
übernehmen". Akkordfolge abtippen, Taktaufteilung über Beat-Suffixe abbilden,
als JSON exportieren.

**Mögliche Ausbaustufe:** Die App lädt Charts derzeit nur per Datei-Dialog. Ein
Auswahlmenü, das die Dateien aus `charts/` direkt anbietet, wäre der nächste
sinnvolle Schritt — auf GitHub Pages ginge das per `fetch()` auf ein
`charts/index.json` mit der Dateiliste.

---

## 3. Skills aus diesem Projekt ableiten

Was sich aus dem bisherigen Verlauf als eigenständiger, wiederverwendbarer Skill
lohnt — nach erwartetem Nutzen sortiert. Details und Begründung in
[`skill-ideen.md`](skill-ideen.md).

1. **`griffbild-extraktion`** — Griffbilder aus PDF/Bild auslesen und verifizieren.
   Das ist die klarste Kandidatin: abgeschlossene Aufgabe, erprobte Werkzeuge,
   nicht-offensichtliche Methode, außerhalb dieses Projekts nutzbar.
2. **`akkord-voicing-pruefung`** — Voicings gegen Akkordtöne rechnen. Klein; ginge
   auch als Teil von (1) statt eigenständig.
3. **`harmonische-analyse`** — Stufenanalyse einer Akkordfolge in Textform.
   Nutzen unabhängig von der App, Regelwerk steht in `analyse.md`.

Vor dem Bau jeweils prüfen, ob der Skill wirklich wiederkehrend gebraucht wird —
ein Skill, der einmal läuft, ist ein Skript, kein Skill.

---

## Kleinere offene Punkte

- **Transponieren**: Tonart wechseln → Akkorde mitziehen. Nicht implementiert.
- **Automatische Tonarterkennung** als Vorschlag für den Kopfbereich.
- **La Pompe**: derzeit schlägt die Wiedergabe stur jeden Beat an. Ein echter
  Gypsy-Rhythmus (kurz-lang, Betonung 2 und 4) wäre hörbar besser.
- **Lagenwahl nach Griffnähe**: aktuell wird die tiefste spielbare Lage gewählt,
  ohne den Vorgängerakkord zu berücksichtigen.
- **Songbook-PDF** über mehrere Charts.
- **Druckbild**: bei 8 Takten/Zeile noch nicht auf A4 gegengeprüft.
