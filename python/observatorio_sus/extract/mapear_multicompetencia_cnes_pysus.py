from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import tempfile
import time
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
    "5N4": "docs/migracao_python/05N4_mapeamento_estrutural_grupos_cnes_pysus.md",
}
DESC_GRUPO = {"ST": "estabelecimentos", "LT": "leitos", "SR": "serviços/classificação"}
CAMPOS_CHAVE = ["CNES", "CODUFMUN", "COMPETEN", "TPGESTAO", "NAT_JUR"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--modo", choices=["planejamento", "mapear_multicompetencia", "resumo"], default="planejamento")
    p.add_argument("--uf", default="ES")
    p.add_argument("--ano", type=int, default=2024)
    p.add_argument("--meses", nargs="+", type=int, default=[1, 6, 12])
    p.add_argument("--grupos", nargs="+", default=["ST", "LT", "SR"])
    p.add_argument("--tentativas", type=int, default=5)
    p.add_argument("--base-backoff", type=float, default=2.0)
    p.add_argument("--jitter-max", type=float, default=1.0)
    return p.parse_args()


def carregar_campos_contratos() -> tuple[list[str], dict[str, Any]]:
    info = {"carregado": False, "quantidade_campos_criticos": 0, "erro_importacao": None, "origem": "nao_inicializada"}
    try:
        if str(PYTHON_DIR) not in sys.path:
            sys.path.insert(0, str(PYTHON_DIR))
        from observatorio_sus.cnes import contratos

        campos = set()
        for cfg in contratos.CONTRATOS_TABELAS.values():
            campos.update(str(c) for c in cfg.get("campos_criticos", []))
        campos = sorted(campos)
        info.update({"carregado": True, "quantidade_campos_criticos": len(campos), "origem": "python/observatorio_sus/cnes/contratos.py"})
        return campos, info
    except Exception as exc:
        info.update({"erro_importacao": f"{exc.__class__.__name__}: {exc}", "origem": "falha_ao_importar_contratos"})
        return [], info


def classificar_erro(msg: str) -> str:
    s = msg.lower()
    if any(x in s for x in ["timeout", "connection", "network", "dns"]):
        return "ERRO_DE_REDE"
    if "dbc" in s:
        return "ERRO_DE_CONVERSAO_DBC"
    if any(x in s for x in ["cache", "duckdb", "config.db"]):
        return "ERRO_DE_CACHE_PYSUS"
    if any(x in s for x in ["group", "grupo"]) and any(x in s for x in ["invalid", "inválido", "invalido"]):
        return "ERRO_DE_GRUPO_CNES"
    if "not found" in s and "module" in s:
        return "DEPENDENCIA_AUSENTE"
    if "file" in s and "not found" in s:
        return "ARQUIVO_NAO_ENCONTRADO"
    return "OUTRO_ERRO_CONTROLADO"


def detectar_campos_chave(colunas: list[str]) -> list[str]:
    lower_cols = [c.lower() for c in colunas]
    encontrados = [c for c in CAMPOS_CHAVE if any(c.lower() in k for k in lower_cols)]
    return sorted(set(encontrados))


def detectar_riscos_coercao(colunas: list[str]) -> list[str]:
    fixos = {"CNES", "CODUFMUN", "CPF_CNPJ", "CNPJ_MAN", "COMPETEN", "TPGESTAO", "NAT_JUR", "CODLEITO", "CNESTERC"}
    out = {c for c in colunas if c.upper() in fixos}
    out.update(c for c in colunas if re.match(r"^(COD|CO_|CPF|CNPJ)", c.upper()))
    return sorted(out)


def avaliar_contratos(colunas: list[str], campos_contrato: list[str]) -> dict[str, Any]:
    norm = {c.lower(): c for c in colunas}
    literais = sorted([c for c in campos_contrato if c.lower() in norm])
    aproximados = sorted([c for c in campos_contrato if c.lower() not in norm and any(t in c.lower() for t in ["cnes", "unidade", "municipio", "gestao", "natureza", "habilitacao"])])
    ausentes = sorted([c for c in campos_contrato if c.lower() not in norm])
    if literais:
        tipo = "correspondência literal"
        cobertura = "COBERTURA_POTENCIAL_PARCIAL" if ausentes else "COBERTURA_POTENCIAL_FORTE"
    elif aproximados:
        tipo = "correspondência aproximada"
        cobertura = "COBERTURA_POTENCIAL_PARCIAL"
    else:
        tipo = "ausência"
        cobertura = "COBERTURA_NAO_CONFIRMADA"
    return {
        "relacao_com_contratos_tipo": tipo,
        "cobertura_contratos_status": cobertura,
        "campos_contratuais_literais": literais,
        "campos_contratuais_aproximados": aproximados,
        "campos_criticos_ausentes": ausentes,
    }


def executar_combinacao(args: argparse.Namespace, grupo: str, mes: int, campos_contrato: list[str]) -> dict[str, Any]:
    comp = f"{args.ano:04d}-{mes:02d}"
    out = {"grupo": grupo, "descricao_grupo": DESC_GRUPO.get(grupo, "nao_mapeado"), "competencia": comp,
           "chamada_executada": f"cnes(state='{args.uf}', year={args.ano}, month={mes}, group='{grupo}')",
           "tentativas_realizadas": 0, "sucesso": False, "tipo_retorno": None, "eh_dataframe": False,
           "numero_linhas": 0, "numero_colunas": 0, "colunas": [], "dtypes": {}, "campos_chave_detectados": [],
           "relacao_com_contratos_tipo": "não avaliado", "cobertura_contratos_status": "COBERTURA_INCONCLUSIVA",
           "campos_contratuais_literais": [], "campos_contratuais_aproximados": [], "campos_criticos_ausentes": [],
           "riscos_coercao": [], "classe_excecao": None, "mensagem_excecao": None,
           "causa_classificada": "OUTRO_ERRO_CONTROLADO", "persistiu_dados": False}

    from pysus import cnes

    for i in range(args.tentativas):
        out["tentativas_realizadas"] = i + 1
        try:
            ret = cnes(state=args.uf, year=args.ano, month=mes, group=grupo)
            out["tipo_retorno"] = type(ret).__name__
            if pd is not None and isinstance(ret, pd.DataFrame):
                out["eh_dataframe"] = True
                out["sucesso"] = True
                out["numero_linhas"] = int(ret.shape[0])
                out["numero_colunas"] = int(ret.shape[1])
                out["colunas"] = [str(c) for c in ret.columns]
                out["dtypes"] = {str(c): str(dt) for c, dt in ret.dtypes.astype(str).items()}
                out["campos_chave_detectados"] = detectar_campos_chave(out["colunas"])
                out["riscos_coercao"] = detectar_riscos_coercao(out["colunas"])
                out.update(avaliar_contratos(out["colunas"], campos_contrato))
                out["causa_classificada"] = "GRUPO_ACEITO_COM_RETORNO" if out["numero_linhas"] > 0 else "GRUPO_ACEITO_RETORNO_VAZIO"
            else:
                out["sucesso"] = True
                out["causa_classificada"] = "RETORNO_NAO_DATAFRAME"
            break
        except Exception as exc:
            out["classe_excecao"] = exc.__class__.__name__
            out["mensagem_excecao"] = str(exc)
            out["causa_classificada"] = classificar_erro(f"{exc.__class__.__name__}: {exc}")
            if i < args.tentativas - 1:
                time.sleep((args.base_backoff * (2**i)) + random.uniform(0, args.jitter_max))
    return out


def gerar_matrizes(resultados: list[dict[str, Any]], grupos: list[str]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    por_grupo: dict[str, list[dict[str, Any]]] = {g: [r for r in resultados if r["grupo"] == g] for g in grupos}
    mcols: dict[str, Any] = {}
    mdtypes: dict[str, Any] = {}
    mkeys: dict[str, Any] = {}
    mcont: dict[str, Any] = {}
    diffs: dict[str, Any] = {}
    for g, regs in por_grupo.items():
        regs_sorted = sorted(regs, key=lambda r: r["competencia"])
        ref = next((r for r in regs_sorted if r["competencia"].endswith("-01")), regs_sorted[0] if regs_sorted else None)
        ref_cols = set(ref["colunas"]) if ref else set()
        ref_dtypes = ref["dtypes"] if ref else {}
        ref_keys = set(ref["campos_chave_detectados"]) if ref else set()
        mcols[g] = {r["competencia"]: r["colunas"] for r in regs_sorted}
        mdtypes[g] = {r["competencia"]: r["dtypes"] for r in regs_sorted}
        mkeys[g] = {r["competencia"]: r["campos_chave_detectados"] for r in regs_sorted}
        mcont[g] = {r["competencia"]: {"tipo": r["relacao_com_contratos_tipo"], "cobertura": r["cobertura_contratos_status"]} for r in regs_sorted}
        diffs[g] = {}
        for r in regs_sorted:
            cset = set(r["colunas"])
            added = sorted(cset - ref_cols)
            removed = sorted(ref_cols - cset)
            dtype_changes = sorted([c for c in set(ref_dtypes) & set(r["dtypes"]) if ref_dtypes[c] != r["dtypes"][c]])
            keys = set(r["campos_chave_detectados"])
            diffs[g][r["competencia"]] = {
                "referencia": ref["competencia"] if ref else None,
                "colunas_adicionadas": added,
                "colunas_removidas": removed,
                "dtypes_alterados": dtype_changes,
                "campos_chave_apareceram": sorted(keys - ref_keys),
                "campos_chave_desapareceram": sorted(ref_keys - keys),
                "alteracao_qtd_colunas": r["numero_colunas"] - (ref["numero_colunas"] if ref else 0),
                "alteracao_qtd_linhas": r["numero_linhas"] - (ref["numero_linhas"] if ref else 0),
            }
    return mcols, mdtypes, mkeys, mcont, diffs


def main() -> int:
    args = parse_args()
    campos_contrato, contratos_info = carregar_campos_contratos()
    payload: dict[str, Any] = {
        "ambiente": {"python": sys.version, "timestamp_utc": datetime.now(timezone.utc).isoformat()},
        "parametros": {"modo": args.modo, "uf": args.uf, "ano": args.ano, "meses": args.meses, "grupos": args.grupos},
        "cadeia_documental": {k: (REPO / v).exists() for k, v in DOCS_CADEIA.items()},
        "isolamento": {"home_temporario": True, "xdg_config_home_temporario": True, "xdg_cache_home_temporario": True},
        "retry": {"tentativas": args.tentativas, "base_backoff": args.base_backoff, "jitter_max": args.jitter_max},
        "usa_api_publica_pysus": True,
        "contratos_cnes": contratos_info,
        "resultados_por_competencia": [],
        "matriz_estabilidade_colunas": {},
        "matriz_estabilidade_dtypes": {},
        "matriz_campos_chave": {},
        "matriz_contratos": {},
        "riscos_coercao_codigos": {},
        "diferencas_estruturais": {},
        "erros_controlados": [],
        "conclusao": {},
        "proxima_recomendacao": "",
    }

    if args.modo in {"planejamento", "resumo"}:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    try:
        with tempfile.TemporaryDirectory(prefix="pysus-5n5-") as temp_dir:
            os.environ["HOME"] = temp_dir
            os.environ["XDG_CONFIG_HOME"] = f"{temp_dir}/.config"
            os.environ["XDG_CACHE_HOME"] = f"{temp_dir}/.cache"

            for grupo in args.grupos:
                for mes in args.meses:
                    r = executar_combinacao(args, grupo, mes, campos_contrato)
                    payload["resultados_por_competencia"].append(r)
                    payload["riscos_coercao_codigos"][f"{grupo}-{r['competencia']}"] = r["riscos_coercao"]
                    if not r["sucesso"]:
                        payload["erros_controlados"].append({"grupo": grupo, "competencia": r["competencia"], "causa": r["causa_classificada"], "mensagem": r["mensagem_excecao"]})

        mcols, mdtypes, mkeys, mcont, diffs = gerar_matrizes(payload["resultados_por_competencia"], args.grupos)
        payload["matriz_estabilidade_colunas"] = mcols
        payload["matriz_estabilidade_dtypes"] = mdtypes
        payload["matriz_campos_chave"] = mkeys
        payload["matriz_contratos"] = mcont
        payload["diferencas_estruturais"] = diffs

        por_grupo = {g: [r for r in payload["resultados_por_competencia"] if r["grupo"] == g] for g in args.grupos}
        col_estavel = {g: len({tuple(r["colunas"]) for r in rs if r["eh_dataframe"]}) <= 1 for g, rs in por_grupo.items()}
        dtype_estavel = {g: len({json.dumps(r["dtypes"], sort_keys=True, ensure_ascii=False) for r in rs if r["eh_dataframe"]}) <= 1 for g, rs in por_grupo.items()}
        keys_estavel = {g: len({tuple(r["campos_chave_detectados"]) for r in rs if r["eh_dataframe"]}) <= 1 for g, rs in por_grupo.items()}

        payload["conclusao"] = {
            "todas_combinacoes_retornaram_dataframe": all(r["eh_dataframe"] for r in payload["resultados_por_competencia"]),
            "colunas_estaveis_por_grupo": col_estavel,
            "dtypes_estaveis_por_grupo": dtype_estavel,
            "campos_chave_estaveis_por_grupo": keys_estavel,
            "ha_risco_relevante_coercao": any(bool(r["riscos_coercao"]) for r in payload["resultados_por_competencia"]),
            "pode_testar_janela_maior": all(r["eh_dataframe"] for r in payload["resultados_por_competencia"]),
            "substituicao_r": "Não. Nenhum script R pode ser substituído nesta etapa.",
        }
        payload["proxima_recomendacao"] = "Etapa 5N.6 — desenho do contrato intermediário PySUS→CNES sem geração de base." if payload["conclusao"]["pode_testar_janela_maior"] else "Retestar combinações com falha controlada antes de ampliar janela."

        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        payload["erros_controlados"].append({"grupo": "_global", "causa": "OUTRO_ERRO_CONTROLADO", "mensagem": f"{exc.__class__.__name__}: {exc}"})
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
