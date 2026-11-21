"""Reunir as onze edições reprocessadas e documentar os desvios dos checkpoints."""
import argparse
import json
from pathlib import Path

from observatorio_sus.estudos.camila import sim
from observatorio_sus.estudos.camila.lote import executar, ler, produtos, salvar


def consolidar(historico, recentes, destino):
    anos = range(2014, 2025)
    edicoes = {r["ano"]: r["sha256"] for r in ler(sim.FONTES)}
    entradas = {"edicoes": sim.FONTES}
    for ano in anos:
        pasta = historico / str(ano) / "comparacao" if ano < 2022 else recentes
        entradas[f"contagens{ano}"] = pasta / "confronto_anual.csv"
        entradas[f"prematuras{ano}"] = pasta / "prematura_desde_original.csv"
        entradas[f"recibo{ano}"] = pasta / "recibo.json"
        if ano <= 2022 and produtos(pasta) != json.loads((pasta / "recibo.json").read_text(encoding="utf-8"))["saidas"]:
            raise ValueError("Recibo de comparação incompatível")
        evidencia = json.loads((pasta / str(ano) / "recibo.json").read_text(encoding="utf-8"))
        if evidencia["contrato"]["entradas"]["original"] != edicoes[str(ano)]:
            raise ValueError(f"Edição divergente em {ano}")

    def medir(stage):
        n_preenchidas = 0
        totais = {}
        for tipo in ("contagens", "prematuras"):
            linhas = []
            for ano in anos:
                regs = [r for r in ler(entradas[f"{tipo}{ano}"]) if r["ano"] == str(ano)]
                chaves = {(r["territorio"], r.get("grupo")) for r in regs}
                territorios = {"ES", "Central", "Norte", "Metropolitana", "Sul"}
                grupos = {"G0", *sim.GRUPOS} if tipo == "contagens" else {None}
                if len(regs) != len(chaves) or chaves != {(t, g) for t in territorios for g in grupos}:
                    raise ValueError(f"Cobertura incompleta: {tipo} {ano}")
                for r in regs:
                    valor = r["original"] if tipo == "contagens" else r["taxa_padronizada_100mil"]
                    if valor == "":
                        raise ValueError(f"Resultado primário ausente: {tipo} {ano}")
                    r["sha256_zip"] = edicoes[str(ano)]
                    if tipo == "prematuras" and r["padronizada_CP03"] == "":
                        n_preenchidas += 1
                    linhas.append(r)
            salvar(stage / f"{tipo}_2014_2024.csv", list(linhas[0]), [tuple(r.values()) for r in linhas])
            delta = "delta_original_CP02" if tipo == "contagens" else "delta_obitos"
            totais[tipo] = {"linhas": len(linhas), "divergencias_contagem": sum(int(r[delta]) != 0 for r in linhas)}
            if tipo == "prematuras":
                pares = [float(r["delta_padronizada_100mil"]) for r in linhas if r["delta_padronizada_100mil"] != ""]
                totais[tipo].update(padronizadas_antes_ausentes=n_preenchidas, pares_taxa=len(pares),
                                    diferencas_taxa=sum(v != 0 for v in pares))
        return totais

    return executar(destino, entradas, {"anos": list(anos), "padrao": "Brasil Censo 2010, 30-69"}, medir)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ("historico", "recentes", "destino"):
        p.add_argument(arg, type=Path)
    a = p.parse_args()
    print(consolidar(a.historico, a.recentes, a.destino)["controles"])

