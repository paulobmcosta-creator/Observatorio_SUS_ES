"""Validar provas SIH recebidas legitimamente; nunca transformar fixture em empírico."""
import argparse
from pathlib import Path
from observatorio_sus.io.aceite_sih import preparar_ou_verificar

if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plano", required=True, type=Path)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--saida", type=Path)
    g.add_argument("--aceite", type=Path)
    a = p.parse_args()
    print(preparar_ou_verificar(a.plano, a.saida, a.aceite))
