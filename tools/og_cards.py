#!/usr/bin/env python3
"""Branded 1200x675 share cards (X / Open Graph) for AFNS articles. Requires Pillow.
Called automatically by build.py; can also be run alone:  python3 tools/og_cards.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"
W, H = 1200, 675
NAVY, NAVY2 = (10, 22, 48), (22, 40, 86)
GOLD, RED, WHITE = (201, 162, 74), (200, 32, 47), (255, 255, 255)
FOOTER_URL = "amclips.github.io/AFNS"

def font(name, size, weight):
    f = ImageFont.truetype(str(FONTS / name), size)
    try: f.set_variation_by_name(weight)
    except Exception: pass
    return f

def oswald(size, w="Bold"): return font("Oswald-VariableFont_wght.ttf", size, w)
def inter(size, w="SemiBold"): return font("Inter-VariableFont.ttf", size, w)

_BASE = None
def base():
    """Background shared by every card: navy gradient, faded flag on the right, eagle watermark."""
    global _BASE
    if _BASE is not None: return _BASE.copy()
    bg = Image.new("RGB", (W, H), NAVY)
    grad = Image.linear_gradient("L").rotate(90).resize((W, H))      # 0 left -> 255 right
    bg = Image.composite(Image.new("RGB", (W, H), NAVY2), bg, grad.point(lambda v: int(v * .55)))
    # flag from the brand banner (top-right of hero-banner.jpg), faded in from the right
    ban = Image.open(ROOT / "assets" / "hero-banner.jpg").convert("RGB")
    bw, bh = ban.size
    flag = ban.crop((int(bw * .815), int(bh * .17), bw, int(bh * .78))).resize((560, H), Image.LANCZOS)
    flag = flag.filter(ImageFilter.GaussianBlur(2))
    mask = Image.linear_gradient("L").rotate(90).resize((560, H)).point(lambda v: int(v * .30))
    bg.paste(flag, (W - 560, 0), mask)
    # eagle badge watermark, large and faint
    logo = Image.open(ROOT / "assets" / "logo-512.png").convert("RGBA").resize((620, 620), Image.LANCZOS)
    a = logo.getchannel("A").point(lambda v: int(v * .10))
    bg.paste(logo.convert("RGB"), (W - 480, 40), a)
    d = ImageDraw.Draw(bg)
    d.rectangle((0, 0, W, 8), fill=GOLD)
    # bottom stripe red / white / navy-blue
    y = H - 64
    d.rectangle((0, y, W, H), fill=(6, 14, 32))
    d.rectangle((0, y, W // 3, y + 4), fill=RED); d.rectangle((W // 3, y, 2 * W // 3, y + 4), fill=WHITE)
    d.rectangle((2 * W // 3, y, W, y + 4), fill=(40, 70, 150))
    # header: logo + wordmark
    sm = Image.open(ROOT / "assets" / "logo-192.png").convert("RGBA").resize((92, 92), Image.LANCZOS)
    bg.paste(sm, (60, 44), sm)
    d.text((168, 46), "AFNS", font=oswald(50), fill=WHITE)
    d.text((170, 110), "AMERICA FIRST NEWS SYNDICATE", font=oswald(20, "Medium"), fill=GOLD, spacing=0)
    _BASE = bg
    return bg.copy()

def tracked(d, xy, text, f, fill, track):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + track
    return x

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def make_card(title, desk_name, status, out_path):
    im = base(); d = ImageDraw.Draw(im)
    x0, maxw = 60, 1000
    # desk label + status badge
    y = 186
    d.rectangle((x0, y + 4, x0 + 5, y + 30), fill=RED)
    xe = tracked(d, (x0 + 18, y), desk_name.upper(), oswald(27, "SemiBold"), GOLD, 3)
    if status:
        bf = inter(19, "Bold"); label = status.upper()
        tw = d.textlength(label, font=bf)
        bx = xe + 18
        d.rounded_rectangle((bx, y + 1, bx + tw + 28, y + 35), radius=5, fill=RED)
        d.text((bx + 14, y + 6), label, font=bf, fill=WHITE)
    # headline: largest size that fits in 4 lines
    top, bottom = 250, H - 84
    for size in range(78, 39, -2):
        f = oswald(size, "Bold"); lh = int(size * 1.14)
        lines = wrap(d, title, f, maxw)
        if len(lines) * lh <= bottom - top and len(lines) <= 4: break
    if len(lines) > 4:   # very long headline: truncate
        lines = lines[:4]; lines[-1] = lines[-1].rstrip(" ,.;:") + "…"
    for i, ln in enumerate(lines):
        d.text((x0, top + i * lh), ln, font=f, fill=WHITE)
    # footer
    d.text((x0, H - 46), FOOTER_URL, font=inter(22, "SemiBold"), fill=(215, 222, 235))
    tag = "AMERICA FIRST. TRUTH FIRST. AMERICA ALWAYS."
    tf = oswald(18, "Medium")
    tracked(d, (W - 60 - d.textlength(tag, font=tf) - len(tag) * 2, H - 44), tag, tf, GOLD, 2)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(out_path, optimize=True)
    return out_path

if __name__ == "__main__":
    import sys; sys.path.insert(0, str(ROOT))
    import build
    for a in build.load_articles():
        if not a["sample"]:
            print(make_card(a["title"], build.DESKS[a["desk"]]["name"], a["status"], ROOT / "static" / "og" / f"{a['slug']}.png"))
