"""Reponha o RD de novembro de 2024 exclusivamente por identidade com o CP04."""
import argparse
import json
import tempfile
from pathlib import Path

from assistencia_ftp_camila import obter
from lote_assistencial_camila import sih
from observatorio_sus.io.custodia import sha256_arquivo, escrever_json


def repor(v, saida):
    """Preserve a aquisição anterior e confronte a cópia com a identidade do membro."""
    nome = "RDES2411"
    evidencia = v.parent/"acervo/CP04/Evidencias/RDES2411.dbc.proveniencia.json"
    pin = json.loads(evidencia.read_text(encoding="utf8"))
    pasta = v/"originais-assistencia/RD/ES/202411"
    alvo = pasta/(nome+".dbc")
    url = "ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/RDES2411.dbc"
    if pin["url_catalogo"] != url or pin["arquivo"] != alvo.name:
        raise ValueError("Identidade de catálogo incompatível com CP04")

    def verificar(path):
        if path.stat().st_size != pin["bytes"] or sha256_arquivo(path) != pin["sha256"]:
            raise ValueError("Edição incompatível com o CP04")
        meta = json.loads((path.parent/"aquisicao.json").read_text())
        if (meta["uri_efetiva"] != url or meta["revisao_antes"] != meta["revisao_depois"]
                or meta["bytes"] != pin["bytes"] or meta["sha256"] != pin["sha256"]):
            raise ValueError("Recibo da reposição incompatível com CP04")

    if not pasta.exists():
        pasta.parent.mkdir(exist_ok=True, parents=True)
        with tempfile.TemporaryDirectory(dir=pasta.parent) as tmp:
            candidato = obter(Path(tmp),nome)
            verificar(candidato)
            candidato.parent.rename(pasta)
    verificar(alvo)
    rec = sih(v, alvo)
    prova = {"objeto":nome,"bytes":pin["bytes"],"sha256":pin["sha256"],"url":url,
             "proveniencia_cp04":sha256_arquivo(evidencia),"recibo_analitico":rec["id"]}
    saida.mkdir(exist_ok=True,parents=True)
    recibo = saida/"reposicao-cp04.json"
    if recibo.exists():
        if json.loads(recibo.read_text()) != prova:
            raise ValueError("Recibo preexistente de reposição divergente")
    else:
        escrever_json(recibo, prova)
    return prova


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("custodia", type=Path)
    p.add_argument("saida", type=Path)
    args = p.parse_args()
    print(repor(args.custodia, args.saida))
