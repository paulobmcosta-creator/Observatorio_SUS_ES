"""Completar apenas a família SR do ES pelo catálogo oficial e pela custódia comum."""
import argparse
import ftplib
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from assistencia_ftp_camila import obter
from observatorio_sus.extract.adquirir_objetos import FTPOficial


class FTPEstendido(ftplib.FTP):
    """Negociar a porta de dados com EPSV no mesmo endereço da conexão de controle."""
    def makepasv(self):
        return ftplib.parse229(self.sendcmd("EPSV"), self.sock.getpeername())


def adquirir(out):
    lista = (out/"fontes/sr-lista.txt").read_text()
    def objeto(nome):
        tamanho, = re.findall(r"\s(\d+)\s+"+nome+r"\.dbc\s*$",lista,re.I|re.M)
        path = obter(out,nome,cliente=FTPOficial(fabrica=FTPEstendido,timeout=45))
        if path.stat().st_size!=int(tamanho):
            raise ValueError(nome)
        return nome
    with ThreadPoolExecutor(3) as pool:
        for n in pool.map(objeto,[f"SRES{y:02}{m:02}" for y in range(14,25) for m in range(1,13)]):
            print(n,flush=True)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("saida",type=Path)
    adquirir(parser.parse_args().saida)
