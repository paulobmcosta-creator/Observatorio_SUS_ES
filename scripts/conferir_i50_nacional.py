"""Recontar as margens nacionais e confrontar os campos de processamento no ES."""
import argparse
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

import investigar_i50_nacional as estudo
from observatorio_sus.estudos.camila.lote import executar, ler, salvar
from observatorio_sus.io.custodia import sha256_arquivo

CAMPOS = ("TIPOBITO DTOBITO CODMUNRES CAUSABAS CAUSABAS_O ATESTADO ALTCAUSA "
          "DTCADASTRO DTINVESTIG VERSAOSCB TP_ALTERA CB_ALT").split()


def conferir(ano, zip_path, mensal, destino):
    ed = next(r for r in ler(estudo.sim.FONTES) if int(r["ano"]) == ano)
    if sha256_arquivo(zip_path) != ed["sha256"]:
        raise ValueError("ZIP divergente")

    def medir(stage):
        blocos = []
        pares = Counter()
        with ZipFile(zip_path) as z, z.open(ed["membro"]) as stream:
            for b in pd.read_csv(stream, sep=";", dtype=str, keep_default_na=False, encoding="latin1",
                                 usecols=lambda c: c.upper() in CAMPOS, chunksize=60000):
                b.columns = b.columns.str.upper()
                b = b.apply(lambda col: col.str.strip())
                data = pd.to_datetime(b.DTOBITO.where(b.DTOBITO.str.fullmatch(r"[0-9]{7,8}")).str.zfill(8),
                                      format="%d%m%Y", errors="coerce")
                b["uf"] = b.CODMUNRES.str[:2].map(estudo.UFS)
                b["mes"] = data.dt.month
                b = b[b.uf.notna() & data.dt.year.eq(ano) & b.TIPOBITO.eq("2")].copy()
                fim, orig = b.CAUSABAS.str.upper(), b.CAUSABAS_O.str.upper()
                b["obitos"] = 1
                b["G0"] = fim.str.fullmatch(r"I[0-9]{2}(?:\.?[A-Z0-9])?")
                b["I50"] = fim.str.fullmatch(r"I50(?:\.?[A-Z0-9])?")
                b["I50_original"] = orig.str.fullmatch(r"I50(?:\.?[A-Z0-9])?")
                b["mencao_atestado"] = b.ATESTADO.str.contains(estudo.I50_NO_TEXTO)
                blocos.append(b.groupby(["mes","uf"])[list(medidas)].sum())
                es = b[b.uf.eq("ES") & (b.I50 | b.I50_original)].copy()
                es["mes_cadastro"] = pd.to_datetime(es.DTCADASTRO.str.zfill(8), format="%d%m%Y",
                                                     errors="coerce").dt.strftime("%Y-%m").fillna("")
                es["dtinvestig_preenchida"] = es.DTINVESTIG.ne("")
                investigacao = pd.to_datetime(es.DTINVESTIG.str.zfill(8), format="%d%m%Y", errors="coerce")
                es["mes_investigacao"] = investigacao.dt.strftime("%Y-%m").fillna("SEM_DATA_VALIDA")
                chaves = ["mes", "mes_cadastro", "mes_investigacao", "CAUSABAS_O", "CAUSABAS", "VERSAOSCB", "ALTCAUSA",
                          "dtinvestig_preenchida", "TP_ALTERA", "CB_ALT"]
                pares.update(es.groupby(chaves).size().to_dict())
        atual = pd.concat(blocos).groupby(level=["mes","uf"]).sum()
        base = pd.read_csv(mensal).set_index(["mes","uf"])[list(medidas)]
        atual = atual.reindex(base.index, fill_value=0)
        delta = atual - base
        if (delta != 0).any().any():
            raise ValueError(f"Margens nacionais divergentes: {delta.abs().sum().to_dict()}")
        salvar(stage / "pares_processamento_ES.csv", [*chaves,"n"],
               ((*k, v) for k, v in sorted(pares.items())))
        return dict(ano=ano, margens=delta.size, diferencas=0, medidas=medidas)

    medidas = ["obitos","G0","I50","I50_original","mencao_atestado"]
    return executar(destino, {"zip":zip_path,"mensal":mensal,"edicoes":estudo.sim.FONTES},
                    {"ano":ano, "pandas":pd.__version__}, medir, [Path(estudo.__file__)])


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("ano", type=int, choices=(2022,2023,2024))
    for arg in ("zip", "mensal", "destino"):
        p.add_argument(arg, type=Path)
    a = p.parse_args()
    print(conferir(a.ano, a.zip, a.mensal, a.destino)["controles"])

