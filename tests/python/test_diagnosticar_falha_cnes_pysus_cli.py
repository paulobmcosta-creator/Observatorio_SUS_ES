from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "python" / "observatorio_sus" / "extract" / "diagnosticar_falha_cnes_pysus.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["python", str(SCRIPT), *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False)


def test_arquivo_existe() -> None:
    assert SCRIPT.exists()


def test_help_retorna_0() -> None:
    proc = run_cli("--help")
    assert proc.returncode == 0


def test_planejamento_json_causas_e_sem_escrita_data_dirs() -> None:
    data_dirs = [REPO_ROOT / "data_raw", REPO_ROOT / "data_interim", REPO_ROOT / "data_processed"]
    before = {d: sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file()) for d in data_dirs if d.exists()}

    proc = run_cli("--modo", "planejamento")
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)

    assert isinstance(payload["causas_possiveis"], list)
    assert "CHAMADA_FUNCIONOU" in payload["causas_possiveis"]
    assert "ERRO_DE_REDE" in payload["causas_possiveis"]
    assert payload["parametros"]["grupo"] == "ST"
    assert payload["diagnostico"]["tentativas_maximas"] == 3

    after = {d: sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file()) for d in data_dirs if d.exists()}
    assert before == after
