"""Gerar a edição congelada do cadastro a partir dos dois membros conferidos."""
import argparse
import re
import subprocess
import unicodedata
from collections import Counter
from pathlib import Path

from observatorio_sus.io.custodia import sha256_arquivo
from .lote import ler, salvar

CSV_SHA = "4eaa33867efdc1c7197f64d5fbbbb04618f13028f6ab9a572e557afff67352d1"
PDF_SHA = "cc4dedb5dba7bdb18d6ac60c200426fe3a1e1ad031ab8c4ebceba0099d631896"
VERSAO = "PDR_ES_2024_CIB259_TCC_v1"
DATA = "2024-12-20"
PAGINAS = {"Central":6, "Norte":7, "Metropolitana":8, "Sul":9}
TABELA = Path(__file__).resolve().parents[4]/"metadata/territorio/pdr_es_2024_tcc_v1.csv"
CAMPOS = ("versao_territorial cod_municipio_cnes cod_municipio_ibge regiao_id regiao_nome "
          "vigencia_inicio vigencia_fim fonte_url ato_referencia sha256_fonte").split()


def texto(s):
    letras = unicodedata.normalize("NFKD", s.casefold())
    return " ".join(re.findall("[a-z]+", "".join(c for c in letras if not unicodedata.combining(c))))


def gerar(cadastro, ato, destino):
    if sha256_arquivo(cadastro) != CSV_SHA or sha256_arquivo(ato) != PDF_SHA:
        raise ValueError("Edição da correspondência ou do ato divergente")
    municipios = ler(cadastro)
    reg = {r["datasus6"]:r["regiao_pdr_2024"] for r in municipios}
    if any(not re.fullmatch(r"32[0-9]{5}", r["ibge7"]) or r["ibge7"][:6] != r["datasus6"] for r in municipios):
        raise ValueError("Códigos IBGE incompatíveis")
    if (len(municipios)!=78 or len(reg)!=78 or len({r["ibge7"] for r in municipios})!=78 or reg["320330"]!="Central" or
            Counter(reg.values())!={"Central":15,"Norte":14,"Metropolitana":23,"Sul":26}):
        raise ValueError("Domínio territorial incompatível")
    # Coluna de nomes, sem população, rodapé lateral ou rótulo à esquerda.
    paginas = subprocess.check_output(["pdftotext","-layout","-f","6","-l","9",str(ato),"-"],text=True).split("\f")
    texto_pagina = [texto(" ".join(l[22:46] for l in p.splitlines())) for p in paginas]
    linhas = []
    for r in municipios:
        nome, regiao = r["nome"], r["regiao_pdr_2024"]
        pag = PAGINAS[regiao]
        # O Anexo III omite a preposição deste município na linha da tabela.
        nome_no_ato = {"Divino de São Lourenço": "Divino São Lourenço"}.get(nome, nome)
        if not re.search(r"\b"+texto(nome_no_ato)+r"\b", texto_pagina[pag-6]):
            raise ValueError(f"Conferir {nome} na página {pag}")
        linhas.append((VERSAO,r["datasus6"],r["ibge7"],regiao,regiao,DATA,DATA,
                       "https://e-docs.es.gov.br/d/2024-L5WDBB",f"CIB/SUS-ES 259/2024 Anexo III p. {pag}",PDF_SHA))
    salvar(destino, CAMPOS, linhas)


def mapa(caminho=TABELA):
    """Consumidores do estudo usam uma edição explícita por hash da configuração."""
    config = {r["chave"]:r["valor"] for r in ler(TABELA.parents[2]/"config/estudos/tcc_cardiovascular.csv")}
    if sha256_arquivo(caminho) != config["territorio_sha256"]:
        raise ValueError("Edição territorial não corresponde à configuração do TCC")
    return {r["cod_municipio_cnes"]: r["regiao_nome"] for r in ler(caminho)}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ("cadastro","ato","destino"):
        p.add_argument(arg,type=Path)
    a=p.parse_args()
    gerar(a.cadastro,a.ato,a.destino)
