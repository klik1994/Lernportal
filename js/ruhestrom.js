// Ruhestrom-Fehlersuche: reine Logik, ohne Oberfläche.
const Ruhestrom = (() => {
  const SCHLAF_MIN = 20;   // Busruhe nach so vielen Minuten
  const GRENZE = 50;       // Herstellervorgabe in mA (in dieser Übung)
  const MA_MAX = 400;      // Sicherung der mA-Buchse im Messgerät
  const GRUND = 6;         // Batteriesensor/Uhr, nicht im Sicherungskasten

  // ungefährer Kaltwiderstand von Flachsicherungen in mΩ (je nach Hersteller etwas anders)
  const R_MOHM = { 5: 15, 7.5: 9.7, 10: 7.4, 15: 4.2, 20: 3.1, 25: 2.4, 30: 2 };
  const FARBE = { 5: '#d9b77e', 7.5: '#8a5a2b', 10: '#d8382c', 15: '#2f6fd6', 20: '#f2c230', 25: '#e9e9e9', 30: '#2fa84f' };

  const SICHERUNGEN = [
    { id: 'F1', a: 15, name: 'Radio / Infotainment', schlaf: 3, wach: 900 },
    { id: 'F2', a: 10, name: 'Innenleuchten', schlaf: 0, wach: 0 },
    { id: 'F3', a: 7.5, name: 'Kofferraumleuchte', schlaf: 0, wach: 0 },
    { id: 'F4', a: 10, name: 'Komfortsteuergerät (ZV, Alarm)', schlaf: 12, wach: 250 },
    { id: 'F5', a: 15, name: 'Anhängersteuergerät', schlaf: 1, wach: 60 },
    { id: 'F6', a: 20, name: '12-V-Steckdose', schlaf: 0, wach: 0 },
    { id: 'F7', a: 5, name: 'Handschuhfachleuchte', schlaf: 0, wach: 0 },
    { id: 'F8', a: 5, name: 'Kombiinstrument', schlaf: 4, wach: 180 },
    { id: 'F9', a: 10, name: 'Gateway / Diagnose', schlaf: 5, wach: 150 },
    { id: 'F10', a: 15, name: 'Motorsteuergerät', schlaf: 2, wach: 300 }
  ];

  const FEHLER = [
    { id: 'kein', sicherung: null, extra: 0, kunde: 'Die Batterie war nach drei Wochen Urlaub leer. Der Kunde will wissen, ob am Auto etwas nicht stimmt.',
      erklaerung: 'Der Ruhestrom liegt nach der Busruhe bei gut 30 mA und damit unter der Vorgabe. Nach drei Wochen Standzeit ist eine leere Batterie normal. Batterie laden und prüfen.' },
    { id: 'handschuh', sicherung: 'F7', extra: 300, kunde: 'Nach zwei Tagen Standzeit springt das Auto nicht mehr an.',
      erklaerung: 'Der Schalter der Handschuhfachleuchte ist defekt, die Lampe brennt dauernd. Rund 300 mA leeren die Batterie in wenigen Tagen.' },
    { id: 'radio', sicherung: 'F1', extra: 220, kunde: 'Seit dem Radiotausch ist die Batterie jeden Montag leer.',
      erklaerung: 'Das nachgerüstete Radio hängt am Dauerplus und schaltet nicht ab. Abhilfe: Radio richtig anschließen (Zündungsplus bzw. Adapter).' },
    { id: 'dongle', sicherung: 'F6', extra: 150, kunde: 'Die Batterie ist öfter leer, seit ein Ortungsgerät im Auto steckt.',
      erklaerung: 'Ein Gerät in der 12-V-Steckdose (Dauerplus) zieht dauernd Strom. Gerät abziehen oder an eine geschaltete Steckdose.' },
    { id: 'kofferraum', sicherung: 'F3', extra: 420, kunde: 'Über Nacht ist die Batterie leer, vorher war alles in Ordnung.',
      erklaerung: 'Der Schalter im Heckklappenschloss meldet „offen“, die Kofferraumleuchte bleibt an. Schloss bzw. Schalter prüfen.' },
    { id: 'anhaenger', sicherung: 'F5', extra: 0, buswach: true, kunde: 'Seit die Anhängerkupplung nachgerüstet wurde, ist die Batterie nach einem Tag leer.',
      erklaerung: 'Das Anhängersteuergerät hält den CAN-Bus wach, deshalb schlafen die anderen Steuergeräte nie ein. Der Strom bleibt hoch, bis diese Sicherung gezogen ist. Codierung bzw. Einbau prüfen.' }
  ];

  const info = id => FEHLER.find(f => f.id === id);
  const sicherung = id => SICHERUNGEN.find(s => s.id === id);

  function neu(fehlerId) {
    return { fehler: fehlerId, minuten: 0, gezogen: [], haube: false, anschluss: null, buchse: '10A', geraetDefekt: '', geweckt: 0, wartezeit: 0 };
  }

  function wach(st) {
    const f = info(st.fehler);
    if (f.buswach && !st.gezogen.includes(f.sicherung)) return true;
    if (!st.haube) return true;
    return st.minuten < SCHLAF_MIN;
  }

  // Strom durch eine Sicherung in mA
  function stromSicherung(st, id) {
    if (st.gezogen.includes(id)) return 0;
    const s = sicherung(id), f = info(st.fehler);
    return (wach(st) ? s.wach : s.schlaf) + (f.sicherung === id ? f.extra : 0);
  }

  // Strom aus der Batterie in mA
  function strom(st) {
    return GRUND + SICHERUNGEN.reduce((sum, s) => sum + stromSicherung(st, s.id), 0);
  }

  function warte(st, min) { st.minuten += min; st.wartezeit += min; return st; }

  function ziehe(st, id) {
    if (st.gezogen.includes(id)) {           // wieder einstecken weckt den Bus
      const schlief = !wach(st);
      st.gezogen = st.gezogen.filter(x => x !== id);
      if (schlief) st.geweckt++;
      st.minuten = 0;
    } else st.gezogen.push(id);
    pruefeGeraet(st);
    return st;
  }

  function setzeHaube(st, zu) {
    if (st.haube !== zu) st.minuten = 0;     // Haube auf oder zu weckt das Fahrzeug
    st.haube = zu;
    return st;
  }

  function anschliessen(st, anschluss, buchse) {
    if (anschluss !== undefined) st.anschluss = anschluss;
    if (buchse !== undefined) st.buchse = buchse;
    pruefeGeraet(st);
    return st;
  }

  function pruefeGeraet(st) {
    if (st.geraetDefekt || !st.anschluss) return;
    if (st.anschluss === 'parallel') st.geraetDefekt = 'kurzschluss';
    else if (st.buchse === 'mA' && strom(st) > MA_MAX) st.geraetDefekt = 'ueberlast';
  }

  function geraetReparieren(st) { st.geraetDefekt = ''; st.anschluss = null; st.buchse = '10A'; return st; }

  // Was zeigt das Multimeter an?
  function anzeige(st) {
    if (!st.anschluss) return { text: '– – –', wert: null };
    if (st.geraetDefekt) return { text: st.buchse === 'mA' ? '0,0 mA' : '0,00 A', wert: 0 };
    const i = strom(st);
    if (st.buchse === '10A') return { text: (Math.round(i / 10) / 100).toFixed(2).replace('.', ',') + ' A', wert: Math.round(i / 10) * 10 };
    return { text: (Math.round(i * 10) / 10).toFixed(1).replace('.', ',') + ' mA', wert: Math.round(i * 10) / 10 };
  }

  // Spannungsfall über einer gesteckten Sicherung in mV (weckt nichts)
  function spannungsfall(st, id) {
    const mv = stromSicherung(st, id) * R_MOHM[sicherung(id).a] / 1000;
    return Math.round(mv * 10) / 10;
  }

  function pruefe(st, antwort) {
    const f = info(st.fehler);
    const loesung = f.sicherung || 'kein';
    return { richtig: antwort === loesung, loesung, erklaerung: f.erklaerung };
  }

  return { SCHLAF_MIN, GRENZE, MA_MAX, R_MOHM, FARBE, SICHERUNGEN, FEHLER, info, sicherung, neu, wach, strom, stromSicherung, warte, ziehe, setzeHaube, anschliessen, geraetReparieren, anzeige, spannungsfall, pruefe };
})();
if (typeof module !== 'undefined') module.exports = Ruhestrom;
