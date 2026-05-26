from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "python" / "observatorio_sus" / "extract" / "inventariar_grupos_cnes_pysus.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["python", str(SCRIPT), *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False)


def test_arquivo_existe() -> None:
    assert SCRIPT.exists()


def test_help_retorna_0() -> None:
    proc = run_cli("--help")
    assert proc.returncode == 0


def test_planejamento_json_e_defaults_sem_escrita_data_dirs() -> None:
    data_dirs = [REPO_ROOT / "data_raw", REPO_ROOT / "data_interim", REPO_ROOT / "data_processed"]
    before = {d: sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file()) for d in data_dirs if d.exists()}

    proc = run_cli("--modo", "planejamento")
    assert proc.returncode == 0
    payload = json.loads(proc.stdout)

    assert payload["grupos_candidatos_iniciais"]["grupos"] == ["ST", "LT", "SR"]
    assert "não" in payload["grupos_candidatos_iniciais"]["observacao"].lower() or "nao" in payload["grupos_candidatos_iniciais"]["observacao"].lower()
    assert payload["retry"]["tentativas"] == 3
    assert "isolamento" in payload
    assert payload["parametros"]["uf"] == "ES"
    assert payload["parametros"]["ano"] == 2024
    assert payload["parametros"]["mes"] == 1

    after = {d: sorted(str(p.relative_to(d)) for p in d.rglob("*") if p.is_file()) for d in data_dirs if d.exists()}
    assert before == after
