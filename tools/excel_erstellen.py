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
PRAES = {'Spannung, Strom und Widerstand': 'Spannung | praesentationen/spannung.html\nStrom | praesentationen/strom.html\nWiderstand | praesentationen/widerstand.html'}
for name, text in THEMEN:
    ws.append([name, BEREICH, text, '', PRAES.get(name, '')])
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
