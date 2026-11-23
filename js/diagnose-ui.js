(function () {
  const D = Diagnose, PL = DiagnosePlan;
  const root = document.getElementById('diagnose');
  const RING = ['vorne', 'links', 'hinten', 'rechts'];
  const TITEL = { vorne: 'Fahrzeug von vorne', links: 'Fahrerseite', hinten: 'Fahrzeug von hinten', rechts: 'Beifahrerseite', innen: 'Fahrerplatz', fussraum: 'Fußraum Fahrerseite', sk: 'Sicherungskasten Innenraum', tuer: 'Fahrertür innen (Verkleidung ab)', motorraum: 'Motorraum', box: 'Sicherungs- und Relaisbox Motorraum', rlL: 'Rückleuchte links (ausgebaut)', rlR: 'Rückleuchte rechts (ausgebaut)' };
  const ZURUECK = { innen: 'links', fussraum: 'innen', sk: 'innen', tuer: 'innen', motorraum: 'vorne', box: 'motorraum', rlL: 'hinten', rlR: 'hinten' };
  const PUNKTNAME = {
    'B+': 'Batterie Plus', M: 'Masse (Batterie Minus)', M1: 'Massepunkt M1', M2: 'Massepunkt M2', M3: 'Massepunkt M3', M5: 'Massepunkt M5'
  };

  let st, ansicht, meta, werkzeug, mm, auswahl, meldung, tester, planSys, messungen, antwort, ergebnis, stapel = [], letzter = null;

  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const komma = (x, d) => (Math.abs(x) < 0.005 ? 0 : x).toFixed(d).replace('.', ',');
  const btn = (attr, wert, text, aktiv, cls) => '<button data-' + attr + '="' + wert + '" class="' + (aktiv ? 'on ' : '') + (cls || '') + '">' + text + '</button>';

  function naechsterFall() {
    if (!stapel.length) {
      stapel = D.FAELLE.map(f => f.id);
      for (let i = stapel.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [stapel[i], stapel[j]] = [stapel[j], stapel[i]]; }
      if (stapel[0] === letzter && stapel.length > 1) stapel.push(stapel.shift());
    }
    return (letzter = stapel.shift());
  }
  function neuerAuftrag(id) {
    st = D.neu(id || naechsterFall());
    ansicht = 'vorne'; meta = { tuer: false, haubeFrei: false, haube: false, lampen: {}, gezogen: {} };
    werkzeug = null; mm = { modus: 'V', rot: null, schwarz: null, naechste: 'rot' }; auswahl = null; meldung = '';
    tester = { verbunden: false, sg: null, seite: null }; planSys = 'Licht'; messungen = 0; antwort = { ort: null, art: null, offen: false, fehler: '' }; ergebnis = null;
  }

  const punktName = k => {
    if (PUNKTNAME[k]) return PUNKTNAME[k];
    const [teil, pin] = k.split('.');
    const stern = pin && pin.endsWith('*');
    const p = (pin || '').replace('*', '');
    if (/^X\d+/.test(teil)) return 'Stecker ' + teil + ' Pin ' + p + (stern ? ' (Bauteilseite)' : ' (Leitungsseite)');
    if (/^F\d+/.test(teil)) return 'Sicherung ' + teil + ' Ausgang';
    if (teil === 'A10') return 'Bordnetz-SG A10 Pin ' + p;
    if (teil === 'A20') return 'Türsteuergerät A20 Pin ' + p;
    if (teil === 'K7') return 'Relaissockel K7 Klemme ' + p;
    return k;
  };

  // ---------- Zeichnungen ----------
  const glanz = (x, y, rx, ry, h, farbe) => h > 0.05 ? '<ellipse cx="' + x + '" cy="' + y + '" rx="' + (rx * 1.8) + '" ry="' + (ry * 2.2) + '" fill="' + farbe + '" opacity="' + Math.min(0.55, h * 0.5).toFixed(2) + '" filter="url(#weich)"/>' : '';
  const DEFS = '<defs><filter id="weich" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>' +
    '<linearGradient id="lack" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9eef5"/><stop offset="1" stop-color="#aeb9c8"/></linearGradient>' +
    '<linearGradient id="glas" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5d7fa8"/><stop offset="1" stop-color="#1e2f47"/></linearGradient></defs>';
  const HG = '<rect width="360" height="230" fill="#141f30"/><rect y="200" width="360" height="30" fill="#0d1624"/>';
  const blinkKlasse = (an, schnell) => an ? ' class="' + (schnell ? 'blink-s' : 'blink') + '"' : ' opacity="0.25"';

  const sicherungSvg = (f, x, y, c) => meta.gezogen[f] ? '<rect x="' + (x - 9) + '" y="' + (y - 9) + '" width="18" height="18" rx="2" fill="#0a0f18" stroke="#5a6d88" stroke-dasharray="2 2"/>' :
    '<rect x="' + (x - 9) + '" y="' + (y - 10) + '" width="18" height="20" rx="3" fill="' + c + '"/><rect x="' + (x - 6) + '" y="' + (y + 4) + '" width="12" height="4" fill="rgba(0,0,0,.25)"/>';
  function zeichne(b) {
    const fp = st.fensterPos;
    switch (ansicht) {
      case 'vorne': return HG +
        '<rect x="62" y="178" width="34" height="26" rx="5" fill="#0a0f18"/><rect x="264" y="178" width="34" height="26" rx="5" fill="#0a0f18"/>' +
        '<path d="M100 104 L128 46 Q180 36 232 46 L260 104 Z" fill="url(#lack)"/><path d="M112 100 L134 54 Q180 46 226 54 L248 100 Z" fill="url(#glas)"/>' +
        '<path d="M44 132 Q50 106 100 102 L260 102 Q310 106 316 132 L320 182 Q180 192 40 182 Z" fill="url(#lack)"/>' +
        '<path d="M70 104 L290 104 L306 124 L54 124 Z" fill="#dfe6ef" stroke="#9aa7b8" stroke-width="1"/>' +
        '<rect x="150" y="142" width="60" height="22" rx="6" fill="#26303e"/><rect x="152" y="168" width="56" height="12" rx="2" fill="#f4f6f9" stroke="#9aa7b8"/>' +
        '<ellipse cx="96" cy="138" rx="30" ry="11" fill="#cfd8e3" stroke="#6f7c8d" stroke-width="2"/><ellipse cx="264" cy="138" rx="30" ry="11" fill="#cfd8e3" stroke="#6f7c8d" stroke-width="2"/>' +
        glanz(96, 138, 30, 11, b.abr, '#fff7c2') + glanz(264, 138, 30, 11, b.abl, '#fff7c2') +
        '<ellipse cx="96" cy="138" rx="14" ry="6" fill="' + (b.abr > 0.05 ? '#fffbe0' : '#e7edf4') + '"/><ellipse cx="264" cy="138" rx="14" ry="6" fill="' + (b.abl > 0.05 ? '#fffbe0' : '#e7edf4') + '"/>' +
        '<rect x="50" y="132" width="14" height="10" rx="3" fill="#ffa21f"' + blinkKlasse(b.blvr > 0.3, b.schnellR) + '/><rect x="296" y="132" width="14" height="10" rx="3" fill="#ffa21f"' + blinkKlasse(b.blvl > 0.3, b.schnellL) + '/>';
      case 'hinten': return HG +
        '<rect x="62" y="178" width="34" height="26" rx="5" fill="#0a0f18"/><rect x="264" y="178" width="34" height="26" rx="5" fill="#0a0f18"/>' +
        '<path d="M104 104 L130 50 Q180 42 230 50 L256 104 Z" fill="url(#lack)"/><path d="M116 98 L136 58 Q180 52 224 58 L244 98 Z" fill="url(#glas)"/>' +
        '<path d="M44 128 Q50 106 104 102 L256 102 Q310 106 316 128 L320 182 Q180 192 40 182 Z" fill="url(#lack)"/>' +
        '<rect x="148" y="146" width="64" height="14" rx="2" fill="#f4f6f9" stroke="#9aa7b8"/>' +
        '<rect x="54" y="116" width="62" height="30" rx="6" fill="#3a1414" stroke="#6f7c8d"/><rect x="244" y="116" width="62" height="30" rx="6" fill="#3a1414" stroke="#6f7c8d"/>' +
        '<rect x="58" y="120" width="26" height="22" rx="3" fill="#ffa21f"' + blinkKlasse(b.blhl > 0.3, b.schnellL) + '/><rect x="276" y="120" width="26" height="22" rx="3" fill="#ffa21f"' + blinkKlasse(b.blhr > 0.3, b.schnellR) + '/>' +
        '<rect x="88" y="120" width="24" height="22" rx="3" fill="' + (b.brl > 0.3 ? '#ff2b2b' : '#6a1d1d') + '"/><rect x="248" y="120" width="24" height="22" rx="3" fill="' + (b.brr > 0.3 ? '#ff2b2b' : '#6a1d1d') + '"/>' +
        glanz(100, 131, 14, 10, b.brl, '#ff3030') + glanz(260, 131, 14, 10, b.brr, '#ff3030');
      case 'links': case 'rechts': {
        const sp = ansicht === 'rechts';
        const g = sp ? ' transform="translate(360 0) scale(-1 1)"' : '';
        const glasUnten = 150, glasOben = 104, glasY = glasOben + (glasUnten - glasOben) * fp / 100;
        let s = HG + '<g' + g + '>';
        s += '<path d="M24 170 Q22 140 60 132 L104 128 L150 92 Q196 80 262 88 L300 126 Q336 132 338 168 L336 182 L24 182 Z" fill="url(#lack)"/>';
        s += '<path d="M160 98 L216 92 L216 128 L120 130 Z" fill="#1e2f47"/><path d="M222 92 Q258 92 284 126 L222 128 Z" fill="url(#glas)"/>';
        if (!sp) s += '<path d="M160 98 L216 92 L216 128 L120 130 Z" fill="none"/><clipPath id="fc"><path d="M160 98 L216 92 L216 128 L120 130 Z"/></clipPath><rect x="110" y="' + glasY + '" width="110" height="60" fill="url(#glas)" clip-path="url(#fc)"/>';
        else s += '<path d="M160 98 L216 92 L216 128 L120 130 Z" fill="url(#glas)"/>';
        s += '<circle cx="86" cy="182" r="24" fill="#0a0f18"/><circle cx="86" cy="182" r="11" fill="#7d8a9c"/><circle cx="276" cy="182" r="24" fill="#0a0f18"/><circle cx="276" cy="182" r="11" fill="#7d8a9c"/>';
        if (!sp && meta.tuer) s += '<path d="M118 130 L218 128 L218 178 L124 178 Z" fill="#0b121d"/><path d="M118 130 L72 118 L80 174 L124 178 Z" fill="#d5dde8" stroke="#8a97a8"/><text x="168" y="158" text-anchor="middle" font-size="11" fill="#94a4ba">Tür offen</text>';
        else s += '<path d="M118 130 L218 128 L218 178 L124 178" fill="none" stroke="#8a97a8" stroke-width="1.5"/><rect x="190" y="138" width="16" height="5" rx="2" fill="#7d8a9c"/>';
        s += '<path d="M218 128 L218 178" stroke="#8a97a8" stroke-width="1.5"/><path d="M128 110 l-14 4 l2 10 l14 -2z" fill="#9aa7b8"/>';
        return s + '</g>';
      }
      case 'innen': {
        const kl = st.zuendung;
        let s = '<rect width="360" height="230" fill="#0f1826"/><path d="M0 0 H360 V70 Q180 50 0 70 Z" fill="#2c4466" opacity="0.6"/>';
        s += '<path d="M0 82 Q180 62 360 82 L360 170 L0 170 Z" fill="#1d2939"/><rect x="0" y="80" width="30" height="150" fill="#25344a"/>';
        s += '<rect x="96" y="84" width="96" height="34" rx="12" fill="#0a0f18" stroke="#33465f"/>';
        if (kl) s += '<text x="144" y="106" text-anchor="middle" font-size="10" fill="#7fe0a8">ZÜNDUNG EIN</text>';
        const pfeil = (x, dir, an, schnell) => '<path d="M' + x + ' 96 l' + (dir * -8) + ' 5 l' + (dir * 8) + ' 5 z" fill="#34c778"' + (an ? ' class="' + (schnell ? 'blink-s' : 'blink') + '"' : ' opacity="0.15"') + '/>';
        s += pfeil(108, 1, b.blinktL, b.schnellL) + pfeil(180, -1, b.blinktR, b.schnellR);
        if (kl && st.licht === 'abblend') s += '<text x="144" y="94" text-anchor="middle" font-size="9" fill="#5fd27f">≡D</text>';
        s += '<circle cx="144" cy="150" r="50" fill="none" stroke="#3b4b62" stroke-width="12"/><circle cx="144" cy="150" r="18" fill="' + (st.hupe ? '#5b8cff' : '#33465f') + '"/><text x="144" y="154" text-anchor="middle" font-size="9" fill="#cbd5e1">Hupe</text>';
        s += '<rect x="78" y="118" width="30" height="7" rx="3" fill="#4a5c75" transform="rotate(' + ({ links: 12, rechts: -12, aus: 0 }[st.blinker]) + ' 106 121)"/>';
        s += '<circle cx="52" cy="124" r="15" fill="#33465f" stroke="#5a6d88"/><line x1="52" y1="124" x2="' + (st.licht === 'abblend' ? 62 : 52) + '" y2="' + (st.licht === 'abblend' ? 114 : 110) + '" stroke="#f7b612" stroke-width="3"/><text x="52" y="152" text-anchor="middle" font-size="9" fill="#94a4ba">Licht</text>';
        s += '<circle cx="232" cy="122" r="13" fill="' + (kl ? '#34c778' : '#33465f') + '" stroke="#5a6d88"/><text x="232" y="125" text-anchor="middle" font-size="7" fill="#0e192b">START</text><text x="232" y="146" text-anchor="middle" font-size="9" fill="#94a4ba">Zündung</text>';
        s += '<rect x="34" y="160" width="44" height="26" rx="4" fill="#2a3a52" stroke="#5a6d88" stroke-dasharray="3 2"/><text x="56" y="177" text-anchor="middle" font-size="8" fill="#94a4ba">Abdeckung</text>';
        s += '<text x="15" y="110" text-anchor="middle" font-size="8" fill="#94a4ba">Tür-</text><text x="15" y="120" text-anchor="middle" font-size="8" fill="#94a4ba">verkl.</text>';
        s += '<rect x="6" y="150" width="18" height="30" rx="3" fill="#33465f"/><text x="15" y="194" text-anchor="middle" font-size="8" fill="#94a4ba">FH</text>';
        s += '<rect x="110" y="200" width="70" height="24" rx="5" fill="#1b2433" stroke="#5a6d88" stroke-dasharray="3 2"/><text x="145" y="216" text-anchor="middle" font-size="9" fill="#94a4ba">Fußraum ▼</text>';
        return s;
      }
      case 'fussraum': return '<rect width="360" height="230" fill="#0f1826"/><rect x="0" y="0" width="360" height="56" fill="#1d2939"/>' +
        '<rect x="96" y="36" width="34" height="16" rx="3" fill="#0a0f18" stroke="#5a6d88"/><text x="113" y="30" text-anchor="middle" font-size="9" fill="#94a4ba">OBD-Buchse</text>' +
        '<path d="M206 56 L206 150" stroke="#4a5c75" stroke-width="8"/><rect x="186" y="' + (st.bremse ? 158 : 148) + '" width="44" height="22" rx="5" fill="#5a6d88"/><text x="208" y="200" text-anchor="middle" font-size="9" fill="#94a4ba">Bremspedal</text>' +
        '<path d="M290 56 L290 140" stroke="#4a5c75" stroke-width="6"/><rect x="278" y="140" width="26" height="40" rx="4" fill="#4a5c75"/>' +
        '<rect x="214" y="70" width="34" height="18" rx="4" fill="#33465f" stroke="#7d8a9c"/><text x="231" y="66" text-anchor="middle" font-size="9" fill="#94a4ba">S5</text>' +
        '<path d="M40 150 l26 0 l0 12 l-26 0 z" fill="#f7b612"/><text x="53" y="178" text-anchor="middle" font-size="9" fill="#94a4ba">Haubenhebel</text>';
      case 'sk': return '<rect width="360" height="230" fill="#141f30"/>' +
        '<rect x="20" y="20" width="130" height="176" rx="8" fill="#1d2939" stroke="#5a6d88"/><text x="85" y="212" text-anchor="middle" font-size="9" fill="#94a4ba">Sicherungen</text>' +
        '<rect x="180" y="20" width="160" height="150" rx="8" fill="#22314a" stroke="#5a6d88"/><text x="260" y="38" text-anchor="middle" font-size="10" fill="#cbd5e1">A10 Bordnetz-SG</text>' +
        '<rect x="196" y="48" width="128" height="112" rx="4" fill="#111a28"/>' +
        [['F8', 40, '#d8382c'], ['F21', 80, '#f2c230'], ['F22', 120, '#2f6fd6'], ['F30', 160, '#e9e9e9']].map(([f, y, c]) => sicherungSvg(f, 54, y, c)).join('');
      case 'motorraum': return '<rect width="360" height="230" fill="#121b2a"/>' +
        '<rect x="130" y="40" width="100" height="90" rx="10" fill="#2a3446" stroke="#4a5c75"/><text x="180" y="90" text-anchor="middle" font-size="10" fill="#7d8a9c">Motor</text>' +
        '<rect x="30" y="24" width="80" height="54" rx="5" fill="#0a0f18" stroke="#4a5c75"/><text x="70" y="70" text-anchor="middle" font-size="9" fill="#94a4ba">Batterie' + (st.batterie ? '' : ' (abgeklemmt)') + '</text>' +
        '<rect x="252" y="24" width="78" height="54" rx="5" fill="#1d2939" stroke="#5a6d88" stroke-dasharray="3 2"/><text x="291" y="56" text-anchor="middle" font-size="9" fill="#94a4ba">E-Box</text>' +
        '<rect x="246" y="176" width="92" height="34" rx="10" fill="#cfd8e3" opacity="0.85"/><text x="292" y="224" text-anchor="middle" font-size="9" fill="#94a4ba">Scheinwerfer links</text>' +
        '<rect x="22" y="176" width="92" height="34" rx="10" fill="#cfd8e3" opacity="0.85"/><text x="68" y="224" text-anchor="middle" font-size="9" fill="#94a4ba">Scheinwerfer rechts</text>' +
        '<circle cx="180" cy="194" r="14" fill="#2a3446" stroke="#7d8a9c"/><text x="180" y="198" text-anchor="middle" font-size="9" fill="#cbd5e1">H1</text>' +
        '<text x="180" y="20" text-anchor="middle" font-size="9" fill="#5a6d88">▲ Spritzwand</text><text x="180" y="226" text-anchor="middle" font-size="9" fill="#5a6d88">vorne</text>';
      case 'box': return '<rect width="360" height="230" fill="#141f30"/><rect x="30" y="20" width="300" height="190" rx="10" fill="#1d2939" stroke="#5a6d88"/>' +
        '<text x="180" y="40" text-anchor="middle" font-size="10" fill="#cbd5e1">E-Box Motorraum</text>' + sicherungSvg('F15', 90, 101, '#2f6fd6') +
        (st.relais.K7 ? '<rect x="196" y="76" width="64" height="64" rx="4" fill="#0a0f18" stroke="#5a6d88" stroke-dasharray="3 2"/><text x="228" y="160" text-anchor="middle" font-size="9" fill="#94a4ba">Sockel K7 (Relais gezogen)</text>' : '<rect x="196" y="76" width="64" height="64" rx="6" fill="#33465f" stroke="#7d8a9c"/><text x="228" y="112" text-anchor="middle" font-size="12" fill="#cbd5e1">K7</text>');
      case 'tuer': return '<rect width="360" height="230" fill="#141f30"/><path d="M40 30 H330 V210 H52 Z" fill="#2a3446" stroke="#5a6d88"/>' +
        '<path d="M14 60 q14 10 0 20 q14 10 0 20 q14 10 0 20 q14 10 0 20" fill="none" stroke="#7d8a9c" stroke-width="5"/><text x="20" y="160" font-size="8" fill="#94a4ba">Tür-</text><text x="18" y="170" font-size="8" fill="#94a4ba">übergang</text>' +
        '<rect x="70" y="100" width="90" height="46" rx="5" fill="#22314a" stroke="#7d8a9c"/><text x="115" y="96" text-anchor="middle" font-size="9" fill="#cbd5e1">A20 Türsteuergerät</text>' +
        '<circle cx="262" cy="110" r="24" fill="#33465f" stroke="#7d8a9c"/><text x="262" y="114" text-anchor="middle" font-size="11" fill="#cbd5e1">M20</text>' +
        '<rect x="70" y="40" width="250" height="' + (14 + 40 * (100 - fp) / 100) + '" fill="url(#glas)" opacity="0.8"/>';
      case 'rlL': case 'rlR': return '<rect width="360" height="230" fill="#141f30"/><rect x="110" y="40" width="160" height="110" rx="12" fill="#2a3446" stroke="#7d8a9c"/>' +
        '<text x="190" y="34" text-anchor="middle" font-size="9" fill="#94a4ba">Lampenträger</text>' +
        '<circle cx="150" cy="90" r="18" fill="#ffd28a" stroke="#7d8a9c"/><text x="150" y="124" text-anchor="middle" font-size="9" fill="#cbd5e1">Blinker</text>' +
        '<circle cx="230" cy="90" r="18" fill="#ffd0d0" stroke="#7d8a9c"/><text x="230" y="124" text-anchor="middle" font-size="9" fill="#cbd5e1">Bremslicht</text>';
    }
    return '';
  }

  // Hotspots je Ansicht: o = Objekt (Aktion), p = Messpunkt, n = Navigation
  const X = (s, x, y, kab, bau, dy) => {
    const pins = ({ X4: ['1', '2'], X5: ['1', '2'], X6: ['1', '2'], X7: ['1', '2'], X9: ['1', '2'], X12: ['1', '2'], X20: ['1', '2'], X30: ['2', '3', '4'], X31: ['2', '3', '4'] })[s];
    const out = [{ t: 'o', id: 'st:' + s, x: x - 8 - pins.length * 8, y: y - 10, w: 16 + pins.length * 16, h: 20, l: s }];
    pins.forEach((p, i) => {
      const px = x - (pins.length - 1) * 9 + i * 18;
      out.push({ t: 'p', k: s + '.' + p, x: px, y: y + (kab || 22), l: p });
      out.push({ t: 'p', k: s + '.' + p + '*', x: px, y: y - (bau || 22), l: p + '*' });
    });
    return out;
  };
  function hotspots() {
    switch (ansicht) {
      case 'vorne': return [{ t: 'o', id: 'haube', x: 64, y: 100, w: 232, h: 28, l: 'Motorhaube' }];
      case 'hinten': return [{ t: 'o', id: 'rlL', x: 50, y: 112, w: 70, h: 38, l: 'Rückleuchte links' }, { t: 'o', id: 'rlR', x: 240, y: 112, w: 70, h: 38, l: 'Rückleuchte rechts' }];
      case 'links': return [{ t: 'o', id: 'tuer', x: 116, y: 92, w: 104, h: 88, l: meta.tuer ? 'Einsteigen' : 'Fahrertür' }];
      case 'rechts': return [];
      case 'innen': return [
        { t: 'o', id: 'hupe', x: 124, y: 130, w: 40, h: 40, l: '' }, { t: 'o', id: 'licht', x: 34, y: 106, w: 36, h: 52, l: '' },
        { t: 'o', id: 'blinker', x: 74, y: 108, w: 36, h: 22, l: '' }, { t: 'o', id: 'zuendung', x: 214, y: 106, w: 36, h: 46, l: '' },
        { t: 'o', id: 'abdeckung', x: 32, y: 158, w: 48, h: 30, l: '' }, { t: 'o', id: 'fenster', x: 2, y: 146, w: 26, h: 52, l: '' },
        { t: 'o', id: 'verkleidung', x: 0, y: 84, w: 30, h: 58, l: '' }, { t: 'n', id: 'fussraum', x: 108, y: 198, w: 74, h: 28, l: '' }
      ];
      case 'fussraum': return [
        { t: 'o', id: 'obd', x: 92, y: 24, w: 42, h: 32, l: '' }, { t: 'o', id: 'bremse', x: 180, y: 140, w: 56, h: 46, l: '' },
        { t: 'o', id: 'haubenhebel', x: 34, y: 140, w: 40, h: 30, l: '' }
      ].concat(X('X12', 231, 104, 22, 0).filter(h => h.t !== 'p' || !h.k.endsWith('*') || true).map(h => h.t === 'p' && h.k.endsWith('*') ? Object.assign({}, h, { y: 79 + 0, x: h.x + 60 }) : h));
      case 'sk': {
        const out = [];
        [['F8', 40], ['F21', 80], ['F22', 120], ['F30', 160]].forEach(([f, y]) => {
          out.push({ t: 'o', id: 'si:' + f, x: 34, y: y - 12, w: 40, h: 24, l: f });
          out.push({ t: 'p', k: 'B+', x: 94, y, l: 'ein', klein: true });
          out.push({ t: 'p', k: f + '.2', x: 124, y, l: 'aus' });
        });
        const pins = ['T30a', 'T30b', '31', '12', '13', '20', '21', '24', '40'];
        pins.forEach((p, i) => out.push({ t: 'p', k: 'A10.' + p, x: 216 + (i % 3) * 44, y: 70 + Math.floor(i / 3) * 34, l: p }));
        out.push({ t: 'p', k: 'M3', x: 260, y: 196, l: 'M3' });
        return out;
      }
      case 'motorraum': return [
        { t: 'o', id: 'batterie', x: 30, y: 24, w: 80, h: 54, l: '' }, { t: 'p', k: 'B+', x: 44, y: 34, l: '+' }, { t: 'p', k: 'M', x: 96, y: 34, l: '−' },
        { t: 'n', id: 'box', x: 252, y: 24, w: 78, h: 54, l: '' },
        { t: 'p', k: 'M1', x: 330, y: 120, l: 'M1' }, { t: 'p', k: 'M2', x: 30, y: 120, l: 'M2' }
      ].concat(X('X4', 276, 166, 0, 22).map(h => h.t === 'p' && !h.k.endsWith('*') ? Object.assign({}, h, { y: 166 - 28 }) : h))
        .concat(X('X6', 330, 166, 0, 22).map(h => h.t === 'p' && !h.k.endsWith('*') ? Object.assign({}, h, { y: 166 - 28 }) : h))
        .concat(X('X5', 84, 166, 0, 22).map(h => h.t === 'p' && !h.k.endsWith('*') ? Object.assign({}, h, { y: 166 - 28 }) : h))
        .concat(X('X7', 30, 166, 0, 22).map(h => h.t === 'p' && !h.k.endsWith('*') ? Object.assign({}, h, { y: 166 - 28 }) : h))
        .concat(X('X9', 216, 194, 0, 0).map(h => h.t === 'p' ? Object.assign({}, h, { y: h.k.endsWith('*') ? 174 : 214 }) : h))
        .filter(h => !(h.t === 'p' && h.k.endsWith('*') && h.k.startsWith('X') && false));
      case 'box': {
        const out = [{ t: 'o', id: 'si:F15', x: 70, y: 86, w: 40, h: 30, l: 'F15' }, { t: 'p', k: 'B+', x: 90, y: 66, l: 'ein' }, { t: 'p', k: 'F15.2', x: 90, y: 136, l: 'aus' },
          { t: 'o', id: 'relais', x: 196, y: 76, w: 64, h: 64, l: '' }];
        if (st.relais.K7) [['30', 210, 90], ['87', 246, 90], ['86', 210, 126], ['85', 246, 126]].forEach(([p, x, y]) => out.push({ t: 'p', k: 'K7.' + p, x, y, l: p }));
        return out;
      }
      case 'tuer': return [{ t: 'p', k: 'A20.30', x: 84, y: 124, l: '30' }, { t: 'p', k: 'A20.31', x: 106, y: 124, l: '31' }, { t: 'p', k: 'A20.M1', x: 128, y: 124, l: 'M1' }, { t: 'p', k: 'A20.M2', x: 150, y: 124, l: 'M2' }]
        .concat(X('X20', 262, 166, 24, 0).map(h => h.t === 'p' && h.k.endsWith('*') ? Object.assign({}, h, { y: 144 }) : h));
      case 'rlL': case 'rlR': {
        const s = ansicht === 'rlL' ? 'X30' : 'X31', l = ansicht === 'rlL';
        return [{ t: 'o', id: 'gl:' + (l ? 'e-blhl' : 'e-blhr'), x: 130, y: 70, w: 40, h: 40, l: '' }, { t: 'o', id: 'gl:' + (l ? 'e-brl' : 'e-brr'), x: 210, y: 70, w: 40, h: 40, l: '' },
          { t: 'p', k: 'M5', x: 320, y: 200, l: 'M5' }].concat(X(s, 190, 172, 30, 20));
      }
    }
    return [];
  }

  function sichtbar(h) {
    if (h.t !== 'p') return true;
    if (h.k.includes('*')) return D.sternFrei(st, h.k);
    return true;
  }

  function ansichtSvg() {
    const b = D.beobachte(st);
    let s = '<svg class="auto" viewBox="0 0 360 230" role="img" aria-label="' + esc(TITEL[ansicht]) + '">' + DEFS + zeichne(b);
    hotspots().filter(sichtbar).forEach(h => {
      if (h.t === 'p') {
        const rot = mm.rot === h.k, schw = mm.schwarz === h.k;
        s += '<g class="hs pt" data-punkt="' + esc(h.k) + '" tabindex="0" role="button" aria-label="Messpunkt ' + esc(punktName(h.k)) + '">' +
          '<circle cx="' + h.x + '" cy="' + h.y + '" r="13" fill="transparent"/>' +
          '<circle cx="' + h.x + '" cy="' + h.y + '" r="6" fill="' + (h.k.includes('*') ? '#cbd5e1' : '#f7b612') + '" stroke="#0e192b" stroke-width="1.5"/>' +
          (rot ? '<circle cx="' + h.x + '" cy="' + h.y + '" r="10" fill="none" stroke="#f05e4e" stroke-width="3"/>' : '') +
          (schw ? '<circle cx="' + h.x + '" cy="' + h.y + '" r="10" fill="none" stroke="#e6edf6" stroke-width="3" stroke-dasharray="3 2"/>' : '') +
          '<text x="' + h.x + '" y="' + (h.y - 9) + '" text-anchor="middle" font-size="8" font-weight="700" fill="#e6edf6">' + esc(h.l) + '</text></g>';
      } else {
        const id = h.t === 'n' ? 'nav:' + h.id : h.id;
        s += '<g class="hs" data-obj="' + esc(id) + '" tabindex="0" role="button" aria-label="' + esc(h.l || h.id) + '"><rect x="' + h.x + '" y="' + h.y + '" width="' + h.w + '" height="' + h.h + '" rx="6" fill="transparent" stroke="#5b8cff" stroke-opacity="' + (auswahl === id ? 0.95 : 0.35) + '" stroke-width="' + (auswahl === id ? 2.5 : 1.2) + '" stroke-dasharray="4 3"/>' +
          (h.l ? '<text x="' + (h.x + h.w / 2) + '" y="' + (h.y + h.h + 10) + '" text-anchor="middle" font-size="9" fill="#9fb7e6">' + esc(h.l) + '</text>' : '') + '</g>';
      }
    });
    return s + '</svg>';
  }

  // ---------- Aktionen an Objekten ----------
  function aktionsPanel() {
    if (!auswahl) return '';
    const [art, wer] = auswahl.split(':');
    let t = '', k = '';
    if (auswahl === 'hupe') { t = 'Hupe (Lenkrad)'; k = btn('bed', 'hupe', st.hupe ? 'Hupe loslassen' : 'Hupe drücken und halten', st.hupe); }
    else if (auswahl === 'licht') { t = 'Lichtschalter'; k = '<div class="seg">' + btn('licht', 'aus', 'Aus', st.licht === 'aus') + btn('licht', 'abblend', 'Abblendlicht', st.licht === 'abblend') + '</div>'; }
    else if (auswahl === 'blinker') { t = 'Blinkerhebel'; k = '<div class="seg">' + btn('blinker', 'links', 'Links', st.blinker === 'links') + btn('blinker', 'aus', 'Mitte', st.blinker === 'aus') + btn('blinker', 'rechts', 'Rechts', st.blinker === 'rechts') + '</div>'; }
    else if (auswahl === 'zuendung') { t = 'Start-Stopp-Taster'; k = btn('bed', 'zuendung', st.zuendung ? 'Zündung ausschalten' : 'Zündung einschalten (ohne Motorstart)', st.zuendung); }
    else if (auswahl === 'fenster') { t = 'Fensterheberschalter Fahrer'; k = '<div class="seg">' + btn('fenster', 'auf', 'Schließen (halten)', st.fenster === 'auf') + btn('fenster', 'aus', 'Loslassen', st.fenster === 'aus') + btn('fenster', 'ab', 'Öffnen (halten)', st.fenster === 'ab') + '</div>'; }
    else if (auswahl === 'bremse') { t = 'Bremspedal'; k = btn('bed', 'bremse', st.bremse ? 'Pedal loslassen' : 'Pedal treten und halten', st.bremse); }
    else if (auswahl === 'batterie') { t = 'Batterie'; k = btn('bed', 'batterie', st.batterie ? 'Minuspol abklemmen' : 'Minuspol wieder anklemmen', !st.batterie); }
    else if (auswahl === 'relais') { t = 'Hupenrelais K7'; k = btn('relais', 'K7', st.relais.K7 ? 'Relais wieder einstecken' : 'Relais ziehen', !!st.relais.K7); }
    else if (art === 'st') { t = 'Stecker ' + wer; k = btn('stecker', wer, st.stecker[wer] ? 'Stecker wieder aufstecken' : 'Stecker abziehen', !!st.stecker[wer]) + '<p class="muted" style="margin:6px 0 0">Gelbe Punkte: Leitungsseite (rückseitig messbar). Helle Punkte erscheinen, wenn der Stecker abgezogen ist: Bauteilseite.</p>'; }
    else if (art === 'si') {
      const z = st.sich[wer], gez = !!meta.gezogen[wer];
      t = D.ortName(wer);
      k = (gez ? '<p style="margin:0 0 8px">Sicherung ist gezogen. Sichtprüfung: <b>' + (z === 'durch' ? 'Schmelzleiter durchgebrannt' : 'in Ordnung') + '</b></p>' : '<p class="muted" style="margin:0 0 8px">Steckt. Ob sie in Ordnung ist, siehst du erst nach dem Ziehen oder durch Messen an beiden Prüfpunkten.</p>') +
        '<div class="seg">' + (gez ? btn('sich', wer + ':rein', 'Wieder einstecken') + btn('sich', wer + ':neu', 'Neue Sicherung einsetzen') : btn('sich', wer + ':raus', 'Ziehen')) + '</div>';
    }
    else if (art === 'gl') {
      t = D.ortName(wer);
      const kaputt = st.fehler && st.fehler.el === wer;
      k = meta.lampen[wer] ? '<p style="margin:0">Glühlampe ausgebaut und angesehen: <b>' + (kaputt ? 'Glühfaden durchgebrannt' : 'in Ordnung') + '</b></p>' : btn('lampe', wer, 'Glühlampe ausbauen und ansehen');
    }
    else return '';
    return '<div class="card aktion"><p class="lbl">' + esc(t) + '</p>' + k + '</div>';
  }

  // ---------- Werkzeuge ----------
  function messwert() {
    if (!mm.rot || !mm.schwarz) return { text: werkzeug === 'pl' ? '' : '– – –' };
    messungenZaehlen();
    if (werkzeug === 'pl') {
      const p = D.prueflampe(st, mm.rot, mm.schwarz);
      return { text: { hell: 'Prüflampe leuchtet hell', schwach: 'Prüflampe glimmt schwach', aus: 'Prüflampe bleibt dunkel' }[p.stufe] + (p.wechsel ? ' (im Blinktakt)' : ''), stufe: p.stufe };
    }
    if (mm.modus === 'V') {
      const u = D.spannung(st, mm.rot, mm.schwarz);
      return { text: komma(u.wert, 2) + ' V' + (u.wechsel !== undefined ? ' ↔ ' + komma(u.wechsel, 2) + ' V' : ''), hinweis: u.wechsel !== undefined ? 'Der Wert springt im Blinktakt.' : '' };
    }
    const r = D.widerstand(st, mm.rot, mm.schwarz);
    if (r.fremd) return { text: 'Fehler', warn: 'Fremdspannung! Widerstand nur im spannungslosen Zustand messen: Bauteil abstecken, Sicherung ziehen oder Batterie abklemmen.' };
    const w = r.wert;
    return { text: w === Infinity ? 'OL' : w < 10 ? komma(w, 2) + ' Ω' : w < 1000 ? komma(w, 1) + ' Ω' : komma(w / 1000, 2) + ' kΩ' };
  }
  let letzteMessung = '';
  function messungenZaehlen() {
    const key = [werkzeug, mm.modus, mm.rot, mm.schwarz].join('|');
    if (key !== letzteMessung) { messungen++; letzteMessung = key; }
  }

  function werkzeugPanel() {
    let h = '<p class="lbl">Werkzeugwagen</p><div class="seg wrap werkzeuge">' + btn('wz', 'mm', '🔌 Multimeter', werkzeug === 'mm') + btn('wz', 'pl', '💡 Prüflampe', werkzeug === 'pl') + btn('wz', 'tester', '🖥 Diagnosetester', werkzeug === 'tester') + btn('wz', 'plan', '📄 Schaltplan', werkzeug === 'plan') + '</div>';
    if (werkzeug === 'mm' || werkzeug === 'pl') {
      const w = messwert();
      h += '<div class="card">';
      if (werkzeug === 'mm') h += '<div class="seg">' + btn('modus', 'V', 'V= Spannung', mm.modus === 'V') + btn('modus', 'R', 'Ω Widerstand', mm.modus === 'R') + '</div><div class="display">' + w.text + '</div>';
      else h += '<div class="mini-display"><span>Prüflampe 12 V / 5 W</span><b style="font-size:16px">' + (w.text || 'Spitzen anlegen') + '</b></div>';
      if (w.warn) h += '<div class="meld warn">' + w.warn + '</div>';
      if (w.hinweis) h += '<p class="muted" style="margin:0 0 6px">' + w.hinweis + '</p>';
      h += '<div class="seg">' + btn('spitze', 'rot', '<span class="dot rot"></span>Rote Spitze: ' + (mm.rot ? esc(punktName(mm.rot)) : 'frei'), mm.naechste === 'rot') + btn('spitze', 'schwarz', '<span class="dot sw"></span>Schwarze Spitze: ' + (mm.schwarz ? esc(punktName(mm.schwarz)) : 'frei'), mm.naechste === 'schwarz') + '</div>';
      h += '<p class="muted" style="margin:0">Wähle die Spitze und tippe dann einen gelben Messpunkt am Auto an. Die Spitzen bleiben dran, wenn du die Ansicht wechselst.</p>';
      if (werkzeug === 'pl' && [mm.rot, mm.schwarz].some(k => k && /^A(10|20)\./.test(k))) h += '<div class="meld info">Vorsicht: Mit der Prüflampe an Steuergeräte-Anschlüssen kannst du Elektronik beschädigen. Dort besser mit dem Multimeter messen.</div>';
      h += '</div>';
    }
    if (werkzeug === 'tester') h += testerPanel();
    if (werkzeug === 'plan') h += '<div class="card"><div class="seg wrap">' + PL.SYSTEME.map(s => btn('plan', s, PL.PLAENE[s].titel, planSys === s)).join('') + '</div><div class="plan-box">' + PL.svg(planSys) + '</div>' +
      '<p class="lbl" style="margin-top:8px">Einbauorte</p><ul class="orte">' + PL.PLAENE[planSys].orte.map(([a, b]) => '<li><b>' + a + ':</b> ' + b + '</li>').join('') + '</ul></div>';
    return h;
  }

  function testerPanel() {
    let h = '<div class="card tester"><div class="tester-kopf">Diagnosetester</div>';
    if (!tester.verbunden) return h + '<p style="margin:0">Schließe den Tester an der OBD-Buchse an: Sie sitzt im Fußraum unter dem Armaturenbrett.</p></div>';
    const fehler = D.testerVerbindung(st);
    if (fehler) return h + '<div class="meld warn">' + fehler + '</div></div>';
    if (!tester.sg) {
      h += '<p class="lbl">Steuergerät wählen</p><div class="seg wrap">' + Object.keys(D.SG).map(id => btn('sg', id, D.SG[id].name + (st.speicher[id].length ? ' ⚠' : ''))).join('') + '</div>';
      return h + '</div>';
    }
    h += '<p style="margin:0 0 8px"><b>' + D.SG[tester.sg].name + '</b> <button class="klein" data-sg="">← zurück</button></p>';
    h += '<div class="seg">' + btn('ts', 'speicher', 'Fehlerspeicher', tester.seite === 'speicher') + btn('ts', 'ist', 'Istwerte', tester.seite === 'ist') + btn('ts', 'stell', 'Stellglieder', tester.seite === 'stell') + '</div>';
    if (tester.seite === 'speicher') {
      const l = st.speicher[tester.sg];
      h += l.length ? '<ul class="codes">' + l.map(c => '<li><b>' + c.code + '</b> ' + esc(c.text) + '<span class="muted"> · ' + c.anzahl + '×</span></li>').join('') + '</ul>' : '<p style="margin:0 0 8px">Kein Fehler gespeichert.</p>';
      h += '<button data-loeschen="1">Fehlerspeicher löschen</button>';
    }
    if (tester.seite === 'ist') h += '<table class="ist">' + D.istwerte(st, tester.sg).map(([a, b]) => '<tr><td>' + esc(a) + '</td><td>' + esc(b) + '</td></tr>').join('') + '</table><p class="muted" style="margin:6px 0 0">Die Werte sind live: Bediene das Auto, während du hier schaust.</p>';
    if (tester.seite === 'stell') {
      const l = D.STELLGLIEDER[tester.sg];
      h += l.length ? '<div class="seg wrap">' + l.map(([id, t]) => btn('stell', id, (st.stell[id] ? '■ Stopp: ' : '▶ ') + t, !!st.stell[id])).join('') + '</div><p class="muted" style="margin:6px 0 0">Während ein Stellglied läuft, kannst du am Auto schauen und messen.</p>' : '<p style="margin:0">Für dieses Steuergerät gibt es hier keine Stellglieder.</p>';
    }
    return h + '</div>';
  }

  // ---------- Ergebnis ----------
  function ergebnisPanel() {
    if (ergebnis) {
      const zeigen = ergebnis.richtig || ergebnis.zeigen;
      let h = '<div class="meld ' + (ergebnis.richtig ? 'ok' : 'warn') + '"><b>' + (ergebnis.richtig ? 'Richtig! Fehler gefunden.' : ergebnis.ortOk ? 'Der Ort stimmt, die Fehlerart nicht.' : 'Leider falsch.') + '</b> Messungen: ' + messungen + '.' + (ergebnis.hinweis ? '<br>' + esc(ergebnis.hinweis) : '');
      if (zeigen) h += '<br><b>' + esc(D.ortName(ergebnis.loesung.ort)) + ' – ' + D.ARTEN.find(a => a[0] === ergebnis.loesung.art)[1] + ':</b> ' + esc(ergebnis.erklaerung);
      h += '</div>';
      return h + (zeigen ? '<button class="primary" style="width:100%" data-neu="1">Nächster Auftrag</button>' : '<div class="seg"><button class="primary" data-weiter="1">Weiter suchen</button><button data-loesung="1">Lösung zeigen</button></div>');
    }
    if (!antwort.offen) return '<button class="primary" style="width:100%" data-melden="1">Fehler gefunden</button>';
    const gruppen = {};
    D.FEHLERORTE.forEach(o => { (gruppen[o.sys] = gruppen[o.sys] || []).push(o); });
    let h = '<div class="card"><p class="lbl">Wo sitzt der Fehler?</p><select data-ort="1" class="auswahl"><option value="">– Bauteil oder Leitung wählen –</option>' +
      Object.keys(gruppen).map(g => '<optgroup label="' + g + '">' + gruppen[g].map(o => '<option value="' + o.id + '"' + (antwort.ort === o.id ? ' selected' : '') + '>' + esc(o.name) + '</option>').join('') + '</optgroup>').join('') + '</select>';
    h += '<p class="lbl">Was ist kaputt?</p><div class="seg wrap">' + D.ARTEN.map(([id, t]) => btn('art', id, t, antwort.art === id)).join('') + '</div>';
    if (antwort.fehler) h += '<p class="meld warn">' + antwort.fehler + '</p>';
    return h + '<button class="primary" style="width:100%" data-pruefen="1">Antwort prüfen</button></div>';
  }

  // ---------- Gesamtbild ----------
  function navLeiste() {
    const imRing = RING.includes(ansicht);
    let h = '<div class="nav-auto">';
    if (imRing) h += btn('dreh', '-1', '◀') + '<b>' + TITEL[ansicht] + '</b>' + btn('dreh', '1', '▶');
    else h += btn('zurueck', '1', '← Zurück') + '<b>' + TITEL[ansicht] + '</b><span></span>';
    return h + '</div>';
  }

  function render() {
    const f = D.fall(st.fall);
    let h = '<div class="card auftrag"><p class="lbl">Kundenauftrag</p><p class="kunde">„' + esc(f.kunde) + '“</p><p class="muted" style="margin:0">Übungsauto (fiktiv) · Finde die Ursache wie in der Werkstatt.</p></div>';
    h += '<div class="card fahrzeug">' + navLeiste() + ansichtSvg() + (meldung ? '<div class="meld info">' + meldung + '</div>' : '') + '</div>';
    h += aktionsPanel();
    h += werkzeugPanel();
    h += ergebnisPanel();
    root.innerHTML = h;
  }

  // ---------- Bedienung ----------
  function objekt(id) {
    meldung = '';
    if (id.startsWith('nav:')) { ansicht = id.slice(4); auswahl = null; return; }
    if (id === 'haube') {
      if (!meta.haubeFrei) { meldung = 'Die Motorhaube ist verriegelt. Den Entriegelungshebel findest du im Fußraum auf der Fahrerseite.'; return; }
      meta.haube = true; ansicht = 'motorraum'; auswahl = null; return;
    }
    if (id === 'tuer') {
      if (meta.tuer) { ansicht = 'innen'; auswahl = null; return; }
      meta.tuer = true; meldung = 'Die Fahrertür ist offen. Tippe nochmal auf die Tür, um einzusteigen.'; return;
    }
    if (id === 'rlL' || id === 'rlR') { ansicht = id; auswahl = null; meldung = 'Rückleuchte vom Kofferraum aus ausgebaut. Der Stecker ' + (id === 'rlL' ? 'X30' : 'X31') + ' hängt noch dran.'; return; }
    if (id === 'abdeckung') { ansicht = 'sk'; auswahl = null; return; }
    if (id === 'verkleidung') { ansicht = 'tuer'; auswahl = null; meldung = 'Türverkleidung abgebaut.'; return; }
    if (id === 'haubenhebel') { meta.haubeFrei = true; meldung = 'Klack: Die Motorhaube ist entriegelt. Jetzt vorne die Haube öffnen.'; return; }
    if (id === 'obd') {
      if (werkzeug !== 'tester') { meldung = 'Hier wird der Diagnosetester angeschlossen. Nimm ihn vom Werkzeugwagen.'; return; }
      tester.verbunden = true; meldung = 'Diagnosetester angeschlossen.'; return;
    }
    auswahl = auswahl === id ? null : id;
  }

  function punkt(k) {
    if (werkzeug !== 'mm' && werkzeug !== 'pl') { meldung = 'Messpunkt ' + esc(punktName(k)) + '. Nimm zum Messen das Multimeter oder die Prüflampe vom Werkzeugwagen.'; return; }
    meldung = '';
    mm[mm.naechste] = k;
    mm.naechste = mm.naechste === 'rot' ? 'schwarz' : 'rot';
  }

  root.addEventListener('click', e => {
    const g = e.target.closest('[data-punkt],[data-obj]');
    if (g) { if (g.dataset.punkt) punkt(g.dataset.punkt); else objekt(g.dataset.obj); return render(); }
    const b = e.target.closest('button');
    if (!b) return;
    const d = b.dataset;
    if (d.dreh) { ansicht = RING[(RING.indexOf(ansicht) + +d.dreh + 4) % 4]; auswahl = null; meldung = ''; }
    else if (d.zurueck) { ansicht = ZURUECK[ansicht] || 'vorne'; auswahl = null; meldung = ''; }
    else if (d.bed) { const v = {}; v[d.bed] = !st[d.bed]; D.bediene(st, v); }
    else if (d.licht) D.bediene(st, { licht: d.licht });
    else if (d.blinker) D.bediene(st, { blinker: d.blinker });
    else if (d.fenster) { const b2 = D.bediene(st, { fenster: d.fenster }); if (d.fenster !== 'aus') meldung = b2.motor ? 'Die Scheibe fährt.' : 'Die Scheibe bewegt sich nicht.'; }
    else if (d.relais) { st.relais[d.relais] = st.relais[d.relais] ? undefined : 'raus'; if (!st.relais[d.relais]) delete st.relais[d.relais]; D.bediene(st, {}); }
    else if (d.stecker) { if (st.stecker[d.stecker]) delete st.stecker[d.stecker]; else st.stecker[d.stecker] = true; D.bediene(st, {}); }
    else if (d.sich) {
      const [f, was] = d.sich.split(':');
      if (was === 'raus') { meta.gezogen[f] = true; if (!st.sich[f]) st.sich[f] = 'raus'; }
      else { meta.gezogen[f] = false; if (was === 'neu' || st.sich[f] === 'raus') delete st.sich[f]; }
      const heil = !st.sich[f];
      D.bediene(st, {});
      if (heil && st.sich[f] === 'durch') meldung = 'Die Sicherung ist sofort wieder durchgebrannt!';
    }
    else if (d.lampe) meta.lampen[d.lampe] = true;
    else if (d.wz) { werkzeug = werkzeug === d.wz ? null : d.wz; if (werkzeug === 'pl') mm.modus = 'V'; }
    else if (d.modus) mm.modus = d.modus;
    else if (d.spitze) mm.naechste = d.spitze;
    else if (d.plan) planSys = d.plan;
    else if (d.sg !== undefined) { tester.sg = d.sg || null; tester.seite = 'speicher'; }
    else if (d.ts) tester.seite = d.ts;
    else if (d.loeschen) D.loescheSpeicher(st, tester.sg);
    else if (d.stell) { const b2 = D.stellglied(st, tester.sg, d.stell, !st.stell[d.stell]); if (tester.sg === 'A20') meldung = b2.motor ? 'Der Fensterhebermotor läuft.' : 'Am Fenster tut sich nichts.'; }
    else if (d.melden) antwort.offen = true;
    else if (d.art) { antwort.art = d.art; antwort.fehler = ''; }
    else if (d.pruefen) {
      if (!antwort.ort || !antwort.art) antwort.fehler = 'Wähle Ort und Fehlerart aus.';
      else ergebnis = D.pruefe(st, antwort.ort, antwort.art);
    }
    else if (d.weiter) { ergebnis = null; }
    else if (d.loesung) ergebnis.zeigen = true;
    else if (d.neu) neuerAuftrag();
    else return;
    render();
  });
  root.addEventListener('change', e => { if (e.target.dataset.ort) { antwort.ort = e.target.value || null; antwort.fehler = ''; } });
  root.addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && e.target.closest('[data-punkt],[data-obj]')) { e.preventDefault(); e.target.dispatchEvent(new MouseEvent('click', { bubbles: true })); } });

  const wunsch = new URLSearchParams(location.search).get('fall');
  neuerAuftrag(D.fall(wunsch) ? wunsch : null);
  render();
})();
