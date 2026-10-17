"""Generates the site's illustration set (services, about, silk backgrounds).

Run: python scripts/illustrations.py
Writes SVGs to public/images/illustrations/ and a Figma-friendly copy (no
<style> animation block) to scripts/figma-svg/ for pushing into the Figma
file "Alexandria Braniff Website Illustrations".
"""
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'public', 'images', 'illustrations')
FIG = os.path.join(ROOT, 'scripts', 'figma-svg')

NAVY = '#1B2A4A'
CORAL = '#C8553D'
GOLD = '#B8935A'
GOLD_L = '#D4B483'
PAPER = '#F7F6F2'
BG = '#EFEDE7'
LINE = '#D5D3CB'
WHITE = '#FFFFFF'
MUTED = '#8C93A8'

W, H = 1200, 840
CX, CY = 600, 430

S = f'stroke="{NAVY}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'


def st(extra=''):
    """Default navy stroke attributes, minus any that `extra` overrides."""
    keys = {k.split('=')[0] for k in extra.split() if '=' in k}
    base = [a for a in S.split() if a.split('=')[0] not in keys]
    return ' '.join(base)


# ---------- primitives ----------

def rect(x, y, w, h, fill=WHITE, r=10, stroke=True, extra=''):
    st_ = st(extra) if stroke else 'stroke="none"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {st_} {extra}/>'


def bar(x, y, w, h=10, fill=LINE, r=None):
    r = h / 2 if r is None else r
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'


def circle(cx, cy, r, fill=WHITE, stroke=True, extra=''):
    st_ = st(extra) if stroke else 'stroke="none"'
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {st_} {extra}/>'


def path(d, fill='none', extra=''):
    return f'<path d="{d}" fill="{fill}" {st(extra)} {extra}/>'


def line(x1, y1, x2, y2, color=NAVY, w=3, extra=''):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{w}" stroke-linecap="round" {extra}/>')


def check(x, y, s=1.0, color=CORAL, w=4):
    return (f'<path d="M{x - 14 * s} {y} L{x - 4 * s} {y + 10 * s} L{x + 16 * s} {y - 12 * s}" '
            f'fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def window(x, y, w, h, body=''):
    """Browser window with a three-dot bar."""
    out = [
        rect(x + 10, y + 12, w, h, fill=LINE, stroke=False, r=14),  # offset shadow
        rect(x, y, w, h, r=14),
        line(x, y + 44, x + w, y + 44),
        circle(x + 26, y + 22, 6, fill=CORAL, stroke=False),
        circle(x + 46, y + 22, 6, fill=GOLD, stroke=False),
        circle(x + 66, y + 22, 6, fill=LINE, stroke=False),
        bar(x + 96, y + 17, min(220, w - 130), 10, fill=BG),
    ]
    return ''.join(out) + body


def page_layout(x, y, w, h):
    """Generic hero layout inside a window body."""
    pad = 28
    ix, iy = x + pad, y + 44 + pad
    iw = w - pad * 2
    col = iw * 0.48
    out = [
        bar(ix, iy + 10, col * 0.9, 16, fill=NAVY),
        bar(ix, iy + 38, col * 0.7, 16, fill=NAVY),
        bar(ix, iy + 76, col * 0.95, 8),
        bar(ix, iy + 94, col * 0.8, 8),
        bar(ix, iy + 112, col * 0.6, 8),
        rect(ix, iy + 140, 110, 34, fill=NAVY, r=4, stroke=False),
    ]
    px = ix + col + 24
    pw = iw - col - 24
    ph = min(h - 44 - pad * 2 - 10, 190)
    out.append(rect(px, iy, pw, ph, fill=BG, r=8, stroke=False))
    out.append(f'<path d="M{px} {iy + ph * 0.7} C{px + pw * 0.3} {iy + ph * 0.35}, {px + pw * 0.6} {iy + ph * 0.95}, {px + pw} {iy + ph * 0.5} L{px + pw} {iy + ph} L{px} {iy + ph} Z" fill="{GOLD_L}" opacity="0.7"/>')
    out.append(circle(px + pw * 0.75, iy + ph * 0.3, 16, fill=CORAL, stroke=False))
    return ''.join(out)


def magnifier(cx, cy, r, inner=''):
    hx, hy = cx + r * 0.72, cy + r * 0.72
    return (f'<line x1="{hx}" y1="{hy}" x2="{hx + r * 0.75}" y2="{hy + r * 0.75}" stroke="{NAVY}" stroke-width="16" stroke-linecap="round"/>'
            + circle(cx, cy, r, fill=WHITE, extra='fill-opacity="0.82" stroke-width="6"') + inner)


def arrow(x1, y1, x2, y2, color=NAVY, w=3, head=14):
    ang = math.atan2(y2 - y1, x2 - x1)
    a1 = ang + math.radians(150)
    a2 = ang - math.radians(150)
    p1 = (x2 + head * math.cos(a1), y2 + head * math.sin(a1))
    p2 = (x2 + head * math.cos(a2), y2 + head * math.sin(a2))
    return (line(x1, y1, x2, y2, color, w)
            + f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2} {y2} L{p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def swatches(x, y, size=56, gap=14, colors=(NAVY, CORAL, GOLD, PAPER)):
    return ''.join(rect(x + i * (size + gap), y, size, size, fill=c, r=8) for i, c in enumerate(colors))


def nib(x, y, s=1.0):
    """Fountain pen nib pointing down, tip at (x, y)."""
    d = (f'M{x} {y} L{x - 34 * s} {y - 70 * s} L{x - 26 * s} {y - 150 * s} '
         f'L{x + 26 * s} {y - 150 * s} L{x + 34 * s} {y - 70 * s} Z')
    return (path(d, fill=GOLD_L)
            + line(x, y, x, y - 70 * s)
            + circle(x, y - 78 * s, 8 * s, fill=WHITE)
            + rect(x - 30 * s, y - 210 * s, 60 * s, 64 * s, fill=NAVY, r=6))


def monogram(cx, cy, r):
    """Abstract monogram seal: concentric rings and a flowing stroke (no lettering)."""
    return (circle(cx, cy, r, fill=WHITE, extra='stroke-width="4"')
            + circle(cx, cy, r - 14, fill='none', extra=f'stroke="{GOLD}" stroke-width="2"')
            + f'<path d="M{cx - r * 0.55} {cy + r * 0.1} C{cx - r * 0.3} {cy - r * 0.45}, {cx - r * 0.05} {cy - r * 0.2}, {cx} {cy} S{cx + r * 0.3} {cy + r * 0.45}, {cx + r * 0.55} {cy - r * 0.1}" fill="none" stroke="{NAVY}" stroke-width="5" stroke-linecap="round"/>'
            + circle(cx, cy, 6, fill=CORAL, stroke=False))


def phone(x, y, w=150, h=290, body=''):
    return (rect(x + 8, y + 10, w, h, fill=LINE, stroke=False, r=24)
            + rect(x, y, w, h, r=24)
            + bar(x + w / 2 - 22, y + 14, 44, 8, fill=BG)
            + body)


def doc(x, y, w, h, lines=5, fill=WHITE):
    out = [rect(x, y, w, h, fill=fill, r=8)]
    for i in range(lines):
        out.append(bar(x + 26, y + 34 + i * 30, (w - 52) * (0.95 if i % 3 else 0.6), 9))
    return ''.join(out)


def server(x, y, w=300, h=64, n=3):
    out = []
    for i in range(n):
        yy = y + i * (h + 14)
        out.append(rect(x, yy, w, h, r=10))
        out.append(circle(x + 32, yy + h / 2, 7, fill=CORAL if i == 0 else GOLD, stroke=False))
        out.append(circle(x + 56, yy + h / 2, 7, fill=LINE, stroke=False))
        for k in range(4):
            out.append(line(x + w - 110 + k * 22, yy + 20, x + w - 110 + k * 22, yy + h - 20, LINE, 4))
    return ''.join(out)


def envelope(x, y, w=300, h=200, fill=WHITE):
    return (rect(x, y, w, h, fill=fill, r=10)
            + path(f'M{x + 6} {y + 8} L{x + w / 2} {y + h * 0.58} L{x + w - 6} {y + 8}'))


def globe(cx, cy, r):
    return (circle(cx, cy, r, fill=WHITE)
            + f'<ellipse cx="{cx}" cy="{cy}" rx="{r * 0.45}" ry="{r}" fill="none" {S}/>'
            + line(cx - r, cy, cx + r, cy)
            + path(f'M{cx - r * 0.87} {cy - r * 0.5} Q{cx} {cy - r * 0.3} {cx + r * 0.87} {cy - r * 0.5}')
            + path(f'M{cx - r * 0.87} {cy + r * 0.5} Q{cx} {cy + r * 0.7} {cx + r * 0.87} {cy + r * 0.5}'))


def key(x, y, s=1.0, fill=GOLD_L):
    return (circle(x, y, 46 * s, fill=fill, extra='stroke-width="4"')
            + circle(x, y, 16 * s, fill=BG)
            + rect(x + 44 * s, y - 9 * s, 190 * s, 18 * s, fill=fill, r=4)
            + rect(x + 190 * s, y + 9 * s, 16 * s, 34 * s, fill=fill, r=2)
            + rect(x + 150 * s, y + 9 * s, 16 * s, 24 * s, fill=fill, r=2))


def gift(x, y, w=260, h=200):
    return (rect(x, y + 50, w, h, fill=WHITE)
            + rect(x - 16, y, w + 32, 56, fill=PAPER)
            + rect(x + w / 2 - 18, y, 36, h + 50, fill=CORAL, r=2)
            + path(f'M{x + w / 2} {y} C{x + w / 2 - 70} {y - 70}, {x + w / 2 - 110} {y - 10}, {x + w / 2} {y}', fill=GOLD_L)
            + path(f'M{x + w / 2} {y} C{x + w / 2 + 70} {y - 70}, {x + w / 2 + 110} {y - 10}, {x + w / 2} {y}', fill=GOLD_L))


def chart_bars(x, y, w, h, vals, hi=-1):
    n = len(vals)
    bw = w / n * 0.6
    out = [line(x, y + h, x + w, y + h)]
    for i, v in enumerate(vals):
        bh = h * v
        out.append(rect(x + i * w / n + (w / n - bw) / 2, y + h - bh, bw, bh,
                        fill=CORAL if i == hi else (NAVY if i == n - 1 and hi < 0 else WHITE), r=4))
    return ''.join(out)


def checklist(x, y, w, rows=4, done=3):
    out = []
    for i in range(rows):
        yy = y + i * 58
        out.append(rect(x, yy, 34, 34, fill=WHITE, r=6))
        if i < done:
            out.append(check(x + 17, yy + 17, 0.9))
        out.append(bar(x + 56, yy + 12, w * (0.9 if i % 2 else 0.7), 10))
    return ''.join(out)


def toggle(x, y, on=True):
    return (rect(x, y, 76, 40, fill=NAVY if on else BG, r=20)
            + circle(x + (56 if on else 20), y + 20, 14, fill=WHITE, stroke=False))


def bubble(x, y, w, h, fill=WHITE, tail_left=True, dots=True, dot_color=NAVY):
    tx = x + 40 if tail_left else x + w - 40
    t = (f'M{tx - 14} {y + h - 2} L{tx + (-24 if tail_left else 24)} {y + h + 32} L{tx + 14} {y + h - 2}')
    out = [path(t, fill=fill), rect(x, y, w, h, fill=fill, r=26),
           f'<rect x="{tx - 12}" y="{y + h - 8}" width="24" height="10" fill="{fill}"/>']
    if dots:
        for k in range(3):
            out.append(circle(x + w / 2 - 30 + k * 30, y + h / 2, 7, fill=dot_color, stroke=False))
    return ''.join(out)


def cursor(x, y, s=1.0):
    d = (f'M{x} {y} L{x} {y + 64 * s} L{x + 16 * s} {y + 50 * s} L{x + 28 * s} {y + 76 * s} '
         f'L{x + 40 * s} {y + 70 * s} L{x + 28 * s} {y + 45 * s} L{x + 48 * s} {y + 45 * s} Z')
    return path(d, fill=WHITE)


def pin(cx, cy, s=1.0, fill=CORAL):
    d = (f'M{cx} {cy} C{cx - 20 * s} {cy - 34 * s}, {cx - 46 * s} {cy - 56 * s}, {cx - 46 * s} {cy - 86 * s} '
         f'A{46 * s} {46 * s} 0 0 1 {cx + 46 * s} {cy - 86 * s} C{cx + 46 * s} {cy - 56 * s}, {cx + 20 * s} {cy - 34 * s}, {cx} {cy} Z')
    return path(d, fill=fill) + circle(cx, cy - 86 * s, 16 * s, fill=WHITE)


def shield(cx, cy, s=1.0, fill=WHITE):
    d = (f'M{cx} {cy - 130 * s} L{cx + 110 * s} {cy - 90 * s} L{cx + 110 * s} {cy} '
         f'C{cx + 110 * s} {cy + 80 * s}, {cx + 50 * s} {cy + 120 * s}, {cx} {cy + 140 * s} '
         f'C{cx - 50 * s} {cy + 120 * s}, {cx - 110 * s} {cy + 80 * s}, {cx - 110 * s} {cy} '
         f'L{cx - 110 * s} {cy - 90 * s} Z')
    return path(d, fill=fill, extra='stroke-width="4"') + check(cx, cy + 4, 3.0 * s, CORAL, 10)


def refresh(cx, cy, r, color=CORAL):
    return (f'<path d="M{cx + r} {cy} A{r} {r} 0 1 1 {cx + r * 0.2} {cy - r * 0.98}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round"/>'
            + f'<path d="M{cx + r * 0.2 - 4} {cy - r * 0.98 - 16} L{cx + r * 0.2 + 14} {cy - r * 0.98} L{cx + r * 0.2 - 6} {cy - r * 0.98 + 16}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')


def card(x, y, w=380, h=230, fill=NAVY):
    return (rect(x + 10, y + 12, w, h, fill=LINE, stroke=False, r=18)
            + rect(x, y, w, h, fill=fill, r=18)
            + rect(x + 30, y + 60, 60, 44, fill=GOLD_L, r=6, stroke=False)
            + bar(x + 30, y + h - 60, w * 0.55, 12, fill=PAPER)
            + bar(x + 30, y + h - 36, w * 0.25, 9, fill=MUTED)
            + circle(x + w - 70, y + 50, 22, fill=CORAL, stroke=False)
            + circle(x + w - 44, y + 50, 22, fill=GOLD, stroke=False, extra='fill-opacity="0.85"'))


def bag(x, y, w=220, h=240, fill=CORAL):
    return (path(f'M{x + w * 0.3} {y + 40} C{x + w * 0.3} {y - 40}, {x + w * 0.7} {y - 40}, {x + w * 0.7} {y + 40}', extra=f'stroke="{GOLD}" stroke-width="8"')
            + path(f'M{x} {y + 30} L{x + w} {y + 30} L{x + w - 14} {y + h} L{x + 14} {y + h} Z', fill=fill, extra='stroke-width="4"')
            + circle(x + w / 2, y + h * 0.55, 26, fill=PAPER, stroke=False))


def plant(x, y, s=1.0):
    """Sprig rising from (x, y)."""
    return (path(f'M{x} {y} C{x - 6 * s} {y - 80 * s}, {x + 10 * s} {y - 150 * s}, {x} {y - 220 * s}', extra='stroke-width="4"')
            + path(f'M{x} {y - 70 * s} C{x - 60 * s} {y - 70 * s}, {x - 90 * s} {y - 120 * s}, {x - 96 * s} {y - 150 * s} C{x - 50 * s} {y - 150 * s}, {x - 10 * s} {y - 120 * s}, {x} {y - 70 * s} Z', fill=GOLD_L)
            + path(f'M{x + 2 * s} {y - 130 * s} C{x + 60 * s} {y - 130 * s}, {x + 96 * s} {y - 170 * s}, {x + 100 * s} {y - 210 * s} C{x + 50 * s} {y - 210 * s}, {x + 10 * s} {y - 180 * s}, {x + 2 * s} {y - 130 * s} Z', fill=CORAL)
            + path(f'M{x} {y - 200 * s} C{x - 40 * s} {y - 210 * s}, {x - 50 * s} {y - 250 * s}, {x - 44 * s} {y - 270 * s} C{x - 14 * s} {y - 260 * s}, {x + 4 * s} {y - 230 * s}, {x} {y - 200 * s} Z', fill=WHITE))


def gauge(cx, cy, r):
    out = [path(f'M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}', fill=WHITE, extra='stroke-width="4"'),
           line(cx - r, cy, cx + r, cy, w=4)]
    out.append(f'<path d="M{cx + r * math.cos(math.radians(-40)) * 0.84:.1f} {cy + r * math.sin(math.radians(-40)) * 0.84:.1f} A{r * 0.84} {r * 0.84} 0 0 1 {cx + r * 0.84} {cy}" fill="none" stroke="{CORAL}" stroke-width="22"/>')
    out.append(f'<path d="M{cx - r * 0.84} {cy} A{r * 0.84} {r * 0.84} 0 0 1 {cx + r * math.cos(math.radians(-140)) * 0.84:.1f} {cy + r * math.sin(math.radians(-140)) * 0.84:.1f}" fill="none" stroke="{LINE}" stroke-width="22"/>')
    for k in range(11):
        a = math.radians(180 + k * 18)
        out.append(line(cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a),
                        cx + r * 0.7 * math.cos(a), cy + r * 0.7 * math.sin(a), NAVY, 3))
    a = math.radians(-28)
    out.append(line(cx, cy, cx + r * 0.66 * math.cos(a), cy + r * 0.66 * math.sin(a), NAVY, 8))
    out.append(circle(cx, cy, 16, fill=GOLD))
    return ''.join(out)


def search_bar(x, y, w, h=70):
    return (rect(x, y, w, h, r=h / 2, extra='stroke-width="4"')
            + circle(x + 44, y + h / 2 - 3, 13, fill='none')
            + line(x + 54, y + h / 2 + 7, x + 64, y + h / 2 + 17, NAVY, 4)
            + bar(x + 86, y + h / 2 - 5, w * 0.4, 10))


def results(x, y, w, n=3, hi=0):
    out = []
    for i in range(n):
        yy = y + i * 92
        f = PAPER if i != hi else WHITE
        out.append(rect(x, yy, w, 76, fill=f, r=10))
        if i == hi:
            out.append(rect(x, yy, 10, 76, fill=CORAL, r=0, stroke=False))
        out.append(bar(x + 30, yy + 20, w * 0.45, 12, fill=NAVY if i == hi else MUTED))
        out.append(bar(x + 30, yy + 46, w * 0.75, 8))
    return ''.join(out)


def line_chart(x, y, w, h, pts):
    out = [line(x, y + h, x + w, y + h), line(x, y, x, y + h)]
    for k in range(1, 4):
        out.append(line(x, y + h * k / 4, x + w, y + h * k / 4, LINE, 2, 'stroke-dasharray="6 10"'))
    coords = [(x + w * i / (len(pts) - 1), y + h - h * p) for i, p in enumerate(pts)]
    d = 'M' + ' L'.join(f'{a:.1f} {b:.1f}' for a, b in coords)
    area = d + f' L{x + w} {y + h} L{x} {y + h} Z'
    out.append(f'<path d="{area}" fill="{GOLD_L}" opacity="0.45"/>')
    out.append(f'<path d="{d}" fill="none" stroke="{CORAL}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, (a, b) in enumerate(coords):
        out.append(circle(a, b, 9 if i == len(coords) - 1 else 6, fill=NAVY if i == len(coords) - 1 else WHITE))
    return ''.join(out)


def nodes(cx, cy, r, n=5, center_fill=NAVY):
    out = []
    pts = [(cx + r * math.cos(math.radians(-90 + i * 360 / n)), cy + r * math.sin(math.radians(-90 + i * 360 / n))) for i in range(n)]
    for (a, b) in pts:
        out.append(line(cx, cy, a, b, NAVY, 3, 'stroke-dasharray="2 10"'))
    out.append(circle(cx, cy, 64, fill=center_fill, extra='stroke-width="4"'))
    out.append(circle(cx, cy, 22, fill=CORAL, stroke=False))
    fills = [WHITE, GOLD_L, WHITE, CORAL, WHITE, GOLD_L]
    for i, (a, b) in enumerate(pts):
        out.append(rect(a - 42, b - 42, 84, 84, fill=fills[i % len(fills)], r=20))
    return ''.join(out)


def calendar(x, y, w=300, h=280, hi=(2, 1)):
    out = [rect(x, y, w, h, r=14), rect(x, y, w, 60, fill=NAVY, r=14),
           f'<rect x="{x}" y="{y + 40}" width="{w}" height="20" fill="{NAVY}"/>',
           line(x + 70, y - 14, x + 70, y + 20, NAVY, 8), line(x + w - 70, y - 14, x + w - 70, y + 20, NAVY, 8)]
    cw, ch = (w - 40) / 5, (h - 90) / 4
    for r_ in range(4):
        for c in range(5):
            cx_, cy_ = x + 20 + c * cw, y + 76 + r_ * ch
            f = CORAL if (c, r_) == hi else BG
            out.append(f'<rect x="{cx_ + 4}" y="{cy_ + 4}" width="{cw - 8}" height="{ch - 8}" rx="6" fill="{f}"/>')
    return ''.join(out)


def clock(cx, cy, r):
    return (circle(cx, cy, r, fill=WHITE, extra='stroke-width="4"')
            + line(cx, cy, cx, cy - r * 0.6, NAVY, 5) + line(cx, cy, cx + r * 0.45, cy + r * 0.1, CORAL, 5)
            + circle(cx, cy, 6, fill=NAVY, stroke=False))


def person(cx, cy, s=1.0, fill=CORAL):
    return (path(f'M{cx - 110 * s} {cy + 120 * s} C{cx - 110 * s} {cy + 20 * s}, {cx - 60 * s} {cy - 10 * s}, {cx} {cy - 10 * s} C{cx + 60 * s} {cy - 10 * s}, {cx + 110 * s} {cy + 20 * s}, {cx + 110 * s} {cy + 120 * s} Z', fill=fill, extra='stroke-width="4"')
            + circle(cx, cy - 80 * s, 62 * s, fill=PAPER, extra='stroke-width="4"'))


def heart(cx, cy, s=1.0, fill=CORAL):
    return path(f'M{cx} {cy + 26 * s} C{cx - 50 * s} {cy - 6 * s}, {cx - 30 * s} {cy - 46 * s}, {cx} {cy - 22 * s} C{cx + 30 * s} {cy - 46 * s}, {cx + 50 * s} {cy - 6 * s}, {cx} {cy + 26 * s} Z', fill=fill)


def code_lines(x, y, rows):
    out = []
    for i, (indent, wdt, col) in enumerate(rows):
        out.append(bar(x + indent * 34, y + i * 32, wdt, 12, fill=col))
    return ''.join(out)


def brackets(cx, cy, s=1.0, color=CORAL):
    return (f'<path d="M{cx - 60 * s} {cy - 50 * s} L{cx - 110 * s} {cy} L{cx - 60 * s} {cy + 50 * s}" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
            + f'<path d="M{cx + 60 * s} {cy - 50 * s} L{cx + 110 * s} {cy} L{cx + 60 * s} {cy + 50 * s}" fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
            + line(cx + 22 * s, cy - 60 * s, cx - 22 * s, cy + 60 * s, NAVY, 12))


def map_panel(x, y, w=520, h=320):
    p = w / 3
    out = [path(f'M{x} {y + 20} L{x + p} {y} L{x + 2 * p} {y + 20} L{x + w} {y} L{x + w} {y + h - 20} L{x + 2 * p} {y + h} L{x + p} {y + h - 20} L{x} {y + h} Z', fill=WHITE, extra='stroke-width="4"'),
           f'<path d="M{x + p} {y} L{x + 2 * p} {y + 20} L{x + 2 * p} {y + h} L{x + p} {y + h - 20} Z" fill="{BG}"/>',
           line(x + p, y, x + p, y + h - 20), line(x + 2 * p, y + 20, x + 2 * p, y + h),
           f'<path d="M{x + 30} {y + h * 0.7} C{x + w * 0.3} {y + h * 0.5}, {x + w * 0.5} {y + h * 0.9}, {x + w - 30} {y + h * 0.35}" fill="none" stroke="{GOLD}" stroke-width="5" stroke-dasharray="4 12" stroke-linecap="round"/>']
    return ''.join(out)


def bricks(x, y, w=420):
    out = []
    rows = [(4, WHITE), (3, GOLD_L), (2, NAVY)]
    bh = 70
    for r_, (n, f) in enumerate(rows):
        rw = w - r_ * 100
        rx = x + r_ * 50
        bw = rw / n
        for c in range(n):
            out.append(rect(rx + c * bw + 4, y - r_ * (bh + 8), bw - 8, bh, fill=f, r=6))
    return ''.join(out)


def booklet(cx, cy):
    return (path(f'M{cx} {cy - 150} C{cx - 80} {cy - 180}, {cx - 200} {cy - 170}, {cx - 280} {cy - 140} L{cx - 280} {cy + 150} C{cx - 200} {cy + 120}, {cx - 80} {cy + 120}, {cx} {cy + 150} Z', fill=WHITE, extra='stroke-width="4"')
            + path(f'M{cx} {cy - 150} C{cx + 80} {cy - 180}, {cx + 200} {cy - 170}, {cx + 280} {cy - 140} L{cx + 280} {cy + 150} C{cx + 200} {cy + 120}, {cx + 80} {cy + 120}, {cx} {cy + 150} Z', fill=PAPER, extra='stroke-width="4"')
            + monogram(cx - 140, cy - 30, 70)
            + bar(cx - 220, cy + 70, 160, 10)
            + swatches(cx + 50, cy - 90, size=48, gap=12, colors=(NAVY, CORAL, GOLD))
            + bar(cx + 50, cy + 0, 180, 18, fill=NAVY)
            + bar(cx + 50, cy + 34, 150, 10)
            + bar(cx + 50, cy + 56, 170, 10))


# ---------- backdrop ----------

def backdrop(seed, animate=True):
    rnd = random.Random(seed)
    out = [f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    out.append(f'<g class="silk">')
    for i in range(3):
        y0 = rnd.uniform(120, 720)
        y1 = rnd.uniform(120, 720)
        c1 = (rnd.uniform(200, 500), rnd.uniform(-100, 900))
        c2 = (rnd.uniform(700, 1000), rnd.uniform(-100, 900))
        d = f'M-80 {y0:.0f} C{c1[0]:.0f} {c1[1]:.0f}, {c2[0]:.0f} {c2[1]:.0f}, 1280 {y1:.0f}'
        out.append(f'<path d="{d}" fill="none" stroke="{WHITE}" stroke-width="{rnd.choice([70, 110, 150])}" stroke-opacity="0.55" stroke-linecap="round"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    out.append('</g>')
    out.append(circle(CX + rnd.uniform(-180, 180), CY + rnd.uniform(-120, 60), 230, fill=GOLD_L, stroke=False, extra='fill-opacity="0.18"'))
    # editorial corner marks
    for (x, y) in [(40, 40), (W - 40, 40), (40, H - 40), (W - 40, H - 40)]:
        out.append(line(x - 10, y, x + 10, y, LINE, 2) + line(x, y - 10, x, y + 10, LINE, 2))
    return ''.join(out)


STYLE = ('<style>@media (prefers-reduced-motion: no-preference){'
         '.silk{animation:silk 4.5s cubic-bezier(.22,.61,.36,1) both}'
         '@keyframes silk{from{transform:translateX(-60px);opacity:0}to{transform:none;opacity:1}}}</style>')


def svg(body, seed, title):
    inner = backdrop(seed) + body
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title.replace(chr(39), '&#39;')}">'
    return head + STYLE + inner + '</svg>', head + inner + '</svg>'


# ---------- compositions ----------

ART = {
    'audits': [
        ('Website audit: a magnifying glass over a web page',
         window(250, 200, 620, 420, page_layout(250, 200, 620, 420)) + magnifier(800, 520, 120, check(800, 520, 2.4, CORAL, 9))),
        ('Layers of a website reviewed together',
         window(380, 150, 500, 330) + window(320, 230, 500, 330) + window(260, 310, 500, 330, page_layout(260, 310, 500, 330))
         + magnifier(880, 300, 80)),
        ('Speed gauge reading fast',
         gauge(600, 560, 300) + bar(420, 620, 360, 14, fill=NAVY) + bar(480, 650, 240, 10)),
        ('Search bar with your site ranked first',
         search_bar(270, 200, 660) + results(270, 320, 660)),
        ('Clipboard report with prioritised fixes',
         rect(380, 150, 440, 560, fill=WHITE, r=16) + rect(520, 120, 160, 60, fill=NAVY, r=12)
         + ''.join(circle(430, 270 + i * 90, 22, fill=GOLD_L) + bar(472, 262 + i * 90, 280 - i * 30, 14, fill=NAVY if i == 0 else LINE) for i in range(4))
         + check(760, 266, 1.2)),
        ('Envelope with the written audit report',
         doc(470, 150, 300, 340, lines=7) + envelope(400, 360, 440, 280, fill=PAPER) + circle(620, 540, 40, fill=CORAL)
         + circle(620, 540, 22, fill='none', extra=f'stroke="{PAPER}" stroke-width="3"')),
    ],
    'website-design-development': [
        ('A custom website layout with a pen nib',
         window(200, 170, 680, 470, page_layout(200, 170, 680, 470)) + nib(960, 520, 1.1)),
        ('Target with an arrow in the centre',
         circle(600, 440, 250, fill=WHITE, extra='stroke-width="4"') + circle(600, 440, 175, fill=PAPER) + circle(600, 440, 100, fill=GOLD_L)
         + circle(600, 440, 34, fill=CORAL) + arrow(930, 150, 612, 428, NAVY, 6, 30)
         + line(930, 150, 980, 120, GOLD, 6) + line(915, 135, 945, 90, GOLD, 6)),
        ('Colour swatches and a pen nib for a one-of-a-kind design',
         swatches(260, 330, size=120, gap=24) + bar(260, 490, 300, 16, fill=NAVY) + bar(260, 520, 220, 10)
         + nib(900, 600, 1.3)),
        ('Hand-written code in a browser window',
         window(170, 170, 560, 470, code_lines(210, 260, [(0, 220, NAVY), (1, 300, CORAL), (2, 180, LINE), (2, 240, LINE), (1, 120, GOLD), (0, 260, NAVY), (1, 200, LINE), (1, 280, CORAL), (0, 140, NAVY), (0, 200, LINE)]))
         + brackets(910, 410, 1.2)),
        ('A key handed over with a finished site',
         window(200, 170, 520, 400, page_layout(200, 170, 520, 400)) + key(780, 520, 1.25)),
        ('Gift-wrapped deliverable',
         gift(470, 260, 260, 220) + doc(820, 350, 180, 230, lines=5) + doc(200, 380, 180, 200, lines=4, fill=PAPER)),
    ],
    'website-maintenance': [
        ('A website kept fresh with ongoing care',
         window(260, 180, 560, 420, page_layout(260, 180, 560, 420)) + circle(870, 560, 110, fill=WHITE) + refresh(870, 560, 62)),
        ('A plant growing out of a browser window',
         window(330, 420, 540, 260) + plant(600, 450, 1.25)),
        ('Shield with a check and a steady heartbeat',
         shield(600, 410, 1.5)
         + f'<path d="M160 640 L420 640 L460 580 L500 700 L540 610 L580 640 L620 640" fill="none" stroke="{CORAL}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
         + line(620, 640, 1040, 640, LINE, 5)),
        ('Calendar and clock for quick changes',
         calendar(300, 220, 380, 360) + clock(820, 520, 110)),
        ('Two chat bubbles, a direct line to one person',
         bubble(240, 220, 420, 150) + bubble(540, 440, 420, 150, fill=CORAL, tail_left=False, dot_color=PAPER)),
        ('Checklist of what maintenance covers',
         rect(330, 170, 540, 520, fill=WHITE, r=16) + checklist(390, 240, 360, rows=6, done=6)
         + circle(880, 640, 70, fill=PAPER) + refresh(880, 640, 36)),
    ],
    'seo': [
        ('Search bar and rising results',
         search_bar(200, 170, 620) + chart_bars(240, 330, 520, 320, [0.25, 0.4, 0.55, 0.75, 0.95]) + pin(960, 560, 1.2)),
        ('Your result at the top, with a cursor clicking it',
         results(280, 210, 640, 4) + cursor(780, 230, 1.3)),
        ('Solid building blocks as SEO foundations',
         bricks(390, 560, 420) + line(240, 640, 960, 640, NAVY, 4)),
        ('A map with a pinned local business',
         map_panel(320, 280, 560, 340) + pin(640, 450, 1.3)),
        ('A line chart climbing steadily',
         line_chart(230, 200, 740, 420, [0.12, 0.2, 0.18, 0.35, 0.42, 0.6, 0.72, 0.9])),
        ('SEO checklist under a magnifying glass',
         rect(300, 180, 460, 480, fill=WHITE, r=16) + checklist(350, 240, 300, rows=6, done=4) + magnifier(830, 520, 100)),
    ],
    'ui-ux-design': [
        ('Interface across desktop and phone',
         window(180, 180, 640, 440, page_layout(180, 180, 640, 440)) + phone(820, 300, 170, 330,
             bar(850, 360, 110, 14, fill=NAVY) + bar(850, 390, 90, 8) + rect(850, 420, 110, 110, fill=BG, r=8, stroke=False) + rect(850, 548, 110, 30, fill=CORAL, r=6, stroke=False))),
        ('A cursor gliding effortlessly to a button',
         f'<path d="M240 620 C380 640, 420 360, 600 420 S820 300, 820 330" fill="none" stroke="{NAVY}" stroke-width="3" stroke-dasharray="4 14" stroke-linecap="round"/>'
         + rect(760, 280, 240, 90, fill=NAVY, r=45) + bar(820, 320, 120, 10, fill=PAPER) + cursor(860, 330, 1.2)
         + circle(240, 620, 12, fill=CORAL, stroke=False)),
        ('A person at the centre of the design',
         person(600, 520, 1.5) + bubble(220, 190, 200, 110, dots=False) + heart(320, 245, 1.0)
         + bubble(800, 170, 200, 110, fill=NAVY, tail_left=False, dots=False) + check(900, 225, 1.4, PAPER, 6)),
        ('Wireframe becoming a finished interface',
         rect(170, 200, 360, 440, fill='none', r=12, extra='stroke-dasharray="8 10"')
         + ''.join(rect(200, 230 + i * 130, 300, 110, fill='none', r=6, extra='stroke-dasharray="4 8"') + line(200, 230 + i * 130, 500, 340 + i * 130, LINE, 2) + line(500, 230 + i * 130, 200, 340 + i * 130, LINE, 2) for i in range(3))
         + arrow(560, 420, 640, 420, CORAL, 6, 20)
         + window(670, 200, 380, 440, page_layout(670, 200, 380, 440))),
        ('Phone, tablet and desktop',
         window(140, 180, 560, 400, page_layout(140, 180, 560, 400)) + rect(700, 300, 260, 350, r=22) + bar(730, 340, 180, 14, fill=NAVY) + rect(730, 380, 200, 140, fill=BG, r=8, stroke=False) + bar(730, 540, 150, 8)
         + phone(930, 380, 140, 270, rect(948, 430, 104, 104, fill=GOLD_L, r=8, stroke=False) + rect(948, 550, 104, 26, fill=CORAL, r=6, stroke=False))),
        ('A tidy component sheet',
         rect(220, 160, 760, 520, fill=WHITE, r=18)
         + rect(270, 210, 200, 64, fill=NAVY, r=32, stroke=False) + rect(500, 210, 200, 64, fill=WHITE, r=32)
         + toggle(740, 222) + toggle(840, 222, on=False)
         + rect(270, 320, 430, 64, fill=PAPER, r=10) + bar(296, 347, 160, 10)
         + swatches(740, 320, size=64, gap=12, colors=(NAVY, CORAL, GOLD))
         + rect(270, 430, 200, 200, fill=BG, r=12, stroke=False) + rect(500, 430, 200, 200, fill=BG, r=12, stroke=False)
         + checklist(740, 440, 160, rows=3, done=2)),
    ],
    'ecommerce-integrations': [
        ('An online storefront and shopping bag',
         window(200, 170, 620, 460, ''.join(rect(240 + i * 190, 270, 160, 200, fill=BG, r=10, stroke=False) + bar(240 + i * 190, 490, 120, 10, fill=NAVY) + bar(240 + i * 190, 512, 60, 10, fill=CORAL) for i in range(3)))
         + bag(840, 380)),
        ('Product cards with price tags',
         ''.join(rect(180 + i * 290, 230, 250, 360, fill=WHITE, r=14) + rect(200 + i * 290, 250, 210, 200, fill=[GOLD_L, BG, PAPER][i], r=10, stroke=False)
                 + circle(305 + i * 290, 350, 50, fill=[CORAL, NAVY, GOLD][i], stroke=False)
                 + bar(200 + i * 290, 475, 150, 12, fill=NAVY) + rect(200 + i * 290, 520, 100, 40, fill=CORAL if i == 1 else PAPER, r=20) for i in range(3))),
        ('A card payment completing at checkout',
         card(230, 220, 420, 260) + rect(560, 470, 420, 110, fill=NAVY, r=55) + check(770, 525, 1.8, PAPER, 8)),
        ('Your tools all connected',
         nodes(600, 430, 260, 6)),
        ('A simple dashboard that is easy to run',
         window(220, 170, 760, 480, rect(260, 250, 300, 360, fill=PAPER, r=10) + ''.join(toggle(290, 290 + i * 80, i != 2) + bar(390, 304 + i * 80, 140, 10) for i in range(4))
                + chart_bars(600, 260, 340, 330, [0.35, 0.5, 0.45, 0.7, 0.85]))),
        ('A finished order: bag and receipt',
         doc(320, 190, 250, 420, lines=9) + bag(620, 330, 260, 280)),
    ],
    'brand-redesign': [
        ('A brand identity: seal, swatches and business card',
         monogram(380, 380, 150) + card(560, 260, 400, 240) + swatches(560, 560, size=70, gap=16)),
        ('An outgrown brand replaced with one that fits',
         rect(170, 260, 340, 260, fill=PAPER, r=14, extra='stroke-dasharray="8 10" opacity="0.6"') + circle(340, 390, 70, fill=LINE, stroke=False)
         + arrow(550, 390, 650, 390, CORAL, 6, 22)
         + rect(690, 260, 340, 260, fill=WHITE, r=14) + monogram(860, 390, 90)),
        ('A complete brand board',
         rect(200, 150, 800, 560, fill=WHITE, r=18) + monogram(380, 330, 110)
         + swatches(560, 230, size=80, gap=16) + bar(560, 360, 360, 22, fill=NAVY) + bar(560, 400, 280, 14, fill=MUTED) + bar(560, 430, 320, 10)
         + ''.join(rect(260 + i * 130, 520, 100, 100, fill=[PAPER, GOLD_L, PAPER, CORAL, PAPER][i], r=50 if i % 2 else 14) for i in range(5))),
        ('A pen drawing a single flowing line',
         f'<path d="M180 560 C320 300, 460 680, 620 470 S880 260, 980 360" fill="none" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>'
         + f'<path d="M180 600 C330 360, 470 720, 630 510" fill="none" stroke="{CORAL}" stroke-width="4" stroke-linecap="round" stroke-opacity="0.7"/>'
         + nib(980, 360, 1.1)),
        ('The same identity on a card, a phone and a bag',
         card(150, 300, 360, 220) + phone(560, 240, 180, 360, monogram(650, 390, 60) + bar(600, 480, 100, 10)) + bag(820, 340, 240, 270, fill=NAVY)
         + circle(940, 520, 34, fill=GOLD_L, stroke=False)),
        ('Open brand guidelines book',
         booklet(600, 430)),
    ],
    'digital-infrastructure': [
        ('Domain, hosting and email connected',
         globe(330, 400, 140) + server(600, 250, 300, 70, 3) + envelope(700, 540, 260, 170)
         + line(470, 400, 600, 330, NAVY, 3, 'stroke-dasharray="2 10"') + line(470, 430, 700, 600, NAVY, 3, 'stroke-dasharray="2 10"')),
        ('A website resting on foundations underneath',
         window(380, 120, 440, 280, page_layout(380, 120, 440, 280)) + line(140, 460, 1060, 460, NAVY, 5)
         + nodes(600, 630, 170, 5, center_fill=GOLD_L)),
        ('Your own domain with email',
         rect(220, 220, 760, 90, r=45, extra='stroke-width="4"') + rect(260, 248, 30, 36, fill=GOLD, r=4) + bar(320, 260, 300, 14, fill=NAVY) + bar(640, 260, 140, 14, fill=CORAL)
         + envelope(330, 380, 340, 230, fill=WHITE) + globe(840, 500, 110)),
        ('Fast, reliable hosting',
         server(380, 280, 440, 90, 3) + arrow(940, 600, 940, 260, CORAL, 6, 26) + arrow(1010, 600, 1010, 320, GOLD, 6, 22)),
        ('A plug and socket, everything wired up',
         rect(160, 340, 260, 180, r=20) + circle(260, 430, 18, fill=NAVY, stroke=False) + circle(330, 430, 18, fill=NAVY, stroke=False)
         + f'<path d="M420 430 C560 430, 560 600, 700 600" fill="none" stroke="{NAVY}" stroke-width="8" stroke-linecap="round"/>'
         + rect(700, 540, 200, 120, fill=CORAL, r=18) + rect(900, 570, 60, 18, fill=GOLD, r=4) + rect(900, 612, 60, 18, fill=GOLD, r=4)
         + circle(960, 300, 46, fill=GOLD_L) + check(960, 300, 1.6, NAVY, 6)),
        ('Folder of logins, records and keys handed over',
         path('M260 260 L470 260 L510 300 L940 300 L940 640 L260 640 Z', fill=GOLD_L, extra='stroke-width="4"')
         + doc(330, 200, 240, 300, lines=6) + doc(600, 220, 240, 280, lines=5, fill=PAPER)
         + rect(260, 380, 680, 260, fill=WHITE, r=10) + key(420, 510, 0.9) + checklist(700, 440, 160, rows=3, done=3)),
    ],
}

ABOUT = ('A designer\'s desk: website on screen, swatches, pen and plant',
         window(160, 160, 600, 440, page_layout(160, 160, 600, 440))
         + swatches(820, 200, size=60, gap=14, colors=(NAVY, CORAL, GOLD))
         + nib(900, 640, 0.9)
         + rect(1000, 520, 110, 120, fill=WHITE, r=10) + plant(1055, 530, 0.6)
         + monogram(880, 380, 70))


def silk_hero():
    """Original silk-wave background, replaces the old stock image."""
    w, h = 1920, 1080
    rnd = random.Random(7)
    bands = []
    for i in range(7):
        y0 = 200 + i * 110 + rnd.uniform(-60, 60)
        y1 = 100 + i * 140 + rnd.uniform(-80, 80)
        d = (f'M-200 {y0:.0f} C{rnd.uniform(300, 700):.0f} {y0 - rnd.uniform(200, 420):.0f}, '
             f'{rnd.uniform(1100, 1500):.0f} {y1 + rnd.uniform(200, 420):.0f}, 2120 {y1:.0f}')
        bands.append((d, rnd.choice([90, 140, 200, 260]), rnd.uniform(0.35, 0.75)))
    body = [f'<rect x="-200" y="-200" width="{w + 400}" height="{h + 400}" fill="#DEDBD4"/>']
    for k, (d, sw, op) in enumerate(bands):
        body.append(f'<g class="b b{k % 3}"><path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="{sw}" stroke-opacity="{op:.2f}" stroke-linecap="round"/>'
                    f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.9"/></g>')
    style = ('<style>@media (prefers-reduced-motion: no-preference){'
             '.b{animation:drift 4.8s cubic-bezier(.22,.61,.36,1) both}'
             '.b1{animation-delay:.15s}.b2{animation-delay:.3s}'
             '@keyframes drift{from{transform:translate(-90px,24px);opacity:0}to{transform:none;opacity:1}}}</style>')
    head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
    defs = '<defs><filter id="soft" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="18"/></filter></defs>'
    g = f'<g filter="url(#soft)">{"".join(body)}</g>'
    return head + style + defs + g + '</svg>', head + defs + g + '</svg>'


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FIG, exist_ok=True)
    seed = 1
    manifest = []
    for svc, items in ART.items():
        for i, (title, body) in enumerate(items):
            web, fig = svg(body, seed, title)
            seed += 1
            name = f'{svc}-{i}.svg'
            open(os.path.join(OUT, name), 'w', encoding='utf-8').write(web)
            open(os.path.join(FIG, name), 'w', encoding='utf-8').write(fig)
            manifest.append(name)
    web, fig = svg(ABOUT[1], 99, ABOUT[0])
    open(os.path.join(OUT, 'about-studio.svg'), 'w', encoding='utf-8').write(web)
    open(os.path.join(FIG, 'about-studio.svg'), 'w', encoding='utf-8').write(fig)
    web, fig = silk_hero()
    open(os.path.join(OUT, 'silk.svg'), 'w', encoding='utf-8').write(web)
    open(os.path.join(FIG, 'silk.svg'), 'w', encoding='utf-8').write(fig)
    print(f'{len(manifest) + 2} illustrations written')


if __name__ == '__main__':
    main()
