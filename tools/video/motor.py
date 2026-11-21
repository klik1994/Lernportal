"""Lernvideos zum Thema Motormanagement."""
import math
from engine import *
from scenes import title_scene, values_scene, merke_scene

TEA = (31, 200, 179)
KICK = 'MOTORMANAGEMENT  ·  LERNVIDEO'


def card(d, box, a, col=TEA):
    x0, y0, x1, y1 = box
    rrect(d, box, 18, CARD, a)
    rect(d, (x0 + 14, y0, x1 - 14, y0 + 7), col, a, bg=CARD)


def pulse(d, p0, p1, col, t, a, k=3, speed=1.2, r=6):
    for i in range(k):
        q = (t * speed + i / k) % 1
        circle(d, (lerp(p0[0], p1[0], q), lerp(p0[1], p1[1], q)), r, col, a)


# =================== AUFGABEN UND STEUERGERAET ===================
def mm_tasks(d, t, dur):
    header(d, t, 'MOTORMANAGEMENT', 'Wozu ein Motormanagement?', TEA)
    items = [('Leistung', 'den Fahrerwunsch umsetzen'), ('Verbrauch', 'so wenig wie möglich'),
             ('Abgas', 'Grenzwerte einhalten'), ('Schutz', 'Klopfen und Überhitzung vermeiden')]
    for i, (ti, de) in enumerate(items):
        st = 0.5 + i * 1.2
        a = pr(t, st, st + 0.6)
        x = 70 + (i % 2) * 580
        y = 130 + (i // 2) * 200 + (1 - eout((t - st) / 0.6)) * 20
        card(d, (x, y, x + 560, y + 170), a)
        text(d, x + 34, y + 70, ti, 40, 'XB', TEA, a, 'lm', bg=CARD)
        text(d, x + 34, y + 124, de, 24, 'Semi', TXT, a, 'lm', bg=CARD)
    caption(d, t, [(5.4, dur, 'Das Steuergerät sucht für jede Situation den besten Kompromiss')], TEA)


def mm_ecu(d, t, dur):
    header(d, t, 'MOTORMANAGEMENT', 'Das Motorsteuergerät im Überblick', TEA)
    a = pr(t, 0.1, 0.7)
    sens = ['Drehzahl', 'Last (Luftmasse)', 'Fahrpedal', 'Temperatur', 'Lambdasonde', 'Klopfsensor']
    akt = ['Einspritzventile', 'Zündspulen', 'Drosselklappe', 'Kraftstoffpumpe', 'Ladedruck', 'AGR-Ventil']
    rrect(d, (500, 200, 780, 470), 24, CARD2, a, outline=PUR, width=4)
    text(d, 640, 300, 'Motor-', 34, 'XB', TXT, a, 'mm', bg=CARD2)
    text(d, 640, 345, 'steuergerät', 34, 'XB', TXT, a, 'mm', bg=CARD2)
    text(d, 640, 410, 'Kennfelder · Regelungen', 18, 'Semi', MUTED, a, 'mm', bg=CARD2)
    text(d, 230, 128, 'SENSOREN', 18, 'Bold', GRN, a, 'mm')
    text(d, 1050, 128, 'AKTOREN', 18, 'Bold', ORA, a, 'mm')
    for i, s in enumerate(sens):
        st = 0.8 + i * 0.6
        ai = pr(t, st, st + 0.4)
        y = 160 + i * 64
        rrect(d, (90, y, 370, y + 48), 12, CARD, ai)
        rect(d, (90, y + 10, 96, y + 38), GRN, ai, bg=CARD)
        text(d, 112, y + 24, s, 21, 'Bold', TXT, ai, 'lm', bg=CARD)
        if t > st + 0.4:
            pulse(d, (372, y + 24), (498, 335), GRN, t + i * 0.2, ai * 0.9, k=2, speed=0.8, r=5)
    for i, s in enumerate(akt):
        st = 5.4 + i * 0.6
        ai = pr(t, st, st + 0.4)
        y = 160 + i * 64
        rrect(d, (910, y, 1190, y + 48), 12, CARD, ai)
        rect(d, (910, y + 10, 916, y + 38), ORA, ai, bg=CARD)
        text(d, 932, y + 24, s, 21, 'Bold', TXT, ai, 'lm', bg=CARD)
        if t > st + 0.4:
            pulse(d, (782, 335), (908, y + 24), ORA, t + i * 0.2, ai * 0.9, k=2, speed=0.8, r=5)
    caption(d, t, [(0.6, 5.2, 'Eingabe: viele Sensoren melden den Zustand des Motors'),
                   (5.4, 9.4, 'Ausgabe: das Steuergerät steuert die Aktoren an'),
                   (9.6, dur, 'Das EVA-Prinzip – mit sehr vielen Ein- und Ausgängen')], TEA)


N_ = [800, 1600, 2400, 3200, 4000, 4800, 5600, 6400]
L_ = [10, 20, 30, 40, 55, 70, 85, 100]


def zw(fi, fj):
    return max(4, min(40, 10 + 30 * fi - 16 * fj))


def hsl(h, s, l):
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


def mm_kennfeld(d, t, dur):
    header(d, t, 'MOTORMANAGEMENT', 'Das Kennfeld', TEA)
    a = pr(t, 0.1, 0.8)
    X0, Y0, CW, CH = 150, 120, 66, 50
    for j in range(8):
        text(d, X0 - 12, Y0 + (7 - j) * CH + CH / 2, f'{L_[j]} %', 15, 'Bold', MUTED, a, 'rm')
        for i in range(8):
            v = zw(i / 7, j / 7)
            k = (v - 4) / 36
            col = hsl(200 - 170 * k, 0.7, 0.62 - 0.06 * k)
            ai = a * pr(t, 0.3 + (i + j) * 0.05, 0.6 + (i + j) * 0.05)
            x, y = X0 + i * CW, Y0 + (7 - j) * CH
            rrect(d, (x + 2, y + 2, x + CW - 2, y + CH - 2), 5, col, ai)
            text(d, x + CW / 2, y + CH / 2, f'{v:.0f}°', 16, 'Bold', (14, 25, 43), ai, 'mm', bg=col)
    for i in range(8):
        text(d, X0 + i * CW + CW / 2, Y0 + 8 * CH + 18, str(N_[i]), 15, 'Bold', MUTED, a, 'mm')
    text(d, X0 + 4 * CW, Y0 + 8 * CH + 44, 'Drehzahl in 1/min', 16, 'Bold', MUTED, a, 'mm')
    text(d, X0 - 60, Y0 - 16, 'Last', 16, 'Bold', MUTED, a, 'lm')
    # Punkt bewegt sich ueber das Kennfeld
    q = pr(t, 2.5, 10.5, clamp)
    fi = 0.15 + 0.7 * q
    fj = 0.25 + 0.55 * math.sin(q * math.pi)
    px, py = X0 + fi * 7 * CW + CW / 2, Y0 + (7 - fj * 7) * CH + CH / 2
    if q > 0:
        circle(d, (px, py), 16, None, a, outline=TXT, width=5)
    n = 800 + fi * 5600
    l = 10 + fj * 90
    v = zw(fi, fj)
    for k, (lab, val) in enumerate([('DREHZAHL', f'{n:.0f} 1/min'), ('LAST', f'{l:.0f} %'), ('ZÜNDZEITPUNKT', f'{v:.0f}° vor OT')]):
        y = 140 + k * 120
        text(d, 760, y, lab, 15, 'Bold', MUTED, a, 'lm')
        rrect(d, (760, y + 16, 1150, y + 92), 10, (196, 214, 190), a)
        text(d, 1134, y + 54, val, 38, 'Bold', (25, 35, 28), a, 'rm', bg=(196, 214, 190))
    caption(d, t, [(0.6, 6.0, 'Ein Kennfeld ist eine Tabelle im Steuergerät'),
                   (6.2, dur, 'Für jede Drehzahl und Last steht der passende Wert drin')], TEA, y=618)


MM_NOTLAUF = values_scene('MOTORMANAGEMENT', TEA, [], [
    ('1', 'Das Steuergerät erkennt einen unplausiblen Wert'), ('2', 'Es rechnet mit einem Ersatzwert weiter (Notlauf)'),
    ('3', 'Eintrag im Fehlerspeicher, ggf. Motorkontrollleuchte')],
    note='Der Fehlerspeicher zeigt, wo es hakt – erst prüfen, dann tauschen', title='Wenn ein Sensor ausfällt', vsize=40)

MM_A_MERKE = merke_scene('MOTORMANAGEMENT', TEA, [
    'Aufgaben: Leistung, Verbrauch, Abgas, Schutz', 'Drehzahl + Last → Kennfeld → Grundwert\nandere Sensoren korrigieren',
    'Ausgänge: Einspritzung, Zündung, Drosselklappe …', 'Fehler: Ersatzwert, Notlauf, Fehlerspeicher'])


# =================== LAMBDA ===================
def lam_mix(d, t, dur):
    header(d, t, 'LAMBDA', 'Die ideale Mischung beim Benziner', TEA)
    text(d, 90, 170, '14,7 kg Luft', 30, 'XB', TEA, pr(t, 0.3, 0.9), 'lm')
    for i in range(15):
        st = 0.8 + i * 0.25
        a = pr(t, st, st + 0.3)
        w = 56 if i < 14 else 39
        x = 90 + i * 72
        rrect(d, (x, 200, x + w, 256), 10, BLU, a)
    a2 = pr(t, 5.0, 5.6)
    text(d, 90, 330, '1 kg Benzin', 30, 'XB', ORA, a2, 'lm')
    rrect(d, (90, 360, 146, 416), 10, ORA, a2)
    a3 = pr(t, 6.2, 6.8)
    text(d, 640, 500, 'stöchiometrisch: λ = 1', 40, 'XB', TXT, a3, 'mm')
    caption(d, t, [(0.6, 6.0, 'Für 1 kg Benzin braucht der Motor 14,7 kg Luft'),
                   (6.2, dur, 'Das sind rund 9.000 Liter Luft für einen Liter Benzin')], TEA, y=612)


def lam_scale(d, t, dur):
    header(d, t, 'LAMBDA', 'Fett, ideal oder mager?', TEA)
    a = pr(t, 0.1, 0.7)
    X0, X1, Y = 120, 1160, 230
    LO, HI = 0.6, 1.5
    stops = [(0.6, (138, 75, 47)), (0.87, RED), (0.99, YEL), (1.0, GRN), (1.01, GRN), (1.02, BLU), (1.25, (108, 127, 216)), (1.5, (138, 115, 201))]
    for px in range(X0, X1, 4):
        l = LO + (px - X0) / (X1 - X0) * (HI - LO)
        for (l0, c0), (l1, c1) in zip(stops, stops[1:]):
            if l0 <= l <= l1:
                k = (l - l0) / (l1 - l0) if l1 > l0 else 0
                c = tuple(int(lerp(c0[i], c1[i], k)) for i in range(3))
                break
        rect(d, (px, Y, px + 4, Y + 60), c, a)
    for v in (0.6, 0.8, 1.0, 1.2, 1.5):
        x = X0 + (v - LO) / (HI - LO) * (X1 - X0)
        text(d, x, Y + 86, f'{v:.1f}'.replace('.', ','), 20, 'Bold', MUTED, a, 'mm')
    # Marker: 1,0 -> 0,75 -> 1,3 -> 1,0
    if t < 3:
        l = 1.0
    elif t < 6:
        l = lerp(1.0, 0.75, ease((t - 3) / 3))
    elif t < 10:
        l = lerp(0.75, 1.3, ease((t - 6) / 4))
    else:
        l = lerp(1.3, 1.0, ease((t - 10) / 2.5))
    x = X0 + (l - LO) / (HI - LO) * (X1 - X0)
    poly(d, [(x, Y - 6), (x - 16, Y - 32), (x + 16, Y - 32)], TXT, a)
    line(d, [(x, Y - 6), (x, Y + 66)], TXT, 4, a)
    text(d, x, Y - 56, f'λ = {l:.2f}'.replace('.', ','), 30, 'XB', TXT, a, 'mm')
    if l < 0.97:
        z, c, tx = 'fett (Luftmangel)', RED, 'mehr Leistung – aber mehr Verbrauch, CO und HC'
    elif l <= 1.03:
        z, c, tx = 'λ = 1 – ideal', GRN, 'der Kat baut CO, HC und NOx gleichzeitig ab'
    else:
        z, c, tx = 'mager (Luftüberschuss)', BLU, 'weniger Verbrauch – aber mehr NOx'
    rrect(d, (240, 380, 1040, 520), 18, CARD, a)
    text(d, 640, 425, z, 34, 'XB', c, a, 'mm', bg=CARD)
    text(d, 640, 478, tx, 24, 'Semi', TXT, a, 'mm', bg=CARD)
    caption(d, t, [(0.6, dur, 'λ = tatsächliche Luftmenge : benötigte Luftmenge')], TEA, y=612)


LAM_VALUES = values_scene('LAMBDA', TEA, [], [
    ('ca. 0,85–0,95', 'höchste Leistung, mehr Verbrauch'), ('λ = 1', 'Katalysator arbeitet optimal'),
    ('ca. 1,05–1,1', 'geringster Verbrauch, mehr NOx'), ('über ca. 1,3', 'zu mager: Zündaussetzer')],
    note='Richtwerte für Ottomotoren', title='Was passiert bei welchem Lambda?', vsize=26)


def lam_od(d, t, dur):
    header(d, t, 'LAMBDA', 'Ottomotor und Diesel', TEA)
    for i, (ti, l, lines) in enumerate([('Ottomotor', 'meist λ = 1', ['wegen des Katalysators', 'Volllast: etwas fett']),
                                        ('Diesel', 'immer λ > 1', ['Luftüberschuss', 'Leistung über die Einspritzmenge'])]):
        st = 0.4 + i * 2.5
        a = pr(t, st, st + 0.6)
        x = 80 + i * 580
        card(d, (x, 130, x + 540, 520), a)
        text(d, x + 270, 200, ti, 38, 'XB', TXT, a, 'mm', bg=CARD)
        text(d, x + 270, 290, l, 50, 'XB', TEA, a, 'mm', bg=CARD)
        for k, s in enumerate(lines):
            text(d, x + 270, 390 + k * 46, s, 24, 'Semi', MUTED, a, 'mm', bg=CARD)
    caption(d, t, [(5.6, dur, 'Richtwerte: Diesel bei Volllast ca. λ 1,2–1,4')], TEA, y=612)


LAM_MERKE = merke_scene('LAMBDA', TEA, [
    '14,7 kg Luft : 1 kg Benzin = λ 1', 'λ < 1 fett · λ > 1 mager',
    'Ottomotor meist λ = 1 – wegen des Kats', 'Diesel immer λ > 1'])


# =================== BETRIEBSZUSTAENDE ===================
PH = [  # (Name, Dauer-Anteil, Drehzahl Start, Drehzahl Ende, Einspritzung, Lambda)
    ('Kaltstart', 0.14, 1200, 780, True, 'λ < 1'),
    ('Leerlauf', 0.12, 780, 780, True, 'λ = 1'),
    ('Beschleunigen', 0.12, 780, 2600, True, 'kurz < 1'),
    ('Teillast', 0.16, 2600, 2600, True, 'λ = 1'),
    ('Volllast', 0.16, 2600, 5500, True, 'ca. 0,9'),
    ('Schub', 0.30, 5500, 1250, False, 'nur Luft'),
]


def bz_drive(d, t, dur):
    header(d, t, 'BETRIEBSZUSTÄNDE', 'Eine Fahrt', TEA)
    a = pr(t, 0.1, 0.7)
    X0, X1, Y0, Y1 = 120, 1180, 150, 430
    line(d, [(X0, Y0 - 10), (X0, Y1), (X1, Y1)], MUTED, 3, a)
    for rpm in (1000, 3000, 5000):
        y = Y1 - rpm / 6000 * (Y1 - Y0)
        text(d, X0 - 12, y, f'{rpm}', 15, 'Bold', MUTED, a, 'rm')
    text(d, X0 - 12, Y0 - 4, '1/min', 15, 'Bold', MUTED, a, 'rm')
    T0, T1 = 1.0, dur - 2.0
    prog = clamp((t - T0) / (T1 - T0))
    xs = X0
    pts = []
    cur = None
    acc = 0
    for name, w, n0, n1, inj, lam in PH:
        xa, xb = X0 + acc * (X1 - X0), X0 + (acc + w) * (X1 - X0)
        text(d, (xa + xb) / 2, Y0 - 50 + (14 if name == 'Beschleunigen' else 0), name, 17, 'Bold', TEA if prog >= acc else MUTED, a, 'mm')
        line(d, [(xb, Y0 - 30), (xb, Y1)], CARD2, 2, a)
        steps = 20
        for s in range(steps + 1):
            q = s / steps
            g = acc + w * q
            if g > prog:
                break
            if name == 'Schub':
                n = n1 + (n0 - n1) * (1 - q) ** 1.3
            else:
                n = lerp(n0, n1, ease(q))
            pts.append((xa + (xb - xa) * q, Y1 - n / 6000 * (Y1 - Y0)))
            cur = (name, inj, lam, n)
        # Einspritzbalken
        if prog > acc:
            k = clamp((prog - acc) / w)
            col = GRN if inj else RED
            rrect(d, (xa + 2, Y1 + 24, xa + 2 + (xb - xa - 4) * k, Y1 + 44), 8, col, a)
        acc += w
    text(d, X0 - 12, Y1 + 34, 'Einspr.', 14, 'Bold', MUTED, a, 'rm')
    if len(pts) > 1:
        line(d, pts, TEA, 6, a)
        circle(d, pts[-1], 10, TEA, a, outline=TXT, width=3)
    if cur:
        name, inj, lam, n = cur
        rrect(d, (290, 500, 990, 560), 14, CARD, a)
        text(d, 315, 530, f'{n:.0f} 1/min', 22, 'Bold', TXT, a, 'lm', bg=CARD)
        text(d, 600, 530, 'Lambda: ' + lam, 22, 'Bold', TEA, a, 'mm', bg=CARD)
        text(d, 965, 530, 'Einspritzung ' + ('AN' if inj else 'AUS'), 22, 'Bold', GRN if inj else RED, a, 'rm', bg=CARD)
    caps = []
    acc = 0
    texts = {'Kaltstart': 'Kaltstart: mehr Kraftstoff, höhere Leerlaufdrehzahl', 'Leerlauf': 'Leerlauf: die Drehzahl wird geregelt',
             'Beschleunigen': 'Beschleunigen: kurz mehr Kraftstoff', 'Teillast': 'Teillast: λ = 1, sparsam',
             'Volllast': 'Volllast: leicht fett, höchste Leistung', 'Schub': 'Schub: Einspritzung aus – 0 l/100 km'}
    for name, w, *_ in PH:
        st = T0 + acc * (T1 - T0)
        en = T0 + (acc + w) * (T1 - T0)
        caps.append((st + 0.1, en if name != 'Schub' else dur, texts[name]))
        acc += w
    caption(d, t, caps, TEA, y=640)


BZ_VALUES = values_scene('BETRIEBSZUSTÄNDE', TEA, [], [
    ('Kaltstart', 'mehr Kraftstoff, höhere Leerlaufdrehzahl'), ('Leerlauf', 'Drehzahl wird geregelt'),
    ('Teillast', 'λ = 1 – sparsam und sauber'), ('Volllast', 'leicht fett – höchste Leistung'),
    ('Schub', 'Einspritzung aus')], title='Was das Steuergerät macht', vsize=28)


def bz_schub(d, t, dur):
    header(d, t, 'BETRIEBSZUSTÄNDE', 'Schubabschaltung', TEA)
    a = pr(t, 0.1, 0.7)
    n = 3000 if t < 1.5 else max(900, 3000 - (t - 1.5) * 260)
    inj = not (1.5 <= t and n > 1300)
    # Drehzahlmesser
    cx, cy, R = 360, 330, 170
    for k in range(0, 61, 5):
        ang = math.radians(150 + k * 4)
        r0 = R - (20 if k % 10 == 0 else 10)
        line(d, [(cx + r0 * math.cos(ang), cy + r0 * math.sin(ang)), (cx + R * math.cos(ang), cy + R * math.sin(ang))], MUTED, 3, a)
        if k % 10 == 0:
            text(d, cx + (R - 44) * math.cos(ang), cy + (R - 44) * math.sin(ang), str(k // 10), 20, 'Bold', TXT, a, 'mm')
    ang = math.radians(150 + n / 100 * 4)
    line(d, [(cx, cy), (cx + (R - 30) * math.cos(ang), cy + (R - 30) * math.sin(ang))], RED, 7, a)
    circle(d, (cx, cy), 14, TXT, a)
    text(d, cx, cy + 90, 'x 1000 1/min', 18, 'Bold', MUTED, a, 'mm')
    # Wiedereinsetzdrehzahl markieren
    ang2 = math.radians(150 + 13 * 4)
    circle(d, (cx + (R + 14) * math.cos(ang2), cy + (R + 14) * math.sin(ang2)), 8, TEA, a)
    rrect(d, (640, 170, 1180, 280), 18, CARD, a)
    text(d, 670, 225, 'Einspritzung', 28, 'Bold', TXT, a, 'lm', bg=CARD)
    rrect(d, (980, 200, 1150, 250), 25, GRN if inj else RED, a, bg=CARD)
    text(d, 1065, 225, 'AN' if inj else 'AUS', 26, 'XB', BG, a, 'mm', bg=GRN if inj else RED)
    rrect(d, (640, 300, 1180, 410), 18, CARD, a)
    text(d, 670, 355, 'Verbrauch', 28, 'Bold', TXT, a, 'lm', bg=CARD)
    text(d, 1150, 355, '0,0 l/100 km' if not inj else ('7,5 l/100 km' if t < 1.5 else '0,8 l/h'), 30, 'XB', TEA, a, 'rm', bg=CARD)
    text(d, 910, 450, 'Wiedereinsetzdrehzahl ca. 1.300 1/min (Richtwert)', 18, 'Semi', MUTED, a, 'mm')
    caption(d, t, [(0.4, 1.5, 'Fahren mit Gas'), (1.6, 7.6, 'Fuß vom Gas, Gang drin: Einspritzung aus'),
                   (7.8, dur, 'Unter der Wiedereinsetzdrehzahl: Einspritzung wieder an')], TEA, y=612)


BZ_MERKE = merke_scene('BETRIEBSZUSTÄNDE', TEA, [
    'Kaltstart: Anreicherung', 'Leerlauf: Drehzahl wird geregelt',
    'Teillast λ = 1 · Volllast leicht fett', 'Schub: Einspritzung aus'])


VIDEOS_MOTOR = {
    'mm-aufgaben': (TEA, [(title_scene('MM', 'Motormanagement', 'Aufgaben und Steuergerät', TEA, size=84, kicker=KICK), 5.0),
                          (mm_tasks, 8.5), (mm_ecu, 13.0), (mm_kennfeld, 12.0), (MM_NOTLAUF, 8.0), (MM_A_MERKE, 7.5)]),
    'mm-lambda': (TEA, [(title_scene('λ', 'Luftverhältnis Lambda', 'Die richtige Mischung aus Luft und Kraftstoff', TEA, kicker=KICK), 5.0),
                        (lam_mix, 10.0), (lam_scale, 13.0), (LAM_VALUES, 9.0), (lam_od, 9.0), (LAM_MERKE, 7.5)]),
    'mm-betrieb': (TEA, [(title_scene('n', 'Betriebszustände', 'Was das Steuergerät in jeder Situation anders macht', TEA, kicker=KICK), 5.0),
                         (bz_drive, 20.0), (BZ_VALUES, 10.0), (bz_schub, 11.5), (BZ_MERKE, 7.5)]),
}


# =================== GEMISCHBILDUNG OTTO ===================
ROY = (91, 140, 255)
KICK2 = 'GEMISCHBILDUNG OTTO  ·  LERNVIDEO'


def kette_boxes(d, t, items, y, h, col, a_start=0.4, step=0.5, flow=True, hd=()):
    n = len(items)
    gap = 40
    w = (1100 - gap * (n - 1)) / n
    xs = []
    for i, (ti, sub) in enumerate(items):
        x = 90 + i * (w + gap)
        xs.append(x)
        a = pr(t, a_start + i * step, a_start + i * step + 0.5)
        c = RED if i in hd else col
        rrect(d, (x, y, x + w, y + h), 16, CARD, a)
        rect(d, (x + 12, y, x + w - 12, y + 6), c, a, bg=CARD)
        text(d, x + w / 2, y + h / 2 - (14 if sub else 0), ti, 22, 'Bold', TXT, a, 'mm', bg=CARD)
        if sub:
            text(d, x + w / 2, y + h / 2 + 20, sub, 17, 'Semi', c if i in hd else MUTED, a, 'mm', bg=CARD)
        if i and flow:
            ap = pr(t, a_start + i * step, a_start + i * step + 0.5)
            x0 = x - gap + 4
            poly(d, [(x - 4, y + h / 2), (x - 16, y + h / 2 - 9), (x - 16, y + h / 2 + 9)], c, ap)
            if t > a_start + n * step:
                pulse(d, (x0, y + h / 2), (x - 18, y + h / 2), c, t, ap, k=2, speed=1.5, r=4)
    return xs, w


def gk_saug(d, t, dur):
    header(d, t, 'KRAFTSTOFFSYSTEM', 'Saugrohreinspritzung', ROY)
    kette_boxes(d, t, [('Tank', ''), ('Pumpe', 'im Tank'), ('Filter', ''), ('Rail', 'ca. 3–5 bar'), ('Einspritz-', 'ventile')], 230, 130, ROY)
    caption(d, t, [(0.6, 5.5, 'Die Pumpe im Tank erzeugt den Druck'), (5.7, dur, 'Eingespritzt wird vor das Einlassventil')], ROY)


def gk_direkt(d, t, dur):
    header(d, t, 'KRAFTSTOFFSYSTEM', 'Direkteinspritzung', ROY)
    kette_boxes(d, t, [('Tank', ''), ('Pumpe', 'ca. 4–6 bar'), ('Hochdruck-', 'pumpe'), ('Rail', 'ca. 200–350 bar'), ('Einspritz-', 'ventile')], 230, 130, ROY, hd=(2, 3, 4))
    caption(d, t, [(0.6, 5.5, 'Die Hochdruckpumpe wird von der Nockenwelle angetrieben'),
                   (5.7, dur, 'Eingespritzt wird direkt in den Brennraum – Richtwerte')], ROY)


GK_DRUCK = values_scene('KRAFTSTOFFSYSTEM', ROY, [], [
    ('ca. 3–5 bar', 'Saugrohreinspritzung'), ('ca. 4–6 bar', 'Direkteinspritzung, Niederdruck'),
    ('ca. 200–350 bar', 'Direkteinspritzung, Hochdruck'), ('über 2.000 bar', 'zum Vergleich: Diesel Common-Rail')],
    note='Richtwerte – vor dem Öffnen immer Druck abbauen!', title='Typische Drücke', vsize=26)


def gk_tank(d, t, dur):
    header(d, t, 'KRAFTSTOFFSYSTEM', 'Tankentlüftung', ROY)
    kette_boxes(d, t, [('Tank', 'Dämpfe'), ('Aktivkohle-', 'behälter'), ('Tankentlüftungs-', 'ventil'), ('Saugrohr', 'verbrannt')], 230, 130, GRN)
    caption(d, t, [(0.6, dur, 'Kraftstoffdämpfe kommen nicht in die Umwelt – sie werden verbrannt')], ROY)


GK_MERKE = merke_scene('KRAFTSTOFFSYSTEM', ROY, [
    'Tank → Pumpe → Filter → Rail → Einspritzventile', 'Direkteinspritzung: Hochdruckpumpe\nRichtwert ca. 200–350 bar',
    'Tankentlüftung: Dämpfe werden verbrannt', 'Vor dem Öffnen: Druck abbauen!'])


def zylinder(d, x, t, direkt, a):
    # Zylinder mit Kolben, Einlasskanal, Einspritzventil und Spruehstrahl
    line(d, [(x, 470), (x, 260), (x + 220, 260), (x + 220, 470)], TXT, 5, a)
    kol = 400 + 30 * math.sin(t * 2.5)
    rrect(d, (x + 10, kol, x + 210, kol + 60), 8, CARD2, a, outline=MUTED, width=3)
    line(d, [(x - 140, 190), (x + 40, 190), (x + 70, 258)], MUTED, 4, a)
    line(d, [(x - 140, 235), (x + 20, 235), (x + 45, 258)], MUTED, 4, a)
    text(d, x - 130, 170, 'Saugrohr', 17, 'Bold', MUTED, a, 'lm')
    puls = (t * 1.2) % 1 < 0.35
    if direkt:
        rrect(d, (x + 98, 200, x + 122, 262), 4, ROY, a)
        if puls:
            poly(d, [(x + 110, 264), (x + 70, 340), (x + 150, 340)], mix(ROY, 0.6), a)
    else:
        rrect(d, (x - 40, 140, x - 16, 196), 4, ROY, a)
        if puls:
            poly(d, [(x - 22, 198), (x + 40, 225), (x + 20, 240)], mix(ROY, 0.6), a)


def ge_zyl(d, t, dur):
    header(d, t, 'EINSPRITZUNG', 'Wo wird eingespritzt?', ROY)
    a1 = pr(t, 0.3, 0.9)
    a2 = pr(t, 5.2, 5.8)
    zylinder(d, 260, t, False, a1)
    zylinder(d, 900, t, True, a2)
    text(d, 370, 520, 'Saugrohreinspritzung', 26, 'XB', TXT, a1, 'mm')
    text(d, 1010, 520, 'Direkteinspritzung', 26, 'XB', TXT, a2, 'mm')
    caption(d, t, [(0.6, 5.0, 'Saugrohr: vor das Einlassventil'), (5.2, dur, 'Direkt: in den Brennraum – unter hohem Druck')], ROY, y=612)


def ge_ventil(d, t, dur):
    header(d, t, 'EINSPRITZUNG', 'So arbeitet ein Einspritzventil', ROY)
    a = pr(t, 0.2, 0.8)
    cyc = (t % 2.0) < 0.9 and t > 2
    x = 420
    rrect(d, (x - 70, 130, x + 70, 470), 16, CARD2, a, outline=MUTED, width=3)
    rrect(d, (x - 55, 180, x + 55, 300), 8, mix(ORA, 0.9 if cyc else 0.25, CARD2), a, outline=ORA, width=4, bg=CARD2)
    text(d, x, 240, 'Spule', 22, 'Bold', BG if cyc else ORA, a, 'mm', bg=mix(ORA, 0.9 if cyc else 0.25, CARD2))
    lift = 18 if cyc else 0
    rrect(d, (x - 10, 310 - lift, x + 10, 470 - lift), 6, TXT, a, bg=CARD2)
    poly(d, [(x - 16, 470), (x + 16, 470), (x + 8, 495), (x - 8, 495)], MUTED, a)
    if cyc:
        poly(d, [(x, 497), (x - 50, 560), (x + 50, 560)], mix(ROY, 0.7), a)
    rrect(d, (700, 200, 1180, 300), 16, CARD, a)
    text(d, 730, 250, 'Spannung', 28, 'Bold', TXT, a, 'lm', bg=CARD)
    rrect(d, (1000, 225, 1150, 275), 25, GRN if cyc else CARD2, a, bg=CARD)
    text(d, 1075, 250, 'AN' if cyc else 'AUS', 24, 'XB', BG if cyc else MUTED, a, 'mm', bg=GRN if cyc else CARD2)
    rrect(d, (700, 320, 1180, 420), 16, CARD, a)
    text(d, 730, 370, 'Nadel', 28, 'Bold', TXT, a, 'lm', bg=CARD)
    text(d, 1150, 370, 'offen' if cyc else 'zu', 28, 'XB', ROY if cyc else MUTED, a, 'rm', bg=CARD)
    caption(d, t, [(0.6, 6.0, 'Spannung an: Die Spule zieht die Nadel hoch – der Kraftstoff spritzt'),
                   (6.2, dur, 'Spannung aus: Die Feder drückt die Nadel zu')], ROY, y=618)


def ge_ti(d, t, dur):
    header(d, t, 'EINSPRITZUNG', 'Die Einspritzzeit bestimmt die Menge', ROY)
    a = pr(t, 0.2, 0.8)
    ti = 2 + 6 * pr(t, 1.5, 7.5)
    rrect(d, (120, 200, 1160, 250), 25, CARD, a)
    rrect(d, (120, 200, 120 + 1040 * ti / 10, 250), 25, ROY, a)
    text(d, 120, 170, f'Einspritzzeit: {ti:.1f} ms'.replace('.', ','), 30, 'XB', ROY, a, 'lm')
    rrect(d, (420, 310, 860, 420), 14, (196, 214, 190), a)
    text(d, 840, 365, f'ca. {ti * 4:.0f} mg', 50, 'Bold', (25, 35, 28), a, 'rm', bg=(196, 214, 190))
    text(d, 640, 450, 'Beispielwerte', 18, 'Med', MUTED, a, 'mm')
    caption(d, t, [(0.6, dur, 'Doppelte Einspritzzeit = doppelte Menge (bei gleichem Druck)')], ROY, y=612)


GE_MERKE = merke_scene('EINSPRITZUNG', ROY, [
    'Saugrohr: vor das Einlassventil', 'Direkt: in den Brennraum, Hochdruck',
    'Menge über die Einspritzzeit', 'Hochdruck-Ventile: ca. 65 V – keine Prüflampe'])


def gl_gas(d, t, dur):
    header(d, t, 'LUFT UND LAST', 'Erst die Luft, dann der Kraftstoff', ROY)
    a = pr(t, 0.2, 0.8)
    p = 0.1 + 0.85 * pr(t, 2.0, 9.0)
    rect(d, (80, 230, 700, 350), CARD2, a)
    line(d, [(80, 228), (700, 228)], TXT, 4, a)
    line(d, [(80, 352), (700, 352)], TXT, 4, a)
    flow_dots(d, Path([(80, 290), (700, 290)]), t, 40 + 300 * p, 44, 7, (207, 230, 255), a, bg=CARD2)
    ang = math.radians(8 + 80 * p)
    cx, cy = 390, 290
    L = 56
    line(d, [(cx - L * math.sin(ang), cy - L * math.cos(ang)), (cx + L * math.sin(ang), cy + L * math.cos(ang))], ROY, 10, a, bg=CARD2)
    circle(d, (cx, cy), 7, TXT, a, bg=CARD2)
    text(d, 390, 390, 'Drosselklappe', 20, 'Bold', MUTED, a, 'mm')
    text(d, 80, 180, f'Gaspedal: {p * 100:.0f} %', 30, 'XB', ROY, a, 'lm')
    lm = 12 + 210 * p
    for k, (lab, val) in enumerate([('LUFTMASSE', f'{lm:.0f} kg/h'), ('KRAFTSTOFF FÜR λ = 1', f'{lm / 14.7:.1f} kg/h'.replace('.', ','))]):
        y = 190 + k * 130
        text(d, 780, y, lab, 15, 'Bold', MUTED, a, 'lm')
        rrect(d, (780, y + 16, 1180, y + 96), 10, (196, 214, 190), a)
        text(d, 1164, y + 56, val, 40, 'Bold', (25, 35, 28), a, 'rm', bg=(196, 214, 190))
    caption(d, t, [(0.6, 6.0, 'Mehr Gas: Die Drosselklappe öffnet, mehr Luft strömt'),
                   (6.2, dur, 'Das Steuergerät berechnet daraus die Kraftstoffmenge')], ROY, y=612)


def gl_sensoren(d, t, dur):
    header(d, t, 'LUFT UND LAST', 'Zwei Wege, die Luft zu erfassen', ROY)
    for i, (ti, l1, l2, l3) in enumerate([('Luftmassenmesser', 'misst die Luftmasse', 'direkt (kg/h)', 'sitzt nach dem Luftfilter'),
                                           ('Saugrohrdrucksensor', 'misst den Druck', 'im Saugrohr', 'Luftmenge wird berechnet')]):
        st = 0.4 + i * 2.6
        a = pr(t, st, st + 0.6)
        x = 80 + i * 580
        card(d, (x, 130, x + 540, 520), a, ROY)
        text(d, x + 270, 200, ti, 34, 'XB', TXT, a, 'mm', bg=CARD)
        text(d, x + 270, 300, l1, 30, 'Bold', ROY, a, 'mm', bg=CARD)
        text(d, x + 270, 345, l2, 30, 'Bold', ROY, a, 'mm', bg=CARD)
        text(d, x + 270, 440, l3, 22, 'Semi', MUTED, a, 'mm', bg=CARD)
    caption(d, t, [(5.8, dur, 'Viele Motoren haben beides – das Steuergerät vergleicht')], ROY, y=612)


def gl_egas(d, t, dur):
    header(d, t, 'LUFT UND LAST', 'Das elektronische Gaspedal (E-Gas)', ROY)
    kette_boxes(d, t, [('Fahrpedal', '2 Sensoren'), ('Steuergerät', 'vergleicht'), ('Drosselklappe', 'Motor + 2 Sensoren')], 220, 140, ROY)
    caption(d, t, [(0.6, 5.5, 'Doppelte Sensoren zur Sicherheit'),
                   (5.7, dur, 'Passen die Werte nicht zusammen: Notlauf mit wenig Leistung')], ROY)


GL_MERKE = merke_scene('LUFT UND LAST', ROY, [
    'Erst die Luft messen, dann den Kraftstoff berechnen', 'LMM: Luftmasse · Saugrohrdrucksensor: Druck',
    'E-Gas: doppelte Sensoren, sonst Notlauf', 'Falschluft → mager'])

VIDEOS_MOTOR.update({
    'mm-kraftstoff': (ROY, [(title_scene('K', 'Kraftstoffsystem', 'Vom Tank bis zum Einspritzventil', ROY, kicker=KICK2), 5.0),
                            (gk_saug, 10.0), (gk_direkt, 11.0), (GK_DRUCK, 9.0), (gk_tank, 8.5), (GK_MERKE, 7.5)]),
    'mm-einspritzung': (ROY, [(title_scene('ti', 'Einspritzung', 'Saugrohr- und Direkteinspritzung', ROY, size=96, kicker=KICK2), 5.0),
                              (ge_zyl, 11.0), (ge_ventil, 11.5), (ge_ti, 10.0), (GE_MERKE, 7.5)]),
    'mm-luft': (ROY, [(title_scene('L', 'Luft und Last', 'Wie das Steuergerät die Luft erfasst', ROY, kicker=KICK2), 5.0),
                      (gl_gas, 12.5), (gl_sensoren, 10.0), (gl_egas, 10.0), (GL_MERKE, 7.5)]),
})
