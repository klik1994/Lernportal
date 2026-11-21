/* Lernportal – Folien-Steuerung: Pfeiltasten, Leertaste, Wischen, Klick.
   Elemente mit class="step" erscheinen nacheinander (wie Animationen in PowerPoint). */
(function () {
  const stage = document.getElementById('stage');
  const slides = Array.from(document.querySelectorAll('.slide'));
  const bar = document.querySelector('#bar i');
  const count = document.getElementById('count');
  let cur = 0, stepIdx = 0;

  const mq = window.matchMedia('(max-width: 820px), (max-height: 520px)');
  const isMobile = () => mq.matches;
  function fit() {
    if (isMobile()) { stage.style.transform = 'none'; return; }
    const wrap = document.getElementById('stage-wrap');
    const s = Math.min(wrap.clientWidth / 1280, wrap.clientHeight / 720) * 0.97;
    stage.style.transform = 'scale(' + s + ')';
  }
  window.addEventListener('resize', fit);
  fit();

  const steps = (i) => Array.from(slides[i].querySelectorAll('.step'));

  function fire(el, on) {
    el.dispatchEvent(new CustomEvent(on ? 'stepon' : 'stepoff', { bubbles: true }));
  }

  function show(i, showAllSteps) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => {
      s.classList.toggle('active', k === i);
      s.classList.toggle('prev', k < i);
      if (k !== i) s.querySelectorAll('video').forEach(v => v.pause());
    });
    if (!showAllSteps) slides[i].scrollTop = 0;
    const st = steps(i);
    stepIdx = showAllSteps ? st.length : 0;
    st.forEach((el, k) => { const on = k < stepIdx; el.classList.toggle('on', on); fire(el, on); });
    cur = i;
    slides[i].dispatchEvent(new CustomEvent('slideshow', { bubbles: true }));
    bar.style.width = ((i + 1) / slides.length * 100) + '%';
    count.textContent = (i + 1) + ' / ' + slides.length;
    try { history.replaceState(null, '', '#' + (i + 1)); } catch (e) {}
  }

  function next() {
    const st = steps(cur);
    if (stepIdx < st.length) {
      const el = st[stepIdx];
      el.classList.add('on'); fire(el, true); stepIdx++;
      if (isMobile()) setTimeout(() => el.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 60);
    }
    else if (cur < slides.length - 1) show(cur + 1, false);
  }
  function prev() {
    const st = steps(cur);
    if (stepIdx > 0) { stepIdx--; st[stepIdx].classList.remove('on'); fire(st[stepIdx], false); }
    else if (cur > 0) show(cur - 1, true);
  }
  window.deck = { next, prev, show };

  document.addEventListener('keydown', (e) => {
    const tag = (e.target.tagName || '').toLowerCase();
    if (tag === 'input' || tag === 'video' || tag === 'button' && (e.key === ' ' || e.key === 'Enter')) return;
    if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); prev(); }
    else if (e.key === 'Home') show(0);
    else if (e.key === 'End') show(slides.length - 1, true);
    else if (e.key === 'f' || e.key === 'F') toggleFs();
  });

  // Klick auf freie Fläche = weiter
  stage.addEventListener('click', (e) => {
    if (e.target.closest('button, a, input, video, label, .opt, .noclick')) return;
    next();
  });

  // Wischen (Handy / Tablet)
  let tx = null, ty = null;
  stage.addEventListener('touchstart', (e) => { tx = e.touches[0].clientX; ty = e.touches[0].clientY; }, { passive: true });
  stage.addEventListener('touchend', (e) => {
    if (tx === null) return;
    const dx = e.changedTouches[0].clientX - tx, dy = e.changedTouches[0].clientY - ty;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) { dx < 0 ? next() : prev(); }
    tx = null;
  });

  function toggleFs() {
    if (!document.fullscreenElement) document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
    else document.exitFullscreen && document.exitFullscreen();
  }
  document.getElementById('btn-prev').onclick = prev;
  document.getElementById('btn-next').onclick = next;
  document.getElementById('btn-fs').onclick = toggleFs;

  // Kurztest
  document.querySelectorAll('.quiz').forEach((quiz) => {
    const qs = quiz.querySelectorAll('.q');
    const score = quiz.querySelector('.score');
    let right = 0, done = 0;
    qs.forEach((q) => {
      const ok = parseInt(q.dataset.correct, 10);
      q.querySelectorAll('.opt').forEach((b, k) => {
        b.addEventListener('click', () => {
          if (q.classList.contains('done')) return;
          q.classList.add('done');
          done++;
          if (k === ok) { b.classList.add('right'); right++; }
          else { b.classList.add('wrong'); q.querySelectorAll('.opt')[ok].classList.add('right'); }
          if (score) score.textContent = right + ' von ' + qs.length + ' richtig' + (done === qs.length ? (right === qs.length ? ' – super!' : ' – schau dir die Folien noch mal an.') : '');
        });
      });
    });
  });

  const start = parseInt((location.hash || '#1').slice(1), 10) - 1;
  show(isNaN(start) ? 0 : start, false);
})();
