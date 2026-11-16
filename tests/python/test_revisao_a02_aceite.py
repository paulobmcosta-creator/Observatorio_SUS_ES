"""A02: fixtures rotuladas indevidamente e coberturas incompletas são bloqueadas."""
import json
import pytest
from test_custodia import executar
from observatorio_sus.io.aceite_sih import conferir_provas


def test_fixture_nao_vira_empirico(tmp_path):
    p = tmp_path / "provas.json"; p.write_text(json.dumps({"natureza": "fixture_sintetica"}))
    with pytest.raises(ValueError, match="Fixture"):
        conferir_provas(p)


def test_strings_e_manifesto_uma_uf_nao_bastam(tmp_path):
    id = executar(tmp_path / "snapshot", {"a": b"sintetico"})
    p = tmp_path / "provas.json"
    p.write_text(json.dumps(dict(natureza="empirico", sistema="SIH", familia="RD", competencia="202401", conteudo_id=id,
                                snapshot="snapshot/versoes/" + id, cobertura_nacional="APROVADO", paridade_leitores="APROVADO")))
    with pytest.raises(ValueError, match="27 UFs"):
        conferir_provas(p)
