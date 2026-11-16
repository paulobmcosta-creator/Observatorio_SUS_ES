"""Estados de qualidade e casos de fronteira técnicos; fixtures sintéticas."""
import pyarrow.parquet as pq
import pytest

from observatorio_sus.transform.converter_csv_parquet import converter_csv_parquet, sha256
from observatorio_sus.transform.validar_partes_csv import avaliar_regra, validar_partes_csv


@pytest.mark.parametrize("universo,violacoes,kwargs,estado", [
    (0, 0, {}, "FALHOU"), (None, None, {}, "PENDENTE"), (10, 0, {}, "APROVADO"),
    (10, 1, {}, "FALHOU"), (10, 1, {"limite": 1}, "APROVADO"),
    (None, None, {"aplicavel": False, "motivo": "Não se aplica ao estimando."}, "NÃO_APLICÁVEL"),
    (None, None, {"erro": "Exceção do leitor"}, "ERRO")])
def test_estados_sem_sucesso_vazio(universo, violacoes, kwargs, estado):
    r = avaliar_regra("Q01", "1", universo, violacoes, criterio="zero violações estruturais; limite excepcional quando declarado", **kwargs)
    assert r["estado"] == estado


def test_sobreposicao_nao_deduplica_n_aih(tmp_path):
    a, b = tmp_path / "a.csv", tmp_path / "b.csv"
    a.write_text("N_AIH,valor\n0001,aa\n0001,bb\n")
    b.write_text("valor,N_AIH\nbb,0001\n")
    r = validar_partes_csv({"a": a, "b": b}, ["N_AIH"], ["N_AIH", "valor"])
    assert r["linhas"] == 3 and r["sobreposicoes"] == 1 and r["estado"] == "PENDENTE"
    assert a.read_text().count("0001") == 2


@pytest.mark.parametrize("texto", ["valor\naa\n", "N_AIH,novo\n0001,x\n", "N_AIH,N_AIH\nx,y\n", ""])
def test_esquema_exige_decisao(tmp_path, texto):
    a = tmp_path / "a.csv"; a.write_text(texto)
    with pytest.raises(ValueError):
        validar_partes_csv({"a": a}, ["N_AIH"], ["N_AIH", "valor"])


@pytest.mark.parametrize("n", [0, 1, 10000, 20000])
def test_csv_vazio_e_multiplos_exatos_preservados(tmp_path, n):
    a = tmp_path / "a.csv"; a.write_text("codigo,valor\n" + "0001,NA\n" * n)
    r = validar_partes_csv({"a": a}, ["codigo"], ["codigo", "valor"])
    assert r["linhas"] == n and r["sobreposicoes"] == 0
    m = converter_csv_parquet(a, tmp_path / "saida", sha256(a), proveniencia=dict(
        sistema="fixture", familia="CSV", competencia="202401", origem_primaria="fixture", origem_recuperacao="local"))
    assert m["linhas"] == n and pq.ParquetFile(m["arquivo_derivado"]).metadata.num_rows == n


def test_recusar_alteracao_durante_conversao(tmp_path, monkeypatch):
    import observatorio_sus.transform.converter_csv_parquet as mod
    a = tmp_path / "a.csv"; a.write_text("codigo\n0001\n")
    original = mod.resumir_parquet
    def alterar(arquivo):
        retorno = original(arquivo)
        a.write_text("codigo\n0002\n")
        return retorno
    monkeypatch.setattr(mod, "resumir_parquet", alterar)
    with pytest.raises(ValueError, match="alterada"):
        mod.converter_csv_parquet(a, tmp_path / "saida", sha256(a), proveniencia=dict(
            sistema="fixture", familia="CSV", competencia="202401", origem_primaria="fixture", origem_recuperacao="local"))
    assert not (tmp_path / "saida/dados.parquet").exists()
