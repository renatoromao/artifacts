"""Copilot Studio spending policies in the Microsoft 365 admin center (public preview).
Tweet-card carousels: Instagram (PT, own masked screenshots + 1 official image) and X (EN, official blog images only).
Usage: python copilot_studio_spending_limits_slides.py <frames_dir> <blog_img_dir>"""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "/home/claude/artifacts"
FR, BI = sys.argv[1], sys.argv[2]
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)

def rounded(img, r=24, border=(226, 232, 240)):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0)); out.paste(img, (0, 0), m)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r, outline=border, width=2)
    return out

def tweet_slide(header, paras, img, path, src=None):
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
    avail_h = H - y - (80 if src else 50); avail_w = W - 2 * M
    r = min(avail_w / img.width, avail_h / img.height, 1.6)
    pic = img.convert("RGB").resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    x = M + (avail_w - pic.width) // 2
    p = rounded(pic); im.paste(p, (x, y), p)
    if src: d.text((M, y + pic.height + 14), src, font=font("Regular", 26), fill=(110, 118, 125))
    im.save(path, quality=92)

def fr(n, box): return Image.open(f"{FR}/{n}.png").convert("RGB").crop(box)

def light_scene(card, W=948, H=620, M=40):
    glow = Image.new("RGB", (W, H), "white"); g = ImageDraw.Draw(glow)
    g.ellipse((W - 520, -420, W + 380, 380), fill=(214, 230, 255))
    g.ellipse((-460, H - 300, 360, H + 380), fill=(232, 240, 255))
    im = glow.filter(ImageFilter.GaussianBlur(120))
    r = (W - 2 * M) / card.width
    c = card.resize((W - 2 * M, int(card.height * r)), Image.LANCZOS)
    y = (H - c.height) // 2
    sh = Image.new("RGBA", (c.width + 120, c.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 76, c.width + 60, c.height + 70), 24, fill=(0, 60, 160, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(24)); im.paste(sh, (M - 60, y - 60), sh)
    t = rounded(c, border=(203, 213, 225)); im.paste(t, (M, y), t)
    return im

REVIEW = fr("s11", (930, 1098, 1780, 1341))
LIMITS = fr("s8", (909, 621, 2094, 1080))
SCOPE = fr("s4", (909, 378, 1827, 1179))
BILL = fr("s10", (909, 252, 2066, 1125))
BLOG = {k: Image.open(f"{BI}/{k}.png") for k in ["mac_overview", "scenario1", "billing_top", "cycle"]}

IG = [
 (["**Limite de gasto por agente no Copilot Studio, direto no admin do M365.**",
   "Novo: spending policies no Microsoft 365 admin center (public preview)."], light_scene(REVIEW), None),
 (["Seu agente mais popular pode queimar o crédito do ambiente inteiro.",
   "Agora a política tem dois limites: um mensal para o ambiente e outro por agente.",
   "**Testei: $400 no ambiente e $50 por agente.**"], LIMITS, None),
 (["Em Copilot > Cost management > Add spending policy você escolhe Identity ou Resources.",
   "**Cuidado: em Resource collection o padrão vem All environments. Comece por Specific environments.**"], SCOPE, None),
 (["Alertas diários por e-mail: % do limite da política e valor por agente.",
   "**Pré-pago (Capacity packs) ou pay-as-you-go via assinatura Azure, com chargeback por área.**"], BILL, None),
 (["Por agente ou ambiente: public preview. Por pessoa ou grupo: em breve. Papéis novos: AI Administrator e AI Reader.",
   "**Comenta LIMITE que eu te mando o link no direct!**"], BLOG["scenario1"], "Imagem: Microsoft"),
]
X = [
 (["Your most popular agent can burn the whole environment's credits.",
   "**Copilot Studio now has spending policies in the Microsoft 365 admin center: Copilot > Cost management (public preview).**"], BLOG["mac_overview"], "Image: Microsoft"),
 (["Scope a policy to Resources: a specific agent, or a collection of environments.",
   "**Set a monthly limit for the policy AND a limit per agent, so one agent can't drain the rest.**"], BLOG["scenario1"], "Image: Microsoft"),
 (["Fund it with prepaid Capacity Packs or pay-as-you-go on an Azure subscription.",
   "**Link an Azure subscription for chargeback, so each department owns its cost.**"], BLOG["billing_top"], "Image: Microsoft"),
 (["Per-agent and per-environment limits: public preview. Per user or group: coming soon.",
   "**New roles: AI Administrator and AI Reader.**"], BLOG["cycle"], "Image: Microsoft"),
]

SLUG = "2026-11-25-copilot-studio-spending-limits"
HDR = {"pt": Image.open(f"{ROOT}/instagram/2026-11-18-cowork-subagents/slide1.jpg").crop((0, 0, 1080, 205)),
       "en": Image.open(f"{ROOT}/x/2026-11-18-cowork-subagents/slide1.jpg").crop((0, 0, 1080, 205))}
for lang, folder, data in (("pt", "instagram", IG), ("en", "x", X)):
    out = f"{ROOT}/{folder}/{SLUG}"; os.makedirs(out, exist_ok=True)
    for i, (paras, img, src) in enumerate(data, 1):
        tweet_slide(HDR[lang], paras, img, f"{out}/slide{i}.jpg", src)
print("ok")
