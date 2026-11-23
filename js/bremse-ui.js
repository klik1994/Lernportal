(function () {
  const B = Bremse;
  const root = document.getElementById('bremse');
  const SKALA = 6;   // kN Vollausschlag
  const DAUER = { rollen: 900, bremsen: 2600 };
  let fall, achse = 'va', mess = {}, laeuft = null, anz = [0, 0], schlepp = [0, 0], eingaben = {}, befund = null, ergebnis = null, hinweis = '';

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const komma = (x, d) => x.toFixed(d).replace('.', ',');
  const btn = (attr, wert, text, aktiv, cls) => '<button data-' + attr + '="' + wert + '" class="' + (aktiv ? 'on ' : '') + (cls || '') + '">' + text + '</button>';
  const ACHSEN = [['va', 'Vorderachse'], ['ha', 'Hinterachse'], ['fba', 'Feststellbremse']];
  const ezJahr = () => 2014 + Math.floor(Math.random() * 11);
  let jahr;

  function neuesFahrzeug() {
    let neu; do { neu = B.FAELLE[Math.floor(Math.random() * B.FAELLE.length)]; } while (fall && neu.id === fall.id && B.FAELLE.length > 1);
    fall = neu; jahr = ezJahr(); achse = 'va'; mess = {}; anz = [0, 0]; schlepp = [0, 0]; eingaben = {}; befund = null; ergebnis = null; hinweis = '';
  }

  function raeder(a) {
    if (a === 'fba') return fall.fba.map((max, i) => ({ max, roll: fall.ha[i].roll, schw: 0.03 }));
    return fall[a];
  }

  function uhr(i, wert, max) {
    const W = 160, cx = 80, cy = 86, r = 64;
    const winkel = v => -210 + Math.min(1, v / SKALA) * 240;
    const pol = (w, rr) => [cx + rr * Math.cos(w * Math.PI / 180), cy + rr * Math.sin(w * Math.PI / 180)];
    let s = '<svg viewBox="0 0 ' + W + ' 150" role="img" aria-label="Anzeige ' + (i ? 'rechts' : 'links') + ': ' + komma(wert, 1) + ' kN">';
    s += '<rect width="' + W + '" height="150" rx="12" fill="#0a1220"/>';
    for (let k = 0; k <= SKALA * 2; k++) {
      const w = winkel(k / 2), [x1, y1] = pol(w, r), [x2, y2] = pol(w, k % 2 ? r - 6 : r - 11);
      s += '<line x1="' + x1.toFixed(1) + '" y1="' + y1.toFixed(1) + '" x2="' + x2.toFixed(1) + '" y2="' + y2.toFixed(1) + '" stroke="#8ea2bf" stroke-width="' + (k % 2 ? 1 : 2) + '"/>';
      if (!(k % 2)) { const [tx, ty] = pol(w, r - 22); s += '<text x="' + tx.toFixed(1) + '" y="' + (ty + 4).toFixed(1) + '" text-anchor="middle" font-size="10" fill="#cbd5e1">' + k / 2 + '</text>'; }
    }
    const [mx, my] = pol(winkel(max), r - 2);
    s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + mx.toFixed(1) + '" y2="' + my.toFixed(1) + '" stroke="#f05e4e" stroke-width="2" stroke-dasharray="3 3"/>';
    const [nx, ny] = pol(winkel(wert), r - 8);
    s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + nx.toFixed(1) + '" y2="' + ny.toFixed(1) + '" stroke="#f7b612" stroke-width="4" stroke-linecap="round"/><circle cx="' + cx + '" cy="' + cy + '" r="6" fill="#f7b612"/>';
    s += '<text x="' + cx + '" y="128" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="18" font-weight="800" fill="#ecf1f8">' + komma(wert, 2) + ' kN</text>';
    s += '<text x="' + cx + '" y="144" text-anchor="middle" font-size="10" fill="#94a4ba">max ' + komma(max, 2) + '</text>';
    return s + '</svg>';
  }

  function uhren() {
    return '<div class="bp-uhr">' + uhr(0, anz[0], schlepp[0]) + '<p>' + (achse === 'va' ? 'vorne links' : 'hinten links') + '</p></div>' +
      '<div class="bp-uhr">' + uhr(1, anz[1], schlepp[1]) + '<p>' + (achse === 'va' ? 'vorne rechts' : 'hinten rechts') + '</p></div>';
  }

  function messen() {
    if (laeuft) return;
    const rr = raeder(achse), start = performance.now();
    schlepp = [0, 0];
    laeuft = { text: 'Rollen laufen …' };
    render();
    const schritt = jetzt => {
      const dt = jetzt - start;
      const t = Math.max(0, (dt - DAUER.rollen) / DAUER.bremsen);
      const phase = dt / 700;
      anz = rr.map(r => B.kraft(r, t, phase));
      schlepp = schlepp.map((m, i) => Math.max(m, anz[i]));
      laeuft.text = t > 0 ? 'Bremspedal wird langsam bis zur Blockiergrenze getreten …' : 'Rollen laufen, Pedal noch nicht betätigt: Rollwiderstand';
      const box = document.getElementById('bp-uhren'), st = document.getElementById('bp-status');
      if (box) box.innerHTML = uhren();
      if (st) st.textContent = laeuft.text;
      if (t < 1.25) requestAnimationFrame(schritt);
      else {
        mess[achse] = rr.map((r, i) => ({ roll: r.roll, max: r.max, schw: r.schw }));
        laeuft = null;
        const naechste = ACHSEN.map(a => a[0]).find(a => !mess[a]);
        hinweis = naechste ? 'Gemessen. Weiter mit: ' + ACHSEN.find(a => a[0] === naechste)[1] + '.' : 'Alle Messungen fertig. Jetzt auswerten.';
        render();
      }
    };
    requestAnimationFrame(schritt);
  }

  function protokoll() {
    const zeile = (name, m, i, fba) => '<tr><td>' + name + '</td><td>' + (m ? (fba ? '–' : komma(m[i].roll, 2)) : '') + '</td><td>' + (m ? komma(m[i].max, 2) : '') + '</td><td>' + (m && !fba ? '± ' + komma(m[i].schw, 2) : m ? '–' : '') + '</td></tr>';
    return '<table class="bp-tab"><thead><tr><th>Rad</th><th>Roll&shy;widerst.</th><th>Brems&shy;kraft</th><th>Schwan&shy;kung</th></tr></thead><tbody>' +
      zeile('VL', mess.va, 0) + zeile('VR', mess.va, 1) + zeile('HL', mess.ha, 0) + zeile('HR', mess.ha, 1) + zeile('HL Feststellbr.', mess.fba, 0, true) + zeile('HR Feststellbr.', mess.fba, 1, true) +
      '</tbody></table><p class="muted" style="margin:6px 0 0">Alle Werte in kN.</p>';
  }

  const FELDER = [['diffVA', 'Bremskraftdifferenz Vorderachse in %'], ['diffHA', 'Bremskraftdifferenz Hinterachse in %'], ['zBetrieb', 'Abbremsung Betriebsbremse in %'], ['zFBA', 'Abbremsung Feststellbremse in %']];

  function auswertungKarte() {
    const a = B.auswertung(fall.id);
    let h = '<div class="card"><p class="lbl">Auswertung: rechne selbst (auf 1 % genau)</p><div class="bp-eingabe">' + FELDER.map(([id, t]) => {
      const cls = ergebnis ? (B.pruefeWert(a[id], eingaben[id] || '') ? 'ok' : 'falsch') : '';
      return '<label for="in-' + id + '">' + t + '</label><input id="in-' + id + '" data-feld="' + id + '" inputmode="decimal" class="' + cls + '" value="' + esc(eingaben[id] || '') + '"' + (ergebnis ? ' readonly' : '') + '>';
    }).join('') + '</div>';
    h += '<p class="lbl">Befund</p><div class="seg wrap">' + B.BEFUNDE.map(([id, t]) => btn('befund', id, t, befund === id)).join('') + '</div>';
    if (hinweis && !ergebnis && hinweis.startsWith('Wähle')) h += '<p class="meld warn">' + hinweis + '</p>';
    if (!ergebnis) h += '<button class="primary" style="width:100%" data-auswerten="1">Auswertung prüfen</button>';
    h += '</div>';
    if (ergebnis) {
      const g = a.gewichtskraft, kn = x => komma(x, 1);
      const f = fall;
      h += '<div class="meld ' + (ergebnis.richtig ? 'ok' : 'warn') + '"><b>' + (ergebnis.richtig ? 'Befund richtig!' : 'Befund leider falsch.') + '</b> Richtig ist: <b>' + esc(B.BEFUNDE.find(b => b[0] === fall.id)[1]) + '</b>. ' + esc(ergebnis.erklaerung) + '</div>';
      h += '<div class="card"><p class="lbl">Rechenweg</p><p style="margin:0 0 6px;font-size:14px">Gewichtskraft = ' + f.masse + ' kg × 9,81 m/s² = <b>' + komma(g, 2) + ' kN</b><br>' +
        'Differenz VA = (' + kn(Math.max(f.va[0].max, f.va[1].max)) + ' − ' + kn(Math.min(f.va[0].max, f.va[1].max)) + ') ÷ ' + kn(Math.max(f.va[0].max, f.va[1].max)) + ' × 100 = <b>' + komma(a.diffVA, 1) + ' %</b> (max. ' + B.MAX_DIFF + ' %)<br>' +
        'Differenz HA = (' + kn(Math.max(f.ha[0].max, f.ha[1].max)) + ' − ' + kn(Math.min(f.ha[0].max, f.ha[1].max)) + ') ÷ ' + kn(Math.max(f.ha[0].max, f.ha[1].max)) + ' × 100 = <b>' + komma(a.diffHA, 1) + ' %</b> (max. ' + B.MAX_DIFF + ' %)<br>' +
        'Abbremsung = Summe Bremskräfte ÷ Gewichtskraft × 100 = ' + komma(a.summe, 1) + ' ÷ ' + komma(g, 2) + ' × 100 = <b>' + komma(a.zBetrieb, 1) + ' %</b> (mind. ' + B.MIN_BETRIEB + ' %)<br>' +
        'Feststellbremse = ' + kn(f.fba[0] + f.fba[1]) + ' ÷ ' + komma(g, 2) + ' × 100 = <b>' + komma(a.zFBA, 1) + ' %</b> (mind. ' + B.MIN_FBA + ' %)</p></div>';
      h += '<button class="primary" style="width:100%" data-neu="1">Nächstes Fahrzeug</button>';
    }
    return h;
  }

  function render() {
    const alle = ACHSEN.every(([a]) => mess[a]);
    let h = '<div class="card"><p class="lbl">Fahrzeug</p><p style="margin:0 0 6px"><b>Pkw (Klasse M1), Erstzulassung ' + jahr + ', zulässige Gesamtmasse ' + fall.masse + ' kg</b></p>' +
      '<p class="muted" style="margin:0">Grenzwerte: Abbremsung Betriebsbremse mind. ' + B.MIN_BETRIEB + ' %, Feststellbremse mind. ' + B.MIN_FBA + ' %, Bremskraftdifferenz je Achse max. ' + B.MAX_DIFF + ' %. Vereinfacht rechnen wir mit der zulässigen Gesamtmasse; bei der HU bewertet der Prüfstand mit Bezugsbremskräften bzw. Hochrechnung.</p></div>';
    h += '<p class="lbl">Was wird geprüft?</p><div class="seg">' + ACHSEN.map(([id, t]) => btn('achse', id, t + (mess[id] ? ' ✓' : ''), achse === id)).join('') + '</div>';
    h += '<div class="card"><div class="bp-uhren" id="bp-uhren">' + uhren() + '</div>' +
      '<p id="bp-status" class="muted" style="margin:8px 0;min-height:20px">' + esc(laeuft ? laeuft.text : hinweis && !hinweis.startsWith('Wähle') ? hinweis : (achse === 'fba' ? 'Hinterachse auf den Rollen, Feststellbremse langsam anziehen.' : 'Achse auf die Rollen fahren und Messung starten.')) + '</p>' +
      '<button class="primary" style="width:100%" data-messen="1"' + (laeuft ? ' disabled' : '') + '>' + (mess[achse] ? 'Nochmal messen' : 'Messung starten') + '</button></div>';
    h += '<div class="card"><p class="lbl">Prüfprotokoll</p>' + protokoll() + '</div>';
    if (alle) h += auswertungKarte();
    root.innerHTML = h;
  }

  root.addEventListener('input', e => { if (e.target.dataset.feld) eingaben[e.target.dataset.feld] = e.target.value; });
  root.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    const d = b.dataset;
    if (d.achse) { if (laeuft) return; achse = d.achse; anz = [0, 0]; schlepp = mess[achse] ? mess[achse].map(m => m.max) : [0, 0]; hinweis = ''; }
    else if (d.messen) return messen();
    else if (d.befund) { befund = d.befund; if (hinweis.startsWith('Wähle')) hinweis = ''; }
    else if (d.auswerten) {
      if (!befund) hinweis = 'Wähle zuerst einen Befund aus.';
      else { ergebnis = B.pruefeBefund(fall.id, befund); hinweis = ''; }
    }
    else if (d.neu) neuesFahrzeug();
    else return;
    render();
  });

  neuesFahrzeug();
  render();
})();
