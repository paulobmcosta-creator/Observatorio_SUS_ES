"""PoC limitada: CSV nacional CNES 202601, referências R e fixture DBC sintética.

Executar da raiz, com PYTHONPATH=python e extras DBC isolados quando disponíveis.
Não acessa rede, não recalcula indicadores e não modifica as camadas oficiais.
"""
import argparse
import asyncio
import csv
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import duckdb
import pyarrow.parquet as pq

from observatorio_sus.transform.converter_csv_parquet import converter_csv_parquet, sha256


def executar(fonte, saida, evidencia, referencia):
    """Executar PoC em diretórios novos; registrar hashes e resultados agregados."""
    inicio = datetime.now(timezone.utc).isoformat()
    saida.mkdir(parents=True, exist_ok=False)
    evidencia.mkdir(parents=True, exist_ok=False)
    os.environ["PYSUS_CACHEPATH"] = str((saida / "cache_pysus").resolve())
    raw_hash = "a6dd87e847e2905949dd160f1d88ddd5e7f088fdf61b1124404cf566297d36d6"
    refs = {
        "estabelecimentos": ("estabelecimentos/cnes_estabelecimentos_es_202601.csv", "24b6eda70bbbf502fea9e987ac15be4a7b521dfaacc96e93c670066766ca7c7a"),
        "habilitacoes": ("habilitacoes/cnes_habilitacoes_es_202601.csv", "2a02077f69029b08af79994eb7faa0ded6a1cb1ad8badb6705dde0b32f6a9042"),
    }
    insumos = [fonte, *[referencia / v[0] for v in refs.values()],
               *Path("data_raw/cnes/202601").glob("*.csv"),
               *Path("metadata/cnes").glob("*.csv"),
               Path("src/transform/preparar_estabelecimentos_cnes.R"),
               Path("src/transform/preparar_habilitacoes_cnes.R"),
               Path("src/validation/conferir_contrato_snapshot_cnes.R"),
               Path("scripts/conferir_paridade_parquet_r.R"), Path(__file__),
               Path("python/observatorio_sus/transform/converter_csv_parquet.py"),
               Path("tests/fixtures/ferramentas/microdatasus_sintetico.dbc")]
    hashes = {str(p): sha256(p) for p in insumos}
    for nome, (arquivo, esperado) in refs.items():
        if hashes[str(referencia / arquivo)] != esperado:
            raise ValueError(f"Referência {nome} diferente da reconciliação.")
    provenance = dict(sistema="CNES", competencia="2026-01", origem_primaria="nao_documentada_no_acervo_recebido",
                      origem_recuperacao="Git LFS recuperado por hash; manifesto metadata/cnes/fontes/tbEstabelecimento202601.csv",
                      familia="tbEstabelecimento", abrangencia="Brasil", responsavel="Codex sob solicitação do pesquisador")
    manifestos = [converter_csv_parquet(fonte, saida / "raw_parquet", raw_hash, encoding="latin-1", delimitador=";", proveniencia=provenance)]
    # Restituição tabular, sem recuperar/afirmar identidade binária do CSV original.
    restituido = saida / "tbEstabelecimento202601_restituido.csv"
    parquet = pq.ParquetFile(manifestos[0]["arquivo_derivado"])
    with restituido.open("w", encoding="latin-1", newline="") as stream:
        escritor = csv.writer(stream, delimiter=";", lineterminator="\n")
        escritor.writerow(parquet.schema_arrow.names)
        for lote in parquet.iter_batches(batch_size=10000):
            escritor.writerows(zip(*(c.to_pylist() for c in lote.columns)))
    for nome, (arquivo, esperado) in refs.items():
        manifestos.append(converter_csv_parquet(referencia / arquivo, saida / nome, esperado,
            proveniencia={**provenance, "familia": nome, "abrangencia": "ES por município gestor",
                          "origem_recuperacao": "derivado R; execucao reconciliacao_dossies_20261022"}))
    # SQL somente leitura sobre dados textuais já verificados; referência é R.
    with duckdb.connect(":memory:") as con:
        est = con.read_parquet(str(saida / "estabelecimentos/dados.parquet"))
        hab = con.read_parquet(str(saida / "habilitacoes/dados.parquet"))
        medidas = {
            "estabelecimentos": est.aggregate("count(*)").fetchone()[0],
            "chaves_operacionais_distintas": est.aggregate("count(distinct co_unidade)").fetchone()[0],
            "codigos_publicos_zero_inicial": est.filter("starts_with(cnes, '0')").aggregate("count(*)").fetchone()[0],
            "municipios_gestores": est.aggregate("count(distinct cod_municipio)").fetchone()[0],
            "habilitacoes": hab.aggregate("count(*)").fetchone()[0],
            "selecionadas": hab.filter("usar_observatorio = 'Sim'").aggregate("count(*)").fetchone()[0],
            "selecionadas_validado_interno": hab.filter("usar_observatorio = 'Sim' and status_validacao = 'validado'").aggregate("count(*)").fetchone()[0],
            "selecionadas_revisar": hab.filter("usar_observatorio = 'Sim' and status_validacao = 'revisar'").aggregate("count(*)").fetchone()[0],
        }
    esperado = dict(zip(medidas, [12548, 12548, 1297, 78, 1963, 501, 304, 197]))
    if medidas != esperado:
        raise ValueError("Agregações SQL diferentes das referências R.")
    (evidencia / "duckdb.json").write_text(json.dumps({"observado": medidas, "referencia_r": esperado, "iguais": True}, indent=2))
    # A fixture vem dos testes originais microdatasus; não representa dados oficiais.
    from pysus.api.extensions import DBC, Parquet
    fixture = Path("tests/fixtures/ferramentas/microdatasus_sintetico.dbc")
    copia = saida / "sintetico.dbc"
    copia.write_bytes(fixture.read_bytes())
    async def converter_dbc():
        p = await DBC(path=copia).to_parquet(saida / "sintetico.parquet")
        return await p.load(parse=False)
    df = asyncio.run(converter_dbc())
    # Marcadores constam dos bytes DBF da fixture; R interpreta-os como NA.
    # Esta comparação léxica não autoriza normalização geral de ausentes.
    esperado_dbc = {"CODE": ["001", "010"], "VALUE": ["1.500000000000000", "*******************"], "WHEN": ["20200102", "00000000"]}
    observado = df.to_dict(orient="list")
    dbc = {"fixture": str(fixture), "sha256": sha256(fixture), "sintetica": True,
           "referencia": "microdatasus tests/testthat/test-read_dbc.R; CODE 001/010; VALUE 1.5/NA; WHEN 2020-01-02/NA",
           "esperado_lexico_dbf": esperado_dbc, "observado": observado,
           "campos_linhas_lexico_iguais": observado == esperado_dbc,
           "limite": "Não valida conversão de DBC oficial nem séries históricas; tipos e ausentes R/Python distintos."}
    (evidencia / "dbc_sintetico.json").write_text(json.dumps(dbc, ensure_ascii=False, indent=2))
    if observado != esperado_dbc:
        raise ValueError("Fixture DBC diverge da referência léxica esperada.")
    # Contraexemplo: parse padrão altera CODMUNRES; leitura sem parse conserva.
    import pandas as pd
    sentinel = saida / "sentinela.parquet"
    pd.DataFrame({"CODMUNRES": ["012345"], "IDADE": ["001"]}).to_parquet(sentinel)
    async def sentinela():
        p = Parquet(path=sentinel, add_dv=False)
        return (await p.load()).to_dict(orient="list"), (await p.load(parse=False)).to_dict(orient="list")
    padrao, sem_parse = asyncio.run(sentinela())
    (evidencia / "pysus_parse.json").write_text(json.dumps({"sintetico": True, "padrao": padrao, "parse_false": sem_parse}, indent=2))
    cmd = ["Rscript", "scripts/conferir_paridade_parquet_r.R", str(restituido), str(saida / "reexecucao_r"), str(referencia), str(evidencia)]
    with (evidencia / "reexecucao_r.txt").open("w") as log:
        result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=600)
    if result.returncode:
        raise RuntimeError("Reexecução R falhou; consultar log.")
    if hashes != {str(p): sha256(p) for p in insumos}:
        raise ValueError("Insumo modificado durante a PoC.")
    (evidencia / "manifestos_conversao.json").write_text(json.dumps(manifestos, ensure_ascii=False, indent=2))
    (evidencia / "insumos_sha256.json").write_text(json.dumps(hashes, ensure_ascii=False, indent=2))
    (evidencia / "execucao.json").write_text(json.dumps({
        "inicio_utc": inicio, "fim_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "plataforma": platform.platform(),
        "versoes": {p: version(p) for p in ["pysus", "pyreaddbc", "pyarrow", "duckdb", "pandas", "dbfread"]},
        "argv": sys.argv, "comando_r": cmd, "aquisicao_remota": "nao_executada_neste_script",
        "integridade": "CSV/Parquet todas as células e fixture DBC aprovados",
        "paridade": "R após roundtrip do CSV nacional; mesmos preparadores, sem migração analítica",
        "responsavel": "Codex sob solicitação do pesquisador", "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "codigo_efetivo": "insumos_sha256.json; diff local não commitado",
    }, ensure_ascii=False, indent=2))
    produtos = [p for p in saida.rglob("*") if p.is_file() and "cache_pysus" not in p.parts]
    (evidencia / "produtos_sha256.json").write_text(json.dumps({str(p): sha256(p) for p in produtos}, indent=2))
    print(json.dumps({"resultado": "aprovado_no_escopo", "evidencias": str(evidencia), "medidas": medidas}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fonte", type=Path)
    parser.add_argument("saida", type=Path)
    parser.add_argument("evidencia", type=Path)
    parser.add_argument("--referencia", type=Path, default=Path(".cache/cnes/execucoes/reconciliacao_dossies_20261022"))
    args = parser.parse_args()
    executar(args.fonte, args.saida, args.evidencia, args.referencia)
