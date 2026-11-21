"""Auditoria da causa básica em uma edição anual do SIM identificada por hash."""
import argparse
import csv
import io
import json
import platform
import re
import tempfile
from collections import Counter
from datetime import date
from importlib.metadata import version
from pathlib import Path
from zipfile import ZipFile

from observatorio_sus.io.custodia import escrever_json, sha256_arquivo
from . import territorio
from .lote import executar, ler, salvar
from .territorio import TABELA, mapa

FONTES = TABELA.parents[2]/"config/estudos/edicoes_sim_camila.csv"
CAMPOS = ["TIPOBITO", "DTOBITO", "CODMUNRES", "CAUSABAS", "IDADE"]
CHAVE = ["mes", "idade_quinquenal", "municipio_residencia", "regiao", "causa_basica"]
CID = re.compile(r"[A-Z][0-9]{2}(?:\.?[A-Z0-9])?")
GRUPOS = {"G1": (20,25), "G2": (50,50), "G3": (60,69), "G4": (10,15), "G5": (70,79)}


def causa(valor):
    valor = valor.strip().upper()
    if not valor:
        return "AUSENTE"
    return valor.replace(".", "") if CID.fullmatch(valor) else "INVALIDA"


def faixa(valor):
    if not re.fullmatch(r"[1-5][0-9]{2}", valor):
        return "IGNORADA"
    unidade, n = valor[0], int(valor[1:])
    if unidade in "123" and n:
        return "00"
    if unidade == "5" and n < 30:
        return "85+"
    if unidade != "4":
        return "IGNORADA"
    return "85+" if n >= 85 else f"{n//5*5:02d}"


def leitor_csv(stream, ano, regioes):
    tabela = csv.DictReader(io.TextIOWrapper(stream, encoding="latin1", newline=""), delimiter=";")
    campos = [c.strip().upper() for c in tabela.fieldnames]
    if len(set(campos)) != len(campos) or not set(CAMPOS)<=set(campos):
        raise ValueError("Layout SIM incompatível")
    tabela.fieldnames = campos
    cubo, qa = Counter(), Counter()
    for row in tabela:
        if None in row or any(row[c] is None for c in CAMPOS):
            raise ValueError("Registro fora do layout SIM")
        tipo, data, mun, cid, idade = [row[c].strip() for c in CAMPOS]
        qa["origem"] += 1
        if not mun.startswith("32") or tipo!="2":
            continue
        qa["res_es_tipo2"] += 1
        d = data.zfill(8)
        try:
            if not re.fullmatch(r"[0-9]{7,8}", data):
                raise ValueError()
            dt = date(int(d[4:]),int(d[2:4]),int(d[:2]))
        except ValueError:
            qa["data_invalida"] += 1
            continue
        if dt.year != ano:
            qa["outro_ano"] += 1
            continue
        normal = causa(cid)
        antigo = cid.upper().replace(".", "")
        if re.fullmatch(r"I50[A-Z0-9]?",antigo) and normal=="INVALIDA":
            qa["I50_apenas_apos_retirada_irrestrita_de_pontos"] += 1
        if normal.startswith("I50"):
            qa["I50_com_ponto" if "." in cid else "I50_sem_ponto"] += 1
        qa["elegiveis"] += 1
        if normal in ("INVALIDA","AUSENTE"):
            qa[normal] += 1
        if normal.startswith("I") and normal!="INVALIDA":
            cubo[(d[2:4],faixa(idade),mun,regioes.get(mun,"RES_ES_IGNORADO"),normal)] += 1
    return cubo, +qa, campos


def leitor_pandas(stream, ano, regioes):
    import pandas as pd
    cubo, qa = Counter(), Counter()
    for bloco in pd.read_csv(stream, sep=";", encoding="latin1", dtype=str, keep_default_na=False,
                             chunksize=60000, skip_blank_lines=False):
        bloco.columns = bloco.columns.str.strip().str.upper()
        b = bloco[CAMPOS].apply(lambda c: c.str.strip())
        qa["origem"] += len(b)
        b = b.loc[b.CODMUNRES.str[:2].eq("32") & b.TIPOBITO.eq("2")].copy()
        qa["res_es_tipo2"] += len(b)
        data = pd.to_datetime(b.DTOBITO.where(b.DTOBITO.str.fullmatch(r"[0-9]{7,8}")).str.zfill(8),
                              format="%d%m%Y", errors="coerce")
        qa["data_invalida"] += int(data.isna().sum())
        qa["outro_ano"] += int((data.notna() & data.dt.year.ne(ano)).sum())
        b = b.loc[data.dt.year.eq(ano)].copy()
        qa["elegiveis"] += len(b)
        cod = b.CAUSABAS.str.upper()
        valido = cod.str.fullmatch(r"(?:[A-Z][0-9]{2}|[A-Z][0-9]{2}\.?[0-9A-Z])")
        legado_i50 = cod.str.replace(".", "",regex=False).str.fullmatch(r"I50[A-Z0-9]?")
        ponto = cod.str.contains(".",regex=False)
        qa["I50_apenas_apos_retirada_irrestrita_de_pontos"] += int((legado_i50 & ~valido).sum())
        qa["I50_com_ponto"] += int((legado_i50 & valido & ponto).sum())
        qa["I50_sem_ponto"] += int((legado_i50 & valido & ~ponto).sum())
        qa["AUSENTE"] += int(cod.eq("").sum())
        qa["INVALIDA"] += int((cod.ne("") & ~valido).sum())
        b = b.loc[valido & cod.str.startswith("I")].copy()
        b["causa_basica"] = cod.loc[b.index].str.replace(".", "",regex=False)
        b["mes"] = data.loc[b.index].dt.strftime("%m")
        b["municipio_residencia"] = b.CODMUNRES
        b["regiao"] = b.CODMUNRES.map(regioes).fillna("RES_ES_IGNORADO")
        b["idade_quinquenal"] = "IGNORADA"
        age = pd.to_numeric(b.IDADE.str[1:].where(b.IDADE.str.fullmatch(r"[1-5][0-9]{2}")),errors="coerce")
        unit = b.IDADE.str[0]
        b.loc[unit.isin(list("123")) & age.gt(0),"idade_quinquenal"] = "00"
        years = unit.eq("4") & age.lt(85)
        b.loc[years,"idade_quinquenal"] = (age[years]//5*5).astype(int).astype(str).str.zfill(2)
        b.loc[(unit.eq("4") & age.ge(85)) | (unit.eq("5") & age.lt(30)),"idade_quinquenal"] = "85+"
        cubo.update(b.groupby(CHAVE).size().to_dict())
    return cubo, +qa


def duplo(origem, membro, ano, regioes, stage):
    with ZipFile(origem) as z:
        if z.namelist() != [membro]:
            raise ValueError("Membro SIM incompatível com a edição")
        with z.open(membro) as stream:
            a,qa,campos = leitor_csv(stream,ano,regioes)
        with z.open(membro) as stream:
            b,qb = leitor_pandas(stream,ano,regioes)
    if qa!=qb or a!=b:
        raise ValueError("Leitores divergem em QA ou chave de observação")
    arquivos = {}
    for leitor,cubo in (("csv",a),("pandas",b)):
        p=stage/f"{leitor}.csv"
        salvar(p, [*CHAVE,"obitos"], [(*k,v) for k,v in sorted(cubo.items())])
        arquivos[leitor]=sha256_arquivo(p)
    detalhamento = Counter()
    for (*_,cid),n in a.items():
        if cid.startswith("I50"):
            detalhamento[cid]+=n
    return dict(layout=campos, qa=dict(qa), hashes_leituras=arquivos, chaves=len(a), G0=a.total(),
                I50=detalhamento.total(), subcategorias=dict(detalhamento))


def diagnosticar(origem, ano, destino, conferir=False):
    edicao = next(r for r in ler(FONTES) if int(r["ano"])==ano)
    if origem.stat().st_size!=int(edicao["bytes"]) or sha256_arquivo(origem)!=edicao["sha256"]:
        raise ValueError("Original difere da edição SIM identificada no CP01")
    entradas = dict(original=origem, edicoes=FONTES, territorio=TABELA)
    regra = dict(ano=ano, membro=edicao["membro"], filtro="residencia prefixo 32; TIPOBITO=2; ano DTOBITO; CAUSABAS I00-I99",
                 chaves=CHAVE, versao=1, pandas=version("pandas"), python=platform.python_version())
    def calcular(stage):
        evidencia = duplo(origem,edicao["membro"],ano,mapa(),stage)
        escrever_json(stage/"dupla_leitura.json",dict(evidencia, original=edicao["sha256"], parametros=regra,
                     metodo=sha256_arquivo(Path(__file__))))
        return evidencia
    recibo=executar(destino,entradas,regra,calcular,[Path(territorio.__file__)])
    if conferir:
        with tempfile.TemporaryDirectory() as tmp:
            esperado=calcular(Path(tmp))
            if (sha256_arquivo(Path(tmp)/"dupla_leitura.json")!=recibo["saidas"]["dupla_leitura.json"]
                    or esperado!=recibo["controles"]):
                raise ValueError("A releitura do original divergiu do recibo")
    return recibo


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("ano",type=int,choices=range(2014,2025))
    p.add_argument("original",type=Path)
    p.add_argument("destino",type=Path)
    p.add_argument("--conferir",action="store_true")
    a=p.parse_args()
    print(diagnosticar(a.original,a.ano,a.destino,a.conferir)["id"])
