const Lernstand = (() => {
  const GRENZE = 80;
  const KEY = 'kfz-lernportal-v1';

  const initialState = () => ({ eingangstestFertig: false, themen: {}, sterne: [] });
  const copy = s => ({ eingangstestFertig: s.eingangstestFertig, themen: Object.assign({}, s.themen), sterne: s.sterne.slice() });

  function applyResult(state, thema, prozent, art) {
    const s = copy(state);
    const alt = statusOf(state, thema);
    let neu = alt;
    if (art === 'eingang') neu = prozent >= GRENZE ? 'sitzt' : 'offen';
    else if (art === 'kurz') neu = prozent >= GRENZE ? 'sitzt' : 'angefangen';
    else if (prozent < GRENZE) neu = 'angefangen';
    s.themen[thema] = neu;
    return s;
  }

  function markEingangFertig(state) {
    const s = copy(state);
    s.eingangstestFertig = true;
    return s;
  }

  const statusOf = (state, thema) => state.themen[thema] || 'offen';

  function toggleStern(state, thema) {
    const s = copy(state);
    const i = s.sterne.indexOf(thema);
    if (i >= 0) s.sterne.splice(i, 1); else s.sterne.push(thema);
    return s;
  }

  function nextSteps(state, alleThemen, max = 3) {
    const out = [];
    const add = (thema, text) => { if (out.length < max && !out.some(x => x.thema === thema)) out.push({ thema, text }); };
    state.sterne.filter(t => alleThemen.includes(t)).forEach(t => add(t, t + ' nochmal anschauen (gemerkt)'));
    alleThemen.filter(t => statusOf(state, t) === 'angefangen').forEach(t => add(t, t + ' wiederholen und Kurztest machen'));
    alleThemen.filter(t => statusOf(state, t) === 'offen').forEach(t => add(t, t + ' lernen'));
    return out;
  }

  function fortschritt(state, alleThemen) {
    if (!alleThemen.length) return 0;
    const n = alleThemen.filter(t => statusOf(state, t) === 'sitzt').length;
    return Math.round((n / alleThemen.length) * 100);
  }

  function createStore(storage) {
    let memory = initialState();
    let persistent = false;
    try {
      storage.setItem(KEY + '-test', '1');
      persistent = true;
    } catch (e) { persistent = false; }
    return {
      persistent,
      load() {
        if (!persistent) return copy(memory);
        try {
          const raw = storage.getItem(KEY);
          if (!raw) return initialState();
          const p = JSON.parse(raw);
          return {
            eingangstestFertig: !!p.eingangstestFertig,
            themen: p.themen && typeof p.themen === 'object' ? p.themen : {},
            sterne: Array.isArray(p.sterne) ? p.sterne : []
          };
        } catch (e) { return initialState(); }
      },
      save(state) {
        memory = copy(state);
        if (persistent) { try { storage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* ignorieren */ } }
      }
    };
  }

  return { GRENZE, initialState, applyResult, markEingangFertig, statusOf, toggleStern, nextSteps, fortschritt, createStore };
})();
if (typeof module !== 'undefined') module.exports = Lernstand;
