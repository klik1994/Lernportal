const test = require('node:test');
const assert = require('node:assert');
const D = require('../js/diagnose.js');

const an = (st, x) => { D.bediene(st, Object.assign({ zuendung: true }, x)); return D.beobachte(st); };
const codes = (st, sg) => st.speicher[sg].map(c => c.code);
const nah = (a, b, t = 0.3) => assert.ok(Math.abs(a - b) <= t, a + ' ≈ ' + b);

test('Ohne Fehler: alles funktioniert, Fehlerspeicher leer', () => {
  const st = D.neu(null);
  let b = an(st, { licht: 'abblend' }); assert.ok(b.abl > 0.8 && b.abr > 0.8);
  b = an(st, { licht: 'aus', blinker: 'links' }); assert.ok(b.blvl > 0.8 && b.blhl > 0.8 && !b.schnellL);
  b = an(st, { blinker: 'aus', bremse: true }); assert.ok(b.brl > 0.8 && b.brr > 0.8);
  b = an(st, { bremse: false, hupe: true }); assert.ok(b.hupe);
  b = an(st, { hupe: false, fenster: 'ab' }); assert.strictEqual(b.motor, 'ab'); assert.strictEqual(st.fensterPos, 100);
  ['A10', 'A20', 'J1'].forEach(sg => assert.deepStrictEqual(st.speicher[sg], [], sg));
  assert.ok(!Object.keys(st.sich).length);
});

test('Abblendlicht links: aus, Code Unterbrechung, 12 V am SG, 0 V am Stecker, Leitung OL', () => {
  const st = D.neu('abblend');
  assert.ok(codes(st, 'A10').includes('B1A12-13'));
  const b = an(st, { licht: 'abblend' }); assert.ok(b.abl < 0.05 && b.abr > 0.8);
  nah(D.spannung(st, 'A10.12', 'M').wert, 12.6);
  nah(D.spannung(st, 'X4.1', 'M').wert, 0);
  D.bediene(st, { batterie: false });
  assert.strictEqual(D.widerstand(st, 'A10.12', 'X4.1').wert, Infinity);
  D.bediene(st, { batterie: true });
  assert.ok(D.pruefe(st, 'w-abl', 'unterbrechung').richtig);
});

test('Bremslicht: Schalter-Istwert bleibt "nicht betätigt", P0504, Stellglied lässt Lampen leuchten', () => {
  const st = D.neu('bremslicht');
  assert.ok(codes(st, 'J1').includes('P0504'));
  let b = an(st, { bremse: true }); assert.ok(b.brl < 0.05);
  assert.strictEqual(D.istwerte(st, 'A10').find(x => x[0] === 'Bremslichtschalter')[1], 'nicht betätigt');
  nah(D.spannung(st, 'X12.1', 'M').wert, 12.6);
  nah(D.spannung(st, 'X12.2', 'M').wert, 0);
  b = D.stellglied(st, 'A10', 'br', true); assert.ok(b.brl > 0.8);
  D.stellglied(st, 'A10', 'br', false);
  assert.ok(D.pruefe(st, 's5', 'defekt').richtig);
  assert.ok(D.pruefe(st, 's5', 'unterbrechung').richtig);
});

test('Blinker: hinten links dunkel, schnelles Blinken, Lampenausfall, Lampe OL', () => {
  const st = D.neu('blinker');
  assert.ok(codes(st, 'A10').includes('B1C20-1B'));
  const b = an(st, { blinker: 'links' }); assert.ok(b.blvl > 0.8 && b.blhl < 0.05 && b.schnellL);
  const u = D.spannung(st, 'X30.2', 'X30.4');
  nah(u.wert, 12.6); nah(u.wechsel, 0);
  D.bediene(st, { stecker: { X30: true } });
  assert.strictEqual(D.widerstand(st, 'X30.2*', 'X30.4*').wert, Infinity);
  assert.ok(D.pruefe(st, 'e-blhl', 'defekt').richtig);
});

test('Hupe: F15 schon durch, neue Sicherung brennt beim Hupen wieder durch, Leitung hat Masseschluss', () => {
  const st = D.neu('hupe');
  assert.strictEqual(st.sich.F15, 'durch');
  assert.deepStrictEqual(st.speicher.A10, []);
  delete st.sich.F15;
  let b = an(st, {}); assert.ok(!st.sich.F15, 'ohne Hupen hält sie');
  b = an(st, { hupe: true }); assert.ok(!b.hupe); assert.strictEqual(st.sich.F15, 'durch');
  D.bediene(st, { hupe: false, relais: { K7: 'raus' } });
  nah(D.widerstand(st, 'K7.87', 'M').wert, 0, 0.1);
  const r = D.pruefe(st, 'F15', 'defekt'); assert.ok(!r.richtig); assert.ok(r.hinweis);
  assert.ok(D.pruefe(st, 'w-hupe', 'masse').richtig);
});

test('Fensterheber: Motor bewegt sich nicht, Code, Spannung am SG ja, am Motorstecker nein', () => {
  const st = D.neu('fenster');
  assert.ok(codes(st, 'A20').includes('B1F20-13'));
  const b = an(st, { fenster: 'ab' }); assert.strictEqual(b.motor, null); assert.strictEqual(st.fensterPos, 0);
  nah(D.spannung(st, 'A20.M2', 'M').wert, 12.6);
  nah(D.spannung(st, 'X20.2', 'M').wert, 12.6);
  D.bediene(st, { fenster: 'auf' });
  nah(D.spannung(st, 'A20.M1', 'M').wert, 12.6, 0.4);
  nah(D.spannung(st, 'X20.1', 'M').wert, 0, 0.4);
  assert.ok(D.pruefe(st, 'w-fh1', 'unterbrechung').richtig);
});

test('Widerstand unter Spannung wird verweigert, Tester braucht Zündung', () => {
  const st = D.neu('abblend');
  D.bediene(st, { zuendung: true });
  assert.ok(D.widerstand(st, 'F21.2', 'M').fremd);
  D.bediene(st, { zuendung: false });
  assert.ok(D.testerVerbindung(st));
  D.bediene(st, { zuendung: true });
  assert.strictEqual(D.testerVerbindung(st), '');
  D.loescheSpeicher(st, 'A10'); assert.deepStrictEqual(st.speicher.A10, []);
  D.bediene(st, { licht: 'abblend' }); assert.ok(codes(st, 'A10').includes('B1A12-13'));
});
