import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "python"))

from pathlib import Path

from observatorio_sus.io.manifestos import criar_manifesto_execucao
from observatorio_sus.utils.normalizacao import (
    normalizar_competencia,
    normalizar_nome_coluna,
)


def test_importacoes_locais():
    assert callable(criar_manifesto_execucao)
    assert callable(normalizar_nome_coluna)
    assert callable(normalizar_competencia)


def test_normalizar_nome_coluna():
    assert normalizar_nome_coluna(" CO_UNIDADE ") == "co_unidade"
    assert normalizar_nome_coluna("Município/UF") == "municipio_uf"


def test_normalizar_competencia():
    assert normalizar_competencia("202601") == "2026-01"
    assert normalizar_competencia("2026-01") == "2026-01"


def test_normalizar_competencia_invalida():
    import pytest

    with pytest.raises(ValueError):
        normalizar_competencia("2026/01")


def test_criar_manifesto_execucao():
    manifesto = criar_manifesto_execucao(
        ferramenta="poc_pysus",
        parametros={"uf": "ES", "competencia": "2026-01"},
        observacoes="teste",
    )
    assert manifesto["ferramenta"] == "poc_pysus"
    assert manifesto["parametros"]["uf"] == "ES"
    assert "timestamp_utc" in manifesto


def test_script_avaliacao_existe():
    caminho = Path("python/observatorio_sus/extract/avaliar_pysus_cnes.py")
    assert caminho.exists()
