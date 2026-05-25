import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("python/observatorio_sus/extract/investigar_fallback_cnes.py")


def test_script_existe():
    assert SCRIPT.exists()


def test_help_exit_zero():
    proc = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "--modo" in proc.stdout


def test_planejamento_exit_zero_json_parseavel():
    proc = subprocess.run([sys.executable, str(SCRIPT), "--uf", "ES", "--ano", "2025", "--modo", "planejamento"], capture_output=True, text=True)
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["parametros"]["modo"] == "planejamento"
    assert payload["competencias"] == [f"2025{m:02d}" for m in range(1, 13)]
    assert "tbEstabelecimento" in payload["tabelas_investigadas"]
    assert "tbMunicipio" in payload["tabelas_investigadas"]
    assert "rlEstabSipac" in payload["tabelas_investigadas"]
    assert "tbSubGruposHabilitacao" in payload["tabelas_investigadas"]


def test_planejamento_nao_escreve_diretorios_dados():
    for nome in ["data_raw", "data_interim", "data_processed"]:
        base = Path(nome)
        before = sorted(p.relative_to(base) for p in base.rglob("*") if p.is_file())
        proc = subprocess.run([sys.executable, str(SCRIPT), "--modo", "planejamento"], capture_output=True, text=True)
        assert proc.returncode == 0
        after = sorted(p.relative_to(base) for p in base.rglob("*") if p.is_file())
        assert before == after
