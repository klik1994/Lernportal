# Azubi-Prüfstand (Lernportal Kfz)

Kostenloses Lernportal für Kfz-Mechatroniker-Azubis: Eingangstest, Lernstand mit „Als Nächstes“, Themen mit Erklärung, Präsentationen, Video und Kurztest, eigener Übungstest, Prüfungscheck und Multimeter-Übung mit Fehlersuche.

## Inhalte ändern (ohne Programmieren)

1. `inhalte/Lernportal-Inhalte.xlsx` herunterladen und in Excel bearbeiten (Erklärung im Blatt „Hilfe“).
2. Auf github.com im Ordner `inhalte` auf **Add file → Upload files** klicken, die Datei mit **gleichem Namen** hineinziehen, **Commit changes**.
3. Nach 1–2 Minuten ist alles online.

## Präsentationen und eigene Videos

- Präsentationen liegen im Ordner `praesentationen` (z. B. Spannung, Strom, Widerstand mit Animationen, Lernvideo und Kurztest).
- In der Excel-Datei, Blatt „Themen“, Spalte „Präsentationen“: eine Zeile pro Präsentation im Format `Titel | praesentationen/datei.html`.
- Eigene Videos: MP4-Datei in einen Ordner hochladen (z. B. `videos/mein-video.mp4`) und den Pfad in die Spalte „Video-Link“ schreiben. YouTube-Links gehen weiterhin.

## Technik

- Reine statische Seite (HTML, CSS, JavaScript), läuft auf GitHub Pages.
- Die Excel-Datei wird direkt im Browser gelesen (`js/xlsx.js`).
- Lernstand nur im Browser des Azubis (localStorage), keine Anmeldung, kein Tracking.
- Tests: `node --test tests/*.test.js`
