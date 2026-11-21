const Multimeter = (() => {
  const U_BATT = 12.6;
  const KNOTEN = ['B+', 'S1', 'S2', 'T1', 'T2', 'L1', 'L2', 'Masse'];
  const IDX = {}; KNOTEN.forEach((k, i) => { IDX[k] = i; });
  const MASSE = 7;
  const R_LAMPE_HEISS = 6.0, R_LAMPE_KALT = 0.8, R_UEBERGANG_KABEL = 4.0, R_UEBERGANG_SCHALTER = 3.0, R_SCHLUSS = 0.01;
  const SICHERUNG_A = 15;

  const ORTE = {
    K1: { name: 'Leitung Batterie–Sicherung', von: 'B+', bis: 'S1', el: 0 },
    sicherung: { name: 'Sicherung', von: 'S1', bis: 'S2', el: 1 },
    K2: { name: 'Leitung Sicherung–Schalter', von: 'S2', bis: 'T1', el: 2, schluss: 'T1' },
    schalter: { name: 'Schalter', von: 'T1', bis: 'T2', el: 3 },
    K3: { name: 'Leitung Schalter–Lampe', von: 'T2', bis: 'L1', el: 4, schluss: 'L1' },
    lampe: { name: 'Lampe', von: 'L1', bis: 'L2', el: 5 },
    K4: { name: 'Masseleitung Lampe–Masse', von: 'L2', bis: 'Masse', el: 6 }
  };
  const ARTEN = { unterbrechung: 'Unterbrechung', uebergang: 'Übergangswiderstand', masse: 'Kurzschluss nach Masse', plus: 'Kurzschluss nach Plus' };

  const SZENARIEN = [
    { ort: 'sicherung', art: 'unterbrechung' }, { ort: 'schalter', art: 'unterbrechung' }, { ort: 'schalter', art: 'uebergang' },
    { ort: 'lampe', art: 'unterbrechung' },
    { ort: 'K1', art: 'unterbrechung' }, { ort: 'K2', art: 'unterbrechung' }, { ort: 'K3', art: 'unterbrechung' }, { ort: 'K4', art: 'unterbrechung' },
    { ort: 'K1', art: 'uebergang' }, { ort: 'K2', art: 'uebergang' }, { ort: 'K3', art: 'uebergang' }, { ort: 'K4', art: 'uebergang' },
    { ort: 'K2', art: 'masse' }, { ort: 'K3', art: 'masse' }, { ort: 'K3', art: 'plus' }
  ];

  const ist = (f, ort, art) => !!f && f.ort === ort && f.art === art;

  function elemente(z, kalt) {
    const f = z.fehler;
    const r = [0.01, 0.01, 0.01, 0.02, 0.03, kalt ? R_LAMPE_KALT : R_LAMPE_HEISS, 0.02];
    ['K1', 'K2', 'K3', 'K4'].forEach(k => {
      if (ist(f, k, 'unterbrechung')) r[ORTE[k].el] = Infinity;
      if (ist(f, k, 'uebergang')) r[ORTE[k].el] = R_UEBERGANG_KABEL;
    });
    if (!z.sicherungDrin || z.sicherungDurch || ist(f, 'sicherung', 'unterbrechung')) r[1] = Infinity;
    if (!z.schalterZu || ist(f, 'schalter', 'unterbrechung')) r[3] = Infinity;
    else if (ist(f, 'schalter', 'uebergang')) r[3] = R_UEBERGANG_SCHALTER;
    if (!z.lampeDran || ist(f, 'lampe', 'unterbrechung')) r[5] = Infinity;
    return r;
  }

  function kanten(z, kalt, mitQuelle) {
    const r = elemente(z, kalt);
    const k = [];
    r.forEach((w, i) => { if (w !== Infinity) k.push([i, i + 1, 1 / w]); });
    const f = z.fehler;
    if (f && f.art === 'masse' && ORTE[f.ort].schluss) k.push([IDX[ORTE[f.ort].schluss], MASSE, 1 / R_SCHLUSS]);
    if (f && f.art === 'plus' && ORTE[f.ort].schluss) k.push([IDX[ORTE[f.ort].schluss], mitQuelle ? 'P' : 0, 1 / R_SCHLUSS]);
    return k;
  }

  function loese(n, fest, kantenListe, quellen) {
    const unbek = [];
    for (let i = 0; i < n; i++) if (!(i in fest)) unbek.push(i);
    const pos = {}; unbek.forEach((u, j) => { pos[u] = j; });
    const m = unbek.length;
    const A = Array.from({ length: m }, () => new Array(m + 1).fill(0));
    unbek.forEach((u, j) => { A[j][j] += 1e-12; });
    const add = (a, b, g) => {
      const va = typeof a === 'number' && a in fest ? fest[a] : null;
      const vb = b === 'P' ? U_BATT : (b in fest ? fest[b] : null);
      if (va === null) { const j = pos[a]; A[j][j] += g; if (vb === null) A[j][pos[b]] -= g; else A[j][m] += g * vb; }
      if (b !== 'P' && vb === null) { const j = pos[b]; A[j][j] += g; if (va === null) A[j][pos[a]] -= g; else A[j][m] += g * va; }
    };
    kantenListe.forEach(([a, b, g]) => add(a, b, g));
    (quellen || []).forEach(([knoten, strom]) => { if (knoten in pos) A[pos[knoten]][m] += strom; });
    for (let c = 0; c < m; c++) {
      let p = c;
      for (let r = c + 1; r < m; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
      [A[c], A[p]] = [A[p], A[c]];
      for (let r = 0; r < m; r++) {
        if (r === c || !A[r][c]) continue;
        const fak = A[r][c] / A[c][c];
        for (let k = c; k <= m; k++) A[r][k] -= fak * A[c][k];
      }
    }
    const v = new Array(n).fill(0);
    Object.keys(fest).forEach(i => { v[i] = fest[i]; });
    unbek.forEach((u, j) => { v[u] = A[j][m] / A[j][j]; });
    return v;
  }

  function potentiale(z) {
    if (!z.batterieAn) return KNOTEN.map(() => 0);
    const fest = { 0: U_BATT }; fest[MASSE] = 0;
    return loese(KNOTEN.length, fest, kanten(z, false, true));
  }

  function aktualisiere(z) {
    const neu = Object.assign({}, z);
    let geradeDurchgebrannt = false;
    if (neu.batterieAn && neu.sicherungDrin && !neu.sicherungDurch && !ist(neu.fehler, 'sicherung', 'unterbrechung')) {
      const v = potentiale(neu);
      const strom = (v[1] - v[2]) / 0.01;
      if (Math.abs(strom) > SICHERUNG_A) { neu.sicherungDurch = true; geradeDurchgebrannt = true; }
    }
    return { zustand: neu, geradeDurchgebrannt };
  }

  function neueSicherung(z) {
    const neu = Object.assign({}, z, { sicherungDrin: true, sicherungDurch: false });
    if (ist(neu.fehler, 'sicherung', 'unterbrechung')) neu.fehler = null;
    return aktualisiere(neu);
  }

  function widerstand(z, a, b) {
    if (a === b) return 0;
    const fest = {}; fest[IDX[b]] = 0;
    const v = loese(KNOTEN.length, fest, kanten(z, true, false), [[IDX[a], 1]]);
    return v[IDX[a]] > 1e7 ? Infinity : v[IDX[a]];
  }

  function helligkeit(z) {
    const v = potentiale(z);
    const n = potentiale({ fehler: null, batterieAn: true, sicherungDrin: true, sicherungDurch: false, schalterZu: true, lampeDran: true });
    if (!z.lampeDran || ist(z.fehler, 'lampe', 'unterbrechung')) return 0;
    const h = (v[5] - v[6]) ** 2 / (n[5] - n[6]) ** 2;
    return Math.round(h * 100) / 100;
  }

  function symptom(f) {
    const start = aktualisiere({ fehler: f, batterieAn: true, sicherungDrin: true, sicherungDurch: false, schalterZu: true, lampeDran: true }).zustand;
    const an = helligkeit(start);
    const aus = helligkeit(aktualisiere(Object.assign({}, start, { schalterZu: false })).zustand);
    if (aus > 0.1) return 'Die Lampe geht nicht mehr aus, auch wenn der Schalter aus ist.';
    if (an < 0.05) return 'Die Lampe leuchtet nicht.';
    if (an < 0.8) return 'Die Lampe leuchtet nur schwach.';
    return 'Mit der Lampe stimmt etwas nicht.';
  }

  const komma = (x, d) => x.toFixed(d).replace('.', ',');

  function messe(z) {
    const leer = { anzeige: '', wert: null, ok: false, meldung: '' };
    if (z.modus === 'aus') return Object.assign(leer, { meldung: 'Das Messgerät ist aus. Dreh den Wahlschalter.' });
    if (!z.rot || !z.schwarz) return Object.assign(leer, { anzeige: '0,0', meldung: 'Halte beide Messspitzen an einen Messpunkt.' });
    const v = potentiale(z);
    const diff = v[IDX[z.rot]] - v[IDX[z.schwarz]];
    if (z.buchseRot !== 'VΩ') {
      if (Math.abs(diff) > 0.5) return { anzeige: '0,00 A', wert: null, ok: false, meldung: 'Kurzschluss! Die rote Leitung steckt in der Strombuchse. Das Messgerät hat fast keinen Widerstand. Die Sicherung im Messgerät ist durchgebrannt.' };
      if (z.modus !== 'A=') return { anzeige: '0,0', wert: null, ok: false, meldung: 'Falsche Buchse: Für Spannung und Widerstand gehört die rote Leitung in VΩ.' };
      return { anzeige: '0,00 A', wert: 0, ok: false, meldung: 'Für eine Strommessung muss der Stromkreis aufgetrennt werden. In dieser Übung misst du Spannung und Widerstand.' };
    }
    if (z.modus === 'A=') return { anzeige: '0,00 A', wert: null, ok: false, meldung: 'Für Strom gehört die rote Leitung in die A-Buchse, und das Messgerät muss in Reihe geschaltet werden.' };
    if (z.modus === 'V~') return { anzeige: '0,0 V~', wert: 0, ok: false, meldung: 'Das Bordnetz hat Gleichspannung. Stell den Wahlschalter auf V⎓ (DC).' };
    if (z.modus === 'V=') {
      if (!z.batterieAn) return { anzeige: '0,0 V', wert: 0, ok: true, meldung: 'Die Batterie ist abgeklemmt, darum liegt keine Spannung an.' };
      const w = Math.round(diff * 10) / 10;
      return { anzeige: komma(w, 1) + ' V', wert: w, ok: true, meldung: w < 0 ? 'Minuszeichen: Die Messspitzen sind vertauscht.' : '' };
    }
    if (z.modus === 'Ω') {
      if (z.batterieAn) return { anzeige: 'Fehler', wert: null, ok: false, meldung: 'Widerstand nie unter Spannung messen! Erst die Batterie abklemmen.' };
      const r = widerstand(z, z.rot, z.schwarz);
      if (r === Infinity) return { anzeige: 'OL', wert: Infinity, ok: true, meldung: 'OL: keine Verbindung zwischen den Messpunkten.' };
      const w = Math.round(r * 10) / 10;
      return { anzeige: komma(w, 1) + ' Ω', wert: w, ok: true, meldung: '' };
    }
    return leer;
  }

  function erklaerung(f) {
    const o = ORTE[f.ort];
    if (f.ort === 'sicherung') return 'Die Sicherung war durchgebrannt, ohne dass ein Kurzschluss vorlag. Vor der Sicherung (S1) lagen 12,6 V gegen Masse an, dahinter (S2) 0 V. Mit einer neuen Sicherung funktionierte alles.';
    if (f.ort === 'lampe') return 'Die Lampe war durchgebrannt. Über der Lampe (L1 gegen L2) lagen die vollen 12,6 V an, trotzdem leuchtete sie nicht. Stromlos gemessen zeigte sie OL.';
    if (f.ort === 'schalter' && f.art === 'unterbrechung') return 'Der Schalter schaltete nicht durch. Auch eingeschaltet lagen über dem Schalter (T1 gegen T2) 12,6 V an. Stromlos zeigte er OL.';
    if (f.ort === 'schalter') return 'Der Schalter hatte einen Übergangswiderstand. Über dem geschlossenen Schalter (T1 gegen T2) fielen ca. 4 V ab. Normal sind fast 0 V.';
    if (f.art === 'unterbrechung') return 'Die ' + o.name + ' war unterbrochen. ' + (f.ort === 'K4'
      ? 'An L2 lagen 12,6 V gegen Masse an. Bei einer intakten Masseleitung sind es fast 0 V.'
      : 'Am Anfang der Leitung (' + o.von + ') lagen 12,6 V gegen Masse an, am Ende (' + o.bis + ') 0 V. Stromlos: ' + o.von + ' gegen ' + o.bis + ' zeigte OL.');
    if (f.art === 'uebergang') return 'Die ' + o.name + ' hatte einen Übergangswiderstand (z. B. Korrosion am Stecker). Bei eingeschalteter Lampe fielen über der Leitung (' + o.von + ' gegen ' + o.bis + ') ca. 5 V ab. Normal sind fast 0 V.';
    if (f.art === 'masse') return 'Die ' + o.name + ' hatte einen Kurzschluss nach Masse (z. B. Isolierung durchgescheuert). Darum ist die Sicherung durchgebrannt. Sie ist nur die Folge, nicht die Ursache: Eine neue Sicherung brennt sofort wieder durch. So findest du ihn: Batterie abklemmen, Lampe abstecken, Schalter aus. Dann zeigt die Leitung gegen Masse 0 Ω statt OL.';
    if (f.art === 'plus') return 'Die ' + o.name + ' hatte einen Kurzschluss nach Plus (Kontakt zu einer anderen Plusleitung). Die Lampe bekam Plus am Schalter vorbei. Bei ausgeschaltetem Schalter lagen an T2 und L1 trotzdem 12,6 V an.';
    return '';
  }

  function pruefeAntwort(f, ort, art) {
    const richtig = f.ort === ort && f.art === art;
    let rueckmeldung = richtig ? 'Richtig! Stelle und Fehlerart stimmen.' : 'Leider falsch.';
    if (!richtig && f.art === 'masse' && ort === 'sicherung') rueckmeldung = 'Nicht ganz: Die Sicherung ist zwar durchgebrannt, aber das ist nur die Folge. Die Ursache sitzt woanders.';
    else if (!richtig && f.ort === ort) rueckmeldung = 'Die Stelle stimmt, aber die Fehlerart nicht.';
    else if (!richtig && f.art === art) rueckmeldung = 'Die Fehlerart stimmt, aber die Stelle nicht.';
    return { richtig, rueckmeldung, erklaerung: erklaerung(f) };
  }

  const AUFGABEN = {
    batterie: { text: 'Miss die Batteriespannung.', pruef: (z, r) => z.modus === 'V=' && z.batterieAn && z.rot === 'B+' && z.schwarz === 'Masse' && r.wert !== null && r.wert > 12 },
    'lampe-v': { text: 'Schalter an: Miss den Spannungsfall an der Lampe.', pruef: (z, r) => z.modus === 'V=' && z.batterieAn && z.schalterZu && [z.rot, z.schwarz].sort().join() === 'L1,L2' && r.wert > 11 },
    'lampe-r': { text: 'Miss den Widerstand der Lampe.', pruef: (z, r) => z.modus === 'Ω' && !z.batterieAn && [z.rot, z.schwarz].sort().join() === 'L1,L2' && r.wert !== null && r.wert < 2 }
  };

  function aufgabeErfuellt(id, z) {
    const voll = Object.assign({ sicherungDrin: true, sicherungDurch: false, lampeDran: true }, z);
    return !!AUFGABEN[id].pruef(voll, messe(voll));
  }

  return { KNOTEN, ORTE, ARTEN, SZENARIEN, AUFGABEN, potentiale, widerstand, helligkeit, aktualisiere, neueSicherung, symptom, messe, pruefeAntwort, aufgabeErfuellt };
})();
if (typeof module !== 'undefined') module.exports = Multimeter;
