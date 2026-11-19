"""Reconciliar pilotos e resumir séries assistenciais regionais para revisão local."""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from observatorio_sus.estudos.camila.lote import executar


def validar(v,assist,sih,destino):
    inputs={"sih":sih/"serie.csv","grupos":sih/"grupos.csv","cnes":assist/"cnes_mensal.csv",
            "sia":assist/"sia_mensal.csv","cobertura":assist/"cobertura.csv","equipes":v/"equipes/equipes_mensais.csv",
            "cp02":v.parent/"acervo/CP02/Resultados/SIH_PILOTO_PRODUCAO.csv",
            "espelho":assist/"confronto_espelho_primario.csv"}
    def apurar(stage):
        h=pd.read_csv(inputs["sih"],dtype={"competencia":str})
        grupos=pd.read_csv(inputs["grupos"],dtype={"competencia":str}).query("escopo=='atendimento_ES'")
        antigo=pd.read_csv(inputs["cp02"],dtype={"competencia_processamento":str}).query("atendimento=='ES'")
        antigo=antigo.rename(columns={"competencia_processamento":"competencia","aih_ident1":"aih_anterior"})
        conf=antigo.merge(grupos,on=["competencia","grupo"],how="left",validate="one_to_one")
        if len(conf)!=24 or not conf.aih.eq(conf.aih_anterior).all():
            raise ValueError("Os quatro pilotos SIH não reconciliam")
        conf.to_csv(stage/"qa_sih_pilotos.csv",index=False)
        est=pd.read_csv(inputs["cnes"],dtype={"competencia":str,"tipo":str})
        # Para HB a chave termina em vigência. Para as demais famílias os domínios definem a unidade.
        est=est.loc[~est.familia.eq("HB")|est.tipo.str.endswith("/vigente")].copy()
        men=est.groupby(["competencia","regiao","familia","medida"],as_index=False).quantidade.sum()
        equiv=pd.read_csv(inputs["equipes"],dtype={"competencia":str}).query("vigencia=='ativa_ao_fim'").groupby(
            ["competencia","regiao"],as_index=False).equipes.sum().rename(columns={"equipes":"quantidade"})
        men=pd.concat([men,equiv.assign(familia="EP",medida="equipe_ativa_ao_fim")],ignore_index=True)
        estado=men.groupby(["competencia","familia","medida"],as_index=False).quantidade.sum().assign(regiao="ES")
        men=pd.concat([men,estado],ignore_index=True)
        men.to_csv(stage/"estoque_mensal.csv",index=False)
        men["ano"]=men.competencia.str[:4]
        men.groupby(["ano","regiao","familia","medida"]).quantidade.agg(["count","mean","min","max"]).to_csv(stage/"estoque_anual_meses_observados.csv")
        producao=pd.read_csv(inputs["sia"],dtype={"movimento":str,"producao":str,"procedimento":str,"cbo":str})
        setores=producao.groupby(["movimento","vigencia","medida"],as_index=False).quantidade.sum()
        setores.to_csv(stage/"resumo_PA_por_vigencia.csv",index=False)
        eleg=producao.query("vigencia=='vigente' and medida=='aprov'").copy()
        eleg.groupby(["movimento","producao","regiao_atendimento","procedimento","cbo"]).quantidade.sum().to_csv(stage/"procedimentos_aprovados_elegiveis.csv.gz")
        hist= h.assign(ano=h.competencia.str[:4]).groupby("ano").atendimento_es.agg(["sum","count"])
        if len(hist)!=11 or not hist["count"].eq(12).all():
            raise ValueError("Série de atendimento SIH não cobre os 132 meses")
        hist.to_csv(stage/"sih_atendimento_es_anual.csv")
        fig,ax=plt.subplots(figsize=(9,4.8))
        ax.plot(hist.index,hist["sum"],marker="o")
        ax.set(xlabel="Ano de processamento",ylabel="AIHs principais (n)",title="Internações circulatórias atendidas no Espírito Santo")
        fig.tight_layout()
        fig.savefig(stage/"atendimento_ES.png",dpi=150)
        plt.close(fig)
        esp=pd.read_csv(inputs["espelho"],dtype=str,keep_default_na=False)
        return dict(celulas_pilotos_SIH=len(conf),competencias_PA=int(producao.movimento.nunique()),
                    divergencias_presenca_espelho=int((esp.presente_espelho!=esp.presente_primario).sum()),
                    divergencias_cbo_espelho=int((esp.cbo_espelho!=esp.cbo_primario).sum()),
                    definicao_estoque_anual="média somente dos meses observados para a medida e território")
    return executar(destino,inputs,{"sexo_idade":"mantidos nos cubos de cada competência","sih":"IDENT1"},apurar)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for nome in ("v","assist","sih","destino"):
        p.add_argument(nome,type=Path)
    a=p.parse_args()
    print(validar(a.v,a.assist,a.sih,a.destino)["controles"])
