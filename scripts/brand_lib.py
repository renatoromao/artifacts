"""Instagram carousel - Option 2 (brand style, renatoromao.com.br palette).
Dark navy background with blue glow, big bold headline with accent words,
image card, pill label, body text, footer handle + page counter."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, sys, re

R = "/tmp/claude-tool-results/90b4f830-5e60-5320-b7bc-33db32d1b29d/"

# Brand palette (renatoromao.com.br CSS vars)
NAVY = (2, 8, 23)          # --foreground 222.2 84% 4.9%
NAVY2 = (8, 22, 56)
PRIMARY = (0, 85, 204)     # --primary 215 100% 40%
GLOW = (51, 136, 255)      # --primary-glow 215 100% 60%
ACCENT = (102, 163, 255)   # 215 100% 70% (dark-mode glow) for text on navy
WHITE = (255, 255, 255)
MUTED = (148, 163, 184)

F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)
W, H, M = 1080, 1350, 72

def background():
    bg = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(bg)
    for y in range(H):  # vertical navy gradient
        t = y / H
        c = tuple(int(NAVY[i] * (1 - t) + NAVY2[i] * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((W - 520, -380, W + 380, 420), fill=PRIMARY)
    gd.ellipse((-420, H - 360, 380, H + 300), fill=(0, 45, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(170))
    return Image.blend(bg, Image.composite(glow, bg, glow.convert("L")), 0.85)

def rich_lines(d, text, f, maxw):
    """text with *accent* markup -> list of lines of (word, accent)"""
    toks = []
    for part in re.split(r"(\*[^*]+\*)", text):
        acc = part.startswith("*")
        for w in part.strip("*").split():
            toks.append((w, acc))
    lines, cur, sp = [], [], d.textlength(" ", font=f)
    for w, a in toks:
        test = sum(d.textlength(x, font=f) + sp for x, _ in cur) + d.textlength(w, font=f)
        if cur and test > maxw: lines.append(cur); cur = []
        cur.append((w, a))
    if cur: lines.append(cur)
    return lines

def draw_rich(d, x, y, text, f, lh, maxw, color=WHITE, acc=ACCENT, bold_acc=None):
    sp = d.textlength(" ", font=f)
    for line in rich_lines(d, text, f, maxw):
        cx = x
        for w, a in line:
            ff = bold_acc if (a and bold_acc) else f
            d.text((cx, y), w, font=ff, fill=acc if a else color)
            cx += d.textlength(w, font=ff) + sp
        y += lh
    return y

def card(im, img, x, y, w, h):
    r = max(w / img.width, h / img.height)
    pic = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    l, t = (pic.width - w) // 2, (pic.height - h) // 2
    pic = pic.crop((l, t, l + w, t + h))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), 28, fill=255)
    sh = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 50, w + 40, h + 50), 28, fill=(0, 40, 120, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(24))
    im.paste(sh, (x - 40, y - 40), sh)
    im.paste(pic, (x, y), mask)
    ImageDraw.Draw(im).rounded_rectangle((x, y, x + w - 1, y + h - 1), 28, outline=(255, 255, 255, 60), width=2)

def pill(d, x, y, text, maxw):
    f = font("SemiBold", 36)
    w = d.textlength(text, font=f) + 56
    w = min(w, maxw)
    d.rounded_rectangle((x, y, x + maxw, y + 72), 16, fill=(0, 85, 204, 90) if False else (14, 40, 92), outline=(51, 136, 255), width=2)
    d.text((x + maxw / 2, y + 36), text, font=f, fill=ACCENT, anchor="mm")
    return y + 72

def footer(d, n, total):
    f = font("Medium", 28)
    d.text((M, H - 70), "@renatoromaos", font=f, fill=MUTED)
    d.text((W - M, H - 70), f"{n:02d}/{total:02d}", font=f, fill=MUTED, anchor="ra")
    # progress dots
    cx = W / 2 - (total - 1) * 11
    for i in range(total):
        c = WHITE if i + 1 == n else (71, 85, 105)
        d.ellipse((cx + i * 22 - 5, H - 57 - 5, cx + i * 22 + 5, H - 57 + 5), fill=c)

def slide(n, total, title, img, pill_text=None, body=None, title_size=92, img_h=520, path=None):
    im = background(); d = ImageDraw.Draw(im, "RGBA")
    y = draw_rich(d, M, 110, title, font("ExtraBold", title_size), int(title_size * 1.12), W - 2 * M)
    y += 40
    if img is not None:
        cw = W - 2 * M
        nh = int(cw * img.height / img.width)
        if nh > img_h:
            nh = img_h; cw = int(nh * img.width / img.height)
        img_h = nh
        card(im, img, (W - cw) // 2, y, cw, img_h); d = ImageDraw.Draw(im, "RGBA")
        y += img_h + 36
    if pill_text:
        y = pill(d, M, y, pill_text, W - 2 * M) + 30
    if body:
        draw_rich(d, M, y, body, font("Regular", 42), 58, W - 2 * M, color=(226, 232, 240), acc=ACCENT, bold_acc=font("Bold", 42))
    footer(d, n, total)
    im.save(path, quality=92)

