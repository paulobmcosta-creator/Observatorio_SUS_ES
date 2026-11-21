"""Localizar insumos por papel em um JSON fornecido pelo operador."""
import json
import sys
from pathlib import Path

def papel(nome):
    if len(sys.argv) < 2:
        raise ValueError("Forneça um arquivo JSON de caminhos relativos por papel")
    manifest = Path(sys.argv[1]).resolve()
    entries = json.loads(manifest.read_text(encoding="utf-8-sig"))
    if nome not in entries:
        raise ValueError("Papel ausente no manifesto: " + nome)
    return (manifest.parent / entries[nome]).resolve()
