"""Montar a entrega acadêmica a partir de agregados selados, sem ler DBC ou declarações."""
import argparse
import json
import platform
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree

import matplotlib
import numpy as np
import pandas as pd

import figuras_academicas_camila as figuras
from observatorio_sus.estudos.camila.lote import executar, produtos
from observatorio_sus.io.custodia import sha256_arquivo

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs/estudos/tcc_camila"
PDR = REPO / "metadata/territorio/pdr_es_2024_tcc_v1.csv"
PA = "SIA/PA e SIGTAP mensal"
CNES = "CNES e domínios históricos"
SIM = "SIM e denominadores anuais RIPSA"
SIH = "SIH/RD nacional e denominadores anuais RIPSA"
JANELA = "Produção em PA_CMP observada nos movimentos até dez/2024. Os meses finais podem receber lançamentos posteriores."
ESTOQUE = "Média mensal dos estoques cadastrados. Consulte o número de competências válidas."
ESPECIFICOS = ["exames_especificos", "fisioterapia_especifica"]
REG = figuras.REGIOES
NOME = "ENTREGA_TCC_CAMILA_2014_2024"
SCRIPTS = ["entrega_academica_camila.py","figuras_academicas_camila.py","qualificar_particoes_camila.py",
           "historico_clinico_camila.py","integrar_oferta_camila.py","fechar_assistencia_camila.py",
           "repor_leitos_camila.py","adquirir_servicos_camila.py","assistencia_ftp_camila.py","conferir_recortes_leitos_camila.py"]


class Entrega:
    """Registrar unidade, origem e tabelas de reprodução junto com os produtos."""
    def __init__(self, stage):
        self.stage = stage
        self.itens = []

    def registrar(self, tipo, pasta, id_, titulo, unidade, fonte, nota, origem, periodo, territorio, formula):
        p = self.stage / pasta / id_
        p.parent.mkdir(parents=True, exist_ok=True)
        caminho = p.relative_to(self.stage).as_posix()
        self.itens.append(dict(id=id_, tipo=tipo, titulo=titulo, periodo=periodo, territorio=territorio,
                               unidade=unidade, fonte=fonte, numerador_denominador=formula, notas=nota,
                               status="Validado no escopo e na janela indicados", base=origem,
                               tabela=caminho+".csv", figura=caminho+".svg" if tipo!="Tabela" else "",
                               script="scripts/entrega_academica_camila.py"))
        return p

    def tabela(self, pasta, id_, df, titulo, unidade, fonte, nota, origem, formula, territorio="ES e territórios indicados", periodo="2014–2024", compacta=False):
        p = self.registrar("Tabela", pasta, id_, titulo, unidade, fonte, nota, origem, periodo, territorio, formula)
        if compacta:
            self.itens[-1]["tabela"] += ".gz"
            df.to_csv(p.with_suffix(".csv.gz"), index=False, compression={"method":"gzip","mtime":0})
        else:
            df.to_csv(p.with_suffix(".csv"), index=False)
        return df

    def figura(self, pasta, id_, df, titulo, unidade, fonte, nota, origem, formula, territorio, periodo="2014–2024", modo="linhas", **kwargs):
        if df.empty:
            raise ValueError("Figura sem observações: "+id_)
        p = self.registrar("Mapa" if modo=="mapa" else "Gráfico",pasta,id_,titulo,unidade,fonte,nota,origem,periodo,territorio,formula)
        df.to_csv(p.with_suffix(".csv"),index=False)
        getattr(figuras,modo)(df,arquivo=p,titulo=titulo,unidade=unidade,fonte=fonte,nota=nota,**kwargs)


def conferir(diretorio):
    recibo = diretorio/"recibo.json"
    r = json.loads(recibo.read_text(encoding="utf8"))
    if r["saidas"] != produtos(diretorio):
        raise ValueError(f"Saídas divergentes do recibo em {diretorio.name}")
    return recibo


def longo(df, colunas, nomes=None, eixo="ano"):
    d = df.melt(id_vars=[eixo],value_vars=colunas,var_name="serie",value_name="valor").rename(columns={eixo:"x"})
    return d.replace({"serie":nomes or {}})


def pontos(df, serie, valor, eixo="ano", nomes=None):
    d = df[[eixo,serie,valor]].rename(columns={eixo:"x",serie:"serie",valor:"valor"})
    return d.replace({"serie":nomes or {}})


def comparar(valores, esperados, mensagem):
    if not np.allclose(valores,esperados,rtol=0,atol=1e-8,equal_nan=True):
        raise ValueError(mensagem)


def gerar(d, v, h, o, manuscrito, guia):
    e = Entrega(d)
    figuras.iniciar()
    cp, etapa = o/"checkpoint-etapa1", o/"etapa1"
    taxas = v/"taxas-ed2"
    geo = pd.read_csv(PDR,dtype=str).rename(columns={"cod_municipio_cnes":"municipio","cod_municipio_ibge":"chave","regiao_nome":"regiao"})
    if len(geo)!=78 or geo.chave.nunique()!=78 or set(geo.regiao)!=set(REG):
        raise ValueError("Regionalização")
    mor = pd.read_csv(taxas/"indicadores.csv", dtype={"sexo_sim":str})
    esp = pd.read_csv(taxas/"especificas.csv",dtype={"sexo_sim":str})
    i50 = pd.read_csv(v/"sintese-verificada/sensibilidade_i50.csv")
    hosp = pd.read_csv(h/"indicadores_anuais.csv")
    hosidade = pd.read_csv(h/"sexo_idade_anual.csv")
    fluxo = pd.read_csv(h/"fluxos_mensais.csv",dtype={"uf_res_ibge":str})
    reg_h = pd.read_csv(h/"indicadores_regionais.csv")
    mun_h = pd.read_csv(h/"indicadores_municipais.csv",dtype={"municipio_res":str})
    estado_h = pd.read_csv(h/"utilizacao_e_evasao_es.csv")
    den = pd.read_csv(taxas/"RIPSA_DEM101_QA_TOTAIS.csv",dtype={"datasus6":str}).rename(columns={"datasus6":"municipio","total":"habitantes"})
    cad = pd.read_csv(etapa/"dicionario_recursos.csv")
    ids = set(cad.loc[cad.status=="Validado","id"])
    est = pd.read_csv(etapa/"estoques_anuais.csv").query("id in @ids")
    meses_est = pd.read_csv(etapa/"estoques_regionais.csv.gz").query("id in @ids")
    clin = pd.read_csv(etapa/"catalogo_clinico.csv",dtype=str)
    cod = set(clin.loc[clin.classe.isin(["A","B"]),"codigo"])
    pa = pd.read_csv(etapa/"pa_anuais.csv",dtype={"codigo":str}).query("codigo in @cod")
    pm = pd.read_csv(etapa/"pa_series_mensais.csv.gz",dtype={"codigo":str}).query("codigo in @cod")
    sub = pd.read_csv(etapa/"pa_subtotais.csv")
    for path in ["00_LEIA_PRIMEIRO","05_MANUAL_DA_ESTUDANTE","06_ROTEIRO_DO_ORIENTADOR","07_DOCUMENTACAO_METODOLOGICA","08_REPRODUTIBILIDADE"]:
        (d/path).mkdir()
    base = "01_BASES_E_INDICADORES/"
    tab = "02_TABELAS/"
    graf = "03_GRAFICOS/"
    simnota = "Ano do óbito e residência. A causa básica final define o grupo. O total ES conserva os residentes sem município conhecido."
    simform = "Óbitos / população anual × 100 mil. Taxa direta = soma das taxas etárias ponderadas pelos pesos censitários."
    aihnota = "AIHs principais cardiovasculares de residentes, em qualquer UF. Ano de processamento."
    aihform = "AIHs / população anual × 100 mil. Evasão = AIHs fora do ES / AIHs dos residentes × 100."
    paform = "Somas separadas das quantidades aprovadas e apresentadas nos códigos e instrumentos elegíveis."
    estform = "Soma dos estoques mensais válidos / número de competências. Densidade = média / habitantes × 100 mil."
    def tabela(pasta,id_,df,titulo,unidade,fonte,nota,ref,formula):
        return e.tabela(pasta,id_,df,titulo,unidade,fonte,nota,ref,formula)
    tabela(base+"mortalidade","B01",mor,"Mortalidade geral e prematura por grupo, sexo e padrão","óbitos e taxas por 100 mil",SIM,simnota,"taxas-ed2/indicadores.csv",simform)
    tabela(base+"mortalidade","B02",esp,"Mortalidade específica por idade e sexo","óbitos e taxa por 100 mil do estrato",SIM,"Faixa final 80+. Idade ignorada aparece em separado.","taxas-ed2/especificas.csv",simform)
    tabela(base+"complementares","B03",i50,"I50 como causa final, causa original e menção","óbitos", "SIM","Uma declaração pode preencher mais de um critério. A união conta cada declaração uma vez. Campos em branco indicam recorte indisponível.","sintese-verificada/sensibilidade_i50.csv","Contagem independente segundo o campo e o critério.")
    tabela(base+"internacoes","B04",hosp,"Utilização hospitalar por sexo e padrão","AIHs e taxas por 100 mil",SIH,aihnota,"entrega-final/indicadores_anuais.csv",aihform)
    tabela(base+"internacoes","B05",hosidade,"AIHs por sexo e idade","AIHs e taxas por 100 mil do estrato",SIH,aihnota,"entrega-final/sexo_idade_anual.csv",aihform)
    tabela(tab+"fluxos","T01",reg_h,"Origem, destino e participação nos fluxos regionais","AIHs e percentuais",SIH,aihnota,"entrega-final/indicadores_regionais.csv","Denominadores por residência e por atendimento nas respectivas colunas.")
    tabela(tab+"fluxos","T02",estado_h,"Utilização hospitalar, evasão e atração anuais","AIHs e percentuais",SIH,aihnota,"entrega-final/utilizacao_e_evasao_es.csv","Evasão usa AIHs de residentes. Atração usa AIHs atendidas no ES.")
    tabela(tab+"utilizacao_hospitalar","T03",mun_h,"Utilização e evasão por município de residência","AIHs e taxas",SIH,aihnota,"entrega-final/indicadores_municipais.csv",aihform)
    adm=pd.read_csv(h/"admissao_por_ano_processamento.csv")
    tabela(tab+"utilizacao_hospitalar","T04",adm,"Ano de admissão por ano de processamento","AIHs",SIH,aihnota,"entrega-final/admissao_por_ano_processamento.csv","Contagem por par de anos, inclusive admissões anteriores à janela.")
    tabela(base+"cnes","B06",meses_est,"Estoques por competência cadastral e território","unidade declarada no dicionário",CNES,"Consultar o código da medida no dicionário e o estado de vigência.","etapa1/estoques_regionais.csv.gz","Valor mensal da medida definida por id.")
    tabela(tab+"oferta","T05",est,"Capacidade cadastrada por ano e território","média mensal e densidade por 100 mil",CNES,ESTOQUE,"etapa1/estoques_anuais.csv",estform)
    tabela(base+"sia_sigtap","B07",pm,"Produção por código e competência com situação histórica","procedimentos e estabelecimentos",PA,JANELA,"etapa1/pa_series_mensais.csv.gz",paform)
    tabela(tab+"producao","T06",pa,"Produção aprovada e apresentada por código oficial","procedimentos",PA,JANELA,"etapa1/pa_anuais.csv",paform)
    tabela(tab+"producao","T07",sub,"Subtotais específicos e contextuais por competência","procedimentos",PA,JANELA,"etapa1/pa_subtotais.csv",paform)
    pop = den[["ano","municipio","habitantes"]].merge(geo[["municipio","chave","regiao"]],validate="many_to_one")
    if len(pop)!=78*11 or pop.duplicated(["ano","municipio"]).any():
        raise ValueError("Grade populacional")
    partes=[]
    for ano in range(2014,2025):
        estr=pd.read_csv(v/f"estratos/{ano}/cardiovascular.csv",dtype={"municipio":str,"final":str})
        if not estr.final.str.fullmatch(r"I[0-9]{2}.*").all():
            raise ValueError("CID fora de G0 nos agregados cardiovasculares")
        cont=estr.groupby("municipio",dropna=False).obitos.sum().rename("obitos").reset_index()
        cont["ano"]=ano
        partes.append(cont)
    eventos=pd.concat(partes,ignore_index=True)
    pad=mor.query("territorio=='ES' and grupo=='G0' and sexo_sim=='T' and universo=='todas' and censo==2022").sort_values("ano")
    comparar(eventos.groupby("ano").obitos.sum().values,pad.obitos,"Resíduo no SIM estadual")
    mun=pop.merge(eventos,on=["ano","municipio"],how="left",validate="one_to_one")
    mun.obitos=mun.obitos.fillna(0).astype(int)
    mun["bruta_100mil"]=100000*mun.obitos/mun.habitantes
    sobra=eventos[~eventos.municipio.isin(geo.municipio)].groupby("ano").obitos.sum()
    reconc=mun.groupby("ano").agg(obitos_mapeados=("obitos","sum"),habitantes=("habitantes","sum"))
    reconc["obitos_sem_municipio"]=sobra.reindex(reconc.index,fill_value=0)
    reconc["obitos_es"]=pad.set_index("ano").obitos
    comparar(reconc.obitos_mapeados+reconc.obitos_sem_municipio,reconc.obitos_es,"Resíduo de residência")
    comparar(reconc.habitantes,pad.habitantes,"População municipal")
    tabela(tab+"mortalidade","T08",mun,"Mortalidade circulatória municipal por residência","óbitos e taxa bruta por 100 mil",SIM,simnota,"estratos anuais e RIPSA_DEM101_QA_TOTAIS.csv",simform)
    tabela(tab+"mortalidade","T09",reconc.reset_index(),"Reconciliação dos óbitos estaduais e municipais","óbitos e habitantes",SIM,simnota,"T08 e B01","Óbitos mapeados mais óbitos sem município = total estadual.")
    totais=estado_h[["aih_residentes","evasao_aih","atendimento_es","atracao_aih","interregional_intra_es"]].sum()
    controle_sih=json.loads((h/"controles.json").read_text())
    esperado=[controle_sih[k] for k in ["residentes","evasao","atendimento","atracao"]]
    esperado.append(reg_h.em_outra_regiao_es.sum())
    comparar(totais,esperado,"Checkpoint nacional do SIH")
    nacional=pd.read_csv(h/"matriz_132_competencias.csv")
    if len(nacional)!=132 or nacional.competencia.nunique()!=132 or not nacional.ufs_validadas.eq(27).all():
        raise ValueError("Competência nacional incompleta")
    tabela(base+"internacoes","B08",nacional,"Matriz nacional de cobertura do SIH","arquivos e competências",SIH,"27 UFs de atendimento por competência.","entrega-final/matriz_132_competencias.csv","Uma linha por competência com os controles de cobertura.")
    simsel=mor.query("grupo=='G0' and censo==2022 and sexo_sim=='T' and universo=='todas'")
    sint=simsel[["ano","territorio","obitos","habitantes","bruta_100mil","direta_100mil"]].merge(
        hosp.query("sexo=='T'")[["ano","territorio","aih_residentes","evasao_pct","utilizacao_bruta_100mil","padronizada_censo2022_100mil"]],on=["ano","territorio"],validate="one_to_one")
    sint=sint.merge(est.query("id=='SR_CARD'")[["ano","territorio","media_mensal"]].rename(columns={"media_mensal":"estabelecimentos_sr116_media"}),how="left",on=["ano","territorio"],validate="one_to_one")
    sub=sub.assign(ano=sub.competencia//100)
    prod=sub.query("grupo_clinico=='soma_especificos_elegiveis'").groupby(["ano","territorio"]).agg(meses=("aprovadas","count"),aprovadas=("aprovadas","sum")).reset_index()
    prod.loc[prod.meses!=12,"aprovadas"]=np.nan
    sint=sint.merge(prod,on=["ano","territorio"],how="left",validate="one_to_one")
    tabela(tab+"producao","T10",sint,"Leitura conjunta por ano e território","unidades próprias nas colunas","SIM, SIH, CNES, SIA e SIGTAP","Óbitos por ocorrência, AIHs por processamento, oferta por cadastro e PA por competência de produção. ES sem Norte disponível no SIM e SIH.","B01, B04, T05 e T07","Medidas justapostas. Ausência de valor indica comparador indisponível.")
    grupos_h=pd.read_csv(h/"grupos.csv")
    tabela(base+"internacoes","B09",grupos_h,"AIHs por grupo cardiovascular e UF de atendimento","AIHs",SIH,aihnota,"entrega-final/grupos.csv","Contagem por grupo e competência. G0 inclui os grupos específicos.")
    tabela(tab+"fluxos","T11",pd.read_csv(h/"matriz_regional_anual.csv"),"Matriz anual de residência e atendimento","AIHs",SIH,aihnota,"entrega-final/matriz_regional_anual.csv","AIHs principais por origem e destino.")
    for id_,nivel in [("T13","municipios"),("T14","regioes")]:
        leitos=pd.read_csv(o/f"recortes-lt-202412/{nivel}.csv",dtype={"municipio":str,"TP_LEITO":str,"CODLEITO":str})
        e.tabela(tab+"oferta",id_,leitos,"Leitos cadastrados por tipo e código em dezembro de 2024","leitos",
                 CNES,"Todos os tipos registrados. Leia as categorias gerais como contexto. A custódia mantém o detalhe por CNES.",
                 "recortes-lt-202412/"+nivel+".csv","Soma por território, tipo, código e campo de quantidade.",
                 territorio="Municípios com registro" if nivel=="municipios" else "Quatro Regiões de Saúde",periodo="Dezembro de 2024")
    estoques_mun=pd.read_csv(etapa/"estoques_municipais.csv.gz",dtype={"municipio":str}).query("id in @ids")
    e.tabela(tab+"oferta","T15",estoques_mun,"Recursos cadastrados por município, competência e medida",
             "unidade cadastrada segundo o dicionário",CNES,"Conserve as lacunas de vigência e os zeros explícitos.",
             "etapa1/estoques_municipais.csv.gz","Valor de cada medida por mês e município.",territorio="78 municípios",compacta=True)
    mapa_e_graficos(e,o,geo,mun,mor,esp,i50,hosp,hosidade,reg_h,estado_h,fluxo,est,pa,pm,sub,clin,etapa,simform,aihform,estform,paform)
    documentar(e,o,manuscrito,guia)
    return dict(anos=11,municipios=78,regioes=4,competencias_sih=len(nacional),aih_residentes=int(totais.iloc[0]),
                evasao=int(totais.iloc[1]),atracao=int(totais.iloc[3]),itens=len(e.itens),
                tabelas=sum(r["tipo"]=="Tabela" for r in e.itens),graficos=sum(r["tipo"]=="Gráfico" for r in e.itens),
                mapas=sum(r["tipo"]=="Mapa" for r in e.itens),microdados_incluidos=False)


def mapa_e_graficos(e,o,geo,mun,mor,esp,i50,hosp,hosidade,reg_h,estado_h,fluxo,est,pa,pm,sub,clin,etapa,simform,aihform,estform,paform):
    def graf(id_,pasta,df,titulo,unidade,fonte,nota,base,formula,territorio="Espírito Santo",periodo="2014–2024",**kwargs):
        e.figura("03_GRAFICOS/"+pasta,id_,df,titulo,unidade,fonte,nota,base,formula,territorio,periodo,**kwargs)
    anual="series_temporais"
    sex="sexo_idade"
    reg="comparacoes_regionais"
    of="oferta_producao"
    cens=mor.query("grupo=='G0' and sexo_sim=='T' and universo=='todas' and territorio=='ES'")
    mort=cens.query("censo==2022")
    d=longo(mort,["bruta_100mil","direta_100mil"],{"bruta_100mil":"Bruta","direta_100mil":"Padrão Brasil 2022"})
    c=cens.query("censo==2010")[["ano","direta_100mil"]].rename(columns={"ano":"x","direta_100mil":"valor"}).assign(serie="Padrão Brasil 2010")
    graf("F01",anual,pd.concat([d,c]),"Mortalidade circulatória no Espírito Santo","Óbitos por 100 mil habitantes",SIM,"Todas as idades. Padronização direta com faixa final 80+.","B01",simform)
    sel=mor.query("grupo=='G0' and sexo_sim=='T' and universo=='30-69' and censo==2022 and territorio in @REG")
    graf("F02",reg,pontos(sel,"territorio","direta_100mil"),"Mortalidade prematura nas quatro Regiões de Saúde","Óbitos por 100 mil habitantes de 30–69 anos",SIM,"Padrão Brasil 2022, pesos renormalizados entre 30 e 69 anos.","B01",simform,"Regiões de residência")
    sexos={"1":"Masculino","2":"Feminino","M":"Masculino","F":"Feminino"}
    for id_,univ,rot in [("F03","todas","todas as idades"),("F04","30-69","30–69 anos")]:
        sel=mor.query("grupo=='G0' and territorio=='ES' and sexo_sim in ['1','2'] and universo==@univ and censo==2022")
        graf(id_,sex,pontos(sel,"sexo_sim","direta_100mil",nomes=sexos),"Mortalidade circulatória por sexo, "+rot,"Óbitos por 100 mil habitantes do estrato",SIM,"Padrão Brasil 2022.","B01",simform)
    sel=esp.query("ano==2024 and territorio=='ES' and grupo=='G0' and sexo_sim in ['1','2'] and idade_inicio>=0")
    graf("F05",sex,pontos(sel,"sexo_sim","taxa_100mil","idade_inicio",sexos),"Mortalidade por idade e sexo no Espírito Santo","Óbitos por 100 mil habitantes do estrato",SIM,"Taxas específicas. Última faixa aberta.","B02",simform,periodo="2024",eixo="Idade em anos",idades=True)
    graf("F06",anual,longo(i50.query("territorio=='ES'"),["i50_final","i50_original","mencao_uniao"],{"i50_final":"Causa básica final","i50_original":"Causa básica original","mencao_uniao":"Menção na declaração"}),"Insuficiência cardíaca nos campos da declaração de óbito","Óbitos de residentes do ES","SIM","Os três critérios podem identificar o mesmo óbito. A menção é a união dos campos de menções.","B03","Contagem segundo cada critério de I50.")
    sel=hosp.query("sexo=='T' and territorio in ['Norte','ES sem Norte']")
    graf("F07",reg,pontos(sel,"territorio","padronizada_censo2022_100mil"),"Utilização hospitalar na Região Norte e no restante do ES","AIHs por 100 mil habitantes",SIH,"Residência, todas as idades, Brasil/Censo 2022. Ano de processamento.","B04",aihform,"Norte e ES sem Norte")
    sel=hosidade.query("ano==2024 and territorio=='ES' and sexo in ['M','F'] and idade_inicio>=0")
    graf("F08",sex,pontos(sel,"sexo","utilizacao_100mil","idade_inicio",sexos),"AIHs cardiovasculares por sexo e idade","AIHs por 100 mil habitantes do estrato",SIH,"Ano de processamento 2024. Faixa terminal aberta.","B05",aihform,periodo="2024",eixo="Idade em anos",idades=True)
    graf("F09",anual,longo(estado_h,["aih_residentes","atendimento_es"],{"aih_residentes":"Por residência no ES","atendimento_es":"Por atendimento no ES"}),"AIHs cardiovasculares por residência e atendimento","AIHs principais",SIH,"Cada universo inclui as AIHs comuns aos dois critérios.","T02","Contagens separadas segundo a residência e o atendimento.")
    graf("F10","derivados",longo(estado_h,["evasao_pct","atracao_pct"],{"evasao_pct":"Evasão","atracao_pct":"Atração"}),"Evasão e atração hospitalar interestadual","Percentual de AIHs",SIH,"Evasão usa as AIHs dos residentes. Atração usa as AIHs atendidas no estado.","T02",aihform)
    estoque_grafs=[
        ("F11","SR_CARD","Serviço cardiovascular classificado","Estabelecimentos"),
        ("F12","HB_0801","Habilitação cardiovascular 0801","Estabelecimentos com habilitação vigente"),
        ("F13","LT_32_QT_SUS","Leitos clínicos de cardiologia destinados ao SUS","Leitos SUS cadastrados"),
        ("F14","EQ_441_QT_USO","Eletrocardiógrafos cadastrados em uso","Equipamentos em uso"),
        ("F15","PF_225120_vinculos","Registros de vínculo de cardiologistas","Registros de vínculo"),
        ("F16","PF_225120_horas_amb","Carga horária ambulatorial de cardiologistas","Horas ambulatoriais cadastradas"),
        ("F17","EP_ATIVAS","Equipes ativas ao fim de cada competência","Equipes de todas as especialidades")]
    for id_,recurso,nome,un in estoque_grafs:
        sel=est.query("id==@recurso and territorio in @REG")
        graf(id_,of,pontos(sel,"territorio","media_mensal"),nome+" por região",un+" · média mensal",CNES,ESTOQUE,"T05",estform,"Regiões do estabelecimento")
    for id_,grupo,titulo in [("F18","exames_especificos","Exames cardiovasculares específicos"),("F19","fisioterapia_especifica","Fisioterapia cardiovascular específica"),
                              ("F20","doppler_contextual","Doppler vascular • indicador contextual"),("F21","consulta_cbo","Consulta por ocupação • indicador contextual")]:
        s=sub.query("grupo_clinico==@grupo and territorio in @REG").groupby(["ano","territorio"]).aprovadas.sum(min_count=12).reset_index()
        graf(id_,of,pontos(s,"territorio","aprovadas"),titulo+" por região","Quantidade aprovada de procedimentos",PA,JANELA,"T07",paform,"Regiões do prestador")
    nomes={"0208010025":"Estresse","0208010033":"Repouso"}
    s=pa[pa.codigo.isin(nomes)&pa.territorio.eq("ES")]
    graf("F22",of,pontos(s,"codigo","aprovadas_12_meses",nomes=nomes),"Cintilografia de perfusão miocárdica no ES","Quantidade aprovada de procedimentos",PA,JANELA,"T06",paform)
    part=pd.read_csv(etapa/"participacao_producao.csv.gz",dtype={"cnes":str,"codigo":str})
    a=set(clin.loc[clin.classe=="A","codigo"])
    prest=part[part.codigo.isin(a)&part.n.gt(0)&part.ano.between(2014,2024)].copy()
    pr=prest.groupby(["ano","regiao_at"]).cnes.nunique().rename("estabelecimentos").reindex(
        pd.MultiIndex.from_product([range(2014,2025),REG],names=["ano","regiao_at"]),fill_value=0).reset_index()
    graf("F23",of,pontos(pr,"regiao_at","estabelecimentos"),"Estabelecimentos com produção cardiovascular específica","CNES distintos com quantidade aprovada positiva",PA,JANELA,"etapa1/participacao_producao.csv.gz","Contagem distinta de CNES por região e ano de produção.","Regiões do prestador")
    grupos=mor.query("territorio=='ES' and censo==2022 and universo=='todas' and sexo_sim=='T' and grupo!='G0'")
    graf("F24",anual,pontos(grupos,"grupo","direta_100mil",nomes={"G1":"I20–I25","G2":"I50","G3":"I60–I69","G4":"I10–I15","G5":"I70–I79"}),"Mortalidade por grupos cardiovasculares selecionados","Óbitos por 100 mil habitantes",SIM,"Padrão Brasil 2022. Os cinco grupos cobrem parte do capítulo IX.","B01",simform)
    maps="04_MAPAS_E_FLUXOS"
    es=o/"fontes/municipios-es.geojson"
    def mapa(id_,df,titulo,unidade,fonte,nota,origem,formula,periodo="2014–2024",malha=es,ter="Municípios do ES"):
        e.figura(maps,id_,df,titulo,unidade,fonte,nota,origem,formula,ter,periodo,modo="mapa",malha=malha)
    acumulado=mun.groupby(["chave","regiao"]).agg(obitos=("obitos","sum"),pessoas_ano=("habitantes","sum")).reset_index()
    acumulado["valor"]=100000*acumulado.obitos/acumulado.pessoas_ano
    if (acumulado.obitos<=0).any():
        raise ValueError("Conferir células municipais do período")
    mapa("M01",acumulado.assign(painel="Município de residência"),"Mortalidade circulatória municipal, 2014–2024","Óbitos por 100 mil pessoas-ano",SIM,"Série acumulada e taxa bruta. Residência sem município consta de T09.","T08 e T09","Soma dos óbitos / soma das populações anuais × 100 mil.")
    s=est.query("ano==2024 and id=='LT_32_QT_SUS' and territorio in @REG")
    m=geo[["chave","regiao"]].merge(s[["territorio","media_por_100mil"]],left_on="regiao",right_on="territorio",validate="many_to_one").rename(columns={"media_por_100mil":"valor"})
    mapa("M02",m.assign(painel="Região do estabelecimento"),"Leitos clínicos de cardiologia SUS por região, 2024","Leitos SUS por 100 mil habitantes",CNES,"Cada município recebe o valor da sua Região de Saúde. Média dos estoques mensais.","T05",estform,"2024",ter="Quatro Regiões de Saúde do ES")
    pmu=pd.read_csv(etapa/"pa_municipal.csv.gz",dtype={"municipio":str,"codigo":str})
    s=pmu.query("situacao=='elegivel' and grupo_clinico in @ESPECIFICOS and competencia>=201401 and competencia<=202412")
    por_mun=s.groupby("municipio").aprovadas.sum()
    comparar([por_mun.sum()],[sub.query("territorio=='ES' and grupo_clinico=='soma_especificos_elegiveis'").aprovadas.sum()],"Produção cartográfica estadual")
    m=geo[["chave","municipio","regiao"]].copy()
    m["valor"]=m.municipio.map(por_mun).fillna(0).astype(int)
    mapa("M03",m.assign(painel="Município do estabelecimento"),"Produção ambulatorial cardiovascular específica, 2014–2024","Quantidade aprovada acumulada",PA,JANELA,"etapa1/pa_municipal.csv.gz e T07",paform)
    munpa=s.groupby(["competencia","municipio","regiao","codigo","grupo_clinico"],as_index=False)[["aprovadas","apresentadas"]].sum()
    e.tabela("02_TABELAS/producao","T12",munpa,"Produção específica observada por município, mês e código","procedimentos",PA,JANELA,"etapa1/pa_municipal.csv.gz",paform)
    context=pmu.query("situacao=='elegivel' and grupo_clinico in ['doppler_contextual','consulta_cbo'] and competencia>=201401 and competencia<=202412")
    context=context.groupby(["competencia","municipio","regiao","codigo","grupo_clinico"],as_index=False)[["aprovadas","apresentadas"]].sum()
    e.tabela("02_TABELAS/producao","T16",context,"Produção contextual observada por município, mês e código","procedimentos",PA,
             JANELA+" Recortes independentes, externos à soma específica.","etapa1/pa_municipal.csv.gz",paform)
    inter=fluxo[fluxo.regiao_res.isin(REG)&fluxo.regiao_at.isin(REG)&fluxo.uf_atendimento.eq("ES")]
    matriz=inter.groupby(["regiao_res","regiao_at"]).aih.sum().unstack(fill_value=0).reindex(index=REG,columns=REG,fill_value=0)
    comparar([matriz.values.sum()-np.trace(matriz)],[estado_h.interregional_intra_es.sum()],"Matriz inter-regional")
    mf=matriz.rename_axis(index="origem",columns="destino").stack().rename("aih").reset_index()
    e.figura(maps,"F25",mf,"Origem e destino das AIHs dentro do Espírito Santo","AIHs principais acumuladas",SIH,
             "A diagonal indica atendimento na própria região. A cor usa escala logarítmica, e as células exibem a contagem.",
             "entrega-final/fluxos_mensais.csv","Contagem por região de residência e atendimento.","Quatro regiões","2014–2024",modo="fluxo")
    ufs=figuras.SIGLAS
    externo=fluxo[fluxo.uf_res_ibge.eq("32")&fluxo.uf_atendimento.ne("ES")]
    saida=externo.groupby("uf_atendimento").aih.sum()
    entrada=fluxo[fluxo.regiao_res.eq("OUTRA_UF_CODIGO_PLAUSIVEL")&fluxo.uf_atendimento.eq("ES")].groupby("uf_res_ibge").aih.sum()
    comparar([saida.sum(),entrada.sum()],[estado_h.evasao_aih.sum(),estado_h.atracao_aih.sum()],"Malha interestadual")
    ext=pd.DataFrame([(k,sig,painel,np.nan if k=="32" else cont.get(ref,0)) for k,sig in ufs.items()
                      for painel,cont,ref in [("Destino de residentes do ES",saida,sig),("Origem dos atendidos no ES",entrada,k)]],
                     columns=["chave","uf","painel","valor"])
    mapa("M04",ext,"Fluxos hospitalares entre o ES e as demais UFs","AIHs principais acumuladas",SIH,"Mesma escala nos dois painéis. Cinza identifica o ES. Residência externa com código de UF plausível.",
         "entrega-final/fluxos_mensais.csv","AIHs segundo UF de origem ou destino.",malha=o/"fontes/ufs-br.geojson",ter="Brasil")


def documentar(e,o,manuscrito,guia):
    d=e.stage
    doc=d/"07_DOCUMENTACAO_METODOLOGICA"
    repro=d/"08_REPRODUTIBILIDADE"
    for src in [o/"checkpoint-etapa1/catalogo_indicadores.csv",o/"checkpoint-etapa1/situacao_de_uso.csv",
                o/"checkpoint-etapa1/criterios_de_uso.md",o/"etapa1/catalogo_clinico.csv",
                o/"etapa1/intervalos_sigtap.csv.gz",o/"historico/procedimentos.csv.gz",
                DOCS/"registro_decisoes_metodologicas.md",PDR]:
        shutil.copyfile(src,doc/src.name)
    (doc/"fontes.md").write_text("""# Fontes e edições

Os recibos de aquisição em custódia identificam URL do objeto, edição, tamanho e SHA-256 de cada arquivo. A cobertura nacional do SIH está em B08. O histórico do SIGTAP conserva os atributos vigentes por competência e código. O inventário de produtos relaciona cada série ao seu agregado de origem.

- SIM, SIH/RD, CNES, SIA/PA e distribuições mensais do SIGTAP. [DATASUS — transferência de arquivos](https://datasus.saude.gov.br/transferencia-de-arquivos/)
- Domínios de leitos do cadastro. [Manual de Operação SCNES, fevereiro de 2009](https://bvsms.saude.gov.br/bvs/publicacoes/pdoc/MNL-GPSL-PDOC-SCNES-ManualOperacao-Edicao3.0.pdf)
- Instrumentos de origem na produção ambulatorial. [Informe técnico SIA/SUS de julho de 2019](ftp://ftp.datasus.gov.br/dissemin/publicos/SIASUS/200801_/Doc/Informe_Tecnico_SIASUS_2019_07.pdf)
- Regionalização retrospectiva dos 78 municípios. [CIB/SUS-ES 259/2024, Anexo III](https://e-docs.es.gov.br/d/2024-L5WDBB)
- As malhas municipais e das UFs vêm da API de malhas do IBGE. As URLs exatas e os hashes estão em ambiente_e_malhas.json. Os mapas do ES enquadram seu território continental e conservam os valores integrais de todos os municípios.
""",encoding="utf8")
    shutil.copyfile(DOCS/"manual_leitura_assistencial.md",d/"05_MANUAL_DA_ESTUDANTE/manual.md")
    with zipfile.ZipFile(manuscrito) as z:
        xml=ElementTree.fromstring(z.read("word/document.xml"))
    tag="{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragrafos={i:"".join(node.text or "" for node in p.iter(tag+"t")) for i,p in enumerate(xml.find(tag+"body").findall(tag+"p"),1)}
    plano=json.loads(guia.read_text(encoding="utf-8-sig"))
    if sha256_arquivo(manuscrito)!=plano["sha256"]:
        raise ValueError("O roteiro está vinculado a outra edição do manuscrito")
    pasta_guia=d/"06_ROTEIRO_DO_ORIENTADOR"
    cab=["# Roteiro de orientação acadêmica","",
         f"Manuscrito examinado em leitura local: **{manuscrito.name}**. SHA-256: `{plano['sha256']}`.",
         "Os localizadores § contam os parágrafos do corpo do DOCX, inclusive os vazios, em ordem desde o início. Os títulos e as referências abaixo vêm dessa edição.",
         "","## Objetivos específicos do manuscrito",""]
    for i in plano["objetivos"]:
        cab.append(f"- §{i} · {paragrafos[i].lstrip('• ').strip()}")
    cab+=["","O objetivo territorial e a seção 3.2 (§163) ainda indicam Noroeste 1. A revisão da estudante e do orientador deverá explicitar a Região Norte como aprofundamento homologado; o comparador ES sem Norte está disponível para mortalidade e utilização hospitalar.","",
          "A matriz a seguir relaciona perguntas aos produtos. As referências indicam onde começar a leitura conceitual da edição examinada. A atribuição de explicações clínicas ou causais exige evidência adicional.",""]
    matriz=[]
    for tema,obj,prods,pergunta,conceito,sec,trecho,ref,cuidado,pedido in plano["linhas"]:
        objetivo=paragrafos[obj].lstrip("• ").strip()
        referencia=paragrafos[ref].strip()
        if not all([objetivo,referencia,paragrafos[trecho].strip()]):
            raise ValueError("Âncora vazia no manuscrito")
        matriz.append(dict(tema=tema,objetivo=objetivo,paragrafo_objetivo=obj,produtos=prods,pergunta=pergunta,
                           conceito=conceito,referencia=referencia,secao=sec,paragrafo_no_texto=trecho,paragrafo_bibliografia=ref,
                           cuidado=cuidado,novo_cruzamento=pedido))
        cab += [f"## {tema}","",f"**Objetivo** (§{obj}) · {objetivo}","",f"**Produtos** · {prods}","",
                f"**Pergunta para a estudante** · {pergunta}","",f"**Conceito** · {conceito}. Seção {sec}, §{trecho}.","",
                f"**Referência do manuscrito** (§{ref}) · {referencia}","",f"**Cuidados e lacunas** · {cuidado}","",
                f"**Possível aprofundamento** · {pedido}",""]
    (pasta_guia/"roteiro.md").write_text("\n".join(cab),encoding="utf8")
    pd.DataFrame(matriz).to_csv(pasta_guia/"matriz_orientacao.csv",index=False)
    shutil.copyfile(guia,repro/"roteiro-referencial.json")
    pd.DataFrame(columns=["pergunta","indicador","produto_existente","novo_cruzamento","granularidade","disponibilidade",
                          "processamento_adicional","decisao_metodologica","produto_de_saida","status"]).to_csv(doc/"solicitacoes.csv",index=False)
    nav=d/"00_LEIA_PRIMEIRO"
    inventario=pd.DataFrame(e.itens)
    if not inventario.id.is_unique:
        raise ValueError("Identificação de produto repetida")
    inventario.to_csv(nav/"inventario_produtos.csv",index=False)
    indice=["# Atenção cardiovascular no Espírito Santo, 2014–2024","",
            "Entrega acadêmica da Camila · Observatório SUS-ES","","[Manual de leitura](../05_MANUAL_DA_ESTUDANTE/manual.md) · [Guia de navegação](guia_de_navegacao.md) · [Inventário com unidades e fontes](inventario_produtos.csv) · [Roteiro do orientador](../06_ROTEIRO_DO_ORIENTADOR/roteiro.md)","",
            "As tabelas analíticas permitem filtrar todos os anos e estratos. As figuras abrem em SVG e têm uma versão PNG na mesma pasta. Cada figura usa o CSV indicado ao lado.",""]
    for tipo in ["Tabela","Gráfico","Mapa"]:
        indice += ["## "+tipo+"s",""]
        for r in e.itens:
            if r["tipo"]!=tipo:
                continue
            nome=r["id"]+" · "+r["titulo"]
            linha=f"- [{nome}](../{r['tabela']})"
            if r["figura"]:
                linha=f"- [{nome}](../{r['figura']}) · [PNG](../{r['figura'][:-4]}.png) · [Tabela](../{r['tabela']})"
            indice.append(linha)
        indice.append("")
    indice += ["## Documentação","","- [Catálogo de indicadores CNES e PA](../07_DOCUMENTACAO_METODOLOGICA/catalogo_indicadores.csv)",
               "- [Indicadores validados, provisórios e exploratórios](../07_DOCUMENTACAO_METODOLOGICA/situacao_de_uso.csv)",
               "- [Registro de alterações para o manuscrito](../07_DOCUMENTACAO_METODOLOGICA/registro_decisoes_metodologicas.md)",
               "- [Ficha para solicitar cruzamentos](../07_DOCUMENTACAO_METODOLOGICA/solicitacoes.csv)",
               "- [Reprodução e verificação](../08_REPRODUTIBILIDADE/reproduzir.md)"]
    for alvo in re.findall(r"\]\(([^)]+)\)", "\n".join(indice)):
        if not (nav/alvo).exists() and alvo not in ["guia_de_navegacao.md","../08_REPRODUTIBILIDADE/reproduzir.md"]:
            raise ValueError("Destino de navegação ausente: "+alvo)
    (nav/"indice_geral.md").write_text("\n".join(indice),encoding="utf8")
    (nav/"guia_de_navegacao.md").write_text("""# Guia de navegação

Comece no manual e abra T10 para localizar o ano e o território. Os códigos B identificam bases analíticas; T identifica tabelas; F identifica figuras e M, mapas. O CSV com o mesmo nome de cada figura reproduz suas curvas ou células. O inventário informa fonte, numerador, denominador, unidade e janela.

Para mortalidade e I50, use B01–B03, T08 e T09. Para hospitalização e fluxos, use B04, B05, B08, B09, T01–T04, T11 e F25. Para cadastro e produção, consulte B06, B07, T05–T07, T10 e T12. O catálogo histórico detalha o código e a competência. Os centrais de leitura territorial são F02, F07 e os quatro mapas.

As tabelas contêm agregados para a análise acadêmica local. Os recortes detalhados por estabelecimento, os DBC, os recibos de aquisição e os logs integrais permanecem na custódia controlada. Para registrar pedidos, copie a ficha de solicitações da pasta 07 para fora desta edição selada.
""",encoding="utf8")
    for script in SCRIPTS:
        shutil.copyfile(REPO/"scripts"/script,repro/script)
    malhas={}
    for nome,url in [("municipios-es.geojson","https://servicodados.ibge.gov.br/api/v3/malhas/estados/32?formato=application/vnd.geo%2Bjson&qualidade=intermediaria&intrarregiao=municipio"),
                     ("ufs-br.geojson","https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo%2Bjson&qualidade=minima&intrarregiao=UF")]:
        malhas[nome]={"fonte":url,"sha256":sha256_arquivo(o/"fontes"/nome)}
    (repro/"ambiente_e_malhas.json").write_text(json.dumps(dict(python=platform.python_version(),pandas=pd.__version__,
            matplotlib=matplotlib.__version__,numpy=np.__version__,malhas=malhas),indent=2,ensure_ascii=False),encoding="utf8")
    (repro/"reproduzir.md").write_text("""# Reprodução local

A partir do checkout institucional, carregue o ambiente em que os leitores foram validados e acrescente a pasta python ao PYTHONPATH. A entrada é o diretório de custódia que contém mandato-v3, mandato-v3.1-sih e mandato-v3.2. O segundo argumento é a edição identificada no roteiro do orientador.

```powershell
$env:PYTHONPATH=(Resolve-Path python).Path
python scripts/entrega_academica_camila.py $custodia $manuscrito
```

Os scripts deste diretório identificam a implementação. O checkout fornece os módulos institucionais de lote, custódia e leitura. O roteiro-referencial.json corresponde ao argumento opcional --guia. O padrão usa fontes/roteiro-referencial-v4.json na custódia v3.2. As malhas municipais e estaduais do IBGE estão vinculadas por SHA-256. O processamento usa os agregados congelados nos recibos de entrada e testa as somas dos mapas, as margens estadual e municipal, as contagens hospitalares e as chaves territoriais. A data de referência geográfica do estudo é a da tabela PDR, independentemente da simplificação gráfica da malha.

O recibo na raiz contém o SHA-256 de cada saída. Para verificar uma cópia, calcule o SHA-256 dos caminhos em saidas, todos relativos à raiz. Uma execução no mesmo destino confere o cache selado. Para testar uma nova versão, informe outro diretório externo com --destino. Os DBC e os registros individuais ficam na custódia original.
""",encoding="utf8")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("custodia",type=Path)
    p.add_argument("manuscrito",type=Path)
    p.add_argument("--guia",type=Path)
    p.add_argument("--destino",type=Path)
    args=p.parse_args()
    v=args.custodia/"mandato-v3"
    o=args.custodia/"mandato-v3.2"
    h=args.custodia/"mandato-v3.1-sih/entrega-final"
    guia=args.guia or o/"fontes/roteiro-referencial-v4.json"
    entradas={"entrega_sih":conferir(h),"taxas":conferir(v/"taxas-ed2"),"i50":conferir(v/"sintese-verificada"),
              "recortes_lt":conferir(o/"recortes-lt-202412"),
              "etapa1":conferir(o/"etapa1"),"historico":conferir(o/"historico"),"checkpoint":conferir(o/"checkpoint-etapa1"),
              "manuscrito":args.manuscrito,"guia":guia,"pdr":PDR}
    for ano in range(2014,2025):
        entradas[f"estratos_{ano}"]=conferir(v/f"estratos/{ano}")
    for f in [o/"fontes/municipios-es.geojson",o/"fontes/ufs-br.geojson",DOCS/"registro_decisoes_metodologicas.md",DOCS/"manual_leitura_assistencial.md"]:
        entradas[f.name]=f
    def calcular(stage):
        return gerar(stage,v,h,o,args.manuscrito,guia)
    r=executar(args.destino or o/NOME,entradas,{"etapa":2,"pdr":"ES 2024","censo_principal":2022,"censo_complementar":2010},calcular,[REPO/"scripts"/s for s in SCRIPTS])
    print(json.dumps({"id":r["id"],**r["controles"]},ensure_ascii=False))


if __name__=="__main__":
    main()
