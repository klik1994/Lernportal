const Xlsx = (() => {
  const dec = new TextDecoder('utf-8');

  async function inflate(bytes) {
    const ds = new DecompressionStream('deflate-raw');
    const stream = new Blob([bytes]).stream().pipeThrough(ds);
    return new Uint8Array(await new Response(stream).arrayBuffer());
  }

  async function unzip(buffer) {
    const b = new Uint8Array(buffer);
    const dv = new DataView(buffer);
    let eocd = -1;
    for (let i = b.length - 22; i >= Math.max(0, b.length - 65557); i--) {
      if (dv.getUint32(i, true) === 0x06054b50) { eocd = i; break; }
    }
    if (eocd < 0) throw new Error('Keine gültige Excel-Datei');
    const anzahl = dv.getUint16(eocd + 10, true);
    let p = dv.getUint32(eocd + 16, true);
    const dateien = {};
    for (let n = 0; n < anzahl; n++) {
      if (dv.getUint32(p, true) !== 0x02014b50) throw new Error('Excel-Datei beschädigt');
      const methode = dv.getUint16(p + 10, true);
      const groesse = dv.getUint32(p + 20, true);
      const nameLen = dv.getUint16(p + 28, true), extraLen = dv.getUint16(p + 30, true), kommLen = dv.getUint16(p + 32, true);
      const offset = dv.getUint32(p + 42, true);
      const name = dec.decode(b.subarray(p + 46, p + 46 + nameLen));
      const lNameLen = dv.getUint16(offset + 26, true), lExtraLen = dv.getUint16(offset + 28, true);
      const start = offset + 30 + lNameLen + lExtraLen;
      dateien[name] = { methode, daten: b.subarray(start, start + groesse) };
      p += 46 + nameLen + extraLen + kommLen;
    }
    return {
      async text(name) {
        const f = dateien[name];
        if (!f) return null;
        return dec.decode(f.methode === 0 ? f.daten : await inflate(f.daten));
      }
    };
  }

  const entity = s => s.replace(/&(#x[0-9a-f]+|#\d+|amp|lt|gt|quot|apos);/gi, (m, e) => {
    if (e[0] === '#') return String.fromCodePoint(e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10));
    return { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" }[e.toLowerCase()];
  });
  const attr = (tag, name) => { const m = tag.match(new RegExp('\\s' + name + '="([^"]*)"')); return m ? entity(m[1]) : null; };
  const texte = xml => { let s = ''; xml.replace(/<t(?:\s[^>]*)?>([\s\S]*?)<\/t>/g, (m, t) => { s += entity(t); }); return s; };
  const spalte = ref => { let n = 0; for (const ch of ref.replace(/\d+/g, '')) n = n * 26 + ch.charCodeAt(0) - 64; return n - 1; };

  async function readXlsx(buffer) {
    const zip = await unzip(buffer);
    const wb = await zip.text('xl/workbook.xml');
    if (!wb) throw new Error('Keine gültige Excel-Datei');
    const rels = (await zip.text('xl/_rels/workbook.xml.rels')) || '';
    const ziel = {};
    rels.replace(/<Relationship\b[^>]*>/g, tag => { ziel[attr(tag, 'Id')] = attr(tag, 'Target'); });
    const shared = [];
    const ss = await zip.text('xl/sharedStrings.xml');
    if (ss) ss.replace(/<si>([\s\S]*?)<\/si>/g, (m, inner) => { shared.push(texte(inner)); });
    const ergebnis = {};
    const blaetter = [];
    wb.replace(/<sheet\b[^>]*>/g, tag => { blaetter.push({ name: attr(tag, 'name'), rid: attr(tag, 'r:id') }); });
    for (const bl of blaetter) {
      let t = ziel[bl.rid] || '';
      t = t.startsWith('/') ? t.slice(1) : 'xl/' + t.replace(/^\.\//, '');
      const xml = (await zip.text(t)) || '';
      const zeilen = [];
      xml.replace(/<row\b([^>]*)>([\s\S]*?)<\/row>/g, (m, rowAttr, inner) => {
        const nr = parseInt(attr('<x ' + rowAttr, 'r'), 10) - 1;
        const zeile = [];
        inner.replace(/<c\b([^>]*?)(?:\/>|>([\s\S]*?)<\/c>)/g, (m2, cAttr, cInner) => {
          const tag = '<c ' + cAttr;
          const typ = attr(tag, 't');
          const ref = attr(tag, 'r');
          let wert = '';
          cInner = cInner || '';
          if (typ === 'inlineStr') wert = texte(cInner);
          else {
            const v = cInner.match(/<v>([\s\S]*?)<\/v>/);
            if (v) wert = typ === 's' ? (shared[parseInt(v[1], 10)] || '') : entity(v[1]);
          }
          const idx = ref ? spalte(ref) : zeile.length;
          while (zeile.length < idx) zeile.push('');
          zeile[idx] = wert;
        });
        while (zeile.length && zeile[zeile.length - 1] === '') zeile.pop();
        zeilen[nr] = zeile;
      });
      for (let i = 0; i < zeilen.length; i++) if (!zeilen[i]) zeilen[i] = [];
      ergebnis[bl.name] = zeilen;
    }
    return ergebnis;
  }

  return { readXlsx };
})();
if (typeof module !== 'undefined') module.exports = Xlsx;
