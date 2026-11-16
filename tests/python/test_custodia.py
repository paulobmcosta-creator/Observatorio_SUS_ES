"""Fixtures sintéticas: identidade não ambígua, falhas, rollback e restauração."""
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from observatorio_sus.extract.adquirir_objetos import ArquivosLocais, HTTPSOficial
from observatorio_sus.io.custodia import (adquirir_conjunto, escritor_unico, restaurar_snapshot,
                                        retornar_versao, validar_versao)
from observatorio_sus.io.manifestos import criar_identidade_conjunto


def contrato(id, dados, caminho=None):
    return dict(id=id, caminho=caminho or id + ".csv", sistema="fixture", familia="RD_sintetico",
                competencia="202401", uf="ES", parte=id, revisao="r1", layout="fixture-v1",
                bytes=len(dados), sha256=hashlib.sha256(dados).hexdigest(), limite_bytes=1024,
                uri_oficial="https://example.invalid/" + id, evidencia_origem="fixture; nao oficial")


class Memoria:
    def __init__(self, dados, falha=None):
        self.dados = dados
        self.falha = falha

    @contextmanager
    def abrir(self, objeto):
        if objeto["id"] == self.falha:
            raise OSError("falha sintética na parte")
        yield io.BytesIO(self.dados[objeto["id"]]), {"transporte": "memoria_sintetica"}


def atual(raiz):
    return json.loads((raiz / "CURRENT.json").read_text())["conteudo_id"]


def executar(raiz, dados, **kwargs):
    return adquirir_conjunto(raiz, [contrato(k, v) for k, v in dados.items()], Memoria(dados), **kwargs)["conteudo_id"]


def test_fronteiras_adversariais_ordem_e_idempotencia(tmp_path):
    # Mesma concatenação abc; manifestos distinguem partes/tamanhos/hashes.
    primeiro = executar(tmp_path, {"a": b"ab", "b": b"c"})
    segundo = executar(tmp_path, {"a": b"a", "b": b"bc"})
    assert primeiro != segundo
    assert executar(tmp_path, {"b": b"bc", "a": b"a"}) == segundo
    assert len(list((tmp_path / "versoes").iterdir())) == 2
    assert validar_versao(tmp_path / "versoes" / primeiro)[0] == primeiro
    m = contrato("a", b"ab")
    assert criar_identidade_conjunto([m]) == criar_identidade_conjunto([{**m, "timestamp": "outro", "uri_efetiva": "outra"}])


@pytest.mark.parametrize("caminho", ["../a", "/a", "a/../b", "a//b", "./a", "a\\b", "C:a", "a/.", "NUL", "a.", "a\x00b"])
def test_caminhos_recusados(tmp_path, caminho):
    with pytest.raises(ValueError):
        adquirir_conjunto(tmp_path, [contrato("a", b"a", caminho)], Memoria({"a": b"a"}))
    assert not (tmp_path / "CURRENT.json").exists()


@pytest.mark.parametrize("segundo", [contrato("a", b"b", "b.csv"), contrato("b", b"b", "a.csv"),
                                    contrato("b", b"b", "A.csv"), contrato("b", b"b", "a.csv/b")])
def test_ids_duplicados_e_conflitos(segundo):
    with pytest.raises(ValueError):
        criar_identidade_conjunto([contrato("a", b"a"), segundo])


def test_falha_segunda_parte_limite_hash_e_rollback(tmp_path):
    anterior = executar(tmp_path, {"a": b"old"})
    dados = {"a": b"new", "b": b"new"}
    with pytest.raises(OSError):
        adquirir_conjunto(tmp_path, [contrato(k, v) for k, v in dados.items()], Memoria(dados, falha="b"))
    assert atual(tmp_path) == anterior
    falhas = list((tmp_path / "recibos").glob("*.falha.json"))
    assert falhas and json.loads(falhas[0].read_text())["objetos"][1]["status"] == "falha"
    with pytest.raises(ValueError, match="tamanho/hash"):
        adquirir_conjunto(tmp_path, [contrato("a", b"old")], Memoria({"a": b"new"}))
    with pytest.raises(ValueError, match="limite"):
        adquirir_conjunto(tmp_path, [{**contrato("a", b"xx"), "limite_bytes": 1}], Memoria({"a": b"xx"}))
    assert atual(tmp_path) == anterior
    novo = executar(tmp_path, dados)
    retornar_versao(tmp_path, anterior)
    assert atual(tmp_path) == anterior and novo != anterior


def test_tres_para_dois_sem_chunk_orfao(tmp_path):
    anterior = executar(tmp_path, {"a": b"1", "b": b"2", "c": b"3"})
    novo = executar(tmp_path, {"a": b"4", "b": b"5"})
    assert anterior != novo
    assert len(list((tmp_path / "versoes" / novo / "objetos").iterdir())) == 2
    validar_versao(tmp_path / "versoes" / novo)
    extra = tmp_path / "versoes" / novo / "objetos/orfao.csv"
    extra.write_bytes(b"x")
    with pytest.raises(ValueError, match="não manifestados"):
        validar_versao(tmp_path / "versoes" / novo)


def test_restaurar_vazio_corrupto_e_adaptador_substituivel(tmp_path):
    raiz = tmp_path / "origem"; dados = b"codigo,valor\n0001,NA\n"
    id = executar(raiz, {"a": dados})
    fonte = raiz / "versoes" / id
    arquivo = fonte / "objetos/a.csv"
    outro = adquirir_conjunto(tmp_path / "contingencia", [contrato("a", dados)], ArquivosLocais({"a": arquivo}))
    assert outro["conteudo_id"] == id
    restaurado = restaurar_snapshot(fonte, tmp_path / "vazio", id)
    assert (restaurado / "objetos/a.csv").read_bytes() == dados
    with pytest.raises(ValueError, match="vazio"):
        restaurar_snapshot(fonte, tmp_path / "vazio", id)
    arquivo.write_bytes(b"corrupto")
    with pytest.raises(ValueError, match="corrompido"):
        restaurar_snapshot(fonte, tmp_path / "outro", id)
    assert not (tmp_path / "outro").exists()


def test_fonte_alterada_e_imutavel_corrompido(tmp_path):
    origem = tmp_path / "fonte.csv"; origem.write_bytes(b"aa")
    class Mutante(ArquivosLocais):
        @contextmanager
        def abrir(self, objeto):
            with super().abrir(objeto) as stream:
                yield stream
                origem.write_bytes(b"bb")
    with pytest.raises(ValueError, match="alterado"):
        adquirir_conjunto(tmp_path / "cache", [contrato("a", b"aa")], Mutante({"a": origem}))
    raiz = tmp_path / "cache"; id = executar(raiz, {"a": b"aa"})
    parte = raiz / "versoes" / id / "objetos/a.csv"; parte.write_bytes(b"bb")
    with pytest.raises(ValueError, match="corrompido"):
        executar(raiz, {"a": b"aa"})
    assert parte.read_bytes() == b"bb"  # Jamais sobrescrever versão existente.


def test_escritor_unico_e_falha_antes_ponteiro(tmp_path):
    anterior = executar(tmp_path, {"a": b"old"})
    with escritor_unico(tmp_path):
        with pytest.raises(RuntimeError, match="lock"):
            executar(tmp_path, {"a": b"new"})
    def falhar(_):
        raise OSError("crash simulado")
    with pytest.raises(OSError):
        executar(tmp_path, {"a": b"new"}, antes_promocao=falhar)
    assert atual(tmp_path) == anterior
    validar_versao(tmp_path / "versoes" / anterior)


def test_crash_abrupto_preserva_ponteiro_e_lock(tmp_path):
    anterior = executar(tmp_path, {"a": b"old"})
    codigo = """
import os,sys
from test_custodia import executar
from pathlib import Path
executar(Path(sys.argv[1]), {'a': b'new'}, antes_promocao=lambda _: os._exit(23))
"""
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(Path("python").resolve()), str(Path("tests/python").resolve())])}
    proc = subprocess.run([sys.executable, "-c", codigo, str(tmp_path)], env=env, timeout=10)
    assert proc.returncode == 23
    assert atual(tmp_path) == anterior and (tmp_path / "escritor.lock/owner.json").is_file()
    validar_versao(tmp_path / "versoes" / anterior)


def test_cliente_oficial_recusa_espelho_e_credenciais():
    cliente = HTTPSOficial(["ftp.datasus.gov.br"])
    for uri in ["http://ftp.datasus.gov.br/a", "https://example.invalid/a", "https://user:secret@ftp.datasus.gov.br/a"]:
        with pytest.raises(ValueError):
            cliente._validar_uri(uri)


def test_exclusao_entre_processos(tmp_path):
    with escritor_unico(tmp_path):
        codigo = "from observatorio_sus.io.custodia import escritor_unico; import sys;\nwith escritor_unico(sys.argv[1]): pass"
        proc = subprocess.run([sys.executable, "-c", codigo, str(tmp_path)], capture_output=True, text=True,
                              env={**os.environ, "PYTHONPATH": str(Path("python").resolve())}, timeout=10)
        assert proc.returncode != 0 and "lock" in proc.stderr
    assert not (tmp_path / "escritor.lock").exists()
