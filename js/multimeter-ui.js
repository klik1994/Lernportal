(function () {
  const M = Multimeter;
  const root = document.getElementById('mm');
  const POS = { 'B+': [40, 40], S1: [95, 40], S2: [150, 40], T1: [190, 40], T2: [240, 40], L1: [300, 75], L2: [300, 150], Masse: [40, 190] };
  const AUFG = Object.keys(M.AUFGABEN);
  const START = { fehler: null, modus: 'aus', buchseRot: 'VΩ', rot: null, schwarz: null, schalterZu: true, batterieAn: true, sicherungDrin: true, sicherungDurch: false, lampeDran: true };
  let z = Object.assign({}, START);
  let modus = 'aufgaben', aufgabe = 0, erledigt = {}, spitze = 'rot', messungen = 0, antwortPhase = false, ergebnis = null;
  let szenario = null, wahlOrt = null, wahlArt = null, antwortFehler = '', ereignis = '';

  function setze(teil) {
    const r = M.aktualisiere(Object.assign({}, z, teil));
    z = r.zustand;
    if (r.geradeDurchgebrannt) ereignis = 'Peng! Die Sicherung ist durchgebrannt.';
  }

  function neuerFehler() {
    const f = M.SZENARIEN[Math.floor(Math.random() * M.SZENARIEN.length)];
    szenario = f;
    z = Object.assign({}, START, { fehler: f, modus: z.modus, buchseRot: z.buchseRot });
    setze({});
    ereignis = '';
    messungen = 0; antwortPhase = false; ergebnis = null; wahlOrt = null; wahlArt = null; antwortFehler = '';
  }

  function svg() {
    const hell = M.helligkeit(z);
    const sicherungOffen = !z.sicherungDrin || z.sicherungDurch;
    let s = '<svg viewBox="0 0 340 215" role="img" aria-label="Stromkreis mit Batterie, Sicherung, Schalter und Lampe">';
    s += '<path d="M40 40 H95 M150 40 H190 M240 40 H300 V75 M300 150 V190 H40 V118 M40 40 V95" fill="none" stroke="#555" stroke-width="2.5"/>';
    if (!z.batterieAn) s += '<rect x="30" y="52" width="20" height="16" fill="#fff"/><text x="48" y="84" font-size="11" fill="#c62828">abgeklemmt</text>';
    s += '<line x1="22" y1="98" x2="58" y2="98" stroke="#333" stroke-width="3"/><line x1="30" y1="112" x2="50" y2="112" stroke="#333" stroke-width="6"/>';
    s += '<text x="64" y="102" font-size="12" fill="#333">+</text><text x="64" y="118" font-size="12" fill="#333">12 V</text>';
    if (z.sicherungDrin) {
      s += '<rect x="102" y="31" width="42" height="18" rx="3" fill="#fff" stroke="#333" stroke-width="2"/>';
      s += z.sicherungDurch ? '<path d="M110 40 L120 34 M126 46 L136 40" stroke="#c62828" stroke-width="2"/>' : '<line x1="106" y1="40" x2="140" y2="40" stroke="#333" stroke-width="1.5"/>';
    } else s += '<rect x="102" y="31" width="42" height="18" rx="3" fill="#fff" stroke="#999" stroke-width="1.5" stroke-dasharray="3 3"/>';
    s += '<text x="123" y="64" font-size="11" text-anchor="middle" fill="' + (sicherungOffen && z.sicherungDrin ? '#c62828' : '#333') + '">' + (z.sicherungDrin ? 'Sicherung' : 'gezogen') + '</text>';
    s += z.schalterZu ? '<line x1="190" y1="40" x2="240" y2="40" stroke="#333" stroke-width="3"/>' : '<line x1="190" y1="40" x2="232" y2="18" stroke="#333" stroke-width="3"/>';
    s += '<text x="215" y="62" font-size="11" text-anchor="middle" fill="#333">Schalter</text>';
    if (z.lampeDran) {
      s += '<circle cx="300" cy="112" r="20" fill="rgba(255,200,0,' + (0.1 + hell * 0.85) + ')" stroke="#333" stroke-width="2"/>';
      s += '<path d="M286 98 L314 126 M314 98 L286 126" stroke="#333" stroke-width="2"/>';
    } else s += '<circle cx="300" cy="112" r="20" fill="#fff" stroke="#999" stroke-width="1.5" stroke-dasharray="3 3"/>';
    s += '<text x="268" y="116" font-size="11" text-anchor="end" fill="#333">' + (z.lampeDran ? 'Lampe' : 'abgesteckt') + '</text>';
    s += '<path d="M28 200 H52 M32 205 H48 M36 210 H44" stroke="#333" stroke-width="2"/>';
    Object.keys(POS).forEach(k => {
      const [x, y] = POS[k];
      const farbe = z.rot === k ? '#c62828' : z.schwarz === k ? '#111' : '#fff';
      s += '<g class="pt" data-punkt="' + k + '"><circle cx="' + x + '" cy="' + y + '" r="18" fill="transparent"/>' +
        '<circle cx="' + x + '" cy="' + y + '" r="7" fill="' + farbe + '" stroke="#1a5fb4" stroke-width="2"/>' +
        '<text x="' + (x + (k === 'Masse' ? 14 : 0)) + '" y="' + (k === 'Masse' ? y + 20 : (y > 60 ? y + 4 : y - 12)) + '" dx="' + (y > 60 && k !== 'Masse' ? 12 : 0) + '" font-size="11" text-anchor="' + (y > 60 || k === 'Masse' ? 'start' : 'middle') + '" fill="#1a5fb4">' + k + '</text></g>';
    });
    return s + '</svg>';
  }

  function btn(attr, wert, text, aktiv, cls) {
    return '<button data-' + attr + '="' + wert + '" class="' + (aktiv ? 'on ' : '') + (cls || '') + '">' + text + '</button>';
  }

  function render() {
    const r = M.messe(z);
    let h = '<div class="seg">' + btn('modus', 'aufgaben', 'Messaufgaben', modus === 'aufgaben') + btn('modus', 'fehler', 'Fehlersuche', modus === 'fehler') + '</div>';
    if (modus === 'aufgaben') {
      const id = AUFG[aufgabe];
      h += '<div class="card"><p class="lbl">Aufgabe ' + (aufgabe + 1) + ' von ' + AUFG.length + '</p><p style="margin:0"><b>' + M.AUFGABEN[id].text + '</b></p>' +
        (erledigt[id] ? '<div class="meld ok" style="margin:8px 0 0">Richtig gemessen.' + (aufgabe + 1 < AUFG.length ? ' <button data-naechste="1">Nächste Aufgabe</button>' : ' Alle Aufgaben geschafft. Probier jetzt die Fehlersuche.') + '</div>' : '') + '</div>';
    } else {
      h += '<div class="card"><p class="lbl">Kunde sagt:</p><p style="margin:0 0 6px"><b>' + M.symptom(szenario) + '</b></p><p class="muted" style="margin:0">Finde den Fehler durch Messen. Messungen: ' + messungen + '</p></div>';
    }
    h += svg();
    if (ereignis) h += '<div class="meld warn">' + ereignis + '</div>';
    h += '<div class="seg">' + btn('schalter', '1', z.schalterZu ? 'Schalter: an' : 'Schalter: aus', z.schalterZu) + btn('batterie', '1', z.batterieAn ? 'Batterie: dran' : 'Batterie: ab', !z.batterieAn) + '</div>';
    h += '<div class="seg">' + btn('ziehen', '1', z.sicherungDrin ? 'Sicherung ziehen' : 'Sicherung einsetzen', !z.sicherungDrin) + btn('neusich', '1', 'Neue Sicherung', false) + btn('lampe', '1', z.lampeDran ? 'Lampe abstecken' : 'Lampe anstecken', !z.lampeDran) + '</div>';
    h += '<div class="card"><div class="display" aria-live="polite">' + r.anzeige + '</div>';
    h += '<p class="lbl">Wahlschalter</p><div class="seg">' + [['aus', 'AUS'], ['V=', 'V⎓'], ['V~', 'V~'], ['Ω', 'Ω'], ['A=', 'A⎓']].map(([w, t]) => btn('dreh', w, t, z.modus === w)).join('') + '</div>';
    h += '<p class="lbl">Rote Leitung steckt in Buchse (Schwarz immer in COM)</p><div class="seg">' + ['VΩ', 'mA', '10A'].map(w => btn('buchse', w, w, z.buchseRot === w)).join('') + '</div>';
    h += '<p class="lbl">Erst Messspitze wählen, dann Messpunkt im Bild antippen</p><div class="seg">' +
      btn('spitze', 'rot', 'Rot: ' + (z.rot || '–'), spitze === 'rot', 'probe-rot') + btn('spitze', 'schwarz', 'Schwarz: ' + (z.schwarz || '–'), spitze === 'schwarz', 'probe-schwarz') + '</div></div>';
    if (r.meldung) h += '<div class="meld ' + (r.ok ? 'info' : 'warn') + '">' + r.meldung + '</div>';
    if (modus === 'fehler') {
      if (ergebnis) {
        const zeigen = ergebnis.richtig || ergebnis.loesung;
        h += '<div class="meld ' + (ergebnis.richtig ? 'ok' : 'warn') + '"><b>' + ergebnis.rueckmeldung + (ergebnis.richtig ? ' Gefunden mit ' + messungen + ' Messungen.' : '') + '</b>' + (zeigen ? '<br>' + ergebnis.erklaerung : '') + '</div>';
        if (zeigen) h += '<button class="primary" style="width:100%" data-neu="1">Neuer Fehler</button>';
        else h += '<div class="seg"><button class="primary" data-weiter="1">Weiter suchen</button><button data-loesung="1">Lösung zeigen</button></div>';
      } else if (antwortPhase) {
        h += '<div class="card"><p class="lbl">1. Wo sitzt der Fehler?</p><div class="seg">' + Object.keys(M.ORTE).map(o => btn('ort', o, M.ORTE[o].name, wahlOrt === o)).join('') + '</div>';
        h += '<p class="lbl">2. Was für ein Fehler ist es?</p><div class="seg">' + Object.keys(M.ARTEN).map(a => btn('art', a, M.ARTEN[a], wahlArt === a)).join('') + '</div>';
        if (antwortFehler) h += '<p class="meld warn">' + antwortFehler + '</p>';
        h += '<button class="primary" style="width:100%" data-antwort="1">Antwort prüfen</button></div>';
      } else {
        h += '<button class="primary" style="width:100%" data-gefunden="1">Fehler gefunden</button>';
      }
    }
    root.innerHTML = h;
  }

  function nachMessung() {
    if (modus === 'aufgaben') { const id = AUFG[aufgabe]; if (M.aufgabeErfuellt(id, z)) erledigt[id] = true; }
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
    const b = e.target.closest('button');
    if (!b) return;
    const d = b.dataset;
    ereignis = '';
    if (d.modus) {
      modus = d.modus;
      if (modus === 'fehler') neuerFehler(); else z = Object.assign({}, START, { modus: z.modus, buchseRot: z.buchseRot });
    } else if (d.dreh) { z.modus = d.dreh; nachMessung(); }
    else if (d.buchse) { z.buchseRot = d.buchse; nachMessung(); }
    else if (d.spitze) spitze = d.spitze;
    else if (d.schalter) { setze({ schalterZu: !z.schalterZu }); nachMessung(); }
    else if (d.batterie) { setze({ batterieAn: !z.batterieAn }); nachMessung(); }
    else if (d.ziehen) setze({ sicherungDrin: !z.sicherungDrin });
    else if (d.neusich) {
      const r = M.neueSicherung(z);
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
      else ergebnis = M.pruefeAntwort(szenario, wahlOrt, wahlArt);
    }
    else if (d.weiter) { ergebnis = null; antwortPhase = false; wahlOrt = null; wahlArt = null; }
    else if (d.loesung) ergebnis.loesung = true;
    else if (d.neu) neuerFehler();
    render();
  });

  render();
})();
