# Eingabesyntax

Eine Zeile im Textfeld = ein System (Notenzeile). Enthält eine Zeile mehr Takte
als unter „Takte/Zeile“ eingestellt, wird automatisch umgebrochen.

## Takte und Struktur

| Zeichen | Bedeutung |
|---|---|
| `\|` | Taktstrich (trennt Takte) |
| `%` oder `/` | Takt wiederholen (übernimmt Akkorde des Vortakts, auch für die Wiedergabe) |
| `[A]`, `[B]`, `[Kopf]` | Formteil-Marke in eigener Zeile |
| Leerzeile | wird ignoriert |

## Akkorde

| Schreibweise | Bedeutung |
|---|---|
| `C`, `Cm`, `C-` | Dur / Moll |
| `C6`, `CM6` | Sextakkord |
| `C6/9` | Sext-None (die `9` nach dem Slash ist keine Bassnote) |
| `Cmaj7`, `CM7` | große Septime |
| `C7`, `C9`, `C11`, `C13` | Dominantformen |
| `C7b5`, `C7b9`, `C7#9` | alterierte Dominanten |
| `C7+`, `C7#5`, `C+` | übermäßig |
| `C-7`, `Cm7`, `C-9` | Moll-Sept/None |
| `C-6`, `Cm6` | Moll-Sext |
| `C°`, `Co`, `Cdim` | vermindert |
| `C0`, `Cø`, `Cm7b5` | halbvermindert |
| `C6/G` | Bassnote (nach dem Slash steht ein Notenname) |

## Suffixe

| Suffix | Bedeutung | Beispiel |
|---|---|---|
| `@n` | Lage erzwingen — Ankerton in Bund n | `C6@8` |
| `:n` | Dauer in Beats (steuert Taktaufteilung **und** Wiedergabe) | `C6:2` |

Beides kombinierbar: `C6@8:2`.

## Taktaufteilung

Mehrere Akkorde in einem Takt werden durch **Leerzeichen** getrennt:

```
C6 Bb7            -> 2 + 2 Beats  (Diagonale)
C6:1 Bb7:1 A7:2   -> 1 + 1 + 2    (Diagonale + Linie oben links)
C6:2 Bb7:1 A7:1   -> 2 + 1 + 1    (Diagonale + Linie unten rechts)
C6 Bb7 A7 D7      -> 1+1+1+1      (Andreaskreuz)
```

Ohne `:n` verteilt die App die Beats automatisch (bei 4/4 und drei Akkorden: 2 + 1 + 1).

## Nur ein Schlag im Takt

| Präfix | Bedeutung |
|---|---|
| `>C6` | nur den **1. Beat** des Taktes spielen |
| `<C6` | nur den **letzten Beat** des Taktes spielen |

## Beispiel

```
[A]
 C6/G | % | E7/B | %
 A7 | % | B0 | %
[B]
 C6 Bb7 | A7 | D7 | C#7
 C6/9 Eb7 | D-9 C#7 | >C6 | %
```
