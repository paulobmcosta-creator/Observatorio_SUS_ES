"""Conferência aritmética delimitada de uma célula histórica, sem refazer aquisição.

Não reconstrói a consulta original Painel/TabNet/Excel nem homologação científica.
O DOCX fica local; somente o resumo sem valores pode ser versionado.
"""
import argparse
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET


def conferir(arquivo, hash_esperado):
    """Conferir razão histórica de casos/100 mil da linha Sul na Tabela 2."""
    digest = hashlib.sha256(arquivo.read_bytes()).hexdigest()
    if digest != hash_esperado:
        raise ValueError("Versão documental diverge do hash congelado.")
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with ZipFile(arquivo) as zip:
        raiz = ET.fromstring(zip.read("word/document.xml"))
    candidatos = []
    for tabela in raiz.findall(".//w:tbl", ns):
        linhas = [["".join(t.text or "" for t in c.findall(".//w:t", ns)) for c in r.findall("w:tc", ns)] for r in tabela.findall("w:tr", ns)]
        if linhas and linhas[0][0] == "Região de Saúde (residência)":
            candidatos += [r for r in linhas if r[0] == "Sul"]
    if len(candidatos) != 1:
        raise ValueError("Célula não localizada inequivocamente na edição fornecida.")
    linha = candidatos[0]
    numero = lambda v: Decimal(v.replace(".", "").replace(",", "."))
    populacao, casos, reportado = map(numero, [linha[1], linha[3], linha[4]])
    if populacao <= 0:
        raise ValueError("Denominador inválido.")
    calculado = (casos / populacao * 100000).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    if calculado != reportado:
        raise ValueError("Razão calculada diverge da célula histórica.")
    return dict(sha256_documento=digest, tabela="2", linha="Sul", campo="casos por 100 mil",
                numerador=str(casos), denominador=str(populacao), reportado=str(reportado), calculado=str(calculado),
                resultado="CONFERENCIA_ARITMETICA_HISTORICA", cadeia_consulta_original="PENDENTE",
                limite="Conjunto tabulado com população de referência 2024; não taxa anual nem validação dos casos.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("arquivo", type=Path)
    p.add_argument("--sha256", required=True)
    p.add_argument("--saida", required=True, type=Path)
    a = p.parse_args()
    r = conferir(a.arquivo, a.sha256)
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    with a.saida.open("x", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Conferência aritmética histórica aprovada; cadeia de consulta original pendente.")
