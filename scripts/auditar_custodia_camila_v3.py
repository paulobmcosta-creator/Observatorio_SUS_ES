"""Inventário restrito e confronto entre recibos e bytes preservados."""
import argparse
import json
import shutil
from collections import Counter
from pathlib import Path

from observatorio_sus.estudos.camila.lote import ler, produtos, salvar
from observatorio_sus.io.custodia import sha256_arquivo, escrever_json


def auditar(v,catalogo,destino):
    destino.mkdir(parents=True,exist_ok=False)
    top=v.parent
    linhas=[]
    def original(path,esperado,tamanho,url,edicao,tipo,origem):
        valor=sha256_arquivo(path)
        if valor!=esperado or path.stat().st_size!=int(tamanho):
            raise ValueError(f"Original divergente: {path}")
        linhas.append((tipo,edicao,str(path),path.stat().st_size,valor,url,str(origem)))
    sim=top/"continuacao-nacional/manifesto-originais.csv"
    for r in ler(sim):
        original(Path(r["arquivo"]),r["sha256_verificado"],r["bytes"],r["url"],r["ano"],"SIM",sim)
    for rp in (v/"originais-assistencia").rglob("aquisicao.json"):
        meta=json.loads(rp.read_text(encoding="utf8"))
        path,=rp.parent.glob("*.dbc")
        original(path,meta["sha256"],meta["bytes"],meta["uri_oficial"],rp.parent.name,path.stem[:2],rp)
    for root in (v/"fontes/pops",top/"acervo/consolidado/1B_Populacao_Originais"):
        for path in root.glob("*.zip"):
            rp=path.with_suffix(".zip.proveniencia.json")
            m=json.loads(rp.read_text(encoding="utf8"))
            original(path,m["sha256"],m["bytes"],m["url_catalogo"],"20"+path.stem[-2:],"POPSVS",rp)
    for path in (v/"fontes/sigtap").rglob("*.zip"):
        rp=path.with_suffix(".json")
        m=json.loads(rp.read_text(encoding="utf8"))
        original(path,m["sha256"],m["bytes"],m["uri_oficial"],path.name.split("_")[1],"SIGTAP",rp)
    # Insumos Work de SIH/CNES reaproveitados, identificados pelos pinos da linha de base.
    repo=Path(__file__).resolve().parents[1]
    for r in ler(repo/"config/estudos/pilotos_assistenciais_camila.csv"):
        if not r["membro"].endswith(".dbc"):
            continue
        path=top/"acervo"/r["membro"]
        original(path,r["sha256"],path.stat().st_size,"acervo Work com origem descrita no manifesto","20"+path.stem[-4:],path.stem[:2],r["membro"])
    salvar(destino/"originais.csv",["familia","edicao","arquivo_local","bytes","sha256","fonte","evidencia"],sorted(linhas))
    recibos=[]
    for rp in v.rglob("recibo.json"):
        if any(parte.startswith(".pendente-") for parte in rp.parts):
            continue
        rec=json.loads(rp.read_text(encoding="utf8"))
        if produtos(rp.parent)!=rec["saidas"]:
            raise ValueError(f"Produtos alterados: {rp.parent}")
        recibos.append((str(rp.parent.relative_to(v)),len(rec["saidas"]),rec["id"],sha256_arquivo(rp)))
    salvar(destino/"recibos.csv",["lote","arquivos_do_recibo","id","sha256_recibo"],sorted(recibos))
    ages={r["codigo"]:int(r["faixa"]) for r in ler(catalogo)}
    audit=[]
    for arq in sorted((v/"estratos").glob("*/idade_sexo.csv")):
        total,delta,ignorados=0,0,0
        for r in ler(arq):
            old=-1 if r["faixa"]=="IGNORADA" else int(r["faixa"])
            atual=ages.get(r["idade_bruta"],-1)
            n=int(r["obitos"])
            delta+=n*(old!=atual)
            total+=n
            ignorados+=n*(atual==-1)
        audit.append((arq.parent.name,total,delta,ignorados))
    salvar(destino/"idade_versus_tabdo.csv",["ano","G0","faixa_divergente","idade_ignorada"],audit)
    if any(r[2] for r in audit):
        raise ValueError("Faixas do TCC e TABDO divergentes")
    resumo=dict(arquivos_originais=len(linhas),por_familia=dict(Counter(r[0] for r in linhas)),recibos=len(recibos),
                sha256_origem=sha256_arquivo(destino/"originais.csv"),sha256_recibos=sha256_arquivo(destino/"recibos.csv"),
                livre_bytes=shutil.disk_usage(v).free)
    escrever_json(destino/"verificacao.json",resumo)
    return resumo


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for k in ("v","catalogo_idade","destino"):
        p.add_argument(k,type=Path)
    a=p.parse_args()
    print(auditar(a.v,a.catalogo_idade,a.destino))
