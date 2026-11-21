"""Lernvideos zum Thema Sensoren, Aktoren und EVA-Prinzip."""
import math
from engine import *
from scenes import title_scene, values_scene, merke_scene

KICK = 'SENSOREN UND AKTOREN  ·  LERNVIDEO'
EVA_COL = {'E': GRN, 'V': PUR, 'A': ORA}


def eva_card(d, x, y, w, h, letter, title, lines, a, hot=0.0):
    col = EVA_COL[letter]
    if hot > 0.01:
        rrect(d, (x - 6, y - 6, x + w + 6, y + h + 6), 24, col, a * hot * 0.6)
    rrect(d, (x, y, x + w, y + h), 18, CARD, a)
    rect(d, (x + 14, y, x + w - 14, y + 7), col, a, bg=CARD)
    text(d, x + 24, y + 32, title.upper(), 15, 'Bold', MUTED, a, 'lm', bg=CARD)
    text(d, x + 24, y + 80, letter, 50, 'XB', col, a, 'lm', bg=CARD)
    for i, l in enumerate(lines):
        text(d, x + 24, y + 132 + i * 34, l, 22, 'Bold', TXT if i == 0 else col, a, 'lm', bg=CARD)


def pulse_arrow(d, x0, x1, y, col, t, a, active=1.0):
    line(d, [(x0, y), (x1 - 14, y)], mix(col, 0.35), 6, a)
    poly(d, [(x1, y), (x1 - 18, y - 11), (x1 - 18, y + 11)], col, a)
    if active > 0.01:
        for k in range(3):
            p = ((t * 1.4 + k / 3) % 1)
            circle(d, (lerp(x0, x1 - 16, p), y), 7, col, a * active)


# =================== EVA ===================
def eva_human(d, t, dur):
    header(d, t, 'EVA-PRINZIP', 'So macht es dein Körper', PUR)
    text(d, 640, 118, 'Du fasst aus Versehen an einen heißen Auspuff …', 24, 'Med', MUTED, pr(t, 0.3, 0.9), 'mm')
    cards = [('E', 'Eingabe', ['Die Haut fühlt:', 'heiß!']), ('V', 'Verarbeitung', ['Das Gehirn sagt:', 'Hand weg!']),
             ('A', 'Ausgabe', ['Die Muskeln ziehen', 'die Hand zurück.'])]
    for i, (l, ti, ls) in enumerate(cards):
        st = 0.8 + i * 1.8
        a = pr(t, st, st + 0.6)
        dy = (1 - eout((t - st) / 0.6)) * 30
        hot = pr(t, st + 0.3, st + 0.8) * (1 - pr(t, st + 1.4, st + 1.9))
        eva_card(d, 90 + i * 400, 170 + dy, 300, 230, l, ti, ls, a, hot)
        if i < 2:
            pulse_arrow(d, 400 + i * 400, 480 + i * 400, 285, EVA_COL[cards[i + 1][0]], t, pr(t, st + 1.2, st + 1.6))
    caption(d, t, [(0.8, 6.2, 'Dein Körper arbeitet nach dem EVA-Prinzip'),
                   (6.4, dur, 'Sensor = Sinnesorgan · Steuergerät = Gehirn · Aktor = Muskel')], PUR)


def eva_kfz(d, t, dur):
    header(d, t, 'EVA-PRINZIP', 'EVA im Kfz: der Kühlerlüfter', PUR)
    a = pr(t, 0.1, 0.8)
    temp = lerp(80, 105, pr(t, 1.0, 4.6))
    hotE = pr(t, 3.8, 4.4) * (1 - pr(t, 5.4, 5.9))
    hotV = pr(t, 6.0, 6.5) * (1 - pr(t, 8.0, 8.5))
    hotA = pr(t, 8.6, 9.1)
    eva_card(d, 70, 150, 330, 300, 'E', 'Eingabe', ['Temperatursensor', f'{temp:.0f} °C'], a, hotE)
    eva_card(d, 475, 150, 330, 300, 'V', 'Verarbeitung', ['Motorsteuergerät', 'zu warm!' if t > 6.2 else 'prüft …'], a, hotV)
    eva_card(d, 880, 150, 330, 300, 'A', 'Ausgabe', ['Kühlerlüfter', 'läuft' if t > 8.8 else 'steht'], a, hotA)
    # Thermometer im E-Kasten
    tx, ty = 330, 200
    rrect(d, (tx - 10, ty, tx + 10, ty + 120), 10, None, a, outline=TXT, width=3, bg=CARD)
    circle(d, (tx, ty + 132), 18, RED, a, bg=CARD)
    lvl = ty + 112 - (temp - 70) / 40 * 100
    rect(d, (tx - 4, lvl, tx + 4, ty + 125), RED, a, bg=CARD)
    pulse_arrow(d, 405, 470, 300, PUR, t, a * 0.9, pr(t, 4.6, 5.0) * (1 - pr(t, 6.4, 6.8)))
    pulse_arrow(d, 810, 875, 300, ORA, t, a * 0.9, pr(t, 7.0, 7.4) * (1 - pr(t, 9.0, 9.4)))
    ang = max(0, t - 8.8) ** 1.6 * 160
    fan(d, (1130, 230), 55, ang, ORA, a, bg=CARD)
    caption(d, t, [(0.6, 5.0, 'Eingabe: Der Temperatursensor meldet die Kühlmitteltemperatur'),
                   (5.2, 8.6, 'Verarbeitung: Das Motorsteuergerät erkennt – zu warm!'),
                   (8.8, dur, 'Ausgabe: Der Kühlerlüfter läuft an')], PUR)


def eva_examples(d, t, dur):
    header(d, t, 'EVA-PRINZIP', 'Weitere Beispiele im Kfz', PUR)
    xs = [(90, 'E', 'Sensor'), (480, 'V', 'Steuergerät'), (870, 'A', 'Aktor')]
    ha = pr(t, 0.2, 0.8)
    for x, l, n in xs:
        text(d, x + 160, 128, l + '  ·  ' + n, 22, 'XB', EVA_COL[l], ha, 'mm')
    rows = [('Regensensor', 'Bordnetzsteuergerät', 'Wischermotor'),
            ('Raddrehzahlsensor', 'ABS-Steuergerät', 'Hydraulikventile'),
            ('Fahrpedalsensor', 'Motorsteuergerät', 'Drosselklappe')]
    for i, r in enumerate(rows):
        st = 1.0 + i * 2.2
        y = 170 + i * 120
        for j, (x, l, n) in enumerate(xs):
            a = pr(t, st + j * 0.4, st + j * 0.4 + 0.5)
            rrect(d, (x, y, x + 320, y + 84), 16, CARD, a)
            rect(d, (x, y + 14, x + 6, y + 70), EVA_COL[l], a, bg=CARD)
            text(d, x + 160, y + 42, r[j], 23, 'Bold', TXT, a, 'mm', bg=CARD)
            if j < 2:
                poly(d, [(x + 365, y + 42), (x + 345, y + 30), (x + 345, y + 54)], EVA_COL[xs[j + 1][1]], a)
    caption(d, t, [(7.6, dur, 'Immer gleich: Sensor → Steuergerät → Aktor')], PUR)


def chain(d, x, y, t, a, loop=0.0):
    for i, l in enumerate('EVA'):
        cx = x + i * 150
        circle(d, (cx, y), 40, EVA_COL[l], a)
        text(d, cx, y, l, 34, 'XB', BG, a, 'mm', bg=EVA_COL[l])
        if i < 2:
            poly(d, [(cx + 100, y), (cx + 80, y - 12), (cx + 80, y + 12)], MUTED, a)
            line(d, [(cx + 50, y), (cx + 84, y)], MUTED, 5, a)
    if loop > 0.01:
        pts = [(x + 300, y + 44), (x + 300, y + 100), (x, y + 100), (x, y + 52)]
        line(d, pts, PUR, 6, a * loop)
        poly(d, [(x, y + 46), (x - 12, y + 66), (x + 12, y + 66)], PUR, a * loop)
        text(d, x + 150, y + 126, 'Rückmeldung', 20, 'Bold', PUR, a * loop, 'mm')


def eva_regeln(d, t, dur):
    header(d, t, 'EVA-PRINZIP', 'Steuern oder Regeln?', PUR)
    a1 = pr(t, 0.3, 0.9)
    rrect(d, (80, 120, 610, 540), 22, CARD, a1)
    text(d, 345, 165, 'Steuern', 34, 'XB', TXT, a1, 'mm', bg=CARD)
    text(d, 345, 205, 'ohne Rückmeldung', 20, 'Med', MUTED, a1, 'mm', bg=CARD)
    chain(d, 195, 300, t, a1)
    text(d, 345, 470, 'z. B. Fensterheber', 22, 'Bold', TXT, a1, 'mm', bg=CARD)
    a2 = pr(t, 5.2, 5.8)
    rrect(d, (670, 120, 1200, 540), 22, CARD, a2)
    text(d, 935, 165, 'Regeln', 34, 'XB', TXT, a2, 'mm', bg=CARD)
    text(d, 935, 205, 'mit Rückmeldung (Istwert ↔ Sollwert)', 20, 'Med', MUTED, a2, 'mm', bg=CARD)
    chain(d, 785, 290, t, a2, pr(t, 6.0, 6.8))
    text(d, 935, 490, 'z. B. Lambda-Regelung', 22, 'Bold', TXT, a2, 'mm', bg=CARD)
    caption(d, t, [(0.6, 5.0, 'Steuern: ohne Rückmeldung'), (5.2, dur, 'Regeln: Die Rückmeldung wird ständig mit dem Sollwert verglichen')], PUR, y=600)


EVA_MERKE = merke_scene('EVA-PRINZIP', PUR, [
    'EVA = Eingabe – Verarbeitung – Ausgabe', 'Sensor → Steuergerät → Aktor\nSinnesorgan → Gehirn → Muskel',
    'Regeln = Steuern mit Rückmeldung', 'Fehlersuche: Liegt es an E, V oder A?'])


# =================== SENSOREN ===================
def sens_what(d, t, dur):
    header(d, t, 'SENSOREN', 'Was macht ein Sensor?', GRN)
    a = pr(t, 0.2, 0.8)
    temp = lerp(20, 90, pr(t, 2.0, 8.0))
    R = 2500 * math.exp(3400 * (1 / (temp + 273.15) - 1 / 293.15))
    U = 5 * R / (R + 2500)
    boxes = [(80, 'MESSGRÖSSE', 'Temperatur', f'{temp:.0f} °C', GRN), (480, 'SENSOR (NTC)', 'wandelt um', f'{R/1000:.2f} kΩ'.replace('.', ','), GRN),
             (880, 'SIGNAL ANS STEUERGERÄT', 'Spannung', f'{U:.2f} V'.replace('.', ','), PUR)]
    for i, (x, l, n, v, col) in enumerate(boxes):
        ai = pr(t, 0.4 + i * 0.6, 1.0 + i * 0.6)
        rrect(d, (x, 160, x + 320, 430), 20, CARD, ai)
        rect(d, (x + 14, 160, x + 306, 167), col, ai, bg=CARD)
        text(d, x + 24, 196, l, 15, 'Bold', MUTED, ai, 'lm', bg=CARD)
        text(d, x + 24, 240, n, 26, 'XB', TXT, ai, 'lm', bg=CARD)
        rrect(d, (x + 24, 300, x + 296, 390), 10, (196, 214, 190), ai, bg=CARD)
        text(d, x + 280, 345, v, 40, 'Bold', (25, 35, 28), ai, 'rm', bg=(196, 214, 190))
        if i < 2:
            pulse_arrow(d, x + 325, x + 475, 295, col if i == 0 else PUR, t, ai, pr(t, 2.0, 2.5))
    caption(d, t, [(0.6, 5.5, 'Ein Sensor wandelt eine physikalische Größe …'),
                   (5.7, dur, '… in ein elektrisches Signal für das Steuergerät um')], GRN)


SENS_VALUES = values_scene('SENSOREN', GRN, [], [
    ('Temperatur', 'Kühlmittel-Temperatursensor (NTC)'), ('Drehzahl', 'Kurbelwellen-, Raddrehzahlsensor'),
    ('Druck', 'Saugrohr-, Ladedrucksensor'), ('Position', 'Fahrpedal-, Drosselklappensensor'),
    ('Abgas', 'Lambdasonde (Restsauerstoff)')], title='Sensoren im Kfz', vsize=28)


def sens_ntc(d, t, dur):
    header(d, t, 'SENSOREN', 'Temperatursensor (NTC)', GRN)
    a = pr(t, 0.2, 0.8)
    X0, Y0, W_, H_ = 120, 130, 640, 380
    line(d, [(X0, Y0), (X0, Y0 + H_), (X0 + W_, Y0 + H_)], MUTED, 3, a)
    text(d, X0 - 14, Y0 + 8, '5 V', 18, 'Bold', MUTED, a, 'rm')
    text(d, X0 - 14, Y0 + H_, '0 V', 18, 'Bold', MUTED, a, 'rm')
    text(d, X0, Y0 + H_ + 26, '−20 °C', 18, 'Bold', MUTED, a, 'mm')
    text(d, X0 + W_, Y0 + H_ + 26, '120 °C', 18, 'Bold', MUTED, a, 'mm')
    U = lambda T: 5 * (lambda R: R / (R + 2500))(2500 * math.exp(3400 * (1 / (T + 273.15) - 1 / 293.15)))
    px = lambda T: X0 + (T + 20) / 140 * W_
    py = lambda u: Y0 + H_ - u / 5 * H_
    k = pr(t, 1.0, 9.0, clamp)
    Tn = -20 + 140 * k
    pts = [(px(T), py(U(T))) for T in [x * 2 - 20 for x in range(0, int((Tn + 20) / 2) + 1)]]
    if len(pts) > 1:
        line(d, pts, GRN, 6, a)
    if k > 0:
        circle(d, (px(Tn), py(U(Tn))), 12, GRN, a, outline=TXT, width=3)
    R = 2500 * math.exp(3400 * (1 / (Tn + 273.15) - 1 / 293.15))
    for i, (lab, val) in enumerate([('TEMPERATUR', f'{Tn:.0f} °C'), ('WIDERSTAND', (f'{R/1000:.1f} kΩ' if R >= 1000 else f'{R:.0f} Ω').replace('.', ',')),
                                    ('SIGNALSPANNUNG', f'{U(Tn):.2f} V'.replace('.', ','))]):
        y = 140 + i * 125
        text(d, 840, y, lab, 15, 'Bold', MUTED, a, 'lm')
        rrect(d, (840, y + 16, 1180, y + 96), 10, (196, 214, 190), a)
        text(d, 1164, y + 56, val, 40, 'Bold', (25, 35, 28), a, 'rm', bg=(196, 214, 190))
    caption(d, t, [(0.6, 6.4, 'NTC: wärmer → kleinerer Widerstand'),
                   (6.6, dur, 'Das Steuergerät sieht: Spannung sinkt → Motor wird warm')], GRN, y=612)


def sens_signals(d, t, dur):
    header(d, t, 'SENSOREN', 'Welche Signale liefern Sensoren?', GRN)
    panels = [('Analog', 'stufenlose Spannung', 'Temperatur-, Drucksensor'),
              ('Digital', 'nur an / aus (Rechteck)', 'Hallgeber'),
              ('Induktiv', 'Wechselspannung', 'Kurbelwellensensor')]
    for i, (ti, de, ex) in enumerate(panels):
        st = 0.5 + i * 2.6
        a = pr(t, st, st + 0.6)
        x = 70 + i * 390
        rrect(d, (x, 120, x + 360, 540), 20, CARD, a)
        text(d, x + 24, 160, ti, 30, 'XB', GRN, a, 'lm', bg=CARD)
        k = pr(t, st + 0.4, st + 2.6, clamp)
        gx0, gx1, gy = x + 24, x + 336, 330
        line(d, [(gx0, gy + 60), (gx1, gy + 60)], MUTED, 2, a, bg=CARD)
        pts = []
        n = int(80 * k)
        for j in range(n + 1):
            q = j / 80
            xx = gx0 + (gx1 - gx0) * q
            if i == 0:
                yy = gy + 40 - 80 * (0.5 - 0.5 * math.cos(math.pi * q)) * 0.9
            elif i == 1:
                yy = gy - 40 if (q * 4) % 1 < 0.5 else gy + 40
            else:
                yy = gy - math.sin(q * 2 * math.pi * 5) * 60 * (0.2 + 0.8 * q)
            pts.append((xx, yy))
        if i == 1 and len(pts) > 1:  # Rechteck mit senkrechten Flanken
            sq = [pts[0]]
            for p0, p1 in zip(pts, pts[1:]):
                if p0[1] != p1[1]:
                    sq.append((p1[0], p0[1]))
                sq.append(p1)
            pts = sq
        if len(pts) > 1:
            line(d, pts, GRN, 5, a, bg=CARD)
        text(d, x + 24, 450, de, 21, 'Bold', TXT, a, 'lm', bg=CARD)
        text(d, x + 24, 488, ex, 19, 'Med', MUTED, a, 'lm', bg=CARD)
    caption(d, t, [(8.4, dur, 'Analog, digital oder induktiv – je nach Sensor')], GRN, y=612)


SENS_MERKE = merke_scene('SENSOREN', GRN, [
    'Sensor = Eingabe im EVA-Prinzip', 'Physikalische Größe → elektrisches Signal',
    'NTC: wärmer → kleinerer Widerstand\nund niedrigere Signalspannung', 'Erst messen, dann tauschen'])


# =================== AKTOREN ===================
def gear(d, c, r, ang, col, a, bg=CARD):
    x, y = c
    for k in range(8):
        w = math.radians(ang + k * 45)
        p = [(x + (r + 12) * math.cos(w + s), y + (r + 12) * math.sin(w + s)) for s in (-0.18, 0.18)]
        p += [(x + (r - 2) * math.cos(w + 0.28), y + (r - 2) * math.sin(w + 0.28)), (x + (r - 2) * math.cos(w - 0.28), y + (r - 2) * math.sin(w - 0.28))]
        poly(d, [p[0], p[1], p[2], p[3]], col, a, bg)
    circle(d, c, r, col, a, bg=bg)
    circle(d, c, r * 0.4, bg, a, bg=bg)


def akt_what(d, t, dur):
    header(d, t, 'AKTOREN', 'Was macht ein Aktor?', ORA)
    items = [('Bewegung', 'Elektromotor, Magnetventil'), ('Wärme', 'Glühkerze, Sitzheizung'),
             ('Licht', 'LED, Kontrollleuchte'), ('Ton', 'Hupe, Warnsummer')]
    for i, (ti, ex) in enumerate(items):
        st = 0.5 + i * 1.4
        a = pr(t, st, st + 0.6)
        x = 60 + i * 295
        rrect(d, (x, 140, x + 270, 520), 20, CARD, a)
        c = (x + 135, 280)
        if i == 0:
            gear(d, c, 50, t * 60, ORA, a)
        elif i == 1:
            fl = 1 + 0.08 * math.sin(t * 9)
            poly(d, [(c[0], c[1] - 80 * fl), (c[0] + 50, c[1] + 10), (c[0] + 30, c[1] + 60), (c[0] - 30, c[1] + 60), (c[0] - 50, c[1] + 10)], ORA, a, CARD)
            poly(d, [(c[0], c[1] - 20), (c[0] + 22, c[1] + 30), (c[0], c[1] + 55), (c[0] - 22, c[1] + 30)], YEL, a, CARD)
        elif i == 2:
            on = 0.6 + 0.4 * math.sin(t * 4) ** 2
            for k in range(5, 0, -1):
                circle(d, c, 50 + k * 10, mix(YEL, 0.07 * (6 - k) * on, CARD), a, bg=CARD)
            circle(d, c, 50, YEL, a, bg=CARD)
        else:
            poly(d, [(c[0] - 60, c[1] - 25), (c[0] - 30, c[1] - 25), (c[0] + 5, c[1] - 60), (c[0] + 5, c[1] + 60), (c[0] - 30, c[1] + 25), (c[0] - 60, c[1] + 25)], ORA, a, CARD)
            for k in range(3):
                ph = (t * 1.5 + k / 3) % 1
                r0 = 30 + ph * 50
                d.arc((P(c[0] - r0 + 5), P(c[1] - r0), P(c[0] + r0 + 5), P(c[1] + r0)), -45, 45, fill=mix(ORA, a * (1 - ph), CARD), width=P(5))
        text(d, x + 135, 420, ti, 30, 'XB', ORA, a, 'mm', bg=CARD)
        text(d, x + 135, 465, ex, 18, 'Med', MUTED, a, 'mm', bg=CARD)
    caption(d, t, [(0.6, dur, 'Ein Aktor wandelt ein elektrisches Signal in Bewegung, Wärme, Licht oder Ton um')], ORA, y=612)


def akt_relais(d, t, dur):
    header(d, t, 'AKTOREN', 'Das Relais: klein steuert groß', ORA)
    a = pr(t, 0.1, 0.8)
    on = pr(t, 4.0, 4.4)
    flow = pr(t, 4.4, 4.8)
    # Relais-Kasten
    for x0 in range(440, 840, 24):
        line(d, [(x0, 150), (min(x0 + 12, 840), 150)], MUTED, 3, a)
        line(d, [(x0, 420), (min(x0 + 12, 840), 420)], MUTED, 3, a)
    for y0 in range(150, 420, 24):
        line(d, [(440, y0), (440, min(y0 + 12, 420))], MUTED, 3, a)
        line(d, [(840, y0), (840, min(y0 + 12, 420))], MUTED, 3, a)
    text(d, 640, 440, 'Relais', 20, 'Bold', MUTED, a, 'mt')
    # Steuerkreis: +12 V -> 85 -> Spule -> 86 -> Steuergeraet -> Masse
    st_path = [(110, 170), (520, 170), (520, 400), (520, 470), (330, 470)]
    line(d, [(110, 170), (520, 170), (520, 210)], WIRE, 5, a)
    line(d, [(520, 350), (520, 470), (330, 470)], WIRE, 5, a)
    text(d, 110, 150, '+12 V', 22, 'XB', RED, a, 'lm')
    text(d, 260, 200, 'Steuerstrom: klein', 18, 'Bold', MUTED, a, 'mm')
    rrect(d, (500, 210, 540, 350), 6, mix(ORA, 0.25 + 0.75 * on, CARD), a, outline=ORA, width=4)
    text(d, 520, 196, '85', 18, 'XB', TXT, a, 'mm')
    text(d, 494, 384, '86', 18, 'XB', TXT, a, 'rm')
    rrect(d, (150, 430, 330, 510), 12, CARD2, a, outline=PUR, width=3)
    text(d, 240, 458, 'Steuergerät', 18, 'Bold', TXT, a, 'mm', bg=CARD2)
    text(d, 240, 484, 'ein' if on > 0.5 else 'aus', 18, 'Bold', ORA if on > 0.5 else MUTED, a, 'mm', bg=CARD2)
    # Laststrom: +12 V -> 30 -> Kontakt -> 87 -> Luefter -> Masse
    line(d, [(1180, 170), (740, 170), (740, 210)], WIRE, 5, a)
    line(d, [(740, 350), (740, 480), (980, 480), (980, 400)], WIRE, 5, a)
    line(d, [(1040, 330), (1150, 330), (1150, 480)], WIRE, 5, a)
    line(d, [(1130, 480), (1170, 480)], MUTED, 4, a)
    line(d, [(1138, 490), (1162, 490)], MUTED, 4, a)
    text(d, 1180, 150, '+12 V', 22, 'XB', RED, a, 'rm')
    text(d, 960, 200, 'Laststrom: groß', 18, 'Bold', MUTED, a, 'mm')
    text(d, 740, 196, '30', 18, 'XB', TXT, a, 'mm')
    text(d, 770, 384, '87', 18, 'XB', TXT, a, 'lm')
    circle(d, (740, 210), 7, TXT, a)
    circle(d, (740, 350), 7, TXT, a)
    ang = math.radians(-28 * (1 - on))
    L = 136
    line(d, [(740, 210), (740 - L * math.sin(ang), 210 + L * math.cos(ang))], TXT, 7, a)
    if flow > 0.01:
        flow_dots(d, Path(st_path), t, 40, 60, 5, BLU, flow * a)
        flow_dots(d, Path([(1180, 170), (740, 170), (740, 480), (980, 480), (980, 330), (1150, 330), (1150, 480)]), t, 130, 30, 8, BLU, flow * a)
    spin = max(0, t - 4.6) ** 1.5 * 200
    fan(d, (980, 330), 62, spin, ORA, a)
    caption(d, t, [(0.6, 4.0, 'Das Steuergerät schaltet nur den kleinen Spulenstrom (85 → 86)'),
                   (4.2, 9.0, 'Die Spule zieht den Kontakt an: Großer Strom von 30 nach 87'),
                   (9.2, dur, 'Klein steuert groß – so werden Lüfter, Pumpen und Hupen geschaltet')], ORA, y=612)


def akt_pwm(d, t, dur):
    header(d, t, 'AKTOREN', 'PWM: stufenlos ansteuern', ORA)
    a = pr(t, 0.1, 0.8)
    duty = 0.2 if t < 4.5 else (0.2 + 0.6 * pr(t, 4.5, 7.5))
    X0, Y0 = 90, 200
    text(d, X0 - 20, Y0, 'an', 18, 'Bold', MUTED, a, 'rm')
    text(d, X0 - 20, Y0 + 160, 'aus', 18, 'Bold', MUTED, a, 'rm')
    line(d, [(X0, Y0 + 175), (X0 + 700, Y0 + 175)], MUTED, 2, a)
    pts = [(X0, Y0 + 160)]
    for i in range(6):
        x0 = X0 + i * 115
        x1 = x0 + 115 * duty
        pts += [(x0, Y0 + 160), (x0, Y0), (x1, Y0), (x1, Y0 + 160), (x0 + 115, Y0 + 160)]
    line(d, pts, ORA, 6, a)
    text(d, X0, 450, f'Tastverhältnis: {duty * 100:.0f} %', 34, 'XB', ORA, a, 'lm')
    rrect(d, (X0, 495, X0 + 690, 520), 12, CARD, a)
    rrect(d, (X0, 495, X0 + 690 * duty, 520), 12, ORA, a)
    spd = 0.4 + 9 * duty
    fan(d, (1030, 320), 130, t * spd * 60, ORA, a)
    text(d, 1030, 480, 'Kühlerlüfter', 20, 'Bold', MUTED, a, 'mm')
    caption(d, t, [(0.6, 4.4, 'PWM: Das Steuergerät schaltet sehr schnell ein und aus'),
                   (4.6, dur, 'Längere Einschaltzeit → mehr Leistung → der Lüfter dreht schneller')], ORA, y=612)


AKT_CHECK = values_scene('AKTOREN', ORA, [], [
    ('1', 'Aktortest mit dem Diagnosegerät'), ('2', 'Versorgung und Masse messen'),
    ('3', 'Wicklung spannungsfrei messen'), ('4', 'Ansteuerung: LED-Prüflampe oder Oszilloskop')],
    note='Keine Glühlampen-Prüflampe an Steuergeräte-Ausgängen!', title='Aktor prüfen – Schritt für Schritt', vsize=40)

AKT_MERKE = merke_scene('AKTOREN', ORA, [
    'Aktor = Ausgabe im EVA-Prinzip', 'Relais: klein steuert groß\n85/86 Spule, 30 → 87 Laststrom',
    'Ansteuerung über Plus, Masse oder PWM', 'Am Steuergerät nur LED-Prüflampe oder Oszi'])

VIDEOS_SENSORIK = {
    'eva': (PUR, [(title_scene('EVA', 'Das EVA-Prinzip', 'Eingabe – Verarbeitung – Ausgabe', PUR, size=70, kicker=KICK), 5.0),
                  (eva_human, 10.0), (eva_kfz, 13.5), (eva_examples, 10.5), (eva_regeln, 10.5), (EVA_MERKE, 7.5)]),
    'sensoren': (GRN, [(title_scene('S', 'Sensoren', 'Die Sinnesorgane des Fahrzeugs', GRN, kicker=KICK), 5.0),
                       (sens_what, 10.5), (SENS_VALUES, 10.0), (sens_ntc, 12.0), (sens_signals, 11.5), (SENS_MERKE, 7.5)]),
    'aktoren': (ORA, [(title_scene('A', 'Aktoren', 'Die Muskeln des Fahrzeugs', ORA, kicker=KICK), 5.0),
                      (akt_what, 9.0), (akt_relais, 13.5), (akt_pwm, 11.5), (AKT_CHECK, 9.0), (AKT_MERKE, 7.5)]),
}
