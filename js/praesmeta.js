const PraesMeta = (() => {
  const FARBEN = { 't-strom': 'blu', 't-widerstand': 'red', 't-eva': 'pur', 't-sensoren': 'grn', 't-aktoren': 'ora', 't-mm': 'tea', 't-mm2': 'roy', 't-mm3': 'ora', 't-mm4': 'pur', 't-mm5': 'grn', 't-mm6': 'blu', 't-mm7': 'yel', 't-reihe': 'tea', 't-parallel': 'roy', 't-gemischt': 'pur', 't-hv': 'ora', 't-bus': 'tea', 't-bn1': 'yel', 't-bn2': 'roy', 't-bn3': 'grn', 't-bn4': 'ora', 't-bn5': 'pur', 't-fw1': 'tea', 't-fw2': 'red', 't-fw3': 'roy', 't-mw1': 'ora', 't-mw2': 'pur', 't-mw3': 'blu', 't-mw4': 'grn', 't-ku1': 'yel', 't-ku2': 'tea', 't-ku3': 'roy', 't-ku4': 'red' };
  const ohneTags = s => s.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();

  function parseMeta(html) {
    const titelFolie = (html.match(/<section class="slide title-slide"[^>]*>([\s\S]*?)<\/section>/) || [])[1] || '';
    const symbol = ohneTags((titelFolie.match(/<div class="symbol[^"]*"[^>]*>([\s\S]*?)<\/div>/) || [])[1] || '');
    const titel = ohneTags((titelFolie.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [])[1] || '');
    const untertitel = ohneTags((titelFolie.match(/<\/h1>\s*<p[^>]*>([\s\S]*?)<\/p>/) || [])[1] || '');
    const folien = (html.match(/<section class="slide[\s"]/g) || []).length;
    const fragen = (html.match(/class="q"/g) || []).length;
    const body = (html.match(/<body class="([^"]*)"/) || [])[1] || '';
    const farbe = FARBEN[body.split(/\s+/).find(c => FARBEN[c])] || 'yel';
    return { symbol, titel, untertitel, folien, fragen, farbe };
  }

  function videoPfad(link) {
    const m = String(link || '').match(/^(praesentationen\/)([\w-]+)\.html$/);
    return m ? m[1] + 'videos/' + m[2] + '.mp4' : null;
  }

  return { parseMeta, videoPfad };
})();
if (typeof module !== 'undefined') module.exports = PraesMeta;
