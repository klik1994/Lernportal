(function () {
  const root = document.documentElement;
  const btn = document.getElementById('btn-theme');
  function setze(hell) {
    root.classList.toggle('light', hell);
    if (btn) {
      btn.textContent = hell ? '☾' : '☀';
      btn.title = hell ? 'Dunkler Modus' : 'Heller Modus';
      btn.setAttribute('aria-label', btn.title);
    }
  }
  setze(root.classList.contains('light'));
  if (btn) btn.addEventListener('click', () => {
    const hell = !root.classList.contains('light');
    setze(hell);
    try { localStorage.setItem('lp-theme', hell ? 'light' : 'dark'); } catch (e) { /* nicht speicherbar */ }
  });
})();
