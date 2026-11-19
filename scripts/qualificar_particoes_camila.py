"""Recuperar chaves de estabelecimento e atributos clínicos ausentes dos agregados v3."""
import argparse
import csv
import json
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

from oferta_producao_camila import blocos
from observatorio_sus.estudos.camila import sigtap, territorio
from observatorio_sus.estudos.camila.lote import executar, ler
from observatorio_sus.io.custodia import sha256_arquivo

CHAVES = {
    "ST":"TP_UNID TPGESTAO NAT_JUR VINC_SUS ATENDAMB ATENDHOS",
    "SR":"SERV_ESP CLASS_SR AMB_SUS HOSP_SUS TERCEIRO",
    "HB":"SGRUPHAB CMPT_INI CMPT_FIM",
    "LT":"TP_LEITO CODLEITO", "EQ":"TIPEQUIP CODEQUIP IND_SUS",
    "PF":"CBO VINCULAC PROF_SUS", "EP":"TIPO_EQP",
    "PA":"PA_CMP PA_PROC_ID PA_CBOCOD PA_DOCORIG PA_NIVCPL"
}
VALORES = {"LT":["QT_EXIST","QT_SUS","QT_NSUS"],"EQ":["QT_EXIST","QT_USO"],
           "PF":["HORA_AMB","HORAHOSP","HORAOUTR"],"PA":["PA_QTDAPR","PA_QTDPRO"]}
PROF = ("225120","225210","225203")
MESES = tuple(f"{ano}{m:02d}" for ano in range(2014,2025) for m in range(1,13))


def situacao_equipe(ini, fim, motivo, mes):
    """Mesma vigência e sentinela da reconciliação EP anterior."""
    aberta = fim=="900001" and motivo=="00"
    def valido(x):
        return len(x)==6 and x.isdigit() and "190001"<=x<="209912" and "01"<=x[-2:]<="12"
    if not valido(ini) or not (aberta or valido(fim)) or (not aberta and fim<ini):
        return "datas_indeterminadas"
    if ini>mes or (not aberta and fim<mes):
        return "fora_da_competencia"
    return "desativada_na_competencia" if not aberta and fim==mes else "ativa_ao_fim"


def extrair(fam,path,mes,stage,candidatos):
    """Agrupar sem carregar CPF, CNS, nome ou identificadores de autorização."""
    origem,mun,comp = ("PA_CODUNI","PA_UFMUN","PA_MVM") if fam=="PA" else ("CNES","CODUFMUN","COMPETEN")
    chaves=[origem,mun,*CHAVES[fam].split()]
    valores=VALORES.get(fam,[])
    campos=[comp,*chaves,*valores]
    if fam=="EP":
        campos+=["IDEQUIPE","DT_ATIVA","DT_DESAT","MOTDESAT"]
    with path.open("rb") as f:
        n,h,t=struct.unpack_from("<IHH",f.read(32),4)
        esquema=[f.read(32)[:11].split(bytes(1))[0].decode("ascii") for _ in range((h-33)//32)]
    if shutil.disk_usage(stage).free<n*t+h+path.stat().st_size+500_000_000:
        raise OSError("Sem espaço para a decodificação")
    qa=dict(cabecalho=n,ativos=0,excluidos=0,selecionados=0,campos=campos,esquema=esquema)
    partes=[]
    with tempfile.TemporaryDirectory(dir=stage) as temp:
        tmp=Path(temp)
        shutil.copyfile(path,tmp/"orig.dbc")
        subprocess.run([sys.executable,"-c","from pyreaddbc.readdbc import _dbc2dbf; _dbc2dbf('orig.dbc','dados.dbf')"],cwd=temp,check=True)
        for b,_ in blocos(tmp/"dados.dbf",campos):
            ativo=b["estado"]==b" "
            excl=b["estado"]==b"*"
            if not (ativo|excl).all() or not (b[comp][ativo]==mes.encode()).all():
                raise ValueError(f"Competência ou marcador {path.name}")
            qa["ativos"]+=int(ativo.sum())
            qa["excluidos"]+=int(excl.sum())
            if fam=="PA":
                ativo &= np.isin(b["PA_PROC_ID"],candidatos)
            if fam=="PF":
                ativo &= np.isin(b["CBO"],[s.encode() for s in PROF])
            selecionado=b[ativo]
            qa["selecionados"]+=len(selecionado)
            if not len(selecionado):
                continue
            df=pd.DataFrame({c:pd.Series(selecionado[c]).str.decode("latin1").str.strip() for c in campos if c!=comp})
            if fam=="EP":
                partes.append(df)
                continue
            for c in valores:
                df[c]=pd.to_numeric(df[c].replace("",None),errors="raise").astype("Int64")
            df["linhas"]=1
            partes.append(df.groupby(chaves,as_index=False,sort=False)[["linhas",*valores]].sum(min_count=1))
    if qa["ativos"]+qa["excluidos"]!=n:
        raise ValueError("Balanço DBF divergente")
    if fam=="EP":
        df=pd.concat(partes,ignore_index=True)
        df["vigencia"]=[situacao_equipe(*r,mes) for r in df[["DT_ATIVA","DT_DESAT","MOTDESAT"]].itertuples(index=False,name=None)]
        valid=df.IDEQUIPE.str.strip("0").ne("")
        cat=df.loc[valid,[*chaves,"vigencia","IDEQUIPE"]].drop_duplicates()
        conflito=cat.IDEQUIPE.duplicated(keep=False)
        qa["conflitos"]=cat.loc[conflito,"IDEQUIPE"].nunique()
        df=cat.loc[~conflito].groupby([*chaves,"vigencia"]).size().rename("linhas").reset_index()
        qa["sem_id"]=int((~valid).sum())
    elif partes:
        df=pd.concat(partes).groupby(chaves,as_index=False)[["linhas",*valores]].sum(min_count=1)
        if df.linhas.sum()!=qa["selecionados"]:
            raise ValueError("Balanço da seleção divergente")
    else:
        df=pd.DataFrame(columns=[*chaves,"linhas",*valores])
    df.rename(columns={origem:"cnes",mun:"municipio"}).to_csv(stage/(fam+".csv.gz"),index=False)
    return qa


def processar(v,out,anos):
    auditoria=v/"auditoria-final"
    inv=auditoria/"originais.csv"
    if sha256_arquivo(inv)!=json.loads((auditoria/"verificacao.json").read_text())["sha256_origem"]:
        raise ValueError("Inventário basal modificado")
    itens={(r["familia"],r["edicao"]):r for r in ler(inv) if r["familia"] in CHAVES}
    hist=v/"assistencia-final/sigtap_historico.csv.gz"
    cod=pd.read_csv(hist,dtype=str).codigo.unique()
    candidatos=np.array([c.encode() for c in cod])
    for mes in MESES:
        if int(mes[:4]) not in anos:
            continue
        arquivos={}
        for fam in CHAVES:
            if fam=="LT" and mes=="202412":
                continue
            if fam=="SR":
                pasta=out/"originais-assistencia/SR/ES"/mes
                path=pasta/("SRES"+mes[2:]+".dbc")
                esperado=json.loads((pasta/"aquisicao.json").read_text())["sha256"]
            else:
                item=itens[fam,mes]
                path=Path(item["arquivo_local"])
                esperado=item["sha256"]
            if sha256_arquivo(path)!=esperado:
                raise ValueError(f"Hash incompatível {fam}/{mes}")
            arquivos[fam]=path
        def medir(stage):
            return {fam:extrair(fam,path,mes,stage,candidatos) for fam,path in arquivos.items()}
        rec=executar(out/"particoes"/mes,{**arquivos,"candidatos":hist},{"competencia":mes,"cbo":list(PROF)},medir,
                     [Path(sys.modules[blocos.__module__].__file__)])
        print(mes,rec["id"],flush=True)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("v",type=Path)
    p.add_argument("out",type=Path)
    p.add_argument("anos",nargs="*",type=int)
    a=p.parse_args()
    processar(a.v,a.out,a.anos or list(range(2014,2025)))
