"""Qualificação histórica dos serviços especializados com recortes por CNES e competência."""
from itertools import combinations
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from observatorio_sus.estudos.camila import sigtap
from observatorio_sus.io.custodia import sha256_arquivo


# A decisão se refere à interpretação do cadastro na edição corretiva do TCC.
DECISOES = {
    "122/003": ("Contextual", "Capacidade diagnóstica cadastrada para eletrocardiografia. O mesmo estabelecimento pode oferecer outros serviços."),
    "122/007": ("Contextual", "Cadastro de eletrocardiografia por telemedicina. A modalidade possui série própria."),
    "126/004": ("Contextual composto", "A classificação combina fisioterapia cardiovascular e pneumo-funcional. A parcela exclusivamente cardiovascular permanece indeterminada."),
    "140/014": ("Específico de urgência", "O título delimita pronto-socorro cardiovascular. A medida conta estabelecimentos com essa classificação de urgência."),
    "162/005": ("Provisório", "A classificação cadastral identifica UCO. A continuidade de seu significado assistencial carece de homologação para uso longitudinal definitivo."),
}
S116 = "116"
CBO = "225120, 225210 e 225203"


def dominio_oficial(arquivos, historico):
    """Conferir os títulos e a presença nas edições mensais preservadas, sem nova aquisição."""
    resultados = []
    for mes, arquivo in sorted(arquivos.items()):
        with ZipFile(arquivo) as z:
            nomes = dict(sigtap.registros(z, "tb_servico", ["CO_SERVICO", "NO_SERVICO"], mes))
            classes = sigtap.registros(z, "tb_servico_classificacao",
                                      ["CO_SERVICO", "CO_CLASSIFICACAO", "NO_CLASSIFICACAO"], mes)
            achados = {s+"/"+c: (nomes[s], titulo) for s,c,titulo in classes if s+"/"+c in DECISOES}
        for codigo, (decisao, motivo) in DECISOES.items():
            nomes_classe = achados.get(codigo, ("",""))
            resultados.append((mes, codigo, codigo in achados, *nomes_classe, decisao, motivo, arquivo.name))
    d = pd.DataFrame(resultados, columns=["competencia","classe_sr","vigente","titulo_servico","titulo_classe","decisao","justificativa","edicao_oficial"])
    anterior = pd.read_csv(historico, dtype=str)
    anterior["classe_sr"] = anterior.servico+"/"+anterior.classificacao
    k = ["competencia","classe_sr"]
    ref = anterior[anterior.classe_sr.isin(DECISOES)].set_index(k)[["descricao_servico","descricao_classe"]].sort_index()
    ver = d[d.vigente].set_index(k)[["titulo_servico","titulo_classe"]].sort_index()
    if not ver.index.equals(ref.index) or not (ver.to_numpy()==ref.to_numpy()).all():
        raise ValueError("O catálogo histórico diverge dos títulos ou vigências oficiais")
    return d


def historico_sr(etapa, pdr, dominio):
    """Contar CNES uma vez em cada classe e mês e medir a interseção de cada par."""
    cols = ["mes","cnes","municipio","SERV_ESP","CLASS_SR","descricao_servico","descricao_classe"]
    sr = pd.read_csv(etapa/"servicos_historicos_cnes.csv.gz", usecols=cols, dtype=str, keep_default_na=False)
    sr["classe_sr"] = sr.SERV_ESP+"/"+sr.CLASS_SR
    base116 = sr.SERV_ESP.eq(S116) & sr.descricao_servico.str.contains("cardio", case=False)
    alvo = sr[sr.classe_sr.isin(DECISOES) | base116].copy()
    alvo.loc[base116.loc[alvo.index],"classe_sr"] = S116
    sem_regra = alvo.classe_sr.ne(S116) & ~pd.MultiIndex.from_frame(alvo[["mes","classe_sr"]]).isin(
        pd.MultiIndex.from_frame(dominio.loc[dominio.vigente,["competencia","classe_sr"]]))
    if sem_regra.any() or alvo.cnes.eq("").any():
        raise ValueError("Código de serviço sem domínio vigente ou CNES ausente")
    geo = pd.read_csv(pdr, dtype=str).set_index("cod_municipio_cnes").regiao_nome
    alvo["regiao"] = alvo.municipio.map(geo)
    if alvo.regiao.isna().any() or alvo.groupby(["mes","cnes"]).municipio.nunique().max()!=1:
        raise ValueError("Territorialização não unívoca de CNES e competência")
    presenca = alvo[["mes","cnes","municipio","regiao","classe_sr"]].drop_duplicates()
    meses = sorted(dominio.competencia.unique())
    dom = dominio.set_index(["competencia","classe_sr"]).vigente
    if len(meses)!=132 or len(geo)!=78:
        raise ValueError("Cobertura temporal ou territorial insuficiente")
    regioes = sorted(geo.unique())
    niveis = [("Estado",["ES"]), ("Região",regioes), ("Município",sorted(geo.index))]
    mensal, pares = [], []
    c116 = []
    for mes, movimentos in presenca.groupby("mes"):
        for nivel, chaves in niveis:
            loc = {"Estado":pd.Series("ES",index=movimentos.index),"Região":movimentos.regiao,"Município":movimentos.municipio}[nivel]
            sets = movimentos.assign(chave=loc).groupby(["chave","classe_sr"]).cnes.agg(set).to_dict()
            for chave in chaves:
                def grupo(c):
                    return sets.get((chave,c),set())
                for classe in DECISOES:
                    q = len(grupo(classe)) if dom[mes,classe] else None
                    mensal.append((mes,nivel,chave,classe,DECISOES[classe][0],q))
                if nivel!="Município":
                    c116.append((mes,chave,len(grupo(S116))))
                    for c1,c2 in combinations([S116,*DECISOES],2):
                        vigente = (c1==S116 or dom[mes,c1]) and dom[mes,c2]
                        n = len(grupo(c1) & grupo(c2)) if vigente else None
                        pares.append((mes,nivel,chave,c1,c2,n))
    cont = pd.DataFrame(mensal,columns=["competencia","nivel","territorio","classe_sr","decisao","cnes_distintos"])
    inter = pd.DataFrame(pares,columns=["competencia","nivel","territorio","classe_1","classe_2","cnes_em_ambas"])
    grade = pd.DataFrame(c116,columns=["mes","territorio","n"]).set_index(["mes","territorio"]).n.sort_index()
    old = pd.read_csv(etapa/"estoques_regionais.csv.gz",dtype={"mes":str})
    ref = old[old.id.eq("SR_CARD")].set_index(["mes","territorio"]).valor.sort_index()
    if not grade.index.equals(ref.index) or not grade.eq(ref).all() or len(grade)!=132*5:
        raise ValueError("Divergência no indicador original SR 116")
    k = ["competencia","classe_sr"]
    es = cont[cont.nivel.eq("Estado")].set_index(k).cnes_distintos.sort_index()
    for nivel in ("Região","Município"):
        n = cont[cont.nivel.eq(nivel)].groupby(k).cnes_distintos.sum(min_count=1).sort_index()
        pd.testing.assert_series_equal(n, es, check_dtype=False)
    return cont, inter, presenca


def dicionario(origem, historico, edicoes, dominio, regra_sha):
    """Manter o ID analítico e vincular cada denominação histórica à sua edição oficial."""
    base = pd.read_csv(origem,dtype=str,keep_default_na=False)
    rec = base[base.familia.ne("PA")].copy()
    rec["competencia"] = ""
    rec["edicao"] = "definicao_cnes_v3.2"
    rec["sha256_edicao"] = regra_sha
    rec["chave_historica"] = rec.id+"@"+rec.edicao
    rec["versao_atributos"] = ""
    rec["escopo_vigencia"] = "Definição de medida. Consultar o domínio do mês e o estado da competência nas bases CNES."
    pa = pd.read_csv(historico, dtype=str, keep_default_na=False)
    pa = pa[pa.presente.eq("1")][["competencia","codigo","descricao","versao_atributos"]].rename(columns={"descricao":"titulo"})
    anterior = base[base.familia.eq("PA")].copy()
    pa["id"] = "PA_"+pa.codigo
    if set(zip(anterior.id,anterior.titulo)) != set(zip(pa.id,pa.titulo)):
        raise ValueError("Descrição histórica perdida ou sem entrada no dicionário v3.2")
    pa = pa.merge(anterior,on=["id","titulo"],validate="many_to_one").drop(columns="codigo")
    pa.loc[pa.id.eq("PA_0301010072"),"filtro"] = f"Consulta contextual por CBO {CBO}, com relação SIGTAP válida no mês da produção. Motivo clínico individual desconhecido."
    pa["escopo_vigencia"] = "Edição do SIGTAP vigente na competência de produção."
    sr = dominio[dominio.vigente].copy()
    sr["id"] = "SR_"+sr.classe_sr.str.replace("/","_",regex=False)
    sr["familia"] = "SR"
    sr["titulo"] = sr.titulo_servico+" · "+sr.titulo_classe
    sr["unidade"] = "estabelecimentos"
    sr["codigos"] = sr.classe_sr
    sr["filtro"] = "Par serviço/classificação vigente e registrado na competência do CNES/SR."
    sr["formula"] = "Contagem distinta de CNES na classe, no território e no mês."
    sr["status"] = sr.decisao
    sr["limitacao"] = sr.justificativa
    sr["fonte"] = "CNES/SR e SIGTAP"
    sr["temporalidade"] = "Competência cadastral"
    sr["territorio"] = "Estabelecimento; PDR/ES 2024"
    sr["teste"] = "Domínio oficial, unicidade, interseções e margens territoriais."
    sr["script"] = "corrigir_servicos_camila.py"
    sr["escopo_vigencia"] = "Presença do par no domínio oficial da competência."
    sr["versao_atributos"] = ""
    mensais = pd.concat([pa,sr],ignore_index=True)
    mensais["edicao"] = mensais.competencia.map({m:f.name for m,f in edicoes.items()})
    mensais["sha256_edicao"] = mensais.competencia.map({m:sha256_arquivo(f) for m,f in edicoes.items()})
    mensais["chave_historica"] = mensais.id+"@"+mensais.competencia+"@"+mensais.sha256_edicao
    out = pd.concat([rec,mensais[rec.columns]],ignore_index=True).sort_values(["id","competencia"])
    if out.chave_historica.duplicated().any() or out.chave_historica.isna().any() or not set(base.id)<=set(out.id):
        raise ValueError("Chave histórica inválida")
    return out
