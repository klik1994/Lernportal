# Lernvideo-Werkzeug

Zeichnet die Lernvideos zu den Präsentationen (Python + Pillow + ffmpeg, Schrift Inter).

- `engine.py` – Zeichenfunktionen (Text, Karten, Batterie, Lampe, Multimeter, Messleitungen) und Rendern
- `scenes.py` – wiederverwendbare Szenen (Titel, Werte-Liste, Merke, Stromkreis)
- `videos.py` – die Videos; neues Thema = neuer Eintrag in `VIDEOS`

Aufruf aus dem Hauptordner: `python3 tools/video/videos.py strom stills` zum Prüfen, dann `python3 tools/video/videos.py strom`.
Regeln: technische Stromrichtung (+ → −), kein Sprecher, Texteinblendungen, ca. 1 Minute.
