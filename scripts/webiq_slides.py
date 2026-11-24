"""Microsoft Web IQ (Ignite 2026) - tweet-card Instagram carousel (PT).
Content only from official Microsoft sources (Tech Community, Azure blog, Learn, microsoft.com/webiq).
Usage: python webiq_slides.py <structured.png> <header.png>"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "/home/claude/artifacts"
STRUCT = Image.open(sys.argv[1]).convert("RGB")
HEADER = Image.open(sys.argv[2]).convert("RGB")
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono"
def mono(s, b=False): return ImageFont.truetype(MONO + ("-Bold" if b else "") + ".ttf", s)

INK = (15, 23, 42); BLUE3 = (102, 163, 255); GRAY = (100, 116, 139)
TERM = (13, 17, 23); TBAR = (30, 35, 45); TXT = (226, 232, 240); DIM = (110, 120, 140)
GREEN = (39, 201, 63); AMBER = (245, 158, 11)

def rounded(img, r=26, border=(226, 232, 240)):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0)); out.paste(img, (0, 0), m)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r, outline=border, width=2)
    return out

def window(rows, w, title, fs=28, keyw=None):
    """rows: list of (key, desc, tag) ; key in blue bold mono, desc in light, tag pill (GA/preview)."""
    lh = int(fs * 1.9)
    h = 60 + 30 + lh * len(rows) + 24
    im = Image.new("RGB", (w, h), TERM); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 60), fill=TBAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((24 + i * 34, 20, 44 + i * 34, 40), fill=c)
    d.text((w / 2, 30), title, font=font("Medium", 24), fill=(148, 163, 184), anchor="mm")
    y = 90; B, R = mono(fs, True), mono(fs)
    kw = keyw or max(d.textlength(k, font=B) for k, _, _ in rows if k) + 30
    for k, desc, tag in rows:
        if k.startswith("#"):
            d.text((32, y), k, font=R, fill=DIM); y += lh; continue
        d.text((32, y), k, font=B, fill=BLUE3)
        d.text((32 + kw, y), desc, font=R, fill=TXT)
        if tag:
            col = GREEN if tag == "GA" else AMBER
            tf = font("SemiBold", 22); tw = d.textlength(tag, font=tf) + 24
            d.rounded_rectangle((w - 32 - tw, y - 2, w - 32, y + 36), 18, outline=col, width=2)
            d.text((w - 32 - tw / 2, y + 17), tag, font=tf, fill=col, anchor="mm")
        y += lh
    return im

def glow_scene(card, W, H, M=50):
    g = Image.new("RGB", (W, H), "white"); gd = ImageDraw.Draw(g)
    gd.ellipse((W - 520, -420, W + 380, 380), fill=(214, 230, 255))
    gd.ellipse((-460, H - 300, 360, H + 380), fill=(232, 240, 255))
    im = g.filter(ImageFilter.GaussianBlur(150))
    y = (H - card.height) // 2
    sh = Image.new("RGBA", (card.width + 120, card.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 76, card.width + 60, card.height + 70), 26, fill=(0, 60, 160, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(26)); im.paste(sh, (M - 60, y - 60), sh)
    t = rounded(card, border=(51, 65, 85)); im.paste(t, (M, y), t)
    return im

def tweet_slide(header, paras, img, path, src=None, framed=True):
    W, H, M = 1080, 1350, 64
    im = Image.new("RGB", (W, H), "white"); im.paste(header, (0, 0)); d = ImageDraw.Draw(im)
    y = 228
    for txt in paras:
        bold = txt.startswith("**"); txt = txt.strip("*")
        f = font("Bold" if bold else "Regular", 44)
        line = ""
        for w in txt.split():
            t = (line + " " + w).strip()
            if d.textlength(t, font=f) > W - 2 * M: d.text((M, y), line, font=f, fill=(15, 20, 25)); y += 58; line = w
            else: line = t
        d.text((M, y), line, font=f, fill=(15, 20, 25)); y += 58 + 24
    y += 6
    avail_h = H - y - (90 if src else 50); avail_w = W - 2 * M
    r = min(avail_w / img.width, avail_h / img.height, 1.6)
    pic = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    p = rounded(pic, 24) if framed else pic.convert("RGBA")
    im.paste(p, (M, y), p)
    if src: d.text((M, y + pic.height + 16), src, font=font("Regular", 26), fill=(110, 118, 125))
    im.convert("RGB").save(path, quality=92)

LW = 948
# slide 1: LinkedIn-image style scene (light glow + dark terminal with blue calls)
S1 = glow_scene(window([("# Microsoft Web IQ · REST · SDK · MCP", "", None),
                        ("Auto", "one call, cited passages", "GA"),
                        ("  mode", "advanced  (iterative)", "GA"),
                        ("/web /news", "ranked + citations", "GA"),
                        ("/images /video", "with metadata", "GA"),
                        ("/browse", "live URL extraction", "GA")],
                       848, "web-iq — api.microsoft.ai", fs=25, keyw=290), 948, 660)
# slide 2: endpoint menu
S2 = window([("Auto", "picks sources, 1 call", "GA"),
             ("  mode", "advanced", "GA"),
             ("/web", "web pages", "GA"),
             ("/news", "fresh news", "GA"),
             ("/images", "images + metadata", "GA"),
             ("/video", "video search", "GA"),
             ("/browse", "content from a URL", "GA"),
             ("Places", "207M+ places", "GA"),
             ("Weather", "via Auto", "GA"),
             ("Commerce", "40B+ offers", "private preview")],
            LW, "Web IQ — calls", fs=26, keyw=200)
# slide 4: scopes / governance
S4 = window([("# Scopes: include + exclude lists", "", None),
             ("scopeName", "your named scope", None),
             ("failOnMissingScope", "fail closed", None),
             ("scopeApplied", "proof in response", None),
             ("# up to 10,000 + 10,000 selectors", "", None),
             ("# exclusion wins over inclusion", "", None),
             ("Web / News", "", "GA"),
             ("Auto", "", "preview")],
            LW, "Web IQ — governance", fs=26, keyw=360)

SLIDES = [
 (["**Seus agentes agora buscam na web com citação e governança, via API.**",
   "Microsoft Web IQ está disponível para todos os clientes Azure. Sem waitlist."], S1, None, True),
 (["Em vez de uma busca genérica, você escolhe a chamada certa.",
   "Auto escolhe as fontes numa chamada só. Com mode advanced, faz recuperação iterativa.",
   "**/browse extrai o conteúdo de uma URL. É a chamada mais barata.**"], S2, None, True),
 (["Não é só página da web: Places (207M+ lugares), Weather e Commerce (private preview).",
   "**E dá para trazer o seu conteúdo licenciado (BYOL) para o mesmo ranking.**"], STRUCT, "Imagem: Microsoft", True),
 (["O detalhe que eu mostraria para um CISO: Scopes.",
   "Listas de sites permitidos e bloqueados, direto na camada de busca.",
   "**Com failOnMissingScope, o agente falha fechado em vez de cair na web aberta.**"], S4, None, True),
 (["GA: Auto, Auto Advanced, Web, News, Images, Video, Browse, Places e Weather. Commerce em private preview.",
   "**A partir de $1 por 1K chamadas (Browse). Exige assinatura Azure paga.**"], HEADER, "Imagem: Microsoft", True),
]

SLUG = "2026-11-23-web-iq"
HDR = Image.open(f"{ROOT}/instagram/2026-11-18-cowork-subagents/slide1.jpg").crop((0, 0, 1080, 205))
out = f"{ROOT}/instagram/{SLUG}"; os.makedirs(out, exist_ok=True)
for i, (paras, img, src, framed) in enumerate(SLIDES, 1):
    tweet_slide(HDR, paras, img, f"{out}/slide{i}.jpg", src, framed)
print("ok", out)
