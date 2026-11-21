"""Hochvolt im Kfz – fünf Präsentationen nach DGUV Information 209-093 (Ausgabe 08/2021).
Aufruf: cd tools && python3 hochvolt.py"""
from praesentation_bauen import *

THEMA = 'Hochvolt im Kfz'
K = 'HOCHVOLT IM KFZ · DGUV INFORMATION 209-093'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'
QUELLE = '<div class="note step">Quelle: DGUV Information 209-093 „Qualifizierung für Arbeiten an Fahrzeugen mit Hochvoltsystemen“ (Ausgabe 08/2021). Herstellervorgaben beachten.</div>'
HINWEIS = '''    <div class="warn step"><b>Wichtig</b>Diese Präsentation ersetzt keine Qualifizierung und keine Unterweisung. Wer was am Hochvoltsystem darf, legt dein Betrieb fest – auf Grundlage der DGUV Information 209-093 und der Gefährdungsbeurteilung.</div>'''
ORA = '#ff8f3f'

# ---------------------------------------------------------------- 1 Grundlagen und Gefahren
T = 'HV-GRUNDLAGEN'
SYS = [('12-V-Bordnetz', '12 V DC', 0, 'Kein Hochvolt. Das ist das normale Bordnetz – Arbeiten wie gewohnt.'),
       ('48-V-Mildhybrid', '48 V DC', 0, 'Kein Hochvolt – unter 60 V DC. Trotzdem: Herstellervorgaben beachten, hohe Ströme und Kurzschlussgefahr.'),
       ('Hybrid / E-Auto', 'ca. 400 V DC', 1, 'Hochvolt! Über 60 V DC. Arbeiten am HV-System nur mit Qualifizierung nach DGUV 209-093.'),
       ('E-Auto mit 800-V-Technik', 'ca. 800 V DC', 1, 'Hochvolt! Über 60 V DC. Lebensgefahr bei Berührung – Hände weg von orange.')]
grundlagen = [
    titel_folie(K, 'HV', 'Hochvolt-Grundlagen', 'Was Hochvolt ist und warum es gefährlich ist', 'font-size:84px'),
    lernziele(T, ['Ab wann eine Spannung im Fahrzeug als Hochvolt gilt', 'Welche Gefahren vom Hochvoltsystem ausgehen',
                  'Woran du Hochvolt-Bauteile erkennst', 'Die wichtigste Regel: Hände weg von orange']),
    folie(T, 'Was ist Hochvolt?', '''    <div class="values">
      <div class="val step from-left"><b>über 60 V</b><span>Gleichspannung (DC) – bis 1.500 V</span></div>
      <div class="val step from-left"><b>über 30 V</b><span>Wechselspannung (AC) – bis 1.000 V</span></div>
    </div>
    <div class="tip step" style="margin-top:14px"><b>Zum Vergleich</b>Das normale Bordnetz hat 12 V. Hochvoltsysteme in E-Autos arbeiten heute meist mit rund 400 V oder 800 V Gleichspannung.</div>
''' + QUELLE),
    folie(T, 'Hochvolt oder nicht? – zum Ausprobieren', '''    <div class="choice" style="margin-bottom:12px;flex-wrap:wrap">''' + ''.join(f'<button class="btn ghost" data-s="{i}">{n}</button>' for i, (n, v, h, t) in enumerate(SYS)) + '''</div>
    <div class="grid2" style="align-items:center">
      <div class="card" style="text-align:center"><div class="muted" style="font-size:15px;font-weight:800">SYSTEMSPANNUNG</div><div id="hs-v" style="font-size:46px;font-weight:900;margin:6px 0">—</div><div id="hs-b" style="display:inline-block;padding:8px 18px;border-radius:999px;font-weight:900;font-size:20px"></div></div>
      <div class="card" id="hs-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Richtwerte – die genaue Spannung steht in den Herstellerunterlagen.</p>''', sid='s-hs', body_cls='body noclick'),
    folie(T, 'Die Gefahren', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Elektrischer Schlag</b>Strom durch den Körper: Herzkammerflimmern, Verbrennungen – Lebensgefahr.</div>
      <div class="warn step"><b>Störlichtbogen</b>Bei einem Kurzschluss entsteht ein Lichtbogen mit großer Hitze und grellem Licht – Verbrennungen, Augenschäden.</div>
      <div class="warn step"><b>Brand und Hitze</b>Eine beschädigte Batterie kann sich stark erhitzen und brennen – auch noch Stunden oder Tage später.</div>
      <div class="warn step"><b>Austretende Stoffe</b>Aus beschädigten Batterien können gefährliche Stoffe austreten – nicht berühren, nicht einatmen.</div>
    </div>
    <div class="tip step" style="margin-top:12px"><b>Restladung</b>Auch nach dem Abschalten kann noch Spannung anliegen, z. B. in Kondensatoren der Leistungselektronik.</div>'''),
    folie(T, 'So erkennst du Hochvolt-Bauteile', '''    <div class="grid2" style="align-items:center">
      <div class="card step" style="text-align:center">
        <svg viewBox="0 0 260 200" width="240" height="185" style="display:block;margin:0 auto" class="dev">
          <path d="M130 14 L246 186 H14 Z" fill="#ffd34d" stroke="#1a1a1a" stroke-width="8" stroke-linejoin="round"/>
          <path d="M140 60 L104 124 H132 L116 172 L162 104 H132 Z" fill="#1a1a1a"/>
        </svg>
        <div style="font-weight:800;margin-top:6px">Warnzeichen „Elektrische Spannung“</div></div>
      <ul class="step" UL>
        <li><b>Orange Leitungen</b> und Stecker – das ist Hochvolt</li>
        <li><b>Warnaufkleber</b> an Batterie, Leistungselektronik und anderen HV-Bauteilen</li>
        <li>In der Werkstatt: <b>Schild am Fahrzeug</b> zeigt den Zustand des HV-Systems</li>
      </ul>
    </div>
    <div class="warn step" style="margin-top:12px"><b>Hände weg von orange!</b>Orange Leitungen und gekennzeichnete Bauteile nur anfassen, wenn du dafür qualifiziert und beauftragt bist.</div>'''.replace('UL', UL)),
    folie(T, 'Wichtig für dich', HINWEIS + '''
    <div class="tip step" style="margin-top:12px"><b>Im Zweifel</b>Nichts anfassen, Arbeitsplatz verlassen und die Fachkundige Person Hochvolt (FHV) oder deinen Ausbilder fragen.</div>'''),
    video(T, 'hv-grundlagen'),
    kurztest(T, [
        ('Ab welcher Gleichspannung spricht man im Fahrzeug von Hochvolt?', ['Über 12 V', 'Über 60 V', 'Über 230 V'], 1, 'Hochvolt: über 60 V DC (bis 1.500 V) bzw. über 30 V AC (bis 1.000 V).'),
        ('Ist ein 48-V-Mildhybrid ein Hochvoltsystem?', ['Nein, 48 V DC liegt unter 60 V', 'Ja, immer', 'Nur beim Laden'], 0, 'Hochvolt beginnt erst über 60 V DC.'),
        ('Welche Farbe haben Hochvoltleitungen?', ['Rot', 'Blau', 'Orange'], 2, 'Darum gilt: Hände weg von orange!'),
        ('Warum kann nach dem Abschalten noch Spannung anliegen?', ['Durch Restladungen, z. B. in Kondensatoren', 'Weil die 12-V-Batterie nachlädt', 'Das ist nicht möglich'], 0, 'Darum gibt es Wartezeiten und die Spannungsprüfung.'),
    ]),
    merke(T, ['Hochvolt: über 60 V DC oder über 30 V AC', 'Gefahren: Schlag, Lichtbogen, Brand, Stoffe',
              'Orange = Hochvolt – Hände weg!', 'Im Zweifel: FHV oder Ausbilder fragen']),
]
grundlagen_js = '''<script>
(function () {
  const S = ''' + str([[v, h, t] for n, v, h, t in SYS]).replace("'", '"') + ''';
  const bt = document.querySelectorAll('#s-hs [data-s]');
  function s(i) {
    const [v, h, t] = S[i];
    document.getElementById('hs-v').textContent = v;
    const b = document.getElementById('hs-b');
    b.textContent = h ? 'HOCHVOLT' : 'kein Hochvolt';
    b.style.background = h ? '#ff8f3f' : 'var(--card2)'; b.style.color = h ? '#1a1a1a' : 'var(--txt)';
    document.getElementById('hs-t').innerHTML = t;
    bt.forEach(x => x.classList.toggle('on', +x.dataset.s === i));
  }
  bt.forEach(x => x.onclick = () => s(+x.dataset.s)); s(0);
})();
</script>'''

# ---------------------------------------------------------------- 2 Aufbau des E-Autos
T = 'AUFBAU'
KOMP = [
    ('bat', 'HV-Batterie', 'Speichert die Energie. Viele Lithium-Ionen-Zellen, zu Modulen zusammengefasst. Ein Batteriemanagement überwacht Spannung und Temperatur. Schütze (Schalter) verbinden die Batterie mit dem Fahrzeug.'),
    ('le', 'Leistungselektronik', 'Der Wechselrichter macht aus der Gleichspannung der Batterie Drehstrom für die E-Maschine – und regelt so Drehzahl und Kraft. Achtung: Kondensatoren können Restladung haben.'),
    ('em', 'E-Maschine', 'Treibt das Fahrzeug an. Beim Bremsen arbeitet sie als Generator und lädt die Batterie wieder auf (Rekuperation).'),
    ('dc', 'DC/DC-Wandler', 'Macht aus der Hochvoltspannung 12 V für das normale Bordnetz – er ersetzt die Lichtmaschine.'),
    ('ol', 'Ladegerät (On-Board)', 'Beim Laden an Wechselstrom (AC) macht es aus Wechselspannung Gleichspannung für die Batterie. Beim Schnellladen (DC) liefert die Ladesäule direkt Gleichspannung.'),
    ('nv', 'Klima / Heizung', 'Elektrischer Klimakompressor und Hochvolt-Heizung hängen ebenfalls am Hochvoltsystem – auch sie haben orange Leitungen.'),
    ('dose', 'Ladedose', 'Hier wird das Ladekabel angeschlossen – für Wechselstrom (AC) und oft auch für Gleichstrom (DC).'),
    ('bn', '12-V-Bordnetz', 'Licht, Steuergeräte, Radio und Co. laufen weiter mit 12 V. Auch E-Autos haben eine 12-V-Batterie.'),
]
def blockbild(px):
    O = ORA
    def box(k, x, y, w, h, lab, fs=28):
        ls = lab.split('|')
        tx = ''.join(f'<text x="{x + w / 2}" y="{y + h / 2 + fs * 0.36 + (j - (len(ls) - 1) / 2) * fs * 1.05}" text-anchor="middle" font-size="{fs}" font-weight="900" fill="#ecf1f8">{l}</text>' for j, l in enumerate(ls))
        return (f'<g class="{px}-bx" data-k="{k}" style="transition:opacity .3s"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#18283f" stroke="{O}" stroke-width="6"/>{tx}</g>')
    ln = lambda g, d: (f'<path class="{px}-ln" data-g="{g}" d="{d}" fill="none" stroke="{O}" stroke-width="10" stroke-linecap="round" style="transition:opacity .3s"/>')
    out = [f'<svg viewBox="0 10 1000 380" width="1000" height="380" style="display:block;margin:0 auto;max-width:100%;height:auto" id="{px}-svg">',
      '<path d="M20 300 Q30 180 180 165 L320 70 H650 L810 160 Q970 175 980 300 Z" fill="#213552" stroke="#94a4ba" stroke-width="4"/>',
      '<circle cx="200" cy="318" r="50" fill="#18283f" stroke="#94a4ba" stroke-width="8"/><circle cx="810" cy="318" r="50" fill="#18283f" stroke="#94a4ba" stroke-width="8"/>',
      ln('lad', 'M80 225 H100'), ln('lad', 'M260 225 H285 V290'),
      ln('dc', 'M415 290 V260'), ln('fahr', 'M625 290 V270'), ln('fahr', 'M705 220 H742'),
      ln('nv', 'M625 150 V127 H490'),
      f'<g class="{px}-bx" data-k="dose" style="transition:opacity .3s"><rect x="36" y="203" width="44" height="44" rx="6" fill="#94a4ba"/><text x="58" y="276" text-anchor="middle" font-size="24" font-weight="800" fill="#94a4ba">Ladedose</text></g>',
      box('ol', 100, 195, 160, 60, 'Ladegerät'), box('dc', 340, 200, 150, 60, 'DC/DC'),
      box('le', 545, 150, 160, 120, 'Leistungs-|elektronik', 26),
      box('nv', 340, 100, 150, 54, 'Klima', 28),
      f'<g class="{px}-bx" data-k="em" style="transition:opacity .3s"><circle cx="790" cy="220" r="48" fill="#18283f" stroke="{O}" stroke-width="6"/><text x="790" y="230" text-anchor="middle" font-size="28" font-weight="900" fill="#ecf1f8">EM</text></g>',
      f'<g class="{px}-bx" data-k="bat" style="transition:opacity .3s"><rect x="265" y="290" width="490" height="62" rx="10" fill="{O}"/><text x="510" y="332" text-anchor="middle" font-size="32" font-weight="900" fill="#1a1a1a" class="dev">HV-Batterie</text></g>',
      f'<path id="{px}-p-fahr" d="M510 300 H625 V272" fill="none" stroke="none"/>',
      f'<path id="{px}-p-fahr2" d="M707 220 H740" fill="none" stroke="none"/>',
      f'<path id="{px}-p-dc" d="M470 300 H415 V262" fill="none" stroke="none"/>',
      f'<path id="{px}-p-rek" d="M740 220 H707" fill="none" stroke="none"/>',
      f'<path id="{px}-p-rek2" d="M625 272 V300 H510" fill="none" stroke="none"/>',
      f'<path id="{px}-p-lad" d="M58 225 H98" fill="none" stroke="none"/>',
      f'<path id="{px}-p-lad2" d="M262 225 H285 V300 H470" fill="none" stroke="none"/>',
      '</svg>']
    return '\n  '.join(out)



# ---- Batterieaufbau
def zellen_svg():
    O = ORA
    o = ['<svg viewBox="0 0 620 300" width="600" height="290" style="display:block;margin:0 auto" id="bz-svg">']
    # Zelle
    o.append('<g class="bz-l" data-l="0"><rect x="250" y="60" width="120" height="180" rx="14" fill="#213552" stroke="#ecf1f8" stroke-width="5"/>'
             '<rect x="285" y="46" width="50" height="16" rx="4" fill="#ecf1f8"/>'
             '<text x="310" y="110" text-anchor="middle" font-size="40" font-weight="900" fill="#f05e4e">+</text><text x="310" y="215" text-anchor="middle" font-size="44" font-weight="900" fill="#5b8cff">−</text>'
             '<text x="310" y="165" text-anchor="middle" font-size="26" font-weight="900" fill="#ecf1f8">3,7 V</text>'
             '<text x="400" y="130" font-size="20" font-weight="800" fill="#94a4ba">eine Zelle</text><text x="400" y="156" font-size="20" font-weight="800" fill="#94a4ba">Lithium-Ionen</text></g>')
    # Modul 3p x 6s
    g = ['<g class="bz-l" data-l="1">']
    for c in range(6):
        x = 70 + c * 80
        g.append(f'<line x1="{x}" y1="70" x2="{x}" y2="230" stroke="{O}" stroke-width="5"/>' if False else '')
        for r in range(3):
            y = 80 + r * 55
            g.append(f'<rect x="{x}" y="{y}" width="44" height="40" rx="6" fill="#213552" stroke="#ecf1f8" stroke-width="3"/>')
        g.append(f'<rect class="bz-par" x="{x - 8}" y="72" width="60" height="164" rx="10" fill="none" stroke="#5b8cff" stroke-width="3" stroke-dasharray="6 5"/>')
        if c < 5:
            g.append(f'<path d="M{x + 52} 154 H{x + 72}" stroke="{O}" stroke-width="6"/>')
    g.append('<text x="40" y="160" text-anchor="end" font-size="30" font-weight="900" fill="#f05e4e">+</text><text x="580" y="160" font-size="34" font-weight="900" fill="#5b8cff">−</text>')
    g.append('<text x="92" y="262" text-anchor="middle" font-size="16" font-weight="800" fill="#5b8cff">3 Zellen parallel</text>')
    g.append(f'<text x="310" y="290" text-anchor="middle" font-size="17" font-weight="800" fill="{O}">Zellgruppen in Reihe → Spannung addiert sich</text>')
    g.append('<text x="310" y="40" text-anchor="middle" font-size="20" font-weight="900" fill="#ecf1f8">Ein Modul (Beispiel)</text></g>')
    o.append(''.join(g))
    # Batterie 8 Module
    b = ['<g class="bz-l" data-l="2"><rect x="20" y="30" width="580" height="240" rx="18" fill="none" stroke="#94a4ba" stroke-width="4"/>']
    for i in range(8):
        x = 45 + (i % 4) * 140; y = 60 if i < 4 else 170
        b.append(f'<rect x="{x}" y="{y}" width="110" height="70" rx="8" fill="#213552" stroke="{O}" stroke-width="4"/><text x="{x + 55}" y="{y + 43}" text-anchor="middle" font-size="22" font-weight="900" fill="#ecf1f8">Modul {i + 1}</text>')
    b.append(f'<path d="M155 95 H185 M295 95 H325 M435 95 H465 M575 95 H588 V205 H575 M465 205 H435 M325 205 H295 M185 205 H155" fill="none" stroke="{O}" stroke-width="6"/>')
    b.append('<text x="310" y="296" text-anchor="middle" font-size="18" font-weight="800" fill="#94a4ba">alle Module in Reihe geschaltet</text></g>')
    o.append(''.join(b))
    o.append('</svg>')
    return ''.join(o)


def stecker_svg():
    O = ORA
    mods = ''.join(f'<rect x="{x}" y="{y}" width="80" height="50" rx="7" fill="#213552" stroke="{O}" stroke-width="4"/><text x="{x + 40}" y="{y + 32}" text-anchor="middle" font-size="17" font-weight="900" fill="#ecf1f8">M{n}</text>'
                   for n, (x, y) in enumerate([(370, 50), (270, 50), (170, 50), (70, 50), (70, 230), (170, 230), (270, 230), (370, 230)], 1))
    return f'''<svg viewBox="0 0 640 320" width="620" height="310" style="display:block;margin:0 auto" id="ws-svg">
  <rect x="20" y="25" width="470" height="275" rx="16" fill="none" stroke="#94a4ba" stroke-width="4"/>
  <text x="255" y="18" text-anchor="middle" font-size="15" font-weight="800" fill="#94a4ba">HV-Batterie</text>
  <path class="ws-live" d="M450 75 H470" stroke="{O}" stroke-width="6"/>
  <path class="ws-live" d="M370 75 H350 M270 75 H250 M170 75 H150 M70 75 H45 V128" fill="none" stroke="{O}" stroke-width="6"/>
  <path class="ws-live" d="M45 172 V255 H70 M150 255 H170 M250 255 H270 M350 255 H370 M450 255 H470" fill="none" stroke="{O}" stroke-width="6"/>
  {mods}
  <g id="ws-plug" style="transition:transform .5s, opacity .5s"><rect x="28" y="124" width="34" height="52" rx="6" fill="#ffd34d" stroke="#1a1a1a" stroke-width="3" class="dev"/></g><text x="70" y="150" font-size="14" font-weight="900" fill="#ecf1f8">Wartungs-</text><text x="70" y="166" font-size="14" font-weight="900" fill="#ecf1f8">stecker</text>
  <rect x="200" y="135" width="110" height="46" rx="8" fill="#18283f" stroke="#a07cf5" stroke-width="3"/><text x="255" y="164" text-anchor="middle" font-size="16" font-weight="900" fill="#ecf1f8">BMS</text>
  <path id="ws-pil" d="M200 158 H62 M310 158 H520 M520 75 V255" fill="none" stroke="#a07cf5" stroke-width="3" stroke-dasharray="7 6"/>
  <text x="360" y="150" font-size="13" font-weight="800" fill="#a07cf5">Pilotlinie</text>
  <circle cx="470" cy="75" r="5" fill="{O}"/><line id="ws-k1" x1="470" y1="75" x2="510" y2="75" stroke="{O}" stroke-width="6" style="transition:transform .4s;transform-origin:470px 75px"/>
  <circle cx="470" cy="255" r="5" fill="{O}"/><line id="ws-k2" x1="470" y1="255" x2="510" y2="255" stroke="{O}" stroke-width="6" style="transition:transform .4s;transform-origin:470px 255px"/>
  <text x="490" y="55" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Schütz +</text><text x="490" y="285" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Schütz −</text>
  <path id="ws-out" d="M512 75 H560 V120 M512 255 H560 V210" fill="none" stroke="{O}" stroke-width="6" style="transition:opacity .4s"/>
  <rect x="540" y="120" width="90" height="90" rx="10" fill="#18283f" stroke="#94a4ba" stroke-width="3"/>
  <text x="585" y="158" text-anchor="middle" font-size="15" font-weight="900" fill="#ecf1f8">zum</text><text x="585" y="178" text-anchor="middle" font-size="15" font-weight="900" fill="#ecf1f8">Fahrzeug</text>
  <text id="ws-h1" x="220" y="122" text-anchor="middle" font-size="16" font-weight="900" fill="#f05e4e" style="opacity:0;transition:opacity .4s">Hälfte 1: ca. 178 V</text>
  <text id="ws-h2" x="220" y="220" text-anchor="middle" font-size="16" font-weight="900" fill="#f05e4e" style="opacity:0;transition:opacity .4s">Hälfte 2: ca. 178 V</text>
</svg>'''


batt_folien = [
    folie(T, 'Aufbau der HV-Batterie – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-l="0">1. Zelle</button><button class="btn ghost" data-l="1">2. Modul</button><button class="btn ghost" data-l="2">3. Batterie</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.35fr 1fr">
      {zellen_svg()}
      <div class="card" id="bz-t" style="font-size:17px;font-weight:600;line-height:1.55"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">Beispielwerte – Zellzahl und Spannung je nach Fahrzeug.</p>''', sid='s-bz', body_cls='body noclick'),
    folie(T, 'Der Wartungsstecker – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" id="ws-in">Stecker gesteckt</button><button class="btn ghost" id="ws-out-b">Stecker gezogen</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.35fr 1fr">
      {stecker_svg()}
      <div>
        <div class="card"><div class="muted" style="font-size:15px;font-weight:800">SPANNUNG AM FAHRZEUG</div><div class="lcd2" id="ws-v" style="font-size:32px;margin-top:6px">ca. 355 V</div></div>
        <div class="card" id="ws-t" style="margin-top:10px;font-size:16px;font-weight:600;line-height:1.5"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">Vereinfachte Darstellung, Beispielwerte. Ob und wo es einen Wartungsstecker gibt, bestimmt der Hersteller.</p>''', sid='s-ws', body_cls='body noclick'),
    folie(T, 'Wartungsstecker oder Niedervolt-Trennstelle?', '''    <div class="grid2" style="align-items:start">
      <div class="card step" style="border-top:4px solid var(--grn)"><div class="big" style="font-size:21px">Wartungsstecker (im HV-Kreis)</div>
        <ul UL><li>trennt den <b>Hauptstromkreis mechanisch</b> – mitten in der Batterie</li><li>teilt die Batterie in zwei Hälften mit kleinerer Spannung</li><li>unterbricht zusätzlich die Pilotlinie – die Schütze öffnen</li><li>wirkt auch, wenn ein Schütz verschweißt (festgeklebt) ist</li><li>kann mitgenommen oder abgeschlossen werden</li></ul></div>
      <div class="card step" style="border-top:4px solid var(--ora)"><div class="big" style="font-size:21px">Niedervolt-Trennstelle / 12 V abklemmen</div>
        <ul UL><li>trennt nur den <b>12-V-Steuerkreis</b></li><li>die Schütze werden nicht mehr angesteuert und öffnen</li><li>der HV-Kreis selbst wird nicht mechanisch getrennt</li><li>ist ein Schütz verschweißt, kann trotzdem Hochvolt anliegen</li></ul></div>
      <div class="warn step" style="grid-column:1/-1"><b>In beiden Fällen</b>Die Module selbst bleiben geladen – die Batterie ist innen nie spannungsfrei, auch jede Hälfte hat noch über 60 V. Darum immer nach Herstellervorgabe freischalten und die Spannungsfreiheit am Fahrzeug feststellen.</div>
    </div>'''.replace('UL', UL)),
]
batt_js = """
  const BT = [
    '<b class="ora">Die Zelle:</b> Eine Lithium-Ionen-Zelle hat nur ca. 3,7 V. Für Hochvolt braucht man viele Zellen.',
    '<b class="ora">Das Modul – gemischt verschaltet:</b> Jeweils mehrere Zellen sind <b>parallel</b> geschaltet (blau umrandet) – das erhöht die Kapazität und den möglichen Strom, die Spannung bleibt 3,7 V. Diese Zellgruppen sind <b>in Reihe</b> geschaltet – die Spannungen addieren sich. Beispiel: 12 Gruppen in Reihe ≈ 44 V.',
    '<b class="ora">Die Batterie:</b> Mehrere Module sind in Reihe geschaltet. Beispiel: 8 Module × 12 Zellgruppen = 96 Gruppen in Reihe ≈ 355 V. Dazu kommen Batteriemanagement (BMS), Schütze, Sicherung, Kühlung und ein stabiles Gehäuse.'
  ];
  const lb = document.querySelectorAll('#s-bz [data-l]'), lg = document.querySelectorAll('#bz-svg .bz-l');
  function lv(i) { lg.forEach(g => g.style.display = +g.dataset.l === i ? '' : 'none'); lb.forEach(b => b.classList.toggle('on', +b.dataset.l === i)); document.getElementById('bz-t').innerHTML = BT[i]; }
  lb.forEach(b => b.onclick = () => lv(+b.dataset.l)); lv(0);

  function ws(on) {
    const pl = document.getElementById('ws-plug'); pl.style.transform = on ? '' : 'translate(-22px,0)'; pl.style.opacity = on ? 1 : 0.35;
    document.getElementById('ws-k1').style.transform = on ? '' : 'rotate(-30deg)';
    document.getElementById('ws-k2').style.transform = on ? '' : 'rotate(30deg)';
    document.getElementById('ws-out').style.opacity = on ? 1 : 0.15;
    document.getElementById('ws-pil').setAttribute('stroke', on ? '#a07cf5' : '#f05e4e');
    ['ws-h1', 'ws-h2'].forEach(id => document.getElementById(id).style.opacity = on ? 0 : 1);
    document.getElementById('ws-v').textContent = on ? 'ca. 355 V' : '0 V*';
    document.getElementById('ws-in').classList.toggle('on', on); document.getElementById('ws-out-b').classList.toggle('on', !on);
    document.getElementById('ws-t').innerHTML = on
      ? '<b>Gesteckt:</b> Alle Module sind in Reihe verbunden, die Pilotlinie ist geschlossen. Das BMS kann die Schütze schließen – am Fahrzeug liegt die volle Spannung an.'
      : '<b>Gezogen:</b> Der Hauptstromkreis ist <b>mitten in der Batterie mechanisch getrennt</b>. Die Pilotlinie ist unterbrochen – die Schütze öffnen. <span class="red">Aber: Jede Batteriehälfte hat noch ca. 178 V!</span><br><span class="muted">* erst nach Wartezeit und Spannungsprüfung sicher</span>';
  }
  document.getElementById('ws-in').onclick = () => ws(true); document.getElementById('ws-out-b').onclick = () => ws(false);
  document.getElementById('s-ws').addEventListener('slideshow', () => ws(true));
  ws(true);
"""

aufbau = [
    titel_folie(K, '⚡', 'Aufbau des E-Autos', 'Batterie, Leistungselektronik, E-Maschine und Laden'),
    lernziele(T, ['Welche Hochvolt-Bauteile ein E-Auto hat', 'Wie die Energie beim Fahren, Bremsen und Laden fließt',
                  'Wie die HV-Batterie aufgebaut ist und was der Wartungsstecker bewirkt', 'Welche Schutzeinrichtungen das HV-System hat']),
    folie(T, 'Die Hochvolt-Bauteile – zum Antippen', f'''    {blockbild('au')}
    <div class="card" id="au-t" style="font-size:18px;font-weight:600;line-height:1.5;margin-top:8px"></div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">Tippe auf ein Bauteil. Vereinfachte Darstellung – Lage und Bauform je nach Hersteller.</p>''', sid='s-au', body_cls='body noclick'),
    *batt_folien,
    folie(T, 'Energiefluss – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-f="fahr">Fahren</button><button class="btn ghost" data-f="rek">Bremsen (Rekuperation)</button><button class="btn ghost" data-f="lad">Laden</button></div>
    {blockbild('ef')}
    <div class="card" id="ef-t" style="font-size:18px;font-weight:600;line-height:1.5;margin-top:8px"></div>''', sid='s-ef', body_cls='body noclick'),
    folie(T, 'Laden: AC und DC', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">AC-Laden (Wechselstrom)</div>
        <ul UL><li>an Wallbox oder Ladesäule mit Wechselstrom</li><li>das Ladegerät im Auto macht Gleichspannung daraus</li><li>meist bis 11 oder 22 kW (Richtwert)</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">DC-Laden (Gleichstrom)</div>
        <ul UL><li>Schnellladesäule liefert direkt Gleichspannung</li><li>am Ladegerät im Auto vorbei direkt zur Batterie</li><li>deutlich höhere Leistung – kürzere Ladezeit</li></ul></div>
    </div>
    <div class="note step">Ladeleistungen je nach Fahrzeug und Ladesäule – Richtwerte.</div>'''.replace('UL', UL)),
    folie(T, 'Schutzeinrichtungen im HV-System', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Isoliertes System</b>Das HV-System hat keine Verbindung zur Karosserie. Eine Isolationsüberwachung meldet, wenn die Isolation schlechter wird.</div>
      <div class="tip step"><b>Schütze in der Batterie</b>Sie trennen die Batterie vom Fahrzeug, z. B. bei Zündung aus oder nach einem Unfall.</div>
      <div class="tip step"><b>Pilotlinie (Interlock)</b>Eine Überwachungsleitung durch die HV-Stecker – wird ein Stecker gezogen, schaltet das System ab.</div>
      <div class="warn step"><b>Kein Ersatz fürs Freischalten</b>Diese Einrichtungen schützen im Betrieb. Vor Arbeiten am HV-System muss es trotzdem nach Vorschrift spannungsfrei geschaltet werden.</div>
    </div>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>12-V-Batterie</b>Auch E-Autos haben eine 12-V-Batterie. Ist sie leer, „startet“ das Fahrzeug nicht – das HV-System wird über 12 V eingeschaltet.</div>
      <div class="tip step"><b>Leise heißt nicht aus</b>Ein E-Auto ist im Stand still – ob es „fahrbereit“ ist, zeigt nur die Anzeige im Kombiinstrument.</div>
      <div class="warn step"><b>Anheben und Hebebühne</b>Nur an den vorgesehenen Aufnahmepunkten – die HV-Batterie im Unterboden nicht beschädigen.</div>
      <div class="tip step"><b>Kühlmittel</b>Batterie und Leistungselektronik haben oft eigene Kühlkreisläufe – nur das vorgeschriebene Kühlmittel verwenden.</div>
    </div>'''),
    video(T, 'hv-aufbau'),
    kurztest(T, [
        ('Was macht der Wechselrichter in der Leistungselektronik?', ['Er macht aus Gleichspannung Drehstrom für die E-Maschine', 'Er lädt die 12-V-Batterie', 'Er kühlt die Batterie'], 0, 'So werden Drehzahl und Kraft der E-Maschine geregelt.'),
        ('Was ersetzt im E-Auto die Lichtmaschine?', ['Die E-Maschine', 'Der DC/DC-Wandler', 'Das Ladegerät'], 1, 'Er macht aus Hochvolt 12 V für das Bordnetz.'),
        ('Was passiert beim Rekuperieren?', ['Die Batterie wird beim Fahren entladen', 'Die Klimaanlage wird abgeschaltet', 'Die E-Maschine arbeitet als Generator und lädt die Batterie'], 2, 'Bremsenergie wird zurückgewonnen.'),
        ('Wie wird beim DC-Schnellladen geladen?', ['Die Ladesäule liefert direkt Gleichspannung zur Batterie', 'Über das Ladegerät im Auto', 'Über die 12-V-Steckdose'], 0, 'Am On-Board-Ladegerät vorbei.'),
    ]),
    merke(T, ['Batterie, Leistungselektronik, E-Maschine', 'DC/DC-Wandler versorgt das 12-V-Bordnetz',
              'AC: Lader im Auto – DC: direkt zur Batterie', 'Schutzeinrichtungen ersetzen kein Freischalten']),
]
aufbau_js = '''<script src="assets/schaltung.js"></script>
<script>
(function () {
  const K = ''' + str({k: [n, t] for k, n, t in KOMP}).replace("'", '"') + ''';
  const gs = document.querySelectorAll('#s-au .au-bx');
  function k(id) {
    gs.forEach(g => g.style.opacity = g.dataset.k === id ? 1 : 0.45);
    document.getElementById('au-t').innerHTML = '<b class="ora">' + K[id][0] + ':</b> ' + K[id][1];
  }
  gs.forEach(g => { g.style.cursor = 'pointer'; g.onclick = () => k(g.dataset.k); }); k('bat');

  const svg = document.getElementById('ef-svg');
  const F = {}; ['fahr', 'fahr2', 'dc', 'rek', 'rek2', 'lad', 'lad2'].forEach(n => F[n] = Flow(svg, document.getElementById('ef-p-' + n), { spacing: 26, speed: 60, r: 9, color: '#ffd34d' }));
  const M = { fahr: { f: ['fahr', 'fahr2', 'dc'], l: ['fahr', 'dc'], b: ['bat', 'le', 'em', 'dc'] }, rek: { f: ['rek', 'rek2'], l: ['fahr'], b: ['bat', 'le', 'em'] }, lad: { f: ['lad', 'lad2'], l: ['lad'], b: ['dose', 'ol', 'bat'] } };
  const TX = {
    fahr: '<b>Fahren:</b> Die Batterie gibt Energie ab. Die Leistungselektronik macht daraus Drehstrom, die E-Maschine (EM) treibt das Auto an. Der DC/DC-Wandler versorgt das 12-V-Bordnetz.',
    rek: '<b>Bremsen:</b> Die E-Maschine arbeitet als Generator. Die Leistungselektronik schickt die Energie zurück in die Batterie (Rekuperation).',
    lad: '<b>Laden (AC):</b> Strom kommt über die Ladedose, das Ladegerät macht Gleichspannung daraus und lädt die Batterie. Beim DC-Schnellladen geht es am Ladegerät vorbei direkt zur Batterie.'
  };
  const bt = document.querySelectorAll('#s-ef [data-f]');
  function f(n) {
    const m = M[n];
    Object.keys(F).forEach(x => F[x].on(m.f.includes(x)));
    document.querySelectorAll('#s-ef .ef-ln').forEach(l => l.style.opacity = m.l.includes(l.dataset.g) ? 1 : 0.2);
    document.querySelectorAll('#s-ef .ef-bx').forEach(g => g.style.opacity = m.b.includes(g.dataset.k) ? 1 : 0.3);
    bt.forEach(b => b.classList.toggle('on', b.dataset.f === n));
    document.getElementById('ef-t').innerHTML = TX[n];
  }
  bt.forEach(b => b.onclick = () => f(b.dataset.f)); f('fahr');
''' + batt_js + '''
})();
</script>'''

# ---------------------------------------------------------------- 3 Qualifizierungsstufen
T = 'QUALIFIZIERUNG'
STUFEN = [
    ('S', 'Sensibilisierte Person', 'Fahrzeug bedienen: fahren, laden, waschen, einfache Tätigkeiten wie Wischerblätter wechseln oder Scheibenwaschwasser auffüllen.'),
    ('1S', 'Fachkundig unterwiesene Person (FuP)', 'Allgemeine Arbeiten am Fahrzeug, die das HV-System nicht direkt betreffen: z. B. Karosserie, Ölwechsel, Räder, Arbeiten am 12-V-Bordnetz. Unterweisung durch eine FHV, mindestens 2 Unterrichtseinheiten, dokumentiert.'),
    ('2S', 'Fachkundige Person Hochvolt (FHV)', 'HV-System spannungsfrei schalten und selbstständig an spannungsfreien HV-Systemen arbeiten: z. B. Isolationswiderstand messen, Bauteile reparieren oder tauschen, prüfen.'),
    ('3S', 'FHV für Arbeiten unter Spannung', 'Fehlersuche an HV-Bauteilen unter Spannung, Tausch unter Spannung stehender Bauteile, Hochspannungsprüfungen nach Herstellervorgabe.'),
]
AUFG = [('Fahrzeug laden und waschen', 'S'), ('Reifen wechseln, Ölwechsel', '1S'), ('Arbeiten am 12-V-Bordnetz', '1S'),
        ('Pannenhilfe', '1S'), ('HV-System spannungsfrei schalten', '2S'), ('HV-Bauteil tauschen (spannungsfrei)', '2S'),
        ('Fehlersuche unter Spannung', '3S')]
stufen = [
    titel_folie(K, '1S·2S', 'Qualifizierungsstufen', 'Wer darf was am Hochvoltfahrzeug?', 'font-size:56px'),
    lernziele(T, ['Die Stufen S, 1S, 2S und 3S für Serienfahrzeuge', 'Welche Arbeiten zu welcher Stufe gehören',
                  'Was für Kfz-Mechatroniker und Auszubildende gilt', 'Wer die Verantwortung trägt']),
    folie(T, 'Die vier Stufen', '''    <div class="values">''' + ''.join(f'''
      <div class="val step from-left"><b>{s}</b><span><em class="c" style="font-style:normal;font-weight:800">{n}</em> – {t}</span></div>''' for s, n, t in STUFEN) + '''
    </div>
''' + QUELLE),
    folie(T, 'Wer darf was? – zum Ausprobieren', '''    <div class="choice" style="margin-bottom:12px;flex-wrap:wrap">''' + ''.join(f'<button class="btn ghost" data-a="{i}">{n}</button>' for i, (n, s) in enumerate(AUFG)) + '''</div>
    <div class="grid2" style="align-items:center;grid-template-columns:200px 1fr">
      <div class="card" style="text-align:center"><div class="muted" style="font-size:15px;font-weight:800">MINDESTENS</div><div id="ww-s" style="font-size:56px;font-weight:900;color:var(--ct)">—</div></div>
      <div class="card" id="ww-t" style="font-size:18px;font-weight:600;line-height:1.5">Tippe eine Arbeit an.</div>
    </div>''', sid='s-ww', body_cls='body noclick'),
    folie(T, 'Was gilt für Kfz-Mechatroniker?', '''    <ol class="steps-list">
      <li class="step">Ausbildung nach der Ausbildungsordnung von 2013 <span class="c">erfolgreich abgeschlossen</span><small>dann besitzt du die Fachkunde nach Stufe 2S</small></li>
      <li class="step">Schwerpunkt System- und Hochvolttechnik<small>hier wird bereits die Fachkunde nach Stufe 3S vermittelt</small></li>
      <li class="step">Während der Ausbildung<small>Arbeiten am HV-System nur unter Leitung und Aufsicht einer Fachkundigen Person Hochvolt (FHV)</small></li>
      <li class="step">Der Betrieb legt fest, wer was darf<small>auf Grundlage der Gefährdungsbeurteilung – und unterweist regelmäßig</small></li>
    </ol>
''' + QUELLE),
    folie(T, 'Stufe 3S: Arbeiten unter Spannung', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Voraussetzungen</div>
        <ul UL><li>Qualifikation 2S</li><li>mindestens 18 Jahre</li><li>Erste-Hilfe-Ausbildung mit Herz-Lungen-Wiederbelebung</li><li>keine gesundheitlichen Einschränkungen</li><li>mindestens ein Jahr Berufserfahrung</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Bei der Arbeit</div>
        <ul UL><li>in der Regel eine zweite Person dabei – mindestens FuP mit Erste-Hilfe-Ausbildung</li><li>besondere Schutzausrüstung</li><li>genaue Herstellervorgaben</li></ul></div>
    </div>
''' + QUELLE.replace('Herstellervorgaben beachten.', '')),
    folie(T, 'Verantwortung und Unterweisung', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Unternehmer</b>trägt die Verantwortung: Nur ausreichend qualifizierte Beschäftigte dürfen an HV-Systemen arbeiten.</div>
      <div class="tip step"><b>Fachkundige Leitung</b>wird vom Unternehmer schriftlich beauftragt.</div>
      <div class="tip step"><b>Unterweisung</b>regelmäßig nach Arbeitsschutzgesetz und DGUV Vorschrift 1 – bei neuen Fahrzeugtypen oder HV-Systemen immer durch eine FHV, dokumentiert.</div>
      <div class="tip step"><b>Wissen aktuell halten</b>FHV bilden sich regelmäßig weiter – die Technik ändert sich schnell.</div>
    </div>'''),
    video(T, 'hv-stufen'),
    kurztest(T, [
        ('Welche Stufe braucht man mindestens für einen Ölwechsel an einem E-Auto?', ['S', '1S (FuP)', '3S'], 1, 'Allgemeine Arbeiten, die das HV-System nicht betreffen: Stufe 1S.'),
        ('Wer darf ein HV-System spannungsfrei schalten?', ['Jeder mit Führerschein', 'Eine sensibilisierte Person', 'Eine Fachkundige Person Hochvolt (2S) oder unter ihrer Leitung'], 2, 'Freischalten ist Aufgabe der FHV.'),
        ('Welche Fachkunde haben Kfz-Mechatroniker nach erfolgreich abgeschlossener Ausbildung (AO 2013)?', ['Stufe 2S', 'Stufe S', 'Keine'], 0, 'Laut DGUV 209-093 besitzen sie die Fachkunde nach Stufe 2S.'),
        ('Was gilt für Arbeiten unter Spannung (3S)?', ['Darf jeder Azubi', 'In der Regel ist eine zweite Person dabei', 'Nur mit Multimeter'], 1, 'Mindestens eine FuP mit Erste-Hilfe-Ausbildung.'),
    ]),
    merke(T, ['S: bedienen – 1S: allgemeine Arbeiten', '2S (FHV): spannungsfrei schalten und arbeiten',
              '3S: Arbeiten unter Spannung', 'Azubis: nur unter Leitung und Aufsicht einer FHV']),
]
stufen_js = '''<script>
(function () {
  const A = ''' + str([[n, s] for n, s in AUFG]).replace("'", '"') + ''';
  const ST = ''' + str({s: n for s, n, t in STUFEN}).replace("'", '"') + ''';
  const bt = document.querySelectorAll('#s-ww [data-a]');
  bt.forEach(b => b.onclick = () => {
    const [n, s] = A[+b.dataset.a];
    document.getElementById('ww-s').textContent = s;
    document.getElementById('ww-t').innerHTML = '<b>' + n + ':</b> mindestens Stufe ' + s + ' – ' + ST[s] + '.';
    bt.forEach(x => x.classList.toggle('on', x === b));
  });
})();
</script>'''

# ---------------------------------------------------------------- 4 Spannungsfreiheit herstellen
T = 'SPANNUNGSFREIHEIT'
SCHRITTE = ['Zündung aus, Schlüssel sicher verwahren', 'Service-Stecker ziehen bzw. Hauptschalter aus – nach Herstellervorgabe',
            'Gegen Wiedereinschalten sichern, z. B. abschließbare Kappe', 'Vorgeschriebene Wartezeit einhalten',
            'Spannungsprüfer vorher auf Funktion prüfen', 'Spannungsfreiheit an allen Polen feststellen',
            'Spannungsprüfer nachher erneut auf Funktion prüfen', 'Schild am Fahrzeug: „spannungsfrei“ mit Name der FHV']
frei = [
    titel_folie(K, '0 V', 'Spannungsfreiheit herstellen', 'Die Sicherheitsregeln am Hochvoltfahrzeug', 'font-size:84px'),
    lernziele(T, ['Die fünf Sicherheitsregeln', 'Welche Regeln am Fahrzeug immer gelten',
                  'Wie die Spannungsfreiheit richtig festgestellt wird', 'Warum ein Multimeter dafür nicht geeignet ist']),
    folie(T, 'Die fünf Sicherheitsregeln', '''    <ol class="steps-list">
      <li class="step">Freischalten</li>
      <li class="step">Gegen Wiedereinschalten sichern</li>
      <li class="step">Spannungsfreiheit feststellen</li>
      <li class="step">Erden und kurzschließen<small>am Fahrzeug nach Herstellervorgabe – Energiespeicher dürfen nicht kurzgeschlossen werden!</small></li>
      <li class="step">Benachbarte, unter Spannung stehende Teile abdecken oder abschranken</li>
    </ol>
    <div class="warn step" style="margin-top:6px"><b>Bei Arbeiten am HV-System</b>müssen immer die ersten drei Regeln umgesetzt werden. Regel 4 und 5 werden im Einzelfall entschieden.</div>'''),
    folie(T, 'Regel 1 und 2 am Fahrzeug', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">1. Freischalten – z. B.</div>
        <ul UL><li>Zündung aus</li><li>Service-Stecker ziehen oder Batterie-Hauptschalter aus</li><li>Sicherung ziehen, Pilotlinie auftrennen</li><li>12-V-Batterie abklemmen, Ladekabel trennen</li><li>geführte Abschaltung mit dem Diagnosegerät</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">2. Sichern – z. B.</div>
        <ul UL><li>Schlüssel sicher verwahren</li><li>Service-Stecker oder Hauptschalter abschließen, z. B. mit abschließbarer Kappe</li><li>nur die verantwortliche FHV darf wieder einschalten</li></ul></div>
    </div>
    <div class="note step">Wie genau freigeschaltet wird, gibt der Hersteller vor.</div>'''.replace('UL', UL)),
    folie(T, 'Regel 3: Spannungsfreiheit feststellen', '''    <ol class="steps-list">
      <li class="step">Geeigneten <span class="c">zweipoligen Spannungsprüfer</span> verwenden<small>z. B. nach DIN EN 61243-3</small></li>
      <li class="step">Spannungsprüfer <span class="c">vorher</span> auf Funktion prüfen</li>
      <li class="step">Alle Teile prüfen, die unter Spannung stehen könnten<small>Messpunkte nach Herstellervorgabe</small></li>
      <li class="step">Spannungsprüfer <span class="c">nachher</span> erneut auf Funktion prüfen<small>nur so ist sicher, dass er bei der Messung funktioniert hat</small></li>
    </ol>
    <div class="warn step" style="margin-top:6px"><b>Vielfachmessgeräte sind nicht geeignet</b>Ein Multimeter ist für das Feststellen der Spannungsfreiheit nicht zugelassen – falscher Messbereich oder leere Batterie täuschen „0 V“ vor.</div>'''),
    folie(T, 'Die richtige Reihenfolge – zum Ausprobieren', '''    <div class="card" style="font-size:17px;font-weight:700;margin-bottom:10px">Tippe die Schritte in der richtigen Reihenfolge an.</div>
    <div class="grid2" style="align-items:start">
      <div id="rf-opts" style="display:flex;flex-direction:column;gap:8px"></div>
      <div><ol class="steps-list" id="rf-done" style="margin:0"></ol><div class="card" id="rf-t" style="margin-top:8px;font-size:16px;font-weight:600"></div></div>
    </div>''', sid='s-rf', body_cls='body noclick'),
    folie(T, 'Nach der Arbeit', '''    <ol class="steps-list">
      <li class="step">Werkzeug und Material vom Fahrzeug entfernen</li>
      <li class="step">Abdeckungen und HV-Stecker ordnungsgemäß montieren</li>
      <li class="step">Die Regeln in umgekehrter Reihenfolge aufheben<small>nach Herstellervorgabe – nur durch die verantwortliche FHV</small></li>
      <li class="step">Sicheren Betriebszustand herstellen, Fehlerspeicher prüfen<small>Schild am Fahrzeug auf den aktuellen Zustand ändern</small></li>
    </ol>
''' + QUELLE),
    video(T, 'hv-freischalten'),
    kurztest(T, [
        ('Welche Sicherheitsregeln müssen bei Arbeiten am HV-System immer umgesetzt werden?', ['Die ersten drei', 'Nur Regel 1', 'Nur Regel 5'], 0, 'Freischalten, gegen Wiedereinschalten sichern, Spannungsfreiheit feststellen.'),
        ('Womit wird die Spannungsfreiheit festgestellt?', ['Mit dem Multimeter', 'Mit einem geeigneten zweipoligen Spannungsprüfer', 'Mit einer Prüflampe'], 1, 'Vielfachmessgeräte sind nicht geeignet.'),
        ('Wann prüfst du den Spannungsprüfer auf Funktion?', ['Nur einmal im Jahr', 'Nur danach', 'Unmittelbar vorher und nachher'], 2, 'So ist sicher, dass er während der Messung funktioniert hat.'),
        ('Darf die HV-Batterie zum „Erden und Kurzschließen“ kurzgeschlossen werden?', ['Nein, Energiespeicher dürfen nicht kurzgeschlossen werden', 'Ja, immer', 'Nur mit dicken Kabeln'], 0, 'Regel 4 am Fahrzeug nur nach Herstellervorgabe.'),
    ]),
    merke(T, ['Freischalten, sichern, Spannungsfreiheit feststellen', 'Zweipoliger Spannungsprüfer – kein Multimeter',
              'Prüfer vorher und nachher testen', 'Energiespeicher nie kurzschließen']),
]
frei_js = '''<script>
(function () {
  const S = ''' + str(SCHRITTE).replace("'", '"') + ''';
  const ord = [3, 0, 6, 2, 5, 1, 7, 4];
  let next = 0;
  function build() {
    next = 0;
    document.getElementById('rf-done').innerHTML = '';
    document.getElementById('rf-t').innerHTML = 'Welcher Schritt kommt zuerst?';
    const o = document.getElementById('rf-opts'); o.innerHTML = '';
    ord.forEach(i => {
      const b = document.createElement('button'); b.className = 'btn ghost'; b.style.textAlign = 'left'; b.textContent = S[i];
      b.onclick = () => {
        if (i === next) {
          b.remove(); const li = document.createElement('li'); li.className = 'step on'; li.textContent = S[i];
          document.getElementById('rf-done').appendChild(li); next++;
          document.getElementById('rf-t').innerHTML = next === S.length ? '<b class="grn">Richtig!</b> So wird das HV-System nach den Sicherheitsregeln spannungsfrei geschaltet – die genauen Schritte gibt der Hersteller vor. <button class="btn ghost" id="rf-neu">Nochmal</button>' : '<b class="grn">Richtig.</b> Und als Nächstes?';
          const n = document.getElementById('rf-neu'); if (n) n.onclick = build;
        } else { document.getElementById('rf-t').innerHTML = '<b class="ora">Noch nicht.</b> Überlege, was vorher passieren muss.'; }
      };
      o.appendChild(b);
    });
  }
  document.getElementById('s-rf').addEventListener('slideshow', build);
  build();
})();
</script>'''

# ---------------------------------------------------------------- 5 Sicher arbeiten
T = 'SICHER ARBEITEN'
SCHILD = '''<svg viewBox="0 0 300 200" width="280" height="186" style="display:block;margin:0 auto" class="dev">
  <rect x="6" y="6" width="288" height="188" rx="12" fill="#ffffff" stroke="#1a1a1a" stroke-width="4"/>
  <rect x="6" y="6" width="288" height="44" rx="12" fill="#34c778"/><rect x="6" y="36" width="288" height="14" fill="#34c778"/>
  <text x="150" y="36" text-anchor="middle" font-size="16" font-weight="900" fill="#1a1a1a">HV-SYSTEM SPANNUNGSFREI</text>
  <text x="20" y="84" font-size="15" font-weight="700" fill="#1a1a1a">Verantwortliche FHV:</text>
  <line x1="20" y1="104" x2="280" y2="104" stroke="#1a1a1a" stroke-width="1.5" stroke-dasharray="4 4"/>
  <text x="20" y="134" font-size="15" font-weight="700" fill="#1a1a1a">Telefon:</text>
  <line x1="20" y1="154" x2="280" y2="154" stroke="#1a1a1a" stroke-width="1.5" stroke-dasharray="4 4"/>
  <text x="20" y="180" font-size="13" font-weight="700" fill="#555555">Datum / Uhrzeit:</text>
</svg>'''
sicher = [
    titel_folie(K, '!', 'Sicher arbeiten', 'Schutzausrüstung, Kennzeichnung, Unfall- und Pannenfahrzeuge', 'font-size:120px'),
    lernziele(T, ['Welche Schutzausrüstung bei HV-Arbeiten nötig ist', 'Wie der Arbeitsplatz und das Fahrzeug gekennzeichnet werden',
                  'Was bei Unfall- und Pannenfahrzeugen gilt', 'Was im Notfall zu tun ist']),
    folie(T, 'Persönliche Schutzausrüstung', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Isolierende Schutzhandschuhe</b>für Arbeiten an Teilen, die unter Spannung stehen könnten – vor jeder Benutzung prüfen.</div>
      <div class="tip step"><b>Gesichtsschutz</b>z. B. Helm mit Visier – Schutz vor Störlichtbogen.</div>
      <div class="tip step"><b>Schutzkleidung</b>gegen die Hitze eines Störlichtbogens – Auswahl nach DGUV Information 203-077.</div>
      <div class="tip step"><b>Isoliertes Werkzeug</b>und geeignete Mess- und Prüfgeräte nach Herstellervorgabe.</div>
    </div>
    <div class="note step">Welche Ausrüstung im Einzelfall nötig ist, ergibt sich aus der Gefährdungsbeurteilung.</div>'''),
    folie(T, 'Kennzeichnung in der Werkstatt', f'''    <div class="grid2" style="align-items:center">
      <div class="card step">{SCHILD}<div class="muted" style="font-size:14px;text-align:center;margin-top:6px">Beispiel für ein Schild am Fahrzeug</div></div>
      <ul class="step" UL>
        <li>Das Schild zeigt den <b>Zustand des HV-Systems</b>: spannungsfrei oder unter Spannung</li>
        <li>Es nennt die <b>verantwortliche FHV</b> mit Telefonnummer</li>
        <li>Es muss am Fahrzeug <b>gut sichtbar</b> sein</li>
        <li>Arbeitsplatz absperren, damit Unbefugte nicht ans Fahrzeug kommen</li>
      </ul>
    </div>'''.replace('UL', UL)),
    folie(T, 'Unfall- und beschädigte Fahrzeuge', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Spannung möglich</b>Auch nach einem Unfall kann Spannung anliegen. Eigenschutz geht vor.</div>
      <div class="warn step"><b>Airbag ausgelöst</b>Das HV-System wird meist automatisch abgeschaltet – das ist aber kein Freischalten nach den Sicherheitsregeln.</div>
      <div class="warn step"><b>Brandgefahr</b>Eine beschädigte Batterie kann sich auch später noch durch innere Reaktionen entzünden. Bei Brandgefahr: absichern, Feuerwehr rufen.</div>
      <div class="warn step"><b>Austretende Stoffe</b>Jeden Kontakt vermeiden. Bergung nur mit geeignetem Werkzeug und Schutzausrüstung.</div>
    </div>
''' + QUELLE),
    folie(T, 'Panne, Abschleppen, Bergung', '''    <div class="values">
      <div class="val step from-left"><b>Pannenhilfe</b><span>mindestens Stufe 1S</span></div>
      <div class="val step from-left"><b>Abschleppen</b><span>nur nach Herstellervorgabe – z. B. ob das Fahrzeug geschleppt werden darf</span></div>
      <div class="val step from-left"><b>Bergung</b><span>mindestens FuP – bei unklarer Lage oder elektrischer Gefahr eine FHV hinzuziehen</span></div>
    </div>
''' + QUELLE),
    folie(T, 'Im Notfall: Stromunfall', '''    <ol class="steps-list">
      <li class="step">Eigenschutz! Nicht in den Stromkreis greifen<small>wenn möglich und gefahrlos: System abschalten oder Person mit isolierendem Gegenstand lösen</small></li>
      <li class="step">Notruf 112</li>
      <li class="step">Erste Hilfe<small>Atmung prüfen, bei Bedarf Herz-Lungen-Wiederbelebung, Defibrillator holen lassen</small></li>
      <li class="step">Immer ärztlich untersuchen lassen<small>auch wenn es der Person gut geht – Herzrhythmusstörungen können später auftreten</small></li>
    </ol>'''),
    video(T, 'hv-sicher'),
    kurztest(T, [
        ('Was zeigt das Schild am HV-Fahrzeug in der Werkstatt?', ['Den Zustand des HV-Systems und die verantwortliche FHV', 'Den Reifendruck', 'Den Ölstand'], 0, 'So weiß jeder, ob das System spannungsfrei ist und wer verantwortlich ist.'),
        ('Nach einem Unfall hat der Airbag ausgelöst. Ist das HV-System damit sicher spannungsfrei?', ['Ja, immer', 'Nein – das ist kein Freischalten nach den Sicherheitsregeln', 'Nur bei Regen'], 1, 'Es wird meist automatisch abgeschaltet, ersetzt aber nicht das Freischalten.'),
        ('Welche Qualifikation braucht man mindestens für die Pannenhilfe an HV-Fahrzeugen?', ['Keine', 'Stufe S', 'Stufe 1S'], 2, 'Laut DGUV 209-093 mindestens Stufe 1S.'),
        ('Was gilt nach einem Stromunfall?', ['Immer ärztlich untersuchen lassen', 'Nur wenn es weh tut', 'Weiterarbeiten'], 0, 'Herzrhythmusstörungen können auch später auftreten.'),
    ]),
    merke(T, ['PSA: isolierende Handschuhe, Gesichtsschutz, Schutzkleidung', 'Schild: Zustand des HV-Systems und FHV',
              'Unfallfahrzeug: Spannung möglich, Brandgefahr', 'Stromunfall: Eigenschutz, 112, Erste Hilfe, Arzt']),
]

STYLE = '  .symbol { font-size: 96px; }'

if __name__ == '__main__':
    seite('hv-grundlagen.html', 'Hochvolt-Grundlagen – Hochvolt im Kfz', 't-hv', THEMA, grundlagen, STYLE, grundlagen_js)
    seite('hv-aufbau.html', 'Aufbau des E-Autos – Hochvolt im Kfz', 't-hv', THEMA, aufbau, STYLE, aufbau_js)
    seite('hv-stufen.html', 'Qualifizierungsstufen – Hochvolt im Kfz', 't-hv', THEMA, stufen, STYLE, stufen_js)
    seite('hv-freischalten.html', 'Spannungsfreiheit herstellen – Hochvolt im Kfz', 't-hv', THEMA, frei, STYLE, frei_js)
    seite('hv-sicher.html', 'Sicher arbeiten – Hochvolt im Kfz', 't-hv', THEMA, sicher, STYLE, '')
    print('ok')
