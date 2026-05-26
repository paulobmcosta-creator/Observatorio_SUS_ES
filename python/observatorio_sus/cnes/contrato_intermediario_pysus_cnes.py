"""Contrato intermediário PySUS→CNES (Etapa 5N.6).

Módulo puramente declarativo: não executa rede, não chama PySUS operacionalmente
nem materializa dados observacionais CNES.
"""

from __future__ import annotations

from csv import DictWriter
from pathlib import Path

GRUPOS_PYSUS_CNES: dict[str, str] = {
    "ST": "estabelecimentos",
    "LT": "leitos",
    "SR": "serviços/classificação",
}

CAMPOS_OBSERVADOS_POR_GRUPO: dict[str, list[str]] = {
    "ST": [
        "CNES", "CODUFMUN", "COD_CEP", "CPF_CNPJ", "PF_PJ", "NIV_DEP", "CNPJ_MAN",
        "TPGESTAO", "COMPETEN", "NAT_JUR", "ESFERA_A", "ATIVIDAD", "RETENCAO",
        "NATUREZA", "CLIENTEL", "TP_UNID", "TURNO_AT", "NIV_HIER", "TERCEIRO",
    ],
    "LT": [
        "CNES", "CODUFMUN", "REGSAUDE", "MICR_REG", "DISTRSAN", "DISTRADM", "TPGESTAO",
        "PF_PJ", "CPF_CNPJ", "NIV_DEP", "CNPJ_MAN", "ESFERA_A", "ATIVIDAD", "RETENCAO",
        "NATUREZA", "CLIENTEL", "TP_UNID", "TURNO_AT", "NIV_HIER", "TERCEIRO", "TP_LEITO",
        "CODLEITO", "QT_EXIST", "QT_CONTR", "QT_SUS", "QT_NSUS", "COMPETEN", "NAT_JUR",
    ],
    "SR": [
        "CNES", "CODUFMUN", "SERV_ESP", "CLASS_SR", "SRVUNICO", "REGSAUDE", "MICR_REG",
        "DISTRSAN", "DISTRADM", "TPGESTAO", "PF_PJ", "CPF_CNPJ", "NIV_DEP", "ESFERA_A",
        "ATIVIDAD", "RETENCAO", "NATUREZA", "CLIENTEL", "TP_UNID", "TURNO_AT", "NIV_HIER",
        "TERCEIRO", "CNPJ_MAN", "CARACTER", "AMB_NSUS", "AMB_SUS", "HOSP_NSUS", "HOSP_SUS",
        "COMPETEN", "CONTSRVU", "CNESTERC", "NAT_JUR",
    ],
}

MAPA_EQUIVALENCIAS_INICIAL: list[dict[str, object]] = [
    {"grupo_pysus":"ST","descricao_grupo":"estabelecimentos","coluna_pysus":"CNES","campo_contrato_cnes":"CO_CNES","campo_legado_r":"cnes","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"CHAVE_PUBLICA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Código público; não equivale automaticamente a CO_UNIDADE."},
    {"grupo_pysus":"ST","descricao_grupo":"estabelecimentos","coluna_pysus":"CODUFMUN","campo_contrato_cnes":"CO_MUNICIPIO_GESTOR","campo_legado_r":"co_municipio_gestor","tipo_equivalencia":"SEMANTICA_POTENCIAL","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"TERRITORIO","preservar_como_texto":True,"risco_coercao":True,"observacao":"Código territorial potencial."},
    {"grupo_pysus":"ST","descricao_grupo":"estabelecimentos","coluna_pysus":"COMPETEN","campo_contrato_cnes":"competencia","campo_legado_r":"competencia","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"CONFIRMADA_NOMINALMENTE","papel_metodologico":"COMPETENCIA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Competência nominalmente estável em 5N.5."},
    {"grupo_pysus":"ST","descricao_grupo":"estabelecimentos","coluna_pysus":"TPGESTAO","campo_contrato_cnes":"TP_GESTAO","campo_legado_r":"tp_gestao","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"GESTAO","preservar_como_texto":True,"risco_coercao":True,"observacao":"Regra de preservação textual."},
    {"grupo_pysus":"ST","descricao_grupo":"estabelecimentos","coluna_pysus":"NAT_JUR","campo_contrato_cnes":"natureza_juridica","campo_legado_r":"nat_jur","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"NATUREZA_JURIDICA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Exige validação com contratos R."},
    {"grupo_pysus":"ST","descricao_grupo":"estabelecimentos","coluna_pysus":"CPF_CNPJ","campo_contrato_cnes":"cpf_cnpj","campo_legado_r":"cpf_cnpj","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"IDENTIFICADOR_PESSOA_JURIDICA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Identificador administrativo sensível a zeros à esquerda."},
    {"grupo_pysus":"ST","descricao_grupo":"estabelecimentos","coluna_pysus":"CNPJ_MAN","campo_contrato_cnes":"cnpj_mantenedora","campo_legado_r":"cnpj_man","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"IDENTIFICADOR_PESSOA_JURIDICA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Identificador de mantenedora."},

    {"grupo_pysus":"LT","descricao_grupo":"leitos","coluna_pysus":"CNES","campo_contrato_cnes":"CO_CNES","campo_legado_r":"cnes","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"CHAVE_PUBLICA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Código público do estabelecimento."},
    {"grupo_pysus":"LT","descricao_grupo":"leitos","coluna_pysus":"CODUFMUN","campo_contrato_cnes":"CO_MUNICIPIO_GESTOR","campo_legado_r":"co_municipio_gestor","tipo_equivalencia":"SEMANTICA_POTENCIAL","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"TERRITORIO","preservar_como_texto":True,"risco_coercao":True,"observacao":"Território de gestão."},
    {"grupo_pysus":"LT","descricao_grupo":"leitos","coluna_pysus":"COMPETEN","campo_contrato_cnes":"competencia","campo_legado_r":"competencia","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"CONFIRMADA_NOMINALMENTE","papel_metodologico":"COMPETENCIA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Competência mensal."},
    {"grupo_pysus":"LT","descricao_grupo":"leitos","coluna_pysus":"TPGESTAO","campo_contrato_cnes":"TP_GESTAO","campo_legado_r":"tp_gestao","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"GESTAO","preservar_como_texto":True,"risco_coercao":True,"observacao":"Tipo de gestão."},
    {"grupo_pysus":"LT","descricao_grupo":"leitos","coluna_pysus":"NAT_JUR","campo_contrato_cnes":"natureza_juridica","campo_legado_r":"nat_jur","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"NATUREZA_JURIDICA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Natureza jurídica."},
    {"grupo_pysus":"LT","descricao_grupo":"leitos","coluna_pysus":"CODLEITO","campo_contrato_cnes":"codigo_leito","campo_legado_r":"codleito","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"OFERTA_LEITOS","preservar_como_texto":True,"risco_coercao":True,"observacao":"Classificação de leito."},
    {"grupo_pysus":"LT","descricao_grupo":"leitos","coluna_pysus":"TP_LEITO","campo_contrato_cnes":"tipo_leito","campo_legado_r":"tp_leito","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"OFERTA_LEITOS","preservar_como_texto":True,"risco_coercao":True,"observacao":"Tipo de leito."},
    {"grupo_pysus":"LT","descricao_grupo":"leitos","coluna_pysus":"QT_EXIST","campo_contrato_cnes":"qt_existente","campo_legado_r":"qt_exist","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"OFERTA_LEITOS","preservar_como_texto":False,"risco_coercao":False,"observacao":"Quantidade de leitos existentes."},
    {"grupo_pysus":"LT","descricao_grupo":"leitos","coluna_pysus":"QT_SUS","campo_contrato_cnes":"qt_sus","campo_legado_r":"qt_sus","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"OFERTA_LEITOS","preservar_como_texto":False,"risco_coercao":False,"observacao":"Oferta SUS."},
    {"grupo_pysus":"LT","descricao_grupo":"leitos","coluna_pysus":"QT_NSUS","campo_contrato_cnes":"qt_nsus","campo_legado_r":"qt_nsus","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"OFERTA_LEITOS","preservar_como_texto":False,"risco_coercao":False,"observacao":"Oferta não SUS."},

    {"grupo_pysus":"SR","descricao_grupo":"serviços/classificação","coluna_pysus":"CNES","campo_contrato_cnes":"CO_CNES","campo_legado_r":"cnes","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"CHAVE_PUBLICA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Código público do estabelecimento."},
    {"grupo_pysus":"SR","descricao_grupo":"serviços/classificação","coluna_pysus":"CODUFMUN","campo_contrato_cnes":"CO_MUNICIPIO_GESTOR","campo_legado_r":"co_municipio_gestor","tipo_equivalencia":"SEMANTICA_POTENCIAL","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"TERRITORIO","preservar_como_texto":True,"risco_coercao":True,"observacao":"Território."},
    {"grupo_pysus":"SR","descricao_grupo":"serviços/classificação","coluna_pysus":"COMPETEN","campo_contrato_cnes":"competencia","campo_legado_r":"competencia","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"CONFIRMADA_NOMINALMENTE","papel_metodologico":"COMPETENCIA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Competência mensal."},
    {"grupo_pysus":"SR","descricao_grupo":"serviços/classificação","coluna_pysus":"TPGESTAO","campo_contrato_cnes":"TP_GESTAO","campo_legado_r":"tp_gestao","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"GESTAO","preservar_como_texto":True,"risco_coercao":True,"observacao":"Tipo de gestão."},
    {"grupo_pysus":"SR","descricao_grupo":"serviços/classificação","coluna_pysus":"NAT_JUR","campo_contrato_cnes":"natureza_juridica","campo_legado_r":"nat_jur","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"NATUREZA_JURIDICA","preservar_como_texto":True,"risco_coercao":True,"observacao":"Natureza jurídica."},
    {"grupo_pysus":"SR","descricao_grupo":"serviços/classificação","coluna_pysus":"SERV_ESP","campo_contrato_cnes":"servico_especializado","campo_legado_r":"serv_esp","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"OFERTA_SERVICOS","preservar_como_texto":True,"risco_coercao":True,"observacao":"Serviço especializado."},
    {"grupo_pysus":"SR","descricao_grupo":"serviços/classificação","coluna_pysus":"CLASS_SR","campo_contrato_cnes":"classificacao_servico","campo_legado_r":"class_sr","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"CLASSIFICACAO_SERVICO","preservar_como_texto":True,"risco_coercao":True,"observacao":"Classificação do serviço."},
    {"grupo_pysus":"SR","descricao_grupo":"serviços/classificação","coluna_pysus":"AMB_SUS","campo_contrato_cnes":"amb_sus","campo_legado_r":"amb_sus","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"OFERTA_SERVICOS","preservar_como_texto":False,"risco_coercao":False,"observacao":"Indicador de oferta ambulatorial SUS."},
    {"grupo_pysus":"SR","descricao_grupo":"serviços/classificação","coluna_pysus":"HOSP_SUS","campo_contrato_cnes":"hosp_sus","campo_legado_r":"hosp_sus","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"OFERTA_SERVICOS","preservar_como_texto":False,"risco_coercao":False,"observacao":"Indicador de oferta hospitalar SUS."},
    {"grupo_pysus":"SR","descricao_grupo":"serviços/classificação","coluna_pysus":"CNESTERC","campo_contrato_cnes":"cnes_terceiro","campo_legado_r":"cnesterc","tipo_equivalencia":"NOMINAL_APROXIMADA","status_equivalencia":"POTENCIAL_A_CONFIRMAR","papel_metodologico":"IDENTIFICADOR_PESSOA_JURIDICA","preservar_como_texto":True,"risco_coercao":True,"observacao":"CNES de terceiro; manter textual."},

    {"grupo_pysus":"ST","descricao_grupo":"estabelecimentos","coluna_pysus":"CO_UNIDADE","campo_contrato_cnes":"CO_UNIDADE","campo_legado_r":"co_unidade","tipo_equivalencia":"AUSENTE_NO_PYSUS","status_equivalencia":"INCONCLUSIVA","papel_metodologico":"CHAVE_OPERACIONAL_POTENCIAL","preservar_como_texto":True,"risco_coercao":True,"observacao":"CO_UNIDADE não apareceu literalmente em 5N.4/5N.5; joins por co_unidade não podem ser substituídos; R permanece oráculo."},
]


def listar_grupos_intermediarios() -> dict[str, str]:
    return dict(GRUPOS_PYSUS_CNES)


def listar_campos_observados(grupo: str) -> list[str]:
    return list(CAMPOS_OBSERVADOS_POR_GRUPO.get(grupo.upper(), []))


def listar_equivalencias() -> list[dict[str, object]]:
    return [dict(item) for item in MAPA_EQUIVALENCIAS_INICIAL]


def filtrar_equivalencias_por_grupo(grupo: str) -> list[dict[str, object]]:
    chave = grupo.upper()
    return [dict(item) for item in MAPA_EQUIVALENCIAS_INICIAL if item["grupo_pysus"] == chave]


def exportar_contrato_intermediario_csv(caminho: str | Path) -> Path:
    destino = Path(caminho)
    destino.parent.mkdir(parents=True, exist_ok=True)
    campos = [
        "grupo_pysus", "descricao_grupo", "coluna_pysus", "campo_contrato_cnes", "campo_legado_r",
        "tipo_equivalencia", "status_equivalencia", "papel_metodologico", "preservar_como_texto",
        "risco_coercao", "observacao",
    ]
    with destino.open("w", encoding="utf-8", newline="") as fp:
        writer = DictWriter(fp, fieldnames=campos)
        writer.writeheader()
        writer.writerows(MAPA_EQUIVALENCIAS_INICIAL)
    return destino
