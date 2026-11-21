"""Comparação privada do SIM com o consolidado e CP02, por grau de evidência."""
import argparse
from collections import Counter
import json
from pathlib import Path

from observatorio_sus.estudos.camila import sim, territorio
from observatorio_sus.estudos.camila.lote import executar, ler, salvar
from observatorio_sus.io.custodia import sha256_arquivo
from obter_edicoes_sim_camila import localizar

BASES = {
    "CP02": "8150bc1d213a96c657cce8eceb587e344da5e6b659704da7143dffbbb77ecdb2",
    "CP03": "83e19d1cf9a7490e3b6ae9086bbb8a5fd0cf1fa9c30a3f4c3d118ad9ca52701d",
    "consolidado": "0be26dd878e6fd841db2605d7ea388b43407fdac3e099812f965651b6d6b031d",
}
REGIOES = tuple(territorio.PAGINAS)
RESIDUAL = "RES_ES_IGNORADO"
GRUPOS = ("G0", *sim.GRUPOS)
FAIXAS = [f"{i:02}" for i in range(0,90,5)]+["ignorada"]
PESOS = tuple(str(i) for i in range(30,70,5))


def fontes(acervo, anos):
    caminhos = dict(
        cp02="CP02/Resultados/SIM_REGIONAL_G0_G5_2014_2024.csv",
        inicial="consolidado/1_SIM_Populacao/MORTALIDADE_SIM_G0_G5_PROVISORIA.csv",
        qa_inicial="consolidado/1_SIM_Populacao/CONTROLES_QUALIDADE_SIM.csv",
        paridade="CP02/Resultados/PARIDADE_SIM_LEITORES.csv",
        pop="CP03/Resultados/DENOMINADOR_RIPSA_CANDIDATO.csv",
        pesos="CP03/Controles/PADRAO_BRASIL_CENSO_2010.csv",
        brutas="CP03/Resultados/MORTALIDADE_BRUTA_G0_G5_2014_2024.csv",
        taxas="CP03/Resultados/MORTALIDADE_PREMATURA_G0_2014_2024.csv")
    for ano in set(anos) & {2023,2024}:
        caminhos[f"cubo{ano}"]=f"CP02/Resultados/SIM_INTERMEDIARIOS/{ano}.json"
        caminhos[f"recibo1_{ano}"]=f"CP02/Evidencias/Origem_CP01/SIM{ano}.zip.proveniencia.json"
        caminhos[f"recibo2_{ano}"]=f"CP02/Evidencias/SIM{ano}.zip.proveniencia.json"
    refs = {}
    for pacote,pino in BASES.items():
        manifesto = acervo/pacote/"MANIFESTO_SHA256.csv"
        if sha256_arquivo(manifesto)!=pino:
            raise ValueError(f"Manifesto incompatível: {pacote}")
        refs.update({pacote+"/"+r["arquivo"]:r["sha256"] for r in ler(manifesto)})
    for caminho in caminhos.values():
        if sha256_arquivo(acervo/caminho)!=refs[caminho]:
            raise ValueError(f"Baseline incompatível: {caminho}")
    return {k:acervo/v for k,v in caminhos.items()}


def cubo_cp02(doc, edicao, paridade):
    if (doc["ano"]!=int(edicao["ano"]) or doc["source_sha256"]!=edicao["sha256"]
            or doc["membro"]!=edicao["membro"]):
        raise ValueError("Edição do intermediário divergente")
    margens = Counter()
    unicas = set()
    for t,g,f,s,n in doc["idade_sexo_grupo"]:
        chave = t,g,f,s
        if (chave in unicas or t not in ("ES",*REGIOES,RESIDUAL) or g not in GRUPOS
                or f not in FAIXAS or s not in ("1","2","ignorado") or type(n)!=int or n<=0):
            raise ValueError("Chave ou contagem inválida no intermediário")
        unicas.add(chave)
        margens[t,g,f]+=n
    obs=Counter({(t,g,b):v for t,g,b,v in doc["obs"]})
    if len(obs)!=len(doc["obs"]):
        raise ValueError("Margem duplicada no intermediário")
    for t in ("ES",*REGIOES,RESIDUAL):
        for g in GRUPOS:
            for f in FAIXAS:
                if margens[t,g,f]!=obs[t,g,f]:
                    raise ValueError("Margem de idade incompatível com idade × sexo")
            if (sum(margens[t,g,f] for f in FAIXAS)!=obs[t,g,"TODAS"] or
                    sum(margens[t,g,f] for f in PESOS)!=obs[t,g,"30_69"]):
                raise ValueError("Total ou faixa prematura divergente")
    if obs["ES","G0","TODAS"]!=doc["checks"]["G0"]:
        raise ValueError("Total G0 incompatível com o controle de elegibilidade")
    controles={"regiao_grupo_idade_sexo":len(unicas),"regiao_grupo_faixa_e_totais":len(obs),
               "exclusoes_e_sentinelas":len(doc["checks"])}
    ver=[r for r in paridade if r["ano"]==edicao["ano"]]
    if len(ver)!=3 or {r["controle"]:int(r["chaves"]) for r in ver}!=controles or any(
            r["diferencas"]!="0" or r["sha256_origem"]!=edicao["sha256"] for r in ver):
        raise ValueError("Recibo de paridade Work divergente")
    return margens


def cubo_original(diretorio):
    contagens=Counter()
    for r in ler(diretorio/"csv.csv"):
        cat=int(r["causa_basica"][1:3])
        grupos=["G0",*(g for g,(lo,hi) in sim.GRUPOS.items() if lo<=cat<=hi)]
        faixa={"85+":"85","IGNORADA":"ignorada"}.get(r["idade_quinquenal"],r["idade_quinquenal"])
        for g in grupos:
            for t in ("ES",r["regiao"]):
                contagens[t,g,faixa]+=int(r["obitos"])
    return contagens


def processar(acervo, raizes, destino, anos):
    entradas=fontes(acervo,anos)
    edicoes={int(r["ano"]):r for r in ler(sim.FONTES)}
    locais=localizar(raizes,[edicoes[a] for a in anos])
    entradas.update({f"zip{y}":p for y,p in locais.items()}, cadastro=sim.TABELA, edicoes=sim.FONTES)

    def medir(stage):
        def indexar(chave):
            return {(int(r["ano"]),r["territorio"],r["grupo"]):r for r in ler(entradas[chave])}
        inicial, cp02, brutas = (indexar(k) for k in ("inicial","cp02","brutas"))
        pop={(int(r["ano"]),r["territorio"],r["faixa"]):int(r["habitantes"]) for r in ler(entradas["pop"])}
        pesos={r["idade_inicio"]:float(r["peso_30_69"]) for r in ler(entradas["pesos"]) if r["peso_30_69"]}
        if set(pesos)!=set(PESOS) or abs(sum(pesos.values())-1)>1e-12:
            raise ValueError("Pesos de padronização incompatíveis")
        prem_cp={(int(r["ano"]),r["territorio"]):r for r in ler(entradas["taxas"])}
        anual,idades,qualidade,retencao,revisoes,prematuras=[],[],[],[],[],[]
        cobertura=[]
        for ano in anos:
            ed=edicoes[ano]
            for r in ler(entradas["qa_inicial"]):
                if int(r["ano"])==ano:
                    qualidade.append((ano,"controle_consolidado",r["controle"],r["valor"]))
            bases={}
            if f"cubo{ano}" in entradas:
                doc=json.loads(entradas[f"cubo{ano}"].read_text())
                bases["intermediario_CP02"]=cubo_cp02(doc,ed,ler(entradas["paridade"]))
                for k,v in doc["checks"].items():
                    qualidade.append((ano,"intermediario_CP02",k,v))
                recs=[json.loads(entradas[f"recibo{i}_{ano}"].read_text()) for i in (1,2)]
                if any(r["sha256"]!=ed["sha256"] or r["membro"]!=ed["membro"] for r in recs):
                    raise ValueError("Recibos históricos e edição federal divergem")
                revisoes.append((ano,ed["sha256"],ed["last_modified"],*[r["sha256_conteudo"] for r in recs],
                                 "mesmo_membro" if recs[0]["sha256_conteudo"]==recs[1]["sha256_conteudo"] else "divergencia"))
            else:
                revisoes.append((ano,ed["sha256"],ed["last_modified"],"","","uma_edicao_identificada"))
            if str(ano) in locais:
                pasta=stage/str(ano)
                recibo=sim.diagnosticar(locais[str(ano)],ano,pasta)
                bases["original_dupla_leitura"]=cubo_original(pasta)
                for k,v in recibo["controles"]["qa"].items():
                    qualidade.append((ano,"original_dupla_leitura",k,v))
            origem = "original_dupla_leitura" in bases
            historico = "intermediario_CP02" in bases
            cobertura.append((ano,ed["membro"],ed["sha256"],int(origem),int(historico),
                              "original" if origem else "CP02" if historico else "legado",
                              "disponivel" if origem else "requer_original",
                              "disponivel" if origem or historico else "requer_original"))
            for nivel,m in bases.items():
                for g in GRUPOS:
                    for f in FAIXAS:
                        if m["ES",g,f]!=sum(m[t,g,f] for t in (*REGIOES,RESIDUAL)):
                            raise ValueError("Balanço entre estado, regiões e resíduo diverge")
                for t in ("ES",*REGIOES,RESIDUAL):
                    for f in FAIXAS:
                        anterior=bases["intermediario_CP02"][t,"G2",f] if historico else None
                        delta=m[t,"G2",f]-anterior if nivel=="original_dupla_leitura" and historico else None
                        idades.append((ano,t,f,nivel,m[t,"G2",f],m[t,"G0",f],delta))
            for g in GRUPOS:
                valores_reg=[int(cp02[ano,t,g]["obitos"]) for t in REGIOES]
                reter=any(0<n<10 for n in valores_reg)
                for t in ("ES",*REGIOES):
                    old=inicial[ano,t,g]
                    base=int(cp02[ano,t,g]["obitos"])
                    atual={nivel:sum(m[t,g,f] for f in FAIXAS) for nivel,m in bases.items()}
                    retencao.append((ano,t,g,int(reter),old["status"],old["obitos"],base))
                    n=atual.get("original_dupla_leitura")
                    inter=atual.get("intermediario_CP02")
                    d=pop[ano,t,"TODAS"]
                    taxa_cp03=brutas[ano,t,g]["taxa_100mil"]
                    taxa_original=round(n/d*100000,6) if n is not None else None
                    delta_taxa=round(taxa_original-float(taxa_cp03),6) if n is not None else None
                    anual.append((ano,t,g,old["obitos"],base,inter,n,
                                  inter-base if inter is not None else None,n-base if n is not None else None,
                                  d,taxa_original,taxa_cp03,delta_taxa))
            if "original_dupla_leitura" in bases:
                m=bases["original_dupla_leitura"]
                for t in ("ES",*REGIOES):
                    anterior=prem_cp[ano,t]
                    n=sum(m[t,"G0",f] for f in PESOS)
                    den=pop[ano,t,"30_69"]
                    if den!=sum(pop[ano,t,f] for f in PESOS):
                        raise ValueError("Denominador prematuro inconsistente")
                    pad=100000*sum(pesos[f]*m[t,"G0",f]/pop[ano,t,f] for f in PESOS)
                    prematuras.append((ano,t,n,den,round(n/den*100000,6),round(pad,6),anterior["obitos_30_69"],
                                       n-int(anterior["obitos_30_69"]),anterior["taxa_padronizada_100mil"],
                                       anterior["estado_padronizacao"],
                                       round(pad-float(anterior["taxa_padronizada_100mil"]),6)
                                       if anterior["taxa_padronizada_100mil"] else None))
        salvar(stage/"confronto_anual.csv","ano territorio grupo consolidado CP02 intermediario_CP02 original delta_intermediario_CP02 delta_original_CP02 populacao taxa_original_100mil taxa_100mil_CP03 delta_taxa_100mil".split(),anual)
        salvar(stage/"cobertura.csv","ano membro sha256_zip original_relido cubo_CP02 fonte_mais_detalhada mes_municipio_subcategoria_I50 idade_regiao_I50".split(),cobertura)
        salvar(stage/"i50_por_idade.csv","ano territorio idade_inicial nivel I50 G0 delta_I50_original_menos_cubo_CP02".split(),idades)
        salvar(stage/"qa.csv","ano nivel controle valor".split(),qualidade)
        salvar(stage/"regra_historica_divulgacao.csv","ano territorio grupo reter_grupo_previsto status_consolidado valor_consolidado valor_CP02".split(),retencao)
        salvar(stage/"edicoes.csv","ano sha256_zip last_modified sha256_membro_CP01 sha256_membro_CP02 comparacao_historica".split(),revisoes)
        salvar(stage/"prematura_desde_original.csv","ano territorio obitos populacao taxa_bruta_100mil taxa_padronizada_100mil obitos_CP03 delta_obitos padronizada_CP03 estado_CP03 delta_padronizada_100mil".split(),prematuras)
        return dict(anos=anos,originais_relidos=sorted(locais),compatibilidade=dict(
            pares_consolidado_preenchidos=sum(r[3]!="" for r in anual),
            divergencias_preenchidas=sum(r[3]!="" and int(r[3])!=r[4] for r in anual),
            pares_intermediario=sum(r[5] is not None for r in anual),
            divergencias_intermediario=sum(r[7] not in (None,0) for r in anual) if any(r[5] is not None for r in anual) else None,
            pares_original=sum(r[6] is not None for r in anual),
            divergencias_original=sum(r[8] not in (None,0) for r in anual) if locais else None),
            prematuras_desde_original=len(prematuras))
    return executar(destino,entradas,{"anos":anos,"unidade":"obitos_residencia_ES"},medir,
                    [Path(sim.__file__),Path(territorio.__file__),Path(__file__).with_name("obter_edicoes_sim_camila.py")])


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("acervo",type=Path)
    parser.add_argument("destino",type=Path)
    parser.add_argument("--custodia",action="append",required=True,type=Path)
    parser.add_argument("--anos",type=int,nargs="+",default=[2022,2023,2024],choices=range(2014,2025))
    a=parser.parse_args()
    print(json.dumps(processar(a.acervo,a.custodia,a.destino,list(dict.fromkeys(a.anos)))["controles"],ensure_ascii=False))
