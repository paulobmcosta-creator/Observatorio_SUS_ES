"""Contratos CNES experimentais para validação operacional da migração R-Python."""

from .contratos import (
    listar_campos_criticos,
    listar_campos_textuais,
    listar_tabelas_obrigatorias,
    obter_contrato_tabela,
    validar_presenca_campos,
)

__all__ = [
    "listar_tabelas_obrigatorias",
    "obter_contrato_tabela",
    "listar_campos_criticos",
    "listar_campos_textuais",
    "validar_presenca_campos",
]
