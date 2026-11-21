"""Kleine Zeichen-Engine fuer die Lernvideos (PIL, 2x Supersampling)."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
S = 2
FPS = 30

BG = (14, 25, 43)
CARD = (24, 40, 64)
CARD2 = (33, 53, 82)
TXT = (236, 241, 248)
MUTED = (148, 164, 186)
WIRE = (140, 155, 178)
YEL = (247, 182, 18)
BLU = (40, 170, 245)
RED = (240, 94, 78)
GRN = (52, 199, 120)
BLACK = (20, 22, 26)
WATER = (52, 140, 230)
PUR = (160, 124, 245)
ORA = (255, 143, 63)

FD = '/usr/share/fonts/opentype/inter/'
_fc = {}


def F(size, w='Bold'):
    k = (size, w)
    if k not in _fc:
        name = {'Bold': 'Inter-Bold.otf', 'Semi': 'Inter-SemiBold.otf', 'Reg': 'Inter-Regular.otf',
                'Med': 'Inter-Medium.otf', 'Black': 'InterDisplay-Black.otf', 'XB': 'InterDisplay-ExtraBold.otf'}[w]
        _fc[k] = ImageFont.truetype(FD + name, int(size * S))
    return _fc[k]


def P(v):
    return int(round(v * S))


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def eout(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def pr(t, a, b, f=ease):
    if b <= a:
        return 1.0 if t >= a else 0.0
    return f((t - a) / (b - a))


def lerp(a, b, k):
    return a + (b - a) * k


def mix(c, a, bg=BG):
    a = clamp(a)
    return tuple(int(round(bg[i] + (c[i] - bg[i]) * a)) for i in range(3))


def text(d, x, y, s, size, w='Bold', fill=TXT, a=1.0, anchor='la', bg=BG):
    if a <= 0.01:
        return
    d.text((P(x), P(y)), s, font=F(size, w), fill=mix(fill, a, bg), anchor=anchor)


def tw(s, size, w='Bold'):
    return F(size, w).getlength(s) / S


def rrect(d, box, r, fill=None, a=1.0, outline=None, width=0, bg=BG):
    if a <= 0.01:
        return
    x0, y0, x1, y1 = box
    d.rounded_rectangle((P(x0), P(y0), P(x1), P(y1)), radius=P(r),
                        fill=mix(fill, a, bg) if fill else None,
                        outline=mix(outline, a, bg) if outline else None, width=P(width) if width else 0)


def rect(d, box, fill, a=1.0, bg=BG):
    if a <= 0.01:
        return
    x0, y0, x1, y1 = box
    d.rectangle((P(x0), P(y0), P(x1), P(y1)), fill=mix(fill, a, bg))


def circle(d, c, r, fill=None, a=1.0, outline=None, width=0, bg=BG):
    if a <= 0.01 or r <= 0:
        return
    x, y = c
    d.ellipse((P(x - r), P(y - r), P(x + r), P(y + r)), fill=mix(fill, a, bg) if fill else None,
              outline=mix(outline, a, bg) if outline else None, width=P(width) if width else 0)


def line(d, pts, fill, width, a=1.0, bg=BG):
    if a <= 0.01:
        return
    d.line([(P(x), P(y)) for x, y in pts], fill=mix(fill, a, bg), width=P(width), joint='curve')
    for x, y in (pts[0], pts[-1]):
        circle(d, (x, y), width / 2, fill, a, bg=bg)


def poly(d, pts, fill, a=1.0, bg=BG):
    if a <= 0.01:
        return
    d.polygon([(P(x), P(y)) for x, y in pts], fill=mix(fill, a, bg))


def arrow(d, p0, p1, fill, width=4, head=14, a=1.0, bg=BG):
    (x0, y0), (x1, y1) = p0, p1
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - head * math.cos(ang), y1 - head * math.sin(ang)
    line(d, [(x0, y0), (bx, by)], fill, width, a, bg)
    l, r = ang + 2.5, ang - 2.5
    poly(d, [(x1, y1), (x1 + head * math.cos(l), y1 + head * math.sin(l)),
             (x1 + head * math.cos(r), y1 + head * math.sin(r))], fill, a, bg)


# ---------- Pfade ----------
class Path:
    def __init__(self, pts):
        self.pts = pts
        self.seg = []
        tot = 0
        for i in range(len(pts) - 1):
            l = math.dist(pts[i], pts[i + 1])
            self.seg.append((tot, l))
            tot += l
        self.L = tot

    def at(self, s):
        s = s % self.L if self.L else 0
        for i, (st, l) in enumerate(self.seg):
            if s <= st + l or i == len(self.seg) - 1:
                k = (s - st) / l if l else 0
                (x0, y0), (x1, y1) = self.pts[i], self.pts[i + 1]
                return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k


def flow_dots(d, path, t, speed, spacing, r, fill, a=1.0, sign=None, bg=BG):
    n = int(path.L // spacing)
    off = (t * speed) % spacing
    for i in range(n + 1):
        s = i * spacing + off
        if s > path.L:
            continue
        x, y = path.at(s)
        circle(d, (x, y), r, fill, a, bg=bg)
        if sign:
            text(d, x, y, sign, r * 1.5, 'Bold', BG, a, 'mm', bg=fill)


def bezier(p0, p1, p2, n=40):
    out = []
    for i in range(n + 1):
        k = i / n
        x = (1 - k) ** 2 * p0[0] + 2 * (1 - k) * k * p1[0] + k * k * p2[0]
        y = (1 - k) ** 2 * p0[1] + 2 * (1 - k) * k * p1[1] + k * k * p2[1]
        out.append((x, y))
    return out


# ---------- Bausteine ----------
def header(d, t, tag, title, color):
    a = pr(t, 0, 0.6)
    w = tw(tag, 15, 'Bold') + 28
    rrect(d, (56, 40, 56 + w, 70), 15, color, a)
    text(d, 56 + w / 2, 55, tag, 15, 'Bold', BG, a, 'mm', bg=color)
    text(d, 56 + w + 18, 55 + (1 - a) * 8, title, 26, 'Bold', TXT, a, 'lm')


def caption(d, t, items, color, y=612):
    """items: Liste (start, ende, text). Text darf '\n' enthalten."""
    for st, en, s in items:
        a = pr(t, st, st + 0.5) * (1 - pr(t, en - 0.4, en))
        if a <= 0.01:
            continue
        lines = s.split('\n')
        size = 28
        wmax = max(tw(l, size) for l in lines)
        h = 34 * len(lines) + 30
        x0 = W / 2 - wmax / 2 - 34
        x1 = W / 2 + wmax / 2 + 34
        dy = (1 - eout((t - st) / 0.5)) * 18
        y0 = y + dy - (h - 64) / 2
        rrect(d, (x0, y0, x1, y0 + h), 18, CARD, a)
        rect(d, (x0, y0 + 14, x0 + 6, y0 + h - 14), color, a)
        for i, l in enumerate(lines):
            text(d, W / 2, y0 + 15 + 17 + i * 34, l, size, 'Bold', TXT, a, 'mm', bg=CARD)


def battery(d, x, y, w, h, a=1.0, label='12 V'):
    """Kfz-Batterie, Pole oben: minus links, plus rechts. Liefert Polpositionen."""
    rrect(d, (x, y, x + w, y + h), 10, (50, 58, 72), a, outline=(90, 100, 118), width=2)
    rect(d, (x, y + 16, x + w, y + 24), (66, 76, 94), a)
    mx, px = x + w * 0.22, x + w * 0.78
    rrect(d, (mx - 14, y - 16, mx + 14, y + 2), 4, (70, 78, 92), a)
    rrect(d, (px - 14, y - 16, px + 14, y + 2), 4, RED, a)
    text(d, mx, y + 50, '−', 30, 'Bold', TXT, a, 'mm', bg=(50, 58, 72))
    text(d, px, y + 50, '+', 30, 'Bold', RED, a, 'mm', bg=(50, 58, 72))
    text(d, x + w / 2, y + h - 26, label, 22, 'Bold', TXT, a, 'mm', bg=(50, 58, 72))
    return (mx, y - 16), (px, y - 16)


def lamp(d, c, r, on=0.0, a=1.0):
    x, y = c
    if on > 0.01:
        for k in range(6, 0, -1):
            circle(d, c, r + k * 9 * on, mix(YEL, 0.05 * (7 - k) * on * a), 1)
    fill = mix(YEL, 0.25 + 0.75 * on, CARD)
    circle(d, c, r, fill, a, outline=TXT, width=3)
    o = r * 0.7
    line(d, [(x - o, y - o), (x + o, y + o)], TXT, 3, a, bg=fill)
    line(d, [(x - o, y + o), (x + o, y - o)], TXT, 3, a, bg=fill)


def resistor(d, c, w, h, a=1.0, color=RED):
    x, y = c
    rrect(d, (x - w / 2, y - h / 2, x + w / 2, y + h / 2), 4, CARD2, a, outline=color, width=4)


MM_BODY = (44, 49, 58)


def multimeter(d, x, y, a=1.0, reading='', mode='V', unit='', color=YEL, sel=None):
    """Multimeter, linke obere Ecke x,y; 220x330. Gibt Buchsenpositionen zurueck."""
    w, h = 220, 330
    rrect(d, (x, y, x + w, y + h), 26, color, a)
    rrect(d, (x + 10, y + 10, x + w - 10, y + h - 10), 20, MM_BODY, a, bg=color)
    disp = (x + 28, y + 28, x + w - 28, y + 108)
    rrect(d, disp, 8, (196, 214, 190), a, bg=MM_BODY)
    dc = (196, 214, 190)
    text(d, disp[2] - 12, disp[3] - 12, reading, 38, 'Bold', (25, 35, 28), a, 'rs', bg=dc)
    text(d, disp[0] + 10, disp[1] + 10, unit, 14, 'Bold', (25, 35, 28), a, 'la', bg=dc)
    # Drehschalter
    cx, cy = x + w / 2, y + 196
    labels = {'V': -150, 'Ω': -90, 'A': -30, 'OFF': 165}
    for k, ang in labels.items():
        rad = math.radians(ang)
        tx, ty = cx + 66 * math.cos(rad), cy + 62 * math.sin(rad) + 2
        col = color if k == mode else MUTED
        text(d, tx, ty, k if k != 'V' else 'V DC', 15 if k != 'OFF' else 12, 'Bold', col, a, 'mm', bg=MM_BODY)
    circle(d, (cx, cy), 42, (30, 33, 40), a, outline=(80, 86, 98), width=3, bg=MM_BODY)
    rad = math.radians(labels.get(mode, 160))
    line(d, [(cx, cy), (cx + 36 * math.cos(rad), cy + 36 * math.sin(rad))], color, 7, a, bg=(30, 33, 40))
    # Buchsen
    sy = y + 286
    socks = {'A': (x + 52, sy), 'COM': (x + 110, sy), 'VΩ': (x + 168, sy)}
    for k, (sx, syy) in socks.items():
        ring = BLACK if k == 'COM' else RED
        hl = (sel is not None and k in sel)
        circle(d, (sx, syy), 15, ring, a, outline=(color if hl else (90, 96, 108)), width=3 if hl else 2,
               bg=MM_BODY)
        circle(d, (sx, syy), 6, (10, 10, 12), a, bg=ring)
        text(d, sx, syy - 26, k, 13, 'Bold', TXT if hl else MUTED, a, 'mm', bg=MM_BODY)
    return socks


def lead(d, s, tip, col, k=1.0, a=1.0, sag=60):
    """Messleitung von Buchse s zur Spitze tip; k = Anteil des Weges (0..1)."""
    if k <= 0.001 or a <= 0.01:
        return
    tx = lerp(s[0], tip[0], k)
    ty = lerp(s[1] + 40, tip[1], k)
    mid = ((s[0] + tx) / 2, max(s[1], ty) + sag)
    pts = bezier(s, mid, (tx, ty))
    line(d, pts, col if col != BLACK else (12, 12, 14), 6, a)
    if col == BLACK:
        line(d, pts, (60, 64, 72), 2, a)
    circle(d, (tx, ty), 9, col if col != BLACK else (40, 42, 48), a, outline=TXT, width=2)


def progress(d, g, total, color):
    rect(d, (0, H - 6, W, H), CARD)
    rect(d, (0, H - 6, W * clamp(g / total), H), color)


# ---------- Rendern ----------
def render_scene(fn, dur, out, g0, total, color, fade=0.35):
    n = int(round(dur * FPS))
    tmp = out + '.tmp.mp4'
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
           '-pix_fmt', 'yuv420p', '-movflags', '+faststart', tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    bgimg = Image.new('RGB', (W, H), BG)
    for i in range(n):
        t = i / FPS
        im = Image.new('RGB', (W * S, H * S), BG)
        d = ImageDraw.Draw(im)
        fn(d, t, dur)
        im = im.reduce(S)
        f = min(1.0, t / fade, (dur - t) / fade) if fade else 1
        if f < 1:
            im = Image.blend(bgimg, im, clamp(f))
        d2 = ImageDraw.Draw(im)
        rect_px(d2, g0 + t, total, color)
        p.stdin.write(im.tobytes())
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, out)
    else:
        raise SystemExit('ffmpeg failed ' + out)


def rect_px(d, g, total, color):
    d.rectangle((0, H - 5, W, H), fill=CARD)
    d.rectangle((0, H - 5, int(W * clamp(g / total)), H), fill=color)


def still(fn, dur, t, path):
    im = Image.new('RGB', (W * S, H * S), BG)
    d = ImageDraw.Draw(im)
    fn(d, t, dur)
    im.reduce(S).save(path)


def fan(d, c, r, ang, color=ORA, a=1.0, bg=BG):
    """Luefter: Kreis mit drei Fluegeln, ang in Grad."""
    x, y = c
    circle(d, c, r, CARD2, a, outline=TXT, width=4, bg=bg)
    for k in range(3):
        base = math.radians(ang + k * 120)
        # Fluegel als Tropfen: aussen breit, innen spitz
        p1 = [(x, y)]
        for i in range(0, 11):
            w = math.radians(-30 + 6 * i)
            p1.append((x + r * 0.82 * math.cos(base + w), y + r * 0.82 * math.sin(base + w)))
        poly(d, p1, color, a, bg=CARD2)
    circle(d, c, r * 0.14, TXT, a, bg=CARD2)
