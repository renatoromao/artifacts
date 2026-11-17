import sys; sys.path.insert(0,'/home/claude/cw')
from brand_lib import *
R="/tmp/claude-tool-results/90b4f830-5e60-5320-b7bc-33db32d1b29d/"
OUT="/home/claude/cw/post1"; os.makedirs(OUT,exist_ok=True)
B=Image.open(R+"mcp-claude-in-chrome-blob-1794956796976-wsvs5v-ad09450f.png").convert("RGB")
A=Image.open(R+"mcp-claude-in-chrome-blob-1794956803786-c5mubs-80be7da2.png").convert("RGB")
C=Image.open(R+"mcp-claude-in-chrome-blob-1794956811022-0skrlj-b91a79b5.png").convert("RGB")
HERO=Image.open(R+"mcp-claude-in-chrome-blob-1794956827610-h0mxas-12d79bb8.png").convert("RGB")
T=5
slide(1,T,"O Copilot Cowork agora decide *o quanto pensar.*",C.crop((180,130,1030,545)),
 "Novidade do Microsoft Ignite 2026",
 "O Auto ajusta o *reasoning effort* para cada tarefa, sozinho.",title_size=92,path=f"{OUT}/slide1.jpg")
slide(2,T,"Tarefa simples, *resposta rápida.*",A.crop((600,280,1020,360)),
 "Quick lookups stay fast",
 "Consultas rápidas continuam rápidas. Trabalho complexo ganha *raciocínio mais profundo.*",path=f"{OUT}/slide2.jpg")
slide(3,T,"Quem decide? O *Microsoft-Decision-1.1*",C.crop((640,300,975,445)),
 "A cada etapa da tarefa",
 "Em cada etapa, o Auto usa o modelo de decisão mais recente da Microsoft para *escolher o modelo certo.*",title_size=74,path=f"{OUT}/slide3.jpg")
slide(4,T,"Prefere controlar? *Ajuste você mesmo.*",B.crop((640,300,975,585)),
 "Effort: Medium",
 "Você ainda pode definir o nível de esforço *manualmente* quando quiser mais controle.",img_h=470,path=f"{OUT}/slide4.jpg")
slide(5,T,"Você deixaria o Auto *escolher por você?*",HERO,
 "Disponível hoje no Frontier",
 "Me siga para aprender sobre *Copilot e agentes de IA.*",title_size=92,path=f"{OUT}/slide5.jpg")
print("ok")
