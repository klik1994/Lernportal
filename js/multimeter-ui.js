(function () {
  const M = Multimeter;
  const root = document.getElementById('mm');
  const START = { fehler: null, modus: 'aus', buchseRot: 'VΩ', rot: null, schwarz: null, schalterZu: true, batterieAn: true, sicherungDrin: true, sicherungDurch: false, lampeDran: true };
  let schaltungId = 'einfach';
  let S = M.SCHALTUNGEN[schaltungId];
  let AUFG = Object.keys(S.AUFGABEN);
  let z = Object.assign({}, START);
  let modus = 'aufgaben', aufgabe = 0, erledigt = {}, spitze = 'rot', messungen = 0, antwortPhase = false, ergebnis = null;
  let szenario = null, wahlOrt = null, wahlArt = null, antwortFehler = '', ereignis = '';

  const LAYOUT = {
    einfach: { vb: [360, 230], draht: 'M40 95 V40 H190 M240 40 H310 V195 H40 V130', batterie: [40, 95, 130], sicherung: [122, 40], schalter: [190, 240, 40],
      lampen: { lampe: [310, 115, 'Lampe', 'l'] }, masse: [40, 195],
      punkte: { 'B+': [40, 40, 'o'], S1: [95, 40, 'o'], S2: [150, 40, 'o'], T1: [190, 40, 'o'], T2: [240, 40, 'o'], L1: [310, 80, 'r'], L2: [310, 150, 'r'], Masse: [40, 195, 'u'] } },
    parallel: { vb: [360, 250], draht: 'M30 95 V40 H150 M190 40 H320 V205 H30 V130 M235 40 V205', batterie: [30, 95, 130], sicherung: [96, 40], schalter: [150, 190, 40],
      lampen: { E1: [235, 120, 'E1', 'l'], E2: [320, 120, 'E2', 'l'] }, masse: [30, 205],
      punkte: { 'B+': [30, 40, 'o'], S1: [70, 40, 'o'], S2: [122, 40, 'o'], T1: [150, 40, 'o'], T2: [190, 40, 'o'], X1: [235, 40, 'o'], 'E1+': [235, 85, 'l'], 'E1−': [235, 155, 'l'], 'E2+': [320, 85, 'r'], 'E2−': [320, 155, 'r'], X2: [235, 205, 'u'], Masse: [30, 205, 'u'] } },
    reihe: { vb: [360, 230], draht: 'M30 95 V40 H150 M190 40 H320 V195 H30 V130', batterie: [30, 95, 130], sicherung: [96, 40], schalter: [150, 190, 40],
      lampen: { E1: [320, 112, 'E1', 'l'], E2: [200, 195, 'E2', 'o'] }, masse: [30, 195],
      punkte: { 'B+': [30, 40, 'o'], S1: [70, 40, 'o'], S2: [122, 40, 'o'], T1: [150, 40, 'o'], T2: [190, 40, 'o'], 'E1+': [320, 75, 'r'], 'E1−': [320, 150, 'r'], 'E2+': [250, 195, 'u'], 'E2−': [150, 195, 'u'], Masse: [30, 195, 'u'] } }
  };

  function wechsleSchaltung(id) {
    schaltungId = id; S = M.SCHALTUNGEN[id]; AUFG = Object.keys(S.AUFGABEN);
    aufgabe = 0; erledigt = {};
    if (modus === 'fehler') neuerFehler();
    else z = Object.assign({}, START, { modus: z.modus, buchseRot: z.buchseRot });
  }

  function setze(teil) {
    const r = S.aktualisiere(Object.assign({}, z, teil));
    z = r.zustand;
    if (r.geradeDurchgebrannt) ereignis = 'Peng! Die Sicherung ist durchgebrannt.';
  }

  function neuerFehler() {
    const f = S.SZENARIEN[Math.floor(Math.random() * S.SZENARIEN.length)];
    szenario = f;
    z = Object.assign({}, START, { fehler: f, modus: z.modus, buchseRot: z.buchseRot });
    setze({});
    ereignis = '';
    messungen = 0; antwortPhase = false; ergebnis = null; wahlOrt = null; wahlArt = null; antwortFehler = '';
  }

  function svg() {
    const L = LAYOUT[schaltungId];
    const hell = S.helligkeiten(z);
    const [W, H] = L.vb;
    let s = '<svg class="plan" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Schaltplan ' + S.name + '">';
    s += '<defs><radialGradient id="glow"><stop offset="0" stop-color="#ffd54a" stop-opacity=".95"/><stop offset=".45" stop-color="#ffc21a" stop-opacity=".45"/><stop offset="1" stop-color="#ffc21a" stop-opacity="0"/></radialGradient></defs>';
    s += '<rect x="0" y="0" width="' + W + '" height="' + H + '" rx="16" fill="#0f1d33"/>';
    s += '<path d="' + L.draht + '" fill="none" stroke="#8ea2bf" stroke-width="3.5" stroke-linejoin="round"/>';
    const [bx, b1, b2] = L.batterie;
    s += '<line x1="' + (bx - 18) + '" y1="' + (b1 + 8) + '" x2="' + (bx + 18) + '" y2="' + (b1 + 8) + '" stroke="#ecf1f8" stroke-width="3.5"/>';
    s += '<line x1="' + (bx - 10) + '" y1="' + (b2 - 8) + '" x2="' + (bx + 10) + '" y2="' + (b2 - 8) + '" stroke="#ecf1f8" stroke-width="7"/>';
    s += '<line x1="' + bx + '" y1="' + b1 + '" x2="' + bx + '" y2="' + (b1 + 8) + '" stroke="#8ea2bf" stroke-width="3.5"/><line x1="' + bx + '" y1="' + (b2 - 8) + '" x2="' + bx + '" y2="' + b2 + '" stroke="#8ea2bf" stroke-width="3.5"/>';
    s += '<text x="' + (bx + 24) + '" y="' + (b1 + 12) + '" font-size="13" font-weight="700" fill="#f05e4e">+</text><text x="' + (bx + 24) + '" y="' + (b2 - 2) + '" font-size="12" font-weight="700" fill="#cbd5e1">12 V</text>';
    if (!z.batterieAn) s += '<rect x="' + (bx - 6) + '" y="' + (b1 - 26) + '" width="12" height="18" fill="#0f1d33"/><text x="' + (bx + 24) + '" y="' + (b1 - 10) + '" font-size="11" font-weight="700" fill="#ff9d92">abgeklemmt</text>';
    const [fx, fy] = L.sicherung;
    if (z.sicherungDrin) {
      s += '<rect x="' + (fx - 20) + '" y="' + (fy - 10) + '" width="40" height="20" rx="4" fill="#213552" stroke="#cbd5e1" stroke-width="2"/>';
      s += z.sicherungDurch ? '<path d="M' + (fx - 13) + ' ' + fy + ' l8 -5 M' + (fx + 5) + ' ' + (fy + 5) + ' l8 -5" stroke="#f05e4e" stroke-width="2.5"/>' : '<line x1="' + (fx - 15) + '" y1="' + fy + '" x2="' + (fx + 15) + '" y2="' + fy + '" stroke="#cbd5e1" stroke-width="2"/>';
    } else s += '<rect x="' + (fx - 20) + '" y="' + (fy - 10) + '" width="40" height="20" rx="4" fill="#0f1d33" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3 3"/>';
    s += '<text x="' + fx + '" y="' + (fy + 26) + '" font-size="11" text-anchor="middle" fill="' + (z.sicherungDurch && z.sicherungDrin ? '#ff9d92' : '#94a4ba') + '">' + (z.sicherungDrin ? 'Sicherung' : 'gezogen') + '</text>';
    const [t1, t2, ty] = L.schalter;
    s += z.schalterZu ? '<line x1="' + t1 + '" y1="' + ty + '" x2="' + t2 + '" y2="' + ty + '" stroke="#ecf1f8" stroke-width="3.5" stroke-linecap="round"/>'
      : '<line x1="' + t1 + '" y1="' + ty + '" x2="' + (t2 - 6) + '" y2="' + (ty - 20) + '" stroke="#ecf1f8" stroke-width="3.5" stroke-linecap="round"/>';
    s += '<text x="' + ((t1 + t2) / 2) + '" y="' + (ty + 26) + '" font-size="11" text-anchor="middle" fill="#94a4ba">Schalter</text>';
    Object.keys(L.lampen).forEach(id => {
      const [cx, cy, label, lp] = L.lampen[id];
      const h = Math.min(1.6, hell[id] || 0);
      if (z.lampeDran) {
        if (h > 0.02) s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + Math.round(26 + 16 * h) + '" fill="url(#glow)" opacity="' + Math.min(1, 0.25 + h * 0.75).toFixed(2) + '"/>';
        const k = Math.min(1, h);
        const fill = 'rgb(' + Math.round(59 + 196 * k) + ',' + Math.round(66 + 147 * k) + ',' + Math.round(80 - 6 * k) + ')';
        s += '<circle cx="' + cx + '" cy="' + cy + '" r="17" fill="' + fill + '" stroke="#ecf1f8" stroke-width="2.5"/>';
        s += '<path d="M' + (cx - 12) + ' ' + (cy - 12) + ' L' + (cx + 12) + ' ' + (cy + 12) + ' M' + (cx + 12) + ' ' + (cy - 12) + ' L' + (cx - 12) + ' ' + (cy + 12) + '" stroke="#1f2937" stroke-width="2.2"/>';
      } else s += '<circle cx="' + cx + '" cy="' + cy + '" r="17" fill="#0f1d33" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3 3"/>';
      const txt = z.lampeDran ? label : 'ab';
      if (lp === 'l') s += '<text x="' + (cx - 26) + '" y="' + (cy + 4) + '" font-size="12" font-weight="700" text-anchor="end" fill="#ecf1f8">' + txt + '</text>';
      else s += '<text x="' + cx + '" y="' + (cy - 26) + '" font-size="12" font-weight="700" text-anchor="middle" fill="#ecf1f8">' + txt + '</text>';
    });
    const [mx, my] = L.masse;
    s += '<path d="M' + (mx - 12) + ' ' + (my + 10) + ' H' + (mx + 12) + ' M' + (mx - 8) + ' ' + (my + 15) + ' H' + (mx + 8) + ' M' + (mx - 4) + ' ' + (my + 20) + ' H' + (mx + 4) + '" stroke="#8ea2bf" stroke-width="2.5"/>';
    Object.keys(L.punkte).forEach(k => {
      const [x, y, lp] = L.punkte[k];
      const farbe = z.rot === k ? '#e0473a' : z.schwarz === k ? '#111418' : '#0f1d33';
      const ring = z.rot === k ? '#ffb3aa' : z.schwarz === k ? '#cbd5e1' : '#7fb2ff';
      let tx = x, ty2 = y - 12, anchor = 'middle';
      if (lp === 'r') { tx = x + 13; ty2 = y + 4; anchor = 'start'; }
      if (lp === 'l') { tx = x - 13; ty2 = y + 4; anchor = 'end'; }
      if (lp === 'u') { tx = x + 12; ty2 = y + 22; anchor = 'start'; }
      const lw = k.length * 7.5, x0 = anchor === 'start' ? tx : anchor === 'end' ? tx - lw : tx - lw / 2;
      const hx1 = Math.min(x - 16, x0), hx2 = Math.max(x + 16, x0 + lw), hy1 = Math.min(y - 16, ty2 - 12), hy2 = Math.max(y + 16, ty2 + 4);
      s += '<g class="pt" data-punkt="' + k + '" role="button" aria-label="Messpunkt ' + k + '"><rect x="' + hx1 + '" y="' + hy1 + '" width="' + (hx2 - hx1) + '" height="' + (hy2 - hy1) + '" fill="transparent"/>' +
        '<circle cx="' + x + '" cy="' + y + '" r="7" fill="' + farbe + '" stroke="' + ring + '" stroke-width="2.5"/>' +
        '<text x="' + tx + '" y="' + ty2 + '" font-size="11" font-weight="700" text-anchor="' + anchor + '" fill="#a9c4ff">' + k + '</text></g>';
    });
    return s + '</svg>';
  }

  const STELLUNGEN = [['aus', 'OFF', 150], ['V=', 'V⎓', 200], ['V~', 'V~', 245], ['Ω', 'Ω', 290], ['A=', 'A⎓', 335]];
  const BUCHSEN = [['10A', '10A', 48], ['mA', 'mA', 98], ['COM', 'COM', 148], ['VΩ', 'VΩ', 198]];
  const MODUS_TEXT = { 'V=': 'V DC', 'V~': 'V AC', 'Ω': 'OHM', 'A=': 'A DC', aus: '' };

  function geraet(r) {
    const cx = 123, cy = 205;
    let s = '<svg class="geraet" viewBox="0 0 246 470" role="group" aria-label="Multimeter">';
    s += '<rect x="3" y="3" width="240" height="384" rx="30" fill="#f7b612"/>';
    s += '<rect x="15" y="15" width="216" height="360" rx="22" fill="#2c313a"/>';
    s += '<rect x="31" y="30" width="184" height="86" rx="10" fill="#c4d6be" stroke="#1b2a12" stroke-width="2"/>';
    s += '<text x="43" y="52" font-size="13" font-weight="800" fill="#1b2a12">' + (MODUS_TEXT[z.modus] || '') + '</text>';
    s += '<text x="203" y="102" text-anchor="end" font-size="34" font-weight="700" font-family="ui-monospace,Menlo,Consolas,monospace" fill="#19231c" aria-live="polite">' + (r.anzeige || '') + '</text>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="78" fill="#23272e"/>';
    STELLUNGEN.forEach(([w, t, a]) => {
      const rad = a * Math.PI / 180, on = z.modus === w;
      const lx = cx + 64 * Math.cos(rad), ly = cy + 64 * Math.sin(rad);
      s += '<g class="mmk" data-dreh="' + w + '" role="button" tabindex="0" aria-label="Wahlschalter ' + t + '" aria-pressed="' + on + '">' +
        '<circle cx="' + lx.toFixed(1) + '" cy="' + ly.toFixed(1) + '" r="19" fill="' + (on ? '#f7b612' : '#353b45') + '"/>' +
        '<text x="' + lx.toFixed(1) + '" y="' + (ly + 5).toFixed(1) + '" text-anchor="middle" font-size="' + (w === 'aus' ? 11 : 15) + '" font-weight="800" fill="' + (on ? '#2c313a' : '#c9d1dc') + '">' + t + '</text></g>';
    });
    const akt = STELLUNGEN.find(x => x[0] === z.modus) || STELLUNGEN[0];
    const pr = akt[2] * Math.PI / 180;
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="36" fill="#15181d" stroke="#505662" stroke-width="3"/>';
    s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + (cx + 30 * Math.cos(pr)).toFixed(1) + '" y2="' + (cy + 30 * Math.sin(pr)).toFixed(1) + '" stroke="#f7b612" stroke-width="8" stroke-linecap="round"/>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="6" fill="#505662"/>';
    BUCHSEN.forEach(([w, t, x]) => {
      const com = w === 'COM', on = !com && z.buchseRot === w;
      const inner = '<text x="' + x + '" y="318" text-anchor="middle" font-size="12" font-weight="800" fill="#c9d1dc">' + t + '</text>' +
        '<circle cx="' + x + '" cy="345" r="16" fill="' + (com ? '#141619' : '#c0392b') + '" stroke="' + (on ? '#f7b612' : '#5a606c') + '" stroke-width="' + (on ? 4 : 2) + '"/>' +
        '<circle cx="' + x + '" cy="345" r="6" fill="#0a0a0c"/>';
      s += com ? '<g>' + inner + '</g>' : '<g class="mmk" data-buchse="' + w + '" role="button" tabindex="0" aria-label="Rote Messleitung in Buchse ' + t + '" aria-pressed="' + on + '">' + inner + '</g>';
    });
    const rx = (BUCHSEN.find(b => b[0] === z.buchseRot) || BUCHSEN[3])[2];
    s += '<path d="M148 345 C 148 420, 100 410, 92 466" fill="none" stroke="#1b1d22" stroke-width="7" stroke-linecap="round"/>';
    s += '<path d="M' + rx + ' 345 C ' + rx + ' 425, 160 410, 156 466" fill="none" stroke="#e0473a" stroke-width="7" stroke-linecap="round"/>';
    s += '<circle cx="148" cy="345" r="9" fill="#1b1d22" stroke="#6b717c" stroke-width="2"/><circle cx="' + rx + '" cy="345" r="9" fill="#e0473a" stroke="#ffb3aa" stroke-width="2"/>';
    s += '</svg>';
    return '<div class="geraet-box"><div class="geraet-hilfe"><p class="lbl" style="margin:0">Multimeter</p><p class="muted" style="margin:4px 0 0">Tippe auf eine Stellung am Drehschalter und auf die Buchse für die rote Messleitung. Schwarz steckt immer in COM.</p></div>' + s + '</div>';
  }

  function btn(attr, wert, text, aktiv, cls) {
    return '<button data-' + attr + '="' + wert + '" class="' + (aktiv ? 'on ' : '') + (cls || '') + '">' + text + '</button>';
  }

  function render() {
    const r = S.messe(z);
    let h = '<p class="lbl">Schaltung</p><div class="seg">' + Object.keys(M.SCHALTUNGEN).map(id => btn('schaltung', id, { einfach: 'Einfach', parallel: 'Parallel', reihe: 'Reihe' }[id], schaltungId === id)).join('') + '</div>';
    h += '<div class="seg">' + btn('modus', 'aufgaben', 'Messaufgaben', modus === 'aufgaben') + btn('modus', 'fehler', 'Fehlersuche', modus === 'fehler') + '</div>';
    if (modus === 'aufgaben') {
      const id = AUFG[aufgabe];
      h += '<div class="card"><p class="lbl">Aufgabe ' + (aufgabe + 1) + ' von ' + AUFG.length + '</p><p style="margin:0"><b>' + S.AUFGABEN[id].text + '</b></p>' +
        (erledigt[id] ? '<div class="meld ok" style="margin:8px 0 0">Richtig gemessen.' + (aufgabe + 1 < AUFG.length ? ' <button data-naechste="1">Nächste Aufgabe</button>' : ' Alle Aufgaben geschafft. Probier jetzt die Fehlersuche.') + '</div>' : '') + '</div>';
    } else {
      h += '<div class="card"><p class="lbl">Kunde sagt:</p><p style="margin:0 0 6px"><b>' + S.symptom(szenario) + '</b></p><p class="muted" style="margin:0">Finde den Fehler durch Messen. Messungen: ' + messungen + '</p></div>';
    }
    h += svg();
    if (ereignis) h += '<div class="meld warn">' + ereignis + '</div>';
    h += '<div class="seg">' + btn('schalter', '1', z.schalterZu ? 'Schalter: an' : 'Schalter: aus', z.schalterZu) + btn('batterie', '1', z.batterieAn ? 'Batterie: dran' : 'Batterie: ab', !z.batterieAn) + '</div>';
    h += '<div class="seg">' + btn('ziehen', '1', z.sicherungDrin ? 'Sicherung ziehen' : 'Sicherung einsetzen', !z.sicherungDrin) + btn('neusich', '1', 'Neue Sicherung', false) + btn('lampe', '1', S.LAMPEN.length > 1 ? (z.lampeDran ? 'Lampen abstecken' : 'Lampen anstecken') : (z.lampeDran ? 'Lampe abstecken' : 'Lampe anstecken'), !z.lampeDran) + '</div>';
    h += geraet(r);
    h += '<p class="lbl">Erst Messspitze wählen, dann Messpunkt im Schaltplan antippen</p><div class="seg">' +
      btn('spitze', 'rot', 'Rote Spitze: ' + (z.rot || '–'), spitze === 'rot', 'probe-rot') + btn('spitze', 'schwarz', 'Schwarze Spitze: ' + (z.schwarz || '–'), spitze === 'schwarz', 'probe-schwarz') + '</div>';
    if (r.meldung) h += '<div class="meld ' + (r.ok ? 'info' : 'warn') + '">' + r.meldung + '</div>';
    if (modus === 'fehler') {
      if (ergebnis) {
        const zeigen = ergebnis.richtig || ergebnis.loesung;
        h += '<div class="meld ' + (ergebnis.richtig ? 'ok' : 'warn') + '"><b>' + ergebnis.rueckmeldung + (ergebnis.richtig ? ' Gefunden mit ' + messungen + ' Messungen.' : '') + '</b>' + (zeigen ? '<br>' + ergebnis.erklaerung : '') + '</div>';
        if (zeigen) h += '<button class="primary" style="width:100%" data-neu="1">Neuer Fehler</button>';
        else h += '<div class="seg"><button class="primary" data-weiter="1">Weiter suchen</button><button data-loesung="1">Lösung zeigen</button></div>';
      } else if (antwortPhase) {
        h += '<div class="card"><p class="lbl">1. Wo sitzt der Fehler?</p><div class="seg wrap">' + Object.keys(S.ORTE).map(o => btn('ort', o, S.ORTE[o].name, wahlOrt === o)).join('') + '</div>';
        h += '<p class="lbl">2. Was für ein Fehler ist es?</p><div class="seg wrap">' + Object.keys(S.ARTEN).map(a => btn('art', a, S.ARTEN[a], wahlArt === a)).join('') + '</div>';
        if (antwortFehler) h += '<p class="meld warn">' + antwortFehler + '</p>';
        h += '<button class="primary" style="width:100%" data-antwort="1">Antwort prüfen</button></div>';
      } else {
        h += '<button class="primary" style="width:100%" data-gefunden="1">Fehler gefunden</button>';
      }
    }
    root.innerHTML = h;
  }

  function nachMessung() {
    if (modus === 'aufgaben') { const id = AUFG[aufgabe]; if (S.aufgabeErfuellt(id, z)) erledigt[id] = true; }
  }

  root.addEventListener('click', e => {
    const p = e.target.closest('[data-punkt]');
    if (p) {
      const k = p.dataset.punkt;
      if (spitze === 'rot') { z.rot = k; spitze = z.schwarz ? 'rot' : 'schwarz'; } else { z.schwarz = k; spitze = 'rot'; }
      if (z.rot && z.schwarz && z.modus !== 'aus') messungen++;
      ereignis = '';
      nachMessung(); render(); return;
    }
    const b = e.target.closest('button, [data-dreh], [data-buchse]');
    if (!b) return;
    const d = b.dataset;
    ereignis = '';
    if (d.schaltung) wechsleSchaltung(d.schaltung);
    else if (d.modus) {
      modus = d.modus;
      if (modus === 'fehler') neuerFehler(); else z = Object.assign({}, START, { modus: z.modus, buchseRot: z.buchseRot });
    } else if (d.dreh) { z.modus = d.dreh; nachMessung(); }
    else if (d.buchse) { z.buchseRot = d.buchse; nachMessung(); }
    else if (d.spitze) spitze = d.spitze;
    else if (d.schalter) { setze({ schalterZu: !z.schalterZu }); nachMessung(); }
    else if (d.batterie) { setze({ batterieAn: !z.batterieAn }); nachMessung(); }
    else if (d.ziehen) setze({ sicherungDrin: !z.sicherungDrin });
    else if (d.neusich) {
      const r = S.neueSicherung(z);
      z = r.zustand;
      ereignis = r.geradeDurchgebrannt ? 'Die neue Sicherung ist sofort wieder durchgebrannt! Es muss noch einen anderen Fehler geben.' : 'Neue Sicherung eingesetzt.';
    }
    else if (d.lampe) setze({ lampeDran: !z.lampeDran });
    else if (d.naechste) { aufgabe++; z.rot = null; z.schwarz = null; }
    else if (d.gefunden) antwortPhase = true;
    else if (d.ort) { wahlOrt = d.ort; antwortFehler = ''; }
    else if (d.art) { wahlArt = d.art; antwortFehler = ''; }
    else if (d.antwort) {
      if (!wahlOrt || !wahlArt) antwortFehler = 'Wähle zuerst die Stelle und die Fehlerart aus.';
      else ergebnis = S.pruefeAntwort(szenario, wahlOrt, wahlArt);
    }
    else if (d.weiter) { ergebnis = null; antwortPhase = false; wahlOrt = null; wahlArt = null; }
    else if (d.loesung) ergebnis.loesung = true;
    else if (d.neu) neuerFehler();
    render();
  });

  root.addEventListener('keydown', e => {
    const g = e.target.closest && e.target.closest('.mmk');
    if (g && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); g.dispatchEvent(new MouseEvent('click', { bubbles: true })); }
  });

  render();
})();
