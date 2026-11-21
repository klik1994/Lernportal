"""Klickt das Portal im Browser durch (375 px). Aufruf: python3 tools/e2e_portal.py <basis-url> <screenshot-ordner>"""
import sys, pathlib
from playwright.sync_api import sync_playwright

base = sys.argv[1].rstrip('/')
shots = pathlib.Path(sys.argv[2]); shots.mkdir(exist_ok=True)
errors = []

def answer_all(page):
    while True:
        page.wait_for_selector('[data-pruefen], [data-fertig]')
        if page.locator('[data-fertig]').count():
            return
        page.locator('[data-antwort]').nth(0).click()
        page.click('[data-pruefen]')
        page.click('[data-weiter]')

with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    page = b.new_context(viewport={'width': 375, 'height': 800}).new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/index.html')
    page.wait_for_selector('[data-start="eingang"]')
    assert '18 Fragen aus 6 Themen' in page.inner_text('#app')
    page.screenshot(path=str(shots / 'p1-willkommen.png'), full_page=True)
    page.goto(base + '/index.html#/themen')
    page.wait_for_selector('[data-start="eingang"]')
    page.click('[data-start="eingang"]')
    page.click('[data-pruefen]')
    assert 'Wähle zuerst' in page.inner_text('#app')
    answer_all(page)
    page.screenshot(path=str(shots / 'p2-auswertung.png'), full_page=True)
    page.click('[data-fertig]')
    page.wait_for_selector('text=Als Nächstes')
    page.screenshot(path=str(shots / 'p3-lernstand.png'), full_page=True)
    page.click('#nav a[data-r="themen"]')
    page.wait_for_selector('.bereich')
    assert 'Elektrik-Grundlagen' in page.inner_text('#app')
    page.locator('[data-stern]').nth(0).click()
    page.screenshot(path=str(shots / 'p4-themen.png'), full_page=True)
    page.locator('a.t').nth(1).click()
    page.wait_for_selector('[data-kurz]')
    page.screenshot(path=str(shots / 'p5-thema.png'), full_page=True)
    page.click('[data-kurz]')
    answer_all(page)
    page.click('[data-fertig]')
    page.click('#nav a[data-r="ueben"]')
    page.click('[data-start="uebung"]')
    assert 'mindestens ein Thema' in page.inner_text('#app')
    page.locator('[data-wahl]').nth(0).check()
    page.click('[data-start="uebung"]')
    page.locator('[data-antwort]').nth(0).click(); page.click('[data-pruefen]')
    page.click('[data-abbrechen]')
    page.wait_for_selector('[data-wahl]')
    page.click('footer >> text=Impressum')
    page.wait_for_selector('text=§ 5 DDG')
    assert 'Excel-Datei' in page.inner_text('#app')
    page.click('footer >> text=Datenschutz')
    page.wait_for_selector('text=GitHub Pages')
    page.screenshot(path=str(shots / 'p7-datenschutz.png'), full_page=True)
    before = page.evaluate("localStorage.getItem('kfz-lernportal-v1')")
    page.goto(base + '/index.html#/')
    page.wait_for_selector('text=Als Nächstes')
    assert page.evaluate("localStorage.getItem('kfz-lernportal-v1')") == before and before
    page.goto(base + '/multimeter.html')
    page.click('[data-dreh="V="]'); page.click('[data-punkt="B+"]'); page.click('[data-punkt="Masse"]')
    assert '12,6 V' in page.inner_text('#mm')
    page.screenshot(path=str(shots / 'p6-multimeter.png'), full_page=True)
    b.close()

if errors:
    print('PAGE ERRORS', errors); sys.exit(1)
print('E2E OK')
