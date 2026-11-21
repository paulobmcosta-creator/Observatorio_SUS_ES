"""Executar regressões empíricas offline e a falha de margem em cópia descartável."""
import argparse
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from observatorio_sus.estudos.camila import assistencia, populacao, popsvs, sigtap
from observatorio_sus.io.custodia import escrever_json, sha256_arquivo


def prova(acervo,destino):
    if destino.resolve().is_relative_to(Path(__file__).resolve().parents[1]):
        raise ValueError("Use um diretório de evidências externo")
    destino.mkdir(parents=True,exist_ok=False)
    recibos={}
    for nome,metodo in (("popsvs",popsvs),("taxas",populacao),("assistencia",assistencia),("sigtap",sigtap)):
        saida=destino/nome
        r=metodo.processar(acervo,saida)
        if r!=metodo.processar(acervo,saida):
            raise ValueError(f"Falha de idempotência: {nome}")
        recibos[nome]=r["id"]
    comparacoes=[]
    for nome,cp in (("taxas","CP03"),("assistencia","CP02")):
        for p in sorted((destino/nome).glob("*.csv")):
            original=acervo/cp/"Resultados"/p.name
            if original.exists():
                obtido=sha256_arquivo(p)
                if obtido!=sha256_arquivo(original):
                    raise ValueError(p.name)
                comparacoes.append(dict(arquivo=p.name,baseline=cp,sha256=obtido))
    for p in sorted((destino/"popsvs").glob("*.csv")):
        if sha256_arquivo(p)!=sha256_arquivo(acervo/"CP03/Resultados/POPSVS_7_ANOS"/p.name):
            raise ValueError("Regressão a partir dos originais POPSVS")
        comparacoes.append(dict(arquivo=p.name,baseline="CP03/POPSVS_7_ANOS",sha256=sha256_arquivo(p)))
    if len(comparacoes)!=15:
        raise ValueError("Faltam controles de regressão")
    pos=destino/"taxas"/"recibo.json"
    anterior=sha256_arquivo(pos)
    original=acervo/"CP03/Resultados/RIPSA_DEM101_REGISTROS_ES.csv"
    with TemporaryDirectory(dir=destino) as tmp:
        copia=Path(tmp)/original.name
        alteracoes=0
        with original.open(newline="") as entrada,copia.open("x",newline="") as saida:
            r=csv.DictReader(entrada)
            w=csv.DictWriter(saida,r.fieldnames)
            w.writeheader()
            for linha in r:
                if (linha["co_anomes"],linha["co_ibge"],linha["sg_categoria"])==("201412","320010","TC"):
                    linha["vl_indicador_calculado_mun"]=str(float(linha["vl_indicador_calculado_mun"])+1)
                    alteracoes+=1
                w.writerow(linha)
        if alteracoes!=1:
            raise ValueError("Mutação de margem incompatível com a edição")
        comando=[sys.executable,"-m","observatorio_sus.estudos.camila.populacao",str(acervo)]
        for alvo in ("invalido","taxas"):
            r=subprocess.run([*comando,str(destino/alvo),"--dem",str(copia)],capture_output=True,text=True)
            (destino/("negativo_"+alvo+".log")).write_text(r.stderr)
            if r.returncode==0 or (alvo=="invalido" and "divergência entre total municipal" not in r.stderr):
                raise ValueError("Falso sucesso ou falha diferente da esperada")
        negativo=dict(sha256_copia=sha256_arquivo(copia),linhas_adulteradas=alteracoes,
                      codigo_saida=r.returncode,sha256_dem=sha256_arquivo(original))
    if (destino/"invalido").exists() or sha256_arquivo(pos)!=anterior:
        raise ValueError("Falha de isolamento")
    for p in destino.glob(".pendente-*"):
        if list(p.glob("MORTALIDADE*")) or not (p/"FALHA.json").exists():
            raise ValueError("Falha na segregação do lote")
    resumo=dict(recibos=recibos,comparacoes=comparacoes,negativo=negativo)
    escrever_json(destino/"regressoes.json",resumo)
    print(json.dumps(resumo,ensure_ascii=False))


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("acervo",type=Path)
    p.add_argument("destino",type=Path)
    a=p.parse_args()
    prova(a.acervo.resolve(),a.destino.resolve())
