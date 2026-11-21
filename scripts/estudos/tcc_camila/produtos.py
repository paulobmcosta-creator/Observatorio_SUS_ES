"""Gerar figuras e contraprovas a partir dos CSVs selecionados."""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from projecao import salvar

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "integracao_estabelecimentos"))
from figuras_conjuntos import venn3, inclusiva

def gerar(dados, saida):
    matplotlib.rcParams.update({"svg.hashsalt":"observatorio-camila-v342", "svg.fonttype":"none","font.family":"DejaVu Sans"})
    figdir = saida / "figuras"
    figdir.mkdir(parents=True, exist_ok=True)
    def ler(nome):return pd.read_csv(dados / (nome+".csv"), dtype={"padrao": str}, float_precision="round_trip")
    def gravar(fig, nome, fonte):
        fig.text(.09,.025,fonte,fontsize=8,color="#475967")
        fig.savefig(figdir / (nome+".svg"),metadata={"Date":None,"Creator":"Observatório SUS-ES"})
        plt.close(fig)
    def linhas(d,x,series,titulo,unidade,nome,fonte):
        fig, ax=plt.subplots(figsize=(8.4,4.9))
        fig.subplots_adjust(left=.14,bottom=.23,top=.84,right=.97)
        for col,label in series:
            ax.plot(d[x],d[col],marker="o",markersize=3,label=label)
        ax.set_title(titulo,loc="left",fontsize=13,fontweight="bold",pad=12)
        ax.set_ylabel(unidade);ax.set_xlabel("Competência de produção" if x=="competencia" else "Ano")
        if x=="competencia":
            ax.set_xticks(d[x].iloc[::2],d[x].astype(str).iloc[::2])
        else:ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.grid(axis="y",alpha=.18);ax.legend(frameon=False,fontsize=8,ncol=2)
        gravar(fig,nome,fonte)
    partitions=ler("particoes_es")
    rotulos={"V01":["Recurso composto","PA específico","AIH cardiovascular"],"V02":["Serviço SR116","PA específico","AIH cardiovascular"],"V03":["Eletrocardiógrafo em uso","Serviço de ECG","ECG aprovado"]}
    totals=[]
    for k,labels in rotulos.items():
        d=partitions[partitions.tema==k].sort_values("padrao")
        if d.padrao.tolist()!=[format(i,"03b") for i in range(8)] or d.territorio.unique().tolist()!=["ES"] or set(d.ano)!={2024}:
            raise ValueError("Partição fora do domínio")
        ex=d.exclusiva_anual.to_numpy()
        inc=[inclusiva(ex,j) for j in range(8)]
        if inc!=d.inclusiva_anual.tolist() or not (d.uniao==ex.sum()-ex[0]).all() or not (d.universo==ex.sum()).all():
            raise ValueError("Falha de reconciliação das interseções")
        totals.append(dict(figura=k,universo=inc[0],uniao=inc[0]-int(ex[0]),exterior=int(ex[0]),tripla_anual=inc[7],tripla_mes=int(d.inclusiva_em_algum_mes.iloc[-1])))
        fig,ax=plt.subplots(figsize=(8,4.7));fig.subplots_adjust(left=.04,right=.55,bottom=.14,top=.83)
        venn3(ax,ex)
        fig.suptitle(k+" · Cadastro e produção no Espírito Santo, 2024",y=.95,fontweight="bold")
        fig.text(.55,.70,"\n".join(c+"   "+label for c,label in zip("ABC",labels)),linespacing=1.7)
        fig.text(.55,.37,f"Universo   {inc[0]:,}\nFora da união   {ex[0]:,}\nTripla na mesma competência   {totals[-1]['tripla_mes']}",linespacing=1.6)
        gravar(fig,k,"CNES, SIA e SIH · estabelecimentos distintos · regiões do desenho mostram contagens exclusivas anuais")
    salvar(pd.DataFrame(totals),saida/"dados/resumo_intersecoes.csv")
    t=ler("t29_selecao")
    ratios={"sim_bruta":100000*t.obitos/t.habitantes,"evasao_pct":100*t.evasao_aih/t.aih_residentes}
    for k,series in ratios.items():
        if not np.allclose(t[k],series,rtol=1e-12,atol=1e-10,equal_nan=True):raise ValueError(k)
        t[k]=series
    long=t.melt(id_vars=["ano","territorio"],var_name="indicador",value_name="valor").sort_values(["indicador","territorio","ano"])
    salvar(long,saida/"dados/t29_reproduzida.csv")
    estadual=t.query("territorio=='ES'")
    linhas(ler("sr116_temporal_es"),"ano",[("inclusiva_anual","Em algum mês do ano"),("inclusiva_em_algum_mes","Na mesma competência")],"SR116 e produção ambulatorial e hospitalar no ES","Estabelecimentos distintos","serie_sr116","CNES, SIA/PA e SIH/RD · interseção dos três conjuntos")
    linhas(estadual,"ano",[("sim_bruta","Bruta"),("sim_direta_2022","Padronizada pelo Censo 2022")],"Mortalidade cardiovascular de residentes do ES","Óbitos por 100 mil habitantes","mortalidade","SIM e população anual · causa básica final · todas as idades")
    linhas(estadual,"ano",[("evasao_aih","Evasão"),("atracao_aih","Atração")],"Fluxos hospitalares interestaduais do ES","AIHs principais","fluxos_sih","SIH/SUS · residentes atendidos fora do ES e não residentes atendidos no ES")
    linhas(estadual,"ano",[("cnes_media_SR_CARD","Serviço especializado SR116")],"Serviço cardiovascular cadastrado no ES","Média anual do número de estabelecimentos","cadastro","CNES · estoque mensal cadastrado")
    linhas(ler("i50_es"),"ano",[("i50_original","Causa básica original"),("i50_final","Causa básica final")],"Insuficiência cardíaca como causa básica no ES","Óbitos de residentes","i50","SIM · I50 · mecanismo da mudança histórica em investigação")
    linhas(ler("pa_janelas_es"),"competencia",[("congelada","Movimentos até dez/2024"),("janela_estendida","Incluindo movimentos de 2025 do recorte")],"Produção ambulatorial cardiovascular específica no ES","Quantidade aprovada","janelas_pa","SIA/PA e SIGTAP histórico · por local do prestador e competência de produção")
