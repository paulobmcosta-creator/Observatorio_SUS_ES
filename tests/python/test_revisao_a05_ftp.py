"""FTP fake com a mesma API stdlib; nenhum servidor/host real é consultado."""
import io
import ftplib
import pytest
from observatorio_sus.extract.adquirir_objetos import FTPOficial
from observatorio_sus.io.custodia import adquirir_conjunto
from test_custodia import contrato, executar, atual


class SocketFake:
    def __init__(self, data): self.data = data
    def makefile(self, modo): return io.BytesIO(self.data)
    def close(self): pass


class FTPFake:
    dados = {"/RD/a.dbc": b"ab", "/RD/b.dbc": b"cd"}
    falha = None
    mudou = False
    def connect(self, host, port, timeout): assert host == "ftp.example.invalid"
    def login(self, user, passwd): assert user == "anonymous"
    def voidcmd(self, cmd): assert cmd == "TYPE I"
    def close(self): pass
    def size(self, path): return len(self.dados[path])
    def sendcmd(self, cmd): return "213 " + ("r2" if self.mudou else "r1")
    def transfercmd(self, cmd):
        path = cmd[5:]
        if path == self.falha: raise ftplib.error_perm("550 parte indisponível")
        return SocketFake(self.dados[path])
    def voidresp(self): return "226 OK"
    def mlsd(self, *args, **kwargs):
        return [("RDES2401a.dbc", {"type":"file","size":"2","modify":"20240102"}),
                ("RDES2401b.dbc", {"type":"file","size":"3","modify":"20240103"}),
                ("RDES2402.dbc", {"type":"file","size":"2"})]


def test_ftp_nativo_e_partes_fake(tmp_path):
    cliente = FTPOficial(["ftp.example.invalid"], fabrica=FTPFake)
    lista = cliente.descobrir_rd("ftp://ftp.example.invalid/RD/", "202401")
    assert [r["nome"] for r in lista] == ["RDES2401a.dbc", "RDES2401b.dbc"]
    objetos = [{**contrato(k, v), "uri_oficial": "ftp://ftp.example.invalid/RD/" + k + ".dbc"}
               for k,v in [("a", b"ab"), ("b", b"cd")]]
    r = adquirir_conjunto(tmp_path, objetos, cliente)
    assert atual(tmp_path) == r["conteudo_id"]
    FTPFake.falha = "/RD/b.dbc"
    try:
        with pytest.raises(ftplib.error_perm): adquirir_conjunto(tmp_path, objetos, cliente)
        assert atual(tmp_path) == r["conteudo_id"]
    finally: FTPFake.falha = None


def test_revisao_ftp_e_path_invalido(tmp_path):
    class Mutante(FTPFake):
        def voidresp(self): self.mudou = True
    cliente = FTPOficial(["ftp.example.invalid"], fabrica=Mutante)
    o = {**contrato("a", b"ab"), "uri_oficial":"ftp://ftp.example.invalid/RD/a.dbc"}
    with pytest.raises(ValueError, match="mudou"): adquirir_conjunto(tmp_path, [o], cliente)
    with pytest.raises(ValueError): cliente._uri("ftp://ftp.example.invalid/RD/%2e%2e/a")
