const test = require('node:test');
const assert = require('node:assert');
const L = require('../js/lernstand.js');

const THEMEN = ['A', 'B', 'C', 'D'];

test('initialState', () => {
  assert.deepStrictEqual(L.initialState(), { eingangstestFertig: false, themen: {}, sterne: [], lehrjahr: null });
});

test('Eingangstest: >= 80 % sitzt, sonst offen; setzt eingangstestFertig', () => {
  let s = L.initialState();
  s = L.applyResult(s, 'A', 80, 'eingang');
  s = L.applyResult(s, 'B', 79, 'eingang');
  s = L.markEingangFertig(s);
  assert.strictEqual(L.statusOf(s, 'A'), 'sitzt');
  assert.strictEqual(L.statusOf(s, 'B'), 'offen');
  assert.strictEqual(L.statusOf(s, 'C'), 'offen');
  assert.strictEqual(s.eingangstestFertig, true);
});

test('Kurztest: >= 80 % sitzt, sonst angefangen', () => {
  let s = L.applyResult(L.initialState(), 'A', 60, 'kurz');
  assert.strictEqual(L.statusOf(s, 'A'), 'angefangen');
  s = L.applyResult(s, 'A', 100, 'kurz');
  assert.strictEqual(L.statusOf(s, 'A'), 'sitzt');
});

test('Prüfung/Übung: < 80 % fällt auf angefangen zurück, >= 80 % ändert nichts', () => {
  let s = L.applyResult(L.initialState(), 'A', 100, 'kurz');
  s = L.applyResult(s, 'A', 50, 'pruefung');
  assert.strictEqual(L.statusOf(s, 'A'), 'angefangen');
  s = L.applyResult(s, 'B', 90, 'uebung');
  assert.strictEqual(L.statusOf(s, 'B'), 'offen');
  s = L.applyResult(s, 'C', 40, 'uebung');
  assert.strictEqual(L.statusOf(s, 'C'), 'angefangen');
});

test('applyResult verändert den alten Zustand nicht', () => {
  const s0 = L.initialState();
  L.applyResult(s0, 'A', 100, 'kurz');
  assert.deepStrictEqual(s0.themen, {});
});

test('nextSteps: Sterne zuerst, dann angefangen, dann offen, max 3, ohne sitzt', () => {
  let s = L.initialState();
  s = L.applyResult(s, 'A', 100, 'kurz');
  s = L.applyResult(s, 'C', 50, 'kurz');
  s = L.toggleStern(s, 'D');
  const n = L.nextSteps(s, THEMEN);
  assert.deepStrictEqual(n.map(x => x.thema), ['D', 'C', 'B']);
  n.forEach(x => assert.ok(x.text.length > 0));
  assert.strictEqual(L.nextSteps(s, THEMEN, 1).length, 1);
});

test('fortschritt in Prozent der sitzenden Themen, gerundet', () => {
  let s = L.applyResult(L.initialState(), 'A', 100, 'kurz');
  assert.strictEqual(L.fortschritt(s, ['A', 'B', 'C']), 33);
  assert.strictEqual(L.fortschritt(s, []), 0);
});

test('toggleStern an und aus', () => {
  let s = L.toggleStern(L.initialState(), 'A');
  assert.deepStrictEqual(s.sterne, ['A']);
  s = L.toggleStern(s, 'A');
  assert.deepStrictEqual(s.sterne, []);
});

test('unbekannte Themen im gespeicherten Stand werden ignoriert', () => {
  let s = L.applyResult(L.initialState(), 'Alt', 100, 'kurz');
  s = L.toggleStern(s, 'Alt');
  assert.strictEqual(L.fortschritt(s, ['A']), 0);
  assert.deepStrictEqual(L.nextSteps(s, ['A']).map(x => x.thema), ['A']);
});

test('createStore speichert und lädt', () => {
  const mem = {};
  const storage = { getItem: k => (k in mem ? mem[k] : null), setItem: (k, v) => { mem[k] = String(v); } };
  const st = L.createStore(storage);
  assert.strictEqual(st.persistent, true);
  const s = L.applyResult(L.initialState(), 'A', 100, 'kurz');
  st.save(s);
  assert.deepStrictEqual(L.createStore(storage).load(), s);
});

test('createStore: gesperrter Speicher -> persistent false, kein Fehler', () => {
  const boom = { getItem() { throw new Error('x'); }, setItem() { throw new Error('x'); } };
  const st = L.createStore(boom);
  assert.strictEqual(st.persistent, false);
  st.save(L.applyResult(L.initialState(), 'A', 100, 'kurz'));
  assert.strictEqual(L.statusOf(st.load(), 'A'), 'sitzt');
  const st2 = L.createStore(null);
  assert.strictEqual(st2.persistent, false);
  assert.deepStrictEqual(st2.load(), L.initialState());
});

test('createStore: kaputter gespeicherter Text -> Anfangszustand', () => {
  const storage = { getItem: () => '{kaputt', setItem() {} };
  assert.deepStrictEqual(L.createStore(storage).load(), L.initialState());
});

test('setLehrjahr speichert 1 bis 4, ungültige Werte werden ignoriert', () => {
  let s = L.setLehrjahr(L.initialState(), 2);
  assert.strictEqual(s.lehrjahr, 2);
  assert.strictEqual(L.setLehrjahr(s, 7).lehrjahr, 2);
  assert.strictEqual(L.setLehrjahr(s, 'x').lehrjahr, 2);
  s = L.applyResult(s, 'A', 100, 'kurz');
  assert.strictEqual(L.setLehrjahr(s, 3).themen.A, 'sitzt');
});

test('createStore behält das Lehrjahr, alter Stand ohne Lehrjahr -> null', () => {
  const mem = {};
  const storage = { getItem: k => (k in mem ? mem[k] : null), setItem: (k, v) => { mem[k] = String(v); } };
  const st = L.createStore(storage);
  st.save(L.setLehrjahr(L.initialState(), 3));
  assert.strictEqual(L.createStore(storage).load().lehrjahr, 3);
  mem['kfz-lernportal-v1'] = JSON.stringify({ eingangstestFertig: true, themen: {}, sterne: [] });
  assert.strictEqual(L.createStore(storage).load().lehrjahr, null);
});
