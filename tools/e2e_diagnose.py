"""Spielt Fälle der Diagnose-Werkstatt durch. Aufruf: python3 tools/e2e_diagnose.py <basis-url> <screenshot-ordner>"""
import sys, pathlib
from playwright.sync_api import sync_playwright
base = sys.argv[1].rstrip('/'); shots = pathlib.Path(sys.argv[2]); shots.mkdir(exist_ok=True)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 390, 'height': 900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    t = lambda: pg.inner_text('#diagnose')
    obj = lambda o: pg.click(f'[data-obj="{o}"]')
    pt = lambda k: pg.click(f'[data-punkt="{k}"]', timeout=5000)

    pg.goto(base + '/diagnose.html?fall=abblend'); pg.wait_for_selector('svg.auto')
    assert 'Abblendlicht links geht nicht' in t()
    pg.screenshot(path=str(shots / 'd-vorne.png'), full_page=True)
    obj('haube'); assert 'verriegelt' in t()
    pg.click('[data-dreh="1"]'); obj('tuer'); obj('tuer')            # Fahrerseite, Tür auf, einsteigen
    assert 'Fahrerplatz' in t()
    pg.screenshot(path=str(shots / 'd-innen.png'))
    obj('zuendung'); pg.click('[data-bed="zuendung"]')
    obj('licht'); pg.click('[data-licht="abblend"]')
    obj('nav:fussraum'); obj('haubenhebel'); assert 'entriegelt' in t()
    pg.click('[data-wz="tester"]'); obj('obd'); pg.click('[data-sg="A10"]')
    assert 'B1A12-13' in t(), t()
    pg.click('[data-ts="ist"]'); assert 'Abblendlicht' in t()
    pg.screenshot(path=str(shots / 'd-tester.png'), full_page=True)
    pg.click('[data-wz="plan"]'); assert 'X4/1' in pg.inner_html('#diagnose')
    pg.screenshot(path=str(shots / 'd-plan.png'), full_page=True)
    # zum Motorraum
    pg.click('[data-zurueck]'); pg.click('[data-zurueck]'); pg.click('[data-dreh="-1"]')
    assert 'von vorne' in t(); obj('haube'); assert 'Motorraum' in t()
    pg.click('[data-wz="mm"]')
    pt('X4.1'); pt('M'); assert '0,00 V' in t(), t()
    obj('nav:box')
    pg.click('[data-zurueck]')
    pg.screenshot(path=str(shots / 'd-motorraum.png'), full_page=True)
    # Spannung am SG
    pg.click('[data-zurueck]'); pg.click('[data-dreh="1"]'); obj('tuer'); obj('abdeckung'); pg.click('[data-spitze="rot"]'); pt('A10.12')
    assert '12,48 V' in t(), t()
    pg.screenshot(path=str(shots / 'd-sk.png'), full_page=True)
    pg.click('[data-melden]'); pg.select_option('select.auswahl', 'w-abl'); pg.click('[data-art="unterbrechung"]'); pg.click('[data-pruefen]')
    assert 'Richtig' in t()

    # Hupe: Sicherung
    pg.goto(base + '/diagnose.html?fall=hupe'); pg.wait_for_selector('svg.auto')
    pg.click('[data-dreh="1"]'); obj('tuer'); obj('tuer'); obj('nav:fussraum'); obj('haubenhebel')
    pg.click('[data-zurueck]'); pg.click('[data-zurueck]'); pg.click('[data-dreh="-1"]'); obj('haube'); obj('nav:box')
    obj('si:F15'); pg.click('[data-sich="F15:raus"]'); assert 'durchgebrannt' in t()
    pg.click('[data-sich="F15:neu"]')
    pg.click('[data-zurueck]'); pg.click('[data-zurueck]'); pg.click('[data-dreh="1"]'); obj('tuer')
    obj('hupe'); pg.click('[data-bed="hupe"]')
    obj('nav:fussraum'); pg.click('[data-zurueck]'); pg.click('[data-zurueck]'); pg.click('[data-dreh="-1"]'); obj('haube'); obj('nav:box'); obj('si:F15')
    pg.click('[data-sich="F15:raus"]'); assert 'durchgebrannt' in t()

    # Blinker hinten
    pg.goto(base + '/diagnose.html?fall=blinker'); pg.wait_for_selector('svg.auto')
    pg.click('[data-dreh="1"]'); pg.click('[data-dreh="1"]'); obj('rlL'); obj('gl:e-blhl'); pg.click('[data-lampe="e-blhl"]'); assert 'durchgebrannt' in t()
    obj('st:X30'); pg.click('[data-stecker="X30"]'); pg.click('[data-wz="mm"]'); pg.click('[data-modus="R"]'); pt('X30.2*'); pt('X30.4*'); assert 'OL' in t(), t()
    pg.screenshot(path=str(shots / 'd-rl.png'), full_page=True)
    b.close()
if errs: print('PAGE ERRORS', errs); sys.exit(1)
print('E2E OK')
