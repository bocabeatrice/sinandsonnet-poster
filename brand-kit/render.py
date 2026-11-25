"""
Sin & Sonnet post renderer.

This is the brand template used for the weekly Instagram / Facebook / TikTok
mock-ups. Import it, define that week's posts, call build().

    import sys; sys.path.insert(0, 'brand-kit')
    from render import *
    P = {}
    P['1a'] = ('ink', FEED, kicker('the library','ink') + head('House<br>rules','ink',120), {'sym':170})
    build(P, outdir='out')
    sheet(['1a','1b'], 'preview.png', outdir='out')

Everything it needs (fonts, symbol art) lives in this folder. No downloads,
no installs. Requires playwright (preinstalled) and Pillow (preinstalled).

DO NOT change the colours, fonts, logo lockup or @handle placement without
Sharon's say-so -- they are the brand. See the Brand Bible project doc.
"""
import os, sys, base64

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rsym import rsym  # noqa: E402

# ---------------------------------------------------------------- fonts
_FONTS = os.path.join(HERE, 'fonts')


def _face(name, filename, style='normal'):
    b = base64.b64encode(open(os.path.join(_FONTS, filename), 'rb').read()).decode()
    return (f"@font-face{{font-family:'{name}';font-style:{style};"
            f"font-weight:100 900;src:url(data:font/ttf;base64,{b})}}")


CSS = '<style>' + \
    _face('Mont', 'Montserrat[wght].ttf') + \
    _face('Corm', 'Cormorant-Italic[wght].ttf', 'italic') + \
    _face('CormR', 'Cormorant[wght].ttf') + \
    _face('Jost', 'Jost[wght].ttf') + '''
html,body{margin:0}
*{box-sizing:border-box}
.m{font-family:Mont;font-weight:200;text-transform:uppercase;letter-spacing:.09em}
.c{font-family:Corm;font-style:italic;font-weight:400}
.j{font-family:Jost;font-weight:400;text-transform:uppercase;letter-spacing:.3em}
</style>'''

# ---------------------------------------------------------------- colours
INK = '#141217'      # near-black
IV = '#F4EFE6'       # ivory
ROSE = '#C24A5F'      # rose accent (on dark)
BUR = '#6E1F2E'      # burgundy
GOLD = '#B08D57'      # hairline rule
BG2 = '#5A1626'      # deep burgundy background
GREY = '#4A4450'
BLUSH = '#E8B4BE'

# palette name -> (background, text, accent, subtext, symbol palette)
PAL = {
    'ink':   (INK, IV, ROSE, '#CFC3B2', 'dark'),
    'ivory': (IV, INK, BUR, GREY, 'light'),
    'bur':   (BG2, IV, BLUSH, '#E9D6C8', 'burg'),
}

# canvas sizes
FEED = (1080, 1350)   # grid / carousel (4:5)
STORY = (1080, 1920)  # story / reel (9:16)
F = FEED              # short aliases, as used in week1
S = STORY


# ---------------------------------------------------------------- pieces
def mark(fg, amp, size=30):
    """The SIN & SONNET wordmark. Burgundy ampersand larger than the words."""
    return (f'<div class="m" style="font-size:{size}px;color:{fg};white-space:nowrap">SIN '
            f'<span class="c" style="text-transform:none;letter-spacing:0;'
            f'font-size:{size*1.6}px;color:{amp};vertical-align:-.12em">&amp;</span> SONNET</div>')


def foot(p, w):
    """Wordmark + hairline + @sinandsonnet, pinned to the bottom."""
    bg, fg, acc, sub, _ = PAL[p]
    return (f'<div style="position:absolute;bottom:70px;left:0;width:{w}px;display:flex;'
            f'flex-direction:column;align-items:center;gap:14px">{mark(fg, acc, 28)}'
            f'<span style="width:120px;height:1.5px;background:{GOLD}"></span>'
            f'<div class="j" style="font-size:15px;color:{sub}">@sinandsonnet</div></div>')


def page(p, w, h, inner, footer=True, sym=None):
    bg, fg, acc, sub, sp = PAL[p]
    top = ''
    if sym:
        top = (f'<div style="position:absolute;top:80px;left:0;width:{w}px;display:flex;'
               f'justify-content:center">{rsym("R1", sp, sym)}</div>')
    return (f'<!doctype html><meta charset="utf-8">{CSS}'
            f'<body style="width:{w}px;height:{h}px;background:{bg};color:{fg};'
            f'position:relative;overflow:hidden">{top}'
            f'<div style="position:absolute;inset:0;display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center;text-align:center;padding:0 110px">'
            f'{inner}</div>{foot(p, w) if footer else ""}</body>')


def kicker(t, p):
    """Small spaced label above the headline."""
    return f'<div class="j" style="font-size:22px;color:{PAL[p][3]};margin-bottom:46px">{t}</div>'


def rule():
    """Gold hairline divider."""
    return (f'<span style="display:block;width:140px;height:1.5px;background:{GOLD};'
            f'margin:46px auto"></span>')


def head(t, p, s=86):
    """Montserrat ExtraLight uppercase headline. <br> for line breaks."""
    return f'<div class="m" style="font-size:{s}px;line-height:1.18;color:{PAL[p][1]}">{t}</div>'


def ital(t, p, s=96):
    """Cormorant italic accent line, in the palette's accent colour."""
    return f'<div class="c" style="font-size:{s}px;line-height:1.05;color:{PAL[p][2]}">{t}</div>'


def small(t, p, s=30):
    """Jost body / caption line."""
    return (f'<div style="font-family:Jost;font-size:{s}px;line-height:1.5;'
            f'color:{PAL[p][3]};letter-spacing:.04em">{t}</div>')


def numeral(n, p, s=150):
    """Big italic numeral, for vote / listicle slides."""
    return (f'<div class="c" style="font-size:{s}px;color:{PAL[p][2]};line-height:1;'
            f'margin-bottom:40px">{n}</div>')


# ---------------------------------------------------------------- output
def build(posts, outdir='.', scale=1):
    """posts: {key: (palette, (w,h), inner_html, opts)}. Writes <key>.png into outdir.

    opts may contain 'sym': height in px of the ribbon-S mark at the top,
    and 'footer': False to drop the bottom lockup.
    """
    from playwright.sync_api import sync_playwright
    os.makedirs(outdir, exist_ok=True)
    written = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for k, (p, (w, h), inner, o) in posts.items():
            pg = b.new_page(viewport={'width': w, 'height': h})
            pg.set_content(page(p, w, h, inner,
                                footer=o.get('footer', True), sym=o.get('sym')))
            pg.wait_for_timeout(400)
            path = os.path.join(outdir, f'{k}.png')
            pg.screenshot(path=path)
            pg.close()
            written.append(path)
        b.close()
    return written


def sheet(keys, out, outdir='.', cols=5, tile=430, pad=26, bg='#17151A', label=True):
    """Contact sheet of several renders, for sending Sharon a preview."""
    from PIL import Image, ImageDraw
    ims = []
    for k in keys:
        im = Image.open(os.path.join(outdir, f'{k}.png')).convert('RGB')
        r = min(tile / im.width, (tile * 1.45) / im.height)
        ims.append((k, im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)))
    rows = (len(ims) + cols - 1) // cols
    cw = tile + pad
    ch = int(tile * 1.45) + pad + (34 if label else 0)
    canvas = Image.new('RGB', (cols * cw + pad, rows * ch + pad), bg)
    d = ImageDraw.Draw(canvas)
    for i, (k, im) in enumerate(ims):
        x = pad + (i % cols) * cw + (tile - im.width) // 2
        y = pad + (i // cols) * ch
        canvas.paste(im, (x, y))
        if label:
            d.text((pad + (i % cols) * cw + 4, y + im.height + 8), k, fill='#9A9099')
    canvas.save(out)
    return out
