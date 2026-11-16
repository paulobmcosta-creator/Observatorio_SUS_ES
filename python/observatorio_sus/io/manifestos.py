"""Criação de manifesto de execução para rastreabilidade da POC."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import hashlib
import json
import re
import unicodedata
from pathlib import PurePosixPath


def json_canonico(valor: Any) -> bytes:
    """Serializar conteúdo sem carimbos voláteis; preservar fronteiras de objetos."""
    return json.dumps(valor, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def caminho_normalizado(valor: str) -> str:
    """Validar caminho relativo portátil; rejeitar aliases, traversal e separadores ambíguos."""
    if not isinstance(valor, str) or not valor or "\\" in valor or ":" in valor:
        raise ValueError("Caminho inválido.")
    caminho = PurePosixPath(valor)
    if caminho.is_absolute() or caminho.as_posix() != valor or any(
        parte in {".", ".."} or parte.endswith((" ", ".")) or
        any(ord(c) < 32 for c in parte) or
        re.fullmatch(r"(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(\..*)?", parte)
        for parte in caminho.parts
    ) or unicodedata.normalize("NFC", valor) != valor:
        raise ValueError("Caminho não normalizado ou inseguro.")
    return valor


def criar_identidade_conjunto(objetos: list[dict]) -> tuple[str, dict]:
    """Retornar SHA-256 e manifesto canônico v1 com identidade lógica e de bytes.

    Cada objeto contém id, caminho, sistema, familia, competencia, uf, parte,
    revisao, layout, bytes e sha256. URIs/transporte/instantes pertencem ao recibo
    de aquisição separado; a revisão declarada integra a identidade lógica.
    """
    campos_texto = ("id", "caminho", "sistema", "familia", "competencia", "uf", "parte", "revisao", "layout")
    if not objetos:
        raise ValueError("Conjunto obrigatório vazio.")
    linhas, ids, nomes = [], set(), set()
    for objeto in objetos:
        linha = {k: objeto[k] for k in (*campos_texto, "bytes", "sha256")}
        if any(not isinstance(linha[k], str) or not linha[k].strip() for k in campos_texto):
            raise ValueError("Identidade lógica incompleta.")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", linha["id"]) or linha["id"] in {".", ".."}:
            raise ValueError("ID de objeto inválido.")
        nome = caminho_normalizado(linha["caminho"]).casefold()
        if linha["id"] in ids or nome in nomes or any(
            nome.startswith(n + "/") or n.startswith(nome + "/") for n in nomes
        ):
            raise ValueError("ID repetido ou conflito de caminhos.")
        if type(linha["bytes"]) is not int or linha["bytes"] < 0 or not re.fullmatch(r"[0-9a-f]{64}", linha["sha256"]):
            raise ValueError("Identidade de bytes inválida.")
        ids.add(linha["id"]); nomes.add(nome); linhas.append(linha)
    manifesto = {"schema_identidade": 1, "objetos": sorted(linhas, key=lambda r: r["id"])}
    return hashlib.sha256(json_canonico(manifesto)).hexdigest(), manifesto


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
