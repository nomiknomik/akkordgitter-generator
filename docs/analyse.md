# Harmonische Analyse

Der Schalter „Analyse“ blendet unter den Griffbildern eine automatische Deutung
der Akkordfolge ein (`analyzeChart()`, Abschnitt 4b). Sie ist regelbasiert und
deterministisch — kein Sprachmodell, keine Erfindungen.

## Vorverarbeitung

Wiederholungstakte (`%`) und unmittelbar wiederholte Akkorde werden zu einer
Sequenz zusammengefasst; analysiert werden also **Akkordwechsel**, nicht Takte.

## Regeln in Reihenfolge der Auswertung

| Erkennung | Bedingung |
|---|---|
| **Quintfallkette** | ≥ 3 Dominanten, deren Grundton jeweils eine Quinte fällt |
| **ii–V(–I)** | Mollseptakkord + Dominante eine Quarte darüber, optional Auflösung |
| **Tritonussubstitution** | Dominante, deren Nachfolger einen Halbton tiefer liegt — nur wenn die ersetzte Dominante oder das Ziel zur Tonart gehört |
| **Chromatische Rückung** | dieselbe Konstellation ohne Tonartbezug: halbtonweise rutschende Dominanten |
| **Zwischendominante** | Dominante auf fremder Stufe, deren Quintfallziel eine Leiterstufe ist; vermerkt, ob sie sich auflöst |
| **Verminderter Akkord** | Beziehung zum Folgeakkord: Leitton von unten (= V7♭9 ohne Grundton), chromatischer Durchgang von oben, gehaltener Grundton, sonst Wechselklang |
| **Modal Interchange** | leiterfremd, aber ♭III / iv / ♭VI / ♭VII → aus der Paralleltonart entlehnt |
| **Schluss** | letzte zwei Akkorde: authentisch (V→I), plagal (IV→I), Backdoor (♭VII7→I), Halbschluss |

Zusätzlich: Stufenfolge je Formteil und eine Kennzahl, wie viele Akkordwechsel
leiterfremd sind.

## Grenzen

- Die Tonart wird **nicht** automatisch erkannt, sondern aus dem Kopfbereich übernommen.
  Bei falscher Tonartangabe ist die gesamte Deutung falsch.
- Modulationen innerhalb des Stücks werden nicht als solche erkannt; sie erscheinen
  als Häufung leiterfremder Akkorde.
- Enharmonik wird nach Halbtönen gerechnet, nicht nach Notation: `C#7` und `Db7`
  sind für die Analyse derselbe Akkord.
- Melodie und Stimmführung fließen nicht ein — die Deutung beruht ausschließlich
  auf der Akkordfolge.

## Erweitern

Neue Regel = ein weiterer Block in `analyzeChart()` mit
`add(tag, takte, text)` und Setzen von `covered[i]`, damit der Akkord nicht
zusätzlich als „leiterfremd“ gemeldet wird.
