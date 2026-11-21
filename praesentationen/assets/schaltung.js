/* Lernportal – wiederverwendbare Grafiken: fließende Teilchen und Stromkreis mit Multimeter. */
(function () {
  const MOBILE = '(max-width: 820px), (max-height: 520px)';
  window.MOBILE_QUERY = MOBILE;
  const NS = 'http://www.w3.org/2000/svg';

  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(e);
    return e;
  }

  /* Teilchen, die entlang eines Pfades wandern. */
  function Flow(parent, pathEl, o) {
    o = Object.assign({ spacing: 40, speed: 70, r: 8, color: '#28aaf5', sign: '', opacity: 1 }, o || {});
    const g = el('g', { 'pointer-events': 'none' }, parent);
    const L = pathEl.getTotalLength();
    const n = Math.floor(L / o.spacing) + 1;
    const dots = [];
    for (let i = 0; i < n; i++) {
      const d = el('g', {}, g);
      el('circle', { r: o.r, fill: o.color }, d);
      if (o.sign) {
        const t = el('text', { 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': o.r * 1.7, 'font-weight': 900, fill: '#0e192b' }, d);
        t.textContent = o.sign;
      }
      dots.push(d);
    }
    let off = 0, last = performance.now(), on = true, alpha = 1;
    const api = { speed: o.speed, spacing: o.spacing };
    function frame(now) {
      const dt = Math.min(0.05, (now - last) / 1000); last = now;
      alpha += ((on ? 1 : 0) - alpha) * Math.min(1, dt * 6);
      g.style.opacity = alpha * o.opacity;
      if (alpha > 0.01) {
        off = (off + api.speed * dt) % api.spacing;
        const cnt = Math.floor(L / api.spacing) + 1;
        dots.forEach((d, i) => {
          const s = i * api.spacing + off;
          if (i >= cnt || s > L) { d.style.display = 'none'; return; }
          d.style.display = '';
          const p = pathEl.getPointAtLength(s);
          d.setAttribute('transform', 'translate(' + p.x + ' ' + p.y + ')');
        });
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
    api.on = (v) => { on = !!v; };
    return api;
  }

  /* Stromkreis: Batterie, Schalter/Lücke, Lampe oder Bauteil, optional Multimeter. */
  function Schaltung(host, o) {
    o = Object.assign({ element: 'lamp', gap: 'wire', meter: false, color: '#f7b612', label: 'Lampe', sublabel: '' }, o || {});
    const M = window.matchMedia(MOBILE).matches, fz = M ? 1.6 : 1;
    const svg = el('svg', { viewBox: M && o.meter ? '0 60 960 420' : '0 0 1136 480', width: '100%', height: '100%' }, host);
    const defs = el('defs', {}, svg);
    const rg = el('radialGradient', { id: 'glow' + Math.random().toString(36).slice(2), cx: '50%', cy: '50%', r: '50%' }, defs);
    el('stop', { offset: '0%', 'stop-color': '#f7b612', 'stop-opacity': '.85' }, rg);
    el('stop', { offset: '100%', 'stop-color': '#f7b612', 'stop-opacity': '0' }, rg);

    const gBat = el('g', { class: 'dev', style: 'transition:opacity .6s' }, svg);
    const gWire = el('g', { style: 'transition:opacity .6s' }, svg);
    el('path', { class: 'wire', d: 'M110 184 V150 H40 V440 H600 V346' }, gWire);
    el('path', { class: 'wire', d: 'M600 254 V120 H470' }, gWire);
    el('path', { class: 'wire', d: 'M370 120 H210 V184' }, gWire);
    if (o.element !== 'lamp') el('path', { class: 'wire', d: 'M600 254 V346' }, gWire);
    const gapWire = el('path', { class: 'wire', d: 'M370 120 H470', style: 'transition:opacity .5s' }, gWire);
    const gSwitch = el('g', { style: 'transition:transform .4s ease; transform-origin:370px 120px' }, svg);
    el('line', { x1: 370, y1: 120, x2: 470, y2: 120, stroke: '#ecf1f8', 'stroke-width': 6, 'stroke-linecap': 'round' }, gSwitch);
    const swLabel = el('text', { x: 420, y: 92, 'text-anchor': 'middle', 'font-size': 18 * fz, fill: '#94a4ba', 'font-weight': 600 }, svg);
    const ends = el('g', {}, svg);
    el('circle', { cx: 370, cy: 120, r: 7, fill: '#ecf1f8' }, ends);
    el('circle', { cx: 470, cy: 120, r: 7, fill: '#ecf1f8' }, ends);

    // Batterie
    el('rect', { x: 70, y: 200, width: 180, height: 130, rx: 10, fill: '#323a48', stroke: '#5a6476', 'stroke-width': 2 }, gBat);
    el('rect', { x: 70, y: 216, width: 180, height: 8, fill: '#424c5e' }, gBat);
    el('rect', { x: 96, y: 184, width: 28, height: 18, rx: 4, fill: '#464e5c' }, gBat);
    el('rect', { x: 196, y: 184, width: 28, height: 18, rx: 4, fill: '#f05e4e' }, gBat);
    const tm = el('text', { x: 110, y: 262, 'text-anchor': 'middle', 'font-size': 30, 'font-weight': 800, fill: '#ecf1f8' }, gBat); tm.textContent = '−';
    const tp = el('text', { x: 210, y: 262, 'text-anchor': 'middle', 'font-size': 30, 'font-weight': 800, fill: '#f05e4e' }, gBat); tp.textContent = '+';
    const tv = el('text', { x: 160, y: 312, 'text-anchor': 'middle', 'font-size': 22 * fz, 'font-weight': 800, fill: '#ecf1f8' }, gBat); tv.textContent = '12 V';
    const xMark = el('g', { opacity: 0, style: 'transition:opacity .5s' }, svg);
    el('path', { d: 'M100 215 L220 320 M100 320 L220 215', stroke: '#f05e4e', 'stroke-width': 8, 'stroke-linecap': 'round' }, xMark);
    const xt = el('text', { x: 160, y: 380, 'text-anchor': 'middle', 'font-size': 20 * fz, 'font-weight': 800, fill: '#f05e4e' }, xMark); xt.textContent = 'abgeklemmt';

    // Stromfluss in technischer Stromrichtung: von + ueber den Verbraucher nach −
    const loop = el('path', { d: 'M210 184 V120 H600 V440 H40 V150 H110 V184', fill: 'none', stroke: 'none' }, svg);
    const flow = Flow(svg, loop, { spacing: 44, speed: 70, r: 7, color: '#28aaf5' });
    flow.on(false);
    const gapMask = el('rect', { x: 380, y: 108, width: 80, height: 24, style: 'fill:var(--bg)', opacity: 0 }, svg);

    // Verbraucher
    let glow, bulb;
    const gEl = el('g', {}, svg);
    if (o.element === 'lamp') {
      el('path', { class: 'wire', d: 'M600 254 V346' }, gEl);
      glow = el('circle', { cx: 600, cy: 300, r: 110, fill: 'url(#' + rg.id + ')', opacity: 0, class: 'glow' }, gEl);
      bulb = el('circle', { cx: 600, cy: 300, r: 46, fill: '#3b4250', stroke: '#ecf1f8', 'stroke-width': 3, style: 'transition:fill .5s' }, gEl);
      el('path', { d: 'M568 268 L632 332 M568 332 L632 268', stroke: '#ecf1f8', 'stroke-width': 3 }, gEl);
    } else {
      el('rect', { x: 576, y: 245, width: 48, height: 110, rx: 4, fill: '#213552', stroke: o.color, 'stroke-width': 4 }, gEl);
    }
    const lampRight = o.element === 'lamp' && !M;
    const lab = el('text', { x: lampRight ? 668 : (o.element === 'lamp' ? 538 : 556), y: 296, 'text-anchor': lampRight ? 'start' : 'end', 'font-size': 20 * fz, 'font-weight': 700, fill: '#ecf1f8' }, gEl);
    lab.textContent = o.label;
    if (o.sublabel) {
      const sl = el('text', { x: 556, y: 296 + 26 * fz, 'text-anchor': 'end', 'font-size': 17 * fz, fill: '#94a4ba' }, gEl); sl.textContent = o.sublabel;
    }

    // Multimeter
    const api = {};
    if (o.meter) {
      const mx = M ? 720 : 860, my = 60, C = o.color;
      const gM = el('g', { class: 'dev', transform: 'translate(' + mx + ' ' + my + ')', opacity: 0, style: 'transition:opacity .5s' }, svg);
      el('rect', { x: 0, y: 0, width: 220, height: 340, rx: 26, fill: C }, gM);
      el('rect', { x: 10, y: 10, width: 200, height: 320, rx: 20, fill: '#2c313a' }, gM);
      el('rect', { x: 28, y: 28, width: 164, height: 82, rx: 8, fill: '#c4d6be' }, gM);
      const rd = el('text', { x: 180, y: 96, 'text-anchor': 'end', 'font-size': 38, 'font-weight': 800, fill: '#19231c' }, gM);
      const unit = el('text', { x: 38, y: 48, 'font-size': 14, 'font-weight': 800, fill: '#19231c' }, gM);
      const cx = 110, cy = 206;
      const pos = { V: -150, 'Ω': -90, A: -30, OFF: 165 };
      const labs = {};
      for (const k in pos) {
        const r = pos[k] * Math.PI / 180;
        const t = el('text', { x: cx + 68 * Math.cos(r), y: cy + 64 * Math.sin(r) + 6, 'text-anchor': 'middle', 'font-size': k === 'OFF' ? 12 : 15, 'font-weight': 800, fill: '#94a4ba' }, gM);
        t.textContent = k === 'V' ? 'V DC' : k; labs[k] = t;
      }
      el('circle', { cx, cy, r: 42, fill: '#1e2128', stroke: '#505662', 'stroke-width': 3 }, gM);
      const ptr = el('line', { x1: cx, y1: cy, x2: cx + 36, y2: cy, stroke: C, 'stroke-width': 7, 'stroke-linecap': 'round', style: 'transition:transform .5s ease; transform-origin:' + cx + 'px ' + cy + 'px' }, gM);
      const socks = { A: [52, 296], COM: [110, 296], 'VΩ': [168, 296] };
      const sockEls = {};
      for (const k in socks) {
        const [sx, sy] = socks[k];
        const t = el('text', { x: sx, y: sy - 24, 'text-anchor': 'middle', 'font-size': 13, 'font-weight': 800, fill: '#94a4ba' }, gM); t.textContent = k;
        sockEls[k] = el('circle', { cx: sx, cy: sy, r: 15, fill: k === 'COM' ? '#141619' : '#f05e4e', stroke: '#5a606c', 'stroke-width': 2 }, gM);
        el('circle', { cx: sx, cy: sy, r: 6, fill: '#0a0a0c' }, gM);
      }
      api.meter = (show, mode, reading, unitTxt) => {
        gM.setAttribute('opacity', show ? 1 : 0);
        ptr.style.transform = 'rotate(' + (pos[mode || 'OFF']) + 'deg)';
        for (const k in labs) labs[k].setAttribute('fill', k === mode ? C : '#94a4ba');
        rd.textContent = reading || '';
        unit.textContent = unitTxt || '';
      };
      api.meter(false, 'OFF');
      const leads = [];
      api.addLead = (sock, tx, ty, color, sag) => {
        const [sx0, sy0] = socks[sock];
        const sx = sx0 + mx, sy = sy0 + my;
        const g = el('g', {}, svg);
        const p = el('path', { class: 'lead ' + (color === 'red' ? 'lead-red' : 'lead-black'), pathLength: 1,
          d: 'M' + sx + ' ' + sy + ' Q ' + ((sx + tx) / 2) + ' ' + (Math.max(sy, ty) + (sag || 60)) + ' ' + tx + ' ' + ty }, g);
        const pr = el('circle', { class: 'probe', cx: tx, cy: ty, r: 9, fill: color === 'red' ? '#f05e4e' : '#2a2c32', stroke: '#ecf1f8', 'stroke-width': 2 }, g);
        leads.push({ p, pr, sock });
        return leads.length - 1;
      };
      api.lead = (i, on) => {
        leads[i].p.classList.toggle('on', on); leads[i].pr.classList.toggle('on', on);
        sockEls[leads[i].sock].setAttribute('stroke', on ? C : '#5a606c');
      };
      // Messpunkte (pulsierend)
      api.points = (pts, on) => {
        if (!api._pts) api._pts = pts.map(([x, y]) => el('circle', { cx: x, cy: y, r: 11, fill: C, class: 'pulse', opacity: 0 }, svg));
        api._pts.forEach(c => c.setAttribute('opacity', on ? 1 : 0));
      };
    }

    api.lamp = (k) => {
      if (!glow) return;
      glow.setAttribute('opacity', k);
      bulb.setAttribute('fill', k > 0.5 ? '#f7b612' : '#3b4250');
    };
    api.flow = (on) => flow.on(on);
    api.flowSpeed = (s) => { flow.speed = s; };
    api.gap = (state) => {
      // 'wire' geschlossen, 'open' aufgetrennt, 'switch-open', 'switch-closed', 'meter' (Messgerät dazwischen)
      gapWire.style.opacity = state === 'wire' ? 1 : 0;
      gSwitch.style.display = state.startsWith('switch') ? '' : 'none';
      gSwitch.style.transform = state === 'switch-open' ? 'rotate(-32deg)' : 'none';
      swLabel.textContent = state.startsWith('switch') ? 'Schalter' : (state === 'open' ? 'aufgetrennt' : '');
      swLabel.setAttribute('fill', state === 'open' ? '#f05e4e' : '#94a4ba');
      gapMask.setAttribute('opacity', state === 'wire' || state === 'switch-closed' ? 0 : 1);
    };
    api.battery = (on) => {
      gBat.style.opacity = on ? 1 : 0.25; gWire.style.opacity = on ? 1 : 0.25;
      xMark.setAttribute('opacity', on ? 0 : 1);
    };
    api.gap(o.gap);
    return api;
  }

  window.Flow = Flow;
  window.Schaltung = Schaltung;
  window.svgEl = el;
})();
