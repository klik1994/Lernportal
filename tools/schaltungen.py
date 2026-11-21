"""Grundlagen Elektrik: Reihenschaltung, Parallelschaltung, Gemischte Schaltung.
Aufruf: cd tools && python3 schaltungen.py"""
from praesentation_bauen import *

K = 'GRUNDLAGEN ELEKTRIK · KFZ-MECHATRONIK'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'
LINE = '#ecf1f8'


def batt(x=60, y1=110, y2=190):
    """Batterie senkrecht, Pluspol oben."""
    m = (y1 + y2) / 2
    return f'''<g class="dev"><line x1="{x - 26}" y1="{m - 8}" x2="{x + 26}" y2="{m - 8}" stroke="#f05e4e" stroke-width="6"/>
    <line x1="{x - 14}" y1="{m + 8}" x2="{x + 14}" y2="{m + 8}" stroke="#94a4ba" stroke-width="8"/></g>
    <line x1="{x}" y1="{y1}" x2="{x}" y2="{m - 8}" stroke="{LINE}" stroke-width="4"/>
    <line x1="{x}" y1="{m + 8}" x2="{x}" y2="{y2}" stroke="{LINE}" stroke-width="4"/>
    <text x="{x - 34}" y="{m - 4}" text-anchor="end" font-size="22" font-weight="900" fill="#f05e4e">+</text>
    <text x="{x - 34}" y="{m + 22}" text-anchor="end" font-size="22" font-weight="900" fill="#94a4ba">−</text>
    <text x="{x + 34}" y="{m + 6}" font-size="16" font-weight="800" fill="#94a4ba">12 V</text>'''


def lampe(cx, cy, id_, lab=''):
    return f'''<circle id="{id_}-glow" cx="{cx}" cy="{cy}" r="34" fill="#f7b612" style="opacity:0;transition:opacity .3s"/>
    <circle cx="{cx}" cy="{cy}" r="20" fill="#18283f" stroke="{LINE}" stroke-width="4"/>
    <path id="{id_}-x" d="M{cx - 14} {cy - 14} L{cx + 14} {cy + 14} M{cx + 14} {cy - 14} L{cx - 14} {cy + 14}" stroke="{LINE}" stroke-width="3"/>
    <text x="{cx}" y="{cy - 30 if lab else cy}" text-anchor="middle" font-size="15" font-weight="800" fill="#94a4ba">{lab}</text>'''


def wid(cx, cy, lab, vertical=False, id_=None):
    w, h = (24, 60) if vertical else (60, 24)
    i = f' id="{id_}"' if id_ else ''
    tx, ty, anc = (cx + 22, cy + 5, 'start') if vertical else (cx, cy - 20, 'middle')
    return f'''<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="3" fill="#18283f" stroke="{LINE}" stroke-width="4"/>
    <text{i} x="{tx}" y="{ty}" text-anchor="{anc}" font-size="16" font-weight="800" fill="#94a4ba">{lab}</text>'''


def flow_js(var, svg, path, color='#ffd34d', spacing=34, speed=80):
    return f"const {var} = Flow(document.getElementById('{svg}'), document.getElementById('{path}'), {{ spacing: {spacing}, speed: {speed}, r: 6, color: '{color}' }});"


def zahl(x, d=1):
    return ("{:." + str(d) + "f}").format(x).replace('.', ',')


LEG = '''<text x="40" y="294" font-size="13" font-weight="800" fill="#f05e4e">rot = Plus</text><text x="140" y="294" font-size="13" font-weight="800" fill="#5b8cff">blau = Minus</text><text x="250" y="294" font-size="13" font-weight="800" fill="#94a4ba">gelbe Punkte = Strom (technisch: + → −)</text>'''
SCHALT_JS = '<script src="assets/schaltung.js"></script>'

# ================================================================ REIHENSCHALTUNG
T = 'REIHENSCHALTUNG'
THEMA_R = 'Reihenschaltung'

R_KREIS = f'''<svg viewBox="0 0 560 300" width="540" height="290" style="display:block;margin:0 auto" id="r1-svg">
  {batt()}
  <path d="M60 110 V50 H200" fill="none" stroke="#f05e4e" stroke-width="5"/>
  <path id="r1-mid" d="M240 50 H360" fill="none" stroke="#ff8f3f" stroke-width="5" style="transition:stroke .3s"/>
  <path d="M400 50 H500 V250 H60 V190" fill="none" stroke="#5b8cff" stroke-width="5"/>
  <path id="r1-p" d="M60 110 V50 H500 V250 H60 V190" fill="none" stroke="none"/>
  {lampe(220, 50, 'r1l1', 'Lampe 1')}
  <g id="r1-l2">{lampe(380, 50, 'r1l2', 'Lampe 2')}</g>
  <text x="120" y="76" text-anchor="middle" font-size="15" font-weight="900" fill="#f05e4e">Plus 12 V</text>
  <text id="r1-mt" x="300" y="76" text-anchor="middle" font-size="15" font-weight="900" fill="#ff8f3f">ca. 6 V</text>
  <text x="280" y="238" text-anchor="middle" font-size="15" font-weight="900" fill="#5b8cff">Minus 0 V</text>
  {LEG}
</svg>'''

R_RECH = f'''<svg viewBox="0 0 560 300" width="540" height="290" style="display:block;margin:0 auto" id="r2-svg">
  {batt()}
  <path d="M60 110 V50 H190" fill="none" stroke="#f05e4e" stroke-width="5"/>
  <path d="M250 50 H350" fill="none" stroke="#ff8f3f" stroke-width="5"/>
  <path d="M410 50 H500 V250 H60 V190" fill="none" stroke="#5b8cff" stroke-width="5"/>
  <path id="r2-p" d="M60 110 V50 H500 V250 H60 V190" fill="none" stroke="none"/>
  {wid(220, 50, 'R1', id_='r2-l1')}
  {wid(380, 50, 'R2', id_='r2-l2')}
  <text id="r2-u1" x="220" y="100" text-anchor="middle" font-size="17" font-weight="900" fill="#1fc8b3">U1</text>
  <text id="r2-u2" x="380" y="100" text-anchor="middle" font-size="17" font-weight="900" fill="#1fc8b3">U2</text>
  <text id="r2-mp" x="300" y="130" text-anchor="middle" font-size="14" font-weight="900" fill="#ff8f3f"></text>
  <text id="r2-i" x="280" y="235" text-anchor="middle" font-size="17" font-weight="900" fill="#28aaf5">I</text>
  {LEG}
</svg>'''

reihe = [
    titel_folie(K, 'R+R', 'Reihenschaltung', 'Alle Bauteile hintereinander – nur ein Stromweg', 'font-size:64px'),
    lernziele(T, ['Woran du eine Reihenschaltung erkennst', 'Was für Strom, Spannung und Widerstand gilt',
                  'Wie du eine Reihenschaltung berechnest', 'Wo dir die Reihenschaltung im Kfz begegnet']),
    folie(T, 'Der Vergleich mit Wasser', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big">Ein Wasserschlauch mit <span class="c">zwei engen Stellen hintereinander</span>.</div></div>
      <div class="card step"><div class="big">Durch beide Engstellen fließt <span class="c">dieselbe Menge</span> Wasser – es gibt nur einen Weg.</div></div>
      <div class="card step"><div class="big">Jede Engstelle bremst. Zusammen bremsen sie <span class="c">mehr</span> als eine allein.</div></div>
      <div class="card step"><div class="big">Ist der Schlauch an einer Stelle zu, fließt <span class="c">überall nichts</span> mehr.</div></div>
    </div>'''),
    folie(T, 'Nur ein Stromweg – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" id="r1-ein">Beide Lampen drin</button><button class="btn ghost" id="r1-aus">Lampe 2 herausdrehen</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {R_KREIS}
      <div class="card" id="r1-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>''', sid='s-r1', body_cls='body noclick'),
    folie(T, 'Die drei Regeln', '''    <div class="values">
      <div class="val step from-left"><b>I = gleich</b><span>Der Strom ist an jeder Stelle gleich groß – es gibt nur einen Weg</span></div>
      <div class="val step from-left"><b>R = R1 + R2 + …</b><span>Die Widerstände werden addiert – der Gesamtwiderstand wird größer</span></div>
      <div class="val step from-left"><b>U = U1 + U2 + …</b><span>Die Spannung teilt sich auf – am größten Widerstand liegt die größte Teilspannung</span></div>
    </div>'''),
    folie(T, 'Rechnen – zum Ausprobieren', f'''    <div class="ctrl"><span style="width:200px">R1: <span class="c" id="r2-v1">4 Ω</span></span><input type="range" id="r2-s1" min="1" max="10" step="1" value="4"></div>
    <div class="ctrl" style="margin-top:6px"><span style="width:200px">R2: <span class="c" id="r2-v2">2 Ω</span></span><input type="range" id="r2-s2" min="1" max="10" step="1" value="2"></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr;margin-top:8px">
      {R_RECH}
      <div class="card" id="r2-t" style="font-size:17px;font-weight:700;line-height:1.7"></div>
    </div>''', sid='s-r2', body_cls='body noclick'),
    folie(T, 'Rechenbeispiel', '''    <div class="card step" style="font-size:19px;font-weight:700;margin-bottom:10px">Gegeben: U = 12 V, R1 = 4 Ω, R2 = 2 Ω (in Reihe)</div>
    <ol class="steps-list">
      <li class="step">Gesamtwiderstand<small>R = R1 + R2 = 4 Ω + 2 Ω = <b>6 Ω</b></small></li>
      <li class="step">Strom (überall gleich)<small>I = U : R = 12 V : 6 Ω = <b>2 A</b></small></li>
      <li class="step">Teilspannung an R1<small>U1 = R1 · I = 4 Ω · 2 A = <b>8 V</b></small></li>
      <li class="step">Teilspannung an R2<small>U2 = R2 · I = 2 Ω · 2 A = <b>4 V</b> – Probe: 8 V + 4 V = 12 V ✓</small></li>
    </ol>'''),
    folie(T, 'Reihenschaltung im Kfz', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Korrodierte Masse</b>Ein Übergangswiderstand liegt in Reihe zur Lampe. Er „nimmt“ sich einen Teil der Spannung – die Lampe leuchtet schwächer.</div>
      <div class="tip step"><b>Spannungsfall messen</b>Im Betrieb über Leitung oder Masseverbindung messen. Richtwert: nur wenige Zehntel Volt – genaue Grenzen laut Hersteller.</div>
      <div class="tip step"><b>Vorwiderstand</b>Früher z. B. beim Innenraumgebläse: Ein Widerstand in Reihe senkt die Spannung am Motor – er dreht langsamer.</div>
      <div class="tip step"><b>Schalter und Sicherung</b>liegen immer in Reihe zum Verbraucher – nur so können sie den Stromkreis unterbrechen.</div>
    </div>'''),
    folie(T, 'Messen in der Reihenschaltung', '''    <ol class="steps-list">
      <li class="step">Strom messen: Kreis auftrennen, Messgerät <span class="c">in Reihe</span><small>egal an welcher Stelle – der Strom ist überall gleich</small></li>
      <li class="step">Teilspannung messen: <span class="c">parallel</span> zum Bauteil<small>die Messspitzen an beide Anschlüsse des Bauteils – im Betrieb</small></li>
      <li class="step">Probe: Alle Teilspannungen zusammen = Batteriespannung<small>fehlt etwas, steckt ein unbekannter Widerstand im Kreis</small></li>
    </ol>
    <div class="tip step" style="margin-top:6px"><b>„OL“ am manuellen Multimeter?</b>Den Messbereich schrittweise bis zum höchsten hochstellen – erst dann gilt: Unterbrechung.</div>'''),
    video(T, 'reihe'),
    kurztest(T, [
        ('Wie groß ist der Strom in einer Reihenschaltung?', ['An jeder Stelle gleich', 'Am ersten Bauteil am größten', 'Er teilt sich auf'], 0, 'Es gibt nur einen Stromweg.'),
        ('R1 = 3 Ω und R2 = 9 Ω sind in Reihe. Wie groß ist der Gesamtwiderstand?', ['3 Ω', '12 Ω', '27 Ω'], 1, 'In Reihe werden die Widerstände addiert: 3 Ω + 9 Ω = 12 Ω.'),
        ('An welchem Widerstand liegt die größte Teilspannung?', ['Am kleinsten', 'An allen gleich', 'Am größten'], 2, 'U = R · I – bei gleichem Strom hat der größte Widerstand die größte Spannung.'),
        ('Eine Lampe in einer Reihenschaltung brennt durch. Was passiert?', ['Alle anderen gehen auch aus', 'Die anderen leuchten heller', 'Nichts'], 0, 'Der einzige Stromweg ist unterbrochen.'),
    ]),
    merke(T, ['Nur ein Stromweg', 'Strom überall gleich', 'R = R1 + R2 + …|Widerstände addieren',
              'U = U1 + U2 + …|Spannung teilt sich auf']),
]
reihe_js = SCHALT_JS + '''
<script>
(function () {
  ''' + flow_js('f1', 'r1-svg', 'r1-p') + '''
  const ein = document.getElementById('r1-ein'), aus = document.getElementById('r1-aus');
  function set(an) {
    f1.on(an);
    ['r1l1', 'r1l2'].forEach(l => document.getElementById(l + '-glow').style.opacity = an ? 0.5 : 0);
    document.getElementById('r1-l2').style.opacity = an ? 1 : 0.15;
    const m = document.getElementById('r1-mid'), mt = document.getElementById('r1-mt');
    m.setAttribute('stroke', an ? '#ff8f3f' : '#f05e4e'); mt.setAttribute('fill', an ? '#ff8f3f' : '#f05e4e'); mt.textContent = an ? 'ca. 6 V' : 'Plus 12 V';
    ein.classList.toggle('on', an); aus.classList.toggle('on', !an);
    document.getElementById('r1-t').innerHTML = an
      ? '<b>Beide Lampen leuchten.</b> Der Strom fließt vom Pluspol durch Lampe 1, dann durch Lampe 2 und zurück zum Minuspol – es gibt <span class="c">nur einen Weg</span>.<br><br>An jeder Lampe fällt ein Teil der Spannung ab: vor Lampe 1 <span class="red">Plus 12 V</span>, zwischen den Lampen <span class="ora">ca. 6 V</span>, nach Lampe 2 <span class="roy">Minus 0 V</span>.'
      : '<b class="red">Alles aus!</b> Lampe 2 fehlt – der einzige Stromweg ist unterbrochen. Darum geht auch Lampe 1 aus.<br><br>Ohne Strom „verbraucht“ Lampe 1 keine Spannung: <span class="red">Plus</span> reicht jetzt bis an den linken Kontakt von Lampe 2, <span class="roy">Minus</span> liegt am rechten. Am leeren Lampensockel misst du die vollen 12 V.';
  }
  ein.onclick = () => set(true); aus.onclick = () => set(false);
  document.getElementById('s-r1').addEventListener('slideshow', () => set(true));
  set(true);

  ''' + flow_js('f2', 'r2-svg', 'r2-p') + '''
  const s1 = document.getElementById('r2-s1'), s2 = document.getElementById('r2-s2');
  const z = (x, d) => x.toFixed(d).replace('.', ',');
  function rech() {
    const R1 = +s1.value, R2 = +s2.value, R = R1 + R2, I = 12 / R, U1 = R1 * I, U2 = R2 * I;
    document.getElementById('r2-v1').textContent = R1 + ' Ω'; document.getElementById('r2-v2').textContent = R2 + ' Ω';
    document.getElementById('r2-l1').textContent = 'R1 = ' + R1 + ' Ω'; document.getElementById('r2-l2').textContent = 'R2 = ' + R2 + ' Ω';
    document.getElementById('r2-u1').textContent = 'U1 = ' + z(U1, 1) + ' V'; document.getElementById('r2-u2').textContent = 'U2 = ' + z(U2, 1) + ' V';
    document.getElementById('r2-i').textContent = 'I = ' + z(I, 2) + ' A';
    document.getElementById('r2-mp').textContent = 'hier noch ' + z(U2, 1) + ' V gegen Minus';
    f2.speed = 30 + I * 25;
    document.getElementById('r2-t').innerHTML = 'R = ' + R1 + ' Ω + ' + R2 + ' Ω = <span class="c">' + R + ' Ω</span><br>I = 12 V : ' + R + ' Ω = <span class="c">' + z(I, 2) + ' A</span><br>U1 = ' + z(U1, 1) + ' V, U2 = ' + z(U2, 1) + ' V<br><span class="muted">Probe: ' + z(U1, 1) + ' V + ' + z(U2, 1) + ' V = 12 V</span>';
  }
  s1.addEventListener('input', rech); s2.addEventListener('input', rech); rech();
})();
</script>'''

# ================================================================ PARALLELSCHALTUNG
T = 'PARALLELSCHALTUNG'
THEMA_P = 'Parallelschaltung'
XS = [200, 320, 440]
P_KREIS = f'''<svg viewBox="0 0 560 300" width="540" height="290" style="display:block;margin:0 auto" id="p1-svg">
  {batt()}
  <path d="M60 110 V50 H440" fill="none" stroke="#f05e4e" stroke-width="5"/>
  <path d="M60 190 V250 H440" fill="none" stroke="#5b8cff" stroke-width="5"/>
  ''' + ''.join(f'''<path d="M{x} 50 V130" fill="none" stroke="#f05e4e" stroke-width="5"/><path d="M{x} 170 V250" fill="none" stroke="#5b8cff" stroke-width="5"/>
  <path id="p1-p{i}" d="M60 110 V50 H{x} V250 H60 V190" fill="none" stroke="none"/>
  {lampe(x, 150, f"p1l{i}", "")}
  <circle cx="{x}" cy="50" r="6" fill="#f05e4e"/><circle cx="{x}" cy="250" r="6" fill="#5b8cff"/>''' for i, x in enumerate(XS)) + '''
  <text x="250" y="38" text-anchor="middle" font-size="15" font-weight="900" fill="#f05e4e">Plus 12 V – an allen Lampen oben</text>
  <text x="250" y="274" text-anchor="middle" font-size="15" font-weight="900" fill="#5b8cff">Minus 0 V – an allen Lampen unten</text>
  ''' + LEG + '''
</svg>'''

W_KREIS = f'''<svg viewBox="0 0 560 300" width="540" height="290" style="display:block;margin:0 auto" id="w-svg">
  {batt()}
  <path d="M60 110 V50 H440" fill="none" stroke="#f05e4e" stroke-width="5"/>
  <path d="M60 190 V250 H440" fill="none" stroke="#5b8cff" stroke-width="5"/>
  ''' + ''.join(f'''<g id="w-z{i}" style="transition:opacity .3s"><path d="M{x} 50 V115" fill="none" stroke="#f05e4e" stroke-width="5"/><path d="M{x} 185 V250" fill="none" stroke="#5b8cff" stroke-width="5"/>
  <rect x="{x - w / 2}" y="115" width="{w}" height="70" rx="4" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/>
  <text x="{x}" y="210" text-anchor="middle" font-size="15" font-weight="900" fill="#94a4ba">{lab}</text>
  <path id="w-p{i}" d="M60 110 V50 H{x} V250 H60 V190" fill="none" stroke="none"/></g>''' for i, (x, w, lab) in enumerate([(200, 34, '6 Ω'), (320, 16, '12 Ω'), (440, 16, '12 Ω')])) + '''
  <text x="250" y="285" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">breiter Kasten = kleiner Widerstand = mehr Strom</text>
</svg>'''

VERBR = [('Abblendlicht links', 4.6), ('Abblendlicht rechts', 4.6), ('Heckscheibenheizung', 10.0), ('Gebläse', 8.0)]

parallel = [
    titel_folie(K, 'R∥R', 'Parallelschaltung', 'Jeder Verbraucher hat seinen eigenen Zweig', 'font-size:64px'),
    lernziele(T, ['Woran du eine Parallelschaltung erkennst', 'Was für Spannung, Strom und Widerstand gilt',
                  'Wie du eine Parallelschaltung berechnest', 'Warum im Kfz fast alles parallel geschaltet ist']),
    folie(T, 'Der Vergleich mit Wasser', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big">Eine Wasserleitung <span class="c">verzweigt</span> sich in mehrere Rohre nebeneinander.</div></div>
      <div class="card step"><div class="big">An jedem Rohr liegt <span class="c">derselbe Druck</span> an.</div></div>
      <div class="card step"><div class="big">Jedes offene Rohr lässt Wasser durch – <span class="c">zusammen fließt mehr</span>.</div></div>
      <div class="card step"><div class="big">Wird ein Rohr zugedreht, fließt durch die anderen <span class="c">trotzdem</span> Wasser.</div></div>
    </div>'''),
    folie(T, 'Eigene Zweige – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-z="0">Lampe 1</button><button class="btn ghost on" data-z="1">Lampe 2</button><button class="btn ghost on" data-z="2">Lampe 3</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {P_KREIS}
      <div>
        <div class="card"><div class="muted" style="font-size:15px;font-weight:800">GESAMTSTROM</div><div class="lcd2" id="p1-i" style="font-size:32px;margin-top:6px">—</div></div>
        <div class="card" id="p1-t" style="margin-top:12px;font-size:17px;font-weight:600;line-height:1.5"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Tippe die Lampen an und aus. Beispiel: jede Lampe 2 A.</p>''', sid='s-p1', body_cls='body noclick'),
    folie(T, 'Die drei Regeln', '''    <div class="values">
      <div class="val step from-left"><b>U = gleich</b><span>An jedem Zweig liegt dieselbe Spannung – im Kfz die Bordnetzspannung</span></div>
      <div class="val step from-left"><b>I = I1 + I2 + …</b><span>Der Gesamtstrom ist die Summe aller Zweigströme</span></div>
      <div class="val step from-left"><b>R &lt; kleinster</b><span>Der Gesamtwiderstand ist kleiner als der kleinste Einzelwiderstand</span></div>
    </div>
    <div class="note step">Zwei gleiche Widerstände parallel: R = halber Einzelwiderstand. Allgemein: 1/R = 1/R1 + 1/R2 + …</div>'''),
    folie(T, 'Warum wird R kleiner? – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost" data-w="1">+ Zweig 2 (12 Ω)</button><button class="btn ghost" data-w="2">+ Zweig 3 (12 Ω)</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {W_KREIS}
      <div class="card" id="w-t" style="font-size:17px;font-weight:700;line-height:1.6"></div>
    </div>''', sid='s-w', body_cls='body noclick'),
    folie(T, 'Warum wird der Widerstand kleiner?', '''    <ol class="steps-list">
      <li class="step">Jeder neue Zweig ist ein <span class="c">zusätzlicher Weg</span><small>der alte Weg bleibt ja – er bekommt weiter seine 12 V und seinen Strom</small></li>
      <li class="step">Auch ein schmaler Weg lässt <span class="c">etwas Strom</span> durch<small>selbst ein großer Widerstand bringt zusätzlichen Strom dazu</small></li>
      <li class="step">Gleiche Spannung, <span class="c">mehr Strom</span><small>aus der Batterie fließt insgesamt mehr</small></li>
      <li class="step">Mehr Strom bei gleicher Spannung = <span class="c">kleinerer Widerstand</span><small>R = U : I – wenn I größer wird, wird R kleiner</small></li>
    </ol>
    <div class="tip step" style="margin-top:6px"><b>Wie Kassen im Supermarkt</b>Macht eine zweite Kasse auf – auch eine langsame –, kommen insgesamt mehr Kunden durch. Die Schlange wird schneller kleiner als mit nur einer Kasse.</div>'''),
    folie(T, 'Verbraucher zuschalten – zum Ausprobieren', '''    <div class="choice" style="margin-bottom:12px;flex-wrap:wrap" id="p2-btn">''' + ''.join(f'<button class="btn ghost" data-v="{i}">{n}</button>' for i, (n, a) in enumerate(VERBR)) + '''</div>
    <div class="grid2" style="align-items:center">
      <div class="card"><div class="muted" style="font-size:15px;font-weight:800">GESAMTSTROM AUS DER BATTERIE</div><div class="lcd2" id="p2-i" style="font-size:32px;margin-top:6px">0 A</div>
        <div style="height:18px;background:var(--card2);border-radius:8px;margin-top:12px;overflow:hidden"><div id="p2-bar" style="height:100%;width:0;background:var(--c);transition:width .25s"></div></div></div>
      <div class="card" id="p2-t" style="font-size:17px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Beispielwerte bei 12 V.</p>''', sid='s-p2', body_cls='body noclick'),
    folie(T, 'Rechenbeispiel', '''    <div class="card step" style="font-size:19px;font-weight:700;margin-bottom:10px">Gegeben: U = 12 V, R1 = 6 Ω, R2 = 3 Ω (parallel)</div>
    <ol class="steps-list">
      <li class="step">Spannung an jedem Zweig<small>U1 = U2 = <b>12 V</b></small></li>
      <li class="step">Zweigströme<small>I1 = 12 V : 6 Ω = <b>2 A</b> – I2 = 12 V : 3 Ω = <b>4 A</b></small></li>
      <li class="step">Gesamtstrom<small>I = I1 + I2 = 2 A + 4 A = <b>6 A</b></small></li>
      <li class="step">Gesamtwiderstand<small>R = U : I = 12 V : 6 A = <b>2 Ω</b> – kleiner als der kleinste (3 Ω) ✓</small></li>
    </ol>'''),
    folie(T, 'Parallelschaltung im Kfz', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Fast alle Verbraucher</b>sind parallel geschaltet: Jeder bekommt die volle Bordnetzspannung und arbeitet unabhängig von den anderen.</div>
      <div class="tip step"><b>Mehr Verbraucher = mehr Strom</b>Leitungen und Sicherungen müssen den Gesamtstrom aushalten.</div>
      <div class="warn step"><b>Kurzschluss</b>Ein Zweig mit fast 0 Ω lässt einen sehr großen Strom fließen – die Sicherung löst aus.</div>
      <div class="tip step"><b>Widerstand messen</b>Parallel liegende Bauteile verfälschen das Ergebnis – das Bauteil zum Messen abklemmen.</div>
    </div>'''),
    folie(T, 'Messen in der Parallelschaltung', '''    <ol class="steps-list">
      <li class="step">Spannung: an jedem Zweig gleich<small>Messgerät parallel zum Verbraucher – im Betrieb</small></li>
      <li class="step">Gesamtstrom: <span class="c">vor</span> der ersten Abzweigung<small>Kreis dort auftrennen oder Stromzange um die Zuleitung</small></li>
      <li class="step">Zweigstrom: <span class="c">im</span> jeweiligen Zweig<small>nur der Strom dieses Verbrauchers</small></li>
    </ol>
    <div class="tip step" style="margin-top:6px"><b>Stromzange</b>Bei großen Strömen bequemer und sicherer – der Stromkreis muss nicht aufgetrennt werden.</div>'''),
    video(T, 'parallel'),
    kurztest(T, [
        ('Welche Spannung liegt in einer Parallelschaltung an jedem Zweig?', ['Dieselbe Spannung', 'Sie teilt sich auf', 'Am ersten Zweig die höchste'], 0, 'Alle Zweige hängen an denselben zwei Punkten.'),
        ('Zweigströme 2 A, 3 A und 5 A. Wie groß ist der Gesamtstrom?', ['5 A', '10 A', '30 A'], 1, 'Die Zweigströme werden addiert.'),
        ('Zwei Widerstände mit je 8 Ω sind parallel. Wie groß ist der Gesamtwiderstand?', ['16 Ω', '8 Ω', '4 Ω'], 2, 'Zwei gleiche parallel: halber Einzelwiderstand.'),
        ('Warum sind die Verbraucher im Kfz parallel geschaltet?', ['Jeder bekommt die volle Spannung und arbeitet unabhängig', 'Damit weniger Strom fließt', 'Damit eine Sicherung reicht'], 0, 'Fällt einer aus, arbeiten die anderen weiter.'),
    ]),
    merke(T, ['Jeder Verbraucher hat seinen eigenen Zweig', 'Spannung überall gleich',
              'I = I1 + I2 + …|Ströme addieren', 'R ist kleiner als der kleinste Einzelwiderstand']),
]
parallel_js = SCHALT_JS + '''
<script>
(function () {
  const svg = document.getElementById('p1-svg');
  const F = [0, 1, 2].map(i => Flow(svg, document.getElementById('p1-p' + i), { spacing: 30 + i * 5, speed: 80, r: 6, color: '#ffd34d' }));
  const an = [true, true, true];
  const bt = document.querySelectorAll('#s-p1 [data-z]');
  function upd() {
    an.forEach((a, i) => { F[i].on(a); document.getElementById('p1l' + i + '-glow').style.opacity = a ? 0.5 : 0; bt[i].classList.toggle('on', a); });
    const n = an.filter(Boolean).length;
    document.getElementById('p1-i').textContent = (n * 2) + ' A';
    document.getElementById('p1-t').innerHTML = n === 0 ? 'Alle Lampen aus – es fließt kein Strom.'
      : '<b>' + n + ' Lampe' + (n > 1 ? 'n' : '') + ' an.</b> Jede Lampe hat ihren <span class="c">eigenen Zweig</span> und bekommt die vollen 12 V. Schaltest du eine aus, leuchten die anderen weiter. Der Gesamtstrom ist die Summe: ' + n + ' × 2 A = ' + (n * 2) + ' A.';
  }
  bt.forEach((b, i) => b.onclick = () => { an[i] = !an[i]; upd(); });
  upd();

  const wsvg = document.getElementById('w-svg');
  const WF = [0, 1, 2].map(i => Flow(wsvg, document.getElementById('w-p' + i), { spacing: 32 + i * 4, speed: i ? 45 : 90, r: 6, color: '#ffd34d' }));
  const wa = [true, false, false], WR = [6, 12, 12];
  const wb = document.querySelectorAll('#s-w [data-w]');
  function w() {
    let I = 0; const teile = [];
    wa.forEach((a, i) => { WF[i].on(a); document.getElementById('w-z' + i).style.opacity = a ? 1 : 0.15; if (a) { I += 12 / WR[i]; teile.push('12 V : ' + WR[i] + ' Ω = ' + (12 / WR[i]) + ' A'); } });
    wb.forEach(b => b.classList.toggle('on', wa[+b.dataset.w]));
    const R = 12 / I, n = wa.filter(Boolean).length;
    document.getElementById('w-t').innerHTML = teile.map((t, i) => 'Zweig ' + (i + 1) + ': ' + t).join('<br>') +
      '<br>Gesamtstrom: <span class="c">' + String(I).replace('.', ',') + ' A</span><br>Gesamtwiderstand: 12 V : ' + String(I).replace('.', ',') + ' A = <span class="c">' + String(R).replace('.', ',') + ' Ω</span>' +
      (n > 1 ? '<br><span class="muted">Obwohl ein 12-Ω-Widerstand dazukam, ist der Gesamtwiderstand jetzt kleiner als 6 Ω – weil mehr Strom fließt.</span>' : '<br><span class="muted">Nur ein Zweig: Gesamtwiderstand = 6 Ω. Schalte einen Zweig dazu!</span>');
  }
  wb.forEach(b => b.onclick = () => { const k = +b.dataset.w; wa[k] = !wa[k]; w(); }); w();

  const V = ''' + str([a for n, a in VERBR]) + ''', N = ''' + str([n for n, a in VERBR]).replace("'", '"') + ''';
  const vb = document.querySelectorAll('#p2-btn [data-v]'); const sel = V.map(() => false);
  function v() {
    let s = 0; const teile = [];
    sel.forEach((x, i) => { vb[i].classList.toggle('on', x); if (x) { s += V[i]; teile.push(String(V[i]).replace('.', ',') + ' A'); } });
    document.getElementById('p2-i').textContent = s.toFixed(1).replace('.', ',') + ' A';
    document.getElementById('p2-bar').style.width = Math.min(100, s / 27.2 * 100) + '%';
    document.getElementById('p2-t').innerHTML = teile.length ? 'Gesamtstrom = ' + teile.join(' + ') + ' = <span class="c">' + s.toFixed(1).replace('.', ',') + ' A</span>.<br>Jeder Verbraucher bekommt 12 V – mit jedem weiteren steigt der Strom aus der Batterie.' : 'Tippe Verbraucher an, um sie einzuschalten.';
  }
  vb.forEach((b, i) => b.onclick = () => { sel[i] = !sel[i]; v(); }); v();
})();
</script>'''

# ================================================================ GEMISCHTE SCHALTUNG
T = 'GEMISCHTE SCHALTUNG'
THEMA_G = 'Gemischte Schaltung'
G_KREIS = f'''<svg viewBox="0 0 600 300" width="560" height="280" style="display:block;margin:0 auto" id="g1-svg">
  {batt()}
  <path d="M60 110 V50 H150" fill="none" stroke="#f05e4e" stroke-width="5"/>
  <path d="M210 50 H480 V120 M300 50 V120" fill="none" stroke="#ff8f3f" stroke-width="5"/>
  <path d="M300 180 V250 M480 180 V250 H60 V190" fill="none" stroke="#5b8cff" stroke-width="5"/>
  <circle cx="300" cy="50" r="6" fill="#ff8f3f"/><circle cx="300" cy="250" r="6" fill="#5b8cff"/>
  <path id="g1-pa" d="M60 110 V50 H300 V250 H60 V190" fill="none" stroke="none"/>
  <path id="g1-pb" d="M60 110 V50 H480 V250 H60 V190" fill="none" stroke="none"/>
  {wid(180, 50, 'R1', id_='g1-l1')}
  {wid(300, 150, 'R2', True, 'g1-l2')}
  {wid(480, 150, 'R3', True, 'g1-l3')}
  <text id="g1-u1" x="180" y="100" text-anchor="middle" font-size="16" font-weight="900" fill="#a07cf5"></text>
  <text id="g1-mp" x="390" y="38" text-anchor="middle" font-size="14" font-weight="900" fill="#ff8f3f"></text>
  <text id="g1-u23" x="390" y="232" text-anchor="middle" font-size="16" font-weight="900" fill="#a07cf5"></text>
  <text id="g1-i" x="180" y="232" text-anchor="middle" font-size="16" font-weight="900" fill="#28aaf5"></text>
  {LEG}
</svg>'''


def vereinfachung():
    a = f'''<g class="vs" data-s="0">
      <path d="M60 110 V50 H480 V250 H60 V190 M300 50 V250" fill="none" stroke="{LINE}" stroke-width="4"/>
      {wid(180, 50, 'R1 = 2 Ω')}{wid(300, 150, 'R2 = 6 Ω', True)}{wid(480, 150, 'R3 = 3 Ω', True)}</g>'''
    b = f'''<g class="vs" data-s="1">
      <path d="M60 110 V50 H400 V250 H60 V190" fill="none" stroke="{LINE}" stroke-width="4"/>
      {wid(180, 50, 'R1 = 2 Ω')}<rect x="388" y="120" width="24" height="60" rx="3" fill="#18283f" stroke="#a07cf5" stroke-width="4"/>
      <text x="422" y="146" font-size="16" font-weight="800" fill="#a07cf5">R23 = 2 Ω</text><text x="422" y="166" font-size="13" font-weight="700" fill="#94a4ba">ersetzt R2 ∥ R3</text></g>'''
    c = f'''<g class="vs" data-s="2">
      <path d="M60 110 V50 H300 V250 H60 V190" fill="none" stroke="{LINE}" stroke-width="4"/>
      <rect x="288" y="120" width="24" height="60" rx="3" fill="#18283f" stroke="#a07cf5" stroke-width="4"/>
      <text x="322" y="146" font-size="16" font-weight="800" fill="#a07cf5">R = 4 Ω</text><text x="322" y="166" font-size="13" font-weight="700" fill="#94a4ba">R1 + R23</text></g>'''
    return f'''<svg viewBox="0 0 600 300" width="560" height="280" style="display:block;margin:0 auto">{batt()}{a}{b}{c}</svg>'''


gemischt = [
    titel_folie(K, 'R+∥', 'Gemischte Schaltung', 'Reihe und parallel in einem Stromkreis', 'font-size:64px'),
    lernziele(T, ['Wie du eine gemischte Schaltung erkennst', 'Wie du sie Schritt für Schritt vereinfachst',
                  'Wie du Strom und Spannungen berechnest', 'Warum das bei der Fehlersuche im Kfz hilft']),
    folie(T, 'Was ist eine gemischte Schaltung?', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Teils in Reihe, teils parallel</div>
        <ul UL><li>manche Bauteile liegen hintereinander</li><li>andere liegen nebeneinander in eigenen Zweigen</li><li>für jeden Teil gelten seine eigenen Regeln</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">So gehst du vor</div>
        <ul UL><li>Gruppen suchen, die eindeutig parallel oder in Reihe sind</li><li>jede Gruppe durch einen Ersatzwiderstand ersetzen</li><li>so lange vereinfachen, bis nur noch ein Widerstand übrig ist</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Schritt für Schritt vereinfachen', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-g="0">1. Schaltung</button><button class="btn ghost" data-g="1">2. Parallelgruppe ersetzen</button><button class="btn ghost" data-g="2">3. Reihe addieren</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {vereinfachung()}
      <div class="card" id="vs-t" style="font-size:17px;font-weight:600;line-height:1.6"></div>
    </div>''', sid='s-vs', body_cls='body noclick'),
    folie(T, 'Rechenbeispiel', '''    <div class="card step" style="font-size:19px;font-weight:700;margin-bottom:10px">U = 12 V, R1 = 2 Ω in Reihe zu R2 = 6 Ω ∥ R3 = 3 Ω</div>
    <ol class="steps-list">
      <li class="step">Ersatzwiderstand der Parallelgruppe<small>R23 = (6 · 3) : (6 + 3) = 18 : 9 = <b>2 Ω</b></small></li>
      <li class="step">Gesamtwiderstand und Gesamtstrom<small>R = 2 Ω + 2 Ω = <b>4 Ω</b> – I = 12 V : 4 Ω = <b>3 A</b></small></li>
      <li class="step">Teilspannungen<small>U1 = 2 Ω · 3 A = <b>6 V</b> – an der Parallelgruppe: U23 = 12 V − 6 V = <b>6 V</b></small></li>
      <li class="step">Zweigströme<small>I2 = 6 V : 6 Ω = <b>1 A</b> – I3 = 6 V : 3 Ω = <b>2 A</b> – Probe: 1 A + 2 A = 3 A ✓</small></li>
    </ol>'''),
    folie(T, 'Rechnen – zum Ausprobieren', f'''    <div class="ctrl"><span style="width:170px">R1: <span class="c" id="g1-v1">2 Ω</span></span><input type="range" id="g1-s1" min="1" max="10" step="1" value="2"></div>
    <div class="ctrl" style="margin-top:4px"><span style="width:170px">R2: <span class="c" id="g1-v2">6 Ω</span></span><input type="range" id="g1-s2" min="1" max="12" step="1" value="6"></div>
    <div class="ctrl" style="margin-top:4px"><span style="width:170px">R3: <span class="c" id="g1-v3">3 Ω</span></span><input type="range" id="g1-s3" min="1" max="12" step="1" value="3"></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr;margin-top:6px">
      {G_KREIS}
      <div class="card" id="g1-t" style="font-size:16px;font-weight:700;line-height:1.7"></div>
    </div>''', sid='s-g1', body_cls='body noclick'),
    folie(T, 'Gemischte Schaltung im Kfz', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Gemeinsame Masse</b>Zwei Rückleuchten (parallel) hängen an einer gemeinsamen Masseleitung (in Reihe). Ist die Masse korrodiert, leuchten beide schwächer.</div>
      <div class="tip step"><b>Gemeinsame Sicherung</b>Mehrere Verbraucher parallel, davor eine Sicherung in Reihe. Löst sie aus, ist der ganze Kreis aus.</div>
      <div class="tip step"><b>Fehlersuche</b>Nur ein Verbraucher betroffen? Fehler in seinem Zweig. Alle zusammen betroffen? Fehler im gemeinsamen Teil.</div>
      <div class="tip step"><b>Stromlaufplan lesen</b>Erst die gemeinsamen Teile suchen (Sicherung, Schalter, Masse), dann die einzelnen Zweige.</div>
    </div>'''),
    folie(T, 'Fehler finden – ein Beispiel', '''    <ol class="steps-list">
      <li class="step">Kunde: „Beide Rückleuchten sind dunkel, Bremslicht auch schwach.“<small>mehrere Verbraucher betroffen → Fehler im gemeinsamen Teil</small></li>
      <li class="step">Spannung an der Leuchte messen – im Betrieb<small>nur 9,5 V statt ca. 12 V: Es fehlen 2,5 V</small></li>
      <li class="step">Spannungsfall an der Masseleitung messen<small>2,3 V – hier steckt ein Übergangswiderstand in Reihe</small></li>
      <li class="step">Massepunkt reinigen, Kontrolle<small>danach nur noch wenige Zehntel Volt – beide Leuchten wieder hell</small></li>
    </ol>
    <div class="note step">Beispielwerte – Grenzwerte laut Hersteller.</div>'''),
    video(T, 'gemischt'),
    kurztest(T, [
        ('Was ist eine gemischte Schaltung?', ['Bauteile teils in Reihe, teils parallel', 'Nur Lampen und Motoren gemischt', 'Zwei Batterien'], 0, 'Für jeden Teil gelten seine eigenen Regeln.'),
        ('Was machst du zuerst beim Berechnen?', ['Alle Widerstände addieren', 'Parallelgruppen durch einen Ersatzwiderstand ersetzen', 'Die Spannungen addieren'], 1, 'Dann bleibt eine einfache Reihenschaltung übrig.'),
        ('R1 = 4 Ω in Reihe mit zwei parallelen Widerständen von je 8 Ω. Wie groß ist der Gesamtwiderstand?', ['20 Ω', '12 Ω', '8 Ω'], 2, 'Parallel: 8 Ω ∥ 8 Ω = 4 Ω, dazu R1: 4 Ω + 4 Ω = 8 Ω.'),
        ('Beide Rückleuchten leuchten schwach. Wo suchst du zuerst?', ['Im gemeinsamen Teil, z. B. an der Masse', 'An einer einzelnen Lampe', 'Am Radio'], 0, 'Sind alle betroffen, liegt der Fehler im gemeinsamen Teil.'),
    ]),
    merke(T, ['Teils in Reihe, teils parallel', 'Parallelgruppen ersetzen, dann Reihe addieren',
              'Rückwärts: Strom, Teilspannungen, Zweigströme', 'Alle betroffen? Gemeinsamen Teil prüfen']),
]
gemischt_js = SCHALT_JS + '''
<script>
(function () {
  const T = [
    '<b>1. Die Schaltung:</b> R1 liegt in Reihe. R2 und R3 liegen parallel – sie hängen an denselben zwei Punkten.',
    '<b>2. Parallelgruppe ersetzen:</b> R2 ∥ R3 = (6 · 3) : (6 + 3) = <span class="c">2 Ω</span>. Jetzt ist es eine einfache Reihenschaltung.',
    '<b>3. Reihe addieren:</b> R = R1 + R23 = 2 Ω + 2 Ω = <span class="c">4 Ω</span>. Gesamtstrom: I = 12 V : 4 Ω = 3 A.'
  ];
  const bt = document.querySelectorAll('#s-vs [data-g]'), gs = document.querySelectorAll('#s-vs .vs');
  function g(i) { gs.forEach(x => x.style.display = +x.dataset.s === i ? '' : 'none'); bt.forEach(x => x.classList.toggle('on', +x.dataset.g === i)); document.getElementById('vs-t').innerHTML = T[i]; }
  bt.forEach(x => x.onclick = () => g(+x.dataset.g)); g(0);

  const svg = document.getElementById('g1-svg');
  const fa = Flow(svg, document.getElementById('g1-pa'), { spacing: 34, speed: 60, r: 6, color: '#ffd34d' });
  const fb = Flow(svg, document.getElementById('g1-pb'), { spacing: 38, speed: 60, r: 6, color: '#ffd34d' });
  const s = [1, 2, 3].map(i => document.getElementById('g1-s' + i));
  const z = (x, d) => (Math.round(x * Math.pow(10, d)) / Math.pow(10, d)).toString().replace('.', ',');
  function r() {
    const [R1, R2, R3] = s.map(x => +x.value);
    const R23 = R2 * R3 / (R2 + R3), R = R1 + R23, I = 12 / R, U1 = R1 * I, U23 = 12 - U1, I2 = U23 / R2, I3 = U23 / R3;
    [R1, R2, R3].forEach((v, i) => { document.getElementById('g1-v' + (i + 1)).textContent = v + ' Ω'; document.getElementById('g1-l' + (i + 1)).textContent = 'R' + (i + 1) + ' = ' + v + ' Ω'; });
    document.getElementById('g1-u1').textContent = 'U1 = ' + z(U1, 1) + ' V';
    document.getElementById('g1-u23').textContent = 'U23 = ' + z(U23, 1) + ' V';
    document.getElementById('g1-i').textContent = 'I = ' + z(I, 2) + ' A';
    document.getElementById('g1-mp').textContent = 'nach R1 noch ' + z(U23, 1) + ' V';
    fa.speed = 20 + I2 * 30; fb.speed = 20 + I3 * 30;
    document.getElementById('g1-t').innerHTML = 'R23 = ' + z(R23, 2) + ' Ω<br>R = ' + R1 + ' Ω + ' + z(R23, 2) + ' Ω = <span class="c">' + z(R, 2) + ' Ω</span><br>I = <span class="c">' + z(I, 2) + ' A</span><br>U1 = ' + z(U1, 1) + ' V, U23 = ' + z(U23, 1) + ' V<br>I2 = ' + z(I2, 2) + ' A, I3 = ' + z(I3, 2) + ' A';
  }
  s.forEach(x => x.addEventListener('input', r)); r();
})();
</script>'''

STYLE = '  .symbol { font-size: 64px; }'

if __name__ == '__main__':
    seite('reihe.html', 'Reihenschaltung – Grundlagen Elektrik', 't-reihe', THEMA_R, reihe, STYLE, reihe_js)
    seite('parallel.html', 'Parallelschaltung – Grundlagen Elektrik', 't-parallel', THEMA_P, parallel, STYLE, parallel_js)
    seite('gemischt.html', 'Gemischte Schaltung – Grundlagen Elektrik', 't-gemischt', THEMA_G, gemischt, STYLE, gemischt_js)
    print('ok')
