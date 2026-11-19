"""Consolidar AIH por atendimento, residência e cobertura efetiva do catálogo nacional."""
import argparse
import re
from collections import Counter,defaultdict
from pathlib import Path

from observatorio_sus.estudos.camila import sim
from observatorio_sus.estudos.camila.lote import executar, ler, salvar, produtos
from observatorio_sus.io.custodia import sha256_arquivo
import json


def consolidar(v,saida):
    fonte=v/"fontes/rd-lista-ftp.txt"
    esperado=defaultdict(set)
    tamanhos={}
    for linha in fonte.read_text().splitlines():
        m=re.search(r"\s(\d+)\s+(RD([A-Z]{2})(\d{4})[A-Za-z0-9_-]*\.dbc)$",linha,re.I)
        if m and "1401"<=m[4]<="2412":
            nome=m[2].upper()[:-4]
            esperado["20"+m[4],m[3]].add(nome)
            tamanhos[nome]=int(m[1])
    if len(esperado)!=132*27:
        raise ValueError("Inventário oficial sem 27 UFs em 132 competências")
    inputs={"catalogo":fonte}
    for raiz in ("sih","sih-residentes"):
        for p in (v/raiz).glob("RD*/*/recibo.json"):
            rec=json.loads(p.read_text())
            if produtos(p.parent)!=rec["saidas"]:
                raise ValueError("Recibo RD inválido")
            # Em competências de regressão os dois leitores cobrem os mesmos residentes.
            # Priorizar a tabela que contém todo o atendimento da UF.
            inputs.setdefault(p.parent.parent.name,p.parent/"fluxos.csv")
    acervo=v.parent/"acervo/CP04/Resultados"
    inputs["novembro"]=acervo/"SIH_PILOTO_FLUXOS.csv"
    inputs["producao_novembro"]=acervo/"SIH_PILOTO_PRODUCAO.csv"

    def medir(stage):
        cobertura=[]
        completo={}
        for (mes,uf),nomes in sorted(esperado.items()):
            locais=nomes&inputs.keys()
            anterior=mes=="202411" and uf=="ES" and nomes=={"RDES2411"} and not locais
            completo[mes,uf]=locais==nomes or anterior
            cobertura.append((mes,uf,len(nomes),len(locais),anterior,completo[mes,uf]))
        salvar(stage/"cobertura.csv",["competencia","uf","objetos_catalogados","dbc_reprocessados","checkpoint_agregado","completo_fluxo_regional"],cobertura)
        geos,indic,sexoidade=Counter(),Counter(),Counter()
        grupos=Counter()
        for nome,path in inputs.items():
            if not nome.startswith("RD"):
                continue
            for r in ler(path):
                mes,uf=r["competencia"],r["uf_arquivo"]
                n=int(r["aih"])
                res,at=r["municipio_res"],r["municipio_atend"]
                if uf=="ES" or res.startswith("32"):
                    geos[mes,uf,res[:2],r["regiao_res"],at[:2],r["regiao_atend"]]+=n
                    if uf=="ES":
                        grupo="atendimento_ES"
                        indic[mes,grupo]+=n
                        if r["regiao_res"]=="OUTRA_UF_CODIGO_PLAUSIVEL":
                            indic[mes,"atracao_observada"]+=n
                        elif r["regiao_res"]=="INDETERMINADO_OU_EXTERIOR":
                            indic[mes,"residencia_indeterminada_no_ES"]+=n
                    if res.startswith("32"):
                        indic[mes,"residentes_observados"]+=n
                        if uf!="ES":
                            indic[mes,"evasao_observada"]+=n
                    cid=int(r["diagnostico"][1:3])
                    for grupo in ["G0",*(g for g,(lo,hi) in sim.GRUPOS.items() if lo<=cid<=hi)]:
                        escopos=(["atendimento_ES"] if uf=="ES" else [])+(["residencia_ES_observada"] if res.startswith("32") else [])
                        for esc in escopos:
                            grupos[mes,esc,grupo]+=n
                            sexoidade[mes,esc,grupo,r["sexo_sih"],r["unidade_idade"],r["idade"]]+=n
        # O checkpoint anterior de novembro conserva fluxos regionais e grupos por atendimento.
        usa_cp04 = "RDES2411" not in inputs
        for r in ler(inputs["novembro"]) if usa_cp04 else ():
            if r["competencia_processamento"]!="202411":
                continue
            orig,dest=r["origem_residencia"],r["destino_atendimento"]
            n=int(r["aih_g0_ident1"])
            local=orig not in ["RES_OUTRA_UF_OU_INDETERMINADA"]
            geos["202411","ES","32" if local else "OUTRA_OU_IGN",orig,"32",dest]+=n
            indic["202411","atendimento_ES"]+=n
            if local:
                indic["202411","residentes_observados"]+=n
        for r in ler(inputs["producao_novembro"]) if usa_cp04 else ():
            if r["competencia_processamento"]=="202411" and r["atendimento"]=="ES":
                grupos["202411","atendimento_ES",r["grupo"]]=int(r["aih_ident1"])
        salvar(stage/"fluxos.csv",["competencia","uf_arquivo","uf_res_ibge","regiao_res","uf_at_ibge","regiao_at","aih"],((*k,n) for k,n in sorted(geos.items())))
        salvar(stage/"grupos.csv",["competencia","escopo","grupo","aih"],((*k,n) for k,n in sorted(grupos.items())))
        salvar(stage/"sexo_idade.csv",["competencia","escopo","grupo","sexo_sih","unidade_idade_sih","idade","aih"],((*k,n) for k,n in sorted(sexoidade.items())))
        meses=sorted({k[0] for k in esperado})
        series=[]
        for mes in meses:
            nuf=sum(ok for (m,_),ok in completo.items() if m==mes)
            if completo[mes,"ES"] and indic[mes,"atendimento_ES"]!=grupos[mes,"atendimento_ES","G0"]:
                raise ValueError(f"Atendimento G0 divergente {mes}")
            series.append((mes,nuf,indic.get((mes,"atendimento_ES")),indic.get((mes,"atracao_observada"),0) if (mes!="202411" or not usa_cp04) and completo[mes,"ES"] else None,
                           indic.get((mes,"residentes_observados")),indic[mes,"evasao_observada"] if nuf>1 else None,
                           indic[mes,"residentes_observados"] if nuf==27 else None,indic[mes,"evasao_observada"] if nuf==27 else None))
        salvar(stage/"serie.csv",["competencia","ufs_fluxo","atendimento_es","atracao_plausivel","residentes_observados","evasao_observada",
                                 "residentes_cobertura_nacional","evasao_cobertura_nacional"],series)
        return dict(meses_atendimento_ES=sum(completo[m,"ES"] for m in meses),
                    meses_27_ufs=[r[0] for r in series if r[1]==27],bytes_catalogo=sum(tamanhos.values()),
                    bytes_pendentes=sum(n for k,n in tamanhos.items() if k not in inputs and k!="RDES2411"))
    return executar(saida,inputs,{"ident":"1","territorio":"PDR 2024","novembro_2024":"RD conferido" if "RDES2411" in inputs else "CP04 agregado"},medir)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("v",type=Path)
    p.add_argument("saida",type=Path)
    a=p.parse_args()
    print(consolidar(a.v,a.saida)["controles"])
