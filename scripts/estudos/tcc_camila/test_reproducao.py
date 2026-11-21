"""Fixtures sintéticas para o contrato de projeção e os diagramas."""
import sys
from pathlib import Path
import numpy as np
import pytest
from reproduzir import novo
from produtos import inclusiva
from figuras_conjuntos import validar_particao

def test_particao_tem_exterior_e_inclusiva():
    valores = validar_particao(np.array([50, 2, 4, 3, 1, 8, 5, 7]), 3)
    assert inclusiva(valores, 0) == 80
    assert inclusiva(valores, 3) == 10
    assert inclusiva(valores, 7) == 7

def test_rejeita_particao_incompleta_ou_negativa():
    with pytest.raises(ValueError):validar_particao(np.ones(7, dtype=int), 3)
    with pytest.raises(ValueError):validar_particao(np.array([-1, 0]), 1)

def test_saida_preserva_edicao_anterior(tmp_path):
    path = tmp_path / "protegida"
    novo(path)
    (path / "termo.txt").write_text("preservar", encoding="utf8")
    with pytest.raises(ValueError):novo(path)
    assert (path / "termo.txt").read_text(encoding="utf8") == "preservar"


def test_upset_ordena_padroes_positivos_sem_exterior():
    from figuras_conjuntos import upset
    import matplotlib.pyplot as plt
    fig=plt.figure()
    try:
        masks=upset(fig, ["A", "B", "C"], np.array([99, 0, 4, 0, 0, 3, 3, 1]))
        assert masks == [2, 5, 6, 7]
    finally:
        plt.close(fig)


def test_ecg_leitor_binario_preserva_zero_a_esquerda_e_competencia():
    from pilotos_oficiais import selecionar_ecg
    cod="0211020036"
    dados=np.array([(b"202412",b"0211020036"),(b"202411",b"0211020036"),(b"202412",b"0211020044")],
                   dtype=[("PA_CMP","S6"),("PA_PROC_ID","S10")])
    resultado=selecionar_ecg(dados,b"202412",cod)
    assert resultado.tolist()==[(b"202412",b"0211020036")]

def test_validador_detecta_troca_de_bytes_com_mesmo_tamanho(tmp_path, monkeypatch):
    import reproduzir

    monkeypatch.setattr(reproduzir, "ROOT", tmp_path)
    relativo = "resultados_publicos/fixture.csv"
    arquivo = tmp_path / relativo
    arquivo.parent.mkdir()
    arquivo.write_bytes(b"c1")
    esperado = reproduzir.sha(arquivo)
    reproduzir.conferir_arquivo(relativo, esperado, 2)
    arquivo.write_bytes(b"c2")
    with pytest.raises(ValueError, match="Arquivo divergente"):
        reproduzir.conferir_arquivo(relativo, esperado, 2)


def test_validador_rejeita_destino_externo_ao_acervo(tmp_path, monkeypatch):
    import reproduzir

    monkeypatch.setattr(reproduzir, "ROOT", tmp_path)
    arquivo = tmp_path / "restrito.csv"
    arquivo.write_bytes(b"x")
    with pytest.raises(ValueError, match="Destino público inválido"):
        reproduzir.conferir_arquivo("resultados_publicos/../restrito.csv", reproduzir.sha(arquivo), 1)
