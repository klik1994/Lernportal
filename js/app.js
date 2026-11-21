(function () {
  const L = Lernstand, T = Tests;
  const app = document.getElementById('app');
  const DATEI = 'inhalte/Lernportal-Inhalte.xlsx';
  let storage = null;
  try { storage = window.localStorage; } catch (e) { storage = null; }
  const store = L.createStore(storage);
  let state = store.load();
  let inhalt = null, themenNamen = [];
  let quiz = null, resetFrage = false, videoAn = {}, metas = {};

  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const absaetze = s => s.split(/\n+/).filter(x => x.trim()).map(x => '<p>' + esc(x) + '</p>').join('');
  const badge = st => '<span class="badge b-' + st + '">' + st + '</span>';
  const themaLink = name => '#/thema/' + encodeURIComponent(name);
  const save = () => store.save(state);
  const anzahlEingang = () => Math.min(18, inhalt.fragen.length);

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
    const { r, arg } = route();
    document.querySelectorAll('#nav a[data-r]').forEach(a => a.classList.toggle('on', a.dataset.r === r || (r === 'thema' && a.dataset.r === 'themen')));
    if (r === 'impressum') return show(renderImpressum());
    if (r === 'datenschutz') return show(renderDatenschutz());
    if (r === 'test' && quiz) return show(quiz.fertig ? renderErgebnis() : renderFrage());
    if (r === 'test') { location.hash = '#/'; return; }
    if (!state.eingangstestFertig) return show(renderWillkommen());
    if (r === 'themen') return show(renderThemen());
    if (r === 'thema') return show(renderThema(arg));
    if (r === 'ueben') return show(renderUeben());
    return show(renderLernstand());
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

  function renderWillkommen() {
    return '<p class="eyebrow">Los geht\'s</p><h1>Willkommen im Lernportal</h1><p class="lead">Hier lernst du die Themen deiner Ausbildung mit Präsentationen, Videos, Tests und Praxisübungen.</p>' +
      '<div class="grid"><div class="kachel a-yel">' + iconHtml('✓') + '<h3>Eingangstest</h3>' +
      '<p>Mach zuerst den Eingangstest. Danach siehst du, welche Themen schon sitzen und was du noch lernen musst.</p>' +
      '<p class="meta">' + anzahlEingang() + ' Fragen · ' + themenNamen.length + ' Themen · ca. 10 Min. · keine Note</p>' +
      '<div class="knoepfe"><button class="primary" data-start="eingang">Eingangstest starten</button></div></div></div>';
  }

  function renderLernstand() {
    const fp = L.fortschritt(state, themenNamen);
    const next = L.nextSteps(state, themenNamen);
    const sitzt = themenNamen.filter(t => L.statusOf(state, t) === 'sitzt').length;
    let h = '<p class="eyebrow">Dein Stand</p><h1>Mein Lernstand</h1>';
    h += '<div class="zweispaltig"><div class="card"><p class="muted" style="margin:0 0 6px">Fortschritt</p><p class="zahl">' + fp + ' %</p><p class="muted">' + sitzt + ' von ' + themenNamen.length + ' Themen sitzen</p><div class="bar"><div style="width:' + fp + '%"></div></div></div>';
    h += '<div class="card a-roy"><p class="muted" style="margin:0 0 6px">Prüfungscheck</p><p>' + anzahlEingang() + ' Fragen quer durch alle Themen. Schwache Themen kommen wieder auf deine Liste.</p><button class="primary" data-start="pruefung">Prüfungscheck starten</button></div></div>';
    h += '<h2>Als Nächstes</h2>';
    h += next.length
      ? '<div class="grid">' + next.map(n => {
          const t = inhalt.themen.find(x => x.name === n.thema);
          return '<div class="kachel a-' + bereichFarbe(t.bereich) + '">' + themaIcon(t) + '<h3>' + esc(t.name) + '</h3><p>' + esc(n.text) + '</p><p class="meta">' + badge(L.statusOf(state, t.name)) + '</p>' +
            '<div class="knoepfe"><a class="btn primary" href="' + themaLink(t.name) + '">Thema öffnen</a></div></div>';
        }).join('') + '</div>'
      : '<div class="card"><p style="margin:0">Alles sitzt. Mach ab und zu den Prüfungscheck, damit es so bleibt.</p></div>';
    h += '<p style="margin-top:24px">' + (resetFrage
      ? '<span class="muted">Wirklich alles löschen? </span><button class="link" data-reset="ja">Ja, löschen</button><button class="link" data-reset="nein">Abbrechen</button>'
      : '<button class="link" data-reset="frage">Lernstand zurücksetzen</button>') + '</p>';
    return h;
  }

  function sternKnopf(t) {
    const on = state.sterne.includes(t);
    return '<button class="star' + (on ? ' on' : '') + '" data-stern="' + esc(t) + '" aria-label="' + (on ? 'Merken aufheben' : 'Merken') + '">' + (on ? '★' : '☆') + '</button>';
  }

  function renderThemen() {
    const bereiche = [];
    inhalt.themen.forEach(t => { if (!bereiche.includes(t.bereich)) bereiche.push(t.bereich); });
    return '<p class="eyebrow">Alle Themen</p><h1>Themen</h1><p class="lead">Tippe auf ein Thema für Präsentation, Erklärung und Kurztest. Mit dem Stern merkst du dir Themen.</p>' +
      bereiche.map(b => '<div class="abschnitt"><h2>' + esc(b) + '</h2></div><div class="grid">' +
        inhalt.themen.filter(t => t.bereich === b).map(t => {
          const np = (t.praesentationen || []).length, nf = anzahlFragen(t.name);
          const meta = [np ? plural(np, 'Präsentation', 'Präsentationen') : '', nf ? plural(nf, 'Testfrage', 'Testfragen') : ''].filter(Boolean).join(' · ');
          return '<div class="kachel a-' + bereichFarbe(b) + '"><div class="kachel-kopf">' + themaIcon(t) + sternKnopf(t.name) + '</div>' +
            '<h3><a class="decklink" href="' + themaLink(t.name) + '">' + esc(t.name) + '</a></h3>' +
            (t.erklaerung ? '<p>' + esc(kurz(t.erklaerung, 130)) + '</p>' : '') +
            '<p class="meta">' + badge(L.statusOf(state, t.name)) + (meta ? ' &nbsp;' + meta : '') + '</p>' +
            '<div class="knoepfe"><a class="btn primary" href="' + themaLink(t.name) + '">Thema öffnen</a></div></div>';
        }).join('') + '</div>').join('');
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
    const farbe = bereichFarbe(t.bereich);
    const anzahl = anzahlFragen(t.name);
    let h = '<p class="eyebrow"><a href="#/themen" style="color:inherit;text-decoration:none">Themen</a> · ' + esc(t.bereich) + '</p>';
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
    if (t.erklaerung) h += '<div class="card text"><h3 style="margin-top:0">Kurz erklärt</h3>' + absaetze(t.erklaerung) + '</div>';
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
      '<div><div class="kachel a-yel" style="margin-bottom:16px">' + iconHtml('✓') + '<h3>Prüfungscheck</h3><p>' + anzahlEingang() + ' Fragen quer durch alle Themen.</p><div class="knoepfe"><button class="primary" data-start="pruefung">Prüfungscheck starten</button></div></div>' +
      '<div class="kachel a-tea">' + iconHtml('V') + '<h3>Multimeter-Übung</h3><p>Messen und Fehlersuche am Stromkreis.</p><div class="knoepfe"><a class="btn primary" href="multimeter.html">Übung öffnen</a></div></div></div></div>';
  }

  function anbieter() {
    const e = inhalt.einstellungen;
    const feld = k => e[k] ? esc(e[k]) : '<span class="muted">[in der Excel-Datei unter „Einstellungen“ eintragen]</span>';
    const tel = e['Impressum Telefon (freiwillig)'] ? '<br>Telefon: ' + esc(e['Impressum Telefon (freiwillig)']) : '';
    return '<p>' + feld('Impressum Name') + '<br>' + feld('Impressum Anschrift').replace(/\n/g, '<br>') + '<br>E-Mail: ' + feld('Impressum E-Mail') + tel + '</p>';
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

  function starte(art, thema) {
    let liste = [];
    if (art === 'eingang' || art === 'pruefung') liste = T.pickEingang(inhalt.fragen, 18);
    if (art === 'kurz') liste = T.pickKurz(inhalt.fragen, thema, 5);
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
    const titel = { eingang: 'Eingangstest', pruefung: 'Prüfungscheck', kurz: 'Kurztest: ' + quiz.thema, uebung: 'Übungstest' }[quiz.art];
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
    return h + '<button class="primary full" data-fertig="1">Zum Lernstand</button>';
  }

  app.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    const d = b.dataset;
    if (d.start) starte(d.start);
    else if (d.kurz) starte('kurz', d.kurz);
    else if (d.stern) { state = L.toggleStern(state, d.stern); save(); render(); }
    else if (d.video) { videoAn[d.video] = true; render(); }
    else if (d.nurvideo) zeigeVideo(d.nurvideo);
    else if (d.antwort !== undefined && quiz && !quiz.geprueft) { quiz.auswahl = +d.antwort; quiz.fehler = ''; render(); }
    else if (d.pruefen) {
      if (quiz.auswahl === null) { quiz.fehler = 'Wähle zuerst eine Antwort aus.'; render(); return; }
      quiz.antworten[quiz.i] = quiz.auswahl; quiz.geprueft = true; render();
    } else if (d.weiter) {
      if (quiz.i + 1 < quiz.liste.length) { quiz.i++; quiz.auswahl = null; quiz.geprueft = false; render(); window.scrollTo(0, 0); }
      else beende();
    } else if (d.abbrechen) { const z = quiz.zurueck; quiz = null; location.hash = z === '#/test' ? '#/' : z; }
    else if (d.fertig) { quiz = null; location.hash = '#/'; }
    else if (d.reset === 'frage') { resetFrage = true; render(); }
    else if (d.reset === 'ja') { state = L.initialState(); save(); resetFrage = false; render(); }
    else if (d.reset === 'nein') { resetFrage = false; render(); }
  });

  window.addEventListener('hashchange', () => {
    if (route().r !== 'test') quiz = null;
    resetFrage = false;
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
      themenNamen = inhalt.themen.map(t => t.name);
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
