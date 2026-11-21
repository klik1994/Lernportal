const Tests = (() => {
  function shuffle(arr, rng) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function themenListe(questions) {
    const out = [];
    questions.forEach(q => { if (!out.includes(q.thema)) out.push(q.thema); });
    return out;
  }

  function roundRobin(questions, n, rng) {
    const gruppen = themenListe(questions).map(t => shuffle(questions.filter(q => q.thema === t), rng));
    const out = [];
    let weiter = true;
    while (out.length < n && weiter) {
      weiter = false;
      for (const g of shuffle(gruppen, rng)) {
        if (out.length >= n) break;
        if (g.length) { out.push(g.shift()); weiter = true; }
      }
    }
    return shuffle(out, rng);
  }

  const pickEingang = (questions, n = 18, rng = Math.random) => roundRobin(questions, n, rng);
  const pickThemen = (questions, themen, n = 10, rng = Math.random) =>
    roundRobin(questions.filter(q => themen.includes(q.thema)), n, rng);
  const pickKurz = (questions, thema, n = 5, rng = Math.random) =>
    shuffle(questions.filter(q => q.thema === thema), rng).slice(0, n);

  function score(fragen, antworten) {
    if (!fragen.length) return { gesamt: 0, proThema: {} };
    const pro = {};
    let richtig = 0;
    fragen.forEach((f, i) => {
      const ok = antworten[i] === f.richtig;
      if (ok) richtig++;
      pro[f.thema] = pro[f.thema] || [0, 0];
      pro[f.thema][0] += ok ? 1 : 0;
      pro[f.thema][1] += 1;
    });
    const proThema = {};
    Object.keys(pro).forEach(t => { proThema[t] = Math.round((pro[t][0] / pro[t][1]) * 100); });
    return { gesamt: Math.round((richtig / fragen.length) * 100), proThema };
  }

  return { shuffle, themenListe, pickEingang, pickThemen, pickKurz, score };
})();
if (typeof module !== 'undefined') module.exports = Tests;
