const test = require('node:test');
const assert = require('node:assert');
const { parseCSV, rowsToQuestions, loadQuestions } = require('../js/questions.js');

const KOPF = 'Thema,Frage,Antwort A,Antwort B,Antwort C,Antwort D,Richtig,Erklärung';

test('parseCSV verarbeitet Anführungszeichen, Kommas und Zeilenumbrüche', () => {
  const rows = parseCSV('a,"b, c","sagt ""hallo"""\r\n"x\ny",2,3\n');
  assert.deepStrictEqual(rows, [['a', 'b, c', 'sagt "hallo"'], ['x\ny', '2', '3']]);
});

test('rowsToQuestions liest gültige Zeilen und überspringt kaputte', () => {
  const rows = parseCSV([
    KOPF,
    'Messen,Wie misst man Spannung?,parallel,in Reihe,gar nicht,egal,a,Immer parallel.',
    'Messen,Kaputt,1,2,3,4,E,falsch',
    'Messen,,1,2,3,4,A,leer',
    'Strom,Einheit?,Volt,Ampere,Ohm,Watt,b,',
    ',,,,,,,'
  ].join('\n'));
  const q = rowsToQuestions(rows);
  assert.strictEqual(q.length, 2);
  assert.strictEqual(q[0].thema, 'Messen');
  assert.strictEqual(q[0].richtig, 0);
  assert.deepStrictEqual(q[0].antworten, ['parallel', 'in Reihe', 'gar nicht', 'egal']);
  assert.strictEqual(q[1].richtig, 1);
  assert.strictEqual(q[1].erklaerung, '');
  assert.notStrictEqual(q[0].id, q[1].id);
});

test('rowsToQuestions erlaubt Fragen mit nur zwei Antworten (C und D leer)', () => {
  const q = rowsToQuestions(parseCSV(KOPF + '\nX,Stimmt das?,Ja,Nein,,,A,'));
  assert.strictEqual(q.length, 1);
  assert.deepStrictEqual(q[0].antworten, ['Ja', 'Nein']);
  const bad = rowsToQuestions(parseCSV(KOPF + '\nX,Stimmt das?,Ja,Nein,,,C,'));
  assert.strictEqual(bad.length, 0);
});

test('loadQuestions nutzt die Tabelle, wenn erreichbar', async () => {
  const fetchFn = async () => ({ ok: true, text: async () => KOPF + '\nA,F?,1,2,3,4,c,' });
  const r = await loadQuestions('https://x', fetchFn, []);
  assert.strictEqual(r.quelle, 'tabelle');
  assert.strictEqual(r.questions[0].richtig, 2);
});

test('loadQuestions fällt auf eingebaute Fragen zurück', async () => {
  const builtin = [{ id: 'b1', thema: 'T', frage: 'F', antworten: ['a', 'b'], richtig: 0, erklaerung: '' }];
  const wirft = async () => { throw new Error('offline'); };
  assert.strictEqual((await loadQuestions('https://x', wirft, builtin)).quelle, 'eingebaut');
  const nichtOk = async () => ({ ok: false, text: async () => '' });
  assert.strictEqual((await loadQuestions('https://x', nichtOk, builtin)).quelle, 'eingebaut');
  const leer = async () => ({ ok: true, text: async () => KOPF });
  assert.strictEqual((await loadQuestions('https://x', leer, builtin)).quelle, 'eingebaut');
  assert.strictEqual((await loadQuestions('', wirft, builtin)).quelle, 'eingebaut');
});
