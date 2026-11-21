// Lexikon: Fachbegriffe aus dem Excel-Blatt „Lexikon“
const Lexikon = (() => {
  const norm = s => String(s || '').toLocaleLowerCase('de').normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/ß/g, 'ss');

  // Zeilen: Begriff | Bereich | Erklärung | Beispiel | Auch gesucht unter
  function parse(rows) {
    const liste = [];
    (rows || []).slice(1).forEach(r => {
      const begriff = String(r[0] || '').trim();
      const erklaerung = String(r[2] || '').trim();
      if (!begriff || !erklaerung || liste.some(x => norm(x.begriff) === norm(begriff))) return;
      const alias = String(r[4] || '').split(/[,;\n]/).map(x => x.trim()).filter(x => x && norm(x) !== norm(begriff));
      liste.push({ begriff, bereich: String(r[1] || '').trim() || 'Weitere Begriffe', erklaerung, beispiel: String(r[3] || '').trim(), alias });
    });
    return liste.sort((a, b) => a.begriff.localeCompare(b.begriff, 'de', { sensitivity: 'base' }));
  }

  // Anfangsbuchstabe für die A–Z-Leiste (Ä→A, Zahlen und Zeichen → #)
  function buchstabe(begriff) {
    const c = norm(begriff).charAt(0).toUpperCase();
    return /[A-Z]/.test(c) ? c : '#';
  }

  // Treffer zuerst im Begriff, dann in Abkürzungen, dann im Text
  function suche(liste, q) {
    const s = norm(q).trim();
    if (!s) return liste.slice();
    const rang = e => {
      const b = norm(e.begriff);
      if (b === s || e.alias.some(a => norm(a) === s)) return 0;
      if (b.startsWith(s)) return 1;
      if (b.includes(s) || e.alias.some(a => norm(a).includes(s))) return 2;
      if (norm(e.erklaerung + ' ' + e.beispiel).includes(s)) return 3;
      return 9;
    };
    return liste.map(e => [rang(e), e]).filter(x => x[0] < 9).sort((a, b) => a[0] - b[0]).map(x => x[1]);
  }

  function finde(liste, wort) {
    const s = norm(wort);
    return liste.find(e => norm(e.begriff) === s) || liste.find(e => e.alias.some(a => norm(a) === s)) || null;
  }

  // Zerlegt einen Text in Stücke: {text} oder {text, begriff}. Jeder Begriff wird höchstens einmal markiert
  // (schon = Set mit bereits markierten Begriffen, damit es über mehrere Absätze gilt).
  // Nur ganze Wörter: Buchstaben, Ziffern und Bindestrich davor/danach verhindern einen Treffer.
  function markiere(text, liste, schon) {
    const s = String(text || '');
    const gesehen = schon || new Set();
    const woerter = [];
    liste.forEach(e => [e.begriff].concat(e.alias).forEach(w => { if (w.length >= 2) woerter.push({ w, e }); }));
    woerter.sort((a, b) => b.w.length - a.w.length);
    if (!woerter.length || !s) return [{ text: s }];
    const esc = w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const re = new RegExp('(?<![\\p{L}\\p{N}\\-])(' + woerter.map(x => esc(x.w)).join('|') + ')(?![\\p{L}\\p{N}\\-])', 'giu');
    const teile = [];
    let pos = 0, m;
    while ((m = re.exec(s))) {
      const t = woerter.find(x => x.w.toLocaleLowerCase('de') === m[1].toLocaleLowerCase('de'));
      // Kurze Abkürzungen (bis 3 Zeichen, z. B. „OT“, „AC“) nur in genauer Schreibweise
      if (!t || (t.w.length <= 3 && t.w !== m[1]) || gesehen.has(t.e.begriff)) continue;
      gesehen.add(t.e.begriff);
      if (m.index > pos) teile.push({ text: s.slice(pos, m.index) });
      teile.push({ text: m[1], begriff: t.e.begriff });
      pos = m.index + m[1].length;
    }
    if (pos < s.length) teile.push({ text: s.slice(pos) });
    return teile;
  }

  return { parse, buchstabe, suche, finde, markiere, norm };
})();
if (typeof module !== 'undefined') module.exports = Lexikon;
