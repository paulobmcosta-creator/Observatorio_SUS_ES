"""Inspeção estrutural direta dos membros do consolidado, sem editar documentos."""
import argparse
import ast
import csv
import json
import struct
import subprocess
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from observatorio_sus.io.custodia import sha256_arquivo
from .lote import ler, salvar


def descrever(p):
    ext=p.suffix.lower()
    if ext==".csv":
        with p.open(encoding="utf-8-sig",newline="") as f:
            r=csv.reader(f)
            campos=next(r)
            return f"{sum(1 for _ in r)} registros; {', '.join(campos)}"
    if ext==".pdf":
        paginas=subprocess.check_output(["pdftotext","-layout",str(p),"-"]).decode().split("\f")
        return f"{len(paginas)-1} páginas; {sum(len(t.split()) for t in paginas)} palavras extraídas"
    if ext in {".docx",".zip"}:
        with ZipFile(p) as z:
            if z.testzip():
                raise ValueError(f"CRC inválido em {p.name}")
            if ext==".docx":
                doc=ET.fromstring(z.read("word/document.xml"))
                return f"{len(doc.findall('.//{*}p'))} parágrafos; {len(doc.findall('.//{*}tbl'))} tabelas"
            return f"{len(z.namelist())} membros verificados; " + ", ".join(z.namelist()[:4])
    if ext==".dbc":
        n,h,t=struct.unpack_from("<IHH",p.read_bytes(),4)
        return f"cabeçalho dBASE: {n} registros, {h} bytes de cabeçalho, {t} bytes por registro"
    if ext==".json":
        obj=json.loads(p.read_text())
        return f"{len(obj)} entradas; "+(", ".join(list(obj)[:8]) if isinstance(obj,dict) else "lista")
    if ext==".py":
        return ", ".join(n.name for n in ast.parse(p.read_bytes()).body if isinstance(n,ast.FunctionDef))
    if ext==".png":
        from PIL import Image
        with Image.open(p) as im:
            size=str(im.size)
            im.verify()
        return f"PNG íntegro; dimensões {size}"
    if ext==".svg":
        return f"SVG válido; viewBox {ET.parse(p).getroot().get('viewBox')}"
    texto=p.read_bytes().decode("latin1" if ext in (".def",".cnv") else "utf-8-sig")
    return f"{len(texto.splitlines())} linhas; {len(texto.split())} palavras"


def inspecionar(acervo,saida):
    inventario = ler(acervo/"ativos.csv")
    cp = {r["sha256"] for r in inventario if r["pacote"]!="consolidado"}
    linhas=[]
    for r in inventario:
        if r["pacote"]=="consolidado":
            p=acervo/"consolidado"/r["membro"]
            if sha256_arquivo(p)!=r["sha256"]:
                raise ValueError(p)
            linhas.append((r["membro"],r["bytes"],r["sha256"],"sim" if r["sha256"] in cp else "nao",descrever(p)))
    salvar(saida,["membro","bytes","sha256","duplicado_em_checkpoint","inspecao_direta"],linhas)
    print(len(linhas),Counter(r[3] for r in linhas))


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("acervo",type=Path)
    p.add_argument("saida",type=Path)
    a=p.parse_args()
    inspecionar(a.acervo,a.saida)
