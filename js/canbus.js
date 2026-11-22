const CanBus = (() => {
  const BIT_US = 2;
  const MUSTER = '1111111111' + '0100110100010110010111000101101' + '1111111' + '0110100100110001011010011101' + '111111111111' + '01011001011100100110100101100' + '1111111111' + '01101001101001011100010110' + '11111111111111' + '010011010001011001011100010110110100110' + '1111111111111111111111111111111111111111111111111111111111111111111111111';
  const OL = Infinity;
  const W = (o) => Object.assign({ '6-14': 60, '6-4': OL, '14-4': OL, '6-16': OL, '14-16': OL }, o || {});

  const DATEN = {
    normal: { name: 'Kein Fehler', h: [2.5, 3.5], l: [2.5, 1.5], widerstand: W(),
      erklaerung: 'So sieht ein gesunder High-Speed-CAN aus: Im Ruhezustand (rezessiv) liegen beide Leitungen bei 2,5 V. Bei einem dominanten Bit steigt CAN-High auf 3,5 V und CAN-Low fällt auf 1,5 V. Die Bilder sind spiegelbildlich, die Differenzspannung beträgt 2 V. Zwischen Pin 6 und Pin 14 misst man 60 Ω, weil die beiden 120-Ω-Abschlusswiderstände parallel liegen.' },
    'h-masse': { name: 'CAN-High Kurzschluss nach Masse', h: [0, 0], l: [2.3, 1.5], widerstand: W({ '6-4': 0 }),
      erklaerung: 'CAN-High liegt dauerhaft auf 0 V und kann keine dominanten Bits mehr senden. CAN-Low pendelt weiter zwischen etwa 2,5 und 1,5 V. Mit Zündung aus und abgeklemmter Batterie misst man zwischen Pin 6 und Pin 4 (Masse) 0 Ω.' },
    'l-masse': { name: 'CAN-Low Kurzschluss nach Masse', h: [2.5, 3.5], l: [0, 0], widerstand: W({ '14-4': 0 }),
      erklaerung: 'CAN-Low liegt dauerhaft auf 0 V. CAN-High pendelt noch zwischen etwa 2,5 und 3,5 V, die Kommunikation ist aber gestört. Zwischen Pin 14 und Pin 4 (Masse) misst man 0 Ω.' },
    'h-plus': { name: 'CAN-High Kurzschluss nach Plus', h: [12, 12], l: [2.5, 1.5], widerstand: W({ '6-16': 0 }),
      erklaerung: 'CAN-High liegt dauerhaft auf Batteriespannung (ca. 12 V). Beim Messbereich 1 V/div läuft das Signal oben aus dem Bild, darum den Messbereich auf 5 V/div vergrößern. Zwischen Pin 6 und Pin 16 (Plus) misst man 0 Ω.' },
    'l-plus': { name: 'CAN-Low Kurzschluss nach Plus', h: [2.5, 3.5], l: [12, 12], widerstand: W({ '14-16': 0 }),
      erklaerung: 'CAN-Low liegt dauerhaft auf Batteriespannung (ca. 12 V), CAN-High pendelt weiter zwischen 2,5 und 3,5 V. Zwischen Pin 14 und Pin 16 (Plus) misst man 0 Ω.' },
    'h-l': { name: 'CAN-High und CAN-Low miteinander kurzgeschlossen', h: [2.5, 2.5], l: [2.5, 2.5], widerstand: W({ '6-14': 0 }), zitter: 0.12,
      erklaerung: 'Beide Leitungen haben dieselbe Spannung um 2,5 V, die Differenzspannung ist 0 V. Es gibt keine dominanten Bits mehr, der ganze Bus fällt aus. Zwischen Pin 6 und Pin 14 misst man statt 60 Ω nur noch 0 Ω.' },
    'r-einer': { name: 'Ein Abschlusswiderstand fehlt', h: [2.5, 3.5], l: [2.5, 1.5], widerstand: W({ '6-14': 120 }), ring: 0.45, tau: 0.25,
      erklaerung: 'Die Pegel stimmen, aber an den Flanken entstehen Überschwinger, weil das Signal am offenen Leitungsende reflektiert wird. Zwischen Pin 6 und Pin 14 misst man 120 Ω statt 60 Ω, es wirkt nur noch ein Abschlusswiderstand. Häufig sporadische Kommunikationsfehler.' },
    'r-beide': { name: 'Beide Abschlusswiderstände fehlen', h: [2.5, 3.5], l: [2.5, 1.5], widerstand: W({ '6-14': OL }), ring: 1.0, tau: 0.45, langsam: 1.2,
      erklaerung: 'Starke Überschwinger an jeder Flanke, und nach einem dominanten Bit kehren die Leitungen nur langsam auf 2,5 V zurück, weil nichts sie zusammenzieht. Zwischen Pin 6 und Pin 14 misst man OL (keine Verbindung).' },
    'h-unterbr': { name: 'CAN-High unterbrochen', h: [2.5, 2.95], l: [2.5, 1.5], widerstand: W({ '6-14': 120 }), luecken: true,
      erklaerung: 'CAN-High erreicht die 3,5 V nicht mehr und zeigt nur schwache, unvollständige Impulse, während CAN-Low normal arbeitet. Die Bilder sind nicht mehr spiegelbildlich. Zwischen Pin 6 und Pin 14 misst man 120 Ω, weil ein Abschlusswiderstand hinter der Unterbrechung liegt.' },
    'l-unterbr': { name: 'CAN-Low unterbrochen', h: [2.5, 3.5], l: [2.5, 2.05], widerstand: W({ '6-14': 120 }), luecken: true,
      erklaerung: 'CAN-Low erreicht die 1,5 V nicht mehr und zeigt nur schwache, unvollständige Impulse, während CAN-High normal arbeitet. Zwischen Pin 6 und Pin 14 misst man 120 Ω, weil ein Abschlusswiderstand hinter der Unterbrechung liegt.' }
  };

  const FEHLER = Object.keys(DATEN).filter(k => k !== 'normal').map(id => ({ id, name: DATEN[id].name }));
  const info = id => DATEN[id];

  function kurven(id, opt) {
    const d = DATEN[id];
    const zeitDiv = (opt && opt.zeitDiv) || 10;
    const dauer = zeitDiv * 10;
    const schritt = Math.max(0.02, dauer / 900);
    const pkt = [];
    const pegelH = dom => dom ? d.h[1] : d.h[0];
    const pegelL = dom => dom ? d.l[1] : d.l[0];
    const bitBei = t => MUSTER[Math.floor(t / BIT_US) % MUSTER.length] === '0';
    const kanteVorher = t => {
      const i = Math.floor(t / BIT_US);
      let k = i; while (k > 0 && (MUSTER[k % MUSTER.length] === '0') === (MUSTER[(k - 1) % MUSTER.length] === '0')) k--;
      return { seit: t - k * BIT_US, hoch: MUSTER[k % MUSTER.length] === '0', k };
    };
    const START = 16;
    for (let t0 = 0; t0 <= dauer + 1e-9; t0 += schritt) {
      const t = t0 + START;
      let dom = bitBei(t);
      const kv = kanteVorher(t);
      if (kv.k === 0) kv.seit = 1e3;
      if (d.luecken && dom && kv.k % 3 === 1) dom = false;
      let h = pegelH(dom), l = pegelL(dom);
      const flanke = Math.min(1, kv.seit / 0.08);
      if (kv.seit < 0.08) {
        h = pegelH(!dom) + (h - pegelH(!dom)) * flanke;
        l = pegelL(!dom) + (l - pegelL(!dom)) * flanke;
      }
      if (d.langsam && !dom) {
        const f = Math.exp(-kv.seit / d.langsam);
        h += (d.h[1] - d.h[0]) * 0.55 * f; l += (d.l[1] - d.l[0]) * 0.55 * f;
      }
      if (d.ring) {
        const a = d.ring * Math.exp(-kv.seit / d.tau) * Math.sin(2 * Math.PI * 4 * kv.seit);
        const richtung = dom ? 1 : -1;
        h += a * richtung; l -= a * richtung;
      }
      if (d.zitter) {
        const z = d.zitter * Math.exp(-kv.seit / 0.15) * (dom ? 1 : -1);
        h += z; l += z;
      }
      pkt.push([Math.round(t0 * 1000) / 1000, Math.round(h * 1000) / 1000, Math.round(l * 1000) / 1000]);
    }
    return pkt;
  }

  const widerstandText = r => r === Infinity ? 'OL' : r === 0 ? '0,0 Ω' : (Math.round(r) + ' Ω');

  function pruefe(fehler, antwort) {
    const richtig = fehler === antwort;
    return { richtig, rueckmeldung: richtig ? 'Richtig erkannt!' : 'Leider falsch.', erklaerung: DATEN[fehler].erklaerung };
  }

  return { BIT_US, FEHLER, info, kurven, widerstandText, pruefe };
})();
if (typeof module !== 'undefined') module.exports = CanBus;
