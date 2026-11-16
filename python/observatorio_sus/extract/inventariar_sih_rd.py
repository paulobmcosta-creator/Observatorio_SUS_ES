"""Inventariar catálogo RD observado, preservando sufixos/partes e revisões.

Sem catálogo, declarar as 27 UFs como esperado_não_consultado, nunca zero ou
inexistência oficial. Não estima bytes de nomes inventados e não baixa arquivos.
"""
import re

UFS = tuple("AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split())


def inventariar_rd(competencia, catalogo=None, evidencia_catalogo=None):
    """Receber entradas observadas com nome/URI/revisão/bytes; retornar reconciliação.

    Aceita apenas 2008+ neste layout de nomes. Sufixos são preservados como parte,
    sem presumir precedência. Lista vazia observada requer prova; ausência de UF
    permanece pendente, não inexistência comprovada. Revisões conflitantes não
    são resolvidas por ordenação de nome ou data.
    """
    if not re.fullmatch(r"20[0-9]{2}(0[1-9]|1[0-2])", competencia) or competencia < "200801":
        raise ValueError("Competência fora do layout RD 2008+.")
    if catalogo is not None and not evidencia_catalogo:
        raise ValueError("Catálogo observado exige referência/hash de evidência.")
    objetos = []
    for entrada in catalogo or []:
        nome = entrada["nome"]
        match = re.fullmatch(r"RD([A-Z]{2})([0-9]{4})([A-Za-z0-9_-]*)\.dbc", nome, re.IGNORECASE)
        if not match or match[1].upper() not in UFS or match[2] != competencia[2:]:
            continue
        if (not entrada.get("uri_oficial") or not entrada.get("revisao") or
            type(entrada.get("bytes")) is not int or entrada["bytes"] < 0):
            raise ValueError("Objeto observado sem URI/revisão/tamanho: " + nome)
        objetos.append({**entrada, "uf": match[1].upper(), "parte": match[3] or "sem_sufixo",
                        "competencia": competencia, "status": "esperado_observado_no_catalogo"})
    nomes = [o["nome"].casefold() for o in objetos]
    conflito = len(nomes) != len(set(nomes))
    cobertura = [{"uf": uf, "objetos_observados": sum(o["uf"] == uf for o in objetos),
                  "status": "catalogado_nao_adquirido" if any(o["uf"] == uf for o in objetos) else
                  ("ausencia_nao_resolvida" if catalogo is not None else "esperado_nao_consultado")}
                 for uf in UFS]
    return {"sistema": "SIH", "familia": "RD", "competencia": competencia,
            "evidencia_catalogo": evidencia_catalogo, "objetos": objetos, "cobertura": cobertura,
            "conflito_revisoes": conflito, "bytes_observados": sum(o["bytes"] for o in objetos),
            "estado": "PENDENTE" if conflito or any(r["objetos_observados"] == 0 for r in cobertura) else "CATALOGO_27UF_NAO_VALIDA_AQUISICAO"}
