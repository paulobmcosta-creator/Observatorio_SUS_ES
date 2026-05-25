"""Etapa 5D: descoberta operacional de arquivos CNES sem extração analítica."""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import os
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from observatorio_sus.cnes.contratos import listar_tabelas_obrigatorias, obter_contrato_tabela

TABELAS_PRIORITARIAS = [
    "tbEstabelecimento",
    "tbMunicipio",
    "rlEstabSipac",
    "tbSubGruposHabilitacao",
]


def _base(competencia: str, modo: str) -> dict:
    contratos = {t: obter_contrato_tabela(t) for t in TABELAS_PRIORITARIAS}
    return {
        "ambiente": {
            "python": sys.version.split()[0],
            "plataforma": platform.platform(),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "cwd": str(Path.cwd()),
        },
        "parametros": {"competencia": competencia, "modo": modo},
        "competencia": competencia,
        "tabelas_prioritarias": TABELAS_PRIORITARIAS,
        "contratos_usados": {
            "listar_tabelas_obrigatorias": listar_tabelas_obrigatorias(),
            "obter_contrato_tabela": contratos,
        },
        "fontes_investigadas": [],
        "modulos_pysus_relevantes": [],
        "diretorios_candidatos": [],
        "arquivos_candidatos": [],
        "padroes_nome_detectados": [],
        "tamanhos_detectados": {},
        "extensoes_detectadas": [],
        "relacao_arquivo_tabela": {},
        "risco_download": "BAIXO_NO_PLANEJAMENTO",
        "conclusao": "",
        "proxima_recomendacao": "",
    }


def _classificar(cand: str | None, tamanho: int | None, competencia: str) -> str:
    if cand and competencia in cand and tamanho is not None:
        return "ARQUIVO_IDENTIFICADO"
    if cand:
        return "CANDIDATO_IDENTIFICADO"
    return "NAO_IDENTIFICADO"


def _planejamento(rel: dict) -> dict:
    rel["fontes_investigadas"] = ["planejamento_offline_sem_rede"]
    rel["conclusao"] = "Etapa 5D em modo de planejamento sem rede e sem download de dados."
    rel["proxima_recomendacao"] = "Executar inspecao_local e, se seguro, listar_remoto apenas para metadados."
    for t in TABELAS_PRIORITARIAS:
        rel["relacao_arquivo_tabela"][t] = {
            "classificacao": "LISTAGEM_NAO_EXECUTADA_POR_SEGURANCA",
            "arquivo_candidato": None,
            "fonte": "planejamento",
            "observacao": "Sem rede; descoberta limitada ao plano operacional.",
        }
    return rel


def _inspecao_local(rel: dict) -> dict:
    rel["fontes_investigadas"].append("inspecao_local_pysus")
    pysus_spec = importlib.util.find_spec("pysus")
    if pysus_spec is None:
        rel["modulos_pysus_relevantes"].append({"modulo": "pysus", "status": "nao_instalado"})
        for t in TABELAS_PRIORITARIAS:
            rel["relacao_arquivo_tabela"][t] = {
                "classificacao": "LISTAGEM_INCONCLUSIVA",
                "arquivo_candidato": None,
                "fonte": "inspecao_local",
                "observacao": "PySUS não instalado para inspeção local.",
            }
        rel["conclusao"] = "Inspeção local inconclusiva por ausência de PySUS."
        rel["proxima_recomendacao"] = "Instalar/inspecionar PySUS em ambiente controlado e repetir inspeção local."
        return rel

    rel["modulos_pysus_relevantes"].append({"modulo": "pysus", "status": "instalado"})
    candidatos = ["pysus", "pysus.ftp", "pysus.online_data", "pysus.online_data.CNES"]
    for m in candidatos:
        try:
            spec = importlib.util.find_spec(m)
            rel["modulos_pysus_relevantes"].append({"modulo": m, "encontrado": spec is not None})
        except Exception as exc:
            rel["modulos_pysus_relevantes"].append({"modulo": m, "erro": str(exc)})
    rel["conclusao"] = "Inspeção local executada sem rede; sem descoberta de arquivo remoto nesta etapa."
    rel["proxima_recomendacao"] = "Executar listar_remoto com proteção de segurança para metadados de tamanho."
    for t in TABELAS_PRIORITARIAS:
        rel["relacao_arquivo_tabela"][t] = {
            "classificacao": "LISTAGEM_INCONCLUSIVA",
            "arquivo_candidato": None,
            "fonte": "inspecao_local",
            "observacao": "Mapeamento local de módulos feito; arquivo remoto não confirmado.",
        }
    return rel


def _listar_remoto(rel: dict) -> dict:
    competencia = rel["competencia"]
    base = "https://ftp.datasus.gov.br/dissemin/publicos/CNES"
    rel["fontes_investigadas"].append(base)
    rel["diretorios_candidatos"] = [f"{base}/200508_/Dados"]
    mapa = {
        "tbEstabelecimento": f"tbEstabelecimento{competencia}.dbc",
        "tbMunicipio": f"tbMunicipio{competencia}.dbc",
        "rlEstabSipac": f"rlEstabSipac{competencia}.dbc",
        "tbSubGruposHabilitacao": f"tbSubGruposHabilitacao{competencia}.dbc",
    }
    extensoes = set()
    for tabela, nome in mapa.items():
        url = f"{base}/200508_/Dados/{nome}"
        tamanho = None
        obs = []
        try:
            req = Request(url, method="HEAD")
            with urlopen(req, timeout=10) as resp:
                cl = resp.headers.get("Content-Length")
                if cl and cl.isdigit():
                    tamanho = int(cl)
                    rel["tamanhos_detectados"][nome] = tamanho
        except (HTTPError, URLError, TimeoutError) as exc:
            obs.append(f"HEAD indisponível: {exc}")
        classificacao = _classificar(url, tamanho, competencia)
        rel["arquivos_candidatos"].append({"tabela": tabela, "arquivo": nome, "url": url})
        rel["relacao_arquivo_tabela"][tabela] = {
            "classificacao": classificacao,
            "arquivo_candidato": url,
            "fonte": "listar_remoto",
            "observacao": "; ".join(obs) if obs else "Metadado de tamanho consultado por HEAD sem download de conteúdo.",
        }
        extensoes.add(Path(nome).suffix.lower())
    rel["padroes_nome_detectados"] = [r"^(tb|rl)[A-Za-z]+\d{6}\.dbc$"]
    rel["extensoes_detectadas"] = sorted(extensoes)
    rel["risco_download"] = "MODERADO_CONTROLADO_SEM_GET_CORPO"
    rel["conclusao"] = "Listagem remota limitada a metadados de nomes/caminhos/tamanho via HEAD."
    rel["proxima_recomendacao"] = "Com candidatos e tamanhos conhecidos, submeter deliberação humana para eventual nova Etapa 5P."
    return rel


def _resumo(rel: dict) -> dict:
    rel["fontes_investigadas"] = ["resumo_offline"]
    rel["conclusao"] = "Resumo offline da Etapa 5D sem rede e sem extração analítica."
    rel["proxima_recomendacao"] = "Consolidar matriz de candidatos antes de qualquer download temporário."
    for t in TABELAS_PRIORITARIAS:
        rel["relacao_arquivo_tabela"][t] = {
            "classificacao": "LISTAGEM_NAO_EXECUTADA_POR_SEGURANCA",
            "arquivo_candidato": None,
            "fonte": "resumo",
            "observacao": "Resumo não executa inspeção remota.",
        }
    return rel


def main() -> int:
    parser = argparse.ArgumentParser(description="Descoberta operacional de arquivos CNES (Etapa 5D).")
    parser.add_argument("--competencia", default="202501")
    parser.add_argument("--modo", default="planejamento", choices=["planejamento", "inspecao_local", "listar_remoto", "resumo"])
    args = parser.parse_args()

    rel = _base(args.competencia, args.modo)
    if args.modo == "planejamento":
        rel = _planejamento(rel)
    elif args.modo == "inspecao_local":
        rel = _inspecao_local(rel)
    elif args.modo == "listar_remoto":
        rel = _listar_remoto(rel)
    else:
        rel = _resumo(rel)

    print(json.dumps(rel, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
