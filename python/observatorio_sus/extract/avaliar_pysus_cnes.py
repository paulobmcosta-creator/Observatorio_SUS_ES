#!/usr/bin/env python
"""CLI de diagnóstico controlado para avaliar viabilidade PySUS/CNES."""

from __future__ import annotations

import argparse
import importlib
import json
import pkgutil
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from observatorio_sus.utils.normalizacao import normalizar_competencia

KEYWORDS = ("cnes", "estabele", "uf", "compet", "month", "state")

def _buscar_objetos_relacionados(modulo: Any) -> list[str]:
    return sorted([n for n in dir(modulo) if any(k in n.lower() for k in KEYWORDS)])

def executar_diagnostico(uf: str, competencia: str, modo: str) -> int:
    resultado: dict[str, Any] = {
        "modo": modo, "uf": uf, "competencia": competencia,
        "pysus_importado": False, "versao_pysus": "não confirmado nesta POC",
        "modulos_relacionados_cnes": [],
        "suporte_uf_aparente": "não confirmado nesta POC",
        "suporte_competencia_aparente": "não confirmado nesta POC",
        "retorno_dataframe_aparente": "não confirmado nesta POC",
        "coluna_co_unidade_aparente": "não confirmado nesta POC",
        "coluna_co_cnes_aparente": "não confirmado nesta POC",
        "tabelas_relacionais_aparentes": "não confirmado nesta POC",
        "risco_conversao_numerica_codigos": "não confirmado nesta POC",
        "observacoes": [],
    }
    with tempfile.TemporaryDirectory(prefix="poc_pysus_cnes_"):
        try:
            pysus = importlib.import_module("pysus")
            resultado["pysus_importado"] = True
            resultado["versao_pysus"] = getattr(pysus, "__version__", "não confirmado nesta POC")
        except Exception as exc:
            resultado["observacoes"].append(f"Falha ao importar pysus: {exc}")
            print(json.dumps(resultado, ensure_ascii=False, indent=2))
            return 0

        candidatos = []
        for m in pkgutil.walk_packages(pysus.__path__, prefix="pysus."):
            if re.search(r"cnes|estabele", m.name, re.IGNORECASE):
                candidatos.append(m.name)
        resultado["modulos_relacionados_cnes"] = sorted(set(candidatos))

        objetos = []
        for nome_modulo in resultado["modulos_relacionados_cnes"][:15]:
            try:
                mod = importlib.import_module(nome_modulo)
                objetos.extend([f"{nome_modulo}.{x}" for x in _buscar_objetos_relacionados(mod)])
            except Exception as exc:
                resultado["observacoes"].append(f"Erro ao importar {nome_modulo}: {exc}")

        if objetos:
            txt = " ".join(objetos).lower()
            resultado["suporte_uf_aparente"] = "sim" if "uf" in txt or "state" in txt else "não confirmado nesta POC"
            resultado["suporte_competencia_aparente"] = "sim" if "compet" in txt or "month" in txt else "não confirmado nesta POC"
            resultado["tabelas_relacionais_aparentes"] = "possível" if any("rl" in x.lower() for x in objetos) else "não confirmado nesta POC"
            resultado["risco_conversao_numerica_codigos"] = "sim, se leitura sem dtype textual (inferência)"
        else:
            resultado["observacoes"].append("Nenhum objeto CNES inequívoco identificado sem download potencialmente massivo.")

        resultado["observacoes"].append("POC não executa downloads massivos; apenas inspeção controlada de interfaces.")

    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(description="Diagnóstico controlado de cobertura PySUS para CNES")
    parser.add_argument("--uf", default="ES")
    parser.add_argument("--competencia", default="202601")
    parser.add_argument("--modo", default="diagnostico")
    args = parser.parse_args()
    try:
        return executar_diagnostico(args.uf.upper(), normalizar_competencia(args.competencia), args.modo)
    except Exception as exc:
        print(f"ERRO_INESPERADO: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
