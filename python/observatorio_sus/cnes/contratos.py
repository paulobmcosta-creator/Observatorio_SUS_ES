"""Contratos lógicos mínimos para extração CNES na Etapa 4."""

from __future__ import annotations

from copy import deepcopy

TABELAS_OBRIGATORIAS = {
    "estabelecimentos": [
        "tbEstabelecimento",
        "tbMunicipio",
        "rlEstabSubTipo",
        "tbSubTipo",
        "rlEstabAtendPrestConv",
        "tbAtendimentoPrestado",
        "tbConvenio",
        "tbTipoEstabelecimento",
        "tbNaturezaJuridica",
        "tbGestao",
    ],
    "habilitacoes": [
        "rlEstabSipac",
        "tbSubGruposHabilitacao",
        "base_estabelecimentos",
    ],
}

CAMPOS_TEXTUAIS_OBRIGATORIOS = [
    "CO_UNIDADE",
    "CO_CNES",
    "CO_MUNICIPIO_GESTOR",
    "COD_SUB_GRUPO_HABILITACAO",
    "TP_HABILITACAO",
    "CMTP_INICIO",
    "CMTP_FIM",
    "CO_MUNICIPIO",
    "CO_UF",
]

CONTRATOS_TABELAS = {
    "tbEstabelecimento": {
        "necessaria_para": "estabelecimentos",
        "campos_criticos": [
            "CO_UNIDADE",
            "CO_CNES",
            "CO_MUNICIPIO_GESTOR",
            "NO_FANTASIA",
            "NO_RAZAO_SOCIAL",
            "TP_GESTAO",
        ],
        "observacao": "TP_GESTAO pode exigir interpretação conservadora por limitação de domínio tbGestao.",
    },
    "tbMunicipio": {
        "necessaria_para": "estabelecimentos",
        "campos_criticos": ["CO_MUNICIPIO", "NO_MUNICIPIO", "CO_UF"],
    },
    "rlEstabSubTipo": {"necessaria_para": "estabelecimentos", "campos_criticos": ["CO_UNIDADE"]},
    "tbSubTipo": {"necessaria_para": "estabelecimentos", "campos_criticos": ["CO_SUB_TIPO", "NO_SUB_TIPO"]},
    "rlEstabAtendPrestConv": {"necessaria_para": "estabelecimentos", "campos_criticos": ["CO_UNIDADE"]},
    "tbAtendimentoPrestado": {"necessaria_para": "estabelecimentos", "campos_criticos": ["CO_ATENDIMENTO", "NO_ATENDIMENTO"]},
    "tbConvenio": {"necessaria_para": "estabelecimentos", "campos_criticos": ["CO_CONVENIO", "NO_CONVENIO"]},
    "tbTipoEstabelecimento": {"necessaria_para": "estabelecimentos", "campos_criticos": ["CO_TIPO_ESTABELECIMENTO", "NO_TIPO_ESTABELECIMENTO"]},
    "tbNaturezaJuridica": {"necessaria_para": "estabelecimentos", "campos_criticos": ["CO_NATUREZA_JURIDICA", "NO_NATUREZA_JURIDICA"]},
    "tbGestao": {
        "necessaria_para": "estabelecimentos",
        "campos_criticos": ["CO_GESTAO", "NO_GESTAO"],
        "observacao": "Cobertura pode ser parcial por incompatibilidade estrutural já documentada na competência 202601.",
    },
    "rlEstabSipac": {
        "necessaria_para": "habilitacoes",
        "campos_criticos": [
            "CO_UNIDADE",
            "COD_SUB_GRUPO_HABILITACAO",
            "TP_HABILITACAO",
            "CMTP_INICIO",
            "CMTP_FIM",
            "NU_LEITOS",
            "NO_PORTARIA",
            "DT_ATUALIZACAO",
        ],
    },
    "tbSubGruposHabilitacao": {
        "necessaria_para": "habilitacoes",
        "campos_criticos": ["CO_CODIGO_GRUPO", "TP_HABILITACAO", "NO_DESCRICAO_GRUPO", "TP_ORIGEM"],
    },
    "base_estabelecimentos": {
        "necessaria_para": "habilitacoes",
        "campos_criticos": ["co_unidade", "cnes"],
        "observacao": "Dependência derivada futura para integração das habilitações com estabelecimentos.",
    },
}


def listar_tabelas_obrigatorias() -> dict:
    return deepcopy(TABELAS_OBRIGATORIAS)


def obter_contrato_tabela(nome_tabela: str) -> dict:
    if nome_tabela not in CONTRATOS_TABELAS:
        raise ValueError(f"Tabela desconhecida no contrato CNES: {nome_tabela}")
    return deepcopy(CONTRATOS_TABELAS[nome_tabela])


def listar_campos_criticos(nome_tabela: str) -> list[str]:
    return list(obter_contrato_tabela(nome_tabela)["campos_criticos"])


def listar_campos_textuais() -> list[str]:
    return list(CAMPOS_TEXTUAIS_OBRIGATORIOS)


def validar_presenca_campos(colunas: list[str], tabela: str) -> dict:
    if tabela not in CONTRATOS_TABELAS:
        raise ValueError(f"Tabela desconhecida no contrato CNES: {tabela}")

    colunas_normalizadas = {str(col).strip().lower() for col in colunas if col is not None}
    campos_criticos = CONTRATOS_TABELAS[tabela]["campos_criticos"]

    presentes = [c for c in campos_criticos if c.lower() in colunas_normalizadas]
    ausentes = [c for c in campos_criticos if c.lower() not in colunas_normalizadas]

    return {
        "tabela": tabela,
        "campos_presentes": presentes,
        "campos_ausentes": ausentes,
        "ok": len(ausentes) == 0,
    }
