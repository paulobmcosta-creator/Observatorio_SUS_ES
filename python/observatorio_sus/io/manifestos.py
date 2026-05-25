"""Criação de manifesto de execução para rastreabilidade da POC."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def criar_manifesto_execucao(
    ferramenta: str,
    parametros: dict[str, Any] | None = None,
    observacoes: str | None = None,
) -> dict[str, Any]:
    """Cria um dicionário manifesto mínimo de execução."""
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "ferramenta": ferramenta,
        "parametros": parametros or {},
        "observacoes": observacoes or "",
    }
