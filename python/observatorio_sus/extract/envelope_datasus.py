"""Transporte mensal do portal DATASUS para um membro identificado no inventário."""
from contextlib import contextmanager
from hashlib import sha256
import json
from pathlib import Path
import re
from tempfile import TemporaryFile
from urllib.parse import urlencode
from urllib.request import Request
from zipfile import ZipFile

from .adquirir_objetos import HTTPSOficial

PORTAL="https://datasus.saude.gov.br/wp-content"
FAMILIAS={"RD":("SIHSUS","SIHSUS/200801_/Dados"),"PA":("SIASUS","SIASUS/200801_/Dados"),
          **{f:("CNES","CNES/200508_/Dados/"+f) for f in ("ST","HB","LT","EQ","PF","SR")}}
UFS=set("AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split())


def consulta(objeto):
    fam,periodo,uf=objeto["familia"],objeto["competencia"],objeto["uf"]
    sistema,pasta=FAMILIAS[fam]
    if not re.fullmatch(r"20[0-9]{2}(0[1-9]|1[0-2])",periodo) or uf not in UFS:
        raise ValueError("Competência/UF inválida")
    nome=Path(objeto["caminho"]).name
    if not re.fullmatch(fam+uf+periodo[2:]+r"[a-z0-9_-]*\.dbc",nome,re.I):
        raise ValueError("Nome do membro não corresponde à partição")
    uri=f"ftp://ftp.datasus.gov.br/dissemin/publicos/{pasta}/{nome}"
    if objeto["uri_oficial"].lower()!=uri.lower():
        raise ValueError("URI lógica incompatível")
    return nome,{"fonte[]":sistema,"modalidade[]":"1","tipo_arquivo[]":fam,
                 "ano[]":periodo[:4],"mes[]":periodo[4:],"uf[]":uf}


def selecionar(catalogo,nome,fonte,uri):
    encontrados=[r["endereco"] for r in catalogo if r["arquivo"].lower()==nome.lower() and r["fonte"]==fonte]
    if len(encontrados)!=1 or encontrados[0].lower()!=uri.lower():
        raise ValueError("Membro/fonte ausente, ambíguo ou fora do inventário")
    return encontrados[0]


class EnvelopeMensal:
    def __init__(self,temporarios,limite_envelope,cliente=None):
        self.temp=Path(temporarios)
        self.limite=limite_envelope
        self.cliente=cliente or HTTPSOficial(["datasus.saude.gov.br"])
        if type(self.limite)!=int or self.limite<=0:
            raise ValueError("Limite positivo do envelope obrigatório")

    def _post(self,endpoint,form,limite):
        req=Request(PORTAL+endpoint,data=urlencode(form).encode(),
                    headers={"X-Requested-With":"XMLHttpRequest","Referer":"https://datasus.saude.gov.br/transferencia-de-arquivos/"})
        with self.cliente.opener.open(req,timeout=self.cliente.timeout) as resp:
            if resp.url!=PORTAL+endpoint:
                raise ValueError("Endpoint de catálogo/empacotamento divergente")
            data=resp.read(limite+1)
            if len(data)>limite:
                raise ValueError("Resposta excede limite")
        return json.loads(data),sha256(data).hexdigest()

    @contextmanager
    def abrir(self,objeto):
        nome,form=consulta(objeto)
        cat,hash_cat=self._post("/ftp.php",form,2_000_000)
        uri=selecionar(cat,nome,form["fonte[]"],objeto["uri_oficial"])
        membro=uri.rsplit("/",1)[1]
        pedido={"dados[0][arquivo]":membro,"dados[0][link]":uri}
        url,hash_pedido=self._post("/download.php",pedido,100_000)
        while isinstance(url,list) and len(url)==1:
            url=url[0]
        if not isinstance(url,str) or not re.fullmatch(r"https://datasus\.saude\.gov\.br/wp-content/zipupload/Arq_[0-9]+/arquivo\.zip",url):
            raise ValueError("Envelope incompatível")
        self.temp.mkdir(exist_ok=True,parents=True)
        with TemporaryFile(dir=self.temp) as tmp:
            digest=sha256()
            with self.cliente.abrir(dict(uri_oficial=url,evidencia_origem=hash_cat)) as (resp,meta):
                if meta["uri_efetiva"]!=url:
                    raise ValueError("URL efetiva do envelope divergente")
                while bloco:=resp.read(1<<20):
                    if tmp.tell()+len(bloco)>self.limite:
                        raise ValueError("Envelope excede espaço reservado")
                    digest.update(bloco)
                    tmp.write(bloco)
            n=tmp.tell()
            tamanho=meta["headers"].get("Content-Length")
            if tamanho is not None and n!=int(tamanho):
                raise ValueError("Envelope incompleto")
            with ZipFile(tmp) as z:
                if z.namelist()!=[membro] or z.getinfo(membro).file_size>objeto["limite_bytes"]:
                    raise ValueError("Membro incompatível com o lote")
                info=z.getinfo(membro)
                recibo=dict(meta,uri_oficial=uri,transporte="envelope_https_datasus",catalogo=PORTAL+"/ftp.php",
                        consulta=form,sha256_catalogo=hash_cat,servico=PORTAL+"/download.php",pedido=pedido,
                        sha256_resposta_pedido=hash_pedido,uri_envelope=url,sha256_envelope=digest.hexdigest(),
                        bytes_envelope=n,membro=membro,crc32=f"{info.CRC:08x}",revisao=objeto["revisao"],
                        headers_envelope=meta["headers"],headers={"Content-Length":str(info.file_size)})
                with z.open(info) as dados:
                    yield dados,recibo
