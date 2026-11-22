"""Fahrwerk, Bremsanlage, Fahrerassistenzsysteme – je eine Präsentation.
Aufruf: cd tools && python3 fahrwerk.py"""
from praesentation_bauen import *

UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'
GE = '#ffd34d'
STYLE = '''  .symbol { font-size: 80px; }
  .rb { display: flex; flex-wrap: wrap; justify-content: center; gap: 6px; font-size: 44px; font-weight: 900; margin: 6px 0 14px; }
  .rb span { cursor: pointer; padding: 4px 12px; border-radius: 12px; background: var(--card); transition: background .2s, color .2s; }
  .rb span.on { background: var(--c); color: var(--on-c); }
  html.light svg text[fill="#ffd34d"] { fill: #8a6400; }
  @media (max-width: 820px), (max-height: 520px) { .rb { font-size: 28px; } .val b { font-size: 14px; hyphens: auto; overflow-wrap: anywhere; } }'''


def btns(attr, items, first=0):
    return ''.join(f'<button class="btn ghost{" on" if i == first else ""}" data-{attr}="{k}">{t}</button>' for i, (k, t) in enumerate(items))


def grafik(pid, w=600, h=240):
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="display:block;margin:0 auto;max-width:100%;height:auto" id="{pid}-svg">
      <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#18283f"/><g id="{pid}-g"></g></svg>'''


# ================================================================ Fahrwerk
T = 'FAHRWERK'
K = 'FAHRWERK UND BREMSEN'


def feder_svg():
    return f'''<svg viewBox="0 0 260 300" width="260" height="300" class="klein" style="display:block;margin:0 auto;max-width:100%;height:auto" id="fd-svg">
      <line x1="10" y1="280" x2="250" y2="280" stroke="#94a4ba" stroke-width="4"/>
      <g id="fd-k"><rect x="40" y="40" width="180" height="56" rx="10" fill="#213552" stroke="#ecf1f8" stroke-width="3"/><text x="130" y="74" text-anchor="middle" font-size="17" font-weight="900" fill="#ecf1f8">Aufbau</text></g>
      <polyline id="fd-f" fill="none" stroke="{GE}" stroke-width="4" points=""/>
      <g id="fd-d"><rect id="fd-d1" x="168" y="96" width="22" height="70" rx="3" fill="#94a4ba"/><rect x="164" y="160" width="30" height="70" rx="4" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/></g>
      <circle cx="130" cy="240" r="40" fill="#18283f" stroke="#ecf1f8" stroke-width="6"/><circle cx="130" cy="240" r="12" fill="#94a4ba"/>
      <text x="70" y="160" text-anchor="end" font-size="14" font-weight="800" fill="{GE}">Feder</text>
      <text x="200" y="250" font-size="14" font-weight="800" fill="#94a4ba">Dämpfer</text>
    </svg>'''


def geo_svg():
    return '''<svg viewBox="0 0 600 300" width="600" height="300" style="display:block;margin:0 auto;max-width:100%;height:auto" id="ge-svg">
      <rect x="0" y="0" width="600" height="300" rx="12" fill="#18283f"/><g id="ge-g"></g></svg>'''


def reifen_svg():
    return f'''<svg viewBox="0 0 520 230" width="520" height="230" style="display:block;margin:0 auto;max-width:100%;height:auto" id="rv-svg">
      <rect x="0" y="0" width="520" height="230" rx="12" fill="#18283f"/><g id="rv-g"></g></svg>'''


fahrwerk = [
    titel_folie(K, 'FW', 'Das Fahrwerk', 'Federung, Dämpfung, Lenkung, Achsgeometrie, Räder und Reifen', 'font-size:96px'),
    lernziele(T, ['Welche Aufgaben das Fahrwerk hat und wie es aufgebaut ist', 'Was Feder und Stoßdämpfer machen',
                  'Was Spur, Sturz und Nachlauf bedeuten', 'Wie du Räder, Reifen und Fahrwerk prüfst']),
    folie(T, 'Aufgaben und Aufbau', '''    <div class="values">
      <div class="val step from-left"><b>Radaufhängung</b><span>führt die Räder – Achsen, Querlenker, Gelenke, Gummilager</span></div>
      <div class="val step from-left"><b>Federn</b><span>tragen das Fahrzeug und fangen Stöße von der Straße auf</span></div>
      <div class="val step from-left"><b>Stoßdämpfer</b><span>bremsen das Nachschwingen der Federn – die Räder bleiben auf der Straße</span></div>
      <div class="val step from-left"><b>Lenkung</b><span>bewegt die Vorderräder in die gewünschte Richtung</span></div>
      <div class="val step from-left"><b>Räder, Reifen</b><span>einzige Verbindung zur Straße – je Reifen nur etwa eine Handfläche</span></div>
    </div>'''),
    folie(T, 'Achsarten', '''    <div class="grid3" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:21px">Starrachse</div><ul UL><li>beide Räder fest verbunden</li><li>sehr robust, trägt viel</li><li>z. B. Lkw, Transporter, Geländewagen</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">Verbundlenkerachse</div><ul UL><li>zwei Längslenker mit Querprofil</li><li>einfach und platzsparend</li><li>oft hinten bei Klein- und Kompaktwagen</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">Einzelradaufhängung</div><ul UL><li>jedes Rad federt für sich</li><li>z. B. McPherson-Federbein vorn, Mehrlenkerachse hinten</li><li>guter Komfort und gute Straßenlage</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Feder und Stoßdämpfer – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap">{btns('d', [('gut', 'Dämpfer in Ordnung'), ('def', 'Dämpfer defekt'), ('ohne', 'Ohne Dämpfer')])}<button class="btn" id="fd-go" style="--c:var(--tea)">▶ Über die Bodenwelle</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:0.7fr 1.3fr">
      {feder_svg()}
      <div>{grafik('fg', 600, 220)}
        <div class="card" id="fd-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px"></div></div>
    </div>''', sid='s-fd', body_cls='body noclick'),
    folie(T, 'Spur, Sturz und Nachlauf – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:8px">{btns('g', [('spur', 'Spur (von oben)'), ('sturz', 'Sturz (von vorn)'), ('nl', 'Nachlauf (von der Seite)')])}<button class="btn" id="ge-bs" style="--c:var(--tea);display:none">▶ Rad trifft Bordstein</button></div>
    <div class="ctrl"><span style="width:220px">Einstellung: <span class="c" id="ge-n">0°</span></span><input type="range" id="ge-r" min="-3" max="3" step="0.5" value="0"></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr;margin-top:8px">
      {geo_svg()}
      <div class="card" id="ge-t" style="font-size:16px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Winkel im Bild stark übertrieben. Sollwerte laut Hersteller, gemessen auf dem Achsmessstand.</p>''', sid='s-ge', body_cls='body noclick'),
    folie(T, 'Die Lenkung', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Aufbau</div>
        <ul UL><li>Lenkrad und Lenksäule</li><li>Zahnstangenlenkung: das Ritzel bewegt die Zahnstange nach links oder rechts</li><li>Spurstangen mit Gelenken führen zu den Rädern</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Elektrische Servolenkung</div>
        <ul UL><li>ein Sensor misst, wie stark du lenkst</li><li>ein Elektromotor hilft mit</li><li>Lenkwinkelsensor meldet die Lenkradstellung, z. B. an das ESP</li></ul></div>
    </div>
    <div class="warn step" style="margin-top:12px"><b>Nach Arbeiten an der Lenkung</b>Achsvermessung durchführen und den Lenkwinkelsensor mit dem Tester neu einstellen (Grundeinstellung) – sonst arbeiten ESP und Assistenzsysteme falsch.</div>'''.replace('UL', UL)),
    folie(T, 'Die Reifenbezeichnung – zum Antippen', '''    <div class="rb" id="rb"><span data-k="0">205</span><span>/</span><span data-k="1">55</span><span data-k="2">R</span><span data-k="3">16</span><span data-k="4">91</span><span data-k="5">V</span></div>
    <div class="grid2" style="align-items:start">
      <div class="card" id="rb-t" style="font-size:18px;font-weight:600;line-height:1.5;margin:0"></div>
      <div class="card" style="margin:0;font-size:16px;line-height:1.55"><b>Alter: DOT-Nummer</b><br>Die letzten vier Ziffern, z. B. <b>3424</b>, bedeuten: hergestellt in der <b>34. Woche 2024</b>.<br><br><b>Profiltiefe</b><br>Gesetzlich mindestens <b>1,6 mm</b>. Empfohlen: Sommerreifen ca. 3 mm, Winterreifen ca. 4 mm.</div>
    </div>''', sid='s-rb', body_cls='body noclick'),
    folie(T, 'Reifenverschleiß lesen – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap;gap:6px">{btns('v', [('ok', 'Gleichmäßig'), ('hoch', 'Mitte abgefahren'), ('nied', 'Beide Schultern'), ('innen', 'Innen abgefahren'), ('aussen', 'Außen, mit Grat'), ('wasch', 'Auswaschungen')])}</div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {reifen_svg()}
      <div class="card" id="rv-t" style="font-size:16px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Querschnitt durch das Profil, vereinfacht. Rote Linie: gesetzliche Mindestprofiltiefe 1,6 mm.</p>''', sid='s-rv', body_cls='body noclick'),
    folie(T, 'Fahrwerk prüfen', '''    <ol class="steps-list">
      <li class="step">Sichtprüfung<small>Stoßdämpfer ölfeucht? Gummilager rissig? Manschetten an Gelenken und Lenkung dicht? Federn gebrochen?</small></li>
      <li class="step">Spiel prüfen<small>Rad oben/unten und links/rechts greifen und rütteln: Radlager, Traggelenk, Spurstangenkopf</small></li>
      <li class="step">Räder und Reifen<small>Profiltiefe, Verschleißbild, Alter, Beschädigungen, Reifendruck laut Hersteller</small></li>
      <li class="step">Probefahrt<small>Geräusche, zieht das Fahrzeug zur Seite, steht das Lenkrad gerade?</small></li>
      <li class="step">Achsvermessung<small>nach Arbeiten an Lenkung oder Radaufhängung und bei auffälligem Reifenverschleiß</small></li>
    </ol>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Radschrauben</b>Mit dem Drehmomentschlüssel nach Herstellerangabe anziehen – über Kreuz. Kunden auf das Nachziehen nach einer kurzen Strecke hinweisen.</div>
      <div class="tip step"><b>Achsweise tauschen</b>Stoßdämpfer und Federn immer paarweise an einer Achse erneuern.</div>
      <div class="warn step"><b>Federspanner</b>Eine gespannte Feder hat enorme Kraft. Nur geprüfte Federspanner verwenden, richtig ansetzen, nie mit Schlagschrauber.</div>
      <div class="tip step"><b>Reifendruck</b>Sollwert steht im Tankdeckel oder in der Türsäule. Bei Reifendruck-Kontrollsystem (RDKS) nach Änderung anlernen laut Hersteller.</div>
    </div>'''),
    video(T, 'fw-fahrwerk'),
    kurztest(T, [
        ('Welche Aufgabe hat der Stoßdämpfer?', ['Er trägt das Gewicht des Fahrzeugs', 'Er bremst das Nachschwingen der Feder', 'Er lenkt die Räder'], 1, 'So bleiben die Räder auf der Straße.'),
        ('Was bedeutet in „205/55 R16 91V“ die Zahl 205?', ['Reifenbreite in mm', 'Felgendurchmesser', 'Höchstgeschwindigkeit'], 0, '55 = Höhe in % der Breite, 16 = Felgendurchmesser in Zoll.'),
        ('Ein Reifen ist in der Mitte stärker abgefahren. Was ist die Ursache?', ['Zu wenig Luftdruck', 'Stoßdämpfer defekt', 'Zu hoher Luftdruck'], 2, 'Zu wenig Luftdruck verschleißt die Schultern.'),
        ('Wann ist eine Achsvermessung nötig?', ['Nach jedem Ölwechsel', 'Nach Arbeiten an Lenkung oder Radaufhängung', 'Nur beim Reifenwechsel'], 1, 'Z. B. nach dem Tausch einer Spurstange oder eines Querlenkers.'),
    ]),
    merke(T, ['Feder trägt – Dämpfer bremst das Schwingen', 'Spur, Sturz, Nachlauf: Sollwerte laut Hersteller',
              '205/55 R16 91V: Breite, Höhe %, Radial, Zoll, Last, Tempo', 'Mindestprofil 1,6 mm – Verschleißbild verrät Ursachen']),
]
fahrwerk_js = '''<script>
(function () {
  const g = (id, s) => document.getElementById(id).innerHTML = s;
  // Feder/Dämpfer
  const Z = { gut: 0.35, def: 0.07, ohne: 0.015 };
  const TX = {
    gut: '<b class="grn">Dämpfer in Ordnung:</b> Nach der Bodenwelle schwingt der Aufbau nur kurz nach. Die Räder bleiben auf der Straße.',
    def: '<b class="red">Dämpfer defekt:</b> Der Aufbau schwingt lange nach. Das Rad springt, die Haftung fehlt immer wieder: längerer Bremsweg, schlechtere Kurvenlage, ABS und ESP regeln öfter.',
    ohne: '<b class="red">Ohne Dämpfer:</b> Die Feder schwingt fast ungebremst weiter – das Fahrzeug „schaukelt“. Darum ist ein defekter Dämpfer ein Sicherheitsmangel.'
  };
  let m = 'gut', t0 = null, raf = null;
  const yOf = t => t < 0 ? 0 : -38 * Math.exp(-Z[m] * 2 * Math.PI * 1.2 * t) * Math.cos(2 * Math.PI * 1.2 * Math.sqrt(1 - Z[m] * Z[m]) * t);
  function feder(y) {
    document.getElementById('fd-k').setAttribute('transform', 'translate(0 ' + y + ')');
    document.getElementById('fd-d1').setAttribute('y', 96 + y);
    const top = 96 + y, bot = 220, n = 10; let p = '100,' + top;
    for (let i = 1; i < n; i++) p += ' ' + (i % 2 ? 80 : 120) + ',' + (top + (bot - top) * i / n);
    document.getElementById('fd-f').setAttribute('points', p + ' 100,' + bot);
  }
  function kurve(tm) {
    let o = '<line x1="30" y1="110" x2="590" y2="110" stroke="#94a4ba" stroke-width="1.5" stroke-dasharray="5 5"/><text x="34" y="24" font-size="14" font-weight="800" fill="#94a4ba">Bewegung des Aufbaus</text><text x="586" y="210" text-anchor="end" font-size="13" font-weight="800" fill="#94a4ba">Zeit →</text>';
    let d = '';
    for (let x = 30; x <= 590; x += 2) { const t = (x - 30) / 560 * 5; if (t > tm) break; d += (d ? ' L' : 'M') + x + ' ' + (110 + 2.2 * yOf(t)).toFixed(1); }
    g('fg-g', o + '<path d="' + d + '" fill="none" stroke="#1fc8b3" stroke-width="4"/>');
  }
  function lauf(ts) {
    if (t0 === null) t0 = ts;
    const t = (ts - t0) / 1000;
    feder(yOf(t)); kurve(t);
    if (t < 5) raf = requestAnimationFrame(lauf);
  }
  function start() { cancelAnimationFrame(raf); t0 = null; raf = requestAnimationFrame(lauf); }
  const db = document.querySelectorAll('#s-fd [data-d]');
  db.forEach(b => b.onclick = () => { m = b.dataset.d; db.forEach(x => x.classList.toggle('on', x === b)); document.getElementById('fd-t').innerHTML = TX[m]; start(); });
  document.getElementById('fd-go').onclick = start;
  feder(0); kurve(0); document.getElementById('fd-t').innerHTML = TX.gut;
  document.getElementById('s-fd').addEventListener('slideshow', start);

  // Achsgeometrie
  let gm = 'spur', dreh = 0, bsT = 0, bsRaf = null;
  const gr = document.getElementById('ge-r');
  function rad(x, y, w, h, rot, cx, cy) { return '<rect x="' + (x - w / 2) + '" y="' + (y - h / 2) + '" width="' + w + '" height="' + h + '" rx="8" fill="#213552" stroke="#ecf1f8" stroke-width="4" transform="rotate(' + rot + ' ' + (cx || x) + ' ' + (cy || y) + ')"/>'; }
  function geo() {
    const a = +gr.value, k = 6;
    let o = '', t = '';
    document.getElementById('ge-n').textContent = (a > 0 ? '+' : '') + String(a).replace('.', ',') + '°';
    if (gm === 'spur') {
      o += '<rect x="190" y="60" width="220" height="200" rx="30" fill="none" stroke="#94a4ba" stroke-width="3" stroke-dasharray="8 6"/>';
      o += '<path d="M300 40 V14 M290 26 L300 12 L310 26" fill="none" stroke="#94a4ba" stroke-width="3"/><text x="320" y="30" font-size="14" font-weight="800" fill="#94a4ba">Fahrtrichtung</text>';
      o += rad(190, 120, 30, 90, a * k) + rad(410, 120, 30, 90, -a * k);
      o += '<line x1="190" y1="60" x2="190" y2="180" stroke="#94a4ba" stroke-width="1.5" stroke-dasharray="4 4"/><line x1="410" y1="60" x2="410" y2="180" stroke="#94a4ba" stroke-width="1.5" stroke-dasharray="4 4"/>';
      t = a > 0 ? '<b>Vorspur:</b> Die Räder stehen vorne enger zusammen als hinten. Das gibt guten Geradeauslauf. Zu viel Vorspur: Reifen außen abgefahren, oft mit Grat.'
        : a < 0 ? '<b>Nachspur:</b> Die Räder stehen vorne weiter auseinander als hinten. Zu viel Nachspur: Reifen innen abgefahren, Fahrzeug unruhig.'
        : '<b>Spur 0:</b> Die Räder stehen parallel. Bewege den Regler.';
    } else if (gm === 'sturz') {
      o += '<line x1="80" y1="250" x2="520" y2="250" stroke="#94a4ba" stroke-width="4"/><rect x="200" y="70" width="200" height="90" rx="20" fill="none" stroke="#94a4ba" stroke-width="3" stroke-dasharray="8 6"/>';
      o += rad(170, 190, 44, 120, -a * k, 170, 250) + rad(430, 190, 44, 120, a * k, 430, 250);
      o += '<line x1="170" y1="110" x2="170" y2="250" stroke="#94a4ba" stroke-width="1.5" stroke-dasharray="4 4"/><line x1="430" y1="110" x2="430" y2="250" stroke="#94a4ba" stroke-width="1.5" stroke-dasharray="4 4"/>';
      o += '<text x="300" y="285" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Ansicht von vorn</text>';
      t = a < 0 ? '<b>Negativer Sturz:</b> Die Räder sind oben nach innen geneigt. Das gibt gute Seitenführung in Kurven. Zu viel: Reifen innen abgefahren.'
        : a > 0 ? '<b>Positiver Sturz:</b> Die Räder sind oben nach außen geneigt. Der Reifen wird außen stärker abgefahren.'
        : '<b>Sturz 0:</b> Die Räder stehen senkrecht. Bewege den Regler.';
    } else {
      const cx0 = 210;
      o += '<line x1="30" y1="260" x2="350" y2="260" stroke="#94a4ba" stroke-width="4"/><circle cx="' + cx0 + '" cy="170" r="90" fill="#213552" stroke="#ecf1f8" stroke-width="5"/><circle cx="' + cx0 + '" cy="170" r="10" fill="#94a4ba"/>';
      const r = (a * k) * Math.PI / 180, dx = Math.tan(r) * 150;
      o += '<line x1="' + (cx0 + dx * 0.9) + '" y1="35" x2="' + (cx0 - dx * 0.6) + '" y2="260" stroke="#ffd34d" stroke-width="5"/>';
      o += '<circle cx="' + cx0 + '" cy="260" r="6" fill="#ecf1f8"/><circle cx="' + (cx0 - dx * 0.6) + '" cy="260" r="6" fill="#ffd34d"/>';
      o += '<path d="M90 40 H30 M42 30 L28 40 L42 50" fill="none" stroke="#94a4ba" stroke-width="3"/><text x="98" y="45" font-size="14" font-weight="800" fill="#94a4ba">Fahrtrichtung</text>';
      o += '<text x="' + (cx0 + 30) + '" y="30" font-size="14" font-weight="800" fill="#ffd34d">Lenkachse</text>';
      // Draufsicht
      const px = 480 - a * 14, py = 170, cxw = 480;
      o += '<rect x="370" y="56" width="216" height="228" rx="12" fill="#213552" stroke="#94a4ba" stroke-width="2"/><text x="478" y="80" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">von oben</text>';
      o += '<line x1="385" y1="' + py + '" x2="575" y2="' + py + '" stroke="#94a4ba" stroke-width="1.5" stroke-dasharray="5 5"/>';
      if (bsT > 0 && bsT < 0.6) o += '<rect x="' + (395 + (1 - Math.min(1, bsT / 0.4)) * 40) + '" y="122" width="26" height="22" rx="3" fill="#94a4ba"/><text x="408" y="114" text-anchor="middle" font-size="12" font-weight="800" fill="#94a4ba">Bordstein</text>';
      o += '<g transform="rotate(' + (-dreh).toFixed(1) + ' ' + px + ' ' + py + ')"><rect x="' + (cxw - 48) + '" y="' + (py - 14) + '" width="96" height="28" rx="8" fill="#18283f" stroke="#ecf1f8" stroke-width="4"/><circle cx="' + cxw + '" cy="' + py + '" r="6" fill="#ecf1f8"/></g>';
      o += '<circle cx="' + px + '" cy="' + py + '" r="6" fill="#ffd34d"/>';
      o += '<text x="478" y="268" text-anchor="middle" font-size="12" font-weight="800" fill="#94a4ba">gelb: Lenkachse · weiß: Reifen</text>';
      t = a > 0 ? '<b>Positiver Nachlauf:</b> Die Lenkachse trifft die Straße <span class="c">vor</span> dem Reifen-Aufstandspunkt. Das Rad wird „gezogen“ wie beim Einkaufswagen: Die Lenkung stellt sich von selbst gerade.'
        : a < 0 ? '<b>Negativer Nachlauf:</b> Die Lenkung stellt sich nicht mehr gerade, das Fahrzeug läuft unruhig. Ungleicher Nachlauf links/rechts: das Fahrzeug zieht zur Seite.'
        : '<b>Nachlauf 0:</b> Die Lenkachse geht genau durch den Aufstandspunkt. Bewege den Regler.';
      if (bsT > 0) t = (a > 0 ? '<b class="grn">Stoß vom Bordstein:</b> Das Rad wird kurz verdreht. Weil der Reifen <span class="c">hinter</span> der Lenkachse aufsteht, zieht die Seitenkraft am Reifen das Rad wieder gerade – wie beim Einkaufswagen. Die Lenkung bleibt ruhig.'
          : a < 0 ? '<b class="red">Stoß vom Bordstein:</b> Mit negativem Nachlauf dreht die Seitenkraft das Rad noch weiter weg – die Lenkung schlägt aus, das Fahrzeug wird unruhig.'
          : '<b class="ora">Stoß vom Bordstein:</b> Ohne Nachlauf fehlt der Hebelarm. Nichts dreht das Rad zurück – der Fahrer muss selbst gegenlenken.')
        + '<br><span class="muted" style="font-size:15px">Hartes Auffahren kann aber auch Teile verbiegen (Querlenker, Spurstange, Federbein). Dann zieht das Fahrzeug, das Lenkrad steht schief: Achsvermessung, verbogene Teile erneuern – nie richten.</span>';
    }
    document.getElementById('ge-bs').style.display = gm === 'nl' ? '' : 'none';
    g('ge-g', o); document.getElementById('ge-t').innerHTML = t;
    document.querySelectorAll('#s-ge [data-g]').forEach(b => b.classList.toggle('on', b.dataset.g === gm));
  }
  function bordstein() {
    const a = +gr.value; let t0 = null;
    cancelAnimationFrame(bsRaf);
    const step = ts => {
      if (t0 === null) t0 = ts;
      bsT = (ts - t0) / 1000;
      if (bsT < 0.4) dreh = 18 * bsT / 0.4;
      else { const u = bsT - 0.4; dreh = a > 0 ? 18 * Math.exp(-u * a * 1.2) : a < 0 ? 18 + 22 * (1 - Math.exp(-u * -a * 0.8)) : 18; }
      geo();
      if (bsT < 3) bsRaf = requestAnimationFrame(step);
    };
    bsRaf = requestAnimationFrame(step);
  }
  document.getElementById('ge-bs').onclick = bordstein;
  gr.addEventListener('input', () => { cancelAnimationFrame(bsRaf); bsT = 0; dreh = 0; geo(); });
  document.querySelectorAll('#s-ge [data-g]').forEach(b => b.onclick = () => { gm = b.dataset.g; gr.value = gm === 'sturz' ? -1 : 1; cancelAnimationFrame(bsRaf); bsT = 0; dreh = 0; geo(); });
  gr.value = 1; geo();

  // Reifenbezeichnung
  const RB = ['<b>205</b> = Reifenbreite in Millimetern.', '<b>55</b> = Querschnittsverhältnis: Die Flanke ist 55 % so hoch wie der Reifen breit ist.', '<b>R</b> = Radialbauart (fast alle Pkw-Reifen).',
    '<b>16</b> = Felgendurchmesser in Zoll.', '<b>91</b> = Tragfähigkeitsindex: 91 steht für 615 kg pro Reifen.', '<b>V</b> = Geschwindigkeitsindex: V steht für höchstens 240 km/h.'];
  const rs = document.querySelectorAll('#rb [data-k]');
  function rb(i) { rs.forEach(s => s.classList.toggle('on', +s.dataset.k === i)); document.getElementById('rb-t').innerHTML = RB[i]; }
  rs.forEach(s => s.onclick = () => rb(+s.dataset.k)); rb(0);

  // Reifenverschleiß
  const RV = {
    ok: [[8, 8, 8, 8, 8, 8], '<b class="grn">Gleichmäßig:</b> Luftdruck, Spur und Sturz passen.'],
    hoch: [[6.5, 4.5, 3, 3, 4.5, 6.5], '<b class="red">Mitte abgefahren:</b> Der Luftdruck war zu hoch – der Reifen liegt nur in der Mitte auf.'],
    nied: [[3, 5, 7, 7, 5, 3], '<b class="red">Beide Schultern abgefahren:</b> Der Luftdruck war zu niedrig. Der Reifen walkt, wird heiß und verbraucht mehr Kraftstoff.'],
    innen: [[2.2, 4, 5.5, 6.5, 7, 7.5], '<b class="red">Innen abgefahren:</b> Zu viel negativer Sturz oder zu viel Nachspur. Achsvermessung!'],
    aussen: [[7.5, 7, 6.5, 5.5, 4, 2.2], '<b class="red">Außen abgefahren, mit Grat:</b> Zu viel Vorspur (oder positiver Sturz). Achsvermessung!'],
    wasch: [[5, 7, 4.5, 7, 4, 6.5], '<b class="red">Auswaschungen:</b> Unregelmäßige Stellen rund um den Reifen. Meist Stoßdämpfer defekt oder Rad unwuchtig.']
  };
  const vb = document.querySelectorAll('#s-rv [data-v]');
  function rv(k) {
    const h = RV[k][0]; let o = '<line x1="40" y1="190" x2="480" y2="190" stroke="#94a4ba" stroke-width="4"/>';
    const y = mm => 190 - mm * 18;
    h.forEach((mm, i) => { const x = 60 + i * 70; o += '<rect x="' + x + '" y="' + y(mm) + '" width="58" height="' + (190 - y(mm)) + '" rx="4" fill="#213552" stroke="#ecf1f8" stroke-width="2"/>'; });
    o += '<line x1="40" y1="' + y(1.6) + '" x2="480" y2="' + y(1.6) + '" stroke="#f05e4e" stroke-width="2.5" stroke-dasharray="6 5"/>';
    o += '<text x="60" y="214" font-size="14" font-weight="800" fill="#94a4ba">innen</text><text x="460" y="214" text-anchor="end" font-size="14" font-weight="800" fill="#94a4ba">außen</text>';
    o += '<text x="40" y="30" font-size="14" font-weight="800" fill="#94a4ba">Profil neu ca. 8 mm</text>';
    g('rv-g', o); document.getElementById('rv-t').innerHTML = RV[k][1];
    vb.forEach(b => b.classList.toggle('on', b.dataset.v === k));
  }
  vb.forEach(b => b.onclick = () => rv(b.dataset.v)); rv('ok');
})();
</script>'''


# ================================================================ Bremse
T = 'BREMSE'


def hydr_svg():
    return '''<svg viewBox="0 0 560 310" width="560" height="310" style="display:block;margin:0 auto;max-width:100%;height:auto" id="hy-svg">
      <path id="hy-fl" d="" fill="#ff8f3f" opacity=".5"/>
      <path d="M76 40 V266 H504 V100 M356 100 V226 H141 V40" fill="none" stroke="#ecf1f8" stroke-width="5" stroke-linejoin="round"/>
      <g id="hy-k1"></g><g id="hy-k2"></g>
      <text x="248" y="252" text-anchor="middle" font-size="17" font-weight="900" fill="#ecf1f8" id="hy-p">p</text>
      <text x="108" y="296" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Hauptzylinder Ø 22 mm</text>
      <text x="430" y="296" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Sattelkolben Ø 54 mm</text>
    </svg>'''


def scheibe_svg():
    return '''<svg viewBox="0 0 420 300" width="420" height="300" style="display:block;margin:0 auto;max-width:100%;height:auto" id="sb-svg">
      <g id="sb-sattel"><path d="M100 60 H300 V240 H100 Z M164 92 V208 H262 V92 Z" fill="#213552" fill-rule="evenodd" stroke="#ecf1f8" stroke-width="4"/>
        <rect x="230" y="96" width="18" height="108" rx="3" fill="#ffd34d"/><rect x="248" y="96" width="12" height="108" fill="#ecf1f8"/>
        <text x="310" y="70" font-size="14" font-weight="800" fill="#94a4ba">Sattel</text></g>
      <rect x="198" y="20" width="26" height="260" rx="4" fill="#94a4ba"/><text x="211" y="296" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Bremsscheibe</text>
      <g id="sb-innen"><rect x="120" y="116" width="46" height="68" fill="#ff8f3f"/><rect x="166" y="96" width="12" height="108" fill="#ecf1f8"/><rect x="178" y="96" width="14" height="108" rx="3" fill="#ffd34d"/></g>
      <text x="20" y="155" font-size="14" font-weight="800" fill="#ff8f3f">Kolben</text>
      <text x="310" y="268" font-size="14" font-weight="800" fill="#ffd34d">Beläge</text>
    </svg>'''


bremse = [
    titel_folie(K, 'bar', 'Die Bremsanlage', 'Hydraulik, Scheiben- und Trommelbremse, Bremsflüssigkeit, Prüfen', 'font-size:96px'),
    lernziele(T, ['Wie eine hydraulische Bremsanlage aufgebaut ist', 'Wie aus deinem Fuß eine große Bremskraft wird',
                  'Wie Scheiben- und Trommelbremse arbeiten', 'Warum Bremsflüssigkeit gewechselt werden muss und wie du prüfst']),
    folie(T, 'Aufbau der Bremsanlage', '''    <div class="kette">
      <div class="glied step"><b>Bremspedal</b><span>Hebel verstärkt die Fußkraft</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Bremskraft­verstärker</b><span>hilft mit Unterdruck oder elektrisch</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Hauptbrems­zylinder</b><span>erzeugt den Druck – zwei Kreise</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Radbremsen</b><span>Bremssattel oder Radbremszylinder</span></div>
    </div>
    <div class="grid2" style="margin-top:18px">
      <div class="tip step"><b>Zwei Bremskreise</b>Fällt ein Kreis aus (z. B. undichte Leitung), bremst der andere noch – mit längerem Bremsweg. Aufteilung z. B. diagonal oder vorn/hinten.</div>
      <div class="tip step"><b>ABS/ESP-Hydraulik</b>Zwischen Hauptbremszylinder und Rädern sitzt das Hydraulikaggregat von ABS und ESP.</div>
    </div>'''),
    folie(T, 'Hydraulik – zum Ausprobieren', f'''    <div class="ctrl"><span style="width:300px;white-space:nowrap">Kraft Hauptzylinder: <span class="c" id="hy-fn">2.000 N</span></span><input type="range" id="hy-f" min="500" max="3000" step="100" value="2000"></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr;margin-top:8px">
      {hydr_svg()}
      <div>
        <div class="grid2" style="gap:10px"><div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">DRUCK (ÜBERALL GLEICH)</div><div class="lcd2" id="hy-pv" style="font-size:26px">53 bar</div></div>
        <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">KRAFT AM SATTELKOLBEN</div><div class="lcd2" id="hy-f2" style="font-size:26px">12.000 N</div></div></div>
        <div class="card" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px">Der Druck ist in der ganzen Flüssigkeit <span class="c">gleich</span>. Der Sattelkolben ist viel größer als der Kolben im Hauptzylinder (hier ca. 6-mal so viel Fläche) – darum ist die Kraft dort auch ca. 6-mal so groß.</div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Beispielwerte: Hauptzylinder Ø 22 mm (3,8 cm²), Sattelkolben Ø 54 mm (22,9 cm²). Druck = Kraft : Fläche.</p>''', sid='s-hy', body_cls='body noclick'),
    folie(T, 'Die Scheibenbremse – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px"><button class="btn ghost" id="sb-b">Bremse treten</button></div>
    <div class="grid2" style="align-items:center">
      {scheibe_svg()}
      <div class="card" id="sb-t" style="font-size:16px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Faustsattel, von oben gesehen, vereinfacht.</p>''', sid='s-sb', body_cls='body noclick'),
    folie(T, 'Trommelbremse und Feststellbremse', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Trommelbremse</div>
        <ul UL><li>der Radbremszylinder drückt zwei Bremsbacken von innen gegen die Trommel</li><li>oft hinten, gut als Feststellbremse</li><li>gekapselt, aber schlechtere Kühlung als die Scheibe</li><li>muss nachgestellt werden (meist automatisch)</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Elektrische Feststellbremse</div>
        <ul UL><li>ein Elektromotor am Sattel spannt die Bremse per Knopf</li><li>zum Belagwechsel mit dem Tester in die <b>Servicestellung</b> fahren</li><li>Kolben nie mit Gewalt zurückdrücken – der Antrieb geht kaputt</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Bremsflüssigkeit – zum Ausprobieren', '''    <div class="ctrl"><span style="width:280px">Wasser in der Flüssigkeit: <span class="c" id="bf-n">0,0 %</span></span><input type="range" id="bf" min="0" max="4" step="0.1" value="0"></div>
    <div class="grid2" style="align-items:center;margin-top:12px">
      <div class="card"><div class="muted" style="font-size:15px;font-weight:800">SIEDEPUNKT (DOT 4, CA.)</div><div class="lcd2" id="bf-v" style="font-size:34px;margin:6px 0">230 °C</div>
        <div style="height:22px;background:var(--card2);border-radius:11px;overflow:hidden"><div id="bf-bar" style="height:100%;width:100%;background:var(--grn);transition:width .2s,background .2s"></div></div></div>
      <div class="card" id="bf-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:8px 0 0">Richtwerte für DOT 4: neu mindestens 230 °C, mit ca. 3,7 % Wasser mindestens 155 °C. Wechselintervall laut Hersteller (oft alle 2 Jahre).</p>''', sid='s-bf', body_cls='body noclick'),
    folie(T, 'Entlüften', '''    <ol class="steps-list">
      <li class="step">Nur frische Bremsflüssigkeit<small>aus verschlossenem Gebinde, Sorte laut Hersteller (z. B. DOT 4)</small></li>
      <li class="step">Reihenfolge laut Hersteller<small>oft vom Rad, das am weitesten vom Hauptzylinder entfernt ist</small></li>
      <li class="step">Entlüftungsgerät oder zu zweit<small>so lange, bis klare Flüssigkeit ohne Blasen kommt</small></li>
      <li class="step">Behälter nie leer laufen lassen<small>sonst gelangt Luft ins System – bei ABS/ESP oft Entlüften mit dem Tester nötig</small></li>
      <li class="step">Pedal und Dichtheit prüfen<small>Pedal muss hart sein. Altflüssigkeit als Sondermüll entsorgen</small></li>
    </ol>'''),
    folie(T, 'Bremse prüfen', '''    <ol class="steps-list">
      <li class="step">Sichtprüfung<small>Leitungen und Schläuche dicht, nicht korrodiert oder rissig?</small></li>
      <li class="step">Beläge und Scheiben<small>Belagdicke und Scheibendicke messen – Mindestmaß laut Hersteller, bei Scheiben oft eingeschlagen („MIN TH“)</small></li>
      <li class="step">Bremsflüssigkeit<small>Stand am Behälter, Siedepunkt mit dem Prüfgerät</small></li>
      <li class="step">Bremsenprüfstand<small>Bremskraft und Unterschied links/rechts je Achse – Grenzwerte laut Prüfvorschrift</small></li>
      <li class="step">Probefahrt<small>zieht das Fahrzeug zur Seite? Rubbeln, Quietschen, Pedalweg?</small></li>
    </ol>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Achsweise</b>Beläge und Scheiben immer an beiden Rädern einer Achse erneuern.</div>
      <div class="warn step"><b>Vor der ersten Fahrt</b>Nach Arbeiten an der Bremse das Pedal mehrmals treten, bis es hart ist. Neue Beläge laut Hersteller einbremsen.</div>
      <div class="warn step"><b>Bremsstaub</b>Nicht mit Druckluft wegblasen – mit Bremsenreiniger reinigen. Keine Fette oder Öle an Beläge und Scheiben.</div>
      <div class="warn step"><b>Bremsflüssigkeit</b>ist giftig und greift Lack an. Spritzer sofort mit viel Wasser abwaschen.</div>
    </div>'''),
    video(T, 'fw-bremse'),
    kurztest(T, [
        ('Warum ist die Kraft am Sattelkolben größer als am Hauptzylinder?', ['Gleicher Druck, aber größere Kolbenfläche', 'Weil die Leitung länger ist', 'Weil die Flüssigkeit heißer ist'], 0, 'Kraft = Druck × Fläche.'),
        ('Warum muss Bremsflüssigkeit regelmäßig gewechselt werden?', ['Sie wird dicker', 'Sie nimmt Wasser auf, der Siedepunkt sinkt', 'Sie verdunstet'], 1, 'Bei starkem Bremsen können sonst Dampfblasen entstehen.'),
        ('Was passiert, wenn sich in der Bremsflüssigkeit Dampfblasen bilden?', ['Die Bremse wird stärker', 'Nichts', 'Das Pedal fällt durch, die Bremse wirkt kaum'], 2, 'Dampf lässt sich zusammendrücken – Flüssigkeit nicht.'),
        ('Was musst du beim Belagwechsel an einer elektrischen Feststellbremse beachten?', ['Erst mit dem Tester in die Servicestellung fahren', 'Kolben mit dem Hammer zurückschlagen', 'Batterie laden'], 0, 'Sonst wird der Antrieb am Sattel beschädigt.'),
    ]),
    merke(T, ['Hauptzylinder erzeugt Druck – zwei Bremskreise', 'Gleicher Druck, größere Fläche = größere Kraft',
              'Bremsflüssigkeit zieht Wasser – regelmäßig wechseln', 'Beläge und Scheiben achsweise, Mindestmaß laut Hersteller']),
]
bremse_js = '''<script>
(function () {
  const hf = document.getElementById('hy-f'), A1 = 3.8, A2 = 22.9;
  const pfeil = (x, y0, y1, c, w) => { const r = y1 > y0 ? -1 : 1; return '<line x1="' + x + '" y1="' + y0 + '" x2="' + x + '" y2="' + (y1 + r * 10) + '" stroke="' + c + '" stroke-width="' + w + '"/><path d="M' + (x - w * 1.8) + ' ' + (y1 + r * w * 2.2) + ' L' + x + ' ' + y1 + ' L' + (x + w * 1.8) + ' ' + (y1 + r * w * 2.2) + ' Z" fill="' + c + '"/>'; };
  function hy() {
    const F = +hf.value, p = F / A1 / 10, F2 = p * 10 * A2, k = (F - 500) / 2500;
    const ys = 110 + 50 * k, yb = 150 - 50 * k * 57 / 140;
    document.getElementById('hy-fn').textContent = F.toLocaleString('de-DE') + ' N';
    document.getElementById('hy-pv').textContent = Math.round(p) + ' bar';
    document.getElementById('hy-f2').textContent = (Math.round(F2 / 100) * 100).toLocaleString('de-DE') + ' N';
    document.getElementById('hy-p').textContent = 'p = ' + Math.round(p) + ' bar';
    document.getElementById('hy-fl').setAttribute('d', 'M79 ' + ys + ' V263 H501 V' + yb + ' H359 V229 H138 V' + ys + ' Z');
    document.getElementById('hy-k1').innerHTML = '<rect x="80" y="' + (ys - 18) + '" width="57" height="18" rx="3" fill="#94a4ba"/>' + pfeil(108, ys - 18 - (34 + 26 * k), ys - 20, '#ffd34d', 6);
    document.getElementById('hy-k2').innerHTML = '<rect x="360" y="' + (yb - 18) + '" width="140" height="18" rx="3" fill="#94a4ba"/>' + pfeil(430, yb - 20, yb - 20 - (40 + 60 * k), '#34c778', 12);
  }
  hf.addEventListener('input', hy); hy();

  let an = false;
  function sb() {
    document.getElementById('sb-innen').setAttribute('transform', an ? 'translate(6 0)' : '');
    document.getElementById('sb-sattel').setAttribute('transform', an ? 'translate(-6 0)' : '');
    document.getElementById('sb-b').textContent = an ? 'Bremse loslassen' : 'Bremse treten';
    document.getElementById('sb-b').classList.toggle('on', an);
    document.getElementById('sb-t').innerHTML = an
      ? '<b>Bremsen:</b> Der Druck schiebt den <span class="ora">Kolben</span> mit dem inneren Belag gegen die Scheibe. Der <span class="c">Sattel</span> ist beweglich gelagert und zieht dabei den äußeren Belag von der anderen Seite heran. Die Scheibe wird von beiden Seiten gebremst.'
      : '<b>Gelöst:</b> Die Beläge liegen fast ohne Kraft an der Scheibe. Beim Verschleiß rutscht der Kolben weiter heraus – die Scheibenbremse stellt sich selbst nach. Scheibenbremsen werden gut gekühlt.';
  }
  document.getElementById('sb-b').onclick = () => { an = !an; sb(); }; sb();

  const bf = document.getElementById('bf');
  function f() {
    const w = +bf.value, s = Math.round(230 - w * 20.3);
    document.getElementById('bf-n').textContent = w.toFixed(1).replace('.', ',') + ' %';
    document.getElementById('bf-v').textContent = s + ' °C';
    const bar = document.getElementById('bf-bar'); bar.style.width = Math.max(10, (s - 140) / 90 * 100) + '%';
    bar.style.background = w < 1.5 ? 'var(--grn)' : w < 3 ? 'var(--yel)' : 'var(--red)';
    document.getElementById('bf-t').innerHTML = w < 0.2 ? '<b class="grn">Neue Flüssigkeit:</b> hoher Siedepunkt. Aber Bremsflüssigkeit zieht Wasser aus der Luft an (sie ist hygroskopisch) – durch Schläuche und den Behälterdeckel.'
      : w < 3 ? '<b class="yel">Mit der Zeit:</b> Jedes Prozent Wasser senkt den Siedepunkt deutlich. Von außen sieht man das nicht – nur ein Prüfgerät zeigt es.'
      : '<b class="red">Gefährlich:</b> Bei langen Bergabfahrten wird die Bremse sehr heiß. Das Wasser verdampft, es bilden sich <span class="red">Dampfblasen</span>. Das Pedal fällt durch, die Bremse wirkt kaum noch. Bremsflüssigkeit wechseln!';
  }
  bf.addEventListener('input', f); f();
})();
</script>'''


# ================================================================ Assistenzsysteme
T = 'ASSISTENZ'


def esp_svg():
    return '''<svg viewBox="0 0 640 330" width="640" height="330" style="display:block;margin:0 auto;max-width:100%;height:auto" id="es-svg">
      <rect x="0" y="0" width="640" height="330" rx="12" fill="#18283f"/>
      <path d="M340 330 V250 A200 200 0 0 0 140 50 H60" fill="none" stroke="#213552" stroke-width="70"/>
      <path d="M340 330 V250 A200 200 0 0 0 140 50 H60" fill="none" stroke="#94a4ba" stroke-width="2" stroke-dasharray="10 10"/>
      <path id="es-ohne" d="" fill="none" stroke="#f05e4e" stroke-width="5"/>
      <path id="es-mit" d="" fill="none" stroke="#34c778" stroke-width="5"/>
      <text x="20" y="300" font-size="14" font-weight="800" fill="#f05e4e">ohne ESP</text><text x="20" y="320" font-size="14" font-weight="800" fill="#34c778">mit ESP</text>
      <g transform="translate(500 90)"><rect x="-40" y="-70" width="80" height="140" rx="22" fill="#213552" stroke="#ecf1f8" stroke-width="3"/>
        <rect class="es-r" data-r="vl" x="-56" y="-60" width="16" height="36" rx="4" fill="#94a4ba"/><rect class="es-r" data-r="vr" x="40" y="-60" width="16" height="36" rx="4" fill="#94a4ba"/>
        <rect class="es-r" data-r="hl" x="-56" y="24" width="16" height="36" rx="4" fill="#94a4ba"/><rect class="es-r" data-r="hr" x="40" y="24" width="16" height="36" rx="4" fill="#94a4ba"/>
        <path d="M0 -60 V-90 M-8 -80 L0 -92 L8 -80" fill="none" stroke="#94a4ba" stroke-width="3"/>
        <text x="0" y="104" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">ESP bremst</text></g>
      <text x="500" y="230" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Linkskurve</text>
    </svg>'''


def sens_svg():
    return '''<svg viewBox="0 0 640 260" width="640" height="260" style="display:block;margin:0 auto;max-width:100%;height:auto" id="sn-svg">
      <rect x="0" y="0" width="640" height="260" rx="12" fill="#18283f"/>
      <g class="sn-f" data-s="radar"><path d="M420 130 L635 90 L635 170 Z" fill="#5b8cff" opacity=".35"/></g>
      <g class="sn-f" data-s="kamera"><path d="M360 130 L600 40 L600 220 Z" fill="#34c778" opacity=".3"/></g>
      <g class="sn-f" data-s="us"><path d="M420 85 A60 60 0 0 1 420 175 Z M200 85 A60 60 0 0 0 200 175 Z" fill="#ff8f3f" opacity=".4"/><path d="M425 90 Q490 130 425 170 M195 90 Q130 130 195 170" fill="#ff8f3f" opacity=".4"/></g>
      <g class="sn-f" data-s="seite"><path d="M210 95 L60 20 L40 70 Z M210 165 L60 240 L40 190 Z" fill="#a07cf5" opacity=".35"/></g>
      <rect x="200" y="90" width="220" height="80" rx="26" fill="#213552" stroke="#ecf1f8" stroke-width="3"/>
      <rect x="330" y="100" width="34" height="60" rx="6" fill="#18283f" stroke="#94a4ba" stroke-width="2"/>
      <path d="M440 130 H470 M460 122 L472 130 L460 138" fill="none" stroke="#94a4ba" stroke-width="3"/>
    </svg>'''


assistenz = [
    titel_folie(K, 'ABS', 'Fahrerassistenzsysteme', 'ABS, ESP, Radar, Kamera und Kalibrieren', 'font-size:90px'),
    lernziele(T, ['Wie ABS und ESP arbeiten', 'Welche Sensoren Assistenzsysteme nutzen',
                  'Was ACC, Notbremse und Spurhalteassistent machen', 'Wann Sensoren kalibriert werden müssen']),
    folie(T, 'ABS – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px">{btns('a', [('ohne', 'Vollbremsung ohne ABS'), ('mit', 'Vollbremsung mit ABS')])}</div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {grafik('ab', 600, 250)}
      <div class="card" id="ab-t" style="font-size:16px;font-weight:600;line-height:1.5"></div>
    </div>''', sid='s-ab', body_cls='body noclick'),
    folie(T, 'Aufbau von ABS und ESP', '''    <div class="values">
      <div class="val step from-left"><b>Raddrehzahl­sensoren</b><span>an jedem Rad – meist aktive Sensoren mit Magnetring im Radlager</span></div>
      <div class="val step from-left"><b>Hydraulik­aggregat</b><span>Ventile und Pumpe: Druck halten, abbauen, wieder aufbauen</span></div>
      <div class="val step from-left"><b>Steuergerät</b><span>vergleicht die Raddrehzahlen und steuert die Ventile</span></div>
      <div class="val step from-left"><b>nur bei ESP</b><span>Lenkwinkelsensor, Drehratensensor, Querbeschleunigung, Bremsdruck</span></div>
    </div>'''),
    folie(T, 'ESP – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px">{btns('e', [('unter', 'Untersteuern'), ('ueber', 'Übersteuern')])}</div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {esp_svg()}
      <div class="card" id="es-t" style="font-size:16px;font-weight:600;line-height:1.5"></div>
    </div>''', sid='s-es', body_cls='body noclick'),
    folie(T, 'Die Sensoren – zum Antippen', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap">{btns('s', [('radar', 'Radar'), ('kamera', 'Kamera'), ('us', 'Ultraschall'), ('seite', 'Radar seitlich/hinten')])}</div>
    {sens_svg()}
    <div class="card" id="sn-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:8px"></div>''', sid='s-sn', body_cls='body noclick'),
    folie(T, 'Wichtige Assistenzsysteme', '''    <div class="values">
      <div class="val step from-left"><b>ACC</b><span>Abstandsregeltempomat – hält Tempo und Abstand zum Vorderfahrzeug</span></div>
      <div class="val step from-left"><b>Notbrems­assistent</b><span>warnt und bremst selbst, wenn ein Aufprall droht</span></div>
      <div class="val step from-left"><b>Spurhalte­assistent</b><span>erkennt die Fahrspur und lenkt sanft zurück</span></div>
      <div class="val step from-left"><b>Totwinkel­warner</b><span>warnt beim Spurwechsel vor Fahrzeugen neben dir</span></div>
      <div class="val step from-left"><b>Einparkhilfe</b><span>Ultraschall piept – oder das Auto lenkt selbst ein</span></div>
    </div>
    <div class="note step">Assistenzsysteme helfen – verantwortlich bleibt immer der Fahrer.</div>'''),
    folie(T, 'Kalibrieren – wann und wie?', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Wann?</div>
        <ul UL><li>nach dem Tausch der Frontscheibe (Kamera)</li><li>nach Achsvermessung oder Arbeiten am Fahrwerk</li><li>nach Aus- und Einbau oder Tausch von Radar, Kamera oder Stoßfänger</li><li>nach einem Unfall</li><li>immer laut Hersteller</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Wie?</div>
        <ul UL><li><b>statisch</b>: mit Kalibriertafel in der Werkstatt – ebener Boden, genauer Abstand, gute Beleuchtung</li><li><b>dynamisch</b>: auf einer Probefahrt nach Vorgabe des Testers</li></ul></div>
    </div>
    <div class="warn step" style="margin-top:12px"><b>Reihenfolge</b>Erst die Achsvermessung, dann die Kalibrierung – die Sensoren richten sich nach der Fahrachse aus.</div>'''.replace('UL', UL)),
    folie(T, 'ABS und ESP prüfen', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher lesen<small>welches Rad, welcher Sensor?</small></li>
      <li class="step">Raddrehzahlen im Messwertblock vergleichen<small>bei Geradeausfahrt müssen alle vier gleich sein</small></li>
      <li class="step">Aktiven Sensor richtig prüfen<small>Versorgung und Signal mit Oszilloskop oder Messwerten – nie mit dem Ohmmeter</small></li>
      <li class="step">Magnetring und Geberrad<small>verschmutzt, beschädigt oder falsch eingebaut (Radlager)?</small></li>
      <li class="step">Nach Arbeiten an Lenkung oder Fahrwerk<small>Lenkwinkelsensor neu einstellen</small></li>
    </ol>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>ABS-Leuchte an</b>Die Bremse funktioniert noch – aber ohne ABS. Fahrzeug bald prüfen.</div>
      <div class="tip step"><b>Reifen gleich groß</b>Verschiedene Reifengrößen oder stark unterschiedliches Profil können ABS- und ESP-Fehler auslösen.</div>
      <div class="tip step"><b>Sensoren sauber</b>Schnee, Schmutz oder Aufkleber vor Radar und Kamera stören die Systeme.</div>
      <div class="warn step"><b>Stoßfänger lackieren</b>Vor dem Radar nur nach Herstellervorgabe lackieren – falsche Lackschichten stören das Radar.</div>
    </div>'''),
    video(T, 'fw-assistenz'),
    kurztest(T, [
        ('Was verhindert ABS?', ['Dass die Räder beim Bremsen blockieren', 'Dass der Motor ausgeht', 'Dass die Reifen verschleißen'], 0, 'So bleibt das Fahrzeug lenkbar.'),
        ('Das Fahrzeug untersteuert in einer Linkskurve. Welches Rad bremst ESP?', ['Vorne rechts', 'Hinten rechts', 'Hinten links (kurveninnen)'], 2, 'Das dreht das Fahrzeug in die Kurve hinein.'),
        ('Welcher Sensor misst beim ACC den Abstand zum Vorderfahrzeug?', ['Ultraschall', 'Radar', 'Lenkwinkelsensor'], 1, 'Radar misst Abstand und Geschwindigkeit – auch bei Nebel.'),
        ('Was kommt zuerst?', ['Erst die Achsvermessung, dann die Kalibrierung', 'Erst kalibrieren, dann vermessen', 'Egal'], 0, 'Die Sensoren richten sich nach der Fahrachse aus.'),
    ]),
    merke(T, ['ABS: Räder blockieren nicht – lenkbar bleiben', 'ESP: bremst einzelne Räder gegen Schleudern',
              'Radar, Kamera, Ultraschall – sauber halten', 'Nach Scheibe, Fahrwerk, Unfall: kalibrieren laut Hersteller']),
]
assistenz_js = '''<script>
(function () {
  const g = (id, s) => document.getElementById(id).innerHTML = s;
  let am = 'ohne', t0 = null, raf = null;
  const X = t => 40 + t / 5 * 540, Y = v => 210 - v * 1.6;
  function fz(t) { const T = am === 'ohne' ? 4.6 : 3.7; return t >= T ? 0 : 100 * (1 - t / T); }
  function rd(t) {
    if (am === 'ohne') return t < 0.5 ? 100 * (1 - t / 0.5 * 0.15) * (1 - t / 0.5) + fz(t) * 0 + (t < 0.5 ? 0 : 0) : 0;
    const v = fz(t); if (v <= 0) return 0;
    const ph = (t * 6) % 1; return v * (0.88 - 0.22 * (ph < 0.5 ? ph * 2 : 2 - ph * 2));
  }
  function bild(tm) {
    let o = '';
    for (let v = 0; v <= 100; v += 25) o += '<line x1="40" y1="' + Y(v) + '" x2="580" y2="' + Y(v) + '" stroke="#94a4ba" stroke-width="1" opacity=".2"/>';
    o += '<text x="44" y="22" font-size="14" font-weight="800" fill="#94a4ba">Geschwindigkeit</text><text x="580" y="240" text-anchor="end" font-size="13" font-weight="800" fill="#94a4ba">Zeit →</text>';
    let a = '', b = '';
    for (let t = 0; t <= Math.min(tm, 5); t += 0.02) { a += (a ? ' L' : 'M') + X(t).toFixed(1) + ' ' + Y(fz(t)).toFixed(1); b += (b ? ' L' : 'M') + X(t).toFixed(1) + ' ' + Y(am === 'ohne' ? (t < 0.5 ? 100 * (1 - t / 0.5) : 0) : rd(t)).toFixed(1); }
    o += '<path d="' + a + '" fill="none" stroke="#ecf1f8" stroke-width="4"/><path d="' + b + '" fill="none" stroke="#ffd34d" stroke-width="4"/>';
    o += '<text x="420" y="22" font-size="14" font-weight="800" fill="#ecf1f8">Fahrzeug</text><text x="510" y="22" font-size="14" font-weight="800" fill="#ffd34d">Rad</text>';
    g('ab-g', o);
  }
  function lauf(ts) { if (t0 === null) t0 = ts; const t = (ts - t0) / 1000 * 1.4; bild(t); if (t < 5) raf = requestAnimationFrame(lauf); }
  const TX = {
    ohne: '<b class="red">Ohne ABS:</b> Das Rad <span class="red">blockiert</span> nach kurzer Zeit (gelbe Linie fällt auf 0). Ein blockiertes Rad kann keine Seitenkräfte übertragen – das Fahrzeug <b>lässt sich nicht mehr lenken</b> und rutscht geradeaus.',
    mit: '<b class="grn">Mit ABS:</b> Das Steuergerät erkennt, dass ein Rad blockieren will. Es baut den Druck kurz ab, hält ihn und baut ihn wieder auf – mehrmals pro Sekunde. Das Rad dreht weiter (gelbe Linie knapp unter dem Fahrzeug): Das Fahrzeug <b>bleibt lenkbar</b>. Das Pedal pulsiert dabei.'
  };
  const ab = document.querySelectorAll('#s-ab [data-a]');
  function abs(m) { am = m; ab.forEach(b => b.classList.toggle('on', b.dataset.a === m)); document.getElementById('ab-t').innerHTML = TX[m]; cancelAnimationFrame(raf); t0 = null; raf = requestAnimationFrame(lauf); }
  ab.forEach(b => b.onclick = () => abs(b.dataset.a)); abs('ohne');
  document.getElementById('s-ab').addEventListener('slideshow', () => abs(am));

  const ES = {
    unter: { r: 'hl', ohne: 'M340 330 V250 Q330 120 270 20', mit: 'M340 330 V250 A200 200 0 0 0 150 52',
      t: '<b>Untersteuern:</b> Das Fahrzeug schiebt über die Vorderräder nach außen – es fährt eine größere Kurve als gelenkt. ESP bremst das <span class="c">kurveninnere Hinterrad</span> (hier hinten links). Das dreht das Fahrzeug in die Kurve hinein.' },
    ueber: { r: 'vr', ohne: 'M340 330 V250 Q320 150 230 170 Q190 180 200 230', mit: 'M340 330 V250 A200 200 0 0 0 150 52',
      t: '<b>Übersteuern:</b> Das Heck bricht aus, das Fahrzeug dreht sich zu stark ein und kann schleudern. ESP bremst das <span class="c">kurvenäußere Vorderrad</span> (hier vorne rechts). Das stabilisiert das Fahrzeug.' }
  };
  const eb = document.querySelectorAll('#s-es [data-e]');
  function esp(m) {
    const e = ES[m];
    document.getElementById('es-ohne').setAttribute('d', e.ohne); document.getElementById('es-mit').setAttribute('d', e.mit);
    document.querySelectorAll('#es-svg .es-r').forEach(r => r.setAttribute('fill', r.dataset.r === e.r ? '#f05e4e' : '#94a4ba'));
    document.getElementById('es-t').innerHTML = e.t;
    eb.forEach(b => b.classList.toggle('on', b.dataset.e === m));
  }
  eb.forEach(b => b.onclick = () => esp(b.dataset.e)); esp('unter');

  const SN = {
    radar: '<b>Radar (vorn):</b> misst Abstand und Geschwindigkeit des Vorderfahrzeugs – auch bei Dunkelheit und Nebel. Für ACC und Notbremsassistent. Sitzt hinter dem Emblem oder im Stoßfänger.',
    kamera: '<b>Kamera (an der Frontscheibe):</b> erkennt Fahrspuren, Verkehrszeichen, Fußgänger und Fahrzeuge. Für Spurhalteassistent, Verkehrszeichenerkennung und Notbremse.',
    us: '<b>Ultraschall (in den Stoßfängern):</b> misst kurze Abstände beim Einparken – bis wenige Meter.',
    seite: '<b>Radar seitlich/hinten:</b> überwacht den toten Winkel und den Verkehr von hinten – für Totwinkelwarner und Spurwechselassistent.'
  };
  const sb = document.querySelectorAll('#s-sn [data-s]');
  function sn(k) {
    document.querySelectorAll('#sn-svg .sn-f').forEach(f => f.style.display = f.dataset.s === k ? '' : 'none');
    document.getElementById('sn-t').innerHTML = SN[k];
    sb.forEach(b => b.classList.toggle('on', b.dataset.s === k));
  }
  sb.forEach(b => b.onclick = () => sn(b.dataset.s)); sn('radar');
})();
</script>'''


if __name__ == '__main__':
    seite('fw-fahrwerk.html', 'Das Fahrwerk – Fahrwerk', 't-fw1', 'Fahrwerk', fahrwerk, STYLE, fahrwerk_js)
    seite('fw-bremse.html', 'Die Bremsanlage – Bremsanlage', 't-fw2', 'Bremsanlage', bremse, STYLE, bremse_js)
    seite('fw-assistenz.html', 'Fahrerassistenzsysteme', 't-fw3', 'Fahrerassistenzsysteme', assistenz, STYLE, assistenz_js)
    print('ok')
