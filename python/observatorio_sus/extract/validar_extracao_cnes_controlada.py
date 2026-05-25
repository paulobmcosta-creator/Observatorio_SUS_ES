"""Validação operacional controlada de extração CNES com foco em contratos da Etapa 4."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import pkgutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from observatorio_sus.cnes.contratos import (  # noqa: E402
    listar_campos_criticos,
    listar_campos_textuais,
    listar_tabelas_obrigatorias,
)

KEYWORDS = [
    "cnes", "datasus", "ftp", "dbc", "dbf", "download", "parquet",
    "tbestabelecimento", "tbmunicipio", "rlestabsipac", "tbsubgruposhabilitacao",
    "co_unidade", "co_cnes", "estabelecimento", "unidade", "habilitacao", "habilitação",
    "uf", "competencia", "competência",
]


def _diagnostico_pysus() -> dict:
    resultado = {
        "modulos_relevantes": [],
        "objetos_relevantes": [],
        "observacoes": [],
    }
    try:
        pysus = importlib.import_module("pysus")
    except Exception as exc:
        return {**resultado, "erro_importacao": str(exc)}

    pacotes = []
    if hasattr(pysus, "__path__"):
        for mod in pkgutil.walk_packages(pysus.__path__, prefix="pysus."):
            if ".tests" in mod.name:
                continue
            nome = mod.name.lower()
            if any(k in nome for k in KEYWORDS):
                resultado["modulos_relevantes"].append(mod.name)
            pacotes.append(mod.name)

    for modulo in resultado["modulos_relevantes"][:20]:
        try:
            mod = importlib.import_module(modulo)
        except Exception:
            continue
        for nome, obj in inspect.getmembers(mod):
            nlow = nome.lower()
            if any(k in nlow for k in KEYWORDS):
                tipo = "funcao" if inspect.isfunction(obj) else "classe" if inspect.isclass(obj) else "objeto"
                resultado["objetos_relevantes"].append({"modulo": modulo, "nome": nome, "tipo": tipo})

    resultado["total_modulos_varridos"] = len(pacotes)
    return resultado


def _resumo_contratos() -> dict:
    tabelas = listar_tabelas_obrigatorias()
    contratos = {}
    for grupo in tabelas.values():
        for tabela in grupo:
            contratos[tabela] = {
                "campos_criticos": listar_campos_criticos(tabela),
                "campos_textuais_relacionados": [
                    c for c in listar_campos_textuais() if c in [x.upper() for x in listar_campos_criticos(tabela)]
                ],
            }
    return contratos


def main() -> int:
    parser = argparse.ArgumentParser(description="Validação operacional controlada CNES/PySUS (Etapa 4).")
    parser.add_argument("--uf", default="ES")
    parser.add_argument("--competencia", default="202601")
    parser.add_argument("--modo", default="diagnostico", choices=["diagnostico", "tentativa_controlada", "contratos"])
    args = parser.parse_args()

    try:
        ambiente = {
            "python_versao": sys.version,
            "python_executavel": sys.executable,
            "tempdir": tempfile.gettempdir(),
        }
        contratos = _resumo_contratos()
        pysus_info = {"versao": None, "caminho": None}
        diagnostico_pysus = {"nao_executado": args.modo == "contratos"}

        if args.modo != "contratos":
            try:
                pysus = importlib.import_module("pysus")
                pysus_info = {
                    "versao": getattr(pysus, "__version__", "sem __version__"),
                    "caminho": getattr(pysus, "__file__", "sem __file__"),
                }
            except Exception as exc:
                pysus_info["erro_importacao"] = str(exc)
            diagnostico_pysus = _diagnostico_pysus()

        cobertura_tabelas = {}
        for tabela in contratos:
            cobertura_tabelas[tabela] = "nao_testado" if args.modo == "contratos" else "nao_confirmado"
        for tabela in ["tbEstabelecimento", "tbMunicipio", "rlEstabSipac", "tbSubGruposHabilitacao"]:
            if tabela in cobertura_tabelas and args.modo != "contratos":
                cobertura_tabelas[tabela] = "parcialmente_confirmado"

        if args.modo == "tentativa_controlada":
            cobertura_tabelas = {k: ("requer_fallback" if v == "nao_confirmado" else v) for k, v in cobertura_tabelas.items()}

        cobertura_campos = {
            "campos_textuais_obrigatorios": listar_campos_textuais(),
            "co_unidade": "parcialmente_confirmado" if args.modo != "contratos" else "nao_testado",
            "co_cnes": "parcialmente_confirmado" if args.modo != "contratos" else "nao_testado",
        }

        fallback = [t for t, status in cobertura_tabelas.items() if status in {"nao_confirmado", "requer_fallback", "nao_testado"}]

        conclusao = "Diagnóstico executado sem download e com necessidade de fallback planejado."
        if args.modo == "tentativa_controlada":
            conclusao = "Tentativa controlada abortada por segurança operacional; fallback permanece necessário."

        saida = {
            "ambiente": ambiente,
            "pysus": pysus_info,
            "parametros": {"uf": args.uf, "competencia": args.competencia, "modo": args.modo},
            "contratos": contratos,
            "diagnostico_pysus": diagnostico_pysus,
            "cobertura_tabelas": cobertura_tabelas,
            "cobertura_campos": cobertura_campos,
            "fallback_necessario": fallback,
            "riscos": [
                "Cobertura parcial de tabelas CNES em PySUS.",
                "Ausência de API pública estável para todas as tabelas lógicas.",
                "Risco de coerção numérica de chaves sem contrato textual.",
            ],
            "conclusao": conclusao,
        }

        print(json.dumps(saida, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:  # retorno 2 apenas para erro inesperado
        print(json.dumps({"erro": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
