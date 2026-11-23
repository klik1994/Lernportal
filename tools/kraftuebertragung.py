"""Kraftübertragung – vier Präsentationen.
Aufruf: cd tools && python3 kraftuebertragung.py"""
from praesentation_bauen import *

K = 'KRAFTÜBERTRAGUNG'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'
STYLE = '''  .symbol { font-size: 80px; }
  .rb { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; font-size: 44px; font-weight: 900; margin: 6px 0 14px; }
  .rb span { cursor: pointer; padding: 4px 18px; border-radius: 12px; background: var(--card); transition: background .2s, color .2s; }
  .rb span.on { background: var(--c); color: var(--on-c); }
  html.light svg text[fill="#ffd34d"] { fill: #8a6400; }
  @media (max-width: 820px), (max-height: 520px) { .rb { font-size: 30px; } .val b { font-size: 14px; hyphens: auto; overflow-wrap: anywhere; } }'''


def btns(attr, items, first=0):
    return ''.join(f'<button class="btn ghost{" on" if i == first else ""}" data-{attr}="{k}">{t}</button>' for i, (k, t) in enumerate(items))


def svgbox(pid, w, h):
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="display:block;margin:0 auto;max-width:100%;height:auto" id="{pid}-svg">
      <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#18283f"/><g id="{pid}-g"></g></svg>'''


def fehlerfolie(T, titel, sid, items):
    return folie(T, titel, f'''    <div class="choice" style="margin-bottom:12px;flex-wrap:wrap;gap:6px">{btns('f', [(str(i), n) for i, n in enumerate(items)])}</div>
    <div class="grid2" style="align-items:start">
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">MÖGLICHE URSACHEN</div><ul class="fe-u" style="font-size:16px;line-height:1.55;padding-left:20px;margin:8px 0 0"></ul></div>
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">SO PRÜFST DU</div><ul class="fe-p" style="font-size:16px;line-height:1.55;padding-left:20px;margin:8px 0 0"></ul></div>
    </div>''', sid=sid, body_cls='body noclick')


def fehler_js(sid, daten):
    import json
    return f'''  (function () {{
    const FE = {json.dumps(daten, ensure_ascii=False)};
    const s = document.getElementById('{sid}'), fb = s.querySelectorAll('[data-f]');
    function fe(i) {{
      s.querySelector('.fe-u').innerHTML = FE[i][0].map(x => '<li>' + x + '</li>').join('');
      s.querySelector('.fe-p').innerHTML = FE[i][1].map(x => '<li>' + x + '</li>').join('');
      fb.forEach(x => x.classList.toggle('on', +x.dataset.f === i));
    }}
    fb.forEach(x => x.onclick = () => fe(+x.dataset.f)); fe(0);
  }})();
'''


# ================================================================ 1 Kupplung
T = 'KUPPLUNG'

kupplung = [
    titel_folie(K, 'K', 'Die Kupplung', 'Aufgaben, Aufbau, Betätigung, Zweimassenschwungrad, Fehler', 'font-size:130px'),
    lernziele(T, ['Welche Aufgaben die Kupplung hat', 'Wie eine Einscheiben-Trockenkupplung aufgebaut ist und arbeitet',
                  'Wie die Kupplung betätigt wird', 'Was ein Zweimassenschwungrad macht und wie du Fehler erkennst']),
    folie(T, 'Aufgaben der Kupplung', '''    <div class="values">
      <div class="val step from-left"><b>Anfahren</b><span>Kraftschluss zwischen Motor und Getriebe sanft herstellen</span></div>
      <div class="val step from-left"><b>Schalten</b><span>Kraftfluss kurz trennen, damit der Gang gewechselt werden kann</span></div>
      <div class="val step from-left"><b>Dämpfen</b><span>Drehschwingungen des Motors abbauen (Torsionsdämpfer)</span></div>
      <div class="val step from-left"><b>Schützen</b><span>bei Überlast rutscht die Kupplung, bevor Teile brechen</span></div>
    </div>'''),
    folie(T, 'So arbeitet die Kupplung – zum Ausprobieren', f'''    <div class="ctrl"><span style="width:260px">Kupplungspedal: <span class="c" id="kp-n">0 %</span></span><input type="range" id="kp" min="0" max="100" step="1" value="0"></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.25fr 1fr;margin-top:8px">
      {svgbox('kp', 600, 330)}
      <div>
        <div class="grid2" style="gap:10px"><div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">MOTOR</div><div class="lcd2" id="kp-mo" style="font-size:24px">2.000 1/min</div></div>
        <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">GETRIEBE-EINGANG</div><div class="lcd2" id="kp-ge" style="font-size:24px">2.000 1/min</div></div></div>
        <div class="card" id="kp-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px"></div>
      </div>
    </div>''', sid='s-kp', body_cls='body noclick'),
    folie(T, 'Aufbau und Betätigung', '''    <div class="values">
      <div class="val step from-left"><b>Schwungrad</b><span>sitzt auf der Kurbelwelle – Reibfläche für die Kupplungsscheibe</span></div>
      <div class="val step from-left"><b>Kupplungs­scheibe</b><span>Reibbeläge und Torsionsdämpfer (Federn), sitzt auf der Getriebe-Eingangswelle</span></div>
      <div class="val step from-left"><b>Druckplatte</b><span>mit Tellerfeder – presst die Scheibe gegen das Schwungrad</span></div>
      <div class="val step from-left"><b>Ausrücklager</b><span>drückt auf die Tellerfeder – oft als Zentralausrücker</span></div>
      <div class="val step from-left"><b>Betätigung</b><span>hydraulisch: Geberzylinder am Pedal → Nehmerzylinder am Getriebe</span></div>
    </div>
    <p class="muted" style="font-size:14px">Die Kupplungshydraulik nutzt oft die Bremsflüssigkeit aus dem gemeinsamen Behälter – laut Hersteller.</p>'''),
    folie(T, 'Das Zweimassenschwungrad', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Aufbau und Aufgabe</div>
        <ul UL><li>zwei Schwungmassen, dazwischen Bogenfedern</li><li>die Federn schlucken die Drehschwingungen des Motors</li><li>das Getriebe läuft ruhiger, kein Dröhnen – besonders bei Dieselmotoren</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Fehler und Prüfen</div>
        <ul UL><li>Klappern im Leerlauf, Schlag beim Abstellen, Vibrationen beim Anfahren</li><li>Verdrehspiel und Kippspiel mit Spezialwerkzeug messen – Grenzwerte laut Hersteller</li><li>beim Kupplungstausch immer mit prüfen</li></ul></div>
    </div>'''.replace('UL', UL)),
    fehlerfolie(T, 'Fehlerbilder – zum Ausprobieren', 's-kf', ['Kupplung rutscht', 'Trennt nicht', 'Rupft beim Anfahren', 'Geräusch beim Treten', 'Pedal bleibt unten']),
    folie(T, 'Prüfen und Tauschen', '''    <ol class="steps-list">
      <li class="step">Rutschtest auf der Probefahrt<small>hoher Gang, niedrige Drehzahl, kräftig Gas geben: Die Drehzahl darf nicht hochlaufen, ohne dass das Fahrzeug schneller wird</small></li>
      <li class="step">Hydraulik prüfen<small>Flüssigkeitsstand, Dichtheit an Geber- und Nehmerzylinder, ggf. entlüften</small></li>
      <li class="step">Beim Tausch: komplett erneuern<small>Scheibe, Druckplatte und Ausrücklager als Satz – Zweimassenschwungrad prüfen</small></li>
      <li class="step">Scheibe zentrieren<small>mit Zentrierdorn, Druckplatte über Kreuz mit Drehmoment laut Hersteller anziehen</small></li>
      <li class="step">Getriebe abstützen<small>nie an der Eingangswelle hängen lassen – Getriebeheber verwenden</small></li>
    </ol>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Kupplungsstaub</b>Nicht mit Druckluft wegblasen – absaugen oder feucht reinigen.</div>
      <div class="tip step"><b>Verzahnung</b>Nabe der Kupplungsscheibe nur ganz dünn mit dem vorgeschriebenen Fett versehen – zu viel Fett landet auf dem Belag.</div>
      <div class="tip step"><b>Kundentipp</b>An der Ampel nicht dauerhaft mit getretener Kupplung stehen – das belastet das Ausrücklager.</div>
      <div class="tip step"><b>Nach dem Tausch</b>Bei manchen Fahrzeugen den Kupplungspedalsensor oder die Kupplung mit dem Tester anlernen – laut Hersteller.</div>
    </div>'''),
    video(T, 'ku-kupplung'),
    kurztest(T, [
        ('Was presst die Kupplungsscheibe gegen das Schwungrad?', ['Das Ausrücklager', 'Die Druckplatte mit der Tellerfeder', 'Der Nehmerzylinder'], 1, 'Beim Treten drückt das Ausrücklager die Tellerfeder – die Druckplatte hebt ab.'),
        ('Die Motordrehzahl steigt beim Gasgeben, das Fahrzeug wird aber kaum schneller. Was ist das?', ['Die Kupplung rutscht', 'Die Kupplung trennt nicht', 'Das ZMS klappert'], 0, 'Belag verschlissen oder verölt.'),
        ('Wozu dient das Zweimassenschwungrad?', ['Es ersetzt die Kupplung', 'Es lädt die Batterie', 'Es dämpft die Drehschwingungen des Motors'], 2, 'Mit Bogenfedern zwischen zwei Schwungmassen.'),
        ('Was tauschst du bei einem Kupplungstausch?', ['Nur die Scheibe', 'Scheibe, Druckplatte und Ausrücklager als Satz', 'Nur das Pedal'], 1, 'Zweimassenschwungrad dabei prüfen.'),
    ]),
    merke(T, ['Anfahren, Schalten, Dämpfen, Schützen', 'Druckplatte presst – Ausrücklager trennt',
              'Kupplung rutscht: Drehzahl steigt, Auto nicht schneller', 'Satz tauschen, ZMS prüfen, Getriebe abstützen']),
]
kupplung_js = '''<script>
(function () {
  const g = (id, s) => document.getElementById(id).innerHTML = s;
  const kp = document.getElementById('kp');
  let wm = 0, wg = 0, ng = 2000, nm = 2000;
  function zeichne() {
    const p = +kp.value / 100, auf = p < 0.35 ? 0 : p > 0.6 ? 1 : (p - 0.35) / 0.25;
    const lift = auf * 14, cx = 200, cy = 165;
    let o = '';
    o += '<line x1="20" y1="' + cy + '" x2="150" y2="' + cy + '" stroke="#94a4ba" stroke-width="14"/><text x="30" y="' + (cy - 18) + '" font-size="13" font-weight="800" fill="#94a4ba">Kurbelwelle</text>';
    o += '<line x1="240" y1="' + cy + '" x2="580" y2="' + cy + '" stroke="#94a4ba" stroke-width="12"/><text x="430" y="' + (cy + 34) + '" font-size="13" font-weight="800" fill="#94a4ba">Getriebe-Eingangswelle</text>';
    o += '<rect x="150" y="40" width="44" height="250" rx="6" fill="#213552" stroke="#ecf1f8" stroke-width="3"/><text x="144" y="60" text-anchor="end" font-size="13" font-weight="800" fill="#ecf1f8">Schwungrad</text>';
    const sx = 198 + lift * 0.4;
    o += '<rect x="' + sx + '" y="60" width="12" height="210" rx="3" fill="#ffd34d"/><rect x="' + (sx + 2) + '" y="' + (cy - 26) + '" width="8" height="52" fill="#ecf1f8"/>';
    o += '<text x="' + (sx + 6) + '" y="300" text-anchor="middle" font-size="13" font-weight="800" fill="#ffd34d">Scheibe</text>';
    const dx = 214 + lift;
    o += '<rect x="' + dx + '" y="56" width="22" height="218" rx="4" fill="#94a4ba"/>';
    o += '<text x="' + (dx + 11) + '" y="28" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Druckplatte</text>';
    const fx = 290 - auf * 22;
    o += '<path d="M' + (dx + 22) + ' 70 L' + fx + ' ' + (cy - 30) + ' M' + (dx + 22) + ' 260 L' + fx + ' ' + (cy + 30) + '" stroke="#ecf1f8" stroke-width="5" fill="none"/>';
    o += '<path d="M236 50 H300 V280 H236" fill="none" stroke="#94a4ba" stroke-width="3" stroke-dasharray="6 5"/>';
    o += '<text x="304" y="66" font-size="13" font-weight="800" fill="#ecf1f8">Tellerfeder</text>';
    const ax = fx - 4;
    o += '<rect x="' + ax + '" y="' + (cy - 34) + '" width="30" height="68" rx="6" fill="#a07cf5"/><text x="' + (ax + 36) + '" y="' + (cy - 40) + '" font-size="13" font-weight="800" fill="#a07cf5">Ausrücklager</text>';
    const r = (x, a, c) => { const ra = a * Math.PI / 180; return '<circle cx="' + x + '" cy="315" r="10" fill="none" stroke="' + c + '" stroke-width="3"/><line x1="' + x + '" y1="315" x2="' + (x + 10 * Math.sin(ra)) + '" y2="' + (315 - 10 * Math.cos(ra)) + '" stroke="' + c + '" stroke-width="3"/>'; };
    o += r(85, wm, '#ecf1f8') + r(500, wg, '#ffd34d');
    g('kp-g', o);
    nm = 2000; ng = Math.round(2000 * (1 - auf) / 10) * 10;
    document.getElementById('kp-n').textContent = Math.round(p * 100) + ' %';
    document.getElementById('kp-mo').textContent = nm.toLocaleString('de-DE') + ' 1/min';
    document.getElementById('kp-ge').textContent = ng.toLocaleString('de-DE') + ' 1/min';
    document.getElementById('kp-t').innerHTML = auf === 0 ? '<b>Eingekuppelt:</b> Die Tellerfeder drückt die <span class="c">Druckplatte</span> mit großer Kraft gegen die Scheibe und das Schwungrad. Alles dreht gleich schnell – das Drehmoment geht ins Getriebe.'
      : auf === 1 ? '<b>Ausgekuppelt:</b> Das <span class="c">Ausrücklager</span> drückt auf die Mitte der Tellerfeder, die Druckplatte hebt ab. Die Scheibe ist frei – der Kraftfluss ist getrennt, du kannst schalten. (Hier steht das Fahrzeug mit eingelegtem Gang – darum steht auch die Getriebewelle.)'
      : '<b>Schleifpunkt:</b> Die Scheibe <span class="ora">rutscht</span> noch etwas – so fährst du sanft an. Dabei entsteht Wärme und Verschleiß. Darum nicht lange schleifen lassen.';
  }
  setInterval(() => { wm = (wm + 24) % 360; wg = (wg + 24 * ng / 2000) % 360; zeichne(); }, 50);
  kp.addEventListener('input', zeichne); zeichne();
''' + fehler_js('s-kf', [
    [['Kupplungsbelag verschlissen', 'Belag verölt (undichter Wellendichtring an Kurbelwelle oder Getriebe)', 'Druckplatte zu schwach'], ['Rutschtest auf der Probefahrt', 'Getriebe ausbauen, Belagdicke und Ölspuren prüfen']],
    [['Luft im Hydrauliksystem', 'Geber- oder Nehmerzylinder undicht', 'Scheibe klemmt auf der Verzahnung'], ['Flüssigkeitsstand und Dichtheit prüfen', 'Hydraulik entlüften', 'Pedalweg und Ausrückweg prüfen']],
    [['Belag verölt oder verglast', 'Motor- oder Getriebelager defekt', 'Zweimassenschwungrad defekt'], ['Motorlager prüfen', 'ZMS-Spiel messen', 'Kupplung ausbauen und ansehen']],
    [['Ausrücklager defekt', 'Tellerfederzungen verschlissen'], ['Geräusch nur beim Treten? Dann meist Ausrücklager', 'Bei der Reparatur den Kupplungssatz komplett erneuern']],
    [['Luft im System', 'Geberzylinder oder Nehmerzylinder defekt', 'Pedalfeder gebrochen'], ['Flüssigkeitsstand prüfen', 'System entlüften', 'Zylinder auf Undichtigkeit prüfen']],
]) + '''})();
</script>'''


# ================================================================ 2 Schaltgetriebe
T = 'SCHALTGETRIEBE'

schalt = [
    titel_folie(K, 'i', 'Das Schaltgetriebe', 'Übersetzung, Gänge, Aufbau, Synchronisation, Fehler', 'font-size:140px'),
    lernziele(T, ['Warum ein Fahrzeug ein Getriebe braucht', 'Wie du eine Übersetzung berechnest',
                  'Wie ein Schaltgetriebe aufgebaut ist', 'Was die Synchronisation macht und welche Fehler es gibt']),
    folie(T, 'Warum ein Getriebe?', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Das Problem</div>
        <ul UL><li>der Motor arbeitet gut nur in einem bestimmten Drehzahlbereich</li><li>beim Anfahren und am Berg braucht das Auto viel Drehmoment</li><li>bei hoher Geschwindigkeit soll die Drehzahl niedrig bleiben</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Die Lösung</div>
        <ul UL><li>das Getriebe wandelt Drehzahl und Drehmoment</li><li>kleine Gänge: viel Drehmoment, wenig Geschwindigkeit</li><li>große Gänge: wenig Drehmoment, hohe Geschwindigkeit</li><li>dazu Rückwärtsgang und Leerlauf</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Die Übersetzung – zum Ausprobieren', f'''    <div class="ctrl"><span style="width:320px">Zähne treibendes Rad z1: <span class="c" id="ue-1n">15</span></span><input type="range" id="ue-1" min="10" max="40" step="1" value="15"></div>
    <div class="ctrl"><span style="width:320px">Zähne getriebenes Rad z2: <span class="c" id="ue-2n">45</span></span><input type="range" id="ue-2" min="10" max="60" step="1" value="45"></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr;margin-top:8px">
      {svgbox('ue', 560, 300)}
      <div>
        <div class="grid3" style="gap:8px"><div class="card" style="margin:0"><div class="muted" style="font-size:13px;font-weight:800">ÜBERSETZUNG i</div><div class="lcd2" id="ue-i" style="font-size:20px">3,00</div></div>
        <div class="card" style="margin:0"><div class="muted" style="font-size:13px;font-weight:800">DREHZAHL n2</div><div class="lcd2" id="ue-n" style="font-size:20px">–</div></div>
        <div class="card" style="margin:0"><div class="muted" style="font-size:13px;font-weight:800">DREHMOMENT M2</div><div class="lcd2" id="ue-m" style="font-size:20px">–</div></div></div>
        <div class="card" id="ue-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">i = z2 : z1 · n2 = n1 : i · M2 = M1 · i (ohne Verluste). Antrieb hier: 3.000 1/min und 200 Nm.</p>''', sid='s-ue', body_cls='body noclick'),
    folie(T, 'Die Gänge – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap;gap:6px">{btns('g', [('0', '1. Gang'), ('1', '2.'), ('2', '3.'), ('3', '4.'), ('4', '5.'), ('5', '6.'), ('6', 'R')])}</div>
    {svgbox('gg', 640, 230)}
    <div class="card" id="gg-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px"></div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Beispielwerte: Motor 3.000 1/min, Achsantrieb i = 3,9, Reifenumfang 1,95 m.</p>''', sid='s-gg', body_cls='body noclick'),
    folie(T, 'Aufbau', '''    <div class="values">
      <div class="val step from-left"><b>Wellen</b><span>Antriebswelle (von der Kupplung) und Abtriebswelle (zum Achsantrieb)</span></div>
      <div class="val step from-left"><b>Zahnradpaare</b><span>immer im Eingriff, schräg verzahnt – das ist leise</span></div>
      <div class="val step from-left"><b>Losräder</b><span>drehen frei auf der Welle, bis sie geschaltet werden</span></div>
      <div class="val step from-left"><b>Schaltmuffe</b><span>verbindet das Losrad fest mit der Welle – so wird der Gang eingelegt</span></div>
      <div class="val step from-left"><b>Rückwärtsgang</b><span>ein Zwischenrad kehrt die Drehrichtung um</span></div>
    </div>'''),
    folie(T, 'Die Synchronisation – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap">{btns('y', [('ok', 'Synchronring in Ordnung'), ('def', 'Synchronring verschlissen')])}<button class="btn" id="sy-go" style="--c:var(--tea)">▶ Gang einlegen</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {svgbox('sy', 560, 260)}
      <div class="card" id="sy-t" style="font-size:16px;font-weight:600;line-height:1.5"></div>
    </div>''', sid='s-sy', body_cls='body noclick'),
    fehlerfolie(T, 'Fehlerbilder – zum Ausprobieren', 's-sf', ['Gang kracht beim Schalten', 'Gang springt heraus', 'Heulen beim Fahren', 'Ölverlust', 'Schaltet schwer']),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Getriebeöl</b>Oft Lebensdauerfüllung – bei Undichtigkeit Stand an der Kontrollschraube prüfen (meist bis zur Unterkante). Nur Öl laut Hersteller.</div>
      <div class="tip step"><b>Schaltung einstellen</b>Schaltseilzüge oder Gestänge nach Herstellervorgabe einstellen, oft mit Arretierstift.</div>
      <div class="warn step"><b>Aus- und Einbau</b>Getriebe immer mit Getriebeheber abstützen und sichern – es ist schwer.</div>
      <div class="tip step"><b>Rückfahrlicht</b>Der Rückfahrlichtschalter sitzt meist am Getriebe.</div>
    </div>'''),
    video(T, 'ku-schaltgetriebe'),
    kurztest(T, [
        ('Treibendes Rad 15 Zähne, getriebenes Rad 45 Zähne. Wie groß ist i?', ['0,33', '3', '60'], 1, 'i = z2 : z1 = 45 : 15 = 3.'),
        ('Was passiert bei i = 3 mit dem Drehmoment (ohne Verluste)?', ['Es wird dreimal so groß', 'Es bleibt gleich', 'Es wird ein Drittel'], 0, 'Die Drehzahl wird dafür ein Drittel.'),
        ('Was verbindet beim Schalten das Losrad mit der Welle?', ['Die Kupplung', 'Das Zwischenrad', 'Die Schaltmuffe'], 2, 'Vorher gleicht der Synchronring die Drehzahlen an.'),
        ('Ein Gang kracht beim Schalten, obwohl die Kupplung trennt. Was ist wahrscheinlich?', ['Getriebeöl zu kalt', 'Synchronring verschlissen', 'Rückfahrlichtschalter defekt'], 1, 'Er gleicht die Drehzahlen nicht mehr an.'),
    ]),
    merke(T, ['Getriebe wandelt Drehzahl und Drehmoment', 'i = z2 : z1 · n2 = n1 : i · M2 = M1 · i',
              'Schaltmuffe verbindet Losrad mit Welle', 'Synchronring gleicht Drehzahlen an – sonst kracht es']),
]
schalt_js = '''<script>
(function () {
  const g = (id, s) => document.getElementById(id).innerHTML = s;
  const fmt = (v, n) => v.toLocaleString('de-DE', { minimumFractionDigits: n, maximumFractionDigits: n });
  let w1 = 0;
  function rad(cx, cy, z, ang, c) {
    const r = z * 3.2, t = 7; let d = '';
    for (let i = 0; i < z; i++) {
      const a0 = (ang + i * 360 / z) * Math.PI / 180, a1 = a0 + Math.PI / z * 0.5, a2 = a0 + Math.PI / z, a3 = a0 + Math.PI / z * 1.5;
      d += (i ? ' L' : 'M') + (cx + r * Math.cos(a0)) + ' ' + (cy + r * Math.sin(a0)) + ' L' + (cx + (r + t) * Math.cos(a1)) + ' ' + (cy + (r + t) * Math.sin(a1)) + ' L' + (cx + (r + t) * Math.cos(a2)) + ' ' + (cy + (r + t) * Math.sin(a2)) + ' L' + (cx + r * Math.cos(a3)) + ' ' + (cy + r * Math.sin(a3));
    }
    return '<path d="' + d + ' Z" fill="#213552" stroke="' + c + '" stroke-width="3"/><circle cx="' + cx + '" cy="' + cy + '" r="8" fill="' + c + '"/><line x1="' + cx + '" y1="' + cy + '" x2="' + (cx + (r - 6) * Math.cos(ang * Math.PI / 180)) + '" y2="' + (cy + (r - 6) * Math.sin(ang * Math.PI / 180)) + '" stroke="' + c + '" stroke-width="4"/>';
  }
  function ue() {
    const z1 = +document.getElementById('ue-1').value, z2 = +document.getElementById('ue-2').value, i = z2 / z1;
    const r1 = z1 * 3.2, r2 = z2 * 3.2, sc = Math.min(1, 520 / (2 * r1 + 2 * r2 + 40), 250 / (2 * r2 + 20));
    const c1x = 20 + (r1 + 8), c2x = c1x + r1 + r2 + 7;
    let o = '<g transform="translate(' + (280 - (c2x + r2 + 8) * sc / 2) + ' ' + 150 + ') scale(' + sc + ') translate(0 0)">';
    o += rad(c1x, 0, z1, w1, '#ffd34d') + rad(c2x, 0, z2, -w1 / i + 180 / z2, '#1fc8b3') + '</g>';
    o += '<text x="20" y="28" font-size="14" font-weight="800" fill="#ffd34d">treibend (z1 = ' + z1 + ')</text><text x="540" y="28" text-anchor="end" font-size="14" font-weight="800" fill="#1fc8b3">getrieben (z2 = ' + z2 + ')</text>';
    g('ue-g', o);
    document.getElementById('ue-1n').textContent = z1; document.getElementById('ue-2n').textContent = z2;
    document.getElementById('ue-i').textContent = fmt(i, 2);
    document.getElementById('ue-n').textContent = fmt(Math.round(3000 / i), 0) + ' 1/min';
    document.getElementById('ue-m').textContent = fmt(Math.round(200 * i), 0) + ' Nm';
    document.getElementById('ue-t').innerHTML = i > 1.02 ? '<b>i größer 1 – Übersetzung ins Langsame:</b> Das getriebene Rad dreht <span class="c">langsamer</span>, dafür steigt das <span class="c">Drehmoment</span>. So ist es in den kleinen Gängen.'
      : i < 0.98 ? '<b>i kleiner 1 – Übersetzung ins Schnelle:</b> Das getriebene Rad dreht schneller, das Drehmoment sinkt. So ist es in den großen „Spargängen“.'
      : '<b>i = 1:</b> Beide Räder drehen gleich schnell – Drehmoment und Drehzahl bleiben gleich.';
  }
  setInterval(() => { w1 = (w1 + 4) % 360; ue(); }, 50);
  ['ue-1', 'ue-2'].forEach(id => document.getElementById(id).addEventListener('input', ue));

  const IG = [3.77, 2.09, 1.32, 0.97, 0.76, 0.62, 3.6], NA = ['1. Gang', '2. Gang', '3. Gang', '4. Gang', '5. Gang', '6. Gang', 'Rückwärtsgang'];
  const v = i => 3000 / (i * 3.9) * 1.95 * 0.06;
  function gg(k) {
    let o = '';
    IG.slice(0, 6).forEach((i, n) => {
      const x = 40 + n * 96, h = v(i) / 150 * 150;
      o += '<rect x="' + x + '" y="' + (190 - h) + '" width="70" height="' + h + '" rx="6" fill="' + (n === k ? '#1fc8b3' : '#213552') + '" stroke="#ecf1f8" stroke-width="2"/>';
      o += '<text x="' + (x + 35) + '" y="' + (182 - h) + '" text-anchor="middle" font-size="14" font-weight="900" fill="#ecf1f8">' + Math.round(v(i)) + '</text>';
      o += '<text x="' + (x + 35) + '" y="212" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">' + (n + 1) + '.</text>';
    });
    o += '<text x="20" y="26" font-size="14" font-weight="800" fill="#94a4ba">km/h bei 3.000 1/min</text>';
    g('gg-g', o);
    const i = IG[k];
    document.getElementById('gg-t').innerHTML = '<b>' + NA[k] + ':</b> Getriebe i = ' + fmt(i, 2) + ', gesamt i = ' + fmt(i, 2) + ' · 3,9 = <b>' + fmt(i * 3.9, 1) + '</b>. ' +
      (k === 6 ? 'Ein <span class="c">Zwischenrad</span> kehrt die Drehrichtung um – das Auto fährt rückwärts, ähnlich langsam wie im 1. Gang.'
        : 'Bei 3.000 1/min fährt das Auto ca. <span class="c">' + Math.round(v(i)) + ' km/h</span>. ' + (k < 2 ? 'Viel Drehmoment zum Anfahren und am Berg.' : k > 3 ? 'Niedrige Drehzahl bei hoher Geschwindigkeit – spart Kraftstoff.' : ''));
    document.querySelectorAll('#s-gg [data-g]').forEach(b => b.classList.toggle('on', +b.dataset.g === k));
  }
  document.querySelectorAll('#s-gg [data-g]').forEach(b => b.onclick = () => gg(+b.dataset.g)); gg(0);

  // Synchronisation
  let sy = 'ok', t0 = null, raf = null, nW = 1, nR = 0.45, pha = 0, aw = 0, ar = 0;
  function syz(state) {
    let o = '';
    const ring = (cx, a, c, lab) => '<circle cx="' + cx + '" cy="120" r="70" fill="#213552" stroke="' + c + '" stroke-width="5"/><line x1="' + cx + '" y1="120" x2="' + (cx + 60 * Math.cos(a)) + '" y2="' + (120 + 60 * Math.sin(a)) + '" stroke="' + c + '" stroke-width="6"/><text x="' + cx + '" y="218" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">' + lab + '</text>';
    o += ring(140, aw, '#ffd34d', 'Welle mit Schaltmuffe') + ring(420, ar, '#1fc8b3', 'Losrad (neuer Gang)');
    const mx = 220 + (state.muffe || 0) * 80;
    o += '<rect x="' + mx + '" y="95" width="40" height="50" rx="6" fill="#ffd34d"/><text x="' + (mx + 20) + '" y="88" text-anchor="middle" font-size="12" font-weight="800" fill="#ffd34d">Muffe</text>';
    o += '<rect x="330" y="100" width="14" height="40" rx="3" fill="' + (state.reib ? '#ff8f3f' : '#94a4ba') + '"/><text x="337" y="160" text-anchor="middle" font-size="12" font-weight="800" fill="#94a4ba">Synchronring</text>';
    if (state.krach) o += '<text x="280" y="40" text-anchor="middle" font-size="24" font-weight="900" fill="#f05e4e">KRRR!</text>';
    o += '<text x="140" y="250" text-anchor="middle" font-size="13" font-weight="800" fill="#ffd34d">' + Math.round(nW * 100) + ' %</text><text x="420" y="250" text-anchor="middle" font-size="13" font-weight="800" fill="#1fc8b3">' + Math.round(nR * 100) + ' %</text>';
    g('sy-g', o);
  }
  function step(ts) {
    if (t0 === null) t0 = ts;
    const t = (ts - t0) / 1000; let st = {};
    if (t < 1.2) { st.reib = true; st.muffe = Math.min(1, t / 0.4) * 0.4; nR = sy === 'ok' ? 0.45 + 0.55 * Math.min(1, t / 1.0) : 0.45 + 0.25 * Math.min(1, t / 1.0); }
    else if (t < 1.8) { st.muffe = 0.4 + 0.6 * Math.min(1, (t - 1.2) / 0.4); st.krach = sy !== 'ok'; if (sy === 'ok') nR = 1; }
    else { st.muffe = 1; st.krach = sy !== 'ok' && t < 2.4; nR = 1; }
    aw += nW * 0.25; ar += nR * 0.25; syz(st);
    document.getElementById('sy-t').innerHTML = t < 1.2 ? '<b>1. Angleichen:</b> Die Schaltmuffe drückt den <span class="ora">Synchronring</span> auf den Reibkegel des Losrads. Die Reibung bringt beide auf die gleiche Drehzahl.'
      : sy === 'ok' ? '<b class="grn">2. Einrasten:</b> Erst wenn die Drehzahlen gleich sind, gleitet die Schaltmuffe weich über die Verzahnung – der Gang ist drin, leise und ohne Kraft.'
      : '<b class="red">Synchronring verschlissen:</b> Die Drehzahlen sind noch verschieden, wenn die Muffe einrastet – die Zähne schlagen aufeinander: Es <span class="red">kracht</span>. Getriebe instand setzen.';
    if (t < 3) raf = requestAnimationFrame(step); else idle();
  }
  function idle() { cancelAnimationFrame(raf); raf = requestAnimationFrame(function lp() { aw += nW * 0.25; ar += nR * 0.25; syz({ muffe: nR === 1 ? 1 : 0 }); raf = requestAnimationFrame(lp); }); }
  function start() { cancelAnimationFrame(raf); t0 = null; nR = 0.45; raf = requestAnimationFrame(step); }
  document.getElementById('sy-go').onclick = start;
  document.querySelectorAll('#s-sy [data-y]').forEach(b => b.onclick = () => { sy = b.dataset.y; document.querySelectorAll('#s-sy [data-y]').forEach(x => x.classList.toggle('on', x === b)); nR = 0.45; idle(); document.getElementById('sy-t').innerHTML = 'Tippe auf <b>▶ Gang einlegen</b>.'; });
  nR = 0.45; idle(); document.getElementById('sy-t').innerHTML = 'Welle und Losrad drehen <b>verschieden schnell</b>. Tippe auf <b>▶ Gang einlegen</b>.';
''' + fehler_js('s-sf', [
    [['Synchronring verschlissen', 'Kupplung trennt nicht ganz'], ['Kupplung prüfen (Pedalweg, Hydraulik)', 'Kracht nur ein Gang: Synchronisation dieses Gangs']],
    [['Schaltmuffe oder Zahnräder verschlissen', 'Arretierung defekt', 'Motor- oder Getriebelager defekt'], ['Getriebelager prüfen', 'Getriebe instand setzen']],
    [['Lager oder Verzahnung im Getriebe verschlissen', 'zu wenig Getriebeöl'], ['Ölstand prüfen', 'Geräusch lastabhängig? Gas geben und Schub vergleichen']],
    [['Wellendichtringe an Antriebswellen oder Eingangswelle', 'Dichtung am Gehäuse'], ['Getriebe reinigen, Spur verfolgen', 'Ölstand an der Kontrollschraube prüfen']],
    [['Schaltseile schwergängig oder falsch eingestellt', 'Kupplung trennt nicht', 'falsches Getriebeöl'], ['Schaltung bei stehendem Motor prüfen', 'Seilzüge einstellen laut Hersteller']],
]) + '''})();
</script>'''


# ================================================================ 3 Automatikgetriebe
T = 'AUTOMATIK'

auto = [
    titel_folie(K, 'D', 'Automatikgetriebe', 'Wählhebel, Drehmomentwandler, Planetensatz, Doppelkupplung, CVT', 'font-size:140px'),
    lernziele(T, ['Was die Wählhebelstellungen bedeuten', 'Wie der Drehmomentwandler arbeitet',
                  'Wie ein Planetengetriebe verschiedene Übersetzungen macht', 'Was Doppelkupplungsgetriebe und CVT sind']),
    folie(T, 'Der Wählhebel – zum Antippen', '''    <div class="rb" id="wh"><span data-k="0">P</span><span data-k="1">R</span><span data-k="2">N</span><span data-k="3">D</span><span data-k="4">M</span></div>
    <div class="card" id="wh-t" style="font-size:18px;font-weight:600;line-height:1.5"></div>''', sid='s-wh', body_cls='body noclick'),
    folie(T, 'Der Drehmomentwandler – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap">{btns('w', [('0', 'Anfahren'), ('1', 'Fahren'), ('2', 'Überbrückt')])}</div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {svgbox('dw', 560, 300)}
      <div>
        <div class="grid3" style="gap:8px"><div class="card" style="margin:0"><div class="muted" style="font-size:13px;font-weight:800">PUMPENRAD</div><div class="lcd2" id="dw-p" style="font-size:20px">–</div></div>
        <div class="card" style="margin:0"><div class="muted" style="font-size:13px;font-weight:800">TURBINENRAD</div><div class="lcd2" id="dw-t2" style="font-size:20px">–</div></div>
        <div class="card" style="margin:0"><div class="muted" style="font-size:13px;font-weight:800">DREHMOMENT</div><div class="lcd2" id="dw-m" style="font-size:20px">–</div></div></div>
        <div class="card" id="dw-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px"></div>
      </div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Vereinfacht, Beispielwerte.</p>''', sid='s-dw', body_cls='body noclick'),
    folie(T, 'Das Planetengetriebe – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap;gap:6px">{btns('p', [('a', 'Hohlrad fest'), ('b', 'Sonne fest'), ('c', 'Zwei Teile verbunden'), ('d', 'Träger fest')])}</div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.1fr 1fr">
      {svgbox('pl', 420, 460)}
      <div class="card" id="pl-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>''', sid='s-pl', body_cls='body noclick'),
    folie(T, 'Doppelkupplungsgetriebe und CVT', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Doppelkupplungsgetriebe</div>
        <ul UL><li>zwei Teilgetriebe: eins für die ungeraden, eins für die geraden Gänge</li><li>jedes hat seine eigene Kupplung</li><li>der nächste Gang ist schon eingelegt – Schalten ohne Zugkraftunterbrechung</li><li>trockene oder nasse Kupplungen</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">CVT (stufenlos)</div>
        <ul UL><li>ein Schubgliederband oder eine Kette läuft zwischen zwei Kegelscheibenpaaren</li><li>die Scheiben gehen auseinander oder zusammen – der Laufdurchmesser ändert sich</li><li>die Übersetzung ändert sich stufenlos</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Getriebeöl und Diagnose', '''    <ol class="steps-list">
      <li class="step">Fehlerspeicher lesen<small>das Getriebesteuergerät meldet Fehler, bei schweren Fehlern Notlauf (fester Gang)</small></li>
      <li class="step">Ölstand nur nach Vorgabe prüfen<small>oft bei bestimmter Öltemperatur mit dem Tester, Motor läuft</small></li>
      <li class="step">Nur freigegebenes Getriebeöl (ATF)<small>Ölwechsel mit Filter laut Hersteller</small></li>
      <li class="step">Nach Arbeiten anlernen<small>Adaptionswerte zurücksetzen, Grundeinstellung mit dem Tester</small></li>
      <li class="step">Probefahrt<small>Schaltpunkte, Rucke, Schlupf beobachten</small></li>
    </ol>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Abschleppen</b>Nur nach Herstellervorgabe – oft nur kurze Strecke und langsam, sonst die Antriebsachse anheben. Sonst fehlt die Schmierung im Getriebe.</div>
      <div class="tip step"><b>Parksperre</b>P ist keine Bremse – beim Abstellen immer auch die Feststellbremse benutzen.</div>
      <div class="tip step"><b>Starten</b>Der Motor startet nur in P oder N.</div>
      <div class="tip step"><b>E-Auto</b>Viele Elektroautos haben nur ein einstufiges Getriebe – der E-Motor hat schon ab Stillstand viel Drehmoment.</div>
    </div>'''),
    video(T, 'ku-automatik'),
    kurztest(T, [
        ('Was bedeutet die Wählhebelstellung P?', ['Parksperre – das Getriebe ist mechanisch gesperrt', 'Pumpe', 'Leerlauf'], 0, 'P ersetzt aber nicht die Feststellbremse.'),
        ('Welches Teil verbindet beim Wandler Pumpen- und Turbinenrad ohne Schlupf?', ['Das Leitrad', 'Die Überbrückungskupplung', 'Der Planetenträger'], 1, 'So arbeitet der Wandler bei Fahrt ohne Verluste.'),
        ('Beim Planetengetriebe sind zwei Teile miteinander verbunden. Was passiert?', ['Rückwärtsgang', 'Leerlauf', 'Alles dreht gleich schnell – direkter Gang 1 : 1'], 2, 'Der Planetensatz dreht als Block.'),
        ('Warum schaltet ein Doppelkupplungsgetriebe ohne Zugkraftunterbrechung?', ['Der nächste Gang ist im zweiten Teilgetriebe schon eingelegt', 'Es hat keinen Gang', 'Der Wandler hilft'], 0, 'Eine Kupplung öffnet, während die andere schließt.'),
    ]),
    merke(T, ['P – R – N – D: Starten nur in P oder N', 'Wandler: Anfahren mit Drehmomentverstärkung, dann überbrücken',
              'Planetensatz: ein Teil fest – andere Übersetzung', 'Ölstand und Anlernen nur nach Herstellervorgabe']),
]
auto_js = '''<script>
(function () {
  const g = (id, s) => document.getElementById(id).innerHTML = s;
  const WH = ['<b>P – Parken:</b> Eine Sperrklinke im Getriebe blockiert die Abtriebswelle. Nur bei stehendem Fahrzeug einlegen. Der Motor kann gestartet werden.',
    '<b>R – Rückwärts:</b> Nur bei stehendem Fahrzeug einlegen. Rückfahrlicht und Rückfahrkamera gehen an.',
    '<b>N – Neutral (Leerlauf):</b> Kein Kraftfluss zu den Rädern, das Fahrzeug kann rollen. Der Motor kann gestartet werden.',
    '<b>D – Drive (Fahren):</b> Das Getriebesteuergerät schaltet die Gänge selbst – abhängig von Geschwindigkeit, Gaspedal und Fahrprogramm.',
    '<b>M bzw. S – Manuell oder Sport:</b> Der Fahrer schaltet selbst mit Wählhebel oder Schaltwippen – oder das Getriebe schaltet später (Sport).'];
  const ws = document.querySelectorAll('#wh [data-k]');
  function wh(i) { ws.forEach(s => s.classList.toggle('on', +s.dataset.k === i)); document.getElementById('wh-t').innerHTML = WH[i]; }
  ws.forEach(s => s.onclick = () => wh(+s.dataset.k)); wh(0);

  // Wandler
  const DW = [
    [2000, 0, 2.0, '<b>Anfahren:</b> Das <span class="c">Pumpenrad</span> (vom Motor) schleudert Öl auf das <span class="c">Turbinenrad</span>. Das <span class="c">Leitrad</span> lenkt das Öl zurück und verstärkt dabei das Drehmoment – ca. auf das Doppelte. Das Auto fährt sanft an, auch wenn die Turbine noch fast steht.'],
    [2500, 2150, 1.0, '<b>Fahren:</b> Die Turbine dreht fast so schnell wie die Pumpe. Es bleibt ein kleiner <span class="ora">Schlupf</span> – das kostet etwas Kraftstoff und macht Wärme.'],
    [2000, 2000, 1.0, '<b>Überbrückt:</b> Die <span class="c">Überbrückungskupplung</span> verbindet Pumpe und Turbine fest. Kein Schlupf mehr – wie eine geschlossene Kupplung.']];
  let dk = 0, ap = 0, at = 0;
  function dw() {
    const d = DW[dk]; let o = '';
    const rad = (cx, a, c, lab) => { let s = '<circle cx="' + cx + '" cy="150" r="90" fill="#213552" stroke="' + c + '" stroke-width="5"/>'; for (let i = 0; i < 8; i++) { const ra = a + i * Math.PI / 4; s += '<line x1="' + cx + '" y1="150" x2="' + (cx + 82 * Math.cos(ra)) + '" y2="' + (150 + 82 * Math.sin(ra)) + '" stroke="' + c + '" stroke-width="4"/>'; } return s + '<text x="' + cx + '" y="270" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">' + lab + '</text>'; };
    o += rad(150, ap, '#ffd34d', 'Pumpenrad (Motor)') + rad(410, at, '#1fc8b3', 'Turbinenrad (Getriebe)');
    o += '<rect x="262" y="110" width="36" height="80" rx="6" fill="#a07cf5"/><text x="280" y="98" text-anchor="middle" font-size="13" font-weight="800" fill="#a07cf5">Leitrad</text>';
    if (dk < 2) { o += '<path d="M240 120 Q280 60 320 120" fill="none" stroke="#ff8f3f" stroke-width="4" stroke-dasharray="8 6"/><path d="M320 180 Q280 240 240 180" fill="none" stroke="#ff8f3f" stroke-width="4" stroke-dasharray="8 6"/><text x="280" y="40" text-anchor="middle" font-size="13" font-weight="800" fill="#ff8f3f">Ölstrom</text>'; }
    else o += '<rect x="230" y="138" width="100" height="24" rx="6" fill="#34c778"/><text x="280" y="40" text-anchor="middle" font-size="13" font-weight="800" fill="#34c778">Überbrückungskupplung geschlossen</text>';
    g('dw-g', o);
    document.getElementById('dw-p').textContent = d[0].toLocaleString('de-DE');
    document.getElementById('dw-t2').textContent = d[1].toLocaleString('de-DE');
    document.getElementById('dw-m').textContent = '× ' + d[2].toFixed(1).replace('.', ',');
    document.getElementById('dw-t').innerHTML = d[3];
  }
  setInterval(() => { const d = DW[dk]; ap += d[0] / 2000 * 0.12; at += d[1] / 2000 * 0.12; dw(); }, 40);
  document.querySelectorAll('#s-dw [data-w]').forEach(b => b.onclick = () => { dk = +b.dataset.w; document.querySelectorAll('#s-dw [data-w]').forEach(x => x.classList.toggle('on', x === b)); dw(); });

  // Planetensatz
  const ZS = 30, ZR = 72, ZP = 21;
  const PL = {
    a: { s: 1, r: 0, fest: 'Hohlrad', t: '<b>Hohlrad fest:</b> Antrieb über die <span class="c">Sonne</span>, Abtrieb über den <span class="c">Planetenträger</span>. Der Träger dreht viel langsamer: i ≈ 3,4 – Übersetzung ins Langsame (kleiner Gang).' },
    b: { r: 1, s: 0, fest: 'Sonne', t: '<b>Sonne fest:</b> Antrieb über das <span class="c">Hohlrad</span>, Abtrieb über den Träger. Der Träger dreht etwas langsamer: i ≈ 1,4 – ein mittlerer Gang.' },
    c: { s: 1, r: 1, fest: '', t: '<b>Zwei Teile verbunden:</b> Sonne und Hohlrad sind gekoppelt – der ganze Satz dreht als Block. i = 1 : 1, der direkte Gang.' },
    d: { s: 1, c: 0, fest: 'Träger', t: '<b>Träger fest:</b> Antrieb über die Sonne, die Planeten drehen auf der Stelle und treiben das Hohlrad <span class="red">rückwärts</span> an: Rückwärtsgang (i ≈ −2,4).' }
  };
  let pk = 'a', as = 0, ac = 0, ar = 0, ap2 = 0;
  function pl() {
    const p = PL[pk]; let ns, nc, nr;
    if (pk === 'd') { ns = p.s; nc = 0; nr = -ns * ZS / ZR; }
    else if (pk === 'c') { ns = nc = nr = 1; }
    else if (pk === 'a') { ns = 1; nr = 0; nc = ns * ZS / (ZS + ZR); }
    else { nr = 1; ns = 0; nc = nr * ZR / (ZS + ZR); }
    const npl = nc - (ns - nc) * ZS / ZP;
    as += ns * 0.05; ac += nc * 0.05; ar += nr * 0.05; ap2 += npl * 0.05;
    const cx = 210, cy = 260, Rs = 45, Rr = 150, Rp = (Rr - Rs) / 2, Rc = Rs + Rp;
    let o = '<circle cx="' + cx + '" cy="' + cy + '" r="' + (Rr + 18) + '" fill="' + (p.fest === 'Hohlrad' ? '#f05e4e" fill-opacity=".45' : '#213552') + '" stroke="#1fc8b3" stroke-width="5"/><circle cx="' + cx + '" cy="' + cy + '" r="' + Rr + '" fill="#18283f"/>';
    o += '<circle cx="' + (cx + (Rr + 9) * Math.cos(ar)) + '" cy="' + (cy + (Rr + 9) * Math.sin(ar)) + '" r="7" fill="#1fc8b3"/>';
    o += '<line x1="' + cx + '" y1="' + cy + '" x2="' + (cx + Rc * Math.cos(ac)) + '" y2="' + (cy + Rc * Math.sin(ac)) + '" stroke="' + (p.fest === 'Träger' ? '#f05e4e' : '#a07cf5') + '" stroke-width="10"/>';
    o += '<circle cx="' + cx + '" cy="' + cy + '" r="' + Rc + '" fill="none" stroke="' + (p.fest === 'Träger' ? '#f05e4e' : '#a07cf5') + '" stroke-width="10"/>';
    for (let i = 0; i < 3; i++) {
      const a = ac + i * 2 * Math.PI / 3, px = cx + Rc * Math.cos(a), py = cy + Rc * Math.sin(a);
      o += '<line x1="' + cx + '" y1="' + cy + '" x2="' + px + '" y2="' + py + '" stroke="' + (p.fest === 'Träger' ? '#f05e4e' : '#a07cf5') + '" stroke-width="10"/>';
      o += '<circle cx="' + px + '" cy="' + py + '" r="' + (Rp - 3) + '" fill="#213552" stroke="#ecf1f8" stroke-width="4"/><line x1="' + px + '" y1="' + py + '" x2="' + (px + (Rp - 8) * Math.cos(ap2 + i)) + '" y2="' + (py + (Rp - 8) * Math.sin(ap2 + i)) + '" stroke="#ecf1f8" stroke-width="4"/>';
    }
    o += '<circle cx="' + cx + '" cy="' + cy + '" r="' + Rs + '" fill="' + (p.fest === 'Sonne' ? '#f05e4e" fill-opacity=".45' : '#213552') + '" stroke="#ffd34d" stroke-width="5"/><line x1="' + cx + '" y1="' + cy + '" x2="' + (cx + (Rs - 6) * Math.cos(as)) + '" y2="' + (cy + (Rs - 6) * Math.sin(as)) + '" stroke="#ffd34d" stroke-width="5"/>';
    o += '<text x="20" y="30" font-size="14" font-weight="800" fill="#ffd34d">Sonne</text><text x="20" y="50" font-size="14" font-weight="800" fill="#a07cf5">Planetenträger</text><text x="20" y="70" font-size="14" font-weight="800" fill="#1fc8b3">Hohlrad</text>';
    if (p.fest) o += '<text x="400" y="30" text-anchor="end" font-size="14" font-weight="900" fill="#f05e4e">' + p.fest + ' gebremst</text>';
    g('pl-g', o);
  }
  setInterval(pl, 40);
  document.querySelectorAll('#s-pl [data-p]').forEach(b => b.onclick = () => { pk = b.dataset.p; document.querySelectorAll('#s-pl [data-p]').forEach(x => x.classList.toggle('on', x === b)); document.getElementById('pl-t').innerHTML = PL[pk].t + '<br><span class="muted" style="font-size:15px">Im Getriebe halten Lamellenbremsen und -kupplungen die Teile fest oder verbinden sie – gesteuert vom Getriebesteuergerät.</span>'; });
  document.getElementById('pl-t').innerHTML = PL.a.t + '<br><span class="muted" style="font-size:15px">Im Getriebe halten Lamellenbremsen und -kupplungen die Teile fest oder verbinden sie – gesteuert vom Getriebesteuergerät.</span>';
})();
</script>'''


# ================================================================ 4 Achsantrieb
T = 'ACHSANTRIEB'

achse = [
    titel_folie(K, 'Diff', 'Achsantrieb und Differenzial', 'Antriebsarten, Differenzial, Antriebswellen, Allrad', 'font-size:90px'),
    lernziele(T, ['Welche Antriebsarten es gibt', 'Was der Achsantrieb macht',
                  'Warum das Differenzial in Kurven nötig ist', 'Wie Antriebswellen, Gelenke und Allrad arbeiten']),
    folie(T, 'Antriebsarten', '''    <div class="grid3" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:21px">Frontantrieb</div><ul UL><li>Motor meist quer eingebaut</li><li>Getriebe und Differenzial in einem Gehäuse</li><li>zwei Antriebswellen zu den Vorderrädern</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">Heckantrieb</div><ul UL><li>Motor meist längs vorn</li><li>Kardanwelle zum Hinterachsgetriebe</li><li>Umlenkung um 90° mit Kegel- und Tellerrad</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">Allradantrieb</div><ul UL><li>alle Räder werden angetrieben</li><li>Verteilergetriebe oder zuschaltbare Lamellenkupplung</li><li>mehr Traktion auf Schnee und Schotter</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Der Achsantrieb', '''    <div class="values">
      <div class="val step from-left"><b>Übersetzen</b><span>noch einmal ins Langsame – meist ca. 3 bis 4,5</span></div>
      <div class="val step from-left"><b>Umlenken</b><span>bei längs eingebautem Motor um 90° (Kegelrad und Tellerrad)</span></div>
      <div class="val step from-left"><b>Verteilen</b><span>das Differenzial verteilt das Drehmoment auf die beiden Räder</span></div>
      <div class="val step from-left"><b>Gesamt­übersetzung</b><span>i gesamt = i Getriebe · i Achsantrieb</span></div>
    </div>
    <p class="muted" style="font-size:14px">Richtwerte – genaue Übersetzung laut Hersteller.</p>'''),
    folie(T, 'Das Differenzial – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap;gap:6px">{btns('d', [('gerade', 'Geradeaus'), ('kurve', 'Linkskurve'), ('eis', 'Rechtes Rad auf Eis')])}</div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {svgbox('df', 560, 330)}
      <div class="card" id="df-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>''', sid='s-df', body_cls='body noclick'),
    folie(T, 'Antriebswellen und Gelenke', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Antriebswelle (Frontantrieb)</div>
        <ul UL><li>radseitig: Gleichlauf-Kugelgelenk – erlaubt den Lenkeinschlag</li><li>getriebeseitig: Verschiebegelenk – gleicht das Einfedern aus</li><li>Gelenke sind mit Fett gefüllt und mit Manschetten geschützt</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Kardanwelle (Heckantrieb)</div>
        <ul UL><li>verbindet Getriebe und Hinterachsgetriebe</li><li>Kreuzgelenke oder Gummigelenkscheiben</li><li>bei langen Wellen ein Mittellager</li></ul></div>
    </div>
    <div class="warn step" style="margin-top:12px"><b>Manschette gerissen?</b>Fett tritt aus, Schmutz und Wasser dringen ein – das Gelenk ist bald defekt. Manschette sofort erneuern, Gelenk prüfen.</div>'''.replace('UL', UL)),
    folie(T, 'Allrad und Sperren', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Allradsysteme</div>
        <ul UL><li>permanent mit Mittendifferenzial</li><li>zuschaltbar mit Lamellenkupplung – das Steuergerät verteilt die Kraft bei Bedarf</li><li>bei E-Autos oft ein eigener Motor pro Achse</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Sperren</div>
        <ul UL><li>Sperrdifferenzial: begrenzt den Drehzahlunterschied</li><li>elektronische Sperre: das ESP bremst das durchdrehende Rad</li><li>so kommt das Drehmoment wieder an das Rad mit Grip</li></ul></div>
    </div>
    <div class="warn step" style="margin-top:12px"><b>Reifen beim Allrad</b>Alle Reifen gleich groß und mit ähnlichem Profil – sonst verspannt sich der Antrieb. Prüfstände nur nach Herstellervorgabe benutzen.</div>'''.replace('UL', UL)),
    fehlerfolie(T, 'Fehlerbilder – zum Ausprobieren', 's-af', ['Knacken in Kurven', 'Heulen beim Fahren', 'Vibration beim Beschleunigen', 'Ölverlust am Achsantrieb', 'Schlag beim Lastwechsel']),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Achsmutter</b>Oft nur einmal verwendbar: erneuern und mit Drehmoment (ggf. Drehwinkel) laut Hersteller anziehen – Fahrzeug dabei auf den Rädern oder Bremse betätigt.</div>
      <div class="warn step"><b>Antriebswelle</b>Nicht frei hängen lassen und nicht überstrecken – das innere Gelenk kann auseinanderfallen.</div>
      <div class="tip step"><b>Öl</b>Achsantrieb und Verteilergetriebe haben oft eigenes Öl – Sorte und Intervall laut Hersteller.</div>
      <div class="tip step"><b>Probefahrt</b>Mit eingeschlagener Lenkung langsam im Kreis fahren: Knackt es, ist das radseitige Gelenk verdächtig.</div>
    </div>'''),
    video(T, 'ku-achsantrieb'),
    kurztest(T, [
        ('Warum braucht ein Fahrzeug ein Differenzial?', ['Damit das kurvenäußere Rad schneller drehen kann als das innere', 'Damit es schneller fährt', 'Damit es leiser ist'], 0, 'In der Kurve legt das äußere Rad einen längeren Weg zurück.'),
        ('Ein Antriebsrad steht auf Eis. Was macht ein normales Differenzial?', ['Es treibt beide Räder gleich stark an', 'Das Rad auf Eis dreht durch, das andere bekommt kaum Kraft', 'Es bremst'], 1, 'Abhilfe: Sperre oder Bremseingriff durch das ESP.'),
        ('Es knackt bei Kurvenfahrt mit eingeschlagener Lenkung. Was ist verdächtig?', ['Das Ausrücklager', 'Der Synchronring', 'Das radseitige Gleichlaufgelenk'], 2, 'Oft nach gerissener Manschette.'),
        ('Wie berechnest du die Gesamtübersetzung?', ['i gesamt = i Getriebe · i Achsantrieb', 'i gesamt = i Getriebe + i Achsantrieb', 'i gesamt = i Getriebe : i Achsantrieb'], 0, 'z. B. 3,77 · 3,9 ≈ 14,7 im 1. Gang.'),
    ]),
    merke(T, ['Front, Heck oder Allrad', 'Achsantrieb übersetzt und lenkt um', 'Differenzial: Kurve – außen schneller als innen',
              'Manschetten prüfen – Knacken in Kurven = Gelenk']),
]
achse_js = '''<script>
(function () {
  const g = (id, s) => document.getElementById(id).innerHTML = s;
  const DF = {
    gerade: [100, 100, 0, '<b>Geradeaus:</b> Beide Räder drehen gleich schnell wie der Differenzialkorb. Die <span class="c">Ausgleichsräder</span> drehen sich nicht um sich selbst – sie laufen nur mit.'],
    kurve: [88, 112, 1, '<b>Linkskurve:</b> Das äußere (rechte) Rad muss einen längeren Weg fahren als das innere. Die <span class="c">Ausgleichsräder</span> drehen sich und lassen das äußere Rad schneller, das innere langsamer drehen. Der Durchschnitt bleibt gleich. Ohne Differenzial würden die Reifen radieren.'],
    eis: [0, 200, 2, '<b class="red">Rechtes Rad auf Eis:</b> Das Differenzial gibt beiden Rädern nur so viel Drehmoment, wie das Rad mit dem <b>wenigsten</b> Grip übertragen kann. Das Rad auf Eis dreht doppelt so schnell durch, das andere steht – das Auto kommt nicht weg. Abhilfe: <span class="c">Sperre</span> oder das <span class="c">ESP bremst das durchdrehende Rad</span>.']
  };
  let dk = 'gerade', al = 0, ar = 0, aa = 0;
  function df() {
    const d = DF[dk]; let o = '';
    if (dk === 'kurve') o += '<path d="M340 62 H220" stroke="#94a4ba" stroke-width="3"/><path d="M220 62 l12 -7 v14 z" fill="#94a4ba"/><text x="280" y="54" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Kurve nach links</text>';
    if (dk === 'eis') o += '<rect x="410" y="110" width="140" height="150" rx="16" fill="#9fd6ff" opacity=".25"/><text x="480" y="290" text-anchor="middle" font-size="14" font-weight="800" fill="#9fd6ff">Eis</text>';
    o += '<line x1="130" y1="185" x2="430" y2="185" stroke="#94a4ba" stroke-width="10"/>';
    const rad = (cx, a, n, lab) => '<rect x="' + (cx - 26) + '" y="115" width="52" height="140" rx="12" fill="#213552" stroke="#ecf1f8" stroke-width="4"/>' +
      [0, 1, 2, 3].map(i => { const y = 120 + ((a * 30 + i * 35) % 140); return '<line x1="' + (cx - 22) + '" y1="' + y + '" x2="' + (cx + 22) + '" y2="' + y + '" stroke="#94a4ba" stroke-width="3"/>'; }).join('') +
      '<text x="' + cx + '" y="95" text-anchor="middle" font-size="18" font-weight="900" fill="#ffd34d">' + n + ' %</text><text x="' + cx + '" y="290" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">' + lab + '</text>';
    o += rad(110, al, d[0], 'links') + rad(450, ar, d[1], 'rechts');
    o += '<circle cx="280" cy="185" r="56" fill="#213552" stroke="#a07cf5" stroke-width="5"/>';
    o += '<circle cx="280" cy="185" r="16" fill="#18283f" stroke="#ecf1f8" stroke-width="3" transform="rotate(' + (aa * 57) + ' 280 185)"/>';
    for (let i = 0; i < 2; i++) { const y = 150 + i * 70; o += '<g transform="rotate(' + (aa * 57 * (i ? -1 : 1)) + ' 280 ' + y + ')"><circle cx="280" cy="' + y + '" r="14" fill="#ffd34d"/><line x1="268" y1="' + y + '" x2="292" y2="' + y + '" stroke="#18283f" stroke-width="3"/></g>'; }
    o += '<text x="280" y="268" text-anchor="middle" font-size="13" font-weight="800" fill="#a07cf5">Differenzial</text><text x="280" y="30" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Ausgleichsräder (gelb) drehen bei Drehzahlunterschied</text>';
    g('df-g', o);
    document.getElementById('df-t').innerHTML = d[3];
  }
  setInterval(() => { const d = DF[dk]; al += d[0] / 100 * 0.15; ar += d[1] / 100 * 0.15; aa += (d[1] - d[0]) / 100 * 0.08; df(); }, 40);
  document.querySelectorAll('#s-df [data-d]').forEach(b => b.onclick = () => { dk = b.dataset.d; document.querySelectorAll('#s-df [data-d]').forEach(x => x.classList.toggle('on', x === b)); });
''' + fehler_js('s-af', [
    [['radseitiges Gleichlaufgelenk verschlissen (oft nach gerissener Manschette)'], ['Manschetten ansehen', 'Probefahrt: langsam mit eingeschlagener Lenkung im Kreis']],
    [['Lager oder Verzahnung im Achsantrieb', 'Radlager (ändert sich in Kurven)', 'zu wenig Öl im Achsantrieb'], ['Geräusch bei Last und im Schub vergleichen', 'Radlager auf Spiel und Geräusch prüfen', 'Ölstand prüfen']],
    [['inneres Verschiebegelenk der Antriebswelle', 'Kardanwelle: Mittellager oder Gelenkscheibe', 'Motorlager'], ['Gelenke und Manschetten prüfen', 'Mittellager und Gelenkscheibe ansehen']],
    [['Wellendichtring an Antriebswelle oder Antriebsritzel', 'Dichtung am Deckel'], ['Spur verfolgen', 'Ölstand prüfen, Dichtring erneuern']],
    [['Spiel im Achsantrieb oder in den Gelenken', 'Motor- oder Getriebelager', 'Kardanwelle verschlissen'], ['Spiel von Hand prüfen (Welle drehen)', 'Lager auf Risse prüfen']],
]) + '''})();
</script>'''


if __name__ == '__main__':
    seite('ku-kupplung.html', 'Die Kupplung – Kraftübertragung', 't-ku1', 'Kupplung und Zweimassenschwungrad', kupplung, STYLE, kupplung_js)
    seite('ku-schaltgetriebe.html', 'Das Schaltgetriebe – Kraftübertragung', 't-ku2', 'Schaltgetriebe', schalt, STYLE, schalt_js)
    seite('ku-automatik.html', 'Automatikgetriebe – Kraftübertragung', 't-ku3', 'Automatikgetriebe', auto, STYLE, auto_js)
    seite('ku-achsantrieb.html', 'Achsantrieb und Differenzial – Kraftübertragung', 't-ku4', 'Achsantrieb und Differenzial', achse, STYLE, achse_js)
    print('ok')
