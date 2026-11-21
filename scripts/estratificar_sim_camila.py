"""Numeradores do TCC por residência, sexo e idade com a elegibilidade do SIM preservada."""
import argparse
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
from investigar_i50_nacional import I50_NO_TEXTO, LINHAS
from observatorio_sus.estudos.camila import sim, territorio
from observatorio_sus.estudos.camila.lote import executar, ler, salvar
from observatorio_sus.io.custodia import sha256_arquivo


def processar(manifesto, saida):
    edicoes = {r["ano"]: r for r in ler(sim.FONTES)}
    regioes = territorio.mapa()
    for r in ler(manifesto):
        ano = r["ano"]
        ed = edicoes[ano]
        arquivo = Path(r["arquivo"])
        if sha256_arquivo(arquivo) != ed["sha256"]:
            raise ValueError(f"Original divergente em {ano}")

        def medir(stage):
            cubo, insuf, idades = Counter(), Counter(), Counter()
            campos = set(sim.CAMPOS + ["SEXO", "CAUSABAS_O", "ATESTADO", *LINHAS])
            origem = 0
            with ZipFile(arquivo) as z, z.open(ed["membro"]) as stream:
                for b in pd.read_csv(stream, sep=";", encoding="latin1", dtype=str, keep_default_na=False,
                                     usecols=lambda c: c.strip().upper() in campos, chunksize=100000):
                    b.columns = b.columns.str.strip().str.upper()
                    if not campos <= set(b.columns):
                        raise ValueError(f"Layout incompleto {ano}: {campos-set(b.columns)}")
                    origem += len(b)
                    b = b.loc[b.TIPOBITO.str.strip().eq("2") & b.CODMUNRES.str.strip().str.startswith("32")].copy()
                    b = b.apply(lambda col: col.str.strip())
                    data = pd.to_datetime(b.DTOBITO.where(b.DTOBITO.str.fullmatch(r"[0-9]{7,8}")).str.zfill(8),
                                          format="%d%m%Y", errors="coerce")
                    b = b.loc[data.dt.year.eq(int(ano))].copy()
                    b["mes"] = data.loc[b.index].dt.month
                    b["regiao"] = b.CODMUNRES.map(regioes).fillna("RES_ES_IGNORADO")
                    b["final"] = b.CAUSABAS.map(sim.causa)
                    b["original"] = b.CAUSABAS_O.map(sim.causa)
                    b["sexo"] = b.SEXO.where(b.SEXO.isin(["1","2"]), "IGNORADO")
                    b["faixa"] = b.IDADE.map(sim.faixa).replace({"85+":"80"})
                    b["mencao_atestado"] = b.ATESTADO.str.contains(I50_NO_TEXTO)
                    b["mencao_linhas"] = b[LINHAS].apply(lambda c: c.str.contains(I50_NO_TEXTO)).any(axis=1)
                    b["ampliada"] = b.final.str.startswith("I50") | b.final.isin(["I110","I130","I132"])
                    b["i50_final"] = b.final.str.startswith("I50")
                    b["i50_original"] = b.original.str.startswith("I50")
                    hf = b.loc[b[["mencao_linhas","mencao_atestado","ampliada","i50_original"]].any(axis=1)]
                    keys = ["mes","regiao","sexo","faixa","original","final","i50_original","i50_final","ampliada","mencao_atestado","mencao_linhas"]
                    insuf.update(hf.groupby(keys).size().to_dict())
                    circ = b.loc[b.final.str.fullmatch(r"I[0-9]{2}[A-Z0-9]?")]
                    cubo.update(circ.groupby(["mes","CODMUNRES","regiao","sexo","faixa","final"]).size().to_dict())
                    idades.update(circ.groupby(["IDADE","faixa","SEXO","sexo"]).size().to_dict())
            for name, cols, tab in [("cardiovascular",["mes","municipio","regiao","sexo","faixa","final"],cubo),
                                    ("insuficiencia",keys,insuf),("idade_sexo",["idade_bruta","faixa","sexo_bruto","sexo"],idades)]:
                salvar(stage / (name+".csv"), [*cols,"obitos"], ((*k,v) for k,v in sorted(tab.items())))
            return dict(ano=int(ano), registros=origem, G0=cubo.total(), declaracoes_selecionadas=insuf.total())

        recibo = executar(saida / ano, {"original":arquivo, "territorio":territorio.TABELA,"edicoes":sim.FONTES},
                          {"ano":ano,"terminal":80}, medir, [Path(sim.__file__),Path(__file__).with_name("investigar_i50_nacional.py")])
        print(ano, recibo["id"], flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifesto",type=Path)
    p.add_argument("saida",type=Path)
    a = p.parse_args()
    processar(a.manifesto, a.saida)
