"""Gerar inventário RD de catálogo observado ou declarar falta de consulta."""
import argparse
import hashlib
import json
from pathlib import Path
from observatorio_sus.extract.inventariar_sih_rd import inventariar_rd

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--competencia", default="202401")
    p.add_argument("--catalogo", type=Path, help="JSON observado: lista de nome/uri_oficial/revisao/bytes")
    p.add_argument("--saida", required=True, type=Path)
    a = p.parse_args()
    catalogo = json.loads(a.catalogo.read_text()) if a.catalogo else None
    prova = "sha256:" + hashlib.sha256(a.catalogo.read_bytes()).hexdigest() if a.catalogo else None
    resultado = inventariar_rd(a.competencia, catalogo, prova)
    a.saida.parent.mkdir(parents=True, exist_ok=True)
    with a.saida.open("x", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(resultado["estado"])
