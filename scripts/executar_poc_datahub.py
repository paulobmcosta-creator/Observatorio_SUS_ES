"""Avaliação local do código original DataHub Brasil, sem aquisição ou publicação.

Python é necessário para executar as funções Python do candidato (D1 §4.2–4.3).
Execute da raiz do Observatório, com os extras em PYTHONPATH isolado. Os insumos
e o checkout original são somente leitura; saídas exigem diretórios novos.
Os casos sintéticos demonstram limites, não equivalência de arquivos oficiais.
"""
import argparse
import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from unittest.mock import patch

PIN = "60aa9cbd82509e0595d5c99ec74794e6be1588bd"
REF_HASH = "24b6eda70bbbf502fea9e987ac15be4a7b521dfaacc96e93c670066766ca7c7a"


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def sql_string(value):
    return "'" + str(value).replace("'", "''") + "'"


def executar(repo, saida, evidencia, referencia):
    inicio = datetime.now(timezone.utc).isoformat()
    repo = repo.resolve()
    saida = saida.resolve()
    if git(repo, "rev-parse", "HEAD") != PIN or git(repo, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("Exige checkout original limpo no commit documentado.")
    if (repo / ".env").exists():
        raise ValueError("Use checkout de inspeção sem .env/credenciais.")
    if sha256(referencia) != REF_HASH:
        raise ValueError("Referência R diverge da reconciliação preservada.")
    saida.mkdir(parents=True, exist_ok=False)
    evidencia.mkdir(parents=True, exist_ok=False)
    fixture = Path("tests/fixtures/ferramentas/microdatasus_sintetico.dbc")
    anterior = Path("metadata/ciclo_2026_2027/avaliacao_ferramentas/poc_20261022_v2/dbc_sintetico.json")
    insumos = {str(p): sha256(p) for p in [referencia, fixture, anterior, Path(__file__)]}
    fontes = {p: sha256(repo / p) for p in git(repo, "ls-files").splitlines() if (repo / p).is_file()}
    os.environ.update(DATAHUB_STORAGE="local", SOCKS5_PROXY_ENABLED="false",
                      KAGGLE_DATAHUB_LANDING_DIR=str(saida / "landing"),
                      KAGGLE_DATAHUB_PUBLISH_CACHE_DIR=str(saida / "publish"))
    sys.path.insert(0, str(repo))
    import datasus_dbc
    import duckdb
    import pandas as pd
    import pyarrow.parquet as pq
    from scripts.extract.datasus.base_ftp import _verificar_em_lote
    from scripts.extract.datasus.base_sia import criar_regra
    from scripts.process.dados_abertos.base_process_abertos import query_para_parquet
    from scripts.process.datasus.base_process_dbc import _iter_chunks_dbf, _iter_chunks_dbfread
    from scripts.process.datasus import base_process_pa as pa

    resultados = {}
    # 1. A mesma fixture DBC sintética já examinada via PySUS.
    dbf = saida / "microdatasus_sintetico.dbf"
    datasus_dbc.decompress(str(fixture), str(dbf))
    leitores = {}
    for nome, leitor in [("principal", lambda: _iter_chunks_dbf(str(dbf), fixture.name, 10)),
                         ("fallback_dbfread", lambda: _iter_chunks_dbfread(str(dbf), 10))]:
        try:
            df = pd.concat(list(leitor()), ignore_index=True)
            leitores[nome] = {"resultado": "converteu", "linhas": len(df),
                             "valores": {c: [None if pd.isna(v) else str(v) for v in df[c]] for c in df}}
        except Exception as erro:
            leitores[nome] = {"resultado": "falhou", "erro": f"{type(erro).__name__}: {erro}"}
    lexico = json.loads(anterior.read_text())["esperado_lexico_dbf"]
    for leitor in leitores.values():
        leitor["igual_lexico_raw_pysus"] = leitor.get("valores") == lexico
        leitor["preserva_CODE"] = leitor.get("valores", {}).get("CODE") == ["001", "010"]
    resultados["dbc_sintetico"] = {"sintetico": True, "dbf_sha256": sha256(dbf), "leitores": leitores,
        "referencia_lexica_pysus": lexico, "referencia_teste_r": "CODE=001/010; VALUE=1.5/NA; WHEN=2020-01-02/NA",
        "limite": "Teste original microdatasus consultado; pacote R não executado. Não é DBC oficial."}

    # 2. Filtro de aquisição versus parser de competência, sem qualquer FTP.
    regra = criar_regra("PA")
    nomes = ["PAES2401.dbc", "PASP2401a.dbc", "PASP2401b.dbc"]
    resultados["pa_nomes"] = {n: {"aceito_fetch": regra(n), "competencia_process": pa._competencia_de(n)} for n in nomes}

    # 3. Test double do transporte: conteúdo diferente com mesmo tamanho.
    class FTPFalso:
        def size(self, nome):
            return 4
    resultados["manifesto_tamanho"] = {"sintetico": True, "hash_antes": hashlib.sha256(b"AAAA").hexdigest(),
        "hash_depois": hashlib.sha256(b"BBBB").hexdigest(), "tamanho_ambos": 4,
        "downloads_selecionados": _verificar_em_lote(FTPFalso(), ["PAES2401.dbc"], {"PAES2401.DBC": 4})}

    # 4. Função original de consolidação PA; leitor/decompressor substituídos
    # por doubles para isolar mudança de schema, não simular download/conversão.
    def leitor_falso(caminho, chunksize):
        if Path(caminho).name == "PAES2401.dbf":
            yield pd.DataFrame({"CNES": ["0012345"], "VALOR": ["1"]})
        else:
            yield pd.DataFrame({"CNES": ["0023456"], "VALOR": ["2"], "CAMPO_NOVO": ["preservar"]})
    with patch.object(pa.datasus_dbc, "decompress", return_value=None), patch.object(pa, "_ler_dbf_pa", leitor_falso):
        produto = pa._converter_competencia(saida, "202401", ["PAES2401.dbc", "PASP2401.dbc"], saida)
    tabela = pq.read_table(produto)
    resultados["pa_schema"] = {"sintetico": True, "leitor_e_descompressor": "doubles sem rede",
        "linhas": tabela.num_rows, "campos_saida": tabela.column_names,
        "campo_novo_preservado": "CAMPO_NOVO" in tabela.column_names,
        "origens": tabela.column("_ARQUIVO_ORIGEM").to_pylist()}

    # 5. Referência real R: mesma função SQL genérica, UTF-8/vírgula porque
    # este insumo é derivado R. Não executa o main CNES/Latin-1 nem publica.
    with referencia.open(newline="", encoding="utf-8") as stream:
        linhas = list(csv.reader(stream))
    cabecalho, dados = linhas[0], linhas[1:]
    destino = saida / "referencia_r.parquet"
    query = f"SELECT * FROM read_csv({sql_string(referencia.resolve())}, delim=',', header=true, encoding='utf-8', all_varchar=true, ignore_errors=true)"
    with duckdb.connect(":memory:") as con:
        con.execute("SET preserve_insertion_order=true")
        con.execute("SET threads=1")
        query_para_parquet(query, destino, con)
    tabela = pq.read_table(destino)
    convertido = list(zip(*(col.to_pylist() for col in tabela.columns)))
    mesmo_shape = tabela.column_names == cabecalho and len(convertido) == len(dados)
    diferentes = sum(a != b for ra, rb in zip(dados, convertido) for a, b in zip(ra, rb)) if mesmo_shape else None
    normalizados = sum(a == "" and b is None for ra, rb in zip(dados, convertido) for a, b in zip(ra, rb)) if mesmo_shape else None
    chaves = ["co_unidade", "cnes", "cod_municipio", "competencia"]
    resultados["referencia_r"] = {"fonte": str(referencia), "sha256": REF_HASH, "query": query,
        "linhas_entrada": len(dados), "linhas_saida": tabela.num_rows, "colunas": tabela.num_columns,
        "schema_ordem_linhas_dimensoes_iguais": mesmo_shape, "celulas_diferentes": diferentes,
        "vazios_para_null": normalizados,
        "chaves_identicas": {c: [r[cabecalho.index(c)] for r in dados] == tabela.column(c).to_pylist() for c in chaves},
        "limite": "Compara derivado R existente; não executa preparadores nem demonstra equivalência metodológica de dados Kaggle."}

    # 6. Linha de CSV malformada: ignore_errors é configuração do candidato.
    malformado = saida / "sintetico_malformado.csv"
    malformado.write_text("CNES;VALOR\n" + "0012345;1\n" * 30 + "0023456;2;extra\n", encoding="utf-8")
    consulta = f"SELECT * FROM read_csv({sql_string(malformado)}, delim=';', header=true, columns={{'CNES':'VARCHAR','VALOR':'VARCHAR'}}, ignore_errors=true)"
    with duckdb.connect(":memory:") as con:
        query_para_parquet(consulta, saida / "malformado.parquet", con)
        try:
            con.execute(consulta.replace("ignore_errors=true", "ignore_errors=false")).fetchall()
            estrito = "aceitou"
        except duckdb.Error:
            estrito = "rejeitou"
    resultados["csv_malformado"] = {"sintetico": True, "schema_explicito_para_isolar_ignore_errors": True,
        "linhas_entrada": 31, "linhas_saida": pq.read_table(saida / "malformado.parquet").num_rows,
        "modo_estrito": estrito, "query": consulta}
    if insumos != {p: sha256(Path(p)) for p in insumos} or fontes != {p: sha256(repo / p) for p in fontes}:
        raise ValueError("Insumos ou fontes modificados durante avaliação.")
    execucao = {"inicio_utc": inicio, "fim_utc": datetime.now(timezone.utc).isoformat(), "argv": sys.argv,
        "commit_datahub": PIN, "python": platform.python_version(),
        "versoes": {p: version(p) for p in ["datasus-dbc", "simpledbf", "pandas", "pyarrow", "duckdb", "dbfread", "numpy", "boto3"]},
        "aquisicao": "não executada; somente insumos locais", "publicacao": "não executada",
        "integridade": "ver resultados por caso; converter não basta para preservar células e schema",
        "equivalencia_metodologica": "não demonstrada para produtos oficiais/Kaggle; referências R preservadas",
        "fontes_e_insumos_inalterados": True}
    for nome, valor in [("resultados", resultados), ("execucao", execucao), ("insumos_sha256", insumos), ("checkout_sha256", fontes)]:
        (evidencia / f"{nome}.json").write_text(json.dumps(valor, ensure_ascii=False, indent=2) + "\n")
    produtos = {str(p): sha256(p) for p in saida.rglob("*") if p.is_file()}
    (evidencia / "produtos_sha256.json").write_text(json.dumps(produtos, indent=2) + "\n")
    print(json.dumps({"evidencias": str(evidencia), "casos_executados": len(resultados), "fontes_e_insumos_inalterados": True}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument("saida", type=Path)
    parser.add_argument("evidencia", type=Path)
    parser.add_argument("--referencia", type=Path, default=Path(".cache/cnes/execucoes/reconciliacao_dossies_20261022/estabelecimentos/cnes_estabelecimentos_es_202601.csv"))
    args = parser.parse_args()
    executar(args.checkout, args.saida, args.evidencia, args.referencia)
