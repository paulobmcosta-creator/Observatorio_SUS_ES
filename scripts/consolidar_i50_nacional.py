"""Comparações descritivas e figuras privadas a partir dos agregados nacionais."""
import argparse
import json
from importlib.metadata import version
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import investigar_i50_nacional as nacional
from observatorio_sus.estudos.camila.lote import executar, produtos
from observatorio_sus.io.custodia import sha256_arquivo

REGIOES = {
    "Norte": "AC AP AM PA RO RR TO", "Nordeste": "AL BA CE MA PB PE PI RN SE",
    "Centro-Oeste": "DF GO MT MS", "Sudeste": "ES MG RJ SP", "Sul": "PR RS SC",
}
REGIAO = {uf: r for r, lista in REGIOES.items() for uf in lista.split()}
ANOS = (2022, 2023, 2024)


def territorios(df):
    blocos = [df.assign(territorio=df.uf), df.assign(territorio=df.uf.map(REGIAO)),
              df.assign(territorio="Brasil"), df[df.uf != "ES"].assign(territorio="Brasil sem ES"),
              df[df.uf.isin(["MG", "RJ", "SP"])].assign(territorio="Sudeste sem ES")]
    return pd.concat(blocos, ignore_index=True)


def percent(n, d):
    return 100 * n / d.where(d.ne(0))


def medidas(df):
    out = df.copy()
    out["pct_I50_em_G0"] = percent(df.I50, df.G0)
    out["pct_mencao_entre_obitos"] = percent(df.mencao_atestado, df.obitos)
    out["pct_mencao_atestado_com_CID"] = percent(df.mencao_atestado, df.atestado_com_cid)
    out["pct_selecionada_entre_mencoes"] = percent(df.I50_e_mencao, df.mencao_atestado)
    return out


def figuras(pasta, mensal, anual):
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axs = plt.subplots(2, 1, figsize=(10, 7), sharex=True, layout="constrained")
    for ax, campo, titulo in zip(axs, ("pct_I50_em_G0", "pct_mencao_entre_obitos"),
                                 ("I50 como causa básica entre óbitos circulatórios",
                                  "Menção de I50 no atestado entre todos os óbitos")):
        for t, cor in (("Brasil sem ES", "#555555"), ("Sudeste sem ES", "#297f78"), ("ES", "#aa412a")):
            d = mensal[mensal.territorio == t].sort_values(["ano", "mes"])
            ax.plot(range(len(d)), d[campo], label=t, color=cor, lw=2)
        ax.set(title=titulo, ylabel="%")
        ax.grid(axis="y", alpha=.25)
    axs[0].legend(ncol=3, loc="center", bbox_to_anchor=(.5, .65), frameon=False)
    axs[1].set_xticks(range(0, 36, 3), [f"{m:02}/{y}" for y in ANOS for m in (1,4,7,10)], rotation=30)
    fig.savefig(pasta / "serie_mensal.png", dpi=160)
    plt.close(fig)

    estados = anual[anual.territorio.isin(REGIAO)].pivot(index="territorio", columns="ano", values="pct_I50_em_G0")
    estados = estados.sort_values(2024)
    fig, ax = plt.subplots(figsize=(8, 8), layout="constrained")
    for y, marca in zip(ANOS, ("o", "x", "^")):
        ax.scatter(estados[y], estados.index, marker=marca, label=y)
    ax.set(xlabel="I50 como causa básica entre óbitos circulatórios (%)", ylabel="UF de residência")
    ax.grid(axis="x", alpha=.25)
    ax.legend()
    fig.savefig(pasta / "comparacao_ufs.png", dpi=160)
    plt.close(fig)


def consolidar(raiz, referencia, destino):
    entradas = {}
    for ano in ANOS:
        pasta = raiz / str(ano) / "leitura"
        recibo = json.loads((pasta / "recibo.json").read_text(encoding="utf-8"))
        if produtos(pasta) != recibo["saidas"]:
            raise ValueError("Integridade da leitura anual divergente")
        for nome in ("mensal", "processamento", "matriz", "categorias", "subcategorias", "preenchimento"):
            entradas[f"{nome}_{ano}"] = pasta / f"{nome}.csv"
        entradas[f"recibo_{ano}"] = pasta / "recibo.json"
        anterior = referencia / str(ano)
        recibo_es = json.loads((anterior / "recibo.json").read_text(encoding="utf-8"))
        cubo = anterior / "csv.csv"
        if (sha256_arquivo(cubo) != recibo_es["saidas"]["csv.csv"] or
                recibo_es["contrato"]["entradas"]["original"] != recibo["contrato"]["entradas"]["zip"]):
            raise ValueError("Referência ES incompatível")
        entradas[f"ES_{ano}"] = cubo

    def medir(stage):
        def carregar(nome, **kwargs):
            return pd.concat([pd.read_csv(entradas[f"{nome}_{a}"], keep_default_na=False, **kwargs)
                              for a in ANOS], ignore_index=True)

        def salvar(df, nome):
            df.to_csv(stage / (nome + ".csv"), index=False, float_format="%.8f")

        df = carregar("mensal")
        if len(df) != 3 * 27 * 12 or df.duplicated(["ano", "mes", "uf"]).any():
            raise ValueError("Cobertura UF-mês divergente")
        for ano in ANOS:
            cubo = pd.read_csv(entradas[f"ES_{ano}"])
            cubo["I50"] = cubo.obitos.where(cubo.causa_basica.str.startswith("I50"), 0)
            esperado = cubo.groupby("mes")[["obitos", "I50"]].sum()
            atual = df[(df.ano == ano) & (df.uf == "ES")].set_index("mes").sort_index()
            esperado = esperado.rename(columns={"obitos": "G0"}).reindex(atual.index, fill_value=0)
            if not esperado.equals(atual[["G0", "I50"]]):
                raise ValueError("Divergência mensal na reconstrução do ES")
        geo = territorios(df)
        def agregar(chaves):
            return medidas(geo.groupby(chaves, as_index=False)[nacional.MEDIDAS].sum())
        mensal = agregar(["ano", "mes", "territorio"])
        anual = agregar(["ano", "territorio"])
        salvar(mensal, "geografia_mensal")
        salvar(anual, "geografia_anual")
        ufs = anual[anual.territorio.isin(REGIAO)].pivot(index="territorio", columns="ano", values="pct_I50_em_G0")
        ufs["delta_pp_22_24"] = ufs[2024] - ufs[2022]
        ufs["ordem_delta_asc"] = ufs.delta_pp_22_24.rank(method="min")
        salvar(ufs.reset_index(), "variacoes_UF")

        proc = carregar("processamento", dtype={"scb": str, "sistema": str, "altcausa": str})
        campos = nacional.MEDIDAS[:6]
        for eixo in ("cadastro", "scb", "sistema", "altcausa"):
            tab = proc.groupby(["ano","mes","uf", eixo], as_index=False)[campos].sum()
            tab["pct_I50_em_G0"] = percent(tab.I50, tab.G0)
            salvar(tab, "por_" + eixo)
        for filtro, nome in ((proc.cadastro.str[:4].eq(proc.ano.astype(str)), "cadastro_no_ano"),
                             (proc.cadastro.str[:4].isin(["2022","2023","2024"]), "cadastro_2022_24"),
                             (proc.scb.ne("SEM_VALOR"), "scb_preenchido")):
            sel = proc[filtro].groupby(["ano", "uf"], as_index=False)[campos].sum()
            sel["pct_I50_em_G0"] = percent(sel.I50, sel.G0)
            salvar(sel, "sensibilidade_" + nome)

        matriz = carregar("matriz")
        for campo in ("original", "pre"):
            sel = matriz[matriz[campo].str.startswith("I50") | matriz.selecionada.str.startswith("I50")]
            salvar(sel.groupby(["ano", "uf", campo, "selecionada"], as_index=False).n.sum(), "pares_" + campo)
        mencionados = matriz[matriz.mencao_atestado == 1].copy()
        mencionados["categoria"] = mencionados.selecionada.str[:3]
        salvar(mencionados.groupby(["ano","mes","uf","categoria"], as_index=False).n.sum(), "basicas_com_mencao")
        cats = carregar("categorias")
        # Categorias sentinela preservadas individualmente. O capítulo R é agregado à parte.
        sentinelas = ["I11", "I13", "I20", "I21", "I25", "I42", "I46", "I48", "I50", "I51", "I64", "R98", "R99"]
        cats = pd.concat([cats[cats.categoria.isin(sentinelas)],
                          cats[cats.categoria.str.fullmatch(r"R[0-9]{2}")].assign(categoria="R00-R99")])
        def completar(tabela, campo, dominio):
            grade = pd.MultiIndex.from_product([ANOS, range(1, 13), sorted(REGIAO), dominio],
                                               names=["ano", "mes", "uf", campo])
            totais = tabela.groupby(grade.names).n.sum()
            return totais.reindex(grade, fill_value=0).reset_index()

        salvar(completar(cats, "categoria", [*sentinelas, "R00-R99"]), "causas_sentinela")
        sub = carregar("subcategorias")
        salvar(completar(sub, "cid", sorted(set(sub.cid) | {"I50", "I500", "I501", "I509"})), "subcategorias")
        salvar(carregar("preenchimento"), "preenchimento")
        figuras(stage, mensal, anual)
        return {"anos": list(ANOS), "UF_mes": len(df), "margens_ES_conferidas": 72,
                "elegiveis": int(df.obitos.sum())}

    return executar(destino, entradas, {"anos": list(ANOS), "pandas": version("pandas"),
                    "matplotlib": version("matplotlib")}, medir, [Path(nacional.__file__)])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ("raiz", "referencia", "destino"):
        p.add_argument(arg, type=Path)
    args = p.parse_args()
    print(consolidar(args.raiz, args.referencia, args.destino)["controles"])

