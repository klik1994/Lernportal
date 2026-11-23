// Diagnose-Werkstatt: fiktives Übungsauto, Elektrik-Modell, Steuergeräte, Fehlerspeicher.
// Reine Logik ohne Oberfläche.
const Diagnose = (() => {
  const U = 12.6;
  const R_STD = { kabel: 0.02, masse: 0.005, sicherung: 0.005, stecker: 0.002, schalter: 0.02, kontakt: 0.02, ausgang: 0.05 };
  const R_UEBERGANG = 3, R_SCHLUSS = 0.01;

  // ---------- Bauteile und Leitungen des Übungsautos ----------
  // sys: Stromkreis (für Schaltplan und Antwortliste)
  const E = [];
  const el = (id, typ, a, b, name, sys, extra) => E.push(Object.assign({ id, typ, a, b, name, sys }, extra || {}));
  // Versorgung und Masse
  el('F21', 'sicherung', 'B+', 'F21.2', 'Sicherung F21 (Bordnetz-SG, Licht)', 'Versorgung', { amp: 20 });
  el('w-f21', 'kabel', 'F21.2', 'A10.T30a', 'Leitung F21 – Bordnetz-SG (T30a)', 'Versorgung');
  el('F22', 'sicherung', 'B+', 'F22.2', 'Sicherung F22 (Bordnetz-SG, Blinker/Bremslicht)', 'Versorgung', { amp: 15 });
  el('w-f22', 'kabel', 'F22.2', 'A10.T30b', 'Leitung F22 – Bordnetz-SG (T30b)', 'Versorgung');
  el('w-a10m', 'kabel', 'A10.31', 'M3', 'Masseleitung Bordnetz-SG', 'Versorgung');
  el('m1', 'masse', 'M1', 'M', 'Massepunkt M1 (Motorraum links)', 'Versorgung');
  el('m2', 'masse', 'M2', 'M', 'Massepunkt M2 (Motorraum rechts)', 'Versorgung');
  el('m3', 'masse', 'M3', 'M', 'Massepunkt M3 (A-Säule links)', 'Versorgung');
  el('m5', 'masse', 'M5', 'M', 'Massepunkt M5 (Kofferraum)', 'Versorgung');
  // Abblendlicht
  const lampe = (pre, x, nr, ausgangKnoten, masse, name, sys, r, leitName, masseName) => {
    el('w-' + pre, 'kabel', ausgangKnoten, x + '.' + nr[0], leitName, sys);
    el(x + '-' + nr[0], 'stecker', x + '.' + nr[0], x + '.' + nr[0] + '*', 'Stecker ' + x + ' Pin ' + nr[0], sys, { stecker: x });
    el('e-' + pre, 'lampe', x + '.' + nr[0] + '*', x + '.' + nr[1] + '*', name, sys, { r });
    if (masse) {
      el(x + '-' + nr[1], 'stecker', x + '.' + nr[1] + '*', x + '.' + nr[1], 'Stecker ' + x + ' Pin ' + nr[1], sys, { stecker: x });
      el('w-' + pre + '-m', 'kabel', x + '.' + nr[1], masse, masseName, sys);
    }
  };
  el('o-abl', 'ausgang', 'A10.T30a', 'A10.12', 'Endstufe Abblendlicht links im Bordnetz-SG', 'Licht', { kanal: 'abl', seite: 'high' });
  lampe('abl', 'X4', ['1', '2'], 'A10.12', 'M1', 'Glühlampe Abblendlicht links (E1)', 'Licht', 2.6, 'Leitung Bordnetz-SG – Scheinwerfer links (X4 Pin 1)', 'Masseleitung Scheinwerfer links (X4 Pin 2 – M1)');
  el('o-abr', 'ausgang', 'A10.T30a', 'A10.13', 'Endstufe Abblendlicht rechts im Bordnetz-SG', 'Licht', { kanal: 'abr', seite: 'high' });
  lampe('abr', 'X5', ['1', '2'], 'A10.13', 'M2', 'Glühlampe Abblendlicht rechts (E2)', 'Licht', 2.6, 'Leitung Bordnetz-SG – Scheinwerfer rechts (X5 Pin 1)', 'Masseleitung Scheinwerfer rechts (X5 Pin 2 – M2)');
  // Blinker
  el('o-bll', 'ausgang', 'A10.T30b', 'A10.20', 'Endstufe Blinker links im Bordnetz-SG', 'Blinker', { kanal: 'bll', seite: 'high' });
  lampe('blvl', 'X6', ['1', '2'], 'A10.20', 'M1', 'Blinkerlampe vorne links (E3)', 'Blinker', 6.9, 'Leitung Bordnetz-SG – Blinker vorne links (X6 Pin 1)', 'Masseleitung Blinker vorne links (X6 Pin 2 – M1)');
  lampe('blhl', 'X30', ['2', '4'], 'A10.20', 'M5', 'Blinkerlampe hinten links (E5)', 'Blinker', 6.9, 'Leitung Bordnetz-SG – Rückleuchte links (X30 Pin 2)', 'Masseleitung Rückleuchte links (X30 Pin 4 – M5)');
  el('o-blr', 'ausgang', 'A10.T30b', 'A10.21', 'Endstufe Blinker rechts im Bordnetz-SG', 'Blinker', { kanal: 'blr', seite: 'high' });
  lampe('blvr', 'X7', ['1', '2'], 'A10.21', 'M2', 'Blinkerlampe vorne rechts (E4)', 'Blinker', 6.9, 'Leitung Bordnetz-SG – Blinker vorne rechts (X7 Pin 1)', 'Masseleitung Blinker vorne rechts (X7 Pin 2 – M2)');
  lampe('blhr', 'X31', ['2', '4'], 'A10.21', 'M5', 'Blinkerlampe hinten rechts (E6)', 'Blinker', 6.9, 'Leitung Bordnetz-SG – Rückleuchte rechts (X31 Pin 2)', 'Masseleitung Rückleuchte rechts (X31 Pin 4 – M5)');
  // Bremslicht (Lampen teilen sich Pin 4 der Rückleuchten)
  el('o-br', 'ausgang', 'A10.T30b', 'A10.24', 'Endstufe Bremslicht im Bordnetz-SG', 'Bremslicht', { kanal: 'br', seite: 'high' });
  lampe('brl', 'X30', ['3', '4'], 'A10.24', null, 'Bremslichtlampe links (E7)', 'Bremslicht', 6.9, 'Leitung Bordnetz-SG – Rückleuchte links (X30 Pin 3)');
  lampe('brr', 'X31', ['3', '4'], 'A10.24', null, 'Bremslichtlampe rechts (E8)', 'Bremslicht', 6.9, 'Leitung Bordnetz-SG – Rückleuchte rechts (X31 Pin 3)');
  el('F8', 'sicherung', 'B+', 'F8.2', 'Sicherung F8 (Bremslichtschalter)', 'Bremslicht', { amp: 10 });
  el('w-s5-1', 'kabel', 'F8.2', 'X12.1', 'Leitung F8 – Bremslichtschalter (X12 Pin 1)', 'Bremslicht');
  el('X12-1', 'stecker', 'X12.1', 'X12.1*', 'Stecker X12 Pin 1', 'Bremslicht', { stecker: 'X12' });
  el('s5', 'schalter', 'X12.1*', 'X12.2*', 'Bremslichtschalter (S5)', 'Bremslicht', { steuer: 'bremse' });
  el('X12-2', 'stecker', 'X12.2*', 'X12.2', 'Stecker X12 Pin 2', 'Bremslicht', { stecker: 'X12' });
  el('w-s5-2', 'kabel', 'X12.2', 'A10.40', 'Signalleitung Bremslichtschalter – Bordnetz-SG (X12 Pin 2)', 'Bremslicht');
  el('i-a10-40', 'eingang', 'A10.40', 'A10.31', 'Eingang Bremslichtschalter im Bordnetz-SG', 'Bremslicht', { r: 4700 });
  // Hupe
  el('F15', 'sicherung', 'B+', 'F15.2', 'Sicherung F15 (Hupe)', 'Hupe', { amp: 15 });
  el('w-k7-30', 'kabel', 'F15.2', 'K7.30', 'Leitung F15 – Relais K7 (30)', 'Hupe');
  el('w-k7-86', 'kabel', 'F15.2', 'K7.86', 'Leitung F15 – Relais K7 (86)', 'Hupe');
  el('k7-sp', 'spule', 'K7.86', 'K7.85', 'Hupenrelais K7 (Spule)', 'Hupe', { relais: 'K7', r: 80 });
  el('k7-k', 'kontakt', 'K7.30', 'K7.87', 'Hupenrelais K7 (Kontakt)', 'Hupe', { relais: 'K7' });
  el('w-k7-85', 'kabel', 'K7.85', 'S10.1', 'Leitung Relais K7 (85) – Hupentaster', 'Hupe');
  el('s10', 'schalter', 'S10.1', 'S10.2', 'Hupentaster im Lenkrad (S10)', 'Hupe', { steuer: 'hupe' });
  el('w-s10-m', 'kabel', 'S10.2', 'M3', 'Masseleitung Hupentaster (– M3)', 'Hupe');
  el('w-hupe', 'kabel', 'K7.87', 'X9.1', 'Leitung Relais K7 (87) – Hupe (X9 Pin 1)', 'Hupe');
  el('X9-1', 'stecker', 'X9.1', 'X9.1*', 'Stecker X9 Pin 1', 'Hupe', { stecker: 'X9' });
  el('h1', 'last', 'X9.1*', 'X9.2*', 'Hupe (H1)', 'Hupe', { r: 3 });
  el('X9-2', 'stecker', 'X9.2*', 'X9.2', 'Stecker X9 Pin 2', 'Hupe', { stecker: 'X9' });
  el('w-hupe-m', 'kabel', 'X9.2', 'M1', 'Masseleitung Hupe (X9 Pin 2 – M1)', 'Hupe');
  // Fensterheber Fahrertür
  el('F30', 'sicherung', 'B+', 'F30.2', 'Sicherung F30 (Türsteuergerät Fahrer)', 'Fensterheber', { amp: 25 });
  el('w-tsg', 'kabel', 'F30.2', 'A20.30', 'Leitung F30 – Türsteuergerät (T30)', 'Fensterheber');
  el('w-tsg-m', 'kabel', 'A20.31', 'M3', 'Masseleitung Türsteuergerät (– M3)', 'Fensterheber');
  el('o-fh1h', 'ausgang', 'A20.30', 'A20.M1', 'Endstufe Motor Pin M1 (Plus)', 'Fensterheber', { kanal: 'fh1', seite: 'high' });
  el('o-fh1l', 'ausgang', 'A20.M1', 'A20.31', 'Endstufe Motor Pin M1 (Masse)', 'Fensterheber', { kanal: 'fh1', seite: 'low' });
  el('o-fh2h', 'ausgang', 'A20.30', 'A20.M2', 'Endstufe Motor Pin M2 (Plus)', 'Fensterheber', { kanal: 'fh2', seite: 'high' });
  el('o-fh2l', 'ausgang', 'A20.M2', 'A20.31', 'Endstufe Motor Pin M2 (Masse)', 'Fensterheber', { kanal: 'fh2', seite: 'low' });
  el('w-fh1', 'kabel', 'A20.M1', 'X20.1', 'Leitung Türsteuergerät – Fensterhebermotor (X20 Pin 1)', 'Fensterheber');
  el('X20-1', 'stecker', 'X20.1', 'X20.1*', 'Stecker X20 Pin 1', 'Fensterheber', { stecker: 'X20' });
  el('m20', 'last', 'X20.1*', 'X20.2*', 'Fensterhebermotor Fahrer (M20)', 'Fensterheber', { r: 1.5 });
  el('X20-2', 'stecker', 'X20.2*', 'X20.2', 'Stecker X20 Pin 2', 'Fensterheber', { stecker: 'X20' });
  el('w-fh2', 'kabel', 'X20.2', 'A20.M2', 'Leitung Türsteuergerät – Fensterhebermotor (X20 Pin 2)', 'Fensterheber');

  const EL = {}; E.forEach(e => { EL[e.id] = e; });
  const KNOTEN = [];
  E.forEach(e => [e.a, e.b].forEach(k => { if (!KNOTEN.includes(k)) KNOTEN.push(k); }));
  const IDX = {}; KNOTEN.forEach((k, i) => { IDX[k] = i; });

  // Orte, die als Fehlerursache gewählt werden können
  const RELAIS = { K7: 'Hupenrelais K7' };
  const FEHLERORTE = E.filter(e => ['kabel', 'masse', 'lampe', 'last', 'schalter', 'sicherung'].includes(e.typ)).map(e => ({ id: e.id, name: e.name, sys: e.sys }))
    .concat(Object.keys(RELAIS).map(k => ({ id: k, name: RELAIS[k], sys: 'Hupe' })));
  const ARTEN = [['unterbrechung', 'Unterbrechung'], ['uebergang', 'Übergangswiderstand'], ['masse', 'Kurzschluss nach Masse'], ['plus', 'Kurzschluss nach Plus'], ['defekt', 'Bauteil defekt']];

  // ---------- Steuergeräte ----------
  const SG = {
    A10: { name: 'Bordnetz-Steuergerät (A10)' },
    A20: { name: 'Türsteuergerät Fahrer (A20)' },
    J1: { name: 'Motorsteuergerät (J1)' }
  };
  const UEBERW = [
    { kanal: 'abl', el: 'o-abl', inom: 4.8, code: 'B1A12', name: 'Abblendlicht links' },
    { kanal: 'abr', el: 'o-abr', inom: 4.8, code: 'B1A13', name: 'Abblendlicht rechts' },
    { kanal: 'bll', el: 'o-bll', inom: 3.6, code: 'B1C20', name: 'Blinker links' },
    { kanal: 'blr', el: 'o-blr', inom: 3.6, code: 'B1C21', name: 'Blinker rechts' },
    { kanal: 'br', el: 'o-br', inom: 3.6, code: 'B1C24', name: 'Bremsleuchten' }
  ];
  const STELLGLIEDER = {
    A10: [['abl', 'Abblendlicht links'], ['abr', 'Abblendlicht rechts'], ['bll', 'Blinker links'], ['blr', 'Blinker rechts'], ['br', 'Bremsleuchten']],
    A20: [['auf', 'Fensterheber Fahrer: schließen'], ['ab', 'Fensterheber Fahrer: öffnen']],
    J1: []
  };

  // ---------- Fälle ----------
  const FAELLE = [
    { id: 'abblend', lj: 1, kunde: 'Das Abblendlicht links geht nicht.', fehler: { el: 'w-abl', art: 'unterbrechung' },
      erklaerung: 'Die Leitung vom Bordnetz-Steuergerät (A10 Pin 12) zum Scheinwerfer links (X4 Pin 1) ist unterbrochen. Am Steuergerät liegen 12 V an, am Stecker X4 Pin 1 kommt nichts an. Das Steuergerät erkennt keinen Strom und speichert „Unterbrechung“.' },
    { id: 'bremslicht', lj: 1, kunde: 'Bei einer Polizeikontrolle wurde mir gesagt, dass meine Bremslichter nicht gehen.', fehler: { el: 's5', art: 'defekt' },
      erklaerung: 'Der Bremslichtschalter S5 schaltet nicht durch. Im Istwert bleibt er auf „nicht betätigt“, obwohl das Pedal getreten ist; das Motorsteuergerät meldet eine Unplausibilität. Über die Stellglieddiagnose leuchten die Bremslichter: Lampen und Leitungen sind in Ordnung.' },
    { id: 'blinker', lj: 1, kunde: 'Wenn ich links blinke, tickt der Blinker doppelt so schnell.', fehler: { el: 'e-blhl', art: 'defekt' },
      erklaerung: 'Die Blinkerlampe hinten links ist durchgebrannt. Das Bordnetz-Steuergerät misst nur den halben Strom, meldet „Lampenausfall“ und blinkt zur Warnung doppelt so schnell.' },
    { id: 'hupe', lj: 1, kunde: 'Die Hupe geht nicht mehr.', fehler: { el: 'w-hupe', art: 'masse' },
      erklaerung: 'Die Leitung vom Relais K7 (Klemme 87) zur Hupe hat einen Kurzschluss nach Masse. Sobald das Relais anzieht, fließt ein sehr hoher Strom und die Sicherung F15 brennt durch. Die durchgebrannte Sicherung ist nur die Folge, nicht die Ursache. Die Hupe hängt an keinem Steuergerät, darum steht nichts im Fehlerspeicher.' },
    { id: 'fenster', lj: 1, kunde: 'Das Fenster auf der Fahrerseite geht weder hoch noch runter.', fehler: { el: 'w-fh1', art: 'unterbrechung' },
      erklaerung: 'Die Leitung vom Türsteuergerät (Pin M1) zum Fensterhebermotor (X20 Pin 1) ist im Türübergang gebrochen. Typisch: Die Leitungen knicken dort bei jedem Öffnen der Tür. Am Steuergerät kommt die Spannung raus, am Motorstecker nicht.' }
  ];
  const fall = id => FAELLE.find(f => f.id === id);

  // ---------- Zustand ----------
  function neu(fallId) {
    const st = {
      fall: fallId, fehler: fallId ? Object.assign({}, fall(fallId).fehler) : null,
      batterie: true, zuendung: false, licht: 'aus', blinker: 'aus', bremse: false, hupe: false, fenster: 'aus',
      sich: {}, stecker: {}, relais: {}, stell: {}, speicher: { A10: [], A20: [], J1: [] }, fensterPos: 0, phase: true
    };
    if (fallId) kundeBenutzt(st);
    return st;
  }

  // Der Kunde hat alles einmal benutzt: Fehlerspeicher füllt sich, Sicherungen brennen ggf. durch.
  function kundeBenutzt(st) {
    const schritte = [{ zuendung: true }, { licht: 'abblend' }, { licht: 'aus', blinker: 'links' }, { blinker: 'rechts' }, { blinker: 'aus', bremse: true }, { bremse: false, fenster: 'auf' }, { fenster: 'ab' }, { fenster: 'aus', hupe: true }, { hupe: false, zuendung: false }];
    schritte.forEach(s => { Object.assign(st, s); simuliere(st); });
  }

  // ---------- Rechnen ----------
  function loese(fest, kanten, quellen) {
    const n = KNOTEN.length, unbek = [], pos = {};
    for (let i = 0; i < n; i++) if (!(i in fest)) { pos[i] = unbek.length; unbek.push(i); }
    const m = unbek.length;
    const A = Array.from({ length: m }, () => new Float64Array(m + 1));
    unbek.forEach((u, j) => { A[j][j] += 1e-9; });
    kanten.forEach(([a, b, g]) => {
      const fa = a in fest, fb = b in fest;
      if (!fa) { const j = pos[a]; A[j][j] += g; if (fb) A[j][m] += g * fest[b]; else A[j][pos[b]] -= g; }
      if (!fb) { const j = pos[b]; A[j][j] += g; if (fa) A[j][m] += g * fest[a]; else A[j][pos[a]] -= g; }
    });
    (quellen || []).forEach(([k, s]) => { if (k in pos) A[pos[k]][m] += s; });
    for (let c = 0; c < m; c++) {
      let p = c;
      for (let r = c + 1; r < m; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
      if (p !== c) { const t = A[c]; A[c] = A[p]; A[p] = t; }
      const piv = A[c][c];
      for (let r = 0; r < m; r++) {
        if (r === c || !A[r][c]) continue;
        const f = A[r][c] / piv;
        for (let k = c; k <= m; k++) A[r][k] -= f * A[c][k];
      }
    }
    const v = new Array(n).fill(0);
    Object.keys(fest).forEach(i => { v[i] = fest[i]; });
    unbek.forEach((u, j) => { v[u] = A[j][m] / A[j][j]; });
    return v;
  }

  const fehlerAn = (st, id, art) => st.fehler && st.fehler.el === id && (!art || st.fehler.art === art);

  // Widerstand eines Elements im aktuellen Zustand (Infinity = offen)
  function widerstandEl(e, st, cmd, relaisZu, kalt) {
    const f = st.fehler && st.fehler.el === e.id ? st.fehler.art : null;
    if (f === 'unterbrechung' || f === 'defekt') return Infinity;
    if (e.relais && (st.relais[e.relais] === 'raus' || fehlerAn(st, e.relais))) return Infinity;
    switch (e.typ) {
      case 'sicherung': return st.sich[e.id] ? Infinity : R_STD.sicherung;
      case 'stecker': return st.stecker[e.stecker] ? Infinity : R_STD.stecker;
      case 'schalter': return st[e.steuer] ? (f === 'uebergang' ? R_UEBERGANG : R_STD.schalter) : Infinity;
      case 'kontakt': return relaisZu[e.relais] ? R_STD.kontakt : Infinity;
      case 'ausgang': return cmd[e.kanal] === e.seite ? R_STD.ausgang : Infinity;
      case 'lampe': return kalt ? e.r * 0.12 : e.r;
      case 'last': case 'spule': case 'eingang': return e.r;
      default: return f === 'uebergang' ? R_UEBERGANG : R_STD[e.typ];
    }
  }

  function kanten(st, cmd, relaisZu, kalt, extra) {
    const k = [];
    E.forEach(e => { const r = widerstandEl(e, st, cmd, relaisZu, kalt); if (r !== Infinity) k.push([IDX[e.a], IDX[e.b], 1 / r]); });
    if (st.fehler && (st.fehler.art === 'masse' || st.fehler.art === 'plus') && EL[st.fehler.el]) {
      k.push([IDX[EL[st.fehler.el].b], IDX[st.fehler.art === 'masse' ? 'M' : 'B+'], 1 / R_SCHLUSS]);
    }
    (extra || []).forEach(x => k.push(x));
    return k;
  }

  // Logik der Steuergeräte: welche Endstufen schalten?
  function logik(st, V) {
    const cmd = {}, s = st.stell, kl15 = st.zuendung;
    const pA = V[IDX['A10.T30a']] > 9, pB = V[IDX['A10.T30b']] > 9, pT = V[IDX['A20.30']] > 9;
    if (pA && ((kl15 && st.licht === 'abblend') || s.abl)) cmd.abl = 'high';
    if (pA && ((kl15 && st.licht === 'abblend') || s.abr)) cmd.abr = 'high';
    if (pB && st.phase && ((kl15 && st.blinker === 'links') || s.bll)) cmd.bll = 'high';
    if (pB && st.phase && ((kl15 && st.blinker === 'rechts') || s.blr)) cmd.blr = 'high';
    if (pB && (V[IDX['A10.40']] > 6 || s.br)) cmd.br = 'high';
    const fenster = s.auf ? 'auf' : s.ab ? 'ab' : (kl15 ? st.fenster : 'aus');
    if (pT) {
      cmd.fh1 = fenster === 'auf' ? 'high' : 'low';
      cmd.fh2 = fenster === 'ab' ? 'high' : 'low';
    }
    return cmd;
  }

  function strom(e, v, st, cmd, relaisZu, kalt) {
    const r = widerstandEl(e, st, cmd, relaisZu, kalt);
    return r === Infinity ? 0 : (v[IDX[e.a]] - v[IDX[e.b]]) / r;
  }

  // Rechnet den Zustand durch (inkl. Relais, Steuergeräte, durchbrennende Sicherungen, Fehlerspeicher)
  function simuliere(st, opt) {
    opt = opt || {};
    if (!st.batterie) {
      const v = KNOTEN.map(() => 0);
      return { v, cmd: {}, relaisZu: {}, I: id => 0, U: k => 0 };
    }
    let v = KNOTEN.map(() => 0), cmd = {}, relaisZu = {};
    const fest = {}; fest[IDX['B+']] = U; fest[IDX.M] = 0;
    for (let runde = 0; runde < 12; runde++) {
      const neuCmd = logik(st, v);
      const neuRel = { K7: Math.abs(v[IDX['K7.86']] - v[IDX['K7.85']]) > 7 };
      v = loese(fest, kanten(st, neuCmd, neuRel, false, opt.extra));
      let durch = false;
      E.filter(e => e.typ === 'sicherung' && !st.sich[e.id]).forEach(e => {
        if (Math.abs(strom(e, v, st, neuCmd, neuRel)) > e.amp) { st.sich[e.id] = 'durch'; durch = true; }
      });
      const stabil = !durch && JSON.stringify(neuCmd) === JSON.stringify(cmd) && JSON.stringify(neuRel) === JSON.stringify(relaisZu);
      cmd = neuCmd; relaisZu = neuRel;
      if (stabil && runde > 0) break;
    }
    if (durch2(st, v, cmd, relaisZu)) v = loese(fest, kanten(st, cmd, relaisZu, false, opt.extra));
    const I = id => strom(EL[id], v, st, cmd, relaisZu);
    if (!opt.ohneSpeicher) ueberwache(st, v, cmd, I);
    return { v, cmd, relaisZu, I, U: k => v[IDX[k]] };
  }
  function durch2(st, v, cmd, relaisZu) {
    let d = false;
    E.filter(e => e.typ === 'sicherung' && !st.sich[e.id]).forEach(e => {
      if (Math.abs(strom(e, v, st, cmd, relaisZu)) > e.amp) { st.sich[e.id] = 'durch'; d = true; }
    });
    return d;
  }

  function merke(st, sg, code, text) {
    const liste = st.speicher[sg];
    const da = liste.find(x => x.code === code);
    if (da) da.anzahl++; else liste.push({ code, text, anzahl: 1 });
  }

  function ueberwache(st, v, cmd, I) {
    UEBERW.forEach(u => {
      if (cmd[u.kanal] !== 'high') return;
      const i = I(u.el);
      if (i < 0.1 * u.inom) merke(st, 'A10', u.code + '-13', u.name + ': Unterbrechung');
      else if (i < 0.75 * u.inom) merke(st, 'A10', u.code + '-1B', u.name + ': Lampenausfall');
      else if (i > 2 * u.inom) merke(st, 'A10', u.code + '-11', u.name + ': Kurzschluss nach Masse');
    });
    const fhAktiv = cmd.fh1 === 'high' || cmd.fh2 === 'high';
    if (fhAktiv && Math.abs(I('m20')) < 1) merke(st, 'A20', 'B1F20-13', 'Fensterhebermotor Fahrer: Unterbrechung');
    const schalter = v[IDX['A10.40']] > 6;
    if (st.zuendung && st.bremse !== schalter) merke(st, 'J1', 'P0504', 'Bremslichtschalter: Signal unplausibel zum Bremspedalsensor');
  }

  // ---------- Was sieht man am Auto? ----------
  function beobachte(st) {
    const sim = simuliere(st, { ohneSpeicher: true });
    const hell = id => { const e = EL[id], i = Math.abs(sim.I(id)); return Math.min(1.5, (i * e.r) ** 2 / (U * U)); };
    const blinkerSchnell = s => {
      const u = UEBERW.find(x => x.kanal === s);
      const s2 = Object.assign({}, st, { phase: true });
      const sim2 = simuliere(s2, { ohneSpeicher: true });
      const i = sim2.I(u.el);
      return i > 0.1 * u.inom && i < 0.75 * u.inom;
    };
    const an = Object.assign({}, st, { phase: true });
    const simAn = simuliere(an, { ohneSpeicher: true });
    const hellAn = id => { const e = EL[id], i = Math.abs(simAn.I(id)); return Math.min(1.5, (i * e.r) ** 2 / (U * U)); };
    return {
      abl: hell('e-abl'), abr: hell('e-abr'), brl: hell('e-brl'), brr: hell('e-brr'),
      blvl: hellAn('e-blvl'), blhl: hellAn('e-blhl'), blvr: hellAn('e-blvr'), blhr: hellAn('e-blhr'),
      blinktL: !!simAn.cmd.bll, blinktR: !!simAn.cmd.blr, schnellL: blinkerSchnell('bll'), schnellR: blinkerSchnell('blr'),
      hupe: Math.abs(sim.I('h1')) > 2, motor: Math.abs(sim.I('m20')) > 2 ? (sim.I('m20') > 0 ? 'auf' : 'ab') : null,
      relaisKlick: !!sim.relaisZu.K7
    };
  }

  // Bedienung mit Folgen (Fensterscheibe fährt)
  function bediene(st, aenderung) {
    Object.assign(st, aenderung);
    simuliere(st);
    const b = beobachte(st);
    if (b.motor === 'auf') st.fensterPos = 0;
    if (b.motor === 'ab') st.fensterPos = 100;
    return b;
  }

  // ---------- Messen ----------
  const sternFrei = (st, k) => !k.includes('*') || !!st.stecker[k.split('.')[0]];

  function spannung(st, rot, schwarz) {
    const a = simuliere(Object.assign({}, st, { phase: true, sich: Object.assign({}, st.sich) }), { ohneSpeicher: true });
    const b = simuliere(Object.assign({}, st, { phase: false, sich: Object.assign({}, st.sich) }), { ohneSpeicher: true });
    const ua = a.U(rot) - a.U(schwarz), ub = b.U(rot) - b.U(schwarz);
    return Math.abs(ua - ub) > 0.5 ? { wert: ua, wechsel: ub } : { wert: ua };
  }

  function widerstand(st, a, b) {
    // Fremdspannung?
    const sim = simuliere(Object.assign({}, st, { sich: Object.assign({}, st.sich) }), { ohneSpeicher: true });
    if (st.batterie && (Math.abs(sim.U(a)) > 0.2 || Math.abs(sim.U(b)) > 0.2 || Math.abs(sim.U(a) - sim.U(b)) > 0.05)) return { fremd: true };
    if (a === b) return { wert: 0 };
    const extra = st.batterie ? [[IDX['B+'], IDX.M, 100]] : [];
    const kalt = Object.assign({}, st, { phase: false });
    const fest = {}; fest[IDX[b]] = 0;
    const v = loese(fest, kanten(kalt, {}, {}, true, extra), [[IDX[a], 1]]);
    const r = v[IDX[a]];
    return { wert: r > 4e7 ? Infinity : r };
  }

  // Prüflampe (ca. 5 W) zwischen zwei Punkten
  function prueflampe(st, a, b) {
    const s2 = Object.assign({}, st, { phase: true, sich: Object.assign({}, st.sich) });
    const sim = simuliere(s2, { ohneSpeicher: true, extra: [[IDX[a], IDX[b], 1 / 30]] });
    const u = Math.abs(sim.U(a) - sim.U(b));
    const s3 = Object.assign({}, st, { phase: false, sich: Object.assign({}, st.sich) });
    const u2 = Math.abs(simuliere(s3, { ohneSpeicher: true, extra: [[IDX[a], IDX[b], 1 / 30]] }).U(a) - simuliere(s3, { ohneSpeicher: true, extra: [[IDX[a], IDX[b], 1 / 30]] }).U(b));
    const stufe = x => x > 9 ? 'hell' : x > 3 ? 'schwach' : 'aus';
    return { stufe: stufe(u), wechsel: stufe(u) !== stufe(u2) };
  }

  // ---------- Tester ----------
  function testerVerbindung(st) {
    if (!st.batterie) return 'Keine Spannung am Diagnosestecker (Batterie abgeklemmt).';
    if (!st.zuendung) return 'Keine Kommunikation. Schalte die Zündung ein.';
    return '';
  }

  function istwerte(st, sg) {
    const sim = simuliere(st, { ohneSpeicher: true });
    const a = x => Math.abs(sim.I(x)).toFixed(1).replace('.', ',') + ' A';
    const v = k => sim.U(k).toFixed(1).replace('.', ',') + ' V';
    if (sg === 'A10') return [
      ['Klemme 15 (Zündung)', st.zuendung ? 'ein' : 'aus'],
      ['Spannung Klemme 30a', v('A10.T30a')], ['Spannung Klemme 30b', v('A10.T30b')],
      ['Lichtschalter', { aus: 'aus', abblend: 'Abblendlicht' }[st.licht]],
      ['Blinkerhebel', { aus: 'Mitte', links: 'links', rechts: 'rechts' }[st.blinker]],
      ['Bremslichtschalter', sim.U('A10.40') > 6 ? 'betätigt' : 'nicht betätigt'],
      ['Strom Abblendlicht links', a('o-abl')], ['Strom Abblendlicht rechts', a('o-abr')],
      ['Strom Blinker links', a('o-bll')], ['Strom Blinker rechts', a('o-blr')], ['Strom Bremsleuchten', a('o-br')]
    ];
    if (sg === 'A20') return [
      ['Versorgungsspannung', v('A20.30')],
      ['Schalter Fensterheber', { aus: 'nicht betätigt', auf: 'schließen', ab: 'öffnen' }[st.fenster]],
      ['Strom Fensterhebermotor', a('m20')],
      ['Scheibenposition', st.fensterPos === 0 ? 'geschlossen' : 'offen']
    ];
    return [
      ['Motordrehzahl', '0 1/min'], ['Batteriespannung', (st.batterie ? U : 0).toFixed(1).replace('.', ',') + ' V'],
      ['Bremspedalsensor', st.bremse ? 'betätigt' : 'nicht betätigt'],
      ['Bremslichtschalter (vom Bordnetz-SG)', sim.U('A10.40') > 6 ? 'betätigt' : 'nicht betätigt']
    ];
  }

  function stellglied(st, sg, id, an) {
    if (sg === 'A20') { st.stell.auf = false; st.stell.ab = false; }
    st.stell[id] = !!an;
    simuliere(st);
    const b = beobachte(st);
    if (b.motor === 'auf') st.fensterPos = 0;
    if (b.motor === 'ab') st.fensterPos = 100;
    return b;
  }

  function loescheSpeicher(st, sg) { st.speicher[sg] = []; simuliere(st); return st.speicher[sg]; }

  // ---------- Bewertung ----------
  function pruefe(st, ort, art) {
    const f = fall(st.fall).fehler;
    const zielOrt = EL[f.el] && EL[f.el].relais ? EL[f.el].relais : f.el;
    const bauteil = ['lampe', 'last', 'schalter'].includes((EL[zielOrt] || {}).typ);
    const artOk = art === f.art || (bauteil && ['defekt', 'unterbrechung'].includes(art) && ['defekt', 'unterbrechung'].includes(f.art));
    const ortOk = ort === zielOrt;
    let hinweis = '';
    if (!ortOk && EL[ort] && EL[ort].typ === 'sicherung' && st.speicherFolge !== false && f.art === 'masse') hinweis = 'Die durchgebrannte Sicherung ist nur die Folge. Was hat sie durchbrennen lassen?';
    return { richtig: ortOk && artOk, ortOk, artOk, hinweis, erklaerung: fall(st.fall).erklaerung, loesung: { ort: zielOrt, art: f.art } };
  }

  const ortName = id => (EL[id] && EL[id].name) || RELAIS[id] || id;

  return { U, E, EL, KNOTEN, FEHLERORTE, ARTEN, SG, STELLGLIEDER, FAELLE, RELAIS, fall, neu, simuliere, beobachte, bediene, sternFrei, spannung, widerstand, prueflampe, testerVerbindung, istwerte, stellglied, loescheSpeicher, pruefe, ortName };
})();
if (typeof module !== 'undefined') module.exports = Diagnose;
