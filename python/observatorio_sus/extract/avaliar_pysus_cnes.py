#!/usr/bin/env python
"""CLI de diagnóstico controlado para avaliar viabilidade PySUS/CNES."""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import pkgutil
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from observatorio_sus.utils.normalizacao import normalizar_competencia

KEYWORDS_CNES = ("cnes", "estabele")
KEYWORDS_UF = ("uf", "state", "estado")
KEYWORDS_COMP = ("compet", "month", "period")
KEYWORDS_DF = ("dataframe", "pandas", "parquet", "to_parquet", "to_pandas")
KEYWORDS_REL = ("rl", "rel", "join", "relationship", "vinc", "vinculo")
KEYWORDS_IO = ("download", "list", "fetch", "get", "ftp", "datasus")


def _safe_signature(obj: Any) -> str:
    try:
        return str(inspect.signature(obj))
    except Exception:
        return "assinatura_não_disponível"


def _classificar_objeto(nome: str) -> dict[str, Any]:
    baixo = nome.lower()
    return {
        "nome": nome,
        "suporte_uf": any(k in baixo for k in KEYWORDS_UF),
        "suporte_competencia": any(k in baixo for k in KEYWORDS_COMP),
        "retorno_df_parquet": any(k in baixo for k in KEYWORDS_DF),
        "relacional": any(k in baixo for k in KEYWORDS_REL),
        "download_listagem": any(k in baixo for k in KEYWORDS_IO),
    }


def executar_diagnostico(uf: str, competencia: str, modo: str) -> int:
    resultado: dict[str, Any] = {
        "modo": modo,
        "parametros": {"uf": uf, "competencia": competencia},
        "ambiente": {
            "python_version": sys.version,
            "python_executavel": sys.executable,
        },
        "pysus": {
            "importado": False,
            "versao": "não confirmado nesta POC",
            "path_pacote": "não confirmado nesta POC",
        },
        "evidencias": {
            "api_publica_aparente": [],
            "modulos_internos_relacionados": [],
            "interfaces_download_listagem": [],
            "objetos_relacionados_cnes": [],
            "evidencias_colunas_chave": [],
            "evidencias_suporte_uf": [],
            "evidencias_suporte_competencia": [],
            "evidencias_dataframe_parquet": [],
            "evidencias_tabelas_relacionais": [],
        },
        "modulos_ignorados_tests": [],
        "execucao_controlada": {
            "tentativa": "não",
            "status": "não executado",
            "motivo": "não foi identificada API CNES pública inequívoca com recorte estrito e seguro",
            "download_massivo": "não executado por risco de download inadequado",
        },
        "observacoes": [],
    }

    with tempfile.TemporaryDirectory(prefix="poc_pysus2_cnes_") as _tmp:
        try:
            pysus = importlib.import_module("pysus")
            resultado["pysus"]["importado"] = True
            resultado["pysus"]["versao"] = getattr(pysus, "__version__", "sem __version__")
            resultado["pysus"]["path_pacote"] = str(getattr(pysus, "__file__", "sem __file__"))
        except Exception as exc:
            resultado["observacoes"].append(f"Falha ao importar pysus: {exc}")
            print(json.dumps(resultado, ensure_ascii=False, indent=2))
            return 0

        candidatos: list[str] = []
        for m in pkgutil.walk_packages(pysus.__path__, prefix="pysus."):
            nome = m.name
            if ".tests" in nome:
                resultado["modulos_ignorados_tests"].append(nome)
                continue
            baixo = nome.lower()
            if any(k in baixo for k in ["cnes", "datasus", "ftp", "sih", "sia", "sim"]):
                candidatos.append(nome)

        resultado["evidencias"]["modulos_internos_relacionados"] = sorted(set(candidatos))

        for nome_modulo in resultado["evidencias"]["modulos_internos_relacionados"]:
            try:
                mod = importlib.import_module(nome_modulo)
            except Exception as exc:
                resultado["observacoes"].append(f"Erro ao importar módulo {nome_modulo}: {exc}")
                continue

            if any(seg in nome_modulo.lower() for seg in ["api", "interface", "client"]):
                resultado["evidencias"]["api_publica_aparente"].append(nome_modulo)

            objetos = [x for x in dir(mod) if not x.startswith("_")]
            for obj_nome in objetos:
                baixo = obj_nome.lower()
                full = f"{nome_modulo}.{obj_nome}"
                if any(k in baixo for k in KEYWORDS_CNES):
                    classif = _classificar_objeto(full)
                    try:
                        attr = getattr(mod, obj_nome)
                        classif["assinatura"] = _safe_signature(attr) if callable(attr) else "não_aplicável"
                    except Exception:
                        classif["assinatura"] = "indisponível"
                    resultado["evidencias"]["objetos_relacionados_cnes"].append(classif)

                if any(k in baixo for k in KEYWORDS_IO):
                    resultado["evidencias"]["interfaces_download_listagem"].append(full)
                if any(k in baixo for k in KEYWORDS_UF):
                    resultado["evidencias"]["evidencias_suporte_uf"].append(full)
                if any(k in baixo for k in KEYWORDS_COMP):
                    resultado["evidencias"]["evidencias_suporte_competencia"].append(full)
                if any(k in baixo for k in KEYWORDS_DF):
                    resultado["evidencias"]["evidencias_dataframe_parquet"].append(full)
                if any(k in baixo for k in KEYWORDS_REL):
                    resultado["evidencias"]["evidencias_tabelas_relacionais"].append(full)
                if any(k in baixo for k in ["co_unidade", "co_cnes", "tbestabelecimento", "tbmunicipio", "rlestabsipac", "tbsubgruposhabilitacao", "estabele", "unidade", "habilitacao", "habilitação"]):
                    resultado["evidencias"]["evidencias_colunas_chave"].append(full)

        for k in resultado["evidencias"]:
            if isinstance(resultado["evidencias"][k], list):
                # unique mantendo ordem
                seen = set()
                uniq = []
                for item in resultado["evidencias"][k]:
                    marker = json.dumps(item, sort_keys=True, ensure_ascii=False) if isinstance(item, dict) else str(item)
                    if marker not in seen:
                        seen.add(marker)
                        uniq.append(item)
                resultado["evidencias"][k] = uniq

        if resultado["evidencias"]["objetos_relacionados_cnes"]:
            resultado["execucao_controlada"]["tentativa"] = "não"
            resultado["execucao_controlada"]["status"] = "não executado"
            resultado["execucao_controlada"]["motivo"] = (
                "API potencial identificada por inspeção, mas sem garantia de recorte estrito UF/competência "
                "e com risco de download amplo; chamada real abortada preventivamente"
            )

        resultado["observacoes"].append(
            "Diagnóstico concluído sem downloads de dados CNES; inspeção estática e segura apenas."
        )

    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnóstico controlado de cobertura PySUS 2.x para CNES")
    parser.add_argument("--uf", default="ES")
    parser.add_argument("--competencia", default="202601")
    parser.add_argument("--modo", default="diagnostico")
    args = parser.parse_args()
    try:
        comp = normalizar_competencia(args.competencia)
        return executar_diagnostico(args.uf.upper(), comp, args.modo)
    except Exception as exc:
        print(f"ERRO_INESPERADO: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
