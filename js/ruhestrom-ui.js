(function () {
  const R = Ruhestrom;
  const root = document.getElementById('ruhestrom');
  let st, methode = 'ziehen', mv = null, antwortPhase = false, wahl = null, ergebnis = null, antwortFehler = '';

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const komma = (x, d) => x.toFixed(d).replace('.', ',');
  const btn = (attr, wert, text, aktiv, cls) => '<button data-' + attr + '="' + wert + '" class="' + (aktiv ? 'on ' : '') + (cls || '') + '">' + text + '</button>';

  let stapel = [], letzter = null;
  function naechsterFall() {
    if (!stapel.length) {
      stapel = R.FEHLER.map(f => f.id);
      for (let i = stapel.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [stapel[i], stapel[j]] = [stapel[j], stapel[i]]; }
      if (stapel[0] === letzter && stapel.length > 1) stapel.push(stapel.shift());
    }
    letzter = stapel.shift();
    return letzter;
  }
  function neuerAuftrag(id) {
    st = R.neu(id || naechsterFall());
    methode = 'ziehen'; mv = null; antwortPhase = false; wahl = null; ergebnis = null; antwortFehler = '';
  }

  function schaltbild() {
    const a = st.anschluss, kaputt = !!st.geraetDefekt;
    let s = '<svg class="rs-bild" viewBox="0 0 320 150" role="img" aria-label="Batterie mit Multimeter">';
    s += '<rect width="320" height="150" rx="12" fill="#0a1220"/>';
    s += '<rect x="24" y="52" width="110" height="70" rx="8" fill="#1d2b44" stroke="#8ea2bf" stroke-width="2"/>';
    s += '<text x="79" y="94" text-anchor="middle" font-size="14" font-weight="800" fill="#cbd5e1">12 V</text>';
    s += '<rect x="38" y="40" width="20" height="12" rx="2" fill="#f05e4e"/><text x="48" y="34" text-anchor="middle" font-size="15" font-weight="800" fill="#f05e4e">+</text>';
    s += '<rect x="100" y="40" width="20" height="12" rx="2" fill="#94a4ba"/><text x="110" y="34" text-anchor="middle" font-size="16" font-weight="800" fill="#94a4ba">−</text>';
    s += '<path d="M48 40 V20 H300" stroke="#f05e4e" stroke-width="3" fill="none"/><text x="300" y="14" text-anchor="end" font-size="11" fill="#9fb0c8">zum Bordnetz</text>';
    s += '<path d="M250 140 H300" stroke="#94a4ba" stroke-width="3"/><text x="300" y="134" text-anchor="end" font-size="11" fill="#9fb0c8">Karosserie</text>';
    const mm = (x, y) => '<rect x="' + (x - 26) + '" y="' + (y - 18) + '" width="52" height="36" rx="7" fill="#f7b612"/><rect x="' + (x - 20) + '" y="' + (y - 12) + '" width="40" height="14" rx="2" fill="#d7e3cf"/><text x="' + x + '" y="' + (y + 14) + '" text-anchor="middle" font-size="9" font-weight="800" fill="#0e192b">' + (kaputt ? 'defekt' : 'A') + '</text>';
    if (a === 'reihe') {
      s += '<path d="M110 40 V30 H190 V68" stroke="#94a4ba" stroke-width="3" fill="none"/><path d="M190 104 V140 H250" stroke="#94a4ba" stroke-width="3" fill="none"/>';
      s += mm(190, 86) + '<text x="230" y="90" font-size="11" fill="#9fb0c8">in Reihe</text>';
    } else {
      s += '<path d="M110 40 V30 H170 M200 30 H230 V140 H250" stroke="#94a4ba" stroke-width="3" fill="none"/>';
      s += '<text x="185" y="34" text-anchor="middle" font-size="10" fill="#9fb0c8">Massekabel</text>';
      if (a === 'parallel') s += '<path d="M48 52 V136 H79 M110 52 V136 H79" stroke="#f7b612" stroke-width="2" stroke-dasharray="4 3" fill="none"/>' + mm(79, 136 - 6) ;
    }
    return s + '</svg>';
  }

  function sicherungen() {
    return '<div class="sk">' + R.SICHERUNGEN.map(s => {
      const raus = st.gezogen.includes(s.id);
      return '<button class="sk-s' + (raus ? ' raus' : '') + (mv && mv.id === s.id ? ' on' : '') + '" data-sich="' + s.id + '">' +
        '<span class="blatt" style="background:' + (raus ? 'transparent' : R.FARBE[s.a]) + '">' + (raus ? '' : String(s.a).replace('.', ',')) + '</span>' +
        '<b>' + s.id + '</b><small>' + esc(s.name) + (raus ? ' · gezogen' : '') + '</small></button>';
    }).join('') + '</div>';
  }

  function render() {
    const f = R.info(st.fehler), anz = R.anzeige(st);
    let h = '<div class="card"><p class="lbl">Auftrag</p><p style="margin:0 0 6px"><b>' + esc(f.kunde) + '</b></p><p class="muted" style="margin:0">Vorgabe Hersteller: Ruhestrom höchstens ' + R.GRENZE + ' mA, gemessen nach der Busruhe.</p></div>';

    h += '<div class="card"><p class="lbl">1. Multimeter anschließen (Strommessung)</p>' + schaltbild() +
      '<div class="seg wrap" style="margin-top:10px">' + btn('anschluss', 'parallel', 'Parallel an die Batterie (+ und −)', st.anschluss === 'parallel') + btn('anschluss', 'reihe', 'In Reihe: zwischen Minuspol und Massekabel', st.anschluss === 'reihe') + '</div>' +
      '<p class="lbl">Buchse am Messgerät</p><div class="seg">' + btn('buchse', '10A', '10-A-Buchse', st.buchse === '10A') + btn('buchse', 'mA', 'mA-Buchse (max. 400 mA)', st.buchse === 'mA') + '</div>' +
      '<div class="display">' + anz.text + '</div>';
    if (st.geraetDefekt === 'kurzschluss') h += '<div class="meld warn"><b>Kurzschluss!</b> Im Strommessbereich hat das Multimeter fast keinen Widerstand. Parallel an der Batterie ist das ein Kurzschluss, die Sicherung im Messgerät ist durchgebrannt. Strom misst man immer <b>in Reihe</b>.</div>';
    if (st.geraetDefekt === 'ueberlast') h += '<div class="meld warn"><b>Die mA-Sicherung im Messgerät ist durchgebrannt.</b> Solange die Steuergeräte wach sind, fließt über 1 A. Starte mit der 10-A-Buchse und stecke erst nach der Busruhe auf mA um.</div>';
    if (st.geraetDefekt) h += '<button style="width:100%;margin-bottom:6px" data-reparieren="1">Sicherung im Messgerät tauschen und neu anschließen</button>';
    else if (st.anschluss === 'reihe' && st.buchse === '10A' && R.strom(st) < R.MA_MAX) h += '<div class="meld info">Die 10-A-Buchse zeigt nur auf 10 mA genau. Für den genauen Wert jetzt auf die mA-Buchse umstecken.</div>';
    h += '</div>';

    h += '<div class="card"><p class="lbl">2. Fahrzeug einschlafen lassen</p><div class="seg">' + btn('haube', '1', st.haube ? 'Haubenkontakt überbrückt ✓' : 'Motorhaube offen: Haubenkontakt überbrücken', st.haube) + '</div>' +
      '<p style="margin:4px 0 8px">Zeit seit Zündung aus und Abschließen: <b>' + st.minuten + ' min</b></p>' +
      '<div class="seg">' + btn('warte', '5', '5 min warten') + btn('warte', '15', '15 min warten') + '</div>' +
      '<p class="muted" style="margin:0">Die Steuergeräte brauchen bei diesem Fahrzeug etwa ' + R.SCHLAF_MIN + ' Minuten bis zur Busruhe. Öffnen der Haube und Einstecken einer Sicherung weckt sie wieder.</p></div>';

    h += '<div class="card"><p class="lbl">3. Sicherungskasten</p><div class="seg">' + btn('methode', 'ziehen', 'Sicherung ziehen / stecken', methode === 'ziehen') + btn('methode', 'mv', 'Spannungsfall messen (mV)', methode === 'mv') + '</div>' + sicherungen();
    if (methode === 'mv') {
      if (mv) {
        const s = R.sicherung(mv.id);
        h += '<div class="mini-display"><span>Über ' + s.id + ' (' + String(s.a).replace('.', ',') + ' A, ca. ' + komma(R.R_MOHM[s.a], 1) + ' mΩ)</span><b>' + komma(R.spannungsfall(st, mv.id), 1) + ' mV</b></div>' +
          '<p class="muted" style="margin:6px 0 0">Strom ausrechnen: I = U ÷ R. Beispiel: 3,0 mV ÷ 15 mΩ = 0,2 A = 200 mA.</p>';
      } else h += '<p class="muted" style="margin:6px 0 0">Tippe eine Sicherung an: Du misst mit dem Voltmeter (mV) an den beiden Prüfpunkten oben auf der Sicherung. Die Sicherung bleibt stecken, nichts wird geweckt.</p>';
    } else h += '<p class="muted" style="margin:6px 0 0">Tippe eine Sicherung an, um sie zu ziehen. Nochmal tippen steckt sie wieder ein.</p>';
    h += '</div>';

    if (ergebnis) {
      const zeigen = ergebnis.richtig || ergebnis.zeigen;
      const ziel = ergebnis.loesung === 'kein' ? 'Kein Fehler' : ergebnis.loesung + ' ' + R.sicherung(ergebnis.loesung).name;
      h += '<div class="meld ' + (ergebnis.richtig ? 'ok' : 'warn') + '"><b>' + (ergebnis.richtig ? 'Richtig!' : 'Leider falsch.') + '</b> Wartezeit insgesamt ' + st.wartezeit + ' min, Steuergeräte ' + st.geweckt + '× neu geweckt.' +
        (zeigen ? '<br><b>' + esc(ziel) + ':</b> ' + esc(ergebnis.erklaerung) : '') + '</div>';
      h += zeigen ? '<button class="primary" style="width:100%" data-neu="1">Neuer Auftrag</button>' : '<div class="seg"><button class="primary" data-weiter="1">Weiter suchen</button><button data-loesung="1">Lösung zeigen</button></div>';
    } else if (antwortPhase) {
      h += '<div class="card"><p class="lbl">Was ist dein Ergebnis?</p><div class="seg wrap">' + btn('wahl', 'kein', 'Kein Fehler: Ruhestrom in Ordnung', wahl === 'kein') +
        R.SICHERUNGEN.map(s => btn('wahl', s.id, s.id + ' ' + esc(s.name), wahl === s.id)).join('') + '</div>';
      if (antwortFehler) h += '<p class="meld warn">' + antwortFehler + '</p>';
      h += '<button class="primary" style="width:100%" data-antwort="1">Antwort prüfen</button></div>';
    } else h += '<button class="primary" style="width:100%" data-gefunden="1">Ergebnis abgeben</button>';
    root.innerHTML = h;
  }

  root.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    const d = b.dataset;
    if (d.anschluss) R.anschliessen(st, d.anschluss);
    else if (d.buchse) R.anschliessen(st, undefined, d.buchse);
    else if (d.reparieren) R.geraetReparieren(st);
    else if (d.haube) R.setzeHaube(st, !st.haube);
    else if (d.warte) R.warte(st, +d.warte);
    else if (d.methode) { methode = d.methode; mv = null; }
    else if (d.sich) {
      if (methode === 'mv') mv = { id: d.sich };
      else R.ziehe(st, d.sich);
    }
    else if (d.gefunden) antwortPhase = true;
    else if (d.wahl) { wahl = d.wahl; antwortFehler = ''; }
    else if (d.antwort) { if (!wahl) antwortFehler = 'Wähle zuerst ein Ergebnis aus.'; else ergebnis = R.pruefe(st, wahl); }
    else if (d.weiter) { ergebnis = null; antwortPhase = false; wahl = null; }
    else if (d.loesung) ergebnis.zeigen = true;
    else if (d.neu) neuerAuftrag();
    else return;
    render();
  });

  neuerAuftrag();
  render();
})();
