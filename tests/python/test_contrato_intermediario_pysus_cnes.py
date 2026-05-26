from python.observatorio_sus.cnes import contrato_intermediario_pysus_cnes as contrato


def test_importa_modulo_sem_rede():
    assert contrato is not None


def test_listar_grupos():
    grupos = contrato.listar_grupos_intermediarios()
    assert set(["ST", "LT", "SR"]).issubset(grupos.keys())


def test_campos_st():
    campos = contrato.listar_campos_observados("ST")
    assert {"CNES", "CODUFMUN", "COMPETEN"}.issubset(set(campos))


def test_campos_lt():
    campos = contrato.listar_campos_observados("LT")
    assert {"CODLEITO", "QT_SUS"}.issubset(set(campos))


def test_campos_sr():
    campos = contrato.listar_campos_observados("SR")
    assert {"SERV_ESP", "CLASS_SR"}.issubset(set(campos))


def test_equivalencias_nao_vazia():
    assert len(contrato.listar_equivalencias()) > 0


def test_equivalencia_cnes_preserva_texto():
    matches = [e for e in contrato.listar_equivalencias() if e["coluna_pysus"] == "CNES"]
    assert matches
    assert all(e["preservar_como_texto"] is True for e in matches)


def test_equivalencia_codufmun_preserva_texto():
    matches = [e for e in contrato.listar_equivalencias() if e["coluna_pysus"] == "CODUFMUN"]
    assert matches
    assert all(e["preservar_como_texto"] is True for e in matches)


def test_registro_co_unidade_inconclusivo():
    matches = [
        e for e in contrato.listar_equivalencias()
        if e["coluna_pysus"] == "CO_UNIDADE" and e["status_equivalencia"] == "INCONCLUSIVA"
    ]
    assert matches


def test_exporta_csv_cabecalho(tmp_path):
    destino = tmp_path / "contrato.csv"
    contrato.exportar_contrato_intermediario_csv(destino)
    assert destino.exists()
    header = destino.read_text(encoding="utf-8").splitlines()[0]
    assert header == (
        "grupo_pysus,descricao_grupo,coluna_pysus,campo_contrato_cnes,campo_legado_r,"
        "tipo_equivalencia,status_equivalencia,papel_metodologico,preservar_como_texto,"
        "risco_coercao,observacao"
    )
