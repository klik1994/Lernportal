"""Datenbus-Systeme – vier Präsentationen.
Aufruf: cd tools && python3 datenbus.py"""
from praesentation_bauen import *

THEMA = 'Datenbus-Systeme'
K = 'FAHRZEUGELEKTRONIK · DATENBUS'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'
CH, CL = '#ff8f3f', '#28aaf5'   # CAN-High, CAN-Low

# ---------------------------------------------------------------- 1 Grundlagen
T = 'VERNETZUNG'
SG = [('Motor', 80, 60), ('Getriebe', 260, 60), ('ABS/ESP', 440, 60), ('Kombi', 80, 240), ('Klima', 260, 240), ('Airbag', 440, 240)]


def netz_svg():
    o = ['<svg viewBox="0 0 600 320" width="580" height="310" style="display:block;margin:0 auto" id="nz-svg">']
    # ohne Bus: viele Einzelleitungen
    w = []
    for i, (n, x, y) in enumerate(SG):
        for j, (m, x2, y2) in enumerate(SG):
            if j > i:
                w.append(f'<line x1="{x + 40}" y1="{y + 25}" x2="{x2 + 40}" y2="{y2 + 25}" stroke="#94a4ba" stroke-width="2"/>')
    o.append('<g id="nz-ohne">' + ''.join(w) + '</g>')
    o.append(f'<g id="nz-mit" style="display:none"><line x1="40" y1="160" x2="560" y2="160" stroke="{CH}" stroke-width="5"/><line x1="40" y1="172" x2="560" y2="172" stroke="{CL}" stroke-width="5"/>'
             + ''.join(f'<line x1="{x + 40}" y1="{y + 50 if y < 160 else y}" x2="{x + 40}" y2="{160 if y < 160 else 172}" stroke="#94a4ba" stroke-width="3"/>' for n, x, y in SG)
             + f'<text x="40" y="150" font-size="14" font-weight="800" fill="{CH}">CAN-High</text><text x="40" y="192" font-size="14" font-weight="800" fill="{CL}">CAN-Low</text>'
             + '<path id="nz-msg" d="M120 166 H560" fill="none" stroke="none"/></g>')
    for n, x, y in SG:
        o.append(f'<g class="nz-sg" data-n="{n}"><rect x="{x}" y="{y}" width="80" height="50" rx="8" fill="#213552" stroke="#ecf1f8" stroke-width="3"/><text x="{x + 40}" y="{y + 31}" text-anchor="middle" font-size="14" font-weight="900" fill="#ecf1f8">{n}</text></g>')
    o.append('</svg>')
    return ''.join(o)


grund = [
    titel_folie(K, 'BUS', 'Grundlagen der Vernetzung', 'Warum Steuergeräte miteinander „reden“', 'font-size:72px'),
    lernziele(T, ['Warum moderne Fahrzeuge Datenbusse haben', 'Wie Steuergeräte Botschaften austauschen',
                  'Welche Aufgabe das Gateway hat', 'Wie die Diagnose über den Bus läuft']),
    folie(T, 'Ohne und mit Datenbus – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" id="nz-a">Ohne Datenbus</button><button class="btn ghost" id="nz-b">Mit Datenbus</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.35fr 1fr">
      {netz_svg()}
      <div class="card" id="nz-t" style="font-size:17px;font-weight:600;line-height:1.55"></div>
    </div>''', sid='s-nz', body_cls='body noclick'),
    folie(T, 'Wie beim Gruppenchat', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big">Ein Steuergerät <span class="c">sendet eine Botschaft</span> – z. B. „Motordrehzahl 2.000 1/min“.</div></div>
      <div class="card step"><div class="big"><span class="c">Alle</span> Steuergeräte am Bus empfangen sie.</div></div>
      <div class="card step"><div class="big">Jedes Steuergerät nimmt nur, <span class="c">was es braucht</span> – Kombiinstrument und Getriebe nutzen die Drehzahl.</div></div>
      <div class="card step"><div class="big">Wichtige Botschaften haben <span class="c">Vorrang</span> – z. B. vom Airbag oder ABS.</div></div>
    </div>'''),
    folie(T, 'Die Vorteile', '''    <div class="values">
      <div class="val step from-left"><b>weniger Leitungen</b><span>weniger Gewicht, weniger Stecker, weniger Fehlerquellen</span></div>
      <div class="val step from-left"><b>ein Sensor – viele Nutzer</b><span>ein Signal, z. B. die Raddrehzahl, nutzen ABS, Motor, Navi und Kombi</span></div>
      <div class="val step from-left"><b>neue Funktionen</b><span>Assistenzsysteme brauchen Daten aus vielen Steuergeräten</span></div>
      <div class="val step from-left"><b>Diagnose</b><span>alle Steuergeräte über einen Stecker auslesen</span></div>
    </div>'''),
    folie(T, 'Das Gateway', '''    <div class="kette">
      <div class="glied step"><b>Antriebs-CAN</b><span>ISO 11898-2 – Motor, Getriebe, ABS</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Gateway</b><span>„Dolmetscher“ zwischen den Bussen</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Komfort-CAN (ISO 11898-3), LIN …</b><span>andere Geschwindigkeiten</span></div>
    </div>
    <div class="grid2" style="margin-top:18px">
      <div class="tip step"><b>Verschiedene Busse</b>Im Fahrzeug gibt es mehrere Bussysteme mit unterschiedlicher Geschwindigkeit. Das Gateway gibt Botschaften gezielt weiter.</div>
      <div class="tip step"><b>Diagnose</b>Der Diagnosetester ist am OBD-Stecker angeschlossen und spricht über das Gateway mit allen Steuergeräten.</div>
    </div>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>U-Fehlercodes</b>Kommunikationsfehler beginnen meist mit „U“, z. B. „keine Kommunikation mit Steuergerät …“.</div>
      <div class="tip step"><b>Ein Fehler – viele Meldungen</b>Fällt ein Steuergerät aus, melden viele andere, dass ihnen seine Botschaften fehlen.</div>
      <div class="warn step"><b>Spannungsversorgung</b>Eine schwache Batterie oder schlechte Masse kann viele Busfehler auslösen – zuerst prüfen.</div>
      <div class="tip step"><b>Software</b>Steuergeräte werden über den Bus programmiert und codiert – dabei Batterie mit Ladegerät stützen.</div>
    </div>'''),
    video(T, 'bus-grundlagen'),
    kurztest(T, [
        ('Warum haben moderne Fahrzeuge Datenbusse?', ['Weniger Leitungen, gemeinsame Nutzung von Daten', 'Damit das Auto schneller fährt', 'Weil Sensoren dann keinen Strom brauchen'], 0, 'Ein Signal kann von vielen Steuergeräten genutzt werden.'),
        ('Wer empfängt eine Botschaft auf dem CAN-Bus?', ['Nur ein Steuergerät', 'Alle Steuergeräte am Bus', 'Nur das Gateway'], 1, 'Jedes nimmt sich, was es braucht.'),
        ('Welche Aufgabe hat das Gateway?', ['Es lädt die Batterie', 'Es misst die Drehzahl', 'Es verbindet Busse und gibt Botschaften weiter'], 2, 'Es ist der „Dolmetscher“ zwischen den Bussystemen.'),
        ('Ein Steuergerät fällt aus. Was zeigt der Fehlerspeicher oft?', ['Viele Kommunikationsfehler bei anderen Steuergeräten', 'Gar nichts', 'Nur einen Ölstandsfehler'], 0, 'Die anderen vermissen seine Botschaften.'),
    ]),
    merke(T, ['Steuergeräte tauschen Botschaften über den Bus aus', 'Alle hören mit – jeder nimmt, was er braucht',
              'Gateway verbindet die Bussysteme', 'Diagnose über OBD-Stecker und Gateway']),
]
grund_js = '''<script src="assets/schaltung.js"></script>
<script>
(function () {
  const svg = document.getElementById('nz-svg');
  const fl = Flow(svg, document.getElementById('nz-msg'), { spacing: 60, speed: 120, r: 7, color: '#ffd34d' });
  const a = document.getElementById('nz-a'), b = document.getElementById('nz-b');
  function s(mit) {
    document.getElementById('nz-ohne').style.display = mit ? 'none' : '';
    document.getElementById('nz-mit').style.display = mit ? '' : 'none';
    fl.on(mit); a.classList.toggle('on', !mit); b.classList.toggle('on', mit);
    document.getElementById('nz-t').innerHTML = mit
      ? '<b>Mit Datenbus:</b> Alle Steuergeräte hängen an <span class="c">zwei gemeinsamen Leitungen</span> (CAN-High und CAN-Low). Die Daten laufen als Botschaften nacheinander über den Bus.'
      : '<b>Ohne Datenbus:</b> Jedes Steuergerät bräuchte eine eigene Leitung zu jedem anderen – schon bei 6 Steuergeräten 15 Leitungen. Heutige Fahrzeuge haben oft 50 und mehr Steuergeräte.';
  }
  a.onclick = () => s(false); b.onclick = () => s(true); s(false);
})();
</script>'''

# ---------------------------------------------------------------- 2 CAN-Bus
T = 'CAN-BUS'


def oszi_svg(id_, h=240):
    return f'''<svg viewBox="0 0 560 {h}" width="900" height="{int(h * 1.6)}" style="display:block;margin:0 auto;max-width:100%;height:auto" id="{id_}-svg">
  <rect x="40" y="10" width="510" height="{h - 40}" rx="8" fill="#18283f" stroke="#94a4ba" stroke-width="2"/>
  <g id="{id_}-grid"></g>
  <path id="{id_}-h" d="" fill="none" stroke="{CH}" stroke-width="3.5"/>
  <path id="{id_}-l" d="" fill="none" stroke="{CL}" stroke-width="3.5"/>
  <text x="44" y="{h - 12}" font-size="14" font-weight="800" fill="{CH}">CAN-High</text>
  <text x="140" y="{h - 12}" font-size="14" font-weight="800" fill="{CL}">CAN-Low</text>
  <g id="{id_}-ax"></g><text x="8" y="22" font-size="13" font-weight="800" fill="#94a4ba">V</text>
</svg>'''


R_SVG = f'''<svg viewBox="0 0 560 220" width="540" height="212" style="display:block;margin:0 auto" id="rw-svg">
  <line x1="60" y1="70" x2="500" y2="70" stroke="{CH}" stroke-width="5"/><line x1="60" y1="150" x2="500" y2="150" stroke="{CL}" stroke-width="5"/>
  <g id="rw-r1"><line x1="60" y1="70" x2="60" y2="85" stroke="#ecf1f8" stroke-width="3"/><rect x="48" y="85" width="24" height="50" rx="3" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/><line x1="60" y1="135" x2="60" y2="150" stroke="#ecf1f8" stroke-width="3"/><text x="82" y="116" font-size="14" font-weight="800" fill="#94a4ba">120 Ω</text></g>
  <g id="rw-r2"><line x1="500" y1="70" x2="500" y2="85" stroke="#ecf1f8" stroke-width="3"/><rect x="488" y="85" width="24" height="50" rx="3" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/><line x1="500" y1="135" x2="500" y2="150" stroke="#ecf1f8" stroke-width="3"/><text x="436" y="116" font-size="14" font-weight="800" fill="#94a4ba">120 Ω</text></g>
  <line id="rw-ks" x1="280" y1="70" x2="280" y2="150" stroke="#f05e4e" stroke-width="5" style="display:none"/>
  <text x="62" y="55" font-size="14" font-weight="800" fill="#94a4ba">Steuergerät A</text><text x="500" y="55" text-anchor="end" font-size="14" font-weight="800" fill="#94a4ba">Steuergerät B</text>
  <circle cx="230" cy="70" r="6" fill="#ecf1f8"/><circle cx="230" cy="150" r="6" fill="#ecf1f8"/>
  <path d="M230 70 V40 H200 M230 150 V190 H200" fill="none" stroke="#ecf1f8" stroke-width="2" stroke-dasharray="5 4"/>
  <text x="196" y="44" text-anchor="end" font-size="13" font-weight="800" fill="#94a4ba">Messspitze rot</text><text x="196" y="194" text-anchor="end" font-size="13" font-weight="800" fill="#94a4ba">Messspitze schwarz</text>
</svg>'''

can = [
    titel_folie(K, 'CAN', 'CAN-Bus', 'Zwei Leitungen, zwei Pegel, zwei Abschlusswiderstände', 'font-size:72px'),
    lernziele(T, ['Wie der CAN-Bus aufgebaut ist', 'Wie die Pegel auf CAN-High und CAN-Low aussehen',
                  'Wozu die Abschlusswiderstände dienen', 'Was CAN nach ISO 11898-2 und ISO 11898-3 unterscheidet']),
    folie(T, 'Aufbau', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Zwei verdrillte Leitungen</b>CAN-High und CAN-Low sind miteinander verdrillt. Störungen wirken auf beide gleich – das Steuergerät wertet nur den Unterschied aus.</div>
      <div class="tip step"><b>Abschlusswiderstände</b>An den beiden Enden des Busses je 120 Ω zwischen CAN-High und CAN-Low – sie verhindern Signal-Reflexionen.</div>
      <div class="tip step"><b>Linienstruktur</b>Alle Steuergeräte hängen an denselben zwei Leitungen. Jedes kann senden und empfangen.</div>
      <div class="tip step"><b>Geschwindigkeit</b>CAN nach ISO 11898-2 (z. B. Antrieb) bis 1 Mbit/s, meist 500 kbit/s. CAN nach ISO 11898-3 (fehlertolerant, z. B. Komfort) bis 125 kbit/s – Richtwerte.</div>
    </div>'''),
    folie(T, 'Die Pegel – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-c="hs">ISO 11898-2</button><button class="btn ghost" data-c="ls">ISO 11898-3</button></div>
    {oszi_svg('pg', 200)}
    <div class="card" id="pg-t" style="font-size:17px;font-weight:600;line-height:1.55;margin-top:8px"></div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">Beide Leitungen gegen Masse gemessen. Richtwerte – genaue Werte laut Hersteller.</p>''', sid='s-pg', body_cls='body noclick'),
    folie(T, 'Dominant und rezessiv', '''    <div class="values">
      <div class="val step from-left"><b>rezessiv = 1</b><span>Ruhezustand nach ISO 11898-2 – beide Leitungen ca. 2,5 V, kein Unterschied</span></div>
      <div class="val step from-left"><b>dominant = 0</b><span>CAN-High steigt auf ca. 3,5 V, CAN-Low fällt auf ca. 1,5 V – Unterschied ca. 2 V</span></div>
      <div class="val step from-left"><b>dominant gewinnt</b><span>Senden zwei gleichzeitig, setzt sich die „0“ durch – die Botschaft mit der höheren Priorität kommt zuerst</span></div>
    </div>
    <div class="note step">Richtwerte für CAN nach ISO 11898-2</div>'''),
    folie(T, 'Abschlusswiderstände messen – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px;flex-wrap:wrap"><button class="btn ghost on" data-r="ok">Alles in Ordnung</button><button class="btn ghost" data-r="r2">Ein Widerstand fehlt</button><button class="btn ghost" data-r="ks">CAN-H an CAN-L</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.35fr 1fr">
      {R_SVG}
      <div>
        <div class="card"><div class="muted" style="font-size:15px;font-weight:800">OHMMETER ZEIGT</div><div class="lcd2" id="rw-v" style="font-size:32px;margin-top:6px">60 Ω</div></div>
        <div class="card" id="rw-t" style="margin-top:10px;font-size:16px;font-weight:600;line-height:1.5"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">Nur am spannungsfreien Bus messen: Zündung aus, Busruhe abwarten bzw. Batterie abklemmen – nach Herstellervorgabe. Über den Prüfadapter, z. B. am OBD-Stecker (Pin 6 und 14).</p>''', sid='s-rw', body_cls='body noclick'),
    folie(T, 'ISO 11898-3 und Eindrahtbetrieb', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">CAN nach ISO 11898-3 (fehlertolerant)</div>
        <ul UL><li>langsamer, bis 125 kbit/s – z. B. Komfortbereich</li><li>andere Pegel: CAN-High ca. 0 V ↔ 3,6 V, CAN-Low ca. 5 V ↔ 1,4 V (Richtwerte)</li><li>z. B. Türen, Sitze, Klima</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Eindrahtbetrieb</div>
        <ul UL><li>fällt eine Leitung aus, arbeitet der CAN nach ISO 11898-3 mit der anderen weiter</li><li>Fehlerspeicher: „Eindrahtbetrieb“</li><li>der CAN nach ISO 11898-2 kann das nicht – dort fällt die Kommunikation aus</li></ul></div>
    </div>'''.replace('UL', UL)),
    video(T, 'bus-can'),
    kurztest(T, [
        ('Warum sind CAN-High und CAN-Low verdrillt?', ['Damit Störungen auf beide Leitungen gleich wirken', 'Damit sie besser halten', 'Damit sie weniger kosten'], 0, 'Ausgewertet wird nur der Unterschied zwischen den Leitungen.'),
        ('Welche Pegel hat der CAN nach ISO 11898-2 im dominanten Zustand etwa?', ['Beide 2,5 V', 'CAN-H ca. 3,5 V, CAN-L ca. 1,5 V', 'Beide 12 V'], 1, 'Im Ruhezustand (rezessiv) liegen beide bei ca. 2,5 V.'),
        ('Was misst du zwischen CAN-High und CAN-Low am intakten, spannungsfreien Bus?', ['120 Ω', '0 Ω', 'ca. 60 Ω'], 2, 'Zwei Abschlusswiderstände à 120 Ω parallel ergeben 60 Ω.'),
        ('Du misst 120 Ω statt 60 Ω. Was ist wahrscheinlich?', ['Ein Abschlusswiderstand fehlt oder eine Leitung ist unterbrochen', 'Alles in Ordnung', 'Kurzschluss zwischen CAN-H und CAN-L'], 0, 'Dann wird nur noch ein Widerstand gemessen.'),
    ]),
    merke(T, ['Zwei verdrillte Leitungen: CAN-High und CAN-Low', 'ISO 11898-2: Ruhe 2,5 V – dominant 3,5 V / 1,5 V',
              '2 × 120 Ω parallel = 60 Ω', 'ISO 11898-3 kann im Eindrahtbetrieb weiterarbeiten']),
]
OSZI_JS = '''
function Oszi(id, opt) {
  const H = opt.h || 240, x0 = 40, x1 = 550, y0 = 10, y1 = H - 30;
  const vmax = opt.vmax || 5;
  const Y = v => y1 - (v / vmax) * (y1 - y0 - 10) - 5;
  const g = document.getElementById(id + '-grid'), ax = document.getElementById(id + '-ax');
  g.innerHTML = ''; ax.innerHTML = '';
  for (let v = 0; v <= vmax; v += (opt.step || 1)) {
    g.insertAdjacentHTML('beforeend', '<line x1="' + x0 + '" y1="' + Y(v) + '" x2="' + x1 + '" y2="' + Y(v) + '" stroke="#94a4ba" stroke-width="1" stroke-dasharray="3 5" opacity=".5"/>');
    ax.insertAdjacentHTML('beforeend', '<text x="34" y="' + (Y(v) + 4) + '" text-anchor="end" font-size="12" font-weight="800" fill="#94a4ba">' + String(v).replace('.', ',') + '</text>');
  }
  return function (fh, fl) {
    let dh = '', dl = '';
    for (let x = x0 + 4; x <= x1 - 4; x += 2) {
      const k = (x - x0) / (x1 - x0);
      dh += (dh ? ' L' : 'M') + x + ' ' + Y(fh(k)).toFixed(1);
      dl += (dl ? ' L' : 'M') + x + ' ' + Y(fl(k)).toFixed(1);
    }
    document.getElementById(id + '-h').setAttribute('d', dh);
    document.getElementById(id + '-l').setAttribute('d', dl);
  };
}
const BITS = [1,1,0,1,0,0,1,0,1,1,0,1,1];
const bit = k => BITS[Math.min(BITS.length - 1, Math.floor(k * BITS.length))];
'''
can_js = '''<script>
(function () {
''' + OSZI_JS + '''
  const bt = document.querySelectorAll('#s-pg [data-c]');
  const T = {
    hs: '<b>CAN nach ISO 11898-2:</b> In Ruhe (rezessiv) liegen <span class="ora">CAN-High</span> und <span class="blu">CAN-Low</span> bei ca. 2,5 V. Bei einer „0“ (dominant) geht CAN-High auf ca. 3,5 V und CAN-Low auf ca. 1,5 V. Die beiden Signale sind spiegelbildlich.',
    ls: '<b>CAN nach ISO 11898-3 (fehlertolerant):</b> In Ruhe liegt <span class="ora">CAN-High</span> bei ca. 0 V und <span class="blu">CAN-Low</span> bei ca. 5 V. Dominant: CAN-High ca. 3,6 V, CAN-Low ca. 1,4 V. Auch hier spiegelbildlich.'
  };
  function c(m) {
    const draw = Oszi('pg', { vmax: 5, step: 1, h: 200 });
    if (m === 'hs') draw(k => bit(k) ? 2.5 : 3.5, k => bit(k) ? 2.5 : 1.5);
    else draw(k => bit(k) ? 0.1 : 3.6, k => bit(k) ? 4.9 : 1.4);
    bt.forEach(b => b.classList.toggle('on', b.dataset.c === m));
    document.getElementById('pg-t').innerHTML = T[m];
  }
  bt.forEach(b => b.onclick = () => c(b.dataset.c)); c('hs');

  const R = {
    ok: ['60 Ω', '<b class="grn">In Ordnung:</b> Beide 120-Ω-Widerstände sind <b>parallel</b> geschaltet – zusammen 60 Ω.', 1, 0],
    r2: ['120 Ω', '<b class="ora">Ein Widerstand fehlt:</b> Nur noch 120 Ω – Abschlusswiderstand oder Steuergerät mit Widerstand fehlt, oder eine Leitung ist unterbrochen.', 0, 0],
    ks: ['ca. 0 Ω', '<b class="red">Kurzschluss:</b> CAN-High und CAN-Low haben Verbindung – z. B. gequetschte Leitung. Der Bus funktioniert nicht.', 1, 1]
  };
  const rb = document.querySelectorAll('#s-rw [data-r]');
  function r(m) {
    const [v, t, r2, ks] = R[m];
    document.getElementById('rw-v').textContent = v; document.getElementById('rw-t').innerHTML = t;
    document.getElementById('rw-r2').style.opacity = r2 ? 1 : 0.12;
    document.getElementById('rw-ks').style.display = ks ? '' : 'none';
    rb.forEach(b => b.classList.toggle('on', b.dataset.r === m));
  }
  rb.forEach(b => b.onclick = () => r(b.dataset.r)); r('ok');
})();
</script>'''

# ---------------------------------------------------------------- 3 Weitere Bussysteme
T = 'BUSSYSTEME'
BUS = [
    ('lin', 'LIN', '1 Leitung', 'bis 20 kbit/s', 'Master und Slaves (bis 16 Teilnehmer)', 'Fensterheber, Regensensor, Spiegel, Generator, Klimabedienteil',
     'Günstig für einfache Aufgaben. Der Master fragt die Slaves der Reihe nach ab. Pegel: rezessiv ca. 12 V (Batteriespannung), dominant ca. 1 V.'),
    ('can', 'CAN', '2 Leitungen (verdrillt)', 'z. B. 100 bis 500 kbit/s', 'alle gleichberechtigt', 'Motor, Getriebe, ABS, Komfort',
     'Das Standard-Bussystem im Fahrzeug. Wer die wichtigste Botschaft hat, darf zuerst senden.'),
    ('flex', 'FlexRay', '2 Leitungen, oft 2 Kanäle', 'bis 10 Mbit/s', 'feste Zeitfenster für jedes Steuergerät', 'Fahrwerk, Lenkung, Assistenzsysteme',
     'Sehr schnell und zeitgesteuert: Jedes Steuergerät hat einen festen Sendeplatz – wichtig für sicherheitsrelevante Systeme.'),
    ('most', 'MOST', 'Lichtwellenleiter', 'bis ca. 150 Mbit/s', 'Ring – Daten laufen von Gerät zu Gerät', 'Radio, Navigation, Verstärker, Bildschirme',
     'Daten werden als Licht übertragen. Fällt ein Gerät aus oder ist der Lichtwellenleiter beschädigt, ist der ganze Ring gestört (Ringbruch).'),
    ('eth', 'Automotive Ethernet', '2 verdrillte Leitungen', '100 Mbit/s bis über 1 Gbit/s', 'Stern über Switches', 'Kameras, Assistenzsysteme, Software-Updates',
     'Für sehr große Datenmengen – z. B. Kamerabilder für Assistenzsysteme und Updates über das Internet.'),
]
busse = [
    titel_folie(K, 'LIN', 'LIN, FlexRay, MOST, Ethernet', 'Welches Bussystem wofür?', 'font-size:72px'),
    lernziele(T, ['Welche Bussysteme es im Fahrzeug gibt', 'Wie LIN arbeitet',
                  'Wie FlexRay zeitgesteuert arbeitet', 'Worauf du bei Lichtwellenleitern achten musst']),
    folie(T, 'Bussysteme im Vergleich – zum Ausprobieren', '''    <div class="choice" style="margin-bottom:12px;flex-wrap:wrap">''' + ''.join(f'<button class="btn ghost" data-b="{k}">{n}</button>' for k, n, *_ in BUS) + '''</div>
    <div class="grid2" style="align-items:start">
      <div class="values" id="bs-v"></div>
      <div class="card" id="bs-t" style="font-size:17px;font-weight:600;line-height:1.55"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">Richtwerte – je nach Hersteller und Fahrzeug.</p>''', sid='s-bs', body_cls='body noclick'),
    folie(T, 'LIN-Bus – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-n="0">Master fragt</button><button class="btn ghost" data-n="1">Slave antwortet</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.35fr 1fr">
      {oszi_svg('ln', 220)}
      <div class="card" id="ln-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>''', sid='s-ln', body_cls='body noclick'),
    folie(T, 'FlexRay – zeitgesteuert, zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-m="fr">FlexRay</button><button class="btn ghost" data-m="can">Zum Vergleich: CAN</button></div>
    <svg viewBox="0 0 900 230" style="display:block;margin:0 auto;max-width:100%;height:auto" id="fz-svg"></svg>
    <div class="card" id="fz-t" style="font-size:17px;font-weight:600;line-height:1.55;margin-top:8px"></div>''', sid='s-fz', body_cls='body noclick'),
    folie(T, 'FlexRay – Aufbau und Pegel', f'''    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {oszi_svg('fp', 200)}
      <ul UL>
        <li>Zwei verdrillte Leitungen: <b>BP</b> (Bus Plus) und <b>BM</b> (Bus Minus)</li>
        <li>Ruhe: beide ca. 2,5 V – Daten: ca. 3 V / 2 V, spiegelbildlich</li>
        <li>oft <b>zwei Kanäle</b> (A und B) – fällt einer aus, läuft der andere weiter</li>
        <li>Aufbau als Linie oder Stern mit Abschlusswiderständen</li>
        <li>z. B. adaptive Dämpfer, Aktivlenkung, Abstandsregeltempomat</li>
      </ul>
    </div>
    <div class="grid2" style="margin-top:10px">
      <div class="tip step"><b>Prüfen</b>Signal mit dem Oszilloskop (BP und BM gegen Masse) am Prüfadapter, Abschlusswiderstände nach Herstellerangabe messen.</div>
      <div class="warn step"><b>Reparatur</b>Nur nach Herstellervorgabe – Verdrillung und Leitungslänge sind wichtig. Nach Steuergerätetausch oft codieren.</div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Richtwerte – genaue Werte laut Hersteller.</p>'''.replace('UL', UL), sid='s-fp'),
    folie(T, 'Lichtwellenleiter (MOST)', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Nicht knicken</b>Mindest-Biegeradius einhalten (Richtwert ca. 25 mm) – sonst wird das Licht gedämpft oder die Faser bricht.</div>
      <div class="warn step"><b>Nicht hineinschauen</b>Nicht direkt in leuchtende Lichtwellenleiter oder Stecker schauen.</div>
      <div class="tip step"><b>Sauber halten</b>Steckerenden mit Schutzkappen verschließen – Schmutz dämpft das Licht.</div>
      <div class="tip step"><b>Reparatur</b>Nur mit dem Reparaturset und Werkzeug des Herstellers. Ringbruchdiagnose mit dem Diagnosetester.</div>
    </div>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>LIN-Slave tauschen</b>Neue LIN-Teilnehmer müssen oft angelernt oder codiert werden.</div>
      <div class="tip step"><b>Generator am LIN</b>Viele Generatoren werden über LIN vom Motorsteuergerät geregelt.</div>
      <div class="tip step"><b>Ethernet</b>Für Kameras und Updates. Steckverbinder nicht beschädigen, Verdrillung bei Reparaturen erhalten.</div>
      <div class="warn step"><b>Verdrillung</b>Bei Reparaturen an CAN- und Ethernet-Leitungen die Verdrillung erhalten – nur nach Herstellervorgabe reparieren.</div>
    </div>'''),
    video(T, 'bus-systeme'),
    kurztest(T, [
        ('Wie viele Leitungen hat der LIN-Bus?', ['Eine', 'Zwei', 'Vier'], 0, 'LIN ist ein Eindraht-Bus mit einem Master.'),
        ('Womit überträgt der MOST-Bus die Daten?', ['Mit Funk', 'Mit Licht über Lichtwellenleiter', 'Über die Stromversorgung'], 1, 'Darum: nicht knicken, Biegeradius einhalten.'),
        ('Wofür wird Automotive Ethernet vor allem genutzt?', ['Für den Fensterheber', 'Für den Zigarettenanzünder', 'Für große Datenmengen, z. B. Kameras und Updates'], 2, 'Ethernet ist sehr schnell.'),
        ('Was ist bei FlexRay besonders?', ['Feste Zeitfenster für jedes Steuergerät', 'Nur eine Leitung', 'Übertragung mit Licht'], 0, 'Zeitgesteuert – wichtig für sicherheitsrelevante Systeme.'),
    ]),
    merke(T, ['LIN: 1 Leitung, Master und Slaves, langsam', 'CAN: Standard, 2 verdrillte Leitungen',
              'FlexRay: schnell und zeitgesteuert|MOST: Licht im Ring', 'Ethernet: sehr große Datenmengen']),
]
busse_js = '''<script>
(function () {
''' + OSZI_JS + '''
  const B = ''' + str({k: [n, l, v, t, a, txt] for k, n, l, v, t, a, txt in BUS}).replace("'", '"') + ''';
  const bt = document.querySelectorAll('#s-bs [data-b]');
  function b(k) {
    const [n, l, v, t, a, txt] = B[k];
    document.getElementById('bs-v').innerHTML = [['Leitung', l], ['Tempo', v], ['Aufbau', t], ['Beispiele', a]].map(x => '<div class="val"><b>' + x[0] + '</b><span>' + x[1] + '</span></div>').join('');
    document.getElementById('bs-t').innerHTML = '<b class="c">' + n + ':</b> ' + txt;
    bt.forEach(x => x.classList.toggle('on', x.dataset.b === k));
  }
  bt.forEach(x => x.onclick = () => b(x.dataset.b)); b('lin');

  const lb = document.querySelectorAll('#s-ln [data-n]');
  const LT = ['<b>Master fragt:</b> Das LIN-Master-Steuergerät (z. B. Türsteuergerät) sendet den Kopf der Botschaft: „Fensterheber, meldet euch!“ Pegel: in Ruhe (rezessiv) ca. 12 V (Batteriespannung), dominant ca. 1 V. Der Kopf beginnt mit einer langen dominanten Pause (Break), dann folgt das Synchronisationsfeld.',
              '<b>Slave antwortet:</b> Nur der angesprochene Slave (z. B. Fensterhebermotor) hängt seine Antwort an – z. B. Position und Status. So wird ein Teilnehmer nach dem anderen abgefragt.'];
  document.getElementById('ln-l').style.display = 'none';
  document.querySelector('#ln-svg text[fill="#28aaf5"]').style.display = 'none';
  document.querySelector('#ln-svg text[fill="#ff8f3f"]').textContent = 'LIN-Leitung';
  function seq(i) {
    const byte = v => { const o = [0]; for (let k = 0; k < 8; k++) o.push((v >> k) & 1); o.push(1); return o; };
    let q = [1, 1, 1, 1, 1];
    q = q.concat(Array(13).fill(0), [1], byte(0x55), byte(0x8A));
    if (i) q = q.concat([1], byte(0x3C), byte(0xA6));
    while (q.length < 80) q.push(1);
    return q;
  }
  function l(i) {
    const draw = Oszi('ln', { vmax: 14, step: 2, h: 220 });
    const q = seq(i);
    draw(k => q[Math.min(q.length - 1, Math.floor(k * q.length))] ? 12 : 1, k => 0);
    lb.forEach(x => x.classList.toggle('on', +x.dataset.n === i));
    document.getElementById('ln-t').innerHTML = LT[i];
  }
  lb.forEach(x => x.onclick = () => l(+x.dataset.n)); l(0);

  // FlexRay
  const SL = ['Fahrwerk', 'Lenkung', 'ACC', 'ABS/ESP', 'Motor', 'Getriebe'];
  const fzb = document.querySelectorAll('#s-fz [data-m]'); let fm = 'fr', tt = 0;
  function fzDraw() {
    const sv = document.getElementById('fz-svg'), v = window.innerWidth < 700;
    // Box in Zeitachse: t = Position 0..1, len = Länge, ch = Kanal 0/1
    const W = v ? 360 : 900, H = v ? 470 : 230;
    sv.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    const t0 = v ? 50 : 100, tL = v ? 390 : 780;
    const box = (t, len, ch, txt, col, dash) => {
      let x, y, w, h;
      if (v) { x = 90 + ch * 140; w = 120; y = t0 + t * tL; h = len * tL - 6; }
      else { y = 40 + ch * 80; h = 50; x = t0 + t * tL; w = len * tL - 5; }
      return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="6" fill="' + (dash ? 'none' : '#213552') + '" stroke="' + col + '" stroke-width="' + (dash ? 2 : 3) + '"' + (dash ? ' stroke-dasharray="6 5"' : '') + '/>' +
        '<text x="' + (x + w / 2) + '" y="' + (y + h / 2 + 5) + '" text-anchor="middle" font-size="' + (v ? 15 : 13) + '" font-weight="900" fill="' + (dash ? '#94a4ba' : '#ecf1f8') + '">' + txt + '</text>';
    };
    let o = v ? '<text x="150" y="30" text-anchor="middle" font-size="16" font-weight="900" fill="#ecf1f8">Kanal A</text><text x="290" y="30" text-anchor="middle" font-size="16" font-weight="900" fill="#ecf1f8">Kanal B</text>'
              : '<text x="10" y="70" font-size="16" font-weight="900" fill="#ecf1f8">Kanal A</text><text x="10" y="150" font-size="16" font-weight="900" fill="#ecf1f8">Kanal B</text>';
    const lab = (t, txt) => v ? '<text x="78" y="' + (t0 + t * tL + 14) + '" text-anchor="end" font-size="12" font-weight="800" fill="#94a4ba">' + txt + '</text>'
                               : '<text x="' + (t0 + t * tL) + '" y="215" font-size="14" font-weight="800" fill="#94a4ba">' + txt + '</text>';
    if (fm === 'fr') {
      for (let c = 0; c < 2; c++) { for (let i = 0; i < 6; i++) o += box(i * 0.1, 0.1, c, SL[i], '#1fc8b3'); o += box(0.6, 0.4, c, v ? 'bei Bedarf' : 'dynamisch: bei Bedarf', '#94a4ba', 1); }
      o += v ? lab(0, 'fest') + lab(0.6, 'frei') : lab(0, 'statischer Teil: feste Zeitfenster') + lab(0.6, 'dynamischer Teil');
      document.getElementById('fz-t').innerHTML = '<b>FlexRay:</b> Jedes Steuergerät hat in jedem Zyklus sein <span class="c">festes Zeitfenster</span> – wie ein Fahrplan. So kommt jede Botschaft garantiert pünktlich an. Die gleichen Daten laufen oft auf <span class="c">Kanal A und B</span> – doppelt sicher. Ein Zyklus dauert nur wenige Millisekunden.';
    } else {
      [[0, 'Motor'], [0.11, 'ABS'], [0.3, 'Klima'], [0.4, 'Motor'], [0.58, 'Lenkung'], [0.74, 'ABS'], [0.85, 'Getriebe']].forEach(([t, n]) => o += box(t, 0.1, 0, n, '#ff8f3f'));
      o += v ? '<text x="290" y="250" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">kein zweiter</text><text x="290" y="270" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Kanal</text>'
             : '<text x="480" y="150" text-anchor="middle" font-size="15" font-weight="800" fill="#94a4ba">kein zweiter Kanal</text>';
      o += v ? lab(0, 'nach Bedarf') : lab(0, 'Botschaften, wenn sie gerade anfallen');
      document.getElementById('fz-t').innerHTML = '<b>CAN zum Vergleich:</b> Gesendet wird, wenn eine Botschaft anfällt. Wollen zwei gleichzeitig, gewinnt die wichtigere – die andere muss <span class="ora">warten</span>. Darum ist nicht genau vorhersehbar, wann eine Botschaft ankommt.';
    }
    o += v ? '<line id="fz-cur" x1="84" x2="356" stroke="#ffd34d" stroke-width="4"/>' : '<line id="fz-cur" y1="30" y2="190" stroke="#ffd34d" stroke-width="4"/>';
    sv.innerHTML = o; fzb.forEach(b => b.classList.toggle('on', b.dataset.m === fm));
  }
  window.addEventListener('resize', fzDraw);
  fzb.forEach(b => b.onclick = () => { fm = b.dataset.m; fzDraw(); }); fzDraw();
  setInterval(() => { tt = (tt + 0.005) % 1; const c = document.getElementById('fz-cur'); if (!c) return; const v = window.innerWidth < 700, q = (v ? 50 : 100) + tt * (v ? 390 : 780); if (v) { c.setAttribute('y1', q); c.setAttribute('y2', q); } else { c.setAttribute('x1', q); c.setAttribute('x2', q); } }, 40);
  const fpd = Oszi('fp', { vmax: 5, step: 1, h: 200 });
  fpd(k => { const b = bit(k * 1.3 % 1); return k < 0.12 || k > 0.92 ? 2.5 : (b ? 3 : 2); }, k => { const b = bit(k * 1.3 % 1); return k < 0.12 || k > 0.92 ? 2.5 : (b ? 2 : 3); });
  document.querySelector('#fp-svg text[fill="#ff8f3f"]').textContent = 'BP';
  document.querySelector('#fp-svg text[fill="#28aaf5"]').textContent = 'BM';
})();
</script>'''

# ---------------------------------------------------------------- 4 Diagnose
T = 'BUS-DIAGNOSE'
diag = [
    titel_folie(K, '?', 'Diagnose am Datenbus', 'Fehlerspeicher, Oszilloskop, 60 Ω und Ruhestrom', 'font-size:120px'),
    lernziele(T, ['In welcher Reihenfolge du Busfehler suchst', 'Die 7 Fehlerfälle nach ISO am Oszilloskop erkennen',
                  'Wie du die Abschlusswiderstände prüfst', 'Was Busruhe und Ruhestrom miteinander zu tun haben']),
    folie(T, 'Schritt für Schritt', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher aller Steuergeräte lesen<small>welche Steuergeräte melden Kommunikationsfehler – und mit wem?</small></li>
      <li class="step">Spannungsversorgung und Masse prüfen<small>Batterie, Sicherungen, Masse der betroffenen Steuergeräte</small></li>
      <li class="step">Signal mit dem Oszilloskop ansehen<small>CAN-High und CAN-Low gegen Masse, am Prüfadapter</small></li>
      <li class="step">Spannungsfrei: Widerstand zwischen CAN-High und CAN-Low<small>ca. 60 Ω – Steuergeräte nacheinander abstecken, um den Fehler einzugrenzen</small></li>
    </ol>'''),
    folie(T, 'Fehlerbilder – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px;flex-wrap:wrap"><button class="btn ghost on" data-f="ok">In Ordnung</button><button class="btn ghost" data-f="hl">CAN-H an CAN-L</button><button class="btn ghost" data-f="hm">CAN-H an Masse</button><button class="btn ghost" data-f="lp">CAN-L an Plus</button><button class="btn ghost" data-f="rf">Abschluss fehlt</button></div>
    {oszi_svg('fb', 200)}
    <div class="card" id="fb-t" style="font-size:17px;font-weight:600;line-height:1.55;margin-top:8px"></div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">CAN nach ISO 11898-2, vereinfacht. Richtwerte.</p>''', sid='s-fb', body_cls='body noclick'),
    folie(T, 'Die 7 Fehlerfälle nach ISO – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:8px"><button class="btn ghost on" data-n="2">ISO 11898-2</button><button class="btn ghost" data-n="3">ISO 11898-3</button></div>
    <div class="choice f7c" style="margin-bottom:10px;flex-wrap:wrap;gap:6px"><button class="btn ghost on" data-i="1">1 · CAN-H unterbrochen</button><button class="btn ghost" data-i="2">2 · CAN-L unterbrochen</button><button class="btn ghost" data-i="3">3 · CAN-H an Plus</button><button class="btn ghost" data-i="4">4 · CAN-L an Masse</button><button class="btn ghost" data-i="5">5 · CAN-H an Masse</button><button class="btn ghost" data-i="6">6 · CAN-L an Plus</button><button class="btn ghost" data-i="7">7 · CAN-H an CAN-L</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {oszi_svg('f7', 200)}
      <div class="card" id="f7-t" style="font-size:16px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">Vereinfachte Beispielbilder, gemessen gegen Masse am Prüfadapter. Das echte Bild hängt davon ab, wo der Fehler sitzt und wo du misst. Richtwerte.</p>''', sid='s-f7', body_cls='body noclick'),
    folie(T, 'Die 7 Fehlerfälle – so findest du sie', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher lesen<small>z. B. „Eindrahtbetrieb“, „Kurzschluss nach Masse“ oder „nach Plus“ – gibt den ersten Hinweis</small></li>
      <li class="step">Oszilloskop: beide Leitungen gegen Masse<small>welche Leitung zeigt kein Signal, 0 V oder Batteriespannung?</small></li>
      <li class="step">Spannungsfrei messen (Batterie abklemmen)<small>CAN-H gegen CAN-L, CAN-H und CAN-L jeweils gegen Masse und gegen Plus – ein Kurzschluss zeigt fast 0 Ω</small></li>
      <li class="step">Eingrenzen<small>Steuergeräte und Steckverbindungen nacheinander trennen, bis der Fehler verschwindet – dann Leitung freilegen (Scheuerstelle, Korrosion)</small></li>
    </ol>
    <div class="tip step" style="margin-top:6px"><b>Gleiches Bild, anderer Fehler</b>Fall 1 und Fall 5 sehen bei ISO 11898-3 am Oszilloskop gleich aus (CAN-H bleibt bei 0 V). Unterscheiden kannst du sie nur mit der Widerstandsmessung gegen Masse.</div>'''),
    folie(T, 'Busruhe und Ruhestrom – zum Ausprobieren', '''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-z="0">Alles in Ordnung</button><button class="btn ghost" data-z="1">Ein Steuergerät bleibt wach</button></div>
    <div class="ctrl"><span style="width:300px">Zeit nach „Fahrzeug abschließen“: <span class="c" id="rs-n">0 min</span></span><input type="range" id="rs" min="0" max="60" step="1" value="0"></div>
    <div class="grid2" style="align-items:center;margin-top:12px">
      <div class="card"><div class="muted" style="font-size:15px;font-weight:800">RUHESTROM (STROMZANGE)</div><div class="lcd2" id="rs-v" style="font-size:32px;margin-top:6px">—</div><div id="rs-s" style="margin-top:8px;font-weight:800"></div></div>
      <div class="card" id="rs-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">Beispielwerte. Zeit bis zur Busruhe und zulässiger Ruhestrom laut Hersteller.</p>''', sid='s-rs', body_cls='body noclick'),
    folie(T, 'Ruhestrom richtig messen', '''    <ol class="steps-list">
      <li class="step">Stromzange um das Minuskabel der Batterie<small>so bleibt der Bordnetzspeicher erhalten – kein Abklemmen nötig</small></li>
      <li class="step">Fahrzeug in Ruhe versetzen<small>alle Verbraucher aus, Türen zu bzw. Kontakte überlisten, Fahrzeug verriegeln</small></li>
      <li class="step">Busruhe abwarten<small>die Steuergeräte schlafen erst nach einer Zeit ein – Zeit laut Hersteller</small></li>
      <li class="step">Zu hoch? Verbraucher eingrenzen<small>Stromzange bleibt dran. Sicherungen nacheinander ziehen und den Ruhestrom beobachten. Fällt der Wert auf normal, steckt der Fehler in diesem Stromkreis. Danach weiter eingrenzen: Steckverbindungen oder Steuergeräte in diesem Stromkreis nacheinander trennen.</small></li>
    </ol>
    <div class="warn step" style="margin-top:6px"><b>Nicht stören</b>Tür öffnen, Schlüssel in der Nähe oder Diagnosetester angesteckt – das weckt den Bus wieder auf.</div>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Wasser im Stecker</b>Korrosion an Steckern ist ein häufiger Grund für Busfehler – Sichtprüfung lohnt sich.</div>
      <div class="tip step"><b>Nachrüstgeräte</b>Falsch angeschlossenes Zubehör kann den Bus stören oder wach halten.</div>
      <div class="warn step"><b>Nicht in den Stecker stechen</b>Am Bus nur über Prüfadapter messen – keine Prüflampe, keine Messspitzen in die Kontakte.</div>
      <div class="tip step"><b>Steuergerät abstecken</b>Verschwindet die Störung, wenn ein Steuergerät abgesteckt ist, liegt der Fehler dort oder in seiner Leitung.</div>
    </div>'''),
    video(T, 'bus-diagnose'),
    kurztest(T, [
        ('Womit siehst du die Signale auf CAN-High und CAN-Low am besten?', ['Mit dem Oszilloskop', 'Mit der Prüflampe', 'Mit dem Ohmmeter im Betrieb'], 0, 'Am besten zweikanalig, beide Leitungen gegen Masse.'),
        ('Beide CAN-Leitungen zeigen dauernd ca. 2,5 V, kein Signal. Was kann die Ursache sein?', ['Alles in Ordnung', 'Kurzschluss zwischen CAN-High und CAN-Low', 'Batterie zu voll'], 1, 'Die Leitungen haben Verbindung – kein Unterschied möglich.'),
        ('Warum ist die Batterie nach einigen Tagen Standzeit leer?', ['Weil der Bus immer zu schnell ist', 'Wegen des Reifendrucks', 'Ein Steuergerät hält den Bus wach – Ruhestrom zu hoch'], 2, 'Ruhestrom mit der Stromzange nach Busruhe messen.'),
        ('Bei einem CAN nach ISO 11898-3 liegt CAN-L an Masse. Was passiert?', ['Der ganze Bus fällt sofort aus', 'Der Bus arbeitet im Eindrahtbetrieb über CAN-H weiter', 'Nichts, das ist normal'], 1, 'ISO 11898-3 ist fehlertolerant – Fehler wird gespeichert und muss trotzdem behoben werden.'),
        ('Was weckt den Bus während der Ruhestrommessung wieder auf?', ['Tür öffnen oder Diagnosetester anstecken', 'Die Stromzange', 'Gar nichts'], 0, 'Darum während der Messung nichts am Fahrzeug tun.'),
    ]),
    merke(T, ['Fehlerspeicher, Versorgung, Oszilloskop, 60 Ω', 'Fehlerbilder am Oszi erkennen',
              'Steuergeräte abstecken grenzt den Fehler ein', 'Ruhestrom: Stromzange, Busruhe abwarten']),
]
diag_js = '''<script>
(function () {
''' + OSZI_JS + '''
  const F = {
    ok: [k => bit(k) ? 2.5 : 3.5, k => bit(k) ? 2.5 : 1.5, 5, '<b class="grn">In Ordnung:</b> CAN-High und CAN-Low spiegelbildlich zwischen ca. 2,5 V und 3,5 V bzw. 1,5 V.'],
    hl: [k => 2.5, k => 2.45, 5, '<b class="red">CAN-High an CAN-Low:</b> Beide Leitungen liegen dauernd bei ca. 2,5 V – es ist kein Unterschied mehr möglich. Der Bus fällt aus.'],
    hm: [k => 0.05, k => bit(k) ? 0.3 : 0.1, 5, '<b class="red">CAN-High an Masse:</b> CAN-High liegt bei 0 V, das Signal bricht zusammen – beim CAN nach ISO 11898-2 keine Kommunikation.'],
    lp: [k => 12, k => 12, 14, '<b class="red">CAN-Low an Plus:</b> Die Leitung liegt auf Batteriespannung – keine Kommunikation. Leitung freilegen und Scheuerstelle suchen.'],
    rf: [k => (bit(k) ? 2.5 : 3.5) + 0.5 * Math.sin(k * 260) * Math.exp(-((k * 13) % 1) * 6), k => (bit(k) ? 2.5 : 1.5) - 0.5 * Math.sin(k * 260) * Math.exp(-((k * 13) % 1) * 6), 5, '<b class="ora">Abschlusswiderstand fehlt:</b> An den Flanken schwingt das Signal (Reflexionen). Widerstandsmessung zeigt ca. 120 Ω statt 60 Ω.']
  };
  const fb = document.querySelectorAll('#s-fb [data-f]');
  function f(m) {
    const [h, l, vmax, t] = F[m];
    Oszi('fb', { vmax: vmax, step: vmax > 5 ? 2 : 1, h: 200 })(h, l);
    fb.forEach(b => b.classList.toggle('on', b.dataset.f === m));
    document.getElementById('fb-t').innerHTML = t;
  }
  fb.forEach(b => b.onclick = () => f(b.dataset.f)); f('ok');

  // 7 Fehlerfälle
  const H2 = k => bit(k) ? 2.5 : 3.5, L2 = k => bit(k) ? 2.5 : 1.5, H3 = k => bit(k) ? 0 : 3.6, L3 = k => bit(k) ? 5 : 1.4;
  const AUS = ' <b class="red">Kommunikation fällt aus.</b>', EIN = ' <b class="grn">Der Bus arbeitet im Eindrahtbetrieb weiter</b> – Fehler wird gespeichert.';
  const G = {
    2: {
      1: [k => 2.5, L2, 5, 'CAN-H ist unterbrochen. Hinter der Unterbrechung bleibt CAN-H bei ca. 2,5 V stehen, nur CAN-L zeigt noch Signal. Die abgetrennten Steuergeräte sind nicht mehr erreichbar, es gibt viele Fehlereinträge.'],
      2: [H2, k => 2.5, 5, 'CAN-L ist unterbrochen. Hinter der Unterbrechung bleibt CAN-L bei ca. 2,5 V stehen, nur CAN-H zeigt noch Signal. Die abgetrennten Steuergeräte sind nicht mehr erreichbar.'],
      3: [k => 12, k => 11.5, 14, 'CAN-H liegt an Batteriespannung. Über die Abschlusswiderstände wird auch CAN-L hochgezogen.' + AUS],
      4: [k => bit(k) ? 0.1 : 1.2, k => 0.05, 5, 'CAN-L liegt an Masse (0 V). CAN-H wird mit heruntergezogen, es bleiben nur kleine Signalreste. Die Kommunikation ist stark gestört, meist fällt sie aus.'],
      5: [k => 0.05, k => bit(k) ? 0.1 : 0.3, 5, 'CAN-H liegt an Masse (0 V). Das Signal bricht zusammen.' + AUS],
      6: [k => 11.6, k => 12, 14, 'CAN-L liegt an Batteriespannung. Beide Leitungen werden hochgezogen.' + AUS],
      7: [k => 2.56, k => 2.44, 5, 'CAN-H und CAN-L haben Verbindung. Beide liegen bei ca. 2,5 V, ein Unterschied ist nicht mehr möglich.' + AUS]
    },
    3: {
      1: [k => 0, L3, 5, 'CAN-H ist unterbrochen. Hinter der Unterbrechung bleibt CAN-H bei 0 V, die Botschaften laufen nur noch über CAN-L.' + EIN],
      2: [H3, k => 5, 5, 'CAN-L ist unterbrochen. Hinter der Unterbrechung bleibt CAN-L bei ca. 5 V, die Botschaften laufen nur noch über CAN-H.' + EIN],
      3: [k => 12, L3, 14, 'CAN-H liegt an Batteriespannung. Die Steuergeräte schalten CAN-H ab und senden nur über CAN-L.' + EIN],
      4: [H3, k => 0, 5, 'CAN-L liegt an Masse (0 V). Die Steuergeräte senden nur noch über CAN-H.' + EIN],
      5: [k => 0, L3, 5, 'CAN-H liegt an Masse (0 V). Die Steuergeräte senden nur noch über CAN-L. Achtung: Das sieht aus wie Fall 1.' + EIN],
      6: [H3, k => 12, 14, 'CAN-L liegt an Batteriespannung. Die Steuergeräte senden nur noch über CAN-H.' + EIN],
      7: [k => L3(k) + 0.06, k => L3(k) - 0.06, 5, 'CAN-H und CAN-L haben Verbindung. Beide Leitungen zeigen das gleiche Bild. Die Steuergeräte schalten eine Leitung ab.' + EIN]
    }
  };
  let f7n = 2, f7i = 1;
  const f7b = document.querySelectorAll('#s-f7 [data-n]'), f7c = document.querySelectorAll('#s-f7 [data-i]');
  function f7() {
    const [h, l, vmax, t] = G[f7n][f7i];
    Oszi('f7', { vmax: vmax, step: vmax > 5 ? 2 : 1, h: 200 })(h, l);
    f7b.forEach(b => b.classList.toggle('on', +b.dataset.n === f7n));
    f7c.forEach(b => b.classList.toggle('on', +b.dataset.i === f7i));
    document.getElementById('f7-t').innerHTML = '<b>Fall ' + f7i + ' bei ISO 11898-' + f7n + ':</b> ' + t;
  }
  f7b.forEach(b => b.onclick = () => { f7n = +b.dataset.n; f7(); });
  f7c.forEach(b => b.onclick = () => { f7i = +b.dataset.i; f7(); }); f7();

  const rs = document.getElementById('rs'); let wach = 0;
  const zb = document.querySelectorAll('#s-rs [data-z]');
  function r() {
    const t = +rs.value;
    let I;
    if (t < 1) I = 3.0; else if (t < 15) I = 0.6 - 0.5 * (t - 1) / 14; else I = 0.03;
    if (wach && t >= 15) I = 0.45;
    document.getElementById('rs-n').textContent = t + ' min';
    document.getElementById('rs-v').textContent = I >= 1 ? I.toFixed(1).replace('.', ',') + ' A' : Math.round(I * 1000) + ' mA';
    const ruhe = t >= 15 && !wach;
    const s = document.getElementById('rs-s'); s.textContent = ruhe ? 'Busruhe – Steuergeräte schlafen' : (t >= 15 ? 'keine Busruhe!' : 'Steuergeräte schlafen ein …'); s.className = ruhe ? 'grn' : (t >= 15 ? 'red' : 'muted');
    document.getElementById('rs-t').innerHTML = t < 15 ? 'Nach dem Abschließen laufen die Steuergeräte noch nach und schlafen nacheinander ein. Der Strom sinkt.'
      : (wach ? '<b class="red">Zu hoch:</b> Ein Steuergerät hält den Bus wach. Die Batterie ist nach wenigen Tagen leer. Fehlerspeicher lesen, dann Sicherungen nacheinander ziehen: Fällt der Ruhestrom auf normal, steckt der Fehler in diesem Stromkreis.'
              : '<b class="grn">Busruhe:</b> Alle Steuergeräte schlafen. Der Ruhestrom ist sehr klein (Beispiel ca. 30 mA) – Grenzwert laut Hersteller.');
    zb.forEach(b => b.classList.toggle('on', +b.dataset.z === wach));
  }
  rs.addEventListener('input', r); zb.forEach(b => b.onclick = () => { wach = +b.dataset.z; r(); }); r();
})();
</script>'''

STYLE = '''  .symbol { font-size: 80px; }
  @media (max-width: 700px) { #s-f7 .f7c { display: grid !important; grid-template-columns: 1fr 1fr; gap: 6px; } #s-f7 .f7c .btn { font-size: 13px; padding: 8px 6px; margin: 0; width: auto; } }'''

if __name__ == '__main__':
    seite('bus-grundlagen.html', 'Grundlagen der Vernetzung – Datenbus', 't-bus', THEMA, grund, STYLE, grund_js)
    seite('bus-can.html', 'CAN-Bus – Datenbus', 't-bus', THEMA, can, STYLE, can_js)
    seite('bus-systeme.html', 'LIN, FlexRay, MOST, Ethernet – Datenbus', 't-bus', THEMA, busse, STYLE, busse_js)
    seite('bus-diagnose.html', 'Diagnose am Datenbus – Datenbus', 't-bus', THEMA, diag, STYLE, diag_js)
    print('ok')
