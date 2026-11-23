// Fiktive Schaltpläne des Übungsautos als SVG
const DiagnosePlan = (() => {
  const P = {
    Licht: {
      titel: 'Abblendlicht',
      box: { name: 'A10 Bordnetz-SG', cols: [0, 1], oben: { 0: 'T30a' }, unten: { 0: '12', 1: '13' } },
      cols: [
        { sich: ['F21', '20 A'], items: [['w', 'ge/sw 1,5'], ['p', 'X4/1'], ['lampe', 'E1 links'], ['p', 'X4/2'], ['w', 'br 1,5'], ['masse', 'M1']] },
        { ohneKopf: true, items: [['w', 'ge/ws 1,5'], ['p', 'X5/1'], ['lampe', 'E2 rechts'], ['p', 'X5/2'], ['w', 'br 1,5'], ['masse', 'M2']] }
      ],
      orte: [['F21', 'Sicherungskasten Innenraum'], ['A10', 'hinter der Abdeckung, Armaturenbrett links'], ['X4 / X5', 'Rückseite Scheinwerfer links / rechts, Motorraum'], ['M1 / M2', 'Längsträger links / rechts, Motorraum']]
    },
    Blinker: {
      titel: 'Blinker',
      box: { name: 'A10 Bordnetz-SG', cols: [0, 1, 2, 3], oben: { 0: 'T30b' }, unten: { 0: '20', 1: '20', 2: '21', 3: '21' } },
      cols: [
        { sich: ['F22', '15 A'], items: [['w', 'sw/ws 1'], ['p', 'X6/1'], ['lampe', 'E3 v. li.'], ['p', 'X6/2'], ['w', 'br 1'], ['masse', 'M1']] },
        { ohneKopf: true, items: [['w', 'sw/ws 1'], ['p', 'X30/2'], ['lampe', 'E5 h. li.'], ['p', 'X30/4'], ['w', 'br 1'], ['masse', 'M5']] },
        { ohneKopf: true, items: [['w', 'sw/gn 1'], ['p', 'X7/1'], ['lampe', 'E4 v. re.'], ['p', 'X7/2'], ['w', 'br 1'], ['masse', 'M2']] },
        { ohneKopf: true, items: [['w', 'sw/gn 1'], ['p', 'X31/2'], ['lampe', 'E6 h. re.'], ['p', 'X31/4'], ['w', 'br 1'], ['masse', 'M5']] }
      ],
      orte: [['F22', 'Sicherungskasten Innenraum'], ['X6 / X7', 'Blinker vorne, Motorraum'], ['X30 / X31', 'Rückleuchte links / rechts (Lampenträger)'], ['M5', 'Kofferraum, neben der Rückleuchte links']]
    },
    Bremslicht: {
      titel: 'Bremslicht',
      box: { name: 'A10 Bordnetz-SG', cols: [1, 2], unten: { 1: '24', 2: '24' }, oben: { 1: '40 (Eingang)' } },
      cols: [
        { sich: ['F8', '10 A'], items: [['w', 'rt 0,5'], ['p', 'X12/1'], ['schalter', 'S5'], ['p', 'X12/2'], ['w', 'sw/rt 0,5'], ['ende', '→ A10/40']] },
        { ohneKopf: true, items: [['w', 'sw/rt 1'], ['p', 'X30/3'], ['lampe', 'E7 links'], ['p', 'X30/4'], ['w', 'br 1'], ['masse', 'M5']] },
        { ohneKopf: true, items: [['w', 'sw/rt 1'], ['p', 'X31/3'], ['lampe', 'E8 rechts'], ['p', 'X31/4'], ['w', 'br 1'], ['masse', 'M5']] }
      ],
      orte: [['F8', 'Sicherungskasten Innenraum'], ['S5 / X12', 'Bremslichtschalter am Pedalbock, Fußraum'], ['X30 / X31', 'Rückleuchten (Lampenträger)'], ['M5', 'Kofferraum']]
    },
    Hupe: {
      titel: 'Hupe',
      box: { name: 'K7 Hupenrelais', cols: [0, 1], oben: { 0: '86', 1: '30' }, unten: { 0: '85', 1: '87' } },
      cols: [
        { sich: ['F15', '15 A'], items: [['w', 'gn 0,5'], ['schalter', 'S10 Taster'], ['w', 'br 0,5'], ['masse', 'M3']] },
        { abzweig: 0, items: [['w', 'rt/gn 1,5'], ['p', 'X9/1'], ['hupe', 'H1'], ['p', 'X9/2'], ['w', 'br 1,5'], ['masse', 'M1']] }
      ],
      orte: [['F15 / K7', 'Sicherungs- und Relaisbox im Motorraum'], ['S10', 'Lenkrad'], ['X9 / H1', 'hinter dem Stoßfänger, Mitte (von oben im Motorraum)'], ['M1', 'Längsträger links'], ['M3', 'A-Säule links']]
    },
    Fensterheber: {
      titel: 'Fensterheber Fahrer',
      box: { name: 'A20 Türsteuergerät', cols: [0, 1], oben: { 0: '30' }, unten: { 0: 'M1', 1: '31' } },
      cols: [
        { sich: ['F30', '25 A'], items: [['w', 'bl 2,5 (Türübergang)'], ['p', 'X20/1'], ['motor', 'M20'], ['p', 'X20/2'], ['w', 'bl/ws 2,5 (Türübergang)'], ['ende', '→ A20/M2']] },
        { ohneKopf: true, items: [['w', 'br 2,5'], ['masse', 'M3']] }
      ],
      orte: [['F30', 'Sicherungskasten Innenraum'], ['A20', 'in der Fahrertür hinter der Verkleidung'], ['X20 / M20', 'Fensterhebermotor in der Fahrertür'], ['Türübergang', 'Gummitülle zwischen Tür und A-Säule']]
    }
  };

  function svg(sys) {
    const p = P[sys], n = p.cols.length, W = Math.max(320, n * 90 + 20), dx = (W - 20) / n;
    const x = i => 10 + dx * (i + 0.5);
    const maxItems = Math.max(...p.cols.map(c => c.items.length));
    const yBox = 92, yStart = p.box ? 132 : 70, step = 34, H = yStart + maxItems * step + 10;
    const T = (xx, yy, t, anchor, size, col) => '<text x="' + xx + '" y="' + yy + '" text-anchor="' + (anchor || 'middle') + '" font-size="' + (size || 10) + '" fill="' + (col || 'currentColor') + '">' + t + '</text>';
    let s = '<svg class="plan" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Schaltplan ' + p.titel + '" style="color:var(--txt)">';
    s += '<line x1="6" y1="14" x2="' + (W - 6) + '" y2="14" stroke="#f05e4e" stroke-width="2.5"/>' + T(8, 10, '30 (Batterie +)', 'start', 10, '#f05e4e');
    p.cols.forEach((c, i) => {
      const cx = x(i);
      if (c.sich) {
        s += '<line x1="' + cx + '" y1="14" x2="' + cx + '" y2="' + (p.box ? yBox : yStart) + '" stroke="currentColor" stroke-width="1.6"/>';
        s += '<rect x="' + (cx - 8) + '" y="34" width="16" height="26" rx="2" fill="var(--card)" stroke="currentColor" stroke-width="1.6"/><line x1="' + cx + '" y1="38" x2="' + cx + '" y2="56" stroke="currentColor" stroke-width="1"/>';
        s += T(cx + 12, 46, c.sich[0], 'start', 10, '#f7b612') + T(cx + 12, 58, c.sich[1], 'start', 9);
      }
      if (c.abzweig !== undefined) {
        const ax = x(c.abzweig);
        s += '<path d="M' + ax + ' 70 H' + cx + ' V' + yBox + '" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="' + ax + '" cy="70" r="2.5" fill="currentColor"/>';
      }
    });
    if (p.box) {
      const b = p.box, x0 = x(b.cols[0]) - dx / 2 + 6, x1 = x(b.cols[b.cols.length - 1]) + dx / 2 - 6;
      s += '<rect x="' + x0 + '" y="' + yBox + '" width="' + (x1 - x0) + '" height="26" rx="4" fill="var(--card2)" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 3"/>' + T((x0 + x1) / 2, yBox + 17, b.name, 'middle', 11);
      Object.keys(b.oben || {}).forEach(i => { s += T(x(+i) + 4, yBox - 3, b.oben[i], 'start', 9, '#7fb0ff'); });
      Object.keys(b.unten || {}).forEach(i => { s += T(x(+i) + 4, yBox + 37, b.unten[i], 'start', 9, '#7fb0ff'); });
    }
    p.cols.forEach((c, i) => {
      const cx = x(i);
      let y = p.box ? yBox + 26 : yStart - 10;
      c.items.forEach(([t, l], k) => {
        const y0 = y, y1 = (p.box ? yStart : yStart) + k * step + step - 4;
        const mid = (y0 + y1) / 2;
        const linie = (a, b2) => '<line x1="' + cx + '" y1="' + a + '" x2="' + cx + '" y2="' + b2 + '" stroke="currentColor" stroke-width="1.6"/>';
        if (t === 'w') s += linie(y0, y1) + T(cx + 6, mid + 3, l, 'start', 9, 'var(--muted)');
        else if (t === 'p') s += linie(y0, y1) + '<circle cx="' + cx + '" cy="' + mid + '" r="4" fill="var(--card)" stroke="#34c778" stroke-width="2"/>' + T(cx + 8, mid + 3, l, 'start', 10, '#34c778');
        else if (t === 'lampe') s += linie(y0, mid - 9) + linie(mid + 9, y1) + '<circle cx="' + cx + '" cy="' + mid + '" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M' + (cx - 6) + ' ' + (mid - 6) + 'L' + (cx + 6) + ' ' + (mid + 6) + 'M' + (cx + 6) + ' ' + (mid - 6) + 'L' + (cx - 6) + ' ' + (mid + 6) + '" stroke="currentColor" stroke-width="1.4"/>' + T(cx + 13, mid + 3, l, 'start', 9);
        else if (t === 'motor') s += linie(y0, mid - 10) + linie(mid + 10, y1) + '<circle cx="' + cx + '" cy="' + mid + '" r="10" fill="none" stroke="currentColor" stroke-width="1.6"/>' + T(cx, mid + 4, 'M', 'middle', 11) + T(cx + 14, mid + 3, l, 'start', 9);
        else if (t === 'hupe') s += linie(y0, mid - 8) + linie(mid + 8, y1) + '<path d="M' + (cx - 8) + ' ' + (mid - 8) + 'h16v16h-16z M' + (cx - 12) + ' ' + (mid + 12) + 'L' + (cx + 12) + ' ' + (mid + 12) + '" fill="none" stroke="currentColor" stroke-width="1.6"/>' + T(cx + 14, mid + 3, l, 'start', 9);
        else if (t === 'schalter') s += linie(y0, mid - 8) + linie(mid + 8, y1) + '<line x1="' + cx + '" y1="' + (mid + 8) + '" x2="' + (cx + 9) + '" y2="' + (mid - 7) + '" stroke="currentColor" stroke-width="1.8"/>' + T(cx + 13, mid + 3, l, 'start', 9);
        else if (t === 'masse') s += linie(y0, mid) + '<path d="M' + (cx - 9) + ' ' + mid + 'h18 M' + (cx - 6) + ' ' + (mid + 4) + 'h12 M' + (cx - 3) + ' ' + (mid + 8) + 'h6" stroke="currentColor" stroke-width="1.6"/>' + T(cx + 12, mid + 3, l, 'start', 10, '#94a4ba');
        else if (t === 'ende') s += linie(y0, mid) + T(cx, mid + 13, l, 'middle', 10, '#7fb0ff');
        y = y1;
      });
    });
    return s + '</svg>';
  }

  return { PLAENE: P, SYSTEME: Object.keys(P), svg };
})();
if (typeof module !== 'undefined') module.exports = DiagnosePlan;
