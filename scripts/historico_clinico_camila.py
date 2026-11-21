"""Qualificar descrições e compatibilidades pela edição SIGTAP da produção."""
import argparse
import csv
import io
import json
import sys
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
from observatorio_sus.estudos.camila import sigtap
from observatorio_sus.estudos.camila.lote import executar, ler
from observatorio_sus.io.custodia import sha256_arquivo
from qualificar_particoes_camila import MESES, PROF, extrair

REAB = ("0301070229","0302040030","0302040048","0302040056","0302040064")
EXAMES = ("0205010032","0208010025","0208010033","0211020010","0211020036","0211020044","0211020052","0211020060")
DOPPLER = "0205010040"
REL = {"modalidade":["CO_MODALIDADE"],"registro":["CO_REGISTRO"],"ocupacao":["CO_OCUPACAO"],
       "servico":["CO_SERVICO","CO_CLASSIFICACAO"],"habilitacao":["CO_HABILITACAO","NU_GRUPO_HABILITACAO"]}


def classe(codigo):
    if codigo==DOPPLER:
        return "B","doppler_contextual"
    if codigo==sigtap.CONSULTA:
        return "B","consulta_cbo"
    if codigo in EXAMES:
        return "A","exames_especificos"
    if codigo in (REAB[1],REAB[2],REAB[4]):
        return "A","fisioterapia_especifica"
    if codigo in REAB:
        return "D","reabilitacao_em_revisao"
    return "D","intervencao_em_revisao"


def historico(v,out):
    arquivos={f.name.split("_")[1][:6]:f for f in (v/"fontes/sigtap").rglob("*.zip")}
    if set(arquivos)!=set(MESES):
        raise ValueError("Edições SIGTAP incompletas")
    for p in arquivos.values():
        if sha256_arquivo(p)!=json.loads(p.with_suffix(".json").read_text())["sha256"]:
            raise ValueError(p)
    antigo=v/"assistencia-final/sigtap_historico.csv.gz"
    def medir(stage):
        base=pd.read_csv(antigo,dtype=str,keep_default_na=False)
        selecao=set(base.codigo)|set(REAB)
        proc,ser,hab,cbo=[],[],[],[]
        for mes,path in sorted(arquivos.items()):
            with ZipFile(path) as z:
                campos=["CO_PROCEDIMENTO","NO_PROCEDIMENTO","TP_COMPLEXIDADE","TP_SEXO","VL_IDADE_MINIMA","VL_IDADE_MAXIMA","QT_MAXIMA_EXECUCAO"]
                atuais={r[0]:r[1:] for r in sigtap.registros(z,"tb_procedimento",campos,mes) if r[0] in selecao}
                detalhes={c:d for c,d in sigtap.registros(z,"tb_descricao",["CO_PROCEDIMENTO","DS_PROCEDIMENTO"],mes) if c in selecao}
                rels={}
                for nome,cols in REL.items():
                    links=defaultdict(set)
                    for c,*atrib in sigtap.registros(z,"rl_procedimento_"+nome,["CO_PROCEDIMENTO",*cols],mes):
                        if c in selecao: links[c].add("/".join(atrib))
                    rels[nome]=links
                for c in sorted(selecao):
                    categoria,grupo=classe(c)
                    vals=atuais.get(c,[""]*6)
                    proc.append([mes,c,*vals,detalhes.get(c,""),c[:2],c[:4],c[:6],int(c in atuais),categoria,grupo,
                                 *[" ".join(sorted(x[c])) for x in rels.values()]])
                nomes=dict(sigtap.registros(z,"tb_servico",["CO_SERVICO","NO_SERVICO"],mes))
                ser.extend((mes,s,k,nomes.get(s,""),desc) for s,k,desc in sigtap.registros(z,"tb_servico_classificacao",["CO_SERVICO","CO_CLASSIFICACAO","NO_CLASSIFICACAO"],mes))
                hab.extend((mes,*r) for r in sigtap.registros(z,"tb_habilitacao",["CO_HABILITACAO","NO_HABILITACAO"],mes))
                layout=list(csv.DictReader(io.StringIO(z.read("tb_ocupacao_layout.txt").decode("latin1"))))
                a,b=[slice(int(x["Inicio"])-1,int(x["Fim"])) for x in layout[:2]]
                for linha in z.read("tb_ocupacao.txt").splitlines():
                    c=linha[a].decode("latin1").strip()
                    if c in PROF: cbo.append((mes,c,linha[b].decode("latin1").strip()))
        df=pd.DataFrame(proc,columns="competencia codigo descricao complexidade sexo_normativo idade_min idade_max qt_max finalidade grupo subgrupo forma presente classe grupo_clinico".split()+list(REL))
        conf=base.merge(df,on=["competencia","codigo"],validate="one_to_one",suffixes=("_v3",""))
        if len(conf)!=len(base) or not (conf.presente_v3.astype(int)==conf.presente).all() or not (conf.descricao==conf.descricao_v3).all():
            raise ValueError("Catálogo v3 divergente")
        attrs=["descricao","finalidade","complexidade","idade_min","idade_max","qt_max","sexo_normativo","modalidade","registro","ocupacao","servico","habilitacao","presente"]
        df=df.sort_values(["codigo","competencia"])
        df["versao_atributos"]=df.groupby("codigo")[attrs].transform(lambda s:s.ne(s.shift())).any(axis=1).groupby(df.codigo).cumsum()
        df.to_csv(stage/"procedimentos.csv.gz",index=False)
        for nome,rows,cols in [("servicos",ser,"competencia servico classificacao descricao_servico descricao_classe"),
                               ("habilitacoes",hab,"competencia codigo descricao"),("ocupacoes",cbo,"competencia codigo descricao")]:
            pd.DataFrame(rows,columns=cols.split()).to_csv(stage/(nome+".csv.gz"),index=False)
        return {"edicoes":len(arquivos),"codigos":len(selecao),"celulas_comparadas_v3":len(conf)}
    return executar(out/"historico",{**arquivos,"v3":antigo},{"tabelas":list(REL)},medir,[Path(sigtap.__file__)])


def adicional(v,out):
    """Ler somente a seleção nova de reabilitação ausente da projeção anterior."""
    inv=v/"auditoria-final/originais.csv"
    if sha256_arquivo(inv)!=json.loads(inv.with_name("verificacao.json").read_text())["sha256_origem"]:
        raise ValueError("Inventário basal divergente")
    for r in ler(inv):
        if r["familia"]!="PA":continue
        mes=r["edicao"]; path=Path(r["arquivo_local"])
        if sha256_arquivo(path)!=r["sha256"]:raise ValueError(path)
        def medir(stage):
            return extrair("PA",path,mes,stage,np.array([c.encode() for c in REAB]))
        rec=executar(out/"reabilitacao"/mes,{"PA":path},{"codigos":list(REAB)},medir,[Path(sys.modules[extrair.__module__].__file__)])
        print(mes,rec["id"],flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("v",type=Path)
    p.add_argument("out",type=Path)
    p.add_argument("modo",choices=["historico","reabilitacao"])
    a=p.parse_args()
    if a.modo=="historico":
        print(historico(a.v,a.out)["controles"])
    else:
        adicional(a.v,a.out)
