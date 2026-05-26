import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("python/observatorio_sus/extract/mapear_multicompetencia_cnes_pysus.py")


def run_cmd(*args: str):
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def test_arquivo_existe():
    assert SCRIPT.exists()


def test_help_retorna_zero():
    proc = run_cmd("--help")
    assert proc.returncode == 0
    assert "--modo" in proc.stdout


def test_planejamento_json_e_defaults_sem_escrita_data_dirs():
    before = {d: set(Path(d).glob("**/*")) if Path(d).exists() else set() for d in ["data_raw", "data_interim", "data_processed"]}
    proc = run_cmd("--modo", "planejamento")
    after = {d: set(Path(d).glob("**/*")) if Path(d).exists() else set() for d in ["data_raw", "data_interim", "data_processed"]}

    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["parametros"]["grupos"] == ["ST", "LT", "SR"]
    assert payload["parametros"]["meses"] == [1, 6, 12]
    assert payload["retry"]["tentativas"] == 5
    assert payload["retry"]["base_backoff"] == 2.0
    assert payload["retry"]["jitter_max"] == 1.0
    assert "isolamento" in payload
    assert "usa_api_publica_pysus" in payload
    assert "contratos_cnes" in payload
    assert "matriz_estabilidade_colunas" in payload
    assert "matriz_estabilidade_dtypes" in payload
    assert "diferencas_estruturais" in payload
    assert "riscos_coercao_codigos" in payload
    assert before == after
