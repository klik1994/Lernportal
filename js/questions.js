const Questions = (() => {
  function parseCSV(text) {
    const rows = [];
    let row = [], field = '', inQuotes = false, i = 0;
    text = String(text || '').replace(/^﻿/, '');
    while (i < text.length) {
      const c = text[i];
      if (inQuotes) {
        if (c === '"') {
          if (text[i + 1] === '"') { field += '"'; i++; } else inQuotes = false;
        } else field += c;
      } else if (c === '"') inQuotes = true;
      else if (c === ',') { row.push(field); field = ''; }
      else if (c === '\n' || c === '\r') {
        if (c === '\r' && text[i + 1] === '\n') i++;
        row.push(field); rows.push(row); row = []; field = '';
      } else field += c;
      i++;
    }
    if (field !== '' || row.length) { row.push(field); rows.push(row); }
    return rows;
  }

  function rowsToQuestions(rows) {
    const out = [];
    rows.slice(1).forEach((r, idx) => {
      const get = n => (r[n] || '').trim();
      const thema = get(0), frage = get(1);
      if (!thema || !frage) return;
      const alle = [get(2), get(3), get(4), get(5)];
      let letzte = -1;
      alle.forEach((a, k) => { if (a) letzte = k; });
      const antworten = alle.slice(0, letzte + 1);
      if (antworten.length < 2 || antworten.some(a => !a)) return;
      const richtig = 'ABCD'.indexOf(get(6).toUpperCase());
      if (get(6).length !== 1 || richtig < 0 || richtig >= antworten.length) return;
      out.push({ id: 'q' + (idx + 1) + '-' + hash(thema + frage), thema, frage, antworten, richtig, erklaerung: get(7) });
    });
    return out;
  }

  function hash(s) {
    let h = 0;
    for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
    return (h >>> 0).toString(36);
  }

  async function loadQuestions(url, fetchFn, builtin) {
    const fallback = { questions: builtin, quelle: 'eingebaut' };
    if (!url) return fallback;
    try {
      const res = await fetchFn(url);
      if (!res.ok) return fallback;
      const q = rowsToQuestions(parseCSV(await res.text()));
      return q.length ? { questions: q, quelle: 'tabelle' } : fallback;
    } catch (e) {
      return fallback;
    }
  }

  return { parseCSV, rowsToQuestions, loadQuestions };
})();
if (typeof module !== 'undefined') module.exports = Questions;
