(function () {
  const H = Hochvolt;
  const root = document.getElementById('hochvolt');
  let teil = 'ablauf', liste = [], karten = [], pruefung = null;
  let m = null, anzeige = null, urteil = null, ergebnis = null, urteilFehler = '';

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const btn = (attr, wert, text, aktiv, cls) => '<button data-' + attr + '="' + wert + '" class="' + (aktiv ? 'on ' : '') + (cls || '') + '">' + text + '</button>';
  const mischen = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const REGELN = ['Freischalten', 'Gegen Wiedereinschalten sichern', 'Spannungsfreiheit feststellen', 'Erden und kurzschließen (am Fahrzeug meist nicht anzuwenden)', 'Benachbarte, unter Spannung stehende Teile abdecken'];

  function neuerAblauf() { liste = []; karten = mischen(H.SCHRITTE.map(s => s.id)); pruefung = null; }
  function neueMessung() {
    m = H.neueMessung(H.SZENARIEN[Math.floor(Math.random() * H.SZENARIEN.length)].id);
    anzeige = null; urteil = null; ergebnis = null; urteilFehler = '';
  }

  function renderAblauf() {
    let h = '<div class="card"><p class="lbl">Aufgabe</p><p style="margin:0">Ein Elektroauto kommt zum Tausch des Klimakompressors (HV-Bauteil). Bringe die Schritte zum <b>Herstellen der Spannungsfreiheit</b> in die richtige Reihenfolge. Achtung: Es sind auch falsche Schritte dabei.</p></div>';
    h += '<div class="card"><p class="lbl">Dein Ablauf</p>';
    if (!liste.length) h += '<p class="muted" style="margin:0">Noch leer. Tippe unten die Schritte in der richtigen Reihenfolge an.</p>';
    else h += '<ol class="hv-liste">' + liste.map((id, i) => {
      const cls = pruefung ? (pruefung.ok ? 'richtig' : (pruefung.fehler.some(f => f.id === id && !f.fehlt) || pruefung.falschePos.includes(id) ? 'falsch' : '')) : '';
      return '<li class="' + cls + '"><span>' + esc(H.schritt(id).text) + '</span>' +
        (i > 0 ? '<button data-hoch="' + i + '" aria-label="nach oben">↑</button>' : '') + '<button data-weg="' + i + '" aria-label="entfernen">✕</button></li>';
    }).join('') + '</ol>';
    h += '</div>';
    const rest = karten.filter(id => !liste.includes(id));
    if (rest.length) h += '<div class="card"><p class="lbl">Schritte zur Auswahl</p><div class="hv-karten">' + rest.map(id => btn('nimm', id, esc(H.schritt(id).text))).join('') + '</div></div>';
    if (pruefung && pruefung.ok) {
      h += '<div class="meld ok"><b>Alles richtig!</b> So sind die Sicherheitsregeln umgesetzt:<br>' + [1, 2, 3].map(r => '<b>' + r + '. ' + REGELN[r - 1] + ':</b> ' + H.SCHRITTE.filter(s => s.regel === r).map(s => esc(s.text)).join('; ')).join('<br>') +
        '<br><b>Nach der Arbeit</b> werden die Maßnahmen in umgekehrter Reihenfolge wieder aufgehoben.</div>';
      h += '<div class="seg"><button class="primary" data-teil="messen">Weiter zum Freimessen</button><button data-nochmal="1">Nochmal</button></div>';
    } else {
      if (pruefung) h += '<div class="meld warn"><b>Noch nicht richtig:</b><ul style="margin:6px 0 0;padding-left:18px">' + pruefung.fehler.map(f => '<li>' + esc(f.text) + '</li>').join('') + '</ul></div>';
      h += '<div class="seg"><button class="primary" data-pruefen="1">Ablauf prüfen</button><button data-nochmal="1">Neu anfangen</button></div>';
    }
    return h;
  }

  function pruefer() {
    const txt = anzeige === null ? '' : anzeige.v === null ? '' : anzeige.v + ' V';
    const warn = anzeige && anzeige.v > 60;
    let s = '<svg viewBox="0 0 320 170" role="img" aria-label="Zweipoliger Spannungsprüfer am HV-Anschluss">';
    s += '<rect width="320" height="170" rx="12" fill="#0a1220"/>';
    s += '<rect x="20" y="40" width="120" height="90" rx="10" fill="#2a3a55" stroke="#8ea2bf" stroke-width="2"/><text x="80" y="62" text-anchor="middle" font-size="11" font-weight="700" fill="#cbd5e1">Leistungselektronik</text>';
    s += '<path d="M60 130 V160 M100 130 V160" stroke="#ff8a1f" stroke-width="7" stroke-linecap="round"/>';
    s += '<circle cx="55" cy="96" r="11" fill="#f05e4e"/><text x="55" y="100" text-anchor="middle" font-size="11" font-weight="800" fill="#0e192b">HV+</text>';
    s += '<circle cx="105" cy="96" r="11" fill="#94a4ba"/><text x="105" y="100" text-anchor="middle" font-size="11" font-weight="800" fill="#0e192b">HV−</text>';
    s += '<text x="20" y="28" font-size="11" fill="#9fb0c8">Karosserie = Masse ⏚</text>';
    s += '<rect x="190" y="18" width="96" height="140" rx="16" fill="#f7b612"/><rect x="202" y="32" width="72" height="34" rx="4" fill="' + (warn ? '#ffd2cc' : '#d7e3cf') + '"/>';
    s += '<text x="238" y="56" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="18" font-weight="800" fill="#1b2a12">' + txt + '</text>';
    s += '<circle cx="216" cy="84" r="6" fill="' + (warn ? '#f05e4e' : '#5a4310') + '"/><text x="228" y="88" font-size="10" font-weight="700" fill="#0e192b">&gt; 50 V</text>';
    s += '<text x="238" y="120" text-anchor="middle" font-size="10" font-weight="800" fill="#0e192b">CAT III 1000 V</text><text x="238" y="136" text-anchor="middle" font-size="9" font-weight="700" fill="#0e192b">zweipolig</text>';
    return s + '</svg>';
  }

  function renderMessen() {
    let h = '<div class="card"><p class="lbl">Freimessen</p><p style="margin:0">Wartungsstecker ist gezogen und gesichert, die Wartezeit ist abgelaufen. Stelle jetzt mit dem zweipoligen Spannungsprüfer fest, ob das System spannungsfrei ist.</p></div>';
    h += '<div class="card">' + pruefer() + '<p class="lbl" style="margin-top:10px">Prüfspitzen anlegen an</p><div class="seg wrap">' + H.PUNKTE.map(([id, t]) => btn('punkt', id, t, anzeige && anzeige.punkt === id)).join('') + '</div>';
    if (m.log.length) h += '<p class="lbl">Deine Messungen</p><ol style="margin:0;padding-left:20px;font-size:14px">' + m.log.map(([p, v]) => '<li>' + esc(H.PUNKTE.find(x => x[0] === p)[1]) + ': <b>' + (v === null ? 'keine Anzeige' : v + ' V') + '</b></li>').join('') + '</ol>';
    h += '</div>';
    if (ergebnis) {
      const zeigen = ergebnis.richtig || ergebnis.zeigen;
      h += '<div class="meld ' + (ergebnis.richtig ? 'ok' : 'warn') + '"><b>' + (ergebnis.richtig ? 'Richtig!' : 'Leider falsch.') + '</b>' +
        (ergebnis.hinweise.length ? '<ul style="margin:6px 0 0;padding-left:18px">' + ergebnis.hinweise.map(t => '<li>' + esc(t) + '</li>').join('') + '</ul>' : '') +
        (zeigen ? '<br>' + esc(ergebnis.erklaerung) : '') + '</div>';
      h += zeigen ? '<button class="primary" style="width:100%" data-neumessung="1">Neues Fahrzeug</button>' : '<div class="seg"><button class="primary" data-weiter="1">Nochmal überlegen</button><button data-loesung="1">Lösung zeigen</button></div>';
    } else {
      h += '<div class="card"><p class="lbl">Dein Urteil</p><div class="seg wrap">' + H.URTEILE.map(([id, t]) => btn('urteil', id, t, urteil === id)).join('') + '</div>';
      if (urteilFehler) h += '<p class="meld warn">' + urteilFehler + '</p>';
      h += '<button class="primary" style="width:100%" data-bewerten="1">Urteil prüfen</button></div>';
    }
    return h;
  }

  function render() {
    root.innerHTML = '<div class="seg">' + btn('teil', 'ablauf', '1. Ablauf ordnen', teil === 'ablauf') + btn('teil', 'messen', '2. Freimessen', teil === 'messen') + '</div>' +
      '<div class="meld info">Übung zum Verständnis. In der Werkstatt gilt immer die Reparaturanleitung des Herstellers, und nur Personen mit HV-Qualifikation (mind. Stufe 2S) dürfen die Spannungsfreiheit herstellen.</div>' +
      (teil === 'ablauf' ? renderAblauf() : renderMessen());
  }

  root.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    const d = b.dataset;
    if (d.teil) { teil = d.teil; if (teil === 'messen' && !m) neueMessung(); }
    else if (d.nimm) { liste.push(d.nimm); pruefung = null; }
    else if (d.weg) { liste.splice(+d.weg, 1); pruefung = null; }
    else if (d.hoch) { const i = +d.hoch; [liste[i - 1], liste[i]] = [liste[i], liste[i - 1]]; pruefung = null; }
    else if (d.pruefen) pruefung = H.pruefeReihenfolge(liste);
    else if (d.nochmal) neuerAblauf();
    else if (d.punkt) { if (!ergebnis) anzeige = { punkt: d.punkt, v: H.messe(m, d.punkt) }; }
    else if (d.urteil) { urteil = d.urteil; urteilFehler = ''; }
    else if (d.bewerten) { if (!urteil) urteilFehler = 'Wähle zuerst ein Urteil aus.'; else ergebnis = H.bewerte(m, urteil); }
    else if (d.weiter) { ergebnis = null; urteil = null; }
    else if (d.loesung) ergebnis.zeigen = true;
    else if (d.neumessung) neueMessung();
    else return;
    render();
  });

  neuerAblauf();
  render();
})();
