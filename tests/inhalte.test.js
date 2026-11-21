const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const X = require('../js/xlsx.js');
const I = require('../js/inhalte.js');

const DATEI = path.join(__dirname, '../inhalte/Lernportal-Inhalte.xlsx');
const buf = p => { const b = fs.readFileSync(p); return b.buffer.slice(b.byteOffset, b.byteOffset + b.byteLength); };

function fixture(name, py) {
  const out = path.join(require('node:os').tmpdir(), name);
  execFileSync('python3', ['-c', 'from openpyxl import Workbook\nwb=Workbook()\n' + py + '\nwb.save(' + JSON.stringify(out) + ')']);
  return out;
}

test('readXlsx liest Blattnamen, Texte, Zahlen, Umlaute, Zeilenumbrüche und Lücken', async () => {
  const f = fixture('t1.xlsx', [
    'ws=wb.active; ws.title="Eins"',
    'ws["A1"]="Grüße & <Tags>"; ws["C1"]=12.5; ws["A2"]="Zeile1\\nZeile2"; ws["B3"]="x"',
    'w2=wb.create_sheet("Zwei"); w2["A1"]="b"'
  ].join('\n'));
  const s = await X.readXlsx(buf(f));
  assert.deepStrictEqual(Object.keys(s), ['Eins', 'Zwei']);
  assert.deepStrictEqual(s.Eins[0], ['Grüße & <Tags>', '', '12.5']);
  assert.strictEqual(s.Eins[1][0], 'Zeile1\nZeile2');
  assert.deepStrictEqual(s.Eins[2], ['', 'x']);
  assert.deepStrictEqual(s.Zwei, [['b']]);
});

test('readXlsx: keine Excel-Datei -> Fehler', async () => {
  await assert.rejects(X.readXlsx(new TextEncoder().encode('kein zip').buffer));
});

test('youtubeId erkennt übliche Links', () => {
  assert.strictEqual(I.youtubeId('https://www.youtube.com/watch?v=abcDEF12345'), 'abcDEF12345');
  assert.strictEqual(I.youtubeId('https://youtu.be/abcDEF12345?si=xy'), 'abcDEF12345');
  assert.strictEqual(I.youtubeId('https://www.youtube.com/shorts/abcDEF12345'), 'abcDEF12345');
  assert.strictEqual(I.youtubeId('https://www.youtube.com/embed/abcDEF12345'), 'abcDEF12345');
  assert.strictEqual(I.youtubeId(''), null);
  assert.strictEqual(I.youtubeId('https://example.com'), null);
});

test('parseInhalte: Themen, Fragen, Einstellungen; Themen nur aus Fragen werden ergänzt', () => {
  const sheets = {
    Themen: [['Thema', 'Bereich', 'Erklärung', 'Video-Link'], ['A', 'Elektrik', 'Text A', 'https://youtu.be/abcDEF12345'], ['', '', '', ''], ['B', '', 'Text B', '']],
    Fragen: [['Thema', 'Frage', 'Antwort A', 'Antwort B', 'Antwort C', 'Antwort D', 'Richtig', 'Erklärung'], ['A', 'F?', '1', '2', '', '', 'A', ''], ['C', 'G?', '1', '2', '', '', 'b', '']],
    Einstellungen: [['Einstellung', 'Wert'], ['Portal-Name', 'Mein Portal'], ['Impressum Name', 'Max']]
  };
  const r = I.parseInhalte(sheets);
  assert.deepStrictEqual(r.themen.map(t => t.name), ['A', 'B', 'C']);
  assert.strictEqual(r.themen[0].video, 'abcDEF12345');
  assert.strictEqual(r.themen[1].bereich, 'Weitere Themen');
  assert.strictEqual(r.themen[2].erklaerung, '');
  assert.strictEqual(r.fragen.length, 2);
  assert.strictEqual(r.einstellungen['Portal-Name'], 'Mein Portal');
});

test('parseInhalte: fehlende Blätter -> leere Listen, kein Absturz', () => {
  const r = I.parseInhalte({});
  assert.deepStrictEqual(r.themen, []);
  assert.deepStrictEqual(r.fragen, []);
});

test('Echte Inhaltsdatei: 10 Themen, 87 gültige Fragen, je Thema >= 5', async () => {
  const r = I.parseInhalte(await X.readXlsx(buf(DATEI)));
  assert.strictEqual(r.themen.length, 10);
  assert.strictEqual(r.fragen.length, 87);
  r.themen.forEach(t => assert.ok(r.fragen.filter(f => f.thema === t.name).length >= 5, t.name));
  assert.ok(r.themen[0].erklaerung.includes('\n'));
});

test('parsePraesentationen: "Titel | Link" pro Zeile, Titel optional, unsichere Links werden verworfen', () => {
  const r = I.parsePraesentationen('Spannung | praesentationen/spannung.html\npraesentationen/mein-thema.html\n\njavascript:alert(1)\nX | ../geheim.html\nY | //fremd.de/a.html\nWeb | https://example.com/a.html');
  assert.deepStrictEqual(r, [
    { titel: 'Spannung', link: 'praesentationen/spannung.html' },
    { titel: 'mein thema', link: 'praesentationen/mein-thema.html' },
    { titel: 'Web', link: 'https://example.com/a.html' }
  ]);
  assert.deepStrictEqual(I.parsePraesentationen(''), []);
  assert.deepStrictEqual(I.parsePraesentationen(undefined), []);
});

test('videoDatei erkennt eigene Videodateien, YouTube bleibt YouTube', () => {
  assert.strictEqual(I.videoDatei('videos/strom.mp4'), 'videos/strom.mp4');
  assert.strictEqual(I.videoDatei('https://example.com/v.webm'), 'https://example.com/v.webm');
  assert.strictEqual(I.videoDatei('https://youtu.be/abcDEF12345'), null);
  assert.strictEqual(I.videoDatei('javascript:x.mp4'), null);
  assert.strictEqual(I.videoDatei(''), null);
});

test('Echte Inhaltsdatei: Präsentationen zu Spannung, Strom und Widerstand sind verlinkt und vorhanden', async () => {
  const r = I.parseInhalte(await X.readXlsx(buf(DATEI)));
  const t = r.themen.find(x => x.name === 'Spannung, Strom und Widerstand');
  assert.deepStrictEqual(t.praesentationen.map(p => p.titel), ['Spannung', 'Strom', 'Widerstand']);
  t.praesentationen.forEach(p => assert.ok(fs.existsSync(path.join(__dirname, '..', p.link)), p.link));
  ['spannung', 'strom', 'widerstand'].forEach(n => assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.mp4')), n));
  assert.ok(!t.erklaerung.includes('Elektronen'));
});

test('Echte Inhaltsdatei: Präsentationen zu Sensoren, Aktoren und EVA-Prinzip sind verlinkt und vorhanden', async () => {
  const r = I.parseInhalte(await X.readXlsx(buf(DATEI)));
  const t = r.themen.find(x => x.name === 'Sensoren, Aktoren und EVA-Prinzip');
  assert.strictEqual(t.bereich, 'Fahrzeugelektronik');
  assert.deepStrictEqual(t.praesentationen.map(p => p.titel), ['EVA-Prinzip', 'Sensoren', 'Aktoren']);
  t.praesentationen.forEach(p => assert.ok(fs.existsSync(path.join(__dirname, '..', p.link)), p.link));
  ['eva', 'sensoren', 'aktoren'].forEach(n => {
    assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.mp4')), n);
    assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.jpg')), n);
  });
  assert.ok(r.fragen.filter(f => f.thema === t.name).length >= 5);
});

test('Echte Inhaltsdatei: Motormanagement Grundlagen mit Präsentationen und Videos', async () => {
  const r = I.parseInhalte(await X.readXlsx(buf(DATEI)));
  const t = r.themen.find(x => x.name === 'Motormanagement: Grundlagen');
  assert.strictEqual(t.bereich, 'Motormanagement');
  assert.deepStrictEqual(t.praesentationen.map(p => p.titel), ['Aufgaben und Steuergerät', 'Luftverhältnis Lambda', 'Betriebszustände']);
  t.praesentationen.forEach(p => assert.ok(fs.existsSync(path.join(__dirname, '..', p.link)), p.link));
  ['mm-aufgaben', 'mm-lambda', 'mm-betrieb'].forEach(n => {
    assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.mp4')), n);
    assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.jpg')), n);
  });
  assert.ok(r.fragen.filter(f => f.thema === t.name).length >= 5);
});

test('Echte Inhaltsdatei: Motormanagement Gemischbildung Otto mit Präsentationen und Videos', async () => {
  const r = I.parseInhalte(await X.readXlsx(buf(DATEI)));
  const t = r.themen.find(x => x.name === 'Motormanagement: Gemischbildung Otto');
  assert.strictEqual(t.bereich, 'Motormanagement');
  assert.deepStrictEqual(t.praesentationen.map(p => p.titel), ['Kraftstoffsystem', 'Einspritzung', 'Luft und Last']);
  t.praesentationen.forEach(p => assert.ok(fs.existsSync(path.join(__dirname, '..', p.link)), p.link));
  ['mm-kraftstoff', 'mm-einspritzung', 'mm-luft'].forEach(n => {
    assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.mp4')), n);
    assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.jpg')), n);
  });
});

test('Echte Inhaltsdatei: Motormanagement Zündung mit Präsentationen und Videos', async () => {
  const r = I.parseInhalte(await X.readXlsx(buf(DATEI)));
  const t = r.themen.find(x => x.name === 'Motormanagement: Zündung');
  assert.strictEqual(t.bereich, 'Motormanagement');
  assert.deepStrictEqual(t.praesentationen.map(p => p.titel), ['Zündanlage', 'Zündkerze', 'Zündzeitpunkt']);
  t.praesentationen.forEach(p => assert.ok(fs.existsSync(path.join(__dirname, '..', p.link)), p.link));
  ['mm-zuendanlage', 'mm-zuendkerze', 'mm-zuendzeitpunkt'].forEach(n => {
    assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.mp4')), n);
    assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.jpg')), n);
  });
});

test('Echte Inhaltsdatei: Motormanagement Dieselmanagement mit Präsentationen und Videos', async () => {
  const r = I.parseInhalte(await X.readXlsx(buf(DATEI)));
  const t = r.themen.find(x => x.name === 'Motormanagement: Dieselmanagement');
  assert.strictEqual(t.bereich, 'Motormanagement');
  assert.deepStrictEqual(t.praesentationen.map(p => p.titel), ['Diesel-Grundlagen', 'Common-Rail', 'Turbo und AGR']);
  t.praesentationen.forEach(p => assert.ok(fs.existsSync(path.join(__dirname, '..', p.link)), p.link));
  ['mm-diesel-grundlagen', 'mm-common-rail', 'mm-diesel-turbo'].forEach(n => {
    assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.mp4')), n);
    assert.ok(fs.existsSync(path.join(__dirname, '../praesentationen/videos', n + '.jpg')), n);
  });
});
