"""Restaurar somente o JSON autorizado do MVP original, mantendo-o fora de Git."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

HASH_ZIP = "8fa73c6a9b00efeda20cfaaffe56e96dc038326af16f3b9a8fa7eb97efc749b1"
MEMBRO = "mvp_observatorio_sus_es_cnes_v2/public/data/mvp-data.json"

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("zip_original", type=Path)
    a = p.parse_args()
    if hashlib.sha256(a.zip_original.read_bytes()).hexdigest() != HASH_ZIP:
        raise ValueError("MVP original diverge do hash da Ponte.")
    with ZipFile(a.zip_original) as z:
        data = z.read(MEMBRO)
    # Inspeção estrutural mínima; o contrato JS completo é aplicado antes da tela.
    parsed = json.loads(data)
    if parsed.get("schemaVersion") != "2.0.0": raise ValueError("Contrato de dados inesperado.")
    destino = Path(__file__).resolve().parents[1] / "public/data/mvp-data.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        if destino.read_bytes() != data: raise ValueError("Dados locais existentes divergentes; não sobrescrever.")
    else:
        with destino.open("xb") as f: f.write(data)
    print(json.dumps({"arquivo_local": str(destino), "sha256": hashlib.sha256(data).hexdigest(), "git": "ignorado; nao publicar"}))
