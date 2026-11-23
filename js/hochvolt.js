// Spannungsfreiheit am HV-Fahrzeug herstellen: reine Logik, ohne Oberfläche.
const Hochvolt = (() => {
  // regel: Nummer der 5 Sicherheitsregeln, 0 = falscher oder nicht nötiger Schritt
  const SCHRITTE = [
    { id: 'zuendung', regel: 1, text: 'Zündung aus, Fahrzeugschlüssel außer Reichweite ablegen', warum: 'Ohne Schlüssel kann niemand das HV-System versehentlich einschalten (Keyless beachten).' },
    { id: 'stecker', regel: 1, text: 'Wartungsstecker (Service-Disconnect) ziehen', warum: 'Damit wird die HV-Batterie vom übrigen HV-Bordnetz getrennt: Freischalten.' },
    { id: 'schloss', regel: 2, text: 'Wartungsstecker und Schlüssel sicher verwahren, Vorhängeschloss anbringen', warum: 'Gegen Wiedereinschalten sichern: Nur du hast den Schlüssel zum Schloss.' },
    { id: 'schild', regel: 2, text: 'Warnschild „Arbeiten am HV-System“ und Warnhütchen aufstellen', warum: 'Alle in der Werkstatt sehen, dass an diesem Fahrzeug gearbeitet wird.' },
    { id: 'warten', regel: 3, text: 'Wartezeit nach Herstellerangabe abwarten (mindestens 10 Minuten)', warum: 'Die Kondensatoren in der Leistungselektronik müssen sich erst entladen.' },
    { id: 'vorher', regel: 3, text: 'Zweipoligen Spannungsprüfer an einer bekannten Spannungsquelle prüfen', warum: 'Funktionsprüfung vorher: Ein defekter Prüfer würde „spannungsfrei“ vortäuschen.' },
    { id: 'messen', regel: 3, text: 'Spannungsfreiheit messen: HV+ gegen HV−, HV+ gegen Masse, HV− gegen Masse', warum: 'Alle drei Kombinationen, sonst bleibt z. B. eine Spannung gegen die Karosserie unentdeckt.' },
    { id: 'nachher', regel: 3, text: 'Spannungsprüfer erneut an der bekannten Spannungsquelle prüfen', warum: 'Funktionsprüfung nachher: Der Prüfer könnte während der Messung kaputtgegangen sein.' },
    { id: 'doku', regel: 3, text: 'Spannungsfreiheit dokumentieren und am Fahrzeug kennzeichnen', warum: 'Protokoll nach Herstellervorgabe: Wer, wann, mit welchem Ergebnis.' },
    { id: 'erden', regel: 0, text: 'HV-Leitungen erden und kurzschließen', warum: 'Regel 4 ist am Serienfahrzeug in der Regel nicht anzuwenden. Nur wenn der Hersteller es ausdrücklich vorschreibt.' },
    { id: 'multimeter', regel: 0, text: 'Spannungsfreiheit mit einem einfachen Multimeter ohne CAT-III-Zulassung messen', warum: 'Nur zugelassene zweipolige Spannungsprüfer (meist CAT III) oder Herstellergeräte verwenden.' },
    { id: 'einpolig', regel: 0, text: 'Mit dem einpoligen Phasenprüfer an die HV-Leitung tippen', warum: 'Ein einpoliger Prüfer ist für Gleichspannung am HV-System ungeeignet und gefährlich.' },
    { id: 'sofort', regel: 0, text: 'Gleich nach dem Ziehen des Wartungssteckers mit der Arbeit anfangen', warum: 'Erst nach Wartezeit und Messung ist das System spannungsfrei. Vorher kann noch Spannung anliegen.' }
  ];

  // a muss vor b kommen
  const VORHER = [
    ['zuendung', 'stecker'], ['stecker', 'schloss'], ['stecker', 'schild'], ['stecker', 'warten'],
    ['schloss', 'messen'], ['schild', 'messen'], ['warten', 'messen'],
    ['vorher', 'messen'], ['messen', 'nachher'], ['nachher', 'doku']
  ];

  const schritt = id => SCHRITTE.find(s => s.id === id);
  const PFLICHT = SCHRITTE.filter(s => s.regel > 0).map(s => s.id);

  function pruefeReihenfolge(ids) {
    const fehler = [];
    ids.filter(id => schritt(id).regel === 0).forEach(id => fehler.push({ id, text: schritt(id).warum }));
    PFLICHT.filter(id => !ids.includes(id)).forEach(id => fehler.push({ id, fehlt: true, text: 'Es fehlt: ' + schritt(id).text + '. ' + schritt(id).warum }));
    const falschePos = new Set();
    VORHER.forEach(([a, b]) => {
      const ia = ids.indexOf(a), ib = ids.indexOf(b);
      if (ia >= 0 && ib >= 0 && ia > ib) {
        falschePos.add(b);
        fehler.push({ id: b, text: '„' + schritt(a).text + '“ muss vor „' + schritt(b).text + '“ kommen.' });
      }
    });
    return { ok: fehler.length === 0, fehler, falschePos: [...falschePos] };
  }

  // Messung mit dem zweipoligen Spannungsprüfer
  const PUNKTE = [['quelle', 'Bekannte Spannungsquelle (Prüfadapter)'], ['hv+hv-', 'HV+ gegen HV−'], ['hv+m', 'HV+ gegen Masse'], ['hv-m', 'HV− gegen Masse']];
  const SZENARIEN = [
    { id: 'frei', urteil: 'frei', erklaerung: 'Prüfer vorher und nachher in Ordnung, alle drei Messungen 0 V: Das System ist spannungsfrei, die Arbeit darf beginnen.' },
    { id: 'schuetz', urteil: 'nicht-frei', erklaerung: 'Zwischen HV+ und HV− liegen noch rund 390 V an, z. B. weil ein Schütz verklebt ist. Nicht arbeiten! Fahrzeug sichern und Fachkraft bzw. Hersteller hinzuziehen.' },
    { id: 'isolation', urteil: 'nicht-frei', erklaerung: 'HV+ gegen HV− zeigt 0 V, aber gegen Masse liegen etwa 160 V an: ein Isolationsfehler. Genau deshalb misst man alle drei Kombinationen. Nicht arbeiten!' },
    { id: 'pruefer-vorher', urteil: 'ungueltig', erklaerung: 'Der Prüfer zeigt schon an der bekannten Spannungsquelle nichts an. Er ist defekt, jede Messung damit ist wertlos. Prüfer tauschen und neu messen.' },
    { id: 'pruefer-nachher', urteil: 'ungueltig', erklaerung: 'Vorher hat der Prüfer funktioniert, bei der Prüfung danach zeigt er nichts mehr an. Die 0-V-Messungen sind deshalb nicht sicher. Mit einem intakten Prüfer wiederholen.' }
  ];
  const URTEILE = [['frei', 'Spannungsfrei: Arbeit darf beginnen'], ['nicht-frei', 'Nicht spannungsfrei: nicht arbeiten'], ['ungueltig', 'Messung ungültig: Prüfer defekt']];
  const QUELLE = 400;

  function neueMessung(id) { return { szenario: id, vorher: false, nachher: false, gemessen: [], log: [] }; }

  // Rückgabe: angezeigte Spannung in V oder null (Prüfer zeigt nichts)
  function messe(m, punkt) {
    const sz = m.szenario;
    let v;
    if (punkt === 'quelle') {
      const danach = m.gemessen.length > 0;
      if (danach) m.nachher = true; else m.vorher = true;
      const tot = sz === 'pruefer-vorher' || (sz === 'pruefer-nachher' && danach);
      v = tot ? null : QUELLE;
    } else {
      if (!m.gemessen.includes(punkt)) m.gemessen.push(punkt);
      if (sz === 'pruefer-vorher') v = null;
      else if (sz === 'schuetz') v = punkt === 'hv+hv-' ? 390 : 0;
      else if (sz === 'isolation') v = punkt === 'hv+hv-' ? 0 : 160;
      else v = 0;
    }
    m.log.push([punkt, v]);
    return v;
  }

  function bewerte(m, urteil) {
    const sz = SZENARIEN.find(s => s.id === m.szenario);
    const hinweise = [];
    if (urteil === 'frei') {
      if (!m.vorher) hinweise.push('Du hast den Prüfer vor der Messung nicht an der bekannten Spannungsquelle getestet.');
      if (m.gemessen.length < 3) hinweise.push('Es fehlen Messungen: Immer HV+ gegen HV−, HV+ gegen Masse und HV− gegen Masse.');
      if (!m.nachher) hinweise.push('Die Funktionsprüfung nach der Messung fehlt.');
    }
    const richtig = urteil === sz.urteil && hinweise.length === 0;
    return { richtig, hinweise, erklaerung: sz.erklaerung, loesung: sz.urteil };
  }

  return { SCHRITTE, VORHER, PFLICHT, PUNKTE, SZENARIEN, URTEILE, QUELLE, schritt, pruefeReihenfolge, neueMessung, messe, bewerte };
})();
if (typeof module !== 'undefined') module.exports = Hochvolt;
