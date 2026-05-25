#!/usr/bin/env python3
from __future__ import annotations

import argparse
import inspect
import json
import os
import platform
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GRUPOS = ["ST", "LT", "SR"]
CLASSIFICACOES = {
    "ok": "ISOLAMENTO_RESOLVEU_LOCK_E_CHAMADA_FUNCIONOU",
    "outro_erro": "ISOLAMENTO_RESOLVEU_LOCK_MAS_CHAMADA_FALHOU_POR_OUTRO_MOTIVO",
    "lock": "ISOLAMENTO_NAO_RESOLVEU_LOCK",
    "inconclusivo": "ISOLAMENTO_INCONCLUSIVO",
    "nao_executada": "CHAMADA_NAO_EXECUTADA",
}


def base(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "ambiente": {
            "python_versao": platform.python_version(),
            "plataforma": platform.platform(),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        },
        "parametros": {"modo": args.modo, "uf": args.uf, "ano": args.ano, "mes": args.mes, "grupo": args.grupo},
        "isolamento": {
            "home_original": os.environ.get("HOME"),
            "home_temporario": None,
            "xdg_config_home_temporario": None,
            "xdg_cache_home_temporario": None,
            "import_pysus_apos_isolamento": False,
            "root_pysus_usado": None,
            "config_db_temporario_detectado": False,
            "config_db_root_detectado": False,
            "lock_duckdb_ocorreu": False,
        },
        "pysus": {"import_ok": False, "versao": None, "path": None, "assinatura_cnes": None},
        "duckdb": {"erro_lock_detectado": False, "mensagem": None},
        "chamada_piloto": {"executada": False, "sucesso": False, "tipo_objeto": None, "linhas": None, "colunas": None},
        "colunas_retornadas": [],
        "campos_chave_detectados": {"unidade": [], "co_unidade": [], "cnes": [], "co_cnes": [], "municipio": [], "uf": []},
        "arquivos_temporarios": [],
        "erros_controlados": [],
        "conclusao": "",
        "proxima_recomendacao": "",
    }


def detectar_campos(colunas: list[str]) -> dict[str, list[str]]:
    termos = ["unidade", "co_unidade", "cnes", "co_cnes", "municipio", "uf"]
    achados = {t: [] for t in termos}
    for c in colunas:
        low = c.lower()
        for t in termos:
            if t in low:
                achados[t].append(c)
    return achados


def executar(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    out = base(args)

    if args.modo == "planejamento":
        out["conclusao"] = CLASSIFICACOES["nao_executada"]
        out["proxima_recomendacao"] = "Executar inspecao_config e chamada_piloto_isolada com isolamento em tempfile."
        return 0, out

    if args.modo == "resumo":
        out["conclusao"] = CLASSIFICACOES["inconclusivo"]
        out["proxima_recomendacao"] = "Consolidar resultado de isolamento e lock DuckDB."
        return 0, out

    if args.modo == "inspecao_config":
        try:
            import pysus  # type: ignore
            from pysus import cnes  # type: ignore

            out["pysus"]["import_ok"] = True
            out["pysus"]["versao"] = getattr(pysus, "__version__", "sem __version__")
            out["pysus"]["path"] = getattr(pysus, "__file__", "sem __file__")
            out["pysus"]["assinatura_cnes"] = str(inspect.signature(cnes))
        except Exception as exc:
            out["erros_controlados"].append(f"Falha inspecao_config: {exc}")
        out["conclusao"] = CLASSIFICACOES["inconclusivo"]
        out["proxima_recomendacao"] = "Executar chamada_piloto_isolada para validar lock."
        return 0, out

    if args.modo == "chamada_piloto_isolada":
        out["chamada_piloto"]["executada"] = True
        original_home = os.environ.get("HOME")
        original_xdg_conf = os.environ.get("XDG_CONFIG_HOME")
        original_xdg_cache = os.environ.get("XDG_CACHE_HOME")

        with tempfile.TemporaryDirectory(prefix="pysus_isolado_") as td:
            td_path = Path(td)
            home_tmp = td_path / "home"
            xdg_conf_tmp = td_path / "xdg_config"
            xdg_cache_tmp = td_path / "xdg_cache"
            for p in (home_tmp, xdg_conf_tmp, xdg_cache_tmp):
                p.mkdir(parents=True, exist_ok=True)

            os.environ["HOME"] = str(home_tmp)
            os.environ["XDG_CONFIG_HOME"] = str(xdg_conf_tmp)
            os.environ["XDG_CACHE_HOME"] = str(xdg_cache_tmp)
            os.environ["PYSUS_ISOLAMENTO_DIR"] = str(td_path)

            out["isolamento"]["home_temporario"] = str(home_tmp)
            out["isolamento"]["xdg_config_home_temporario"] = str(xdg_conf_tmp)
            out["isolamento"]["xdg_cache_home_temporario"] = str(xdg_cache_tmp)

            try:
                import pysus  # type: ignore
                from pysus import cnes  # type: ignore

                out["isolamento"]["import_pysus_apos_isolamento"] = True
                out["pysus"]["import_ok"] = True
                out["pysus"]["versao"] = getattr(pysus, "__version__", "sem __version__")
                out["pysus"]["path"] = getattr(pysus, "__file__", "sem __file__")
                out["pysus"]["assinatura_cnes"] = str(inspect.signature(cnes))

                try:
                    df = cnes(state=args.uf, year=args.ano, month=args.mes, group=args.grupo)
                    out["chamada_piloto"]["sucesso"] = True
                    out["chamada_piloto"]["tipo_objeto"] = type(df).__name__
                    shape = getattr(df, "shape", (None, None))
                    out["chamada_piloto"]["linhas"] = shape[0]
                    out["chamada_piloto"]["colunas"] = shape[1]
                    cols = [str(c) for c in list(getattr(df, "columns", []))]
                    out["colunas_retornadas"] = cols
                    out["campos_chave_detectados"] = detectar_campos(cols)
                except Exception as exc:
                    msg = str(exc)
                    out["erros_controlados"].append(f"Falha chamada_piloto_isolada: {msg}")
                    out["duckdb"]["mensagem"] = msg
                    lock = "config.db" in msg.lower() and "lock" in msg.lower()
                    out["duckdb"]["erro_lock_detectado"] = lock
                    out["isolamento"]["lock_duckdb_ocorreu"] = lock
            except Exception as exc:
                out["erros_controlados"].append(f"Falha import apos isolamento: {exc}")

            arquivos = [str(p.relative_to(td_path)) for p in td_path.rglob("*") if p.is_file()]
            out["arquivos_temporarios"] = arquivos
            out["isolamento"]["config_db_temporario_detectado"] = any(Path(a).name == "config.db" for a in arquivos)

            root_db = Path("/root/pysus/config.db")
            out["isolamento"]["config_db_root_detectado"] = root_db.exists()
            out["isolamento"]["root_pysus_usado"] = "/root/pysus" if (root_db.exists() and out["duckdb"]["erro_lock_detectado"]) else None

        # restore
        if original_home is not None:
            os.environ["HOME"] = original_home
        if original_xdg_conf is not None:
            os.environ["XDG_CONFIG_HOME"] = original_xdg_conf
        else:
            os.environ.pop("XDG_CONFIG_HOME", None)
        if original_xdg_cache is not None:
            os.environ["XDG_CACHE_HOME"] = original_xdg_cache
        else:
            os.environ.pop("XDG_CACHE_HOME", None)

        if out["chamada_piloto"]["sucesso"]:
            out["conclusao"] = CLASSIFICACOES["ok"]
            out["proxima_recomendacao"] = "Prosseguir para Etapa 5N.2 com mapeamento ST/LT/SR."
        elif out["isolamento"]["lock_duckdb_ocorreu"]:
            out["conclusao"] = CLASSIFICACOES["lock"]
            out["proxima_recomendacao"] = "Investigar configuracao PySUS/DuckDB para suprimir lock em config.db."
        else:
            out["conclusao"] = CLASSIFICACOES["outro_erro"]
            out["proxima_recomendacao"] = "Repetir em ambiente com conectividade e validar erro nao relacionado a lock."
        return 0, out

    out["erros_controlados"].append(f"Modo invalido: {args.modo}")
    out["conclusao"] = CLASSIFICACOES["inconclusivo"]
    out["proxima_recomendacao"] = "Use --help."
    return 2, out


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--modo", default="planejamento", choices=["planejamento", "inspecao_config", "chamada_piloto_isolada", "resumo"])
    p.add_argument("--uf", default="ES")
    p.add_argument("--ano", type=int, default=2024)
    p.add_argument("--mes", type=int, default=1)
    p.add_argument("--grupo", default="ST")
    return p.parse_args()


if __name__ == "__main__":
    try:
        code, payload = executar(parse_args())
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        raise SystemExit(code)
    except SystemExit:
        raise
    except Exception as exc:
        print(json.dumps({"erros_controlados": [f"Erro inesperado: {exc}"], "conclusao": "ISOLAMENTO_INCONCLUSIVO"}, ensure_ascii=False, indent=2))
        raise SystemExit(2)
