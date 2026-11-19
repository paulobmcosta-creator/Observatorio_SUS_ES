"""Sensibilidade do indicador de causa final ao capítulo perinatal da CID-10."""
import argparse
from pathlib import Path
import duckdb
import pandas as pd
from observatorio_sus.estudos.camila.lote import executar


def calcular(v,catalogo,destino):
    entradas={str(a):v/"institucional/matrizes"/str(a)/"pares.parquet" for a in range(2014,2025)}
    entradas.update(catalogo=catalogo,comparador=v/"sintese/sensibilidade_i50.csv")
    def medir(stage):
        cat=pd.read_csv(catalogo,dtype=str,keep_default_na=False)
        selecao=cat.loc[cat.descricao.str.contains(r"insuficiência (?:cardíaca|ventricular)",case=False,regex=True)]
        candidatos=set(selecao.cid)
        previstos={"I110","I119","I130","I132","I50","I500","I501","I509","P290"}
        if candidatos!=previstos:
            raise ValueError(f"Reavaliar os títulos candidatos nesta edição: {candidatos^previstos}")
        selecao.to_csv(stage/"titulos_examinados.csv",index=False)
        saidas=[]
        historico=pd.read_csv(entradas["comparador"]).query("territorio=='ES'").set_index("ano")
        with duckdb.connect() as db:
            for ano in range(2014,2025):
                db.read_parquet(str(entradas[str(ano)])).create_view("p",replace=True)
                tab=db.sql("""select mes,pdr,idade5,sexo,sum(case when left(f,3)='I50' or f in ('I110','I130','I132') then n else 0 end) ampliada_circulatoria,
                    sum(case when f='P290' then n else 0 end) neonatal
                    from p where tipo='2' and uf='ES' group by all""").df()
                tab["ampliada_entre_capitulos"]=tab.ampliada_circulatoria+tab.neonatal
                if tab.ampliada_circulatoria.sum()!=historico.at[ano,"ampliada"]:
                    raise ValueError("A sensibilidade diverge do produto do TCC")
                tab.insert(0,"ano",ano)
                saidas.append(tab)
        x=pd.concat(saidas)
        x.to_csv(stage/"sensibilidade_territorial.csv.gz",index=False)
        x.groupby("ano")[["ampliada_circulatoria","neonatal","ampliada_entre_capitulos"]].sum().to_csv(stage/"resumo.csv")
        return dict(anos=11,I119="o título exclui insuficiência",P290="sensibilidade neonatal entre capítulos")
    return executar(destino,entradas,{"elegibilidade":"residentes ES, não fetais, ano ocorrência","principal":"I50"},medir)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for nome in ["v","catalogo","destino"]:
        p.add_argument(nome,type=Path)
    a=p.parse_args()
    print(calcular(a.v,a.catalogo,a.destino)["controles"])
