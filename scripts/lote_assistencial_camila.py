"""Custódia incremental e agregação mensal dos arquivos oficiais de assistência."""
from contextlib import contextmanager
from hashlib import sha256
from urllib.request import Request

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from dbfread import DBF

from observatorio_sus.estudos.camila import assistencia as ass
from observatorio_sus.estudos.camila.lote import executar, salvar
from observatorio_sus.estudos.camila.territorio import mapa, TABELA
from observatorio_sus.extract.adquirir_objetos import HTTPSOficial
from observatorio_sus.extract.envelope_datasus import EnvelopeMensal, FAMILIAS
from observatorio_sus.io.custodia import sha256_arquivo, escrever_json


class ClienteEnvelope(HTTPSOficial):
    """O envelope dinâmico pode mudar Last-Modified entre GET e HEAD.
    Confere duas cópias integrais do envelope e conserva os cabeçalhos das duas.
    """
    @contextmanager
    def abrir(self, objeto):
        url = objeto["uri_oficial"]
        self._validar_uri(url)
        limite = 250_000_000
        with tempfile.TemporaryFile() as temp:
            cabecalhos = []
            hashes = []
            for tentativa in range(2):
                h = sha256()
                tamanho = 0
                with self.opener.open(Request(url), timeout=self.timeout) as resp:
                    if resp.url != url:
                        raise ValueError("URL de envelope divergente")
                    cabecalhos.append(dict(resp.headers))
                    while bloco := resp.read(1 << 20):
                        tamanho += len(bloco)
                        if tamanho > limite:
                            raise ValueError("Envelope fora do orçamento")
                        h.update(bloco)
                        if tentativa == 0:
                            temp.write(bloco)
                    if resp.headers.get("Content-Length") and int(resp.headers["Content-Length"]) != tamanho:
                        raise ValueError("GET incompleto")
                hashes.append(h.hexdigest())
            if hashes[0] != hashes[1]:
                raise ValueError("Bytes do envelope mudaram")
            temp.seek(0)
            yield temp, dict(uri_efetiva=url,headers={"Content-Length":str(tamanho)},
                             cabecalhos_get=cabecalhos, sha256_duplo_get=hashes[0])


def adquirir(custodia, nome):
    fam, uf, aa, mm = re.fullmatch(r"(RD|HB|ST|LT|EQ|PF|PA)([A-Z]{2})(\d{2})(\d{2})",nome).groups()
    comp = "20"+aa+mm
    root = custodia/"originais-assistencia"/fam/uf/comp
    arquivo = root/(nome+".dbc")
    recibo = root/"aquisicao.json"
    if recibo.exists():
        if sha256_arquivo(arquivo) != json.loads(recibo.read_text())["sha256"]:
            raise ValueError("Original diverge do recibo")
        return arquivo
    limite = 250_000_000
    livre = shutil.disk_usage(custodia).free
    if livre < 3*limite+1_000_000_000:
        raise OSError("Espaço insuficiente para DBC, envelope e DBF")
    root.mkdir(exist_ok=True,parents=True)
    obj = dict(familia=fam, uf=uf, competencia=comp, caminho=arquivo.name, limite_bytes=limite,
               revisao=comp, uri_oficial=f"ftp://ftp.datasus.gov.br/dissemin/publicos/{FAMILIAS[fam][1]}/{arquivo.name}")
    with tempfile.TemporaryDirectory(dir=root) as tmp:
        stage = Path(tmp)/arquivo.name
        with EnvelopeMensal(tmp, limite, ClienteEnvelope(["datasus.saude.gov.br"],timeout=80)).abrir(obj) as (stream, meta), stage.open("xb") as out:
            shutil.copyfileobj(stream, out)
        if stage.stat().st_size != int(meta["headers"]["Content-Length"]):
            raise ValueError("Tamanho divergente")
        meta.update(sha256=sha256_arquivo(stage), bytes=stage.stat().st_size, livre_antes=livre,
                    utc=datetime.now(timezone.utc).isoformat())
        if arquivo.exists():
            if sha256_arquivo(arquivo) != meta["sha256"]:
                raise ValueError("Colisão de edição")
        else:
            stage.rename(arquivo)
        escrever_json(recibo,meta)
    return arquivo


def sih(custodia, arquivo):
    nome = arquivo.stem
    comp = "20"+nome[-4:]
    uf = nome[2:4]
    def medir(stage):
        reg = mapa()
        counts, qa, aih = Counter(),Counter(),Counter()
        with tempfile.TemporaryDirectory(dir=stage) as tmp:
            dbf = Path(tmp)/"mes.dbf"
            shutil.copyfile(arquivo, Path(tmp)/"fonte.dbc")
            subprocess.run([sys.executable,"-c","from pyreaddbc.readdbc import _dbc2dbf; _dbc2dbf('fonte.dbc','mes.dbf')"],
                           cwd=tmp,check=True)
            tabela = DBF(str(dbf),raw=True)
            campos = "ANO_CMPT MES_CMPT DIAG_PRINC N_AIH IDENT MUNIC_RES MUNIC_MOV DT_INTER DT_SAIDA SEXO COD_IDADE IDADE".split()
            if not set(campos)<=set(tabela.field_names):
                raise ValueError("Layout RD sem campos necessários")
            for row in tabela:
                a = {c:row[c].decode("latin1").strip() for c in campos}
                qa["ativos"] += 1
                if a["ANO_CMPT"]+a["MES_CMPT"] != comp:
                    raise ValueError("Competência incompatível")
                cid = ass.causa(a["DIAG_PRINC"])
                if not re.fullmatch(r"I\d{2}[A-Z0-9]?",cid):
                    continue
                qa["circulatorias_ident_"+a["IDENT"]] += 1
                if a["IDENT"] != "1":
                    continue
                key = a["N_AIH"]
                if key:
                    aih[key] += 1
                else:
                    qa["aih_sem_numero"] += 1
                adm,alta = ass.iso(a["DT_INTER"]),ass.iso(a["DT_SAIDA"])
                qa["datas_inconsistentes"] += (adm is None or alta is None or alta < adm)
                resid,atend = a["MUNIC_RES"],a["MUNIC_MOV"]
                counts[(adm.year if adm else 0,resid,ass.situacao(resid,reg),atend,ass.situacao(atend,reg),
                        a["SEXO"],a["COD_IDADE"],a["IDADE"],cid)] += 1
            qa["excluidos"] = sum(1 for _ in tabela.deleted)
            qa["cabecalho"] = tabela.header.numrecords
            qa["repeticoes_numero_aih"] = sum(n-1 for n in aih.values())
            if qa["ativos"]+qa["excluidos"] != qa["cabecalho"] or counts.total()!=qa["circulatorias_ident_1"]:
                raise ValueError("Balanço SIH inválido")
            salvar(stage/"fluxos.csv",["competencia","uf_arquivo","ano_admissao","municipio_res","regiao_res",
                  "municipio_atend","regiao_atend","sexo_sih","unidade_idade","idade","diagnostico","aih"],
                  ((comp,uf,*k,n) for k,n in sorted(counts.items())))
            return dict(qa=dict(qa), sha256_dbf=sha256_arquivo(dbf), campos=tabela.field_names)
    return executar(custodia/"sih"/nome/comp, {"dbc":arquivo,"pdr":TABELA},
                    {"competencia":comp,"uf_atendimento_arquivo":uf,"ident":"1","cid":"I00-I99"},medir,[Path(ass.__file__)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("custodia",type=Path)
    parser.add_argument("nomes",nargs="+")
    args=parser.parse_args()
    for nome in args.nomes:
        print(datetime.now(timezone.utc).isoformat(),nome,"preflight",shutil.disk_usage(args.custodia).free,flush=True)
        arquivo=adquirir(args.custodia,nome)
        print(nome,sha256_arquivo(arquivo),flush=True)
        if nome.startswith("RD"):
            print(nome,sih(args.custodia,arquivo)["id"],flush=True)
