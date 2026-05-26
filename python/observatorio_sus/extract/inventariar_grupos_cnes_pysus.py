from __future__ import annotations

import argparse
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
    "unidade", "co_unidade", "cnes", "co_cnes", "municipio", "cod_municipio", "co_municipio", "uf",
    "leito", "servico", "serviço", "classificacao", "classificação", "habilitacao", "habilitação", "estabelecimento",
]

REL_TERMS = ["cnes", "unidade", "municipio", "leito", "servico", "classificacao", "habilitacao"]
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
    except Exception:
        return {"campos": []}
    campos = set()
    for v in contratos.CONTRATOS_TABELAS.values():
        for c in v.get("campos_criticos", []):
            campos.add(str(c).lower())
    return {"campos": sorted(campos)}


def detectar_campos(cols: list[str]) -> list[str]:
    low = [c.lower() for c in cols]
    return sorted({k for k in CAMPOS_CHAVE if any(k in c for c in low)})


def classificar_erro(exc: Exception) -> str:
    s = f"{exc.__class__.__name__}: {exc}".lower()
    if any(x in s for x in ["timeout", "readtimeout", "connection", "network"]):
        return "ERRO_DE_REDE"
    if "group" in s and any(x in s for x in ["invalid", "inval"]):
        return "ERRO_DE_GRUPO_CNES"
    if any(x in s for x in ["duckdb", "config.db", "cache"]):
        return "ERRO_DE_CACHE_PYSUS"
    if "dbc" in s:
        return "ERRO_DE_CONVERSAO_DBC"
    if "file" in s and "not found" in s:
        return "ARQUIVO_NAO_ENCONTRADO"
    if "module" in s and "not found" in s:
        return "DEPENDENCIA_AUSENTE"
    return "OUTRO_ERRO_CONTROLADO"


def inspecao_api() -> tuple[list[str], dict[str, Any]]:
    ev, detectados = {}, set()
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


def classificar_relacao(cols: list[str], contrato_campos: list[str]) -> tuple[str, list[str], list[str]]:
    if not cols:
        return "NAO_AVALIADA", [], []
    low = [c.lower() for c in cols]
    diretos = sorted([c for c in contrato_campos if c in low])
    aprox = sorted({t for t in REL_TERMS if any(t in c for c in low)})
    if diretos:
        return "NOMINAL_DIRETA", diretos, aprox
    if aprox:
        return "NOMINAL_APROXIMADA", [], aprox
    return "SEM_RELACAO_CONFIRMADA", [], []


def preencher_avaliacao(grupo: str, out: dict[str, Any], rel_tipo: str, diretos: list[str], aprox: list[str]) -> None:
    if not out["sucesso"]:
        out["interesse_metodologico"] = "INCONCLUSIVO"
        out["nivel_evidencia_interesse"] = "INCONCLUSIVO"
        out["cobertura_contratos_status"] = "COBERTURA_INCONCLUSIVA"
        out["justificativa_interesse_metodologico"] = "Falha controlada na execução; resultado inconclusivo para decisão metodológica."
        out["recomendado_para_5n4"] = False
        out["ressalvas_para_5n4"] = ["Reexecutar em janela de rede estável antes do mapeamento estrutural."]
        return

    if not out["eh_dataframe"] or out["numero_linhas"] == 0:
        out["interesse_metodologico"] = "BAIXO_INTERESSE"
        out["nivel_evidencia_interesse"] = "EVIDENCIA_FRACA"
        out["cobertura_contratos_status"] = "COBERTURA_NAO_CONFIRMADA"
        out["justificativa_interesse_metodologico"] = "Sem DataFrame utilizável com conteúdo para apoiar mapeamento estrutural."
        out["recomendado_para_5n4"] = False
        out["ressalvas_para_5n4"] = ["Necessário retorno tabular consistente antes de avançar."]
        return

    fortes = bool(set(out["campos_chave_detectados"]) & {"cnes", "co_cnes", "unidade", "co_unidade", "municipio", "co_municipio", "leito", "servico", "classificacao", "habilitacao", "estabelecimento"})
    herdado = grupo in {"ST", "LT", "SR"}

    if rel_tipo == "NOMINAL_DIRETA" and fortes:
        out["interesse_metodologico"] = "ALTO_INTERESSE"
        out["nivel_evidencia_interesse"] = "EVIDENCIA_FORTE"
        out["cobertura_contratos_status"] = "COBERTURA_POTENCIAL_FORTE"
        out["justificativa_interesse_metodologico"] = "DataFrame com campos-chave e correspondência nominal direta com contratos; evidência forte para mapeamento exploratório."
    elif fortes and rel_tipo == "NOMINAL_APROXIMADA":
        out["interesse_metodologico"] = "ALTO_INTERESSE" if herdado else "INTERESSE_MODERADO"
        out["nivel_evidencia_interesse"] = "EVIDENCIA_MODERADA"
        out["cobertura_contratos_status"] = "COBERTURA_POTENCIAL_PARCIAL"
        out["justificativa_interesse_metodologico"] = (
            "DataFrame com campos-chave e relação nominal aproximada. Para ST/LT/SR, o alto interesse é escopo operacional inicial e não prova de cobertura contratual plena."
            if herdado else "DataFrame com campos-chave, porém relação contratual indireta/aproximada."
        )
    else:
        out["interesse_metodologico"] = "INTERESSE_MODERADO"
        out["nivel_evidencia_interesse"] = "EVIDENCIA_OPERACIONAL"
        out["cobertura_contratos_status"] = "COBERTURA_NAO_CONFIRMADA"
        out["justificativa_interesse_metodologico"] = "Retorno operacional de DataFrame, mas relação com contratos/campos-chave ainda inconclusiva para cobertura potencial robusta."

    out["recomendado_para_5n4"] = out["interesse_metodologico"] in {"ALTO_INTERESSE", "INTERESSE_MODERADO"}
    out["ressalvas_para_5n4"] = [
        "Autorização apenas para mapeamento estrutural exploratório.",
        "Não implica cobertura contratual confirmada.",
        "Manter R como oráculo metodológico."
    ]


def testar_grupo(args: argparse.Namespace, grupo: str, contrato_campos: list[str]) -> dict[str, Any]:
    out = {
        "grupo": grupo,
        "descricao_inferida": {"ST": "estabelecimentos", "LT": "leitos", "SR": "serviços/classificação"}.get(grupo, "nao_inferida"),
        "origem_da_candidatura": "herdado_script_local_funcional" if grupo in ["ST", "LT", "SR"] else "inspecao_api_ou_manual",
        "chamada_executada": f"cnes(state='{args.uf}', year={args.ano}, month={args.mes}, group='{grupo}')",
        "tentativas_realizadas": 0, "sucesso": False, "tipo_retorno": None, "eh_dataframe": False,
        "numero_linhas": 0, "numero_colunas": 0, "colunas": [], "dtypes": {}, "campos_chave_detectados": [],
        "classe_excecao": None, "mensagem_excecao": None, "causa_classificada": "OUTRO_ERRO_CONTROLADO", "persistiu_dados": False,
        "justificativa_interesse_metodologico": "", "nivel_evidencia_interesse": "INCONCLUSIVO",
        "relacao_com_contratos_tipo": "NAO_AVALIADA", "cobertura_contratos_status": "COBERTURA_INCONCLUSIVA",
        "recomendado_para_5n4": False, "ressalvas_para_5n4": [], "interesse_metodologico": "INCONCLUSIVO",
    }
    with tempfile.TemporaryDirectory(prefix="pysus-5n3-") as t:
        os.environ["HOME"] = t
        os.environ["XDG_CONFIG_HOME"] = f"{t}/.config"
        os.environ["XDG_CACHE_HOME"] = f"{t}/.cache"
        from pysus import cnes
        last_exc = None
        for i in range(args.tentativas):
            out["tentativas_realizadas"] = i + 1
            try:
                ret = cnes(state=args.uf, year=args.ano, month=args.mes, group=grupo)
                out["tipo_retorno"] = type(ret).__name__
                if pd is not None and isinstance(ret, pd.DataFrame):
                    out["eh_dataframe"] = True
                    out["sucesso"] = True
                    out["numero_linhas"], out["numero_colunas"] = int(ret.shape[0]), int(ret.shape[1])
                    out["colunas"] = [str(c) for c in ret.columns.tolist()]
                    out["dtypes"] = {str(c): str(dt) for c, dt in ret.dtypes.astype(str).items()}
                    out["campos_chave_detectados"] = detectar_campos(out["colunas"])
                    out["causa_classificada"] = "GRUPO_ACEITO_COM_RETORNO" if out["numero_linhas"] > 0 else "GRUPO_ACEITO_RETORNO_VAZIO"
                else:
                    out["sucesso"] = True
                    out["causa_classificada"] = "RETORNO_NAO_DATAFRAME"
                break
            except Exception as exc:
                last_exc = exc
                out["classe_excecao"], out["mensagem_excecao"] = exc.__class__.__name__, str(exc)
                out["causa_classificada"] = classificar_erro(exc)
                if i < args.tentativas - 1:
                    time.sleep((args.base_backoff * (2**i)) + random.uniform(0, args.jitter_max))
        if not out["sucesso"] and last_exc is not None:
            out["causa_classificada"] = classificar_erro(last_exc)

    rel_tipo, diretos, aprox = classificar_relacao(out["colunas"], contrato_campos)
    out["relacao_com_contratos_tipo"] = rel_tipo
    out["campos_contratuais_literalmente_encontrados"] = diretos
    out["campos_contratuais_aproximados"] = aprox
    preencher_avaliacao(grupo, out, rel_tipo, diretos, aprox)
    return out


def main() -> int:
    args = parse_args()
    template_result = {
        "nivel_evidencia_interesse": "INCONCLUSIVO",
        "relacao_com_contratos_tipo": "NAO_AVALIADA",
        "cobertura_contratos_status": "COBERTURA_INCONCLUSIVA",
        "justificativa_interesse_metodologico": "",
        "recomendado_para_5n4": False,
    }
    payload: dict[str, Any] = {
        "ambiente": {"python": sys.version, "timestamp_utc": datetime.now(timezone.utc).isoformat()},
        "parametros": {"modo": args.modo, "uf": args.uf, "ano": args.ano, "mes": args.mes, "grupos_candidatos": args.grupos_candidatos},
        "cadeia_documental": {"5N": (REPO / "docs/migracao_python/05N_reinicio_cnes_python_api_pysus.md").exists(), "5N1": (REPO / "docs/migracao_python/05N1_isolamento_pysus_duckdb_cnes.md").exists(), "5N2": (REPO / "docs/migracao_python/05N2_diagnostico_falha_cnes_pos_isolamento.md").exists()},
        "isolamento": {"aplica_home_temporario": True, "aplica_xdg_config_home_temporario": True, "aplica_xdg_cache_home_temporario": True},
        "retry": {"tentativas": args.tentativas, "base_backoff": args.base_backoff, "jitter_max": args.jitter_max},
        "grupos_candidatos_iniciais": {"grupos": ["ST", "LT", "SR"], "observacao": "ST/LT/SR são candidatos iniciais herdados do script local funcional; não são lista fechada."},
        "estrutura_resultado_por_grupo": template_result,
        "grupos_detectados_por_inspecao": [], "grupos_testados": [], "resultados_por_grupo": [], "relacao_com_contratos_cnes": [],
        "matriz_interesse_metodologico": [], "grupos_recomendados_para_mapeamento": [], "grupos_nao_recomendados_ou_inconclusivos": [],
        "erros_controlados": [], "decisao_5n4": {"autorizada": False, "grupos_autorizados": [], "natureza_da_autorizacao": "mapeamento estrutural exploratório, não validação contratual plena", "justificativa": "Sem grupos avaliados ainda.", "ressalvas": ["Manter caráter exploratório."]},
        "conclusao": "", "proxima_recomendacao": "",
    }

    if args.modo in {"inspecao_api", "testar_grupos"}:
        det, evid = inspecao_api()
        payload["grupos_detectados_por_inspecao"] = {"grupos": det, "evidencias": evid, "limitacoes": "Inspeção sem download; pode não revelar lista oficial completa."}

    if args.modo == "testar_grupos":
        contrato_campos = carregar_contratos()["campos"]
        for g in args.grupos_candidatos:
            r = testar_grupo(args, g, contrato_campos)
            payload["resultados_por_grupo"].append(r)
            payload["grupos_testados"].append(g)
            payload["relacao_com_contratos_cnes"].append({
                "grupo": g,
                "relacao_com_contratos_tipo": r["relacao_com_contratos_tipo"],
                "campos_contratuais_literalmente_encontrados": r["campos_contratuais_literalmente_encontrados"],
                "campos_contratuais_aproximados": r["campos_contratuais_aproximados"],
                "cobertura_contratos_status": r["cobertura_contratos_status"],
            })
            payload["matriz_interesse_metodologico"].append({"grupo": g, "interesse": r["interesse_metodologico"], "nivel_evidencia": r["nivel_evidencia_interesse"]})
            if r["interesse_metodologico"] in {"ALTO_INTERESSE", "INTERESSE_MODERADO"} and r["recomendado_para_5n4"]:
                payload["grupos_recomendados_para_mapeamento"].append(g)
            else:
                payload["grupos_nao_recomendados_ou_inconclusivos"].append(g)
            if not r["sucesso"]:
                payload["erros_controlados"].append({"grupo": g, "causa": r["causa_classificada"]})

        autorizados = payload["grupos_recomendados_para_mapeamento"]
        payload["decisao_5n4"] = {
            "autorizada": len(autorizados) > 0,
            "grupos_autorizados": autorizados,
            "natureza_da_autorizacao": "mapeamento estrutural exploratório, não validação contratual plena",
            "justificativa": "Há pelo menos um grupo com DataFrame e interesse ALTO_INTERESSE/INTERESSE_MODERADO." if autorizados else "Nenhum grupo atingiu critério mínimo de autorização.",
            "ressalvas": [
                "Não implica cobertura contratual confirmada.",
                "Não autoriza extração histórica.",
                "Não substitui scripts R."
            ],
        }

    payload["conclusao"] = "Inventário executado sem persistência de dados e com classificação metodológica transparente." if args.modo == "testar_grupos" else "Etapa de inventário em modo sem persistência de dados."
    payload["proxima_recomendacao"] = "Preparar mapeamento estrutural exploratório (5N.4) apenas para grupos autorizados." if payload["decisao_5n4"]["autorizada"] else "Revisar critérios e repetir diagnóstico antes de considerar 5N.4."
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
