const test = require('node:test');
const assert = require('node:assert');
const M = require('../js/multimeter.js');

const basis = { fehler: null, modus: 'V=', buchseRot: 'VΩ', rot: 'B+', schwarz: 'Masse', schalterZu: true, batterieAn: true, sicherungDrin: true, sicherungDurch: false, lampeDran: true };
const zu = o => M.aktualisiere(Object.assign({}, basis, o)).zustand;
const m = o => M.messe(zu(o));
const nah = (a, b, tol = 0.15) => assert.ok(Math.abs(a - b) <= tol, a + ' ≈ ' + b);
const F = (ort, art) => ({ ort, art });

test('Normalfall: Batterie 12,6 V, Lampe ca. 12,3 V, Lampe hell, Sicherung hält', () => {
  nah(m({}).wert, 12.6);
  nah(m({ rot: 'L1', schwarz: 'L2' }).wert, 12.3);
  assert.ok(M.helligkeit(zu({})) > 0.9);
  assert.strictEqual(M.helligkeit(zu({ schalterZu: false })), 0);
  assert.strictEqual(zu({}).sicherungDurch, false);
});

test('Anzeige, vertauschte Spitzen, Modus aus, Wechselspannung', () => {
  assert.strictEqual(m({}).anzeige, '12,6 V');
  assert.match(m({ rot: 'Masse', schwarz: 'B+' }).meldung, /vertauscht/);
  assert.strictEqual(m({ modus: 'aus' }).anzeige, '');
  assert.match(m({ modus: 'V~' }).meldung, /Gleichspannung/);
});

test('Falsche Buchse an Spannung: Kurzschluss im Messgerät', () => {
  assert.match(m({ buchseRot: '10A' }).meldung, /Kurzschluss/);
});

test('Widerstand unter Spannung: Warnung; stromlos Lampe 0,8 Ω', () => {
  assert.match(m({ modus: 'Ω', rot: 'L1', schwarz: 'L2' }).meldung, /abklemmen/);
  nah(m({ modus: 'Ω', rot: 'L1', schwarz: 'L2', batterieAn: false }).wert, 0.8, 0.05);
});

test('Szenarien: 15 Stück, alle mit Symptom', () => {
  assert.strictEqual(M.SZENARIEN.length, 15);
  M.SZENARIEN.forEach(f => assert.ok(M.symptom(f).length > 5, JSON.stringify(f)));
});

test('Unterbrechung Leitung Schalter–Lampe (K3): T2 12,6 V, L1 0 V, stromlos OL', () => {
  const f = F('K3', 'unterbrechung');
  nah(m({ fehler: f, rot: 'T2' }).wert, 12.6);
  nah(m({ fehler: f, rot: 'L1' }).wert, 0);
  assert.strictEqual(m({ fehler: f, modus: 'Ω', rot: 'T2', schwarz: 'L1', batterieAn: false }).anzeige, 'OL');
});

test('Unterbrechung Masseleitung (K4): L2 gegen Masse 12,6 V', () => {
  nah(m({ fehler: F('K4', 'unterbrechung'), rot: 'L2' }).wert, 12.6);
});

test('Übergangswiderstand in Zuleitung (K1): ca. 5 V Spannungsfall B+ gegen S1, Lampe schwach', () => {
  const f = F('K1', 'uebergang');
  assert.ok(m({ fehler: f, rot: 'B+', schwarz: 'S1' }).wert > 3);
  const h = M.helligkeit(zu({ fehler: f }));
  assert.ok(h > 0.1 && h < 0.6);
});

test('Übergangswiderstand Masseleitung (K4): L2 gegen Masse > 3 V', () => {
  assert.ok(m({ fehler: F('K4', 'uebergang'), rot: 'L2' }).wert > 3);
});

test('Masseschluss K3: Sicherung brennt beim Einschalten durch', () => {
  const f = F('K3', 'masse');
  assert.strictEqual(zu({ fehler: f, schalterZu: false }).sicherungDurch, false);
  const r = M.aktualisiere(Object.assign({}, basis, { fehler: f }));
  assert.strictEqual(r.zustand.sicherungDurch, true);
  assert.strictEqual(r.geradeDurchgebrannt, true);
  nah(m({ fehler: f, rot: 'S1' }).wert, 12.6);
  nah(m({ fehler: f, rot: 'S2' }).wert, 0);
  assert.strictEqual(M.helligkeit(r.zustand), 0);
});

test('Masseschluss K2: brennt sofort durch, auch mit Schalter aus', () => {
  assert.strictEqual(zu({ fehler: F('K2', 'masse'), schalterZu: false }).sicherungDurch, true);
});

test('Masseschluss finden: Lampe ab, Batterie ab, Schalter aus -> Leitung gegen Masse 0 Ω, andere Seite OL', () => {
  const s = { fehler: F('K3', 'masse'), modus: 'Ω', batterieAn: false, lampeDran: false, schalterZu: false, schwarz: 'Masse' };
  nah(m(Object.assign({ rot: 'L1' }, s)).wert, 0, 0.05);
  nah(m(Object.assign({ rot: 'T2' }, s)).wert, 0, 0.05);
  assert.strictEqual(m(Object.assign({ rot: 'T1' }, s)).anzeige, 'OL');
  const k2 = Object.assign({}, s, { fehler: F('K2', 'masse') });
  nah(m(Object.assign({ rot: 'T1' }, k2)).wert, 0, 0.05);
  assert.strictEqual(m(Object.assign({ rot: 'T2' }, k2)).anzeige, 'OL');
  const ok = Object.assign({}, s, { fehler: null });
  assert.strictEqual(m(Object.assign({ rot: 'L1' }, ok)).anzeige, 'OL');
});

test('Plusschluss K3: Lampe leuchtet auch bei Schalter aus, T2 hat 12,6 V', () => {
  const f = F('K3', 'plus');
  assert.ok(M.helligkeit(zu({ fehler: f, schalterZu: false })) > 0.9);
  nah(m({ fehler: f, schalterZu: false, rot: 'T2' }).wert, 12.6);
  assert.strictEqual(zu({ fehler: f }).sicherungDurch, false);
  nah(m({ fehler: f, modus: 'Ω', batterieAn: false, lampeDran: false, rot: 'L1', schwarz: 'B+', schalterZu: false }).wert, 0, 0.05);
});

test('Defekte Sicherung allein: neue Sicherung behebt den Fehler', () => {
  const f = F('sicherung', 'unterbrechung');
  assert.strictEqual(M.helligkeit(zu({ fehler: f })), 0);
  const r = M.neueSicherung(zu({ fehler: f }));
  assert.ok(M.helligkeit(r.zustand) > 0.9);
  assert.strictEqual(r.geradeDurchgebrannt, false);
});

test('Masseschluss: neue Sicherung brennt sofort wieder durch', () => {
  const r = M.neueSicherung(zu({ fehler: F('K3', 'masse') }));
  assert.strictEqual(r.zustand.sicherungDurch, true);
  assert.strictEqual(r.geradeDurchgebrannt, true);
});

test('Sicherung gezogen: S2 0 V', () => {
  nah(m({ sicherungDrin: false, rot: 'S2' }).wert, 0);
});

test('pruefeAntwort: richtig, Ort richtig/Art falsch, Masseschluss mit Antwort Sicherung', () => {
  assert.strictEqual(M.pruefeAntwort(F('K3', 'masse'), 'K3', 'masse').richtig, true);
  const a = M.pruefeAntwort(F('K3', 'masse'), 'K3', 'unterbrechung');
  assert.strictEqual(a.richtig, false);
  assert.match(a.rueckmeldung, /Stelle stimmt/);
  const b = M.pruefeAntwort(F('K3', 'masse'), 'sicherung', 'unterbrechung');
  assert.strictEqual(b.richtig, false);
  assert.match(b.rueckmeldung, /Folge/);
  assert.strictEqual(M.pruefeAntwort(F('lampe', 'unterbrechung'), 'lampe', 'unterbrechung').richtig, true);
  M.SZENARIEN.forEach(f => {
    const r = M.pruefeAntwort(f, f.ort, f.art);
    assert.ok(r.richtig && r.erklaerung.length > 20, JSON.stringify(f));
  });
});

test('Aufgaben werden erkannt', () => {
  assert.strictEqual(M.aufgabeErfuellt('batterie', basis), true);
  assert.strictEqual(M.aufgabeErfuellt('batterie', Object.assign({}, basis, { rot: 'L1' })), false);
  assert.strictEqual(M.aufgabeErfuellt('lampe-v', Object.assign({}, basis, { rot: 'L1', schwarz: 'L2' })), true);
  assert.strictEqual(M.aufgabeErfuellt('lampe-r', Object.assign({}, basis, { modus: 'Ω', rot: 'L2', schwarz: 'L1', batterieAn: false })), true);
  assert.strictEqual(M.aufgabeErfuellt('lampe-r', Object.assign({}, basis, { modus: 'Ω', rot: 'L2', schwarz: 'L1' })), false);
});
