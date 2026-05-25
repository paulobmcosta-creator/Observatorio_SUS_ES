from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "python"))

import pytest

from observatorio_sus.cnes.contratos import (
    listar_campos_textuais,
    listar_tabelas_obrigatorias,
    obter_contrato_tabela,
    validar_presenca_campos,
)


def test_tabelas_obrigatorias_contem_nucleares():
    tabelas = listar_tabelas_obrigatorias()
    assert "tbEstabelecimento" in tabelas["estabelecimentos"]
    assert "rlEstabSipac" in tabelas["habilitacoes"]


def test_obter_contrato_tabela_conhecida():
    contrato = obter_contrato_tabela("tbEstabelecimento")
    assert "campos_criticos" in contrato
    assert "CO_UNIDADE" in contrato["campos_criticos"]


def test_obter_contrato_tabela_desconhecida_erro():
    with pytest.raises(ValueError):
        obter_contrato_tabela("nao_existe")


def test_campos_textuais_nucleares():
    campos = listar_campos_textuais()
    assert "CO_UNIDADE" in campos
    assert "CO_CNES" in campos


def test_validar_presenca_campos_case_insensitive():
    resultado = validar_presenca_campos(
        ["co_unidade", "co_cnes", "NO_FANTASIA", "no_razao_social"], "tbEstabelecimento"
    )
    assert "CO_UNIDADE" in resultado["campos_presentes"]
    assert "CO_MUNICIPIO_GESTOR" in resultado["campos_ausentes"]
    assert resultado["ok"] is False
