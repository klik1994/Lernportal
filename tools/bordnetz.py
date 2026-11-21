"""Bordnetz – fünf Präsentationen.
Aufruf: cd tools && python3 bordnetz.py"""
from praesentation_bauen import *

THEMA = 'Bordnetz'
K = 'BORDNETZ'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'
PL, MI, GE = '#f05e4e', '#28aaf5', '#ffd34d'   # Plus rot, Minus/Masse blau, Strom-Punkte gelb
STYLE = '''  .symbol { font-size: 80px; }
  .kl { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
  .kl .card { margin: 0; text-align: center; transition: opacity .3s, box-shadow .3s; }
  .kl .card b { display: block; font-size: 34px; font-weight: 900; }
  .kl .card span { font-size: 15px; font-weight: 700; color: var(--muted); }
  .kl .card.an { box-shadow: 0 0 0 3px var(--c); }
  .kl .card.aus { opacity: .35; }
  .fz { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
  .fz span { display: inline-flex; align-items: center; gap: 8px; font-weight: 800; font-size: 15px; background: var(--card2); border-radius: 10px; padding: 6px 10px; }
  .fz i { width: 22px; height: 28px; border-radius: 4px; display: inline-block; border: 2px solid rgba(0,0,0,.25); }
  .mp { cursor: pointer; }
  html.light svg text[fill="#ffd34d"] { fill: #8a6400; }
  html.light .mp circle[stroke="#ffd34d"] { stroke: #c79400; }
  @media (max-width: 820px), (max-height: 520px) { .kl .card b { font-size: 26px; } .zz { grid-template-columns: repeat(2, 1fr) !important; } .zz svg { max-width: 72px !important; margin: 0 auto; } .val b { font-size: 14px; hyphens: auto; overflow-wrap: anywhere; } }'''


def massezeichen(x, y, w=22):
    return (f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 10}" stroke="{MI}" stroke-width="4"/>'
            f'<line x1="{x - w / 2}" y1="{y + 10}" x2="{x + w / 2}" y2="{y + 10}" stroke="{MI}" stroke-width="4"/>'
            f'<line x1="{x - w / 3}" y1="{y + 16}" x2="{x + w / 3}" y2="{y + 16}" stroke="{MI}" stroke-width="4"/>'
            f'<line x1="{x - w / 6}" y1="{y + 22}" x2="{x + w / 6}" y2="{y + 22}" stroke="{MI}" stroke-width="4"/>')


# ================================================================ 1 Aufbau
T = 'AUFBAU'


def auto_svg():
    def box(k, x, y, w, h, lab, fs=22):
        return (f'<g class="ab-bx" data-k="{k}" style="transition:opacity .3s"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/>'
                f'<text x="{x + w / 2}" y="{y + h / 2 + fs * 0.36}" text-anchor="middle" font-size="{fs}" font-weight="900" fill="#ecf1f8">{lab}</text></g>')
    pl = lambda d, w=6, g='': f'<path class="ab-ln" data-g="{g}" d="{d}" fill="none" stroke="{PL}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" style="transition:opacity .3s"/>'
    o = ['<svg viewBox="0 30 1000 350" width="1000" height="350" style="display:block;margin:0 auto;max-width:100%;height:auto" id="ab-svg">',
         '<path d="M20 300 Q30 180 180 165 L320 70 H650 L810 160 Q970 175 980 300 Z" fill="#213552" stroke="#94a4ba" stroke-width="4"/>',
         '<circle cx="200" cy="318" r="50" fill="#18283f" stroke="#94a4ba" stroke-width="8"/><circle cx="810" cy="318" r="50" fill="#18283f" stroke="#94a4ba" stroke-width="8"/>',
         # Plusleitungen
         pl('M190 200 V175 H430', 6, 'bus'), pl('M290 185 V175', 6, 'gen'), pl('M240 175 V282 H300', 10, 'st'),
         pl('M430 160 H42 V205', 4, 'sw'), pl('M540 165 H560 V140 H575', 4, 'ko'), pl('M540 182 H560 V205 H575', 4, 'gb'),
         pl('M520 195 V258 H940 V240', 4, 'rl'),
         # Masse
         f'<path d="M130 196 V176 H96" fill="none" stroke="{MI}" stroke-width="6"/>' + massezeichen(96, 176),
         f'<text x="84" y="196" text-anchor="end" font-size="15" font-weight="800" fill="{MI}">Masse</text>',
         # Bauteile
         f'<g class="ab-bx" data-k="bat" style="transition:opacity .3s"><rect x="110" y="200" width="100" height="52" rx="8" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/>'
         f'<rect x="120" y="193" width="20" height="9" fill="{MI}"/><rect x="180" y="193" width="20" height="9" fill="{PL}"/>'
         '<text x="160" y="234" text-anchor="middle" font-size="18" font-weight="900" fill="#ecf1f8">Batterie</text></g>',
         '<g class="ab-bx" data-k="gen" style="transition:opacity .3s"><circle cx="290" cy="215" r="30" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/><text x="290" y="223" text-anchor="middle" font-size="24" font-weight="900" fill="#ecf1f8">G</text>'
         '<text x="290" y="262" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Generator</text></g>',
         box('st', 300, 266, 84, 34, 'Starter', 17),
         box('si', 430, 150, 110, 48, 'Sicherungen', 16),
         box('ko', 575, 120, 130, 40, 'Kombi/Radio', 17),
         box('gb', 575, 185, 130, 40, 'Gebläse', 17),
         box('sw', 30, 205, 46, 34, '', 12) + '<text x="53" y="262" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Licht</text>',
         box('rl', 915, 205, 50, 34, '', 12) + '<text x="940" y="196" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Rückl.</text>',
         ]
    for n, d in [('aus', 'M190 200 V175 H430'), ('ko', 'M540 165 H560 V140 H575'), ('gb', 'M540 182 H560 V205 H575'),
                 ('rl', 'M520 198 V258 H940 V240'), ('sw', 'M430 160 H42 V205'), ('st', 'M190 200 V175 H240 V282 H300'),
                 ('lad', 'M290 185 V175 H190 V200'), ('gen', 'M290 185 V175 H430')]:
        o.append(f'<path id="ab-p-{n}" d="{d}" fill="none" stroke="none"/>')
    o.append('</svg>')
    return '\n    '.join(o)


def relais_svg():
    return f'''<svg viewBox="0 0 640 330" width="640" height="330" style="display:block;margin:0 auto;max-width:100%;height:auto" id="re-svg">
      <text x="20" y="34" font-size="16" font-weight="900" fill="#94a4ba">STEUERSTROMKREIS</text>
      <text x="360" y="34" font-size="16" font-weight="900" fill="#94a4ba">LASTSTROMKREIS</text>
      <line x1="40" y1="60" x2="600" y2="60" stroke="{PL}" stroke-width="5"/>
      <text x="44" y="52" font-size="16" font-weight="900" fill="{PL}">15</text><text x="580" y="52" font-size="16" font-weight="900" fill="{PL}">30</text>
      <line x1="100" y1="60" x2="100" y2="110" stroke="{PL}" stroke-width="3"/>
      <circle cx="100" cy="112" r="4" fill="#ecf1f8"/><line id="re-sch" x1="100" y1="112" x2="126" y2="150" stroke="#ecf1f8" stroke-width="4"/><circle cx="100" cy="160" r="4" fill="#ecf1f8"/>
      <text x="40" y="142" font-size="16" font-weight="900" fill="#ecf1f8">S1</text>
      <path d="M100 160 V180 H220 V190" fill="none" stroke="{PL}" stroke-width="3"/>
      <text x="228" y="186" font-size="14" font-weight="900" fill="#94a4ba">86</text>
      <rect x="200" y="190" width="40" height="60" rx="4" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/>
      <line x1="200" y1="250" x2="240" y2="190" stroke="#ecf1f8" stroke-width="2"/>
      <text x="228" y="270" font-size="14" font-weight="900" fill="#94a4ba">85</text>
      <path d="M220 250 V285" fill="none" stroke="{MI}" stroke-width="3"/>{massezeichen(220, 285)}
      <line x1="245" y1="220" x2="400" y2="220" stroke="#94a4ba" stroke-width="2" stroke-dasharray="6 6"/>
      <line x1="440" y1="60" x2="440" y2="150" stroke="{PL}" stroke-width="7"/><text x="450" y="140" font-size="14" font-weight="900" fill="#94a4ba">30</text>
      <circle cx="440" cy="152" r="5" fill="#ecf1f8"/><line id="re-kon" x1="440" y1="152" x2="470" y2="186" stroke="#ecf1f8" stroke-width="5"/><circle cx="440" cy="200" r="5" fill="#ecf1f8"/>
      <text x="450" y="226" font-size="14" font-weight="900" fill="#94a4ba">87</text>
      <text x="380" y="190" font-size="16" font-weight="900" fill="#ecf1f8">K1</text>
      <line x1="440" y1="200" x2="440" y2="236" stroke="{PL}" stroke-width="7"/>
      <circle id="re-lampe" cx="440" cy="262" r="24" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/>
      <line x1="423" y1="245" x2="457" y2="279" stroke="#ecf1f8" stroke-width="3"/><line x1="457" y1="245" x2="423" y2="279" stroke="#ecf1f8" stroke-width="3"/>
      <text x="476" y="268" font-size="16" font-weight="900" fill="#ecf1f8">Scheinwerfer</text>
      <path d="M440 286 V300" fill="none" stroke="{MI}" stroke-width="5"/>{massezeichen(440, 300, 28)}
      <path id="re-p1" d="M100 60 V110 M100 160 V180 H220 V250 V285" fill="none" stroke="none"/>
      <path id="re-p1a" d="M100 62 V180 H220 V284" fill="none" stroke="none"/>
      <path id="re-p2" d="M440 62 V286 V300" fill="none" stroke="none"/>
    </svg>'''


aufbau = [
    titel_folie(K, 'kl. 30', 'Aufbau des Bordnetzes', 'Batterie, Generator, Klemmen, Sicherungen und Relais', 'font-size:64px'),
    lernziele(T, ['Welche Teile zum Bordnetz gehören', 'Wie die Energie bei Motor aus, beim Start und bei laufendem Motor fließt',
                  'Was die Klemmenbezeichnungen 30, 15, 31, 50 und 75 bedeuten', 'Wie Sicherung und Relais arbeiten']),
    folie(T, 'Das Bordnetz im Fahrzeug – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap"><button class="btn ghost on" data-m="aus">Motor aus</button><button class="btn ghost" data-m="st">Motor startet</button><button class="btn ghost" data-m="an">Motor läuft</button></div>
    {auto_svg()}
    <div class="card" id="ab-t" style="font-size:17px;font-weight:600;line-height:1.5;margin-top:8px"></div>
    <p class="muted" style="font-size:14px;margin:6px 0 0"><span style="color:{PL};font-weight:800">Rot = Plus</span> · <span style="color:{MI};font-weight:800">Blau = Masse (Minus)</span> · gelbe Punkte = Strom (technische Stromrichtung). Vereinfachte Darstellung.</p>''', sid='s-ab', body_cls='body noclick'),
    folie(T, 'Die Klemmen am Zündschloss – zum Ausprobieren', '''    <div class="choice" style="margin-bottom:12px;flex-wrap:wrap"><button class="btn ghost on" data-z="0">Schlüssel abgezogen</button><button class="btn ghost" data-z="1">Zündung an</button><button class="btn ghost" data-z="2">Starten</button></div>
    <div class="kl">
      <div class="card" data-k="30"><b>30</b><span>Dauerplus<br>direkt von der Batterie</span></div>
      <div class="card" data-k="15"><b>15</b><span>Zündungsplus<br>nur bei Zündung an</span></div>
      <div class="card" data-k="75"><b>75</b><span>Entlastung<br>beim Starten aus</span></div>
      <div class="card" data-k="50"><b>50</b><span>Starter<br>nur beim Starten</span></div>
      <div class="card" data-k="31"><b style="color:var(--blu)">31</b><span>Masse<br>Rückleitung zum Minuspol</span></div>
    </div>
    <div class="card" id="kz-t" style="font-size:17px;font-weight:600;line-height:1.5;margin-top:12px"></div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Klemmenbezeichnungen nach DIN 72552. In neueren Fahrzeugen schaltet oft ein Steuergerät die Klemmen (z. B. bei Start-Knopf).</p>''', sid='s-kz', body_cls='body noclick'),
    folie(T, 'Weitere wichtige Klemmen', '''    <div class="values">
      <div class="val step from-left"><b>61</b><span>Ladekontrolle – Leuchte im Kombiinstrument</span></div>
      <div class="val step from-left"><b>B+ / D+</b><span>Generator: B+ zur Batterie, D+ für die Ladekontrolle</span></div>
      <div class="val step from-left"><b>56 · 56a · 56b</b><span>Scheinwerfer · Fernlicht · Abblendlicht</span></div>
      <div class="val step from-left"><b>58</b><span>Standlicht, Rückleuchten, Kennzeichenleuchte</span></div>
      <div class="val step from-left"><b>85 · 86 · 30 · 87</b><span>Relais: Spule (85, 86) – Schaltkontakt (30 Eingang, 87 Ausgang)</span></div>
    </div>'''),
    folie(T, 'Sicherungen', f'''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Aufgabe</div>
        <ul UL><li>schützt die <b>Leitung</b> vor zu großem Strom (Kurzschluss, Überlast)</li><li>bei zu großem Strom schmilzt der Draht – der Stromkreis ist unterbrochen</li><li>Wert in Ampere steht drauf, die Farbe zeigt ihn auch</li></ul>
        <div class="fz">
          <span><i style="background:#c8a46a"></i>5 A</span><span><i style="background:#8b5a2b"></i>7,5 A</span><span><i style="background:#e03c31"></i>10 A</span>
          <span><i style="background:#2a6fdb"></i>15 A</span><span><i style="background:#f2c200"></i>20 A</span><span><i style="background:#f4f4f4"></i>25 A</span><span><i style="background:#2fa84f"></i>30 A</span>
        </div>
        <p class="muted" style="font-size:14px;margin:6px 0 0">Übliche Farben bei Flachsicherungen.</p></div>
      <div class="card step"><div class="big" style="font-size:22px">Prüfen</div>
        <ul UL><li>Sichtprüfung reicht nicht immer – feine Risse sieht man schlecht</li><li>besser: Stromkreis einschalten und an <b>beiden Prüfpunkten</b> der Sicherung gegen Masse messen</li><li>beide Seiten Batteriespannung: Sicherung in Ordnung</li><li>eine Seite 0 V: Sicherung defekt</li></ul></div>
    </div>
    <div class="warn step" style="margin-top:10px"><b>Nie stärker absichern</b>Eine durchgebrannte Sicherung hat einen Grund – erst die Ursache suchen. Nie eine stärkere Sicherung oder einen Draht einsetzen: Die Leitung kann glühen und brennen.</div>'''.replace('UL', UL)),
    folie(T, 'Das Relais – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px"><button class="btn ghost" id="re-b">Schalter S1 drücken</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {relais_svg()}
      <div>
        <div class="grid2" style="gap:10px"><div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">STEUERSTROM</div><div class="lcd2" id="re-i1" style="font-size:26px">0 A</div></div>
        <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">LASTSTROM</div><div class="lcd2" id="re-i2" style="font-size:26px">0 A</div></div></div>
        <div class="card" id="re-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Beispielwerte. Dünne Linie = kleiner Strom, dicke Linie = großer Strom.</p>''', sid='s-re', body_cls='body noclick'),
    folie(T, 'Masse – der unterschätzte Rückweg', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">So ist es aufgebaut</div>
        <ul UL><li>Batterie-Minus ist mit der Karosserie verbunden</li><li>ein Masseband verbindet Motor und Karosserie</li><li>viele Verbraucher haben ihre Masse an einem Massepunkt der Karosserie</li><li>der Strom fließt über die Masse zurück zum Minuspol</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Typische Fehler</div>
        <ul UL><li>Korrosion oder lockere Schraube am Massepunkt</li><li>es entsteht ein <b>Übergangswiderstand</b></li><li>Folge: Lampen leuchten schwach, Motoren laufen langsam, merkwürdige Fehler in Steuergeräten</li></ul></div>
    </div>
    <div class="tip step" style="margin-top:10px"><b>Prüfen</b>Verbraucher einschalten und den Spannungsfall zwischen Batterie-Minus und Masse des Verbrauchers messen. Richtwert: wenige Zehntel Volt – genauer Wert laut Hersteller.</div>'''.replace('UL', UL)),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Batterie abklemmen</b>Erst Minus, dann Plus abklemmen. Beim Anklemmen umgekehrt: erst Plus, dann Minus. So gibt es keinen Kurzschluss, wenn das Werkzeug die Karosserie berührt.</div>
      <div class="tip step"><b>Vor dem Abklemmen</b>Herstellervorgaben beachten: z. B. Fensterheber neu anlernen, Radiocode bereithalten, Batterie nach dem Tausch anlernen.</div>
      <div class="tip step"><b>Nachrüsten</b>Zusätzliche Verbraucher immer mit eigener Sicherung und passendem Leitungsquerschnitt anschließen.</div>
      <div class="warn step"><b>Nicht anstechen</b>Leitungen nicht anstechen und nicht von vorne in Stecker messen – nur mit Prüfadapter.</div>
    </div>'''),
    video(T, 'bn-aufbau'),
    kurztest(T, [
        ('Was bedeutet Klemme 30?', ['Dauerplus direkt von der Batterie', 'Masse', 'Zündungsplus'], 0, 'Klemme 30 führt immer Spannung – auch bei abgezogenem Schlüssel.'),
        ('Wann liegt an Klemme 15 Spannung an?', ['Immer', 'Nur bei eingeschalteter Zündung', 'Nur beim Starten'], 1, 'Klemme 15 = Zündungsplus.'),
        ('Warum schaltet man Scheinwerfer über ein Relais?', ['Damit sie heller sind', 'Damit sie blinken', 'Der Schalter muss nur einen kleinen Steuerstrom schalten'], 2, 'Der große Laststrom fließt über den Relaiskontakt 30 → 87.'),
        ('Eine Sicherung brennt immer wieder durch. Was tust du?', ['Ursache suchen, z. B. einen Kurzschluss', 'Eine stärkere Sicherung einsetzen', 'Einen Draht einsetzen'], 0, 'Die Sicherung schützt die Leitung – stärker absichern ist Brandgefahr.'),
    ]),
    merke(T, ['Motor aus: Batterie versorgt|Motor läuft: Generator versorgt und lädt', '30 Dauerplus · 15 Zündung · 31 Masse · 50 Starter',
              'Sicherung schützt die Leitung – nie stärker absichern', 'Relais: kleiner Steuerstrom schaltet großen Laststrom']),
]
aufbau_js = '''<script src="assets/schaltung.js"></script>
<script>
(function () {
  const svg = document.getElementById('ab-svg');
  const F = {};
  ['aus', 'ko', 'gb', 'rl', 'sw', 'st', 'lad', 'gen'].forEach(n => F[n] = Flow(svg, document.getElementById('ab-p-' + n), { spacing: n === 'st' ? 14 : 26, speed: n === 'st' ? 110 : 55, r: n === 'st' ? 7 : 6, color: '#ffd34d' }));
  const M = {
    aus: { f: ['aus', 'ko', 'rl'], b: ['bat', 'si', 'ko', 'rl'], l: ['bus', 'ko', 'rl'],
      t: '<b>Motor aus:</b> Nur die <span class="c">Batterie</span> liefert Strom – z. B. für Radio, Standlicht und Steuergeräte, die noch arbeiten. Darum wird die Batterie bei langem Stehen leer.' },
    st: { f: ['st', 'aus', 'ko'], b: ['bat', 'st', 'si', 'ko'], l: ['bus', 'st', 'ko'],
      t: '<b>Motor startet:</b> Der <span class="c">Starter</span> bekommt über eine dicke Leitung einen sehr großen Strom direkt von der Batterie (einige 100 A, Richtwert). Große Verbraucher wie das Gebläse werden dabei abgeschaltet (Klemme 75).' },
    an: { f: ['lad', 'gen', 'ko', 'gb', 'rl', 'sw'], b: ['gen', 'bat', 'si', 'ko', 'gb', 'rl', 'sw'], l: ['bus', 'gen', 'ko', 'gb', 'rl', 'sw'],
      t: '<b>Motor läuft:</b> Der <span class="c">Generator</span> versorgt alle Verbraucher und <span class="c">lädt die Batterie</span> wieder auf. Ladespannung ca. 14 V (Richtwert laut Hersteller).' }
  };
  const bt = document.querySelectorAll('#s-ab [data-m]');
  function m(n) {
    const x = M[n];
    Object.keys(F).forEach(k => F[k].on(x.f.includes(k)));
    document.querySelectorAll('#s-ab .ab-bx').forEach(g => g.style.opacity = x.b.includes(g.dataset.k) ? 1 : 0.35);
    document.querySelectorAll('#s-ab .ab-ln').forEach(l => l.style.opacity = x.l.includes(l.dataset.g) ? 1 : 0.25);
    bt.forEach(b => b.classList.toggle('on', b.dataset.m === n));
    document.getElementById('ab-t').innerHTML = x.t;
  }
  bt.forEach(b => b.onclick = () => m(b.dataset.m)); m('aus');

  // Klemmen
  const KZ = [
    { an: ['30', '31'], t: '<b>Schlüssel abgezogen:</b> Nur <span class="c">Klemme 30</span> führt Spannung – z. B. für Warnblinker, Innenlicht und Diebstahlwarnanlage. Klemme 31 ist die Masse, sie ist immer da.' },
    { an: ['30', '15', '75', '31'], t: '<b>Zündung an:</b> Jetzt kommen <span class="c">Klemme 15</span> (Zündungsplus, z. B. Motorsteuergerät, Kombiinstrument) und <span class="c">Klemme 75</span> (Entlastung, z. B. Gebläse, Radio) dazu.' },
    { an: ['30', '15', '50', '31'], t: '<b>Starten:</b> <span class="c">Klemme 50</span> steuert den Starter an. <span class="c">Klemme 75 schaltet ab</span> – so bleibt mehr Strom für den Starter. Nach dem Loslassen ist Klemme 50 wieder aus und 75 wieder an.' }
  ];
  const zb = document.querySelectorAll('#s-kz [data-z]'), kc = document.querySelectorAll('#s-kz .kl .card');
  function z(i) {
    kc.forEach(c => { const an = KZ[i].an.includes(c.dataset.k); c.classList.toggle('an', an); c.classList.toggle('aus', !an); });
    zb.forEach(b => b.classList.toggle('on', +b.dataset.z === i));
    document.getElementById('kz-t').innerHTML = KZ[i].t;
  }
  zb.forEach(b => b.onclick = () => z(+b.dataset.z)); z(0);

  // Relais
  const rs = document.getElementById('re-svg');
  const f1 = Flow(rs, document.getElementById('re-p1a'), { spacing: 30, speed: 50, r: 4, color: '#ffd34d' });
  const f2 = Flow(rs, document.getElementById('re-p2'), { spacing: 16, speed: 70, r: 7, color: '#ffd34d' });
  let an = false;
  function r() {
    const sch = document.getElementById('re-sch'), kon = document.getElementById('re-kon');
    sch.setAttribute('x2', an ? 100 : 126); sch.setAttribute('y2', an ? 158 : 150);
    kon.setAttribute('x2', an ? 440 : 470); kon.setAttribute('y2', an ? 198 : 186);
    document.getElementById('re-lampe').setAttribute('fill', an ? '#ffd34d' : '#18283f');
    f1.on(an); f2.on(an);
    document.getElementById('re-i1').textContent = an ? '0,15 A' : '0 A';
    document.getElementById('re-i2').textContent = an ? '10 A' : '0 A';
    document.getElementById('re-b').textContent = an ? 'Schalter S1 loslassen' : 'Schalter S1 drücken';
    document.getElementById('re-b').classList.toggle('on', an);
    document.getElementById('re-t').innerHTML = an
      ? '<b>Ein:</b> Durch die Spule (86 → 85) fließt ein <span class="c">kleiner Steuerstrom</span>. Sie wird zum Magneten und zieht den Kontakt an: Der <span class="c">große Laststrom</span> fließt von 30 nach 87 zum Scheinwerfer.'
      : '<b>Aus:</b> Kein Strom durch die Spule, der Kontakt 30 → 87 ist offen. Der Scheinwerfer ist aus. Der Schalter muss später nur den kleinen Steuerstrom schalten – er bleibt klein und hält lange.';
  }
  document.getElementById('re-b').onclick = () => { an = !an; r(); }; r();
})();
</script>'''


# ================================================================ 2 Stromlaufplan
T = 'STROMLAUFPLAN'


def plan_svg():
    return f'''<svg viewBox="0 0 520 330" width="520" height="330" style="display:block;margin:0 auto;max-width:100%;height:auto">
      <line x1="30" y1="40" x2="500" y2="40" stroke="{PL}" stroke-width="5"/><text x="8" y="46" font-size="18" font-weight="900" fill="{PL}">30</text>
      <line x1="30" y1="76" x2="500" y2="76" stroke="{PL}" stroke-width="5"/><text x="8" y="82" font-size="18" font-weight="900" fill="{PL}">15</text>
      <line x1="30" y1="282" x2="500" y2="282" stroke="{MI}" stroke-width="5"/><text x="8" y="288" font-size="18" font-weight="900" fill="{MI}">31</text>
      <line x1="120" y1="40" x2="120" y2="96" stroke="#ecf1f8" stroke-width="3"/>
      <rect x="110" y="96" width="20" height="40" rx="3" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/><line x1="120" y1="96" x2="120" y2="136" stroke="#ecf1f8" stroke-width="2"/>
      <text x="138" y="122" font-size="16" font-weight="900" fill="#ecf1f8">F1</text>
      <line x1="120" y1="136" x2="120" y2="170" stroke="#ecf1f8" stroke-width="3"/>
      <circle cx="120" cy="172" r="4" fill="#ecf1f8"/><line x1="120" y1="172" x2="140" y2="204" stroke="#ecf1f8" stroke-width="3"/><circle cx="120" cy="210" r="4" fill="#ecf1f8"/>
      <text x="146" y="196" font-size="16" font-weight="900" fill="#ecf1f8">S1</text>
      <line x1="120" y1="210" x2="120" y2="226" stroke="#ecf1f8" stroke-width="3"/>
      <circle cx="120" cy="246" r="18" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/>
      <line x1="107" y1="233" x2="133" y2="259" stroke="#ecf1f8" stroke-width="2"/><line x1="133" y1="233" x2="107" y2="259" stroke="#ecf1f8" stroke-width="2"/>
      <text x="146" y="252" font-size="16" font-weight="900" fill="#ecf1f8">E1</text>
      <line x1="120" y1="264" x2="120" y2="282" stroke="#ecf1f8" stroke-width="3"/>
      <line x1="330" y1="76" x2="330" y2="130" stroke="#ecf1f8" stroke-width="3"/>
      <rect x="310" y="130" width="40" height="60" rx="4" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/><line x1="310" y1="190" x2="350" y2="130" stroke="#ecf1f8" stroke-width="2"/>
      <text x="358" y="166" font-size="16" font-weight="900" fill="#ecf1f8">K1</text>
      <line x1="330" y1="190" x2="330" y2="282" stroke="#ecf1f8" stroke-width="3"/>
      <line x1="440" y1="40" x2="440" y2="150" stroke="#ecf1f8" stroke-width="3"/>
      <circle cx="440" cy="152" r="4" fill="#ecf1f8"/><line x1="440" y1="152" x2="462" y2="184" stroke="#ecf1f8" stroke-width="3"/><circle cx="440" cy="190" r="4" fill="#ecf1f8"/>
      <line x1="354" y1="168" x2="436" y2="168" stroke="#94a4ba" stroke-width="2" stroke-dasharray="5 5"/>
      <line x1="440" y1="190" x2="440" y2="214" stroke="#ecf1f8" stroke-width="3"/>
      <circle cx="440" cy="236" r="22" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/><text x="440" y="243" text-anchor="middle" font-size="20" font-weight="900" fill="#ecf1f8">M</text>
      <text x="470" y="242" font-size="16" font-weight="900" fill="#ecf1f8">M1</text>
      <line x1="440" y1="258" x2="440" y2="282" stroke="#ecf1f8" stroke-width="3"/>
      <text x="200" y="232" font-size="13" font-weight="800" fill="#94a4ba">1,0 gr/sw</text>
      <text x="120" y="318" text-anchor="middle" font-size="16" font-weight="900" fill="#94a4ba">1</text>
      <text x="330" y="318" text-anchor="middle" font-size="16" font-weight="900" fill="#94a4ba">2</text>
      <text x="440" y="318" text-anchor="middle" font-size="16" font-weight="900" fill="#94a4ba">3</text>
      <line x1="30" y1="298" x2="500" y2="298" stroke="#94a4ba" stroke-width="1"/>
    </svg>'''


def zeichen(sym, lab, kb):
    return f'<div class="card step" style="margin:0;text-align:center"><svg viewBox="0 0 80 60" width="80" height="60">{sym}</svg><div style="font-weight:800">{lab}</div><div class="muted" style="font-size:14px">z. B. {kb}</div></div>'


W = '#ecf1f8'
ZEICHEN = [
    zeichen(f'<line x1="10" y1="30" x2="32" y2="30" stroke="{W}" stroke-width="3"/><line x1="32" y1="14" x2="32" y2="46" stroke="{W}" stroke-width="4"/><line x1="42" y1="22" x2="42" y2="38" stroke="{W}" stroke-width="8"/><line x1="42" y1="30" x2="70" y2="30" stroke="{W}" stroke-width="3"/>', 'Batterie', 'G1'),
    zeichen(f'<line x1="5" y1="30" x2="20" y2="30" stroke="{W}" stroke-width="3"/><rect x="20" y="20" width="40" height="20" rx="3" fill="none" stroke="{W}" stroke-width="3"/><line x1="20" y1="30" x2="60" y2="30" stroke="{W}" stroke-width="2"/><line x1="60" y1="30" x2="75" y2="30" stroke="{W}" stroke-width="3"/>', 'Sicherung', 'F1'),
    zeichen(f'<line x1="5" y1="40" x2="22" y2="40" stroke="{W}" stroke-width="3"/><line x1="22" y1="40" x2="55" y2="20" stroke="{W}" stroke-width="3"/><line x1="58" y1="40" x2="75" y2="40" stroke="{W}" stroke-width="3"/><circle cx="22" cy="40" r="3" fill="{W}"/>', 'Schalter', 'S1'),
    zeichen(f'<rect x="25" y="10" width="30" height="40" rx="3" fill="none" stroke="{W}" stroke-width="3"/><line x1="25" y1="50" x2="55" y2="10" stroke="{W}" stroke-width="2"/>', 'Relais (Spule)', 'K1'),
    zeichen(f'<circle cx="40" cy="30" r="17" fill="none" stroke="{W}" stroke-width="3"/><line x1="28" y1="18" x2="52" y2="42" stroke="{W}" stroke-width="2"/><line x1="52" y1="18" x2="28" y2="42" stroke="{W}" stroke-width="2"/>', 'Lampe', 'E1'),
    zeichen(f'<circle cx="40" cy="30" r="18" fill="none" stroke="{W}" stroke-width="3"/><text x="40" y="38" text-anchor="middle" font-size="20" font-weight="900" fill="{W}">M</text>', 'Motor', 'M1'),
    zeichen(f'<line x1="5" y1="30" x2="22" y2="30" stroke="{W}" stroke-width="3"/><rect x="22" y="22" width="36" height="16" fill="none" stroke="{W}" stroke-width="3"/><line x1="58" y1="30" x2="75" y2="30" stroke="{W}" stroke-width="3"/>', 'Widerstand', 'R1'),
    zeichen(massezeichen(40, 14, 34), 'Masse', 'Klemme 31'),
]


def mess_svg():
    pts = [('P1', 160, 64, 136, 70, 'end'), ('P2', 160, 156, 136, 162, 'end'), ('P3', 160, 236, 136, 242, 'end'),
           ('P4', 262, 236, 262, 212, 'middle'), ('P5', 380, 310, 356, 316, 'end')]
    mp = ''.join(f'<g class="mp" data-p="{i}"><circle cx="{x}" cy="{y}" r="15" fill="#213552" stroke="#ffd34d" stroke-width="3"/><text x="{lx}" y="{ly}" text-anchor="{an}" font-size="16" font-weight="900" fill="#ffd34d">{n}</text></g>'
                 for i, (n, x, y, lx, ly, an) in enumerate(pts))
    return f'''<svg viewBox="0 0 460 400" width="460" height="400" style="display:block;margin:0 auto;max-width:100%;height:auto" id="ms-svg">
      <line x1="40" y1="40" x2="440" y2="40" stroke="{PL}" stroke-width="5"/><text x="46" y="30" font-size="16" font-weight="900" fill="{PL}">30</text>
      <line x1="40" y1="372" x2="440" y2="372" stroke="{MI}" stroke-width="5"/><text x="46" y="394" font-size="16" font-weight="900" fill="{MI}">31</text>
      <line x1="160" y1="40" x2="160" y2="90" stroke="{PL}" stroke-width="4"/>
      <rect id="ms-f" x="148" y="90" width="24" height="44" rx="4" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/><line id="ms-fd" x1="160" y1="90" x2="160" y2="134" stroke="#ecf1f8" stroke-width="2"/>
      <text x="184" y="118" font-size="16" font-weight="900" fill="#ecf1f8">F1 10 A</text>
      <line x1="160" y1="134" x2="160" y2="180" stroke="{PL}" stroke-width="4"/>
      <circle cx="160" cy="182" r="4" fill="#ecf1f8"/><line x1="160" y1="182" x2="160" y2="214" stroke="#ecf1f8" stroke-width="4"/><circle cx="160" cy="214" r="4" fill="#ecf1f8"/>
      <text x="184" y="204" font-size="16" font-weight="900" fill="#ecf1f8">S1 (ein)</text>
      <path id="ms-l1" d="M160 214 V236 H304" fill="none" stroke="{PL}" stroke-width="4"/>
      <g id="ms-bruch" style="display:none"><line x1="204" y1="226" x2="218" y2="246" stroke="#ffd34d" stroke-width="4"/><line x1="218" y1="226" x2="204" y2="246" stroke="#ffd34d" stroke-width="4"/></g>
      <circle id="ms-lampe" cx="330" cy="236" r="26" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/>
      <line id="ms-w1" x1="312" y1="218" x2="348" y2="254" stroke="#ecf1f8" stroke-width="3"/><line id="ms-w2" x1="348" y1="218" x2="312" y2="254" stroke="#ecf1f8" stroke-width="3"/>
      <text x="330" y="200" text-anchor="middle" font-size="16" font-weight="900" fill="#ecf1f8">E1</text>
      <path d="M356 236 H380 V372" fill="none" stroke="{MI}" stroke-width="4"/>
      <g id="ms-masse" style="display:none"><circle cx="380" cy="345" r="14" fill="none" stroke="#ffd34d" stroke-width="4"/></g>
      {mp}
      <text x="392" y="280" font-size="13" font-weight="800" fill="#94a4ba">Masse-</text><text x="392" y="296" font-size="13" font-weight="800" fill="#94a4ba">seite</text>
    </svg>'''


def sf_svg():
    return f'''<svg viewBox="0 0 520 240" width="520" height="240" style="display:block;margin:0 auto;max-width:100%;height:auto" id="sf-svg">
      <rect x="20" y="90" width="90" height="60" rx="8" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/><text x="65" y="128" text-anchor="middle" font-size="18" font-weight="900" fill="#ecf1f8">12,5 V</text>
      <rect x="92" y="80" width="14" height="10" fill="{PL}"/><rect x="24" y="80" width="14" height="10" fill="{MI}"/>
      <path d="M99 80 V50 H400 V100" fill="none" stroke="{PL}" stroke-width="5"/>
      <g><rect x="230" y="38" width="40" height="24" rx="4" fill="#ffd34d"/><text x="250" y="84" text-anchor="middle" font-size="13" font-weight="800" fill="#ffd34d">Übergangswiderstand</text></g>
      <circle id="sf-l" cx="400" cy="124" r="24" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/>
      <line x1="383" y1="107" x2="417" y2="141" stroke="#ecf1f8" stroke-width="3"/><line x1="417" y1="107" x2="383" y2="141" stroke="#ecf1f8" stroke-width="3"/>
      <path d="M400 148 V200 H8 V66 H31 V80" fill="none" stroke="{MI}" stroke-width="5"/>
      <path id="sf-p" d="M99 80 V50 H400 V148 V200 H8 V66 H31 V80" fill="none" stroke="none"/>
      <path d="M120 50 Q120 10 160 10 H360 Q400 10 400 40" fill="none" stroke="#94a4ba" stroke-width="2" stroke-dasharray="5 5"/>
      <text x="260" y="226" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Multimeter von Batterie-Plus bis Verbraucher-Plus (gestrichelt)</text>
    </svg>'''


plan = [
    titel_folie(K, 'F1·K1', 'Stromlaufplan und Fehlersuche', 'Pläne lesen und Fehler gezielt finden', 'font-size:56px'),
    lernziele(T, ['Wie ein Stromlaufplan aufgebaut ist', 'Was Schaltzeichen und Kennbuchstaben bedeuten',
                  'Wie du entlang des Stromwegs misst', 'Wie du Unterbrechung, Masse- und Übergangsfehler findest']),
    folie(T, 'So ist ein Stromlaufplan aufgebaut', f'''    <div class="grid2" style="align-items:center;grid-template-columns:1.1fr 1fr">
      {plan_svg()}
      <ol class="steps-list">
        <li class="step">Oben Plus, unten Masse<small>oben Klemme 30 und 15, unten Klemme 31</small></li>
        <li class="step">Strompfade senkrecht<small>von oben (Plus) nach unten (Masse) – unten stehen die Strompfad-Nummern</small></li>
        <li class="step">Ruhestellung<small>Schalter und Relais sind so gezeichnet, wie sie bei Zündung aus stehen</small></li>
        <li class="step">Leitungen beschriftet<small>z. B. „1,0 gr/sw“ = 1,0 mm², grau mit schwarzem Streifen</small></li>
      </ol>
    </div>'''),
    folie(T, 'Schaltzeichen und Kennbuchstaben', '''    <div class="zz" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px">
      ''' + '\n      '.join(ZEICHEN) + '''
    </div>
    <div class="note step" style="margin-top:12px">Kennbuchstaben nach DIN. Viele Hersteller verwenden eigene Buchstaben (z. B. VW: S = Sicherung, J = Steuergerät oder Relais). Immer die Legende des Stromlaufplans lesen.</div>'''),
    folie(T, 'Messen im Stromkreis – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:8px;flex-wrap:wrap;gap:6px" id="ms-fb"><button class="btn ghost on" data-f="ok">In Ordnung</button><button class="btn ghost" data-f="sich">Sicherung defekt</button><button class="btn ghost" data-f="leit">Leitung unterbrochen</button><button class="btn ghost" data-f="lampe">Lampe defekt</button><button class="btn ghost" data-f="mu">Masse unterbrochen</button><button class="btn ghost" data-f="mk">Masse korrodiert</button><button class="btn" data-f="zufall" style="--c:var(--yel)">? Zufallsfehler</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1fr 1fr">
      {mess_svg()}
      <div>
        <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">MULTIMETER (SCHWARZ AN MASSE)</div><div class="lcd2" id="ms-v" style="font-size:34px;margin-top:4px">–</div><div class="muted" id="ms-p" style="font-size:15px;font-weight:700">Tippe auf einen Messpunkt P1 … P5</div></div>
        <div class="card" id="ms-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Schalter S1 ist eingeschaltet. Gemessen wird gegen Masse. Beispielwerte.</p>''', sid='s-ms', body_cls='body noclick'),
    folie(T, 'Fehlersuche Schritt für Schritt', '''    <ol class="steps-list">
      <li class="step">Beanstandung prüfen<small>Was genau geht nicht? Immer, oder nur manchmal?</small></li>
      <li class="step">Stromlaufplan für genau dieses Fahrzeug holen<small>Strompfad suchen: Sicherung, Schalter, Relais, Verbraucher, Masse</small></li>
      <li class="step">Sicherung und Sichtprüfung<small>Stecker, Leitungen, Massepunkte ansehen</small></li>
      <li class="step">Spannung messen – von Plus Richtung Verbraucher<small>wo die Spannung wegfällt, liegt die Unterbrechung davor</small></li>
      <li class="step">Masse prüfen<small>liegt auf der Masseseite des Verbrauchers Spannung an, fehlt die Masse</small></li>
      <li class="step">Reparieren und Funktion prüfen<small>danach Fehlerspeicher lesen und löschen</small></li>
    </ol>'''),
    folie(T, 'Spannungsfall unter Last – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px"><button class="btn ghost on" data-l="0">Verbraucher aus</button><button class="btn ghost" data-l="1">Verbraucher ein</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {sf_svg()}
      <div>
        <div class="grid2" style="gap:10px"><div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">AM VERBRAUCHER</div><div class="lcd2" id="sf-u" style="font-size:26px">12,5 V</div></div>
        <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">SPANNUNGSFALL LEITUNG</div><div class="lcd2" id="sf-d" style="font-size:26px">0,0 V</div></div></div>
        <div class="card" id="sf-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Beispielwerte. Zulässiger Spannungsfall: wenige Zehntel Volt – genauer Wert laut Hersteller.</p>''', sid='s-sf', body_cls='body noclick'),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Richtiger Plan</b>Den Stromlaufplan genau für dieses Fahrzeug verwenden (Fahrgestellnummer, Ausstattung). Pläne ähnlicher Modelle können abweichen.</div>
      <div class="tip step"><b>Stecker sind häufig schuld</b>Korrosion, aufgeweitete oder herausgerutschte Kontakte. Kontakte nur mit passendem Prüfkontakt prüfen.</div>
      <div class="tip step"><b>Fehler nur manchmal?</b>Während der Messung an Leitungen und Steckern leicht wackeln (Wackeltest) – so findest du Wackelkontakte.</div>
      <div class="warn step"><b>Messung ohne Last täuscht</b>Ein Übergangswiderstand fällt ohne Strom nicht auf. Darum Spannung und Spannungsfall immer mit eingeschaltetem Verbraucher messen.</div>
    </div>'''),
    video(T, 'bn-stromlaufplan'),
    kurztest(T, [
        ('Was steht im Stromlaufplan oben?', ['Masse (Klemme 31)', 'Plus (z. B. Klemme 30 und 15)', 'Die Strompfad-Nummern'], 1, 'Oben Plus, unten Masse – die Strompfade laufen von oben nach unten.'),
        ('Lampe aus. An beiden Anschlüssen der Lampe misst du 12,5 V gegen Masse. Was ist defekt?', ['Die Masse der Lampe ist unterbrochen', 'Die Sicherung', 'Alles in Ordnung'], 0, 'Ohne Masse fließt kein Strom – die Spannung „steht“ auf beiden Seiten.'),
        ('Warum misst du den Spannungsfall unter Last?', ['Weil das Multimeter sonst kaputt geht', 'Weil die Batterie sonst leer wird', 'Ohne Strom fällt ein Übergangswiderstand nicht auf'], 2, 'Erst wenn Strom fließt, fällt am Übergangswiderstand Spannung ab.'),
        ('Was bedeutet die Leitungsangabe „1,5 rt“?', ['1,5 mm², rot', '1,5 A, rot', '1,5 m lang, rot'], 0, 'Querschnitt in mm² und Farbe.'),
    ]),
    merke(T, ['Oben Plus, unten Masse|Strompfade von oben nach unten', 'Von Plus Richtung Verbraucher messen|wo die Spannung fehlt, liegt der Fehler davor',
              'Spannung auf der Masseseite = Masse fehlt', 'Spannungsfall immer unter Last messen']),
]
plan_js = '''<script src="assets/schaltung.js"></script>
<script>
(function () {
  const V = {
    ok: [[12.5, 12.5, 12.4, 12.3, 0.1], 1, '<b class="grn">In Ordnung:</b> Die Spannung kommt bis zur Lampe an (P4 ca. 12,3 V), auf der Masseseite (P5) fast 0 V. Die Lampe leuchtet.'],
    sich: [[12.5, 0, 0, 0, 0], 0, '<b class="red">Sicherung defekt:</b> Vor der Sicherung (P1) 12,5 V, dahinter (P2) 0 V. Ursache für das Durchbrennen suchen!'],
    leit: [[12.5, 12.5, 12.5, 0, 0], 0, '<b class="red">Leitung unterbrochen:</b> Am Schalter (P3) noch 12,5 V, an der Lampe (P4) 0 V. Die Unterbrechung liegt zwischen P3 und P4.'],
    lampe: [[12.5, 12.5, 12.5, 12.5, 0], 0, '<b class="red">Lampe defekt:</b> Vor der Lampe 12,5 V, dahinter 0 V – die Spannung „verschwindet“ in der Lampe. Glühfaden unterbrochen.'],
    mu: [[12.5, 12.5, 12.5, 12.5, 12.5], 0, '<b class="red">Masse unterbrochen:</b> Auf beiden Seiten der Lampe 12,5 V! Es fließt kein Strom, darum fällt an der Lampe keine Spannung ab. Masseleitung und Massepunkt prüfen.'],
    mk: [[12.5, 12.5, 12.4, 12.4, 4.2], 0.35, '<b class="ora">Masse korrodiert:</b> Die Lampe leuchtet schwach. Auf der Masseseite (P5) liegen 4,2 V statt fast 0 V – am Massepunkt fällt zu viel Spannung ab (Übergangswiderstand).']
  };
  const NAMEN = { ok: 'In Ordnung', sich: 'Sicherung defekt', leit: 'Leitung unterbrochen', lampe: 'Lampe defekt', mu: 'Masse unterbrochen', mk: 'Masse korrodiert' };
  let f = 'ok', geheim = false, p = -1;
  const fb = document.querySelectorAll('#ms-fb [data-f]');
  const fmt = v => v.toFixed(1).replace('.', ',') + ' V';
  function zeichne() {
    const w = V[f], hell = w[1];
    document.getElementById('ms-lampe').setAttribute('fill', hell ? (hell < 1 ? '#7a6a2a' : '#ffd34d') : '#18283f');
    const zeig = !geheim;
    document.getElementById('ms-bruch').style.display = zeig && f === 'leit' ? '' : 'none';
    document.getElementById('ms-masse').style.display = zeig && (f === 'mu' || f === 'mk') ? '' : 'none';
    document.getElementById('ms-fd').style.display = zeig && f === 'sich' ? 'none' : '';
    document.getElementById('ms-w1').setAttribute('stroke-dasharray', zeig && f === 'lampe' ? '6 8' : '');
    document.getElementById('ms-v').textContent = p < 0 ? '–' : fmt(w[0][p]);
    document.getElementById('ms-p').textContent = p < 0 ? 'Tippe auf einen Messpunkt P1 … P5' : 'P' + (p + 1) + ' gegen Masse';
    document.querySelectorAll('#ms-svg .mp circle').forEach((c, i) => c.setAttribute('fill', i === p ? '#ffd34d' : '#213552'));
    document.getElementById('ms-t').innerHTML = geheim
      ? '<b class="yel">Zufallsfehler:</b> Miss an den Punkten P1 bis P5. Wenn du weißt, was defekt ist, tippe oben auf deine Vermutung.'
      : w[2];
    fb.forEach(b => b.classList.toggle('on', !geheim && b.dataset.f === f));
  }
  fb.forEach(b => b.onclick = () => {
    const n = b.dataset.f;
    if (n === 'zufall') { const k = Object.keys(V).filter(x => x !== 'ok'); f = k[Math.floor(Math.random() * k.length)]; geheim = true; p = -1; zeichne(); return; }
    if (geheim) {
      if (n === f) { geheim = false; zeichne(); document.getElementById('ms-t').innerHTML = '<b class="grn">Richtig erkannt!</b> ' + V[f][2]; }
      else document.getElementById('ms-t').innerHTML = '<b class="red">Noch nicht.</b> „' + NAMEN[n] + '“ passt nicht zu den Messwerten. Miss weiter und vergleiche.';
      return;
    }
    f = n; zeichne();
  });
  document.querySelectorAll('#ms-svg .mp').forEach(g => g.onclick = () => { p = +g.dataset.p; zeichne(); const m = document.getElementById('ms-t'); if (geheim) return; });
  zeichne();

  const sv = document.getElementById('sf-svg');
  const fl = Flow(sv, document.getElementById('sf-p'), { spacing: 26, speed: 50, r: 6, color: '#ffd34d' });
  const lb = document.querySelectorAll('#s-sf [data-l]');
  function l(i) {
    fl.on(!!i);
    document.getElementById('sf-l').setAttribute('fill', i ? '#a08a30' : '#18283f');
    document.getElementById('sf-u').textContent = i ? '10,1 V' : '12,5 V';
    document.getElementById('sf-d').textContent = i ? '2,4 V' : '0,0 V';
    document.getElementById('sf-t').innerHTML = i
      ? '<b class="red">Mit Last:</b> Jetzt fließt Strom. Am Übergangswiderstand fallen 2,4 V ab – am Verbraucher kommen nur 10,1 V an. Die Lampe leuchtet schwach. <span class="c">Jetzt ist der Fehler sichtbar.</span>'
      : '<b>Ohne Last:</b> Es fließt kein Strom. Am Übergangswiderstand fällt keine Spannung ab – das Multimeter zeigt am Verbraucher volle 12,5 V. <span class="ora">Der Fehler bleibt unsichtbar!</span>';
    lb.forEach(b => b.classList.toggle('on', +b.dataset.l === i));
  }
  lb.forEach(b => b.onclick = () => l(+b.dataset.l)); l(0);
})();
</script>'''


# ================================================================ 3 Batterie
T = 'BATTERIE'


def batt_svg():
    o = [f'<svg viewBox="0 0 640 260" width="640" height="260" style="display:block;margin:0 auto;max-width:100%;height:auto" id="bz-svg">',
         '<rect x="20" y="40" width="600" height="190" rx="14" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/>',
         f'<rect x="40" y="20" width="40" height="22" rx="4" fill="{MI}"/><text x="60" y="15" text-anchor="middle" font-size="20" font-weight="900" fill="{MI}">−</text>',
         f'<rect x="560" y="20" width="40" height="22" rx="4" fill="{PL}"/><text x="580" y="15" text-anchor="middle" font-size="20" font-weight="900" fill="{PL}">+</text>']
    for i in range(6):
        x = 34 + i * 97
        o.append(f'<g class="bz-z" data-i="{i}" style="transition:opacity .3s"><rect x="{x}" y="56" width="88" height="160" rx="8" fill="#213552" stroke="#94a4ba" stroke-width="2"/>')
        for j in range(5):
            c = PL if j % 2 == 0 else MI
            o.append(f'<rect x="{x + 10 + j * 15}" y="76" width="9" height="100" rx="2" fill="{c}" opacity=".8"/>')
        o.append(f'<text x="{x + 44}" y="202" text-anchor="middle" font-size="17" font-weight="900" fill="#ecf1f8">2,1 V</text></g>')
    for i in range(5):
        x = 34 + i * 97 + 88
        o.append(f'<path class="bz-v" data-i="{i}" d="M{x - 10} 66 V48 H{x + 19} V66" fill="none" stroke="#ecf1f8" stroke-width="4" style="transition:opacity .3s"/>')
    o.append('</svg>')
    return ''.join(o)


def starthilfe_svg():
    def bat(x, lab):
        return (f'<rect x="{x}" y="120" width="170" height="100" rx="10" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/>'
                f'<rect x="{x + 18}" y="106" width="30" height="16" rx="3" fill="{MI}"/><rect x="{x + 122}" y="106" width="30" height="16" rx="3" fill="{PL}"/>'
                f'<text x="{x + 33}" y="152" text-anchor="middle" font-size="22" font-weight="900" fill="{MI}">−</text><text x="{x + 137}" y="152" text-anchor="middle" font-size="22" font-weight="900" fill="{PL}">+</text>'
                f'<text x="{x + 85}" y="200" text-anchor="middle" font-size="17" font-weight="900" fill="#ecf1f8">{lab}</text>')
    return f'''<svg viewBox="0 0 640 300" width="640" height="300" style="display:block;margin:0 auto;max-width:100%;height:auto" id="sh-svg">
      {bat(30, 'leere Batterie')}{bat(440, 'Spender')}
      <rect x="230" y="200" width="120" height="70" rx="10" fill="#213552" stroke="#94a4ba" stroke-width="3"/><text x="290" y="240" text-anchor="middle" font-size="16" font-weight="800" fill="#ecf1f8">Motor</text>
      <circle cx="300" cy="206" r="6" fill="#94a4ba"/><text x="300" y="290" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Massepunkt am Motor</text>
      <path class="sh-k" data-i="0" d="M167 106 Q167 60 260 60" fill="none" stroke="{PL}" stroke-width="8" stroke-linecap="round" style="display:none"/>
      <path class="sh-k" data-i="1" d="M260 60 H500 Q577 60 577 106" fill="none" stroke="{PL}" stroke-width="8" stroke-linecap="round" style="display:none"/>
      <path class="sh-k" data-i="2" d="M473 106 Q473 85 420 85 H380" fill="none" stroke="#3a3a3a" stroke-width="8" stroke-linecap="round" style="display:none"/>
      <path class="sh-k" data-i="3" d="M380 85 Q320 85 300 200" fill="none" stroke="#3a3a3a" stroke-width="8" stroke-linecap="round" style="display:none"/>
      <g id="sh-n"></g>
    </svg>'''


batterie = [
    titel_folie(K, '12&nbsp;V', 'Die Starterbatterie', 'Aufbau, Bauarten, Prüfen, Laden und Starthilfe', 'font-size:84px'),
    lernziele(T, ['Wie eine Starterbatterie aufgebaut ist', 'Was Standard-, EFB- und AGM-Batterien unterscheidet',
                  'Wie du den Ladezustand prüfst und richtig lädst', 'Wie du sicher abklemmst und Starthilfe gibst']),
    folie(T, 'Aufbau – zum Ausprobieren', f'''    <div class="ctrl"><span style="width:260px">Zellen in Reihe: <span class="c" id="bz-n">6</span></span><input type="range" id="bz" min="1" max="6" step="1" value="6"></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.4fr 1fr;margin-top:10px">
      {batt_svg()}
      <div>
        <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">SPANNUNG</div><div class="lcd2" id="bz-u" style="font-size:34px">12,6 V</div></div>
        <div class="card" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px">Jede Zelle hat <span style="color:{PL};font-weight:800">Plus-Platten</span> (Bleidioxid) und <span style="color:{MI};font-weight:800">Minus-Platten</span> (Blei) in verdünnter Schwefelsäure. Eine Zelle liefert ca. 2,1 V – <b>6 Zellen in Reihe</b> ergeben ca. 12,6 V.</div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Richtwerte für eine voll geladene Batterie in Ruhe.</p>''', sid='s-bz', body_cls='body noclick'),
    folie(T, 'Bauarten', '''    <div class="grid3" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:21px">Standard (Nassbatterie)</div><ul UL><li>flüssige Säure</li><li>für Fahrzeuge ohne Start-Stopp</li><li>günstig</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">EFB</div><ul UL><li>verbesserte Nassbatterie</li><li>verträgt mehr Lade- und Entladezyklen</li><li>für einfache Start-Stopp-Systeme</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">AGM</div><ul UL><li>Säure in einem Glasvlies gebunden</li><li>auslaufsicher, sehr zyklenfest</li><li>für Start-Stopp mit Bremsenergie-Rückgewinnung</li></ul></div>
    </div>
    <div class="warn step" style="margin-top:12px"><b>Beim Tausch</b>Immer die gleiche Technik einbauen (AGM nur durch AGM ersetzen) – oder laut Hersteller. Danach die Batterie im Steuergerät anlernen.</div>'''.replace('UL', UL)),
    folie(T, 'Die Angaben auf der Batterie', '''    <div class="card step" style="text-align:center;font-size:30px;font-weight:900;letter-spacing:.02em">12 V &nbsp; 70 Ah &nbsp; 680 A (EN)</div>
    <div class="values">
      <div class="val step from-left"><b>12 V</b><span>Nennspannung</span></div>
      <div class="val step from-left"><b>70 Ah</b><span>Kapazität – wie viel Ladung die Batterie speichern kann</span></div>
      <div class="val step from-left"><b>680 A (EN)</b><span>Kälteprüfstrom – so viel Strom liefert sie bei −18 °C kurzzeitig für den Kaltstart</span></div>
    </div>
    <p class="muted" style="font-size:14px">Beispielwerte. Die richtige Batterie steht in den Herstellerunterlagen.</p>'''),
    folie(T, 'Ladezustand über die Ruhespannung – zum Ausprobieren', '''    <div class="ctrl"><span style="width:250px">Ruhespannung: <span class="c" id="lz-n">12,50 V</span></span><input type="range" id="lz" min="11.6" max="12.9" step="0.05" value="12.5"></div>
    <div class="grid2" style="align-items:center;margin-top:12px">
      <div class="card"><div class="muted" style="font-size:15px;font-weight:800">LADEZUSTAND (CA.)</div><div class="lcd2" id="lz-v" style="font-size:34px;margin:6px 0">75 %</div>
        <div style="height:22px;background:var(--card2);border-radius:11px;overflow:hidden"><div id="lz-bar" style="height:100%;width:75%;background:var(--grn);transition:width .2s,background .2s"></div></div></div>
      <div class="card" id="lz-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">Richtwerte für eine Standardbatterie bei ca. 20 °C. Erst messen, wenn die Batterie einige Stunden geruht hat (nicht geladen, keine Verbraucher). Genaue Werte laut Batteriehersteller.</p>''', sid='s-lz', body_cls='body noclick'),
    folie(T, 'Batterie prüfen', '''    <ol class="steps-list">
      <li class="step">Sichtprüfung<small>Gehäuse dicht und heil? Pole sauber und fest? Batterie richtig befestigt?</small></li>
      <li class="step">Ruhespannung messen<small>zeigt den Ladezustand – nicht, ob die Batterie noch gut ist</small></li>
      <li class="step">Batterietester<small>prüft die Startfähigkeit – Technik (AGM, EFB …) und Kälteprüfstrom eingeben</small></li>
      <li class="step">Spannung beim Starten<small>darf nicht zu tief einbrechen – Richtwert nicht unter ca. 9,6 V</small></li>
      <li class="step">Batterie öfter leer?<small>Ruhestrom und Ladespannung des Generators prüfen</small></li>
    </ol>'''),
    folie(T, 'Laden – aber sicher', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Knallgas</b>Beim Laden entsteht Wasserstoff. Gut lüften, keine Funken, nicht rauchen. Ladegerät erst einschalten, wenn die Zangen dran sind – und vor dem Abnehmen ausschalten.</div>
      <div class="tip step"><b>Passendes Ladegerät</b>Ladegerät mit Ladekennlinie für die Batterieart verwenden (z. B. AGM-Modus). Es regelt die Spannung und schaltet rechtzeitig ab.</div>
      <div class="warn step"><b>Säure</b>Schutzbrille und Handschuhe tragen. Spritzer auf Haut oder in die Augen sofort mit viel Wasser ausspülen.</div>
      <div class="warn step"><b>Gefroren?</b>Eine gefrorene Batterie nicht laden und nicht Starthilfe geben – sie kann platzen.</div>
    </div>'''),
    folie(T, 'Ab- und Anklemmen – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-a="ab">Abklemmen</button><button class="btn ghost" data-a="an">Anklemmen</button></div>
    <div class="grid2" style="align-items:center">
      <svg viewBox="0 0 360 230" width="360" height="230" style="display:block;margin:0 auto;max-width:100%;height:auto">
        <rect x="40" y="70" width="280" height="140" rx="14" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/>
        <rect x="70" y="50" width="50" height="22" rx="4" fill="{MI}"/><rect x="240" y="50" width="50" height="22" rx="4" fill="{PL}"/>
        <text x="95" y="120" text-anchor="middle" font-size="34" font-weight="900" fill="{MI}">−</text><text x="265" y="120" text-anchor="middle" font-size="34" font-weight="900" fill="{PL}">+</text>
        <circle id="ak-m" cx="95" cy="26" r="20" fill="#ffd34d"/><text id="ak-mt" x="95" y="34" text-anchor="middle" font-size="22" font-weight="900" fill="#0e192b">1</text>
        <circle id="ak-p" cx="265" cy="26" r="20" fill="#ffd34d"/><text id="ak-pt" x="265" y="34" text-anchor="middle" font-size="22" font-weight="900" fill="#0e192b">2</text>
        <text x="180" y="180" text-anchor="middle" font-size="18" font-weight="900" fill="#ecf1f8">Batterie</text>
      </svg>
      <div class="card" id="ak-t" style="font-size:17px;font-weight:600;line-height:1.55"></div>
    </div>''', sid='s-ak', body_cls='body noclick'),
    folie(T, 'Starthilfe – die richtige Reihenfolge', f'''    <div class="choice" style="margin-bottom:10px"><button class="btn" id="sh-b" style="--c:var(--grn)">Nächster Schritt</button><button class="btn ghost" id="sh-r">Von vorn</button></div>
    {starthilfe_svg()}
    <div class="card" id="sh-t" style="font-size:17px;font-weight:600;line-height:1.5;margin-top:8px"></div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Beide Batterien müssen die gleiche Spannung haben (12 V). Herstellervorgaben beachten – manche Fahrzeuge haben eigene Starthilfepunkte.</p>''', sid='s-sh', body_cls='body noclick'),
    folie(T, 'Batteriesensor und Batteriemanagement', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Batteriesensor</div>
        <ul UL><li>sitzt meist direkt an der Minusklemme</li><li>misst Strom, Spannung und Temperatur</li><li>meldet den Zustand der Batterie an ein Steuergerät</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Batteriemanagement</div>
        <ul UL><li>kennt den Ladezustand der Batterie</li><li>regelt die Ladespannung des Generators passend dazu</li><li>schaltet bei schwacher Batterie Komfortverbraucher ab</li></ul></div>
    </div>
    <div class="warn step" style="margin-top:12px"><b>Nach dem Batterietausch anlernen</b>Neue Batterie mit dem Diagnosetester im Fahrzeug anmelden (Technik, Kapazität). Sonst wird sie falsch geladen und hält nicht lange.</div>'''.replace('UL', UL)),
    video(T, 'bn-batterie'),
    kurztest(T, [
        ('Wie viele Zellen hat eine 12-V-Starterbatterie?', ['3', '6', '12'], 1, '6 Zellen mit je ca. 2,1 V in Reihe ergeben ca. 12,6 V.'),
        ('Die Ruhespannung beträgt 12,1 V. Was bedeutet das?', ['Die Batterie ist voll', 'Die Batterie ist defekt', 'Die Batterie ist nur noch zu etwa einem Viertel geladen'], 2, 'Richtwert: 12,7 V voll, 12,1 V ca. 25 %. Sofort laden.'),
        ('Welche Klemme nimmst du beim Abklemmen zuerst ab?', ['Minus', 'Plus', 'Egal'], 0, 'Erst Minus: Berührt das Werkzeug dann die Karosserie, gibt es keinen Kurzschluss.'),
        ('Wo schließt du bei der Starthilfe das schwarze Kabel am Fahrzeug mit der leeren Batterie an?', ['Am Pluspol', 'An einem Massepunkt am Motor, nicht an der Batterie', 'Am Minuspol der Spenderbatterie'], 1, 'So entsteht ein möglicher Funke nicht direkt an der Batterie (Knallgas).'),
    ]),
    merke(T, ['6 Zellen × ca. 2,1 V = ca. 12,6 V', 'Standard, EFB, AGM – beim Tausch gleiche Technik',
              'Ladezustand über Ruhespannung|Startfähigkeit mit dem Batterietester', 'Abklemmen: Minus zuerst|Anklemmen: Plus zuerst']),
]
batterie_js = '''<script>
(function () {
  const bz = document.getElementById('bz');
  function z() {
    const n = +bz.value;
    document.querySelectorAll('#bz-svg .bz-z').forEach(g => g.style.opacity = +g.dataset.i < n ? 1 : 0.25);
    document.querySelectorAll('#bz-svg .bz-v').forEach(g => g.style.opacity = +g.dataset.i < n - 1 ? 1 : 0.15);
    document.getElementById('bz-n').textContent = n;
    document.getElementById('bz-u').textContent = (n * 2.1).toFixed(1).replace('.', ',') + ' V';
  }
  bz.addEventListener('input', z); z();

  const lz = document.getElementById('lz');
  const P = [[11.9, 0], [12.1, 25], [12.3, 50], [12.5, 75], [12.7, 100]];
  function soc(u) {
    if (u <= P[0][0]) return 0; if (u >= P[4][0]) return 100;
    for (let i = 1; i < P.length; i++) if (u <= P[i][0]) return P[i - 1][1] + (u - P[i - 1][0]) / (P[i][0] - P[i - 1][0]) * (P[i][1] - P[i - 1][1]);
  }
  function l() {
    const u = +lz.value, s = Math.round(soc(u) / 5) * 5;
    document.getElementById('lz-n').textContent = u.toFixed(2).replace('.', ',') + ' V';
    document.getElementById('lz-v').textContent = s + ' %';
    const bar = document.getElementById('lz-bar'); bar.style.width = s + '%';
    bar.style.background = s >= 75 ? 'var(--grn)' : s >= 50 ? 'var(--yel)' : 'var(--red)';
    document.getElementById('lz-t').innerHTML = s >= 75 ? '<b class="grn">Gut geladen.</b> Die Batterie ist startbereit – ob sie noch gut ist, zeigt erst der Batterietester.'
      : s >= 50 ? '<b class="yel">Halb voll.</b> Batterie nachladen. Ursache suchen: viel Kurzstrecke? Ruhestrom zu hoch?'
      : s > 0 ? '<b class="red">Stark entladen.</b> Sofort laden. Bleibt die Batterie so stehen, bilden sich Kristalle an den Platten (Sulfatierung) – sie verliert Kapazität.'
      : '<b class="red">Tiefentladen.</b> Die Batterie kann dauerhaft geschädigt sein. Laden und danach mit dem Batterietester prüfen.';
  }
  lz.addEventListener('input', l); l();

  const ab = document.querySelectorAll('#s-ak [data-a]');
  function a(m) {
    const abk = m === 'ab';
    document.getElementById('ak-mt').textContent = abk ? '1' : '2';
    document.getElementById('ak-pt').textContent = abk ? '2' : '1';
    document.getElementById('ak-t').innerHTML = abk
      ? '<b>Abklemmen:</b> <span class="blu">1. Minus</span>, dann <span class="red">2. Plus</span>.<br>Warum? Ist Minus ab, gibt es keine Verbindung mehr zur Karosserie. Rutscht der Schlüssel am Pluspol gegen die Karosserie, passiert nichts.'
      : '<b>Anklemmen:</b> <span class="red">1. Plus</span>, dann <span class="blu">2. Minus</span>.<br>Warum? Solange Minus noch ab ist, gibt es keinen Kurzschluss, wenn das Werkzeug am Pluspol die Karosserie berührt.';
    ab.forEach(b => b.classList.toggle('on', b.dataset.a === m));
  }
  ab.forEach(b => b.onclick = () => a(b.dataset.a)); a('ab');

  const ST = [
    'Los geht\\'s: Beide Fahrzeuge aus, Verbraucher aus. Die Fahrzeuge dürfen sich nicht berühren.',
    '<b>1.</b> <span class="red">Rotes Kabel</span> an den Pluspol der <b>leeren</b> Batterie.',
    '<b>2.</b> Das andere Ende des <span class="red">roten Kabels</span> an den Pluspol der <b>Spenderbatterie</b>.',
    '<b>3.</b> <b>Schwarzes Kabel</b> an den Minuspol der <b>Spenderbatterie</b>.',
    '<b>4.</b> Das andere Ende des <b>schwarzen Kabels</b> an einen <b>Massepunkt am Motor</b> des liegengebliebenen Fahrzeugs – nicht an dessen Minuspol. Ein möglicher Funke entsteht so weit weg von der Batterie (Knallgas!).',
    '<b>Starten:</b> Spenderfahrzeug laufen lassen, dann das liegengebliebene Fahrzeug starten. <b>Abklemmen in umgekehrter Reihenfolge</b>: 4, 3, 2, 1.'
  ];
  let s = 0;
  function sh() {
    document.querySelectorAll('#sh-svg .sh-k').forEach(k => k.style.display = +k.dataset.i < s ? '' : 'none');
    const pos = [[167, 60], [577, 60], [473, 85], [300, 200]];
    document.getElementById('sh-n').innerHTML = pos.slice(0, Math.min(s, 4)).map((p, i) => '<circle cx="' + p[0] + '" cy="' + (p[1] - (i === 3 ? 34 : 0)) + '" r="15" fill="#ffd34d"/><text x="' + p[0] + '" y="' + (p[1] - (i === 3 ? 34 : 0) + 6) + '" text-anchor="middle" font-size="17" font-weight="900" fill="#0e192b">' + (i + 1) + '</text>').join('');
    document.getElementById('sh-t').innerHTML = ST[s];
    document.getElementById('sh-b').disabled = s >= ST.length - 1;
  }
  document.getElementById('sh-b').onclick = () => { if (s < ST.length - 1) s++; sh(); };
  document.getElementById('sh-r').onclick = () => { s = 0; sh(); };
  sh();
})();
</script>'''


# ================================================================ 4 Generator
T = 'GENERATOR'


def welle_svg(pid, h=230):
    return f'''<svg viewBox="0 0 600 {h}" width="600" height="{h}" style="display:block;margin:0 auto;max-width:100%;height:auto" id="{pid}-svg">
      <rect x="0" y="0" width="600" height="{h}" rx="12" fill="#18283f"/>
      <g id="{pid}-grid"></g><g id="{pid}-w"></g>
      <text id="{pid}-lab" x="16" y="24" font-size="15" font-weight="800" fill="#94a4ba"></text>
    </svg>'''


gen = [
    titel_folie(K, 'G', 'Der Generator', 'Aufbau, Regler, Ladespannung und Prüfen', 'font-size:110px'),
    lernziele(T, ['Welche Aufgabe der Generator hat', 'Wie Drehstrom entsteht und zu Gleichspannung wird',
                  'Was der Regler macht', 'Wie du Generator und Ladesystem prüfst']),
    folie(T, 'Aufgabe des Generators', '''    <div class="kette">
      <div class="glied step"><b>Motor</b><span>dreht über den Riemen</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Generator</b><span>erzeugt elektrische Energie</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Verbraucher</b><span>Licht, Steuergeräte, Gebläse …</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Batterie</b><span>wird wieder geladen</span></div>
    </div>
    <div class="grid2" style="margin-top:18px">
      <div class="tip step"><b>Ohne Generator</b>würde die Batterie bei laufendem Motor immer leerer – nach kurzer Zeit geht nichts mehr.</div>
      <div class="tip step"><b>Ladekontrollleuchte</b>Leuchtet sie bei laufendem Motor, lädt der Generator nicht richtig. Bald prüfen!</div>
    </div>'''),
    folie(T, 'Vom Drehstrom zur Gleichspannung – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px"><button class="btn ghost on" data-w="0">Drehstrom (im Ständer)</button><button class="btn ghost" data-w="1">Nach dem Gleichrichter</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {welle_svg('dw')}
      <div class="card" id="dw-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>''', sid='s-dw', body_cls='body noclick'),
    folie(T, 'Der Regler – zum Ausprobieren', '''    <div class="ctrl"><span style="width:250px">Motordrehzahl: <span class="c" id="rg-dn">2.000 1/min</span></span><input type="range" id="rg-d" min="800" max="6000" step="100" value="2000"></div>
    <div class="ctrl"><span style="width:250px">Verbraucher: <span class="c" id="rg-vn">mittel</span></span><input type="range" id="rg-v" min="0" max="2" step="1" value="1"></div>
    <div class="grid3" style="margin-top:12px">
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">LADESPANNUNG</div><div class="lcd2" id="rg-u" style="font-size:30px">14,2 V</div></div>
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">ERREGERSTROM</div><div class="lcd2" id="rg-e" style="font-size:30px">40 %</div>
        <div style="height:14px;background:var(--card2);border-radius:7px;overflow:hidden;margin-top:6px"><div id="rg-eb" style="height:100%;width:40%;background:var(--c)"></div></div></div>
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">BATTERIE</div><div class="lcd2" id="rg-b" style="font-size:24px">wird geladen</div></div>
    </div>
    <div class="card" id="rg-t" style="font-size:16px;font-weight:600;line-height:1.55;margin-top:12px"></div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Vereinfachtes Beispiel. Ladespannung ca. 14 V – genauer Wert laut Hersteller.</p>''', sid='s-rg', body_cls='body noclick'),
    folie(T, 'Aufbau', '''    <div class="values">
      <div class="val step from-left"><b>Riemenscheibe</b><span>oft mit Freilauf – dämpft Drehschwingungen des Motors</span></div>
      <div class="val step from-left"><b>Läufer</b><span>Klauenpolläufer mit Erregerwicklung – ein drehender Elektromagnet</span></div>
      <div class="val step from-left"><b>Schleifringe</b><span>mit Kohlebürsten – bringen den Erregerstrom in den drehenden Läufer</span></div>
      <div class="val step from-left"><b>Ständer</b><span>drei Wicklungen – hier entsteht der Drehstrom</span></div>
      <div class="val step from-left"><b>Gleichrichter</b><span>Dioden machen aus Drehstrom Gleichspannung</span></div>
      <div class="val step from-left"><b>Regler</b><span>hält die Ladespannung konstant</span></div>
    </div>'''),
    folie(T, 'Anschlüsse und Werte', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Anschlüsse</div>
        <ul UL><li><b>B+</b>: dicke Leitung zur Batterie – führt <b>immer</b> Batteriespannung</li><li><b>D+ / L</b>: Ladekontrolle (Klemme 61)</li><li>bei neueren Fahrzeugen: Datenleitung (z. B. LIN) zum Motorsteuergerät</li><li>Masse über das Gehäuse</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Ladespannung</div>
        <ul UL><li>Richtwert ca. 13,8 bis 14,8 V</li><li>mit Generatormanagement zeitweise auch weniger oder mehr – das Steuergerät regelt nach Ladezustand der Batterie</li><li>genaue Werte laut Hersteller</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Generator prüfen', '''    <ol class="steps-list">
      <li class="step">Sichtprüfung<small>Riemen, Spanner, Freilauf, Stecker, B+-Mutter fest?</small></li>
      <li class="step">Ladespannung an der Batterie<small>im Leerlauf und bei ca. 2.500 1/min, mit und ohne Verbraucher</small></li>
      <li class="step">Spannungsfall unter Last<small>B+-Leitung und Masse zwischen Generator und Batterie</small></li>
      <li class="step">Welligkeit mit dem Oszilloskop<small>zeigt defekte Dioden oder Wicklungen</small></li>
      <li class="step">Fehlerspeicher<small>bei Generatoren mit Datenleitung meldet das Steuergerät Fehler</small></li>
    </ol>'''),
    folie(T, 'Welligkeit am Oszilloskop – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap"><button class="btn ghost on" data-o="ok">In Ordnung</button><button class="btn ghost" data-o="dio">Diode defekt</button><button class="btn ghost" data-o="reg">Regler defekt</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {welle_svg('ow', 220)}
      <div class="card" id="ow-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Vereinfachte Beispielbilder, gemessen an B+ gegen Masse bei laufendem Motor.</p>''', sid='s-ow', body_cls='body noclick'),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>B+ führt immer Spannung</b>Vor Arbeiten am Generator die Batterie abklemmen (Minus zuerst). Ein abgerutschter Schlüssel an B+ macht einen Kurzschluss.</div>
      <div class="warn step"><b>Nie bei laufendem Motor abklemmen</b>Die Batterie nie bei laufendem Motor abklemmen – Spannungsspitzen können Steuergeräte zerstören.</div>
      <div class="tip step"><b>Freilauf prüfen</b>Die Freilaufriemenscheibe muss in eine Richtung frei drehen und in die andere sperren. Prüfen und tauschen nur mit Spezialwerkzeug.</div>
      <div class="tip step"><b>Batterie oft leer?</b>Erst die Batterie prüfen, dann Ladespannung und Ruhestrom. Ein Generator allein ist selten die einzige Ursache.</div>
    </div>'''),
    video(T, 'bn-generator'),
    kurztest(T, [
        ('Was macht der Gleichrichter im Generator?', ['Er hält die Spannung konstant', 'Er macht aus Drehstrom Gleichspannung', 'Er dreht den Läufer'], 1, 'Dioden lassen den Strom nur in eine Richtung durch.'),
        ('Wie hält der Regler die Ladespannung konstant?', ['Er verändert den Erregerstrom', 'Er verändert die Motordrehzahl', 'Er schaltet die Batterie ab'], 0, 'Weniger Erregerstrom → schwächeres Magnetfeld → weniger Spannung.'),
        ('Welche Ladespannung ist ein üblicher Richtwert?', ['ca. 12 V', 'ca. 16–17 V', 'ca. 13,8–14,8 V'], 2, 'Genauer Wert laut Hersteller.'),
        ('Warum darfst du die Batterie nicht bei laufendem Motor abklemmen?', ['Spannungsspitzen können Steuergeräte zerstören', 'Der Motor geht sofort aus', 'Die Batterie wird zu voll'], 0, 'Ohne Batterie fehlt der „Puffer“ im Bordnetz.'),
    ]),
    merke(T, ['Generator versorgt die Verbraucher und lädt die Batterie', 'Drehstrom im Ständer → Gleichrichter → Gleichspannung',
              'Regler verändert den Erregerstrom|Ladespannung bleibt ca. 14 V', 'B+ führt immer Batteriespannung']),
]
gen_js = '''<script>
(function () {
  function grid(id, h) {
    let g = '';
    for (let x = 50; x < 600; x += 50) g += '<line x1="' + x + '" y1="0" x2="' + x + '" y2="' + h + '" stroke="#94a4ba" stroke-width="1" opacity=".18"/>';
    for (let y = 30; y < h; y += 40) g += '<line x1="0" y1="' + y + '" x2="600" y2="' + y + '" stroke="#94a4ba" stroke-width="1" opacity=".18"/>';
    document.getElementById(id + '-grid').innerHTML = g;
  }
  const pfad = (fn, h, c, w) => { let d = ''; for (let x = 10; x <= 590; x += 2) d += (d ? ' L' : 'M') + x + ' ' + fn(x).toFixed(1); return '<path d="' + d + '" fill="none" stroke="' + c + '" stroke-width="' + w + '"/>'; };
  grid('dw', 230);
  const C = ['#f05e4e', '#ffd34d', '#28aaf5'];
  const ph = (x, k) => Math.sin((x - 10) / 580 * 2 * Math.PI * 3 - k * 2 * Math.PI / 3);
  const db = document.querySelectorAll('#s-dw [data-w]');
  function dw(i) {
    const mid = 115, A = 80;
    let o = '';
    if (!i) { for (let k = 0; k < 3; k++) o += pfad(x => mid - A * ph(x, k), 230, C[k], 3); o += '<line x1="10" y1="' + mid + '" x2="590" y2="' + mid + '" stroke="#94a4ba" stroke-width="1.5"/>'; }
    else {
      for (let k = 0; k < 3; k++) o += pfad(x => 200 - 0.75 * A * Math.abs(ph(x, k)), 230, C[k], 1.5).replace('stroke-width', 'opacity=".35" stroke-width');
      o += pfad(x => 200 - 0.75 * A * Math.max(Math.abs(ph(x, 0)), Math.abs(ph(x, 1)), Math.abs(ph(x, 2))), 230, '#34c778', 5);
      o += '<line x1="10" y1="200" x2="590" y2="200" stroke="#94a4ba" stroke-width="1.5"/><text x="580" y="218" text-anchor="end" font-size="13" font-weight="800" fill="#94a4ba">0 V</text>';
    }
    document.getElementById('dw-w').innerHTML = o;
    document.getElementById('dw-lab').textContent = i ? 'Gleichspannung mit kleiner Welligkeit' : 'Drei Wechselspannungen, versetzt';
    document.getElementById('dw-t').innerHTML = i
      ? '<b>Gleichrichter:</b> Die <span class="c">Dioden</span> lassen den Strom nur in eine Richtung durch. Aus den drei Wechselspannungen wird eine <span class="grn">Gleichspannung</span> (grün) – mit einer kleinen Welligkeit.'
      : '<b>Drehstrom:</b> Der Läufer ist ein drehender <span class="c">Elektromagnet</span>. Er dreht sich in den drei Wicklungen des Ständers. In jeder Wicklung entsteht eine Wechselspannung – zeitlich versetzt. Das nennt man Drehstrom.';
    db.forEach(b => b.classList.toggle('on', +b.dataset.w === i));
  }
  db.forEach(b => b.onclick = () => dw(+b.dataset.w)); dw(0);

  const rd = document.getElementById('rg-d'), rv = document.getElementById('rg-v');
  function rg() {
    const n = +rd.value, v = +rv.value;
    const bedarf = [0.3, 0.6, 1.0][v];
    const kann = Math.min(1, (n - 600) / 1800);
    let e = bedarf / kann, u = 14.2, bat = 'wird geladen';
    if (e > 1) { u = 14.2 - (e - 1) * 1.6; e = 1; }
    u = Math.max(12.2, u);
    if (u < 13.3) bat = 'wird entladen'; else if (u < 13.9) bat = 'kaum Ladung';
    document.getElementById('rg-dn').textContent = n.toLocaleString('de-DE') + ' 1/min';
    document.getElementById('rg-vn').textContent = ['wenig', 'mittel', 'viele (Licht, Heckscheibe, Gebläse)'][v];
    document.getElementById('rg-u').textContent = u.toFixed(1).replace('.', ',') + ' V';
    document.getElementById('rg-e').textContent = Math.round(e * 100) + ' %';
    document.getElementById('rg-eb').style.width = Math.round(e * 100) + '%';
    const b = document.getElementById('rg-b'); b.textContent = bat; b.className = 'lcd2 ' + (u < 13.3 ? 'red' : u < 13.9 ? 'yel' : 'grn');
    document.getElementById('rg-t').innerHTML = e >= 1 && u < 14.1
      ? '<b class="ora">Am Limit:</b> Bei niedriger Drehzahl und vielen Verbrauchern reicht auch der volle Erregerstrom nicht. Die Spannung sinkt – die Batterie hilft mit und wird entladen. Darum heben manche Fahrzeuge die Leerlaufdrehzahl an.'
      : '<b>Der Regler arbeitet:</b> Er verändert den <span class="c">Erregerstrom</span> im Läufer. Mehr Erregerstrom = stärkeres Magnetfeld = mehr Spannung. So bleibt die Ladespannung bei unterschiedlicher Drehzahl und Last gleich.';
  }
  rd.addEventListener('input', rg); rv.addEventListener('input', rg); rg();

  grid('ow', 220);
  const ob = document.querySelectorAll('#s-ow [data-o]');
  function ow(m) {
    const rip = x => Math.abs(Math.sin((x - 10) / 580 * Math.PI * 18));
    let fn, t;
    if (m === 'ok') { fn = x => 110 - 8 * rip(x); t = '<b class="grn">In Ordnung:</b> Kleine, gleichmäßige Welligkeit – alle Dioden arbeiten.'; }
    if (m === 'dio') { fn = x => { const i = Math.floor((x - 10) / 580 * 18); return 110 - 8 * rip(x) + (i % 3 === 0 ? 40 * rip(x) : 0); }; t = '<b class="red">Diode defekt:</b> In regelmäßigen Abständen fehlt ein Stück – tiefe Einbrüche im Bild. Der Generator bringt weniger Leistung, die Batterie wird schlecht geladen.'; }
    if (m === 'reg') { fn = x => 60 - 8 * rip(x); t = '<b class="red">Regler defekt:</b> Die Spannung ist viel zu hoch (z. B. 16 V). Die Batterie gast, Lampen brennen durch, Steuergeräte können Schaden nehmen.'; }
    document.getElementById('ow-w').innerHTML = pfad(fn, 220, '#34c778', 4) + '<line x1="10" y1="110" x2="590" y2="110" stroke="#94a4ba" stroke-width="1" stroke-dasharray="5 5"/><text x="586" y="104" text-anchor="end" font-size="13" font-weight="800" fill="#94a4ba">ca. 14 V</text>';
    document.getElementById('ow-lab').textContent = m === 'reg' ? 'Spannung zu hoch' : 'Welligkeit der Ladespannung';
    document.getElementById('ow-t').innerHTML = t;
    ob.forEach(b => b.classList.toggle('on', b.dataset.o === m));
  }
  ob.forEach(b => b.onclick = () => ow(b.dataset.o)); ow('ok');
})();
</script>'''


# ================================================================ 5 Starter
T = 'STARTER'


def starter_svg():
    return f'''<svg viewBox="0 0 760 340" width="760" height="340" style="display:block;margin:0 auto;max-width:100%;height:auto" id="sv-svg">
      <rect x="20" y="40" width="110" height="60" rx="8" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/><text x="75" y="76" text-anchor="middle" font-size="16" font-weight="900" fill="#ecf1f8">Batterie</text>
      <rect x="100" y="32" width="20" height="9" fill="{PL}"/><rect x="30" y="32" width="20" height="9" fill="{MI}"/>
      <rect x="20" y="170" width="110" height="50" rx="8" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/><text x="75" y="200" text-anchor="middle" font-size="15" font-weight="900" fill="#ecf1f8">Zündschloss</text>
      <path d="M110 32 V14 H560 V58" fill="none" stroke="{PL}" stroke-width="9"/><text x="300" y="36" font-size="15" font-weight="900" fill="{PL}">Klemme 30 (dick)</text>
      <path d="M100 32 V20 H90 V170" fill="none" stroke="{PL}" stroke-width="3"/>
      <path id="sv-50" d="M130 195 H260 V110" fill="none" stroke="{PL}" stroke-width="3"/><text x="140" y="188" font-size="15" font-weight="900" fill="{PL}">Klemme 50</text>
      <rect x="240" y="50" width="360" height="60" rx="10" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/>
      <text x="420" y="45" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">MAGNETSCHALTER</text>
      <g id="sv-spule">{''.join(f'<path d="M{270 + i * 18} 95 q9 -30 18 0" fill="none" stroke="#ecf1f8" stroke-width="3"/>' for i in range(7))}</g>
      <rect id="sv-anker" x="410" y="66" width="120" height="28" rx="5" fill="#94a4ba"/>
      <circle cx="560" cy="64" r="5" fill="#ecf1f8"/><line id="sv-hk" x1="560" y1="64" x2="586" y2="86" stroke="#ecf1f8" stroke-width="5"/><circle cx="560" cy="104" r="5" fill="#ecf1f8"/>
      <text x="610" y="90" font-size="13" font-weight="800" fill="#94a4ba">Haupt-</text><text x="610" y="106" font-size="13" font-weight="800" fill="#94a4ba">kontakt</text>
      <path d="M560 104 V150 H420 V200" fill="none" stroke="{PL}" stroke-width="9"/>
      <circle id="sv-m" cx="420" cy="245" r="45" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/>
      <g id="sv-mr"><line x1="420" y1="212" x2="420" y2="278" stroke="#ecf1f8" stroke-width="4"/><line x1="387" y1="245" x2="453" y2="245" stroke="#ecf1f8" stroke-width="4"/></g>
      <text x="420" y="315" text-anchor="middle" font-size="15" font-weight="900" fill="#ecf1f8">Elektromotor</text>
      <line x1="465" y1="245" x2="640" y2="245" stroke="#94a4ba" stroke-width="8"/>
      <line id="sv-hebel" x1="530" y1="94" x2="555" y2="240" stroke="#ecf1f8" stroke-width="6" stroke-linecap="round"/>
      <circle cx="540" cy="160" r="6" fill="#ecf1f8"/>
      <g id="sv-rz"><rect x="545" y="222" width="34" height="46" rx="4" fill="#ffd34d"/>{''.join(f'<rect x="{545 + i * 9}" y="216" width="5" height="58" fill="#ffd34d"/>' for i in range(4))}</g>
      <text id="sv-rzl" x="562" y="296" text-anchor="middle" font-size="14" font-weight="900" fill="#ffd34d">Ritzel</text>
      <g id="sv-zk"><circle cx="700" cy="245" r="56" fill="none" stroke="#94a4ba" stroke-width="8" stroke-dasharray="7 5"/><circle cx="700" cy="245" r="40" fill="#213552"/><line x1="700" y1="205" x2="700" y2="285" stroke="#94a4ba" stroke-width="3"/></g>
      <text x="700" y="325" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Zahnkranz (Motor)</text>
      <path id="sv-p30" d="M110 34 V14 H560 V58 M560 104 V150 H420 V200" fill="none" stroke="none"/>
      <path id="sv-p30a" d="M110 32 V14 H560 V150 H420 V200" fill="none" stroke="none"/>
      <path id="sv-p50" d="M90 40 V170 M130 195 H260 V110" fill="none" stroke="none"/>
      <path id="sv-p50a" d="M130 195 H260 V110" fill="none" stroke="none"/>
    </svg>'''


starter = [
    titel_folie(K, '50', 'Der Starter', 'Aufbau, Startvorgang, Prüfen und Fehlerbilder', 'font-size:110px'),
    lernziele(T, ['Wie der Starter aufgebaut ist', 'Was beim Starten nacheinander passiert',
                  'Welche Klemmen am Starter sind', 'Wie du Starterfehler eingrenzt']),
    folie(T, 'Aufbau', '''    <div class="values">
      <div class="val step from-left"><b>Elektromotor</b><span>Gleichstrommotor, meist mit Dauermagneten</span></div>
      <div class="val step from-left"><b>Vorgelege</b><span>Planetengetriebe – macht den kleinen Motor kräftig</span></div>
      <div class="val step from-left"><b>Magnetschalter</b><span>spurt das Ritzel ein und schaltet den großen Strom zum Motor</span></div>
      <div class="val step from-left"><b>Einrückhebel</b><span>schiebt das Ritzel zum Zahnkranz</span></div>
      <div class="val step from-left"><b>Ritzel</b><span>mit Freilauf – greift in den Zahnkranz am Schwungrad – der Freilauf schützt den Starter, wenn der Motor anspringt</span></div>
    </div>'''),
    folie(T, 'Der Startvorgang – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:8px;flex-wrap:wrap;gap:6px"><button class="btn ghost on" data-s="0">Ruhe</button><button class="btn ghost" data-s="1">1 · Schlüssel auf Start</button><button class="btn ghost" data-s="2">2 · Ritzel spurt ein</button><button class="btn ghost" data-s="3">3 · Motor springt an</button><button class="btn ghost" data-s="4">4 · Schlüssel los</button></div>
    {starter_svg()}
    <div class="card" id="sv-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:6px"></div>''', sid='s-sv', body_cls='body noclick'),
    folie(T, 'Klemmen und Werte', '''    <div class="grid3" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:30px;color:var(--red)">30</div><p style="margin:6px 0 0">Dicke Leitung direkt von der Batterie. Oft <b>ohne Sicherung</b>!</p></div>
      <div class="card step"><div class="big" style="font-size:30px;color:var(--red)">50</div><p style="margin:6px 0 0">Steuerleitung vom Zündschloss oder Steuergerät, oft über ein Startrelais.</p></div>
      <div class="card step"><div class="big" style="font-size:30px;color:var(--blu)">31</div><p style="margin:6px 0 0">Masse über Gehäuse und Motor – das Masseband muss gut sein.</p></div>
    </div>
    <div class="values" style="margin-top:12px">
      <div class="val step from-left"><b>einige 100 A</b><span>Starterstrom beim Pkw – Richtwert</span></div>
      <div class="val step from-left"><b>ca. 9,6 V</b><span>so tief darf die Batteriespannung beim Starten höchstens fallen – Richtwert</span></div>
    </div>
    <p class="muted" style="font-size:14px">Genaue Werte laut Hersteller.</p>'''),
    folie(T, 'Fehlerbilder – zum Ausprobieren', '''    <div class="choice" style="margin-bottom:12px;flex-wrap:wrap;gap:6px"><button class="btn ghost on" data-f="0">Nichts passiert</button><button class="btn ghost" data-f="1">Es klickt nur</button><button class="btn ghost" data-f="2">Dreht zu langsam</button><button class="btn ghost" data-f="3">Starter dreht, Motor nicht</button><button class="btn ghost" data-f="4">Starter läuft weiter</button></div>
    <div class="grid2" style="align-items:start">
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">MÖGLICHE URSACHEN</div><ul id="fb-u" style="font-size:16px;line-height:1.55;padding-left:20px;margin:8px 0 0"></ul></div>
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">SO PRÜFST DU</div><ul id="fb-p" style="font-size:16px;line-height:1.55;padding-left:20px;margin:8px 0 0"></ul></div>
    </div>''', sid='s-fb', body_cls='body noclick'),
    folie(T, 'Starter prüfen', '''    <ol class="steps-list">
      <li class="step">Batterie zuerst<small>geladen und startfähig? Ohne gute Batterie ist jede Starterprüfung sinnlos</small></li>
      <li class="step">Spannung beim Starten<small>an der Batterie – Richtwert nicht unter ca. 9,6 V</small></li>
      <li class="step">Klemme 50 beim Starten<small>kommt die Steuerspannung am Starter an? Wert laut Hersteller</small></li>
      <li class="step">Spannungsfall unter Last<small>Plusleitung (Batterie-Plus bis Klemme 30) und Masse (Batterie-Minus bis Startergehäuse) beim Starten</small></li>
      <li class="step">Starterstrom<small>mit der Stromzange – zu hoch: Starter schwergängig, zu niedrig: Übergangswiderstand</small></li>
    </ol>
    <p class="muted" style="font-size:14px">Damit der Motor beim Prüfen nicht anspringt, nach Herstellerangabe vorgehen.</p>'''),
    folie(T, 'Start-Stopp und neue Systeme', '''    <div class="grid3" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:21px">Verstärkter Starter</div><p style="margin:6px 0 0">Für viel mehr Startvorgänge gebaut: haltbarere Bürsten, Freilauf und Lager.</p></div>
      <div class="card step"><div class="big" style="font-size:21px">Passende Batterie</div><p style="margin:6px 0 0">Start-Stopp braucht eine EFB- oder AGM-Batterie mit Batteriesensor.</p></div>
      <div class="card step"><div class="big" style="font-size:21px">Riemen-Startergenerator</div><p style="margin:6px 0 0">Startet den Motor über den Riemen und arbeitet auch als Generator – oft mit 48 V (Mild-Hybrid).</p></div>
    </div>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Klemme 30 ohne Sicherung</b>Vor Arbeiten am Starter die Batterie abklemmen (Minus zuerst). Ein Kurzschluss an Klemme 30 kann die Leitung zum Glühen bringen.</div>
      <div class="tip step"><b>Pausen machen</b>Nicht lange am Stück starten (Richtwert höchstens ca. 10 s), dann eine Pause – der Starter wird sonst heiß.</div>
      <div class="warn step"><b>Starter läuft weiter</b>Bleibt der Starter nach dem Loslassen an, sofort die Batterie abklemmen – sonst wird er zerstört.</div>
      <div class="tip step"><b>Masseband</b>Ein lockeres oder korrodiertes Masseband zwischen Motor und Karosserie ist eine häufige Ursache für Startprobleme.</div>
    </div>'''),
    video(T, 'bn-starter'),
    kurztest(T, [
        ('Was macht der Magnetschalter?', ['Er lädt die Batterie', 'Er spurt das Ritzel ein und schaltet den großen Strom zum Starter', 'Er misst die Drehzahl'], 1, 'Er wird über Klemme 50 angesteuert.'),
        ('Wozu dient der Freilauf am Ritzel?', ['Er schützt den Starter, wenn der Motor anspringt', 'Er macht den Starter schneller', 'Er ersetzt den Zahnkranz'], 0, 'Sonst würde der laufende Motor den Starter viel zu schnell antreiben.'),
        ('Beim Starten klickt es nur. Was prüfst du zuerst?', ['Den Luftfilter', 'Die Zündkerzen', 'Batterie und Spannungsfall an Plusleitung und Masse'], 2, 'Der Magnetschalter zieht an, aber es kommt zu wenig Strom am Motor an.'),
        ('Welche Klemme ist die Steuerleitung des Starters?', ['30', '31', '50'], 2, 'Klemme 50 kommt vom Zündschloss oder Steuergerät.'),
    ]),
    merke(T, ['Magnetschalter: Ritzel einspuren und Hauptstrom schalten', 'Freilauf schützt den Starter beim Anspringen',
              '30 dick und oft ungesichert · 50 Steuerleitung · 31 Masse', 'Erst Batterie prüfen, dann Spannungsfall unter Last']),
]
starter_js = '''<script src="assets/schaltung.js"></script>
<script>
(function () {
  const svg = document.getElementById('sv-svg');
  const f30 = Flow(svg, document.getElementById('sv-p30a'), { spacing: 16, speed: 120, r: 7, color: '#ffd34d' });
  const f50 = Flow(svg, document.getElementById('sv-p50a'), { spacing: 30, speed: 50, r: 4, color: '#ffd34d' });
  const S = [
    { e: 0, hk: 0, mot: 0, zk: 0, f50: 0, f30: 0, t: '<b>Ruhe:</b> Der Anker im Magnetschalter ist draußen, das Ritzel steht vom Zahnkranz weg, der Hauptkontakt ist offen.' },
    { e: 1, hk: 0, mot: 0.2, zk: 0, f50: 1, f30: 0, t: '<b>1 · Schlüssel auf Start:</b> Über <span class="c">Klemme 50</span> fließt Strom in den Magnetschalter. Er wird zum Magneten und zieht den Anker hinein. Der Einrückhebel schiebt das Ritzel zum Zahnkranz.' },
    { e: 1, hk: 1, mot: 1, zk: 1, f50: 1, f30: 1, t: '<b>2 · Ritzel spurt ein:</b> Das Ritzel greift in den Zahnkranz. Am Ende schließt der <span class="c">Hauptkontakt</span>: Ein sehr großer Strom fließt über <span class="c">Klemme 30</span> zum Elektromotor. Der Starter dreht den Verbrennungsmotor.' },
    { e: 1, hk: 1, mot: 1, zk: 3, f50: 1, f30: 1, t: '<b>3 · Motor springt an:</b> Jetzt dreht der Motor schneller als der Starter. Der <span class="c">Freilauf</span> im Ritzel trennt – so wird der Starter nicht viel zu schnell gedreht.' },
    { e: 0, hk: 0, mot: 0, zk: 2, f50: 0, f30: 0, t: '<b>4 · Schlüssel los:</b> Klemme 50 ist aus. Eine Feder drückt den Anker zurück, der Hauptkontakt öffnet, das Ritzel spurt aus. Der Motor läuft allein weiter.' }
  ];
  let st = S[0], wm = 0, wz = 0;
  const b = document.querySelectorAll('#s-sv [data-s]');
  function s(i) {
    st = S[i];
    document.getElementById('sv-anker').setAttribute('x', st.e ? 370 : 410);
    document.getElementById('sv-hebel').setAttribute('x1', st.e ? 490 : 530);
    document.getElementById('sv-hebel').setAttribute('x2', st.e ? 595 : 555);
    document.getElementById('sv-rz').setAttribute('transform', st.e ? 'translate(40 0)' : '');
    document.getElementById('sv-rzl').setAttribute('x', st.e ? 602 : 562);
    document.getElementById('sv-hk').setAttribute('x2', st.hk ? 560 : 586); document.getElementById('sv-hk').setAttribute('y2', st.hk ? 100 : 86);
    f30.on(!!st.f30); f50.on(!!st.f50);
    b.forEach(x => x.classList.toggle('on', +x.dataset.s === i));
    document.getElementById('sv-t').innerHTML = st.t;
  }
  b.forEach(x => x.onclick = () => s(+x.dataset.s)); s(0);
  setInterval(() => {
    wm = (wm + st.mot * 14) % 360; wz = (wz + st.zk * 4) % 360;
    document.getElementById('sv-mr').setAttribute('transform', 'rotate(' + wm + ' 420 245)');
    document.getElementById('sv-zk').setAttribute('transform', 'rotate(' + wz + ' 700 245)');
  }, 40);

  const FB = [
    [['Batterie leer', 'Steuerspannung an Klemme 50 fehlt (z. B. Wegfahrsperre, Kupplungs- oder Wählhebelschalter, Startrelais)', 'Magnetschalter defekt'],
     ['Batterie prüfen', 'Fehlerspeicher lesen', 'Spannung an Klemme 50 beim Starten messen']],
    [['Batterie zu schwach', 'Übergangswiderstand an Klemme 30 oder an der Masse', 'Hauptkontakt im Magnetschalter verbrannt', 'Starter defekt'],
     ['Spannung beim Starten an der Batterie', 'Spannungsfall Plusleitung und Masse unter Last', 'Spannung direkt an Klemme 30 am Starter beim Starten']],
    [['Batterie schwach oder kalt', 'Übergangswiderstände (Pole, Masseband)', 'Starter verschlissen (Bürsten, Lager)', 'falsches oder zu dickes Motoröl'],
     ['Batterietester', 'Spannungsfall unter Last', 'Starterstrom mit der Stromzange']],
    [['Freilauf rutscht durch', 'Ritzel spurt nicht ein (Einrückhebel, Magnetschalter)', 'Zähne am Ritzel oder Zahnkranz beschädigt'],
     ['Geräusch genau anhören', 'Starter ausbauen und Ritzel, Freilauf prüfen', 'Zahnkranz durch die Öffnung ansehen']],
    [['Klemme 50 bleibt an (Zündschloss oder Startrelais hängt)', 'Magnetschalter klemmt, Hauptkontakt verschweißt'],
     ['Sofort Batterie abklemmen!', 'Spannung an Klemme 50 nach dem Loslassen messen', 'Startrelais und Magnetschalter prüfen']]
  ];
  const fb = document.querySelectorAll('#s-fb [data-f]');
  function f(i) {
    document.getElementById('fb-u').innerHTML = FB[i][0].map(x => '<li>' + x + '</li>').join('');
    document.getElementById('fb-p').innerHTML = FB[i][1].map(x => '<li>' + x + '</li>').join('');
    fb.forEach(x => x.classList.toggle('on', +x.dataset.f === i));
  }
  fb.forEach(x => x.onclick = () => f(+x.dataset.f)); f(0);
})();
</script>'''


if __name__ == '__main__':
    seite('bn-aufbau.html', 'Aufbau des Bordnetzes – Bordnetz', 't-bn1', THEMA, aufbau, STYLE, aufbau_js)
    seite('bn-stromlaufplan.html', 'Stromlaufplan und Fehlersuche – Bordnetz', 't-bn2', THEMA, plan, STYLE, plan_js)
    seite('bn-batterie.html', 'Starterbatterie – Bordnetz', 't-bn3', THEMA, batterie, STYLE, batterie_js)
    seite('bn-generator.html', 'Generator – Bordnetz', 't-bn4', THEMA, gen, STYLE, gen_js)
    seite('bn-starter.html', 'Starter – Bordnetz', 't-bn5', THEMA, starter, STYLE, starter_js)
    print('ok')
