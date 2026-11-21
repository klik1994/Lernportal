"""Motormanagement: Aufladung – vier Präsentationen.
Aufruf: cd tools && python3 mm_aufladung.py"""
from praesentation_bauen import *

THEMA = 'Motormanagement: Aufladung'
K = 'MOTORMANAGEMENT · AUFLADUNG'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'

LADER = '''<svg viewBox="0 0 560 260" width="540" height="250" style="display:block;margin:0 auto">
  <rect x="190" y="110" width="180" height="40" rx="8" fill="#3b4250" stroke="#94a4ba" stroke-width="2"/>
  <text x="280" y="136" text-anchor="middle" font-size="14" font-weight="800" fill="#ecf1f8">Welle + Lager</text>
  <g class="drehen-t"><circle cx="120" cy="130" r="70" fill="none" stroke="#ff8f3f" stroke-width="5"/>
    <path d="M120 130 L120 66 M120 130 L175 98 M120 130 L175 162 M120 130 L120 194 M120 130 L65 162 M120 130 L65 98" stroke="#ff8f3f" stroke-width="6"/></g>
  <g class="drehen-v"><circle cx="440" cy="130" r="70" fill="none" stroke="#28aaf5" stroke-width="5"/>
    <path d="M440 130 L440 66 M440 130 L495 98 M440 130 L495 162 M440 130 L440 194 M440 130 L385 162 M440 130 L385 98" stroke="#28aaf5" stroke-width="6"/></g>
  <text x="120" y="230" text-anchor="middle" font-size="16" font-weight="800" fill="#ff8f3f">Turbine</text>
  <text x="120" y="250" text-anchor="middle" font-size="13" font-weight="700" fill="#94a4ba">heißes Abgas treibt an</text>
  <text x="440" y="230" text-anchor="middle" font-size="16" font-weight="800" fill="#28aaf5">Verdichter</text>
  <text x="440" y="250" text-anchor="middle" font-size="13" font-weight="700" fill="#94a4ba">drückt Luft in den Motor</text>
</svg>'''

# ---------------------------------------------------------------- Abgasturbolader
T = 'TURBOLADER'
turbo = [
    titel_folie(K, 'T', 'Abgasturbolader', 'Mehr Leistung aus dem Abgas'),
    lernziele(T, ['Warum Motoren aufgeladen werden', 'Wie ein Abgasturbolader aufgebaut ist und arbeitet',
                  'Wozu der Ladeluftkühler dient', 'Wie der Lader geschmiert und gekühlt wird']),
    folie(T, 'Warum aufladen?', '''    <ol class="steps-list">
      <li class="step">Mehr Luft im Zylinder<small>dann kann mehr Kraftstoff verbrannt werden</small></li>
      <li class="step">Mehr Leistung aus kleinem Hubraum<small>„Downsizing“: kleiner Motor, gleiche Leistung</small></li>
      <li class="step">Weniger Verbrauch<small>der kleine Motor hat weniger Reibung und arbeitet öfter im günstigen Bereich</small></li>
    </ol>
    <div class="tip step" style="margin-top:8px"><b>Zwei Wege</b>Abgasturbolader (angetrieben vom Abgas) oder Kompressor (angetrieben vom Motor). Heute haben fast alle Diesel und die meisten Benziner einen Turbo.</div>'''),
    folie(T, 'Aufbau und Funktion', f'''    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {LADER}
      <ol class="steps-list">
        <li class="step">Das Abgas treibt die <span class="c">Turbine</span></li>
        <li class="step">Über die <span class="c">Welle</span> dreht der Verdichter mit<small>bis über 200.000 1/min (Richtwert)</small></li>
        <li class="step">Der <span class="c">Verdichter</span> drückt Luft in den Motor</li>
      </ol>
    </div>'''),
    folie(T, 'Der Ladeluftkühler', '''    <div class="kette">
      <div class="glied step"><b>Verdichter</b><span>Luft wird verdichtet – und dabei heiß</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Ladeluftkühler</b><span>kühlt die Luft wieder ab</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Motor</b><span>kühle Luft ist dichter – mehr Sauerstoff</span></div>
    </div>
    <div class="grid2" style="margin-top:18px">
      <div class="tip step"><b>Luft-Luft-Kühler</b>Sitzt vorne im Fahrtwind, meist vor dem Kühler.</div>
      <div class="tip step"><b>Wassergekühlt</b>Ein eigener Kühlkreislauf kühlt die Ladeluft – oft direkt im Saugrohr.</div>
    </div>'''),
    folie(T, 'Schmierung und Kühlung', '''    <div class="values">
      <div class="val step from-left"><b>Motoröl</b><span>schmiert die Lager der Welle – eine Ölzulauf- und eine Ölrücklaufleitung</span></div>
      <div class="val step from-left"><b>Kühlmittel</b><span>beim Benziner meist zusätzlich – das Abgas ist dort heißer</span></div>
      <div class="val step from-left"><b>bis ca. 1.000 °C</b><span>Abgastemperatur an der Turbine beim Benziner (Diesel weniger)</span></div>
    </div>
    <div class="note step">Richtwerte. Ohne sauberes Öl hält kein Turbo – Ölwechsel nach Vorgabe ist Pflicht.</div>'''),
    folie(T, 'Turbo schonen', '''    <ol class="steps-list">
      <li class="step">Kalt nicht voll belasten<small>das Öl muss erst warm werden und überall hinkommen</small></li>
      <li class="step">Nach starker Belastung kurz nachlaufen lassen<small>damit der heiße Lader abkühlt und das Öl nicht verkokt</small></li>
      <li class="step">Ölwechsel nach Vorgabe, richtiges Öl<small>die Lagerung braucht sauberes Öl</small></li>
      <li class="step">Luftfilter regelmäßig tauschen<small>Schmutz und Fremdkörper beschädigen das Verdichterrad</small></li>
    </ol>'''),
    video(T, 'mm-auf-turbo'),
    kurztest(T, [
        ('Was treibt die Turbine des Abgasturboladers an?', ['Der Keilriemen', 'Das Abgas', 'Ein Elektromotor'], 1, 'Auf derselben Welle sitzt der Verdichter.'),
        ('Wozu dient der Ladeluftkühler?', ['Kühle Luft ist dichter – mehr Sauerstoff im Zylinder', 'Er kühlt das Motoröl', 'Er wärmt den Motor schneller auf'], 0, 'Beim Verdichten wird die Luft warm – gekühlt passt mehr hinein.'),
        ('Womit werden die Lager des Turboladers geschmiert?', ['Mit Fett', 'Mit Kühlmittel', 'Mit Motoröl'], 2, 'Darum sind Ölzulauf, Ölrücklauf und sauberes Öl so wichtig.'),
        ('Warum soll man den Motor nach starker Belastung kurz nachlaufen lassen?', ['Damit der heiße Lader abkühlt und das Öl nicht verkokt', 'Damit die Batterie lädt', 'Damit der Tank leer wird'], 0, 'Verkoktes Öl verstopft die Lager.'),
    ]),
    merke(T, ['Abgas → Turbine → Welle → Verdichter → Luft', 'Ladeluftkühler: kühle Luft ist dichter',
              'Lager werden mit Motoröl geschmiert', 'Warm fahren, nachlaufen lassen']),
]

SUV = '''<svg viewBox="0 0 520 300" width="500" height="290" style="display:block;margin:0 auto" id="suv-svg">
  <text x="20" y="186" font-size="13" font-weight="800" fill="#94a4ba">Ansaugluft</text>
  <path d="M20 200 H120" fill="none" stroke="#ecf1f8" stroke-width="5"/>
  <path d="M150 170 V70 H470" fill="none" stroke="#ecf1f8" stroke-width="5"/>
  <path d="M260 70 V250 H100 V200" fill="none" stroke="#94a4ba" stroke-width="4" stroke-dasharray="7 6"/>
  <rect id="suv-druck" x="146" y="64" width="234" height="12" rx="6" fill="#f05e4e" style="opacity:0;transition:opacity .3s"/>
  <path id="suv-a" d="M20 200 H120 L150 200 V70 H470" fill="none" stroke="none"/>
  <path id="suv-b" d="M150 170 V70 H260 V250 H100 V200 H150" fill="none" stroke="none"/>
  <g class="suv-rad"><circle cx="150" cy="200" r="30" fill="#213552" stroke="#28aaf5" stroke-width="4"/>
    <path d="M150 200 L150 174 M150 200 L172 213 M150 200 L128 213" stroke="#28aaf5" stroke-width="5"/></g>
  <text x="92" y="238" text-anchor="end" font-size="13" font-weight="800" fill="#28aaf5">Verdichter</text>
  <rect x="240" y="135" width="40" height="40" rx="6" fill="#213552" stroke="#94a4ba" stroke-width="2"/>
  <circle id="suv-v" cx="260" cy="155" r="10" fill="#f05e4e" style="transition:fill .3s"/>
  <text x="290" y="150" font-size="13" font-weight="800" fill="#94a4ba">Schubumluft-</text>
  <text x="290" y="166" font-size="13" font-weight="800" fill="#94a4ba">ventil</text>
  <circle cx="400" cy="70" r="16" fill="none" stroke="#94a4ba" stroke-width="2"/>
  <line id="suv-dk" x1="400" y1="56" x2="400" y2="84" stroke="#ffb020" stroke-width="5" stroke-linecap="round" style="transition:transform .5s;transform-origin:400px 70px;transform:rotate(90deg)"/>
  <text x="400" y="40" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Drosselklappe</text>
  <rect x="470" y="40" width="40" height="60" rx="6" fill="#213552" stroke="#94a4ba" stroke-width="2"/>
  <text x="490" y="120" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Motor</text>
  <text id="suv-txt" x="165" y="100" font-size="15" font-weight="900" fill="#f05e4e" style="opacity:0">Druckstoß!</text>
</svg>'''
suv_js = '''
<script>
(function () {
  const s = document.getElementById('s-suv'), svg = document.getElementById('suv-svg');
  const fa = Flow(svg, document.getElementById('suv-a'), { spacing: 30, speed: 90, r: 5, color: '#28aaf5' });
  const fb = Flow(svg, document.getElementById('suv-b'), { spacing: 30, speed: 90, r: 5, color: '#34c778' });
  const rad = svg.querySelector('.suv-rad');
  function upd() {
    const n = s.querySelectorAll('.step.on').length;
    fa.on(n === 0); fb.on(n >= 3);
    document.getElementById('suv-dk').style.transform = n >= 1 ? 'rotate(0deg)' : 'rotate(90deg)';
    const druck = n === 2;
    document.getElementById('suv-druck').style.opacity = druck ? 0.85 : 0;
    document.getElementById('suv-txt').style.opacity = druck ? 1 : 0;
    document.getElementById('suv-v').setAttribute('fill', n >= 3 ? '#34c778' : '#f05e4e');
    rad.style.animationDuration = druck ? '3s' : '0.8s';
  }
  s.addEventListener('stepon', upd); s.addEventListener('stepoff', upd); s.addEventListener('slideshow', upd);
  upd();
})();
</script>'''

# ---------------------------------------------------------------- Ladedruckregelung
T = 'LADEDRUCK'
regel = [
    titel_folie(K, 'p', 'Ladedruckregelung', 'Wastegate, VTG und Schubumluftventil', 'font-size:120px'),
    lernziele(T, ['Warum der Ladedruck geregelt werden muss', 'Wie Wastegate und VTG arbeiten',
                  'Was das Schubumluftventil macht', 'Welche Sensoren und Steller beteiligt sind']),
    folie(T, 'Warum regeln?', '''    <div class="card step" style="font-size:20px;font-weight:600;margin-bottom:14px">Je mehr Abgas, desto schneller dreht der Lader. Ohne Regelung würde der Ladedruck bei hoher Drehzahl <span class="c">viel zu hoch</span>.</div>
    <div class="kette">
      <div class="glied step"><b>Ladedrucksensor</b><span>misst den Ist-Druck</span></div><div class="flow-arrow step k-e"></div>
      <div class="glied step"><b>Steuergerät</b><span>vergleicht mit dem Soll-Druck</span></div><div class="flow-arrow step k-v"></div>
      <div class="glied step"><b>Steller</b><span>Wastegate oder VTG</span></div>
    </div>'''),
    folie(T, 'Wastegate – zum Ausprobieren', '''    <div class="ctrl"><span style="width:280px">Drehzahl: <span class="c" id="wg-n">1.500 1/min</span></span><input type="range" id="wg" min="1000" max="6000" step="100" value="1500"></div>
    <div class="grid2" style="margin-top:14px;align-items:center">
      <div class="card">
        <div class="muted" style="font-size:15px;font-weight:800">LADEDRUCK (ABSOLUT)</div><div class="lcd2" id="wg-p" style="font-size:32px;margin-top:6px">—</div>
        <div class="muted" style="font-size:15px;font-weight:800;margin-top:14px">WASTEGATE GEÖFFNET</div>
        <div style="height:18px;background:var(--card2);border-radius:8px;margin-top:6px;overflow:hidden"><div id="wg-bar" style="height:100%;width:0;background:var(--c);transition:width .2s"></div></div>
      </div>
      <div class="card" id="wg-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Beispiel Benziner, Beispielwerte. 1 bar absolut = kein Ladedruck.</p>''', sid='s-wg', body_cls='body noclick'),
    folie(T, 'VTG – verstellbare Leitschaufeln', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Niedrige Drehzahl</div>
        <ul UL><li>Leitschaufeln stehen <b>eng</b></li><li>das Abgas strömt schnell auf die Turbine</li><li>schon früh viel Ladedruck – kaum Turboloch</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Hohe Drehzahl</div>
        <ul UL><li>Leitschaufeln stehen <b>weit offen</b></li><li>das Abgas strömt langsamer</li><li>der Ladedruck wird nicht zu hoch</li></ul></div>
    </div>
    <div class="note step">VTG gibt es vor allem beim Diesel. Beim Benziner ist das Abgas meist zu heiß dafür – dort regelt das Wastegate.</div>'''.replace('UL', UL)),
    folie(T, 'Das Schubumluftventil (Benziner)', f'''    <div class="grid2" style="align-items:center;grid-template-columns:1.15fr 1fr">
      {SUV}
      <ol class="steps-list">
        <li class="step">Fahrer geht vom Gas<small>die Drosselklappe schließt</small></li>
        <li class="step">Druckstoß vor der Klappe<small>der Verdichter drückt noch Luft gegen die geschlossene Klappe – der Lader würde stark abgebremst</small></li>
        <li class="step">Das Schubumluftventil <span class="c">öffnet</span><small>die Luft strömt zurück vor den Verdichter</small></li>
        <li class="step">Der Lader dreht weiter<small>beim nächsten Gasgeben ist der Ladedruck schneller wieder da</small></li>
      </ol>
    </div>''', sid='s-suv'),
    folie(T, 'Steller und Sensoren', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Unterdruckdose + Taktventil</b>Ein Taktventil (PWM) steuert den Unterdruck an der Dose – sie bewegt Wastegate oder VTG.</div>
      <div class="tip step"><b>Elektrischer Steller</b>Bewegt Wastegate oder VTG direkt, schneller und genauer – mit Rückmeldung der Stellung.</div>
      <div class="tip step"><b>Ladedrucksensor</b>Misst Druck (und oft Temperatur) nach dem Ladeluftkühler – im Diagnosegerät als Ist-Wert.</div>
      <div class="warn step"><b>Überladung</b>Ist der Druck zu hoch, schaltet das Steuergerät in den Notlauf, um den Motor zu schützen.</div>
    </div>'''),
    video(T, 'mm-auf-regelung'),
    kurztest(T, [
        ('Was macht das Wastegate?', ['Es leitet Abgas an der Turbine vorbei', 'Es kühlt die Ladeluft', 'Es misst den Ladedruck'], 0, 'So dreht die Turbine nicht schneller und der Ladedruck bleibt begrenzt.'),
        ('Wie stehen die VTG-Leitschaufeln bei niedriger Drehzahl?', ['Weit offen', 'Eng', 'Sie sind ausgebaut'], 1, 'Eng gestellt strömt das Abgas schneller auf die Turbine – früh viel Ladedruck.'),
        ('Wozu dient das Schubumluftventil?', ['Es erhöht den Ladedruck beim Gasgeben', 'Es kühlt den Turbo', 'Es baut den Druckstoß ab, wenn die Drosselklappe schließt'], 2, 'Die Luft strömt zurück vor den Verdichter, der Lader dreht weiter.'),
        ('Was passiert bei Überladung?', ['Das Steuergerät schaltet in den Notlauf', 'Der Motor bekommt mehr Leistung', 'Nichts'], 0, 'So wird der Motor geschützt.'),
    ]),
    merke(T, ['Ladedrucksensor → Steuergerät → Steller', 'Wastegate: Abgas an der Turbine vorbei',
              'VTG: eng bei niedriger, weit bei hoher Drehzahl', 'Schubumluftventil: Druckstoß abbauen']),
]
regel_js = '''<script>
(function () {
  const wg = document.getElementById('wg');
  function f() {
    const n = +wg.value;
    const ohne = 1 + Math.min(2.4, Math.max(0, (n - 1100) / 1500));
    const soll = 2.2;
    const p = Math.min(ohne, soll);
    const auf = ohne > soll ? Math.min(100, (ohne - soll) / 1.2 * 100) : 0;
    document.getElementById('wg-n').textContent = n.toLocaleString('de-DE') + ' 1/min';
    document.getElementById('wg-p').textContent = 'ca. ' + p.toFixed(1).replace('.', ',') + ' bar';
    document.getElementById('wg-bar').style.width = auf + '%';
    document.getElementById('wg-t').innerHTML = auf > 0
      ? '<b class="grn">Wastegate öffnet:</b> Ein Teil des Abgases strömt an der Turbine vorbei. Der Ladedruck bleibt beim Sollwert – ohne Wastegate wären es jetzt ca. ' + ohne.toFixed(1).replace('.', ',') + ' bar.'
      : '<b>Wastegate zu:</b> Das ganze Abgas treibt die Turbine – der Ladedruck steigt mit der Drehzahl.';
  }
  wg.addEventListener('input', f); f();
})();
</script>'''

# ---------------------------------------------------------------- Kompressor
T = 'KOMPRESSOR'
kompressor = [
    titel_folie(K, 'K', 'Kompressor', 'Mechanische Aufladung – vom Motor angetrieben'),
    lernziele(T, ['Wie ein Kompressor angetrieben wird', 'Welche Bauarten es gibt',
                  'Vor- und Nachteile gegenüber dem Turbo', 'Kombinationen und elektrischer Zusatzverdichter']),
    folie(T, 'Antrieb', '''    <div class="kette">
      <div class="glied step"><b>Kurbelwelle</b><span>Riemenscheibe</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Riemen</b><span>mit Übersetzung – der Lader dreht schneller als der Motor</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Magnetkupplung</b><span>schaltet den Lader zu oder ab</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Kompressor</b><span>drückt Luft in den Motor</span></div>
    </div>
    <div class="tip step" style="margin-top:18px"><b>Fest mit dem Motor verbunden</b>Der Kompressor dreht immer im Verhältnis zur Motordrehzahl – darum liefert er sofort Ladedruck, auch bei niedriger Drehzahl.</div>'''),
    folie(T, 'Bauarten', '''    <div class="grid2" style="align-content:start">
      <div class="card step"><div class="big" style="font-size:21px">Roots-Gebläse</div><ul UL><li>zwei Drehkolben fördern die Luft</li><li>verdichtet erst im Saugrohr</li><li>robust, typisches Heulen</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">Schraubenlader</div><ul UL><li>zwei Schraubenrotoren</li><li>verdichtet schon im Lader</li><li>besserer Wirkungsgrad</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">G-Lader (Spirallader)</div><ul UL><li>spiralförmige Kammern</li><li>bei älteren VW-Modellen</li><li>empfindlich, Wartung wichtig</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">Radialverdichter</div><ul UL><li>Verdichterrad wie beim Turbo</li><li>aber mechanisch angetrieben</li><li>hohe Drehzahlen</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Turbo oder Kompressor? – zum Ausprobieren', '''    <div class="ctrl"><span style="width:280px">Drehzahl: <span class="c" id="tk-n">1.200 1/min</span></span><input type="range" id="tk" min="800" max="6000" step="100" value="1200"></div>
    <div class="grid2" style="margin-top:14px;align-items:center">
      <div class="card" id="tk-bars"></div>
      <div class="card" id="tk-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Ladedruck absolut, Beispielwerte, vereinfacht.</p>''', sid='s-tk', body_cls='body noclick'),
    folie(T, 'Vor- und Nachteile', '''    <div class="grid2" style="align-items:start">
      <div class="card step" style="border-top:4px solid var(--grn)"><div class="big" style="font-size:22px">Vorteile</div>
        <ul UL><li>sofort Ladedruck – kein Turboloch</li><li>kein heißes Abgas am Lader</li><li>einfache Ölversorgung, oft eigene Füllung</li></ul></div>
      <div class="card step" style="border-top:4px solid var(--red)"><div class="big" style="font-size:22px">Nachteile</div>
        <ul UL><li>braucht Motorleistung für den Antrieb</li><li>höherer Verbrauch als ein Turbo</li><li>groß und schwer, Geräusche</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Kombinationen', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Kompressor + Turbo</b>Unten hilft der Kompressor, oben übernimmt der Turbo – z. B. beim 1.4 TSI „Twincharger“. Eine Klappe steuert den Weg der Luft.</div>
      <div class="tip step"><b>Elektrischer Zusatzverdichter</b>Ein Elektromotor treibt einen Verdichter an – oft mit 48-V-Bordnetz. Er hilft beim Anfahren, bis der Turbo Druck aufbaut.</div>
      <div class="tip step"><b>Biturbo</b>Zwei Turbolader: ein kleiner für unten, ein großer für oben – oder einer pro Zylinderbank.</div>
      <div class="warn step"><b>Arbeiten am Riementrieb</b>Riemen nur bei stehendem Motor prüfen. Spannung und Verlauf laut Hersteller – ein gerissener Riemen legt den Kompressor still.</div>
    </div>'''),
    video(T, 'mm-auf-kompressor'),
    kurztest(T, [
        ('Wie wird ein Kompressor angetrieben?', ['Vom Abgas', 'Mechanisch vom Motor, z. B. über einen Riemen', 'Von der Batterie allein'], 1, 'Darum liefert er sofort Ladedruck.'),
        ('Was ist ein Vorteil des Kompressors gegenüber dem Turbo?', ['Kein Turboloch – sofort Ladedruck', 'Er braucht keine Leistung', 'Er ist immer leiser'], 0, 'Er dreht immer im Verhältnis zur Motordrehzahl.'),
        ('Was ist ein Nachteil des Kompressors?', ['Er wird vom Abgas zu heiß', 'Er hat ein großes Turboloch', 'Er braucht Motorleistung für den Antrieb'], 2, 'Das erhöht den Verbrauch.'),
        ('Wozu dient die Magnetkupplung am Kompressor?', ['Sie schaltet den Kompressor zu oder ab', 'Sie misst den Ladedruck', 'Sie kühlt den Riemen'], 0, 'Wird kein Ladedruck gebraucht, kann der Kompressor abgeschaltet werden.'),
    ]),
    merke(T, ['Kompressor: vom Motor angetrieben', 'Sofort Ladedruck, kein Turboloch|kostet aber Motorleistung',
              'Roots, Schraube, G-Lader, Radial', 'Kombination mit Turbo oder E-Verdichter']),
]
kompressor_js = '''<script>
(function () {
  const tk = document.getElementById('tk');
  function f() {
    const n = +tk.value;
    const turbo = 1 + 1.2 * Math.max(0, Math.min(1, (n - 1300) / 1500));
    const komp = 1 + 0.15 + 0.7 * Math.min(1, (n - 800) / 1500);
    const bar = (lab, p, col) => '<div style="font-weight:800;margin:10px 0 6px">' + lab + ' <span class="muted">ca. ' + p.toFixed(1).replace('.', ',') + ' bar</span></div><div style="height:20px;background:var(--card2);border-radius:8px;overflow:hidden"><div style="height:100%;width:' + ((p - 1) / 1.3 * 100) + '%;background:' + col + '"></div></div>';
    document.getElementById('tk-n').textContent = n.toLocaleString('de-DE') + ' 1/min';
    document.getElementById('tk-bars').innerHTML = bar('Turbo', turbo, 'var(--ora)') + bar('Kompressor', komp, 'var(--blu)');
    document.getElementById('tk-t').innerHTML = n < 1800
      ? '<b>Niedrige Drehzahl:</b> Der Kompressor liefert sofort Druck. Beim Turbo fehlt noch Abgas – das „Turboloch“.'
      : '<b>Höhere Drehzahl:</b> Jetzt liefert der Turbo viel Druck – ohne Motorleistung zu kosten. Der Kompressor braucht immer mehr Antriebsleistung.';
  }
  tk.addEventListener('input', f); f();
})();
</script>'''

# ---------------------------------------------------------------- Diagnose und Schäden
T = 'TURBO-DIAGNOSE'
diagnose = [
    titel_folie(K, '!', 'Turbo-Diagnose', 'Fehler finden, Schäden verstehen, richtig tauschen', 'font-size:120px'),
    lernziele(T, ['Typische Fehlerbilder der Aufladung', 'Ladedruck prüfen und das Ladeluftsystem abdrücken',
                  'Ursachen von Turboschäden erkennen', 'Einen Turbolader richtig tauschen']),
    folie(T, 'Fehlerbilder – zum Durchklicken', '''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-f="0">Zu wenig Leistung</button><button class="btn ghost" data-f="1">Notlauf bei Volllast</button><button class="btn ghost" data-f="2">Blauer Rauch</button><button class="btn ghost" data-f="3">Pfeifen / Heulen</button></div>
    <div class="card" id="fb-t" style="font-size:18px;font-weight:600;line-height:1.6"></div>''', sid='s-fb', body_cls='body noclick'),
    folie(T, 'Ladedruck prüfen', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher lesen<small>Regelabweichung Ladedruck, Unter- oder Überladung</small></li>
      <li class="step">Messwerte bei Volllast-Probefahrt<small>Soll- und Ist-Ladedruck vergleichen – ein Beifahrer liest ab oder das Diagnosegerät zeichnet auf</small></li>
      <li class="step">Steller im Aktortest<small>bewegen sich Wastegate oder VTG frei über den ganzen Weg?</small></li>
      <li class="step">Ladeluftsystem abdrücken<small>mit Abdrückgerät und Druck laut Hersteller – Lecks hört oder sieht man</small></li>
    </ol>'''),
    folie(T, 'Den Lader selbst prüfen', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Wellenspiel</b>Ein wenig radiales Spiel ist normal. Streift das Verdichterrad am Gehäuse, ist der Lader defekt.</div>
      <div class="tip step"><b>Verdichterrad</b>Verbogene oder abgebrochene Schaufeln: Fremdkörper – Luftfilter und Ansaugweg prüfen.</div>
      <div class="tip step"><b>Öl im Ladeluftsystem</b>Etwas Ölnebel ist normal. Viel Öl: Ölrücklauf, Kurbelgehäuseentlüftung und Lagerung prüfen.</div>
      <div class="warn step"><b>Motor geht durch</b>Viel Öl im Ansaugtrakt kann der Diesel als Kraftstoff verbrennen – er dreht hoch und lässt sich nicht abstellen. Gefahr!</div>
    </div>'''),
    folie(T, 'Ursachen für Turboschäden', '''    <div class="values">
      <div class="val step from-left"><b>Ölmangel</b><span>verstopfte Zulaufleitung, zu wenig Öl, falsches Öl</span></div>
      <div class="val step from-left"><b>Verschmutztes Öl</b><span>Wechselintervall überzogen, Ölschlamm, Späne</span></div>
      <div class="val step from-left"><b>Ölrücklauf verstopft</b><span>Öl staut sich und wird über die Dichtungen gedrückt</span></div>
      <div class="val step from-left"><b>Fremdkörper</b><span>Schmutz, Teile oder defekter Luftfilter im Ansaugweg</span></div>
    </div>
    <div class="note step">Ein Turbo geht fast nie „einfach so“ kaputt. Die Ursache liegt meist außerhalb des Laders.</div>'''),
    folie(T, 'Turbolader richtig tauschen', '''    <ol class="steps-list">
      <li class="step">Ursache finden und beheben<small>sonst ist der neue Lader nach kurzer Zeit wieder defekt</small></li>
      <li class="step">Ölzulaufleitung erneuern, Ölrücklauf frei, Ölsieb prüfen<small>dazu Ölwechsel mit Filter, Luftfilter neu, Ansaugweg reinigen</small></li>
      <li class="step">Neuen Lader mit frischem Öl befüllen<small>nur neue Dichtungen verwenden</small></li>
      <li class="step">Vor dem ersten Start Öldruck aufbauen<small>Vorgehen laut Hersteller – dann im Leerlauf laufen lassen und auf Dichtheit prüfen</small></li>
    </ol>'''),
    video(T, 'mm-auf-diagnose'),
    kurztest(T, [
        ('Der Motor geht bei Volllast in den Notlauf, Ladedruck zu niedrig. Was prüfst du zuerst?', ['Ladeluftschläuche auf Undichtigkeit', 'Die Zündkerzen', 'Den Reifendruck'], 0, 'Ein undichter Schlauch ist ein häufiger Grund für Unterladung.'),
        ('Was ist die häufigste Ursache für einen Turboschaden?', ['Zu viel Kühlmittel', 'Probleme mit der Ölversorgung', 'Zu hoher Reifendruck'], 1, 'Ölmangel, Schmutz im Öl oder ein verstopfter Rücklauf.'),
        ('Was musst du beim Turbotausch immer machen?', ['Nur den Lader tauschen', 'Den Ladedrucksensor tauschen', 'Ursache beheben, Ölzulauf erneuern, Ölwechsel'], 2, 'Sonst geht der neue Lader auch kaputt.'),
        ('Viel Öl im Ladeluftsystem eines Diesels – welche Gefahr besteht?', ['Der Motor kann „durchgehen“', 'Die Batterie wird leer', 'Keine'], 0, 'Er verbrennt das Öl als Kraftstoff und lässt sich nicht abstellen.'),
    ]),
    merke(T, ['Ladedruck Soll/Ist bei Volllast vergleichen', 'Undichtigkeit? Ladeluftsystem abdrücken',
              'Turboschaden: meist Ölversorgung', 'Beim Tausch: Ursache beheben, Öl, Ölzulauf']),
]
diagnose_js = '''<script>
(function () {
  const F = [
    '<b>Zu wenig Leistung, Ladedruck zu niedrig (Unterladung)</b><br>Mögliche Ursachen: undichter Ladeluftschlauch oder Ladeluftkühler, Wastegate klemmt offen, VTG klemmt offen, Unterdruckschlauch am Steller undicht, verstopfter Luftfilter, verstopfter Partikelfilter.',
    '<b>Notlauf bei Volllast, Ladedruck zu hoch (Überladung)</b><br>Mögliche Ursachen: VTG-Leitschaufeln verrußt und klemmen, Wastegate klemmt zu, Steller oder Taktventil defekt, Ladedrucksensor misst falsch.',
    '<b>Blauer Rauch, Ölverbrauch</b><br>Mögliche Ursachen: Ölrücklauf des Laders verstopft, Kurbelgehäuseentlüftung defekt (Überdruck im Motor), Lagerschaden am Lader. Erst die Ursache außerhalb des Laders prüfen!',
    '<b>Pfeifen oder Heulen</b><br>Mögliche Ursachen: Undichtigkeit im Ladeluftsystem (Pfeifen beim Gasgeben), Lagerspiel – das Verdichterrad streift. Ladeluftsystem abdrücken, Wellenspiel prüfen.'
  ];
  const bt = document.querySelectorAll('#s-fb [data-f]');
  function f(i) { document.getElementById('fb-t').innerHTML = F[i]; bt.forEach(x => x.classList.toggle('on', +x.dataset.f === i)); }
  bt.forEach(x => x.onclick = () => f(+x.dataset.f)); f(0);
})();
</script>'''

STYLE = '''  .symbol { font-size: 110px; }
  .drehen-t, .drehen-v { animation: dreh 1.2s linear infinite; }
  .drehen-t { transform-origin: 120px 130px; } .drehen-v { transform-origin: 440px 130px; }
  @keyframes dreh { to { transform: rotate(360deg); } }
  .suv-rad { animation: dreh .8s linear infinite; transform-origin: 150px 200px; }'''

if __name__ == '__main__':
    seite('mm-auf-turbo.html', 'Abgasturbolader – Motormanagement', 't-mm7', THEMA, turbo, STYLE, '')
    seite('mm-auf-regelung.html', 'Ladedruckregelung – Motormanagement', 't-mm7', THEMA, regel, STYLE, '<script src="assets/schaltung.js"></script>' + regel_js + suv_js)
    seite('mm-auf-kompressor.html', 'Kompressor – Motormanagement', 't-mm7', THEMA, kompressor, STYLE, kompressor_js)
    seite('mm-auf-diagnose.html', 'Turbo-Diagnose – Motormanagement', 't-mm7', THEMA, diagnose, STYLE, diagnose_js)
    print('ok')
