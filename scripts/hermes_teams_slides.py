"""Hermes Enterprise on Microsoft Foundry - Instagram (PT) and X (EN) carousels, brand style.
Usage: python3 hermes_teams_slides.py <pt|en> <out_dir>"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from brand_lib import *
from PIL import Image, ImageDraw, ImageFont

LANG, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
DL = "/home/claude/dl/"
EMO = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)

def emoji(ch, size):
    im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=EMO, embedded_color=True)
    im = im.crop(im.getbbox()); r = size / max(im.size)
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)

def arch(steps):
    """Logos (Microsoft | Nous Research, from the official partner image) + 3-step flow."""
    w, h = 1000, 920
    im = Image.new("RGB", (w, h), (11, 26, 61)); d = ImageDraw.Draw(im)
    lg = Image.open(DL + "logos_white.png"); lg = lg.resize((700, int(700 * lg.height / lg.width)), Image.LANCZOS)
    im.paste(lg, ((w - lg.width) // 2, 20), lg)
    y = 200
    for i, (ic, a, b) in enumerate(steps):
        d.rounded_rectangle((40, y, w - 40, y + 170), 26, fill=(14, 31, 72), outline=GLOW, width=3)
        e = emoji(ic, 70); im.paste(e, (80, y + 50), e)
        d.text((190, y + 34), a, font=font("Medium", 40), fill=(226, 232, 240))
        d.text((190, y + 88), b, font=font("Bold", 44), fill=WHITE)
        if i < 2:
            d.polygon([(w / 2 - 20, y + 182), (w / 2 + 20, y + 182), (w / 2, y + 210)], fill=ACCENT)
        y += 240
    return im

def slide2(n, total, title, img, pill_text, body, caption=None, title_size=88, img_h=520, path=None):
    im = background(); d = ImageDraw.Draw(im, "RGBA")
    y = draw_rich(d, M, 100, title, font("ExtraBold", title_size), int(title_size * 1.12), W - 2 * M) + 36
    cw = W - 2 * M; nh = int(cw * img.height / img.width)
    if nh > img_h: nh = img_h; cw = int(nh * img.width / img.height)
    card(im, img, (W - cw) // 2, y, cw, nh); d = ImageDraw.Draw(im, "RGBA")
    y += nh + 14
    if caption:
        d.text((W - M, y), caption, font=font("Medium", 24), fill=MUTED, anchor="ra")
    y += 34
    if pill_text:
        y = pill(d, M, y, pill_text, W - 2 * M) + 28
    if body:
        draw_rich(d, M, y, body, font("Regular", 40), 54, W - 2 * M, color=(226, 232, 240), acc=ACCENT, bold_acc=font("Bold", 40))
    footer(d, n, total)
    im.save(path, quality=92)

BP = Image.open(DL + "blueprints.png").convert("RGB")
OWN = Image.open(DL + "ownership.png").convert("RGB")
OG = Image.open(DL + "og.png").convert("RGB")
PARTNER = Image.open(DL + "partner.jpg").convert("RGB").crop((0, 300, 1206, 900))
T = 5

if LANG == "pt":
    A = arch([("💬", "Você menciona o Hermes", "no Microsoft Teams"),
              ("🤖", "Ele roda no", "Microsoft Foundry"),
              ("📧", "Trabalha com seu próprio", "e-mail, agenda e OneDrive")])
    cap = "Imagem: Microsoft"
    S = [("O *Hermes* agora trabalha no *Microsoft Teams.*", A, "Hermes Enterprise no Microsoft Foundry",
          "Um colega de IA com *conta própria no Microsoft 365.*", None, 600),
         ("Ele não usa a *sua identidade.*", OG, "Identidade própria no Microsoft Entra",
          "E-mail, agenda, OneDrive, *um gestor no organograma* e trilha de auditoria.", cap, 440),
         ("Você não cria o agente. Cria o *blueprint.*", BP, "Blueprint → admin aprova → cada um contrata",
          "Mesma lógica, *identidade e acesso próprios* em cada instância.", cap, 380),
         ("A Nous cuida do agente. O *Foundry, do resto.*", OWN, "Aprende com cada correção",
          "O Hermes aprende como o gestor trabalha e *transforma correções em skills.*", cap, 520),
         ("Você contrataria um *agente de IA?*", PARTNER, "Hermes Enterprise: em breve",
          "Hoje: cookbook open source (POC) e Frontier. Me siga para aprender sobre *Copilot e agentes de IA.*", cap, 460)]
else:
    A = arch([("💬", "You @mention Hermes", "in Microsoft Teams"),
              ("🤖", "It runs on", "Microsoft Foundry"),
              ("📧", "It works with its own", "mailbox, calendar & OneDrive")])
    cap = "Image: Microsoft"
    S = [("*Hermes* now works in *Microsoft Teams.*", A, "Hermes Enterprise on Microsoft Foundry",
          "An AI coworker with *its own Microsoft 365 account.*", None, 600),
         ("It doesn't borrow *your identity.*", OG, "Its own Microsoft Entra agent identity",
          "Email, calendar, OneDrive, *a manager in the org chart* and an audit trail.", cap, 440),
         ("You don't build the agent. You build the *blueprint.*", BP, "Blueprint → admin approves → people hire",
          "Same logic, *unique identity and access* for every instance.", cap, 380),
         ("Nous owns the agent. *Foundry runs it.*", OWN, "Learns from every correction",
          "Hermes learns how its manager works and *turns corrections into skills.*", cap, 520),
         ("Would you hire an *AI agent?*", PARTNER, "Hermes Enterprise: coming soon",
          "Today: open-source cookbook (POC) + Frontier. Follow me for more *Copilot and AI agent tips.*", cap, 440)]

for i, (t, img, p, b, c, ih) in enumerate(S, 1):
    slide2(i, T, t, img, p, b, c, title_size=80 if i == 1 else 88, img_h=ih, path=f"{OUT}/slide{i}.jpg")
print("ok")
