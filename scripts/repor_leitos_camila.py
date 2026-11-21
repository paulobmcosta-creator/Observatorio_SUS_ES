"""Restituir LTES2412 e comparar código, tipo e estoques com a evidência independente CP04."""
import argparse
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
import pandas as pd

from adquirir_servicos_camila import FTPEstendido
from assistencia_ftp_camila import obter
from oferta_producao_camila import blocos
from observatorio_sus.estudos.camila import assistencia,territorio
from observatorio_sus.estudos.camila.lote import executar,ler
from observatorio_sus.extract.adquirir_objetos import FTPOficial
from observatorio_sus.io.custodia import sha256_arquivo


def recuperar(v,out):
    cp=v.parent/"acervo/CP04"
    evidencia=cp/"Evidencias/LTES2412.dbc.proveniencia.json"
    referencia=cp/"Resultados/CNES_LT_202412_ESTOQUE_POR_CODIGO.csv"
    pin=json.loads(evidencia.read_text())
    prev={(r["regiao"],r["tp_leito"],r["cod_leito"],r["campo"]):int(r["quantidade"]) for r in ler(referencia)}
    if pin["arquivo"]!="LTES2412.dbc" or set(k[0] for k in prev)!={"ES",*territorio.PAGINAS}:
        raise ValueError("Escopo do CP04 incompatível")
    dbc=obter(out,"LTES2412",cliente=FTPOficial(fabrica=FTPEstendido))
    meta=dbc.parent/"aquisicao.json"
    if (dbc.stat().st_size!=pin["bytes"] or sha256_arquivo(dbc)!=pin["sha256"]
            or json.loads(meta.read_text())["uri_oficial"]!=pin["url_catalogo"]):
        raise ValueError("Divergência com o CP04; bytes em custódia, incorporação bloqueada")
    def medir(stage):
        mapa=territorio.mapa()
        valores=["QT_EXIST","QT_SUS","QT_NSUS","QT_CONTR"]
        chaves=["cnes","municipio","TP_LEITO","CODLEITO"]
        dados=[]; atual=Counter()
        with TemporaryDirectory(dir=stage) as tmp:
            tmp=Path(tmp)
            shutil.copyfile(dbc,tmp/"fonte.dbc")
            subprocess.run([sys.executable,"-c","from pyreaddbc.readdbc import _dbc2dbf; _dbc2dbf('fonte.dbc','leitos.dbf')"],cwd=tmp,check=True)
            campos=["CNES","CODUFMUN","TP_LEITO","CODLEITO","COMPETEN",*valores]
            for bloco,_ in blocos(tmp/"leitos.dbf",campos):
                for linha in bloco:
                    if linha["estado"]==b"*":continue
                    if linha["estado"]!=b" ":raise ValueError("Marcador DBF inválido")
                    r={k:linha[k].decode("ascii").strip() for k in campos}
                    if r["COMPETEN"]!="202412":raise ValueError("Competência divergente")
                    reg=mapa.get(r["CODUFMUN"],"INDETERMINADA")
                    med=[int(r[c] or 0) for c in valores]
                    dados.append([r["CNES"],r["CODUFMUN"],r["TP_LEITO"],r["CODLEITO"],1,*med])
                    for c,val in zip(valores,med):
                        for t in [reg,"ES"]:atual[t,r["TP_LEITO"],r["CODLEITO"],c]+=val
        diff=[(k,atual.get(k),prev.get(k)) for k in atual.keys()|prev.keys() if atual.get(k)!=prev.get(k)]
        if diff:raise ValueError(f"Divergências de estoque com CP04: {diff[:8]}")
        detalhado=pd.DataFrame(dados,columns=[*chaves,"linhas",*valores]).groupby(chaves,as_index=False).sum()
        detalhado.to_csv(stage/"LT.csv.gz",index=False)
        pd.DataFrame([(*k,n,atual[k]) for k,n in sorted(prev.items())],columns=["regiao","tipo","codigo","campo","cp04","reposto"]).to_csv(stage/"confronto.csv",index=False)
        return dict(bytes=pin["bytes"],sha256=pin["sha256"],url=pin["url_catalogo"],celulas=len(prev),divergencias=0,
                    regioes=sorted(territorio.PAGINAS),sem_regiao=sum(r[4] for r in dados if r[1] not in mapa),linhas=len(dados))
    return executar(out/"reposicao-lt"/"202412",{"original":dbc,"aquisicao":meta,"cp04":evidencia,"totais":referencia,"pdr":territorio.TABELA},
                    {"familia":"LT","UF":"ES","competencia":"202412","tolerancia":0},medir,[Path(assistencia.__file__)])


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("v",type=Path)
    p.add_argument("out",type=Path)
    args=p.parse_args()
    print(recuperar(args.v,args.out)["controles"])
