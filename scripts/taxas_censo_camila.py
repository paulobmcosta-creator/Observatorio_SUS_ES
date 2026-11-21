"""Reconciliar 330 contagens e 55 taxas históricas e calcular a especificação v3."""
import argparse
import json
from collections import Counter
from pathlib import Path

from observatorio_sus.estudos.camila import populacao, popsvs, sim, territorio
from observatorio_sus.estudos.camila.lote import executar, ler, salvar, produtos
from observatorio_sus.io.custodia import sha256_arquivo
from observatorio_sus.transform import padronizacao as pad

FAIXAS = list(range(0,85,5))
PREM = list(range(30,70,5))
TERRITORIOS = ["ES", *territorio.PAGINAS, "ES sem Norte"]
GRUPOS = ["G0",*sim.GRUPOS]


def censo2022(path):
    obj, = json.loads(path.read_text(encoding="utf8"))
    if obj["id"] != "93" or obj["unidade"] != "Pessoas":
        raise ValueError("Variável censitária incompatível")
    categorias = {}
    for r in obj["resultados"]:
        c = {x["id"]:next(iter(x["categoria"].items())) for x in r["classificacoes"]}
        s, = r["series"]
        if c["286"][0] != "113635" or s["localidade"]["nivel"]["id"]!="N1" or s["localidade"]["id"]!="1":
            raise ValueError("Recorte SIDRA divergente")
        chave = (c["2"][0],c["287"][1])
        if chave in categorias:
            raise ValueError("Duplicidade SIDRA")
        categorias[chave] = int(s["serie"]["2022"])
    labels = [f"{a} a {a+4} anos" for a in range(0,100,5)]+["100 anos ou mais"]
    if set(categorias)!={(s,a) for s in ["6794","4","5"] for a in ["Total",*labels]}:
        raise ValueError("Cobertura SIDRA inválida")
    for a in ["Total",*labels]:
        if categorias["6794",a]!=categorias["4",a]+categorias["5",a]:
            raise ValueError("Margem por sexo divergente no Censo")
    for s in ["6794","4","5"]:
        if sum(categorias[s,a] for a in labels)!=categorias[s,"Total"]:
            raise ValueError("Margem etária divergente no Censo")
    counts=Counter()
    for a in labels:
        counts[min(80,int(a.split()[0]))] += categorias["6794",a]
    return counts


def escopos(reg):
    yield "ES"
    if reg in territorio.PAGINAS:
        yield reg
    if reg != "Norte":
        yield "ES sem Norte"


def calcular(custodia, destino):
    acervo=custodia/"acervo"
    v=custodia/"mandato-v3"
    orig=custodia/"continuacao-nacional/serie"
    entradas={"censo":v/"fontes/censo2022.json","pdr":territorio.TABELA,
              "contagens":orig/"contagens_2014_2024.csv","prematuras":orig/"prematuras_2014_2024.csv"}
    for r in ler(populacao.PIN):
        if r["id"] in ("dem","pop","pesos"):
            arq=acervo/r["membro"]
            if sha256_arquivo(arq)!=r["sha256"]:
                raise ValueError("Edição de denominadores/pesos divergente")
            entradas[r["id"]]=arq
    for a in range(2014,2025):
        d=v/"estratos"/str(a)
        if produtos(d)!=json.loads((d/"recibo.json").read_text())["saidas"]:
            raise ValueError(f"Cubo alterado em {a}")
        entradas[f"sim{a}"]=d/"cardiovascular.csv"
    for path in (v/"fontes/pops").glob("POPSBR*.zip"):
        meta=path.with_suffix(".zip.proveniencia.json")
        if not meta.exists() or sha256_arquivo(path)!=json.loads(meta.read_text(encoding="utf8"))["sha256"]:
            raise ValueError("POPSVS sem origem validada")
        entradas[path.stem]=path
    def medir(stage):
        reg=territorio.mapa()
        populacao.conferir(entradas, stage, reg)
        den, num = Counter(), Counter()
        mar, conjunto = Counter(), Counter()
        counts={"2022":censo2022(entradas["censo"]), "2010":Counter()}
        for r in ler(entradas["pesos"]):
            counts["2010"][min(80,int(r["idade_inicio"]))]+=int(r["populacao"])
        w={(c,universo):pad.pesos(vetor,faixas) for c,vetor in counts.items()
           for universo,faixas in [("todas",FAIXAS),("30-69",PREM)]}
        salvar(stage/"pesos.csv",["censo","idade_inicio","populacao","peso_todas","peso_30_69"],
              ((c,a,n,w[c,"todas"][a],w[c,"30-69"].get(a,"")) for c in counts for a,n in sorted(counts[c].items())))
        for r in ler(entradas["dem"]):
            ano,m=int(r["co_anomes"][:4]),r["co_ibge"]
            val=populacao.integer(r["vl_indicador_calculado_mun"])
            if r["sg_categoria"]=="Idade":
                a=populacao.IDADES[r["ds_item_categoria"]]
                mar[ano,m,"idade",a]=val
                for t in escopos(reg[m]):
                    den[ano,t,"T",a//5*5]+=val
            elif r["sg_categoria"]=="PESSOA1":
                sexo={"Masculino":"1","Feminino":"2"}[r["ds_item_categoria"]]
                mar[ano,m,"sexo",sexo]=val
        for r in ler(entradas["pop"]):
            conjunto[int(r["ano"]),r["ibge7"][:6],r["sexo"],int(r["idade_codigo"])]=int(r["habitantes"])
        mun7={r["cod_municipio_ibge"]:r["regiao_nome"] for r in ler(territorio.TABELA)}
        for key,path in entradas.items():
            if key.startswith("POPSBR"):
                ano, extra=popsvs.read_population(path,mun7)
                for (m,sex,a),val in extra.items():
                    k=(ano,m[:6],str(sex),a)
                    if k in conjunto:
                        raise ValueError("Edições sobrepostas")
                    conjunto[k]=val
        anos_sexo=sorted({k[0] for k in conjunto})
        qa=[]
        for ano in anos_sexo:
            for m in reg:
                for a in range(81):
                    total=sum(conjunto[ano,m,s,a] for s in ["1","2"])
                    qa.append((ano,m,"idade",a,mar[ano,m,"idade",a],total))
                for s in ["1","2"]:
                    total=sum(conjunto[ano,m,s,a] for a in range(81))
                    qa.append((ano,m,"sexo",s,mar[ano,m,"sexo",s],total))
        salvar(stage/"margens_conjuntas.csv",["ano","municipio","dominio","estrato","dem","popsvs"],qa)
        if any(r[-2]!=r[-1] for r in qa):
            raise ValueError("Edições populacionais divergem. Consulte as diferenças no staging.")
        for (ano,m,s,a),val in conjunto.items():
            for t in escopos(reg[m]):
                den[ano,t,s,a//5*5]+=val
        for ano in range(2014,2025):
            for r in ler(entradas[f"sim{ano}"]):
                cid=int(r["final"][1:3])
                grupos=["G0",*(g for g,(lo,hi) in sim.GRUPOS.items() if lo<=cid<=hi)]
                for t in escopos(r["regiao"]):
                    for s in ["T",r["sexo"]]:
                        for g in grupos:
                            a=-1 if r["faixa"]=="IGNORADA" else int(r["faixa"])
                            num[ano,t,s,g,a]+=int(r["obitos"])
        antigas={(int(r["ano"]),r["territorio"],r["grupo"]):int(r["original"]) for r in ler(entradas["contagens"])}
        prem={(int(r["ano"]),r["territorio"]):float(r["taxa_padronizada_100mil"]) for r in ler(entradas["prematuras"])}
        linhas,esp,qa_hist=[],[],[]
        for ano in range(2014,2025):
            for t in TERRITORIOS:
                for s in ["T","1","2","IGNORADO"]:
                    d={a:den[ano,t,s,a] for a in FAIXAS if (ano,t,s,a) in den}
                    for g in GRUPOS:
                        n={a:num[ano,t,s,g,a] for a in FAIXAS}
                        ig=num[ano,t,s,g,-1]
                        total=sum(n.values())+ig
                        if s=="T" and t!="ES sem Norte" and total!=antigas[ano,t,g]:
                            raise ValueError(f"Contagem histórica divergente: {ano} {t} {g}")
                        for a in FAIXAS:
                            val=d.get(a)
                            esp.append((ano,t,s,g,a,n[a],val,100000*n[a]/val if val else None))
                        for c in counts:
                            for univ,faixas in [("todas",FAIXAS),("30-69",PREM)]:
                                if univ=="30-69" and g!="G0":
                                    continue
                                ob=total if univ=="todas" else sum(n[a] for a in faixas)
                                hab=sum(d[a] for a in faixas) if all(a in d for a in faixas) else None
                                taxa=pad.direta(n,d,w[c,univ])
                                linhas.append((ano,t,s,g,univ,c,ob,ig if univ=="todas" else 0,hab,
                                               100000*ob/hab if hab else None,taxa))
                                if s=="T" and t!="ES sem Norte" and c=="2010" and univ=="30-69":
                                    qa_hist.append((ano,t,prem[ano,t],taxa,taxa-prem[ano,t]))
        if len(qa_hist)!=55 or any(abs(r[-1])>0.000001 for r in qa_hist):
            raise ValueError("As 55 taxas históricas não reconciliam")
        salvar(stage/"indicadores.csv",["ano","territorio","sexo_sim","grupo","universo","censo","obitos",
              "idade_ignorada","habitantes","bruta_100mil","direta_100mil"],linhas)
        salvar(stage/"especificas.csv",["ano","territorio","sexo_sim","grupo","idade_inicio","obitos","habitantes","taxa_100mil"],esp)
        salvar(stage/"confronto_2010.csv",["ano","territorio","historica","recalculada","delta"],qa_hist)
        return dict(anos_sexo=anos_sexo, censo2022=sum(counts["2022"].values()), censo2010=sum(counts["2010"].values()),
                    comparacoes_contagens=len(antigas), comparacoes_prematuras=len(qa_hist), margens=len(qa),
                    comparador="ES menos municípios da Norte, inclui residência estadual sem município")
    return executar(destino,entradas,{"terminal":80,"principal":"2022","sensibilidade":"2010"},medir,
                    [Path(x.__file__) for x in (pad,populacao,popsvs,sim,territorio)])


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("custodia",type=Path)
    p.add_argument("destino",type=Path)
    a=p.parse_args()
    print(calcular(a.custodia,a.destino)["controles"])
