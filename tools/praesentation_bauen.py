"""Hilfsfunktion: baut eine Präsentationsseite im Portal-Design (Kopf, Folien, Leiste).
Wird von den Themen-Skripten (z. B. tools/mm_gemisch.py) benutzt."""
import pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent

KOPF = '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0e192b">
<meta name="robots" content="noindex, nofollow">
<title>{titel}</title>
<script>try{{var t=localStorage.getItem("lp-theme");if(t==="light"||(!t&&matchMedia("(prefers-color-scheme: light)").matches))document.documentElement.classList.add("light")}}catch(e){{}}</script>
<link rel="stylesheet" href="assets/praesentation.css">
<style>
{style}
</style>
</head>
<body class="{klasse}">
<div id="stage-wrap"><div id="stage">
'''

FUSS = '''
</div></div>

<nav id="nav">
  <a href="../index.html#/thema/{thema}" title="Zurück zum Lernportal">✕<span class="lbl">&nbsp;Zum Lernportal</span></a>
  <button id="btn-prev" title="Zurück (←)">←</button>
  <button id="btn-next" title="Weiter (→)">→</button>
  <div id="bar"><i></i></div>
  <span id="count"></span>
  <button id="btn-theme" title="Heller Modus">☀</button>
  <button id="btn-fs" title="Vollbild (F)">⛶</button>
</nav>
{skripte}
<script src="assets/praesentation.js"></script>
</body>
</html>
'''


def titel_folie(kicker, symbol, h1, sub, sym_style=''):
    return f'''<section class="slide title-slide">
  <div class="kicker">{kicker}</div>
  <div class="symbol"{(' style="' + sym_style + '"') if sym_style else ''}>{symbol}</div>
  <h1>{h1}</h1>
  <p>{sub}</p>
  <div class="hint"><span class="desk">Weiter mit → , Leertaste oder Klick</span><span class="mob">Zum Weiterblättern tippen oder wischen</span></div>
</section>'''


def folie(tag, h2, body, sid='', body_cls='body', body_style=''):
    i = f' id="{sid}"' if sid else ''
    st = f' style="{body_style}"' if body_style else ''
    return f'''<section class="slide"{i}>
  <span class="tag">{tag}</span><h2>{h2}</h2>
  <div class="{body_cls}"{st}>
{body}
  </div>
</section>'''


def lernziele(tag, ziele):
    li = '\n'.join(f'      <li class="step from-left"><span class="num">{i + 1}</span>{z}</li>' for i, z in enumerate(ziele))
    return folie(tag, 'Das lernst du hier', f'    <ul class="goals">\n{li}\n    </ul>')


def video(tag, name):
    return folie(tag, 'Lernvideo', f'    <video src="videos/{name}.mp4" poster="videos/{name}.jpg" controls preload="metadata" playsinline></video>',
                 body_cls='body video-box')


def kurztest(tag, fragen):
    """fragen: Liste (frage, [antworten], index_richtig, erklaerung)"""
    qs = []
    for n, (f, opts, ok, fb) in enumerate(fragen, 1):
        o = ''.join(f'<button class="opt">{x}</button>' for x in opts)
        qs.append(f'    <div class="q" data-correct="{ok}"><p>{n}. {f}</p>\n      <div class="opts">{o}</div>\n      <div class="fb">{fb}</div></div>')
    gap = 8 if len(fragen) > 4 else 12
    return folie(tag, 'Kurztest', '\n'.join(qs) + '\n    <div class="score">Klicke auf eine Antwort.</div>', body_cls='body quiz', body_style=f'gap:{gap}px')


def merke(tag, punkte):
    li = []
    for p in punkte:
        if '|' in p:
            a, b = p.split('|', 1)
            li.append(f'        <li class="step"><span>{a}<small>{b}</small></span></li>')
        else:
            li.append(f'        <li class="step"><span>{p}</span></li>')
    return folie(tag, 'Zusammenfassung', '    <div class="merke">\n      <h3>Merke!</h3>\n      <ul>\n' + '\n'.join(li) + '\n      </ul>\n    </div>')


def seite(datei, titel, klasse, thema, folien, style='', skripte=''):
    html = KOPF.format(titel=titel, style=style, klasse=klasse) + '\n\n'.join(folien) + \
        FUSS.format(thema=urllib.parse.quote(thema), skripte=skripte)
    (ROOT / 'praesentationen' / datei).write_text(html, encoding='utf-8')
    return datei
