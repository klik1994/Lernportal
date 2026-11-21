"""Motormanagement: Zündung – drei Präsentationen.
Aufruf: cd tools && python3 mm_zuendung.py"""
from praesentation_bauen import *

THEMA = 'Motormanagement: Zündung'
K = 'MOTORMANAGEMENT · ZÜNDUNG'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'

# Zündkerze als SVG (eigene feste Farben, damit sie im hellen und dunklen Modus gleich aussieht)
def kerze(x=0, y=0, s=1.0, spalt=14, funke=False):
    f = '<path class="funke" d="M118 {a} l-6 5 l8 3 l-6 6" fill="none" stroke="#ffd34d" stroke-width="3" stroke-linecap="round"/>'.format(a=372 - spalt + 2) if funke else ''
    return f'''<g transform="translate({x} {y}) scale({s})">
    <rect x="110" y="8" width="20" height="30" rx="4" fill="#a9b3c1" stroke="#6b7686" stroke-width="2"/>
    <rect x="98" y="38" width="44" height="160" rx="12" fill="#f4f1ea" stroke="#8a94a3" stroke-width="2"/>
    <path d="M98 70 h44 M98 92 h44 M98 114 h44 M98 136 h44" stroke="#c9c3b6" stroke-width="3"/>
    <rect x="84" y="196" width="72" height="46" rx="4" fill="#6b7686" stroke="#4d5664" stroke-width="2"/>
    <rect x="96" y="242" width="48" height="12" fill="#c6a15a"/>
    <rect x="98" y="254" width="44" height="80" fill="#a9b3c1" stroke="#6b7686" stroke-width="2"/>
    <path d="M98 264 l44 10 M98 280 l44 10 M98 296 l44 10 M98 312 l44 10" stroke="#6b7686" stroke-width="3"/>
    <rect x="114" y="334" width="12" height="{38 - spalt}" fill="#c9c3b6" stroke="#8a94a3" stroke-width="1.5"/>
    <path d="M142 334 V{372 + 10} H112" fill="none" stroke="#6b7686" stroke-width="9" stroke-linejoin="round"/>
    {f}
  </g>'''


# ---------------------------------------------------------------- Zündanlage
T = 'ZÜNDANLAGE'
SPULE = '''<svg viewBox="0 0 560 330" width="540" height="318" style="display:block;margin:0 auto" id="zs-svg">
  <text x="24" y="58" font-size="17" font-weight="800" fill="#f05e4e">+ 12 V</text>
  <path id="zs-prim" d="M40 72 H210 V92 V232 V262 H130 V278" fill="none" stroke="#ecf1f8" stroke-width="4"/>
  <path d="M210 100 H218 M210 140 H218 M210 180 H218 M210 220 H218" stroke="#ecf1f8" stroke-width="3"/>
  <rect x="70" y="278" width="120" height="40" rx="8" fill="#213552" stroke="#94a4ba" stroke-width="2"/>
  <text x="130" y="303" text-anchor="middle" font-size="15" font-weight="800" fill="#ecf1f8">Steuergerät</text>
  <rect x="222" y="66" width="76" height="188" rx="6" fill="#3b4250"/>
  <g id="zs-feld" style="transition:opacity .25s, transform .25s;transform-origin:260px 160px;opacity:0">
    <ellipse cx="260" cy="160" rx="66" ry="116" fill="none" stroke="#a07cf5" stroke-width="2.5" stroke-dasharray="7 6"/>
    <ellipse cx="260" cy="160" rx="92" ry="136" fill="none" stroke="#a07cf5" stroke-width="2" stroke-dasharray="7 6" opacity=".6"/>
  </g>
  <g stroke="#ff8f3f" stroke-width="7" fill="none"><ellipse cx="238" cy="100" rx="20" ry="8"/><ellipse cx="238" cy="140" rx="20" ry="8"/><ellipse cx="238" cy="180" rx="20" ry="8"/><ellipse cx="238" cy="220" rx="20" ry="8"/></g>
  <g stroke="#5b8cff" stroke-width="2.5" fill="none"><ellipse cx="282" cy="84" rx="18" ry="5"/><ellipse cx="282" cy="96" rx="18" ry="5"/><ellipse cx="282" cy="108" rx="18" ry="5"/><ellipse cx="282" cy="120" rx="18" ry="5"/><ellipse cx="282" cy="132" rx="18" ry="5"/><ellipse cx="282" cy="144" rx="18" ry="5"/><ellipse cx="282" cy="156" rx="18" ry="5"/><ellipse cx="282" cy="168" rx="18" ry="5"/><ellipse cx="282" cy="180" rx="18" ry="5"/><ellipse cx="282" cy="192" rx="18" ry="5"/><ellipse cx="282" cy="204" rx="18" ry="5"/><ellipse cx="282" cy="216" rx="18" ry="5"/><ellipse cx="282" cy="228" rx="18" ry="5"/></g>
  <path d="M300 84 H460 V140 M300 228 H400 V300 H460 V236" fill="none" stroke="#ecf1f8" stroke-width="3"/>
  <rect x="448" y="140" width="24" height="56" rx="4" fill="#94a4ba"/>
  <rect x="455" y="196" width="10" height="14" fill="#94a4ba"/>
  <rect x="444" y="226" width="32" height="10" fill="#94a4ba"/>
  <path id="zs-funke" d="M462 210 l-9 5 l13 3 l-9 6" fill="none" stroke="#ffd34d" stroke-width="4" stroke-linecap="round" style="opacity:0"/>
  <text x="484" y="222" font-size="15" font-weight="800" fill="#94a4ba">Zünd-</text>
  <text x="484" y="240" font-size="15" font-weight="800" fill="#94a4ba">kerze</text>
  <text x="238" y="30" text-anchor="end" font-size="14" font-weight="700" fill="#ff8f3f">Primär: wenige Windungen</text>
  <text x="282" y="30" font-size="14" font-weight="700" fill="#5b8cff">Sekundär: sehr viele Windungen</text>
</svg>'''

zuendanlage = [
    titel_folie(K, '⚡', 'Zündanlage', 'Wie aus 12 Volt ein Zündfunke wird'),
    lernziele(T, ['Welche Aufgabe die Zündanlage hat', 'Aufbau: Steuergerät, Zündspule, Zündkerze',
                  'Wie die Zündspule Hochspannung erzeugt', 'Bauarten, sicher arbeiten und prüfen']),
    folie(T, 'Aufgabe der Zündanlage', '''    <div class="card step" style="font-size:21px;font-weight:700;margin-bottom:20px">Die Zündanlage entzündet das Gemisch im Brennraum – <span class="c">zum richtigen Zeitpunkt</span> und mit <span class="c">genug Energie</span>.</div>
    <div class="kette">
      <div class="glied step"><b>Steuergerät</b><span>berechnet den Zündzeitpunkt</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Zündspule</b><span>macht aus 12 V Hochspannung</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Zündkerze</b><span>der Funke springt im Brennraum über</span></div>
    </div>'''),
    folie(T, 'Die Zündspule – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost" id="zs-ein">1. Einschalten</button><button class="btn ghost" id="zs-aus">2. Abschalten</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.25fr 1fr">
      {SPULE}
      <div>
        <div class="card"><div class="muted" style="font-size:15px;font-weight:800">SPANNUNG AN DER ZÜNDKERZE</div><div class="lcd2" id="zs-v" style="font-size:34px;margin-top:6px">0 V</div></div>
        <div class="card" id="zs-t" style="margin-top:12px;font-size:18px;font-weight:600"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Vereinfachte Darstellung, Beispielwert. Stromrichtung: technisch von + nach −.</p>''', sid='s-zs', body_cls='body noclick'),
    folie(T, 'Was passiert in der Zündspule?', '''    <ol class="steps-list">
      <li class="step">Das Steuergerät schaltet die <span class="c">Primärwicklung</span> ein<small>Strom fließt, ein Magnetfeld baut sich auf – diese Zeit heißt Schließzeit</small></li>
      <li class="step">Zum Zündzeitpunkt schaltet das Steuergerät <span class="c">ab</span><small>der Strom in der Primärwicklung wird schlagartig unterbrochen</small></li>
      <li class="step">Das Magnetfeld <span class="c">bricht zusammen</span><small>das geht sehr schnell</small></li>
      <li class="step">In der <span class="c">Sekundärwicklung</span> entsteht Hochspannung<small>sie hat sehr viele Windungen – der Funke springt an der Zündkerze über</small></li>
    </ol>'''),
    folie(T, 'Typische Werte', '''    <div class="values">
      <div class="val step from-left"><b>12 V</b><span>Primärseite – Spannung aus dem Bordnetz</span></div>
      <div class="val step from-left"><b>wenige ms</b><span>Schließzeit – so lange baut sich das Magnetfeld auf</span></div>
      <div class="val step from-left"><b>ca. 10.000–30.000 V</b><span>Zündspannung, die der Funke braucht (je nach Last und Elektrodenabstand)</span></div>
      <div class="val step from-left"><b>bis ca. 40.000 V</b><span>was moderne Zündspulen liefern können</span></div>
    </div>
    <div class="note step">Richtwerte – genaue Werte laut Herstellerangabe</div>'''),
    folie(T, 'Bauarten', '''    <div class="grid3" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:21px">Einzelfunken-Zündspule</div>
        <ul UL><li>eine Spule pro Zylinder</li><li>sitzt direkt auf der Zündkerze (Stabzündspule)</li><li class="grn">heute Standard</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">Doppelfunken-Zündspule</div>
        <ul UL><li>eine Spule für zwei Zylinder</li><li>beide Kerzen funken gleichzeitig</li><li>ein Funke ist ein „Stützfunke“ im Ausstoßtakt</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">Zündverteiler</div>
        <ul UL><li>eine Spule für alle Zylinder</li><li>der Verteilerfinger verteilt die Hochspannung</li><li class="muted">nur noch bei älteren Fahrzeugen</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Sicher arbeiten', '''    <div class="warn step"><b>Hochspannung – Lebensgefahr</b>Bei Zündung an oder laufendem Motor nichts an Zündspulen, Zündkabeln oder Kerzensteckern anfassen.</div>
    <div class="warn step" style="margin-top:12px"><b>Herzschrittmacher</b>Wer einen Herzschrittmacher trägt, arbeitet nicht an der laufenden Zündanlage.</div>
    <div class="warn step" style="margin-top:12px"><b>Keine Funkenprobe „an Masse halten“</b>Nur mit Prüf-Funkenstrecke nach Vorgabe. Offene Zündspulen können beschädigt werden, unverbrannter Kraftstoff schadet dem Katalysator.</div>'''),
    folie(T, 'Zündanlage prüfen', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher und Aussetzerzähler lesen<small>welcher Zylinder setzt aus?</small></li>
      <li class="step">Sichtprüfung<small>Risse und Brandspuren an Zündspule und Stecker, Feuchtigkeit im Kerzenschacht</small></li>
      <li class="step">Quertausch<small>Zündspule mit einem anderen Zylinder tauschen – wandert der Fehler mit, ist die Spule defekt</small></li>
      <li class="step">Oszilloskop nach Vorgabe<small>Zündspannungsbild mit Zange am Prüfadapter – nicht in den Stecker stechen</small></li>
    </ol>
    <div class="tip step" style="margin-top:6px"><b>Achtung</b>Viele Zündspulen haben eine eingebaute Endstufe (Elektronik). Diese nicht mit dem Ohmmeter prüfen.</div>'''),
    video(T, 'mm-zuendanlage'),
    kurztest(T, [
        ('Was macht die Zündspule?', ['Sie macht aus 12 V Hochspannung', 'Sie speichert Kraftstoff', 'Sie misst die Drehzahl'], 0, 'Aus 12 V Bordnetzspannung werden viele tausend Volt.'),
        ('Wann springt der Funke an der Zündkerze über?', ['Beim Einschalten der Primärwicklung', 'Beim Abschalten der Primärwicklung', 'Dauernd, solange der Motor läuft'], 1, 'Beim Abschalten bricht das Magnetfeld zusammen – in der Sekundärwicklung entsteht Hochspannung.'),
        ('Welche Wicklung hat sehr viele Windungen?', ['Die Primärwicklung', 'Beide gleich viele', 'Die Sekundärwicklung'], 2, 'Viele Windungen auf der Sekundärseite = hohe Spannung.'),
        ('Wie findest du heraus, ob eine Zündspule defekt ist?', ['Quertausch: wandert der Fehler mit?', 'Kerze an Masse halten', 'Ohmmeter an die Endstufe'], 0, 'Wandert der Aussetzer mit der Spule zum anderen Zylinder, ist die Spule defekt.'),
    ]),
    merke(T, ['Steuergerät → Zündspule → Zündkerze', 'Einschalten: Magnetfeld baut sich auf|die Schließzeit',
              'Abschalten: Hochspannung, der Funke springt', 'Hochspannung – Lebensgefahr!']),
]
zuendanlage_js = '''<script src="assets/schaltung.js"></script>
<script>
(function () {
  const svg = document.getElementById('zs-svg');
  const f = Flow(svg, document.getElementById('zs-prim'), { spacing: 34, speed: 80, r: 6, color: '#28aaf5' });
  f.on(false);
  const feld = document.getElementById('zs-feld'), funke = document.getElementById('zs-funke');
  const v = document.getElementById('zs-v'), t = document.getElementById('zs-t');
  const ein = document.getElementById('zs-ein'), aus = document.getElementById('zs-aus');
  let tm;
  function start() {
    clearTimeout(tm); f.on(false); feld.style.opacity = 0; feld.style.transform = 'scale(.6)'; funke.style.opacity = 0;
    v.textContent = '0 V'; ein.classList.remove('on'); aus.classList.remove('on');
    t.innerHTML = 'Tippe auf <b>Einschalten</b>.';
  }
  ein.onclick = () => {
    clearTimeout(tm); f.on(true); feld.style.opacity = 1; feld.style.transform = 'scale(1)'; funke.style.opacity = 0;
    v.textContent = '0 V'; ein.classList.add('on'); aus.classList.remove('on');
    t.innerHTML = '<span class="c">Strom fließt</span> durch die Primärwicklung, das Magnetfeld baut sich auf (Schließzeit). An der Kerze passiert noch nichts. Jetzt <b>Abschalten</b>.';
  };
  aus.onclick = () => {
    if (!ein.classList.contains('on')) { t.innerHTML = 'Erst <b>Einschalten</b> – ohne Magnetfeld keine Hochspannung.'; return; }
    f.on(false); feld.style.opacity = 0; feld.style.transform = 'scale(.3)'; funke.style.opacity = 1;
    v.textContent = 'ca. 30.000 V'; ein.classList.remove('on'); aus.classList.add('on');
    t.innerHTML = 'Das Magnetfeld <span class="c">bricht zusammen</span>. In der Sekundärwicklung entsteht Hochspannung – <span class="c">der Funke springt</span>.';
    tm = setTimeout(() => { funke.style.opacity = 0; v.textContent = '0 V'; }, 1500);
  };
  document.getElementById('s-zs').addEventListener('slideshow', start);
  start();
})();
</script>'''

# ---------------------------------------------------------------- Zündkerze
T = 'ZÜNDKERZE'
KERZE_SYM = f'<svg viewBox="70 0 100 400" width="56" height="200" style="display:block;margin:auto"><title>ZK</title>{kerze()}</svg>'

LBL = [(24, 'Anschluss'), (120, 'Isolator (Keramik)'), (220, 'Sechskant'), (294, 'Gewinde mit Dichtring'), (356, 'Mittelelektrode'), (388, 'Masseelektrode')]
lbl_svg = ''.join(f'<g class="lbl" style="opacity:0;transition:opacity .3s"><line x1="{165 if i != 4 else 128}" y1="{y}" x2="220" y2="{y}" stroke="#94a4ba" stroke-width="2"/>'
                  f'<text x="228" y="{y + 5}" font-size="16" font-weight="800" fill="#ecf1f8">{tx}</text></g>' for i, (y, tx) in enumerate(LBL))

BILDER = '''    <div class="choice" style="margin-bottom:14px">
      <button class="btn ghost on" data-b="0">Rehbraun</button><button class="btn ghost" data-b="1">Verrußt</button>
      <button class="btn ghost" data-b="2">Verölt</button><button class="btn ghost" data-b="3">Weiß / Schmelzperlen</button>
    </div>
    <div class="grid2" style="align-items:center;grid-template-columns:250px 1fr">
      <svg viewBox="80 296 90 100" width="230" height="255" style="display:block;margin:0 auto">
        <rect x="98" y="300" width="44" height="34" fill="#a9b3c1" stroke="#6b7686" stroke-width="2"/>
        <rect x="114" y="334" width="12" height="24" id="kb-mit" fill="#b88a5a"/>
        <path d="M142 334 V382 H112" fill="none" id="kb-mas" stroke="#b88a5a" stroke-width="9" stroke-linejoin="round"/>
        <g id="kb-perl" style="opacity:0"><circle cx="118" cy="362" r="3" fill="#ffffff" stroke="#8a94a3"/><circle cx="130" cy="376" r="2.5" fill="#ffffff" stroke="#8a94a3"/><circle cx="138" cy="350" r="2.5" fill="#ffffff" stroke="#8a94a3"/></g>
      </svg>
      <div class="card" style="font-size:18px;font-weight:600;line-height:1.5" id="kb-t"></div>
    </div>'''

zuendkerze = [
    titel_folie(K, KERZE_SYM, 'Zündkerze', 'Aufbau, Kerzenbild und richtig wechseln'),
    lernziele(T, ['Wie eine Zündkerze aufgebaut ist', 'Elektrodenabstand und Wärmewert',
                  'Das Kerzenbild lesen', 'Zündkerzen richtig wechseln']),
    folie(T, 'Aufbau einer Zündkerze', f'''    <div class="grid2" style="align-items:center;grid-template-columns:1fr 1fr">
      <svg viewBox="70 0 360 410" width="360" height="400" style="display:block;margin:0 auto" id="zk-svg">{kerze()}{lbl_svg}</svg>
      <ol class="steps-list" id="zk-steps">
        <li class="step">Oben: <span class="c">Anschluss</span> für die Zündspule</li>
        <li class="step"><span class="c">Isolator</span> aus Keramik – hält die Hochspannung vom Gehäuse fern</li>
        <li class="step"><span class="c">Sechskant</span> für den Kerzenschlüssel</li>
        <li class="step"><span class="c">Gewinde</span> mit Dichtring – sitzt im Zylinderkopf</li>
        <li class="step">Zwischen <span class="c">Mittel- und Masseelektrode</span> springt der Funke</li>
      </ol>
    </div>''', sid='s-zk'),
    folie(T, 'Elektrodenabstand – zum Ausprobieren', '''    <div class="ctrl"><span style="width:300px">Elektrodenabstand: <span class="c" id="ea-v">0,9 mm</span></span><input type="range" id="ea" min="0.4" max="1.6" step="0.1" value="0.9"></div>
    <div class="grid2" style="margin-top:14px;align-items:center;grid-template-columns:250px 1fr">
      <svg viewBox="80 296 90 100" width="230" height="255" style="display:block;margin:0 auto">
        <rect x="98" y="300" width="44" height="34" fill="#a9b3c1" stroke="#6b7686" stroke-width="2"/>
        <rect x="114" y="334" width="12" id="ea-mit" height="24" fill="#c9c3b6" stroke="#8a94a3" stroke-width="1.5"/>
        <path d="M142 334 V382 H112" fill="none" stroke="#6b7686" stroke-width="9" stroke-linejoin="round"/>
      </svg>
      <div>
        <div class="card"><div class="muted" style="font-size:15px;font-weight:800">BENÖTIGTE ZÜNDSPANNUNG</div><div class="lcd2" id="ea-kv" style="font-size:34px;margin-top:6px">—</div></div>
        <div class="card" id="ea-t" style="margin-top:12px;font-size:18px;font-weight:600"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Beispielwerte. Richtwert für den Abstand: ca. 0,7–1,1 mm – immer laut Hersteller.</p>''', sid='s-ea', body_cls='body noclick'),
    folie(T, 'Der Wärmewert', '''    <div class="card step" style="font-size:20px;font-weight:600;margin-bottom:16px">Die Kerzenspitze muss <span class="c">heiß genug</span> sein, damit Ablagerungen verbrennen (Selbstreinigung) – aber <span class="c">nicht zu heiß</span>, sonst entzündet sie das Gemisch von selbst.</div>
    <div class="values">
      <div class="val step from-left"><b>unter ca. 450 °C</b><span>zu kalt: Die Kerze verrußt, es kommt zu Aussetzern</span></div>
      <div class="val step from-left"><b>ca. 450–850 °C</b><span>richtiger Bereich: Die Kerze reinigt sich selbst</span></div>
      <div class="val step from-left"><b>über ca. 850 °C</b><span>zu heiß: Glühzündungen – Motorschaden möglich</span></div>
    </div>
    <div class="note step">Richtwerte – immer die Kerze mit dem Wärmewert laut Hersteller einbauen</div>'''),
    folie(T, 'Das Kerzenbild lesen – zum Ausprobieren', BILDER, sid='s-kb', body_cls='body noclick'),
    folie(T, 'Zündkerzen wechseln', '''    <ol class="steps-list">
      <li class="step">Nur bei <span class="c">kaltem Motor</span><small>der Zylinderkopf ist meist aus Aluminium – das Gewinde kann sonst ausreißen</small></li>
      <li class="step">Zündspule vorsichtig abziehen, Kerzenschacht <span class="c">ausblasen</span><small>kein Schmutz in den Brennraum</small></li>
      <li class="step">Neue Kerze prüfen<small>Typ, Wärmewert und Elektrodenabstand laut Hersteller</small></li>
      <li class="step">Erst <span class="c">von Hand</span> eindrehen, dann mit dem <span class="c">Drehmomentschlüssel</span> anziehen<small>nicht verkanten – Anzugsdrehmoment laut Hersteller</small></li>
    </ol>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Wechselintervall</b>laut Wartungsplan. Longlife-Kerzen (Platin, Iridium) halten länger.</div>
      <div class="tip step"><b>Iridium- und Platinkerzen</b>Elektrodenabstand nicht nachbiegen – die feine Mittelelektrode bricht leicht.</div>
      <div class="tip step"><b>Brandspuren am Isolator</b>Der Funke schlägt außen über – Kerze und Kerzenstecker prüfen.</div>
      <div class="warn step"><b>Heruntergefallen?</b>Eine Kerze, die auf den Boden gefallen ist, nicht mehr einbauen – der Isolator kann innen gerissen sein.</div>
    </div>'''),
    video(T, 'mm-zuendkerze'),
    kurztest(T, [
        ('Wozu dient der Isolator aus Keramik?', ['Er hält die Hochspannung vom Gehäuse fern', 'Er kühlt den Motor', 'Er dichtet den Kraftstoff ab'], 0, 'Sonst würde die Hochspannung nicht am Funkenspalt, sondern am Gehäuse überspringen.'),
        ('Was passiert bei zu großem Elektrodenabstand?', ['Der Funke wird stärker, alles besser', 'Es braucht mehr Zündspannung – Aussetzer möglich', 'Nichts'], 1, 'Die Zündspule muss mehr Spannung liefern, bei Last kann der Funke ausbleiben.'),
        ('Die Kerze ist schwarz und trocken verrußt. Was ist eine mögliche Ursache?', ['Gemisch zu mager', 'Zündung zu früh', 'Gemisch zu fett oder viel Kurzstrecke'], 2, 'Verrußt = zu fett oder die Kerze wird nicht heiß genug.'),
        ('Wie wechselst du Zündkerzen richtig?', ['Bei kaltem Motor, von Hand eindrehen, Drehmoment laut Hersteller', 'Bei heißem Motor mit dem Schlagschrauber', 'Möglichst fest anziehen'], 0, 'Kalter Motor schont das Aluminiumgewinde, das Drehmoment kommt vom Hersteller.'),
    ]),
    merke(T, ['Isolator, Mittel- und Masseelektrode|der Funke springt im Elektrodenabstand',
              'Abstand und Wärmewert laut Hersteller', 'Rehbraun = in Ordnung',
              'Wechseln: kalter Motor, Drehmomentschlüssel']),
]
zuendkerze_js = '''<script>
(function () {
  const s = document.getElementById('s-zk');
  const lb = s.querySelectorAll('.lbl');
  const MAP = [[0], [1], [2], [3], [4, 5]];
  function upd() {
    const n = s.querySelectorAll('#zk-steps .step.on').length;
    lb.forEach(l => l.style.opacity = 0);
    for (let i = 0; i < n; i++) MAP[i].forEach(k => lb[k].style.opacity = 1);
  }
  s.addEventListener('stepon', upd); s.addEventListener('stepoff', upd); s.addEventListener('slideshow', upd);

  const ea = document.getElementById('ea');
  function e() {
    const g = +ea.value, kv = 6 + 14 * g;
    document.getElementById('ea-v').textContent = g.toFixed(1).replace('.', ',') + ' mm';
    document.getElementById('ea-kv').textContent = 'ca. ' + (Math.round(kv)).toLocaleString('de-DE') + '.000 V';
    document.getElementById('ea-mit').setAttribute('height', Math.max(4, 38 - g * 15).toFixed(1));
    let t;
    if (g < 0.65) t = '<b class="ora">Zu klein:</b> kleiner, schwacher Funke – das Gemisch entzündet sich schlecht.';
    else if (g <= 1.15) t = '<b class="grn">Passend:</b> im üblichen Bereich – genauer Wert laut Hersteller.';
    else t = '<b class="red">Zu groß:</b> Es braucht viel Spannung. Bei Last bleibt der Funke aus – Zündaussetzer, die Zündspule wird belastet.';
    document.getElementById('ea-t').innerHTML = t;
  }
  ea.addEventListener('input', e); e();

  const B = [
    ['#b88a5a', '#b88a5a', 0, '<b class="grn">Rehbraun bis grau:</b> Alles in Ordnung. Gemisch, Zündung und Wärmewert passen.'],
    ['#1d1d1f', '#1d1d1f', 0, '<b>Schwarz, trocken verrußt:</b> Gemisch zu fett, viel Kurzstrecke oder Wärmewert zu niedrig. Prüfen: Luftfilter, Gemischbildung, Lambdawerte.'],
    ['#2a2418', '#3a2f1c', 0, '<b>Schwarz, feucht und ölig:</b> Öl im Brennraum – z. B. Kolbenringe, Ventilschaftdichtungen oder Turbolader prüfen.'],
    ['#f2f2f2', '#d9d9d9', 1, '<b class="red">Weiß, Schmelzperlen, abgebrannte Elektroden:</b> Die Kerze war zu heiß – Gemisch zu mager, Zündung zu früh oder falscher Wärmewert. Gefahr von Motorschaden!'],
  ];
  const bt = document.querySelectorAll('#s-kb [data-b]');
  function b(i) {
    document.getElementById('kb-mit').setAttribute('fill', B[i][0]);
    document.getElementById('kb-mas').setAttribute('stroke', B[i][1]);
    document.getElementById('kb-perl').style.opacity = B[i][2];
    document.getElementById('kb-t').innerHTML = B[i][3];
    bt.forEach(x => x.classList.toggle('on', +x.dataset.b === i));
  }
  bt.forEach(x => x.onclick = () => b(+x.dataset.b)); b(0);
})();
</script>'''

# ---------------------------------------------------------------- Zündzeitpunkt
T = 'ZÜNDZEITPUNKT'
DRUCK = '''<svg viewBox="0 0 600 300" width="560" height="280" style="display:block;margin:0 auto">
  <line x1="50" y1="250" x2="570" y2="250" stroke="#94a4ba" stroke-width="2"/>
  <line x1="260" y1="30" x2="260" y2="250" stroke="#94a4ba" stroke-width="2" stroke-dasharray="6 6"/>
  <text x="260" y="276" text-anchor="middle" font-size="16" font-weight="800" fill="#ecf1f8">OT</text>
  <text x="70" y="276" font-size="14" font-weight="700" fill="#94a4ba">vor OT</text>
  <text x="550" y="276" text-anchor="end" font-size="14" font-weight="700" fill="#94a4ba">nach OT</text>
  <text x="56" y="40" font-size="14" font-weight="700" fill="#94a4ba">Druck im Zylinder</text>
  <path id="dr-kurve" d="" fill="none" stroke="#ff8f3f" stroke-width="5" stroke-linejoin="round"/>
  <g id="dr-z"><path d="M0 -14 l-7 12 h8 l-6 14" fill="none" stroke="#ffd34d" stroke-width="4" stroke-linecap="round"/><text y="-22" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Zündung</text></g>
</svg>'''
KURBEL = '''<svg class="klein" viewBox="0 0 260 260" width="240" height="240" style="display:block;margin:0 auto">
  <circle cx="130" cy="130" r="95" fill="none" stroke="#94a4ba" stroke-width="3"/>
  <path id="fv-bogen" d="" fill="none" stroke="#ff8f3f" stroke-width="10" stroke-linecap="round"/>
  <line x1="130" y1="22" x2="130" y2="48" stroke="#ecf1f8" stroke-width="4"/>
  <text x="130" y="16" text-anchor="middle" font-size="15" font-weight="800" fill="#ecf1f8">OT</text>
  <g id="fv-z"><circle r="9" fill="#ffd34d"/></g>
  <text x="130" y="138" text-anchor="middle" font-size="26" font-weight="900" fill="#ff8f3f" id="fv-w">—</text>
  <text x="130" y="162" text-anchor="middle" font-size="14" font-weight="700" fill="#94a4ba">vor OT</text>
</svg>'''

zeitpunkt = [
    titel_folie(K, 'OT', 'Zündzeitpunkt', 'Früh, spät, Klopfen und Zündaussetzer', 'font-size:72px'),
    lernziele(T, ['Warum vor dem oberen Totpunkt gezündet wird', 'Wie Drehzahl und Last den Zündzeitpunkt verändern',
                  'Klopfen und Klopfregelung', 'Zündaussetzer erkennen und finden']),
    folie(T, 'Warum vor OT zünden? – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost" data-z="0">Zu früh</button><button class="btn ghost on" data-z="1">Richtig</button><button class="btn ghost" data-z="2">Zu spät</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.4fr 1fr">
      {DRUCK}
      <div class="card" id="dr-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Die Verbrennung braucht Zeit. Der höchste Druck soll kurz nach OT entstehen – darum wird vorher gezündet. Vereinfachte Darstellung.</p>''', sid='s-dr', body_cls='body noclick'),
    folie(T, 'Frühverstellung – zum Ausprobieren', f'''    <div class="ctrl"><span style="width:280px">Drehzahl: <span class="c" id="fv-n">2.000 1/min</span></span><input type="range" id="fv" min="800" max="6000" step="200" value="2000"></div>
    <div class="choice" style="margin:12px 0"><button class="btn ghost on" data-l="t">Teillast</button><button class="btn ghost" data-l="v">Volllast</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:260px 1fr">
      {KURBEL}
      <div class="card" style="font-size:18px;font-weight:600;line-height:1.5">
        <p style="margin:0 0 10px"><span class="c">Mehr Drehzahl → früher zünden:</span> Der Kolben ist schneller, die Verbrennung braucht aber gleich lange.</p>
        <p style="margin:0"><span class="c">Volllast → später zünden:</span> Viel Füllung brennt schneller, und die Klopfgefahr steigt.</p>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Beispielwerte – das Steuergerät nimmt den Wert aus dem Zündkennfeld.</p>''', sid='s-fv', body_cls='body noclick'),
    folie(T, 'Was das Steuergerät berücksichtigt', '''    <div class="kette">
      <div class="glied step" style="border-top-color:var(--grn)"><b>Drehzahl und Last</b><span>Grundwert aus dem Zündkennfeld</span></div><div class="flow-arrow step k-e"></div>
      <div class="glied step" style="border-top-color:var(--grn)"><b>Korrekturen</b><span>Motortemperatur, Ansauglufttemperatur, Klopfen</span></div><div class="flow-arrow step k-v"></div>
      <div class="glied step" style="border-top-color:var(--ora)"><b>Zündzeitpunkt</b><span>für jeden Zylinder</span></div>
    </div>
    <div class="tip step" style="margin-top:20px"><b>Gut zu wissen</b>Den Zündzeitpunkt stellt man heute nicht mehr ein – du kannst ihn aber im Diagnosegerät als Messwert ablesen (Grad vor OT).</div>'''),
    folie(T, 'Klopfen', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Was ist Klopfen?</div>
        <ul UL><li>Das Gemisch entzündet sich an mehreren Stellen <b>von selbst</b></li><li>es entstehen harte Druckspitzen</li><li>man hört ein helles Klingeln</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Ursachen</div>
        <ul UL><li>Zündung zu früh</li><li>Kraftstoff mit zu niedriger Oktanzahl</li><li>Motor zu heiß, Ablagerungen im Brennraum</li></ul></div>
      <div class="warn step" style="grid-column:1/-1"><b>Folgen</b>Dauerhaftes Klopfen zerstört Kolben, Kolbenringe und Zylinderkopfdichtung.</div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Die Klopfregelung', '''    <div class="kette">
      <div class="glied step" style="border-top-color:var(--grn)"><b>Klopfsensor</b><span>am Motorblock – erzeugt bei Klopfschwingungen eine Spannung</span></div><div class="flow-arrow step k-e"></div>
      <div class="glied step" style="border-top-color:var(--pur)"><b>Steuergerät</b><span>erkennt, welcher Zylinder klopft</span></div><div class="flow-arrow step k-v"></div>
      <div class="glied step" style="border-top-color:var(--ora)"><b>Zündung später</b><span>nur bei diesem Zylinder, danach Schritt für Schritt wieder früher</span></div>
    </div>
    <div class="tip step" style="margin-top:20px"><b>Klopfsensor einbauen</b>Genau mit dem Anzugsdrehmoment laut Hersteller anziehen, keine Unterlegscheiben – sonst meldet er falsch. Prüfen mit Diagnosegerät oder Oszilloskop.</div>'''),
    folie(T, 'Zündaussetzer', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">So erkennt sie das Steuergerät</div>
        <ul UL><li>der Kurbelwellensensor meldet die Drehzahl sehr genau</li><li>fehlt eine Verbrennung, wird die Kurbelwelle kurz langsamer</li><li>Eintrag im Fehlerspeicher, Aussetzerzähler pro Zylinder</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Folgen</div>
        <ul UL><li>Ruckeln, Leistungsverlust</li><li>unverbrannter Kraftstoff gelangt in den Katalysator</li><li>der Kat überhitzt und kann zerstört werden</li></ul></div>
      <div class="warn step" style="grid-column:1/-1"><b>Motorkontrollleuchte blinkt</b>Starke Aussetzer, Gefahr für den Kat: Leistung wegnehmen und das Fahrzeug bald in die Werkstatt bringen. Oft wird der Zylinder abgeschaltet.</div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Zündaussetzer finden', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher und Aussetzerzähler lesen<small>welcher Zylinder ist betroffen?</small></li>
      <li class="step">Zündspule quertauschen<small>wandert der Fehler mit, ist die Zündspule defekt</small></li>
      <li class="step">Zündkerze prüfen oder quertauschen<small>Kerzenbild, Elektrodenabstand, Risse im Isolator</small></li>
      <li class="step">Fehler bleibt am Zylinder?<small>Einspritzventil und Kompression prüfen</small></li>
    </ol>'''),
    video(T, 'mm-zuendzeitpunkt'),
    kurztest(T, [
        ('Warum wird vor dem oberen Totpunkt gezündet?', ['Weil die Verbrennung Zeit braucht', 'Damit der Anlasser entlastet wird', 'Weil die Zündspule sonst zu heiß wird'], 0, 'Der höchste Druck soll kurz nach OT entstehen – darum muss vorher gezündet werden.'),
        ('Was macht das Steuergerät bei steigender Drehzahl?', ['Später zünden', 'Früher zünden', 'Nichts'], 1, 'Der Kolben ist schneller, die Verbrennung braucht gleich lange – also früher zünden.'),
        ('Was macht die Klopfregelung, wenn ein Zylinder klopft?', ['Sie erhöht den Ladedruck', 'Sie spritzt mehr Öl ein', 'Sie zündet diesen Zylinder später'], 2, 'Danach wird der Zündzeitpunkt Schritt für Schritt wieder früher gestellt.'),
        ('Die Motorkontrollleuchte blinkt. Was bedeutet das?', ['Starke Zündaussetzer – Gefahr für den Katalysator', 'Ölwechsel fällig', 'Alles in Ordnung'], 0, 'Leistung wegnehmen und bald in die Werkstatt.'),
    ]),
    merke(T, ['Zündung vor OT – die Verbrennung braucht Zeit', 'Mehr Drehzahl → früher|Volllast → später',
              'Klopfen: Zündung später (Klopfregelung)', 'Aussetzer: Quertausch, Kat schützen']),
]
zeitpunkt_js = '''<script>
(function () {
  const X = a => 50 + (a + 60) * 3.5;
  const Z = [
    [-42, -4, 140, true, '<b class="red">Zu früh:</b> Der Druck steigt, während der Kolben noch nach oben läuft. Er arbeitet gegen den Kolben – <b>Klopfgefahr</b>, Motorschaden möglich.'],
    [-20, 14, 165, false, '<b class="grn">Richtig:</b> Der höchste Druck entsteht kurz nach OT. Der Kolben wird kräftig nach unten gedrückt – <b>volle Leistung</b>, wenig Verbrauch.'],
    [6, 42, 85, false, '<b class="ora">Zu spät:</b> Der Kolben läuft schon nach unten, der Druck bleibt niedrig. <b>Weniger Leistung</b>, mehr Verbrauch, heißes Abgas.']
  ];
  const bt = document.querySelectorAll('#s-dr [data-z]');
  function z(i) {
    const [az, pk, h, klopf] = Z[i];
    let d = '';
    for (let a = -60; a <= 80; a += 1) {
      let p = 55 * Math.exp(-Math.pow(a / 32, 2)) + h * Math.exp(-Math.pow((a - pk) / 15, 2)) * (a > az ? 1 : 0.0);
      if (a > az) p = 55 * Math.exp(-Math.pow(a / 32, 2)) + h * Math.exp(-Math.pow((a - pk) / 15, 2)) * Math.min(1, (a - az) / 10);
      if (klopf && a > pk - 6 && a < pk + 16) p += 12 * Math.sin(a * 2.2);
      d += (d ? ' L' : 'M') + X(a).toFixed(1) + ' ' + (250 - p).toFixed(1);
    }
    document.getElementById('dr-kurve').setAttribute('d', d);
    document.getElementById('dr-z').setAttribute('transform', 'translate(' + X(az) + ' ' + 200 + ')');
    document.getElementById('dr-t').innerHTML = Z[i][4];
    bt.forEach(x => x.classList.toggle('on', +x.dataset.z === i));
  }
  bt.forEach(x => x.onclick = () => z(+x.dataset.z)); z(1);

  const fv = document.getElementById('fv'); let last = 't';
  const lb = document.querySelectorAll('#s-fv [data-l]');
  function f() {
    const n = +fv.value;
    const w = Math.round(6 + (n - 800) / 5200 * 24 + (last === 't' ? 10 : 0));
    document.getElementById('fv-n').textContent = n.toLocaleString('de-DE') + ' 1/min';
    document.getElementById('fv-w').textContent = 'ca. ' + w + '°';
    const r = 95, cx = 130, cy = 130, rad = -w * Math.PI / 180;
    const px = cx + r * Math.sin(rad), py = cy - r * Math.cos(rad);
    document.getElementById('fv-z').setAttribute('transform', 'translate(' + px.toFixed(1) + ' ' + py.toFixed(1) + ')');
    document.getElementById('fv-bogen').setAttribute('d', 'M' + px.toFixed(1) + ' ' + py.toFixed(1) + ' A' + r + ' ' + r + ' 0 0 1 ' + cx + ' ' + (cy - r));
    lb.forEach(x => x.classList.toggle('on', x.dataset.l === last));
  }
  fv.addEventListener('input', f);
  lb.forEach(x => x.onclick = () => { last = x.dataset.l; f(); });
  f();
})();
</script>'''

STYLE = '''  .symbol { font-size: 96px; }
  .funke { animation: fk 1.2s infinite; }
  @keyframes fk { 0%, 60% { opacity: 0; } 65%, 80% { opacity: 1; } 100% { opacity: 0; } }'''

if __name__ == '__main__':
    seite('mm-zuendanlage.html', 'Zündanlage – Motormanagement', 't-mm3', THEMA, zuendanlage, STYLE, zuendanlage_js)
    seite('mm-zuendkerze.html', 'Zündkerze – Motormanagement', 't-mm3', THEMA, zuendkerze, STYLE, zuendkerze_js)
    seite('mm-zuendzeitpunkt.html', 'Zündzeitpunkt – Motormanagement', 't-mm3', THEMA, zeitpunkt, STYLE, zeitpunkt_js)
    print('ok')
