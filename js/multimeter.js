const Multimeter = (() => {
  const U_BATT = 12.6;
  const R_LAMPE_HEISS = 6.0, R_LAMPE_KALT = 0.8, R_UEBERGANG_KABEL = 4.0, R_UEBERGANG_SCHALTER = 3.0, R_SCHLUSS = 0.01;
  const SICHERUNG_A = 15;
  const ARTEN = { unterbrechung: 'Unterbrechung', uebergang: 'Übergangswiderstand', masse: 'Kurzschluss nach Masse', plus: 'Kurzschluss nach Plus' };
  const komma = (x, d) => x.toFixed(d).replace('.', ',');
  const ist = (f, ort, art) => !!f && f.ort === ort && f.art === art;

  function loese(n, fest, kantenListe, quellen) {
    const unbek = [];
    for (let i = 0; i < n; i++) if (!(i in fest)) unbek.push(i);
    const pos = {}; unbek.forEach((u, j) => { pos[u] = j; });
    const m = unbek.length;
    const A = Array.from({ length: m }, () => new Array(m + 1).fill(0));
    unbek.forEach((u, j) => { A[j][j] += 1e-12; });
    const add = (a, b, g) => {
      const va = a in fest ? fest[a] : null;
      const vb = b === 'P' ? U_BATT : (b in fest ? fest[b] : null);
      if (va === null) { const j = pos[a]; A[j][j] += g; if (vb === null) A[j][pos[b]] -= g; else A[j][m] += g * vb; }
      if (b !== 'P' && vb === null) { const j = pos[b]; A[j][j] += g; if (va === null) A[j][pos[a]] -= g; else A[j][m] += g * va; }
    };
    kantenListe.forEach(([a, b, g]) => add(a, b, g));
    (quellen || []).forEach(([k, strom]) => { if (k in pos) A[pos[k]][m] += strom; });
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

  function baue(def) {
    const KNOTEN = def.knoten;
    const IDX = {}; KNOTEN.forEach((k, i) => { IDX[k] = i; });
    const MASSE = IDX.Masse, PLUS = IDX['B+'];
    const EL = def.elemente;
    const ORTE = {};
    EL.forEach(e => { ORTE[e.id] = { name: e.name, von: e.a, bis: e.b, typ: e.typ, schluss: e.schluss || null }; });
    const LAMPEN = EL.filter(e => e.typ === 'lampe').map(e => e.id);
    const SICH = EL.find(e => e.typ === 'sicherung');

    function widerstaende(z, kalt) {
      const f = z.fehler;
      return EL.map(e => {
        let r = e.r != null ? e.r : 0.01;
        if (e.typ === 'lampe') r = kalt ? R_LAMPE_KALT : R_LAMPE_HEISS;
        if (ist(f, e.id, 'unterbrechung')) return Infinity;
        if (e.typ === 'kabel' && ist(f, e.id, 'uebergang')) r = R_UEBERGANG_KABEL;
        if (e.typ === 'sicherung' && (!z.sicherungDrin || z.sicherungDurch)) return Infinity;
        if (e.typ === 'schalter') { if (!z.schalterZu) return Infinity; if (ist(f, e.id, 'uebergang')) r = R_UEBERGANG_SCHALTER; }
        if (e.typ === 'lampe' && !z.lampeDran) return Infinity;
        return r;
      });
    }

    function kanten(z, kalt, mitQuelle) {
      const k = [];
      widerstaende(z, kalt).forEach((w, i) => { if (w !== Infinity) k.push([IDX[EL[i].a], IDX[EL[i].b], 1 / w]); });
      const f = z.fehler;
      const o = f && ORTE[f.ort];
      if (o && o.schluss && f.art === 'masse') k.push([IDX[o.schluss], MASSE, 1 / R_SCHLUSS]);
      if (o && o.schluss && f.art === 'plus') k.push([IDX[o.schluss], mitQuelle ? 'P' : PLUS, 1 / R_SCHLUSS]);
      return k;
    }

    function potentiale(z) {
      if (!z.batterieAn) return KNOTEN.map(() => 0);
      const fest = {}; fest[PLUS] = U_BATT; fest[MASSE] = 0;
      return loese(KNOTEN.length, fest, kanten(z, false, true));
    }

    const voll = z => Object.assign({ sicherungDrin: true, sicherungDurch: false, lampeDran: true, schalterZu: true, batterieAn: true }, z);

    function aktualisiere(z0) {
      const z = voll(z0);
      const neu = Object.assign({}, z);
      let geradeDurchgebrannt = false;
      if (SICH && neu.batterieAn && neu.sicherungDrin && !neu.sicherungDurch && !ist(neu.fehler, SICH.id, 'unterbrechung')) {
        const v = potentiale(neu);
        const strom = (v[IDX[SICH.a]] - v[IDX[SICH.b]]) / (SICH.r || 0.01);
        if (Math.abs(strom) > SICHERUNG_A) { neu.sicherungDurch = true; geradeDurchgebrannt = true; }
      }
      return { zustand: neu, geradeDurchgebrannt };
    }

    function neueSicherung(z) {
      const neu = Object.assign({}, voll(z), { sicherungDrin: true, sicherungDurch: false });
      if (SICH && ist(neu.fehler, SICH.id, 'unterbrechung')) neu.fehler = null;
      return aktualisiere(neu);
    }

    function widerstand(z, a, b) {
      if (a === b) return 0;
      const fest = {}; fest[IDX[b]] = 0;
      const v = loese(KNOTEN.length, fest, kanten(voll(z), true, false), [[IDX[a], 1]]);
      return v[IDX[a]] > 1e7 ? Infinity : v[IDX[a]];
    }

    const NORMAL = (() => {
      const v = potentiale(voll({ fehler: null }));
      const n = {};
      LAMPEN.forEach(id => { const e = EL.find(x => x.id === id); n[id] = (v[IDX[e.a]] - v[IDX[e.b]]) ** 2; });
      return n;
    })();

    function helligkeiten(z0) {
      const z = voll(z0);
      const v = potentiale(z);
      const h = {};
      LAMPEN.forEach(id => {
        const e = EL.find(x => x.id === id);
        h[id] = (!z.lampeDran || ist(z.fehler, id, 'unterbrechung')) ? 0 : Math.round((v[IDX[e.a]] - v[IDX[e.b]]) ** 2 / NORMAL[id] * 100) / 100;
      });
      return h;
    }
    const helligkeit = z => helligkeiten(z)[LAMPEN[0]];

    function symptom(f) {
      const start = aktualisiere({ fehler: f }).zustand;
      const an = helligkeiten(start);
      const aus = helligkeiten(aktualisiere(Object.assign({}, start, { schalterZu: false })).zustand);
      if (LAMPEN.some(id => aus[id] > 0.1)) return LAMPEN.length > 1 ? 'Das Licht geht nicht mehr aus, auch wenn der Schalter aus ist.' : 'Die Lampe geht nicht mehr aus, auch wenn der Schalter aus ist.';
      const zustand = h => h < 0.05 ? 'aus' : h < 0.8 ? 'schwach' : h > 1.3 ? 'hell' : 'normal';
      if (LAMPEN.length === 1) {
        const s = zustand(an[LAMPEN[0]]);
        return { aus: 'Die Lampe leuchtet nicht.', schwach: 'Die Lampe leuchtet nur schwach.', hell: 'Die Lampe leuchtet heller als sonst.', normal: 'Mit der Lampe stimmt etwas nicht.' }[s];
      }
      const [a, b] = LAMPEN; const sa = zustand(an[a]), sb = zustand(an[b]);
      if (sa === sb) return { aus: 'Beide Lampen leuchten nicht.', schwach: 'Beide Lampen leuchten nur schwach.', hell: 'Beide Lampen leuchten zu hell.', normal: 'Mit den Lampen stimmt etwas nicht.' }[sa];
      const txt = (id, s) => ({ aus: 'Lampe ' + id + ' leuchtet nicht', schwach: 'Lampe ' + id + ' leuchtet nur schwach', hell: 'Lampe ' + id + ' leuchtet heller als sonst', normal: 'Lampe ' + id + ' leuchtet normal' }[s]);
      if (sa === 'hell' || sb === 'hell') return txt(a, sa) + ', ' + txt(b, sb).replace('Lampe ' + b + ' leuchtet nicht', b + ' gar nicht') + '.';
      return txt(a, sa) + ', ' + txt(b, sb) + '.';
    }

    function messe(z0) {
      const z = voll(z0);
      const leer = { anzeige: '', wert: null, ok: false, meldung: '' };
      if (z.modus === 'aus') return Object.assign(leer, { meldung: 'Das Messgerät ist aus. Dreh den Wahlschalter.' });
      if (!z.rot || !z.schwarz || !(z.rot in IDX) || !(z.schwarz in IDX)) return Object.assign(leer, { anzeige: '0,0', meldung: 'Halte beide Messspitzen an einen Messpunkt.' });
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
      if (!o) return '';
      const z = aktualisiere({ fehler: f }).zustand;
      const v = potentiale(z);
      const V = k => komma(Math.abs(v[IDX[k]]), 1).replace('-', '') + ' V';
      const fall = komma(Math.abs(v[IDX[o.von]] - v[IDX[o.bis]]), 1) + ' V';
      const mehr = LAMPEN.length > 1;
      if (o.typ === 'sicherung') return 'Die Sicherung war durchgebrannt, ohne dass ein Kurzschluss vorlag. Vor der Sicherung (' + o.von + ') lagen 12,6 V gegen Masse an, dahinter (' + o.bis + ') 0 V. Mit einer neuen Sicherung funktionierte alles.';
      if (o.typ === 'lampe') return 'Die Lampe ' + (mehr ? f.ort + ' ' : '') + 'war durchgebrannt. Über der Lampe (' + o.von + ' gegen ' + o.bis + ') lagen ' + fall + ' an, trotzdem leuchtete sie nicht. Stromlos gemessen zeigte sie OL.' +
        (mehr && def.reihe ? ' In der Reihenschaltung unterbricht sie den einzigen Stromweg, darum ist auch die andere Lampe aus.' : '') +
        (mehr && !def.reihe ? ' In der Parallelschaltung hat der andere Zweig seinen eigenen Stromweg und leuchtet weiter.' : '');
      if (o.typ === 'schalter' && f.art === 'unterbrechung') return 'Der Schalter schaltete nicht durch. Auch eingeschaltet lagen über dem Schalter (' + o.von + ' gegen ' + o.bis + ') 12,6 V an. Stromlos zeigte er OL.';
      if (o.typ === 'schalter') return 'Der Schalter hatte einen Übergangswiderstand. Über dem geschlossenen Schalter (' + o.von + ' gegen ' + o.bis + ') fielen ca. ' + fall + ' ab. Normal sind fast 0 V.';
      if (f.art === 'unterbrechung') return 'Die ' + o.name + ' war unterbrochen. ' + (o.bis === 'Masse'
        ? 'An ' + o.von + ' lagen ' + V(o.von) + ' gegen Masse an. Bei einer intakten Masseleitung sind es fast 0 V.'
        : 'Am Anfang der Leitung (' + o.von + ') lagen ' + V(o.von) + ' gegen Masse an, am Ende (' + o.bis + ') ' + V(o.bis) + '. Stromlos: ' + o.von + ' gegen ' + o.bis + ' zeigte OL.');
      if (f.art === 'uebergang') return 'Die ' + o.name + ' hatte einen Übergangswiderstand (z. B. Korrosion am Stecker). Bei eingeschaltetem Licht fielen über der Leitung (' + o.von + ' gegen ' + o.bis + ') ca. ' + fall + ' ab. Normal sind fast 0 V.' +
        (mehr && def.gemeinsam && def.gemeinsam.includes(f.ort) ? ' Weil beide Lampen über diese Leitung laufen, leuchteten beide schwach.' : '');
      if (f.art === 'masse') {
        if (!z.sicherungDurch) return 'Die ' + o.name + ' hatte einen Kurzschluss nach Masse (z. B. Isolierung durchgescheuert). Hinter der Schlussstelle bekam der Rest der Schaltung keine Spannung mehr. Die Lampe davor lag dadurch an der vollen Spannung und leuchtete heller. Die Sicherung hielt, weil die Lampe den Strom begrenzte.';
        return 'Die ' + o.name + ' hatte einen Kurzschluss nach Masse (z. B. Isolierung durchgescheuert). Darum ist die Sicherung durchgebrannt. Sie ist nur die Folge, nicht die Ursache: Eine neue Sicherung brennt sofort wieder durch.' +
          (mehr ? ' Obwohl nur eine Leitung betroffen ist, waren beide Lampen aus, weil sie an derselben Sicherung hängen.' : '') +
          ' So findest du ihn: Batterie abklemmen, ' + (mehr ? 'Lampen' : 'Lampe') + ' abstecken, Schalter aus. Dann zeigt die defekte Leitung gegen Masse 0 Ω statt OL.';
      }
      if (f.art === 'plus') return 'Die ' + o.name + ' hatte einen Kurzschluss nach Plus (Kontakt zu einer anderen Plusleitung). Das Licht bekam Plus am Schalter vorbei. Bei ausgeschaltetem Schalter lagen an ' + o.von + ' und ' + o.bis + ' trotzdem 12,6 V an.';
      return '';
    }

    function pruefeAntwort(f, ort, art) {
      const richtig = f.ort === ort && f.art === art;
      let rueckmeldung = richtig ? 'Richtig! Stelle und Fehlerart stimmen.' : 'Leider falsch.';
      if (!richtig && f.art === 'masse' && SICH && ort === SICH.id && aktualisiere({ fehler: f }).zustand.sicherungDurch) rueckmeldung = 'Nicht ganz: Die Sicherung ist zwar durchgebrannt, aber das ist nur die Folge. Die Ursache sitzt woanders.';
      else if (!richtig && f.ort === ort) rueckmeldung = 'Die Stelle stimmt, aber die Fehlerart nicht.';
      else if (!richtig && f.art === art) rueckmeldung = 'Die Fehlerart stimmt, aber die Stelle nicht.';
      return { richtig, rueckmeldung, erklaerung: erklaerung(f) };
    }

    function aufgabeErfuellt(id, z0) {
      const z = voll(z0);
      return !!def.aufgaben[id].pruef(z, messe(z));
    }

    return { name: def.name, KNOTEN, ORTE, ARTEN, LAMPEN, SZENARIEN: def.szenarien, AUFGABEN: def.aufgaben,
      potentiale, widerstand, helligkeit, helligkeiten, aktualisiere, neueSicherung, symptom, messe, pruefeAntwort, aufgabeErfuellt };
  }

  const paar = (z, a, b) => [z.rot, z.schwarz].sort().join() === [a, b].sort().join();
  const K = (id, a, b, name, schluss, r) => ({ id, a, b, typ: 'kabel', name, schluss, r: r || 0.01 });
  const S = (a, b) => ({ id: 'sicherung', a, b, typ: 'sicherung', name: 'Sicherung', r: 0.01 });
  const T = (a, b) => ({ id: 'schalter', a, b, typ: 'schalter', name: 'Schalter', r: 0.02 });
  const L = (id, a, b, name) => ({ id, a, b, typ: 'lampe', name });
  const sz = (liste) => liste.map(([ort, art]) => ({ ort, art }));

  const EINFACH = baue({
    name: 'Einfacher Stromkreis',
    knoten: ['B+', 'S1', 'S2', 'T1', 'T2', 'L1', 'L2', 'Masse'],
    elemente: [K('K1', 'B+', 'S1', 'Leitung Batterie–Sicherung'), S('S1', 'S2'), K('K2', 'S2', 'T1', 'Leitung Sicherung–Schalter', 'T1'), T('T1', 'T2'),
      K('K3', 'T2', 'L1', 'Leitung Schalter–Lampe', 'L1', 0.03), L('lampe', 'L1', 'L2', 'Lampe'), K('K4', 'L2', 'Masse', 'Masseleitung Lampe–Masse', null, 0.02)],
    szenarien: sz([['sicherung', 'unterbrechung'], ['schalter', 'unterbrechung'], ['schalter', 'uebergang'], ['lampe', 'unterbrechung'],
      ['K1', 'unterbrechung'], ['K2', 'unterbrechung'], ['K3', 'unterbrechung'], ['K4', 'unterbrechung'],
      ['K1', 'uebergang'], ['K2', 'uebergang'], ['K3', 'uebergang'], ['K4', 'uebergang'], ['K2', 'masse'], ['K3', 'masse'], ['K3', 'plus']]),
    aufgaben: {
      batterie: { text: 'Miss die Batteriespannung.', pruef: (z, r) => z.modus === 'V=' && z.batterieAn && z.rot === 'B+' && z.schwarz === 'Masse' && r.wert !== null && r.wert > 12 },
      'lampe-v': { text: 'Schalter an: Miss den Spannungsfall an der Lampe.', pruef: (z, r) => z.modus === 'V=' && z.batterieAn && z.schalterZu && paar(z, 'L1', 'L2') && r.wert > 11 },
      'lampe-r': { text: 'Miss den Widerstand der Lampe.', pruef: (z, r) => z.modus === 'Ω' && !z.batterieAn && paar(z, 'L1', 'L2') && r.wert !== null && r.wert < 2 }
    }
  });

  const PARALLEL = baue({
    name: 'Parallelschaltung',
    gemeinsam: ['K1', 'K2', 'K3', 'K8'],
    knoten: ['B+', 'S1', 'S2', 'T1', 'T2', 'X1', 'E1+', 'E1−', 'E2+', 'E2−', 'X2', 'Masse'],
    elemente: [K('K1', 'B+', 'S1', 'Leitung Batterie–Sicherung'), S('S1', 'S2'), K('K2', 'S2', 'T1', 'Leitung Sicherung–Schalter', 'T1'), T('T1', 'T2'),
      K('K3', 'T2', 'X1', 'gemeinsame Zuleitung Schalter–Verteiler', 'X1'),
      K('K4', 'X1', 'E1+', 'Zuleitung Lampe E1', 'E1+'), L('E1', 'E1+', 'E1−', 'Lampe E1'), K('K5', 'E1−', 'X2', 'Masseleitung Lampe E1'),
      K('K6', 'X1', 'E2+', 'Zuleitung Lampe E2', 'E2+'), L('E2', 'E2+', 'E2−', 'Lampe E2'), K('K7', 'E2−', 'X2', 'Masseleitung Lampe E2'),
      K('K8', 'X2', 'Masse', 'gemeinsame Masseleitung', null, 0.02)],
    szenarien: sz([['K4', 'unterbrechung'], ['K7', 'unterbrechung'], ['E1', 'unterbrechung'], ['E2', 'unterbrechung'],
      ['K8', 'uebergang'], ['K3', 'uebergang'], ['K5', 'uebergang'], ['K6', 'uebergang'],
      ['K4', 'masse'], ['K6', 'masse'], ['K3', 'unterbrechung'], ['K8', 'unterbrechung'],
      ['sicherung', 'unterbrechung'], ['schalter', 'uebergang'], ['K3', 'plus']]),
    aufgaben: {
      'e2-v': { text: 'Schalter an: Miss die Spannung an Lampe E2.', pruef: (z, r) => z.modus === 'V=' && z.batterieAn && z.schalterZu && paar(z, 'E2+', 'E2−') && r.wert > 11 },
      'e1-v': { text: 'Miss auch die Spannung an Lampe E1. Was fällt dir auf?', pruef: (z, r) => z.modus === 'V=' && z.batterieAn && z.schalterZu && paar(z, 'E1+', 'E1−') && r.wert > 11 },
      'ges-r': { text: 'Batterie ab: Miss den Gesamtwiderstand beider Lampen (X1 gegen X2).', pruef: (z, r) => z.modus === 'Ω' && !z.batterieAn && paar(z, 'X1', 'X2') && r.wert !== null && r.wert < 0.7 }
    }
  });

  const REIHE = baue({
    name: 'Reihenschaltung',
    reihe: true,
    knoten: ['B+', 'S1', 'S2', 'T1', 'T2', 'E1+', 'E1−', 'E2+', 'E2−', 'Masse'],
    elemente: [K('K1', 'B+', 'S1', 'Leitung Batterie–Sicherung'), S('S1', 'S2'), K('K2', 'S2', 'T1', 'Leitung Sicherung–Schalter', 'T1'), T('T1', 'T2'),
      K('K3', 'T2', 'E1+', 'Leitung Schalter–Lampe E1', 'E1+'), L('E1', 'E1+', 'E1−', 'Lampe E1'),
      K('K4', 'E1−', 'E2+', 'Verbindung Lampe E1–E2', 'E2+'), L('E2', 'E2+', 'E2−', 'Lampe E2'), K('K5', 'E2−', 'Masse', 'Masseleitung Lampe E2', null, 0.02)],
    szenarien: sz([['E1', 'unterbrechung'], ['E2', 'unterbrechung'], ['K4', 'unterbrechung'], ['K5', 'unterbrechung'],
      ['K3', 'uebergang'], ['K4', 'uebergang'], ['K5', 'uebergang'], ['K3', 'masse'], ['K4', 'masse'],
      ['sicherung', 'unterbrechung'], ['schalter', 'unterbrechung'], ['K3', 'plus']]),
    aufgaben: {
      'e1-v': { text: 'Schalter an: Miss die Spannung an Lampe E1.', pruef: (z, r) => z.modus === 'V=' && z.batterieAn && z.schalterZu && paar(z, 'E1+', 'E1−') && r.wert > 5 && r.wert < 7 },
      'ges-v': { text: 'Miss jetzt über beide Lampen zusammen (E1+ gegen E2−).', pruef: (z, r) => z.modus === 'V=' && z.batterieAn && z.schalterZu && paar(z, 'E1+', 'E2−') && r.wert > 11 },
      'ges-r': { text: 'Batterie ab: Miss den Widerstand beider Lampen zusammen (E1+ gegen E2−).', pruef: (z, r) => z.modus === 'Ω' && !z.batterieAn && paar(z, 'E1+', 'E2−') && r.wert !== null && r.wert > 1.2 && r.wert < 2.5 }
    }
  });

  const SCHALTUNGEN = { einfach: EINFACH, parallel: PARALLEL, reihe: REIHE };
  return Object.assign({ SCHALTUNGEN }, EINFACH);
})();
if (typeof module !== 'undefined') module.exports = Multimeter;
