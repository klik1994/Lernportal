(function () {
  const C = CanBus;
  const root = document.getElementById('can');
  const VOLT = [0.5, 1, 2, 5], ZEIT = [2, 10, 50];
  const PAARE = [['6-14', 'Pin 6 – Pin 14', 'CAN-High gegen CAN-Low'], ['6-4', 'Pin 6 – Pin 4', 'CAN-High gegen Masse'], ['14-4', 'Pin 14 – Pin 4', 'CAN-Low gegen Masse'], ['6-16', 'Pin 6 – Pin 16', 'CAN-High gegen Plus'], ['14-16', 'Pin 14 – Pin 16', 'CAN-Low gegen Plus']];
  const SYMPTOM = {
    'r-einer': 'Ab und zu leuchten Warnleuchten auf, im Fehlerspeicher stehen sporadische Kommunikationsfehler.',
    default: 'Viele Warnleuchten im Kombiinstrument, mehrere Steuergeräte melden „keine Kommunikation“ (U0100 …).'
  };
  let modus = 'lernen', fehler = 'normal', voltDiv = 1, zeitDiv = 10, kanal = { A: true, B: true, D: false };
  let zuendung = true, messung = null, messFehler = '', antwortPhase = false, wahl = null, ergebnis = null, antwortFehler = '', messungen = 0;

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const komma = (x, d) => x.toFixed(d).replace('.', ',').replace('-0,0', '0,0');
  const btn = (attr, wert, text, aktiv, cls) => '<button data-' + attr + '="' + wert + '" class="' + (aktiv ? 'on ' : '') + (cls || '') + '">' + text + '</button>';

  function neuerFehler() {
    fehler = C.FEHLER[Math.floor(Math.random() * C.FEHLER.length)].id;
    zuendung = true; messung = null; messFehler = ''; antwortPhase = false; wahl = null; ergebnis = null; antwortFehler = ''; messungen = 0;
  }

  function oszi() {
    const W = 400, H = 300, dx = W / 10, dy = H / 8, null0 = H - dy;
    const y = v => Math.max(2, Math.min(H - 2, null0 - v / voltDiv * dy));
    const k = zuendung ? C.kurven(fehler, { zeitDiv }) : [[0, 0, 0], [zeitDiv * 10, 0, 0]];
    const x = t => t / (zeitDiv * 10) * W;
    let s = '<svg class="oszi" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Oszilloskop-Bild von CAN-High und CAN-Low">';
    s += '<rect width="' + W + '" height="' + H + '" rx="10" fill="#0a1220"/>';
    for (let i = 1; i < 10; i++) s += '<line x1="' + i * dx + '" y1="0" x2="' + i * dx + '" y2="' + H + '" stroke="#1d2b44" stroke-width="1"/>';
    for (let j = 1; j < 8; j++) s += '<line x1="0" y1="' + j * dy + '" x2="' + W + '" y2="' + j * dy + '" stroke="#1d2b44" stroke-width="1"/>';
    s += '<line x1="0" y1="' + null0 + '" x2="' + W + '" y2="' + null0 + '" stroke="#40577c" stroke-width="1.5" stroke-dasharray="4 4"/>';
    s += '<text x="6" y="' + (null0 - 5) + '" font-size="11" fill="#7f93b3">0 V</text>';
    const spur = (idx, farbe) => '<polyline fill="none" stroke="' + farbe + '" stroke-width="2.2" stroke-linejoin="round" points="' +
      k.map(p => x(p[0]).toFixed(1) + ',' + y(idx === 3 ? p[1] - p[2] : p[idx]).toFixed(1)).join(' ') + '"/>';
    if (kanal.B) s += spur(2, '#34c778');
    if (kanal.A) s += spur(1, '#f7b612');
    if (kanal.D) s += spur(3, '#f05e4e');
    const max = Math.max(...k.map(p => Math.max(kanal.A ? p[1] : -99, kanal.B ? p[2] : -99, kanal.D ? p[1] - p[2] : -99)));
    if (max > 7 * voltDiv + 0.01) s += '<text x="' + (W - 8) + '" y="16" text-anchor="end" font-size="12" font-weight="700" fill="#ff9d92">▲ Signal oben außerhalb</text>';
    s += '<text x="8" y="16" font-size="12" font-weight="700" fill="#cbd5e1">' + komma(voltDiv, voltDiv < 1 ? 1 : 0) + ' V/div · ' + zeitDiv + ' µs/div</text>';
    if (!zuendung) s += '<text x="' + W / 2 + '" y="' + H / 2 + '" text-anchor="middle" font-size="14" font-weight="700" fill="#94a4ba">Zündung aus – der Bus schläft</text>';
    return s + '</svg>';
  }

  function pegelAnzeige() {
    if (!zuendung) return '';
    const k = C.kurven(fehler, { zeitDiv: 10 });
    const mm = i => [Math.min(...k.map(p => p[i])), Math.max(...k.map(p => p[i]))];
    const [aMin, aMax] = mm(1), [bMin, bMax] = mm(2);
    return '<div class="pegel"><span><i style="background:#f7b612"></i>A (CAN-H): ' + komma(aMin, 1) + ' … ' + komma(aMax, 1) + ' V</span>' +
      '<span><i style="background:#34c778"></i>B (CAN-L): ' + komma(bMin, 1) + ' … ' + komma(bMax, 1) + ' V</span></div>';
  }

  function stecker() {
    const pins = { 4: 'Masse', 5: 'Signal-Masse', 6: 'CAN-H', 14: 'CAN-L', 16: '+12 V' };
    let s = '<svg class="dlc" viewBox="0 0 260 96" role="img" aria-label="Diagnosestecker mit Pin 4, 5, 6, 14 und 16">';
    s += '<path d="M14 10 H246 L232 86 H28 Z" fill="#213552" stroke="#8ea2bf" stroke-width="2"/>';
    for (let i = 1; i <= 16; i++) {
      const reihe = i <= 8 ? 0 : 1, sp = (i - 1) % 8;
      const cx = 40 + sp * 25.7 + reihe * 4, cy = 34 + reihe * 30;
      const farbe = i === 6 ? '#f7b612' : i === 14 ? '#34c778' : i === 4 || i === 5 ? '#94a4ba' : i === 16 ? '#f05e4e' : '#0f1d33';
      s += '<circle cx="' + cx.toFixed(1) + '" cy="' + cy + '" r="8" fill="' + farbe + '" stroke="#cbd5e1" stroke-width="1.2"/>';
      if (pins[i]) s += '<text x="' + cx.toFixed(1) + '" y="' + (cy + 4) + '" text-anchor="middle" font-size="9" font-weight="800" fill="#0e192b">' + i + '</text>';
    }
    return s + '</svg><p class="muted dlc-legende"><b style="color:#f7b612">Pin 6</b> CAN-High · <b style="color:#34c778">Pin 14</b> CAN-Low · <b>Pin 4/5</b> Masse · <b style="color:#f05e4e">Pin 16</b> +12 V</p>';
  }

  function render() {
    let h = '<div class="seg">' + btn('modus', 'lernen', 'Signal kennenlernen', modus === 'lernen') + btn('modus', 'fehler', 'Fehlersuche', modus === 'fehler') + '</div>';
    if (modus === 'lernen') {
      h += '<div class="card"><p class="lbl">Fehlerbild ansehen</p><div class="seg wrap">' + btn('bild', 'normal', 'Kein Fehler', fehler === 'normal') +
        C.FEHLER.map(f => btn('bild', f.id, f.name, fehler === f.id)).join('') + '</div><p class="muted" style="margin:6px 0 0">' + esc(C.info(fehler).erklaerung) + '</p></div>';
    } else {
      h += '<div class="card"><p class="lbl">Kunde sagt:</p><p style="margin:0 0 6px"><b>' + (SYMPTOM[fehler] || SYMPTOM.default) + '</b></p><p class="muted" style="margin:0">Schau dir das Signal am Diagnosestecker an und miss die Widerstände. Messungen: ' + messungen + '</p></div>';
    }
    h += '<div class="oszi-box">' + oszi() + pegelAnzeige() + '</div>';
    h += '<p class="lbl">Kanäle</p><div class="seg">' + btn('kanal', 'A', 'A: CAN-High', kanal.A, 'k-a') + btn('kanal', 'B', 'B: CAN-Low', kanal.B, 'k-b') + btn('kanal', 'D', 'A − B', kanal.D, 'k-d') + '</div>';
    h += '<p class="lbl">Messbereich</p><div class="seg">' + VOLT.map(v => btn('volt', v, komma(v, v < 1 ? 1 : 0) + ' V/div', voltDiv === v)).join('') + '</div>';
    h += '<p class="lbl">Zeitbasis</p><div class="seg">' + ZEIT.map(t => btn('zeit', t, t + ' µs/div', zeitDiv === t)).join('') + '</div>';
    h += '<div class="card"><p class="lbl">Diagnosestecker (OBD)</p>' + stecker() +
      '<div class="seg" style="margin-top:10px">' + btn('zuendung', '1', zuendung ? 'Zündung: an' : 'Zündung: aus, Batterie ab', !zuendung) + '</div>' +
      '<p class="lbl">Widerstand messen (Multimeter, Ω)</p><div class="seg wrap">' + PAARE.map(([id, t]) => btn('paar', id, t, messung && messung.paar === id)).join('') + '</div>';
    if (messFehler) h += '<div class="meld warn">' + messFehler + '</div>';
    if (messung) h += '<div class="mini-display"><span>' + esc(PAARE.find(p => p[0] === messung.paar)[2]) + '</span><b>' + C.widerstandText(messung.wert) + '</b></div>';
    h += '</div>';
    if (modus === 'fehler') {
      if (ergebnis) {
        const zeigen = ergebnis.richtig || ergebnis.loesung;
        h += '<div class="meld ' + (ergebnis.richtig ? 'ok' : 'warn') + '"><b>' + ergebnis.rueckmeldung + (ergebnis.richtig ? ' Gefunden mit ' + messungen + ' Messungen.' : '') + '</b>' + (zeigen ? '<br><b>' + esc(C.info(fehler).name) + ':</b> ' + esc(ergebnis.erklaerung) : '') + '</div>';
        h += zeigen ? '<button class="primary" style="width:100%" data-neu="1">Neuer Fehler</button>' : '<div class="seg"><button class="primary" data-weiter="1">Weiter suchen</button><button data-loesung="1">Lösung zeigen</button></div>';
      } else if (antwortPhase) {
        h += '<div class="card"><p class="lbl">Welcher Fehler liegt vor?</p><div class="seg wrap">' + C.FEHLER.map(f => btn('wahl', f.id, f.name, wahl === f.id)).join('') + '</div>';
        if (antwortFehler) h += '<p class="meld warn">' + antwortFehler + '</p>';
        h += '<button class="primary" style="width:100%" data-antwort="1">Antwort prüfen</button></div>';
      } else h += '<button class="primary" style="width:100%" data-gefunden="1">Fehler gefunden</button>';
    }
    root.innerHTML = h;
  }

  root.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    const d = b.dataset;
    if (d.modus) { modus = d.modus; if (modus === 'fehler') neuerFehler(); else { fehler = 'normal'; zuendung = true; messung = null; messFehler = ''; } }
    else if (d.bild) { fehler = d.bild; messung = null; messFehler = ''; }
    else if (d.kanal) kanal[d.kanal] = !kanal[d.kanal];
    else if (d.volt) voltDiv = +d.volt;
    else if (d.zeit) zeitDiv = +d.zeit;
    else if (d.zuendung) { zuendung = !zuendung; messung = null; messFehler = ''; }
    else if (d.paar) {
      if (zuendung) { messFehler = 'Widerstand nie unter Spannung messen! Erst Zündung aus und Batterie abklemmen.'; messung = null; }
      else { messFehler = ''; messung = { paar: d.paar, wert: C.info(fehler).widerstand[d.paar] }; messungen++; }
    }
    else if (d.gefunden) antwortPhase = true;
    else if (d.wahl) { wahl = d.wahl; antwortFehler = ''; }
    else if (d.antwort) { if (!wahl) antwortFehler = 'Wähle zuerst einen Fehler aus.'; else ergebnis = C.pruefe(fehler, wahl); }
    else if (d.weiter) { ergebnis = null; antwortPhase = false; wahl = null; }
    else if (d.loesung) ergebnis.loesung = true;
    else if (d.neu) neuerFehler();
    render();
  });

  render();
})();
