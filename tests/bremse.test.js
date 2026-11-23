const test = require('node:test');
const assert = require('node:assert');
const B = require('../js/bremse.js');

// welche Grenzwerte verletzt ein Fall?
function maengel(id) {
  const a = B.auswertung(id), f = B.fall(id), m = [];
  if (a.diffVA > B.MAX_DIFF) m.push('diff-va');
  if (a.diffHA > B.MAX_DIFF) m.push('diff-ha');
  if (a.zBetrieb < B.MIN_BETRIEB) m.push('schwach');
  if (a.zFBA < B.MIN_FBA || a.diffFBA > 50) m.push('fba');
  if ([...f.va, ...f.ha].some(r => B.schwankung(r) > 20)) m.push('unrund');
  if ([...f.va, ...f.ha].some(r => r.roll > 0.4)) m.push('schleift');
  return m;
}

test('Formeln: Differenz und Abbremsung', () => {
  assert.strictEqual(B.differenz(4, 3), 25);
  assert.strictEqual(B.differenz(3, 4), 25);
  assert.strictEqual(B.abbremsung(10.3, 1800), 58.3);
  assert.strictEqual(B.auswertung('ok').gewichtskraft, 17.66);
});

test('Jeder Fall zeigt genau seinen eigenen Mangel', () => {
  B.FAELLE.forEach(f => {
    assert.deepStrictEqual(maengel(f.id), f.id === 'ok' ? [] : [f.id], f.id + ' ' + JSON.stringify(B.auswertung(f.id)));
    assert.ok(B.BEFUNDE.some(b => b[0] === f.id));
    assert.ok(f.erklaerung.length > 40);
  });
});

test('Kraftverlauf: Rollwiderstand ohne Pedal, Höchstwert an der Blockiergrenze', () => {
  const r = B.fall('ok').va[0];
  assert.strictEqual(B.kraft(r, 0, 0), r.roll);
  assert.ok(Math.abs(B.kraft(r, 1, 0) - r.max) < 1e-9);
  const u = B.fall('unrund').va[0];
  assert.ok(B.kraft(u, 1, 0.25) - B.kraft(u, 1, 0.75) > 1.5);
});

test('Eingaben prüfen mit Toleranz und Komma', () => {
  assert.ok(B.pruefeWert(30, '30,0'));
  assert.ok(B.pruefeWert(30, '31'));
  assert.ok(!B.pruefeWert(30, '33'));
  assert.ok(!B.pruefeWert(30, ''));
  assert.ok(B.pruefeBefund('fba', 'fba').richtig);
  assert.ok(!B.pruefeBefund('fba', 'ok').richtig);
});
