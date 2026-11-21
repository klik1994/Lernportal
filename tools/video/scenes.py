"""Gemeinsame Szenen-Bausteine: Titel, Werte-Liste, Merke, Stromkreis."""
import math
from engine import *


def title_scene(sym, title, sub, color):
    def fn(d, t, dur):
        k = pr(t, 0.1, 1.0, eout)
        # dekorativer Ring
        for i in range(36):
            ang = math.radians(i * 10 + t * 12)
            r0, r1 = 150, 162
            a = 0.35 * pr(t, 0.2 + i * 0.015, 0.8 + i * 0.015)
            line(d, [(640 + r0 * math.cos(ang), 250 + r0 * math.sin(ang)),
                     (640 + r1 * math.cos(ang), 250 + r1 * math.sin(ang))], color, 3, a)
        circle(d, (640, 250), 105 * k, color, 1)
        text(d, 640, 250, sym, 120 * max(k, 0.01), 'Black', BG, k, 'mm', bg=color)
        a2 = pr(t, 0.8, 1.6)
        text(d, 640, 470 + (1 - a2) * 20, title, 76, 'XB', TXT, a2, 'mm')
        a3 = pr(t, 1.3, 2.1)
        text(d, 640, 540 + (1 - a3) * 14, sub, 30, 'Med', MUTED, a3, 'mm')
        a4 = pr(t, 1.8, 2.6)
        text(d, 640, 50, 'GRUNDLAGEN ELEKTRIK  ·  LERNVIDEO', 16, 'Bold', color, a4, 'mm')
    return fn


def values_scene(tag, color, chips, rows, note=None):
    """rows: Liste (wert, beschreibung)."""
    def fn(d, t, dur):
        header(d, t, tag, 'Formelzeichen, Einheit und typische Werte', color)
        x = 160
        for i, (k, v) in enumerate(chips):
            a = pr(t, 0.4 + i * 0.3, 1.0 + i * 0.3)
            w = tw(k, 18, 'Semi') + tw(v, 26, 'Bold') + 60
            rrect(d, (x, 104, x + w, 154), 25, CARD, a)
            text(d, x + 24, 129, k, 18, 'Semi', MUTED, a, 'lm', bg=CARD)
            text(d, x + 36 + tw(k, 18, 'Semi'), 129, v, 26, 'Bold', color, a, 'lm', bg=CARD)
            x += w + 16
        n = len(rows)
        step = min(84, 400 / max(n, 1))
        for i, (val, desc) in enumerate(rows):
            st = 1.6 + i * 1.5
            a = pr(t, st, st + 0.6)
            dx = (1 - eout((t - st) / 0.6)) * 40
            y = 186 + i * step
            rrect(d, (160 + dx, y, 1120 + dx, y + step - 14), 14, CARD, a)
            rrect(d, (160 + dx, y, 420 + dx, y + step - 14), 14, CARD2, a)
            text(d, 290 + dx, y + (step - 14) / 2, val, 32, 'XB', color, a, 'mm', bg=CARD2)
            text(d, 450 + dx, y + (step - 14) / 2, desc, 26, 'Semi', TXT, a, 'lm', bg=CARD)
        if note:
            a = pr(t, 1.6 + n * 1.5 + 0.4, 1.6 + n * 1.5 + 1.0)
            text(d, 640, 186 + n * step + 26, note, 20, 'Med', MUTED, a, 'mm')
    return fn


def merke_scene(tag, color, items):
    def fn(d, t, dur):
        a = pr(t, 0.1, 0.7)
        rrect(d, (200, 90, 1080, 640), 28, CARD, a)
        rrect(d, (200, 90, 1080, 170), 28, color, a)
        rect(d, (200, 140, 1080, 170), color, a)
        text(d, 250, 130, 'Merke!', 40, 'XB', BG, a, 'lm', bg=color)
        text(d, 1030, 130, tag, 20, 'Bold', BG, a, 'rm', bg=color)
        for i, s in enumerate(items):
            st = 0.8 + i * 1.3
            k = pr(t, st, st + 0.5)
            y = 225 + i * 98
            circle(d, (270, y), 22 * eout((t - st) / 0.5), color, k, bg=CARD)
            if k > 0.5:
                line(d, [(259, y + 1), (267, y + 9), (282, y - 8)], BG, 5, 1, bg=color)
            lines = s.split('\n')
            for j, l in enumerate(lines):
                text(d, 316 + (1 - k) * 20, y - (len(lines) - 1) * 17 + j * 34, l, 28 if j == 0 else 22,
                     'Bold' if j == 0 else 'Med', TXT if j == 0 else MUTED, k, 'lm', bg=CARD)
    return fn


# ---------- Stromkreis ----------
BAT = (110, 250, 180, 130)
LAMP_C = (620, 300)
LAMP_R = 45
GAP_L, GAP_R, TOPY = 380, 470, 160
LEFT_WIRE = [(150, 234), (150, 200), (70, 200), (70, 470), (620, 470), (620, 345)]
RIGHT_WIRE = [(620, 255), (620, TOPY), (GAP_R, TOPY)]
BAT_WIRE = [(GAP_L, TOPY), (250, TOPY), (250, 234)]
ELEC_PATH = Path(list(reversed(LEFT_WIRE + [(620, 255), (620, TOPY), (GAP_R, TOPY), (GAP_L, TOPY), (250, TOPY), (250, 234)])))
MM_X, MM_Y = 900, 150


def circuit(d, t, a=1.0, bat_a=None, closed=1.0, bridge='switch', on=0.0, flow=0.0,
            flow_color=BLU, element='lamp', label=None, wire_a=None):
    """bridge: 'switch' (Schalter, closed 0..1), 'wire' (Leitung, closed=Deckkraft), 'none'."""
    wa = a if wire_a is None else wire_a
    ba = a if bat_a is None else bat_a
    line(d, LEFT_WIRE, WIRE, 5, wa)
    line(d, RIGHT_WIRE, WIRE, 5, wa)
    line(d, BAT_WIRE, WIRE, 5, wa)
    battery(d, *BAT, a=ba)
    if bridge == 'switch':
        ang = math.radians(-32 * (1 - closed))
        L = GAP_R - GAP_L
        line(d, [(GAP_L, TOPY), (GAP_L + L * math.cos(ang), TOPY + L * math.sin(ang))], TXT, 6, wa)
        circle(d, (GAP_L, TOPY), 8, TXT, wa)
        circle(d, (GAP_R, TOPY), 8, BG, wa, outline=TXT, width=3)
        text(d, (GAP_L + GAP_R) / 2, TOPY - 30, 'Schalter', 18, 'Semi', MUTED, wa)
    elif bridge == 'wire':
        line(d, [(GAP_L, TOPY), (GAP_R, TOPY)], WIRE, 5, wa * closed)
    if bridge != 'wire' or closed < 0.99:
        circle(d, (GAP_L, TOPY), 7, TXT, wa)
        circle(d, (GAP_R, TOPY), 7, TXT, wa)
    if flow > 0.01:
        flow_dots(d, ELEC_PATH, t, 70, 44, 7, flow_color, flow * a)
        if bridge == 'wire' and closed < 0.5:
            rect(d, (GAP_L + 8, TOPY - 10, GAP_R - 8, TOPY + 10), BG)
            circle(d, (GAP_L, TOPY), 7, TXT, wa)
            circle(d, (GAP_R, TOPY), 7, TXT, wa)
    if element == 'lamp':
        line(d, [(620, 255), (620, 345)], WIRE, 5, wa)
        lamp(d, LAMP_C, LAMP_R, on, a)
        text(d, 690, 300, label or 'Lampe', 20, 'Semi', MUTED, a, 'lm')


def lamp_points():
    return (620, 225), (620, 385)
