// Bremsenprüfstand: reine Logik, ohne Oberfläche.
const Bremse = (() => {
  const G = 9.81;
  const MIN_BETRIEB = 58;   // % für M1 mit Erstzulassung ab 01.01.2012
  const MIN_FBA = 16;       // % Feststellbremse
  const MAX_DIFF = 25;      // % Bremskraftdifferenz je Achse

  // Kräfte in kN: Rollwiderstand (roll), Höchstwert (max), Schwankung je Radumdrehung (schw)
  const rad = (max, roll = 0.12, schw = 0.05) => ({ max, roll, schw });
  const BEFUNDE = [
    ['ok', 'Bremsanlage in Ordnung'],
    ['diff-va', 'Bremskraftdifferenz Vorderachse zu groß'],
    ['diff-ha', 'Bremskraftdifferenz Hinterachse zu groß'],
    ['schwach', 'Abbremsung der Betriebsbremse zu gering'],
    ['fba', 'Feststellbremse mangelhaft'],
    ['unrund', 'Bremskraft schwankt: Scheibe verzogen / unrund'],
    ['schleift', 'Bremse schleift (Rollwiderstand zu hoch)']
  ];
  const FAELLE = [
    { id: 'ok', masse: 1800, va: [rad(3.6), rad(3.5)], ha: [rad(1.9), rad(1.8)], fba: [1.6, 1.5],
      erklaerung: 'Differenz und Abbremsung liegen im grünen Bereich, keine Schwankung, normaler Rollwiderstand.' },
    { id: 'diff-va', masse: 1750, va: [rad(4.0), rad(2.8)], ha: [rad(1.9), rad(1.8)], fba: [1.5, 1.5],
      erklaerung: 'Das rechte Vorderrad bremst deutlich schwächer, das Auto zieht beim Bremsen nach links. Ursachen am schwächeren Rad suchen: festsitzender Kolben oder Führung, verölte Beläge, Bremsschlauch innen zu.' },
    { id: 'diff-ha', masse: 1650, va: [rad(3.4), rad(3.3)], ha: [rad(2.0), rad(1.2)], fba: [1.4, 1.3],
      erklaerung: 'Hinten rechts kommt zu wenig Bremskraft an. Typisch: festgegangener Sattel oder Radbremszylinder, verschlissene oder verglaste Beläge.' },
    { id: 'schwach', masse: 1900, va: [rad(3.0), rad(2.9)], ha: [rad(1.6), rad(1.5)], fba: [1.7, 1.6],
      erklaerung: 'Alle Räder bremsen gleichmäßig, aber insgesamt zu schwach. Typisch: verglaste Beläge, Bremsflüssigkeit mit Wasser oder Luft im System, defekter Bremskraftverstärker.' },
    { id: 'fba', masse: 1700, va: [rad(3.5), rad(3.4)], ha: [rad(1.8), rad(1.8)], fba: [1.0, 0.4],
      erklaerung: 'Die Feststellbremse erreicht die Mindestabbremsung nicht und zieht einseitig. Seilzug oder Betätigung prüfen bzw. elektrische Feststellbremse diagnostizieren.' },
    { id: 'unrund', masse: 1800, va: [rad(3.7, 0.12, 0.9), rad(3.6)], ha: [rad(1.9), rad(1.8)], fba: [1.6, 1.5],
      erklaerung: 'Die Bremskraft vorne links schwankt bei jeder Radumdrehung stark. Das deutet auf eine verzogene oder ungleich dicke Bremsscheibe hin (Bremsrubbeln). Scheibe auf Schlag und Dickentoleranz messen.' },
    { id: 'schleift', masse: 1750, va: [rad(3.6), rad(3.5)], ha: [rad(1.9), rad(1.8, 0.55)], fba: [1.5, 1.6],
      erklaerung: 'Schon ohne Pedal braucht hinten rechts der Prüfstand viel Kraft, um das Rad zu drehen: Die Bremse schleift (Kolben fest, Feststellbremse löst nicht). Das kostet Sprit und überhitzt die Bremse.' }
  ];

  const fall = id => FAELLE.find(f => f.id === id);
  const r1 = x => Math.round(x * 10) / 10;

  const differenz = (l, r) => Math.max(l, r) === 0 ? 0 : r1((Math.max(l, r) - Math.min(l, r)) / Math.max(l, r) * 100);
  const abbremsung = (summeKN, masseKG) => r1(summeKN * 1000 / (masseKG * G) * 100);
  const schwankung = r => r1(r.schw * 2 / r.max * 100);

  function auswertung(id) {
    const f = fall(id);
    const summe = f.va[0].max + f.va[1].max + f.ha[0].max + f.ha[1].max;
    return {
      gewichtskraft: Math.round(f.masse * G / 10) / 100,
      diffVA: differenz(f.va[0].max, f.va[1].max),
      diffHA: differenz(f.ha[0].max, f.ha[1].max),
      zBetrieb: abbremsung(summe, f.masse),
      zFBA: abbremsung(f.fba[0] + f.fba[1], f.masse),
      diffFBA: differenz(f.fba[0], f.fba[1]),
      summe: r1(summe)
    };
  }

  // Kraftverlauf eines Rades: t von 0 (Pedal los) bis 1 (Blockiergrenze), Phase in Radumdrehungen
  function kraft(r, t, phase) {
    if (t <= 0) return r.roll;
    const basis = r.roll + (r.max - r.roll) * Math.min(1, t);
    return Math.max(0, basis + r.schw * Math.min(1, t) * Math.sin(phase * 2 * Math.PI));
  }

  function pruefeWert(soll, ist, tol = 1.5) {
    const x = parseFloat(String(ist).replace(',', '.'));
    return !isNaN(x) && Math.abs(x - soll) <= tol;
  }

  function pruefeBefund(id, befund) {
    return { richtig: id === befund, loesung: id, erklaerung: fall(id).erklaerung };
  }

  return { G, MIN_BETRIEB, MIN_FBA, MAX_DIFF, BEFUNDE, FAELLE, fall, differenz, abbremsung, schwankung, auswertung, kraft, pruefeWert, pruefeBefund };
})();
if (typeof module !== 'undefined') module.exports = Bremse;
