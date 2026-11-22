const test = require('node:test');
const assert = require('node:assert');
const C = require('../js/canbus.js');

const pegel = (id) => {
  const k = C.kurven(id, { zeitDiv: 10 });
  const hs = k.map(p => p[1]), ls = k.map(p => p[2]);
  return { hMin: Math.min(...hs), hMax: Math.max(...hs), lMin: Math.min(...ls), lMax: Math.max(...ls) };
};
const nah = (a, b, tol = 0.15) => assert.ok(Math.abs(a - b) <= tol, a + ' ≈ ' + b);

test('Fehlerliste: normal plus mindestens 9 Fehler mit Name, Erklärung, Widerständen', () => {
  assert.ok(C.FEHLER.length >= 9);
  ['normal', ...C.FEHLER.map(f => f.id)].forEach(id => {
    const f = C.info(id);
    assert.ok(f.name && f.erklaerung.length > 30, id);
    ['6-14', '6-4', '14-4', '6-16', '14-16'].forEach(p => assert.ok(p in f.widerstand, id + ' ' + p));
  });
});

test('Normal: CAN-H 2,5 / 3,5 V, CAN-L 2,5 / 1,5 V, 60 Ω', () => {
  const p = pegel('normal');
  nah(p.hMin, 2.5); nah(p.hMax, 3.5); nah(p.lMin, 1.5); nah(p.lMax, 2.5);
  assert.strictEqual(C.info('normal').widerstand['6-14'], 60);
});

test('Kurzschlüsse nach Masse und Plus: betroffene Leitung fest auf 0 V bzw. 12 V', () => {
  let p = pegel('h-masse'); nah(p.hMax, 0, 0.05); assert.strictEqual(C.info('h-masse').widerstand['6-4'], 0);
  p = pegel('l-masse'); nah(p.lMax, 0, 0.05); assert.strictEqual(C.info('l-masse').widerstand['14-4'], 0);
  p = pegel('h-plus'); nah(p.hMin, 12, 0.05); assert.strictEqual(C.info('h-plus').widerstand['6-16'], 0);
  p = pegel('l-plus'); nah(p.lMin, 12, 0.05); assert.strictEqual(C.info('l-plus').widerstand['14-16'], 0);
});

test('CAN-H und CAN-L kurzgeschlossen: beide gleich, 0 Ω', () => {
  const k = C.kurven('h-l', { zeitDiv: 10 });
  k.forEach(([, h, l]) => nah(h, l, 0.01));
  assert.strictEqual(C.info('h-l').widerstand['6-14'], 0);
});

test('Abschlusswiderstände: einer fehlt 120 Ω mit Überschwingern, beide fehlen OL', () => {
  assert.strictEqual(C.info('r-einer').widerstand['6-14'], 120);
  assert.strictEqual(C.info('r-beide').widerstand['6-14'], Infinity);
  assert.ok(pegel('r-einer').hMax > 3.6);
  assert.ok(pegel('r-beide').hMax > pegel('r-einer').hMax);
});

test('Unterbrechung CAN-H: CAN-H schwach, CAN-L normal, 120 Ω', () => {
  const p = pegel('h-unterbr');
  assert.ok(p.hMax < 3.1 && p.hMax > 2.6);
  nah(p.lMin, 1.5);
  assert.strictEqual(C.info('h-unterbr').widerstand['6-14'], 120);
});

test('Zeitbasis bestimmt Anzahl Bits im Bild', () => {
  const a = C.kurven('normal', { zeitDiv: 2 }), b = C.kurven('normal', { zeitDiv: 50 });
  assert.ok(a[a.length - 1][0] <= 20.01 && b[b.length - 1][0] > 400);
});

test('pruefe: richtig/falsch mit Erklärung', () => {
  assert.strictEqual(C.pruefe('h-masse', 'h-masse').richtig, true);
  const r = C.pruefe('h-masse', 'l-masse');
  assert.strictEqual(r.richtig, false);
  assert.ok(r.erklaerung.length > 30);
});

test('widerstandText', () => {
  assert.strictEqual(C.widerstandText(60), '60 Ω');
  assert.strictEqual(C.widerstandText(Infinity), 'OL');
  assert.strictEqual(C.widerstandText(0), '0,0 Ω');
});
