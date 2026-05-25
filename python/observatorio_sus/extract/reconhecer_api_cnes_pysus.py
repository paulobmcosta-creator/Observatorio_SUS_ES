#!/usr/bin/env python3
"""Reconhecimento mínimo da API CNES do PySUS sem persistência de dados."""

from __future__ import annotations

import argparse
import inspect
import json
import platform
import sys
from datetime import datetime, timezone
from typing import Any

GRUPOS_PADRAO = ["ST", "LT", "SR"]


def _base_payload(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "ambiente": {
            "python_versao": sys.version,
            "executavel": sys.executable,
            "plataforma": platform.platform(),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        },
        "parametros": {
            "modo": args.modo,
            "uf": args.uf,
            "ano": args.ano,
            "mes": args.mes,
            "grupo": args.grupo,
        },
        "api_pysus": {
            "import_cnes_ok": False,
            "assinatura": None,
            "pysus_versao": None,
            "pysus_path": None,
        },
        "grupos_planejados": GRUPOS_PADRAO,
        "chamada_piloto": {
            "executada": False,
            "sucesso": False,
            "tipo_objeto": None,
            "linhas": None,
            "colunas": None,
            "persistencia_realizada": False,
        },
        "colunas_retornadas": [],
        "campos_chave_detectados": {
            "unidade": [],
            "co_unidade": [],
            "cnes": [],
            "co_cnes": [],
            "municipio": [],
            "uf": [],
        },
        "erros_controlados": [],
        "conclusao": "",
        "proxima_recomendacao": "",
    }


def _detectar_campos(colunas: list[str]) -> dict[str, list[str]]:
    chaves = ["unidade", "co_unidade", "cnes", "co_cnes", "municipio", "uf"]
    resultado = {k: [] for k in chaves}
    for coluna in colunas:
        nome = coluna.lower()
        for chave in chaves:
            if chave in nome:
                resultado[chave].append(coluna)
    return resultado


def _importar_cnes(payload: dict[str, Any]) -> Any | None:
    try:
        from pysus import cnes  # type: ignore
        import pysus  # type: ignore

        payload["api_pysus"]["import_cnes_ok"] = True
        payload["api_pysus"]["pysus_versao"] = getattr(pysus, "__version__", "sem __version__")
        payload["api_pysus"]["pysus_path"] = getattr(pysus, "__file__", "sem __file__")
        try:
            payload["api_pysus"]["assinatura"] = str(inspect.signature(cnes))
        except Exception as exc:  # pragma: no cover
            payload["erros_controlados"].append(f"Nao foi possivel inspecionar assinatura: {exc}")
        return cnes
    except Exception as exc:
        payload["erros_controlados"].append(f"Falha ao importar 'from pysus import cnes': {exc}")
        return None


def executar(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    payload = _base_payload(args)

    if args.modo in {"inspecao_api", "chamada_piloto"}:
        func_cnes = _importar_cnes(payload)
    else:
        func_cnes = None

    if args.modo == "planejamento":
        payload["conclusao"] = "Planejamento concluido sem acesso a rede e sem chamada de download."
        payload["proxima_recomendacao"] = "Executar modo inspecao_api e, se disponivel, chamada_piloto ST/ES/2024-01."
        return 0, payload

    if args.modo == "resumo":
        payload["conclusao"] = "Resumo emitido sem rede; trilha 5N focada em reconhecimento da API do PySUS."
        payload["proxima_recomendacao"] = "Prosseguir com mapeamento de colunas por grupo na etapa 5N.1."
        return 0, payload

    if args.modo == "inspecao_api":
        if payload["api_pysus"]["import_cnes_ok"]:
            payload["conclusao"] = "Importacao da API funcional do PySUS confirmada."
            payload["proxima_recomendacao"] = "Executar chamada_piloto controlada sem persistencia."
        else:
            payload["conclusao"] = "API do PySUS indisponivel neste ambiente."
            payload["proxima_recomendacao"] = "Verificar instalacao/versao do pysus."
        return 0, payload

    if args.modo == "chamada_piloto":
        payload["chamada_piloto"]["executada"] = True
        if func_cnes is None:
            payload["conclusao"] = "Chamada piloto nao executada por indisponibilidade de importacao da API."
            payload["proxima_recomendacao"] = "Investigar versao/API do pysus no ambiente com conectividade."
            return 0, payload

        try:
            resultado = func_cnes(state=args.uf, year=args.ano, month=args.mes, group=args.grupo)
            payload["chamada_piloto"]["sucesso"] = True
            payload["chamada_piloto"]["tipo_objeto"] = type(resultado).__name__

            linhas = getattr(resultado, "shape", (None, None))[0]
            colunas_n = getattr(resultado, "shape", (None, None))[1]
            payload["chamada_piloto"]["linhas"] = int(linhas) if isinstance(linhas, int) else linhas
            payload["chamada_piloto"]["colunas"] = int(colunas_n) if isinstance(colunas_n, int) else colunas_n

            colunas = [str(c) for c in list(getattr(resultado, "columns", []))]
            payload["colunas_retornadas"] = colunas
            payload["campos_chave_detectados"] = _detectar_campos(colunas)
            payload["conclusao"] = "Chamada piloto executada sem persistencia local."
            payload["proxima_recomendacao"] = "Se mantido sucesso, iniciar etapa 5N.1 para mapear ST/LT/SR."
        except Exception as exc:
            payload["erros_controlados"].append(f"Falha operacional em chamada_piloto: {exc}")
            payload["conclusao"] = "Chamada piloto falhou de forma controlada (rede/API)."
            payload["proxima_recomendacao"] = "Repetir em ambiente com conectividade ou revisar compatibilidade da API."
        return 0, payload

    payload["erros_controlados"].append(f"Modo invalido: {args.modo}")
    payload["conclusao"] = "Erro de uso do CLI."
    payload["proxima_recomendacao"] = "Use --help para modos validos."
    return 2, payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconhece a API CNES do PySUS sem persistir dados.")
    parser.add_argument("--modo", default="planejamento", choices=["planejamento", "inspecao_api", "chamada_piloto", "resumo"])
    parser.add_argument("--uf", default="ES")
    parser.add_argument("--ano", type=int, default=2024)
    parser.add_argument("--mes", type=int, default=1)
    parser.add_argument("--grupo", default="ST")
    return parser.parse_args()


if __name__ == "__main__":
    try:
        codigo, saida = executar(parse_args())
        print(json.dumps(saida, ensure_ascii=False, indent=2))
        raise SystemExit(codigo)
    except SystemExit:
        raise
    except Exception as exc:  # pragma: no cover
        erro = {
            "erros_controlados": [f"Erro inesperado: {exc}"],
            "conclusao": "Erro inesperado no script.",
        }
        print(json.dumps(erro, ensure_ascii=False, indent=2))
        raise SystemExit(2)
