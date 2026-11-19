"""Ampliação por objetos independentes da distribuição mensal oficial."""
import argparse
import json
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from lote_assistencial_camila import sih
from observatorio_sus.estudos.camila.lote import produtos
from observatorio_sus.extract.adquirir_objetos import FTPOficial
from observatorio_sus.extract.envelope_datasus import FAMILIAS, consulta
from observatorio_sus.io.custodia import sha256_arquivo, escrever_json


def obter(v, nome):
    familia,uf,comp=nome[:2],nome[2:4],"20"+nome[4:]
    raiz=v/"originais-assistencia"/familia/uf/comp
    path=raiz/(nome+".dbc")
    uri=f"ftp://ftp.datasus.gov.br/dissemin/publicos/{FAMILIAS[familia][1]}/{path.name}"
    obj=dict(familia=familia,uf=uf,competencia=comp,caminho=path.name,uri_oficial=uri)
    consulta(obj)
    raiz.mkdir(exist_ok=True,parents=True)
    receipt=raiz/"aquisicao.json"
    if receipt.exists():
        if sha256_arquivo(path)!=json.loads(receipt.read_text())["sha256"]:
            raise ValueError("Edição local incompatível")
        return path
    livre=shutil.disk_usage(v).free
    cliente=FTPOficial(timeout=25)
    with tempfile.TemporaryDirectory(dir=raiz) as tmp:
        stage=Path(tmp)/path.name
        with cliente.abrir(obj) as (stream,meta):
            size=int(meta["headers"]["Content-Length"])
            if not 0<size<=250_000_000 or livre<2_000_000_000+25*size:
                raise OSError("Tamanho fora do orçamento de processamento")
            with stage.open("xb") as out:
                while bloco:=stream.read(1<<20):
                    if out.tell()+len(bloco)>size:
                        raise ValueError("RETR excede SIZE")
                    out.write(bloco)
        if stage.stat().st_size!=size:
            raise ValueError("RETR incompleto")
        meta.update(bytes=size,sha256=sha256_arquivo(stage),livre_antes=livre)
        if path.exists():
            if sha256_arquivo(path)!=meta["sha256"]:
                raise ValueError("Colisão de edição")
        else:
            stage.rename(path)
        escrever_json(receipt,meta)
    return path


def executar_lote(v,nome):
    try:
        arq=obter(v,nome)
        if nome.startswith("RD"):
            recibo=sih(v,arq)
            if produtos(v/"sih"/nome/("20"+nome[4:]))!=recibo["saidas"]:
                raise ValueError("Saídas SIH divergentes")
        return dict(nome=nome,sha256=sha256_arquivo(arq),estado="calculado" if nome.startswith("RD") else "adquirido")
    except Exception as erro:
        return dict(nome=nome,estado="falha",tipo=type(erro).__name__,motivo=str(erro))


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("custodia",type=Path)
    p.add_argument("nomes",nargs="+")
    p.add_argument("--trabalhadores",type=int,default=2,choices=[1,2,3])
    a=p.parse_args()
    if len(a.nomes)!=len(set(a.nomes)):
        p.error("Objeto duplicado")
    with ThreadPoolExecutor(a.trabalhadores) as pool:
        for r in pool.map(lambda n:executar_lote(a.custodia,n),a.nomes):
            print(json.dumps(dict(r,utc=datetime.now(timezone.utc).isoformat())),flush=True)
