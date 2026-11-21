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

# ---------------------------------------------------------------- Pumpe-Düse
T = 'PUMPE-DÜSE'
PDSVG = """<svg viewBox="0 0 420 340" width="400" height="324" style="display:block;margin:0 auto">
  <g id="pd-hebel" style="transition:transform .5s;transform-origin:160px 110px"><rect x="90" y="102" width="240" height="16" rx="8" fill="#a9b3c1"/><circle cx="115" cy="122" r="9" fill="#6b7686"/></g>
  <circle cx="160" cy="110" r="7" fill="#3b4250" stroke="#ecf1f8" stroke-width="2"/>
  <text x="160" y="90" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Kipphebel</text>
  <circle cx="115" cy="165" r="26" fill="#3b4250" stroke="#94a4ba" stroke-width="3"/>
  <g id="pd-nocke" style="transition:transform .5s;transform-origin:115px 165px"><path d="M93 178 Q115 210 137 178 Z" fill="#6b7686"/></g>
  <text x="115" y="214" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Nocke</text>
  <rect x="270" y="125" width="60" height="155" rx="6" fill="#213552" stroke="#94a4ba" stroke-width="2"/>
  <rect id="pd-kammer" x="276" y="198" width="48" height="72" fill="#28aaf5" style="transition:fill .4s"/>
  <rect id="pd-kolben" x="280" y="118" width="40" height="80" rx="4" fill="#c9c3b6"/>
  <rect x="330" y="215" width="60" height="40" rx="8" fill="#213552" stroke="#94a4ba" stroke-width="2"/>
  <text x="360" y="240" text-anchor="middle" font-size="12" font-weight="800" fill="#ecf1f8">Ventil</text>
  <text id="pd-vz" x="360" y="272" text-anchor="middle" font-size="13" font-weight="800" fill="#34c778">offen</text>
  <path d="M290 280 L310 280 L304 310 L296 310 Z" fill="#94a4ba"/>
  <g id="pd-spray" style="opacity:0;transition:opacity .3s"><path d="M300 312 L270 340 M300 312 L300 340 M300 312 L330 340" stroke="#e6d27a" stroke-width="4" stroke-linecap="round"/></g>
  <text x="240" y="300" text-anchor="end" font-size="13" font-weight="800" fill="#94a4ba">Düse</text>
</svg>"""

pd = [
    titel_folie(K, 'PD', 'Pumpe-Düse', 'Pumpe und Einspritzdüse in einem Bauteil', 'font-size:90px'),
    lernziele(T, ['Wie eine Pumpe-Düse-Einheit aufgebaut ist', 'Wie der Druck erzeugt wird',
                  'Vor- und Nachteile gegenüber Common-Rail', 'Einbau, Prüfen und typische Fehler']),
    folie(T, 'Aufbau', """    <div class="kette">
      <div class="glied step"><b>Nockenwelle</b><span>eine zusätzliche Nocke pro Zylinder</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Rollenkipphebel</b><span>drückt den Pumpenkolben nach unten</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Pumpe-Düse-Einheit</b><span>Pumpe, Magnetventil und Düse in einem Bauteil</span></div>
    </div>
    <div class="grid2" style="margin-top:18px">
      <div class="tip step"><b>Jeder Zylinder hat seine eigene Einheit</b>Sie sitzt im Zylinderkopf. Hochdruckleitungen gibt es nicht.</div>
      <div class="tip step"><b>Kraftstoffversorgung</b>Eine Kraftstoffpumpe liefert den Diesel mit Vordruck über Kanäle im Zylinderkopf zu den Einheiten.</div>
    </div>"""),
    folie(T, 'So entsteht der Druck – zum Ausprobieren', f"""    <div class="choice" style="margin-bottom:12px"><button class="btn ghost" data-p="0">1. Saughub</button><button class="btn ghost" data-p="1">2. Vorhub</button><button class="btn ghost" data-p="2">3. Einspritzung</button><button class="btn ghost" data-p="3">4. Ende</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.1fr 1fr">
      {PDSVG}
      <div>
        <div class="card"><div class="muted" style="font-size:15px;font-weight:800">DRUCK IN DER EINHEIT</div><div class="lcd2" id="pd-d" style="font-size:32px;margin-top:6px">—</div></div>
        <div class="card" id="pd-t" style="margin-top:12px;font-size:17px;font-weight:600;line-height:1.5"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:10px 0 0">Vereinfachte Darstellung, Richtwert.</p>""", sid='s-pd', body_cls='body noclick'),
    folie(T, 'Pumpe-Düse und Common-Rail', """    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Pumpe-Düse</div>
        <ul UL><li>sehr hoher Druck – bis ca. 2.000 bar (Richtwert)</li><li>keine Hochdruckleitungen</li><li>Druck hängt von der Nockenwelle und der Drehzahl ab</li><li>lauter, weniger Einspritzungen pro Takt möglich</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Common-Rail</div>
        <ul UL><li>Druck immer verfügbar – unabhängig von der Drehzahl</li><li>viele Einspritzungen pro Takt</li><li>leiser, sauberere Abgase</li><li>hat die Pumpe-Düse abgelöst</li></ul></div>
    </div>
    <div class="note step">Pumpe-Düse findest du vor allem bei älteren TDI-Motoren – sie kommen aber noch oft in die Werkstatt.</div>""".replace('UL', UL)),
    folie(T, 'Einbau und Einstellen', """    <ol class="steps-list">
      <li class="step">Neue Dichtringe und Schrauben<small>immer laut Teileliste – alte O-Ringe nicht wiederverwenden</small></li>
      <li class="step">Einheit gerade einsetzen, Spannpratze nach Vorgabe anziehen<small>Drehmoment und Drehwinkel laut Hersteller</small></li>
      <li class="step">Grundeinstellung am Kipphebel<small>Einstellschraube nach Herstellervorgabe einstellen, z. B. mit Messuhr</small></li>
      <li class="step">Fehlerspeicher, Messwerte, Probefahrt<small>Laufruhe der Zylinder kontrollieren</small></li>
    </ol>"""),
    folie(T, 'Prüfen und typische Fehler', """    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Messwerte</b>Laufruhe- bzw. Mengenabweichung pro Zylinder vergleichen – ein Ausreißer zeigt die auffällige Einheit.</div>
      <div class="warn step"><b>Ölstand steigt</b>Undichte O-Ringe: Diesel gelangt ins Motoröl. Ölstand und Ölgeruch prüfen – Motorschaden möglich.</div>
      <div class="tip step"><b>Kabelbaum im Zylinderkopf</b>Scheuerstellen oder Öl im Stecker führen zu Aussetzern – Kabel und Stecker prüfen.</div>
      <div class="warn step"><b>Magnetventil</b>Hohe Ansteuerspannung – keine Prüflampe, nicht in den Stecker stechen. Prüfen mit Diagnosegerät und Prüfadapter.</div>
    </div>"""),
    video(T, 'mm-pumpe-duese'),
    kurztest(T, [
        ('Wodurch wird bei der Pumpe-Düse der Druck erzeugt?', ['Durch die Nockenwelle über einen Kipphebel', 'Durch eine Hochdruckpumpe am Rail', 'Durch den Turbolader'], 0, 'Eine zusätzliche Nocke drückt über den Rollenkipphebel den Pumpenkolben nach unten.'),
        ('Wann beginnt die Einspritzung?', ['Wenn das Magnetventil öffnet', 'Wenn das Magnetventil schließt', 'Beim Saughub'], 1, 'Erst wenn das Ventil schließt, kann sich der Druck aufbauen und die Düse öffnet.'),
        ('Der Ölstand steigt bei einem Pumpe-Düse-Motor. Was kann die Ursache sein?', ['Zu viel AdBlue', 'Neue Zündkerzen', 'Undichte O-Ringe an den Pumpe-Düse-Einheiten'], 2, 'Diesel gelangt ins Öl – das verdünnt das Motoröl.'),
        ('Was ist ein Vorteil von Common-Rail gegenüber Pumpe-Düse?', ['Der Druck ist unabhängig von der Drehzahl verfügbar', 'Es gibt keine Injektoren', 'Es braucht keinen Kraftstofffilter'], 0, 'Darum sind viele Einspritzungen pro Takt möglich.'),
    ]),
    merke(T, ['Pumpe, Magnetventil und Düse in einem Bauteil', 'Nocke + Kipphebel erzeugen den Druck|bis ca. 2.000 bar',
              'Ventil zu = Einspritzung', 'Ölstand steigt? O-Ringe prüfen']),
]
pd_js = """<script>
(function () {
  const P = [
    [118, '#28aaf5', 'offen', '#34c778', 0, 0, 0, 'ca. Vordruck', '<b>Saughub:</b> Die Feder drückt den Kolben nach oben. Diesel strömt in den Raum unter dem Kolben.'],
    [133, '#28aaf5', 'offen', '#34c778', 0, 140, 6.2, 'ca. Vordruck', '<b>Vorhub:</b> Die Nocke drückt den Kolben nach unten. Das Ventil ist offen – der Diesel wird zurück in den Zulauf gedrückt. Noch keine Einspritzung.'],
    [148, '#ff8f3f', 'zu', '#f05e4e', 1, 170, 12.4, 'bis ca. 2.000 bar', '<b>Einspritzung:</b> Das Steuergerät schließt das Magnetventil. Der Druck steigt stark an, die Düsennadel öffnet – der Diesel wird eingespritzt. Wie lange das Ventil zu bleibt, bestimmt die Menge.'],
    [158, '#28aaf5', 'offen', '#34c778', 0, 190, 16.6, 'fällt ab', '<b>Ende:</b> Das Magnetventil öffnet wieder. Der Druck bricht zusammen, die Düse schließt.']
  ];
  const bt = document.querySelectorAll('#s-pd [data-p]');
  function p(i) {
    const s = P[i];
    document.getElementById('pd-kolben').setAttribute('y', s[0]);
    const k = document.getElementById('pd-kammer'); k.setAttribute('y', s[0] + 80); k.setAttribute('height', Math.max(6, 270 - (s[0] + 80))); k.setAttribute('fill', s[1]);
    const vz = document.getElementById('pd-vz'); vz.textContent = s[2]; vz.setAttribute('fill', s[3]);
    document.getElementById('pd-spray').style.opacity = s[4];
    document.getElementById('pd-nocke').style.transform = 'rotate(' + s[5] + 'deg)';
    document.getElementById('pd-hebel').style.transform = 'rotate(' + s[6] + 'deg)';
    document.getElementById('pd-d').textContent = s[7];
    document.getElementById('pd-t').innerHTML = s[8];
    bt.forEach(x => x.classList.toggle('on', +x.dataset.p === i));
  }
  bt.forEach(x => x.onclick = () => p(+x.dataset.p));
  document.getElementById('s-pd').addEventListener('slideshow', () => p(0));
  p(0);
})();
</script>"""

STYLE = '  .symbol { font-size: 110px; }'

if __name__ == '__main__':
    seite('mm-diesel-grundlagen.html', 'Diesel-Grundlagen – Motormanagement', 't-mm4', THEMA, grundlagen, STYLE, grundlagen_js)
    seite('mm-common-rail.html', 'Common-Rail – Motormanagement', 't-mm4', THEMA, rail, STYLE, rail_js)
    seite('mm-pumpe-duese.html', 'Pumpe-Düse – Motormanagement', 't-mm4', THEMA, pd, STYLE, pd_js)
    print('ok')
