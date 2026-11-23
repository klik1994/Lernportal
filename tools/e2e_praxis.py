"""Klickt Ruhestrom, Hochvolt und Bremsenprüfstand durch. Aufruf: python3 tools/e2e_praxis.py <basis-url> <screenshot-ordner>"""
import sys, pathlib
from playwright.sync_api import sync_playwright
base = sys.argv[1].rstrip('/'); shots = pathlib.Path(sys.argv[2]); shots.mkdir(exist_ok=True)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 375, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    t = lambda sel: pg.inner_text(sel)

    # Ruhestrom: Fehler "handschuh" erzwingen (Index 1)
    pg.add_init_script("Math.random = () => 0.2")
    pg.goto(base + '/ruhestrom.html'); pg.wait_for_selector('.sk')
    assert 'zwei Tagen' in t('#ruhestrom'), t('#ruhestrom')[:200]
    pg.click('[data-anschluss="parallel"]'); assert 'Kurzschluss' in t('#ruhestrom')
    pg.click('[data-reparieren]'); pg.click('[data-anschluss="reihe"]'); pg.click('[data-buchse="mA"]')
    assert 'mA-Sicherung' in t('#ruhestrom')
    pg.click('[data-reparieren]'); pg.click('[data-anschluss="reihe"]')
    assert t('.display').startswith('2,'), t('.display')
    pg.click('[data-haube]'); pg.click('[data-warte="15"]'); pg.click('[data-warte="15"]')
    assert '0,33 A' in t('.display'), t('.display')
    pg.click('[data-buchse="mA"]'); assert '333,0 mA' in t('.display'), t('.display')
    pg.click('[data-methode="mv"]'); pg.click('[data-sich="F7"]'); assert '4,5 mV' in t('.mini-display'), t('.mini-display')
    pg.click('[data-methode="ziehen"]'); pg.click('[data-sich="F7"]'); assert '33,0 mA' in t('.display'), t('.display')
    pg.locator('#ruhestrom').screenshot(path=str(shots / 'ruhestrom.png'))
    pg.click('[data-gefunden]'); pg.click('[data-wahl="F7"]'); pg.click('[data-antwort]'); assert 'Richtig' in t('#ruhestrom')

    # Hochvolt: Ablauf
    pg.goto(base + '/hochvolt.html'); pg.wait_for_selector('.hv-karten')
    for s in ['zuendung', 'stecker', 'schloss', 'schild', 'messen', 'vorher', 'nachher', 'doku']:
        pg.click(f'[data-nimm="{s}"]')
    pg.click('[data-pruefen]'); txt = t('#hochvolt'); assert 'Es fehlt' in txt and 'muss vor' in txt, txt
    pg.screenshot(path=str(shots / 'hv-fehler.png'), full_page=True)
    pg.click('[data-nochmal]')
    for s in ['zuendung', 'stecker', 'schloss', 'schild', 'warten', 'vorher', 'messen', 'nachher', 'doku']:
        pg.click(f'[data-nimm="{s}"]')
    pg.click('[data-pruefen]'); assert 'Alles richtig' in t('#hochvolt')
    pg.click('[data-teil="messen"]')  # random 0.2 -> Szenario 'frei' (Index 1 = schuetz bei 5 Szenarien? 0.2*5=1)
    for s in ['quelle', 'hv+hv-', 'hv+m', 'hv-m', 'quelle']:
        pg.click(f'[data-punkt="{s}"]')
    assert '390 V' in t('#hochvolt'), t('#hochvolt')
    pg.click('[data-urteil="frei"]'); pg.click('[data-bewerten]'); assert 'Leider falsch' in t('#hochvolt')
    pg.click('[data-weiter]'); pg.click('[data-urteil="nicht-frei"]'); pg.click('[data-bewerten]'); assert 'Richtig' in t('#hochvolt')
    pg.screenshot(path=str(shots / 'hv-messen.png'), full_page=True)

    # Bremse: 0.2*7 = 1 -> diff-va
    pg.goto(base + '/bremse.html'); pg.wait_for_selector('#bp-uhren')
    for a in ['va', 'ha', 'fba']:
        pg.click(f'[data-achse="{a}"]'); pg.click('[data-messen]')
        pg.wait_for_function("!document.querySelector('[data-messen]').disabled", timeout=8000)
    pg.wait_for_selector('[data-auswerten]')
    assert '4,00' in t('.bp-tab') and '2,80' in t('.bp-tab'), t('.bp-tab')
    pg.fill('#in-diffVA', '30'); pg.fill('#in-diffHA', '5'); pg.fill('#in-zBetrieb', '61'); pg.fill('#in-zFBA', '10')
    pg.click('[data-auswerten]'); assert 'Wähle zuerst' in t('#bremse')
    pg.click('[data-befund="diff-va"]'); pg.click('[data-auswerten]')
    assert 'Befund richtig' in t('#bremse') and pg.locator('#in-zFBA.falsch').count() == 1 and pg.locator('#in-diffVA.ok').count() == 1
    pg.screenshot(path=str(shots / 'bremse.png'), full_page=True)

    pg.goto(base + '/index.html#/werkstatt')
    b.close()
if errs: print('PAGE ERRORS', errs); sys.exit(1)
print('E2E OK')
