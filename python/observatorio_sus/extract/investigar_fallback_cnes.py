"""Etapa 5S: investigação de recorte seguro e fallback CNES/DATASUS/FTP."""
from __future__ import annotations

import argparse
import importlib
import inspect
import json
import pkgutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from observatorio_sus.cnes.contratos import (  # noqa: E402
    listar_campos_textuais,
    listar_tabelas_obrigatorias,
    obter_contrato_tabela,
)

COMPETENCIAS_2025 = [f"2025{m:02d}" for m in range(1, 13)]
TABELAS_PRIORITARIAS = ["tbEstabelecimento", "tbMunicipio", "rlEstabSipac", "tbSubGruposHabilitacao"]


def _base(uf: str, ano: int, modo: str) -> dict:
    tabelas = listar_tabelas_obrigatorias()
    contratos = {}
    for grupo in tabelas.values():
        for t in grupo:
            contratos[t] = obter_contrato_tabela(t)

    return {
        "ambiente": {
            "python_versao": sys.version,
            "python_executavel": sys.executable,
            "tempdir": tempfile.gettempdir(),
        },
        "parametros": {"uf": uf, "ano": ano, "modo": modo},
        "competencias": COMPETENCIAS_2025,
        "tabelas_investigadas": TABELAS_PRIORITARIAS,
        "contratos_usados": contratos,
        "campos_textuais_contrato": listar_campos_textuais(),
        "inspecao_pysus": {"executada": False},
        "fontes_detectadas": [],
        "arquivos_remotos_candidatos": [],
        "metadados_arquivos": [],
        "tamanhos_detectados": {},
        "risco_download": {"exige_download_real": False, "motivo": "nao_avaliado"},
        "recorte_seguro": {},
        "fallback": {},
        "lacunas": [],
        "conclusao": "",
        "proxima_recomendacao": "",
    }


def _classificar_recorte(item: dict) -> str:
    if not item.get("fonte_encontrada", False):
        return "RECORTE_NAO_CONFIRMADO"
    if item.get("uf_explicita") and item.get("competencia_explicita") and item.get("tamanho_conhecido"):
        return "RECORTE_SEGURO_CONFIRMADO"
    if item.get("competencia_explicita") and not item.get("uf_explicita"):
        return "RECORTE_PARCIAL"
    if item.get("exige_download"):
        return "RECORTE_INSEGURO"
    return "NAO_TESTADO"


def _inspecionar_pysus() -> dict:
    saida = {
        "executada": True,
        "importavel": False,
        "versao": None,
        "caminho": None,
        "modulos_cnes": [],
        "objetos_relevantes": [],
        "candidatos_recorte": [],
        "permite_listagem_sem_download": False,
    }
    try:
        pysus = importlib.import_module("pysus")
    except Exception as exc:
        saida["erro"] = str(exc)
        return saida

    saida["importavel"] = True
    saida["versao"] = getattr(pysus, "__version__", "sem __version__")
    saida["caminho"] = getattr(pysus, "__file__", "sem __file__")

    if hasattr(pysus, "__path__"):
        for mod in pkgutil.walk_packages(pysus.__path__, prefix="pysus."):
            nome = mod.name.lower()
            if ".tests" in nome:
                continue
            if "cnes" in nome or "ftp" in nome or "datasus" in nome:
                saida["modulos_cnes"].append(mod.name)

    for modulo in saida["modulos_cnes"][:40]:
        try:
            mod = importlib.import_module(modulo)
        except Exception:
            continue
        for nome, obj in inspect.getmembers(mod):
            if not (inspect.isfunction(obj) or inspect.isclass(obj)):
                continue
            nlow = nome.lower()
            try:
                sig = inspect.signature(obj)
                params = {p.lower() for p in sig.parameters.keys()}
            except (ValueError, TypeError):
                params = set()
            if any(k in nlow for k in ["cnes", "ftp", "download", "list", "files"]):
                saida["objetos_relevantes"].append({"modulo": modulo, "nome": nome, "parametros": sorted(params)[:20]})
            aceita_uf = "uf" in params or "state" in params
            aceita_comp = "competencia" in params or "competence" in params or "year" in params
            if aceita_uf and aceita_comp:
                saida["candidatos_recorte"].append({"modulo": modulo, "nome": nome, "parametros": sorted(params)[:20]})
            if "list" in nlow and not any(k in nlow for k in ["download", "fetch"]):
                saida["permite_listagem_sem_download"] = True

    return saida


def _preencher_matrizes(resultado: dict, inspecao: dict) -> None:
    for tabela in TABELAS_PRIORITARIAS:
        item = {
            "tabela": tabela,
            "fonte_encontrada": len(inspecao.get("modulos_cnes", [])) > 0,
            "fonte_candidata": "PySUS/DATASUS-FTP (inspecao estatico-dinamica)",
            "competencia_explicita": len(inspecao.get("candidatos_recorte", [])) > 0,
            "uf_explicita": len(inspecao.get("candidatos_recorte", [])) > 0,
            "tamanho_conhecido": False,
            "exige_download": True,
            "observacao": "Não houve download; apenas inspeção/listagem leve.",
        }
        classe = _classificar_recorte(item)
        resultado["recorte_seguro"][tabela] = {
            "classificacao": classe,
            "recorte_por_tabela": "parcial" if item["fonte_encontrada"] else "nao_confirmado",
            "recorte_por_competencia": "sim" if item["competencia_explicita"] else "nao_confirmado",
            "recorte_por_uf": "sim" if item["uf_explicita"] else "nao_confirmado",
            "tamanho_antes_download": "nao",
        }
        if classe == "RECORTE_SEGURO_CONFIRMADO":
            fallback = "Fallback não necessário"
        elif classe == "RECORTE_PARCIAL":
            fallback = "Fallback provável"
        elif classe == "RECORTE_NAO_CONFIRMADO":
            fallback = "Fallback obrigatório"
        elif classe == "RECORTE_INSEGURO":
            fallback = "Fallback inseguro"
        else:
            fallback = "Fallback inconclusivo"
        resultado["fallback"][tabela] = fallback
        resultado["arquivos_remotos_candidatos"].append({
            "tabela": tabela,
            "competencia": "2025MM",
            "fonte": item["fonte_candidata"],
            "nome_caminho_remoto": "nao_confirmado_sem_listagem_dedicada",
            "uf_explicita": item["uf_explicita"],
            "competencia_explicita": item["competencia_explicita"],
            "tamanho_conhecido": item["tamanho_conhecido"],
            "exige_download": item["exige_download"],
            "recorte_seguro": classe,
            "observacao": item["observacao"],
        })


def executar(uf: str, ano: int, modo: str) -> dict:
    r = _base(uf, ano, modo)
    if modo == "planejamento":
        r["conclusao"] = "Planejamento da Etapa 5S concluído sem rede e sem download."
        r["proxima_recomendacao"] = "Executar inspecao_pysus e listar_fontes com bloqueio de download."
        return r

    if modo == "inspecao_pysus":
        ins = _inspecionar_pysus()
        r["inspecao_pysus"] = ins
        _preencher_matrizes(r, ins)
        r["fontes_detectadas"] = sorted(set(ins.get("modulos_cnes", [])))[:30]
        r["risco_download"] = {
            "exige_download_real": True,
            "motivo": "sem endpoint inequívoco de metadado/tamanho por tabela+competência+UF",
        }
        r["lacunas"] = [
            "Sem confirmação de tamanho de arquivo antes de download.",
            "Sem confirmação de recorte explícito UF+competência em assinatura operacional.",
        ]
        r["conclusao"] = "Inspeção PySUS concluída sem download de dados; recorte seguro permanece parcial/não confirmado."
        r["proxima_recomendacao"] = "Executar listar_fontes leve e preparar Etapa 5F somente com limites humanos aprovados."
        return r

    if modo == "listar_fontes":
        ins = _inspecionar_pysus()
        r["inspecao_pysus"] = ins
        _preencher_matrizes(r, ins)
        r["fontes_detectadas"] = sorted(set(ins.get("modulos_cnes", [])))[:30]
        with tempfile.TemporaryDirectory(prefix="etapa5s_logs_") as tdir:
            r["ambiente"]["diretorio_temporario_logs"] = tdir
            r["metadados_arquivos"].append({
                "fonte": "PySUS introspection",
                "tipo": "module_listing",
                "quantidade_modulos": len(ins.get("modulos_cnes", [])),
            })
        r["ambiente"]["diretorio_temporario_logs_excluido"] = True
        r["risco_download"] = {
            "exige_download_real": True,
            "motivo": "listagem remota detalhada sem download não confirmada nesta implementação",
        }
        r["lacunas"] = [
            "Listagem remota de arquivos CNES por competência não confirmada sem download.",
            "Tamanho de arquivo pré-download não confirmado.",
        ]
        r["conclusao"] = "Listar_fontes executado em modo conservador: sem download real e sem persistência local de dados CNES."
        r["proxima_recomendacao"] = "Deliberação humana para Etapa 5F com competência piloto e limite de tamanho."
        return r

    if modo == "resumo":
        r["conclusao"] = "Resumo local disponível; execute inspecao_pysus/listar_fontes para atualizar achados."
        r["proxima_recomendacao"] = "Etapa 5F apenas após deliberação humana de limites operacionais."
        return r

    r["conclusao"] = "Modo desconhecido."
    return r


def main() -> int:
    parser = argparse.ArgumentParser(description="Etapa 5S: investigação de recorte seguro e fallback CNES.")
    parser.add_argument("--uf", default="ES")
    parser.add_argument("--ano", type=int, default=2025)
    parser.add_argument("--modo", choices=["planejamento", "inspecao_pysus", "listar_fontes", "resumo"], default="planejamento")
    args = parser.parse_args()
    try:
        print(json.dumps(executar(args.uf, args.ano, args.modo), ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"erro": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
