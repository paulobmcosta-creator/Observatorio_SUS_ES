"""Padronização direta com uma referência fixa e estratos explícitos."""
from math import fsum, isclose, isfinite


def pesos(contagens, faixas):
    if any(a not in contagens or contagens[a] <= 0 for a in faixas):
        raise ValueError("População de referência incompleta")
    total = sum(contagens[a] for a in faixas)
    return {a: contagens[a]/total for a in faixas}


def direta(obitos, habitantes, referencia):
    if not referencia or not isclose(fsum(referencia.values()),1,rel_tol=0,abs_tol=1e-12):
        raise ValueError("Vetor de pesos incompatível")
    if any(not isfinite(w) or w <= 0 for w in referencia.values()):
        raise ValueError("Peso inválido")
    if any(a not in habitantes or habitantes[a] <= 0 or a not in obitos for a in referencia):
        return None
    if any(obitos[a] < 0 for a in referencia):
        raise ValueError("Óbitos negativos")
    return 100000 * fsum(w * obitos[a]/habitantes[a] for a,w in referencia.items())
