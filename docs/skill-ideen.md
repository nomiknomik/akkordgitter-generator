# Skill-Ideen aus diesem Projekt

Bewertung aus Sicht des bisherigen Verlaufs: Was lohnt sich als eigenständiger,
wiederverwendbarer Skill — und was nicht.

**Maßstab:** Ein Skill lohnt sich, wenn die Aufgabe *wiederkehrt*, das *Vorgehen
nicht offensichtlich* ist (Claude würde es sonst jedes Mal neu und schlechter
erfinden) und das Ergebnis *überprüfbar* ist. Was nur einmal läuft, ist ein Skript.

---

## Empfohlen

### 1. `griffbild-extraktion` — klare Empfehlung

**Warum:** Die Methode ist nicht offensichtlich. Ohne Anleitung würde man beim
nächsten Mal wieder versuchen, den PDF-Textlayer auszulesen (liefert nichts) oder
das Bild „anzuschauen und abzutippen" (fehleranfällig — genau so sind die Fehler in
v1.2 entstanden). Der erprobte Weg über Spalten-/Zeilensummen und Connected
Components steht sonst nirgends.

**Inhalt:**
- `tools/griffbild_lesen.py` und `tools/voicing_pruefen.py` als Skript-Beilage
- Ablauf inklusive der Fallstricke: zu enger Ausschnitt schneidet Saiten ab;
  die Lagenziffer steht neben *ihrer* Bundzeile, nicht zwingend neben der obersten;
  Rootless-Voicings sind kein Fehler
- die Doppelprüfung: Töne rechnen **und** Bild vergleichen

**Auslöser:** „Griffe aus dem PDF übernehmen", „Chord-Diagramme auslesen",
„Akkordbibliothek erweitern", Upload eines Griffbild-Screenshots.

**Nutzen außerhalb dieses Projekts:** ja — jedes Songbook, jede Akkordtabelle.

### 2. `harmonische-analyse` — empfohlen, wenn öfter gebraucht

**Warum:** Das Regelwerk in `analyse.md` ist durchdacht und deterministisch.
Als Skill wäre es unabhängig von der App nutzbar („analysiere diese Akkordfolge").

**Inhalt:** Regelreihenfolge aus `analyse.md`, die Fallunterscheidung
Tritonussubstitution vs. chromatische Rückung (die beim ersten Anlauf falsch war),
und die dokumentierten Grenzen — vor allem: **die Tonart wird nicht erkannt, sie
muss angegeben werden.**

**Vorbehalt:** Nur bauen, wenn das wirklich wiederkehrt. Sonst reicht die App.

---

## Eher nicht eigenständig

### `akkord-voicing-pruefung`
Zu klein für einen eigenen Skill — sinnvoller als Bestandteil von
`griffbild-extraktion`. Das Skript allein ist selbsterklärend.

### `akkordgitter-app-entwicklung`
Projektwissen, kein Skill. Gehört in `CLAUDE.md` (steht dort auch), weil es nur
für genau dieses Repo gilt. Ein Skill sollte projektunabhängig sein.

### `pptx`-artige Chart-Erzeugung
Die App macht das bereits interaktiv und besser, als ein Skill es blind könnte.

---

## Hinweise für den Bau

Beim Erstellen greift `/skill-creator` zusammen mit `skill-creator-add`:
Versionsnummer gehört ins `description`-Feld, Changelog wird ausgelagert, nach
jeder inhaltlichen Änderung wird automatisch eine `.skill`-Datei gepackt.

Die Beschreibung sollte die Auslöser breit fassen (deutsch **und** englisch, plus
typische Umschreibungen), damit der Skill zuverlässig triggert — so wie bei den
bestehenden Skills im Bestand.

Vor dem Bau sinnvoll: an einem **zweiten** PDF prüfen, ob
`tools/griffbild_lesen.py` auch dort trägt. Bisher ist es nur gegen ein einziges
Buch verifiziert; Layout-Annahmen (Punktgröße, Linienstärke, Lagenziffer links)
könnten anderswo abweichen. Erst danach lohnt sich das Festschreiben als Skill.
