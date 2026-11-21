const Inhalte = (() => {
  const Q = typeof Questions !== 'undefined' ? Questions : require('./questions.js');

  function youtubeId(url) {
    const m = String(url || '').match(/(?:youtube(?:-nocookie)?\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/)|youtu\.be\/)([A-Za-z0-9_-]{11})/);
    return m ? m[1] : null;
  }

  function parseInhalte(sheets) {
    const zeilen = sheets.Themen || [];
    const themen = [];
    zeilen.slice(1).forEach(r => {
      const name = (r[0] || '').trim();
      if (!name || themen.some(t => t.name === name)) return;
      themen.push({ name, bereich: (r[1] || '').trim() || 'Weitere Themen', erklaerung: (r[2] || '').trim(), video: youtubeId(r[3]) });
    });
    const fragen = Q.rowsToQuestions(sheets.Fragen || []);
    fragen.forEach(f => {
      if (!themen.some(t => t.name === f.thema)) themen.push({ name: f.thema, bereich: 'Weitere Themen', erklaerung: '', video: null });
    });
    const einstellungen = {};
    (sheets.Einstellungen || []).slice(1).forEach(r => { if (r[0]) einstellungen[r[0].trim()] = (r[1] || '').trim(); });
    return { themen, fragen, einstellungen };
  }

  return { youtubeId, parseInhalte };
})();
if (typeof module !== 'undefined') module.exports = Inhalte;
