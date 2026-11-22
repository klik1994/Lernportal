"""Klickt die CAN-Bus-Diagnose durch. Aufruf: python3 tools/e2e_can.py <basis-url> <screenshot-ordner>"""
import sys, pathlib
from playwright.sync_api import sync_playwright
base = sys.argv[1].rstrip('/'); shots = pathlib.Path(sys.argv[2]); shots.mkdir(exist_ok=True)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 375, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(base + '/can.html')
    pg.wait_for_selector('svg.oszi')
    t = pg.inner_text('#can'); assert '2,5 … 3,5 V' in t and '1,5 … 2,5 V' in t, t
    pg.locator('.oszi-box').screenshot(path=str(shots / 'can-normal.png'))
    pg.click('[data-bild="h-plus"]'); assert 'außerhalb' in pg.inner_text('#can')
    pg.click('[data-volt="5"]'); assert 'außerhalb' not in pg.inner_text('#can')
    pg.locator('.oszi-box').screenshot(path=str(shots / 'can-hplus.png'))
    pg.click('[data-volt="1"]'); pg.click('[data-bild="r-beide"]'); pg.click('[data-zeit="2"]')
    pg.locator('.oszi-box').screenshot(path=str(shots / 'can-rbeide.png'))
    pg.click('[data-zeit="10"]'); pg.click('[data-paar="6-14"]'); assert 'nie unter Spannung' in pg.inner_text('#can')
    pg.click('[data-zuendung]'); pg.click('[data-paar="6-14"]'); assert 'OL' in pg.inner_text('#can')
    pg.evaluate("Math.random = () => 0.01")
    pg.click('[data-modus="fehler"]')
    pg.click('[data-zuendung]'); pg.click('[data-paar="6-4"]'); assert '0,0 Ω' in pg.inner_text('#can')
    pg.click('[data-gefunden]'); pg.click('[data-antwort]'); assert 'Wähle zuerst' in pg.inner_text('#can')
    pg.click('[data-wahl="l-masse"]'); pg.click('[data-antwort]'); assert 'Leider falsch' in pg.inner_text('#can')
    pg.click('[data-weiter]'); pg.click('[data-gefunden]'); pg.click('[data-wahl="h-masse"]'); pg.click('[data-antwort]')
    assert 'Richtig erkannt' in pg.inner_text('#can')
    pg.screenshot(path=str(shots / 'can-seite.png'), full_page=True)
    pg.goto(base + '/index.html#/werkstatt')
    b.close()
if errs: print('PAGE ERRORS', errs); sys.exit(1)
print('E2E OK')
