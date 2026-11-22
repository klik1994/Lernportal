(function () {
  const L = Lernstand, T = Tests;
  const app = document.getElementById('app');
  const DATEI = 'inhalte/Lernportal-Inhalte.xlsx';
  let storage = null;
  try { storage = window.localStorage; } catch (e) { storage = null; }
  const store = L.createStore(storage);
  let state = store.load();
  let inhalt = null, themenNamen = [], lehrjahrOffen = false;
  let quiz = null, resetFrage = false, videoAn = {}, metas = {};

  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const absaetze = s => s.split(/\n+/).filter(x => x.trim()).map(x => '<p>' + esc(x) + '</p>').join('');
  const badge = st => '<span class="badge b-' + st + '">' + st + '</span>';
  const themaLink = name => '#/thema/' + encodeURIComponent(name);
  const save = () => store.save(state);
  const aktiveFragen = () => inhalt.fragen.filter(f => themenNamen.includes(f.thema));
  const anzahlEingang = () => T.anzahlFuerTest(aktiveFragen());
  const LJ_TEXT = n => n + '. Lehrjahr';
  function aktualisiereAktive() { themenNamen = Inhalte.aktiveThemen(inhalt.themen, state.lehrjahr).map(t => t.name); }
  const gesperrt = t => !!state.lehrjahr && (t.lehrjahr || 1) > state.lehrjahr;
  const minuten = () => Math.max(5, Math.round(anzahlEingang() * 0.5 / 5) * 5);

  function route() {
    const h = decodeURIComponent(location.hash.replace(/^#\/?/, ''));
    const [r, ...rest] = h.split('/');
    return { r: r || 'start', arg: rest.join('/') };
  }

  function hinweis() {
    return store.persistent ? '' : '<div class="hint">Dein Lernstand kann auf diesem Gerät nicht gespeichert werden. Er geht beim Schließen verloren.</div>';
  }

  function render() {
    if (!inhalt) return;
    aktualisiereAktive();
    const { r, arg } = route();
    const navR = ['themen', 'thema', 'bereich'].includes(r) ? 'start' : r;
    document.querySelectorAll('#nav a[data-r]').forEach(a => a.classList.toggle('on', a.dataset.r === navR));
    document.body.classList.toggle('ohne-nav', !state.lehrjahr && !['impressum', 'datenschutz'].includes(r));
    if (r === 'impressum') return show(renderImpressum());
    if (r === 'datenschutz') return show(renderDatenschutz());
    if (r === 'test' && quiz) return show(quiz.fertig ? renderErgebnis() : renderFrage());
    if (r === 'test') { location.hash = '#/'; return; }
    if (r === 'lexikon') { if (arg) lexBereich = ''; show(renderLexikon()); return lexikonFertig(arg); }
    if (!state.lehrjahr) return show(renderLehrjahrWahl());
    if (r === 'lernstand') return show(renderLernstand());
    if (r === 'thema') return show(renderThema(arg));
    if (r === 'bereich') return show(renderBereich(arg));
    if (r === 'ueben') return show(renderUeben());
    if (r === 'werkstatt') return show(renderWerkstatt());
    return show(renderThemen());
  }
  function show(html) { app.innerHTML = hinweis() + html; }

  const PALETTE = ['yel', 'pur', 'tea', 'roy', 'blu', 'ora', 'grn', 'red'];
  function bereichFarbe(b) {
    const bereiche = [];
    inhalt.themen.forEach(t => { if (!bereiche.includes(t.bereich)) bereiche.push(t.bereich); });
    return PALETTE[Math.max(0, bereiche.indexOf(b)) % PALETTE.length];
  }
  function iconHtml(text) {
    const t = String(text || '?');
    return '<div class="icon' + (t.length > 2 ? ' lang' : '') + '" aria-hidden="true">' + esc(t) + '</div>';
  }
  function themaIcon(t) {
    const erste = (t.praesentationen || []).map(p => metas[p.link]).find(m => m && m.symbol);
    return iconHtml(erste ? erste.symbol : t.name.trim().charAt(0).toUpperCase());
  }
  const kurz = (s, n) => { const x = (s || '').replace(/\s+/g, ' ').trim(); return x.length > n ? x.slice(0, n).replace(/\s+\S*$/, '') + ' …' : x; };
  const anzahlFragen = name => inhalt.fragen.filter(f => f.thema === name).length;
  const plural = (n, eins, mehr) => n + ' ' + (n === 1 ? eins : mehr);

  function lehrjahrKnoepfe() {
    return '<div class="knopfgitter">' + [1, 2, 3, 4].map(n => {
      const anz = Inhalte.aktiveThemen(inhalt.themen, n).length;
      return '<button class="' + (state.lehrjahr === n ? 'primary' : '') + '" data-lehrjahr="' + n + '">' + LJ_TEXT(n) + '<span class="klein">' + anz + ' Themen</span></button>';
    }).join('') + '</div>';
  }

  function renderLehrjahrWahl() {
    return '<p class="eyebrow">Los geht\'s</p><h1>In welchem Lehrjahr bist du?</h1><p class="lead">Danach werden die Themen freigeschaltet, die laut Rahmenlehrplan bis zu deinem Lehrjahr dran sind. Du kannst das später jederzeit ändern.</p>' +
      '<div class="card a-yel">' + lehrjahrKnoepfe() + '</div>';
  }

  function renderWillkommen() {
    return '<p class="eyebrow">Los geht\'s</p><h1>Willkommen im Lernportal</h1><p class="lead">Hier lernst du die Themen deiner Ausbildung mit Präsentationen, Videos, Tests und Praxisübungen.</p>' +
      '<div class="grid"><div class="kachel a-yel">' + iconHtml('✓') + '<h3>Eingangstest</h3>' +
      '<p>Mach zuerst den Eingangstest. Danach siehst du, welche Themen schon sitzen und was du noch lernen musst.</p>' +
      '<p class="meta">' + anzahlEingang() + ' Fragen · ' + themenNamen.length + ' Themen · ca. ' + minuten() + ' Min. · keine Note</p>' +
      '<div class="knoepfe"><button class="primary" data-start="eingang">Eingangstest starten</button></div></div></div>';
  }

  function renderLernstand() {
    const fp = L.fortschritt(state, themenNamen);
    const next = L.nextSteps(state, themenNamen);
    const sitzt = themenNamen.filter(t => L.statusOf(state, t) === 'sitzt').length;
    let h = '<p class="eyebrow">Dein Stand · ' + LJ_TEXT(state.lehrjahr) + '</p><h1>Mein Lernstand</h1>';
    h += '<div class="zweispaltig"><div class="card"><p class="muted" style="margin:0 0 6px">Fortschritt</p><p class="zahl">' + fp + ' %</p><p class="muted">' + sitzt + ' von ' + themenNamen.length + ' Themen sitzen</p><div class="bar"><div style="width:' + fp + '%"></div></div></div>';
    h += '<div class="card a-roy"><p class="muted" style="margin:0 0 6px">Wissenstest</p><p>' + anzahlEingang() + ' Fragen aus allen freigeschalteten Themen, jedes Mal neu gemischt. Schwache Themen kommen wieder auf deine Liste.</p><button class="primary" data-start="pruefung">Wissenstest starten</button></div></div>';
    h += '<h2>Als Nächstes</h2>';
    h += next.length
      ? '<div class="grid">' + next.map(n => {
          const t = inhalt.themen.find(x => x.name === n.thema);
          return '<div class="kachel a-' + bereichFarbe(t.bereich) + '">' + themaIcon(t) + '<h3>' + esc(t.name) + '</h3><p>' + esc(n.text) + '</p><p class="meta">' + badge(L.statusOf(state, t.name)) + '</p>' +
            '<div class="knoepfe"><a class="btn primary" href="' + themaLink(t.name) + '">Thema öffnen</a></div></div>';
        }).join('') + '</div>'
      : '<div class="card"><p style="margin:0">Alles sitzt. Mach ab und zu den Wissenstest, damit es so bleibt.</p></div>';
    h += '<p style="margin-top:24px">' + (resetFrage
      ? '<span class="muted">Wirklich alles löschen? </span><button class="link" data-reset="ja">Ja, löschen</button><button class="link" data-reset="nein">Abbrechen</button>'
      : '<button class="link" data-reset="frage">Lernstand zurücksetzen</button>') + '</p>';
    h += '<div class="card"><p style="margin:0 0 8px"><b>Dein Lehrjahr:</b> ' + LJ_TEXT(state.lehrjahr) + (lehrjahrOffen ? '' : ' &nbsp;<button class="link" data-lehrjahr-aendern="1">Ändern</button>') + '</p>' +
      (lehrjahrOffen ? '<p class="muted">Neue Themen werden freigeschaltet und stehen dann bei „Als Nächstes“. Dein bisheriger Stand bleibt erhalten.</p>' + lehrjahrKnoepfe() : '') + '</div>';
    return h;
  }

  function sternKnopf(t) {
    const on = state.sterne.includes(t);
    return '<button class="star' + (on ? ' on' : '') + '" data-stern="' + esc(t) + '" aria-label="' + (on ? 'Merken aufheben' : 'Merken') + '">' + (on ? '★' : '☆') + '</button>';
  }

  const bereichLink = name => '#/bereich/' + encodeURIComponent(name);
  const ICONS = {
    blitz: '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    chip: '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    motor: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M2 12h3M19 12h3M4.9 19.1 7 17M17 7l2.1-2.1"/>',
    hv: '<path d="M12 3 2 20h20z"/><path d="m13 8-3 5h4l-3 5"/>',
    schloss: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>'
  };
  function bereichIcon(name, zu) {
    const n = name.toLowerCase();
    const key = zu ? 'schloss' : /hochvolt/.test(n) ? 'hv' : /elektronik|bus|vernetz/.test(n) ? 'chip' : /elektri/.test(n) ? 'blitz' : /motor|antrieb/.test(n) ? 'motor' : null;
    if (!key) return iconHtml(name.trim().charAt(0).toUpperCase());
    return '<div class="icon" aria-hidden="true"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' + ICONS[key] + '</svg></div>';
  }
  const sitzen = namen => namen.filter(n => L.statusOf(state, n) === 'sitzt').length;
  const prozent = namen => namen.length ? Math.round(sitzen(namen) / namen.length * 100) : 0;

  function bereichKachel(bereich, themen, zu, untertitel) {
    const namen = themen.map(t => t.name);
    const angef = namen.filter(n => L.statusOf(state, n) === 'angefangen').length;
    const meta = zu ? plural(themen.length, 'Thema', 'Themen') + ' · ab ' + LJ_TEXT(themen[0].lehrjahr || 1)
      : plural(themen.length, 'Thema', 'Themen') + ' · ' + sitzen(namen) + ' sitzen' + (angef ? ' · ' + angef + ' angefangen' : '');
    const innen = bereichIcon(bereich, zu) + '<div class="bk-text"><span class="bk-name">' + esc(bereich) + '</span>' +
      (untertitel ? '<span class="bk-unter">' + esc(untertitel) + '</span>' : '') + '<span class="bk-meta">' + meta + '</span>' +
      (zu ? '' : '<span class="bar"><span style="width:' + prozent(namen) + '%"></span></span>') + '</div>' +
      (zu ? '' : '<svg class="bk-pfeil" aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="m9 6 6 6-6 6"/></svg>');
    return zu ? '<div class="bereich-kachel gesperrt a-' + bereichFarbe(bereich) + '">' + innen + '</div>'
      : '<a class="bereich-kachel a-' + bereichFarbe(bereich) + '" href="' + bereichLink(bereich) + '">' + innen + '</a>';
  }

  function renderThemen() {
    const lj = state.lehrjahr || 1;
    let h = '<p class="eyebrow">Dein Lernpfad · ' + LJ_TEXT(lj) + '</p><h1>Lernfelder</h1><p class="lead">Die Bereiche in der Reihenfolge deiner Ausbildung. Tippe auf einen Bereich, um seine Themen zu sehen.</p>';
    h += '<div class="kachel a-yel wissenstest">' + iconHtml('✓') + '<div class="wt-text"><h3>Teste hier dein Wissen</h3>' +
      '<p>Ein Test über alles bis zum ' + LJ_TEXT(lj) + ', jedes Mal neu zusammengestellt.</p><p class="meta">' + anzahlEingang() + ' Fragen · ca. ' + minuten() + ' Min.</p>' +
      '<div class="knoepfe"><button class="primary" data-start="pruefung">Wissenstest starten</button></div></div></div><div class="pfad">';
    [1, 2, 3, 4].forEach(jahr => {
      const imJahr = inhalt.themen.filter(t => (t.lehrjahr || 1) === jahr);
      const zu = jahr > lj;
      const alleSitzen = imJahr.length && imJahr.every(t => L.statusOf(state, t.name) === 'sitzt');
      const zustand = zu ? 'zu' : alleSitzen ? 'fertig' : jahr === lj ? 'aktuell' : 'frei';
      const label = { zu: 'gesperrt', fertig: 'alles sitzt', aktuell: 'dein Lehrjahr', frei: 'freigeschaltet' }[zustand];
      const bereiche = [];
      imJahr.forEach(t => { if (!bereiche.includes(t.bereich)) bereiche.push(t.bereich); });
      h += '<div class="pfad-jahr p-' + zustand + '"><div class="pfad-linie"><span class="pfad-punkt"></span></div><div class="pfad-inhalt">' +
        '<div class="pfad-kopf"><span class="pfad-titel">' + LJ_TEXT(jahr) + '</span><span class="pfad-label">' + label + '</span></div>';
      h += bereiche.length ? bereiche.map(b => {
        const th = imJahr.filter(t => t.bereich === b);
        const gesamt = inhalt.themen.filter(t => t.bereich === b).length;
        return bereichKachel(b, th, zu, gesamt > th.length && th.length <= 3 ? th.map(t => t.name.replace(/^.*?:\s*/, '')).join(', ') : '');
      }).join('') : '<p class="muted" style="margin:0">Noch keine Themen</p>';
      h += '</div></div>';
    });
    return h + '</div>';
  }

  function renderBereich(name) {
    const themen = inhalt.themen.filter(t => t.bereich === name).sort((a, b) => (a.lehrjahr || 1) - (b.lehrjahr || 1));
    if (!themen.length) return '<h1>Bereich nicht gefunden</h1><p><a href="#/themen">Zu den Themen</a></p>';
    const frei = themen.filter(t => !gesperrt(t));
    const namen = frei.map(t => t.name);
    const fragen = inhalt.fragen.filter(f => namen.includes(f.thema));
    let h = '<a class="zurueck" href="#/themen"><svg aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="m15 6-6 6 6 6"/></svg>Alle Bereiche</a>';
    h += '<div class="kachel bereich-kopf a-' + bereichFarbe(name) + '"><div style="display:flex;align-items:center;gap:14px">' + bereichIcon(name, false) +
      '<div><p class="eyebrow" style="margin:0">Bereich</p><h1 style="margin:2px 0 0">' + esc(name) + '</h1></div></div>';
    if (frei.length) {
      h += '<p class="muted" style="margin:12px 0 6px">' + sitzen(namen) + ' von ' + plural(frei.length, 'Thema', 'Themen') + ' sitzen' + (frei.length < themen.length ? ' · ' + (themen.length - frei.length) + ' noch gesperrt' : '') + '</p><div class="bar"><div style="width:' + prozent(namen) + '%"></div></div>';
      if (fragen.length) h += '<div class="knoepfe" style="margin-top:14px"><button class="primary" data-bereichstest="' + esc(name) + '">Bereichstest starten</button><span class="muted">' + T.anzahlFuerTest(fragen) + ' Fragen aus diesem Bereich</span></div>';
    } else h += '<p class="muted" style="margin:12px 0 0">Dieser Bereich wird ab dem ' + LJ_TEXT(themen[0].lehrjahr || 1) + ' freigeschaltet.</p>';
    h += '</div><div class="themenliste">';
    h += themen.map(t => {
      const zu = gesperrt(t);
      const np = (t.praesentationen || []).length, nf = anzahlFragen(t.name);
      const meta = [np ? plural(np, 'Präsentation', 'Präsentationen') : '', nf ? plural(nf, 'Frage', 'Fragen') : ''].filter(Boolean).join(' · ');
      const innen = (zu ? bereichIcon(name, true) : themaIcon(t)) + '<div class="tz-text"><span class="tz-name">' + esc(t.name.replace(/^Motormanagement:\s*/, '')) + '</span><span class="tz-meta">' +
        (zu ? '<span class="badge b-offen">ab ' + LJ_TEXT(t.lehrjahr) + '</span>' : badge(L.statusOf(state, t.name))) + (meta ? '<span>' + meta + '</span>' : '') + '</span></div>';
      return zu ? '<div class="themazeile gesperrt a-' + bereichFarbe(name) + '">' + innen + '</div>'
        : '<a class="themazeile a-' + bereichFarbe(name) + '" href="' + themaLink(t.name) + '">' + innen + '<svg class="bk-pfeil" aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="m9 6 6 6-6 6"/></svg></a>';
    }).join('');
    return h + '</div>';
  }

  function deckKachel(p, standardFarbe) {
    const m = metas[p.link] || {};
    const teile = [m.folien ? m.folien + ' Folien' : '', m.video ? 'Video' : '', m.fragen ? plural(m.fragen, 'Testfrage', 'Testfragen') : ''].filter(Boolean).join(' · ');
    return '<div class="kachel a-' + (m.farbe || standardFarbe) + '">' + iconHtml(m.symbol || '▶') +
      '<h3>' + esc(p.titel) + '</h3>' + (m.untertitel ? '<p>' + esc(m.untertitel) + '</p>' : '') +
      (teile ? '<p class="meta">' + teile + '</p>' : '<p class="meta"></p>') +
      '<div class="knoepfe"><a class="btn primary" href="' + esc(p.link) + '">Präsentation starten</a>' +
      (m.video ? '<button data-nurvideo="' + esc(m.video) + '">Nur Video</button>' : '') + '</div></div>';
  }

  function renderThema(name) {
    const t = inhalt.themen.find(x => x.name === name);
    if (!t) return '<h1>Thema nicht gefunden</h1><p><a href="#/themen">Zur Themenliste</a></p>';
    if (gesperrt(t)) return '<p class="eyebrow"><a href="#/themen" style="color:inherit;text-decoration:none">Lernfelder</a> · ' + esc(t.bereich) + '</p><h1>' + esc(t.name) + '</h1>' +
      '<div class="card"><p>🔒 Dieses Thema wird ab dem ' + LJ_TEXT(t.lehrjahr) + ' freigeschaltet.</p><p class="muted" style="margin:0">Dein Lehrjahr kannst du unter „Lernstand“ ändern.</p></div>';
    const farbe = bereichFarbe(t.bereich);
    const anzahl = anzahlFragen(t.name);
    let h = '<p class="eyebrow"><a href="#/themen" style="color:inherit;text-decoration:none">Lernfelder</a> · <a href="' + bereichLink(t.bereich) + '" style="color:inherit;text-decoration:none">' + esc(t.bereich) + '</a></p>';
    h += '<div style="display:flex;align-items:center;gap:6px"><h1 style="flex:1;margin:6px 0">' + esc(t.name) + '</h1>' + sternKnopf(t.name) + '</div>';
    h += '<p>' + badge(L.statusOf(state, t.name)) + '</p>';
    if (t.praesentationen && t.praesentationen.length) {
      h += '<h2>Präsentation' + (t.praesentationen.length > 1 ? 'en' : '') + '</h2><p class="muted">Mit Animationen, Lernvideo und Kurztest. Tippen oder wischen zum Weiterblättern.</p>';
      h += '<div class="grid">' + t.praesentationen.map(p => deckKachel(p, farbe)).join('') + '</div>';
    }
    if (t.videoDatei || t.video) h += '<h2>Video</h2>';
    if (t.videoDatei) h += '<div class="video"><video src="' + esc(t.videoDatei) + '" controls preload="metadata" playsinline></video></div>';
    if (t.video) {
      h += videoAn[t.video]
        ? '<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/' + t.video + '?autoplay=1" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="Video"></iframe></div>'
        : '<div class="card"><p class="muted">Beim Abspielen wird das Video von YouTube geladen.</p><button data-video="' + t.video + '">▶ Video abspielen</button></div>';
    }
    h += '<div class="zweispaltig" style="margin-top:22px">';
    if (t.erklaerung) h += '<div class="card text"><h3 style="margin-top:0">Kurz erklärt</h3>' + absaetzeMitLexikon(t.erklaerung) +
      (inhalt.lexikon.length ? '<p class="muted" style="margin:12px 0 0">Unterstrichene Fachbegriffe kannst du antippen. Alle Begriffe findest du im <a href="#/lexikon">Lexikon</a>.</p>' : '') + '</div>';
    h += '<div class="card a-' + farbe + '"><h3 style="margin-top:0">Kurztest</h3>';
    h += anzahl
      ? '<p class="muted">' + Math.min(5, anzahl) + ' Fragen. Ab 80 % sitzt das Thema.</p><button class="primary" data-kurz="' + esc(t.name) + '">Kurztest starten</button>'
      : '<p class="muted" style="margin:0">Zu diesem Thema gibt es noch keine Fragen.</p>';
    return h + '</div></div>';
  }

  function renderUeben() {
    return '<p class="eyebrow">Trainieren</p><h1>Üben</h1><p class="lead">Stell dir deinen eigenen Test zusammen oder prüfe dich quer durch alle Themen.</p><div class="zweispaltig">' +
      '<div class="card a-roy"><h3 style="margin-top:0">Eigener Übungstest</h3><p class="muted">Wähle die Themen, die du üben willst.</p>' +
      themenNamen.map((t, i) => '<label class="check"><input type="checkbox" data-wahl="' + i + '"> ' + esc(t) + '</label>').join('') +
      '<div class="err" id="err"></div><button class="primary" data-start="uebung">Übungstest starten (bis zu 10 Fragen)</button></div>' +
      '<div><div class="kachel a-yel" style="margin-bottom:16px">' + iconHtml('✓') + '<h3>Wissenstest</h3><p>' + anzahlEingang() + ' Fragen aus allen freigeschalteten Themen, jedes Mal neu gemischt.</p><div class="knoepfe"><button class="primary" data-start="pruefung">Wissenstest starten</button></div></div>' +
      '<div class="kachel a-tea">' + iconHtml('V') + '<h3>Werkstatt</h3><p>Multimeter und CAN-Bus-Oszilloskop: messen und Fehler suchen.</p><div class="knoepfe"><a class="btn primary" href="#/werkstatt">Zur Werkstatt</a></div></div></div></div>';
  }

  function anbieter() {
    const e = inhalt.einstellungen;
    const feld = k => e[k] ? esc(e[k]) : '<span class="muted">[in der Excel-Datei unter „Einstellungen“ eintragen]</span>';
    const tel = e['Impressum Telefon (freiwillig)'] ? '<br>Telefon: ' + esc(e['Impressum Telefon (freiwillig)']) : '';
    return '<p>' + feld('Impressum Name') + '<br>' + feld('Impressum Anschrift').replace(/\n/g, '<br>') + '<br>E-Mail: ' + feld('Impressum E-Mail') + tel + '</p>';
  }

  function renderWerkstatt() {
    return '<p class="eyebrow">Praxis</p><h1>Werkstatt</h1><p class="lead">Übungen zum Messen und zur Fehlersuche, wie in der Werkstatt.</p><div class="grid">' +
      '<div class="kachel a-yel">' + iconHtml('V') + '<h3>Multimeter</h3><p>Spannung und Widerstand messen, Fehler suchen im einfachen Stromkreis, in der Parallel- und in der Reihenschaltung.</p><div class="knoepfe"><a class="btn primary" href="multimeter.html">Übung öffnen</a></div></div>' +
      '<div class="kachel a-pur">' + iconHtml('CAN') + '<h3>CAN-Bus-Diagnose</h3><p>CAN-High und CAN-Low am Oszilloskop ansehen, Widerstände am Diagnosestecker messen und Busfehler erkennen.</p><div class="knoepfe"><a class="btn primary" href="can.html">Übung öffnen</a></div></div>' +
      '</div>';
  }

  function renderImpressum() {
    const name = inhalt.einstellungen['Impressum Name'] ? esc(inhalt.einstellungen['Impressum Name']) : 'der oben genannte Anbieter';
    return '<h1>Impressum</h1><div class="card text"><h2 style="margin-top:0">Angaben gemäß § 5 DDG</h2>' + anbieter() +
      '<h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2><p>' + name + ' (Anschrift wie oben)</p>' +
      '<h2>Über dieses Angebot</h2><p>Privates, kostenloses Lernangebot für Auszubildende im Kfz-Handwerk. Es gibt keine Werbung und keine kostenpflichtigen Inhalte.</p>' +
      '<h2>Haftung für Inhalte</h2><p>Die Inhalte wurden mit Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität wird jedoch keine Gewähr übernommen. Die Lerninhalte ersetzen nicht die Herstellerangaben, Werkstattliteratur und Sicherheitsvorschriften.</p>' +
      '<h2>Haftung für Links</h2><p>Für Inhalte verlinkter externer Seiten (z. B. YouTube) sind ausschließlich deren Betreiber verantwortlich. Bei Bekanntwerden von Rechtsverletzungen werden entsprechende Links umgehend entfernt.</p>' +
      '<h2>Urheberrecht</h2><p>Die Texte, Fragen und Übungen dieses Portals dürfen nur für die Ausbildung genutzt werden. Eine Weitergabe oder Veröffentlichung an anderer Stelle bedarf der Zustimmung des Anbieters.</p></div>' +
      '<p><a href="#/datenschutz">Zur Datenschutzerklärung</a></p>';
  }

  function renderDatenschutz() {
    const a = '<a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">Datenschutzerklärung von GitHub</a>';
    const g = '<a href="https://policies.google.com/privacy?hl=de" target="_blank" rel="noopener">Datenschutzerklärung von Google</a>';
    return '<h1>Datenschutzerklärung</h1><div class="card text">' +
      '<h2 style="margin-top:0">1. Verantwortlicher</h2>' + anbieter() +
      '<h2>2. Kurz gesagt</h2><p>Dieses Lernportal braucht keine Anmeldung, setzt keine Cookies, verwendet kein Tracking und keine Analyse-Tools. Der Anbieter selbst sammelt keine personenbezogenen Daten.</p>' +
      '<h2>3. Hosting über GitHub Pages</h2><p>Die Seite wird bei GitHub Pages bereitgestellt (GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA). Beim Aufruf der Seite verarbeitet GitHub automatisch technisch notwendige Daten, insbesondere deine IP-Adresse, Datum und Uhrzeit des Zugriffs, die aufgerufene Seite sowie Browser- und Gerätetyp (Server-Logfiles). GitHub speichert die IP-Adresse aus Sicherheitsgründen. Der Anbieter dieses Portals hat auf diese Daten keinen Zugriff.</p>' +
      '<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Das berechtigte Interesse liegt in der sicheren und zuverlässigen Bereitstellung der Seite. Dabei können Daten in die USA übermittelt werden. GitHub ist nach dem EU-US Data Privacy Framework zertifiziert (Angemessenheitsbeschluss der EU-Kommission vom 10.07.2023). Weitere Informationen: ' + a + '.</p>' +
      '<h2>4. Dein Lernstand auf deinem Gerät</h2><p>Dein Lernstand (Ergebnisse, Status der Themen, gemerkte Themen) wird nur im lokalen Speicher deines Browsers (localStorage) auf deinem eigenen Gerät abgelegt. Er wird nicht übertragen, und der Anbieter kann ihn nicht einsehen. Die Speicherung ist für die von dir gewünschte Funktion unbedingt erforderlich (§ 25 Abs. 2 Nr. 2 TDDDG). Du kannst den Lernstand jederzeit unter „Lernstand“ → „Lernstand zurücksetzen“ oder über die Browsereinstellungen löschen.</p>' +
      '<h2>5. YouTube-Videos</h2><p>Videos sind im erweiterten Datenschutzmodus (youtube-nocookie.com) eingebunden und werden erst geladen, wenn du auf „Video abspielen“ tippst. Erst dann wird eine Verbindung zu YouTube (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland) hergestellt. Dabei werden unter anderem deine IP-Adresse und die aufgerufene Seite an Google übermittelt, eventuell auch in die USA. Google ist nach dem EU-US Data Privacy Framework zertifiziert.</p>' +
      '<p>Rechtsgrundlage ist deine Einwilligung durch das Antippen (Art. 6 Abs. 1 lit. a DSGVO, § 25 Abs. 1 TDDDG). Ohne Antippen werden keine Daten an YouTube übertragen. Weitere Informationen: ' + g + '.</p>' +
      '<h2>6. Deine Rechte</h2><p>Du hast das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch (Art. 21). Eine erteilte Einwilligung kannst du jederzeit für die Zukunft widerrufen. Außerdem hast du das Recht, dich bei einer Datenschutz-Aufsichtsbehörde zu beschweren (Art. 77 DSGVO). Für Fragen genügt eine E-Mail an die oben genannte Adresse. Für die Server-Logfiles von GitHub wende dich direkt an GitHub.</p>' +
      '<h2>7. Stand</h2><p>November 2026</p></div>';
  }


  // ---------------------------------------------------------------- Lexikon
  const lexId = b => 'lex-' + Lexikon.norm(b).replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  let lexBereich = '';

  function absaetzeMitLexikon(text) {
    const schon = new Set();
    return text.split(/\n+/).filter(x => x.trim()).map(x => '<p>' + Lexikon.markiere(x, inhalt.lexikon, schon).map(t =>
      t.begriff ? '<button class="lexwort" data-lex="' + esc(t.begriff) + '">' + esc(t.text) + '</button>' : esc(t.text)).join('') + '</p>').join('');
  }

  function lexEintrag(e) {
    return '<div class="card lexeintrag" id="' + lexId(e.begriff) + '" data-begriff="' + esc(e.begriff) + '" data-bereich="' + esc(e.bereich) + '">' +
      '<div class="lexkopf"><h3>' + esc(e.begriff) + '</h3><span class="lexbereich a-' + bereichFarbeLex(e.bereich) + '">' + esc(e.bereich) + '</span></div>' +
      '<p>' + esc(e.erklaerung) + '</p>' +
      (e.beispiel ? '<p class="lexbsp"><b>Beispiel:</b> ' + esc(e.beispiel) + '</p>' : '') +
      (e.alias.length ? '<p class="muted" style="margin:0">Auch: ' + e.alias.map(esc).join(', ') + '</p>' : '') + '</div>';
  }
  function bereichFarbeLex(b) {
    return inhalt.themen.some(t => t.bereich === b) ? bereichFarbe(b) : 'roy';
  }

  function renderLexikon() {
    const L = inhalt.lexikon;
    if (!L.length) return '<p class="eyebrow">Nachschlagen</p><h1>Lexikon</h1><div class="card"><p style="margin:0">Noch keine Begriffe. Trage sie in der Excel-Datei im Blatt „Lexikon“ ein.</p></div>';
    const bereiche = [];
    inhalt.themen.forEach(t => { if (L.some(e => e.bereich === t.bereich) && !bereiche.includes(t.bereich)) bereiche.push(t.bereich); });
    L.forEach(e => { if (!bereiche.includes(e.bereich)) bereiche.push(e.bereich); });
    const buchst = [];
    L.forEach(e => { const b = Lexikon.buchstabe(e.begriff); if (!buchst.includes(b)) buchst.push(b); });
    let h = '<p class="eyebrow">Nachschlagen</p><h1>Lexikon</h1><p class="lead">' + L.length + ' Fachbegriffe, einfach erklärt – mit Beispiel aus der Werkstatt.</p>';
    h += '<div class="lexsuche"><input type="search" id="lex-q" placeholder="Begriff suchen, z. B. Lambda" autocomplete="off" aria-label="Begriff suchen"></div>';
    h += '<div class="lexfilter"><button class="chip' + (lexBereich ? '' : ' on') + '" data-lexbereich="">Alle</button>' +
      bereiche.map(b => '<button class="chip a-' + bereichFarbeLex(b) + (lexBereich === b ? ' on' : '') + '" data-lexbereich="' + esc(b) + '">' + esc(b) + '</button>').join('') + '</div>';
    h += '<div class="az" id="lex-az">' + buchst.map(b => '<button data-az="' + b + '">' + b + '</button>').join('') + '</div>';
    h += '<div id="lex-liste">' + buchst.map(b => '<div class="lexgruppe" data-gruppe="' + b + '" id="lexg-' + b + '"><h2>' + b + '</h2>' +
      L.filter(e => Lexikon.buchstabe(e.begriff) === b).map(lexEintrag).join('') + '</div>').join('') + '</div>';
    h += '<div class="card" id="lex-leer" hidden><p style="margin:0">Kein Begriff gefunden. Versuch es mit einem anderen Wort.</p></div>';
    return h;
  }

  function lexFiltern() {
    const q = (document.getElementById('lex-q') || {}).value || '';
    const treffer = new Set(Lexikon.suche(inhalt.lexikon, q).filter(e => !lexBereich || e.bereich === lexBereich).map(e => e.begriff));
    app.querySelectorAll('.lexeintrag').forEach(el => { el.hidden = !treffer.has(el.dataset.begriff); });
    const sichtbar = new Set();
    app.querySelectorAll('.lexgruppe').forEach(g => {
      const an = !!g.querySelector('.lexeintrag:not([hidden])');
      g.hidden = !an; if (an) sichtbar.add(g.dataset.gruppe);
    });
    app.querySelectorAll('#lex-az [data-az]').forEach(b => { b.disabled = !sichtbar.has(b.dataset.az); });
    document.getElementById('lex-leer').hidden = treffer.size > 0;
  }

  function lexikonFertig(arg) {
    if (!inhalt.lexikon.length) return;
    const q = document.getElementById('lex-q');
    q.addEventListener('input', lexFiltern);
    lexFiltern();
    if (arg) {
      const e = Lexikon.finde(inhalt.lexikon, arg);
      const el = e && document.getElementById(lexId(e.begriff));
      if (el) { el.classList.add('markiert'); setTimeout(() => el.scrollIntoView({ block: 'center' }), 0); }
    }
  }

  function zeigeBegriff(name) {
    const e = Lexikon.finde(inhalt.lexikon, name);
    if (!e) return;
    schliesseVideo();
    const o = document.createElement('div');
    o.id = 'overlay';
    o.innerHTML = '<div class="box lexbox" role="dialog" aria-label="' + esc(e.begriff) + '">' + lexEintrag(e).replace(' id="' + lexId(e.begriff) + '"', '') +
      '<div class="lexknoepfe"><a class="btn" href="#/lexikon/' + encodeURIComponent(e.begriff) + '" id="lex-mehr">Im Lexikon öffnen</a><button class="primary" id="video-zu" style="--c:var(--roy)">Schließen</button></div></div>';
    o.addEventListener('click', ev => { if (ev.target === o || ev.target.closest('#video-zu') || ev.target.closest('#lex-mehr')) schliesseVideo(); });
    document.body.appendChild(o);
    o.querySelector('#video-zu').focus();
  }

  function starte(art, thema) {
    let liste = [];
    if (art === 'eingang' || art === 'pruefung') liste = T.pickEingang(aktiveFragen(), anzahlEingang());
    if (art === 'kurz') liste = T.pickKurz(inhalt.fragen, thema, 5);
    if (art === 'bereich') {
      const namen = inhalt.themen.filter(t => t.bereich === thema && !gesperrt(t)).map(t => t.name);
      const fr = inhalt.fragen.filter(f => namen.includes(f.thema));
      liste = T.pickEingang(fr, T.anzahlFuerTest(fr));
    }
    if (art === 'uebung') {
      const gewaehlt = Array.from(app.querySelectorAll('[data-wahl]')).filter(c => c.checked).map(c => themenNamen[+c.dataset.wahl]);
      if (!gewaehlt.length) { app.querySelector('#err').textContent = 'Wähle mindestens ein Thema aus.'; return; }
      liste = T.pickThemen(inhalt.fragen, gewaehlt, 10);
      if (!liste.length) { app.querySelector('#err').textContent = 'Zu diesen Themen gibt es noch keine Fragen.'; return; }
    }
    if (!liste.length) return;
    quiz = { art, thema, liste, antworten: [], i: 0, auswahl: null, geprueft: false, fertig: false, fehler: '', zurueck: location.hash || '#/' };
    location.hash = '#/test';
    render();
    window.scrollTo(0, 0);
  }

  function renderFrage() {
    const f = quiz.liste[quiz.i];
    const titel = { eingang: 'Eingangstest', pruefung: 'Wissenstest · ' + LJ_TEXT(state.lehrjahr || 1), kurz: 'Kurztest: ' + quiz.thema, bereich: 'Bereichstest: ' + quiz.thema, uebung: 'Übungstest' }[quiz.art];
    let h = '<p class="muted">' + esc(titel) + ' · Frage ' + (quiz.i + 1) + ' von ' + quiz.liste.length + '</p>';
    h += '<div class="bar" style="margin-bottom:16px"><div style="width:' + Math.round((quiz.i / quiz.liste.length) * 100) + '%;background:var(--roy)"></div></div>';
    h += '<div class="card"><p class="muted" style="margin:0 0 4px">' + esc(f.thema) + '</p><h2 style="margin:0 0 14px">' + esc(f.frage) + '</h2>';
    h += f.antworten.map((a, k) => {
      let cls = 'answer';
      if (quiz.geprueft) { if (k === f.richtig) cls += ' ok'; else if (k === quiz.auswahl) cls += ' bad'; }
      else if (k === quiz.auswahl) cls += ' sel';
      return '<button class="' + cls + '" data-antwort="' + k + '">' + 'ABCD'[k] + ') ' + esc(a) + '</button>';
    }).join('');
    if (quiz.fehler) h += '<div class="err">' + esc(quiz.fehler) + '</div>';
    if (quiz.geprueft) {
      const ok = quiz.auswahl === f.richtig;
      h += '<div class="fb ' + (ok ? 'ok' : 'bad') + '"><b>' + (ok ? 'Richtig.' : 'Leider falsch.') + '</b> ' + esc(f.erklaerung || '') + '</div>';
      h += '<button class="primary full" data-weiter="1">' + (quiz.i + 1 < quiz.liste.length ? 'Weiter' : 'Auswertung ansehen') + '</button>';
    } else h += '<button class="primary full" data-pruefen="1">Antwort prüfen</button>';
    h += '</div><p><button class="link" data-abbrechen="1">Test abbrechen</button></p>';
    return h;
  }

  function beende() {
    const r = T.score(quiz.liste, quiz.antworten);
    Object.keys(r.proThema).forEach(t => { state = L.applyResult(state, t, r.proThema[t], quiz.art); });
    if (quiz.art === 'eingang') state = L.markEingangFertig(state);
    save();
    quiz.ergebnis = r;
    quiz.fertig = true;
    render();
    window.scrollTo(0, 0);
  }

  function renderErgebnis() {
    const r = quiz.ergebnis;
    let h = '<h1>Auswertung</h1><div class="card"><p style="margin:0"><b>' + r.gesamt + ' %</b> richtig</p></div><h2>Nach Themen</h2><div class="card">';
    h += Object.keys(r.proThema).map(t => {
      const p = r.proThema[t];
      return '<div class="row"><a class="t" href="' + themaLink(t) + '">' + esc(t) + '<div class="bar" style="margin-top:4px"><div style="width:' + p + '%;background:' + (p >= L.GRENZE ? 'var(--grn)' : 'var(--red)') + '"></div></div></a><span>' + p + ' %</span>' + badge(L.statusOf(state, t)) + '</div>';
    }).join('') + '</div>';
    const schwach = Object.keys(r.proThema).filter(t => r.proThema[t] < L.GRENZE);
    if (schwach.length) h += '<p>Diese Themen stehen jetzt bei „Als Nächstes“: ' + schwach.map(esc).join(', ') + '.</p>';
    return h + '<button class="primary full" data-fertig="1">Zur Übersicht</button>';
  }

  app.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    const d = b.dataset;
    if (d.start) starte(d.start);
    else if (d.kurz) starte('kurz', d.kurz);
    else if (d.bereichstest) starte('bereich', d.bereichstest);
    else if (d.stern) { state = L.toggleStern(state, d.stern); save(); render(); }
    else if (d.video) { videoAn[d.video] = true; render(); }
    else if (d.nurvideo) zeigeVideo(d.nurvideo);
    else if (d.lex) zeigeBegriff(d.lex);
    else if (d.lexbereich !== undefined) { lexBereich = d.lexbereich; app.querySelectorAll('[data-lexbereich]').forEach(x => x.classList.toggle('on', x.dataset.lexbereich === lexBereich)); lexFiltern(); }
    else if (d.az) { const g = document.getElementById('lexg-' + d.az); if (g) g.scrollIntoView({ block: 'start' }); }
    else if (d.antwort !== undefined && quiz && !quiz.geprueft) { quiz.auswahl = +d.antwort; quiz.fehler = ''; render(); }
    else if (d.pruefen) {
      if (quiz.auswahl === null) { quiz.fehler = 'Wähle zuerst eine Antwort aus.'; render(); return; }
      quiz.antworten[quiz.i] = quiz.auswahl; quiz.geprueft = true; render();
    } else if (d.weiter) {
      if (quiz.i + 1 < quiz.liste.length) { quiz.i++; quiz.auswahl = null; quiz.geprueft = false; render(); window.scrollTo(0, 0); }
      else beende();
    } else if (d.abbrechen) { const z = quiz.zurueck; quiz = null; location.hash = z === '#/test' ? '#/' : z; }
    else if (d.fertig) { quiz = null; location.hash = '#/'; }
    else if (d.lehrjahr) { state = L.setLehrjahr(state, +d.lehrjahr); save(); lehrjahrOffen = false; if (route().r === 'lernstand') render(); else if (location.hash && location.hash !== '#/') location.hash = '#/'; else render(); window.scrollTo(0, 0); }
    else if (d.lehrjahrAendern) { lehrjahrOffen = true; render(); }
    else if (d.reset === 'frage') { resetFrage = true; render(); }
    else if (d.reset === 'ja') { state = L.initialState(); save(); resetFrage = false; render(); }
    else if (d.reset === 'nein') { resetFrage = false; render(); }
  });

  window.addEventListener('hashchange', () => {
    if (route().r !== 'test') quiz = null;
    resetFrage = false;
    lehrjahrOffen = false;
    render();
    window.scrollTo(0, 0);
  });

  async function ladeMetas() {
    const links = [];
    inhalt.themen.forEach(t => (t.praesentationen || []).forEach(p => { if (/^praesentationen\//.test(p.link) && !links.includes(p.link)) links.push(p.link); }));
    await Promise.all(links.map(async link => {
      try {
        const res = await fetch(link);
        if (!res.ok) return;
        const m = PraesMeta.parseMeta(await res.text());
        const v = PraesMeta.videoPfad(link);
        m.video = null;
        if (v) { try { const r = await fetch(v, { method: 'HEAD' }); if (r.ok) m.video = v; } catch (e) { /* kein Video */ } }
        metas[link] = m;
      } catch (e) { /* Präsentation nicht erreichbar */ }
    }));
    if (!quiz) render();
  }

  function zeigeVideo(src) {
    schliesseVideo();
    const o = document.createElement('div');
    o.id = 'overlay';
    o.innerHTML = '<div class="box"><div class="zu"><button id="video-zu" aria-label="Video schließen">✕ Schließen</button></div><div class="video" style="margin:0"><video src="' + esc(src) + '" controls autoplay playsinline></video></div></div>';
    o.addEventListener('click', e => { if (e.target === o || e.target.closest('#video-zu')) schliesseVideo(); });
    document.body.appendChild(o);
  }
  function schliesseVideo() { const o = document.getElementById('overlay'); if (o) o.remove(); }
  document.addEventListener('keydown', e => { if (e.key === 'Escape') schliesseVideo(); });

  async function laden() {
    app.innerHTML = '<p class="muted">Lade Inhalte …</p>';
    try {
      const res = await fetch(DATEI + '?v=' + Date.now(), { cache: 'no-store' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      inhalt = Inhalte.parseInhalte(await Xlsx.readXlsx(await res.arrayBuffer()));
      aktualisiereAktive();
      if (inhalt.einstellungen['Portal-Name']) {
        document.getElementById('titel').textContent = inhalt.einstellungen['Portal-Name'];
        document.title = inhalt.einstellungen['Portal-Name'];
      }
      if (!inhalt.fragen.length) { app.innerHTML = '<div class="hint">In der Excel-Datei wurden keine gültigen Fragen gefunden.</div>'; return; }
      render();
      ladeMetas();
    } catch (err) {
      app.innerHTML = '<div class="hint">Die Inhalte konnten nicht geladen werden. Prüfe deine Internetverbindung.</div><button class="primary" id="nochmal">Nochmal versuchen</button>';
      document.getElementById('nochmal').onclick = laden;
    }
  }
  laden();
})();
