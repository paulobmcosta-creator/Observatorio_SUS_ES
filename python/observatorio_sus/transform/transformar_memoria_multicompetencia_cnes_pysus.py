#!/usr/bin/env python3
"""Etapa 5N.7-8 — transformação em memória multi-competência PySUS→CNES.

Este script executa somente transformações exploratórias em memória. Ele não
persiste DataFrames, não cria CO_UNIDADE artificial, não faz joins relacionais e
não substitui scripts R.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import platform
import queue
import random
import socket
import sys
import tempfile
import time
from collections.abc import Iterable
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from observatorio_sus.cnes.contrato_intermediario_pysus_cnes import (  # noqa: E402
    filtrar_equivalencias_por_grupo,
)

DOCUMENTOS_CADEIA = [
    "docs/migracao_python/05N_reinicio_cnes_python_api_pysus.md",
    "docs/migracao_python/05N1_isolamento_pysus_duckdb_cnes.md",
    "docs/migracao_python/05N2_diagnostico_falha_cnes_pos_isolamento.md",
    "docs/migracao_python/05N3_inventario_grupos_cnes_pysus.md",
    "docs/migracao_python/05N3R_reteste_controlado_st_cnes_pysus.md",
    "docs/migracao_python/05N4_mapeamento_estrutural_grupos_cnes_pysus.md",
    "docs/migracao_python/05N5_mapeamento_multicompetencia_cnes_pysus.md",
    "docs/migracao_python/05N6_contrato_intermediario_pysus_cnes.md",
    "docs/migracao_python/05N6R_deliberacao_humana_contrato_intermediario_pysus_cnes.md",
    "python/observatorio_sus/cnes/contrato_intermediario_pysus_cnes.py",
    "metadata/cnes/contrato_intermediario_pysus_cnes.csv",
]

STATUS_RENOMEAVEIS = {"CONFIRMADA_NOMINALMENTE", "POTENCIAL_A_CONFIRMAR"}
CAMPOS_TEXTO_EXPLICITOS = {
    "CNES",
    "CODUFMUN",
    "COMPETEN",
    "TPGESTAO",
    "NAT_JUR",
    "CPF_CNPJ",
    "CNPJ_MAN",
    "CNESTERC",
}
PREFIXOS_TEXTO = ("COD", "CO_", "CPF", "CNPJ")


def normalizar_grupos(grupos: Iterable[str]) -> list[str]:
    return [grupo.upper() for grupo in grupos]


def competencia(ano: int, mes: int) -> str:
    return f"{ano:04d}-{mes:02d}"


def tipo_json(valor: Any) -> Any:
    if isinstance(valor, dict):
        return {str(chave): tipo_json(item) for chave, item in valor.items()}
    if isinstance(valor, list):
        return [tipo_json(item) for item in valor]
    return valor


def arquivos_cadeia() -> list[dict[str, Any]]:
    return [{"arquivo": caminho, "existe": Path(caminho).is_file()} for caminho in DOCUMENTOS_CADEIA]


def aplicar_isolamento_pysus(tmp_home: str) -> dict[str, str]:
    xdg_config_home = str(Path(tmp_home) / "xdg_config")
    xdg_cache_home = str(Path(tmp_home) / "xdg_cache")
    Path(xdg_config_home).mkdir(parents=True, exist_ok=True)
    Path(xdg_cache_home).mkdir(parents=True, exist_ok=True)
    os.environ["HOME"] = tmp_home
    os.environ["XDG_CONFIG_HOME"] = xdg_config_home
    os.environ["XDG_CACHE_HOME"] = xdg_cache_home
    return {
        "aplicado": True,
        "home_temporario": tmp_home,
        "xdg_config_home_temporario": xdg_config_home,
        "xdg_cache_home_temporario": xdg_cache_home,
    }


def criar_resultado_base(grupo: str, ano: int, mes: int) -> dict[str, Any]:
    return {
        "grupo": grupo,
        "competencia": competencia(ano, mes),
        "linhas_antes": None,
        "colunas_antes": 0,
        "colunas_depois": 0,
        "linhas_depois": None,
        "colunas_renomeadas": [],
        "colunas_preservadas_texto": [],
        "colunas_quantitativas_preservadas": [],
        "campos_pendentes": ["CO_UNIDADE"],
        "co_unidade_criado": False,
        "join_relacional_executado": False,
        "persistiu_dados": False,
        "tipos_antes": {},
        "tipos_depois": {},
        "sucesso": False,
        "causa_classificada": "NAO_EXECUTADO",
        "mensagem_excecao": "",
        "tentativas_executadas": 0,
        "tempo_segundos": None,
        "tempo_limite_usado": None,
        "timeout_controlado": False,
        "caminho_execucao": None,
        "retornou_dataframe": False,
        "renomeacoes": 0,
    }


def montar_payload_base(args: argparse.Namespace) -> dict[str, Any]:
    cadeia = arquivos_cadeia()
    return {
        "ambiente": {
            "python": sys.version.split()[0],
            "python_executavel": sys.executable,
            "plataforma": platform.platform(),
            "cwd": str(Path.cwd()),
            "hostname": socket.gethostname(),
        },
        "parametros": {
            "modo": args.modo,
            "uf": args.uf.upper(),
            "ano": args.ano,
            "meses": args.meses,
            "grupos": normalizar_grupos(args.grupos),
            "timeout_por_chamada": args.timeout_por_chamada,
            "timeout_global": args.timeout_global,
            "usar_subprocesso": args.usar_subprocesso,
        },
        "cadeia_documental": {
            "itens": cadeia,
            "completa": all(item["existe"] for item in cadeia),
        },
        "isolamento": {
            "aplicado": False,
            "descricao": "HOME, XDG_CONFIG_HOME e XDG_CACHE_HOME temporarios apenas no modo transformar_memoria.",
        },
        "retry": {
            "tentativas": args.tentativas,
            "base_backoff": args.base_backoff,
            "jitter_max": args.jitter_max,
            "timeout_por_chamada": args.timeout_por_chamada,
            "timeout_global": args.timeout_global,
        },
        "timeout_controlado_ativo": True,
        "justificativa_timeout": "Evitar travamento indefinido de chamadas PySUS/CNES e garantir saida auditavel.",
        "classificacao_timeout": "TIMEOUT_CONTROLADO",
        "caminho_padrao_transformacao": "direto_sem_subprocesso",
        "subprocesso_disponivel": True,
        "subprocesso_padrao": False,
        "justificativa_caminho_padrao": "diagnóstico 5N.7-8D indicou timeout causado por subprocesso",
        "observacao_timeout_caminho_direto": "No caminho direto, timeout_por_chamada e timeout_global sao registrados como metadados/controle global, sem kill de subprocesso.",
        "usa_api_publica_pysus": {
            "usa": True,
            "import_operacional": "from pysus import cnes",
            "chamada_operacional": "cnes(state=uf, year=ano, month=mes, group=grupo)",
            "import_apos_isolamento": True,
        },
        "contrato_intermediario": {
            "arquivo_python": "python/observatorio_sus/cnes/contrato_intermediario_pysus_cnes.py",
            "arquivo_csv": "metadata/cnes/contrato_intermediario_pysus_cnes.csv",
            "minimo_nao_exaustivo": True,
        },
        "regras_transformacao": {
            "renomeacao_controlada": [
                "status_equivalencia em CONFIRMADA_NOMINALMENTE ou POTENCIAL_A_CONFIRMAR",
                "tipo_equivalencia diferente de AUSENTE_NO_PYSUS",
                "coluna_pysus existente no DataFrame",
                "campo_contrato_cnes diferente de CO_UNIDADE",
            ],
            "preservacao_textual": [
                "CNES",
                "CODUFMUN",
                "COMPETEN",
                "TPGESTAO",
                "NAT_JUR",
                "CPF_CNPJ",
                "CNPJ_MAN",
                "CNESTERC",
                "COD*",
                "CO_*",
                "CPF*",
                "CNPJ*",
            ],
            "regra_qt": "QT_* permanece numerico se ja vier numerico; QT_* textual nao e coercido para numerico.",
            "competencia_normalizada": "Criada apenas em memoria como AAAA-MM quando COMPETEN existir.",
            "proibicoes": [
                "Nunca renomear CNES para CO_UNIDADE",
                "Nunca criar CO_UNIDADE artificial",
                "Nunca executar join relacional",
                "Nunca persistir DataFrame, CSV, Parquet, DBC ou DBF",
                "Nunca escrever em data_raw, data_interim ou data_processed",
                "Nunca substituir scripts R nesta etapa",
            ],
        },
        "resultados_por_competencia": [],
        "matriz_transformacao": [],
        "matriz_preservacao_textual": [],
        "matriz_tipos_antes_depois": [],
        "matriz_colunas_renomeadas": [],
        "matriz_campos_pendentes": [],
        "matriz_campos_nao_transformados": [],
        "riscos_coercao_codigos": [
            "Identificadores CNES/COD*/CO_*/CPF*/CNPJ*/CNESTERC exigem preservacao textual em memoria.",
            "CO_UNIDADE permanece ausente ou inconclusivo no contrato intermediario e nao pode ser inferido.",
        ],
        "erros_controlados": [],
        "classificacao_etapa": "PLANEJAMENTO_TRANSFORMACAO_MEMORIA",
        "classificacao_validacao_minima": None,
        "conclusao": "Planejamento estruturado; transformacao operacional nao executada neste modo.",
        "diagnostico_sem_subprocesso": [],
        "proxima_recomendacao": "5N.7-8D — diagnostico comparativo entre mapeamento funcional e transformacao com timeout.",
    }


def coluna_deve_ser_texto(coluna: str) -> bool:
    nome = coluna.upper()
    return nome in CAMPOS_TEXTO_EXPLICITOS or nome.startswith(PREFIXOS_TEXTO)


def preservar_texto_em_memoria(df: pd.DataFrame) -> list[str]:
    colunas_preservadas = []
    for coluna in df.columns:
        if coluna.upper().startswith("QT_"):
            continue
        if coluna_deve_ser_texto(coluna):
            df[coluna] = df[coluna].astype("string")
            colunas_preservadas.append(coluna)
    return sorted(set(colunas_preservadas))


def mapa_renomeacao(grupo: str, colunas: Iterable[str]) -> tuple[dict[str, str], list[dict[str, Any]], list[str]]:
    colunas_existentes = set(colunas)
    renomear: dict[str, str] = {}
    matriz: list[dict[str, Any]] = []
    pendentes = ["CO_UNIDADE"]

    for equivalencia in filtrar_equivalencias_por_grupo(grupo):
        origem = str(equivalencia["coluna_pysus"])
        destino = str(equivalencia["campo_contrato_cnes"])
        if destino == "CO_UNIDADE":
            continue
        if (
            equivalencia["status_equivalencia"] in STATUS_RENOMEAVEIS
            and equivalencia["tipo_equivalencia"] != "AUSENTE_NO_PYSUS"
            and origem in colunas_existentes
        ):
            renomear[origem] = destino
            matriz.append(
                {
                    "grupo": grupo,
                    "coluna_original_pysus": origem,
                    "coluna_transformada": destino,
                    "tipo_equivalencia": equivalencia["tipo_equivalencia"],
                    "observacao": equivalencia["observacao"],
                }
            )
    return renomear, matriz, pendentes


def transformar_dataframe_em_memoria(df: Any, grupo: str, ano: int, mes: int) -> dict[str, Any]:
    import pandas as pd

    resultado = criar_resultado_base(grupo, ano, mes)
    resultado["linhas_antes"] = int(len(df))
    resultado["colunas_antes"] = int(len(df.columns))
    resultado["tipos_antes"] = {coluna: str(dtype) for coluna, dtype in df.dtypes.items()}

    renomear, matriz_renomeadas, pendentes = mapa_renomeacao(grupo, df.columns)
    df = df.rename(columns=renomear)
    colunas_texto = preservar_texto_em_memoria(df)

    if "COMPETEN" in df.columns:
        df["competencia_normalizada"] = (
            df["COMPETEN"].astype("string").str.slice(0, 4)
            + "-"
            + df["COMPETEN"].astype("string").str.slice(4, 6)
        )

    colunas_qt = [coluna for coluna in df.columns if coluna.upper().startswith("QT_")]
    qt_numericas = [coluna for coluna in colunas_qt if pd.api.types.is_numeric_dtype(df[coluna])]
    qt_textuais = [coluna for coluna in colunas_qt if pd.api.types.is_string_dtype(df[coluna]) or df[coluna].dtype == object]

    resultado["linhas_depois"] = int(len(df))
    resultado["colunas_depois"] = int(len(df.columns))
    resultado["tipos_depois"] = {coluna: str(dtype) for coluna, dtype in df.dtypes.items()}
    resultado["colunas_renomeadas"] = sorted(renomear.keys())
    resultado["renomeacoes"] = len(renomear)
    resultado["retornou_dataframe"] = True
    resultado["colunas_preservadas_texto"] = colunas_texto
    resultado["colunas_quantitativas_preservadas"] = qt_numericas
    resultado["campos_pendentes"] = sorted(set(resultado["campos_pendentes"] + pendentes))
    resultado["matriz_colunas_renomeadas"] = matriz_renomeadas
    resultado["campos_qt_textuais_nao_coercidos"] = qt_textuais

    textos_validos = all(str(df[coluna].dtype) in {"string", "object"} for coluna in colunas_texto)
    linhas_preservadas = resultado["linhas_antes"] == resultado["linhas_depois"]
    co_unidade_nao_criado = "CO_UNIDADE" not in df.columns
    resultado["co_unidade_criado"] = not co_unidade_nao_criado
    resultado["sucesso"] = bool(linhas_preservadas and co_unidade_nao_criado and textos_validos)
    resultado["causa_classificada"] = "SUCESSO" if resultado["sucesso"] else "VALIDACAO_INTERNA"
    return resultado


def worker_chamada_pysus(fila: mp.Queue, uf: str, ano: int, mes: int, grupo: str) -> None:
    import pandas as pd
    from pysus import cnes

    inicio = time.monotonic()
    try:
        df = cnes(state=uf, year=ano, month=mes, group=grupo)
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"PySUS retornou {type(df)!r}, nao pandas.DataFrame")
        resultado = transformar_dataframe_em_memoria(df, grupo, ano, mes)
        resultado["tempo_segundos"] = round(time.monotonic() - inicio, 3)
        resultado["caminho_execucao"] = "subprocesso"
        fila.put({"ok": True, "resultado": resultado})
    except Exception as exc:  # noqa: BLE001
        fila.put({"ok": False, "erro": f"{type(exc).__name__}: {exc}", "tempo_segundos": round(time.monotonic() - inicio, 3)})


def executar_chamada_com_timeout(uf: str, ano: int, mes: int, grupo: str, timeout: float) -> dict[str, Any]:
    fila: mp.Queue = mp.Queue(maxsize=1)
    processo = mp.Process(target=worker_chamada_pysus, args=(fila, uf, ano, mes, grupo))
    processo.start()
    processo.join(timeout)
    if processo.is_alive():
        processo.terminate()
        processo.join(5)
        return {
            "ok": False,
            "erro": f"TIMEOUT_CHAMADA_APOS_{timeout}_SEGUNDOS",
            "tempo_segundos": timeout,
            "tempo_limite_usado": timeout,
            "timeout_controlado": True,
            "caminho_execucao": "subprocesso",
        }
    try:
        return fila.get_nowait()
    except queue.Empty:
        return {"ok": False, "erro": f"PROCESSO_SEM_RETORNO_EXITCODE_{processo.exitcode}", "tempo_segundos": None}


def classificar_causa(mensagem: str) -> str:
    texto = mensagem.upper()
    if "TIMEOUT" in texto:
        return "TIMEOUT_CONTROLADO"
    if any(padrao in texto for padrao in ["HTTP", "CONNECTION", "FTP", "NETWORK"]):
        return "FALHA_REDE_API_CONTROLADA"
    return "ERRO_CONTROLADO"


def fase_mais_lenta(tempos: dict[str, float | None]) -> str | None:
    tempos_validos = {fase: tempo for fase, tempo in tempos.items() if isinstance(tempo, int | float)}
    if not tempos_validos:
        return None
    return max(tempos_validos, key=tempos_validos.get)


def tempos_st_fases_base() -> dict[str, float | None]:
    return {
        "isolamento": None,
        "import_pysus": None,
        "chamada_cnes": None,
        "leitura_retorno_dataframe": None,
        "coleta_colunas": None,
        "coleta_dtypes": None,
        "deteccao_campos_textuais": None,
        "aplicacao_preservacao_textual": None,
        "aplicacao_renomeacoes": None,
        "validacao_linhas_antes_depois": None,
        "verificacao_co_unidade": None,
        "geracao_metadados": None,
        "serializacao_json": None,
    }


def executar_com_retry(args: argparse.Namespace, grupo: str, mes: int, inicio_global: float) -> dict[str, Any]:
    uf = args.uf.upper()
    resultado = criar_resultado_base(grupo, args.ano, mes)
    resultado["caminho_execucao"] = "subprocesso"
    erros: list[str] = []

    for tentativa in range(1, args.tentativas + 1):
        decorrido = time.monotonic() - inicio_global
        if decorrido >= args.timeout_global:
            resultado["tentativas_executadas"] = tentativa - 1
            resultado["causa_classificada"] = "LIMITE_GLOBAL_CONTROLADO"
            resultado["mensagem_excecao"] = f"Limite global de {args.timeout_global}s atingido antes da chamada."
            resultado["tempo_limite_usado"] = args.timeout_global
            return resultado

        restante_global = max(1.0, args.timeout_global - decorrido)
        timeout = min(args.timeout_por_chamada, restante_global)
        resposta = executar_chamada_com_timeout(uf, args.ano, mes, grupo, timeout)
        resultado["tentativas_executadas"] = tentativa
        resultado["caminho_execucao"] = resposta.get("caminho_execucao", "subprocesso")
        if resposta.get("ok"):
            resultado = resposta["resultado"]
            resultado["tentativas_executadas"] = tentativa
            return resultado

        mensagem = str(resposta.get("erro", "erro desconhecido"))
        resultado["tempo_limite_usado"] = resposta.get("tempo_limite_usado", timeout)
        resultado["timeout_controlado"] = bool(resposta.get("timeout_controlado", False))
        erros.append(mensagem)
        if "TIMEOUT" in mensagem.upper():
            resultado["timeout_controlado"] = True
            break
        if tentativa < args.tentativas and (time.monotonic() - inicio_global) < args.timeout_global:
            espera = min(args.base_backoff ** tentativa + random.uniform(0, args.jitter_max), 5.0)
            time.sleep(espera)

    resultado["causa_classificada"] = classificar_causa(" | ".join(erros))
    resultado["timeout_controlado"] = resultado["causa_classificada"] == "TIMEOUT_CONTROLADO"
    resultado["mensagem_excecao"] = " | ".join(erros)
    return resultado


def registrar_matrizes(payload: dict[str, Any], resultado: dict[str, Any]) -> None:
    payload["matriz_transformacao"].append(
        {
            "grupo": resultado["grupo"],
            "competencia": resultado["competencia"],
            "caminho_execucao": resultado.get("caminho_execucao"),
            "retornou_dataframe": resultado.get("retornou_dataframe", False),
            "renomeacoes_aplicadas": resultado.get("renomeacoes", len(resultado["colunas_renomeadas"])),
            "co_unidade_criado": resultado["co_unidade_criado"],
            "join_relacional_executado": resultado["join_relacional_executado"],
            "persistiu_dados": resultado["persistiu_dados"],
            "sucesso": resultado["sucesso"],
            "causa_classificada": resultado["causa_classificada"],
        }
    )
    payload["matriz_preservacao_textual"].append(
        {
            "grupo": resultado["grupo"],
            "competencia": resultado["competencia"],
            "campos_preservados_como_texto": resultado["colunas_preservadas_texto"],
        }
    )
    payload["matriz_tipos_antes_depois"].append(
        {
            "grupo": resultado["grupo"],
            "competencia": resultado["competencia"],
            "tipos_antes": resultado["tipos_antes"],
            "tipos_depois": resultado["tipos_depois"],
        }
    )
    payload["matriz_colunas_renomeadas"].extend(resultado.pop("matriz_colunas_renomeadas", []))
    payload["matriz_campos_pendentes"].append(
        {"grupo": resultado["grupo"], "competencia": resultado["competencia"], "campos": resultado["campos_pendentes"]}
    )
    payload["matriz_campos_nao_transformados"].append(
        {"grupo": resultado["grupo"], "competencia": resultado["competencia"], "campos": ["CO_UNIDADE"]}
    )
    if not resultado["sucesso"]:
        payload["erros_controlados"].append(
            {
                "grupo": resultado["grupo"],
                "competencia": resultado["competencia"],
                "causa_classificada": resultado["causa_classificada"],
                "mensagem": resultado["mensagem_excecao"],
                "tempo_limite_usado": resultado.get("tempo_limite_usado"),
                "timeout_controlado": resultado.get("timeout_controlado", False),
                "persistiu_dados": resultado.get("persistiu_dados", False),
            }
        )


def executar_planejamento(args: argparse.Namespace) -> dict[str, Any]:
    payload = montar_payload_base(args)
    payload["conclusao"] = "Planejamento concluido sem acesso a rede e sem escrita em data_*."
    return payload


def executar_transformacao_memoria(args: argparse.Namespace) -> dict[str, Any]:
    payload = montar_payload_base(args)
    if not payload["cadeia_documental"]["completa"]:
        payload["conclusao"] = "Cadeia documental/metodologica incompleta; execucao interrompida."
        return payload

    inicio_global = time.monotonic()
    if args.usar_subprocesso:
        with tempfile.TemporaryDirectory(prefix="observatorio-sus-5n7-8-") as tmp_home:
            payload["isolamento"] = aplicar_isolamento_pysus(tmp_home)
            payload["isolamento"]["import_pysus_ocorre_no_worker_apos_isolamento"] = True
            payload["caminho_execucao_efetivo"] = "subprocesso"

            for grupo in normalizar_grupos(args.grupos):
                for mes in args.meses:
                    resultado = executar_com_retry(args, grupo, mes, inicio_global)
                    registrar_matrizes(payload, resultado)
                    payload["resultados_por_competencia"].append(resultado)
    else:
        payload["caminho_execucao_efetivo"] = "direto_sem_subprocesso"
        payload["isolamento"]["descricao"] = "Aplicado por combinacao no proprio processo antes do import direto do PySUS."
        for grupo in normalizar_grupos(args.grupos):
            for mes in args.meses:
                resultado = executar_diagnostico_direto_combinacao(args, grupo, mes)
                resultado["modo_diagnostico"] = None
                resultado["caminho_execucao"] = "direto_sem_subprocesso"
                registrar_matrizes(payload, resultado)
                payload["resultados_por_competencia"].append(resultado)

    total = len(payload["resultados_por_competencia"])
    sucessos = sum(1 for item in payload["resultados_por_competencia"] if item["sucesso"])
    todos_timeout = bool(total) and all(
        item["causa_classificada"] == "TIMEOUT_CONTROLADO" for item in payload["resultados_por_competencia"]
    )
    competencia_unica = len(args.meses) == 1
    if todos_timeout:
        payload["classificacao_etapa"] = "TRANSFORMACAO_MEMORIA_NAO_AVALIADA_POR_TIMEOUT"
        payload["classificacao_validacao_minima"] = "TRANSFORMACAO_MEMORIA_MINIMA_NAO_AVALIADA_POR_TIMEOUT"
        payload["conclusao"] = "Transformacao em memoria nao avaliada operacionalmente: todas as combinacoes retornaram TIMEOUT_CONTROLADO."
    elif sucessos == total:
        if competencia_unica and len(normalizar_grupos(args.grupos)) > 1:
            payload["classificacao_etapa"] = "TRANSFORMACAO_MEMORIA_COMPETENCIA_UNICA_CONCLUIDA_COM_RESSALVAS"
        else:
            payload["classificacao_etapa"] = "TRANSFORMACAO_MEMORIA_MINIMA_CONCLUIDA_COM_RESSALVAS"
        payload["classificacao_validacao_minima"] = "TRANSFORMACAO_MEMORIA_MINIMA_CONCLUIDA_COM_RESSALVAS"
        payload["conclusao"] = "Transformacao em memoria concluida para todas as combinacoes executadas, com CO_UNIDADE ainda pendente."
    elif sucessos > 0:
        payload["classificacao_etapa"] = "TRANSFORMACAO_MEMORIA_MINIMA_PARCIAL"
        payload["classificacao_validacao_minima"] = "TRANSFORMACAO_MEMORIA_MINIMA_PARCIAL"
        payload["conclusao"] = f"Transformacao em memoria parcial: {sucessos}/{total} combinacoes transformadas."
    else:
        payload["classificacao_etapa"] = "TRANSFORMACAO_MEMORIA_MINIMA_FALHOU"
        payload["classificacao_validacao_minima"] = "TRANSFORMACAO_MEMORIA_MINIMA_FALHOU"
        payload["conclusao"] = "Nenhuma combinacao foi transformada; falhas controladas registradas sem persistencia."
    return payload


def executar_diagnostico_direto_combinacao(args: argparse.Namespace, grupo: str, mes: int) -> dict[str, Any]:
    diagnostico = criar_resultado_base(grupo, args.ano, mes)
    diagnostico.update(
        {
            "modo_diagnostico": "diagnostico_sem_subprocesso",
            "usa_subprocesso": False,
            "caminho_execucao": "direto_sem_subprocesso",
            "retornou_dataframe": False,
            "tempos_fases": {
                "isolamento": None,
                "import_pysus": None,
                "chamada_cnes": None,
                "transformacao": None,
                "geracao_metadados": None,
            },
            "erro_classe": None,
            "erro_mensagem": None,
        }
    )

    inicio_total = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="observatorio-sus-5n7-8d-") as tmp_home:
        inicio = time.monotonic()
        isolamento = aplicar_isolamento_pysus(tmp_home)
        diagnostico["tempos_fases"]["isolamento"] = round(time.monotonic() - inicio, 3)
        diagnostico["isolamento"] = isolamento

        inicio = time.monotonic()
        import pandas as pd
        from pysus import cnes

        diagnostico["tempos_fases"]["import_pysus"] = round(time.monotonic() - inicio, 3)

        try:
            df = None
            erros = []
            inicio_chamada = time.monotonic()
            for tentativa in range(1, args.tentativas + 1):
                diagnostico["tentativas_executadas"] = tentativa
                try:
                    df = cnes(state=args.uf.upper(), year=args.ano, month=mes, group=grupo)
                    break
                except Exception as exc:  # noqa: BLE001
                    mensagem = f"{type(exc).__name__}: {exc}"
                    erros.append(mensagem)
                    if "TIMEOUT" in mensagem.upper():
                        break
                    if tentativa < args.tentativas:
                        espera = min(args.base_backoff ** tentativa + random.uniform(0, args.jitter_max), 5.0)
                        time.sleep(espera)

            diagnostico["tempos_fases"]["chamada_cnes"] = round(time.monotonic() - inicio_chamada, 3)
            if df is None:
                mensagem = " | ".join(erros) if erros else "PySUS nao retornou DataFrame"
                diagnostico["causa_classificada"] = classificar_causa(mensagem)
                diagnostico["timeout_controlado"] = diagnostico["causa_classificada"] == "TIMEOUT_CONTROLADO"
                diagnostico["mensagem_excecao"] = mensagem
                diagnostico["erro_mensagem"] = mensagem
                diagnostico["tempo_segundos"] = round(time.monotonic() - inicio_total, 3)
                diagnostico["tempos_fases"]["geracao_metadados"] = 0.0
                return diagnostico

            diagnostico["retornou_dataframe"] = isinstance(df, pd.DataFrame)
            if not diagnostico["retornou_dataframe"]:
                diagnostico["causa_classificada"] = "RETORNO_NAO_DATAFRAME"
                diagnostico["mensagem_excecao"] = f"PySUS retornou {type(df)!r}"
                diagnostico["tempo_segundos"] = round(time.monotonic() - inicio_total, 3)
                diagnostico["tempos_fases"]["geracao_metadados"] = 0.0
                return diagnostico

            inicio = time.monotonic()
            transformado = transformar_dataframe_em_memoria(df, grupo, args.ano, mes)
            diagnostico["tempos_fases"]["transformacao"] = round(time.monotonic() - inicio, 3)

            inicio = time.monotonic()
            transformado.pop("matriz_colunas_renomeadas", None)
            diagnostico.update(transformado)
            diagnostico["modo_diagnostico"] = "diagnostico_sem_subprocesso"
            diagnostico["usa_subprocesso"] = False
            diagnostico["retornou_dataframe"] = True
            diagnostico["caminho_execucao"] = "direto_sem_subprocesso"
            diagnostico["tempos_fases"]["geracao_metadados"] = round(time.monotonic() - inicio, 3)
            diagnostico["tempo_segundos"] = round(time.monotonic() - inicio_total, 3)
            return diagnostico
        except Exception as exc:  # noqa: BLE001
            diagnostico["erro_classe"] = type(exc).__name__
            diagnostico["erro_mensagem"] = str(exc)
            diagnostico["mensagem_excecao"] = f"{type(exc).__name__}: {exc}"
            diagnostico["causa_classificada"] = classificar_causa(diagnostico["mensagem_excecao"])
            diagnostico["timeout_controlado"] = diagnostico["causa_classificada"] == "TIMEOUT_CONTROLADO"
            diagnostico["tempo_segundos"] = round(time.monotonic() - inicio_total, 3)
            diagnostico["tempos_fases"]["geracao_metadados"] = 0.0
            return diagnostico


def executar_diagnostico_st_fases(args: argparse.Namespace) -> dict[str, Any]:
    """Diagnostica fases da transformação ST 2024-01 sem persistir dados."""

    payload = montar_payload_base(args)
    uf = "ES"
    ano = 2024
    mes = 1
    grupo = "ST"
    tempos_por_fase = tempos_st_fases_base()
    resultado = criar_resultado_base(grupo, ano, mes)
    resultado.update(
        {
            "modo_diagnostico": "diagnostico_st_fases",
            "caminho_execucao": "direto_sem_subprocesso",
            "usa_subprocesso": False,
            "escopo_forcado": {"uf": uf, "ano": ano, "mes": mes, "grupo": grupo},
            "retornou_dataframe": False,
            "transformação_executada": False,
            "transformacao_executada": False,
            "preservação_textual_executada": False,
            "preservacao_textual_executada": False,
            "renomeação_executada": False,
            "renomeacao_executada": False,
            "metadados_detalhados_executados": not args.sem_metadados_detalhados,
            "payload_resumido": args.payload_resumido,
            "tempos_por_fase": tempos_por_fase,
            "fase_mais_lenta": None,
            "linhas": None,
            "colunas": None,
            "causa_classificada": "NAO_EXECUTADO",
            "recomendação": "Executar diagnostico ST por fases no escopo fixo ES 2024-01.",
            "recomendacao": "Executar diagnostico ST por fases no escopo fixo ES 2024-01.",
            "sem_transformacao": args.sem_transformacao,
            "sem_dtypes": args.sem_dtypes,
            "sem_metadados_detalhados": args.sem_metadados_detalhados,
        }
    )
    inicio_total = time.monotonic()
    df = None
    erro_pos_download = False

    with tempfile.TemporaryDirectory(prefix="observatorio-sus-5n7-8f-st-") as tmp_home:
        inicio = time.monotonic()
        isolamento = aplicar_isolamento_pysus(tmp_home)
        tempos_por_fase["isolamento"] = round(time.monotonic() - inicio, 3)
        payload["isolamento"] = isolamento
        resultado["isolamento"] = isolamento

        inicio = time.monotonic()
        import pandas as pd
        from pysus import cnes

        tempos_por_fase["import_pysus"] = round(time.monotonic() - inicio, 3)

        inicio = time.monotonic()
        erros: list[str] = []
        for tentativa in range(1, args.tentativas + 1):
            try:
                df = cnes(state=uf, year=ano, month=mes, group=grupo)
                resultado["tentativas_executadas"] = tentativa
                break
            except Exception as exc:  # noqa: BLE001
                mensagem = f"{type(exc).__name__}: {exc}"
                erros.append(mensagem)
                resultado["tentativas_executadas"] = tentativa
                if classificar_causa(mensagem) == "TIMEOUT_CONTROLADO":
                    break
                if tentativa < args.tentativas:
                    espera = min(args.base_backoff ** tentativa + random.uniform(0, args.jitter_max), 5.0)
                    time.sleep(espera)
        tempos_por_fase["chamada_cnes"] = round(time.monotonic() - inicio, 3)

        inicio = time.monotonic()
        resultado["retornou_dataframe"] = isinstance(df, pd.DataFrame)
        if resultado["retornou_dataframe"]:
            resultado["linhas"] = int(len(df))
            resultado["colunas"] = int(len(df.columns))
            resultado["linhas_antes"] = resultado["linhas"]
            resultado["colunas_antes"] = resultado["colunas"]
        tempos_por_fase["leitura_retorno_dataframe"] = round(time.monotonic() - inicio, 3)

        if not resultado["retornou_dataframe"]:
            mensagem = " | ".join(erros) if erros else f"PySUS retornou {type(df)!r}"
            resultado["causa_classificada"] = "TIMEOUT_NA_CHAMADA_PYSUS"
            resultado["timeout_controlado"] = classificar_causa(mensagem) == "TIMEOUT_CONTROLADO"
            resultado["mensagem_excecao"] = mensagem
            resultado["recomendação"] = "Investigar PySUS/ST/rede antes de nova transformação ST."
            resultado["recomendacao"] = resultado["recomendação"]
        else:
            try:
                inicio = time.monotonic()
                colunas_antes = list(df.columns)
                tempos_por_fase["coleta_colunas"] = round(time.monotonic() - inicio, 3)

                inicio = time.monotonic()
                if args.sem_dtypes or args.payload_resumido:
                    tipos_antes = {}
                else:
                    tipos_antes = {coluna: str(dtype) for coluna, dtype in df.dtypes.items()}
                tempos_por_fase["coleta_dtypes"] = round(time.monotonic() - inicio, 3)

                inicio = time.monotonic()
                campos_textuais_detectados = [
                    coluna for coluna in colunas_antes if not coluna.upper().startswith("QT_") and coluna_deve_ser_texto(coluna)
                ]
                tempos_por_fase["deteccao_campos_textuais"] = round(time.monotonic() - inicio, 3)

                resultado["tipos_antes"] = tipos_antes
                resultado["colunas_textuais_detectadas"] = campos_textuais_detectados if not args.payload_resumido else len(campos_textuais_detectados)

                if args.sem_transformacao:
                    resultado["linhas_depois"] = resultado["linhas_antes"]
                    resultado["colunas_depois"] = resultado["colunas_antes"]
                    resultado["co_unidade_criado"] = "CO_UNIDADE" in df.columns
                    resultado["sucesso"] = False
                    resultado["causa_classificada"] = "ST_RETORNA_DATAFRAME_SEM_TRANSFORMACAO"
                    resultado["recomendação"] = "Como ST retornou DataFrame, executar diagnóstico com transformação e payload resumido."
                    resultado["recomendacao"] = resultado["recomendação"]
                    tempos_por_fase["aplicacao_preservacao_textual"] = 0.0
                    tempos_por_fase["aplicacao_renomeacoes"] = 0.0
                else:
                    inicio = time.monotonic()
                    renomear, matriz_renomeadas, pendentes = mapa_renomeacao(grupo, df.columns)
                    df = df.rename(columns=renomear)
                    resultado["renomeação_executada"] = True
                    resultado["renomeacao_executada"] = True
                    tempos_por_fase["aplicacao_renomeacoes"] = round(time.monotonic() - inicio, 3)

                    inicio = time.monotonic()
                    colunas_texto = preservar_texto_em_memoria(df)
                    resultado["preservação_textual_executada"] = True
                    resultado["preservacao_textual_executada"] = True
                    tempos_por_fase["aplicacao_preservacao_textual"] = round(time.monotonic() - inicio, 3)

                    if "COMPETEN" in df.columns:
                        df["competencia_normalizada"] = (
                            df["COMPETEN"].astype("string").str.slice(0, 4)
                            + "-"
                            + df["COMPETEN"].astype("string").str.slice(4, 6)
                        )

                    resultado["linhas_depois"] = int(len(df))
                    resultado["colunas_depois"] = int(len(df.columns))
                    resultado["colunas_renomeadas"] = sorted(renomear.keys())
                    resultado["renomeacoes"] = len(renomear)
                    resultado["colunas_preservadas_texto"] = colunas_texto if not args.payload_resumido else len(colunas_texto)
                    resultado["campos_pendentes"] = sorted(set(resultado["campos_pendentes"] + pendentes))
                    resultado["matriz_colunas_renomeadas"] = [] if args.payload_resumido else matriz_renomeadas
                    resultado["colunas_quantitativas_preservadas"] = [
                        coluna for coluna in df.columns if coluna.upper().startswith("QT_") and pd.api.types.is_numeric_dtype(df[coluna])
                    ]
                    if args.sem_dtypes or args.payload_resumido:
                        resultado["tipos_depois"] = {}
                    else:
                        resultado["tipos_depois"] = {coluna: str(dtype) for coluna, dtype in df.dtypes.items()}
                    resultado["transformação_executada"] = True
                    resultado["transformacao_executada"] = True

                inicio = time.monotonic()
                linhas_preservadas = resultado["linhas_antes"] == resultado["linhas_depois"]
                tempos_por_fase["validacao_linhas_antes_depois"] = round(time.monotonic() - inicio, 3)

                inicio = time.monotonic()
                resultado["co_unidade_criado"] = "CO_UNIDADE" in df.columns
                tempos_por_fase["verificacao_co_unidade"] = round(time.monotonic() - inicio, 3)

                inicio = time.monotonic()
                if args.sem_metadados_detalhados or args.payload_resumido:
                    resultado["metadados_detalhados"] = "omitidos_por_flag"
                else:
                    resultado["metadados_detalhados"] = {
                        "linhas_preservadas": linhas_preservadas,
                        "colunas_antes_lista": colunas_antes,
                        "colunas_depois_lista": list(df.columns),
                    }
                resultado["metadados_detalhados_executados"] = not args.sem_metadados_detalhados
                tempos_por_fase["geracao_metadados"] = round(time.monotonic() - inicio, 3)

                if not args.sem_transformacao:
                    resultado["sucesso"] = bool(linhas_preservadas and not resultado["co_unidade_criado"])
                    if resultado["sucesso"] and args.payload_resumido:
                        resultado["causa_classificada"] = "ST_TRANSFORMA_COM_PAYLOAD_RESUMIDO"
                        resultado["recomendação"] = "Usar payload resumido como opção operacional para ST e testar transformação padrão isolada."
                    elif resultado["sucesso"]:
                        resultado["causa_classificada"] = "ST_TRANSFORMACAO_CONCLUIDA_COM_RESSALVAS"
                        resultado["recomendação"] = "ST pode retornar à transformação de competência única, mantendo ressalva de CO_UNIDADE."
                    else:
                        resultado["causa_classificada"] = "TIMEOUT_OU_LENTIDAO_POS_DOWNLOAD"
                        resultado["recomendação"] = "Investigar fase pós-download indicada pelos tempos por fase."
                    resultado["recomendacao"] = resultado["recomendação"]
            except Exception as exc:  # noqa: BLE001
                erro_pos_download = True
                resultado["mensagem_excecao"] = f"{type(exc).__name__}: {exc}"
                resultado["causa_classificada"] = "TIMEOUT_OU_LENTIDAO_POS_DOWNLOAD"
                resultado["recomendação"] = "DataFrame retornou, mas falhou após download; revisar transformação/metadados/serialização."
                resultado["recomendacao"] = resultado["recomendação"]

    resultado["tempo_segundos"] = round(time.monotonic() - inicio_total, 3)
    resultado["persistiu_dados"] = False
    resultado["join_relacional_executado"] = False
    if not resultado["retornou_dataframe"]:
        resultado["linhas_depois"] = None
        resultado["colunas_depois"] = 0
    resultado["fase_mais_lenta"] = fase_mais_lenta(tempos_por_fase)
    if erro_pos_download and resultado["retornou_dataframe"]:
        resultado["causa_classificada"] = "TIMEOUT_OU_LENTIDAO_POS_DOWNLOAD"

    inicio = time.monotonic()
    json.dumps(tipo_json(resultado), ensure_ascii=False)
    tempos_por_fase["serializacao_json"] = round(time.monotonic() - inicio, 3)
    resultado["fase_mais_lenta"] = fase_mais_lenta(tempos_por_fase)

    payload["parametros"].update(
        {
            "uf": uf,
            "ano": ano,
            "meses": [mes],
            "grupos": [grupo],
            "sem_transformacao": args.sem_transformacao,
            "sem_dtypes": args.sem_dtypes,
            "sem_metadados_detalhados": args.sem_metadados_detalhados,
            "payload_resumido": args.payload_resumido,
        }
    )
    payload["diagnostico_st_fases"] = resultado
    payload["resultados_por_competencia"].append(resultado)
    payload["classificacao_etapa"] = resultado["causa_classificada"]
    payload["conclusao"] = resultado["recomendação"]
    payload["proxima_recomendacao"] = resultado["recomendação"]
    return payload


def executar_diagnostico_sem_subprocesso(args: argparse.Namespace) -> dict[str, Any]:
    payload = montar_payload_base(args)
    payload["isolamento"]["descricao"] = "Aplicado no proprio processo antes do import direto do PySUS."
    payload["diagnostico"] = {
        "usa_subprocesso": False,
        "objetivo": "Comparar chamada direta PySUS+transformacao com o caminho protegido por subprocesso.",
    }
    for grupo in normalizar_grupos(args.grupos):
        for mes in args.meses:
            resultado = executar_diagnostico_direto_combinacao(args, grupo, mes)
            payload["diagnostico_sem_subprocesso"].append(resultado)
            payload["resultados_por_competencia"].append(resultado)

    total = len(payload["resultados_por_competencia"])
    sucessos = sum(1 for item in payload["resultados_por_competencia"] if item["sucesso"])
    todos_timeout = bool(total) and all(
        item["causa_classificada"] == "TIMEOUT_CONTROLADO" for item in payload["resultados_por_competencia"]
    )
    if todos_timeout:
        payload["classificacao_etapa"] = "DIAGNOSTICO_SEM_SUBPROCESSO_TIMEOUT"
        payload["conclusao"] = "Diagnostico direto sem subprocesso tambem retornou TIMEOUT_CONTROLADO."
    elif sucessos:
        payload["classificacao_etapa"] = "DIAGNOSTICO_SEM_SUBPROCESSO_TRANSFORMOU"
        payload["conclusao"] = f"Diagnostico direto transformou {sucessos}/{total} combinacoes sem persistencia."
    else:
        payload["classificacao_etapa"] = "DIAGNOSTICO_SEM_SUBPROCESSO_FALHOU"
        payload["conclusao"] = "Diagnostico direto sem subprocesso falhou sem transformar DataFrame."
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Etapa 5N.7-8 — transformação em memória multi-competência PySUS→CNES"
    )
    parser.add_argument("--modo", default="planejamento", choices=["planejamento", "transformar_memoria", "diagnostico_sem_subprocesso", "diagnostico_st_fases", "resumo"])
    parser.add_argument("--uf", default="ES")
    parser.add_argument("--ano", type=int, default=2024)
    parser.add_argument("--meses", nargs="+", type=int, default=[1, 6, 12])
    parser.add_argument("--grupos", nargs="+", default=["ST", "LT", "SR"])
    parser.add_argument("--tentativas", type=int, default=5)
    parser.add_argument("--base-backoff", type=float, default=2.0)
    parser.add_argument("--jitter-max", type=float, default=1.0)
    parser.add_argument("--timeout-por-chamada", "--timeout-chamada", dest="timeout_por_chamada", type=float, default=300.0)
    parser.add_argument("--timeout-global", "--limite-segundos-total", dest="timeout_global", type=float, default=1800.0)
    parser.add_argument("--usar-subprocesso", action="store_true", help="Usa o caminho protegido por subprocesso; por padrao a transformacao usa chamada direta sem subprocesso.")
    parser.add_argument("--sem-transformacao", action="store_true", help="No diagnostico_st_fases, mede download/retorno de ST sem aplicar transformacao.")
    parser.add_argument("--sem-dtypes", action="store_true", help="No diagnostico_st_fases, omite coleta detalhada de dtypes.")
    parser.add_argument("--sem-metadados-detalhados", action="store_true", help="No diagnostico_st_fases, omite listas detalhadas de metadados estruturais.")
    parser.add_argument("--payload-resumido", action="store_true", help="No diagnostico_st_fases, reduz o payload JSON para diagnosticar serializacao/metadados.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.modo in {"planejamento", "resumo"}:
            payload = executar_planejamento(args)
        elif args.modo == "diagnostico_sem_subprocesso":
            payload = executar_diagnostico_sem_subprocesso(args)
        elif args.modo == "diagnostico_st_fases":
            payload = executar_diagnostico_st_fases(args)
        else:
            payload = executar_transformacao_memoria(args)
        print(json.dumps(tipo_json(payload), ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:  # noqa: BLE001
        erro = {"erro_global": f"{type(exc).__name__}: {exc}", "codigo_saida": 2}
        print(json.dumps(erro, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
