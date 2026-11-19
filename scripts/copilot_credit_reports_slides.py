"""Copilot Credit usage reports API (preview) - LinkedIn image (light) + tweet-card
carousels (Instagram PT, X EN). Content only from the official Learn tutorial.
Usage: python copilot_credit_reports_slides.py <learn_screenshot.png>"""
import sys, os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "/home/claude/artifacts"
LEARN = Image.open(sys.argv[1]).convert("RGB")
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + f"Inter-{w}.otf", s)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono"
def mono(s, b=False): return ImageFont.truetype(MONO + ("-Bold" if b else "") + ".ttf", s)

INK = (15, 23, 42); BLUE = (0, 85, 204); BLUE2 = (51, 136, 255); BLUE3 = (102, 163, 255)
GRAY = (100, 116, 139); TERM = (13, 17, 23); TBAR = (30, 35, 45)

# ---------- shared pieces ----------
def terminal(lines, w, fs=30, title="pac — pwsh"):
    lh = int(fs * 1.7)
    h = 60 + 34 + lh * len(lines) + 30
    im = Image.new("RGB", (w, h), TERM); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 60), fill=TBAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((24 + i * 34, 20, 44 + i * 34, 40), fill=c)
    d.text((w / 2, 30), title, font=font("Medium", 24), fill=(148, 163, 184), anchor="mm")
    y = 94; R, B = mono(fs), mono(fs, True)
    for ln in lines:
        if ln.startswith("#"):
            d.text((34, y), ln, font=R, fill=(110, 120, 140))
        elif ln.startswith("  "):  # continuation flags
            x = 34 + d.textlength("$ ", font=B)
            for tok in ln.split():
                d.text((x, y), tok, font=R, fill=BLUE3 if tok.startswith("--") else (226, 232, 240))
                x += d.textlength(tok + " ", font=R)
        elif ln:
            d.text((34, y), "$", font=B, fill=(39, 201, 63)); x = 34 + d.textlength("$ ", font=B)
            p = ln.split(" ", 2)
            d.text((x, y), p[0], font=B, fill=BLUE3); x += d.textlength(p[0] + " ", font=B)
            if len(p) > 1: d.text((x, y), p[1], font=B, fill=(255, 255, 255)); x += d.textlength(p[1] + " ", font=B)
            if len(p) > 2: d.text((x, y), p[2], font=R, fill=(226, 232, 240))
        y += lh
    return im

def rounded(img, r=26, border=(226, 232, 240)):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0)); out.paste(img, (0, 0), m)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, img.width - 1, img.height - 1), r, outline=border, width=2)
    return out

def flow_card(w, lang):
    acts = [("Generate Licensing Report", "FeatureDetailsPerResource · Summary"),
            ("Get Licensing Report Operation Status", "Do until status ≠ Running"),
            ("Download Licensing Report File", "fileName → Parse JSON"),
            ("Send an email (V2)", "BilledCredits + NonBilledCredits > 1000")]
    top = "Recurrence · every Monday · last 14 days" if lang == "en" else "Recorrência · toda segunda · últimos 14 dias"
    bh, gap = 112, 46
    h = 40 + 70 + len(acts) * (bh + gap) + 10
    im = Image.new("RGB", (w, h), (248, 250, 252)); d = ImageDraw.Draw(im)
    d.text((w / 2, 60), top, font=font("SemiBold", 30), fill=GRAY, anchor="mm")
    y = 110
    for i, (t, s) in enumerate(acts):
        x0, x1 = 50, w - 50
        d.rounded_rectangle((x0, y, x1, y + bh), 16, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
        col = BLUE if i < 3 else (0, 120, 212)
        d.rounded_rectangle((x0 + 22, y + 26, x0 + 82, y + 86), 12, fill=col)
        d.text((x0 + 52, y + 56), "⚙" if i < 3 else "✉", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30), fill="white", anchor="mm")
        d.text((x0 + 104, y + 22), t, font=font("SemiBold", 32), fill=INK)
        d.text((x0 + 104, y + 66), s, font=font("Regular", 26), fill=GRAY)
        if i < len(acts) - 1:
            cx = w / 2; d.line((cx, y + bh, cx, y + bh + gap), fill=(148, 163, 184), width=3)
            d.polygon([(cx - 9, y + bh + gap - 14), (cx + 9, y + bh + gap - 14), (cx, y + bh + gap)], fill=(148, 163, 184))
        y += bh + gap
    return im

def reports_card(w):
    rows = [("FeatureDetailsPerResource", ["ResourceName", "EnvironmentName", "Product", "Feature",
                                           "LLMModel", "BilledCredits", "NonBilledCredits"]),
            ("BillingDetailsPerEnvironment", ["EnvironmentName", "BillingPolicyId", "EntitlementID",
                                              "CapacityPackCreditsConsumed", "PayGoConsumedQuantity"])]
    im = Image.new("RGB", (w, 600), TERM); d = ImageDraw.Draw(im)
    y = 36
    for name, cols in rows:
        d.text((40, y), name, font=mono(32, True), fill=BLUE3); y += 58
        x = 40
        for c in cols:
            tw = d.textlength(c, font=mono(24)) + 28
            if x + tw > w - 40: x = 40; y += 56
            d.rounded_rectangle((x, y, x + tw, y + 44), 10, fill=(30, 41, 59))
            d.text((x + 14, y + 22), c, font=mono(24), fill=(226, 232, 240), anchor="lm"); x += tw + 12
        y += 90
    d.text((40, y - 10), "granularity: Daily | Summary", font=mono(26), fill=(110, 120, 140))
    return im.crop((0, 0, w, y + 40))

# ---------- LinkedIn image / Instagram slide 1 (light identity, dark terminal, blue) ----------
def rich(d, x, y, text, f, lh, maxw):
    toks = []
    for part in re.split(r"(\*[^*]+\*)", text):
        for w in part.strip("*").split(): toks.append((w, part.startswith("*")))
    lines, cur, sp = [], [], d.textlength(" ", font=f)
    for w, a in toks:
        if cur and sum(d.textlength(t, font=f) + sp for t, _ in cur) + d.textlength(w, font=f) > maxw:
            lines.append(cur); cur = []
        cur.append((w, a))
    lines.append(cur)
    for ln in lines:
        cx = x
        for w, a in ln: d.text((cx, y), w, font=f, fill=BLUE if a else INK); cx += d.textlength(w, font=f) + sp
        y += lh
    return y

TERM_LINES = ["# Copilot Credit usage reports API (preview)",
              "pac auth create --name LicensingReports",
              "pac copilot-studio generate-licensing-report",
              "  --report-name FeatureDetailsPerResource",
              "pac copilot-studio get-licensing-report-operation",
              "pac copilot-studio download-licensing-report-file"]

def hero(path, W, H, title, fs=84, tfs=29, M=76, top=96, handle=None):
    glow = Image.new("RGB", (W, H), "white"); g = ImageDraw.Draw(glow)
    g.ellipse((W - 520, -420, W + 380, 380), fill=(214, 230, 255))
    g.ellipse((-460, H - 300, 360, H + 380), fill=(232, 240, 255))
    im = glow.filter(ImageFilter.GaussianBlur(150)); d = ImageDraw.Draw(im)
    y = rich(d, M, top, title, font("ExtraBold", fs), int(fs * 1.14), W - 2 * M) + 44
    T = terminal(TERM_LINES, W - 2 * M, fs=tfs)
    if handle: y += 30
    sh = Image.new("RGBA", (T.width + 120, T.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 76, T.width + 60, T.height + 70), 26, fill=(0, 60, 160, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(26)); im.paste(sh, (M - 60, y - 60), sh)
    t = rounded(T, border=(51, 65, 85)); im.paste(t, (M, y), t)
    if handle:
        d = ImageDraw.Draw(im); d.text((M, H - 80), handle, font=font("SemiBold", 32), fill=GRAY)
        d.text((W - M, H - 80), "Copilot Studio · public preview", font=font("Medium", 28), fill=GRAY, anchor="ra")
    im.save(path, quality=94)

# ---------- tweet-card carousel ----------
def tweet_slide(header, paras, img, path, src=None):
    W, H, M = 1080, 1350, 64
    im = Image.new("RGB", (W, H), "white"); im.paste(header, (0, 0)); d = ImageDraw.Draw(im)
    y = 228
    for txt in paras:
        bold = txt.startswith("**"); txt = txt.strip("*")
        f = font("Bold" if bold else "Regular", 46)
        words, line = txt.split(), ""
        for w in words:
            t = (line + " " + w).strip()
            if d.textlength(t, font=f) > W - 2 * M: d.text((M, y), line, font=f, fill=(15, 20, 25)); y += 60; line = w
            else: line = t
        d.text((M, y), line, font=f, fill=(15, 20, 25)); y += 60 + 26
    y += 6
    avail_h = H - y - (90 if src else 50); avail_w = W - 2 * M
    r = min(avail_w / img.width, avail_h / img.height, 1.6)
    pic = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    p = rounded(pic, 24); im.paste(p, (M, y), p)
    if src: d.text((M, y + pic.height + 16), src, font=font("Regular", 26), fill=(110, 118, 125))
    im.save(path, quality=92)

LW = 948
T_IG = terminal(["pac copilot-studio generate-licensing-report",
                 "  --report-name FeatureDetailsPerResource",
                 "  --start-date --end-date --granularity",
                 "pac copilot-studio get-licensing-report-operation",
                 "  --report-name --operation-id",
                 "pac copilot-studio download-licensing-report-file",
                 "  --report-name --file-name --out-file"], LW, fs=27)
REP = reports_card(LW)
LEARN_TOP = LEARN.crop((0, 0, LEARN.width, 455))
def caveat_card(w, lang):
    en = lang == "en"
    items = [("Public preview", "!"), ("Sovereign clouds aren't supported" if en else "Sovereign clouds: ainda não", "!"),
             ("Delegated user auth only (no service principal)" if en else "Só autenticação delegada (sem SPN)", "!"),
             ("Global, Power Platform or Dynamics 365 Admin" if en else "Global, Power Platform ou Dynamics 365 Admin", "!")]
    soon = [("December 2026: one connector action" if en else "Dez/2026: uma ação única no conector", "submit + poll + download"),
            ("December 2026: JSON via the connector" if en else "Dez/2026: JSON pelo conector", "CSV is the default today" if en else "hoje o padrão é CSV")]
    im = Image.new("RGB", (w, 640), (248, 250, 252)); d = ImageDraw.Draw(im); y = 34
    for t, _ in items:
        d.ellipse((40, y + 4, 80, y + 44), fill=(245, 158, 11)); d.text((60, y + 24), "!", font=font("Bold", 28), fill="white", anchor="mm")
        d.text((100, y + 24), t, font=font("Medium", 32), fill=INK, anchor="lm"); y += 66
    y += 14; d.line((40, y, w - 40, y), fill=(226, 232, 240), width=2); y += 30
    for t, s2 in soon:
        d.rounded_rectangle((40, y, 80, y + 40), 10, fill=BLUE); d.text((60, y + 20), "→", font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26), fill="white", anchor="mm")
        d.text((100, y + 2), t, font=font("SemiBold", 32), fill=BLUE)
        d.text((100, y + 44), s2, font=font("Regular", 26), fill=GRAY); y += 100
    return im.crop((0, 0, w, y + 10))

TXT = {
 "pt": [
  (["O admin center guarda só 30 dias de consumo de Copilot Credits.",
    "Agora dá para guardar o histórico que você quiser.",
    "**Novo tutorial no Learn: Copilot Credit usage reports API (public preview).**"], LEARN_TOP, "Imagem: Microsoft Learn"),
  (["Dois relatórios com os mesmos dados do admin center:",
    "por agente, ambiente, produto e feature. E por ambiente e billing policy, pré-pago vs. pay-as-you-go.",
    "**Com granularidade Daily ou Summary.**"], REP, None),
  (["Três caminhos: conector Power Platform for Admins V2, Power Platform CLI ou REST.",
    "**No terminal são 3 comandos: gerar, consultar e baixar.**"], T_IG, None),
  (["O tutorial monta um workflow semanal: toda segunda, últimos 14 dias, e-mail com as linhas acima de 1.000 créditos.",
    "**FinOps de agentes, rodando no próprio Copilot Studio.**"], flow_card(LW, "pt"), None),
  (["Atenção: public preview, sem sovereign clouds, só autenticação delegada (sem service principal) e exige role de admin.",
    "**Em dezembro de 2026: uma ação única que gera, aguarda e baixa.**"], caveat_card(LW, "pt"), "Fonte: Microsoft Learn"),
 ],
 "en": [
  (["The admin center keeps only 30 days of Copilot Credit consumption.",
    "Now you can keep the history as long as you want.",
    "**New Learn tutorial: Copilot Credit usage reports API (public preview).**"], LEARN_TOP, "Image: Microsoft Learn"),
  (["Two reports, the same data you see in the admin center:",
    "by agent, environment, product and feature. And by environment and billing policy, prepaid vs. pay-as-you-go.",
    "**Daily or Summary granularity.**"], REP, None),
  (["Three ways in: Power Platform for Admins V2 connector, Power Platform CLI or REST.",
    "**From the terminal it's 3 commands: generate, poll, download.**"], T_IG, None),
  (["The tutorial builds a weekly workflow: every Monday, last 14 days, an email with the rows above 1,000 credits.",
    "**Agent FinOps, running in Copilot Studio itself.**"], flow_card(LW, "en"), None),
  (["Heads-up: public preview, no sovereign clouds, delegated user auth only (no service principal), admin role required.",
    "**Coming December 2026: one action that submits, polls and downloads.**"], caveat_card(LW, "en"), "Source: Microsoft Learn"),
 ],
}

SLUG = "2026-11-19-copilot-credit-reports"
HDR = {"pt": Image.open(f"{ROOT}/instagram/2026-11-18-cowork-subagents/slide1.jpg").crop((0, 0, 1080, 205)),
       "en": Image.open(f"{ROOT}/x/2026-11-18-cowork-subagents/slide1.jpg").crop((0, 0, 1080, 205))}
os.makedirs(f"{ROOT}/linkedin/{SLUG}", exist_ok=True)
hero(f"{ROOT}/linkedin/{SLUG}/image.jpg", 1200, 1000, "Keep your Copilot Credit history *as long as you want, via CLI.*")
for lang, folder in (("pt", "instagram"), ("en", "x")):
    out = f"{ROOT}/{folder}/{SLUG}"; os.makedirs(out, exist_ok=True)
    for i, (paras, img, src) in enumerate(TXT[lang], 1):
        tweet_slide(HDR[lang], paras, img, f"{out}/slide{i}.jpg", src)
def term_scene(W, H, M=50, tfs=23):
    glow = Image.new("RGB", (W, H), "white"); g = ImageDraw.Draw(glow)
    g.ellipse((W - 520, -420, W + 380, 380), fill=(214, 230, 255))
    g.ellipse((-460, H - 300, 360, H + 380), fill=(232, 240, 255))
    im = glow.filter(ImageFilter.GaussianBlur(150))
    T = terminal(TERM_LINES, W - 2 * M, fs=tfs); y = (H - T.height) // 2
    sh = Image.new("RGBA", (T.width + 120, T.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((60, 76, T.width + 60, T.height + 70), 26, fill=(0, 60, 160, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(26)); im.paste(sh, (M - 60, y - 60), sh)
    t = rounded(T, border=(51, 65, 85)); im.paste(t, (M, y), t)
    return im

tweet_slide(HDR["pt"], ["**Guarde o histórico de Copilot Credits pelo tempo que quiser, via CLI.**",
                        "Novo no Learn: Copilot Credit usage reports API (public preview). Os mesmos dados do admin center, sem o limite de 30 dias."],
            term_scene(948, 640), f"{ROOT}/instagram/{SLUG}/slide1.jpg")
