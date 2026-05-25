from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "python" / "observatorio_sus" / "extract" / "reconhecer_api_cnes_pysus.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python", str(SCRIPT), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_arquivo_existe() -> None:
    assert SCRIPT.exists()


def test_help_retorna_0() -> None:
    proc = _run("--help")
    assert proc.returncode == 0


def test_planejamento_retorna_json_parseavel_e_sem_escrita_em_data_dirs() -> None:
    data_dirs = [REPO_ROOT / "data_raw", REPO_ROOT / "data_interim", REPO_ROOT / "data_processed"]
    snapshots_antes = {d: sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file()) for d in data_dirs if d.exists()}

    proc = _run("--modo", "planejamento")
    assert proc.returncode == 0

    payload = json.loads(proc.stdout)
    assert payload["grupos_planejados"] == ["ST", "LT", "SR"]
    assert payload["parametros"]["modo"] == "planejamento"
    assert payload["parametros"]["uf"] == "ES"
    assert payload["parametros"]["ano"] == 2024
    assert payload["parametros"]["mes"] == 1
    assert payload["parametros"]["grupo"] == "ST"

    snapshots_depois = {d: sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file()) for d in data_dirs if d.exists()}
    assert snapshots_antes == snapshots_depois
