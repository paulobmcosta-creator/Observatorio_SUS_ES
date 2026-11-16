"""Catálogos inteiramente sintéticos; não alegam cobertura nacional real."""
import pytest
from observatorio_sus.extract.inventariar_sih_rd import inventariar_rd, UFS


def entrada(uf, sufixo=""):
    nome = f"RD{uf}2401{sufixo}.dbc"
    return dict(nome=nome, uri_oficial="https://example.invalid/" + nome, revisao="fixture-r1", bytes=10)


def test_ausencia_catalogo_nao_e_zero():
    r = inventariar_rd("202401")
    assert len(r["cobertura"]) == 27 and r["estado"] == "PENDENTE"
    assert {x["status"] for x in r["cobertura"]} == {"esperado_nao_consultado"}


def test_preservar_partes_e_conflito_revisao():
    catalogo = [entrada(uf) for uf in UFS] + [entrada("SP", "a"), entrada("SP", "b")]
    r = inventariar_rd("202401", catalogo, "fixture")
    assert len(r["objetos"]) == 29 and r["bytes_observados"] == 290
    assert r["estado"] == "CATALOGO_27UF_NAO_VALIDA_AQUISICAO"
    r = inventariar_rd("202401", catalogo + [{**entrada("SP"), "revisao": "fixture-r2"}], "fixture")
    assert r["conflito_revisoes"] and r["estado"] == "PENDENTE"
    with pytest.raises(ValueError):
        inventariar_rd("202401", catalogo)
