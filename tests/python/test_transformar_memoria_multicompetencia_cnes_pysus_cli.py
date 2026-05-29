from __future__ import annotations
import json
import subprocess
from pathlib import Path

SCRIPT = Path("python/observatorio_sus/transform/transformar_memoria_multicompetencia_cnes_pysus.py")

def run_cmd(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["python", str(SCRIPT), *args], capture_output=True, text=True, check=False)

def test_arquivo_existe() -> None:
    assert SCRIPT.is_file()

def test_help_retorna_0() -> None:
    cp = run_cmd("--help")
    assert cp.returncode == 0
    assert "diagnostico_sem_subprocesso" in cp.stdout
    assert "diagnostico_st_fases" in cp.stdout
    assert "--usar-subprocesso" in cp.stdout
    assert "--sem-transformacao" in cp.stdout
    assert "--sem-dtypes" in cp.stdout
    assert "--sem-metadados-detalhados" in cp.stdout
    assert "--payload-resumido" in cp.stdout

def test_planejamento_json_e_campos() -> None:
    cp = run_cmd("--modo", "planejamento")
    assert cp.returncode == 0
    payload = json.loads(cp.stdout)
    assert payload["parametros"]["grupos"] == ["ST", "LT", "SR"]
    assert payload["parametros"]["meses"] == [1, 6, 12]
    assert payload["retry"]["tentativas"] == 5
    assert payload["parametros"]["timeout_por_chamada"] == 300.0
    assert payload["parametros"]["timeout_global"] == 1800.0
    assert payload["retry"]["timeout_por_chamada"] == 300.0
    assert payload["retry"]["timeout_global"] == 1800.0
    assert payload["timeout_controlado_ativo"] is True
    assert payload["classificacao_timeout"] == "TIMEOUT_CONTROLADO"
    assert payload["caminho_padrao_transformacao"] == "direto_sem_subprocesso"
    assert payload["subprocesso_padrao"] is False
    assert payload["subprocesso_disponivel"] is True
    assert "timeout causado por subprocesso" in payload["justificativa_caminho_padrao"]
    assert "travamento indefinido" in payload["justificativa_timeout"]
    assert "usa_api_publica_pysus" in payload
    assert "contrato_intermediario" in payload
    assert "regras_transformacao" in payload
    assert "matriz_transformacao" in payload
    assert "matriz_preservacao_textual" in payload
    assert "matriz_tipos_antes_depois" in payload
    proib = " ".join(payload["regras_transformacao"]["proibicoes"]).lower()
    assert "co_unidade" in proib
    assert "criar co_unidade" in proib
    assert "persistir" in proib
    assert payload["isolamento"]["aplicado"] is False


def test_modo_diagnostico_sem_subprocesso_eh_aceito_no_planejamento_de_args() -> None:
    cp = run_cmd("--modo", "diagnostico_sem_subprocesso", "--help")
    assert cp.returncode == 0
    assert "diagnostico_sem_subprocesso" in cp.stdout


def test_modo_diagnostico_st_fases_e_flags_sao_aceitos_no_help() -> None:
    cp = run_cmd("--modo", "diagnostico_st_fases", "--help")
    assert cp.returncode == 0
    assert "diagnostico_st_fases" in cp.stdout
    assert "--sem-transformacao" in cp.stdout
    assert "--sem-dtypes" in cp.stdout
    assert "--sem-metadados-detalhados" in cp.stdout
    assert "--payload-resumido" in cp.stdout
