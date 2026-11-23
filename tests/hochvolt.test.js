const test = require('node:test');
const assert = require('node:assert');
const H = require('../js/hochvolt.js');

const RICHTIG = ['zuendung', 'stecker', 'schloss', 'schild', 'warten', 'vorher', 'messen', 'nachher', 'doku'];

test('Richtige Reihenfolge ist ok, auch mit vertauschten gleichwertigen Schritten', () => {
  assert.ok(H.pruefeReihenfolge(RICHTIG).ok);
  assert.ok(H.pruefeReihenfolge(['vorher', 'zuendung', 'stecker', 'warten', 'schild', 'schloss', 'messen', 'nachher', 'doku']).ok);
});

test('Fehlender Schritt, falscher Schritt und falsche Reihenfolge werden gemeldet', () => {
  let r = H.pruefeReihenfolge(RICHTIG.filter(id => id !== 'warten'));
  assert.ok(!r.ok); assert.ok(r.fehler.some(f => f.fehlt && f.id === 'warten'));
  r = H.pruefeReihenfolge([...RICHTIG, 'erden']);
  assert.ok(!r.ok); assert.ok(r.fehler.some(f => f.id === 'erden'));
  r = H.pruefeReihenfolge(['zuendung', 'stecker', 'schloss', 'schild', 'warten', 'messen', 'vorher', 'nachher', 'doku']);
  assert.ok(!r.ok); assert.ok(r.falschePos.includes('messen'));
  r = H.pruefeReihenfolge(['stecker', 'zuendung', 'schloss', 'schild', 'warten', 'vorher', 'messen', 'nachher', 'doku']);
  assert.ok(r.falschePos.includes('stecker'));
});

test('Jeder Schritt hat Text und Begründung, es gibt Falle-Schritte', () => {
  H.SCHRITTE.forEach(s => assert.ok(s.text.length > 10 && s.warum.length > 20, s.id));
  assert.ok(H.SCHRITTE.filter(s => s.regel === 0).length >= 3);
});

test('Spannungsfrei: nur richtig mit Prüfung vorher, drei Messungen und Prüfung nachher', () => {
  let m = H.neueMessung('frei');
  assert.strictEqual(H.messe(m, 'quelle'), H.QUELLE);
  ['hv+hv-', 'hv+m', 'hv-m'].forEach(p => assert.strictEqual(H.messe(m, p), 0));
  assert.strictEqual(H.messe(m, 'quelle'), H.QUELLE);
  assert.ok(H.bewerte(m, 'frei').richtig);
  m = H.neueMessung('frei'); H.messe(m, 'hv+hv-');
  const b = H.bewerte(m, 'frei'); assert.ok(!b.richtig); assert.strictEqual(b.hinweise.length, 3);
});

test('Szenarien: Schütz, Isolationsfehler, Prüfer defekt vorher und nachher', () => {
  let m = H.neueMessung('schuetz'); assert.strictEqual(H.messe(m, 'hv+hv-'), 390); assert.ok(H.bewerte(m, 'nicht-frei').richtig);
  m = H.neueMessung('isolation'); assert.strictEqual(H.messe(m, 'hv+hv-'), 0); assert.strictEqual(H.messe(m, 'hv-m'), 160);
  assert.ok(!H.bewerte(m, 'frei').richtig); assert.ok(H.bewerte(m, 'nicht-frei').richtig);
  m = H.neueMessung('pruefer-vorher'); assert.strictEqual(H.messe(m, 'quelle'), null); assert.ok(H.bewerte(m, 'ungueltig').richtig);
  m = H.neueMessung('pruefer-nachher'); assert.strictEqual(H.messe(m, 'quelle'), H.QUELLE);
  H.messe(m, 'hv+hv-'); assert.strictEqual(H.messe(m, 'quelle'), null); assert.ok(H.bewerte(m, 'ungueltig').richtig);
});
