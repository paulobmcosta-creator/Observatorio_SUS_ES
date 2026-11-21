"""Cardinalidades exatas de conjuntos booleanos medidos sobre uma chave distinta."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def codificar(membros):
    """Codificar a primeira coluna no bit mais significativo, conservando a ordem informada."""
    x = np.asarray(membros)
    if x.ndim != 2 or not 1 <= x.shape[1] <= 12:
        raise ValueError("Forneça entre um e doze conjuntos.")
    if x.dtype != np.bool_:
        raise ValueError("As colunas precisam ser booleanas, completas e validadas.")
    pesos = (1 << np.arange(x.shape[1] - 1, -1, -1)).astype(np.int32)
    return x.astype(np.int32) @ pesos


def contagens(codigos, quantidade):
    """Partição completa e inclusivas. O padrão vazio inclusivo equivale ao universo."""
    codigos = np.asarray(codigos)
    capacidade = 1 << quantidade
    if np.any((codigos < 0) | (codigos >= capacidade)):
        raise ValueError("Combinação fora do domínio.")
    exclusivas = np.bincount(codigos, minlength=capacidade)
    inclusivas = exclusivas.copy()
    for bit in range(quantidade):
        for indice in range(capacidade):
            if not indice & (1 << bit):
                inclusivas[indice] += inclusivas[indice | (1 << bit)]
    return exclusivas, inclusivas


def alguma_competencia(indice, codigos, quantidade, n_chaves):
    """Contar cada chave uma vez por combinação vista em pelo menos uma competência."""
    capacidade = 1 << quantidade
    vistos = np.unique(indice.astype(np.int64) * capacidade + codigos)
    ids, mascaras = np.divmod(vistos, capacidade)
    exatas = np.bincount(mascaras, minlength=capacidade)
    inclusivas = np.array([np.unique(ids[(mascaras & m) == m]).size for m in range(capacidade)])
    if inclusivas[0] != n_chaves:
        raise ValueError("Inconsistência de cobertura das chaves.")
    return exatas, inclusivas


def matriz_distinta(tabela, chave, conjuntos):
    """Validar e tabular os membros de um universo com exatamente uma linha por chave."""
    if tabela[chave].isna().any() or tabela[chave].duplicated().any():
        raise ValueError("Chave vazia ou repetida.")
    flags = tabela[conjuntos].copy()
    for c in flags:
        if not pd.api.types.is_bool_dtype(flags[c]):
            flags[c] = flags[c].astype(str).str.lower().map({"true":True, "false":False, "1":True, "0":False})
    if flags.isna().any().any():
        raise ValueError("Pertencimento ausente ou fora do domínio.")
    ex, inc = contagens(codificar(flags.to_numpy(dtype=bool)), len(conjuntos))
    return pd.DataFrame({"padrao":[format(i, f"0{len(conjuntos)}b") for i in range(len(ex))],
                         "exclusiva":ex, "inclusiva":inc})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path)
    parser.add_argument("saida", type=Path)
    parser.add_argument("--chave", required=True)
    parser.add_argument("--conjuntos", nargs="+", required=True)
    a = parser.parse_args()
    matriz_distinta(pd.read_csv(a.entrada, dtype=str), a.chave, a.conjuntos).to_csv(a.saida, index=False)
