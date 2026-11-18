"""Conferência offline das três gerações de recibos e catálogos do Work."""
import json
import re
from pathlib import Path
from zlib import crc32

from observatorio_sus.extract.envelope_datasus import PORTAL, consulta, selecionar
from observatorio_sus.io.custodia import sha256_arquivo


def normalizar(p,originais):
    doc=json.loads(p.read_text())
    if "arquivos" in doc:
        item=next(i for i in doc["arquivos"] if i["arquivo"]=="RDES2401.dbc")
        nome=item["arquivo"]
        uri=item["url_oficial_catalogo"]
        url=doc["url_efetiva_zip"]
        envelope=doc["envelope_sha256"]
        headers=doc["header_zip"]
    else:
        item=doc
        nome=p.name.split(".dbc")[0]+".dbc"
        uri=doc.get("url_catalogo") or doc["origem"]
        url=doc.get("url_efetiva") or doc["envelope_url"]
        envelope=doc.get("sha256_envelope")
        headers=doc.get("headers") or doc["transferencia"]["header"]
    objeto=dict(familia=nome[:2],competencia="20"+nome[4:8],uf=nome[2:4],caminho=nome,uri_oficial=uri)
    consulta(objeto)
    if not re.fullmatch(r"https://datasus\.saude\.gov\.br/wp-content/zipupload/Arq_[0-9]+/arquivo\.zip",url):
        raise ValueError("Envelope fora da rota documentada")
    membro=item.get("membro_envelope") or item.get("arquivo") or nome
    crc=item.get("crc32_envelope")
    if membro.lower()!=nome.lower():
        raise ValueError("Membro do recibo incompatível")
    raw=originais.get(nome)
    if raw:
        if raw.stat().st_size!=item["bytes"] or sha256_arquivo(raw)!=item["sha256"]:
            raise ValueError("Recibo e objeto divergem")
        if crc and f"{crc32(raw.read_bytes()):08x}"!=crc.lower():
            raise ValueError("CRC registrado diverge dos bytes originais")
    return dict(arquivo=nome,catalogo=PORTAL+"/ftp.php",uri_logica=uri,consulta_observada=item.get("consulta"),
                servico=PORTAL+"/download.php",pedido_observado=item.get("pedido"),url_efetiva=url,
                sha256_catalogo=item.get("sha256_catalogo"),membro=membro,crc32_registrado=crc,
                revisao_observada=headers,sha256_envelope=envelope,sha256_objeto=item["sha256"],bytes=item["bytes"],
                sha256_recibo=sha256_arquivo(p),estado="bytes_conferidos" if raw else "somente_recibo")


def conferir(acervo,referencias):
    objetos={p.name:p for p in referencias if p.suffix==".dbc"}
    origens=[normalizar(p,objetos) for p in referencias if p.name.endswith((".dbc.json",".proveniencia.json"))
             or p.name=="PROVENIENCIA_RDES2401.json"]
    if len(origens)!=8 or {r["arquivo"] for r in origens if r["estado"]=="bytes_conferidos"}!=set(objetos):
        raise ValueError("Cobertura de proveniência assistencial incompleta")
    catalogos=[]
    por_nome={r["arquivo"]:r for r in origens}
    for p in referencias:
        if p.parent != acervo/"CP04/Evidencias" or not p.name.endswith("_catalogo.json"):
            continue
        sistema,uf,mes,_=p.stem.split("_")
        familia={"sih":"RD","sia":"PA","cnes-eq":"EQ","cnes-lt":"LT"}[sistema]
        nome=familia+uf+mes[2:]+".dbc"
        rows=json.loads(p.read_text())
        uri=next(r["endereco"] for r in rows if r["arquivo"].lower()==nome.lower())
        obj=dict(familia=familia,uf=uf,competencia=mes,caminho=nome,uri_oficial=uri)
        _,form=consulta(obj)
        selecionar(rows,nome,form["fonte[]"],uri)
        hash_cat=sha256_arquivo(p)
        if nome in por_nome and por_nome[nome]["sha256_catalogo"]!=hash_cat:
            raise ValueError("Catálogo diverge do recibo Work")
        catalogos.append(dict(arquivo=nome,uri=uri,formulario_reconstruido=form,sha256_catalogo=hash_cat))
    return {"origens":origens,"catalogos":catalogos}
