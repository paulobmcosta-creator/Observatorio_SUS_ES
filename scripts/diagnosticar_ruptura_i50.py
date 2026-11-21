"""Localizar edições por tamanho e SHA, comparar com a linha de base e salvar cobertura."""
import argparse
import os
from pathlib import Path
from observatorio_sus.estudos.camila.lote import executar, ler, salvar
from observatorio_sus.estudos.camila import sim, territorio
from observatorio_sus.io.custodia import sha256_arquivo


def investigar(acervo,custodias,destino):
    edicoes={r["ano"]:r for r in ler(sim.FONTES) if r["ano"] in ("2022","2023","2024")}
    tamanhos={int(r["bytes"]):ano for ano,r in edicoes.items()}
    encontrados={}
    for raiz in custodias:
        if not raiz.is_dir():
            raise ValueError(f"Custódia ausente: {raiz}")
        for base,_,nomes in os.walk(raiz):
            for nome in nomes:
                p=Path(base)/nome
                if p.is_symlink() or not p.is_file():
                    continue
                ano=tamanhos.get(p.stat().st_size)
                if ano and ano not in encontrados and sha256_arquivo(p)==edicoes[ano]["sha256"]:
                    encontrados[ano]=p
    anual=acervo/"CP02/Resultados/SIM_REGIONAL_G0_G5_2014_2024.csv"
    pino=next(r for r in ler(sim.TABELA.parents[2]/"config/estudos/fontes_taxas_camila.csv") if r["id"]=="anual")
    if sha256_arquivo(anual)!=pino["sha256"]:
        raise ValueError("Baseline anual diferente da edição conferida")
    baseline={(r["ano"],r["grupo"]):int(r["obitos"]) for r in ler(anual) if r["territorio"]=="ES"}
    parametros=dict(raizes=[str(r.resolve()) for r in custodias],criterio="bytes e SHA-256; prioridade 2022")
    def calcular(stage):
        linhas=[]
        for ano,r in sorted(edicoes.items()):
            atual={}
            if ano in encontrados:
                atual=sim.diagnosticar(encontrados[ano],int(ano),stage/ano,True)["controles"]
            for grupo,nome in (("G0","G0"),("G2","I50")):
                ref=baseline[ano,grupo]
                linhas.append((ano,nome,r["membro"],r["bytes"],r["sha256"],ref,atual.get(nome,""),
                               atual[nome]-ref if atual else "",
                               "dupla_leitura_original" if atual else "original_ausente_na_custodia_examinada"))
        salvar(stage/"diagnostico.csv",["ano","causa","membro_original","bytes_zip","sha256_zip",
              "baseline_CP02","original","diferenca","estado"],linhas)
        return dict(originais=sorted(encontrados),resolucao_causal="depende_da_reconciliacao_documental")
    return executar(destino,dict(edicoes=sim.FONTES,numeradores=anual,cadastro=sim.TABELA,**encontrados),
                    parametros,calcular,[Path(sim.__file__),Path(territorio.__file__)])


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("acervo",type=Path)
    p.add_argument("destino",type=Path)
    p.add_argument("--custodia",action="append",type=Path,required=True)
    a=p.parse_args()
    print(investigar(a.acervo,a.custodia,a.destino)["controles"])
