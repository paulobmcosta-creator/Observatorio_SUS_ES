"""Produtos restritos da comparação demográfica e da sensibilidade de I50."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from observatorio_sus.estudos.camila.lote import executar


def sintetizar(v,destino):
    entradas={str(a):v/"estratos"/str(a)/"insuficiencia.csv" for a in range(2014,2025)}
    entradas["taxas"]=v/"taxas-ed2/indicadores.csv"
    def medir(stage):
        tab=[]
        for ano in range(2014,2025):
            df=pd.read_csv(entradas[str(ano)])
            for coluna in ["i50_final","ampliada","mencao_linhas","mencao_atestado","i50_original"]:
                if df[coluna].dtype != bool:
                    raise ValueError("Flag sem domínio booleano")
            df["mencao_uniao"]=df.mencao_linhas | df.mencao_atestado
            df["saida"]=df.i50_original & ~df.i50_final
            df["entrada"]=df.i50_final & ~df.i50_original & ~df.original.isin(["AUSENTE","INVALIDA"])
            df["retida"]=df.i50_final & df.i50_original
            cols=["i50_final","ampliada","mencao_linhas","mencao_atestado","mencao_uniao","i50_original","saida","entrada","retida"]
            for reg,g in [("ES",df),("ES sem Norte",df.loc[df.regiao.ne("Norte")]),*df.groupby("regiao")]:
                vals=g[cols].multiply(g.obitos,axis=0).sum()
                if vals.saida+vals.retida!=vals.i50_original:
                    raise ValueError("Transições I50 divergentes")
                tab.append(dict(ano=ano,territorio=reg,**vals.to_dict()))
        tab=pd.DataFrame(tab)
        es=tab.loc[tab.territorio.eq("ES")].set_index("ano")
        if es.loc[2022:2024,["i50_final","i50_original","mencao_atestado"]].values.tolist()!=[[292,330,2889],[75,398,2948],[9,436,3040]]:
            raise ValueError("Regressão I50 ES")
        tab.to_csv(stage/"sensibilidade_i50.csv",index=False)
        fig,ax=plt.subplots(figsize=(9,5))
        es[["i50_final","i50_original","ampliada","mencao_atestado"]].rename(columns={
            "i50_final":"I50 final","i50_original":"I50 original","ampliada":"Causa final ampliada",
            "mencao_atestado":"Menção no atestado"}).plot(ax=ax,marker="o")
        ax.set(xlabel="Ano do óbito",ylabel="Declarações (n)",title="Insuficiência cardíaca em residentes do Espírito Santo")
        fig.tight_layout()
        fig.savefig(stage/"insuficiencia.png",dpi=150)
        plt.close(fig)
        d=pd.read_csv(entradas["taxas"])
        d=d.query("grupo=='G0' and universo=='30-69' and sexo_sim=='T'")
        for c in (2022,2010):
            fig,ax=plt.subplots(figsize=(9,5))
            d.loc[(d.censo==c)&d.territorio.isin(["ES","Norte","ES sem Norte"])].pivot(
                index="ano",columns="territorio",values="direta_100mil").plot(ax=ax,marker="o")
            ax.set(xlabel="Ano do óbito",ylabel="Óbitos por 100 mil",title=f"Mortalidade circulatória de 30–69 anos • padrão Brasil {c}")
            fig.tight_layout()
            fig.savefig(stage/f"prematura_{c}.png",dpi=150)
            plt.close(fig)
        return dict(anos=len(es),regressao_I50="3 anos × 3 medidas",compartimento="restrito")
    return executar(destino,entradas,{"pdr":"2024","ampliada":["I50","I110","I130","I132"]},medir)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("custodia_v3",type=Path)
    p.add_argument("destino",type=Path)
    a=p.parse_args()
    print(sintetizar(a.custodia_v3,a.destino)["controles"])
