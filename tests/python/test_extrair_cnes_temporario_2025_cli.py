import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path("python/observatorio_sus/extract/extrair_cnes_temporario_2025.py")


def test_script_existe():
    assert SCRIPT.exists()


def test_help_exit_zero():
    proc = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "--modo" in proc.stdout


def test_planejamento_exit_zero_json_parseavel_sem_rede():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--uf", "ES", "--ano", "2025", "--modo", "planejamento"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)
    assert payload["parametros"]["modo"] == "planejamento"
    assert payload["competencias"] == [f"2025{m:02d}" for m in range(1, 13)]


def test_planejamento_nao_cria_diretorios_dados():
    for nome in ["data_raw", "data_interim", "data_processed"]:
        caminho = Path(nome)
        assert caminho.exists()
        antes = sorted(p.relative_to(caminho) for p in caminho.rglob("*") if p.is_file())
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--uf", "ES", "--ano", "2025", "--modo", "planejamento"],
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0
        depois = sorted(p.relative_to(caminho) for p in caminho.rglob("*") if p.is_file())
        assert antes == depois
