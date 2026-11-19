"""Conciliar o detalhe da reposição LT de dezembro de 2024 com cada margem do CP04."""
import argparse
import json
from pathlib import Path

import pandas as pd
from observatorio_sus.estudos.camila.lote import executar, produtos
from observatorio_sus.estudos.camila.territorio import TABELA

CAMPOS = ["QT_EXIST", "QT_SUS", "QT_NSUS", "QT_CONTR"]


def conferir_recortes(out):
    fonte = out/"reposicao-lt/202412"
    recibo = json.loads((fonte/"recibo.json").read_text())
    if produtos(fonte) != recibo["saidas"]:
        raise ValueError("Edição já verificada do LT divergente")
    def medir(stage):
        dados = pd.read_csv(fonte/"LT.csv.gz", dtype={"municipio": str, "cnes": str, "TP_LEITO": str, "CODLEITO": str})
        mapa = pd.read_csv(TABELA, dtype=str).set_index("cod_municipio_cnes").regiao_nome
        dados["regiao"] = dados.municipio.map(mapa)
        if dados.regiao.isna().any() or (dados[CAMPOS] < 0).any().any():
            raise ValueError("Resíduo territorial ou quantidade inválida")
        grupos = ["TP_LEITO", "CODLEITO"]
        detalhe = dados.groupby(["regiao","municipio","cnes",*grupos],as_index=False)[CAMPOS].sum()
        municipios = detalhe.groupby(["regiao","municipio",*grupos],as_index=False)[CAMPOS].sum()
        regioes = municipios.groupby(["regiao",*grupos],as_index=False)[CAMPOS].sum()
        estadual = regioes.groupby(grupos,as_index=False)[CAMPOS].sum().assign(regiao="ES")
        margens = pd.concat([regioes,estadual],ignore_index=True).melt(id_vars=["regiao",*grupos],value_vars=CAMPOS,
                          var_name="campo",value_name="detalhe_somado").rename(columns={"TP_LEITO":"tipo","CODLEITO":"codigo"})
        chave = ["regiao","tipo","codigo","campo"]
        cp = pd.read_csv(fonte/"confronto.csv",dtype={"tipo":str,"codigo":str})
        controle = cp.merge(margens,on=chave,how="outer",validate="one_to_one",indicator=True)
        if not controle._merge.eq("both").all() or not controle.cp04.eq(controle.detalhe_somado).all():
            raise ValueError("O detalhe diverge do CP04")
        for nome,df in [("estabelecimentos",detalhe),("municipios",municipios),("regioes",regioes),("estado",estadual),
                        ("reconciliacao_cp04",controle.drop(columns="_merge"))]:
            df.assign(competencia="202412").to_csv(stage/(nome+".csv"),index=False)
        pin=recibo["controles"]
        return dict(competencia="202412",fonte=pin["url"],sha256_dbc=pin["sha256"],bytes_dbc=pin["bytes"],
                    linhas_lidas=pin["linhas"],cnes_com_registro=int(detalhe.cnes.nunique()),
                    municipios_com_registro=int(municipios.municipio.nunique()),regioes=int(regioes.regiao.nunique()),
                    celulas_cp04=int(len(controle)),divergencias=0,sem_territorio=0)
    return executar(out/"recortes-lt-202412",{"reposicao":fonte/"recibo.json","detalhe":fonte/"LT.csv.gz",
                    "margens":fonte/"confronto.csv","pdr":TABELA},{"competencia":"202412","tolerancia":0},medir)


if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("out", type=Path)
    print(conferir_recortes(cli.parse_args().out)["controles"])
