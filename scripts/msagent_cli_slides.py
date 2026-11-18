"""msagent CLI carousel (brand style) - Instagram (PT) and X (EN).
Usage: python msagent_cli_slides.py <blog_screenshot.png>
Terminal cards show only commands documented in the official README/Quickstart."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from brand_lib import *

BLOG = Image.open(sys.argv[1]).convert("RGB")
MONO = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 34)
MONO_B = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 34)

def terminal(lines, w=1180, title="msagent — zsh"):
    lh = 58
    h = 90 + lh * len(lines) + 40
    im = Image.new("RGB", (w, h), (13, 17, 23))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 60), fill=(30, 35, 45))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((24 + i * 34, 20, 44 + i * 34, 40), fill=c)
    d.text((w / 2, 30), title, font=font("Medium", 26), fill=(148, 163, 184), anchor="mm")
    y = 90
    for ln in lines:
        if ln.startswith("#"):
            d.text((36, y), ln, font=MONO, fill=(110, 120, 140))
        elif ln:
            d.text((36, y), "$", font=MONO_B, fill=(39, 201, 63))
            parts = ln.split(" ", 2)
            x = 76
            d.text((x, y), parts[0], font=MONO_B, fill=(102, 163, 255)); x += d.textlength(parts[0] + " ", font=MONO_B)
            if len(parts) > 1:
                d.text((x, y), parts[1], font=MONO_B, fill=(255, 255, 255)); x += d.textlength(parts[1] + " ", font=MONO_B)
            if len(parts) > 2:
                d.text((x, y), parts[2], font=MONO, fill=(226, 232, 240))
        y += lh
    return im

T1 = terminal(["# authenticate, pick an environment",
               "msagent auth create --name Dev",
               "msagent env select <environment-id>",
               "", "# scaffold an agent locally",
               "msagent agent create --agent-type MCSAgent",
               "#   -n \"Hello World\" -d \"...\" -ip \"...\""])
T2 = terminal(["msagent deployment create --deployment-name dev",
               "msagent agent deploy --deployment-name dev",
               "msagent agent eval run --generate 3 --watch",
               "msagent agent deploy --deployment-name dev",
               "#   --publish"])
T3 = terminal(["# humans: interactive UI",
               "msagent test playground --deployment-name dev",
               "", "# AI agents / automation",
               "msagent test ask --deployment-name dev",
               "#   --query \"...\" --non-interactive --json"])
T4 = terminal(["msagent auth create --name Dev",
               "msagent auth list",
               "msagent auth select --name Dev",
               "msagent auth who",
               "# legacy auth login / logout: disabled by default"])

TEXT = {
 "pt": [
  ("Seus agentes do Copilot Studio agora vivem no *terminal e no Git.*", T1, "msagent CLI · public preview",
   "Crie ou clone agentes numa pasta local e *versione tudo* como código."),
  ("Do repositório ao *ambiente* em 4 comandos", T2, "deploy · eval · publish",
   "Deploy de um draft, *avaliação* e publicação, tudo pela linha de comando."),
  ("Teste sem *sair do terminal*", T3, "test playground · test ask",
   "Playground para você testar. *test ask* para quando um agente de IA conduz."),
  ("Autenticação *pronta para CI/CD*", T4, "SPN · Azure DevOps · GitHub",
   "Perfis de autenticação acabaram de chegar ao *repo oficial.* auth login vira auth create."),
  ("Você levaria seus agentes *para o Git?*", BLOG, "Code Agents: early-access preview",
   "Me siga para aprender sobre *Copilot e agentes de IA.*"),
 ],
 "en": [
  ("Copilot Studio agents now live in your *terminal and Git repo.*", T1, "msagent CLI · public preview",
   "Create or clone agents into a local folder and *version everything* as code."),
  ("From repo to *environment* in 4 commands", T2, "deploy · eval · publish",
   "Deploy a draft, *run evaluations* and publish, all from the command line."),
  ("Test without *leaving the terminal*", T3, "test playground · test ask",
   "Playground for you. *test ask* when an AI agent is driving."),
  ("Authentication *ready for CI/CD*", T4, "SPN · Azure DevOps · GitHub",
   "Auth profiles just landed in the *official repo.* auth login becomes auth create."),
  ("Would you move your agents *into Git?*", BLOG, "Code Agents: early-access preview",
   "Follow me for more *Copilot and AI agent tips.*"),
 ],
}

for lang, folder in (("pt", "instagram"), ("en", "x")):
    out = f"/home/claude/artifacts/{folder}/2026-11-18-msagent-cli"
    os.makedirs(out, exist_ok=True)
    for i, (t, img, p, b) in enumerate(TEXT[lang], 1):
        slide(i, 5, t, img, p, b, title_size=84, img_h=560, path=f"{out}/slide{i}.jpg")
print("ok")
