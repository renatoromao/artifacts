"""Microsoft Web IQ - LinkedIn image: light glow + dark terminal listing every Web IQ call.
Only calls/params documented by Microsoft (Tech Community Ignite 2026 post, Learn pricing)."""
import os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = "/home/claude/artifacts"
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono"
def mono(s, b=False): return ImageFont.truetype(MONO + ("-Bold" if b else "") + ".ttf", s)
INK=(15,23,42); BLUE=(0,85,204); BLUE3=(102,163,255); GRAY=(100,116,139)
TERM=(13,17,23); TBAR=(30,35,45); TXT=(226,232,240); DIM=(110,120,140); GREEN=(39,201,63); AMBER=(245,158,11)

ROWS = [("#", "Microsoft Web IQ  ·  REST · SDK · MCP", None),
        ("Auto", "multi-source, cited passages", "GA"),
        ("Auto mode=advanced", "iterative retrieval", "GA"),
        ("/web", "ranked web results", "GA"),
        ("/news", "fresh news, source attribution", "GA"),
        ("/images", "image search + metadata", "GA"),
        ("/video", "video search", "GA"),
        ("/browse", "content from a live URL", "GA"),
        ("Places", "207M+ places, 200+ markets", "GA"),
        ("Weather", "via Auto: forecasts, warnings", "GA"),
        ("Commerce", "40B+ offers", "PRIVATE PREVIEW"),
        ("#", "params", None),
        ("responseFilter", "limit evidence types", None),
        ("maxResponseLength", "cap the payload", None),
        ("scopeName", "allow/block site lists", None),
        ("failOnMissingScope", "fail closed", None),
        ("scopeApplied", "proof in the response", None)]

def terminal(w, fs=27):
    lh = int(fs * 1.72); h = 60 + 30 + lh * len(ROWS) + 22
    im = Image.new("RGB", (w, h), TERM); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 60), fill=TBAR)
    for i, c in enumerate([(255,95,86),(255,189,46),(39,201,63)]): d.ellipse((24+i*34, 20, 44+i*34, 40), fill=c)
    d.text((w/2, 30), "web-iq — api.microsoft.ai", font=font("Medium", 24), fill=(148,163,184), anchor="mm")
    y = 90; B, R = mono(fs, True), mono(fs); kx = 34 + d.textlength("$ ", font=B); dx = kx + 400
    for k, desc, tag in ROWS:
        if k == "#":
            d.text((34, y), "# " + desc, font=R, fill=DIM); y += lh; continue
        if k[0] in "/" or k[0].isupper(): d.text((34, y), "$", font=B, fill=GREEN)
        if "mode=" in k:
            a, b = k.split(" "); d.text((kx, y), a, font=B, fill=BLUE3)
            d.text((kx + d.textlength(a + " ", font=B), y), b, font=R, fill=(255,255,255))
        else:
            d.text((kx, y), k, font=B, fill=BLUE3 if (k[0] == "/" or k[0].isupper()) else (255,255,255))
        d.text((dx, y), desc, font=R, fill=TXT)
        if tag:
            col = GREEN if tag == "GA" else AMBER; tf = font("SemiBold", 20); tw = d.textlength(tag, font=tf) + 22
            d.rounded_rectangle((w-30-tw, y, w-30, y+32), 16, outline=col, width=2)
            d.text((w-30-tw/2, y+16), tag, font=tf, fill=col, anchor="mm")
        y += lh
    return im

def rounded(img, r=26, border=(51,65,85)):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle((0,0,img.width-1,img.height-1), r, fill=255)
    out = Image.new("RGBA", img.size, (0,0,0,0)); out.paste(img, (0,0), m)
    ImageDraw.Draw(out).rounded_rectangle((0,0,img.width-1,img.height-1), r, outline=border, width=2); return out

def rich(d, x, y, text, f, lh, maxw):
    toks = []
    for part in re.split(r"(\*[^*]+\*)", text):
        for w in part.strip("*").split(): toks.append((w, part.startswith("*")))
    lines, cur, sp = [], [], d.textlength(" ", font=f)
    for w, a in toks:
        if cur and sum(d.textlength(t, font=f)+sp for t,_ in cur) + d.textlength(w, font=f) > maxw: lines.append(cur); cur = []
        cur.append((w, a))
    lines.append(cur)
    for ln in lines:
        cx = x
        for w, a in ln: d.text((cx, y), w, font=f, fill=BLUE if a else INK); cx += d.textlength(w, font=f) + sp
        y += lh
    return y

W, H, M = 1200, 1500, 70
g = Image.new("RGB", (W, H), "white"); gd = ImageDraw.Draw(g)
gd.ellipse((W-520, -420, W+380, 380), fill=(214,230,255)); gd.ellipse((-460, H-300, 360, H+380), fill=(232,240,255))
im = g.filter(ImageFilter.GaussianBlur(150)); d = ImageDraw.Draw(im)
y = rich(d, M, 80, "Web IQ commands *for agents.*", font("ExtraBold", 74), 86, W-2*M) + 40
T = terminal(W - 2*M)
sh = Image.new("RGBA", (T.width+120, T.height+120), (0,0,0,0))
ImageDraw.Draw(sh).rounded_rectangle((60,76,T.width+60,T.height+70), 26, fill=(0,60,160,70))
sh = sh.filter(ImageFilter.GaussianBlur(26)); im.paste(sh, (M-60, y-60), sh)
t = rounded(T); im.paste(t, (M, y), t)
im = im.crop((0, 0, W, min(H, y + T.height + 130))); d = ImageDraw.Draw(im); Hc = im.height
d.text((M, Hc-62), "@renatoromao", font=font("SemiBold", 30), fill=GRAY)
d.text((W-M, Hc-62), "Microsoft Ignite 2026", font=font("Medium", 28), fill=GRAY, anchor="ra")
out = f"{ROOT}/linkedin/2026-11-23-web-iq"; os.makedirs(out, exist_ok=True)
im.save(f"{out}/image.jpg", quality=94); print(im.size, y + T.height)
