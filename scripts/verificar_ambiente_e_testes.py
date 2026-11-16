"""Executar verificações registrando comando, versão, saída e exit code reais.

Não usa rede nem instala dependências. Execute com o Python do ambiente pinado.
"""
import argparse
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import os


def executar(destino, comandos):
    """Salvar logs delimitados por comando; falhas nunca são omitidas do balanço."""
    destino.mkdir(parents=True, exist_ok=False)
    registros = []
    env = {**os.environ, "PYTHONPATH": str(Path("python").resolve())}
    for id, cmd in comandos:
        inicio = time.monotonic()
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, timeout=180)
        (destino / (id + ".txt")).write_text(proc.stdout)
        registros.append(dict(id=id, comando=cmd, exit_code=proc.returncode,
                              segundos=time.monotonic() - inicio, log=id + ".txt"))
        print(id, proc.returncode, flush=True)
    pacotes = {}
    for p in ["pytest", "pyarrow", "duckdb", "pysus", "pandas", "dbfread"]:
        try:
            pacotes[p] = version(p)
        except PackageNotFoundError:
            pacotes[p] = "AUSENTE"
    resultado = dict(utc=datetime.now(timezone.utc).isoformat(), python=sys.version, plataforma=platform.platform(),
                     pacotes=pacotes, testes=registros, resultado="APROVADO" if all(r["exit_code"] == 0 for r in registros) else "FALHOU")
    (destino / "execucao.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n")
    return resultado


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destino", type=Path)
    parser.add_argument("--rscript", default=shutil.which("Rscript"))
    parser.add_argument("--integracao", action="store_true")
    args = parser.parse_args()
    python = [sys.executable, "-m", "pytest", "tests/python", "-q"] if args.integracao else [
        sys.executable, "-m", "pytest", "tests/python/test_custodia.py", "tests/python/test_qualidade_partes_csv.py",
        "tests/python/test_converter_csv_parquet.py", "-q"]
    comandos = [("python_integracao" if args.integracao else "python_direcionado", python)]
    if args.rscript:
        arquivos = ["tests/test_proveniencia_temporal_cnes.R", "tests/test_cache_cnes.R", "tests/test_preparadores_sem_descarte.R", "tests/test_dimensao_rue.R"]
        if args.integracao:
            # Workflow já existente define o conjunto abrangente; sem reaquisição.
            import re
            workflow = Path(".github/workflows/validar_pipeline_cnes_r.yml").read_text()
            arquivos = re.findall(r"Rscript (tests/\S+\.R)", workflow)
            arquivos += ["tests/test_dimensao_rue.R", "tests/test_percurso_sih.R"]
            arquivos += ["tests/test_revisao_a02_a04_sih.R", "tests/test_revisao_a08_cnes.R"]
            arquivos = list(dict.fromkeys(arquivos))
        comandos += [(Path(f).stem, [args.rscript, f]) for f in arquivos]
    resultado = executar(args.destino, comandos)
    raise SystemExit(0 if resultado["resultado"] == "APROVADO" else 1)
