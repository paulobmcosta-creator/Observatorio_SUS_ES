"""Etapa 5: extração mínima temporária CNES/ES/2025 com controle por competência."""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from observatorio_sus.cnes.contratos import (  # noqa: E402
    listar_campos_textuais,
    listar_tabelas_obrigatorias,
    obter_contrato_tabela,
    validar_presenca_campos,
)

COMPETENCIAS_2025 = [f"2025{mes:02d}" for mes in range(1, 13)]


def _base_saida(uf: str, ano: int, modo: str) -> dict:
    tabelas = listar_tabelas_obrigatorias()
    contratos_usados = {}
    for grupo in tabelas.values():
        for tabela in grupo:
            contratos_usados[tabela] = obter_contrato_tabela(tabela)

    return {
        "ambiente": {
            "python_versao": sys.version,
            "python_executavel": sys.executable,
            "tempdir_sistema": tempfile.gettempdir(),
        },
        "parametros": {"uf": uf, "ano": ano, "modo": modo},
        "competencias": COMPETENCIAS_2025,
        "contratos_usados": contratos_usados,
        "gate_1_estabelecimentos": {"status": "NAO_EXECUTADO", "motivo": "pendente"},
        "gate_2_habilitacoes": {"status": "NAO_EXECUTADO", "motivo": "pendente"},
        "arquivos_temporarios": [],
        "cobertura_por_tabela": {},
        "cobertura_por_competencia": {c: {"gate_1": "nao_avaliado", "gate_2": "nao_avaliado"} for c in COMPETENCIAS_2025},
        "campos_ausentes": {},
        "campos_presentes": {},
        "preservacao_codigos": {
            "campos_avaliados": listar_campos_textuais(),
            "co_unidade": "inconclusivo",
            "co_cnes": "inconclusivo",
            "zeros_a_esquerda": "inconclusivo",
            "evidencias": [],
        },
        "fallback": {"necessario": False, "acionado": False, "motivo": None, "executado": False},
        "riscos": [],
        "conclusao": "",
        "proxima_recomendacao": "",
    }


def _avaliar_contratos_sem_dados(saida: dict) -> None:
    for tabela in saida["contratos_usados"]:
        validacao = validar_presenca_campos([], tabela)
        saida["cobertura_por_tabela"][tabela] = {
            "necessaria_para": saida["contratos_usados"][tabela]["necessaria_para"],
            "competencias_avaliadas": COMPETENCIAS_2025,
            "status": "nao_confirmada",
            "campos_presentes": validacao["campos_presentes"],
            "campos_ausentes": validacao["campos_ausentes"],
        }
        saida["campos_presentes"][tabela] = []
        saida["campos_ausentes"][tabela] = validacao["campos_ausentes"]


def _diagnostico_pysus() -> dict:
    info = {"importavel": False, "versao": None, "caminho": None, "modulos_cnes": []}
    try:
        pysus = importlib.import_module("pysus")
    except Exception as exc:
        info["erro"] = str(exc)
        return info

    info["importavel"] = True
    info["versao"] = getattr(pysus, "__version__", "sem __version__")
    info["caminho"] = getattr(pysus, "__file__", "sem __file__")
    return info


def executar(uf: str, ano: int, modo: str) -> dict:
    saida = _base_saida(uf=uf, ano=ano, modo=modo)
    _avaliar_contratos_sem_dados(saida)

    if modo == "planejamento":
        saida["gate_1_estabelecimentos"] = {"status": "PLANEJADO", "motivo": "sem rede por definicao do modo"}
        saida["gate_2_habilitacoes"] = {"status": "CONDICIONADO", "motivo": "depende da aprovacao do Gate 1"}
        saida["riscos"] = ["Modo planejamento não executa rede nem download."]
        saida["conclusao"] = "Planejamento concluído sem extração real e sem escrita em diretórios versionados."
        saida["proxima_recomendacao"] = "Executar modo diagnostico e, se seguro, extracao_temporaria controlada."
        return saida

    diag = _diagnostico_pysus()
    saida["ambiente"]["pysus"] = diag

    if modo == "diagnostico":
        saida["gate_1_estabelecimentos"] = {"status": "NAO_EXECUTADO_POR_SEGURANCA", "motivo": "diagnostico sem download"}
        saida["gate_2_habilitacoes"] = {"status": "NAO_EXECUTADO_POR_GATE_1", "motivo": "Gate 1 não executado"}
        saida["fallback"] = {"necessario": not diag.get("importavel", False), "acionado": False, "motivo": "modo diagnostico", "executado": False}
        saida["riscos"] = ["Diagnóstico não confirma recorte seguro por UF e competência para download."]
        saida["conclusao"] = "Diagnóstico concluído sem download; cobertura estrutural permanece não confirmada."
        saida["proxima_recomendacao"] = "Validar mecanismo de recorte seguro antes de qualquer extração remota."
        return saida

    # extracao_temporaria
    with tempfile.TemporaryDirectory(prefix="etapa5_cnes_") as tmpdir:
        saida["ambiente"]["diretorio_temporario_execucao"] = tmpdir
        safe_recorte_confirmado = False
        if not diag.get("importavel", False):
            saida["fallback"] = {
                "necessario": True,
                "acionado": False,
                "motivo": "PySUS indisponível",
                "executado": False,
            }
        else:
            saida["fallback"] = {
                "necessario": True,
                "acionado": False,
                "motivo": "fallback necessário, mas não executado por ausência de recorte seguro",
                "executado": False,
            }

        if not safe_recorte_confirmado:
            saida["gate_1_estabelecimentos"] = {"status": "NAO_EXECUTADO_POR_SEGURANCA", "motivo": "ausência de recorte seguro confirmado"}
            saida["gate_2_habilitacoes"] = {"status": "NAO_EXECUTADO_POR_GATE_1", "motivo": "Gate 1 não aprovado"}
            for comp in COMPETENCIAS_2025:
                saida["cobertura_por_competencia"][comp] = {
                    "gate_1": "nao_executado_por_seguranca",
                    "gate_2": "nao_executado_por_gate_1",
                }
            saida["riscos"] = [
                "Risco de download amplo sem recorte seguro por UF+competência.",
                "Cobertura estrutural sem validação empírica nesta execução.",
            ]
            saida["conclusao"] = "Extração temporária bloqueada por segurança operacional; nenhum download realizado."
            saida["proxima_recomendacao"] = "Executar Etapa 5S para investigar recorte seguro/fallback antes de nova tentativa."

    saida["ambiente"]["diretorio_temporario_excluido"] = True
    return saida


def main() -> int:
    parser = argparse.ArgumentParser(description="Etapa 5 CNES/ES/2025: extração mínima temporária controlada.")
    parser.add_argument("--uf", default="ES")
    parser.add_argument("--ano", type=int, default=2025)
    parser.add_argument("--modo", choices=["planejamento", "diagnostico", "extracao_temporaria"], default="planejamento")
    args = parser.parse_args()

    try:
        resultado = executar(args.uf, args.ano, args.modo)
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"erro": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
