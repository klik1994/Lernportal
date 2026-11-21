"""Motormanagement: Gemischbildung Ottomotor – drei Präsentationen.
Aufruf: python3 tools/mm_gemisch.py"""
from praesentation_bauen import *

THEMA = 'Motormanagement: Gemischbildung Otto'
K = 'MOTORMANAGEMENT · GEMISCHBILDUNG OTTO'

# ---------------------------------------------------------------- Kraftstoffsystem
T = 'KRAFTSTOFFSYSTEM'
kraftstoff = [
    titel_folie(K, '⛽', 'Kraftstoffsystem', 'Vom Tank bis zum Einspritzventil', 'font-size:96px'),
    lernziele(T, ['Welchen Weg der Kraftstoff nimmt', 'Saugrohr- und Direkteinspritzung im Vergleich',
                  'Kraftstoffpumpe, Hochdruck und Tankentlüftung', 'Sicher arbeiten und richtig prüfen']),
    folie(T, 'Der Weg des Kraftstoffs – zum Umschalten', '''    <div class="choice" style="margin-bottom:18px"><button class="btn ghost on" id="w-s">Saugrohreinspritzung</button><button class="btn ghost" id="w-d">Direkteinspritzung</button></div>
    <div class="kette" id="weg"></div>
    <div class="card" style="margin-top:20px;font-size:19px;font-weight:600" id="weg-t"></div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Drücke: Richtwerte – genaue Werte laut Herstellerangabe.</p>''', sid='s-weg', body_cls='body noclick'),
    folie(T, 'Die Kraftstoffpumpe', '''    <ol class="steps-list">
      <li class="step">Elektrische Pumpe <span class="c">im Tank</span> (Fördermodul)<small>sie wird vom Kraftstoff gekühlt – darum nicht leer fahren</small></li>
      <li class="step">Beim Öffnen der Tür oder bei Zündung an läuft sie <span class="c">kurz vor</span><small>so ist sofort Druck da – du hörst ein kurzes Summen</small></li>
      <li class="step">Moderne Systeme: <span class="c">bedarfsgeregelt</span> per PWM<small>nur so viel Förderung wie nötig – spart Energie</small></li>
      <li class="step">Motor steht oder Unfall erkannt: Pumpe <span class="c">aus</span><small>Sicherheitsabschaltung</small></li>
    </ol>'''),
    folie(T, 'Hochdruck bei der Direkteinspritzung', '''    <div class="kette">
      <div class="glied step"><b>Niederdruck</b><span>Pumpe im Tank</span></div><div class="flow-arrow step"></div>
      <div class="glied hd step"><b>Hochdruckpumpe</b><span>angetrieben von der Nockenwelle</span></div><div class="flow-arrow step"></div>
      <div class="glied hd step"><b>Rail</b><span>Raildrucksensor meldet den Ist-Druck</span></div><div class="flow-arrow step"></div>
      <div class="glied hd step"><b>Hochdruck-Einspritzventile</b><span>direkt im Brennraum</span></div>
    </div>
    <div class="card step" style="margin-top:20px;font-size:19px;font-weight:600">Das Steuergerät regelt den Druck über das <span class="c">Mengensteuerventil</span> an der Hochdruckpumpe: Ist-Druck (Raildrucksensor) wird ständig mit dem Soll-Druck verglichen.</div>'''),
    folie(T, 'Tankentlüftung', '''    <div class="kette">
      <div class="glied step"><b>Tank</b><span>Kraftstoff verdunstet</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Aktivkohlebehälter</b><span>speichert die Dämpfe</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Tankentlüftungsventil</b><span>Steuergerät öffnet es per PWM</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Saugrohr</b><span>die Dämpfe werden verbrannt</span></div>
    </div>
    <div class="tip step" style="margin-top:20px"><b>Warum?</b>Kraftstoffdämpfe sollen nicht in die Umwelt. Ein klemmendes Tankentlüftungsventil kann zu unruhigem Leerlauf und Fehlerspeichereinträgen führen.</div>'''),
    folie(T, 'Typische Drücke', '''    <div class="values">
      <div class="val step from-left"><b>ca. 3–5 bar</b><span>Saugrohreinspritzung</span></div>
      <div class="val step from-left"><b>ca. 4–6 bar</b><span>Direkteinspritzung, Niederdruck (Vorförderung)</span></div>
      <div class="val step from-left"><b>ca. 200–350 bar</b><span>Direkteinspritzung, Hochdruck im Rail</span></div>
      <div class="val step from-left"><b>über 2.000 bar</b><span>zum Vergleich: Diesel Common-Rail</span></div>
    </div>
    <div class="note step">Richtwerte – Sollwerte immer aus dem Reparaturleitfaden</div>'''),
    folie(T, 'Sicher arbeiten', '''    <div class="warn step"><b>Kraftstoff steht unter Druck</b>Vor dem Öffnen den Druck abbauen – wie der Hersteller es vorgibt. Schutzbrille tragen, Lappen um die Verbindung legen.</div>
    <div class="warn step" style="margin-top:12px"><b>Hochdruck</b>Hochdrucksystem nie bei laufendem Motor öffnen. Hochdruckleitungen nach dem Lösen oft erneuern – Herstellervorgabe beachten.</div>
    <div class="warn step" style="margin-top:12px"><b>Brandgefahr</b>Kein Feuer, keine Funken. Auslaufenden Kraftstoff sofort auffangen, Feuerlöscher bereithalten.</div>''', body_cls='body', body_style=''),
    folie(T, 'Kraftstoffsystem prüfen', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher und Messwerte lesen<small>Raildruck Soll und Ist im Diagnosegerät vergleichen</small></li>
      <li class="step">Pumpe hörbar? Ansteuerung prüfen<small>Vorlauf bei Zündung an, Sicherung und Relais</small></li>
      <li class="step">Niederdruck messen<small>mit Manometer am Prüfanschluss</small></li>
      <li class="step">Fördermenge oder Stromaufnahme prüfen<small>Fördermenge in Zeit X laut Vorgabe, Pumpenstrom mit der Stromzange</small></li>
    </ol>'''),
    video(T, 'mm-kraftstoff'),
    kurztest(T, [
        ('Wo sitzt die elektrische Kraftstoffpumpe meistens?', ['Im Motorraum', 'Im Tank', 'Am Einspritzventil'], 1, 'Im Tank (Fördermodul) – dort wird sie vom Kraftstoff gekühlt.'),
        ('Wer erzeugt bei der Direkteinspritzung den Hochdruck?', ['Die Pumpe im Tank', 'Der Turbolader', 'Die Hochdruckpumpe an der Nockenwelle'], 2, 'Die mechanische Hochdruckpumpe wird von der Nockenwelle angetrieben.'),
        ('Wozu dient der Aktivkohlebehälter?', ['Er speichert Kraftstoffdämpfe aus dem Tank', 'Er filtert die Ansaugluft', 'Er kühlt den Kraftstoff'], 0, 'Die Dämpfe werden später über das Tankentlüftungsventil verbrannt.'),
        ('Was musst du vor dem Öffnen einer Kraftstoffleitung tun?', ['Motor laufen lassen', 'Druck abbauen laut Herstellervorgabe', 'Nichts'], 1, 'Kraftstoff steht unter Druck – Verletzungs- und Brandgefahr.'),
    ]),
    merke(T, ['Tank → Pumpe → Filter → Rail → Einspritzventile', 'Saugrohr ca. 3–5 bar|Direkteinspritzung: Hochdruck ca. 200–350 bar (Richtwerte)',
              'Tankentlüftung: Dämpfe werden verbrannt', 'Vor dem Öffnen: Druck abbauen!']),
]
kraftstoff_js = '''<script>
(function () {
  const W = {
    s: [['Tank', '', 0], ['Kraftstoffpumpe', 'im Tank', 0], ['Filter', '', 0], ['Rail', 'ca. 3–5 bar', 0], ['Einspritzventile', 'im Saugrohr', 0]],
    d: [['Tank', '', 0], ['Kraftstoffpumpe', 'ca. 4–6 bar', 0], ['Hochdruckpumpe', 'an der Nockenwelle', 1], ['Rail', 'ca. 200–350 bar', 1], ['Einspritzventile', 'im Brennraum', 1]]
  };
  const T = { s: 'Saugrohreinspritzung: Der Kraftstoff wird vor das Einlassventil gespritzt. Ein Druck reicht – die elektrische Pumpe schafft das allein.',
              d: 'Direkteinspritzung: Der Kraftstoff wird direkt in den Brennraum gespritzt. Dafür braucht es sehr hohen Druck – den erzeugt die Hochdruckpumpe.' };
  function set(m) {
    const k = document.getElementById('weg'); k.innerHTML = '';
    W[m].forEach((g, i) => {
      if (i) { const a = document.createElement('div'); a.className = 'flow-arrow'; k.appendChild(a); }
      const d = document.createElement('div'); d.className = 'glied' + (g[2] ? ' hd' : '');
      d.innerHTML = '<b>' + g[0] + '</b>' + (g[1] ? '<span>' + g[1] + '</span>' : ''); k.appendChild(d);
    });
    document.getElementById('weg-t').textContent = T[m];
    document.getElementById('w-s').classList.toggle('on', m === 's');
    document.getElementById('w-d').classList.toggle('on', m === 'd');
  }
  document.getElementById('w-s').onclick = () => set('s');
  document.getElementById('w-d').onclick = () => set('d');
  set('s');
})();
</script>'''

# ---------------------------------------------------------------- Einspritzung
T = 'EINSPRITZUNG'
ZYL = '''<svg viewBox="0 0 360 260" width="340" height="245">
  <path d="M110 250 V120 H250 V250" fill="none" stroke="#ecf1f8" stroke-width="5"/>
  <rect x="120" y="190" width="120" height="50" rx="6" fill="#213552" stroke="#94a4ba" stroke-width="3"/>
  <path d="M20 60 H150 L170 118" fill="none" stroke="#94a4ba" stroke-width="4"/>
  <path d="M20 100 H130 L150 118" fill="none" stroke="#94a4ba" stroke-width="4"/>
  <path d="M250 118 L270 70 H350 M250 118 L280 100 H350" fill="none" stroke="#94a4ba" stroke-width="3"/>
  <text x="30" y="45" font-size="15" font-weight="700" fill="#94a4ba">Saugrohr</text>
  <text x="180" y="225" text-anchor="middle" font-size="15" font-weight="700" fill="#94a4ba">Kolben</text>
  {inj}
</svg>'''
INJ_S = '''<rect x="70" y="20" width="22" height="46" rx="4" fill="#5b8cff" transform="rotate(35 81 43)"/>
  <g class="spray"><path d="M100 72 L150 100 L135 112 Z" fill="#5b8cff" opacity=".55"/></g>'''
INJ_D = '''<rect x="170" y="70" width="22" height="50" rx="4" fill="#5b8cff"/>
  <g class="spray"><path d="M181 122 L150 175 L212 175 Z" fill="#5b8cff" opacity=".55"/></g>'''
einspritzung = [
    titel_folie(K, '💧', 'Einspritzung', 'Saugrohr- und Direkteinspritzung', 'font-size:96px'),
    lernziele(T, ['Wo der Kraftstoff eingespritzt wird', 'Vor- und Nachteile von Saugrohr- und Direkteinspritzung',
                  'Wie ein Einspritzventil arbeitet', 'Wie du Einspritzventile prüfst']),
    folie(T, 'Wo wird eingespritzt?', f'''    <div class="grid2">
      <div class="card step" style="text-align:center"><div class="big" style="font-size:22px">Saugrohreinspritzung</div>{ZYL.format(inj=INJ_S)}<p style="font-size:17px;margin:0">vor das Einlassventil – Gemisch bildet sich im Saugrohr</p></div>
      <div class="card step" style="text-align:center"><div class="big" style="font-size:22px">Direkteinspritzung</div>{ZYL.format(inj=INJ_D)}<p style="font-size:17px;margin:0">direkt in den Brennraum – unter sehr hohem Druck</p></div>
    </div>'''),
    folie(T, 'Vor- und Nachteile', '''    <div class="grid2">
      <div class="card step"><div class="big" style="font-size:22px">Saugrohreinspritzung</div>
        <ul style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"><li class="grn">einfach und günstig</li><li class="grn">niedriger Druck</li><li class="grn">Kraftstoff hält die Einlassventile sauber</li><li class="red">etwas mehr Verbrauch</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Direkteinspritzung</div>
        <ul style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"><li class="grn">weniger Verbrauch, mehr Leistung</li><li class="grn">sehr genau, Mehrfacheinspritzung möglich</li><li class="red">teurer, Hochdruck</li><li class="red">Ablagerungen an den Einlassventilen, mehr Partikel (Partikelfilter)</li></ul></div>
      <div class="tip step" style="grid-column:1/-1"><b>Gut zu wissen</b>Manche Motoren haben beides: Saugrohr- und Direkteinspritzung.</div>
    </div>'''),
    folie(T, 'So arbeitet ein Einspritzventil', '''    <div class="grid2" style="align-items:start">
      <svg viewBox="0 0 300 330" width="300" height="320" style="margin:0 auto;display:block">
        <rect x="100" y="10" width="100" height="260" rx="14" fill="#213552" stroke="#94a4ba" stroke-width="3"/>
        <rect x="112" y="60" width="76" height="90" rx="6" fill="#18283f" stroke="#ff8f3f" stroke-width="4"/>
        <text x="150" y="110" text-anchor="middle" font-size="15" font-weight="800" fill="#ff8f3f">Spule</text>
        <g id="nadel" style="transition:transform .25s"><rect x="142" y="155" width="16" height="125" rx="6" fill="#ecf1f8"/></g>
        <path d="M140 280 H160 L155 300 H145 Z" fill="#94a4ba"/>
        <g id="strahl" style="transition:opacity .2s;opacity:0"><path d="M150 300 L118 330 L182 330 Z" fill="#5b8cff" opacity=".6"/></g>
        <text x="215" y="215" font-size="15" font-weight="700" fill="#94a4ba">Nadel</text>
        <text x="215" y="30" font-size="15" font-weight="700" fill="#94a4ba">Kraftstoff</text>
      </svg>
      <ol class="steps-list" id="ev-steps">
        <li class="step">Das Steuergerät schaltet <span class="c">Spannung</span> auf die Spule</li>
        <li class="step">Das Magnetfeld zieht die <span class="c">Nadel</span> hoch – der Kraftstoff spritzt</li>
        <li class="step">Spannung aus: Die <span class="c">Feder</span> drückt die Nadel zu</li>
        <li class="step">Je länger offen (<span class="c">Einspritzzeit</span>), desto mehr Kraftstoff</li>
      </ol>
    </div>''', sid='s-ev'),
    folie(T, 'Einspritzzeit – zum Ausprobieren', '''    <div class="ctrl"><span style="width:260px">Einspritzzeit: <span class="c" id="ti-v">3,0 ms</span></span><input type="range" id="ti" min="1" max="10" step="0.5" value="3"></div>
    <div class="grid2" style="margin-top:16px;align-items:center">
      <div class="card"><div class="muted" style="font-size:15px;font-weight:800">EINSPRITZMENGE PRO EINSPRITZUNG</div><div class="lcd2" id="ti-m" style="font-size:40px;margin-top:6px">—</div>
        <div style="height:16px;background:var(--card2);border-radius:99px;margin-top:14px;overflow:hidden"><div id="ti-bar" style="height:100%;background:var(--c);width:30%;transition:width .3s"></div></div></div>
      <div class="card" style="font-size:19px;font-weight:600">Bei gleichem Kraftstoffdruck gilt: <span class="c">doppelte Einspritzzeit = doppelte Menge</span>. Das Steuergerät bestimmt die Menge über die Einspritzzeit.</div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Beispielwerte – die Durchflussmenge hängt vom Einspritzventil ab.</p>''', body_cls='body noclick'),
    folie(T, 'Einspritzventile prüfen', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Saugrohr-Einspritzventil</div>
        <ul style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"><li>Widerstand spannungsfrei messen (hochohmig ca. 12–16 Ω)</li><li>Ansteuerung mit LED-Prüflampe oder Oszilloskop</li><li>Strahlbild und Dichtheit auf dem Prüfstand</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Hochdruck-Einspritzventil</div>
        <ul style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"><li>wird mit <b>höherer Spannung</b> angesteuert (ca. 65 V)</li><li><b>keine Prüflampe</b> – Diagnosegerät oder Oszilloskop nach Vorgabe</li><li>beim Tausch neue Dichtringe, oft Spezialwerkzeug</li></ul></div>
      <div class="note step" style="grid-column:1/-1">Richtwerte – Sollwerte laut Reparaturleitfaden</div>
    </div>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Undichtes Einspritzventil</b>tropft nach: Gemisch zu fett, schlechter Warmstart, Kraftstoff im Motoröl möglich.</div>
      <div class="tip step"><b>Verkokte Einlassventile</b>Bei Direkteinspritzern fehlt die „Kraftstoffwäsche“ – Ablagerungen können zu Leistungsverlust führen.</div>
      <div class="tip step"><b>Zylinderselektiv</b>Viele Diagnosegeräte zeigen Laufunruhe oder Gemischabweichung pro Zylinder – so findest du das auffällige Ventil.</div>
      <div class="warn step"><b>Hochspannung</b>Ansteuerspannung bei Direkteinspritzung ca. 65 V: Nicht an den Anschlüssen herumprüfen, während der Motor läuft.</div>
    </div>'''),
    video(T, 'mm-einspritzung'),
    kurztest(T, [
        ('Wo spritzt die Direkteinspritzung den Kraftstoff ein?', ['Vor das Einlassventil', 'Direkt in den Brennraum', 'In den Luftfilter'], 1, 'Direkt in den Brennraum – darum braucht es hohen Druck.'),
        ('Wie bestimmt das Steuergerät die Einspritzmenge?', ['Über die Einspritzzeit', 'Über die Batteriespannung', 'Über die Zündspule'], 0, 'Je länger das Ventil offen ist, desto mehr Kraftstoff.'),
        ('Welcher Nachteil kann bei Direkteinspritzern auftreten?', ['Kraftstoff wäscht die Einlassventile', 'Kein Hochdruck nötig', 'Ablagerungen an den Einlassventilen'], 2, 'Es fehlt die „Kraftstoffwäsche“ der Einlassventile.'),
        ('Womit prüfst du ein Hochdruck-Einspritzventil auf keinen Fall?', ['Mit einer Prüflampe', 'Mit dem Diagnosegerät', 'Mit dem Oszilloskop nach Vorgabe'], 0, 'Ansteuerung mit ca. 65 V – keine Prüflampe.'),
    ]),
    merke(T, ['Saugrohr: vor das Einlassventil · Direkt: in den Brennraum', 'Menge = über die Einspritzzeit|bei gleichem Kraftstoffdruck',
              'Einspritzventil: Spule zieht Nadel, Feder schließt', 'Hochdruck-Ventile: ca. 65 V – keine Prüflampe']),
]
einspritzung_js = '''<script>
(function () {
  const s = document.getElementById('s-ev');
  function upd() {
    const n = s.querySelectorAll('#ev-steps .step.on').length;
    const offen = n === 2 || n >= 4;
    document.getElementById('nadel').style.transform = offen ? 'translateY(-14px)' : 'none';
    document.getElementById('strahl').style.opacity = offen ? 1 : 0;
  }
  s.addEventListener('stepon', upd); s.addEventListener('stepoff', upd); s.addEventListener('slideshow', upd);
  const ti = document.getElementById('ti');
  function t() {
    const v = +ti.value, m = v * 4;
    document.getElementById('ti-v').textContent = v.toFixed(1).replace('.', ',') + ' ms';
    document.getElementById('ti-m').textContent = 'ca. ' + m.toFixed(0) + ' mg';
    document.getElementById('ti-bar').style.width = (v / 10 * 100) + '%';
  }
  ti.addEventListener('input', t); t();
})();
</script>'''

# ---------------------------------------------------------------- Luft und Last
T = 'LUFT UND LAST'
luft = [
    titel_folie(K, '🌬️', 'Luft und Last', 'Wie das Steuergerät die angesaugte Luft erfasst', 'font-size:96px'),
    lernziele(T, ['Warum das Steuergerät die Luftmenge kennen muss', 'Luftmassenmesser und Saugrohrdrucksensor',
                  'Das elektronische Gaspedal (E-Gas)', 'Typische Fehler und wie du sie findest']),
    folie(T, 'Erst die Luft, dann der Kraftstoff – zum Ausprobieren', '''    <div class="ctrl"><span style="width:240px">Gaspedal: <span class="c" id="gp-v">20 %</span></span><input type="range" id="gp" min="0" max="100" step="5" value="20"></div>
    <div class="grid2" style="margin-top:16px;align-items:center">
      <svg viewBox="0 0 400 220" width="400" height="220" style="display:block;margin:0 auto">
        <rect x="20" y="70" width="360" height="80" fill="#213552"/>
        <line x1="20" y1="68" x2="380" y2="68" stroke="#ecf1f8" stroke-width="4"/><line x1="20" y1="152" x2="380" y2="152" stroke="#ecf1f8" stroke-width="4"/>
        <g id="dk" style="transform-origin:200px 110px;transition:transform .3s"><line x1="200" y1="72" x2="200" y2="148" stroke="#5b8cff" stroke-width="8" stroke-linecap="round"/></g>
        <circle cx="200" cy="110" r="6" fill="#ecf1f8"/>
        <text x="200" y="190" text-anchor="middle" font-size="16" font-weight="800" fill="#94a4ba">Drosselklappe</text>
        <path id="dk-path" d="M20 110 H380" fill="none"/>
      </svg>
      <div>
        <div class="card"><div class="muted" style="font-size:15px;font-weight:800">LUFTMASSE</div><div class="lcd2" id="gp-l" style="font-size:34px;margin-top:6px">—</div></div>
        <div class="card" style="margin-top:12px"><div class="muted" style="font-size:15px;font-weight:800">KRAFTSTOFF FÜR λ = 1</div><div class="lcd2" id="gp-k" style="font-size:34px;margin-top:6px">—</div></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Beispielwerte bei 2.500 1/min. Kraftstoff = Luftmasse : 14,7.</p>''', sid='s-gp', body_cls='body noclick'),
    folie(T, 'Zwei Wege, die Luft zu erfassen', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Luftmassenmesser (LMM)</div>
        <ul style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"><li>sitzt nach dem Luftfilter</li><li>misst die <b>Luftmasse direkt</b> (kg/h) mit einem beheizten Sensorelement</li><li>oft mit eingebautem Ansauglufttemperatursensor</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Saugrohrdrucksensor</div>
        <ul style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"><li>sitzt am Saugrohr</li><li>misst den <b>Druck</b> im Saugrohr</li><li>das Steuergerät <b>berechnet</b> daraus mit Drehzahl und Temperatur die Luftmenge</li></ul></div>
      <div class="tip step" style="grid-column:1/-1"><b>Gut zu wissen</b>Viele Motoren haben beides – dann prüft das Steuergerät, ob die Werte zusammenpassen.</div>
    </div>'''),
    folie(T, 'Saugrohrdruck – typische Werte', '''    <div class="values">
      <div class="val step from-left"><b>ca. 1 bar</b><span>Motor aus: Saugrohrdruck = Umgebungsdruck</span></div>
      <div class="val step from-left"><b>ca. 0,3 bar</b><span>Leerlauf: Drosselklappe fast zu, starker Unterdruck</span></div>
      <div class="val step from-left"><b>ca. 1 bar</b><span>Volllast beim Saugmotor</span></div>
      <div class="val step from-left"><b>über 1 bar</b><span>Volllast mit Turbo (Ladedruck)</span></div>
    </div>
    <div class="note step">Absolutdruck, Richtwerte</div>'''),
    folie(T, 'Das elektronische Gaspedal (E-Gas)', '''    <div class="kette">
      <div class="glied step" style="border-top-color:var(--grn)"><b>Fahrpedalsensor</b><span>2 Sensoren – doppelt zur Sicherheit</span></div><div class="flow-arrow step k-e"></div>
      <div class="glied step" style="border-top-color:var(--pur)"><b>Steuergerät</b><span>prüft, ob beide Werte zusammenpassen</span></div><div class="flow-arrow step k-v"></div>
      <div class="glied step" style="border-top-color:var(--ora)"><b>Drosselklappensteller</b><span>Elektromotor + 2 Positionssensoren</span></div>
    </div>
    <div class="warn step" style="margin-top:20px"><b>Notlauf</b>Passen die beiden Sensorwerte nicht zusammen, geht die Drosselklappe in Notlaufstellung – das Auto fährt nur noch mit wenig Leistung.</div>
    <div class="tip step" style="margin-top:12px"><b>Nach Reinigung oder Tausch</b>Die Drosselklappe muss oft mit dem Diagnosegerät angelernt werden (Grundeinstellung).</div>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Falschluft</b>Ein Leck nach dem Luftmassenmesser: Diese Luft wird nicht gemessen – das Gemisch wird mager.</div>
      <div class="tip step"><b>Verschmutzter LMM</b>misst zu wenig Luft: Das Steuergerät spritzt zu wenig ein – Leistungsmangel.</div>
      <div class="tip step"><b>Verschmutzte Drosselklappe</b>unruhiger Leerlauf, Motor geht aus: reinigen und anlernen.</div>
      <div class="tip step"><b>Schneller Plausibilitätstest</b>Zündung an, Motor aus: Der Saugrohrdruck muss etwa dem Umgebungsdruck entsprechen.</div>
    </div>'''),
    folie(T, 'Luftsystem prüfen', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher und Messwerte lesen<small>Luftmasse, Saugrohrdruck, Ansaugtemperatur, Drosselklappenwinkel</small></li>
      <li class="step">Sichtprüfung<small>Luftfilter, Schläuche, Schellen: Risse und Lecks (Falschluft)</small></li>
      <li class="step">Luftmasse mit Sollwert vergleichen<small>im Leerlauf und bei Volllast auf der Probefahrt</small></li>
      <li class="step">Saugrohrdruck bei Motor aus prüfen<small>muss etwa dem Umgebungsdruck entsprechen</small></li>
    </ol>'''),
    video(T, 'mm-luft'),
    kurztest(T, [
        ('Warum muss das Steuergerät die angesaugte Luftmenge kennen?', ['Um die passende Kraftstoffmenge zu berechnen', 'Für die Tankanzeige', 'Für die Klimaanlage'], 0, 'Für λ = 1 braucht es zu jeder Luftmenge die passende Kraftstoffmenge.'),
        ('Was misst ein Luftmassenmesser?', ['Den Druck im Saugrohr', 'Die angesaugte Luftmasse', 'Den Restsauerstoff im Abgas'], 1, 'Er misst die Luftmasse direkt, z. B. in kg/h.'),
        ('Ein Schlauch nach dem Luftmassenmesser hat einen Riss. Wie wird das Gemisch?', ['Fett', 'Unverändert', 'Mager'], 2, 'Die Falschluft wird nicht gemessen – zu viel Luft.'),
        ('Warum hat der Fahrpedalsensor zwei Sensoren?', ['Damit das Steuergerät die Werte vergleichen kann (Sicherheit)', 'Für mehr Leistung', 'Für die Kickdown-Funktion'], 0, 'Passen die Werte nicht zusammen, geht das System in den Notlauf.'),
    ]),
    merke(T, ['Erst die Luft messen, dann den Kraftstoff berechnen', 'LMM misst Luftmasse · Saugrohrdrucksensor misst Druck',
              'E-Gas: doppelte Sensoren, bei Fehler Notlauf', 'Falschluft → mager|Drosselklappe nach Reinigung anlernen']),
]
luft_js = '''<script src="assets/schaltung.js"></script>
<script>
(function () {
  const svg = document.querySelector('#s-gp svg');
  const f = Flow(svg, document.getElementById('dk-path'), { spacing: 40, speed: 60, r: 6, color: '#cfe6ff' });
  const gp = document.getElementById('gp');
  function upd() {
    const p = +gp.value / 100;
    const winkel = 8 + 80 * p;
    document.getElementById('dk').style.transform = 'rotate(' + winkel + 'deg)';
    const lm = 12 + 210 * p;
    f.speed = 20 + 260 * p;
    document.getElementById('gp-v').textContent = Math.round(p * 100) + ' %';
    document.getElementById('gp-l').textContent = Math.round(lm) + ' kg/h';
    document.getElementById('gp-k').textContent = (lm / 14.7).toFixed(1).replace('.', ',') + ' kg/h';
  }
  gp.addEventListener('input', upd); upd();
})();
</script>'''

STYLE = '''  .symbol { font-size: 96px; }'''

if __name__ == '__main__':
    seite('mm-kraftstoff.html', 'Kraftstoffsystem – Motormanagement', 't-mm2', THEMA, kraftstoff, STYLE, kraftstoff_js)
    seite('mm-einspritzung.html', 'Einspritzung – Motormanagement', 't-mm2', THEMA, einspritzung, STYLE, einspritzung_js)
    seite('mm-luft.html', 'Luft und Last – Motormanagement', 't-mm2', THEMA, luft, STYLE, luft_js)
    print('ok')
