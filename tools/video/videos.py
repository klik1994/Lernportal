"""Lernvideos fuer das Lernportal (Spannung, Strom, Widerstand; weitere Themen als neuer Eintrag in VIDEOS).
Aufruf: python3 tools/video/videos.py <thema> [stills|render] [szenen]
  stills  -> Standbilder je Szene nach /tmp/lernvideo/stills zum Pruefen
  render  -> praesentationen/videos/<thema>.mp4 (1280x720, 30 fps, ohne Ton)
  szenen  -> optional, z. B. 2,4 = nur diese Szenen neu rendern (-1 = keine, nur zusammenfuegen)"""
import math, os, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import *
from scenes import *

import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = '/tmp/lernvideo'
os.makedirs(OUT, exist_ok=True)


def dashed(d, x0, x1, y, col, a, dash=12, gap=8, w=2):
    x = x0
    while x < x1:
        line(d, [(x, y), (min(x + dash, x1), y)], col, w, a)
        x += dash + gap


def dashed_v(d, x, y0, y1, col, a, dash=12, gap=8, w=2):
    y = y0
    while y < y1:
        line(d, [(x, y), (x, min(y + dash, y1))], col, w, a)
        y += dash + gap


# =================== SPANNUNG ===================
def sp_water(d, t, dur):
    C = YEL
    header(d, t, 'SPANNUNG', 'Der Wasser-Vergleich', C)
    a = pr(t, 0.2, 1.0)
    LX0, LX1, RX0, RX1, TY, BY = 230, 410, 870, 1050, 170, 470
    fill = pr(t, 0.8, 2.6)
    eq = pr(t, 7.4, 12.0)
    yL = lerp(BY, lerp(210, 305, eq), fill)
    yR = lerp(BY, lerp(400, 305, eq), fill)
    # Rohr
    rect(d, (LX1, 425, RX0, 465), WATER, a * fill)
    diff = (yR - yL) / 190 if fill > 0.99 else 0
    vopen = pr(t, 6.2, 7.0)
    if vopen > 0 and diff > 0.01:
        pth = Path([(LX1 - 20, 445), (RX0 + 20, 445)])
        flow_dots(d, pth, t, 40 + 160 * diff, 34, 6, (190, 225, 255), vopen * min(1, diff * 3), bg=WATER)
    line(d, [(LX1, 423), (RX0, 423)], TXT, 4, a)
    line(d, [(LX1, 467), (RX0, 467)], TXT, 4, a)
    # Wasser in Tanks
    rect(d, (LX0, yL, LX1, BY), WATER, a)
    rect(d, (RX0, yR, RX1, BY), WATER, a)
    for x0, x1 in ((LX0, LX1), (RX0, RX1)):
        line(d, [(x0, TY), (x0, BY), (x1, BY), (x1, TY)], TXT, 5, a)
    # Ventil
    vx = 640
    circle(d, (vx, 445), 30, CARD2, a, outline=TXT, width=4)
    ang = math.radians(90 * (1 - vopen))
    line(d, [(vx - 22 * math.cos(ang), 445 - 22 * math.sin(ang)),
             (vx + 22 * math.cos(ang), 445 + 22 * math.sin(ang))], C, 7, a, bg=CARD2)
    text(d, vx, 500, 'Ventil ' + ('offen' if vopen > 0.5 else 'zu'), 20, 'Semi', MUTED, a, 'mm')
    text(d, (LX0 + LX1) / 2, 140, 'hoch', 24, 'Bold', TXT, a * fill, 'mm')
    text(d, (RX0 + RX1) / 2, 140, 'niedrig' if eq < 0.6 else 'gleich hoch', 24, 'Bold', TXT, a * fill, 'mm')
    # Bemassung
    da = pr(t, 2.8, 3.6) * (1 - pr(t, 10.5, 11.5))
    if da > 0.01 and yR - yL > 6:
        dashed(d, LX1 + 6, 1150, yL, C, da)
        dashed(d, RX1 + 6, 1150, yR, C, da)
        arrow(d, (1130, (yL + yR) / 2), (1130, yL + 2), C, 4, 12, da)
        arrow(d, (1130, (yL + yR) / 2), (1130, yR - 2), C, 4, 12, da)
        text(d, 1150, (yL + yR) / 2 - 14, 'Höhen-', 18, 'Bold', C, da, 'lm')
        text(d, 1150, (yL + yR) / 2 + 10, 'unterschied', 18, 'Bold', C, da, 'lm')
    caption(d, t, [(1.0, 6.2, 'Der Höhenunterschied entspricht der Spannung'),
                   (6.4, 10.6, 'Ventil auf: Wasser fließt von hoch nach niedrig'),
                   (10.8, dur, 'Kein Unterschied → kein Fluss.  Ohne Spannung kein Strom!')], C)


random.seed(3)
CH_R = [(random.uniform(670, 850), random.uniform(290, 470), random.uniform(0, 6.28)) for _ in range(26)]
CH_L = [(random.uniform(450, 610), random.uniform(290, 470), random.uniform(0, 6.28)) for _ in range(4)]


def sp_battery(d, t, dur):
    C = YEL
    header(d, t, 'SPANNUNG', 'Was ist Spannung?', C)
    a = pr(t, 0.1, 0.8)
    bgc = (50, 58, 72)
    hl_r = pr(t, 0.6, 1.2) * (1 - pr(t, 4.4, 4.8))
    hl_l = pr(t, 4.6, 5.2) * (1 - pr(t, 7.4, 7.8))
    rrect(d, (400, 240, 880, 500), 18, bgc, a, outline=(90, 100, 118), width=3)
    if hl_l > 0.01:
        rrect(d, (410, 250, 636, 490), 12, mix(MUTED, 0.22 * hl_l, bgc), 1, bg=bgc)
    if hl_r > 0.01:
        rrect(d, (644, 250, 870, 490), 12, mix(RED, 0.25 * hl_r, bgc), 1, bg=bgc)
    for y in range(256, 490, 22):
        line(d, [(640, y), (640, y + 11)], MUTED, 2, a, bg=bgc)
    rrect(d, (480, 206, 520, 242), 6, (70, 78, 92), a)
    rrect(d, (760, 206, 800, 242), 6, RED, a)
    text(d, 500, 186, '−', 40, 'Bold', TXT, a, 'mm')
    text(d, 780, 186, '+', 40, 'Bold', RED, a, 'mm')
    for i, (ex, ey, ph) in enumerate(CH_R + CH_L):
        jx = ex + 4 * math.sin(t * 3 + ph)
        jy = ey + 4 * math.cos(t * 2.6 + ph)
        ka = pr(t, 0.3 + i * 0.03, 0.7 + i * 0.03)
        circle(d, (jx, jy), 11, RED, a * ka, bg=bgc)
        text(d, jx, jy, '+', 16, 'Bold', BG, a * ka, 'mm', bg=RED)
    text(d, 760, 520, 'viel Ladung', 20, 'Bold', RED, a * pr(t, 0.8, 1.4), 'mm')
    text(d, 520, 520, 'wenig Ladung', 20, 'Bold', MUTED, a * pr(t, 4.8, 5.4), 'mm')
    ua = pr(t, 7.6, 8.4)
    if ua > 0.01:
        arrow(d, (640, 186), (532, 186), C, 5, 16, ua)
        arrow(d, (640, 186), (748, 186), C, 5, 16, ua)
        text(d, 640, 150, 'U', 34, 'XB', C, ua, 'mm')
        text(d, 960, 330, 'U = 12,6 V', 40, 'XB', C, ua, 'lm')
        text(d, 960, 372, 'volle Kfz-Batterie', 20, 'Med', MUTED, ua, 'lm')
    caption(d, t, [(0.6, 4.4, 'Pluspol: viel Ladung (+)'),
                   (4.6, 7.4, 'Minuspol: wenig Ladung'),
                   (7.6, dur, 'Der Ladungsunterschied ist die Spannung U –\nder Strom will von + nach − fließen')], C)


SP_VALUES = values_scene('SPANNUNG', YEL, [('Formelzeichen', 'U'), ('Einheit', 'Volt (V)')],
                         [('1,5 V', 'Mignon-Batterie (AA)'),
                          ('5 V', 'Versorgungsspannung vieler Sensoren'),
                          ('12,6 V', 'volle 12-V-Batterie im Ruhezustand'),
                          ('ca. 14 V', 'Bordnetz bei laufendem Motor'),
                          ('400–800 V', 'Hochvolt-Fahrzeuge (nur mit Qualifikation!)')])


def meter_reading(t, st, en, val, dec, unit):
    k = pr(t, st, en)
    if k <= 0:
        return '0' + (',' + '0' * dec if dec else '') + ' ' + unit
    v = val * k
    s = f'{v:.{dec}f}'.replace('.', ',')
    return s + ' ' + unit


def sp_measure(d, t, dur):
    C = YEL
    header(d, t, 'SPANNUNG', 'Spannung messen', C)
    a = pr(t, 0.1, 0.8)
    circuit(d, t, a=a, closed=1, bridge='wire', on=1.0 * a)
    ma = pr(t, 1.2, 2.0)
    mode = 'V' if t > 2.6 else 'OFF'
    k1 = pr(t, 3.6, 5.0)
    k2 = pr(t, 5.0, 6.4)
    sel = ['VΩ', 'COM'] if t > 3.4 else None
    rd = meter_reading(t, 6.6, 7.6, 12.4, 1, 'V') if t > 2.6 else ''
    socks = multimeter(d, MM_X, MM_Y, ma, rd, mode, 'V DC' if t > 2.6 else '', YEL, sel)
    p_top, p_bot = lamp_points()
    pa = pr(t, 3.2, 3.8)
    for p in (p_top, p_bot):
        circle(d, p, 10 + 3 * math.sin(t * 6), C, pa * (1 - k2 * 0.5))
    lead(d, socks['VΩ'], p_top, RED, k1, ma, sag=90)
    lead(d, socks['COM'], p_bot, BLACK, k2, ma, sag=50)
    pa2 = pr(t, 7.4, 8.2)
    if pa2 > 0.01:
        text(d, 760, 120, 'parallel zur Lampe', 22, 'Bold', C, pa2, 'mm')
    caption(d, t, [(0.6, 3.4, 'Messbereich wählen: V DC (Gleichspannung)'),
                   (3.6, 7.2, 'Rot in die VΩ-Buchse, Schwarz in COM'),
                   (7.4, 10.8, 'Parallel zum Verbraucher messen –\nder Stromkreis bleibt geschlossen'),
                   (11.0, dur, 'Anzeige: An der Lampe liegen 12,4 V an')], C)


SP_MERKE = merke_scene('SPANNUNG', YEL, [
    'Spannung U in Volt (V)', 'Spannung ist die Ursache für den Strom',
    'Immer parallel zum Bauteil messen\nMessbereich V DC, Stromkreis bleibt geschlossen',
    'Rot → VΩ-Buchse,  Schwarz → COM'])


# =================== STROM ===================
def st_water(d, t, dur):
    C = BLU
    header(d, t, 'STROM', 'Der Wasser-Vergleich', C)
    for i, (y, sp, gap, lab, st) in enumerate([(210, 55, 120, 'wenig Strom', 0.3), (400, 170, 34, 'viel Strom', 5.6)]):
        a = pr(t, st, st + 0.7)
        rect(d, (150, y, 1130, y + 80), WATER, a * 0.55)
        line(d, [(150, y), (1130, y)], TXT, 4, a)
        line(d, [(150, y + 80), (1130, y + 80)], TXT, 4, a)
        if a > 0.01:
            wbg = mix(WATER, 0.55)
            for row, yy in enumerate((y + 22, y + 40, y + 58)):
                pth = Path([(150, yy), (1130, yy)])
                flow_dots(d, pth, t + row * gap / 3 / sp, sp, gap, 7, (225, 240, 255), a, bg=wbg)
        text(d, 150, y - 26, lab, 26, 'Bold', C, a, 'lm')
        # Zaehler
        cnt = int(max(0, t - st - 0.7) * sp / gap * 3)
        text(d, 1130, y - 26, f'{cnt} Teilchen', 22, 'Semi', MUTED, a, 'rm')
        dashed_v(d, 900, y - 10, y + 92, C, a, w=3)
    ma = pr(t, 1.0, 1.6)
    text(d, 900, 330, 'Messstelle', 18, 'Bold', C, ma, 'mm')
    caption(d, t, [(1.2, 5.4, 'Strom = Menge, die pro Sekunde\ndurch den Leiter fließt'),
                   (6.4, dur, 'Mehr Teilchen pro Sekunde → größerer Strom')], C)


def st_circuit(d, t, dur):
    C = BLU
    header(d, t, 'STROM', 'Strom im Stromkreis', C)
    a = pr(t, 0.1, 0.8)
    cl = pr(t, 2.6, 3.2)
    flow = pr(t, 3.2, 3.8)
    circuit(d, t, a=a, closed=cl, bridge='switch', on=flow, flow=flow)
    la = pr(t, 7.2, 8.0)
    if la > 0.01:
        arrow(d, (290, 100), (530, 100), YEL, 5, 16, la)
        text(d, 545, 100, '+ → −', 20, 'Bold', YEL, la, 'lm')
        rrect(d, (790, 200, 1210, 400), 18, CARD, la)
        text(d, 820, 240, 'Technische Stromrichtung', 24, 'Bold', TXT, la, 'lm', bg=CARD)
        text(d, 820, 290, 'Vom Pluspol über den', 20, 'Semi', TXT, la, 'lm', bg=CARD)
        text(d, 820, 318, 'Verbraucher zum Minuspol', 20, 'Semi', TXT, la, 'lm', bg=CARD)
        text(d, 820, 362, '+  →  −', 30, 'XB', YEL, la, 'lm', bg=CARD)
    caption(d, t, [(0.6, 3.0, 'Schalter offen: Stromkreis unterbrochen – kein Strom'),
                   (3.4, 7.0, 'Schalter zu: Strom fließt, die Lampe leuchtet'),
                   (7.2, dur, 'Der Strom fließt von + nach −')], C)


ST_VALUES = values_scene('STROM', BLU, [('Formelzeichen', 'I'), ('Einheit', 'Ampere (A)'), ('', '1 A = 1000 mA')],
                         [('ca. 20 mA', 'eine LED'),
                          ('< 50 mA', 'Ruhestrom bei abgestelltem Fahrzeug'),
                          ('ca. 4,6 A', 'Halogenlampe H7, 55 W'),
                          ('150–300 A', 'Anlasser beim Starten (Pkw)')],
                         note='Richtwerte – genaue Werte immer laut Herstellerangabe')


def st_measure(d, t, dur):
    C = BLU
    header(d, t, 'STROM', 'Strom messen', C)
    a = pr(t, 0.1, 0.8)
    cut = pr(t, 1.4, 2.4)
    k1 = pr(t, 6.6, 7.8)
    k2 = pr(t, 7.8, 9.0)
    conn = pr(t, 9.0, 9.6)
    on = (1 - cut) if t < 9 else conn
    circuit(d, t, a=a, closed=1 - cut, bridge='wire', on=on * a, flow=on)
    ga = pr(t, 2.0, 2.6) * (1 - pr(t, 6.4, 7.0))
    if ga > 0.01:
        text(d, (GAP_L + GAP_R) / 2, TOPY - 40, 'aufgetrennt', 20, 'Bold', RED, ga, 'mm')
    ma = pr(t, 2.8, 3.6)
    mode = 'A' if t > 4.2 else 'OFF'
    sel = ['A', 'COM'] if t > 4.8 else None
    rd = meter_reading(t, 9.4, 10.4, 4.58, 2, 'A') if t > 4.2 else ''
    socks = multimeter(d, MM_X, MM_Y, ma, rd, mode, 'A DC' if t > 4.2 else '', BLU, sel)
    lead(d, socks['A'], (GAP_L, TOPY), RED, k1, ma, sag=110)
    lead(d, socks['COM'], (GAP_R, TOPY), BLACK, k2, ma, sag=70)
    ra = pr(t, 9.6, 10.2)
    if ra > 0.01:
        text(d, 760, 105, 'in Reihe geschaltet', 22, 'Bold', C, ra, 'mm')
    caption(d, t, [(0.6, 3.2, 'Stromkreis auftrennen –\nder Strom muss durch das Messgerät'),
                   (3.4, 6.4, 'Messbereich A wählen,\nrote Leitung in die A-Buchse'),
                   (6.6, 10.4, 'Messgerät in Reihe schalten'),
                   (10.6, dur, 'Danach die rote Leitung wieder in VΩ stecken!')], C)


ST_MERKE = merke_scene('STROM', BLU, [
    'Strom I in Ampere (A)', 'Strom fließt nur im geschlossenen Stromkreis',
    'Immer in Reihe messen\nStromkreis auftrennen, Messgerät dazwischen',
    'Große Ströme (z. B. Anlasser): Stromzange\nMessgerät-Sicherung meist nur 10 A'])


# =================== WIDERSTAND ===================
def wi_water(d, t, dur):
    C = RED
    header(d, t, 'WIDERSTAND', 'Der Wasser-Vergleich', C)
    a = pr(t, 0.1, 0.8)
    # Behaelter
    rect(d, (120, 180, 320, 500), WATER, a)
    line(d, [(120, 150), (120, 500), (320, 500), (320, 150)], TXT, 5, a)
    for (y, h, sp, gap, lab, val, st) in [(220, 90, 170, 34, 'weites Rohr', 'kleiner Widerstand → viel Strom', 0.5),
                                          (420, 26, 50, 110, 'enges Rohr', 'großer Widerstand → wenig Strom', 3.0)]:
        k = pr(t, st, st + 0.8)
        cy = y + h / 2 if h > 30 else y + 13
        y0, y1 = cy - h / 2, cy + h / 2
        rect(d, (320, y0, 1120, y1), WATER, k * 0.55)
        line(d, [(320, y0), (1120, y0)], TXT, 4, k)
        line(d, [(320, y1), (1120, y1)], TXT, 4, k)
        wbg = mix(WATER, 0.55)
        rows = [cy - 24, cy, cy + 24] if h > 30 else [cy]
        for i, yy in enumerate(rows):
            flow_dots(d, Path([(320, yy), (1120, yy)]), t + i * 0.3, sp, gap, 7 if h > 30 else 6,
                      (225, 240, 255), k, bg=wbg)
        text(d, 360, y0 - 26, lab, 22, 'Bold', TXT, k, 'lm')
        text(d, 1120, y0 - 26, val, 22, 'Bold', C, pr(t, st + 1.0, st + 1.6), 'rm')
    caption(d, t, [(0.8, 6.0, 'Ein enges Rohr bremst das Wasser stärker'),
                   (6.2, dur, 'Der Widerstand bremst den Strom')], C)


def wi_factors(d, t, dur):
    C = RED
    header(d, t, 'WIDERSTAND', 'Wovon hängt der Widerstand ab?', C)
    cards = [(150, 110, 'Länge', 'länger → größerer Widerstand'),
             (660, 110, 'Querschnitt', 'dünner → größerer Widerstand'),
             (150, 335, 'Material', 'Kupfer leitet besser als Eisen'),
             (660, 335, 'Temperatur', 'Metall wärmer → größerer Widerstand')]
    for i, (x, y, ti, de) in enumerate(cards):
        st = 0.4 + i * 2.2
        k = pr(t, st, st + 0.6)
        dy = (1 - eout((t - st) / 0.6)) * 24
        y += dy
        rrect(d, (x, y, x + 470, y + 200), 20, CARD, k)
        text(d, x + 28, y + 36, ti, 28, 'XB', C, k, 'lm', bg=CARD)
        text(d, x + 28, y + 172, de, 20, 'Semi', TXT, k, 'lm', bg=CARD)
        g = pr(t, st + 0.5, st + 1.6)
        if i == 0:
            line(d, [(x + 30, y + 88), (x + 30 + 120, y + 88)], (205, 127, 60), 8, k, bg=CARD)
            line(d, [(x + 30, y + 128), (x + 30 + 120 + 190 * g, y + 128)], (205, 127, 60), 8, k, bg=CARD)
            text(d, x + 440, y + 88, 'R klein', 18, 'Bold', GRN, k, 'rm', bg=CARD)
            text(d, x + 440, y + 128, 'R groß', 18, 'Bold', C, k * g, 'rm', bg=CARD)
        elif i == 1:
            rrect(d, (x + 30, y + 72, x + 330, y + 102), 15, (205, 127, 60), k, bg=CARD)
            hh = lerp(15, 3, g)
            rrect(d, (x + 30, y + 128 - hh, x + 330, y + 128 + hh), hh, (205, 127, 60), k, bg=CARD)
            text(d, x + 440, y + 87, 'R klein', 18, 'Bold', GRN, k, 'rm', bg=CARD)
            text(d, x + 440, y + 128, 'R groß', 18, 'Bold', C, k * g, 'rm', bg=CARD)
        elif i == 2:
            rrect(d, (x + 30, y + 74, x + 200, y + 140), 12, (205, 127, 60), k, bg=CARD)
            text(d, x + 115, y + 107, 'Kupfer', 22, 'Bold', BG, k, 'mm', bg=(205, 127, 60))
            rrect(d, (x + 230, y + 74, x + 400, y + 140), 12, (120, 128, 140), k * g, bg=CARD)
            text(d, x + 315, y + 107, 'Eisen', 22, 'Bold', BG, k * g, 'mm', bg=(120, 128, 140))
        else:
            tx = x + 60
            rrect(d, (tx - 10, y + 62, tx + 10, y + 132), 10, None, k, outline=TXT, width=3, bg=CARD)
            circle(d, (tx, y + 138), 16, C, k, bg=CARD)
            lv = y + lerp(118, 72, g)
            rect(d, (tx - 4, lv, tx + 4, y + 132), C, k, bg=CARD)
            text(d, tx + 50, y + 100, f'{int(lerp(20, 90, g))} °C', 30, 'XB', TXT, k, 'lm', bg=CARD)
    caption(d, t, [(9.4, dur, 'Darum: Kabel mit ausreichendem Querschnitt verwenden!')], C, y=600)


WI_VALUES = values_scene('WIDERSTAND', RED, [('Formelzeichen', 'R'), ('Einheit', 'Ohm (Ω)'), ('', '1 kΩ = 1000 Ω')],
                         [('ca. 0 Ω', 'intakte Leitung oder Sicherung'),
                          ('120 Ω', 'CAN-Abschlusswiderstand (am Bus: 60 Ω)'),
                          ('12–16 Ω', 'hochohmiges Einspritzventil'),
                          ('ca. 2–3 kΩ', 'Temperaturfühler (NTC) bei 20 °C')],
                         note='Richtwerte – Sollwerte immer aus dem Reparaturleitfaden')


def wi_measure(d, t, dur):
    C = RED
    header(d, t, 'WIDERSTAND', 'Widerstand messen', C)
    a = pr(t, 0.1, 0.8)
    off = pr(t, 1.0, 2.6)
    wa = a * (1 - 0.85 * off)
    circuit(d, t, a=a, wire_a=wa, bat_a=wa, closed=1, bridge='wire', on=0, element='none')
    line(d, [(620, 255), (620, 345)], WIRE, 5, wa)
    resistor(d, LAMP_C, 50, 110, a, C)
    text(d, 575, 290, 'Bauteil', 20, 'Bold', TXT, a, 'rm')
    text(d, 575, 316, 'z. B. Einspritzventil', 18, 'Med', MUTED, a, 'rm')
    xa = pr(t, 1.6, 2.2)
    if xa > 0.01:
        line(d, [(150, 270), (250, 360)], C, 7, xa)
        line(d, [(150, 360), (250, 270)], C, 7, xa)
        text(d, 200, 410, 'abgeklemmt', 20, 'Bold', C, xa, 'mm')
    ma = pr(t, 3.0, 3.8)
    mode = 'Ω' if t > 4.4 else 'OFF'
    sel = ['VΩ', 'COM'] if t > 6.8 else None
    rd = meter_reading(t, 10.0, 11.0, 14.5, 1, 'Ω') if t > 4.4 else ''
    socks = multimeter(d, MM_X, MM_Y, ma, rd, mode, 'Ω' if t > 4.4 else '', RED, sel)
    k1 = pr(t, 7.4, 8.6)
    k2 = pr(t, 8.6, 9.8)
    lead(d, socks['VΩ'], (620, 236), RED, k1, ma, sag=90)
    lead(d, socks['COM'], (620, 364), BLACK, k2, ma, sag=50)
    caption(d, t, [(0.4, 3.4, 'Zuerst spannungsfrei machen: Bauteil abklemmen'),
                   (3.6, 7.2, 'Messbereich Ω wählen'),
                   (7.4, 10.6, 'Messspitzen an beide Anschlüsse des Bauteils'),
                   (10.8, dur, 'Anzeige: 14,5 Ω – mit dem Sollwert vergleichen')], C)


def wi_ohm(d, t, dur):
    C = RED
    header(d, t, 'WIDERSTAND', 'Das Ohmsche Gesetz', C)
    k = pr(t, 0.2, 1.2, eout)
    cx, top, base = 380, 150, 470
    pts = [(cx, top), (cx + 210, base), (cx - 210, base)]
    poly(d, pts, CARD, k)
    line(d, pts + [pts[0]], C, 5, k)
    line(d, [(cx - 116, 330), (cx + 116, 330)], C, 4, k, bg=CARD)
    line(d, [(cx, 330), (cx, base)], C, 4, k, bg=CARD)
    text(d, cx, 262, 'U', 64, 'XB', YEL, k, 'mm', bg=CARD)
    text(d, cx - 80, 410, 'R', 56, 'XB', RED, k, 'mm', bg=CARD)
    text(d, cx + 80, 410, 'I', 56, 'XB', BLU, k, 'mm', bg=CARD)
    fs = [('U = R · I', 0.9), ('I = U : R', 1.9), ('R = U : I', 2.9)]
    for i, (f, st) in enumerate(fs):
        ka = pr(t, st, st + 0.6)
        text(d, 720 + (1 - ka) * 20, 200 + i * 70, f, 46, 'XB', TXT, ka, 'lm')
    ea = pr(t, 4.8, 5.4)
    rrect(d, (700, 410, 1180, 520), 18, CARD, ea)
    text(d, 725, 442, 'Beispiel:', 20, 'Bold', C, ea, 'lm', bg=CARD)
    text(d, 725, 484, 'I = 12 V : 4 Ω = 3 A', 32, 'XB', TXT, ea, 'lm', bg=CARD)
    caption(d, t, [(0.5, 4.6, 'Spannung, Strom und Widerstand hängen zusammen'),
                   (4.8, dur, 'Finger auf die gesuchte Größe – der Rest ist die Formel')], C)


WI_MERKE = merke_scene('WIDERSTAND', RED, [
    'Widerstand R in Ohm (Ω)', 'Der Widerstand bremst den Strom',
    'Nur spannungsfrei messen\nBauteil abklemmen, Messbereich Ω',
    'Ohmsches Gesetz: U = R · I'])

VIDEOS = {
    'spannung': (YEL, [(title_scene('U', 'Spannung', 'Der Antrieb für den Strom', YEL), 5.0),
                       (sp_water, 14.0), (sp_battery, 10.5), (SP_VALUES, 10.5), (sp_measure, 14.0),
                       (SP_MERKE, 7.5)]),
    'strom': (BLU, [(title_scene('I', 'Strom', 'Bewegte Ladung im Stromkreis', BLU), 5.0),
                    (st_water, 12.0), (st_circuit, 12.0), (ST_VALUES, 10.0), (st_measure, 14.5),
                    (ST_MERKE, 7.5)]),
    'widerstand': (RED, [(title_scene('R', 'Widerstand', 'Die Bremse für den Strom', RED), 5.0),
                         (wi_water, 11.0), (wi_factors, 12.5), (WI_VALUES, 10.0), (wi_measure, 14.0),
                         (wi_ohm, 9.5), (WI_MERKE, 7.5)]),
}


from sensorik import VIDEOS_SENSORIK
VIDEOS.update(VIDEOS_SENSORIK)
from motor import VIDEOS_MOTOR
VIDEOS.update(VIDEOS_MOTOR)


if __name__ == '__main__':
    name = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'render'
    color, scenes = VIDEOS[name]
    total = sum(dd for _, dd in scenes)
    if mode == 'stills':
        os.makedirs(OUT + '/stills', exist_ok=True)
        for i, (fn, dur) in enumerate(scenes):
            for frac in (0.55, 0.95):
                still(fn, dur, dur * frac, f'{OUT}/stills/{name}_{i}_{int(frac*100)}.png')
        print('ok')
    else:
        only = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else None
        g = 0
        files = []
        for i, (fn, dur) in enumerate(scenes):
            f = f'{OUT}/{name}_{i}.mp4'
            files.append(f)
            if only is None or i in only:
                render_scene(fn, dur, f, g, total, color)
            g += dur
        lst = f'{OUT}/{name}.txt'
        with open(lst, 'w') as fh:
            for f in files:
                fh.write(f"file '{f}'\n")
        final = str(ROOT / 'praesentationen' / 'videos' / f'{name}.mp4')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                        '-c', 'copy', '-movflags', '+faststart', final + '.tmp.mp4'], check=True)
        os.replace(final + '.tmp.mp4', final)
        print('done', final, total)
