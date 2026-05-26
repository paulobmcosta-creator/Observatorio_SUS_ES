from __future__ import annotations

import argparse
import importlib
import inspect
import json
import os
import random
import sys
import tempfile
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None

CAMPOS_CHAVE = [
    "unidade",
    "co_unidade",
    "cnes",
    "co_cnes",
    "municipio",
    "cod_municipio",
    "co_municipio",
    "uf",
    "leito",
    "servico",
    "serviço",
    "classificacao",
    "classificação",
    "habilitacao",
    "habilitação",
    "estabelecimento",
]

CAUSAS = ["CHAMADA_FUNCIONOU","GRUPO_ACEITO_COM_RETORNO","GRUPO_ACEITO_RETORNO_VAZIO","GRUPO_NAO_ACEITO","ERRO_DE_REDE","ERRO_DE_FONTE_DATASUS","ERRO_DE_PARAMETRO","ERRO_DE_GRUPO_CNES","ERRO_DE_CONVERSAO_DBC","ERRO_DE_CACHE_PYSUS","ERRO_INTERNO_PYSUS","ARQUIVO_NAO_ENCONTRADO","RETORNO_VAZIO","RETORNO_NAO_DATAFRAME","DEPENDENCIA_AUSENTE","OUTRO_ERRO_CONTROLADO"]

REPO = Path(__file__).resolve().parents[3]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--modo", choices=["planejamento", "inspecao_api", "testar_grupos", "resumo"], default="planejamento")
    p.add_argument("--uf", default="ES")
    p.add_argument("--ano", type=int, default=2024)
    p.add_argument("--mes", type=int, default=1)
    p.add_argument("--grupos-candidatos", nargs="+", default=["ST", "LT", "SR"])
    p.add_argument("--tentativas", type=int, default=3)
    p.add_argument("--base-backoff", type=float, default=1.0)
    p.add_argument("--jitter-max", type=float, default=0.5)
    return p.parse_args()


def carregar_contratos() -> dict[str, Any]:
    try:
        from observatorio_sus.cnes import contratos
        tabelas = contratos.CONTRATOS_TABELAS
    except Exception:
        return {}
    campos = set()
    for v in tabelas.values():
        for c in v.get("campos_criticos", []):
            campos.add(str(c).lower())
    return {"tabelas": list(tabelas.keys()), "campos": sorted(campos)}


def detectar_campos(cols: list[str]) -> list[str]:
    low = [c.lower() for c in cols]
    found = []
    for k in CAMPOS_CHAVE:
        if any(k in c for c in low):
            found.append(k)
    return sorted(set(found))


def classificar_erro(exc: Exception) -> str:
    s = f"{exc.__class__.__name__}: {exc}".lower()
    if "timeout" in s or "readtimeout" in s or "connection" in s or "network" in s:
        return "ERRO_DE_REDE"
    if "group" in s and ("invalid" in s or "inval" in s):
        return "ERRO_DE_GRUPO_CNES"
    if "duckdb" in s or "config.db" in s or "cache" in s:
        return "ERRO_DE_CACHE_PYSUS"
    if "dbc" in s:
        return "ERRO_DE_CONVERSAO_DBC"
    if "file" in s and "not found" in s:
        return "ARQUIVO_NAO_ENCONTRADO"
    if "module" in s and "not found" in s:
        return "DEPENDENCIA_AUSENTE"
    return "OUTRO_ERRO_CONTROLADO"


def inspecao_api() -> tuple[list[str], dict[str, Any]]:
    ev = {}
    detectados = set()
    with tempfile.TemporaryDirectory(prefix="pysus-5n3-") as t:
        os.environ["HOME"] = t
        os.environ["XDG_CONFIG_HOME"] = f"{t}/.config"
        os.environ["XDG_CACHE_HOME"] = f"{t}/.cache"
        from pysus import cnes
        ev["signature"] = str(inspect.signature(cnes))
        ev["doc"] = (inspect.getdoc(cnes) or "")[:1200]
        for token in ["ST", "LT", "SR", "HB", "PF", "EQ"]:
            if token in ev["doc"]:
                detectados.add(token)
    return sorted(detectados), ev


def testar_grupo(args: argparse.Namespace, grupo: str) -> dict[str, Any]:
    out = {"grupo": grupo, "descricao_inferida": {"ST":"estabelecimentos","LT":"leitos","SR":"serviços/classificação"}.get(grupo,"nao_inferida"),
           "origem_da_candidatura":"herdado_script_local_funcional" if grupo in ["ST","LT","SR"] else "inspecao_api_ou_manual",
           "chamada_executada": f"cnes(state='{args.uf}', year={args.ano}, month={args.mes}, group='{grupo}')", "tentativas_realizadas":0,
           "sucesso":False,"tipo_retorno":None,"eh_dataframe":False,"numero_linhas":0,"numero_colunas":0,"colunas":[],
           "campos_chave_detectados":[],"classe_excecao":None,"mensagem_excecao":None,"causa_classificada":"OUTRO_ERRO_CONTROLADO",
           "persistiu_dados":False}
    with tempfile.TemporaryDirectory(prefix="pysus-5n3-") as t:
        os.environ["HOME"] = t; os.environ["XDG_CONFIG_HOME"] = f"{t}/.config"; os.environ["XDG_CACHE_HOME"] = f"{t}/.cache"
        from pysus import cnes
        last_exc = None
        for i in range(args.tentativas):
            out["tentativas_realizadas"] = i + 1
            try:
                ret = cnes(state=args.uf, year=args.ano, month=args.mes, group=grupo)
                out["tipo_retorno"] = type(ret).__name__
                if pd is not None and isinstance(ret, pd.DataFrame):
                    out["eh_dataframe"] = True; out["sucesso"] = True
                    out["numero_linhas"], out["numero_colunas"] = int(ret.shape[0]), int(ret.shape[1])
                    out["colunas"] = [str(c) for c in list(ret.columns)]
                    out["campos_chave_detectados"] = detectar_campos(out["colunas"])
                    out["causa_classificada"] = "GRUPO_ACEITO_COM_RETORNO" if out["numero_linhas"] > 0 else "GRUPO_ACEITO_RETORNO_VAZIO"
                else:
                    out["sucesso"] = True
                    out["causa_classificada"] = "RETORNO_NAO_DATAFRAME"
                break
            except Exception as exc:
                last_exc = exc
                out["classe_excecao"] = exc.__class__.__name__
                out["mensagem_excecao"] = str(exc)
                out["causa_classificada"] = classificar_erro(exc)
                if i < args.tentativas - 1:
                    time.sleep((args.base_backoff * (2**i)) + random.uniform(0, args.jitter_max))
        if not out["sucesso"] and last_exc is not None:
            out["causa_classificada"] = classificar_erro(last_exc)
    return out


def main() -> int:
    args = parse_args()
    payload: dict[str, Any] = {
        "ambiente": {"python": sys.version, "timestamp_utc": datetime.now(timezone.utc).isoformat()},
        "parametros": {"modo": args.modo, "uf": args.uf, "ano": args.ano, "mes": args.mes, "grupos_candidatos": args.grupos_candidatos},
        "cadeia_documental": {"5N": (REPO / "docs/migracao_python/05N_reinicio_cnes_python_api_pysus.md").exists(), "5N1": (REPO / "docs/migracao_python/05N1_isolamento_pysus_duckdb_cnes.md").exists(), "5N2": (REPO / "docs/migracao_python/05N2_diagnostico_falha_cnes_pos_isolamento.md").exists()},
        "isolamento": {"aplica_home_temporario": True, "aplica_xdg_config_home_temporario": True, "aplica_xdg_cache_home_temporario": True},
        "retry": {"tentativas": args.tentativas, "base_backoff": args.base_backoff, "jitter_max": args.jitter_max},
        "grupos_candidatos_iniciais": {"grupos": ["ST", "LT", "SR"], "observacao": "ST/LT/SR sao candidatos iniciais herdados do script local funcional; nao sao lista fechada."},
        "grupos_detectados_por_inspecao": [], "grupos_testados": [], "resultados_por_grupo": [],
        "relacao_com_contratos_cnes": [], "matriz_interesse_metodologico": [], "grupos_recomendados_para_mapeamento": [],
        "grupos_nao_recomendados_ou_inconclusivos": [], "erros_controlados": [],
        "conclusao": "", "proxima_recomendacao": ""
    }
    if args.modo in {"inspecao_api", "testar_grupos"}:
        det, evid = inspecao_api()
        payload["grupos_detectados_por_inspecao"] = {"grupos": det, "evidencias": evid, "limitacoes": "Inspecao sem download; pode nao revelar lista oficial completa."}
    if args.modo == "testar_grupos":
        contratos = carregar_contratos()
        for g in args.grupos_candidatos:
            r = testar_grupo(args, g)
            payload["resultados_por_grupo"].append(r)
            payload["grupos_testados"].append(g)
            if r["causa_classificada"] not in {"CHAMADA_FUNCIONOU", "GRUPO_ACEITO_COM_RETORNO", "GRUPO_ACEITO_RETORNO_VAZIO", "RETORNO_NAO_DATAFRAME"}:
                payload["erros_controlados"].append({"grupo": g, "causa": r["causa_classificada"]})
            rel = []
            if contratos:
                rel = sorted([c for c in contratos["campos"] if any(c in cc.lower() for cc in r["colunas"])])
            interesse = "INCONCLUSIVO"
            if r["eh_dataframe"] and r["campos_chave_detectados"]:
                interesse = "ALTO_INTERESSE" if rel or g in ["ST", "LT", "SR"] else "INTERESSE_MODERADO"
            elif r["sucesso"]:
                interesse = "BAIXO_INTERESSE"
            payload["relacao_com_contratos_cnes"].append({"grupo": g, "campos_encontrados": r["colunas"], "relacao_nominal_campos_criticos": rel})
            payload["matriz_interesse_metodologico"].append({"grupo": g, "interesse": interesse})
            (payload["grupos_recomendados_para_mapeamento"] if interesse in {"ALTO_INTERESSE", "INTERESSE_MODERADO"} else payload["grupos_nao_recomendados_ou_inconclusivos"]).append(g)
    if args.modo in {"planejamento", "resumo", "inspecao_api"}:
        payload["conclusao"] = "Etapa de inventario sem persistencia de dados e sem substituicao de scripts R."
        payload["proxima_recomendacao"] = "Executar Etapa 5N.4 para mapeamento estrutural dos grupos recomendados e, se necessario, 5N.3A para investigacao documental adicional."
    else:
        payload["conclusao"] = "Teste de grupos concluido com falhas controladas quando presentes."
        payload["proxima_recomendacao"] = "Priorizar grupos com ALTO_INTERESSE na Etapa 5N.4."
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        print(json.dumps({"erro_inesperado": traceback.format_exc(limit=5)}))
        raise SystemExit(2)
