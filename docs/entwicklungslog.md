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

## Solo-Chorus und Tag nachträglich ergänzt (v1.10)

Die erste Fassung des Holovaty-Charts deckte nur den ersten Durchgang plus ein
angehängtes `[Tag]` ab (38 Takte) — die PDF hat aber 68 Takte: nach dem ersten
Durchgang folgt ein vollständiger Solo-Chorus, danach erst das Tag.

**Vorgehen:** Text- statt Vektor-Extraktion für die Akkordfolge (nicht die
Griffbilder). `pdftotext -layout` lieferte für die Solo-Seiten stark verschachtelten,
schwer zuordenbaren Text (Fingersatz- und Taktzahlen vermischt); verlässlich war
erst der Abgleich gegen die rasterisierten Seiten (`pdftoppm`, visuell Takt für
Takt gegen die bekannte Form A-B-A2-C geprüft, wie in `pdf-extraktion.md`
für Griffbilder empfohlen — dasselbe Prinzip gilt für Akkordfolgen).

**Ergebnis:** Solo-Chorus ist akkordgleich mit dem ersten Durchgang (A/B/A2),
nur die zweite Hälfte von C fehlt — dort mündet die Aufnahme direkt in ein
erweitertes Tag (D7–G7 als zusätzlicher Turnaround vor dem eigentlichen
E7–A7–D7–G7–C6/9). Das ursprüngliche `[Tag]` nach dem ersten Durchgang gibt es
in der Aufnahme so nicht — es war eine verkürzte Referenzfassung, kein
tatsächlicher Bestandteil der Form. Entfernt, um Chart und Aufnahme deckungsgleich
zu halten.

**Benennung.** Erst `[Solo]`/`[SoloB]`/`[SoloA2]`/`[SoloC]` benutzt — das
verschleiert, dass z. B. `[SoloB]` exakt `[B]` ist. Umbenannt zu
`[Solo A]`/`[Solo B]`/`[Solo A2]`/`[Solo C]`. Geprüft, ob die App Formteile
referenzieren kann (`parseSource()`, Zeile ~583): nein — `[...]`-Marken sind
reine Anzeigetexte ohne Verweis-Mechanismus, jeder Takt muss ausgeschrieben
werden. Echte Deduplizierung bräuchte neue Syntax (z. B. `[Solo A]=A`) — siehe
`docs/roadmap.md`.

→ *Lehre:* Bei mehrteiligen PDFs (Melodie + Solo + Tag) zuerst die volle
Taktzahl aus `pdfinfo`/Blattzahl gegen die im Chart erfasste Taktzahl prüfen,
bevor eine Extraktion als vollständig gilt.

## Geschwindigkeitsregler im Video-Sync (v1.11)

Wunsch: YouTube-Video zum Üben verlangsamen können, notfalls mit Angabe der
tatsächlich eingestellten Rate, damit die Sync-Zeiten stimmen.

**Prüfung ergab: keine Anpassung nötig.** `barTime()`/`recalc()` bilden
Taktnummer → *Videoposition* ab (`player.getCurrentTime()`), nicht → Echtzeit.
`getCurrentTime()` ist die Position im Medium selbst und läuft unabhängig von
der Wiedergaberate immer korrekt mit — ob per `setPlaybackRate()` oder über
das YouTube-eigene Zahnrad geändert. Die Kalibrierung (Bezugspunkte, Steigung,
Achsenabschnitt) bleibt bei jeder Rate identisch gültig.

**Umsetzung:** nur ein Bedienelement (`f-rate`, ruft `setPlaybackRate()`) plus
Rückkanal (`onPlaybackRateChange`), falls YouTube einen Wunschwert wie 0.85
nicht übernimmt und die Person stattdessen das eigene Zahnrad benutzt — dann
zieht die App den tatsächlichen Wert nur zur Anzeige nach, ohne Neuberechnung.

→ *Lehre:* Vor einer Rechen-Erweiterung erst prüfen, in welcher Einheit
(Zeit vs. Position) die bestehende Kalibrierung überhaupt rechnet — das erspart
hier eine ganze Interpolationsschicht, die der Wunsch zunächst nahelegte.
