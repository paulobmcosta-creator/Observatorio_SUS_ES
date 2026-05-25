import json
import subprocess
from pathlib import Path


def test_script_existe():
    assert Path("python/observatorio_sus/extract/descobrir_arquivos_cnes.py").exists()


def test_help_exit_zero():
    resultado = subprocess.run(
        ["python", "python/observatorio_sus/extract/descobrir_arquivos_cnes.py", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert resultado.returncode == 0


def test_planejamento_json_offline_sem_data_dirs_mutadas():
    dirs = [Path("data_raw"), Path("data_interim"), Path("data_processed")]
    before = {
        d: (d.exists(), d.stat().st_mtime_ns if d.exists() else None)
        for d in dirs
    }

    resultado = subprocess.run(
        [
            "python",
            "python/observatorio_sus/extract/descobrir_arquivos_cnes.py",
            "--competencia",
            "202501",
            "--modo",
            "planejamento",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert resultado.returncode == 0
    payload = json.loads(resultado.stdout)
    assert payload["competencia"] == "202501"
    assert payload["tabelas_prioritarias"] == [
        "tbEstabelecimento",
        "tbMunicipio",
        "rlEstabSipac",
        "tbSubGruposHabilitacao",
    ]
    assert "risco_download" in payload
    assert "proxima_recomendacao" in payload
    assert "sem rede" in payload["conclusao"].lower()

    after = {
        d: (d.exists(), d.stat().st_mtime_ns if d.exists() else None)
        for d in dirs
    }
    assert before == after
