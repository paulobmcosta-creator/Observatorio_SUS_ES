"""Contraprova independente SQL dos estimandos R em fixture explicitamente sintética."""
import csv
import os
from pathlib import Path
import shutil
import subprocess

import duckdb
import pytest


def test_s03_s04_r_sql_independente(tmp_path):
    rscript = shutil.which("Rscript") or os.environ.get("OBS_RSCRIPT")
    if not rscript:
        pytest.skip("Rscript ausente; fornecer OBS_RSCRIPT para a contraprova R/SQL.")
    subprocess.run([rscript, "tests/test_percurso_sih.R", str(tmp_path)], check=True, capture_output=True, text=True, timeout=30)
    con = duckdb.connect()
    con.execute("CREATE TABLE rd AS SELECT * FROM read_csv(?, all_varchar=true)", ["tests/fixtures/sih/rd_sintetico.csv"])
    # Especificação SQL própria, sem consumir classificação ou coorte calculada em R.
    linhas = con.execute("""
        WITH territorio AS (
          SELECT * FROM (VALUES ('320010','A'), ('320016','B')) AS t(codigo,regiao)
        ), elegiveis AS (
          SELECT rd.*, origem.regiao origem, destino.regiao destino
          FROM rd JOIN territorio origem ON rd.MUNIC_RES=origem.codigo
          LEFT JOIN territorio destino ON rd.MUNIC_MOV=destino.codigo
          WHERE IDENT='1' AND ANO_CMPT='2024' AND MES_CMPT='01'
        )
        SELECT origem,
          count(*) total,
          count(*) FILTER (WHERE destino IS NOT NULL AND destino!=origem OR MUNIC_MOV='330010') numerador,
          count(*) FILTER (WHERE destino IS NOT NULL OR MUNIC_MOV='330010') denominador,
          count(*) FILTER (WHERE destino IS NULL AND MUNIC_MOV!='330010') ignorado
        FROM elegiveis GROUP BY origem ORDER BY origem
    """).fetchall()
    with (tmp_path / "s04_sintetico.csv").open() as f:
        r = list(csv.DictReader(f))
    assert linhas == [(x["regiao_residencia"], int(x["total_elegivel"]), int(x["numerador"]),
                       int(x["denominador"]), int(x["destino_ignorado"])) for x in r]
    with (tmp_path / "s03_sintetico.csv").open() as f:
        s03 = list(csv.DictReader(f))
    assert sum(x[1] for x in linhas) == int(s03[0]["registros_elegiveis"]) == 5
    assert float(r[0]["percentual_fora"]) == pytest.approx(200 / 3, abs=1e-10)
    assert r[1]["percentual_fora"] == "NA"
