"""Motormanagement: Abgas – drei Präsentationen.
Aufruf: cd tools && python3 mm_abgas.py"""
from praesentation_bauen import *

THEMA = 'Motormanagement: Abgas'
K = 'MOTORMANAGEMENT · ABGAS'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'


def kurve_svg(id_, h=240, mid=None):
    return f'''<svg viewBox="0 0 560 {h}" width="540" height="{h - 8}" style="display:block;margin:0 auto">
  <line x1="40" y1="{h - 30}" x2="550" y2="{h - 30}" stroke="#94a4ba" stroke-width="2"/>
  <line x1="40" y1="20" x2="40" y2="{h - 30}" stroke="#94a4ba" stroke-width="2"/>
  <text x="34" y="{h - 30 - 18 + 5}" text-anchor="end" font-size="13" font-weight="700" fill="#94a4ba">0,1</text>
  <text x="34" y="{h - 30 - 160 + 5}" text-anchor="end" font-size="13" font-weight="700" fill="#94a4ba">0,9</text>
  <text x="34" y="{h - 30 - 80 + 5}" text-anchor="end" font-size="13" font-weight="700" fill="#94a4ba">0,45</text>
  <line x1="40" y1="{h - 30 - 80}" x2="550" y2="{h - 30 - 80}" stroke="#94a4ba" stroke-width="1" stroke-dasharray="5 6"/>
  <text x="50" y="16" font-size="13" font-weight="700" fill="#94a4ba">Spannung in V</text>
  {mid or ''}
  <path id="{id_}" d="" fill="none" stroke="#34c778" stroke-width="4" stroke-linejoin="round"/>
</svg>'''

# ---------------------------------------------------------------- Lambdasonde
T = 'LAMBDASONDE'
lambdas = [
    titel_folie(K, 'λ', 'Lambdasonde', 'Schadstoffe, Lambdasonden und Lambda-Regelung'),
    lernziele(T, ['Welche Schadstoffe im Abgas sind', 'Wo die Lambdasonden sitzen und was sie messen',
                  'Sprungsonde und Breitbandsonde', 'Wie die Lambda-Regelung arbeitet und wie du prüfst']),
    folie(T, 'Was ist im Abgas?', '''    <div class="grid2" style="align-items:start">
      <div class="card step" style="border-top:4px solid var(--red)"><div class="big" style="font-size:22px">Schadstoffe</div>
        <ul UL><li><b>CO</b> – Kohlenmonoxid, giftig</li><li><b>HC</b> – unverbrannte Kohlenwasserstoffe</li><li><b>NOx</b> – Stickoxide</li><li><b>Partikel</b> – Ruß</li></ul></div>
      <div class="card step" style="border-top:4px solid var(--grn)"><div class="big" style="font-size:22px">Ungiftig</div>
        <ul UL><li><b>N₂</b> – Stickstoff (aus der Luft)</li><li><b>H₂O</b> – Wasserdampf</li><li><b>CO₂</b> – Kohlendioxid: nicht giftig, aber klimaschädlich</li></ul></div>
    </div>
    <div class="warn step" style="margin-top:14px"><b>Kohlenmonoxid</b>Unsichtbar, ohne Geruch und tödlich. Motor in der Werkstatt nur mit Abgasabsaugung laufen lassen.</div>'''.replace('UL', UL)),
    folie(T, 'Wo sitzen die Lambdasonden?', '''    <div class="kette">
      <div class="glied step"><b>Motor</b><span>Abgas mit Restsauerstoff</span></div><div class="flow-arrow step"></div>
      <div class="glied step" style="border-top-color:var(--grn)"><b>Sonde vor Kat</b><span>Regelsonde: misst das Gemisch</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Katalysator</b><span>reinigt das Abgas</span></div><div class="flow-arrow step"></div>
      <div class="glied step" style="border-top-color:var(--grn)"><b>Sonde nach Kat</b><span>Diagnosesonde: überwacht den Kat</span></div>
    </div>
    <div class="tip step" style="margin-top:18px"><b>Was misst die Sonde?</b>Den Restsauerstoff im Abgas. Daraus erkennt das Steuergerät, ob das Gemisch fett (zu wenig Luft) oder mager (zu viel Luft) war.</div>'''),
    folie(T, 'Sprungsonde und Breitbandsonde', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Sprungsonde</div>
        <ul UL><li>erzeugt selbst eine Spannung</li><li>mager: ca. 0,1 V – fett: ca. 0,8–0,9 V</li><li>springt genau bei Lambda = 1</li><li>zeigt nur „fett“ oder „mager“, nicht wie viel</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Breitbandsonde</div>
        <ul UL><li>misst den genauen Lambda-Wert, z. B. 0,92 oder 1,30</li><li>auch für Diesel und Magerbetrieb</li><li>Auswertung im Steuergerät</li><li>im Diagnosegerät als Lambda-Wert ablesen</li></ul></div>
      <div class="tip step" style="grid-column:1/-1"><b>Beide brauchen Hitze</b>Erst ab ca. 300 °C arbeiten sie richtig (Richtwert). Darum sind sie elektrisch beheizt – sonst würde die Regelung lange nach dem Kaltstart nicht arbeiten.</div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Lambda-Regelung – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-m="0">Regelung in Ordnung</button><button class="btn ghost" data-m="1">Falschluft</button><button class="btn ghost" data-m="2">Sonde gealtert</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {kurve_svg('lr-k')}
      <div>
        <div class="card"><div class="muted" style="font-size:15px;font-weight:800">KORREKTUR EINSPRITZMENGE</div><div class="lcd2" id="lr-v" style="font-size:32px;margin-top:6px">0 %</div></div>
        <div class="card" id="lr-t" style="margin-top:12px;font-size:17px;font-weight:600;line-height:1.5"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Sprungsonde vor Kat, vereinfacht. Beispielwerte.</p>''', sid='s-lr', body_cls='body noclick'),
    folie(T, 'Korrekturwerte im Diagnosegerät', '''    <div class="values">
      <div class="val step from-left"><b>Kurzzeit</b><span>schnelle Korrektur der Lambda-Regelung – schwankt ständig um 0 %</span></div>
      <div class="val step from-left"><b>Langzeit</b><span>Adaption: was sich das Steuergerät dauerhaft gemerkt hat</span></div>
      <div class="val step from-left"><b>nahe 0 %</b><span>gut – Gemischbildung in Ordnung</span></div>
      <div class="val step from-left"><b>z. B. über ±10 %</b><span>auffällig: Falschluft, Kraftstoffdruck, Einspritzventile, Luftmassenmesser prüfen</span></div>
    </div>
    <div class="note step">Plus = Steuergerät spritzt mehr ein (Gemisch war mager). Minus = weniger (war fett). Richtwerte – Grenzen laut Hersteller.</div>'''),
    folie(T, 'Lambdasonde prüfen', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher und Messwerte lesen<small>Lambda-Wert, Sondenspannung, Korrekturwerte – bei warmem Motor</small></li>
      <li class="step">Sprungsonde mit dem Oszilloskop<small>Signal muss gleichmäßig zwischen ca. 0,1 und 0,8 V wechseln – am Prüfadapter abgreifen</small></li>
      <li class="step">Sondenheizung prüfen<small>Heizwiderstand spannungsfrei messen oder Heizstrom mit der Stromzange – Werte laut Hersteller</small></li>
      <li class="step">Vor dem Tausch: Ursache suchen<small>Falschluft vor der Sonde (Krümmer undicht) täuscht ein mageres Gemisch vor</small></li>
    </ol>
    <div class="warn step" style="margin-top:6px"><b>Signalleitung nicht belasten</b>Keine Prüflampe, kein Ohmmeter an der Signalleitung – die Sonde erzeugt selbst eine kleine Spannung. Breitbandsonden nur mit dem Diagnosegerät prüfen.</div>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Einbau</b>Gewinde nur mit der Spezialpaste, die der Sonde beiliegt. Kein Kupferfett auf den Sondenkopf.</div>
      <div class="tip step"><b>Silikon</b>Silikonhaltige Dichtmittel am Motor können die Sonde vergiften.</div>
      <div class="warn step"><b>Undichter Krümmer</b>Angesaugte Falschluft vor der Sonde: Sie meldet „mager“, das Steuergerät fettet an – hoher Verbrauch, Fehlerspeicher.</div>
      <div class="tip step"><b>Kabel</b>Sondenkabel nicht knicken und nicht an heiße Teile legen – über das Kabel bekommt die Sonde Referenzluft.</div>
    </div>'''),
    video(T, 'mm-abgas-lambda'),
    kurztest(T, [
        ('Was misst die Lambdasonde?', ['Den Restsauerstoff im Abgas', 'Die Abgastemperatur', 'Den Abgasdruck'], 0, 'Daraus erkennt das Steuergerät, ob das Gemisch fett oder mager war.'),
        ('Welche Spannung liefert eine Sprungsonde bei fettem Gemisch etwa?', ['ca. 0,1 V', 'ca. 0,8–0,9 V', 'ca. 12 V'], 1, 'Fett = hohe Spannung, mager = ca. 0,1 V.'),
        ('Wozu dient die Lambdasonde nach dem Katalysator?', ['Sie regelt das Gemisch', 'Sie heizt den Kat', 'Sie überwacht den Katalysator'], 2, 'Sie ist die Diagnosesonde für den Kat.'),
        ('Die Langzeitkorrektur steht bei +18 %. Was ist eine mögliche Ursache?', ['Falschluft – das Gemisch war zu mager', 'Alles in Ordnung', 'Zu fettes Gemisch'], 0, 'Plus heißt: Das Steuergerät muss mehr einspritzen – oft wegen Falschluft.'),
    ]),
    merke(T, ['Schadstoffe: CO, HC, NOx, Ruß', 'Sonde vor Kat regelt, nach Kat überwacht',
              'Sprungsonde: mager 0,1 V, fett 0,8–0,9 V|springt bei Lambda = 1', 'Korrekturwerte nahe 0 % sind gut']),
]
lambdas_js = '''<script>
(function () {
  const H = 240, Y = v => H - 30 - (v - 0.0) * 200, N = 255;
  let mode = 0, buf = [], tt = 0, korr = 0;
  const bt = document.querySelectorAll('#s-lr [data-m]');
  const TX = [
    '<b class="grn">In Ordnung:</b> Das Signal wechselt gleichmäßig zwischen mager und fett. Das Steuergerät korrigiert ständig ein wenig – Lambda bleibt im Mittel bei 1.',
    '<b class="ora">Falschluft:</b> Die Sonde meldet dauernd „mager“. Das Steuergerät spritzt immer mehr ein, bis es an die Grenze kommt – Eintrag im Fehlerspeicher.',
    '<b class="ora">Sonde gealtert:</b> Das Signal wechselt langsam und schwach. Die Regelung wird ungenau – Verbrauch und Abgaswerte steigen.'
  ];
  function setm(m) { mode = m; buf = []; korr = 0; bt.forEach(x => x.classList.toggle('on', +x.dataset.m === m)); document.getElementById('lr-t').innerHTML = TX[m]; }
  bt.forEach(x => x.onclick = () => setm(+x.dataset.m));
  setm(0);
  setInterval(() => {
    tt += 0.05; let v, k;
    if (mode === 0) { const s = Math.tanh(5 * Math.sin(tt * 2 * Math.PI * 1.0)); v = 0.47 + 0.37 * s; k = -3 * s; korr = k; }
    else if (mode === 1) { korr = Math.min(25, korr + 0.35); v = 0.1 + 0.03 * Math.sin(tt * 9) + (korr >= 25 ? 0 : 0); k = korr; }
    else { const s = Math.sin(tt * 2 * Math.PI * 0.3); v = 0.45 + 0.17 * s; k = -6 * s; korr = k; }
    buf.push(v); if (buf.length > N) buf.shift();
    let d = ''; buf.forEach((b, i) => d += (i ? ' L' : 'M') + (40 + i * 2).toFixed(0) + ' ' + Y(b).toFixed(1));
    document.getElementById('lr-k').setAttribute('d', d);
    document.getElementById('lr-v').textContent = (k > 0 ? '+' : '') + k.toFixed(0) + ' %' + (mode === 1 && korr >= 25 ? '  Grenze!' : '');
  }, 50);
})();
</script>'''

# ---------------------------------------------------------------- Katalysator
T = 'KATALYSATOR'
kat = [
    titel_folie(K, 'KAT', 'Katalysator', 'Dreiwege-Kat, Lambdafenster und Überwachung', 'font-size:72px'),
    lernziele(T, ['Was der Dreiwege-Katalysator macht', 'Warum er Lambda = 1 braucht',
                  'Ab welcher Temperatur er arbeitet', 'Wie er überwacht wird und was ihn zerstört']),
    folie(T, 'Der Dreiwege-Katalysator', '''    <div class="values">
      <div class="val step from-left"><b>CO → CO₂</b><span>giftiges Kohlenmonoxid wird zu Kohlendioxid</span></div>
      <div class="val step from-left"><b>HC → CO₂ + H₂O</b><span>unverbrannter Kraftstoff wird zu Kohlendioxid und Wasser</span></div>
      <div class="val step from-left"><b>NOx → N₂</b><span>Stickoxide werden zu Stickstoff</span></div>
    </div>
    <div class="tip step" style="margin-top:14px"><b>Wie geht das?</b>Im Kat steckt ein Wabenkörper mit einer dünnen Schicht aus Edelmetallen (Platin, Palladium, Rhodium). An ihr laufen die Umwandlungen ab – der Kat selbst verbraucht sich dabei nicht.</div>'''),
    folie(T, 'Das Lambdafenster – zum Ausprobieren', '''    <div class="ctrl"><span style="width:240px">Lambda: <span class="c" id="lf-v">1,00</span></span><input type="range" id="lf" min="0.9" max="1.1" step="0.005" value="1"></div>
    <div class="grid2" style="margin-top:16px;align-items:center">
      <div class="card" id="lf-bars"></div>
      <div class="card" id="lf-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Umwandlung der Schadstoffe im warmen Kat. Vereinfacht, Beispielwerte.</p>''', sid='s-lf', body_cls='body noclick'),
    folie(T, 'Temperatur', '''    <div class="values">
      <div class="val step from-left"><b>unter ca. 250 °C</b><span>kalt – der Kat arbeitet kaum (Kaltstart!)</span></div>
      <div class="val step from-left"><b>ca. 400–800 °C</b><span>bester Bereich</span></div>
      <div class="val step from-left"><b>über ca. 1.000 °C</b><span>der Kat wird zerstört – z. B. durch Zündaussetzer</span></div>
    </div>
    <div class="note step">Richtwerte. Darum heizt das Steuergerät den Kat nach dem Kaltstart schnell auf (z. B. spätere Zündung).</div>'''),
    folie(T, 'Kat-Überwachung – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-k="0">Kat in Ordnung</button><button class="btn ghost" data-k="1">Kat verbraucht</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      <svg viewBox="0 0 560 260" width="540" height="252" style="display:block;margin:0 auto">
        <text x="40" y="22" font-size="14" font-weight="800" fill="#94a4ba">Sonde vor Kat</text>
        <path id="ku-v" d="" fill="none" stroke="#34c778" stroke-width="4"/>
        <line x1="40" y1="128" x2="550" y2="128" stroke="#94a4ba" stroke-width="1" stroke-dasharray="5 6"/>
        <text x="40" y="152" font-size="14" font-weight="800" fill="#94a4ba">Sonde nach Kat</text>
        <path id="ku-h" d="" fill="none" stroke="#ff8f3f" stroke-width="4"/>
      </svg>
      <div class="card" id="ku-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>''', sid='s-ku', body_cls='body noclick'),
    folie(T, 'Was den Kat zerstört', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Zündaussetzer</b>Unverbrannter Kraftstoff verbrennt im Kat – er überhitzt und schmilzt.</div>
      <div class="warn step"><b>Öl und Kühlmittel</b>Ölverbrauch oder defekte Zylinderkopfdichtung überziehen die Edelmetallschicht.</div>
      <div class="warn step"><b>Mechanisch</b>Aufsetzen, Steinschlag oder Anschleppen – der Keramikkörper bricht und klappert.</div>
      <div class="tip step"><b>Vor dem Tausch</b>Immer die Ursache finden und beheben – sonst ist der neue Kat schnell wieder kaputt.</div>
    </div>'''),
    folie(T, 'Aus der Praxis', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher: „Wirkungsgrad Katalysator zu niedrig“<small>erst Sonde nach Kat, Abgasanlage auf Undichtigkeit und Aussetzer prüfen</small></li>
      <li class="step">Abgasuntersuchung (AU)<small>Lambda und CO werden gemessen, dazu die OBD-Daten – Werte laut Vorgabe</small></li>
      <li class="step">Klappern beim Gasgeben oder Abstellen<small>Hinweis auf gebrochenen Keramikkörper</small></li>
      <li class="step">Nach Unfall oder Aufsetzen<small>Kat und Abgasanlage auf Beschädigung prüfen</small></li>
    </ol>'''),
    video(T, 'mm-abgas-kat'),
    kurztest(T, [
        ('Was macht der Dreiwege-Katalysator aus Stickoxiden (NOx)?', ['Kohlendioxid', 'Stickstoff', 'Ruß'], 1, 'NOx wird zu Stickstoff (N₂).'),
        ('Bei welchem Lambda reinigt der Dreiwege-Kat alle drei Schadstoffe gut?', ['Lambda = 1', 'Lambda = 0,8', 'Lambda = 1,3'], 0, 'Nur im engen Lambdafenster um 1.'),
        ('Wie überwacht das Steuergerät den Kat?', ['Mit einem Temperatursensor im Innenraum', 'Über die Drehzahl', 'Es vergleicht die Sonden vor und nach dem Kat'], 2, 'Bei gutem Kat ist das Signal nach dem Kat ruhig.'),
        ('Was kann den Kat durch Überhitzung zerstören?', ['Zu viel Reifendruck', 'Zündaussetzer', 'Eine volle Batterie'], 1, 'Unverbrannter Kraftstoff verbrennt im Kat.'),
    ]),
    merke(T, ['CO, HC und NOx werden umgewandelt', 'Funktioniert nur bei Lambda = 1',
              'Arbeitet erst warm – ab ca. 250 °C', 'Sonde nach Kat ruhig = Kat gut|Aussetzer zerstören den Kat']),
]
kat_js = '''<script>
(function () {
  const lf = document.getElementById('lf');
  const c = (x) => Math.max(5, Math.min(98, x));
  function f() {
    const l = +lf.value;
    const co = c(l < 1 ? 98 - (1 - l) * 900 : 98), hc = c(l < 1 ? 96 - (1 - l) * 700 : 96), nox = c(l > 1 ? 97 - (l - 1) * 1100 : 97);
    document.getElementById('lf-v').textContent = l.toFixed(2).replace('.', ',');
    const bar = (n, v, col) => '<div style="font-weight:800;margin:10px 0 6px">' + n + ' <span class="muted">' + Math.round(v) + ' %</span></div><div style="height:20px;background:var(--card2);border-radius:8px;overflow:hidden"><div style="height:100%;width:' + v + '%;background:' + col + '"></div></div>';
    document.getElementById('lf-bars').innerHTML = bar('CO', co, 'var(--grn)') + bar('HC', hc, 'var(--grn)') + bar('NOx', nox, 'var(--grn)');
    let t;
    if (l < 0.985) t = '<b class="ora">Zu fett:</b> Es fehlt Sauerstoff – CO und HC werden nicht mehr richtig umgewandelt.';
    else if (l <= 1.015) t = '<b class="grn">Lambdafenster:</b> Alle drei Schadstoffe werden gut umgewandelt. Darum regelt der Benziner auf Lambda = 1.';
    else t = '<b class="ora">Zu mager:</b> Zu viel Sauerstoff – die Stickoxide (NOx) werden nicht mehr umgewandelt.';
    document.getElementById('lf-t').innerHTML = t;
  }
  lf.addEventListener('input', f); f();

  const kb = document.querySelectorAll('#s-ku [data-k]');
  function k(i) {
    let dv = '', dh = '';
    for (let x = 0; x <= 510; x += 3) {
      const s = Math.tanh(5 * Math.sin(x / 510 * 2 * Math.PI * 4));
      dv += (x ? ' L' : 'M') + (40 + x) + ' ' + (75 - 40 * s).toFixed(1);
      const h = i ? 205 - 38 * Math.tanh(5 * Math.sin((x - 18) / 510 * 2 * Math.PI * 4)) : 190 + 3 * Math.sin(x / 40);
      dh += (x ? ' L' : 'M') + (40 + x) + ' ' + h.toFixed(1);
    }
    document.getElementById('ku-v').setAttribute('d', dv);
    document.getElementById('ku-h').setAttribute('d', dh);
    document.getElementById('ku-t').innerHTML = i ? '<b class="ora">Kat verbraucht:</b> Er kann keinen Sauerstoff mehr speichern. Das Signal nach dem Kat schwankt genauso wie vorne – Fehlerspeicher „Wirkungsgrad zu niedrig“.' : '<b class="grn">Kat in Ordnung:</b> Er speichert Sauerstoff und gleicht aus. Das Signal nach dem Kat bleibt ruhig.';
    kb.forEach(x => x.classList.toggle('on', +x.dataset.k === i));
  }
  kb.forEach(x => x.onclick = () => k(+x.dataset.k)); k(0);
})();
</script>'''

# ---------------------------------------------------------------- Diesel: DPF und AdBlue
T = 'DPF UND ADBLUE'
dpf = [
    titel_folie(K, 'DPF', 'DPF und AdBlue', 'Abgasreinigung beim Diesel – und der Partikelfilter beim Benziner', 'font-size:72px'),
    lernziele(T, ['Wie die Abgasanlage eines modernen Diesels aufgebaut ist', 'Wie der Partikelfilter Ruß sammelt und freibrennt',
                  'Wie AdBlue die Stickoxide verringert', 'Sicher arbeiten und typische Fehler']),
    folie(T, 'Aufbau der Abgasanlage', '''    <div class="kette">
      <div class="glied step"><b>Oxidations-Kat</b><span>wandelt CO und HC um</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Partikelfilter (DPF)</b><span>hält den Ruß zurück</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>AdBlue-Einspritzung</b><span>Dosierventil vor dem SCR-Kat</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>SCR-Kat</b><span>wandelt Stickoxide um</span></div>
    </div>
    <div class="tip step" style="margin-top:18px"><b>Warum kein Dreiwege-Kat?</b>Der Diesel arbeitet mit Luftüberschuss (Lambda größer 1). Dabei kann ein Dreiwege-Kat die Stickoxide nicht umwandeln – darum gibt es eigene Bauteile.</div>'''),
    folie(T, 'Der Partikelfilter', '''    <ol class="steps-list">
      <li class="step">Das Abgas strömt durch <span class="c">poröse Wände</span><small>die Kanäle sind wechselseitig verschlossen – der Ruß bleibt hängen</small></li>
      <li class="step">Der Filter <span class="c">füllt sich</span><small>ein Differenzdrucksensor misst den Druck vor und nach dem Filter</small></li>
      <li class="step">Der Ruß wird <span class="c">verbrannt</span> (Regeneration)<small>passiv bei langer Fahrt, aktiv durch Nacheinspritzung bei ca. 550–650 °C (Richtwert)</small></li>
      <li class="step">Übrig bleibt <span class="c">Asche</span><small>sie verbrennt nicht – nach sehr hoher Laufleistung muss der Filter gereinigt oder getauscht werden</small></li>
    </ol>'''),
    folie(T, 'Beladung und Regeneration – zum Ausprobieren', '''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost" data-f="stadt">Kurzstrecke</button><button class="btn ghost" data-f="bahn">Autobahn</button><button class="btn ghost" data-f="reg">Aktive Regeneration</button></div>
    <div class="grid2" style="align-items:center">
      <div class="card">
        <div class="muted" style="font-size:15px;font-weight:800">RUSSBELADUNG</div><div class="lcd2" id="dp-v" style="font-size:32px;margin-top:6px">30 %</div>
        <div style="height:20px;background:var(--card2);border-radius:8px;margin-top:12px;overflow:hidden"><div id="dp-bar" style="height:100%;width:30%;background:var(--muted);transition:width .2s"></div></div>
        <div class="muted" style="font-size:15px;font-weight:800;margin-top:14px">ABGASTEMPERATUR <span id="dp-temp" class="c">ca. 200 °C</span></div>
      </div>
      <div class="card" id="dp-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Vereinfacht, Beispielwerte.</p>''', sid='s-dp', body_cls='body noclick'),
    folie(T, 'AdBlue und SCR-Kat', '''    <div class="kette">
      <div class="glied step" style="border-top-color:var(--blu)"><b>AdBlue-Tank</b><span>Harnstoff-Wasser-Lösung, beheizt</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Dosierventil</b><span>spritzt fein ins heiße Abgas – daraus wird Ammoniak</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>SCR-Kat</b><span>Stickoxide + Ammoniak → Stickstoff + Wasser</span></div>
    </div>
    <div class="grid2" style="margin-top:18px">
      <div class="tip step"><b>NOx-Sensoren</b>vor und nach dem SCR-Kat – das Steuergerät dosiert und überwacht damit die Menge.</div>
      <div class="tip step"><b>Gefriert bei ca. −11 °C</b>Darum sind Tank und Leitungen beheizt (Richtwert).</div>
    </div>'''),
    folie(T, 'Sicher arbeiten und Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Heiß!</b>Bei der Regeneration wird die Abgasanlage sehr heiß. Zwangsregeneration nur nach Herstellervorgabe, nicht über trockenem Gras, Abgasabsaugung hitzefest.</div>
      <div class="warn step"><b>AdBlue leer</b>Rechtzeitig nachfüllen – ist der Tank leer, startet der Motor nach dem Abstellen nicht mehr.</div>
      <div class="tip step"><b>Nur AdBlue in den AdBlue-Tank</b>Kein Wasser, kein Diesel. AdBlue nie in den Dieseltank – das zerstört die Einspritzanlage.</div>
      <div class="tip step"><b>Weiße Kristalle</b>Getrocknetes AdBlue an Dosierventil oder Leitungen: auf Undichtigkeit prüfen.</div>
      <div class="tip step"><b>DPF voll trotz Fahrt?</b>Differenzdrucksensor und seine Schläuche prüfen – ein abgerutschter Schlauch täuscht falsche Werte vor.</div>
      <div class="tip step"><b>Ottopartikelfilter (OPF)</b>Auch moderne Benzin-Direkteinspritzer haben einen Partikelfilter. Er brennt meist im normalen Betrieb frei.</div>
    </div>'''),
    video(T, 'mm-abgas-dpf'),
    kurztest(T, [
        ('Was macht der Dieselpartikelfilter (DPF)?', ['Er hält den Ruß zurück', 'Er wandelt Stickoxide um', 'Er kühlt das Abgas'], 0, 'Der Ruß wird gesammelt und später verbrannt.'),
        ('Warum füllt sich der DPF bei vielen Kurzstrecken?', ['Weil der Tank zu voll ist', 'Weil das Abgas nicht heiß genug zum Freibrennen wird', 'Weil die Batterie schwach ist'], 1, 'Für die Regeneration braucht es hohe Abgastemperaturen.'),
        ('Was macht AdBlue im SCR-Kat?', ['Es reinigt den DPF', 'Es kühlt den Turbolader', 'Es wandelt Stickoxide in Stickstoff und Wasser um'], 2, 'Aus AdBlue entsteht Ammoniak, das mit den Stickoxiden reagiert.'),
        ('Was passiert, wenn der AdBlue-Tank leer ist?', ['Der Motor startet nach dem Abstellen nicht mehr', 'Nichts', 'Der Motor läuft mit mehr Leistung'], 0, 'Darum warnt das Fahrzeug frühzeitig – rechtzeitig nachfüllen.'),
    ]),
    merke(T, ['Oxi-Kat → DPF → AdBlue → SCR-Kat', 'DPF sammelt Ruß, Regeneration verbrennt ihn|Kurzstrecke füllt den Filter',
              'AdBlue: Stickoxide → Stickstoff + Wasser', 'Regeneration: heiß! AdBlue nie leer fahren']),
]
dpf_js = '''<script>
(function () {
  let bel = 30, mode = 'stadt', temp = 200;
  const bt = document.querySelectorAll('#s-dp [data-f]');
  const TX = {
    stadt: '<b class="ora">Kurzstrecke:</b> Das Abgas wird nicht heiß genug. Der Ruß sammelt sich – der Filter füllt sich.',
    bahn: '<b class="grn">Autobahn:</b> Hohe Abgastemperatur – ein Teil des Rußes verbrennt von selbst (passive Regeneration).',
    reg: '<b class="grn">Aktive Regeneration:</b> Das Steuergerät spritzt nach. Das Abgas wird ca. 600 °C heiß und der Ruß verbrennt. Dabei möglichst nicht abstellen.',
    voll: '<b class="red">Filter voll:</b> Warnleuchte, weniger Leistung. Jetzt hilft eine längere Fahrt nach Bordbuch – oder die Werkstatt.'
  };
  function setm(m) { mode = m; bt.forEach(x => x.classList.toggle('on', x.dataset.f === m)); }
  bt.forEach(x => x.onclick = () => setm(x.dataset.f));
  setm('stadt');
  setInterval(() => {
    if (!document.getElementById('s-dp').classList.contains('active')) return;
    let tz;
    if (mode === 'stadt') { bel = Math.min(100, bel + 0.6); tz = 200; }
    else if (mode === 'bahn') { bel = Math.max(20, bel - 0.2); tz = 400; }
    else { bel = Math.max(3, bel - 1.2); tz = 600; if (bel <= 3) setm('bahn'); }
    temp += (tz - temp) * 0.08;
    document.getElementById('dp-v').textContent = Math.round(bel) + ' %';
    const b = document.getElementById('dp-bar'); b.style.width = bel + '%'; b.style.background = bel > 85 ? 'var(--red)' : 'var(--muted)';
    document.getElementById('dp-temp').textContent = 'ca. ' + Math.round(temp / 10) * 10 + ' °C';
    document.getElementById('dp-t').innerHTML = (bel >= 95 && mode === 'stadt') ? TX.voll : TX[mode];
  }, 100);
})();
</script>'''

# ---------------------------------------------------------------- AGR
T = 'AGR'
agr = [
    titel_folie(K, 'AGR', 'Abgasrückführung', 'Weniger Stickoxide durch zurückgeführtes Abgas', 'font-size:72px'),
    lernziele(T, ['Warum Abgas zurückgeführt wird', 'Wie die AGR aufgebaut ist',
                  'Wann die AGR arbeitet – und wann nicht', 'Typische Fehler und Prüfen']),
    folie(T, 'Warum Abgas zurückführen?', """    <ol class="steps-list">
      <li class="step">Bei sehr heißer Verbrennung entstehen viele <span class="c">Stickoxide (NOx)</span><small>vor allem beim Diesel mit seinem Luftüberschuss</small></li>
      <li class="step">Ein Teil des Abgases wird der <span class="c">Ansaugluft</span> beigemischt<small>Abgas enthält kaum noch Sauerstoff</small></li>
      <li class="step">Die Verbrennung wird <span class="c">kühler</span><small>weniger Sauerstoff, mehr träges Gas im Zylinder</small></li>
      <li class="step">Es entstehen <span class="c">weniger Stickoxide</span><small>beim Benziner sinkt zusätzlich der Verbrauch in der Teillast</small></li>
    </ol>"""),
    folie(T, 'Aufbau', """    <div class="kette">
      <div class="glied step"><b>Abgas</b><span>ein Teil wird abgezweigt</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>AGR-Kühler</b><span>kühlt das Abgas mit Kühlmittel</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>AGR-Ventil</b><span>das Steuergerät bestimmt die Menge</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Ansaugluft</b><span>weniger Sauerstoff, kühlere Verbrennung</span></div>
    </div>
    <div class="grid2" style="margin-top:18px">
      <div class="tip step"><b>Hochdruck-AGR</b>Abgas wird vor dem Turbolader entnommen und ins Saugrohr geführt.</div>
      <div class="tip step"><b>Niederdruck-AGR</b>Abgas wird nach dem Partikelfilter entnommen und vor dem Verdichter zugeführt – sauberer und kühler.</div>
    </div>"""),
    folie(T, 'AGR-Menge – zum Ausprobieren', """    <div class="ctrl"><span style="width:280px">AGR-Rate: <span class="c" id="agr-v">20 %</span></span><input type="range" id="agr" min="0" max="50" step="5" value="20"></div>
    <div class="grid2" style="margin-top:16px;align-items:center">
      <div class="card">
        <div style="font-weight:800;margin-bottom:6px">Stickoxide (NOx)</div>
        <div style="height:22px;background:var(--card2);border-radius:8px;overflow:hidden"><div id="agr-nox" style="height:100%;background:var(--red);transition:width .2s"></div></div>
        <div style="font-weight:800;margin:16px 0 6px">Ruß</div>
        <div style="height:22px;background:var(--card2);border-radius:8px;overflow:hidden"><div id="agr-russ" style="height:100%;background:var(--muted);transition:width .2s"></div></div>
      </div>
      <div class="card" id="agr-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Beispiel Diesel, vereinfacht – das Steuergerät sucht immer den besten Mittelweg.</p>""", sid='s-agr', body_cls='body noclick'),
    folie(T, 'Wann arbeitet die AGR?', """    <div class="values">
      <div class="val step from-left"><b>Teillast, warm</b><span>AGR aktiv – hier entstehen viele Stickoxide</span></div>
      <div class="val step from-left"><b>Volllast</b><span>AGR zu – der Motor braucht jeden Sauerstoff für die Leistung</span></div>
      <div class="val step from-left"><b>Kaltstart</b><span>AGR meist zu – sonst unruhiger Lauf und viel Ruß</span></div>
    </div>
    <div class="tip step" style="margin-top:14px"><b>Innere AGR beim Benziner</b>Über die Nockenwellenverstellung bleibt etwas Abgas im Zylinder (Ventilüberschneidung) – ganz ohne AGR-Ventil.</div>"""),
    folie(T, 'Typische Fehler und Prüfen', """    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>AGR-Ventil verkokt</b>Klemmt offen: Ruckeln, schwarzer Rauch, Leistungsverlust. Klemmt zu: hohe Stickoxide, Fehlerspeicher.</div>
      <div class="warn step"><b>AGR-Kühler undicht</b>Kühlmittelverlust ohne sichtbares Leck, weißer Rauch – Kühlmittel gelangt in den Ansaugtrakt.</div>
      <div class="tip step"><b>Messwerte</b>AGR-Ventil: Soll- und Ist-Stellung vergleichen. Öffnet die AGR, muss die gemessene Luftmasse sinken.</div>
      <div class="tip step"><b>Aktortest</b>Ventil im Aktortest bewegen lassen und Stellung beobachten – nach dem Tausch oft anlernen.</div>
    </div>"""),
    video(T, 'mm-abgas-agr'),
    kurztest(T, [
        ('Was bewirkt die Abgasrückführung?', ['Mehr Leistung', 'Weniger Stickoxide (NOx)', 'Mehr Ladedruck'], 1, 'Die Verbrennung wird kühler – es entstehen weniger Stickoxide.'),
        ('Wann ist die AGR geschlossen?', ['Bei Volllast', 'In der warmen Teillast', 'Immer'], 0, 'Bei Volllast braucht der Motor allen Sauerstoff für die Leistung.'),
        ('Was passiert bei zu viel AGR?', ['Mehr Stickoxide', 'Weniger Verbrauch, sonst nichts', 'Es entsteht viel Ruß'], 2, 'Es fehlt Sauerstoff für eine saubere Verbrennung.'),
        ('Woran erkennst du im Messwert, dass die AGR öffnet?', ['Die gemessene Luftmasse sinkt', 'Die Drehzahl steigt stark', 'Die Batteriespannung sinkt'], 0, 'Ein Teil der Füllung ist dann Abgas – der Luftmassenmesser misst weniger Frischluft.'),
    ]),
    merke(T, ['AGR: weniger Stickoxide durch kühlere Verbrennung', 'Kühler + Ventil, Steuergerät bestimmt die Menge',
              'Aktiv in der warmen Teillast|zu bei Volllast', 'Verkokt? Soll/Ist-Stellung und Luftmasse prüfen']),
]
agr_js = """<script>
(function () {
  const a = document.getElementById('agr');
  function g() {
    const r = +a.value;
    document.getElementById('agr-v').textContent = r + ' %';
    document.getElementById('agr-nox').style.width = (95 - r * 1.6) + '%';
    document.getElementById('agr-russ').style.width = (8 + Math.pow(r / 50, 2.2) * 87) + '%';
    let t;
    if (r < 10) t = '<b class="red">Kaum AGR:</b> sehr heiße Verbrennung – viele Stickoxide.';
    else if (r <= 30) t = '<b class="grn">Mittelweg:</b> deutlich weniger Stickoxide, noch wenig Ruß.';
    else t = '<b class="ora">Zu viel AGR:</b> Es fehlt Sauerstoff – viel Ruß, schwarzer Rauch, der Partikelfilter füllt sich schnell.';
    document.getElementById('agr-t').innerHTML = t;
  }
  a.addEventListener('input', g); g();
})();
</script>"""

STYLE = '  .symbol { font-size: 110px; }'

if __name__ == '__main__':
    seite('mm-abgas-lambda.html', 'Lambdasonde – Motormanagement', 't-mm5', THEMA, lambdas, STYLE, lambdas_js)
    seite('mm-abgas-kat.html', 'Katalysator – Motormanagement', 't-mm5', THEMA, kat, STYLE, kat_js)
    seite('mm-abgas-dpf.html', 'DPF und AdBlue – Motormanagement', 't-mm5', THEMA, dpf, STYLE, dpf_js)
    seite('mm-abgas-agr.html', 'Abgasrückführung – Motormanagement', 't-mm5', THEMA, agr, STYLE, agr_js)
    print('ok')
