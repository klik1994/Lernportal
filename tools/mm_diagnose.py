"""Motormanagement: Diagnose – drei Präsentationen.
Aufruf: cd tools && python3 mm_diagnose.py"""
from praesentation_bauen import *

THEMA = 'Motormanagement: Diagnose'
K = 'MOTORMANAGEMENT · DIAGNOSE'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'

STECKER = '''<svg viewBox="0 0 320 150" width="300" height="140" style="display:block;margin:0 auto">
  <path d="M20 20 H300 L280 130 H40 Z" fill="#3b4250" stroke="#94a4ba" stroke-width="3"/>
  ''' + ''.join(f'<rect x="{50 + i * 29}" y="{40 + r * 46}" width="16" height="26" rx="3" fill="#c6a15a"/>' for r in range(2) for i in range(8)) + '''
</svg>'''

# ---------------------------------------------------------------- OBD und Fehlerspeicher
T = 'OBD'
obd = [
    titel_folie(K, 'OBD', 'OBD und Fehlerspeicher', 'Diagnosestecker, Fehlercodes und Motorkontrollleuchte', 'font-size:72px'),
    lernziele(T, ['Was OBD ist und wo der Diagnosestecker sitzt', 'Was die Motorkontrollleuchte meldet',
                  'Wie ein Fehlercode aufgebaut ist', 'Wie du den Fehlerspeicher richtig ausliest']),
    folie(T, 'Was ist OBD?', f'''    <div class="grid2" style="align-items:center">
      <div>
        <div class="card step" style="font-size:20px;font-weight:600"><span class="c">On-Board-Diagnose:</span> Das Steuergerät überwacht sich und alle abgasrelevanten Bauteile selbst – während der Fahrt.</div>
        <ul class="step" UL><li>Pflicht in der EU: Benziner ab 2001, Diesel ab 2004</li><li>Fehler werden mit Code im Fehlerspeicher abgelegt</li><li>genormter 16-poliger Diagnosestecker</li></ul>
      </div>
      <div class="card step" style="text-align:center">{STECKER}<div style="font-weight:800;margin-top:8px">Diagnosestecker</div><div class="muted" style="font-size:15px">meist im Fahrerfußraum, in der Nähe der Lenksäule</div></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Die Motorkontrollleuchte', '''    <div class="values">
      <div class="val step from-left"><b>leuchtet kurz</b><span>bei Zündung an – Lampentest, geht nach dem Start aus</span></div>
      <div class="val step from-left"><b>leuchtet dauernd</b><span>ein abgasrelevanter Fehler ist gespeichert – bald in die Werkstatt</span></div>
      <div class="val step from-left"><b>blinkt</b><span>starke Zündaussetzer – Gefahr für den Katalysator: Leistung wegnehmen</span></div>
    </div>
    <div class="tip step" style="margin-top:14px"><b>Nicht jeder Fehler macht die Leuchte an</b>Viele Fehler stehen nur im Fehlerspeicher. Darum bei jeder Beschwerde auslesen – auch wenn keine Lampe leuchtet.</div>'''),
    folie(T, 'Fehlercodes lesen – zum Ausprobieren', '''    <div class="choice" style="margin-bottom:14px"><button class="btn ghost on" data-c="0">P0301</button><button class="btn ghost" data-c="1">P0171</button><button class="btn ghost" data-c="2">P0420</button><button class="btn ghost" data-c="3">P0113</button></div>
    <div class="card" style="display:flex;gap:6px;justify-content:center;font-size:52px;font-weight:900;letter-spacing:2px" id="fc-code"></div>
    <div class="grid2" style="margin-top:14px;grid-template-columns:repeat(4,1fr)" id="fc-teile"></div>
    <div class="card" id="fc-t" style="margin-top:14px;font-size:18px;font-weight:600"></div>''', sid='s-fc', body_cls='body noclick'),
    folie(T, 'Mehr als nur der Code', '''    <div class="grid2" style="align-content:start">
      <div class="card step"><div class="big" style="font-size:21px">Statisch oder sporadisch</div><ul UL><li><b>statisch:</b> Fehler ist jetzt vorhanden</li><li><b>sporadisch:</b> Fehler war da, ist gerade weg – z. B. Wackelkontakt</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">Umgebungsbedingungen</div><ul UL><li>Drehzahl, Temperatur, Kilometerstand, Häufigkeit</li><li>zeigen, <b>wann</b> der Fehler auftrat</li><li>sehr wichtig bei sporadischen Fehlern</li></ul></div>
      <div class="card step"><div class="big" style="font-size:21px">Bereitschaftstests (Readiness)</div><ul UL><li>zeigen, ob alle Eigendiagnosen schon gelaufen sind</li><li>nach dem Löschen erst wieder nach Fahrt vollständig</li><li>wichtig für die Abgasuntersuchung</li></ul></div>
      <div class="tip step"><b>Ein Fehler – viele Codes</b>Ein defekter Sensor oder eine fehlende Masse kann mehrere Fehler auslösen. Mit dem ersten, wichtigsten Fehler anfangen.</div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Fehlerspeicher richtig auslesen', '''    <ol class="steps-list">
      <li class="step">Batteriespannung prüfen<small>bei langer Diagnose ein Ladegerät mit Stützfunktion anschließen</small></li>
      <li class="step">Alle Steuergeräte auslesen<small>auch Fehler in anderen Systemen können die Ursache sein</small></li>
      <li class="step">Fehler und Umgebungsbedingungen <span class="c">speichern oder notieren</span><small>erst dann irgendetwas löschen</small></li>
      <li class="step">Nach der Reparatur: löschen, Probefahrt, erneut auslesen<small>kommt der Fehler wieder, ist die Ursache noch nicht gefunden</small></li>
    </ol>
    <div class="warn step" style="margin-top:6px"><b>Nicht einfach löschen</b>Wer sofort löscht, verliert wichtige Hinweise – und der Fehler kommt wieder.</div>'''),
    video(T, 'mm-diag-obd'),
    kurztest(T, [
        ('Was bedeutet eine blinkende Motorkontrollleuchte?', ['Starke Zündaussetzer – Gefahr für den Kat', 'Ölwechsel fällig', 'Lampentest'], 0, 'Leistung wegnehmen und bald in die Werkstatt.'),
        ('Wofür steht das „P“ in einem Fehlercode wie P0301?', ['Pumpe', 'Antrieb (Motor und Getriebe)', 'Partikelfilter'], 1, 'P = Powertrain, also Antrieb.'),
        ('Was solltest du vor dem Löschen des Fehlerspeichers tun?', ['Nichts', 'Batterie abklemmen', 'Fehler und Umgebungsbedingungen speichern'], 2, 'Sonst gehen wichtige Hinweise verloren.'),
        ('Ein Fehler ist als „sporadisch“ gespeichert. Was heißt das?', ['Der Fehler war da, ist aber gerade nicht vorhanden', 'Der Fehler ist dauernd da', 'Das Steuergerät ist defekt'], 0, 'Typisch für Wackelkontakte – Umgebungsbedingungen helfen.'),
    ]),
    merke(T, ['OBD: Steuergerät überwacht sich selbst', 'Leuchte dauernd: Fehler – blinkt: Kat in Gefahr',
              'P0301: Antrieb, genormt, Zündung, Zylinder 1', 'Erst speichern, dann löschen|Probefahrt, erneut auslesen']),
]
obd_js = '''<script>
(function () {
  const C = [
    ['P0301', ['P', 'Antrieb'], ['0', 'genormt'], ['3', 'Zündung / Aussetzer'], ['01', 'Zylinder 1'], 'Zündaussetzer Zylinder 1. Prüfen: Zündspule quertauschen, Zündkerze, Einspritzventil, Kompression.'],
    ['P0171', ['P', 'Antrieb'], ['0', 'genormt'], ['1', 'Luft- und Kraftstoffmenge'], ['71', 'Gemisch zu mager, Bank 1'], 'Gemisch zu mager. Prüfen: Falschluft, Kraftstoffdruck, Luftmassenmesser, Korrekturwerte.'],
    ['P0420', ['P', 'Antrieb'], ['0', 'genormt'], ['4', 'Abgasnachbehandlung'], ['20', 'Kat-Wirkungsgrad, Bank 1'], 'Wirkungsgrad Katalysator zu niedrig. Prüfen: Sonde nach Kat, Undichtigkeit der Abgasanlage, Aussetzer.'],
    ['P0113', ['P', 'Antrieb'], ['0', 'genormt'], ['1', 'Luft- und Kraftstoffmenge'], ['13', 'Ansauglufttemperatur: Signal zu hoch'], 'Signal zu hoch – oft Unterbrechung in Leitung oder Stecker. Prüfen mit Prüfadapter: Versorgung, Masse, Signal.']
  ];
  const bt = document.querySelectorAll('#s-fc [data-c]');
  const FAR = ['var(--blu)', 'var(--grn)', 'var(--ora)', 'var(--pur)'];
  function c(i) {
    const k = C[i];
    document.getElementById('fc-code').innerHTML = [k[1], k[2], k[3], k[4]].map((p, j) => '<span style="color:' + FAR[j] + '">' + p[0] + '</span>').join('');
    document.getElementById('fc-teile').innerHTML = [k[1], k[2], k[3], k[4]].map((p, j) => '<div class="card" style="border-top:4px solid ' + FAR[j] + ';text-align:center"><div style="font-size:26px;font-weight:900">' + p[0] + '</div><div class="muted" style="font-size:15px;font-weight:700">' + p[1] + '</div></div>').join('');
    document.getElementById('fc-t').innerHTML = k[5];
    bt.forEach(x => x.classList.toggle('on', +x.dataset.c === i));
  }
  bt.forEach(x => x.onclick = () => c(+x.dataset.c)); c(0);
})();
</script>'''

# ---------------------------------------------------------------- Messwerte und Adaption
T = 'MESSWERTE'
mess = [
    titel_folie(K, 'MW', 'Messwerte und Adaption', 'Istwerte lesen, Plausibilität prüfen, Stellglieder testen', 'font-size:84px'),
    lernziele(T, ['Was Messwerte (Istwerte) sind', 'Wie du erkennst, ob ein Wert plausibel ist',
                  'Was ein Stellglied- oder Aktortest ist', 'Was Adaptionswerte sind und wann man sie zurücksetzt']),
    folie(T, 'Messwerte im Diagnosegerät', '''    <div class="card step" style="font-size:20px;font-weight:600;margin-bottom:14px">Das Diagnosegerät zeigt, was das Steuergerät <span class="c">gerade sieht</span> – die Werte aller Sensoren, live.</div>
    <div class="values">
      <div class="val step from-left"><b>ca. 90 °C</b><span>Kühlmitteltemperatur bei warmem Motor</span></div>
      <div class="val step from-left"><b>ca. 650–850 1/min</b><span>Leerlaufdrehzahl, warm</span></div>
      <div class="val step from-left"><b>ca. 1,00</b><span>Lambda beim Benziner im Leerlauf</span></div>
      <div class="val step from-left"><b>nahe 0 %</b><span>Korrekturwerte der Gemischregelung</span></div>
    </div>
    <div class="note step">Richtwerte – Sollwerte immer laut Hersteller bzw. Reparaturleitfaden</div>'''),
    folie(T, 'Was passt nicht? – zum Ausprobieren', '''    <div class="choice" style="margin-bottom:12px"><button class="btn ghost on" data-s="0">Fall 1</button><button class="btn ghost" data-s="1">Fall 2</button><button class="btn ghost" data-s="2">Fall 3</button></div>
    <div class="card" id="pl-lage" style="font-size:18px;font-weight:700;margin-bottom:10px"></div>
    <div id="pl-werte" style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px"></div>
    <div class="card" id="pl-t" style="margin-top:12px;font-size:17px;font-weight:600;line-height:1.5">Tippe auf den Wert, der nicht passt.</div>''', sid='s-pl', body_cls='body noclick'),
    folie(T, 'Plausibel oder nicht?', '''    <ol class="steps-list">
      <li class="step">Werte mit dem <span class="c">Betriebszustand</span> vergleichen<small>kalter Motor, warmer Leerlauf, Volllast – passen die Werte dazu?</small></li>
      <li class="step">Sensoren <span class="c">untereinander</span> vergleichen<small>über Nacht abgekühlt: Kühlmittel- und Ansauglufttemperatur müssen fast gleich sein</small></li>
      <li class="step">Typische <span class="c">Ersatzwerte</span> erkennen<small>z. B. genau −40 °C oder 140 °C: oft Unterbrechung oder Kurzschluss in Leitung oder Stecker</small></li>
      <li class="step">Wert ändert sich nicht?<small>Gas geben, Motor warm werden lassen – ein Sensor muss reagieren</small></li>
    </ol>'''),
    folie(T, 'Stellglieddiagnose (Aktortest)', '''    <div class="kette">
      <div class="glied step"><b>Diagnosegerät</b><span>Aktortest starten</span></div><div class="flow-arrow step"></div>
      <div class="glied step"><b>Steuergerät</b><span>steuert das Bauteil an</span></div><div class="flow-arrow step"></div>
      <div class="glied step hd"><b>Aktor</b><span>z. B. Kraftstoffpumpe, Lüfter, AGR-Ventil, Tankentlüftung</span></div>
    </div>
    <div class="grid2" style="margin-top:18px">
      <div class="tip step"><b>Hören, fühlen, messen</b>Klickt das Ventil, läuft die Pumpe, dreht der Lüfter? So prüfst du Steuergerät, Leitung und Aktor zusammen.</div>
      <div class="warn step"><b>Vorsicht</b>Beim Aktortest können sich Teile bewegen (Lüfter, Drosselklappe). Hände weg, Hinweise im Diagnosegerät beachten.</div>
    </div>'''),
    folie(T, 'Adaptionswerte', '''    <div class="card step" style="font-size:20px;font-weight:600;margin-bottom:14px">Das Steuergerät <span class="c">lernt</span> mit der Zeit dazu und gleicht Verschleiß und Bauteiltoleranzen aus.</div>
    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Beispiele</b>Gemischadaption (Langzeitkorrektur), Drosselklappe, Leerlauf, Mengenabgleich der Injektoren.</div>
      <div class="tip step"><b>Als Hinweis nutzen</b>Eine Adaption an der Grenze zeigt: Hier gleicht das Steuergerät einen Fehler aus.</div>
      <div class="warn step"><b>Nach dem Tausch</b>Neue Bauteile oft anlernen oder Adaption zurücksetzen – genau nach Herstellervorgabe.</div>
      <div class="warn step"><b>Nicht „blind“ zurücksetzen</b>Wer Adaptionen ohne Grund löscht, versteckt den Fehler nur.</div>
    </div>'''),
    video(T, 'mm-diag-messwerte'),
    kurztest(T, [
        ('Was zeigen die Messwerte im Diagnosegerät?', ['Was das Steuergerät gerade von den Sensoren bekommt', 'Nur alte Fehler', 'Die Rechnung'], 0, 'Live-Werte aller Sensoren und berechnete Werte.'),
        ('Das Auto stand über Nacht. Kühlmittel: 8 °C, Ansaugluft: −40 °C. Was ist auffällig?', ['Kühlmitteltemperatur', 'Die Ansauglufttemperatur – oft Unterbrechung', 'Nichts'], 1, 'Nach dem Abkühlen müssen beide Werte fast gleich sein. −40 °C ist ein typischer Ersatzwert.'),
        ('Wozu dient ein Aktortest?', ['Er löscht den Fehlerspeicher', 'Er misst die Batteriespannung', 'Das Steuergerät steuert ein Bauteil gezielt an'], 2, 'So prüfst du Steuergerät, Leitung und Aktor zusammen.'),
        ('Wann setzt man Adaptionswerte zurück?', ['Nach Herstellervorgabe, z. B. nach Bauteiltausch', 'Bei jedem Werkstattbesuch', 'Nie'], 0, 'Ohne Grund zurücksetzen versteckt nur den Fehler.'),
    ]),
    merke(T, ['Messwerte: live, was das Steuergerät sieht', 'Plausibel? Betriebszustand und Sensoren vergleichen|−40 °C oft Unterbrechung',
              'Aktortest prüft Steuergerät, Leitung und Aktor', 'Adaption: lernt mit – zurücksetzen nur nach Vorgabe']),
]
mess_js = '''<script>
(function () {
  const F = [
    ['Motor stand über Nacht in der Halle, Zündung an.', [['Kühlmitteltemperatur', '12 °C'], ['Ansauglufttemperatur', '−40 °C'], ['Drehzahl', '0 1/min'], ['Batteriespannung', '12,5 V']], 1,
     '<b class="red">Ansauglufttemperatur −40 °C</b> passt nicht: Nach der Nacht müssen beide Temperaturen fast gleich sein. −40 °C ist ein typischer Ersatzwert – Leitung und Stecker mit Prüfadapter prüfen.'],
    ['Warmer Motor im Leerlauf.', [['Kühlmitteltemperatur', '91 °C'], ['Drehzahl', '760 1/min'], ['Lambda', '1,00'], ['Langzeitkorrektur', '+22 %']], 3,
     '<b class="red">Langzeitkorrektur +22 %</b> ist viel zu hoch: Das Steuergerät muss stark anfetten – Falschluft, Kraftstoffdruck oder Luftmassenmesser prüfen.'],
    ['Warmer Motor im Leerlauf, keine Verbraucher an.', [['Kühlmitteltemperatur', '20 °C'], ['Drehzahl', '780 1/min'], ['Ladespannung', '14,1 V'], ['Lambda', '1,00']], 0,
     '<b class="red">Kühlmitteltemperatur 20 °C</b> bei warmem Motor passt nicht. Folge: zu fettes Gemisch, hoher Verbrauch, Lüfter-Probleme. Sensor und Leitung prüfen.']
  ];
  const bt = document.querySelectorAll('#s-pl [data-s]');
  let fall = 0;
  function show(i) {
    fall = i; const f = F[i];
    document.getElementById('pl-lage').textContent = f[0];
    document.getElementById('pl-werte').innerHTML = f[1].map((w, j) => '<button class="btn ghost" data-w="' + j + '" style="display:flex;justify-content:space-between;width:100%;font-size:17px"><span>' + w[0] + '</span><b>' + w[1] + '</b></button>').join('');
    document.getElementById('pl-t').innerHTML = 'Tippe auf den Wert, der nicht passt.';
    document.querySelectorAll('#pl-werte [data-w]').forEach(b => b.onclick = () => {
      const j = +b.dataset.w;
      if (j === f[2]) { b.style.borderColor = 'var(--red)'; b.classList.add('on'); document.getElementById('pl-t').innerHTML = f[3]; }
      else { document.getElementById('pl-t').innerHTML = '<b>' + f[1][j][0] + '</b> passt hier. Schau noch einmal.'; }
    });
    bt.forEach(x => x.classList.toggle('on', +x.dataset.s === i));
  }
  bt.forEach(x => x.onclick = () => show(+x.dataset.s)); show(0);
})();
</script>'''

# ---------------------------------------------------------------- Systematische Fehlersuche
T = 'FEHLERSUCHE'
SENSOR = '''<svg viewBox="0 0 560 230" width="540" height="222" style="display:block;margin:0 auto">
  <rect x="20" y="40" width="130" height="150" rx="12" fill="#213552" stroke="#94a4ba" stroke-width="2"/>
  <text x="85" y="120" text-anchor="middle" font-size="16" font-weight="800" fill="#ecf1f8">Steuergerät</text>
  <rect x="420" y="40" width="120" height="150" rx="12" fill="#213552" stroke="#94a4ba" stroke-width="2"/>
  <text x="480" y="120" text-anchor="middle" font-size="16" font-weight="800" fill="#ecf1f8">Sensor</text>
  <line x1="150" y1="70" x2="420" y2="70" stroke="#f05e4e" stroke-width="4"/><text x="255" y="60" text-anchor="middle" font-size="15" font-weight="800" fill="#f05e4e">Versorgung ca. 5 V</text>
  <line x1="150" y1="115" x2="420" y2="115" stroke="#28aaf5" stroke-width="4"/><text x="255" y="105" text-anchor="middle" font-size="15" font-weight="800" fill="#28aaf5">Signal z. B. 0,5–4,5 V</text>
  <line x1="150" y1="160" x2="420" y2="160" stroke="#94a4ba" stroke-width="4"/><text x="255" y="150" text-anchor="middle" font-size="15" font-weight="800" fill="#94a4ba">Masse ca. 0 V</text>
  <rect x="370" y="50" width="36" height="130" rx="6" fill="none" stroke="#34c778" stroke-width="3" stroke-dasharray="6 5"/>
  <text x="388" y="212" text-anchor="middle" font-size="14" font-weight="800" fill="#34c778">Prüfadapter</text>
</svg>'''

fehler = [
    titel_folie(K, '?', 'Systematische Fehlersuche', 'Schritt für Schritt statt Teile tauschen', 'font-size:120px'),
    lernziele(T, ['In welcher Reihenfolge du einen Fehler suchst', 'Warum das Kundengespräch so wichtig ist',
                  'Wie du an einem Sensor gezielt misst', 'Einen Fall Schritt für Schritt lösen']),
    folie(T, 'Der Weg zum Fehler', '''    <ol class="steps-list">
      <li class="step">Kundengespräch<small>Was genau? Wann – kalt, warm, bei Regen? Wie oft? Seit wann?</small></li>
      <li class="step">Fehler nachvollziehen<small>Probefahrt unter den genannten Bedingungen</small></li>
      <li class="step">Fehlerspeicher und Messwerte<small>speichern, Plausibilität prüfen</small></li>
      <li class="step">Prüfplan des Herstellers<small>geführte Fehlersuche, Stromlaufplan, Sollwerte</small></li>
      <li class="step">Gezielt messen<small>Spannungsversorgung, Masse, Signal – mit Prüfadapter</small></li>
      <li class="step">Ursache beheben, kontrollieren, dokumentieren<small>löschen, Probefahrt, erneut auslesen</small></li>
    </ol>'''),
    folie(T, 'Messen an einem Sensor', f'''    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {SENSOR}
      <ol class="steps-list">
        <li class="step">Zündung an, Stecker gesteckt<small>Messung über den Prüfadapter</small></li>
        <li class="step">Versorgung gegen Masse<small>ca. 5 V vom Steuergerät?</small></li>
        <li class="step">Masse prüfen<small>Spannungsfall gegen Batterie-Minus nahe 0 V</small></li>
        <li class="step">Signal bei Betrieb<small>ändert es sich passend?</small></li>
      </ol>
    </div>
    <div class="note step">Beispielwerte – Sollwerte laut Stromlaufplan bzw. Reparaturleitfaden</div>'''),
    folie(T, 'Ein Fall zum Durchklicken', '''    <div class="card" style="font-size:18px;font-weight:700;margin-bottom:10px">Kunde: „Motorkontrollleuchte an, der Motor zieht schlecht.“ Fehlerspeicher: <span class="c">P0102 – Luftmassenmesser, Signal zu niedrig</span></div>
    <div class="card" id="fa-frage" style="font-size:19px;font-weight:800"></div>
    <div class="choice" id="fa-opts" style="margin-top:10px;flex-direction:column;align-items:stretch"></div>
    <div class="card" id="fa-t" style="margin-top:10px;font-size:17px;font-weight:600;line-height:1.5"></div>''', sid='s-fa', body_cls='body noclick'),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="warn step"><b>Teile tauschen nach Gefühl</b>Kostet Geld und Zeit – und oft ist danach der Fehler noch da.</div>
      <div class="tip step"><b>Erst das Einfache</b>Batterie, Sicherungen, Masseverbindungen, Stecker und Korrosion zuerst prüfen.</div>
      <div class="tip step"><b>Nicht von vorne in den Stecker</b>Kontakte werden aufgeweitet – neuer Wackelkontakt. Immer Prüfadapter verwenden.</div>
      <div class="tip step"><b>„OL“ am Multimeter?</b>Bei manuellem Multimeter erst den Messbereich schrittweise bis zum höchsten hochstellen – erst dann gilt: Unterbrechung.</div>
      <div class="warn step"><b>Aktive Sensoren</b>Nicht mit dem Ohmmeter messen – sie können beschädigt werden. Spannung und Signal bei Betrieb prüfen.</div>
      <div class="tip step"><b>Dokumentieren</b>Fehlercodes, Messwerte und was du getan hast aufschreiben – hilft dir und dem Kollegen.</div>
    </div>'''),
    video(T, 'mm-diag-fehlersuche'),
    kurztest(T, [
        ('Was ist der erste Schritt bei der Fehlersuche?', ['Teile bestellen', 'Kundengespräch – was, wann, wie oft?', 'Fehlerspeicher löschen'], 1, 'Die Angaben des Kunden zeigen, wo und wann du suchen musst.'),
        ('Wie misst du an einem Sensorstecker richtig?', ['Von vorne in die Buchse stechen', 'Mit dem Ohmmeter am aktiven Sensor', 'Über einen Prüfadapter bei gestecktem Stecker'], 2, 'So bleiben die Kontakte heil und du misst unter echten Bedingungen.'),
        ('Ein Luftmassenmesser meldet „Signal zu niedrig“. Was prüfst du vor dem Tausch?', ['Versorgung, Masse und Signalleitung', 'Die Zündkerzen', 'Den Reifendruck'], 0, 'Oft ist eine Leitung oder ein Stecker die Ursache, nicht der Sensor.'),
        ('Woran erkennst du, dass die Reparatur erfolgreich war?', ['Die Rechnung ist geschrieben', 'Nach Löschen und Probefahrt kommt der Fehler nicht wieder', 'Das Teil ist neu'], 1, 'Erst die Kontrolle zeigt, ob die Ursache wirklich behoben ist.'),
    ]),
    merke(T, ['Kunde → nachvollziehen → auslesen → Prüfplan → messen', 'Versorgung, Masse, Signal – mit Prüfadapter',
              'Erst das Einfache prüfen', 'Kontrolle: löschen, Probefahrt, erneut auslesen']),
]
fehler_js = '''<script>
(function () {
  const S = [
    ['1. Was machst du zuerst?', ['Luftmassenmesser sofort tauschen', 'Fehler und Umgebungsbedingungen speichern, Messwerte ansehen', 'Fehlerspeicher löschen und abwarten'], 1,
     'Richtig: Erst sichern und ansehen. Im Messwert zeigt der Luftmassenmesser im Leerlauf fast 0 kg/h.'],
    ['2. Wie geht es weiter?', ['Mit dem Prüfadapter Versorgung, Masse und Signal messen', 'Neuen Luftmassenmesser einbauen', 'Zündkerzen wechseln'], 0,
     'Richtig: gezielt messen. Ergebnis: Masse in Ordnung, Signal fast 0 V – aber keine Versorgungsspannung am Sensor.'],
    ['3. Keine Versorgung am Sensor. Was prüfst du?', ['Den Luftfilter', 'Den Sensor mit dem Ohmmeter', 'Sicherung und Leitung laut Stromlaufplan'], 2,
     'Richtig: Die Sicherung ist in Ordnung, aber die Leitung zum Sensor ist am Stecker korrodiert und unterbrochen.'],
    ['4. Leitung repariert. Und jetzt?', ['Fertig – Auto zurückgeben', 'Fehler löschen, Probefahrt, erneut auslesen, dokumentieren', 'Luftmassenmesser trotzdem tauschen'], 1,
     '<b class="grn">Geschafft!</b> Der Fehler kommt nicht wieder. Der Luftmassenmesser war nie defekt – Teiletausch hätte nichts gebracht.']
  ];
  let st = 0;
  function show() {
    const s = S[st];
    document.getElementById('fa-frage').textContent = s[0];
    document.getElementById('fa-opts').innerHTML = s[1].map((o, j) => '<button class="btn ghost" data-o="' + j + '" style="text-align:left">' + o + '</button>').join('');
    document.querySelectorAll('#fa-opts [data-o]').forEach(b => b.onclick = () => {
      const j = +b.dataset.o;
      if (j === s[2]) {
        document.getElementById('fa-t').innerHTML = s[3] + (st < S.length - 1 ? ' <button class="btn" id="fa-next" style="margin-left:8px">Weiter</button>' : ' <button class="btn ghost" id="fa-neu" style="margin-left:8px">Nochmal</button>');
        const n = document.getElementById('fa-next'); if (n) n.onclick = () => { st++; show(); };
        const r = document.getElementById('fa-neu'); if (r) r.onclick = () => { st = 0; show(); };
      } else document.getElementById('fa-t').innerHTML = '<b class="ora">Lieber nicht:</b> Das kostet Zeit oder Geld und bringt dich nicht näher an die Ursache. Probier es noch einmal.';
    });
    document.getElementById('fa-t').innerHTML = 'Wähle den nächsten Schritt.';
  }
  document.getElementById('s-fa').addEventListener('slideshow', () => { st = 0; show(); });
  show();
})();
</script>'''

STYLE = '  .symbol { font-size: 110px; }'

if __name__ == '__main__':
    seite('mm-diag-obd.html', 'OBD und Fehlerspeicher – Motormanagement', 't-mm6', THEMA, obd, STYLE, obd_js)
    seite('mm-diag-messwerte.html', 'Messwerte und Adaption – Motormanagement', 't-mm6', THEMA, mess, STYLE, mess_js)
    seite('mm-diag-fehlersuche.html', 'Systematische Fehlersuche – Motormanagement', 't-mm6', THEMA, fehler, STYLE, fehler_js)
    print('ok')
