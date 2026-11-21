const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const LX = require('../js/lexikon.js');
const X = require('../js/xlsx.js');
const I = require('../js/inhalte.js');

const ROWS = [
  ['Begriff', 'Bereich', 'Erklärung', 'Beispiel', 'Auch gesucht unter'],
  ['Widerstand', 'Elektrik', 'bremst den Strom', 'Masse korrodiert', 'Widerstände'],
  ['Generator', 'Elektrik', 'erzeugt Strom', '', 'Lichtmaschine, Lima'],
  ['Abschlusswiderstand', 'Bus', '120 Ω', '', ''],
  ['Oberer Totpunkt', 'Motor', 'oben', '', 'OT'],
  ['Ärger', '', 'Test Umlaut', '', ''],
  ['ohne Erklärung', 'X', '', '', ''],
  ['widerstand', 'X', 'doppelt', '', '']
];

test('parse: leere Erklärung und doppelte Begriffe fallen weg, sortiert, Alias-Liste', () => {
  const L = LX.parse(ROWS);
  assert.deepStrictEqual(L.map(e => e.begriff), ['Abschlusswiderstand', 'Ärger', 'Generator', 'Oberer Totpunkt', 'Widerstand']);
  assert.deepStrictEqual(L.find(e => e.begriff === 'Generator').alias, ['Lichtmaschine', 'Lima']);
  assert.strictEqual(L.find(e => e.begriff === 'Ärger').bereich, 'Weitere Begriffe');
  assert.strictEqual(LX.buchstabe('Ärger'), 'A');
  assert.strictEqual(LX.buchstabe('12-V-Bordnetz'), '#');
});

test('suche: Begriff, Alias und Text, Begriff zuerst', () => {
  const L = LX.parse(ROWS);
  assert.deepStrictEqual(LX.suche(L, 'lima').map(e => e.begriff), ['Generator']);
  assert.deepStrictEqual(LX.suche(L, 'widerstand').map(e => e.begriff), ['Widerstand', 'Abschlusswiderstand']);
  assert.deepStrictEqual(LX.suche(L, 'korrodiert').map(e => e.begriff), ['Widerstand']);
  assert.strictEqual(LX.suche(L, '').length, L.length);
});

test('markiere: ganze Wörter, längster Treffer, jeder Begriff nur einmal, Abkürzung nur exakt', () => {
  const L = LX.parse(ROWS);
  const t = LX.markiere('Der Abschlusswiderstand ist ein Widerstand. Noch ein Widerstand. Die Lichtmaschine kurz vor OT, nicht ot und nicht OTTO. Vor-Widerstand.', L);
  assert.deepStrictEqual(t.filter(x => x.begriff).map(x => [x.text, x.begriff]),
    [['Abschlusswiderstand', 'Abschlusswiderstand'], ['Widerstand', 'Widerstand'], ['Lichtmaschine', 'Generator'], ['OT', 'Oberer Totpunkt']]);
  assert.strictEqual(t.map(x => x.text).join(''), 'Der Abschlusswiderstand ist ein Widerstand. Noch ein Widerstand. Die Lichtmaschine kurz vor OT, nicht ot und nicht OTTO. Vor-Widerstand.');
  const schon = new Set(['Generator']);
  assert.strictEqual(LX.markiere('Lima', L, schon).some(x => x.begriff), false);
});

test('Echte Inhaltsdatei: Lexikon mit 151 Begriffen, Bereiche wie bei den Themen, keine doppelten Suchwörter', async () => {
  const r = I.parseInhalte(await X.readXlsx((b => b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength))(fs.readFileSync(path.join(__dirname, '..', 'inhalte', 'Lernportal-Inhalte.xlsx')))));
  assert.strictEqual(r.lexikon.length, 151);
  const bereiche = new Set(r.themen.map(t => t.bereich));
  r.lexikon.forEach(e => { assert.ok(bereiche.has(e.bereich), e.begriff); assert.ok(e.beispiel, e.begriff); });
  const w = new Map();
  r.lexikon.forEach(e => [e.begriff].concat(e.alias).forEach(a => {
    const k = LX.norm(a);
    assert.ok(!w.has(k), a + ' doppelt bei ' + e.begriff + ' und ' + w.get(k));
    w.set(k, e.begriff);
  }));
});
