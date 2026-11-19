"""Inventário e vigência por competência no diretório oficial do SIGTAP."""
import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile

from observatorio_sus.estudos.camila import sigtap
from observatorio_sus.estudos.camila.lote import ler, salvar
from observatorio_sus.extract.adquirir_objetos import FTPOficial
from observatorio_sus.io.custodia import sha256_arquivo, escrever_json


def obter(v,nome):
    local=v/"fontes/sigtap"/nome[:21]
    local.mkdir(exist_ok=True,parents=True)
    path=local/nome
    meta=path.with_suffix(".json")
    if meta.exists():
        if sha256_arquivo(path)!=json.loads(meta.read_text())["sha256"]:
            raise ValueError("SIGTAP divergiu do recibo")
        return path
    livre=shutil.disk_usage(v).free
    if livre<2_100_000_000:
        raise OSError("Disco insuficiente")
    cliente=FTPOficial(["ftp2.datasus.gov.br"])
    url="ftp://ftp2.datasus.gov.br/pub/sistemas/tup/downloads/"+nome
    with tempfile.TemporaryDirectory(dir=local) as tmp:
        st=Path(tmp)/nome
        with cliente.abrir(dict(uri_oficial=url,evidencia_origem="inventário FTP")) as (stream,rec),st.open("xb") as out:
            tamanho=int(rec["headers"]["Content-Length"])
            if tamanho>100_000_000:
                raise ValueError("Tamanho fora do lote")
            shutil.copyfileobj(stream,out)
        if st.stat().st_size!=tamanho:
            raise ValueError("Tamanho incompleto")
        with ZipFile(st) as z:
            if z.testzip() is not None:
                raise ValueError("CRC inválido")
            membros={i.filename:[i.file_size,f"{i.CRC:08x}"] for i in z.infolist()}
        rec.update(sha256=sha256_arquivo(st),bytes=tamanho,livre_antes=livre,membros=membros)
        if path.exists() and sha256_arquivo(path)!=rec["sha256"]:
            raise ValueError("Edição já presente diverge")
        if not path.exists():
            st.rename(path)
        escrever_json(meta,rec)
    return path


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("custodia",type=Path)
    a=p.parse_args()
    v=a.custodia
    lista=(v/"fontes/sigtap-downloads.txt").read_text().splitlines()
    candidatos={r["codigo_normalizado"] for r in ler(sigtap.CANDIDATOS) if r["dominio"]=="SIGTAP" and re.fullmatch(r"\d{10}",r["codigo_normalizado"])}
    for ano in range(2024,2013,-1):
        for mm in range(1,13):
            mes=f"{ano}{mm:02d}"
            nomes=sorted(n for n in lista if re.fullmatch("TabelaUnificada_"+mes+r"(_v\d+)?\.zip",n,re.I))
            if not nomes:
                print(mes,"ausente_no_indice",flush=True)
                continue
            try:
                path=obter(v,nomes[-1])
                procs,cbo=sigtap.ler_edicao(path,mes)
                codigos=candidatos|{c for c in procs if c.startswith("040603")}
                rows=[(mes,c,procs.get(c,""),int(c in procs)," ".join(k for k in ("225120","225210","225203") if (c,k) in cbo) if c==sigtap.CONSULTA else "") for c in sorted(codigos)]
                tab=path.with_suffix(".vigencia.csv")
                if not tab.exists():
                    salvar(tab,["competencia","codigo","descricao","presente","cbos_consulta"],rows)
                print(mes,path.name,len(procs),len(rows),sha256_arquivo(tab),flush=True)
            except Exception as exc:
                print(mes,type(exc).__name__,str(exc),flush=True)
