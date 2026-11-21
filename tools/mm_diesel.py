"""Motormanagement: Dieselmanagement – drei Präsentationen.
Aufruf: cd tools && python3 mm_diesel.py"""
from praesentation_bauen import *

THEMA = 'Motormanagement: Dieselmanagement'
K = 'MOTORMANAGEMENT · DIESEL'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'

# ---------------------------------------------------------------- Grundlagen + Glühanlage
T = 'DIESEL'
GLUEH = '''<svg viewBox="0 0 300 300" width="280" height="280" style="display:block;margin:0 auto">
  <rect x="135" y="20" width="30" height="40" rx="5" fill="#a9b3c1" stroke="#6b7686" stroke-width="2"/>
  <rect x="120" y="60" width="60" height="40" rx="4" fill="#6b7686"/>
  <rect x="128" y="100" width="44" height="90" fill="#a9b3c1" stroke="#6b7686" stroke-width="2"/>
  <path d="M128 112 l44 10 M128 130 l44 10 M128 148 l44 10 M128 166 l44 10" stroke="#6b7686" stroke-width="3"/>
  <rect x="138" y="190" width="24" height="40" fill="#a9b3c1" stroke="#6b7686" stroke-width="2"/>
  <rect id="gk-spitze" x="142" y="230" width="16" height="50" rx="8" fill="#6b7686" style="transition:fill .6s"/>
  <circle id="gk-glow" cx="150" cy="262" r="34" fill="#ff8f3f" style="opacity:0;transition:opacity .6s"/>
</svg>'''

grundlagen = [
    titel_folie(K, 'D', 'Diesel-Grundlagen', 'Selbstzündung, Luftüberschuss und Glühanlage'),
    lernziele(T, ['Wie sich der Diesel von selbst entzündet', 'Unterschiede zwischen Otto- und Dieselmotor',
                  'Wie die Leistung geregelt wird', 'Wie die Glühanlage beim Kaltstart hilft']),
    folie(T, 'Selbstzündung', '''    <ol class="steps-list">
      <li class="step">Der Kolben verdichtet <span class="c">nur Luft</span><small>sehr stark – ca. 16 : 1 bis 20 : 1 (Richtwert)</small></li>
      <li class="step">Die Luft wird dabei <span class="c">sehr heiß</span><small>ca. 700–900 °C (Richtwert) – wie beim Aufpumpen eines Fahrradreifens, nur viel stärker</small></li>
      <li class="step">Kurz vor OT wird Diesel <span class="c">eingespritzt</span><small>fein zerstäubt, mit sehr hohem Druck</small></li>
      <li class="step">Der Kraftstoff <span class="c">entzündet sich von selbst</span><small>keine Zündkerze nötig</small></li>
    </ol>'''),
    folie(T, 'Otto und Diesel im Vergleich', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Ottomotor</div>
        <ul UL><li>Zündung durch Funke (Zündkerze)</li><li>Verdichtung ca. 10 : 1 bis 14 : 1</li><li>Last über die Luftmenge (Drosselklappe)</li><li>Lambda meist = 1</li></ul></div>
      <div class="card step" style="border-top:4px solid var(--c)"><div class="big" style="font-size:22px">Dieselmotor</div>
        <ul UL><li>Selbstzündung durch heiße Luft</li><li>Verdichtung ca. 16 : 1 bis 20 : 1</li><li>Last über die <b>Kraftstoffmenge</b></li><li>immer Luftüberschuss: Lambda größer 1</li></ul></div>
    </div>
    <div class="note step">Richtwerte – genaue Werte laut Herstellerangabe</div>'''.replace('UL', UL)),
    folie(T, 'So wird die Leistung geregelt', '''    <div class="kette">
      <div class="glied step"><b>Fahrpedal</b><span>Fahrerwunsch</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Steuergerät</b><span>berechnet die Einspritzmenge</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Injektoren</b><span>mehr Kraftstoff = mehr Leistung</span></div>
    </div>
    <div class="grid2" style="margin-top:20px">
      <div class="tip step"><b>Luft ist immer genug da</b>Der Diesel saugt immer viel Luft an. Geregelt wird nur, wie viel Kraftstoff dazukommt.</div>
      <div class="tip step"><b>Drosselklappe beim Diesel?</b>Gibt es oft – aber nicht für die Leistung, sondern für die Abgasrückführung und zum ruhigen Abstellen.</div>
    </div>'''),
    folie(T, 'Die Glühanlage – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost" data-g="0">Zündung aus</button><button class="btn ghost" data-g="1">Vorglühen</button><button class="btn ghost" data-g="2">Motor startet</button><button class="btn ghost" data-g="3">Nachglühen</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:300px 1fr">
      {GLUEH}
      <div>
        <div class="card" style="display:flex;align-items:center;gap:14px"><div id="gk-lampe" style="width:46px;height:46px;border-radius:50%;background:var(--card2);display:grid;place-items:center;font-size:24px;font-weight:900;color:var(--muted)">~</div><div style="font-weight:800" id="gk-l">Glühkontrollleuchte aus</div></div>
        <div class="card" id="gk-t" style="margin-top:12px;font-size:18px;font-weight:600;line-height:1.5"></div>
      </div>
    </div>''', sid='s-gk', body_cls='body noclick'),
    folie(T, 'Glühkerzen prüfen', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher lesen<small>das Glühzeitsteuergerät erkennt defekte Glühkerzen oft selbst</small></li>
      <li class="step">Stromaufnahme mit der <span class="c">Stromzange</span><small>alle Glühkerzen vergleichen – eine ohne Strom ist defekt</small></li>
      <li class="step">Oder Widerstand messen – <span class="c">spannungsfrei</span>, Stecker ab<small>sehr kleiner Widerstand ist richtig, genauer Wert laut Hersteller</small></li>
      <li class="step">Zeigt das Multimeter „OL“?<small>Bei manuellem Multimeter erst den Messbereich schrittweise bis zum höchsten hochstellen – erst dann gilt: Unterbrechung</small></li>
    </ol>
    <div class="warn step" style="margin-top:6px"><b>Niedervolt-Glühkerzen</b>Moderne Glühkerzen arbeiten mit weniger als 12 V (Ansteuerung mit PWM). Nie direkt an die Batterie anschließen – sie brennen sofort durch.</div>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Springt kalt schlecht an</b>Zuerst an Glühkerzen, Batterie und Raildruck denken.</div>
      <div class="tip step"><b>Weißer Rauch beim Kaltstart</b>Unverbrannter Kraftstoff – oft fehlt das Nachglühen oder eine Glühkerze ist defekt.</div>
      <div class="warn step"><b>Glühkerze ausbauen</b>Nur bei warmem Motor, mit Drehmomentschlüssel und Gefühl – festgebrannte Glühkerzen reißen leicht ab.</div>
      <div class="tip step"><b>Winterdiesel</b>Im Winter kann Diesel ohne Zusätze versulzen – Paraffin verstopft den Filter.</div>
    </div>'''),
    video(T, 'mm-diesel-grundlagen'),
    kurztest(T, [
        ('Wie entzündet sich der Kraftstoff im Dieselmotor?', ['Durch einen Funken', 'Von selbst in der heißen, verdichteten Luft', 'Durch die Glühkerze bei jeder Verbrennung'], 1, 'Die Luft wird beim Verdichten sehr heiß – der Diesel entzündet sich von selbst.'),
        ('Wie wird beim Diesel die Leistung geregelt?', ['Über die Kraftstoffmenge', 'Über die Drosselklappe', 'Über die Zündspannung'], 0, 'Luft ist immer genug da, geregelt wird die Einspritzmenge.'),
        ('Wozu dient das Nachglühen?', ['Es lädt die Batterie', 'Es kühlt den Motor', 'Ruhiger Lauf und weniger Rauch nach dem Kaltstart'], 2, 'Die Glühkerzen bleiben nach dem Start noch eine Zeit an.'),
        ('Was darfst du mit Niedervolt-Glühkerzen nicht machen?', ['Mit der Stromzange prüfen', 'Direkt an 12 V anschließen', 'Fehlerspeicher lesen'], 1, 'Sie arbeiten mit weniger als 12 V und brennen an der Batterie sofort durch.'),
    ]),
    merke(T, ['Selbstzündung durch heiße, verdichtete Luft', 'Leistung über die Kraftstoffmenge|Luftüberschuss, Lambda größer 1',
              'Glühkerzen helfen beim Kaltstart', 'Niedervolt-Glühkerzen nie an 12 V']),
]
grundlagen_js = '''<script>
(function () {
  const G = [
    ['#6b7686', 0, false, 'Glühkontrollleuchte aus', 'Alles aus. Tippe auf <b>Vorglühen</b>.'],
    ['#ff7a2f', .8, true, 'Glühkontrollleuchte an', '<b>Zündung an:</b> Das Glühzeitsteuergerät schaltet Spannung auf die Glühkerzen. Sie werden in wenigen Sekunden sehr heiß und wärmen den Brennraum. Erlischt die Leuchte, kann gestartet werden. Bei warmem Motor entfällt das Vorglühen.'],
    ['#ff7a2f', .8, false, 'Glühkontrollleuchte aus', '<b>Start:</b> Die heiße Glühkerze hilft, dass sich der Kraftstoff im noch kalten Brennraum entzündet.'],
    ['#ff9b3f', .5, false, 'Glühkontrollleuchte aus', '<b>Nachglühen:</b> Die Glühkerzen bleiben nach dem Start noch eine Zeit an – für ruhigen Lauf, weniger Geräusch und weniger weißen Rauch.']
  ];
  const bt = document.querySelectorAll('#s-gk [data-g]');
  function g(i) {
    document.getElementById('gk-spitze').setAttribute('fill', G[i][0]);
    document.getElementById('gk-glow').style.opacity = G[i][1];
    const l = document.getElementById('gk-lampe');
    l.style.background = G[i][2] ? '#ffb020' : 'var(--card2)'; l.style.color = G[i][2] ? '#1a1a1a' : 'var(--muted)';
    document.getElementById('gk-l').textContent = G[i][3];
    document.getElementById('gk-t').innerHTML = G[i][4];
    bt.forEach(x => x.classList.toggle('on', +x.dataset.g === i));
  }
  bt.forEach(x => x.onclick = () => g(+x.dataset.g));
  document.getElementById('s-gk').addEventListener('slideshow', () => g(0));
  g(0);
})();
</script>'''

# ---------------------------------------------------------------- Common-Rail
T = 'COMMON-RAIL'
VERLAUF = '''<svg viewBox="0 0 560 220" width="540" height="212" style="display:block;margin:0 auto">
  <line x1="30" y1="180" x2="540" y2="180" stroke="#94a4ba" stroke-width="2"/>
  <line x1="250" y1="30" x2="250" y2="180" stroke="#94a4ba" stroke-width="2" stroke-dasharray="6 6"/>
  <text x="250" y="206" text-anchor="middle" font-size="16" font-weight="800" fill="#ecf1f8">OT</text>
  <text x="34" y="40" font-size="14" font-weight="700" fill="#94a4ba">Einspritzung</text>
  <g id="ev-vor" style="transition:opacity .3s"><rect x="175" y="140" width="16" height="40" rx="3" fill="#a07cf5"/><rect x="200" y="140" width="16" height="40" rx="3" fill="#a07cf5"/><text x="195" y="128" text-anchor="middle" font-size="14" font-weight="800" fill="#a07cf5">Vor</text></g>
  <g id="ev-haupt" style="transition:opacity .3s"><rect x="240" y="60" width="70" height="120" rx="4" fill="#a07cf5"/><text x="275" y="50" text-anchor="middle" font-size="14" font-weight="800" fill="#a07cf5">Haupt</text></g>
  <g id="ev-nach" style="transition:opacity .3s"><rect x="420" y="130" width="22" height="50" rx="3" fill="#a07cf5"/><text x="431" y="118" text-anchor="middle" font-size="14" font-weight="800" fill="#a07cf5">Nach</text></g>
</svg>'''

rail = [
    titel_folie(K, 'CR', 'Common-Rail', 'Hochdruck, Injektoren und Einspritzverlauf', 'font-size:84px'),
    lernziele(T, ['Wie ein Common-Rail-System aufgebaut ist', 'Welche Drücke dort herrschen',
                  'Warum mehrmals pro Takt eingespritzt wird', 'Sicher arbeiten und prüfen']),
    folie(T, 'Aufbau', '''    <div class="kette">
      <div class="glied step"><b>Vorförderpumpe</b><span>im Tank, Niederdruck</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Kraftstofffilter</b><span>mit Wasserabscheider</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Hochdruckpumpe</b><span>vom Motor angetrieben</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Rail</b><span>Hochdruckspeicher mit Raildrucksensor</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Injektoren</b><span>spritzen in den Brennraum</span></div>
    </div>
    <div class="tip step" style="margin-top:18px"><b>„Common Rail“ heißt „gemeinsame Leiste“</b>Alle Injektoren hängen am selben Rail. Der Druck ist immer da – das Steuergerät bestimmt nur, wann und wie lange jeder Injektor öffnet. Überschüssiger Kraftstoff fließt über den Rücklauf zurück in den Tank.</div>'''),
    folie(T, 'Typische Drücke', '''    <div class="values">
      <div class="val step from-left"><b>ca. 3–6 bar</b><span>Niederdruck nach der Vorförderpumpe</span></div>
      <div class="val step from-left"><b>ca. 250–400 bar</b><span>Raildruck im Leerlauf</span></div>
      <div class="val step from-left"><b>über 2.000 bar</b><span>Raildruck bei Volllast (je nach System bis ca. 2.500 bar)</span></div>
      <div class="val step from-left"><b>ca. 200 bar</b><span>so viel braucht es mindestens, damit der Motor startet</span></div>
    </div>
    <div class="note step">Richtwerte – genaue Werte laut Herstellerangabe. Raildruck Soll und Ist im Diagnosegerät vergleichen.</div>'''),
    folie(T, 'Injektoren', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Magnetventil-Injektor</div>
        <ul UL><li>eine Spule öffnet ein Steuerventil</li><li>der Kraftstoffdruck hebt die Düsennadel</li><li>etwas langsamer, robust</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Piezo-Injektor</div>
        <ul UL><li>ein Piezo-Stapel dehnt sich bei Spannung aus</li><li>schaltet sehr schnell – viele Einspritzungen möglich</li><li>leiser, genauer</li></ul></div>
      <div class="warn step" style="grid-column:1/-1"><b>Hohe Ansteuerspannung</b>Injektoren werden mit deutlich mehr als 12 V angesteuert – keine Prüflampe, nicht in den Stecker stechen. Prüfen nur mit Diagnosegerät, Oszilloskop und Prüfadapter.</div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Einspritzverlauf – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-e="vor">Voreinspritzung</button><button class="btn ghost on" data-e="haupt">Haupteinspritzung</button><button class="btn ghost on" data-e="nach">Nacheinspritzung</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {VERLAUF}
      <div class="card" id="ev-t" style="font-size:17px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Tippe die Einspritzungen an und aus. Vereinfachte Darstellung.</p>''', sid='s-ev', body_cls='body noclick'),
    folie(T, 'Sicher arbeiten', '''    <div class="warn step"><b>Hochdruck – Verletzungsgefahr</b>Ein Kraftstoffstrahl mit über 1.000 bar durchdringt die Haut. Bei laufendem Motor nie an Hochdruckleitungen fassen oder nach Lecks tasten.</div>
    <div class="warn step" style="margin-top:12px"><b>Vor dem Öffnen</b>Motor aus und warten, bis der Druck abgebaut ist – Vorgabe und Wartezeit laut Hersteller.</div>
    <div class="tip step" style="margin-top:12px"><b>Absolute Sauberkeit</b>Schon kleinste Schmutzteilchen zerstören Pumpe und Injektoren. Offene Anschlüsse sofort mit Schutzkappen verschließen. Hochdruckleitungen nach dem Lösen meist erneuern.</div>'''),
    folie(T, 'Common-Rail prüfen', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher und Raildruck lesen<small>Soll und Ist im Diagnosegerät vergleichen – auch beim Starten</small></li>
      <li class="step">Mengenabgleich ansehen<small>Korrekturwerte pro Zylinder – ein Ausreißer zeigt den auffälligen Injektor</small></li>
      <li class="step">Rücklaufmenge messen<small>Rücklauf jedes Injektors in Messgläser – ein Injektor mit viel mehr Rücklauf ist verschlissen</small></li>
      <li class="step">Nach Injektortausch: Codierung<small>den Code vom Injektor im Steuergerät eintragen</small></li>
    </ol>'''),
    video(T, 'mm-common-rail'),
    kurztest(T, [
        ('Welche Aufgabe hat das Rail?', ['Es kühlt den Kraftstoff', 'Es ist der Hochdruckspeicher für alle Injektoren', 'Es filtert Wasser aus dem Diesel'], 1, 'Alle Injektoren hängen am selben Rail – der Druck ist immer da.'),
        ('Wie hoch ist der Raildruck bei Volllast etwa (Richtwert)?', ['ca. 5 bar', 'ca. 50 bar', 'über 2.000 bar'], 2, 'Moderne Systeme arbeiten mit über 2.000 bar.'),
        ('Wozu dient die Voreinspritzung?', ['Die Verbrennung wird weicher und leiser', 'Sie reinigt den Partikelfilter', 'Sie kühlt die Injektoren'], 0, 'Eine kleine Menge vorab macht den Druckanstieg sanfter – das typische Nageln wird leiser.'),
        ('Ein Injektor hat beim Rücklauftest viel mehr Rücklauf als die anderen. Was bedeutet das?', ['Er ist in Ordnung', 'Er ist verschlissen', 'Der Tank ist zu voll'], 1, 'Viel Rücklauf heißt: Der Injektor ist innen undicht.'),
    ]),
    merke(T, ['Vorförderpumpe → Filter → Hochdruckpumpe → Rail → Injektoren', 'Raildruck bis über 2.000 bar',
              'Vor-, Haupt- und Nacheinspritzung', 'Hochdruck: Lebensgefahr, absolute Sauberkeit']),
]
rail_js = '''<script>
(function () {
  const T = {
    vor: '<b>Voreinspritzung:</b> eine kleine Menge vorab. Die Verbrennung startet sanfter – das typische Diesel-Nageln wird leiser.',
    haupt: '<b>Haupteinspritzung:</b> der größte Teil des Kraftstoffs – sie erzeugt die Leistung.',
    nach: '<b>Nacheinspritzung:</b> nach der Verbrennung, z. B. damit der Partikelfilter heiß genug zum Freibrennen wird.'
  };
  const bt = document.querySelectorAll('#s-ev [data-e]');
  function upd(last) {
    bt.forEach(b => document.getElementById('ev-' + b.dataset.e).style.opacity = b.classList.contains('on') ? 1 : 0.12);
    const k = last || 'haupt';
    document.getElementById('ev-t').innerHTML = T[k] + (document.querySelector('#s-ev [data-e="' + k + '"]').classList.contains('on') ? '' : '<br><span class="muted">– gerade ausgeschaltet –</span>');
  }
  bt.forEach(b => b.onclick = () => { b.classList.toggle('on'); upd(b.dataset.e); });
  upd('vor');
})();
</script>'''

# ---------------------------------------------------------------- Luft, Turbo, AGR
T = 'TURBO UND AGR'
luft = [
    titel_folie(K, 'T', 'Turbo und AGR', 'Aufladung und Abgasrückführung beim Diesel'),
    lernziele(T, ['Wie ein Abgasturbolader arbeitet', 'Wozu Ladeluftkühler und VTG dienen',
                  'Was die Abgasrückführung (AGR) macht', 'Typische Fehler finden']),
    folie(T, 'So arbeitet der Turbolader', '''    <ol class="steps-list">
      <li class="step">Das heiße <span class="c">Abgas</span> treibt die Turbine an<small>Energie, die sonst ungenutzt aus dem Auspuff geht</small></li>
      <li class="step">Auf derselben Welle sitzt der <span class="c">Verdichter</span><small>er dreht mit – bis über 200.000 1/min (Richtwert)</small></li>
      <li class="step">Der Verdichter drückt <span class="c">mehr Luft</span> in den Motor<small>mehr Luft = es kann mehr Kraftstoff verbrannt werden = mehr Leistung</small></li>
      <li class="step">Der <span class="c">Ladeluftkühler</span> kühlt die verdichtete Luft<small>kalte Luft ist dichter – noch mehr Sauerstoff im Zylinder</small></li>
    </ol>'''),
    folie(T, 'Ladedruck – zum Ausprobieren', '''    <div class="ctrl"><span style="width:280px">Drehzahl: <span class="c" id="lt-n">1.500 1/min</span></span><input type="range" id="lt" min="800" max="4500" step="100" value="1500"></div>
    <div class="choice" style="margin:12px 0"><button class="btn ghost on" data-v="1">mit VTG</button><button class="btn ghost" data-v="0">ohne VTG</button></div>
    <div class="grid2" style="align-items:center">
      <div class="card"><div class="muted" style="font-size:15px;font-weight:800">LADEDRUCK (ABSOLUT)</div><div class="lcd2" id="lt-p" style="font-size:34px;margin-top:6px">—</div>
        <div style="height:16px;background:var(--card2);border-radius:8px;margin-top:12px;overflow:hidden"><div id="lt-bar" style="height:100%;width:0;background:var(--c);transition:width .2s"></div></div></div>
      <div class="card" id="lt-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Beispielwerte. 1 bar absolut = kein Ladedruck (Umgebungsdruck).</p>''', sid='s-lt', body_cls='body noclick'),
    folie(T, 'Abgasrückführung (AGR)', '''    <div class="kette">
      <div class="glied step"><b>Abgas</b><span>ein Teil wird abgezweigt</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>AGR-Kühler und AGR-Ventil</b><span>das Steuergerät bestimmt die Menge</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Ansaugluft</b><span>weniger Sauerstoff, kühlere Verbrennung</span></div>
    </div>
    <div class="tip step" style="margin-top:20px"><b>Warum das Ganze?</b>Bei sehr heißer Verbrennung entstehen viele Stickoxide (NOx). Mit Abgas in der Ansaugluft brennt es kühler – es entstehen weniger Stickoxide.</div>'''),
    folie(T, 'AGR-Menge – zum Ausprobieren', '''    <div class="ctrl"><span style="width:280px">AGR-Rate: <span class="c" id="agr-v">20 %</span></span><input type="range" id="agr" min="0" max="50" step="5" value="20"></div>
    <div class="grid2" style="margin-top:16px;align-items:center">
      <div class="card">
        <div style="font-weight:800;margin-bottom:6px">Stickoxide (NOx)</div>
        <div style="height:22px;background:var(--card2);border-radius:8px;overflow:hidden"><div id="agr-nox" style="height:100%;background:var(--red);transition:width .2s"></div></div>
        <div style="font-weight:800;margin:16px 0 6px">Ruß</div>
        <div style="height:22px;background:var(--card2);border-radius:8px;overflow:hidden"><div id="agr-russ" style="height:100%;background:var(--muted);transition:width .2s"></div></div>
      </div>
      <div class="card" id="agr-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Beispiel, vereinfacht – das Steuergerät sucht immer den besten Mittelweg.</p>''', sid='s-agr', body_cls='body noclick'),
    folie(T, 'Typische Fehler', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Leistungsverlust, Notlauf</b>Undichter Ladeluftschlauch oder Ladeluftkühler – Ladedruck Soll/Ist vergleichen, Abdrücken.</div>
      <div class="tip step"><b>VTG klemmt</b>Verrußte Leitschaufeln: Ladedruck zu niedrig oder zu hoch (Überladung).</div>
      <div class="tip step"><b>AGR-Ventil verkokt</b>Bleibt offen oder geht nicht auf – schwarzer Rauch, Ruckeln, Fehlerspeicher.</div>
      <div class="warn step"><b>Öl im Ladeluftsystem</b>Etwas Ölnebel ist normal. Viel Öl: Turbolader prüfen – im schlimmsten Fall kann der Motor „durchgehen“.</div>
    </div>'''),
    folie(T, 'Turbo schonen', '''    <ol class="steps-list">
      <li class="step">Kalt nicht voll belasten<small>das Öl muss erst warm werden und überall hinkommen</small></li>
      <li class="step">Nach starker Belastung kurz nachlaufen lassen<small>damit der heiße Lader abkühlt und das Öl nicht verkokt</small></li>
      <li class="step">Ölwechsel nach Vorgabe, richtiges Öl<small>die Lagerung des Laders braucht sauberes Öl</small></li>
      <li class="step">Beim Tausch: Ursache finden<small>Ölzulauf, Ölrücklauf und Luftfilter prüfen – sonst geht der neue Lader auch kaputt</small></li>
    </ol>'''),
    video(T, 'mm-diesel-turbo'),
    kurztest(T, [
        ('Was treibt die Turbine des Abgasturboladers an?', ['Der Keilriemen', 'Das Abgas', 'Ein Elektromotor'], 1, 'Das heiße Abgas treibt die Turbine, auf derselben Welle sitzt der Verdichter.'),
        ('Wozu dient der Ladeluftkühler?', ['Kühle Luft ist dichter – mehr Sauerstoff im Zylinder', 'Er kühlt das Motoröl', 'Er wärmt den Motor schneller auf'], 0, 'Beim Verdichten wird die Luft warm, gekühlt passt mehr hinein.'),
        ('Was bewirkt die Abgasrückführung?', ['Mehr Leistung', 'Weniger Ruß', 'Weniger Stickoxide (NOx)'], 2, 'Die Verbrennung wird kühler – es entstehen weniger Stickoxide.'),
        ('Der Motor geht in Notlauf, Ladedruck zu niedrig. Was prüfst du zuerst?', ['Ladeluftschläuche auf Undichtigkeit', 'Die Zündkerzen', 'Den Reifendruck'], 0, 'Ein undichter Schlauch ist ein häufiger Grund für zu wenig Ladedruck.'),
    ]),
    merke(T, ['Abgas treibt Turbine, Verdichter drückt Luft in den Motor', 'Ladeluftkühler: kühle Luft ist dichter',
              'AGR: weniger Stickoxide|zu viel AGR macht Ruß', 'Turbo: warm fahren, nachlaufen lassen']),
]
luft_js = '''<script>
(function () {
  const lt = document.getElementById('lt'); let vtg = 1;
  const vb = document.querySelectorAll('#s-lt [data-v]');
  function l() {
    const n = +lt.value;
    const k = vtg ? Math.min(1, (n - 800) / 1200) : Math.max(0, Math.min(1, (n - 1600) / 1600));
    const p = 1 + 1.4 * k;
    document.getElementById('lt-n').textContent = n.toLocaleString('de-DE') + ' 1/min';
    document.getElementById('lt-p').textContent = 'ca. ' + p.toFixed(1).replace('.', ',') + ' bar';
    document.getElementById('lt-bar').style.width = (k * 100) + '%';
    let t;
    if (vtg) t = n < 2000 ? '<b>VTG:</b> Bei niedriger Drehzahl stellen sich die Leitschaufeln eng. Das Abgas strömt schneller auf die Turbine – schon früh viel Ladedruck.' : '<b>VTG:</b> Bei hoher Drehzahl öffnen die Leitschaufeln weit, damit der Ladedruck nicht zu hoch wird.';
    else t = n < 2400 ? '<b>Ohne VTG:</b> Bei niedriger Drehzahl ist zu wenig Abgas da – der Lader kommt kaum auf Touren („Turboloch“).' : '<b>Ohne VTG:</b> Erst bei höherer Drehzahl baut sich Ladedruck auf.';
    document.getElementById('lt-t').innerHTML = t;
    vb.forEach(x => x.classList.toggle('on', +x.dataset.v === vtg));
  }
  lt.addEventListener('input', l); vb.forEach(x => x.onclick = () => { vtg = +x.dataset.v; l(); }); l();

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
</script>'''

STYLE = '  .symbol { font-size: 110px; }'

if __name__ == '__main__':
    seite('mm-diesel-grundlagen.html', 'Diesel-Grundlagen – Motormanagement', 't-mm4', THEMA, grundlagen, STYLE, grundlagen_js)
    seite('mm-common-rail.html', 'Common-Rail – Motormanagement', 't-mm4', THEMA, rail, STYLE, rail_js)
    seite('mm-diesel-turbo.html', 'Turbo und AGR – Motormanagement', 't-mm4', THEMA, luft, STYLE, luft_js)
    print('ok')
