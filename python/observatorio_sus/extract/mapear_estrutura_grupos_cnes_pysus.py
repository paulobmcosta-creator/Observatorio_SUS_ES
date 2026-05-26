from __future__ import annotations

import argparse
import json
import os
import random
import re
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

REPO = Path(__file__).resolve().parents[3]
PYTHON_DIR = REPO / "python"
DOCS_CADEIA = {
    "5N": "docs/migracao_python/05N_reinicio_cnes_python_api_pysus.md",
    "5N1": "docs/migracao_python/05N1_isolamento_pysus_duckdb_cnes.md",
    "5N2": "docs/migracao_python/05N2_diagnostico_falha_cnes_pos_isolamento.md",
    "5N3": "docs/migracao_python/05N3_inventario_grupos_cnes_pysus.md",
    "5N3R": "docs/migracao_python/05N3R_reteste_controlado_st_cnes_pysus.md",
}
DESC_GRUPO = {"ST": "estabelecimentos", "LT": "leitos", "SR": "serviços/classificação"}
CAMPOS_CHAVE_NOMES = [
    "CNES", "CO_CNES", "unidade", "CO_UNIDADE", "município", "municipio", "CODUFMUN", "CO_MUNICIPIO", "UF",
    "leito", "serviço", "servico", "classificação", "classificacao", "habilitação", "habilitacao", "estabelecimento",
    "COMPETEN", "TPGESTAO", "NAT_JUR", "CPF_CNPJ", "CNPJ_MAN",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--modo", choices=["planejamento", "mapear_estrutura", "resumo"], default="planejamento")
    p.add_argument("--uf", default="ES")
    p.add_argument("--ano", type=int, default=2024)
    p.add_argument("--mes", type=int, default=1)
    p.add_argument("--grupos", nargs="+", default=["ST", "LT", "SR"])
    p.add_argument("--tentativas", type=int, default=5)
    p.add_argument("--base-backoff", type=float, default=2.0)
    p.add_argument("--jitter-max", type=float, default=1.0)
    return p.parse_args()


def classificar_erro(exc: Exception) -> str:
    s = f"{exc.__class__.__name__}: {exc}".lower()
    if any(x in s for x in ["timeout", "readtimeout", "connection", "network"]):
        return "ERRO_DE_REDE"
    if "dbc" in s:
        return "ERRO_DE_CONVERSAO_DBC"
    if any(x in s for x in ["duckdb", "config.db", "cache"]):
        return "ERRO_DE_CACHE_PYSUS"
    if "group" in s and any(x in s for x in ["invalid", "inval"]):
        return "ERRO_DE_GRUPO_CNES"
    if "module" in s and "not found" in s:
        return "DEPENDENCIA_AUSENTE"
    return "OUTRO_ERRO_CONTROLADO"


def carregar_campos_contratos() -> tuple[list[str], dict[str, Any]]:
    info = {"carregado": False, "quantidade_campos_criticos": 0, "erro_importacao": None, "origem": "nao_inicializada"}
    try:
        if str(PYTHON_DIR) not in sys.path:
            sys.path.insert(0, str(PYTHON_DIR))
        from observatorio_sus.cnes import contratos

        campos = set()
        for cfg in contratos.CONTRATOS_TABELAS.values():
            campos.update(str(c) for c in cfg.get("campos_criticos", []))
        campos_ordenados = sorted(campos)
        info.update({"carregado": True, "quantidade_campos_criticos": len(campos_ordenados), "origem": "python/observatorio_sus/cnes/contratos.py"})
        return campos_ordenados, info
    except Exception as exc:
        info.update({"carregado": False, "erro_importacao": f"{exc.__class__.__name__}: {exc}", "origem": "falha_ao_importar_contratos"})
        return [], info


def detectar_campos_chave(cols: list[str]) -> list[str]:
    low = [c.lower() for c in cols]
    return sorted({k for k in CAMPOS_CHAVE_NOMES if any(k.lower() in c for c in low)})


def avaliar_contratos(colunas: list[str], campos_contrato: list[str]) -> dict[str, Any]:
    if not campos_contrato:
        return {"relacao_com_contratos_tipo": "não avaliado", "cobertura_contratos_status": "COBERTURA_INCONCLUSIVA", "campos_contratuais_literais": [], "campos_contratuais_aproximados": [], "campos_criticos_ausentes": []}
    low = [c.lower() for c in colunas]
    literais = sorted([c for c in campos_contrato if c.lower() in low])
    aprox = sorted([c for c in campos_contrato if c.lower() not in low and any(tok in c.lower() for tok in ["cnes", "unidade", "municipio", "gestao", "natureza", "habilitacao"])])
    ausentes = sorted([c for c in campos_contrato if c.lower() not in low])
    cobertura, rel = ("COBERTURA_POTENCIAL_FORTE", "correspondência literal") if literais and len(ausentes) <= len(campos_contrato) * 0.5 else (("COBERTURA_POTENCIAL_PARCIAL", "correspondência aproximada") if (literais or aprox) else ("COBERTURA_NAO_CONFIRMADA", "ausência"))
    return {"relacao_com_contratos_tipo": rel, "cobertura_contratos_status": cobertura, "campos_contratuais_literais": literais, "campos_contratuais_aproximados": aprox, "campos_criticos_ausentes": ausentes}


def riscos_coercao(colunas: list[str]) -> list[str]:
    bases = {"CNES", "CODUFMUN", "CPF_CNPJ", "CNPJ_MAN", "COMPETEN", "TPGESTAO", "NAT_JUR"}
    out = {c for c in colunas if c.upper() in bases}
    out.update(c for c in colunas if re.match(r"^(COD|CO_|CPF|CNPJ)", c.upper()))
    return sorted(out)


def executar_grupo(args: argparse.Namespace, grupo: str, campos_contrato: list[str]) -> dict[str, Any]:
    out = {"grupo": grupo, "descricao_grupo": DESC_GRUPO.get(grupo, "nao_mapeado"), "chamada_executada": f"cnes(state='{args.uf}', year={args.ano}, month={args.mes}, group='{grupo}')", "tentativas_realizadas": 0, "sucesso": False, "tipo_retorno": None, "eh_dataframe": False, "numero_linhas": 0, "numero_colunas": 0, "colunas": [], "dtypes": {}, "campos_chave_detectados": [], "relacao_com_contratos_tipo": "não avaliado", "cobertura_contratos_status": "COBERTURA_INCONCLUSIVA", "campos_contratuais_literais": [], "campos_contratuais_aproximados": [], "campos_criticos_ausentes": [], "riscos_coercao": [], "classe_excecao": None, "mensagem_excecao": None, "causa_classificada": "OUTRO_ERRO_CONTROLADO", "persistiu_dados": False, "erro_etapa": None, "modulo_faltante": None, "traceback_resumido": None}
    from pysus import cnes
    for i in range(args.tentativas):
        out["tentativas_realizadas"] = i + 1
        try:
            ret = cnes(state=args.uf, year=args.ano, month=args.mes, group=grupo)
            out["tipo_retorno"] = type(ret).__name__
            if pd is not None and isinstance(ret, pd.DataFrame):
                out["eh_dataframe"] = out["sucesso"] = True
                out["numero_linhas"], out["numero_colunas"] = int(ret.shape[0]), int(ret.shape[1])
                out["colunas"] = [str(c) for c in ret.columns]
                out["dtypes"] = {str(c): str(dt) for c, dt in ret.dtypes.astype(str).items()}
                out["campos_chave_detectados"] = detectar_campos_chave(out["colunas"])
                out["riscos_coercao"] = riscos_coercao(out["colunas"])
                out.update(avaliar_contratos(out["colunas"], campos_contrato))
                out["causa_classificada"] = "GRUPO_ACEITO_COM_RETORNO" if out["numero_linhas"] > 0 else "GRUPO_ACEITO_RETORNO_VAZIO"
            else:
                out["sucesso"] = True
                out["causa_classificada"] = "RETORNO_NAO_DATAFRAME"
            break
        except Exception as exc:
            out["classe_excecao"], out["mensagem_excecao"] = exc.__class__.__name__, str(exc)
            out["causa_classificada"] = classificar_erro(exc)
            out["erro_etapa"] = "durante_chamada_cnes"
            if isinstance(exc, ModuleNotFoundError):
                out["modulo_faltante"] = getattr(exc, "name", None)
            out["traceback_resumido"] = " | ".join(traceback.format_exception_only(type(exc), exc)).strip()[:400]
            if i < args.tentativas - 1:
                time.sleep((args.base_backoff * (2**i)) + random.uniform(0, args.jitter_max))
    return out


def main() -> int:
    args = parse_args()
    campos_contrato, contratos_info = carregar_campos_contratos()
    payload: dict[str, Any] = {
        "ambiente": {"python": sys.version, "timestamp_utc": datetime.now(timezone.utc).isoformat()},
        "parametros": {"modo": args.modo, "uf": args.uf, "ano": args.ano, "mes": args.mes, "grupos": args.grupos},
        "cadeia_documental": {k: (REPO / v).exists() for k, v in DOCS_CADEIA.items()},
        "isolamento": {"home_temporario": True, "xdg_config_home_temporario": True, "xdg_cache_home_temporario": True},
        "retry": {"tentativas": args.tentativas, "base_backoff": args.base_backoff, "jitter_max": args.jitter_max},
        "usa_api_publica_pysus": {"ativo": True, "caminho_funcional": "from pysus import cnes; cnes(state=uf, year=ano, month=mes, group=grupo)", "importa_pysus_no_planejamento": False},
        "contratos_cnes": contratos_info,
        "grupos_mapeados": [], "resultados_por_grupo": [], "matriz_colunas_por_grupo": {}, "matriz_campos_chave": {}, "matriz_contratos": {},
        "riscos_coercao_codigos": {}, "recomendacoes_padronizacao": ["Preservar chaves/códigos como texto em etapa futura.", "Criar dicionário PySUS -> contratos CNES antes de validação formal."],
        "erros_controlados": [], "conclusao": {}, "proxima_recomendacao": "Etapa 5N.5 com múltiplas competências piloto sem persistência.",
    }
    if args.modo in {"planejamento", "resumo"}:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    try:
        with tempfile.TemporaryDirectory(prefix="pysus-5n4-") as temp_dir:
            os.environ["HOME"] = temp_dir
            os.environ["XDG_CONFIG_HOME"] = f"{temp_dir}/.config"
            os.environ["XDG_CACHE_HOME"] = f"{temp_dir}/.cache"
            for grupo in args.grupos:
                r = executar_grupo(args, grupo, campos_contrato)
                payload["grupos_mapeados"].append(grupo)
                payload["resultados_por_grupo"].append(r)
                payload["matriz_colunas_por_grupo"][grupo] = r["colunas"]
                payload["matriz_campos_chave"][grupo] = r["campos_chave_detectados"]
                payload["matriz_contratos"][grupo] = {"tipo": r["relacao_com_contratos_tipo"], "cobertura": r["cobertura_contratos_status"], "literais": r["campos_contratuais_literais"], "aproximados": r["campos_contratuais_aproximados"], "ausentes": r["campos_criticos_ausentes"]}
                payload["riscos_coercao_codigos"][grupo] = r["riscos_coercao"]
                if not r["sucesso"]:
                    payload["erros_controlados"].append({"grupo": grupo, "causa": r["causa_classificada"], "modulo_faltante": r["modulo_faltante"]})

        dfs = [r["eh_dataframe"] for r in payload["resultados_por_grupo"]]
        payload["conclusao"] = {"st_lt_sr_mapeados": all(g in payload["grupos_mapeados"] for g in ["ST", "LT", "SR"]), "todos_retornaram_dataframe": all(dfs) if dfs else False, "campos_chave_suficientes": any(len(r["campos_chave_detectados"]) > 0 for r in payload["resultados_por_grupo"]), "deve_seguir_multi_competencia": all(dfs) if dfs else False, "grupos_para_reteste": [r["grupo"] for r in payload["resultados_por_grupo"] if not r["sucesso"]], "substituicao_r": "Não. Nenhum script R pode ser substituído nesta etapa."}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        payload["erros_controlados"].append({"grupo": "_global", "causa": "ERRO_INESPERADO", "detalhe": f"{exc.__class__.__name__}: {exc}"})
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
