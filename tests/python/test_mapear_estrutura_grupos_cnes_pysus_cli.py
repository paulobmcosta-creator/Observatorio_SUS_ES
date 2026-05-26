from __future__ import annotations

import json
import subprocess
from pathlib import Path

SCRIPT = Path("python/observatorio_sus/extract/mapear_estrutura_grupos_cnes_pysus.py")


def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["python", *args], check=False, capture_output=True, text=True)


def test_arquivo_existe() -> None:
    assert SCRIPT.exists()


def test_help_retorna_zero() -> None:
    proc = run_cmd(str(SCRIPT), "--help")
    assert proc.returncode == 0


def test_planejamento_json_defaults() -> None:
    proc = run_cmd(str(SCRIPT), "--modo", "planejamento")
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["parametros"]["grupos"] == ["ST", "LT", "SR"]
    assert payload["retry"]["tentativas"] == 5
    assert payload["retry"]["base_backoff"] == 2.0
    assert payload["retry"]["jitter_max"] == 1.0
    assert "isolamento" in payload
    assert "matriz_colunas_por_grupo" in payload
    assert "matriz_campos_chave" in payload
    assert "matriz_contratos" in payload
    assert "riscos_coercao_codigos" in payload
    assert "recomendacoes_padronizacao" in payload
    assert payload["usa_api_publica_pysus"]["ativo"] is True
    assert "from pysus import cnes" in payload["usa_api_publica_pysus"]["caminho_funcional"]
    assert payload["usa_api_publica_pysus"]["importa_pysus_no_planejamento"] is False


def test_planejamento_nao_escreve_data_dirs() -> None:
    before = {p: sorted(Path(p).glob("**/*")) for p in ["data_raw", "data_interim", "data_processed"] if Path(p).exists()}
    proc = run_cmd(str(SCRIPT), "--modo", "planejamento")
    assert proc.returncode == 0
    after = {p: sorted(Path(p).glob("**/*")) for p in before}
    assert before == after
