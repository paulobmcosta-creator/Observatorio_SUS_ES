#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import random
import os
import time
import tempfile
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CAUSAS = [
    "ERRO_DE_REDE",
    "ERRO_DE_FONTE_DATASUS",
    "ERRO_DE_PARAMETRO",
    "ERRO_DE_GRUPO_CNES",
    "ERRO_DE_CONVERSAO_DBC",
    "ERRO_DE_CACHE_PYSUS",
    "ERRO_INTERNO_PYSUS",
    "ARQUIVO_NAO_ENCONTRADO",
    "RETORNO_VAZIO",
    "RETORNO_NAO_DATAFRAME",
    "DEPENDENCIA_AUSENTE",
    "OUTRO_ERRO_CONTROLADO",
    "CHAMADA_FUNCIONOU",
]


def _base(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "ambiente": {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "python": os.sys.version},
        "parametros": {"modo": args.modo, "uf": args.uf, "ano": args.ano, "mes": args.mes, "grupo": args.grupo},
        "isolamento": {
            "aplicado": False,
            "home_temp": None,
            "xdg_config_home_temp": None,
            "xdg_cache_home_temp": None,
            "import_apos_isolamento": False,
            "config_db_temporario": False,
            "lock_duckdb_detectado": False,
        },
        "diagnostico": {
            "tentativa_rede": False,
            "tentativas_realizadas": 0,
            "tentativas_maximas": args.tentativas,
            "retorno_parcial": False,
            "tipo_retorno": None,
            "retornou_dataframe": False,
            "classe_excecao": None,
            "mensagem_excecao": None,
            "traceback_resumido": None,
            "causa_classificada": None,
        },
        "causas_possiveis": CAUSAS,
        "erros_controlados": [],
        "conclusao": "",
        "proxima_recomendacao": "",
    }


def _classificar(exc_cls: str, msg: str) -> str:
    m = (msg or "").lower()
    c = (exc_cls or "").lower()
    if "no module named" in m or "importerror" in c:
        return "DEPENDENCIA_AUSENTE"
    if "lock" in m and "config.db" in m:
        return "ERRO_DE_CACHE_PYSUS"
    if "timeout" in c or any(t in m for t in ["timeout", "connection", "network", "dns", "name resolution", "ssl", "temporarily unavailable"]):
        return "ERRO_DE_REDE"
    if any(t in m for t in ["404", "not found", "arquivo", "file not found"]):
        return "ARQUIVO_NAO_ENCONTRADO"
    if "group" in m and "invalid" in m:
        return "ERRO_DE_GRUPO_CNES"
    if "parameter" in m or "argument" in m or "typeerror" in c or "valueerror" in c:
        return "ERRO_DE_PARAMETRO"
    if "dbc" in m:
        return "ERRO_DE_CONVERSAO_DBC"
    if "datasus" in m or "ftp" in m:
        return "ERRO_DE_FONTE_DATASUS"
    if "pysus" in m:
        return "ERRO_INTERNO_PYSUS"
    return "OUTRO_ERRO_CONTROLADO"


def executar(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    out = _base(args)

    if args.modo == "planejamento":
        out["conclusao"] = "Planejamento concluído sem rede e sem chamada cnes()."
        out["proxima_recomendacao"] = "Executar chamada_diagnostica com isolamento temporário."
        return 0, out

    if args.modo == "chamada_diagnostica":
        out["diagnostico"]["tentativa_rede"] = True
        old_home = os.environ.get("HOME")
        old_cfg = os.environ.get("XDG_CONFIG_HOME")
        old_cache = os.environ.get("XDG_CACHE_HOME")

        with tempfile.TemporaryDirectory(prefix="pysus_5n2_") as td:
            root = Path(td)
            home = root / "home"
            xcfg = root / "xdg_config"
            xcache = root / "xdg_cache"
            home.mkdir(parents=True, exist_ok=True)
            xcfg.mkdir(parents=True, exist_ok=True)
            xcache.mkdir(parents=True, exist_ok=True)
            os.environ["HOME"] = str(home)
            os.environ["XDG_CONFIG_HOME"] = str(xcfg)
            os.environ["XDG_CACHE_HOME"] = str(xcache)

            out["isolamento"].update(
                {
                    "aplicado": True,
                    "home_temp": str(home),
                    "xdg_config_home_temp": str(xcfg),
                    "xdg_cache_home_temp": str(xcache),
                }
            )
            try:
                from pysus import cnes  # type: ignore

                out["isolamento"]["import_apos_isolamento"] = True
                for tentativa in range(1, args.tentativas + 1):
                    out["diagnostico"]["tentativas_realizadas"] = tentativa
                    try:
                        ret = cnes(state=args.uf, year=args.ano, month=args.mes, group=args.grupo)
                        out["diagnostico"]["tipo_retorno"] = type(ret).__name__
                        if ret is None:
                            out["diagnostico"]["causa_classificada"] = "RETORNO_VAZIO"
                        elif hasattr(ret, "columns") and hasattr(ret, "shape"):
                            out["diagnostico"]["retornou_dataframe"] = True
                            out["diagnostico"]["causa_classificada"] = "CHAMADA_FUNCIONOU"
                        else:
                            out["diagnostico"]["retorno_parcial"] = True
                            out["diagnostico"]["causa_classificada"] = "RETORNO_NAO_DATAFRAME"
                        break
                    except Exception as exc_retry:
                        cls = type(exc_retry).__name__
                        msg = str(exc_retry)
                        causa = _classificar(cls, msg)
                        out["erros_controlados"].append(f"tentativa_{tentativa}: {cls}: {msg}")
                        if "config.db" in msg.lower() and "lock" in msg.lower():
                            out["isolamento"]["lock_duckdb_detectado"] = True
                        if tentativa >= args.tentativas or causa != "ERRO_DE_REDE":
                            raise
                        atraso = args.base_backoff * (2 ** (tentativa - 1)) + random.uniform(0, args.jitter_max)
                        time.sleep(atraso)
            except Exception as exc:
                cls = type(exc).__name__
                msg = str(exc)
                tb = traceback.format_exc(limit=4)
                out["diagnostico"].update(
                    {
                        "classe_excecao": cls,
                        "mensagem_excecao": msg,
                        "traceback_resumido": tb,
                        "causa_classificada": _classificar(cls, msg),
                    }
                )
                out["erros_controlados"].append(f"{cls}: {msg}")
                if "config.db" in msg.lower() and "lock" in msg.lower():
                    out["isolamento"]["lock_duckdb_detectado"] = True

            out["isolamento"]["config_db_temporario"] = any(p.name == "config.db" for p in root.rglob("config.db"))

        if old_home is not None:
            os.environ["HOME"] = old_home
        if old_cfg is not None:
            os.environ["XDG_CONFIG_HOME"] = old_cfg
        else:
            os.environ.pop("XDG_CONFIG_HOME", None)
        if old_cache is not None:
            os.environ["XDG_CACHE_HOME"] = old_cache
        else:
            os.environ.pop("XDG_CACHE_HOME", None)

        causa = out["diagnostico"]["causa_classificada"] or "OUTRO_ERRO_CONTROLADO"
        out["conclusao"] = f"Diagnóstico concluído: {causa}."
        out["proxima_recomendacao"] = "Se não for lock, investigar conectividade/fonte DATASUS e compatibilidade PySUS."
        return 0, out

    out["conclusao"] = "Modo inválido."
    return 2, out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Diagnóstico da falha cnes() pós-isolamento PySUS")
    ap.add_argument("--modo", default="planejamento", choices=["planejamento", "chamada_diagnostica"])
    ap.add_argument("--uf", default="ES")
    ap.add_argument("--ano", type=int, default=2024)
    ap.add_argument("--mes", type=int, default=1)
    ap.add_argument("--grupo", default="ST")
    ap.add_argument("--tentativas", type=int, default=3)
    ap.add_argument("--base-backoff", dest="base_backoff", type=float, default=1.0)
    ap.add_argument("--jitter-max", dest="jitter_max", type=float, default=0.5)
    args = ap.parse_args()
    code, payload = executar(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(code)
