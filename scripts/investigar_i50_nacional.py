"""Apurar agregados por UF diretamente de uma edição oficial identificada por SHA."""
import argparse
import csv
import io
import re
from collections import Counter, defaultdict
from datetime import date
from functools import lru_cache
from pathlib import Path
from zipfile import ZipFile

from observatorio_sus.estudos.camila import sim
from observatorio_sus.estudos.camila.lote import executar, ler, salvar
from observatorio_sus.io.custodia import sha256_arquivo

UFS = dict(zip("11 12 13 14 15 16 17 21 22 23 24 25 26 27 28 29 31 32 33 35 41 42 43 50 51 52 53".split(),
               "RO AC AM RR PA AP TO MA PI CE RN PB PE AL SE BA MG ES RJ SP PR SC RS MS MT GO DF".split(), strict=True))
LINHAS = "LINHAA LINHAB LINHAC LINHAD LINHAII".split()
EXAMINAR = ("CAUSABAS CAUSABAS_O CB_PRE CAUSABAS_R CB_ALT TP_ALTERA STRESSELE ATESTADO "
            "ALTCAUSA VERSAOSCB VERSAOSIST DTCADASTRO DTRECEBIM DTINVESTIG STCODIFICA CODIFICADO").split() + LINHAS
CID_NO_TEXTO = re.compile(r"(?<![A-Z0-9.])[A-Z][0-9]{2}(?:\.?[A-Z0-9])?(?![A-Z0-9.])", re.I)
I50_NO_TEXTO = re.compile(r"(?<![A-Z0-9.])I50(?:\.?[A-Z0-9])?(?![A-Z0-9.])", re.I)
MEDIDAS = ("obitos G0 I50 I50_original I50_pre mencao_atestado mencao_linhas mencao_uniao "
           "atestado_com_cid I50_e_mencao I50_com_original_valida original_valida").split()
normalizar = lru_cache(maxsize=32768)(sim.causa)


@lru_cache(maxsize=65536)
def data_sim(raw):
    if not re.fullmatch(r"[0-9]{7,8}", raw):
        return None
    d = raw.zfill(8)
    try:
        return date(int(d[4:]), int(d[2:4]), int(d[:2]))
    except ValueError:
        return None


def contar(tabela, chave, valores):
    linha = tabela[chave]
    for i, valor in enumerate(valores):
        linha[i] += valor


def tabela_vetores(n):
    return defaultdict(lambda: [0] * n)


def gravar(stage, nome, colunas, tabela):
    salvar(stage / (nome + ".csv"), colunas,
           ((*k, *v) if isinstance(v, list) else (*k, v) for k, v in sorted(tabela.items())))


def analisar(stream, ano, stage):
    reader = csv.DictReader(io.TextIOWrapper(stream, encoding="latin1", newline=""), delimiter=";")
    esquema = reader.fieldnames
    reader.fieldnames = [c.strip().upper() for c in esquema]
    disponiveis = set(reader.fieldnames)
    obrigatorios = set(LINHAS + "TIPOBITO DTOBITO CODMUNRES CAUSABAS CAUSABAS_O CB_PRE ATESTADO DTCADASTRO ALTCAUSA VERSAOSCB VERSAOSIST".split())
    if len(disponiveis) != len(esquema) or obrigatorios - disponiveis:
        raise ValueError("Esquema incompatível com as três edições do protocolo")
    campos = [c for c in EXAMINAR if c in disponiveis]
    mensal = tabela_vetores(len(MEDIDAS))
    processos = tabela_vetores(6)
    preenchidos, categorias, pares, subcategorias, qa = (Counter() for _ in range(5))
    for raw in reader:
        if None in raw or any(raw[c] is None for c in campos):
            raise ValueError("Largura do registro incompatível")
        qa["origem"] += 1
        if raw["TIPOBITO"].strip() != "2":
            qa["tipo_excluido"] += 1
            continue
        data = data_sim(raw["DTOBITO"].strip())
        if data is None or data.year != ano:
            qa["data_invalida" if data is None else "outro_ano"] += 1
            continue
        uf = UFS.get(raw["CODMUNRES"].strip()[:2])
        if uf is None:
            qa["sem_UF_brasileira"] += 1
            continue
        qa["elegiveis"] += 1
        mes = data.month
        final, original, pre = (normalizar(raw[c]) for c in ("CAUSABAS", "CAUSABAS_O", "CB_PRE"))
        bas, orig, antes = (c.startswith("I50") for c in (final, original, pre))
        circ = final.startswith("I") and final != "INVALIDA"
        atestado = raw["ATESTADO"]
        mencao = bool(I50_NO_TEXTO.search(atestado))
        nas_linhas = any(I50_NO_TEXTO.search(raw[c]) for c in LINHAS)
        original_valida = original not in ("AUSENTE", "INVALIDA")
        valores = (1, circ, bas, orig, antes, mencao, nas_linhas, mencao or nas_linhas,
                   bool(CID_NO_TEXTO.search(atestado)), bas and mencao, bas and original_valida, original_valida)
        contar(mensal, (ano, mes, uf), valores)
        for campo in campos:
            if raw[campo].strip():
                preenchidos[uf, campo] += 1
        # Categorias exatas ficam disponíveis inclusive para destinos fora do capítulo I.
        categorias[ano, mes, uf, final[:3] if final not in ("AUSENTE", "INVALIDA") else final] += 1
        if bas:
            subcategorias[ano, mes, uf, final] += 1
        if bas or orig or antes or mencao or nas_linhas:
            pares[ano, mes, uf, original, pre, final, int(mencao), int(nas_linhas)] += 1
        cadastro = data_sim(raw["DTCADASTRO"].strip())
        periodo = cadastro.isoformat()[:7] if cadastro else "SEM_DATA_VALIDA"
        scb = raw["VERSAOSCB"].strip().replace(",", ".") or "SEM_VALOR"
        sistema = raw["VERSAOSIST"].strip() or "SEM_VALOR"
        alt = raw["ALTCAUSA"].strip() or "SEM_VALOR"
        contar(processos, (ano, mes, uf, periodo, scb, sistema, alt),
               (1, circ, bas, orig, antes, mencao))
    for uf in UFS.values():
        for mes in range(1, 13):
            mensal[ano, mes, uf]
    if sum(v[0] for v in mensal.values()) != qa["elegiveis"] or sum(categorias.values()) != qa["elegiveis"]:
        raise ValueError("Balanço de elegibilidade divergente")
    if qa["origem"] != sum(v for k, v in qa.items() if k != "origem"):
        raise ValueError("Balanço de exclusões divergente")
    gravar(stage, "mensal", ["ano", "mes", "uf", *MEDIDAS], mensal)
    gravar(stage, "processamento", ["ano", "mes", "uf", "cadastro", "scb", "sistema", "altcausa", *MEDIDAS[:6]], processos)
    gravar(stage, "categorias", ["ano", "mes", "uf", "categoria", "n"], categorias)
    gravar(stage, "subcategorias", ["ano", "mes", "uf", "cid", "n"], subcategorias)
    gravar(stage, "matriz", "ano mes uf original pre selecionada mencao_atestado mencao_linhas n".split(), pares)
    salvar(stage / "preenchimento.csv", "ano uf campo presente preenchidos elegiveis".split(),
           ((ano, uf, c, int(c in disponiveis), preenchidos[uf, c] if c in disponiveis else None,
             sum(mensal[ano, m, uf][0] for m in range(1, 13))) for uf in sorted(UFS.values()) for c in EXAMINAR))
    return dict(qa=qa, esquema=esquema)


def processar(ano, arquivo, destino):
    ed = next(r for r in ler(sim.FONTES) if int(r["ano"]) == ano)
    if arquivo.stat().st_size != int(ed["bytes"]) or sha256_arquivo(arquivo) != ed["sha256"]:
        raise ValueError("ZIP divergente do manifesto")

    def medir(stage):
        with ZipFile(arquivo) as z:
            if z.namelist() != [ed["membro"]]:
                raise ValueError("Membro divergente")
            with z.open(ed["membro"]) as stream:
                return analisar(stream, ano, stage)
    return executar(destino, {"zip": arquivo, "edicoes": sim.FONTES}, {"ano": ano}, medir, [Path(sim.__file__)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ano", type=int, choices=(2022, 2023, 2024))
    parser.add_argument("zip", type=Path)
    parser.add_argument("destino", type=Path)
    args = parser.parse_args()
    print(processar(args.ano, args.zip, args.destino)["controles"]["qa"])

