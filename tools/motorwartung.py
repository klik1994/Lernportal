"""Motor und Wartung – vier Präsentationen.
Aufruf: cd tools && python3 motorwartung.py"""
from praesentation_bauen import *

K = 'MOTOR UND WARTUNG'
UL = 'style="font-size:17px;line-height:1.55;padding-left:20px;margin:8px 0 0"'
STYLE = '''  .symbol { font-size: 80px; }
  .rb { display: flex; flex-wrap: wrap; justify-content: center; gap: 6px; font-size: 44px; font-weight: 900; margin: 6px 0 14px; }
  .rb span { cursor: pointer; padding: 4px 12px; border-radius: 12px; background: var(--card); transition: background .2s, color .2s; }
  .rb span.on { background: var(--c); color: var(--on-c); }
  .mp { cursor: pointer; }
  html.light svg text[fill="#ffd34d"] { fill: #8a6400; }
  @media (max-width: 820px), (max-height: 520px) { .rb { font-size: 30px; } .val b { font-size: 14px; hyphens: auto; overflow-wrap: anywhere; } }'''


def btns(attr, items, first=0):
    return ''.join(f'<button class="btn ghost{" on" if i == first else ""}" data-{attr}="{k}">{t}</button>' for i, (k, t) in enumerate(items))


def svgbox(pid, w, h, extra=''):
    return f'''<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="display:block;margin:0 auto;max-width:100%;height:auto" id="{pid}-svg">
      <rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#18283f"/>{extra}<g id="{pid}-g"></g></svg>'''


# ================================================================ 1 Viertakt
T = 'VIERTAKT'

viertakt = [
    titel_folie(K, '4T', 'Der Viertaktmotor', 'Arbeitsweise, Otto und Diesel, Hubraum, Verdichtung, Zündfolge', 'font-size:110px'),
    lernziele(T, ['Wie ein Viertaktmotor arbeitet', 'Was Otto- und Dieselmotor unterscheidet',
                  'Wie du Hubraum und Verdichtung berechnest', 'Was Zündfolge und Zündabstand bedeuten']),
    folie(T, 'Die vier Takte – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap;gap:6px"><button class="btn" id="vt-play" style="--c:var(--ora)">⏸ Pause</button>{btns('t', [('0', '1 · Ansaugen'), ('1', '2 · Verdichten'), ('2', '3 · Arbeiten'), ('3', '4 · Ausstoßen')], first=-1)}</div>
    <div class="grid2" style="align-items:center;grid-template-columns:0.9fr 1.1fr">
      {svgbox('vt', 520, 420)}
      <div class="card" id="vt-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>''', sid='s-vt', body_cls='body noclick'),
    folie(T, 'Ottomotor und Dieselmotor', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Ottomotor</div>
        <ul UL><li><b>Fremdzündung</b>: die Zündkerze zündet das Gemisch</li><li>Verdichtung ca. 10 : 1 bis 14 : 1</li><li>Luftmenge über die Drosselklappe geregelt</li><li>Kraftstoff: Benzin (auch Gas)</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Dieselmotor</div>
        <ul UL><li><b>Selbstzündung</b>: nur Luft wird so stark verdichtet, dass sie sehr heiß wird – der eingespritzte Diesel entzündet sich von selbst</li><li>Verdichtung ca. 15 : 1 bis 20 : 1</li><li>Leistung über die Einspritzmenge geregelt</li><li>Glühkerzen helfen beim Kaltstart</li></ul></div>
    </div>
    <p class="muted" style="font-size:14px">Richtwerte – genaue Werte laut Hersteller.</p>'''.replace('UL', UL)),
    folie(T, 'Hubraum und Verdichtung – zum Ausprobieren', '''    <div class="ctrl"><span style="width:290px">Bohrung d: <span class="c" id="hr-dn">81 mm</span></span><input type="range" id="hr-d" min="65" max="100" step="0.5" value="81"></div>
    <div class="ctrl"><span style="width:290px">Hub s: <span class="c" id="hr-sn">86,5 mm</span></span><input type="range" id="hr-s" min="65" max="100" step="0.5" value="86.5"></div>
    <div class="ctrl"><span style="width:290px">Zylinder z: <span class="c" id="hr-zn">4</span></span><input type="range" id="hr-z" min="1" max="8" step="1" value="4"></div>
    <div class="ctrl"><span style="width:290px">Verdichtungsraum Vc: <span class="c" id="hr-cn">45 cm³</span></span><input type="range" id="hr-c" min="20" max="80" step="1" value="45"></div>
    <div class="grid3" style="margin-top:12px">
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">HUBRAUM EIN ZYLINDER Vh</div><div class="lcd2" id="hr-vh" style="font-size:26px">–</div></div>
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">GESAMTHUBRAUM VH</div><div class="lcd2" id="hr-VH" style="font-size:26px">–</div></div>
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">VERDICHTUNG ε</div><div class="lcd2" id="hr-e" style="font-size:26px">–</div></div>
    </div>
    <div class="card" style="font-size:16px;font-weight:600;line-height:1.6;margin-top:12px">Vh = π/4 · d² · s &nbsp;·&nbsp; VH = Vh · z &nbsp;·&nbsp; ε = (Vh + Vc) : Vc<br><span class="muted">Hubraum: Raum, den der Kolben zwischen UT und OT „verdrängt“. Verdichtungsraum: Raum über dem Kolben im OT.</span></div>''', sid='s-hr', body_cls='body noclick'),
    folie(T, 'Zündfolge – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px">{btns('z', [('4', '4 Zylinder'), ('6', '6 Zylinder (Reihe)')])}</div>
    {svgbox('zf', 640, 200)}
    <div class="card" id="zf-t" style="font-size:16px;font-weight:600;line-height:1.55;margin-top:10px"></div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Übliche Zündfolgen – die genaue Zündfolge steht in den Herstellerunterlagen.</p>''', sid='s-zf', body_cls='body noclick'),
    folie(T, 'Leistung und Drehmoment', '''    <div class="values">
      <div class="val step from-left"><b>Drehmoment M</b><span>„Drehkraft“ an der Kurbelwelle in Nm – spürbar als Durchzug</span></div>
      <div class="val step from-left"><b>Leistung P</b><span>in kW: P = M · n : 9550 (M in Nm, n in 1/min)</span></div>
      <div class="val step from-left"><b>Beispiel</b><span>250 Nm bei 3.000 1/min → 250 · 3000 : 9550 ≈ 79 kW</span></div>
      <div class="val step from-left"><b>Fahrzeugschein</b><span>P.1 Hubraum in cm³ · P.2 Nennleistung in kW · P.4 Nenndrehzahl</span></div>
    </div>'''),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Motor von Hand drehen</b>Immer an der Kurbelwelle und nur in Motordrehrichtung – nie über das Nockenwellenrad.</div>
      <div class="tip step"><b>OT Zylinder 1</b>Für Arbeiten am Steuertrieb gibt es Markierungen oder Arretierwerkzeuge – Vorgaben des Herstellers beachten.</div>
      <div class="tip step"><b>Zylinder 1</b>Zylinder 1 liegt meist auf der Steuertriebseite (Riemen oder Kette) – laut Hersteller prüfen.</div>
      <div class="warn step"><b>Heiße Teile</b>Motor, Abgasanlage und Kühlsystem werden sehr heiß. Vor Arbeiten abkühlen lassen.</div>
    </div>'''),
    video(T, 'mw-viertakt'),
    kurztest(T, [
        ('In welchem Takt sind beide Ventile geschlossen und der Kolben bewegt sich nach unten?', ['Ansaugen', 'Arbeiten', 'Ausstoßen'], 1, 'Die Verbrennung drückt den Kolben von OT nach UT.'),
        ('Wie oft dreht sich die Kurbelwelle bei einem Arbeitsspiel?', ['1-mal', '2-mal (720°)', '4-mal'], 1, 'Die Nockenwelle dreht sich dabei nur einmal.'),
        ('Wodurch entzündet sich der Kraftstoff im Dieselmotor?', ['Durch die Zündkerze', 'Durch die Glühkerze bei jedem Takt', 'Durch die heiße, stark verdichtete Luft'], 2, 'Selbstzündung – die Glühkerze hilft nur beim Kaltstart.'),
        ('Welche Zündfolge hat ein Vierzylinder meist?', ['1-3-4-2', '1-2-3-4', '4-3-2-1'], 0, 'Zündabstand 720° : 4 = 180°.'),
    ]),
    merke(T, ['Ansaugen – Verdichten – Arbeiten – Ausstoßen', '1 Arbeitsspiel = 2 Kurbelwellen-Umdrehungen',
              'Otto: Fremdzündung · Diesel: Selbstzündung', 'ε = (Vh + Vc) : Vc · Zündabstand = 720° : z']),
]
viertakt_js = '''<script>
(function () {
  const g = (id, s) => document.getElementById(id).innerHTML = s;
  // Vier Takte
  let th = 0, lauf = true, last = null;
  const N = ['Ansaugen', 'Verdichten', 'Arbeiten', 'Ausstoßen'];
  const TX = [
    '<b>1 · Ansaugen:</b> Der Kolben geht von OT nach UT. Das <span class="c">Einlassventil ist offen</span>, frisches Gemisch (Otto) oder Luft (Diesel) strömt in den Zylinder.',
    '<b>2 · Verdichten:</b> Beide Ventile sind zu. Der Kolben geht von UT nach OT und <span class="c">verdichtet</span> die Füllung – sie wird warm und steht unter hohem Druck.',
    '<b>3 · Arbeiten:</b> Kurz vor OT wird gezündet (Otto) bzw. eingespritzt (Diesel). Die Verbrennung drückt den Kolben mit großer Kraft nach unten – <span class="c">nur dieser Takt gibt Arbeit ab</span>.',
    '<b>4 · Ausstoßen:</b> Das <span class="c">Auslassventil ist offen</span>, der Kolben schiebt das Abgas aus dem Zylinder. Danach beginnt alles von vorn.'
  ];
  function zeichne() {
    const r = 70, L = 170, cx = 210, cy = 330, a = th * Math.PI / 180;
    const yp = cy - (r * Math.cos(a) + Math.sqrt(L * L - Math.pow(r * Math.sin(a), 2)));
    const takt = Math.floor((th % 720) / 180), ein = takt === 0, aus = takt === 3, funke = th % 720 > 340 && th % 720 < 380;
    const top = yp - 10;
    const gas = takt === 0 || takt === 1 ? '#1fc8b3' : takt === 2 ? (th % 720 < 420 ? '#ff8f3f' : '#c97a3a') : '#7d8796';
    let o = '';
    o += '<rect x="150" y="70" width="120" height="' + (top - 70) + '" fill="' + gas + '" opacity=".45"/>';
    o += '<path d="M146 66 V282 M274 66 V282" stroke="#ecf1f8" stroke-width="6"/><path d="M120 66 H300" stroke="#ecf1f8" stroke-width="6"/>';
    o += '<path d="M120 40 H160 V66 M300 40 H260 V66" fill="none" stroke="#94a4ba" stroke-width="4"/>';
    const vi = ein ? 14 : 0, vo = aus ? 14 : 0;
    o += '<line x1="178" y1="20" x2="178" y2="' + (62 + vi) + '" stroke="#ecf1f8" stroke-width="5"/><rect x="164" y="' + (62 + vi) + '" width="28" height="6" fill="#ecf1f8"/>';
    o += '<line x1="242" y1="20" x2="242" y2="' + (62 + vo) + '" stroke="#ecf1f8" stroke-width="5"/><rect x="228" y="' + (62 + vo) + '" width="28" height="6" fill="#ecf1f8"/>';
    o += '<text x="120" y="32" font-size="13" font-weight="800" fill="' + (ein ? '#1fc8b3' : '#94a4ba') + '">Einlass</text><text x="300" y="32" text-anchor="end" font-size="13" font-weight="800" fill="' + (aus ? '#ffd34d' : '#94a4ba') + '">Auslass</text>';
    o += '<line x1="210" y1="56" x2="210" y2="74" stroke="#94a4ba" stroke-width="4"/>';
    if (funke) o += '<path d="M210 74 l-8 10 l10 0 l-6 12" fill="none" stroke="#ffd34d" stroke-width="4"/>';
    o += '<rect x="152" y="' + top + '" width="116" height="52" rx="4" fill="#94a4ba"/><line x1="152" y1="' + (top + 10) + '" x2="268" y2="' + (top + 10) + '" stroke="#18283f" stroke-width="2"/><line x1="152" y1="' + (top + 18) + '" x2="268" y2="' + (top + 18) + '" stroke="#18283f" stroke-width="2"/>';
    const kx = cx + r * Math.sin(a), ky = cy - r * Math.cos(a);
    o += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (r + 14) + '" fill="none" stroke="#94a4ba" stroke-width="2" stroke-dasharray="6 6"/>';
    o += '<line x1="' + cx + '" y1="' + yp + '" x2="' + kx + '" y2="' + ky + '" stroke="#ecf1f8" stroke-width="10" stroke-linecap="round"/>';
    o += '<line x1="' + cx + '" y1="' + cy + '" x2="' + kx + '" y2="' + ky + '" stroke="#ff8f3f" stroke-width="12" stroke-linecap="round"/><circle cx="' + cx + '" cy="' + cy + '" r="10" fill="#ecf1f8"/>';
    const yOT = cy - r - L - 10, yUT = cy + r - L - 10;
    o += '<text x="300" y="' + (yOT + 5) + '" font-size="13" font-weight="800" fill="#94a4ba">OT</text><text x="300" y="' + (yUT + 5) + '" font-size="13" font-weight="800" fill="#94a4ba">UT</text>';
    o += '<line x1="278" y1="' + yOT + '" x2="296" y2="' + yOT + '" stroke="#94a4ba" stroke-width="2"/><line x1="278" y1="' + yUT + '" x2="296" y2="' + yUT + '" stroke="#94a4ba" stroke-width="2"/>';
    o += '<text x="345" y="200" font-size="24" font-weight="900" fill="#ff8f3f">' + (takt + 1) + ' · ' + N[takt] + '</text>';
    o += '<text x="345" y="226" font-size="15" font-weight="800" fill="#94a4ba">' + Math.round(th % 720) + '° Kurbelwinkel</text>';
    g('vt-g', o);
    document.getElementById('vt-t').innerHTML = TX[takt] + '<br><span class="muted" style="font-size:15px">Ein Arbeitsspiel = 2 Umdrehungen der Kurbelwelle (720°). Die Nockenwelle dreht nur halb so schnell.</span>';
  }
  function tick(ts) { if (last !== null && lauf) th = (th + (ts - last) * 0.12) % 720; last = ts; zeichne(); requestAnimationFrame(tick); }
  requestAnimationFrame(tick);
  const pb = document.getElementById('vt-play');
  pb.onclick = () => { lauf = !lauf; pb.textContent = lauf ? '⏸ Pause' : '▶ Weiter'; };
  document.querySelectorAll('#s-vt [data-t]').forEach(b => b.onclick = () => { th = +b.dataset.t * 180 + 90; lauf = false; pb.textContent = '▶ Weiter'; });

  // Hubraum
  const ids = ['d', 's', 'z', 'c'];
  const fmt = (v, n) => v.toLocaleString('de-DE', { minimumFractionDigits: n, maximumFractionDigits: n });
  function hr() {
    const d = +document.getElementById('hr-d').value, s = +document.getElementById('hr-s').value, z = +document.getElementById('hr-z').value, c = +document.getElementById('hr-c').value;
    const vh = Math.PI / 4 * (d / 10) * (d / 10) * (s / 10);
    document.getElementById('hr-dn').textContent = fmt(d, d % 1 ? 1 : 0) + ' mm';
    document.getElementById('hr-sn').textContent = fmt(s, s % 1 ? 1 : 0) + ' mm';
    document.getElementById('hr-zn').textContent = z;
    document.getElementById('hr-cn').textContent = c + ' cm³';
    document.getElementById('hr-vh').textContent = fmt(vh, 0) + ' cm³';
    document.getElementById('hr-VH').textContent = fmt(vh * z, 0) + ' cm³';
    document.getElementById('hr-e').textContent = fmt((vh + c) / c, 1) + ' : 1';
  }
  ids.forEach(i => document.getElementById('hr-' + i).addEventListener('input', hr)); hr();

  // Zündfolge
  const ZF = { 4: [1, 3, 4, 2], 6: [1, 5, 3, 6, 2, 4] };
  let zn = 4, zi = 0;
  function zf() {
    const f = ZF[zn], w = 600 / zn; let o = '';
    for (let i = 1; i <= zn; i++) {
      const x = 20 + (i - 1) * w, an = f[zi] === i;
      o += '<rect x="' + (x + 8) + '" y="40" width="' + (w - 16) + '" height="110" rx="12" fill="' + (an ? '#ff8f3f' : '#213552') + '" stroke="#ecf1f8" stroke-width="3"/>';
      o += '<text x="' + (x + w / 2) + '" y="105" text-anchor="middle" font-size="34" font-weight="900" fill="' + (an ? '#0e192b' : '#ecf1f8') + '">' + i + '</text>';
    }
    o += '<text x="320" y="185" text-anchor="middle" font-size="16" font-weight="800" fill="#94a4ba">Zündfolge: ' + f.join(' – ') + '</text>';
    g('zf-g', o);
    document.getElementById('zf-t').innerHTML = '<b>' + zn + ' Zylinder:</b> Gerade zündet <span class="c">Zylinder ' + f[zi] + '</span>. Zündabstand = 720° : ' + zn + ' = <b>' + (720 / zn) + '° KW</b>. Die Zündfolge verteilt die Kräfte gleichmäßig auf die Kurbelwelle – der Motor läuft ruhiger.';
  }
  setInterval(() => { zi = (zi + 1) % ZF[zn].length; zf(); }, 900);
  document.querySelectorAll('#s-zf [data-z]').forEach(b => b.onclick = () => { zn = +b.dataset.z; zi = 0; document.querySelectorAll('#s-zf [data-z]').forEach(x => x.classList.toggle('on', x === b)); zf(); });
  zf();
})();
</script>'''


# ================================================================ 2 Kurbel- und Ventiltrieb
T = 'MOTORMECHANIK'

triebwerk = [
    titel_folie(K, 'OT', 'Kurbel- und Ventiltrieb', 'Kolben, Pleuel, Kurbelwelle, Nockenwelle, Zahnriemen und Kette', 'font-size:110px'),
    lernziele(T, ['Welche Teile zum Kurbeltrieb gehören', 'Wie der Ventiltrieb arbeitet und warum es Ventilspiel gibt',
                  'Was Zahnriemen und Steuerkette unterscheidet', 'Warum die Steuerzeiten stimmen müssen']),
    folie(T, 'Der Kurbeltrieb', '''    <div class="values">
      <div class="val step from-left"><b>Kolben</b><span>nimmt den Verbrennungsdruck auf – mit Kolbenringen</span></div>
      <div class="val step from-left"><b>Kolbenringe</b><span>2 Verdichtungsringe dichten ab, 1 Ölabstreifring streift Öl von der Zylinderwand</span></div>
      <div class="val step from-left"><b>Pleuel</b><span>verbindet Kolben (über den Kolbenbolzen) und Kurbelwelle</span></div>
      <div class="val step from-left"><b>Kurbelwelle</b><span>macht aus der Auf- und Abbewegung eine Drehbewegung</span></div>
      <div class="val step from-left"><b>Schwungrad</b><span>speichert Schwung, gleicht Stöße aus – oft als Zweimassenschwungrad</span></div>
    </div>'''),
    folie(T, 'Ventiltrieb und Ventilspiel – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap">{btns('v', [('0', 'Ventilspiel richtig'), ('1', 'Ventilspiel zu groß'), ('2', 'Ventilspiel zu klein')])}</div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {svgbox('vs', 560, 300)}
      <div class="card" id="vs-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Vereinfacht. Ventilspiel einstellen nur nach Herstellerangabe (kalt oder warm gemessen).</p>''', sid='s-vs', body_cls='body noclick'),
    folie(T, 'Zahnriemen oder Steuerkette', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Zahnriemen</div>
        <ul UL><li>leise und leicht</li><li><b>muss nach Intervall gewechselt werden</b> (km und Jahre laut Hersteller)</li><li>Spannrolle und Umlenkrollen mit tauschen, oft auch die Wasserpumpe</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Steuerkette</div>
        <ul UL><li>sehr haltbar</li><li>kann sich längen – Rasseln beim Kaltstart ist ein Warnzeichen</li><li>hydraulischer Kettenspanner – braucht guten Öldruck und sauberes Öl</li></ul></div>
    </div>
    <div class="warn step" style="margin-top:12px"><b>Reißt der Riemen oder springt die Kette über</b>bleiben die Ventile stehen. Bei vielen Motoren schlagen dann die Kolben gegen die offenen Ventile – schwerer Motorschaden.</div>'''.replace('UL', UL)),
    folie(T, 'Steuerzeiten – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap">{btns('s', [('0', 'Richtig eingestellt'), ('1', 'Einen Zahn versetzt')])}<button class="btn" id="sz-play" style="--c:var(--pur)">⏸ Pause</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {svgbox('sz', 520, 340)}
      <div class="card" id="sz-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>''', sid='s-sz', body_cls='body noclick'),
    folie(T, 'Hydrostößel und Nockenwellenverstellung', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Hydrostößel</div>
        <ul UL><li>gleicht das Ventilspiel mit Motoröl selbst aus</li><li>kurzes Klappern direkt nach dem Kaltstart ist oft normal</li><li>klappert es dauerhaft: Ölstand, Öldruck und Ölsorte prüfen</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Nockenwellenverstellung</div>
        <ul UL><li>das Steuergerät verdreht die Nockenwelle mit Öldruck über ein Magnetventil</li><li>so passen die Steuerzeiten zu Drehzahl und Last</li><li>Fehler: Fehlerspeicher, Ölqualität, Magnetventil prüfen</li></ul></div>
    </div>'''.replace('UL', UL)),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Spezialwerkzeug</b>Steuerzeiten nur mit dem vorgeschriebenen Arretierwerkzeug einstellen.</div>
      <div class="tip step"><b>Nach der Arbeit</b>Motor von Hand zwei Umdrehungen an der Kurbelwelle durchdrehen und alle Marken erneut prüfen – erst dann starten.</div>
      <div class="warn step"><b>Zylinderkopfschrauben</b>Oft Dehnschrauben: immer erneuern. Anziehen in vorgeschriebener Reihenfolge mit Drehmoment und Drehwinkel laut Hersteller.</div>
      <div class="tip step"><b>Kundenhinweis</b>Zahnriemen-Intervall im Serviceheft prüfen – ein überfälliger Riemen ist ein großes Risiko.</div>
    </div>'''),
    video(T, 'mw-triebwerk'),
    kurztest(T, [
        ('Welche Aufgabe hat der Ölabstreifring?', ['Er dichtet den Brennraum ab', 'Er streift Öl von der Zylinderwand', 'Er kühlt den Kolben'], 1, 'Sonst würde Öl in den Brennraum gelangen und verbrennen.'),
        ('Wie schnell dreht sich die Nockenwelle im Vergleich zur Kurbelwelle?', ['Halb so schnell', 'Gleich schnell', 'Doppelt so schnell'], 0, 'Übersetzung 2 : 1 – ein Arbeitsspiel dauert 2 Kurbelwellen-Umdrehungen.'),
        ('Was passiert bei zu kleinem Ventilspiel?', ['Das Ventil klappert laut', 'Nichts', 'Das Ventil schließt nicht ganz und kann verbrennen'], 2, 'Zu großes Spiel: Klappern, das Ventil öffnet zu spät und zu wenig.'),
        ('Was tust du nach dem Einstellen der Steuerzeiten?', ['Sofort starten', 'Motor von Hand 2 Umdrehungen durchdrehen und Marken prüfen', 'Ölwechsel machen'], 1, 'So erkennst du Fehler, bevor Ventile und Kolben Schaden nehmen.'),
    ]),
    merke(T, ['Kolben – Pleuel – Kurbelwelle: Hub wird Drehung', 'Nockenwelle dreht halb so schnell',
              'Ventilspiel: zu groß klappert, zu klein verbrennt', 'Steuerzeiten mit Spezialwerkzeug, danach 2 Umdrehungen prüfen']),
]
triebwerk_js = '''<script>
(function () {
  const g = (id, s) => document.getElementById(id).innerHTML = s;
  // Ventiltrieb
  let vm = 0, ph = 0;
  const SP = [0, 6, -4];
  const VT = [
    '<b class="grn">Ventilspiel richtig:</b> Zwischen Nocken und Hebel bleibt ein kleiner Spalt, wenn das Ventil zu ist. Wird der Motor heiß, dehnen sich die Teile aus – das Spiel fängt das auf. Das Ventil schließt immer ganz.',
    '<b class="ora">Zu groß:</b> Der Nocken muss erst den Spalt überwinden. Es <span class="ora">klappert</span>, das Ventil öffnet <b>später, kürzer und weniger weit</b> – weniger Füllung, weniger Leistung.',
    '<b class="red">Zu klein:</b> Wird der Motor warm, wächst das Ventil – es <span class="red">schließt nicht mehr ganz</span>. Heißes Gas strömt vorbei: Das Ventil verbrennt, die Kompression sinkt.'
  ];
  const kontur = a => { const x = Math.cos(a); return x > 0.55 ? 30 * Math.pow((x - 0.55) / 0.45, 0.8) : 0; };
  const SPX = [5, 13, -4];
  function vs() {
    const sp = SPX[vm], cx = 140, R = 42, cy = 92 - sp, F0 = 92 + R;
    let d = '';
    for (let i = 0; i <= 90; i++) { const a = i / 90 * 2 * Math.PI, rr = R + kontur(a - ph); d += (i ? ' L' : 'M') + (cx + rr * Math.sin(a)).toFixed(1) + ' ' + (cy + rr * Math.cos(a)).toFixed(1); }
    const cam = kontur(-ph), hub = Math.max(0, cam - sp), spalt = Math.max(0, sp - cam);
    let o = '<path d="' + d + ' Z" fill="#213552" stroke="#ecf1f8" stroke-width="4"/><circle cx="' + cx + '" cy="' + cy + '" r="8" fill="#94a4ba"/>';
    o += '<text x="214" y="70" font-size="14" font-weight="800" fill="#94a4ba">← Nockenwelle</text>';
    const ty = F0 + hub;
    o += '<rect x="' + (cx - 26) + '" y="' + ty + '" width="52" height="18" rx="4" fill="#94a4ba"/>';
    o += '<line x1="' + cx + '" y1="' + (ty + 18) + '" x2="' + cx + '" y2="' + (ty + 90) + '" stroke="#ecf1f8" stroke-width="7"/>';
    o += '<rect x="' + (cx - 34) + '" y="' + (ty + 88) + '" width="68" height="10" rx="3" fill="#ecf1f8"/>';
    const seat = F0 + 98;
    o += '<path d="M50 ' + seat + ' H' + (cx - 36) + ' M' + (cx + 36) + ' ' + seat + ' H230" stroke="#94a4ba" stroke-width="5"/>';
    if (spalt > 1) o += '<text x="' + (cx + 34) + '" y="' + (F0 + 2) + '" font-size="13" font-weight="800" fill="#ffd34d">Spalt</text>';
    if (sp < 0) o += '<text x="' + (cx + 40) + '" y="' + (seat + 24) + '" font-size="13" font-weight="800" fill="#f05e4e">schließt nicht ganz!</text>';
    o += '<text x="' + (cx - 40) + '" y="' + (seat + 24) + '" text-anchor="end" font-size="14" font-weight="800" fill="#94a4ba">Ventil</text>';
    let k = '';
    for (let i = 0; i <= 120; i++) { const a = (i / 120 - 0.5) * 2 * Math.PI, h = Math.max(0, kontur(a) - sp); k += (i ? ' L' : 'M') + (300 + i * 2) + ' ' + (240 - h * 3.5).toFixed(1); }
    o += '<line x1="300" y1="240" x2="545" y2="240" stroke="#94a4ba" stroke-width="2"/><path d="' + k + '" fill="none" stroke="#a07cf5" stroke-width="4"/>';
    const pa = ((-ph % (2 * Math.PI)) + 3 * Math.PI) % (2 * Math.PI), mx = 300 + pa / (2 * Math.PI) * 240;
    o += '<line x1="' + mx + '" y1="110" x2="' + mx + '" y2="245" stroke="#ffd34d" stroke-width="2"/>';
    o += '<text x="300" y="100" font-size="14" font-weight="800" fill="#94a4ba">Ventilhub</text>';
    g('vs-g', o);
  }
  setInterval(() => { ph = (ph + 0.06) % (2 * Math.PI); vs(); }, 40);
  document.querySelectorAll('#s-vs [data-v]').forEach(b => b.onclick = () => { vm = +b.dataset.v; document.querySelectorAll('#s-vs [data-v]').forEach(x => x.classList.toggle('on', x === b)); document.getElementById('vs-t').innerHTML = VT[vm]; });
  document.getElementById('vs-t').innerHTML = VT[0];

  // Steuerzeiten
  let sm = 0, w = 0, sl = true;
  const ST = [
    '<b class="grn">Richtig eingestellt:</b> Die Marken an Kurbelwelle und Nockenwelle stehen genau an ihren Gegenmarken. Das Nockenwellenrad hat doppelt so viele Zähne – es dreht <span class="c">halb so schnell</span>.',
    '<b class="red">Ein Zahn versetzt:</b> Die Nockenwelle steht um einige Grad falsch. Die Ventile öffnen zu früh oder zu spät: Leistungsverlust, unruhiger Lauf, Fehlerspeicher „Zuordnung Kurbelwelle/Nockenwelle“. Bei mehreren Zähnen können Ventile und Kolben zusammenstoßen.'
  ];
  function sz() {
    const kx = 160, ky = 260, kr = 34, nx = 360, ny = 90, nr = 68, off = sm ? 15 : 0;
    const ak = w, an = w / 2 + off;
    let o = '<path d="M' + (kx - kr) + ' ' + ky + ' L' + (nx - nr) + ' ' + ny + ' A' + nr + ' ' + nr + ' 0 0 1 ' + (nx + nr) + ' ' + ny + ' L' + (kx + kr) + ' ' + ky + ' A' + kr + ' ' + kr + ' 0 0 1 ' + (kx - kr) + ' ' + ky + '" fill="none" stroke="#a07cf5" stroke-width="8" stroke-dasharray="6 3"/>';
    o += '<circle cx="' + kx + '" cy="' + ky + '" r="' + kr + '" fill="#213552" stroke="#ecf1f8" stroke-width="4"/><circle cx="' + nx + '" cy="' + ny + '" r="' + nr + '" fill="#213552" stroke="#ecf1f8" stroke-width="4"/>';
    const m = (x, y, r, a, c) => { const ra = a * Math.PI / 180; return '<line x1="' + x + '" y1="' + y + '" x2="' + (x + r * Math.sin(ra)) + '" y2="' + (y - r * Math.cos(ra)) + '" stroke="' + c + '" stroke-width="5"/><circle cx="' + (x + (r - 6) * Math.sin(ra)) + '" cy="' + (y - (r - 6) * Math.cos(ra)) + '" r="6" fill="' + c + '"/>'; };
    o += m(kx, ky, kr - 4, ak, '#ffd34d') + m(nx, ny, nr - 6, an, '#ffd34d');
    o += '<path d="M' + kx + ' ' + (ky - kr - 16) + ' l-8 -12 h16 Z" fill="#ecf1f8"/><path d="M' + nx + ' ' + (ny - nr - 16) + ' l-8 -12 h16 Z" fill="#ecf1f8"/>';
    o += '<text x="' + kx + '" y="' + (ky + kr + 26) + '" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Kurbelwelle</text><text x="' + nx + '" y="' + (ny + nr + 24) + '" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Nockenwelle</text>';
    const ok = Math.abs(((ak % 720) + 720) % 720) < 4 || Math.abs(((ak % 720) + 720) % 720 - 720) < 4;
    if (ok && !sl) o += '<text x="260" y="28" text-anchor="middle" font-size="15" font-weight="900" fill="' + (sm ? '#f05e4e' : '#34c778') + '">' + (sm ? 'Nockenwelle steht neben der Marke!' : 'Beide Marken stehen richtig') + '</text>';
    g('sz-g', o);
  }
  setInterval(() => { if (sl) w = (w + 3) % 720; sz(); }, 40);
  const sp = document.getElementById('sz-play');
  sp.onclick = () => { sl = !sl; if (!sl) w = 0; sp.textContent = sl ? '⏸ Pause' : '▶ Weiter'; };
  document.querySelectorAll('#s-sz [data-s]').forEach(b => b.onclick = () => { sm = +b.dataset.s; sl = false; w = 0; sp.textContent = '▶ Weiter'; document.querySelectorAll('#s-sz [data-s]').forEach(x => x.classList.toggle('on', x === b)); document.getElementById('sz-t').innerHTML = ST[sm]; });
  document.getElementById('sz-t').innerHTML = ST[0];
})();
</script>'''


# ================================================================ 3 Schmierung und Kühlung
T = 'SCHMIERUNG UND KÜHLUNG'


def oel_svg():
    return '''<svg viewBox="0 0 680 360" width="680" height="360" style="display:block;margin:0 auto;max-width:100%;height:auto" id="ol-svg">
      <rect x="0" y="0" width="680" height="360" rx="12" fill="#18283f"/>
      <path d="M180 290 H600 L585 344 H195 Z" fill="#213552" stroke="#94a4ba" stroke-width="3"/>
      <path d="M187 308 H593 L585 344 H195 Z" fill="#c9a227" opacity=".45"/>
      <text x="390" y="336" text-anchor="middle" font-size="14" font-weight="800" fill="#ecf1f8">Ölwanne</text>
      <rect x="200" y="70" width="380" height="60" rx="8" fill="#213552" stroke="#94a4ba" stroke-width="3"/>
      <rect x="190" y="130" width="400" height="160" rx="6" fill="#213552" stroke="#94a4ba" stroke-width="3"/>
      <line x1="208" y1="95" x2="572" y2="95" stroke="#94a4ba" stroke-width="6"/>
      <rect x="215" y="135" width="70" height="100" fill="#18283f" stroke="#94a4ba" stroke-width="2"/><line x1="250" y1="193" x2="250" y2="262" stroke="#94a4ba" stroke-width="7"/><rect x="220" y="175" width="60" height="30" rx="4" fill="#94a4ba"/><ellipse cx="250" cy="95" rx="16" ry="11" fill="#94a4ba"/><rect x="305" y="135" width="70" height="100" fill="#18283f" stroke="#94a4ba" stroke-width="2"/><line x1="340" y1="213" x2="340" y2="262" stroke="#94a4ba" stroke-width="7"/><rect x="310" y="195" width="60" height="30" rx="4" fill="#94a4ba"/><ellipse cx="340" cy="95" rx="16" ry="11" fill="#94a4ba"/><rect x="395" y="135" width="70" height="100" fill="#18283f" stroke="#94a4ba" stroke-width="2"/><line x1="430" y1="213" x2="430" y2="262" stroke="#94a4ba" stroke-width="7"/><rect x="400" y="195" width="60" height="30" rx="4" fill="#94a4ba"/><ellipse cx="430" cy="95" rx="16" ry="11" fill="#94a4ba"/><rect x="485" y="135" width="70" height="100" fill="#18283f" stroke="#94a4ba" stroke-width="2"/><line x1="520" y1="193" x2="520" y2="262" stroke="#94a4ba" stroke-width="7"/><rect x="490" y="175" width="60" height="30" rx="4" fill="#94a4ba"/><ellipse cx="520" cy="95" rx="16" ry="11" fill="#94a4ba"/>
      <line x1="198" y1="262" x2="582" y2="262" stroke="#94a4ba" stroke-width="9" stroke-linecap="round"/>
      <text x="390" y="60" text-anchor="middle" font-size="13" font-weight="800" fill="#ecf1f8">Zylinderkopf mit Nockenwelle</text>
      <text x="390" y="284" text-anchor="middle" font-size="12" font-weight="800" fill="#ecf1f8">Kurbelwelle</text>
      <text x="186" y="244" text-anchor="end" font-size="11" font-weight="800" fill="#ffd34d">Hauptölkanal ▸</text>
      <path id="ol-p" d="M232 322 H90 V290 M90 250 V216 M90 160 V145 H200 V240 H575 V100 H215 M575 175 H622 M300 240 V256 M390 240 V256 M480 240 V256" fill="none" stroke="#c9a227" stroke-width="6" stroke-linejoin="round"/>
      <path id="ol-bp" d="M90 228 H30 V200 M30 176 V145 H90" fill="none" stroke="#94a4ba" stroke-width="5" stroke-linejoin="round"/>
      <g><rect x="18" y="176" width="24" height="28" rx="5" fill="#213552" stroke="#ecf1f8" stroke-width="3"/><circle id="ol-vk" cx="30" cy="196" r="6" fill="#ecf1f8"/><path d="M30 189 l-6 -3 l12 -3 l-12 -3 l6 -3" fill="none" stroke="#ecf1f8" stroke-width="2"/></g>
      <text x="8" y="128" font-size="12" font-weight="800" fill="#ecf1f8">Überströmventil</text>
      <rect x="58" y="250" width="64" height="40" rx="8" fill="#213552" stroke="#ecf1f8" stroke-width="3"/><text x="90" y="275" text-anchor="middle" font-size="12" font-weight="900" fill="#ecf1f8">Ölpumpe</text>
      <rect id="ol-f" x="62" y="160" width="56" height="56" rx="12" fill="#213552" stroke="#ecf1f8" stroke-width="3"/><text x="90" y="193" text-anchor="middle" font-size="12" font-weight="900" fill="#ecf1f8">Filter</text>
      <circle cx="642" cy="175" r="20" fill="#213552" stroke="#ecf1f8" stroke-width="3"/><circle cx="642" cy="175" r="7" fill="#94a4ba"/>
      <text x="642" y="214" text-anchor="middle" font-size="12" font-weight="800" fill="#ecf1f8">Turbo</text>
      <circle id="ol-ds" cx="640" cy="60" r="15" fill="#213552" stroke="#ecf1f8" stroke-width="3"/><text x="670" y="30" text-anchor="end" font-size="11" font-weight="800" fill="#94a4ba">Öldruck-Leuchte</text>
      <path id="ol-p1" d="M232 322 H90 V292" fill="none" stroke="none"/><path id="ol-p2" d="M90 248 V229" fill="none" stroke="none"/><path id="ol-p3" d="M90 228 V217" fill="none" stroke="none"/>
      <path id="ol-pv" d="M90 228 H30 V145 H90" fill="none" stroke="none"/>
      <path id="ol-pa" d="M90 158 V145 H200 V240 H575 V100" fill="none" stroke="none"/>
      <path id="ol-pb" d="M575 100 H215" fill="none" stroke="none"/><path id="ol-pc" d="M575 175 H621" fill="none" stroke="none"/>
      <path id="ol-pd1" d="M300 241 V256" fill="none" stroke="none"/><path id="ol-pd2" d="M390 241 V256" fill="none" stroke="none"/><path id="ol-pd3" d="M480 241 V256" fill="none" stroke="none"/>
      <path id="ol-pr" d="M545 268 V308" fill="none" stroke="none"/>
    </svg>'''


def kuehl_svg():
    return '''<svg viewBox="0 0 600 320" width="600" height="320" style="display:block;margin:0 auto;max-width:100%;height:auto" id="kl-svg">
      <rect x="0" y="0" width="600" height="320" rx="12" fill="#18283f"/>
      <rect x="200" y="110" width="170" height="150" rx="14" fill="#213552" stroke="#ecf1f8" stroke-width="4"/><text x="285" y="190" text-anchor="middle" font-size="17" font-weight="900" fill="#ecf1f8">Motor</text>
      <rect x="440" y="70" width="120" height="200" rx="8" fill="#213552" stroke="#ecf1f8" stroke-width="4"/>
      <path d="M455 90 H545 M455 115 H545 M455 140 H545 M455 165 H545 M455 190 H545 M455 215 H545 M455 240 H545" stroke="#94a4ba" stroke-width="3"/>
      <text x="500" y="292" text-anchor="middle" font-size="14" font-weight="800" fill="#ecf1f8">Kühler</text>
      <g id="kl-lf"><circle cx="500" cy="170" r="34" fill="none" stroke="#ffd34d" stroke-width="3" stroke-dasharray="10 8"/></g>
      <rect x="40" y="50" width="90" height="40" rx="8" fill="#213552" stroke="#ecf1f8" stroke-width="3"/><text x="85" y="118" text-anchor="middle" font-size="13" font-weight="800" fill="#ecf1f8">Heizung (Innenraum)</text>
      <path id="kl-gr" d="M370 140 H400 V60 H500 V70 M500 270 V300 H400 V230 H370" fill="none" stroke="#28aaf5" stroke-width="7" stroke-linejoin="round"/>
      <path id="kl-kl" d="M200 140 H170 V70 H140 M30 70 H10 V230 H200" fill="none" stroke="#28aaf5" stroke-width="7" stroke-linejoin="round"/>
      <rect id="kl-th" x="384" y="120" width="32" height="32" rx="6" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/>
      <text x="400" y="112" text-anchor="middle" font-size="12" font-weight="800" fill="#94a4ba">Thermostat</text>
      <circle cx="185" cy="230" r="15" fill="#18283f" stroke="#ecf1f8" stroke-width="3"/><text x="150" y="258" text-anchor="middle" font-size="12" font-weight="800" fill="#94a4ba">Wasserpumpe</text>
      <path id="kl-fg" d="M370 140 H400 V60 H500 V270 V300 H400 V230 H370" fill="none" stroke="none"/>
      <path id="kl-fk" d="M200 140 H170 V70 H30 H10 V230 H200" fill="none" stroke="none"/>
    </svg>'''


schmierung = [
    titel_folie(K, '°C', 'Schmierung und Kühlung', 'Motoröl, Ölkreislauf, Kühlkreislauf, Thermostat, Kühlmittel', 'font-size:110px'),
    lernziele(T, ['Welche Aufgaben das Motoröl hat und wie der Ölkreislauf arbeitet', 'Was SAE-Klasse und Herstellerfreigabe bedeuten',
                  'Wie der Kühlkreislauf mit Thermostat arbeitet', 'Wie du Öl und Kühlmittel prüfst']),
    folie(T, 'Aufgaben des Motoröls', '''    <div class="values">
      <div class="val step from-left"><b>Schmieren</b><span>Ölfilm zwischen den Teilen – weniger Reibung und Verschleiß</span></div>
      <div class="val step from-left"><b>Kühlen</b><span>führt Wärme ab, z. B. vom Kolben und vom Turbolader</span></div>
      <div class="val step from-left"><b>Reinigen</b><span>nimmt Schmutz und Abrieb auf – der Filter hält ihn fest</span></div>
      <div class="val step from-left"><b>Abdichten</b><span>hilft den Kolbenringen beim Abdichten</span></div>
      <div class="val step from-left"><b>Schützen</b><span>vor Korrosion</span></div>
    </div>'''),
    folie(T, 'Der Ölkreislauf – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap">{btns('o', [('ok', 'Normal'), ('filter', 'Filter verstopft'), ('druck', 'Öldruck zu niedrig')])}</div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr">
      {oel_svg()}
      <div class="card" id="ol-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>''', sid='s-ol', body_cls='body noclick'),
    folie(T, 'Die Ölsorte – zum Antippen', '''    <div class="rb" id="rb"><span data-k="0">SAE</span><span data-k="1">5W</span><span>-</span><span data-k="2">30</span></div>
    <div class="grid2" style="align-items:start">
      <div class="card" id="rb-t" style="font-size:18px;font-weight:600;line-height:1.5;margin:0"></div>
      <div class="card" style="margin:0;font-size:16px;line-height:1.55"><b>Herstellerfreigabe ist Pflicht</b><br>Auf dem Gebinde steht z. B. eine Freigabe des Fahrzeugherstellers. Nur Öl mit der vorgeschriebenen Freigabe verwenden – sonst können Motor, Partikelfilter oder Garantie Schaden nehmen.</div>
    </div>''', sid='s-rb', body_cls='body noclick'),
    folie(T, 'Ölstand prüfen und Ölwechsel', '''    <ol class="steps-list">
      <li class="step">Fahrzeug eben abstellen<small>Motor warm, abstellen, einige Minuten warten, bis das Öl zurückgelaufen ist</small></li>
      <li class="step">Ölmessstab ziehen, abwischen, wieder einstecken<small>Ölstand zwischen Min und Max – nie über Max füllen. Manche Fahrzeuge haben nur eine elektronische Anzeige</small></li>
      <li class="step">Ölwechsel: Altöl ablassen, Ölfilter erneuern<small>Dichtring der Ablassschraube erneuern, Schraube mit Drehmoment laut Hersteller</small></li>
      <li class="step">Neues Öl mit Freigabe einfüllen<small>Menge laut Hersteller, Motor kurz laufen lassen, Dichtheit und Ölstand prüfen</small></li>
      <li class="step">Serviceanzeige zurücksetzen<small>Altöl und Filter als Sondermüll entsorgen</small></li>
    </ol>'''),
    folie(T, 'Der Kühlkreislauf – zum Ausprobieren', f'''    <div class="ctrl"><span style="width:330px;white-space:nowrap">Kühlmitteltemperatur: <span class="c" id="kl-n">40 °C</span></span><input type="range" id="kl-r" min="20" max="115" step="1" value="40"></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.3fr 1fr;margin-top:8px">
      {kuehl_svg()}
      <div class="card" id="kl-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Öffnungs- und Lüftertemperaturen sind Beispielwerte – genaue Werte laut Hersteller.</p>''', sid='s-kl', body_cls='body noclick'),
    folie(T, 'Das Kühlmittel', '''    <div class="grid2" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:22px">Was ist drin?</div>
        <ul UL><li>Wasser und Kühlerschutzmittel (Frostschutz und Korrosionsschutz)</li><li>Frostschutz mit dem Refraktometer prüfen – meist bis ca. −25 °C oder tiefer (laut Hersteller)</li><li>nur freigegebenes Kühlmittel verwenden, Sorten nicht mischen</li></ul></div>
      <div class="card step"><div class="big" style="font-size:22px">Prüfen</div>
        <ul UL><li>Stand im Ausgleichsbehälter bei kaltem Motor zwischen Min und Max</li><li>Schläuche, Kühler und Wasserpumpe auf Undichtigkeit prüfen</li><li>Dichtheit mit dem Kühlsystem-Prüfgerät (Abdrücken)</li></ul></div>
    </div>
    <div class="warn step" style="margin-top:12px"><b>Verbrühungsgefahr</b>Das Kühlsystem steht unter Druck. Den Deckel nie bei heißem Motor öffnen.</div>'''.replace('UL', UL)),
    folie(T, 'Fehler erkennen – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:12px;flex-wrap:wrap;gap:6px">{btns('f', [('0', 'Motor wird zu heiß'), ('1', 'Motor wird nicht warm'), ('2', 'Öl im Kühlmittel'), ('3', 'Kühlmittelverlust'), ('4', 'Ölverlust')])}</div>
    <div class="grid2" style="align-items:start">
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">MÖGLICHE URSACHEN</div><ul id="fe-u" style="font-size:16px;line-height:1.55;padding-left:20px;margin:8px 0 0"></ul></div>
      <div class="card" style="margin:0"><div class="muted" style="font-size:14px;font-weight:800">SO PRÜFST DU</div><ul id="fe-p" style="font-size:16px;line-height:1.55;padding-left:20px;margin:8px 0 0"></ul></div>
    </div>''', sid='s-fe', body_cls='body noclick'),
    video(T, 'mw-schmierung'),
    kurztest(T, [
        ('Was bedeutet „5W“ bei einem Motoröl 5W-30?', ['5 Liter Füllmenge', 'Kältewert: je kleiner, desto besser fließt das Öl bei Kälte', '5 Jahre haltbar'], 1, 'W steht für Winter.'),
        ('Wann öffnet das Thermostat den großen Kühlkreislauf?', ['Sofort beim Start', 'Wenn der Motor warm ist', 'Nur bei Frost'], 1, 'Vorher läuft der kleine Kreislauf – der Motor wird schneller warm.'),
        ('Was ist eine mögliche Ursache für Öl im Kühlmittel?', ['Zylinderkopfdichtung oder Ölkühler defekt', 'Zu viel Frostschutz', 'Luftfilter verstopft'], 0, 'Kühlsystem abdrücken und Zylinderkopfdichtung prüfen.'),
        ('Warum öffnest du den Kühlmitteldeckel nicht bei heißem Motor?', ['Das Kühlmittel wird sonst schlecht', 'Der Motor geht aus', 'Das System steht unter Druck – Verbrühungsgefahr'], 2, 'Erst abkühlen lassen.'),
    ]),
    merke(T, ['Öl: schmieren, kühlen, reinigen, abdichten, schützen', 'SAE 5W-30 – aber immer Herstellerfreigabe beachten',
              'Thermostat: kalt kleiner, warm großer Kreislauf', 'Kühlsystem nie heiß öffnen']),
]
schmierung_js = '''<script src="assets/schaltung.js"></script>
<script>
(function () {
  const sv = document.getElementById('ol-svg');
  const F = ['p1', 'p2', 'pa', 'pb', 'pc', 'pd1', 'pd2', 'pd3', 'pr'].map(n => Flow(sv, document.getElementById('ol-' + n), { spacing: 24, speed: 60, r: 5, color: '#ffd34d' }));
  const FF = Flow(sv, document.getElementById('ol-p3'), { spacing: 24, speed: 60, r: 5, color: '#ffd34d' });
  const FV = Flow(sv, document.getElementById('ol-pv'), { spacing: 24, speed: 60, r: 5, color: '#ffd34d' });
  const OT = {
    ok: '<b class="grn">Normal:</b> Die Ölpumpe saugt Öl aus der Ölwanne, drückt es durch den <span class="c">Filter</span> in den Hauptölkanal. Von dort geht es zu Kurbelwelle, Nockenwelle, Turbolader und Kettenspanner – und tropft zurück in die Wanne. Das <span class="c">Überströmventil</span> neben dem Filter bleibt zu.',
    filter: '<b class="ora">Filter verstopft:</b> Damit der Motor trotzdem Öl bekommt, öffnet das <span class="ora">Überströmventil</span> (Bypassventil) neben dem Filter. Das Öl fließt dann <b>ungefiltert</b> am Filter vorbei – Schmutz gelangt an die Lager. Darum Filter bei jedem Ölwechsel erneuern.',
    druck: '<b class="red">Öldruck zu niedrig:</b> Die <span class="red">Öldruck-Leuchte</span> geht an. Sofort anhalten und Motor abstellen! Ursachen: zu wenig Öl, falsche Ölsorte, Pumpe oder Lager verschlissen. Ölstand prüfen, Öldruck mit Manometer messen (Wert laut Hersteller).'
  };
  const ob = document.querySelectorAll('#s-ol [data-o]');
  function ol(m) {
    const v = m === 'filter';
    F.forEach(f => { f.on(true); f.speed = m === 'druck' ? 20 : 60; });
    FF.on(!v); FF.speed = m === 'druck' ? 20 : 60; FV.on(v);
    document.getElementById('ol-bp').setAttribute('stroke', v ? '#c9a227' : '#94a4ba');
    document.getElementById('ol-vk').setAttribute('cy', v ? 184 : 196);
    document.getElementById('ol-f').setAttribute('stroke', v ? '#ff8f3f' : '#ecf1f8');
    document.getElementById('ol-f').setAttribute('stroke-dasharray', v ? '5 4' : '');
    document.getElementById('ol-ds').setAttribute('fill', m === 'druck' ? '#f05e4e' : '#213552');
    document.getElementById('ol-t').innerHTML = OT[m];
    ob.forEach(b => b.classList.toggle('on', b.dataset.o === m));
  }
  ob.forEach(b => b.onclick = () => ol(b.dataset.o)); ol('ok');

  const RB = ['<b>SAE</b> = Viskositätsklasse – sagt, wie dick- oder dünnflüssig das Öl ist.', '<b>5W</b> = Kältewert (W = Winter). Je kleiner die Zahl, desto besser fließt das Öl bei Kälte – wichtig beim Kaltstart.', '<b>30</b> = Viskosität bei Betriebstemperatur (100 °C). Je größer, desto dickflüssiger bleibt das Öl, wenn es heiß ist.'];
  const rs = document.querySelectorAll('#rb [data-k]');
  function rb(i) { rs.forEach(s => s.classList.toggle('on', +s.dataset.k === i)); document.getElementById('rb-t').innerHTML = RB[i]; }
  rs.forEach(s => s.onclick = () => rb(+s.dataset.k)); rb(1);

  const ks = document.getElementById('kl-svg');
  const fg = Flow(ks, document.getElementById('kl-fg'), { spacing: 26, speed: 60, r: 6, color: '#ffd34d' });
  const fk = Flow(ks, document.getElementById('kl-fk'), { spacing: 26, speed: 60, r: 6, color: '#ffd34d' });
  const kr = document.getElementById('kl-r');
  let lfw = 0, lfan = false;
  function kl() {
    const t = +kr.value, auf = t >= 87, lf = t >= 100;
    fk.on(true); fg.on(auf);
    document.getElementById('kl-gr').style.opacity = auf ? 1 : 0.25;
    document.getElementById('kl-th').setAttribute('fill', auf ? '#34c778' : '#18283f');
    lfan = lf;
    document.getElementById('kl-n').textContent = t + ' °C';
    const farbe = t < 70 ? '#28aaf5' : t < 105 ? '#34c778' : '#f05e4e';
    document.getElementById('kl-n').style.color = farbe;
    document.getElementById('kl-t').innerHTML = !auf ? '<b>Kalter Motor:</b> Das Thermostat ist <span class="c">zu</span>. Das Kühlmittel läuft nur im <b>kleinen Kreislauf</b> (Motor und Heizung) – der Motor wird schnell warm.'
      : !lf ? '<b>Warmer Motor:</b> Das Thermostat <span class="grn">öffnet</span> (hier ab ca. 87 °C). Jetzt fließt Kühlmittel auch durch den <b>Kühler</b> – großer Kreislauf. Der Fahrtwind kühlt.'
      : t < 110 ? '<b>Sehr warm:</b> Zusätzlich springt der <span class="c">Lüfter</span> an (hier ab ca. 100 °C) – z. B. im Stau, wenn der Fahrtwind fehlt.'
      : '<b class="red">Zu heiß!</b> Anhalten, Motor abstellen, abkühlen lassen. Ursachen: zu wenig Kühlmittel, Lüfter oder Thermostat defekt, Kühler verstopft, Wasserpumpe defekt.';
  }
  setInterval(() => { if (lfan) { lfw = (lfw + 12) % 360; document.getElementById('kl-lf').setAttribute('transform', 'rotate(' + lfw + ' 500 170)'); document.getElementById('kl-lf').style.opacity = 1; } else document.getElementById('kl-lf').style.opacity = 0.25; }, 40);
  kr.addEventListener('input', kl); kl();

  const FE = [
    [['zu wenig Kühlmittel (Undichtigkeit)', 'Thermostat öffnet nicht', 'Lüfter läuft nicht an', 'Kühler außen oder innen zugesetzt', 'Wasserpumpe defekt'], ['Kühlmittelstand (kalt!)', 'Temperatur im Messwertblock', 'Lüfter mit Stellglieddiagnose', 'Kühlsystem abdrücken']],
    [['Thermostat hängt offen', 'Temperatursensor liefert falschen Wert'], ['Kühlerschlauch nach dem Thermostat fühlen: wird er sofort warm?', 'Temperatur im Messwertblock mit Messgerät vergleichen']],
    [['Zylinderkopfdichtung defekt', 'Ölkühler (Öl-Wasser-Wärmetauscher) undicht'], ['Kühlmittel ansehen: brauner Schaum?', 'Kühlsystem abdrücken', 'CO-Test am Ausgleichsbehälter (Abgas im Kühlmittel)']],
    [['undichter Schlauch, Kühler oder Wasserpumpe', 'Zylinderkopfdichtung (weißer Rauch aus dem Auspuff)'], ['Sichtprüfung auf Spuren (weiße oder farbige Kristalle)', 'Kühlsystem abdrücken', 'Druckverlusttest der Zylinder']],
    [['undichte Dichtungen (Ventildeckel, Ölwanne, Wellendichtringe)', 'Ölverbrauch über Kolbenringe oder Ventilschaftdichtungen (blauer Rauch)', 'Turbolader'], ['Motor reinigen, Kontrastmittel nutzen, Spur nach oben verfolgen', 'Ölverbrauch messen', 'Kompressions- oder Druckverlusttest']]
  ];
  const fb = document.querySelectorAll('#s-fe [data-f]');
  function fe(i) {
    document.getElementById('fe-u').innerHTML = FE[i][0].map(x => '<li>' + x + '</li>').join('');
    document.getElementById('fe-p').innerHTML = FE[i][1].map(x => '<li>' + x + '</li>').join('');
    fb.forEach(x => x.classList.toggle('on', +x.dataset.f === i));
  }
  fb.forEach(x => x.onclick = () => fe(+x.dataset.f)); fe(0);
})();
</script>'''


# ================================================================ 4 Wartung
T = 'WARTUNG'


def heben_svg():
    pts = [('a', 292, 268), ('b', 84, 222), ('c', 485, 268), ('d', 678, 268), ('e', 822, 266)]
    mp = ''.join(f'<g class="mp" data-p="{k}" style="cursor:pointer"><circle cx="{x}" cy="{y}" r="16" fill="#213552" stroke="#ffd34d" stroke-width="4"/><text x="{x}" y="{y + 6}" text-anchor="middle" font-size="16" font-weight="900" fill="#ffd34d">{k.upper()}</text></g>'
                 for k, x, y in pts)
    return f'''<svg viewBox="0 0 960 330" width="960" height="330" style="display:block;margin:0 auto;max-width:100%;height:auto" id="hb-svg">
      <rect x="0" y="0" width="960" height="330" rx="12" fill="#18283f"/>
      <path d="M60 236 Q66 130 220 112 L340 42 H640 L780 112 Q900 124 910 236 H818 A58 58 0 0 0 702 236 H268 A58 58 0 0 0 152 236 Z" fill="#213552" stroke="#94a4ba" stroke-width="4"/>
      <path d="M380 112 V236 M560 112 V236" stroke="#94a4ba" stroke-width="2" opacity=".6"/>
      <rect x="268" y="230" width="434" height="16" rx="4" fill="#94a4ba"/>
      <text x="485" y="222" text-anchor="middle" font-size="13" font-weight="800" fill="#94a4ba">Schweller</text>
      <path d="M284 246 l8 -12 l8 12 Z M670 246 l8 -12 l8 12 Z" fill="#ecf1f8"/>
      <line x1="760" y1="250" x2="866" y2="272" stroke="#94a4ba" stroke-width="9" stroke-linecap="round"/>
      <circle cx="210" cy="250" r="46" fill="#18283f" stroke="#94a4ba" stroke-width="8"/><circle cx="760" cy="250" r="46" fill="#18283f" stroke="#94a4ba" stroke-width="8"/>
      <circle cx="210" cy="250" r="9" fill="#94a4ba"/><circle cx="760" cy="250" r="9" fill="#94a4ba"/>
      {mp}
      <text x="20" y="28" font-size="13" font-weight="800" fill="#94a4ba">▲ = Markierung am Schweller</text>
      <text x="480" y="315" text-anchor="middle" font-size="15" font-weight="800" fill="#94a4ba">Wo setzt du die Tragarme der Hebebühne an? Wähle A bis E.</text>
    </svg>'''


wartung = [
    titel_folie(K, 'km', 'Wartung und Inspektion', 'Anheben und Sichern, Betriebsstoffe, Checkliste, Kompression, Druckverlust', 'font-size:110px'),
    lernziele(T, ['Was Wartung, Inspektion und Instandsetzung unterscheidet', 'Wie du ein Fahrzeug sicher anhebst',
                  'Welche Betriebsstoffe du prüfst', 'Wie Kompressions- und Druckverlusttest Motorschäden zeigen']),
    folie(T, 'Wartung, Inspektion, Instandsetzung', '''    <div class="grid3" style="align-items:start">
      <div class="card step"><div class="big" style="font-size:21px">Wartung</div><p style="margin:6px 0 0">Zustand erhalten: Ölwechsel, Filter, Flüssigkeiten, Zahnriemen nach Intervall.</p></div>
      <div class="card step"><div class="big" style="font-size:21px">Inspektion</div><p style="margin:6px 0 0">Prüfen und beurteilen nach Plan oder Checkliste – Mängel erkennen und dem Kunden mitteilen.</p></div>
      <div class="card step"><div class="big" style="font-size:21px">Instandsetzung</div><p style="margin:6px 0 0">Reparieren oder tauschen, was defekt ist – nach Freigabe durch den Kunden.</p></div>
    </div>
    <div class="note step" style="margin-top:12px">Serviceintervall: fest (z. B. jährlich) oder flexibel nach Fahrweise – laut Hersteller. Nach dem Service die Serviceanzeige zurücksetzen und die Arbeiten dokumentieren.</div>'''),
    folie(T, 'Fahrzeug sicher anheben – zum Ausprobieren', f'''    {heben_svg()}
    <div class="choice" style="margin-top:8px;flex-wrap:wrap;gap:6px">{btns('hp', [('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D'), ('e', 'E')], first=-1)}</div>
    <div class="card" id="hb-t" style="font-size:16px;font-weight:600;line-height:1.5;margin-top:10px"><b>Tippe auf einen Punkt.</b></div>''', sid='s-hb', body_cls='body noclick'),
    folie(T, 'Sicher arbeiten an der Hebebühne', '''    <ol class="steps-list">
      <li class="step">Nur nach Unterweisung bedienen<small>Tragfähigkeit der Bühne und Gewicht des Fahrzeugs beachten</small></li>
      <li class="step">Aufnahmepunkte laut Hersteller<small>Gummiauflagen verwenden, Tragarme arretieren</small></li>
      <li class="step">Kurz anheben und prüfen<small>Räder knapp über dem Boden: Fahrzeug steht sicher? Leicht rütteln</small></li>
      <li class="step">Ganz anheben und Sicherung einrasten lassen<small>nie unter ein Fahrzeug, das nur auf dem Wagenheber steht – immer Unterstellböcke</small></li>
      <li class="step">Beim Ablassen<small>Werkzeug und Personen weg, Füße frei, Tragarme ganz ausschwenken</small></li>
    </ol>'''),
    folie(T, 'Betriebsstoffe prüfen', '''    <div class="values">
      <div class="val step from-left"><b>Motoröl</b><span>Stand, Zustand, Ölwechsel nach Intervall – mit Herstellerfreigabe</span></div>
      <div class="val step from-left"><b>Kühlmittel</b><span>Stand bei kaltem Motor, Frostschutz mit dem Refraktometer</span></div>
      <div class="val step from-left"><b>Bremsflüssigkeit</b><span>Stand und Siedepunkt, Wechsel nach Intervall</span></div>
      <div class="val step from-left"><b>Scheibenwaschwasser</b><span>Stand und Frostschutz im Winter</span></div>
      <div class="val step from-left"><b>weitere</b><span>Getriebeöl, Servoöl, AdBlue, Kältemittel – laut Wartungsplan</span></div>
    </div>'''),
    folie(T, 'Inspektion nach Checkliste', '''    <ol class="steps-list">
      <li class="step">Fahrzeug annehmen<small>Kundenwünsche aufnehmen, Fehlerspeicher lesen, Schutzbezüge anbringen</small></li>
      <li class="step">Rundgang<small>Beleuchtung, Hupe, Scheibenwischer, Scheiben, Gurte</small></li>
      <li class="step">Motorraum<small>Flüssigkeiten, Riemen, Schläuche, Batterie</small></li>
      <li class="step">Unterboden<small>Undichtigkeiten, Leitungen, Abgasanlage, Manschetten, Spiel an Gelenken</small></li>
      <li class="step">Räder und Bremse<small>Profil, Reifendruck, Beläge, Scheiben</small></li>
      <li class="step">Probefahrt und Dokumentation<small>Mängel aufschreiben und mit dem Kunden besprechen</small></li>
    </ol>'''),
    folie(T, 'Kompressionstest – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:8px;flex-wrap:wrap;gap:6px">{btns('k', [('ok', 'In Ordnung'), ('ring', 'Zyl. 3 niedrig (A)'), ('vent', 'Zyl. 3 niedrig (B)'), ('zkd', 'Zyl. 2 und 3 niedrig')])}<button class="btn" id="km-oel" style="--c:var(--grn)">+ Ölprobe in Zylinder 3</button></div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {svgbox('km', 560, 280)}
      <div class="card" id="km-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Beispielwerte (Otto). Vorher: Motor warm, Batterie voll, Zünd-/Glühkerzen raus, Zündung und Einspritzung laut Hersteller deaktivieren, Drosselklappe offen. Wichtig ist der Unterschied zwischen den Zylindern – Grenzwerte laut Hersteller.</p>''', sid='s-km', body_cls='body noclick'),
    folie(T, 'Druckverlusttest – zum Ausprobieren', f'''    <div class="choice" style="margin-bottom:10px;flex-wrap:wrap;gap:6px">{btns('d', [('ein', 'Zischt im Ansaugtrakt'), ('aus', 'Zischt im Auspuff'), ('ring', 'Zischt am Öleinfüllstutzen'), ('zkd', 'Blasen im Kühlmittel'), ('nach', 'Zischt am Nachbarzylinder')])}</div>
    <div class="grid2" style="align-items:center;grid-template-columns:1.2fr 1fr">
      {svgbox('dv', 560, 320)}
      <div class="card" id="dv-t" style="font-size:16px;font-weight:600;line-height:1.55"></div>
    </div>
    <p class="muted" style="font-size:14px;margin:6px 0 0">Zylinder auf OT im Arbeitstakt stellen (beide Ventile zu), Druckluft über das Zündkerzenloch einleiten, Druckverlust in % ablesen. Grenzwerte laut Gerät oder Hersteller.</p>''', sid='s-dv', body_cls='body noclick'),
    folie(T, 'Aus der Praxis', '''    <div class="grid2" style="align-content:start">
      <div class="tip step"><b>Vorher und nachher</b>Fehlerspeicher vor der Arbeit lesen und am Ende noch einmal – so siehst du, ob alles in Ordnung ist.</div>
      <div class="tip step"><b>Entsorgen</b>Altöl, Filter, Kühlmittel, Bremsflüssigkeit und ölige Lappen getrennt als Sondermüll sammeln.</div>
      <div class="warn step"><b>Hautschutz</b>Bei Arbeiten mit Öl und Kraftstoff Handschuhe tragen, Hautschutzplan beachten.</div>
      <div class="tip step"><b>Dokumentieren</b>Durchgeführte Arbeiten, verwendete Teile und Betriebsstoffe im Auftrag und im (digitalen) Serviceheft eintragen.</div>
    </div>'''),
    video(T, 'mw-wartung'),
    kurztest(T, [
        ('Wo setzt du die Tragarme der Hebebühne an?', ['An der Ölwanne', 'An den Aufnahmepunkten laut Hersteller', 'Irgendwo am Schweller'], 1, 'Sonst kann das Fahrzeug beschädigt werden oder herunterfallen.'),
        ('Was gilt, wenn das Fahrzeug nur auf dem Wagenheber steht?', ['Nie darunter arbeiten – Unterstellböcke verwenden', 'Kurz darunter ist erlaubt', 'Egal'], 0, 'Ein Wagenheber kann absacken oder umkippen.'),
        ('Kompression Zylinder 3 zu niedrig. Nach einer Ölprobe steigt der Wert deutlich. Was ist die Ursache?', ['Ventil undicht', 'Zündkerze defekt', 'Kolbenringe oder Zylinderwand verschlissen'], 2, 'Das Öl dichtet die Ringe kurz ab – bei undichten Ventilen hilft es nicht.'),
        ('Beim Druckverlusttest blubbert es im Kühlmittel-Ausgleichsbehälter. Was ist defekt?', ['Zylinderkopfdichtung', 'Auslassventil', 'Kolbenringe'], 0, 'Die Druckluft gelangt aus dem Brennraum in den Kühlkreislauf.'),
    ]),
    merke(T, ['Wartung erhält – Inspektion prüft – Instandsetzung repariert', 'Nur an Aufnahmepunkten anheben, nie unter ungesicherte Last',
              'Kompression: Unterschied zwischen den Zylindern zählt', 'Druckverlust: wo es zischt, sitzt der Fehler']),
]
wartung_js = '''<script>
(function () {
  const g = (id, s) => document.getElementById(id).innerHTML = s;
  const HB = {
    a: '<b class="grn">A – richtig:</b> Aufnahmepunkt vorn am Schweller, kurz hinter dem Vorderrad. Er ist verstärkt und markiert (Dreieck, Kerbe oder Pfeil). Genaue Lage laut Hersteller.',
    d: '<b class="grn">D – richtig:</b> Aufnahmepunkt hinten am Schweller, kurz vor dem Hinterrad. Gummiauflage verwenden, damit nichts verrutscht oder verkratzt. Alle vier Tragarme an den Aufnahmepunkten ansetzen.',
    b: '<b class="red">B – falsch:</b> Der Stoßfänger ist aus Kunststoff und trägt kein Gewicht. Er bricht, das Fahrzeug kann abrutschen.',
    c: '<b class="red">C – falsch:</b> In der Mitte ist der Schweller nicht verstärkt. Das Blech knickt ein, und der Schwerpunkt passt nicht – das Fahrzeug kann kippen.',
    e: '<b class="red">E – falsch:</b> Achsteile, Lenker und Leitungen sind keine Aufnahmepunkte (außer der Hersteller erlaubt es). Gefahr von Schäden und Abrutschen.'
  };
  function hb(k) {
    document.querySelectorAll('#hb-svg .mp').forEach(m => { const sel = m.dataset.p === k; m.querySelector('circle').setAttribute('fill', sel ? ('ad'.includes(k) ? '#2f8a55' : '#a8352b') : '#213552'); m.querySelector('text').setAttribute('fill', sel ? '#ffffff' : '#ffd34d'); });
    document.querySelectorAll('#s-hb [data-hp]').forEach(b => b.classList.toggle('on', b.dataset.hp === k));
    document.getElementById('hb-t').innerHTML = HB[k];
  }
  document.querySelectorAll('#hb-svg .mp').forEach(m => m.onclick = () => hb(m.dataset.p));
  document.querySelectorAll('#s-hb [data-hp]').forEach(b => b.onclick = () => hb(b.dataset.hp));

  // Kompression
  const KM = {
    ok: [[12.4, 12.6, 12.3, 12.5], null, '<b class="grn">In Ordnung:</b> Alle Zylinder liegen nah beieinander.'],
    ring: [[12.4, 12.6, 8.1, 12.5], 11.6, '<b class="red">Zylinder 3 ist deutlich niedriger.</b> Mach die Ölprobe: etwas Motoröl ins Zündkerzenloch, dann noch einmal messen.'],
    vent: [[12.4, 12.6, 7.9, 12.5], 8.1, '<b class="red">Zylinder 3 ist deutlich niedriger.</b> Mach die Ölprobe: etwas Motoröl ins Zündkerzenloch, dann noch einmal messen.'],
    zkd: [[12.4, 8.3, 8.0, 12.5], null, '<b class="red">Zwei benachbarte Zylinder niedrig:</b> Typisch für eine durchgebrannte <span class="red">Zylinderkopfdichtung zwischen den Zylindern</span>. Mit dem Druckverlusttest bestätigen.']
  };
  let km = 'ok', oel = false;
  function kz() {
    const k = KM[km], v = k[0].slice(); if (oel && k[1]) v[2] = k[1];
    let o = '<line x1="40" y1="240" x2="540" y2="240" stroke="#94a4ba" stroke-width="2"/>';
    for (let b = 0; b <= 14; b += 2) o += '<line x1="40" y1="' + (240 - b * 14) + '" x2="540" y2="' + (240 - b * 14) + '" stroke="#94a4ba" stroke-width="1" opacity=".15"/><text x="34" y="' + (245 - b * 14) + '" text-anchor="end" font-size="11" font-weight="800" fill="#94a4ba">' + b + '</text>';
    v.forEach((x, i) => {
      const xx = 80 + i * 115, h = x * 14, low = x < 10.5;
      o += '<rect x="' + xx + '" y="' + (240 - h) + '" width="70" height="' + h + '" rx="6" fill="' + (low ? '#f05e4e' : '#34c778') + '"/>';
      o += '<text x="' + (xx + 35) + '" y="' + (232 - h) + '" text-anchor="middle" font-size="16" font-weight="900" fill="#ecf1f8">' + x.toFixed(1).replace('.', ',') + '</text>';
      o += '<text x="' + (xx + 35) + '" y="262" text-anchor="middle" font-size="14" font-weight="800" fill="#94a4ba">Zyl. ' + (i + 1) + '</text>';
    });
    o += '<text x="40" y="22" font-size="13" font-weight="800" fill="#94a4ba">bar</text>';
    g('km-g', o);
    let t = k[2];
    if (oel && km === 'ring') t = '<b class="ora">Nach der Ölprobe steigt der Wert deutlich</b> (8,1 → 11,6 bar). Das Öl dichtet kurz zwischen Kolben und Zylinderwand ab: <span class="ora">Kolbenringe oder Zylinderwand verschlissen</span>.';
    if (oel && km === 'vent') t = '<b class="ora">Nach der Ölprobe bleibt der Wert niedrig</b> (7,9 → 8,1 bar). Das Öl hilft nicht – die Undichtigkeit sitzt oben: <span class="ora">Ventil undicht</span> (oder Zylinderkopfdichtung). Druckverlusttest machen.';
    if (oel && !k[1]) t += '<br><span class="muted">Die Ölprobe ist nur sinnvoll, wenn ein einzelner Zylinder zu niedrig ist.</span>';
    document.getElementById('km-t').innerHTML = t;
    document.querySelectorAll('#s-km [data-k]').forEach(b => b.classList.toggle('on', b.dataset.k === km));
    document.getElementById('km-oel').classList.toggle('on', oel);
  }
  document.querySelectorAll('#s-km [data-k]').forEach(b => b.onclick = () => { km = b.dataset.k; oel = false; kz(); });
  document.getElementById('km-oel').onclick = () => { oel = !oel; kz(); };
  kz();

  // Druckverlust
  const DV = {
    ein: [[200, 70], '<b>Zischt im Ansaugtrakt</b> (Luftfilter, Drosselklappe): Das <span class="c">Einlassventil</span> ist undicht.'],
    aus: [[360, 70], '<b>Zischt im Auspuff:</b> Das <span class="c">Auslassventil</span> ist undicht.'],
    ring: [[280, 300], '<b>Zischt am Öleinfüllstutzen oder Ölmessstab:</b> Luft strömt am Kolben vorbei ins Kurbelgehäuse – <span class="c">Kolbenringe oder Zylinderwand</span> verschlissen.'],
    zkd: [[480, 110], '<b>Blasen im Kühlmittel-Ausgleichsbehälter:</b> Die <span class="c">Zylinderkopfdichtung</span> (oder der Zylinderkopf) ist zum Kühlkanal hin undicht.'],
    nach: [[80, 150], '<b>Zischt am Zündkerzenloch des Nachbarzylinders:</b> Die <span class="c">Zylinderkopfdichtung zwischen den Zylindern</span> ist durchgebrannt.']
  };
  let dk = 'ein', dt = 0;
  function dv() {
    const z = DV[dk][0];
    let o = '<rect x="200" y="110" width="160" height="150" fill="#213552" stroke="#ecf1f8" stroke-width="4"/><rect x="40" y="110" width="80" height="150" fill="#213552" stroke="#94a4ba" stroke-width="3" opacity=".6"/>';
    o += '<text x="80" y="200" text-anchor="middle" font-size="12" font-weight="800" fill="#94a4ba">Nachbar-</text><text x="80" y="215" text-anchor="middle" font-size="12" font-weight="800" fill="#94a4ba">zylinder</text>';
    o += '<rect x="206" y="200" width="148" height="50" rx="4" fill="#94a4ba"/><text x="280" y="232" text-anchor="middle" font-size="14" font-weight="900" fill="#18283f">Kolben (OT)</text>';
    o += '<path d="M200 110 V70 H160 M360 110 V70 H400" fill="none" stroke="#94a4ba" stroke-width="4"/><text x="150" y="60" font-size="12" font-weight="800" fill="#94a4ba">Ansaugtrakt</text><text x="410" y="60" text-anchor="end" font-size="12" font-weight="800" fill="#94a4ba">Auspuff</text>';
    o += '<rect x="440" y="80" width="90" height="60" rx="8" fill="#213552" stroke="#28aaf5" stroke-width="3"/><text x="485" y="160" text-anchor="middle" font-size="12" font-weight="800" fill="#94a4ba">Kühlmittel</text>';
    o += '<path d="M200 270 H360 V300 H200 Z" fill="#c9a227" opacity=".3"/><text x="380" y="295" font-size="12" font-weight="800" fill="#94a4ba">Kurbelgehäuse / Öl</text>';
    o += '<line x1="280" y1="40" x2="280" y2="110" stroke="#ffd34d" stroke-width="6"/><text x="292" y="36" font-size="12" font-weight="800" fill="#ffd34d">Druckluft</text>';
    const p = (Math.sin(dt) + 1) / 2;
    o += '<circle cx="' + z[0] + '" cy="' + z[1] + '" r="' + (14 + 10 * p) + '" fill="none" stroke="#ffd34d" stroke-width="4" opacity="' + (1 - p * 0.6) + '"/><circle cx="' + z[0] + '" cy="' + z[1] + '" r="6" fill="#ffd34d"/>';
    o += '<line x1="280" y1="150" x2="' + z[0] + '" y2="' + z[1] + '" stroke="#ffd34d" stroke-width="3" stroke-dasharray="6 6"/>';
    g('dv-g', o);
  }
  setInterval(() => { dt += 0.2; dv(); }, 50);
  document.querySelectorAll('#s-dv [data-d]').forEach(b => b.onclick = () => { dk = b.dataset.d; document.querySelectorAll('#s-dv [data-d]').forEach(x => x.classList.toggle('on', x === b)); document.getElementById('dv-t').innerHTML = DV[dk][1]; });
  document.getElementById('dv-t').innerHTML = DV.ein[1];
})();
</script>'''


if __name__ == '__main__':
    seite('mw-viertakt.html', 'Der Viertaktmotor – Motor und Wartung', 't-mw1', 'Der Viertaktmotor', viertakt, STYLE, viertakt_js)
    seite('mw-triebwerk.html', 'Kurbel- und Ventiltrieb – Motor und Wartung', 't-mw2', 'Kurbel- und Ventiltrieb', triebwerk, STYLE, triebwerk_js)
    seite('mw-schmierung.html', 'Schmierung und Kühlung – Motor und Wartung', 't-mw3', 'Schmierung und Kühlung', schmierung, STYLE, schmierung_js)
    seite('mw-wartung.html', 'Wartung und Inspektion – Motor und Wartung', 't-mw4', 'Wartung und Inspektion', wartung, STYLE, wartung_js)
    print('ok')
