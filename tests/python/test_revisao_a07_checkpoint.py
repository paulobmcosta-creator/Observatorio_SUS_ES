"""Interrupção entre escritas, conflito externo e exclusão de escritores."""
import pytest
from observatorio_sus.io.checkpoints import aplicar_lote, recuperar_lote
from observatorio_sus.io.custodia import escritor_unico
import subprocess
import sys
import os
from pathlib import Path


def test_interrupcao_e_recuperacao_coerente(tmp_path):
    (tmp_path / "plano").write_bytes(b"p0")
    (tmp_path / "estado").write_bytes(b"e0")
    controle = tmp_path / "controle"
    def interromper(i):
        if i == 0:
            raise OSError("interrupção entre duas escritas")
    with escritor_unico(controle):
        with pytest.raises(OSError):
            aplicar_lote(tmp_path, controle, {"plano": b"p1", "estado": b"e1"}, interromper)
        assert (controle / "ATIVA.json").exists()
        with pytest.raises(RuntimeError):
            aplicar_lote(tmp_path, controle, {"plano": b"p2"})
        assert recuperar_lote(tmp_path, controle)
    assert (tmp_path / "plano").read_bytes() == b"p1"
    assert (tmp_path / "estado").read_bytes() == b"e1"
    assert not (controle / "ATIVA.json").exists()


def test_conflito_nao_sobrescreve_trabalho_alheio(tmp_path):
    controle = tmp_path / "controle"
    with escritor_unico(controle):
        with pytest.raises(RuntimeError):
            aplicar_lote(tmp_path, controle, {"a": b"a", "b": b"b"}, lambda _: (_ for _ in ()).throw(RuntimeError("falha")))
        (tmp_path / "b").write_bytes(b"trabalho alheio")
        with pytest.raises(RuntimeError, match="externa"):
            recuperar_lote(tmp_path, controle)
        assert (tmp_path / "b").read_bytes() == b"trabalho alheio"


def test_crash_abrupto_exige_recuperacao_explicita(tmp_path):
    codigo = '''
from pathlib import Path
import sys,os
from observatorio_sus.io.checkpoints import aplicar_lote
from observatorio_sus.io.custodia import escritor_unico
r=Path(sys.argv[1]);c=r/'controle'
with escritor_unico(c):
 aplicar_lote(r,c,{'plano':b'p1','estado':b'e1'},lambda _:os._exit(17))
'''
    p=subprocess.run([sys.executable,'-c',codigo,str(tmp_path)],env={**os.environ,'PYTHONPATH':str(Path('python').resolve())},timeout=10)
    assert p.returncode==17
    c=tmp_path/'controle'
    assert (c/'ATIVA.json').exists() and (c/'escritor.lock').exists()
    # O filho deste próprio teste terminou; liberação não depende da idade/PID de outro host.
    (c/'escritor.lock').rename(c/'lock_crash_preservado')
    with escritor_unico(c):recuperar_lote(tmp_path,c)
    assert (tmp_path/'plano').read_bytes()==b'p1' and (tmp_path/'estado').read_bytes()==b'e1'
