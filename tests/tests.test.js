const test = require('node:test');
const assert = require('node:assert');
const T = require('../js/tests.js');

function bank(spec) {
  const q = [];
  Object.entries(spec).forEach(([thema, n]) => {
    for (let i = 0; i < n; i++) q.push({ id: thema + i, thema, frage: 'F', antworten: ['a', 'b'], richtig: 0, erklaerung: '' });
  });
  return q;
}
function seeded(seed) { return () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }
const count = qs => qs.reduce((m, q) => (m[q.thema] = (m[q.thema] || 0) + 1, m), {});

test('pickEingang verteilt gleichmäßig über alle Themen, keine Duplikate', () => {
  const q = bank({ A: 8, B: 8, C: 8, D: 8, E: 8 });
  const p = T.pickEingang(q, 18, seeded(1));
  assert.strictEqual(p.length, 18);
  assert.strictEqual(new Set(p.map(x => x.id)).size, 18);
  const c = Object.values(count(p));
  assert.strictEqual(c.length, 5);
  assert.ok(Math.max(...c) - Math.min(...c) <= 1);
});

test('pickEingang: Thema mit wenig Fragen -> Rest aus anderen Themen', () => {
  const q = bank({ A: 1, B: 20 });
  const p = T.pickEingang(q, 10, seeded(2));
  assert.strictEqual(p.length, 10);
  assert.strictEqual(count(p).A, 1);
});

test('pickEingang: zu wenige Fragen insgesamt -> alle', () => {
  assert.strictEqual(T.pickEingang(bank({ A: 3, B: 2 }), 18, seeded(3)).length, 5);
  assert.deepStrictEqual(T.pickEingang([], 18, seeded(3)), []);
});

test('pickThemen nimmt nur gewählte Themen', () => {
  const q = bank({ A: 10, B: 10, C: 10 });
  const p = T.pickThemen(q, ['A', 'C'], 10, seeded(4));
  assert.strictEqual(p.length, 10);
  assert.ok(p.every(x => x.thema === 'A' || x.thema === 'C'));
  assert.deepStrictEqual(T.pickThemen(q, [], 10, seeded(4)), []);
});

test('pickKurz: 5 Fragen eines Themas, oder alle vorhandenen', () => {
  const q = bank({ A: 10, B: 3 });
  assert.strictEqual(T.pickKurz(q, 'A', 5, seeded(5)).length, 5);
  assert.strictEqual(T.pickKurz(q, 'B', 5, seeded(5)).length, 3);
});

test('score gesamt und pro Thema, gerundet', () => {
  const f = bank({ A: 3, B: 2 });
  const r = T.score(f, [0, 0, 1, 0, null]);
  assert.strictEqual(r.gesamt, 60);
  assert.deepStrictEqual(r.proThema, { A: 67, B: 50 });
  assert.deepStrictEqual(T.score([], []), { gesamt: 0, proThema: {} });
});

test('themenListe in Reihenfolge des ersten Vorkommens', () => {
  assert.deepStrictEqual(T.themenListe(bank({ B: 1, A: 2 })), ['B', 'A']);
});
