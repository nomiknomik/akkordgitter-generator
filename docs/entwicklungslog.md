# Entwicklungslog — Entscheidungen und Fehler

Chronologie der bisherigen Arbeit, damit spätere Sitzungen nicht dieselben Wege
noch einmal gehen. Ergänzt den Changelog um das **Warum**.

## Ausgangspunkt

Quelle: *Gypsy Jazz Chord eBook*, zusammengestellt von Colin Cosimini
(djangosolos.com, © 2009), Beispielstück *All Of Me*, Key of C, 32 Takte.
Aus dem PDF stammen: Gitterformat, Lagenangabe in der Ecke, Taktaufteilung über
Diagonalen, Notation (`°` vermindert, `0`/`ø` halbvermindert, `-7` Moll-Sept,
`M6` = `6`, `%` Taktwiederholung) und die kuratierten Voicings.

## Bewusste Entscheidungen

**Einzeldatei ohne Build.** `index.html` enthält HTML, CSS und JS. Läuft per
Doppelklick, als Artefakt in claude.ai und auf GitHub Pages, ohne Toolchain.
Kein Framework — der Funktionsumfang rechtfertigt keine Abhängigkeiten.

**Kein `localStorage`.** In claude.ai-Artefakten nicht erlaubt. Persistenz läuft
über JSON-Export/-Import. Das hält die Datei auch außerhalb von claude.ai lauffähig.

**Textquelle als führende Datenhaltung.** Das Textfeld ist die Wahrheit; Klicks im
Gitter schreiben dorthin zurück (`writeBack()`). Dadurch funktioniert Undo über
einen einfachen Snapshot-Stack, und die native Undo-Funktion des Textfelds bleibt nutzbar.

**Kuratierte Voicings statt Generator für die Gitarre.** Automatisch erzeugte Griffe
sind harmonisch korrekt, aber stilistisch beliebig. Die Gypsy-Formen aus dem Buch
klingen anders als „irgendein gültiger Griff". Der Generator springt nur ein, wenn
keine kuratierte Form existiert — und trägt alle anderen Instrumente.

**Analyse regelbasiert, nicht per Sprachmodell.** Deterministisch, überprüfbar,
läuft offline in der Datei. Die Grenzen stehen offen in `analyse.md`.

## Fehler und was daraus folgt

**Voicings nach Gefühl statt nach Quelle (v1.0–v1.2).**
`C6/G` und `E7/B` hatten eine Zusatznote auf der H-Saite, die im Original stumm ist;
`E7/B` war nicht als Rootless-Voicing angelegt. Aufgefallen ist das erst dem Nutzer.
→ *Lehre:* Wer eine Vorlage nachbaut, muss Punkt für Punkt vergleichen. Der
Akkordton-Check reicht nicht — das falsche `E7/B` bestand ihn fehlerfrei.
→ Daraus entstand `tools/griffbild_lesen.py`.

**Fehler beim systematischen Nachrechnen gefunden.**
Beim Prüfen *aller* Slash-Voicings fielen zusätzlich `7/4` und `m7/3` mit
akkordfremden Tönen auf — unabhängig von der gemeldeten Beanstandung.
→ *Lehre:* Wenn ein Fehler auftaucht, die ganze Kategorie prüfen, nicht nur den
gemeldeten Fall.

**Schrift zu klein (v1.2).** Beim Umstieg auf quadratische Boxen und
Container-Query-Skalierung waren die Faktoren zu vorsichtig gewählt. Der visuelle
Vergleich mit dem Original kam erst auf Hinweis des Nutzers.
→ *Lehre:* Bei Layoutänderungen einen Screenshot gegen die Vorlage halten.

**Zeilenumbruch folgte den Textzeilen (bis v1.2).** „Takte/Zeile" wirkte nur, wenn
eine Zeile *mehr* Takte enthielt. Wer vier Takte pro Zeile tippte, bekam vier
Kästchen, egal was eingestellt war.
→ Seit v1.3 bricht `parseSource()` strikt nach der Einstellung um.

**Tritonussubstitution anfangs zu großzügig erkannt.** Jede Dominante, die einen
Halbton abwärts ging, wurde so gedeutet — auch reine chromatische Rückungen.
→ Seit v1.2 nur, wenn die ersetzte Dominante oder das Ziel zur Tonart gehört;
sonst als „chromatische Rückung" ausgewiesen.

## Prüfvorgehen

Ohne Browserfenster wird so getestet:

```python
# Playwright ist in der Sandbox verfügbar
pg.goto('file:///.../index.html')
pg.evaluate("()=>state.bars.map(b=>b.chords.map(c=>c.name+'/'+c.beats))")
pg.evaluate("()=>buildBeatMap().map(s=>s?s.ch.name:'-')")
pg.evaluate("()=>bestVoicing(parseChord('C6/G'),0).frets")
```

Reine Musiklogik in Node: die Abschnitte 1–5 aus dem `<script>` schneiden,
`module.exports` anhängen, direkt aufrufen. Syntaxprüfung mit `node --check`.

Was sich **nicht** in der Sandbox prüfen ließ und offen bleibt:
- der **Klang** der Wiedergabe (keine Audioausgabe)
- das **Druckbild** auf A4 bei 8 Takten pro Zeile
- die **Live-Seite** auf GitHub Pages (github.io nicht in der Netzwerk-Freigabe;
  bestätigt wurde nur der Build-Status über die API)

## Infrastruktur

Repo `nomiknomik/akkordgitter-generator`, **öffentlich** seit v1.2.
GitHub Pages aus `main`, Pfad `/` → https://nomiknomik.github.io/akkordgitter-generator/
Gepusht wird über die REST-API (`github-push`-Skill), kein git-CLI nötig.
Nach einem Push dauert der Pages-Build etwa 15–30 Sekunden; ein zwischenzeitliches
`errored` bei `/pages/builds/latest` kann noch in `built` umschlagen — erst der
Endstand zählt.
