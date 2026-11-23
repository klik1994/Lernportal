const test = require('node:test');
const assert = require('node:assert');
const R = require('../js/ruhestrom.js');

const schlafend = id => { const st = R.neu(id); R.setzeHaube(st, true); R.warte(st, 30); return st; };

test('Ohne Fehler: nach Busruhe zwischen 20 und 50 mA, vorher deutlich über 1 A', () => {
  const st = R.neu('kein'); R.setzeHaube(st, true);
  assert.ok(R.strom(st) > 1000);
  R.warte(st, 15); assert.ok(R.wach(st));
  R.warte(st, 5); assert.ok(!R.wach(st));
  const i = R.strom(st); assert.ok(i >= 20 && i <= R.GRENZE, i);
});

test('Offene Motorhaube: Fahrzeug schläft nie ein', () => {
  const st = R.neu('kein'); R.warte(st, 60); assert.ok(R.wach(st));
  R.setzeHaube(st, true); assert.ok(R.wach(st), 'Haube schließen startet die Zeit neu');
  R.warte(st, 20); assert.ok(!R.wach(st));
});

test('Jeder Fehler: Ruhestrom über 100 mA, Ziehen der richtigen Sicherung bringt ihn unter die Grenze', () => {
  R.FEHLER.filter(f => f.sicherung).forEach(f => {
    const st = schlafend(f.id);
    assert.ok(R.strom(st) > 100, f.id + ' ' + R.strom(st));
    R.ziehe(st, f.sicherung);
    assert.ok(R.strom(st) <= R.GRENZE, f.id + ' nachher ' + R.strom(st));
  });
});

test('Falsche Sicherung ziehen ändert fast nichts, Wiedereinstecken weckt den Bus', () => {
  const st = schlafend('handschuh'); const vorher = R.strom(st);
  R.ziehe(st, 'F2'); assert.strictEqual(R.strom(st), vorher);
  R.ziehe(st, 'F2'); assert.ok(R.wach(st)); assert.strictEqual(st.geweckt, 1);
  assert.ok(R.strom(st) > 1000);
});

test('Bus-Wachhalter: Strom bleibt hoch, bis die Sicherung raus ist', () => {
  const st = schlafend('anhaenger'); assert.ok(R.wach(st)); assert.ok(R.strom(st) > 1000);
  R.ziehe(st, 'F5'); assert.ok(!R.wach(st)); assert.ok(R.strom(st) <= R.GRENZE);
});

test('Messgerät: parallel = Kurzschluss, mA-Buchse bei wachem Bus brennt durch, 10-A-Buchse grob', () => {
  let st = R.neu('kein'); R.anschliessen(st, 'parallel', '10A'); assert.strictEqual(st.geraetDefekt, 'kurzschluss');
  R.geraetReparieren(st); assert.strictEqual(st.geraetDefekt, '');
  R.anschliessen(st, 'reihe', 'mA'); assert.strictEqual(st.geraetDefekt, 'ueberlast');
  assert.strictEqual(R.anzeige(st).text, '0,0 mA');
  st = schlafend('kein'); R.anschliessen(st, 'reihe', '10A'); assert.strictEqual(R.anzeige(st).text, '0,03 A');
  R.anschliessen(st, undefined, 'mA'); assert.strictEqual(st.geraetDefekt, '');
  assert.match(R.anzeige(st).text, /^3\d,\d mA$/);
});

test('Spannungsfall: nur an der belasteten Sicherung messbar, gezogene zeigt 0', () => {
  const st = schlafend('handschuh');
  assert.ok(R.spannungsfall(st, 'F7') > 3);
  assert.ok(R.spannungsfall(st, 'F2') === 0);
  R.ziehe(st, 'F7'); assert.strictEqual(R.spannungsfall(st, 'F7'), 0);
});

test('Antwort prüfen', () => {
  assert.ok(R.pruefe(R.neu('radio'), 'F1').richtig);
  assert.ok(!R.pruefe(R.neu('radio'), 'kein').richtig);
  assert.ok(R.pruefe(R.neu('kein'), 'kein').richtig);
});
