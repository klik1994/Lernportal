(function () {
  const L = Lernstand, T = Tests;
  const app = document.getElementById('app');
  const DATEI = 'inhalte/Lernportal-Inhalte.xlsx';
  let storage = null;
  try { storage = window.localStorage; } catch (e) { storage = null; }
  const store = L.createStore(storage);
  let state = store.load();
  let inhalt = null, themenNamen = [];
  let quiz = null, resetFrage = false, videoAn = {};

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

  function renderWillkommen() {
    return '<h1>Willkommen!</h1><div class="card"><p>Mach zuerst den <b>Eingangstest</b>. Er dauert etwa 10 Minuten. Danach siehst du, welche Themen schon sitzen und was du noch lernen musst.</p>' +
      '<p class="muted">' + anzahlEingang() + ' Fragen aus ' + themenNamen.length + ' Themen. Keine Note, nur für dich.</p>' +
      '<button class="primary full" data-start="eingang">Eingangstest starten</button></div>';
  }

  function renderLernstand() {
    const fp = L.fortschritt(state, themenNamen);
    const next = L.nextSteps(state, themenNamen);
    let h = '<h1>Mein Lernstand</h1><div class="card"><p style="margin:0 0 6px"><b>' + fp + ' %</b> der Themen sitzen</p><div class="bar"><div style="width:' + fp + '%"></div></div></div>';
    h += '<h2>Als Nächstes</h2><div class="card">';
    h += next.length
      ? next.map(n => '<div class="row"><a class="t" href="' + themaLink(n.thema) + '">' + esc(n.text) + '</a><a class="btn" href="' + themaLink(n.thema) + '">Öffnen</a></div>').join('')
      : '<p style="margin:0">Alles sitzt. Mach ab und zu den Prüfungscheck, damit es so bleibt.</p>';
    h += '</div><h2>Prüfungscheck</h2><div class="card"><p class="muted">' + anzahlEingang() + ' Fragen quer durch alle Themen. Schwache Themen kommen wieder auf deine Liste.</p>';
    h += '<button class="primary full" data-start="pruefung">Prüfungscheck starten</button></div>';
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
    return '<h1>Themen</h1>' + bereiche.map(b => '<div class="bereich">' + esc(b) + '</div><div class="card">' +
      inhalt.themen.filter(t => t.bereich === b).map(t =>
        '<div class="row">' + sternKnopf(t.name) + '<a class="t" href="' + themaLink(t.name) + '">' + esc(t.name) + '<br>' + badge(L.statusOf(state, t.name)) + '</a></div>').join('') +
      '</div>').join('');
  }

  function renderThema(name) {
    const t = inhalt.themen.find(x => x.name === name);
    if (!t) return '<h1>Thema nicht gefunden</h1><p><a href="#/themen">Zur Themenliste</a></p>';
    const anzahl = inhalt.fragen.filter(f => f.thema === t.name).length;
    let h = '<p class="muted"><a href="#/themen">Themen</a> · ' + esc(t.bereich) + '</p>';
    h += '<div style="display:flex;align-items:center;gap:6px"><h1 style="flex:1;margin:0">' + esc(t.name) + '</h1>' + sternKnopf(t.name) + '</div>';
    h += '<p>' + badge(L.statusOf(state, t.name)) + '</p>';
    if (t.praesentationen && t.praesentationen.length) {
      h += '<div class="card"><p style="margin:0 0 8px"><b>Präsentation' + (t.praesentationen.length > 1 ? 'en' : '') + '</b></p><p class="muted">Mit Animationen, Lernvideo und Kurztest. Tippen oder wischen zum Weiterblättern.</p><div class="liste">' +
        t.praesentationen.map(p => '<a class="btn full" href="' + esc(p.link) + '">▶ ' + esc(p.titel) + '</a>').join('') + '</div></div>';
    }
    if (t.videoDatei) h += '<div class="video"><video src="' + esc(t.videoDatei) + '" controls preload="metadata" playsinline></video></div>';
    if (t.video) {
      h += videoAn[t.video]
        ? '<div class="video"><iframe src="https://www.youtube-nocookie.com/embed/' + t.video + '?autoplay=1" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="Video"></iframe></div>'
        : '<div class="card"><p class="muted">Beim Abspielen wird das Video von YouTube geladen.</p><button class="full" data-video="' + t.video + '">▶ Video abspielen</button></div>';
    }
    if (t.erklaerung) h += '<div class="card text">' + absaetze(t.erklaerung) + '</div>';
    h += '<div class="card"><p style="margin:0 0 8px"><b>Kurztest</b></p>';
    h += anzahl
      ? '<p class="muted">' + Math.min(5, anzahl) + ' Fragen. Ab 80 % sitzt das Thema.</p><button class="primary full" data-kurz="' + esc(t.name) + '">Kurztest starten</button>'
      : '<p class="muted" style="margin:0">Zu diesem Thema gibt es noch keine Fragen.</p>';
    return h + '</div>';
  }

  function renderUeben() {
    return '<h1>Üben</h1><div class="card"><p><b>Eigener Übungstest</b><br><span class="muted">Wähle die Themen, die du üben willst.</span></p>' +
      themenNamen.map((t, i) => '<label class="check"><input type="checkbox" data-wahl="' + i + '"> ' + esc(t) + '</label>').join('') +
      '<div class="err" id="err"></div><button class="primary full" data-start="uebung">Übungstest starten (bis zu 10 Fragen)</button></div>' +
      '<div class="card"><p><b>Prüfungscheck</b><br><span class="muted">' + anzahlEingang() + ' Fragen quer durch alle Themen.</span></p><button class="full" data-start="pruefung">Prüfungscheck starten</button></div>' +
      '<div class="card"><p><b>Praxis</b><br><span class="muted">Messen und Fehlersuche am Stromkreis.</span></p><a class="btn full" href="multimeter.html">Multimeter-Übung öffnen</a></div>';
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
    h += '<div class="bar" style="margin-bottom:16px"><div style="width:' + Math.round((quiz.i / quiz.liste.length) * 100) + '%;background:#1a5fb4"></div></div>';
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
      return '<div class="row"><a class="t" href="' + themaLink(t) + '">' + esc(t) + '<div class="bar" style="margin-top:4px"><div style="width:' + p + '%;background:' + (p >= L.GRENZE ? '#2e7d32' : '#c62828') + '"></div></div></a><span>' + p + ' %</span>' + badge(L.statusOf(state, t)) + '</div>';
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
    } catch (err) {
      app.innerHTML = '<div class="hint">Die Inhalte konnten nicht geladen werden. Prüfe deine Internetverbindung.</div><button class="primary" id="nochmal">Nochmal versuchen</button>';
      document.getElementById('nochmal').onclick = laden;
    }
  }
  laden();
})();
