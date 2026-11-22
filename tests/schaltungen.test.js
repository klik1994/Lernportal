const test = require('node:test');
const assert = require('node:assert');
const M = require('../js/multimeter.js');

const P = M.SCHALTUNGEN.parallel, R = M.SCHALTUNGEN.reihe, E = M.SCHALTUNGEN.einfach;
const basis = { fehler: null, modus: 'V=', buchseRot: 'VΩ', rot: 'B+', schwarz: 'Masse', schalterZu: true, batterieAn: true, sicherungDrin: true, sicherungDurch: false, lampeDran: true };
const zu = (S, o) => S.aktualisiere(Object.assign({}, basis, o)).zustand;
const m = (S, o) => S.messe(zu(S, o));
const nah = (a, b, tol = 0.2) => assert.ok(Math.abs(a - b) <= tol, a + ' ≈ ' + b);
const F = (ort, art) => ({ ort, art });

test('Drei Schaltungen mit Namen, Knoten, Lampen und Szenarien', () => {
  assert.deepStrictEqual(Object.keys(M.SCHALTUNGEN), ['einfach', 'parallel', 'reihe']);
  [E, P, R].forEach(S => {
    assert.ok(S.name && S.KNOTEN.length && S.LAMPEN.length && S.SZENARIEN.length >= 10);
    S.SZENARIEN.forEach(f => {
      assert.ok(S.ORTE[f.ort], f.ort);
      assert.ok(S.symptom(f).length > 5);
      assert.ok(S.pruefeAntwort(f, f.ort, f.art).richtig);
      assert.ok(S.pruefeAntwort(f, f.ort, f.art).erklaerung.length > 20, JSON.stringify(f));
    });
  });
  assert.strictEqual(E.SZENARIEN.length, 15);
});

test('Einfach-Schaltung bleibt wie bisher (oberste Ebene = einfach)', () => {
  nah(m(E, { rot: 'L1', schwarz: 'L2' }).wert, 12.3);
  assert.strictEqual(M.SZENARIEN.length, 15);
});

test('Parallel normal: beide Lampen ca. 12,3 V, beide hell', () => {
  nah(m(P, { rot: 'E1+', schwarz: 'E1−' }).wert, 12.3, 0.3);
  nah(m(P, { rot: 'E2+', schwarz: 'E2−' }).wert, 12.3, 0.3);
  const h = P.helligkeiten(zu(P, {}));
  assert.ok(h.E1 > 0.9 && h.E2 > 0.9);
});

test('Parallel: Unterbrechung im Zweig E1 -> nur E1 aus', () => {
  const h = P.helligkeiten(zu(P, { fehler: F('K4', 'unterbrechung') }));
  assert.ok(h.E1 < 0.05 && h.E2 > 0.9);
  assert.match(P.symptom(F('K4', 'unterbrechung')), /E1/);
});

test('Parallel: Lampe E2 durchgebrannt -> 12,6 V über E2, E1 normal', () => {
  const f = F('E2', 'unterbrechung');
  nah(m(P, { fehler: f, rot: 'E2+', schwarz: 'E2−' }).wert, 12.6, 0.3);
  const h = P.helligkeiten(zu(P, { fehler: f }));
  assert.ok(h.E2 === 0 && h.E1 > 0.9);
});

test('Parallel: Übergangswiderstand gemeinsame Masse -> beide schwach; im Zweig -> nur eine schwach', () => {
  const a = P.helligkeiten(zu(P, { fehler: F('K8', 'uebergang') }));
  assert.ok(a.E1 < 0.7 && a.E2 < 0.7 && a.E1 > 0.05);
  const b = P.helligkeiten(zu(P, { fehler: F('K5', 'uebergang') }));
  assert.ok(b.E1 < 0.7 && b.E2 > 0.85);
  assert.match(P.symptom(F('K8', 'uebergang')), /[Bb]eide.*schwach/);
});

test('Parallel: Masseschluss im Zweig E2 -> Sicherung durch, beide aus; finden mit Ohm', () => {
  const f = F('K6', 'masse');
  const z = zu(P, { fehler: f });
  assert.strictEqual(z.sicherungDurch, true);
  const h = P.helligkeiten(z);
  assert.ok(h.E1 === 0 && h.E2 === 0);
  const s = { fehler: f, modus: 'Ω', batterieAn: false, lampeDran: false, schalterZu: false, schwarz: 'Masse' };
  nah(m(P, Object.assign({ rot: 'E2+' }, s)).wert, 0, 0.05);
  assert.match(P.pruefeAntwort(f, 'sicherung', 'unterbrechung').rueckmeldung, /Folge/);
  assert.match(P.pruefeAntwort(f, 'K6', 'masse').erklaerung, /beide/i);
});

test('Parallel: Gesamtwiderstand stromlos kleiner als eine Lampe', () => {
  const r = m(P, { modus: 'Ω', batterieAn: false, rot: 'X1', schwarz: 'X2' }).wert;
  assert.ok(r > 0.2 && r < 0.6, String(r));
});

test('Reihe normal: je Lampe ca. 6 V, zusammen ca. 12,3 V', () => {
  nah(m(R, { rot: 'E1+', schwarz: 'E1−' }).wert, 6.1, 0.3);
  nah(m(R, { rot: 'E1+', schwarz: 'E2−' }).wert, 12.3, 0.3);
  const h = R.helligkeiten(zu(R, {}));
  assert.ok(h.E1 > 0.9 && h.E2 > 0.9);
});

test('Reihe: E1 durchgebrannt -> beide aus, über E1 liegen 12,6 V', () => {
  const f = F('E1', 'unterbrechung');
  const h = R.helligkeiten(zu(R, { fehler: f }));
  assert.ok(h.E1 === 0 && h.E2 === 0);
  nah(m(R, { fehler: f, rot: 'E1+', schwarz: 'E1−' }).wert, 12.6, 0.3);
});

test('Reihe: Masseschluss zwischen E1 und E2 -> E1 heller, E2 aus, Sicherung hält', () => {
  const f = F('K4', 'masse');
  const z = zu(R, { fehler: f });
  assert.strictEqual(z.sicherungDurch, false);
  const h = R.helligkeiten(z);
  assert.ok(h.E1 > 1.5 && h.E2 < 0.05, JSON.stringify(h));
  assert.match(R.symptom(f), /heller/);
});

test('Messaufgaben je Schaltung erkennbar', () => {
  assert.ok(Object.keys(P.AUFGABEN).length >= 2 && Object.keys(R.AUFGABEN).length >= 2);
  assert.strictEqual(P.aufgabeErfuellt('e2-v', Object.assign({}, basis, { rot: 'E2+', schwarz: 'E2−' })), true);
  assert.strictEqual(R.aufgabeErfuellt('e1-v', Object.assign({}, basis, { rot: 'E1+', schwarz: 'E1−' })), true);
  assert.strictEqual(R.aufgabeErfuellt('e1-v', Object.assign({}, basis, { rot: 'E2+', schwarz: 'E2−' })), true === false);
});
