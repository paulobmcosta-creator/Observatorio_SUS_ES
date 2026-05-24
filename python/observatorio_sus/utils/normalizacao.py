"""Funções utilitárias de normalização para a POC Python."""

from __future__ import annotations

import re
import unicodedata


def normalizar_nome_coluna(nome: str) -> str:
    """Normaliza nomes de colunas para padrão snake_case sem acentos.

    Regras:
    - minúsculas
    - remoção de acentos
    - caracteres não alfanuméricos substituídos por underscore
    - underscores duplicados colapsados
    - underscores nas bordas removidos
    """
    if nome is None:
        return ""

    texto = str(nome).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(ch for ch in texto if not unicodedata.combining(ch))
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    texto = re.sub(r"_+", "_", texto)
    return texto.strip("_")


def normalizar_competencia(competencia: str) -> str:
    """Normaliza competência para formato AAAA-MM.

    Aceita "YYYYMM" ou "YYYY-MM". Lança ValueError em formatos inválidos.
    """
    if competencia is None:
        raise ValueError("competencia não pode ser None")

    valor = str(competencia).strip()

    if re.fullmatch(r"\d{6}", valor):
        ano = int(valor[:4])
        mes = int(valor[4:6])
    elif re.fullmatch(r"\d{4}-\d{2}", valor):
        ano = int(valor[:4])
        mes = int(valor[5:7])
    else:
        raise ValueError(f"competencia inválida: {competencia}")

    if not (1900 <= ano <= 2100 and 1 <= mes <= 12):
        raise ValueError(f"competencia fora de faixa válida: {competencia}")

    return f"{ano:04d}-{mes:02d}"
