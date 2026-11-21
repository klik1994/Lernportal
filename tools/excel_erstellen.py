"""Erstellt inhalte/Lernportal-Inhalte.xlsx aus den Startinhalten.
Nur für die Ersteinrichtung – danach pflegt der Ausbilder die Excel-Datei selbst."""
import csv, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

ROOT = pathlib.Path(__file__).resolve().parent.parent
BEREICH = 'Elektrik-Grundlagen'
THEMEN = [
    ('Spannung, Strom und Widerstand', 'Spannung (U, Volt) ist der „Druck“, der den Strom antreibt. Strom (I, Ampere) ist die Menge an Ladung, die pro Sekunde durch den Leiter fließt – technische Stromrichtung von + nach −. Widerstand (R, Ohm) bremst den Strom.\nDamit Strom fließt, braucht es eine Spannungsquelle und einen geschlossenen Stromkreis.\nEin langes oder dünnes Kabel hat einen größeren Widerstand als ein kurzes oder dickes. Das Pkw-Bordnetz hat 12 V, Lkw meist 24 V.'),
    ('Ohmsches Gesetz und Leistung', 'U = R · I. Umgestellt: I = U / R und R = U / I.\nMerke: Bei gleicher Spannung bedeutet doppelter Widerstand halben Strom.\nLeistung P = U · I in Watt. Beispiel: Eine 55-W-Lampe an 12 V zieht etwa 4,6 A.'),
    ('Messen mit dem Multimeter', 'Schwarz immer in COM.\nSpannung misst man parallel zum Bauteil, Wahlschalter auf V⎓, Rot in VΩ.\nWiderstand nur stromlos messen, Bauteil abklemmen.\nStrom misst man in Reihe: Stromkreis auftrennen, Rot in die A-Buchse. Niemals mit Rot in der A-Buchse an eine Spannung gehen, das ist ein Kurzschluss.\n„OL“ heißt: Wert zu groß für den Messbereich. Beim manuellen Multimeter den Bereich schrittweise hochstellen – erst wenn im höchsten Bereich noch OL steht, ist es eine Unterbrechung. Ein Minuszeichen heißt: Messspitzen vertauscht.'),
    ('Reihenschaltung', 'Es gibt nur einen Stromweg. Der Strom ist überall gleich. Die Widerstände werden addiert.\nDie Spannung teilt sich auf, am größten Widerstand fällt die meiste Spannung ab.\nFällt ein Bauteil aus, ist der ganze Kreis unterbrochen.\nPraxis: Eine korrodierte Masse ist ein zusätzlicher Widerstand in Reihe. Die Lampe leuchtet dann schwächer.'),
    ('Parallelschaltung', 'An allen Zweigen liegt dieselbe Spannung. Der Gesamtstrom ist die Summe der Zweigströme.\nDer Gesamtwiderstand ist kleiner als der kleinste Einzelwiderstand.\nDarum sind die Verbraucher im Kfz parallel geschaltet: Jeder bekommt 12 V und arbeitet unabhängig. Jeder zusätzliche Verbraucher erhöht den Gesamtstrom.'),
    ('Sensoren, Aktoren und EVA-Prinzip', 'EVA-Prinzip: Eingabe – Verarbeitung – Ausgabe. Sensoren liefern die Eingabe, das Steuergerät verarbeitet, Aktoren führen aus. Wie beim Menschen: Sinnesorgan → Gehirn → Muskel.\nSensoren wandeln eine physikalische Größe (z. B. Temperatur, Druck, Drehzahl) in ein elektrisches Signal um: analog, digital oder induktiv. Aktive Sensoren haben eigene Elektronik und brauchen eine Versorgungsspannung – auch mit nur 2 Leitungen (z. B. aktiver Raddrehzahlsensor). Passive Sensoren (induktiv, NTC) kommen ohne aus. Aktive Sensoren nie mit dem Ohmmeter prüfen – die Elektronik kann beschädigt werden. NTC-Temperatursensor: wärmer → kleinerer Widerstand.\nAktoren wandeln ein elektrisches Signal in Bewegung, Wärme, Licht oder Ton um, z. B. Elektromotor, Magnetventil, Relais. Ein Relais schaltet mit kleinem Steuerstrom einen großen Laststrom. Mit PWM steuert das Steuergerät Aktoren stufenlos an: Tastverhältnis = Einschaltzeit : Periodendauer × 100 %. Das Multimeter zeigt bei PWM nur den Mittelwert – besser mit dem Oszilloskop messen.\nFehlersuche: Liegt es an E, V oder A? Erst prüfen, dann tauschen. Am Steuergerät nur LED-Prüflampe oder Oszilloskop verwenden.', 'Fahrzeugelektronik'),
    ('Motormanagement: Grundlagen', 'Das Motormanagement sorgt für Leistung, wenig Verbrauch, saubere Abgase und Motorschutz. Das Motorsteuergerät arbeitet nach dem EVA-Prinzip: Aus Drehzahl und Last liest es im Kennfeld den Grundwert ab (z. B. Einspritzzeit, Zündzeitpunkt), andere Sensoren korrigieren ihn. Fällt ein Sensor aus: Ersatzwert, Notlauf, Fehlerspeicher.\nLambda (λ) ist das Luftverhältnis. Ottomotor: 14,7 kg Luft auf 1 kg Benzin = λ 1. λ < 1 fett (Luftmangel), λ > 1 mager (Luftüberschuss). Der Ottomotor läuft meist mit λ = 1 wegen des Katalysators, der Diesel immer mit Luftüberschuss.\nBetriebszustände: Kaltstart (Anreicherung), Leerlauf (Drehzahl wird geregelt), Teillast (λ = 1), Volllast (leicht fett), Beschleunigen (kurz mehr Kraftstoff), Schub (Einspritzung aus).', 'Motormanagement'),
    ('Motormanagement: Gemischbildung Otto', 'Kraftstoffsystem: Tank → elektrische Pumpe im Tank → Filter → Rail → Einspritzventile. Saugrohreinspritzung ca. 3–5 bar. Direkteinspritzung: Hochdruckpumpe an der Nockenwelle, im Rail ca. 200–350 bar (Richtwerte). Tankentlüftung: Dämpfe aus dem Aktivkohlebehälter werden über das Tankentlüftungsventil verbrannt. Vor dem Öffnen einer Kraftstoffleitung immer Druck abbauen.\nEinspritzung: Saugrohreinspritzung spritzt vor das Einlassventil, Direkteinspritzung direkt in den Brennraum. Die Menge bestimmt das Steuergerät über die Einspritzzeit. Hochdruck-Einspritzventile werden mit ca. 65 V angesteuert – keine Prüflampe.\nLuft und Last: Erst wird die Luft erfasst (Luftmassenmesser oder Saugrohrdrucksensor), dann berechnet das Steuergerät die Kraftstoffmenge. E-Gas: Fahrpedal und Drosselklappe haben je zwei Sensoren – passen sie nicht zusammen, folgt Notlauf. Falschluft nach dem Luftmassenmesser macht das Gemisch mager.', 'Motormanagement'),
    ('Motormanagement: Zündung', 'Zündanlage: Das Steuergerät berechnet den Zündzeitpunkt, die Zündspule macht aus 12 V Hochspannung, an der Zündkerze springt der Funke über. Einschalten der Primärwicklung: Strom fließt, ein Magnetfeld baut sich auf (Schließzeit). Abschalten: Das Magnetfeld bricht zusammen, in der Sekundärwicklung (sehr viele Windungen) entsteht Hochspannung, ca. 10.000–30.000 V (Richtwert). Hochspannung – Lebensgefahr.\nZündkerze: Isolator aus Keramik, Mittel- und Masseelektrode. Elektrodenabstand und Wärmewert immer laut Hersteller. Kerzenbild rehbraun = in Ordnung. Wechseln nur bei kaltem Motor, von Hand eindrehen, Drehmoment laut Hersteller.\nZündzeitpunkt: Gezündet wird vor OT, weil die Verbrennung Zeit braucht. Mehr Drehzahl → früher zünden. Klopft ein Zylinder, zündet das Steuergerät diesen Zylinder später (Klopfregelung). Zündaussetzer gefährden den Katalysator – Fehler mit Quertausch eingrenzen.', 'Motormanagement'),
    ('Motormanagement: Dieselmanagement', 'Diesel-Grundlagen: Der Kolben verdichtet nur Luft (ca. 16 : 1 bis 20 : 1), sie wird dabei ca. 700–900 °C heiß (Richtwerte). Der eingespritzte Diesel entzündet sich von selbst. Die Leistung wird über die Kraftstoffmenge geregelt, es gibt immer Luftüberschuss (Lambda größer 1). Glühkerzen helfen beim Kaltstart (Vorglühen, Nachglühen). Niedervolt-Glühkerzen nie direkt an 12 V anschließen.\nCommon-Rail: Vorförderpumpe → Filter → Hochdruckpumpe → Rail → Injektoren. Raildruck bis über 2.000 bar (Richtwert). Vor-, Haupt- und Nacheinspritzung. Hochdruck – Verletzungsgefahr, absolute Sauberkeit. Prüfen: Raildruck Soll/Ist, Mengenabgleich, Rücklaufmenge.\nTurbo und AGR: Das Abgas treibt die Turbine, der Verdichter drückt mehr Luft in den Motor, der Ladeluftkühler kühlt sie. Die Abgasrückführung senkt die Stickoxide – zu viel AGR macht Ruß.', 'Motormanagement'),
    ('Motormanagement: Abgas', 'Schadstoffe im Abgas: CO (Kohlenmonoxid), HC (unverbrannter Kraftstoff), NOx (Stickoxide) und Ruß. Kohlenmonoxid ist unsichtbar und tödlich – Motor in der Werkstatt nur mit Abgasabsaugung laufen lassen.\nLambdasonde: Die Sonde vor dem Kat regelt das Gemisch, die Sonde nach dem Kat überwacht den Kat. Sprungsonde: mager ca. 0,1 V, fett ca. 0,8–0,9 V. Die Breitbandsonde misst den genauen Lambda-Wert. Korrekturwerte nahe 0 % sind gut (Richtwerte).\nKatalysator: Der Dreiwege-Kat wandelt CO, HC und NOx um – aber nur bei Lambda = 1 und erst ab ca. 250 °C (Richtwert). Zündaussetzer zerstören den Kat.\nDiesel: Oxidations-Kat → Partikelfilter (DPF) → AdBlue-Einspritzung → SCR-Kat. Der DPF sammelt Ruß, bei der Regeneration wird er verbrannt. AdBlue wandelt Stickoxide in Stickstoff und Wasser um.', 'Motormanagement'),
]
KOPF = Font(bold=True, color='FFFFFF')
FUELL = PatternFill('solid', fgColor='1A5FB4')
WRAP = Alignment(wrap_text=True, vertical='top')

def kopf(ws, spalten, breiten):
    ws.append(spalten)
    for i, b in enumerate(breiten):
        c = ws.cell(row=1, column=i + 1)
        c.font, c.fill = KOPF, FUELL
        ws.column_dimensions[c.column_letter].width = b
    ws.freeze_panes = 'A2'

wb = Workbook()
ws = wb.active
ws.title = 'Themen'
kopf(ws, ['Thema', 'Bereich', 'Erklärung', 'Video-Link', 'Präsentationen'], [32, 22, 90, 40, 48])
PRAES = {'Spannung, Strom und Widerstand': 'Spannung | praesentationen/spannung.html\nStrom | praesentationen/strom.html\nWiderstand | praesentationen/widerstand.html',
         'Sensoren, Aktoren und EVA-Prinzip': 'EVA-Prinzip | praesentationen/eva.html\nSensoren | praesentationen/sensoren.html\nAktoren | praesentationen/aktoren.html',
         'Motormanagement: Grundlagen': 'Aufgaben und Steuergerät | praesentationen/mm-aufgaben.html\nLuftverhältnis Lambda | praesentationen/mm-lambda.html\nBetriebszustände | praesentationen/mm-betrieb.html',
         'Motormanagement: Gemischbildung Otto': 'Kraftstoffsystem | praesentationen/mm-kraftstoff.html\nEinspritzung | praesentationen/mm-einspritzung.html\nLuft und Last | praesentationen/mm-luft.html',
         'Motormanagement: Zündung': 'Zündanlage | praesentationen/mm-zuendanlage.html\nZündkerze | praesentationen/mm-zuendkerze.html\nZündzeitpunkt | praesentationen/mm-zuendzeitpunkt.html',
         'Motormanagement: Dieselmanagement': 'Diesel-Grundlagen | praesentationen/mm-diesel-grundlagen.html\nCommon-Rail | praesentationen/mm-common-rail.html\nTurbo und AGR | praesentationen/mm-diesel-turbo.html',
         'Motormanagement: Abgas': 'Lambdasonde | praesentationen/mm-abgas-lambda.html\nKatalysator | praesentationen/mm-abgas-kat.html\nDPF und AdBlue | praesentationen/mm-abgas-dpf.html'}
for eintrag in THEMEN:
    name, text = eintrag[0], eintrag[1]
    bereich = eintrag[2] if len(eintrag) > 2 else BEREICH
    ws.append([name, bereich, text, '', PRAES.get(name, '')])
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment = WRAP

wf = wb.create_sheet('Fragen')
kopf(wf, ['Thema', 'Frage', 'Antwort A', 'Antwort B', 'Antwort C', 'Antwort D', 'Richtig', 'Erklärung'], [28, 50, 28, 28, 28, 28, 9, 60])
with open(ROOT / 'tools' / 'fragen-start.csv', encoding='utf-8') as f:
    for i, r in enumerate(csv.reader(f)):
        if i: wf.append(r)
for row in wf.iter_rows(min_row=2):
    for c in row: c.alignment = WRAP

we = wb.create_sheet('Einstellungen')
kopf(we, ['Einstellung', 'Wert'], [28, 60])
for k, v in [('Portal-Name', 'Lernportal Kfz'), ('Impressum Name', ''), ('Impressum Anschrift', ''), ('Impressum E-Mail', ''), ('Impressum Telefon (freiwillig)', '')]:
    we.append([k, v])

ws_h = wb.create_sheet('Hilfe')
ws_h.column_dimensions['A'].width = 110
for zeile in [
    'So pflegst du die Inhalte',
    'Blatt „Themen“: eine Zeile pro Thema. Neue Zeile = neues Thema im Portal. Zeilenumbruch in der Erklärung: Alt + Enter.',
    'Video-Link: den normalen YouTube-Link einfügen (Video auf „Nicht gelistet“ stellen) – oder ein eigenes Video, das du in den Ordner „videos“ hochgeladen hast, z. B. videos/mein-video.mp4. Leer lassen, wenn es kein Video gibt.',
    'Präsentationen: eine Präsentation pro Zeile im Format „Titel | Link“, z. B. „Spannung | praesentationen/spannung.html“. Mehrere Zeilen mit Alt + Enter. Leer lassen, wenn es keine gibt.',
    'Blatt „Fragen“: eine Zeile pro Frage. Der Name in der Spalte „Thema“ muss genau so geschrieben sein wie im Blatt „Themen“.',
    'Spalte „Richtig“: Buchstabe der richtigen Antwort (A, B, C oder D). Für Ja/Nein-Fragen Antwort C und D leer lassen.',
    'Pro Thema mindestens 5 Fragen, weil der Kurztest 5 Fragen hat.',
    'Blatt „Einstellungen“: Name des Portals und deine Angaben für das Impressum.',
    'Erste Zeile der Blätter und die Blattnamen nicht ändern.',
    'Danach die Datei auf github.com im Ordner „inhalte“ hochladen (gleicher Dateiname). Nach 1–2 Minuten ist alles online.',
]:
    ws_h.append([zeile])
ws_h['A1'].font = Font(bold=True, size=14)

(ROOT / 'inhalte').mkdir(exist_ok=True)
wb.save(ROOT / 'inhalte' / 'Lernportal-Inhalte.xlsx')
print('ok')
