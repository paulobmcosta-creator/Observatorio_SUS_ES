"""Visualizações de conjuntos a partir de uma partição exata com todos os padrões."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle


INK = "#183447"
BLUE = "#236789"
TEAL = "#277565"
ORANGE = "#aa572e"
GRAY = "#58656d"


def numero(n):
    return f"{int(n):,}".replace(",", ".")


def validar_particao(exatos, k):
    n = np.asarray(exatos)
    if n.shape != (2**k,) or n.dtype.kind not in "iu" or (n < 0).any():
        raise ValueError("Partição incompleta ou contagem inválida.")
    return n


def inclusiva(ex, mask):
    return int(sum(n for j, n in enumerate(ex) if (j & mask) == mask))


def venn3(ax, exatos):
    """Traçar um Venn esquemático e verificar em qual região cada valor foi colocado."""
    ex = validar_particao(exatos, 3)
    centros = [(-.82,.48),(.82,.48),(0,-.78)]
    raio = 1.28
    pos = {4:(-1.38,.60),2:(1.38,.60),1:(0,-1.38),6:(0,1.02),5:(-.67,-.44),3:(.67,-.44),7:(0,.06)}
    for centro, cor in zip(centros, (BLUE, ORANGE, TEAL)):
        ax.add_patch(Circle(centro, raio, facecolor=cor+"22", edgecolor=cor, lw=2))
    for mask, pt in pos.items():
        real = sum(bit for bit, centro in zip((4,2,1),centros) if np.linalg.norm(np.subtract(pt,centro)) < raio)
        if real != mask:
            raise ValueError("Posição do número fora da interseção pretendida.")
        ax.text(*pt, numero(ex[mask]), ha="center", va="center", fontsize=15, fontweight="bold", color=INK)
    for p,s,c in [((-1.56,1.64),"A",BLUE),((1.56,1.64),"B",ORANGE),((0,-2.18),"C",TEAL)]:
        ax.text(*p,s,ha="center",va="center",color=c,weight="bold",fontsize=14)
    ax.set(xlim=(-2.35,2.35),ylim=(-2.4,1.98),aspect="equal")
    ax.axis("off")


def upset(fig, labels, exatos):
    """Mostrar todas as combinações positivas; o exterior é contado na legenda da figura."""
    k = len(labels)
    ex = validar_particao(exatos, k)
    masks = sorted((m for m in range(1,len(ex)) if ex[m]), key=lambda m:(-ex[m],m))
    if not masks:
        fig.text(.5,.47,"Nenhum estabelecimento na união dos conjuntos.",ha="center")
        return []
    gs = fig.add_gridspec(2,2,width_ratios=[2.45,6.6],height_ratios=[2.6,1.8],
                          left=.20,right=.975,bottom=.20,top=.74,hspace=.12,wspace=.10)
    sizes_ax=fig.add_subplot(gs[1,0]); dots=fig.add_subplot(gs[1,1]); bars=fig.add_subplot(gs[0,1],sharex=dots)
    sizes=[inclusiva(ex,1<<(k-1-j)) for j in range(k)]
    y=np.arange(k)
    sizes_ax.barh(y,sizes,color="#7393a2",height=.48);sizes_ax.invert_xaxis()
    sizes_ax.set_yticks(y,labels,fontsize=9);sizes_ax.set_ylim(k-.5,-.5)
    for j,n in enumerate(sizes):
        sizes_ax.text(n+.012*max(sizes),j,numero(n),va="center",ha="right",fontsize=8,color=INK)
    sizes_ax.set_xlim(max(1,max(sizes))*1.40,0);sizes_ax.set_xticks([]);sizes_ax.tick_params(length=0)
    sizes_ax.set_title("Tamanho dos conjuntos",fontsize=9,loc="left")
    for j,m in enumerate(masks):
        active=[i for i in y if m & (1<<(k-1-i))]
        dots.plot([j,j],[min(active),max(active)],color=INK,lw=1.4,zorder=2)
        dots.scatter(np.repeat(j,k),y,s=17,color="#d7dfe0",zorder=1)
        dots.scatter(np.repeat(j,len(active)),active,s=30,color=INK,zorder=3)
    dots.set_ylim(k-.5,-.5);dots.set_yticks([]);dots.set_xticks([]);dots.set_xlim(-.6,len(masks)-.4)
    values=[ex[m] for m in masks]
    bars.bar(range(len(masks)),values,width=.68,color=BLUE)
    for j,n in enumerate(values):
        bars.text(j,n+max(values)*.018,numero(n),ha="center",va="bottom",fontsize=8)
    bars.set_ylim(0,max(1,max(values))*1.19);bars.tick_params(axis="x",bottom=False,labelbottom=False)
    bars.set_ylabel("CNES distintos",fontsize=9);bars.grid(axis="y",alpha=.16);bars.set_axisbelow(True)
    for ax in [sizes_ax,dots,bars]:
        for spine in ax.spines.values():spine.set_visible(False)
    return masks


def euler_aninhado(ax, universo, sus, producao):
    """Representação esquemática após verificar externamente as inclusões nas chaves."""
    if not 0 <= producao <= sus <= universo:raise ValueError("Cardinalidades incompatíveis com inclusão.")
    for x,y,w,h,n,s,c in [(0,.03,1,.95,universo,"Cadastro CNES",INK),(.09,.12,.82,.63,sus,"Vínculo SUS",BLUE),(.16,.21,.68,.25,producao,"PA específico ou SIH cardiovascular",TEAL)]:
        ax.add_patch(Rectangle((x,y),w,h,facecolor=c+"0D",edgecolor=c,lw=1.7))
        ax.text(x+.022,y+h-.055,f"{s}  ·  {numero(n)}",color=c,va="top",weight="bold",fontsize=10.5)
    ax.set(xlim=(-.02,1.02),ylim=(0,1));ax.axis("off")
