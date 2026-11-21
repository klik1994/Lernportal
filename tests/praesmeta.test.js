const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const P = require('../js/praesmeta.js');

test('liest Symbol, Titel, Untertitel, Folien, Fragen und Farbe', () => {
  const html = fs.readFileSync(path.join(__dirname, '../praesentationen/mm-kraftstoff.html'), 'utf8');
  const m = P.parseMeta(html);
  assert.strictEqual(m.symbol, '⛽');
  assert.strictEqual(m.titel, 'Kraftstoffsystem');
  assert.strictEqual(m.untertitel, 'Vom Tank bis zum Einspritzventil');
  assert.strictEqual(m.folien, 12);
  assert.strictEqual(m.fragen, 4);
  assert.strictEqual(m.farbe, 'roy');
});

test('Textsymbol und andere Farbe', () => {
  const m = P.parseMeta(fs.readFileSync(path.join(__dirname, '../praesentationen/eva.html'), 'utf8'));
  assert.strictEqual(m.symbol, 'EVA');
  assert.strictEqual(m.farbe, 'pur');
});

test('kaputtes HTML -> Standardwerte, kein Absturz', () => {
  const m = P.parseMeta('<html><body>nix</body></html>');
  assert.deepStrictEqual(m, { symbol: '', titel: '', untertitel: '', folien: 0, fragen: 0, farbe: 'yel' });
});

test('videoPfad leitet MP4 aus dem Präsentationslink ab', () => {
  assert.strictEqual(P.videoPfad('praesentationen/mm-luft.html'), 'praesentationen/videos/mm-luft.mp4');
  assert.strictEqual(P.videoPfad('https://example.com/x.html'), null);
});

test('Alle Präsentationen im Repo liefern Titel und Folien', () => {
  const dir = path.join(__dirname, '../praesentationen');
  fs.readdirSync(dir).filter(f => f.endsWith('.html')).forEach(f => {
    const m = P.parseMeta(fs.readFileSync(path.join(dir, f), 'utf8'));
    assert.ok(m.titel && m.folien > 0, f);
  });
});
