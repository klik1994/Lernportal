const Inhalte = (() => {
  const Q = typeof Questions !== 'undefined' ? Questions : require('./questions.js');

  function youtubeId(url) {
    const m = String(url || '').match(/(?:youtube(?:-nocookie)?\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/)|youtu\.be\/)([A-Za-z0-9_-]{11})/);
    return m ? m[1] : null;
  }

  // Erlaubt nur https-Links oder Pfade im eigenen Portal (z. B. praesentationen/spannung.html)
  function sichererLink(url) {
    const u = String(url || '').trim();
    if (/^https:\/\/[^\s"'<>]+$/i.test(u)) return u;
    if (/^[A-Za-z0-9_\-./%#]+$/.test(u) && !u.startsWith('//') && !u.includes('..')) return u;
    return null;
  }

  // Eigene Videodatei im Portal (z. B. videos/mein-video.mp4)
  function videoDatei(url) {
    const u = sichererLink(url);
    return u && /\.(mp4|webm|m4v)(\?.*)?$/i.test(u) ? u : null;
  }

  // Eine Präsentation pro Zeile: "Titel | Link" oder nur "Link"
  function parsePraesentationen(text) {
    return String(text || '').split(/\n+/).map(z => z.trim()).filter(Boolean).map(z => {
      const teile = z.split('|');
      const link = sichererLink(teile.length > 1 ? teile.slice(1).join('|') : teile[0]);
      if (!link) return null;
      const titel = teile.length > 1 && teile[0].trim() ? teile[0].trim()
        : decodeURIComponent(link.split('/').pop().replace(/\.html?$/i, '').replace(/[-_]/g, ' '));
      return { titel, link };
    }).filter(Boolean);
  }

  function parseInhalte(sheets) {
    const zeilen = sheets.Themen || [];
    const themen = [];
    zeilen.slice(1).forEach(r => {
      const name = (r[0] || '').trim();
      if (!name || themen.some(t => t.name === name)) return;
      themen.push({ name, bereich: (r[1] || '').trim() || 'Weitere Themen', erklaerung: (r[2] || '').trim(), video: youtubeId(r[3]), videoDatei: videoDatei(r[3]), praesentationen: parsePraesentationen(r[4]) });
    });
    const fragen = Q.rowsToQuestions(sheets.Fragen || []);
    fragen.forEach(f => {
      if (!themen.some(t => t.name === f.thema)) themen.push({ name: f.thema, bereich: 'Weitere Themen', erklaerung: '', video: null, videoDatei: null, praesentationen: [] });
    });
    const einstellungen = {};
    (sheets.Einstellungen || []).slice(1).forEach(r => { if (r[0]) einstellungen[r[0].trim()] = (r[1] || '').trim(); });
    return { themen, fragen, einstellungen };
  }

  return { youtubeId, sichererLink, videoDatei, parsePraesentationen, parseInhalte };
})();
if (typeof module !== 'undefined') module.exports = Inhalte;
