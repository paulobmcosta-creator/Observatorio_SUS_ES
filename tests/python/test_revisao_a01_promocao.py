"""A01: falhas reais injetadas nas fronteiras de replace/fsync, sem rollback alegado."""
import json
import pytest
import observatorio_sus.io.custodia as mod
from test_custodia import executar, atual


@pytest.mark.parametrize("ponto", ["antes_replace", "depois_replace", "fsync"])
def test_estado_observado_apos_falha(tmp_path, monkeypatch, ponto):
    anterior = executar(tmp_path, {"a": b"old"})
    substituir = mod.os.replace
    sincronizar = mod.sincronizar_diretorio
    def replace(a, b):
        if ponto == "antes_replace":
            raise OSError("antes de trocar")
        substituir(a, b)
        if ponto == "depois_replace":
            raise OSError("após trocar")
    def fsync(p):
        if ponto == "fsync" and p == tmp_path:
            raise OSError("fsync do diretório falhou")
        sincronizar(p)
    monkeypatch.setattr(mod.os, "replace", replace)
    monkeypatch.setattr(mod, "sincronizar_diretorio", fsync)
    with pytest.raises(mod.ErroPromocao) as erro:
        executar(tmp_path, {"a": b"new"})
    r = erro.value.resultado
    assert r["rollback_automatico"] is False
    if ponto == "antes_replace":
        assert atual(tmp_path) == anterior and r["promocao"] == "nao_realizada"
    else:
        assert atual(tmp_path) != anterior and r["promocao"] == "versao_integra_ativa"
        assert r["durabilidade"] == "indeterminada"
    mod.validar_versao(tmp_path / "versoes" / anterior)
    falha = json.loads(next((tmp_path / "recibos").glob("*.falha.json")).read_text())
    assert falha["promocao"] == r
