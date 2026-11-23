// Detaillierte Zeichnungen des Übungsautos (viewBox 360 x 230).
// Koordinaten der Messpunkte und Hotspots stehen in diagnose-ui.js.
const DiagnoseGrafik = (() => {
  const DEFS = '<defs>' +
    '<linearGradient id="lack" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8cc7cf"/><stop offset=".35" stop-color="#3f8793"/><stop offset=".7" stop-color="#25606b"/><stop offset="1" stop-color="#183f47"/></linearGradient>' +
    '<linearGradient id="lackS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fd2d9"/><stop offset=".3" stop-color="#4a919c"/><stop offset=".55" stop-color="#2c6a75"/><stop offset=".56" stop-color="#3a7f8a"/><stop offset="1" stop-color="#173a42"/></linearGradient>' +
    '<linearGradient id="glas" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b9d6e6"/><stop offset=".25" stop-color="#5f84a0"/><stop offset=".6" stop-color="#22374b"/><stop offset="1" stop-color="#0f1c2a"/></linearGradient>' +
    '<linearGradient id="chrom" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3f6f9"/><stop offset=".5" stop-color="#9aa6b3"/><stop offset="1" stop-color="#e3e8ee"/></linearGradient>' +
    '<linearGradient id="plastik" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3f47"/><stop offset="1" stop-color="#16191d"/></linearGradient>' +
    '<linearGradient id="grau" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9ced6"/><stop offset="1" stop-color="#8d949e"/></linearGradient>' +
    '<linearGradient id="boden" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6c727a"/><stop offset="1" stop-color="#3b4047"/></linearGradient>' +
    '<linearGradient id="wand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b3644"/><stop offset="1" stop-color="#3d4a5a"/></linearGradient>' +
    '<linearGradient id="motorraum" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2027"/><stop offset="1" stop-color="#2a3038"/></linearGradient>' +
    '<radialGradient id="reifen" cx=".5" cy=".5" r=".5"><stop offset=".55" stop-color="#3a3d42"/><stop offset=".62" stop-color="#1a1c1f"/><stop offset="1" stop-color="#0c0d0f"/></radialGradient>' +
    '<radialGradient id="felge" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#eef1f4"/><stop offset=".7" stop-color="#9aa3ad"/><stop offset="1" stop-color="#5d6670"/></radialGradient>' +
    '<radialGradient id="linse" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#c7d3df"/><stop offset="1" stop-color="#6a7787"/></radialGradient>' +
    '<radialGradient id="rueckRot" cx=".5" cy=".5" r=".6"><stop offset="0" stop-color="#b3262b"/><stop offset="1" stop-color="#4b0d10"/></radialGradient>' +
    '<filter id="weich" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>' +
    '<filter id="schatten" x="-20%" y="-20%" width="140%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>' +
    '<pattern id="wabe" width="8" height="7" patternUnits="userSpaceOnUse"><path d="M0 3.5 L2 0 H6 L8 3.5 L6 7 H2 Z" fill="#14171b" stroke="#2b3037" stroke-width="1"/></pattern>' +
    '<pattern id="lochblech" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="1.4" fill="#1e252e"/></pattern>' +
    '<pattern id="teppich" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="#171c23"/><circle cx="1" cy="1" r=".6" fill="#222934"/></pattern>' +
    '</defs>';

  const glanz = (x, y, rx, ry, h, farbe) => h > 0.05 ? '<ellipse cx="' + x + '" cy="' + y + '" rx="' + (rx * 1.9) + '" ry="' + (ry * 2.4) + '" fill="' + farbe + '" opacity="' + Math.min(0.6, h * 0.55).toFixed(2) + '" filter="url(#weich)"/>' : '';
  const blink = (an, schnell) => an ? ' class="' + (schnell ? 'blink-s' : 'blink') + '"' : '';
  const txt = (x, y, t, o) => '<text x="' + x + '" y="' + y + '" text-anchor="' + ((o && o.a) || 'middle') + '" font-size="' + ((o && o.s) || 8) + '" font-weight="' + ((o && o.w) || 600) + '" fill="' + ((o && o.f) || '#c4cfdc') + '">' + t + '</text>';
  const kabel = (d, farbe, streifen, b) => '<path d="' + d + '" fill="none" stroke="#0b0d10" stroke-width="' + ((b || 2.6) + 1.4) + '" stroke-linecap="round"/><path d="' + d + '" fill="none" stroke="' + farbe + '" stroke-width="' + (b || 2.6) + '" stroke-linecap="round"/>' +
    (streifen ? '<path d="' + d + '" fill="none" stroke="' + streifen + '" stroke-width="' + ((b || 2.6) * 0.4) + '" stroke-dasharray="4 4" stroke-linecap="round"/>' : '');
  const stecker = (x, y, n, offen) => {
    const w = 10 + n * 18;
    return '<rect x="' + (x - w / 2) + '" y="' + (y - 8) + '" width="' + w + '" height="16" rx="3" fill="#59616c" stroke="#2a3038"/><rect x="' + (x - w / 2 + 3) + '" y="' + (y - 5) + '" width="' + (w - 6) + '" height="10" rx="2" fill="#3f464f"/>' +
      '<rect x="' + (x - 5) + '" y="' + (y - 12) + '" width="10" height="5" rx="1.5" fill="#6d7681"/>' + (offen ? '' : '');
  };
  const schraube = (x, y) => '<circle cx="' + x + '" cy="' + y + '" r="5.5" fill="url(#chrom)" stroke="#3a4048"/><path d="M' + (x - 3) + ' ' + y + 'h6M' + x + ' ' + (y - 3) + 'v6" stroke="#5b6570" stroke-width="1.2"/>';
  const masse = (x, y, richtung) => kabel('M' + x + ' ' + y + ' q ' + (richtung || 14) + ' 6 ' + (richtung || 14) * 1.6 + ' 18', '#7a5230') + '<circle cx="' + x + '" cy="' + y + '" r="8" fill="none" stroke="#c9a46a" stroke-width="2.5"/>' + schraube(x, y);
  const sicherungBlatt = (x, y, farbe, gezogen, durch, amp) => gezogen ?
    '<rect x="' + (x - 8) + '" y="' + (y - 10) + '" width="16" height="20" rx="2" fill="#07090b" stroke="#3b424b"/><rect x="' + (x - 5) + '" y="' + (y + 2) + '" width="3" height="6" fill="#8a7a4a"/><rect x="' + (x + 2) + '" y="' + (y + 2) + '" width="3" height="6" fill="#8a7a4a"/>' :
    '<rect x="' + (x - 8) + '" y="' + (y - 11) + '" width="16" height="16" rx="2.5" fill="' + farbe + '" stroke="rgba(0,0,0,.4)"/><rect x="' + (x - 6) + '" y="' + (y - 9) + '" width="12" height="5" rx="1" fill="rgba(255,255,255,.35)"/>' +
    '<rect x="' + (x - 6) + '" y="' + (y + 5) + '" width="4" height="5" fill="#cdbb85"/><rect x="' + (x + 2) + '" y="' + (y + 5) + '" width="4" height="5" fill="#cdbb85"/>' + txt(x, y + 1, amp, { s: 6.5, w: 800, f: '#111' });

  // ---------- Werkstatt-Hintergrund ----------
  const werkstatt = () => '<rect width="360" height="230" fill="url(#wand)"/>' +
    '<g opacity=".35">' + [40, 120, 200, 280].map(x => '<rect x="' + x + '" y="18" width="62" height="62" rx="3" fill="none" stroke="#5d6b7c"/>').join('') + '</g>' +
    '<path d="M44 34 h12 M48 30 v10 M132 30 l10 10 M220 36 h14 M292 32 h10 v8" stroke="#7d8a9a" stroke-width="2" opacity=".4"/>' +
    '<path d="M0 168 H360 V230 H0 Z" fill="url(#boden)"/>' +
    '<path d="M0 168 H360" stroke="#262c33" stroke-width="2"/>' +
    '<g opacity=".18" stroke="#fff">' + [-200, -100, 0, 100, 200].map(d => '<path d="M' + (180 + d * 0.5) + ' 168 L' + (180 + d * 1.6) + ' 230"/>').join('') + '</g>' +
    '<path d="M0 222 H360" stroke="#f2c230" stroke-width="5" stroke-dasharray="14 10" opacity=".75"/>';
  const bodenschatten = (cx, w) => '<ellipse cx="' + cx + '" cy="203" rx="' + w + '" ry="9" fill="#000" opacity=".45" filter="url(#schatten)"/>';

  // ---------- Außen ----------
  function vorne(b) {
    let s = werkstatt() + bodenschatten(180, 150);
    s += '<rect x="58" y="172" width="40" height="32" rx="6" fill="url(#reifen)"/><rect x="262" y="172" width="40" height="32" rx="6" fill="url(#reifen)"/>';
    // Dach, Säulen, Scheibe
    s += '<path d="M98 104 L124 48 Q180 36 236 48 L262 104 Z" fill="url(#lack)"/>';
    s += '<path d="M108 101 L131 55 Q180 45 229 55 L252 101 Z" fill="url(#glas)"/><path d="M140 58 L120 98 L132 98 L150 56 Z" fill="#fff" opacity=".12"/>';
    s += '<path d="M150 99 L196 92 M210 99 L250 92" stroke="#111" stroke-width="2.5" stroke-linecap="round"/>';
    s += '<path d="M78 94 l-22 -6 l-2 14 l22 4 Z M282 94 l22 -6 l2 14 l-22 4 Z" fill="url(#lack)" stroke="#173a42"/>';
    // Karosserie
    s += '<path d="M40 132 Q44 106 98 102 L262 102 Q316 106 320 132 L324 176 Q180 190 36 176 Z" fill="url(#lack)"/>';
    s += '<path d="M66 104 L294 104 L310 126 L50 126 Z" fill="url(#lackS)" opacity=".9"/><path d="M120 106 L110 124 M240 106 L250 124" stroke="#1d4a52" stroke-width="1.5" opacity=".7"/>';
    // Scheinwerfer
    const sw = (x, spiegel, h) => {
      const k = spiegel ? -1 : 1;
      return '<path d="M' + (x - 34 * k) + ' 132 Q' + (x - 30 * k) + ' 126 ' + (x + 6 * k) + ' 128 L' + (x + 34 * k) + ' 136 Q' + (x + 30 * k) + ' 148 ' + (x - 4 * k) + ' 148 Q' + (x - 30 * k) + ' 146 ' + (x - 34 * k) + ' 132 Z" fill="#20262d" stroke="#0e1114" stroke-width="1.5"/>' +
        '<path d="M' + (x - 30 * k) + ' 133 Q' + (x - 26 * k) + ' 129 ' + (x + 4 * k) + ' 131 L' + (x + 28 * k) + ' 137 Q' + (x + 25 * k) + ' 145 ' + (x - 4 * k) + ' 145 Q' + (x - 27 * k) + ' 143 ' + (x - 30 * k) + ' 133 Z" fill="url(#chrom)" opacity=".85"/>' +
        '<circle cx="' + (x - 10 * k) + '" cy="138" r="7" fill="url(#linse)" stroke="#556070"/><circle cx="' + (x + 12 * k) + '" cy="139" r="5" fill="url(#linse)" stroke="#556070"/>' +
        '<path d="M' + (x - 28 * k) + ' 131 Q' + (x - 6 * k) + ' 127 ' + (x + 26 * k) + ' 134" stroke="#eaf6ff" stroke-width="1.8" fill="none" opacity=".8"/>' +
        (h > 0.05 ? '<circle cx="' + (x - 10 * k) + '" cy="138" r="6" fill="#fffbe0"/>' : '');
    };
    s += glanz(96, 138, 30, 11, b.abr, '#fff7c2') + glanz(264, 138, 30, 11, b.abl, '#fff7c2');
    s += sw(96, true, b.abr) + sw(264, false, b.abl);
    s += '<rect x="48" y="130" width="14" height="10" rx="3" fill="#f39a1e" stroke="#7a4708"' + (b.blvr > 0.3 ? blink(true, b.schnellR) : ' opacity=".55"') + '/>';
    s += '<rect x="298" y="130" width="14" height="10" rx="3" fill="#f39a1e" stroke="#7a4708"' + (b.blvl > 0.3 ? blink(true, b.schnellL) : ' opacity=".55"') + '/>';
    // Kühlergrill, Stoßfänger, Kennzeichen
    s += '<path d="M140 138 Q180 132 220 138 L214 160 Q180 164 146 160 Z" fill="url(#wabe)" stroke="#0d0f12" stroke-width="2"/><path d="M144 139 Q180 134 216 139" stroke="url(#chrom)" stroke-width="2.5" fill="none"/>';
    s += '<path d="M44 160 Q180 172 316 160 L320 178 Q180 192 40 178 Z" fill="#1e2328"/><path d="M110 170 Q180 178 250 170 L246 182 Q180 188 114 182 Z" fill="url(#wabe)"/>';
    s += '<rect x="148" y="164" width="64" height="14" rx="2" fill="#f5f7fa" stroke="#7e8894"/><rect x="149" y="165" width="7" height="12" fill="#2b54b8"/>' + txt(184, 175, 'AZ PS 26', { s: 8.5, w: 800, f: '#1a1f26' });
    s += '<circle cx="68" cy="168" r="6" fill="url(#linse)" stroke="#333"/><circle cx="292" cy="168" r="6" fill="url(#linse)" stroke="#333"/>';
    return s;
  }

  function hinten(b) {
    let s = werkstatt() + bodenschatten(180, 150);
    s += '<rect x="58" y="172" width="40" height="32" rx="6" fill="url(#reifen)"/><rect x="262" y="172" width="40" height="32" rx="6" fill="url(#reifen)"/>';
    s += '<path d="M100 104 L126 50 Q180 40 234 50 L260 104 Z" fill="url(#lack)"/><path d="M112 99 L134 58 Q180 50 226 58 L248 99 Z" fill="url(#glas)"/>';
    s += '<path d="M180 96 L150 70" stroke="#111" stroke-width="2.5" stroke-linecap="round"/><rect x="164" y="54" width="32" height="4" rx="2" fill="#5a0f12"/>';
    s += '<path d="M40 128 Q46 106 100 102 L260 102 Q314 106 320 128 L324 176 Q180 190 36 176 Z" fill="url(#lack)"/>';
    s += '<path d="M118 108 H242 L238 150 H122 Z" fill="url(#lackS)" opacity=".7" stroke="#173a42"/>' + '<rect x="172" y="120" width="16" height="8" rx="4" fill="url(#chrom)"/>';
    const rl = (x, bl, br, schnell) => '<path d="M' + x + ' 116 h62 l-4 30 h-54 Z" fill="#1a0b0c" stroke="#0b0506" stroke-width="2"/>' +
      '<rect x="' + (x + 4) + '" y="120" width="26" height="22" rx="3" fill="' + (bl ? '#ffb02e' : '#7a5418') + '"' + (bl ? blink(true, schnell) : '') + '/>' +
      '<rect x="' + (x + 34) + '" y="120" width="24" height="22" rx="3" fill="' + (br ? '#ff2a2a' : 'url(#rueckRot)') + '"/>' +
      '<path d="M' + (x + 4) + ' 121 h54" stroke="#fff" stroke-width="1" opacity=".25"/>';
    s += glanz(100, 131, 14, 10, b.brl, '#ff3030') + glanz(260, 131, 14, 10, b.brr, '#ff3030');
    s += rl(54, b.blhl > 0.3, b.brl > 0.3, b.schnellL);
    s += '<g transform="translate(360 0) scale(-1 1)">' + rl(54, b.blhr > 0.3, b.brr > 0.3, b.schnellR) + '</g>';
    s += '<path d="M44 160 Q180 172 316 160 L320 178 Q180 192 40 178 Z" fill="#1e2328"/>';
    s += '<rect x="148" y="146" width="64" height="14" rx="2" fill="#f5f7fa" stroke="#7e8894"/><rect x="149" y="147" width="7" height="12" fill="#2b54b8"/>' + txt(184, 157, 'AZ PS 26', { s: 8.5, w: 800, f: '#1a1f26' });
    s += '<rect x="56" y="166" width="22" height="5" rx="2" fill="#a51d22"/><rect x="282" y="166" width="22" height="5" rx="2" fill="#a51d22"/>';
    s += '<ellipse cx="96" cy="184" rx="8" ry="4" fill="#0b0c0e" stroke="url(#chrom)" stroke-width="2"/>';
    return s;
  }

  function seite(b, st, meta, beifahrer) {
    const fp = st.fensterPos;
    let s = werkstatt() + bodenschatten(180, 165);
    s += '<g' + (beifahrer ? ' transform="translate(360 0) scale(-1 1)"' : '') + '>';
    s += '<path d="M22 168 Q20 140 58 132 L100 127 Q124 104 152 92 Q200 80 258 86 Q282 90 300 124 Q336 130 340 160 L338 180 L22 180 Z" fill="url(#lackS)"/>';
    s += '<path d="M30 150 Q180 144 334 148" stroke="#1d4a52" stroke-width="1.5" fill="none" opacity=".8"/><path d="M24 168 H338" stroke="#153238" stroke-width="2"/>';
    // Fenster
    s += '<path d="M126 128 L156 98 Q186 90 216 90 L216 128 Z" fill="#101820"/>';
    const glasY = 90 + 40 * fp / 100;
    s += '<clipPath id="fsC"><path d="M126 128 L156 98 Q186 90 216 90 L216 128 Z"/></clipPath>';
    if (!beifahrer) s += '<rect x="110" y="' + glasY.toFixed(1) + '" width="120" height="60" fill="url(#glas)" clip-path="url(#fsC)"/>';
    else s += '<path d="M126 128 L156 98 Q186 90 216 90 L216 128 Z" fill="url(#glas)"/>';
    s += '<path d="M222 90 Q254 90 280 124 L222 128 Z" fill="url(#glas)"/><path d="M216 88 V130 M220 88 V130" stroke="#0e1114" stroke-width="5"/>';
    s += '<path d="M126 128 L156 98 Q186 90 216 90" stroke="#0e1114" stroke-width="2.5" fill="none"/>';
    // Spiegel
    s += '<path d="M120 116 q-14 -2 -16 8 q2 8 16 6 Z" fill="url(#lack)" stroke="#173a42"/>';
    // Radhäuser und Räder
    const rad = x => '<path d="M' + (x - 32) + ' 178 A32 32 0 0 1 ' + (x + 32) + ' 178" fill="#0d1013"/><circle cx="' + x + '" cy="182" r="26" fill="url(#reifen)"/><circle cx="' + x + '" cy="182" r="15" fill="url(#felge)" stroke="#4a525c"/>' +
      [0, 72, 144, 216, 288].map(w => '<path d="M' + x + ' 182 L' + (x + 13 * Math.cos(w * Math.PI / 180)).toFixed(1) + ' ' + (182 + 13 * Math.sin(w * Math.PI / 180)).toFixed(1) + '" stroke="#6f7984" stroke-width="3.5"/>').join('') + '<circle cx="' + x + '" cy="182" r="4" fill="#3a4148"/>';
    s += rad(86) + rad(278);
    // Tür
    if (!beifahrer && meta.tuer) {
      s += '<path d="M122 130 L218 128 L218 172 L126 172 Z" fill="#0b1118"/><path d="M150 140 h40 v28 h-40 Z" fill="#2a2f36"/><path d="M150 132 h28 v10 h-28 Z" fill="#363c44"/>';
      s += '<path d="M122 130 L76 116 L72 170 L126 174 Z" fill="url(#lackS)" stroke="#153238"/><path d="M80 124 L118 134 L120 166 L80 164 Z" fill="#2c323a"/>';
      s += txt(170, 160, 'Tür offen', { s: 9, f: '#9fb0c8' });
    } else {
      s += '<path d="M122 130 L218 128 L218 172 L126 172" fill="none" stroke="#123036" stroke-width="1.6"/><rect x="194" y="138" width="16" height="5" rx="2.5" fill="url(#chrom)"/>';
    }
    s += '<path d="M218 128 L218 172 M280 126 L282 172" stroke="#123036" stroke-width="1.6"/><rect x="254" y="138" width="16" height="5" rx="2.5" fill="url(#chrom)"/>';
    s += '<rect x="26" y="146" width="10" height="7" rx="2" fill="#f39a1e" opacity=".8"/><rect x="326" y="140" width="10" height="10" rx="2" fill="#7a1418"/>';
    return s + '</g>';
  }

  // ---------- Innenraum ----------
  function innen(b, st) {
    const kl = st.zuendung;
    let s = '<rect width="360" height="230" fill="#0d1218"/>';
    s += '<path d="M30 0 H360 V72 Q200 56 30 74 Z" fill="url(#wand)" opacity=".85"/><path d="M60 40 h70 M200 30 h90" stroke="#5d6b7c" stroke-width="3" opacity=".4"/>';
    s += '<path d="M30 0 L52 0 L70 76 L40 82 Z" fill="#1f252d"/>';
    s += '<path d="M30 82 Q190 58 360 80 L360 172 L30 172 Z" fill="#232a33"/><path d="M30 82 Q190 58 360 80" stroke="#3a4450" stroke-width="3" fill="none"/>';
    s += '<path d="M30 120 Q190 108 360 118" stroke="#1a2028" stroke-width="2" fill="none"/>';
    // Instrumente
    s += '<path d="M88 112 Q90 80 144 78 Q198 80 200 112 Z" fill="#14181e" stroke="#2c343e"/>';
    const uhr = (x, an) => '<circle cx="' + x + '" cy="102" r="17" fill="#07090c" stroke="#3a4552" stroke-width="2"/>' +
      Array.from({ length: 9 }, (_, i) => { const w = (-220 + i * 32.5) * Math.PI / 180; return '<path d="M' + (x + 14 * Math.cos(w)).toFixed(1) + ' ' + (102 + 14 * Math.sin(w)).toFixed(1) + ' L' + (x + 11 * Math.cos(w)).toFixed(1) + ' ' + (102 + 11 * Math.sin(w)).toFixed(1) + '" stroke="' + (an ? '#9fd8ff' : '#3a4552') + '" stroke-width="1.2"/>'; }).join('') +
      '<path d="M' + x + ' 102 L' + (x - 9) + ' 109" stroke="#ff5b4a" stroke-width="2" stroke-linecap="round"/>';
    s += uhr(118, kl) + uhr(170, kl) + '<rect x="134" y="92" width="20" height="18" rx="2" fill="' + (kl ? '#0e2a3a' : '#07090c') + '"/>';
    if (kl) s += txt(144, 104, '12,6V', { s: 5.5, f: '#7fd3ff' });
    const pfeil = (x, dir, an, schnell) => '<path d="M' + x + ' 86 l' + (dir * -7) + ' 4.5 l' + (dir * 7) + ' 4.5 z" fill="#34c778"' + (an ? blink(true, schnell) : ' opacity=".12"') + '/>';
    s += pfeil(132, 1, b.blinktL, b.schnellL) + pfeil(156, -1, b.blinktR, b.schnellR);
    if (kl && st.licht === 'abblend') s += '<path d="M140 84 q4 -3 8 0 q-4 3 -8 0 M149 82 l4 -1 M149 84 l4 0 M149 86 l4 1" stroke="#34c778" stroke-width="1.2" fill="none"/>';
    // Lenkrad
    s += '<circle cx="144" cy="150" r="50" fill="none" stroke="#3b444f" stroke-width="13"/><circle cx="144" cy="150" r="50" fill="none" stroke="#56616e" stroke-width="2" stroke-dasharray="2 4"/>';
    s += '<path d="M98 152 Q120 158 128 150 M190 152 Q168 158 160 150 M144 170 V198" stroke="#3b444f" stroke-width="12" stroke-linecap="round"/>';
    s += '<rect x="124" y="132" width="40" height="38" rx="12" fill="' + (st.hupe ? '#3f5f8a' : '#262c34') + '" stroke="#38414c"/>' + txt(144, 155, '⊘', { s: 10, f: '#6e7a88' });
    // Blinkerhebel
    s += '<g transform="rotate(' + ({ links: 10, rechts: -10, aus: 0 }[st.blinker]) + ' 108 121)"><rect x="74" y="117" width="36" height="8" rx="4" fill="#2d343d" stroke="#444e5a"/><rect x="74" y="117" width="9" height="8" rx="4" fill="#3a434e"/></g>';
    // Lichtschalter
    s += '<circle cx="52" cy="124" r="16" fill="#1a1f26" stroke="#3a4450" stroke-width="2"/><circle cx="52" cy="124" r="11" fill="#2b323b"/>';
    s += '<g transform="rotate(' + (st.licht === 'abblend' ? 60 : 0) + ' 52 124)"><rect x="50" y="111" width="4" height="13" rx="2" fill="#f7b612"/></g>';
    s += txt(36, 108, '0', { s: 6.5 }) + txt(68, 108, '≡D', { s: 6.5 }) + txt(52, 152, 'Licht', { s: 7.5 });
    // Start-Stopp
    s += '<circle cx="232" cy="122" r="13" fill="#15191f" stroke="url(#chrom)" stroke-width="2"/><circle cx="232" cy="122" r="9.5" fill="' + (kl ? '#1f7a4a' : '#262c34') + '"/>' + txt(232, 121, 'START', { s: 4.6, w: 800 }) + txt(232, 127, 'STOP', { s: 4.6, w: 800 }) + txt(232, 146, 'Zündung', { s: 7.5 });
    // Mittelkonsole
    s += '<rect x="262" y="88" width="70" height="40" rx="5" fill="#07090c" stroke="#2e3640"/><rect x="266" y="92" width="62" height="32" rx="3" fill="' + (kl ? '#12304a' : '#0b0e12') + '"/>';
    s += '<rect x="270" y="136" width="56" height="12" rx="3" fill="#161b21"/><path d="M276 142 h44" stroke="#2c343e" stroke-width="6" stroke-dasharray="3 2"/>';
    // Tür links
    s += '<path d="M0 78 L30 82 L30 230 L0 230 Z" fill="#2a313a"/><path d="M4 92 L26 94 L26 140 L4 142 Z" fill="#232a33" stroke="#38414c"/>' + txt(15, 112, 'Tür-', { s: 6.5 }) + txt(15, 121, 'verkl.', { s: 6.5 });
    s += '<rect x="6" y="150" width="18" height="30" rx="3" fill="#1d232a" stroke="#38414c"/><path d="M10 160 l5 -5 l5 5 M10 170 l5 5 l5 -5" stroke="#9aa6b4" stroke-width="1.6" fill="none"/>' + txt(15, 194, 'FH', { s: 7 });
    // Abdeckung Sicherungskasten
    s += '<path d="M34 160 H78 V186 H34 Z" fill="#20262e" stroke="#3b4550"/><rect x="50" y="164" width="12" height="3" rx="1.5" fill="#3b4550"/>' + txt(56, 180, 'Sicherungen', { s: 6 });
    // Fußraum
    s += '<path d="M30 172 H360 V230 H30 Z" fill="url(#teppich)"/><rect x="110" y="200" width="70" height="24" rx="6" fill="#1a2028" stroke="#3b4550"/>' + txt(145, 215, 'Fußraum ▾', { s: 8.5 });
    return s;
  }

  function fussraum(b, st) {
    let s = '<rect width="360" height="230" fill="url(#teppich)"/>';
    s += '<path d="M0 0 H360 V56 Q180 64 0 56 Z" fill="#232a33"/><path d="M0 56 Q180 64 360 56" stroke="#3a4450" stroke-width="2" fill="none"/>';
    // OBD-Buchse
    s += '<path d="M96 38 H130 L126 52 H100 Z" fill="#0a0c0f" stroke="#59626e" stroke-width="1.5"/>';
    for (let i = 0; i < 8; i++) s += '<rect x="' + (101 + i * 3.1) + '" y="41" width="1.6" height="3" fill="#c7a858"/><rect x="' + (102 + i * 2.9) + '" y="47" width="1.6" height="3" fill="#c7a858"/>';
    s += txt(113, 32, 'OBD-Buchse', { s: 7.5 });
    // Pedalbock
    s += '<path d="M170 56 L260 56 L250 76 L180 76 Z" fill="#3a424c" stroke="#232930"/>';
    // Bremspedal
    const p = st.bremse ? 8 : 0;
    s += '<path d="M206 70 Q204 110 ' + (206 + p * 0.4) + ' ' + (148 + p) + '" stroke="#5a636e" stroke-width="7" fill="none" stroke-linecap="round"/>';
    s += '<rect x="186" y="' + (148 + p) + '" width="44" height="24" rx="6" fill="#2b3138" stroke="#59626e"/><path d="M190 ' + (154 + p) + ' h36 M190 ' + (160 + p) + ' h36 M190 ' + (166 + p) + ' h36" stroke="#3d454f" stroke-width="2"/>';
    s += txt(208, 198, 'Bremspedal', { s: 8 });
    // Bremslichtschalter S5 + Leitungen
    s += '<rect x="214" y="70" width="34" height="18" rx="4" fill="#e9ecef" stroke="#7a8590"/><rect x="226" y="88" width="10" height="' + (st.bremse ? 4 : 9) + '" fill="#9aa4ae"/>' + txt(231, 82, 'S5', { s: 8, w: 800, f: '#1a1f26' });
    s += kabel('M222 120 Q222 150 270 160 L360 166', '#d32f2f') + kabel('M240 120 Q246 146 290 150 L360 154', '#1b1b1b', '#d32f2f');
    s += stecker(231, 104, 2);
    // Gaspedal
    s += '<path d="M290 60 L290 140" stroke="#4a525c" stroke-width="5"/><rect x="278" y="136" width="26" height="44" rx="5" fill="#2b3138" stroke="#59626e"/>';
    // Haubenhebel
    s += '<path d="M28 146 H78 V168 H28 Z" fill="#1e242b" stroke="#3b4550"/><path d="M40 150 h26 l-3 12 h-20 Z" fill="#f2c230" stroke="#8a6c10"/><path d="M45 156 q8 -5 16 0" stroke="#5a4708" stroke-width="1.5" fill="none"/>' + txt(53, 180, 'Haubenhebel', { s: 7.5 });
    return s;
  }

  function sk(b, st, meta) {
    let s = '<rect width="360" height="230" fill="#161b22"/><path d="M0 0 H360 V14 H0 Z" fill="#232a33"/>';
    s += '<rect x="18" y="18" width="134" height="180" rx="10" fill="url(#plastik)" stroke="#4a535e"/><rect x="24" y="24" width="122" height="168" rx="6" fill="#121519"/>';
    const dummy = ['#d8382c', '#2f6fd6', '#f2c230', '#d9b77e', '#2f6fd6', '#e9e9e9', '#d8382c', '#8a5a2b'];
    [['F8', 40, '#d8382c', '10'], ['F21', 80, '#f2c230', '20'], ['F22', 120, '#2f6fd6', '15'], ['F30', 160, '#e9e9e9', '25']].forEach(([f, y, c, a], i) => {
      s += sicherungBlatt(54, y, c, meta.gezogen[f], st.sich[f] === 'durch', a);
      s += txt(54, y - 13, f, { s: 6.5, f: '#9fb0c8' });
      s += kabel('M94 ' + y + ' H104', '#c9a43a', null, 1.4) + kabel('M124 ' + y + ' H134', '#c9a43a', null, 1.4);
    });
    for (let i = 0; i < 4; i++) s += sicherungBlatt(76, 40 + i * 40 + 20, dummy[i + 3], false, false, '');
    s += txt(85, 210, 'Sicherungskasten Innenraum', { s: 7.5 });
    // Bordnetz-SG
    s += '<rect x="176" y="18" width="168" height="158" rx="10" fill="url(#grau)" stroke="#5b6470"/><rect x="180" y="22" width="80" height="14" rx="2" fill="#f5f7fa"/>' + txt(220, 32, 'A10  Bordnetz-SG', { s: 7, w: 800, f: '#1a1f26' });
    s += '<rect x="196" y="46" width="128" height="116" rx="6" fill="#20252c" stroke="#0d1013" stroke-width="2"/><rect x="200" y="50" width="120" height="108" rx="4" fill="#2b3139"/>';
    s += '<rect x="250" y="40" width="20" height="8" rx="2" fill="#3a414a"/>';
    s += kabel('M216 160 Q210 200 170 214 L40 222', '#202020', null, 7) + kabel('M260 160 Q262 196 300 212', '#202020', null, 7);
    s += masse(260, 196, -14) + txt(286, 200, 'M3 A-Säule', { s: 7.5, a: 'start' });
    return s;
  }

  // ---------- Motorraum ----------
  function motorraum(b, st) {
    let s = '<rect width="360" height="230" fill="url(#motorraum)"/>';
    s += '<path d="M0 0 H360 V14 H0 Z" fill="#11151a"/>' + txt(180, 10, 'Spritzwand', { s: 7, f: '#6d7a8a' });
    s += '<path d="M0 212 H360 V230 H0 Z" fill="url(#lack)"/>' + txt(180, 225, 'vorne', { s: 7.5, f: '#d9eef1' });
    // Längsträger
    s += '<path d="M0 90 H20 V212 H0 Z M340 90 H360 V212 H340 Z" fill="#2d343c"/>';
    // Motor mit Abdeckung
    s += '<rect x="126" y="34" width="108" height="100" rx="14" fill="#1a1e23" stroke="#0b0d10" stroke-width="2"/>';
    s += '<path d="M134 44 Q180 34 226 44 L222 124 Q180 132 138 124 Z" fill="url(#plastik)"/><path d="M150 60 h60 M150 76 h60 M150 92 h60 M150 108 h60" stroke="#2b3038" stroke-width="5" stroke-linecap="round"/>';
    s += '<circle cx="208" cy="52" r="8" fill="#f2c230" stroke="#8a6c10"/>' + txt(180, 120, '1.4 TSI-frei', { s: 7, f: '#59626e' });
    // Luftfilter, Ausgleichsbehälter
    s += '<rect x="244" y="88" width="80" height="44" rx="8" fill="#22272d" stroke="#0b0d10"/><path d="M234 108 Q240 100 244 104" stroke="#111" stroke-width="10" fill="none"/>';
    s += '<rect x="40" y="88" width="56" height="36" rx="8" fill="#e8e8e8" opacity=".85" stroke="#888"/><rect x="44" y="104" width="48" height="16" rx="4" fill="#e85d9f" opacity=".7"/><circle cx="68" cy="92" r="6" fill="#1e7fd1"/>';
    s += '<rect x="196" y="16" width="30" height="16" rx="4" fill="#e8e0b8" opacity=".85" stroke="#776f4a"/><circle cx="211" cy="18" r="4" fill="#111"/>';
    // Batterie
    s += '<rect x="30" y="24" width="80" height="54" rx="5" fill="url(#plastik)" stroke="#0b0d10" stroke-width="2"/><rect x="40" y="46" width="60" height="22" rx="3" fill="#0f1215"/>' + txt(70, 60, st.batterie ? '12 V  70 Ah' : 'abgeklemmt', { s: 7, f: st.batterie ? '#9fb0c8' : '#ff8b7e' });
    s += '<rect x="38" y="28" width="12" height="8" rx="2" fill="#c0392b"/><rect x="90" y="28" width="12" height="8" rx="2" fill="#2b2f35"/>';
    s += kabel('M44 30 Q40 10 70 12 L110 14', '#c0392b', null, 4) + (st.batterie ? kabel('M96 30 Q110 14 124 26 L124 60', '#141414', null, 4) : kabel('M110 40 Q124 30 124 60', '#141414', null, 4));
    // E-Box
    s += '<rect x="252" y="24" width="78" height="54" rx="6" fill="url(#plastik)" stroke="#0b0d10" stroke-width="2"/><path d="M262 34 h58 v34 h-58 Z" fill="none" stroke="#3a414a" stroke-dasharray="3 2"/>' + txt(291, 55, 'E-Box', { s: 8 });
    // Kabelbaum
    s += kabel('M124 140 Q180 156 238 140 L300 150 L340 158', '#141414', null, 8) + kabel('M124 140 L60 150 L20 158', '#141414', null, 8);
    // Scheinwerfer
    const sw = (x, txtS) => '<path d="M' + (x - 46) + ' 180 Q' + (x - 44) + ' 172 ' + (x - 30) + ' 172 H' + (x + 30) + ' Q' + (x + 46) + ' 172 ' + (x + 46) + ' 184 V206 H' + (x - 46) + ' Z" fill="#2a3037" stroke="#0b0d10" stroke-width="2"/>' +
      '<circle cx="' + (x - 10) + '" cy="192" r="11" fill="#14181d" stroke="#3a414a" stroke-width="3"/><circle cx="' + (x + 22) + '" cy="192" r="8" fill="#14181d" stroke="#3a414a" stroke-width="3"/>' + txt(x, 220, txtS, { s: 7, f: '#d9eef1' });
    s += sw(292, 'Scheinwerfer links') + sw(68, 'Scheinwerfer rechts');
    // Leitungen zu den Steckern (Farben wie im Schaltplan)
    s += kabel('M267 160 Q264 150 280 150', '#e8c43a', '#141414') + kabel('M285 160 Q288 152 300 152', '#7a5230');
    s += kabel('M321 160 Q318 152 330 152', '#141414', '#f0f0f0') + kabel('M339 160 Q342 154 346 154', '#7a5230');
    s += kabel('M75 160 Q72 152 60 150', '#e8c43a', '#f0f0f0') + kabel('M93 160 Q96 152 110 150', '#7a5230');
    s += kabel('M21 160 Q18 152 14 152', '#141414', '#3cb85c') + kabel('M39 160 Q42 154 50 152', '#7a5230');
    s += stecker(276, 166, 2) + stecker(330, 166, 2) + stecker(84, 166, 2) + stecker(30, 166, 2);
    // Hupe
    s += '<circle cx="180" cy="194" r="15" fill="#151719" stroke="#3a414a" stroke-width="2"/><circle cx="180" cy="194" r="9" fill="#26292d"/><circle cx="180" cy="194" r="3" fill="#59626e"/>';
    s += kabel('M207 194 Q214 180 230 170 L250 160', '#d32f2f', '#3cb85c') + kabel('M225 194 Q232 200 340 190', '#7a5230') + stecker(216, 194, 2);
    // Massepunkte
    s += masse(330, 120, -16) + masse(30, 120, 16);
    return s;
  }

  function box(b, st, meta) {
    let s = '<rect width="360" height="230" fill="url(#motorraum)"/>';
    s += '<rect x="26" y="16" width="308" height="198" rx="12" fill="url(#plastik)" stroke="#0b0d10" stroke-width="2"/><rect x="34" y="24" width="292" height="182" rx="8" fill="#121519"/>';
    s += txt(180, 40, 'E-Box Motorraum', { s: 8.5, f: '#9fb0c8' });
    // Dummy-Maxisicherungen und Relais
    ['#2fa84f', '#f2c230', '#e9e9e9', '#2f6fd6'].forEach((c, i) => { s += '<rect x="' + (132 + i * 14) + '" y="160" width="12" height="26" rx="2" fill="' + c + '" opacity=".85"/>'; });
    s += '<rect x="280" y="80" width="34" height="34" rx="4" fill="#1d2126" stroke="#3a414a"/>' + txt(297, 100, 'K3', { s: 7, f: '#59626e' });
    s += '<rect x="280" y="124" width="34" height="34" rx="4" fill="#1d2126" stroke="#3a414a"/>' + txt(297, 144, 'K9', { s: 7, f: '#59626e' });
    s += sicherungBlatt(90, 101, '#2f6fd6', meta.gezogen.F15, st.sich.F15 === 'durch', '15') + txt(90, 86, 'F15', { s: 7, f: '#9fb0c8' });
    if (st.relais.K7) {
      s += '<rect x="196" y="76" width="64" height="64" rx="5" fill="#07090b" stroke="#3a414a"/>';
      [[210, 90], [246, 90], [210, 126], [246, 126]].forEach(([x, y]) => { s += '<rect x="' + (x - 6) + '" y="' + (y - 2) + '" width="12" height="4" fill="#c7a858"/>'; });
      s += txt(228, 154, 'Sockel K7 (Relais gezogen)', { s: 7 });
    } else {
      s += '<rect x="196" y="76" width="64" height="64" rx="6" fill="#1b1e22" stroke="#3a414a" stroke-width="2"/><rect x="202" y="82" width="52" height="52" rx="4" fill="#25292e"/>';
      s += txt(228, 104, 'K7', { s: 11, w: 800, f: '#cbd5e1' }) + txt(228, 116, '12V 30A', { s: 6, f: '#7d8a9a' }) + txt(228, 128, '30 85 86 87', { s: 5.5, f: '#7d8a9a' });
    }
    return s;
  }

  function tuer(b, st) {
    const fp = st.fensterPos;
    let s = '<rect width="360" height="230" fill="#161b22"/>';
    s += '<path d="M40 30 H332 V212 H54 Z" fill="#4a5560" stroke="#2a3138" stroke-width="2"/><path d="M48 38 H324 V204 H60 Z" fill="url(#lochblech)" opacity=".9"/>';
    s += '<rect x="70" y="40" width="250" height="' + (12 + 40 * (100 - fp) / 100) + '" fill="url(#glas)" opacity=".85"/>';
    s += '<path d="M226 40 V200 M296 40 V200" stroke="#2a3138" stroke-width="5"/>';
    // Türübergang
    s += '<path d="M6 64 q16 8 0 16 q16 8 0 16 q16 8 0 16 q16 8 0 16 q16 8 0 16" fill="none" stroke="#111418" stroke-width="10" stroke-linecap="round"/>' + txt(20, 160, 'Tür-', { s: 7 }) + txt(22, 169, 'übergang', { s: 7 });
    // Leitungen
    s += kabel('M14 90 Q40 120 70 124', '#141414', null, 6);
    s += kabel('M128 132 Q170 196 253 200', '#2f6fd6') + kabel('M150 132 Q190 186 271 190', '#2f6fd6', '#f0f0f0');
    // Türsteuergerät
    s += '<rect x="70" y="100" width="90" height="46" rx="6" fill="url(#grau)" stroke="#5b6470"/><rect x="112" y="136" width="44" height="8" rx="2" fill="#f5f7fa"/>' + txt(134, 142.5, 'A20 TSG', { s: 6, w: 800, f: '#1a1f26' });
    s += '<rect x="76" y="118" width="82" height="14" rx="2" fill="#2b3139"/>';
    // Motor mit Getriebe
    s += '<circle cx="262" cy="110" r="26" fill="#1f2328" stroke="#0b0d10" stroke-width="2"/><circle cx="262" cy="110" r="14" fill="#2c3137"/><rect x="236" y="130" width="52" height="22" rx="5" fill="#2c3137" stroke="#0b0d10"/>' + txt(262, 114, 'M20', { s: 9, w: 800 });
    s += stecker(262, 166, 2);
    return s;
  }

  function rueckleuchte(b, st, links) {
    let s = '<rect width="360" height="230" fill="#161b22"/><path d="M0 200 H360 V230 H0 Z" fill="#20262e"/>' + txt(300, 222, 'Kofferraumboden', { s: 7, f: '#6d7a8a' });
    s += '<path d="M106 40 H274 Q282 40 282 48 V146 Q282 154 274 154 H106 Q98 154 98 146 V48 Q98 40 106 40 Z" fill="url(#plastik)" stroke="#0b0d10" stroke-width="2"/>' + txt(190, 34, 'Lampenträger', { s: 8 });
    const sockel = (x, glas, txtS) => '<circle cx="' + x + '" cy="90" r="22" fill="#121519" stroke="#3a414a" stroke-width="2"/>' +
      '<path d="M' + (x - 9) + ' 100 Q' + (x - 14) + ' 70 ' + x + ' 68 Q' + (x + 14) + ' 70 ' + (x + 9) + ' 100 Z" fill="' + glas + '" opacity=".9" stroke="#bbb"/><path d="M' + (x - 4) + ' 92 q4 -10 8 0" stroke="#7a6a50" stroke-width="1.4" fill="none"/>' +
      '<rect x="' + (x - 9) + '" y="100" width="18" height="8" rx="2" fill="url(#chrom)"/>' + txt(x, 124, txtS, { s: 7.5 });
    s += sockel(150, '#ffbe55', 'Blinker PY21W') + sockel(230, '#f3f3f3', 'Bremslicht P21W');
    s += '<path d="M150 108 V136 M230 108 V136 M160 146 H220" stroke="#c7a858" stroke-width="2"/>';
    s += kabel('M172 186 Q160 205 120 212 L40 214', '#141414', '#f0f0f0') + kabel('M190 186 Q186 206 130 218', '#141414', '#d32f2f') + kabel('M208 186 Q230 200 300 200', '#7a5230');
    s += stecker(190, 172, 3);
    s += masse(320, 200, -16);
    return s;
  }

  function zeichne(ansicht, st, meta, b) {
    switch (ansicht) {
      case 'vorne': return vorne(b);
      case 'hinten': return hinten(b);
      case 'links': return seite(b, st, meta, false);
      case 'rechts': return seite(b, st, meta, true);
      case 'innen': return innen(b, st);
      case 'fussraum': return fussraum(b, st);
      case 'sk': return sk(b, st, meta);
      case 'motorraum': return motorraum(b, st);
      case 'box': return box(b, st, meta);
      case 'tuer': return tuer(b, st);
      case 'rlL': return rueckleuchte(b, st, true);
      case 'rlR': return rueckleuchte(b, st, false);
    }
    return '';
  }

  return { DEFS, zeichne };
})();
if (typeof module !== 'undefined') module.exports = DiagnoseGrafik;
