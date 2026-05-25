import subprocess
import sys
from pathlib import Path


SCRIPT = Path("python/observatorio_sus/extract/validar_extracao_cnes_controlada.py")


def test_script_existe():
    assert SCRIPT.exists()


def test_help_exit_zero():
    proc = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "--modo" in proc.stdout


def test_modo_contratos_exit_zero_sem_rede():
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--modo", "contratos", "--uf", "ES", "--competencia", "202601"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert '"contratos"' in proc.stdout
