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

test('Echte Inhaltsdatei: 5 Themen, 36 gültige Fragen, je Thema >= 5', async () => {
  const r = I.parseInhalte(await X.readXlsx(buf(DATEI)));
  assert.strictEqual(r.themen.length, 5);
  assert.strictEqual(r.fragen.length, 36);
  r.themen.forEach(t => assert.ok(r.fragen.filter(f => f.thema === t.name).length >= 5, t.name));
  assert.ok(r.themen[0].erklaerung.includes('\n'));
});
