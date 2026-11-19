"""Estoques CNES e produção PA selecionada por competência clínica do procedimento."""
import argparse
import csv
import gzip
import json
import shutil
import struct
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from observatorio_sus.estudos.camila import sigtap, territorio
from observatorio_sus.estudos.camila.lote import executar, ler, salvar
from observatorio_sus.io.custodia import sha256_arquivo

CHAVES={"ST":["TP_UNID","VINC_SUS"],"HB":["SGRUPHAB","CMPT_INI","CMPT_FIM"],"LT":["TP_LEITO","CODLEITO"],
        "EQ":["TIPEQUIP","CODEQUIP","IND_SUS"],"PF":["CBO","PROF_SUS","VINCULAC"],"EP":["TIPO_EQP"]}
VALORES={"LT":["QT_EXIST","QT_SUS","QT_NSUS"],"EQ":["QT_EXIST","QT_USO"],"PF":["HORAOUTR","HORAHOSP","HORA_AMB"]}
PA="PA_MVM PA_CMP PA_PROC_ID PA_CBOCOD PA_MUNPCN PA_UFMUN PA_SEXO PA_IDADE PA_QTDAPR PA_QTDPRO".split()


def blocos(dbf,selecionados):
    with dbf.open("rb") as f:
        cab=f.read(32)
        n,h,t=struct.unpack_from("<IHH",cab,4)
        campos={"estado":(0,1)}
        offset=1
        for _ in range((h-33)//32):
            b=f.read(32)
            nome=b[:11].split(bytes(1))[0].decode("ascii")
            campos[nome]=offset,b[16]
            offset+=b[16]
        if offset!=t or f.read(1)!=b"\r" or not set(selecionados)<=campos.keys():
            raise ValueError(f"Layout DBF incompatível: {set(selecionados)-campos.keys()}")
        cols=["estado",*selecionados]
        dt=np.dtype(dict(names=cols,formats=[f"S{campos[k][1]}" for k in cols],
                         offsets=[campos[k][0] for k in cols],itemsize=t))
        lidos=0
        while lidos<n:
            tam=min(n-lidos,100000)
            raw=f.read(tam*t)
            if len(raw)!=tam*t:
                raise ValueError("DBF truncado")
            yield np.frombuffer(raw,dtype=dt),n
            lidos+=tam
        if f.read() not in (b"",b"\x1a"):
            raise ValueError("Bytes inesperados após registros DBF")


def apurar(v,arq,dominios,versao):
    nome=arq.stem
    fam=nome[:2]
    mes="20"+nome[4:]
    campos=(PA if fam=="PA" else ["CNES","CODUFMUN","COMPETEN",*CHAVES[fam],*VALORES.get(fam,[])])
    if fam=="EP":
        campos.extend(["IDEQUIPE","DT_ATIVA","DT_DESAT"])
    entradas={"dbc":arq,"territorio":territorio.TABELA}
    if fam=="PA":
        entradas["candidatos"]=sigtap.CANDIDATOS
        # Competências adjacentes podem aparecer no movimento. Registrar vigência por PA_CMP.
        from datetime import date
        from dateutil.relativedelta import relativedelta
        data=date(int(mes[:4]),int(mes[4:]),1)
        for lag in range(13):
            prod=(data-relativedelta(months=lag)).strftime("%Y%m")
            if prod in dominios:
                entradas[prod]=dominios[prod]
    def medir(stage):
        cont=Counter()
        medidas=Counter()
        qa=Counter()
        reg=territorio.mapa()
        candidatos={r["codigo_normalizado"] for r in ler(sigtap.CANDIDATOS) if r["dominio"]=="SIGTAP" and len(r["codigo_normalizado"])==10}
        catalogo={}
        if fam=="PA":
            for k,p in entradas.items():
                if k.isdigit():
                    catalogo[k]={r["codigo"]:r for r in ler(p)}
                    candidatos.update(catalogo[k])
        codigos=np.array([c.encode() for c in candidatos])
        unicos=set()
        with arq.open("rb") as stream:
            header=stream.read(32)
        registros,tam_header,tam_registro=struct.unpack_from("<IHH",header,4)
        minimo=tam_header+registros*tam_registro+arq.stat().st_size+300_000_000
        if shutil.disk_usage(stage).free<minimo:
            raise OSError(f"Espaço insuficiente para o DBF e leitura do lote ({minimo})")
        with tempfile.TemporaryDirectory(dir=stage) as tmp:
            shutil.copyfile(arq,Path(tmp)/"fonte.dbc")
            subprocess.run([sys.executable,"-c","from pyreaddbc.readdbc import _dbc2dbf; _dbc2dbf('fonte.dbc','dados.dbf')"],
                           cwd=tmp,check=True)
            for bloco,n in blocos(Path(tmp)/"dados.dbf",campos):
                marcador=bloco["estado"]
                ativos=marcador==b" "
                excluidos=marcador==b"*"
                if not (ativos|excluidos).all():
                    raise ValueError("Marcador DBF inválido")
                qa["cabecalho"]=n
                qa["excluidos"]+=int(excluidos.sum())
                qa["ativos"]+=int(ativos.sum())
                bloco=bloco[ativos]
                if fam=="PA":
                    if not (bloco["PA_MVM"]==mes.encode()).all():
                        raise ValueError("PA_MVM incompatível")
                    mask=np.isin(bloco["PA_PROC_ID"],codigos) | (np.frombuffer(bloco["PA_PROC_ID"].tobytes(),dtype="S10").view("S1").reshape(-1,10)[:,:6].copy().view("S6").ravel()==b"040603")
                    bloco=bloco[mask]
                    if not len(bloco):
                        continue
                df=pd.DataFrame({c:pd.Series(bloco[c]).str.decode("latin1").str.strip() for c in campos})
                if fam=="PA":
                    df["valor_aprovado"]=pd.to_numeric(df.PA_QTDAPR,errors="raise").astype(int)
                    df["valor_apresentado"]=pd.to_numeric(df.PA_QTDPRO,errors="raise").astype(int)
                    df["regiao_res"]=df.PA_MUNPCN.map(reg).fillna("OUTRO_OU_IGN")
                    df["regiao_at"]=df.PA_UFMUN.map(reg).fillna("OUTRO_OU_IGN")
                    keys=["PA_CMP","PA_PROC_ID","PA_CBOCOD","regiao_res","regiao_at","PA_SEXO","PA_IDADE"]
                    for k,g in df.groupby(keys,sort=False).agg(linhas=("PA_CMP","size"),aprov=("valor_aprovado","sum"),apres=("valor_apresentado","sum")).iterrows():
                        prod,proc,cbo,*_=k
                        rr=catalogo.get(prod,{}).get(proc)
                        status="sem_edicao_da_producao" if prod not in catalogo else "ausente" if not rr or rr["presente"]!="1" else "vigente"
                        if status=="vigente" and proc==sigtap.CONSULTA and cbo not in rr["cbos_consulta"].split():
                            status="cbo_fora_do_recorte"
                        for med,val in g.items():
                            medidas[(*k,status,med)]+=int(val)
                else:
                    if not df.COMPETEN.eq(mes).all():
                        raise ValueError("Competência CNES divergente")
                    df["regiao"]=df.CODUFMUN.map(reg).fillna("ES_IGN")
                    keys=["regiao",*CHAVES[fam]]
                    if fam in ("EP","ST"):
                        ids=df.IDEQUIPE if fam=="EP" else df.CNES
                        for k in zip(df.CNES,ids):
                            if k in unicos:
                                qa["chaves_repetidas"]+=1
                            unicos.add(k)
                    for val in VALORES.get(fam,[]):
                        df[val]=pd.to_numeric(df[val].replace("",None),errors="raise")
                        qa["ausente_"+val]+=int(df[val].isna().sum())
                    gr=df.groupby(keys,sort=False)
                    cont.update(gr.size().to_dict())
                    for val in VALORES.get(fam,[]):
                        for k,soma in gr[val].sum(min_count=1).dropna().items():
                            medidas[(*k,val)]+=int(soma)
                    if fam=="EP":
                        qa["desativacao_informada"]+=int((~df.DT_DESAT.isin(["","00000000"])).sum())
        if qa["ativos"]+qa["excluidos"]!=qa["cabecalho"]:
            raise ValueError("Margem de registros DBF divergente")
        if fam!="PA":
            if cont.total()!=qa["ativos"]:
                raise ValueError("Margem de estoque divergente")
            salvar(stage/"estoque.csv",["regiao",*CHAVES[fam],"registros"],((*k,n) for k,n in sorted(cont.items())))
        keys=(["competencia_producao","procedimento","cbo","regiao_res","regiao_at","sexo","idade","vigencia"] if fam=="PA" else ["regiao",*CHAVES[fam]])
        with gzip.open(stage/"medidas.csv.gz","xt",encoding="utf8",newline="") as stream:
            writer=csv.writer(stream)
            writer.writerow([*keys,"medida","valor"])
            writer.writerows((*k,n) for k,n in sorted(medidas.items()))
        return dict(familia=fam,competencia=mes,qa=dict(qa),cobertura="estado por competência de movimento/cadastro")
    return executar(v/versao/nome/mes,entradas,{"familia":fam,"competencia":mes,"campos":campos},
                    medir,[Path(sigtap.__file__),Path(territorio.__file__)])


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("v",type=Path)
    p.add_argument("nomes",nargs="+")
    p.add_argument("--versao",default="oferta-serie")
    a=p.parse_args()
    dom={p.name.split("_")[1][:6]:p for p in (a.v/"fontes/sigtap").rglob("*.vigencia.csv")}
    for nome in a.nomes:
        arq=a.v/"originais-assistencia"/nome[:2]/"ES"/("20"+nome[4:])/(nome+".dbc")
        if not arq.exists() and nome in ("STES2412","HBES2412"):
            arq=a.v.parent/"acervo/CP01/CNES"/(nome+".dbc")
        if not arq.exists():
            print(nome,"original_ausente",flush=True)
            continue
        try:
            print(nome,apurar(a.v,arq,dom,a.versao)["id"],flush=True)
        except Exception as exc:
            print(nome,"falha",type(exc).__name__,str(exc),flush=True)
