"""Riscos de perda de identificadores, vazios, acentos e multiplicidade."""
import csv

import pyarrow.parquet as pq
import pytest

from observatorio_sus.transform.converter_csv_parquet import converter_csv_parquet, sha256


def test_preservar_codigos_vazios_duplicatas_e_encoding(tmp_path):
    fonte = tmp_path / "fonte.csv"
    linhas = [["chave", "valor"], ["0000123", "NA"], ["1234567890123456789012345678901", ""],
              ["0000123", "São José;\ntexto"], ["0000123", "São José;\ntexto"], ["0", "  "]]
    with fonte.open("w", encoding="latin-1", newline="") as f:
        csv.writer(f, delimiter=";").writerows(linhas)
    m = converter_csv_parquet(fonte, tmp_path / "saida", sha256(fonte), encoding="latin-1", delimitador=";",
                              proveniencia=dict(sistema="fixture", familia="sintetica", competencia="teste",
                                                origem_primaria="fixture", origem_recuperacao="teste"))
    t = pq.read_table(m["arquivo_derivado"])
    assert list(zip(*(c.to_pylist() for c in t.columns))) == list(map(tuple, linhas[1:]))
    assert m["linhas"] == 5
    with pytest.raises(FileExistsError):
        converter_csv_parquet(fonte, tmp_path / "saida", sha256(fonte), encoding="latin-1", delimitador=";", proveniencia=m)


@pytest.mark.parametrize("conteudo", ["a,a\n1,2\n", "a,b\n1\n"])
def test_recusar_perda_de_campo(tmp_path, conteudo):
    fonte = tmp_path / "fonte.csv"
    fonte.write_text(conteudo)
    with pytest.raises(ValueError):
        converter_csv_parquet(fonte, tmp_path / "saida", sha256(fonte), proveniencia=dict(
            sistema="fixture", familia="sintetica", competencia="teste", origem_primaria="fixture", origem_recuperacao="teste"))
    assert not (tmp_path / "saida").exists()


def test_recusar_fonte_diferente(tmp_path):
    fonte = tmp_path / "fonte.csv"
    fonte.write_text("a\n001\n")
    with pytest.raises(ValueError, match="SHA-256"):
        converter_csv_parquet(fonte, tmp_path / "saida", "0" * 64, proveniencia=dict(
            sistema="fixture", familia="sintetica", competencia="teste", origem_primaria="fixture", origem_recuperacao="teste"))
    assert not (tmp_path / "saida").exists()
