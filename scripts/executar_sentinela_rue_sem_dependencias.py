"""Contraprova sentinela RUE com biblioteca padrão; não calcula outras dimensões.

O pacote restaurável inclui entradas históricas autorizadas fora de Git. Esta
rotina pode ser executada pelo operador sem IA/rede depois do preparo do pacote.
"""
import csv
import json
from pathlib import Path
import sys


def calcular(estabelecimentos, referencia):
    """Ler campos históricos textuais e contar distintos por município legado."""
    with Path(referencia).open(encoding="utf-8-sig", newline="") as f:
        refs = list(csv.DictReader(f))
    grupos = {r["cod_municipio"]: set() for r in refs}
    if len(grupos) != len(refs) or len(grupos) != 78:
        raise ValueError("Referência exige 78 códigos municipais únicos.")
    observados = set()
    with Path(estabelecimentos).open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            codigo = r["cod_municipio"].strip()
            if r["competencia"] != "202601" or codigo not in grupos or not r["cnes"].strip():
                raise ValueError("Contrato histórico divergente.")
            observados.add(codigo)
            if r["atende_sus"].strip() == "Sim" and "URGENCIA" in [v.strip() for v in r["atendimento_prestado"].split("|")]:
                grupos[codigo].add(r["cnes"].strip())
    if observados != set(grupos):
        raise ValueError("Universo municipal divergente.")
    divergencias = sum(len(grupos[r["cod_municipio"]]) != int(r["n_estab_urgencia_sus"]) for r in refs)
    resultado = {"celulas": 78, "divergencias": divergencias, "dimensoes_verificadas": 1,
                 "escopo": "RUE_historica_202601_papel_municipal_legado"}
    if divergencias:
        raise ValueError("Sentinela divergiu da referência histórica.")
    return resultado


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("Uso: script estabelecimentos.csv referencia.csv resultado_novo.json")
    resultado = calcular(sys.argv[1], sys.argv[2])
    with Path(sys.argv[3]).open("x", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")
    print("Sentinela RUE: 78/78; uma dimensão histórica, sem homologação institucional.")
