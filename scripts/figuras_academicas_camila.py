"""Desenhar figuras acadêmicas e conservar exatamente a tabela usada em cada figura."""
import json
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.collections import PolyCollection
import numpy as np
import pandas as pd

REGIOES = ["Central", "Metropolitana", "Norte", "Sul"]
CORES = ["#326b82", "#bc6439", "#097659", "#785c90", "#a28320", "#576777"]
SIGLAS = dict(zip("11 12 13 14 15 16 17 21 22 23 24 25 26 27 28 29 31 32 33 35 41 42 43 50 51 52 53".split(),
                  "RO AC AM RR PA AP TO MA PI CE RN PB PE AL SE BA MG ES RJ SP PR SC RS MS MT GO DF".split()))


def iniciar():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False, "svg.fonttype": "none", "svg.hashsalt": "tcc-camila-v32",
                         "figure.facecolor": "white", "axes.titlelocation": "left"})


def finalizar(fig, arquivo, titulo, unidade, fonte, nota):
    fig.suptitle(titulo, x=0.085, y=0.98, ha="left", fontsize=15, weight="semibold", color="#16384a")
    fig.text(0.085, 0.905, unidade, color="#385b66")
    rodape = "\n".join(textwrap.wrap(f"Fonte: {fonte}. {nota}", 112))
    fig.text(0.085, 0.025, rodape, fontsize=8, color="#384a54", va="bottom")
    fig.subplots_adjust(left=0.10, right=0.95, top=0.84, bottom=0.25)
    for ext in ("svg", "png"):
        fig.savefig(arquivo.with_suffix("."+ext), dpi=160, metadata={"Date": None} if ext=="svg" else {})
    plt.close(fig)


def linhas(tabela, arquivo, titulo, unidade, fonte, nota, eixo="Ano", idades=False):
    """A lacuna em valor interrompe a linha e permanece ausente no CSV."""
    fig, ax = plt.subplots(figsize=(10, 5.6))
    for i, (nome, grupo) in enumerate(tabela.groupby("serie", sort=False)):
        grupo = grupo.sort_values("x")
        if grupo.x.duplicated().any():
            raise ValueError(f"Pontos repetidos na série {nome}")
        ax.plot(grupo.x, grupo.valor, marker="o", markersize=3.6, linewidth=2,
                color=CORES[i % len(CORES)], linestyle=["-", "--", "-."][i//len(CORES) % 3], label=nome)
    ticks = sorted(tabela.x.unique())
    ax.set_xticks(ticks)
    if idades:
        ax.set_xticklabels([f"{n}–{n+4}" if n<80 else "80+" for n in ticks], rotation=45, ha="right")
    ax.set_xlabel(eixo)
    ax.ticklabel_format(style="plain", axis="y")
    ax.grid(axis="y", alpha=0.22)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.26 if idades else -0.16),
              ncol=min(4, tabela.serie.nunique()), frameon=False, fontsize=8)
    finalizar(fig, arquivo, titulo, unidade, fonte, nota)


def mapa(tabela, malha, arquivo, titulo, unidade, fonte, nota):
    geometria = json.loads(malha.read_text(encoding="utf-8"))["features"]
    figuras = tabela.painel.drop_duplicates().to_list()
    fig, axs = plt.subplots(1, len(figuras), figsize=(10, 6), squeeze=False)
    df = tabela.set_index(["painel", "chave"])
    paleta = plt.get_cmap("YlGnBu").copy()
    paleta.set_bad("#dadada")
    vmax = tabela.valor.max()
    escala = colors.Normalize(0, max(float(vmax), 1))
    chaves = {g["properties"]["codarea"] for g in geometria}
    if any(set(tabela[tabela.painel==p].chave)!=chaves for p in figuras) or not df.index.is_unique:
        raise ValueError("Chaves do mapa incompatíveis com a malha")
    for ax, painel in zip(axs.flat, figuras):
        vertices, valores = [], []
        for g in geometria:
            valor = df.loc[(painel,g["properties"]["codarea"]), "valor"]
            poligonos = g["geometry"]["coordinates"]
            if g["geometry"]["type"]=="Polygon":
                poligonos = [poligonos]
            for pol in poligonos:
                vertices.append(pol[0])
                valores.append(valor)
        colecao = PolyCollection(vertices, array=np.ma.masked_invalid(np.asarray(valores,dtype=float)),
                                 cmap=paleta, norm=escala, edgecolor="#637780", linewidth=0.3)
        ax.add_collection(colecao)
        ax.autoscale_view()
        if len(chaves) == 78:
            # A geometria de Vitória também contém as ilhas oceânicas. O recorte
            # de exibição conserva os 78 valores municipais no mapa e no CSV.
            ax.set_xlim(-42.05, -39.35)
            ax.set_ylim(-21.43, -17.83)
            if painel == "Região do estabelecimento":
                for nome, x, y in [("Norte", -40.29, -18.47), ("Central", -40.49, -19.20),
                                   ("Metropolitana", -40.58, -20.12), ("Sul", -41.38, -20.80)]:
                    ax.text(x, y, nome, ha="center", va="center", fontsize=8,
                            bbox={"facecolor": "white", "alpha": .86, "edgecolor": "none", "pad": 1.2})
        ax.set_aspect(1 / np.cos(np.deg2rad(np.mean(ax.get_ylim()))))
        ax.set_axis_off()
        ax.set_title(painel, fontsize=10, loc="center")
    cax = fig.add_axes([0.22, 0.145, 0.56, 0.021])
    fig.colorbar(colecao, cax=cax, orientation="horizontal")
    finalizar(fig, arquivo, titulo, unidade, fonte, nota)


def fluxo(tabela, arquivo, titulo, unidade, fonte, nota):
    matriz = tabela.pivot(index="origem", columns="destino", values="aih").reindex(index=REGIOES,columns=REGIOES)
    fig, ax = plt.subplots(figsize=(9,6))
    cores = ax.imshow(np.log1p(matriz.to_numpy()), cmap="Blues")
    ax.set_xticks(range(4), REGIOES)
    ax.set_yticks(range(4), REGIOES)
    ax.set_xlabel("Região de atendimento")
    ax.set_ylabel("Região de residência")
    for (i,j), valor in np.ndenumerate(matriz.to_numpy()):
        ax.text(j,i,f"{int(valor):,}".replace(",","."),ha="center",va="center",
                color="white" if cores.norm(np.log1p(valor))>0.63 else "#142f42")
    finalizar(fig, arquivo, titulo, unidade, fonte, nota)
