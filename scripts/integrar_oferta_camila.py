"""Validar e integrar cadastro, norma e produção por estabelecimento e competência."""
import argparse
import json
import re
from pathlib import Path
from zipfile import ZipFile

import duckdb
import pandas as pd
from historico_clinico_camila import REAB, EXAMES, DOPPLER
from qualificar_particoes_camila import CHAVES, MESES, PROF
from observatorio_sus.estudos.camila import territorio, sigtap
from observatorio_sus.estudos.camila.lote import executar, produtos
from observatorio_sus.io.custodia import sha256_arquivo


def registro_pa_sql(campo):
    """Mapear a origem real do PA ao instrumento SIGTAP segundo o informe SIA, p. 3."""
    return f"CASE {campo} WHEN 'C' THEN '01' WHEN 'I' THEN '02' WHEN 'P' THEN '06' WHEN 'S' THEN '07' WHEN 'A' THEN '08' WHEN 'B' THEN '09' END"


def literal(valor):
    return "'"+str(valor).replace("'","''")+"'"


def ler_sql(path):
    return f"read_csv({literal(Path(path).as_posix())},header=true,all_varchar=true,filename=true)"


def copia(db,stage,nome,sql):
    db.execute(f"COPY ({sql}) TO {literal((stage/nome).as_posix())} (HEADER, FORMAT CSV)")


def conferir(p):
    rec=json.loads((p/"recibo.json").read_text())
    if produtos(p)!=rec["saidas"]:
        raise ValueError(f"Recibo incompatível em {p}")
    return p/"recibo.json"


def conversao(z,nome):
    arq=next(x for x in z.namelist() if x.lower()=="cnv/"+nome.lower()+".cnv")
    resultado={}
    for l in z.read(arq).decode("latin1").splitlines():
        m=re.fullmatch(r"\s*\d+\s+(.+?)\s{2,}(\d+)\s*",l)
        if m: resultado[m[2]]=m[1].strip()
    return resultado


def recursos(db,aux):
    """Regras explícitas, com a unidade e o denominador de cada estoque."""
    defs=[]; selecoes=[]
    def regra(id,fam,nome,regra_sql,expr,unidade,codigos,status="Validado",limite="Estoque cadastral mensal."):
        defs.append((id,fam,nome,unidade,codigos,regra_sql,expr,status,limite))
        selecoes.append(f"SELECT mes,cnes,municipio,'{id}' id,({expr})::DOUBLE valor FROM {fam} WHERE {regra_sql} GROUP BY mes,cnes,municipio")
    regra("ST_CAD","ST","Estabelecimentos cadastrados","true","1","estabelecimentos","CNES distinto")
    regra("ST_SUS","ST","Estabelecimentos com vínculo SUS","VINC_SUS='1'","1","estabelecimentos","VINC_SUS=1")
    regra("SR_CARD","SR","Estabelecimentos com serviço cardiovascular classificado","SERV_ESP='116' AND EXISTS (SELECT 1 FROM servicos h WHERE h.competencia=SR.mes AND h.servico=SR.SERV_ESP AND h.classificacao=SR.CLASS_SR AND h.descricao_servico ILIKE '%cardio%')","1","estabelecimentos","SR 116 e classificação histórica")
    regra("SR_CARD_SUS","SR","Estabelecimentos com serviço cardiovascular ambulatorial SUS","SERV_ESP='116' AND AMB_SUS='1' AND EXISTS (SELECT 1 FROM servicos h WHERE h.competencia=SR.mes AND h.servico=SR.SERV_ESP AND h.classificacao=SR.CLASS_SR AND h.descricao_servico ILIKE '%cardio%')","1","estabelecimentos","SR 116, AMB_SUS=1")
    vig="regexp_full_match(CMPT_INI,'(19|20)[0-9]{2}(0[1-9]|1[012])') AND CMPT_INI<=mes AND (coalesce(CMPT_FIM,'') IN ('','000000','999999') OR (regexp_full_match(CMPT_FIM,'(19|20)[0-9]{2}(0[1-9]|1[012])') AND CMPT_FIM>=mes))"
    for cod in ["0801","0802","0803","0804","0805","0806","0807","0815","2411","2608","2609"]:
        regra("HB_"+cod,"HB","Estabelecimentos com habilitação "+cod,f"lpad(SGRUPHAB,4,'0')='{cod}' AND {vig} AND EXISTS (SELECT 1 FROM habilitacoes h WHERE h.competencia=HB.mes AND h.codigo='{cod}')","1","estabelecimentos",cod,limite="Título e vigência na edição mensal. Habilitações diferentes podem coexistir.")
    with ZipFile(aux) as z:
        leitos=conversao(z,"Esp_leit")
        equip=conversao(z,"equipam2507")
    for cod,tipo in {"02":"1","32":"2","85":"3","86":"3","03":"1","33":"2","75":"3","76":"3"}.items():
        for medida in ["QT_EXIST","QT_SUS"]:
            titulo={"1":"cirúrgico","2":"clínico","3":"complementar"}[tipo]+" • "+leitos[cod]+" • "+medida
            regra("LT_"+cod+"_"+medida,"LT",titulo,f"TP_LEITO='{tipo}' AND CODLEITO='{cod}'",f"sum({medida}::INTEGER)","leitos",tipo+"/"+cod+" "+medida,
                  "Validado" if cod in {"02","32","03","33"} else "Provisório",
                  "Domínio LFCES001 do SCNES 2009 e conversão TabWin. UTI e UCO em revisão de continuidade histórica; cirurgia e clínica geral são contexto.")
    for cod in ["101","110","113","441","551","556","559","565","566","676"]:
        for medida in ["QT_EXIST","QT_USO"]:
            regra("EQ_"+cod+"_"+medida,"EQ",equip[cod]+" • "+medida,f"TIPEQUIP||CODEQUIP='{cod}'",f"sum({medida}::INTEGER)","equipamentos",cod+" "+medida,
                  limite="Conversão oficial até 202507. Equipamento compartilhável entre especialidades.")
        regra("EQ_"+cod+"_SUS","EQ",equip[cod]+" • em uso com indicação SUS",f"TIPEQUIP||CODEQUIP='{cod}' AND IND_SUS='1'","sum(QT_USO::INTEGER)","equipamentos",cod+" IND_SUS=1",limite="Indicação cadastral SUS do registro; uso efetivo e exclusividade não mensurados.")
    for c in PROF:
        cond=f"CBO='{c}' AND EXISTS (SELECT 1 FROM ocupacoes h WHERE h.competencia=PF.mes AND h.codigo='{c}')"
        for col,expr,unidade in [("vinculos","sum(linhas::INTEGER)","registros de vínculo"),("horas_amb","sum(HORA_AMB::INTEGER)","horas ambulatoriais cadastradas"),
                ("horas_hosp","sum(HORAHOSP::INTEGER)","horas hospitalares cadastradas"),("outras_horas","sum(HORAOUTR::INTEGER)","outras horas cadastradas"),
                ("estabelecimentos","1","estabelecimentos"),("vinculos_sus","sum(linhas::INTEGER)","registros de vínculo SUS")]:
            regra("PF_"+c+"_"+col,"PF","CBO "+c+" • "+col,cond+(" AND PROF_SUS='1'" if col=="vinculos_sus" else ""),expr,unidade,c,limite="Preservar múltiplos vínculos. Pessoas distintas e postos contratuais não foram contados.")
    regra("EP_ATIVAS","EP","Equipes identificadas ativas ao fim do mês","vigencia='ativa_ao_fim'","sum(linhas::INTEGER)","equipes","IDEQUIPE e datas",limite="Contexto geral das equipes. Não classifica a especialidade de atuação.")
    db.execute("CREATE TABLE recursos AS "+" UNION ALL ".join(selecoes))
    return pd.DataFrame(defs,columns="id familia titulo unidade codigos filtro formula status limitacao".split())


def construir(v,out,stage):
    db=duckdb.connect(str(stage/"trabalho.duckdb"))
    db.execute("SET threads=2")
    def criar(nome,path,mes=False):
        campo="split_part(replace(filename,chr(92),'/'),'/',-2) mes," if mes else ""
        db.execute(f"CREATE TABLE {nome} AS SELECT {campo} * EXCLUDE(filename) FROM {ler_sql(path)}")
    for fam in CHAVES:
        criar(fam,out/"particoes"/"*"/(fam+".csv.gz"),True)
    lt_reposto=ler_sql(out/"reposicao-lt/202412/LT.csv.gz")
    db.execute(f"INSERT INTO LT BY NAME SELECT '202412' mes,* EXCLUDE(filename,QT_CONTR) FROM {lt_reposto}")
    criar("extra",out/"reabilitacao/*/PA.csv.gz",True)
    criar("pdr",territorio.TABELA)
    for nome in ["procedimentos","servicos","habilitacoes","ocupacoes"]:
        criar(nome,out/"historico"/(nome+".csv.gz"))
    criar("cp04",v.parent/"acervo/CP04/Resultados/CNES_LT_202412_ESTOQUE_POR_CODIGO.csv")
    criar("basepa",v/"assistencia-final/sia_mensal.csv")
    criar("baseep",v/"equipes/equipes_mensais.csv")
    criar("basecnes",v/"assistencia-final/cnes_mensal.csv")
    criar("pop",v/"taxas-ed2/RIPSA_DEM101_QA_TOTAIS.csv")
    db.execute("CREATE VIEW geo AS SELECT cod_municipio_cnes municipio,regiao_nome regiao FROM pdr")
    db.execute("CREATE TABLE calendario AS SELECT DISTINCT competencia mes FROM procedimentos")
    if db.execute("SELECT count(*) FROM calendario").fetchone()[0]!=132:raise ValueError("Cobertura SIGTAP")
    if db.execute("SELECT count(*) FROM (SELECT mes,cnes FROM ST GROUP BY ALL HAVING count(*)<>1 OR sum(linhas::INT)<>1)").fetchone()[0]:
        raise ValueError("ST não é único em CNES/mês")
    catalogo=recursos(db,out/"fontes/TAB_CNES.zip")
    catalogo.to_csv(stage/"dicionario_recursos.csv",index=False)
    db.register("dicionario",catalogo)
    db.execute("CREATE TABLE dados_pa AS SELECT *,false adicional FROM PA UNION ALL SELECT *,true adicional FROM extra")
    # O informe SIA distingue registros principais e secundários de APAC no próprio PA.
    db.execute(f"""CREATE TABLE classificacao AS SELECT p.*,s.presente,s.grupo_clinico,s.classe,s.complexidade,
      s.modalidade,s.registro,s.servico,s.habilitacao,s.versao_atributos,
      CASE WHEN s.competencia IS NULL THEN 'sem_edicao'
           WHEN s.presente<>'1' THEN 'ausente_na_edicao'
           WHEN PA_PROC_ID='0301010072' AND (PA_CBOCOD NOT IN ('225120','225210','225203') OR NOT list_contains(string_split(s.ocupacao,' '),PA_CBOCOD)) THEN 'cbo_fora_recorte'
           WHEN NOT coalesce(list_contains(string_split(s.registro,' '), {registro_pa_sql("PA_DOCORIG")}),false) THEN 'instrumento_incompativel'
           WHEN coalesce(PA_QTDAPR::BIGINT,-1)<0 OR coalesce(PA_QTDPRO::BIGINT,-1)<0 THEN 'quantidade_invalida'
           WHEN s.classe='D' THEN 'sob_revisao' ELSE 'elegivel' END situacao
      FROM dados_pa p LEFT JOIN procedimentos s ON p.PA_CMP=s.competencia AND p.PA_PROC_ID=s.codigo""")
    if db.execute("SELECT (SELECT count(*) FROM classificacao)<>(SELECT count(*) FROM dados_pa)").fetchone()[0]:
        raise ValueError("Duplicação na dimensão SIGTAP")
    copia(db,stage,"intervalos_sigtap.csv.gz","SELECT codigo,versao_atributos,min(competencia) inicio,max(competencia) fim,count(*) meses,descricao,classe,grupo_clinico,presente,complexidade,modalidade,registro,ocupacao,servico,habilitacao FROM procedimentos GROUP BY ALL ORDER BY codigo,inicio")
    db.execute("""CREATE TABLE conf_pa AS WITH a AS
      (SELECT mes,PA_CMP prod,PA_PROC_ID cod,PA_CBOCOD cbo,coalesce(regiao,'OUTRO_OU_IGN') reg,
       sum(linhas::BIGINT) linhas,sum(PA_QTDAPR::BIGINT) aprov,sum(PA_QTDPRO::BIGINT) apres FROM PA LEFT JOIN geo USING(municipio) GROUP BY ALL),
      b AS (SELECT movimento mes,producao prod,procedimento cod,cbo,regiao_atendimento reg,
       sum(quantidade::BIGINT) FILTER(WHERE medida='linhas') linhas,sum(quantidade::BIGINT) FILTER(WHERE medida='aprov') aprov,
       sum(quantidade::BIGINT) FILTER(WHERE medida='apres') apres FROM basepa GROUP BY ALL)
       SELECT mes,prod,cod,cbo,reg,coalesce(a.linhas,0)-coalesce(b.linhas,0) dl,
       coalesce(a.aprov,0)-coalesce(b.aprov,0) da,coalesce(a.apres,0)-coalesce(b.apres,0) dp FROM a FULL JOIN b USING(mes,prod,cod,cbo,reg)""")
    desvios=db.execute("SELECT count(*) FROM conf_pa WHERE dl<>0 OR da<>0 OR dp<>0").fetchone()[0]
    if desvios:raise ValueError(f"PA diverge do checkpoint anterior em {desvios} células")
    ep=db.execute("""WITH a AS (SELECT mes,coalesce(regiao,'ES_IGN') regiao,TIPO_EQP tipo,vigencia,sum(linhas::INT) n FROM EP LEFT JOIN geo USING(municipio) GROUP BY ALL),
       b AS (SELECT competencia mes,regiao,tipo,vigencia,equipes::INT n FROM baseep)
       SELECT count(*) FROM a FULL JOIN b USING(mes,regiao,tipo,vigencia) WHERE coalesce(a.n,0)<>coalesce(b.n,0)""").fetchone()[0]
    if ep:raise ValueError(f"EP diverge da série anterior em {ep} células")
    copia(db,stage,"controle_pa_mensal.csv","SELECT mes,count(*) celulas_comparadas,sum(abs(dl)) diferenca_linhas,sum(abs(da)) diferenca_aprovada,sum(abs(dp)) diferenca_apresentada FROM conf_pa GROUP BY mes ORDER BY mes")
    copia(db,stage,"pa_por_estabelecimento.csv.gz","SELECT p.*,coalesce(g.regiao,'INDETERMINADA') regiao_at FROM classificacao p LEFT JOIN geo g USING(municipio)")
    copia(db,stage,"recursos_estabelecimento.csv.gz","SELECT r.*,coalesce(g.regiao,'INDETERMINADA') regiao FROM recursos r LEFT JOIN geo g USING(municipio)")
    copia(db,stage,"cadastro_estabelecimentos.csv.gz","SELECT st.*,coalesce(g.regiao,'INDETERMINADA') regiao FROM ST LEFT JOIN geo g USING(municipio)")
    copia(db,stage,"servicos_historicos_cnes.csv.gz","SELECT r.*,s.descricao_servico,s.descricao_classe FROM SR r LEFT JOIN servicos s ON r.mes=s.competencia AND r.SERV_ESP=s.servico AND r.CLASS_SR=s.classificacao")
    copia(db,stage,"habilitacoes_historicas_cnes.csv.gz","SELECT h.*,s.descricao FROM HB h LEFT JOIN habilitacoes s ON h.mes=s.competencia AND lpad(h.SGRUPHAB,4,'0')=s.codigo")
    copia(db,stage,"qualidade_pa.csv","SELECT mes movimento,PA_CMP producao,PA_DOCORIG instrumento,situacao,coalesce(grupo_clinico,'sem_edicao') grupo,sum(linhas::BIGINT) linhas,sum(PA_QTDAPR::BIGINT) aprovadas,sum(PA_QTDPRO::BIGINT) apresentadas FROM classificacao GROUP BY ALL ORDER BY ALL")
    # Vínculo descritivo ao cadastro da competência de produção. Uma linha por combinação de produção.
    db.execute("""CREATE TABLE vinculo AS WITH src AS (SELECT mes,cnes,list(DISTINCT SERV_ESP||'/'||CLASS_SR) servs FROM SR GROUP BY ALL),
      h AS (SELECT mes,cnes,list(DISTINCT lpad(SGRUPHAB,4,'0')) habs FROM HB WHERE regexp_full_match(CMPT_INI,'(19|20)[0-9]{2}(0[1-9]|1[012])') AND CMPT_INI<=mes AND (coalesce(CMPT_FIM,'') in ('','000000','999999') OR (regexp_full_match(CMPT_FIM,'(19|20)[0-9]{2}(0[1-9]|1[012])') AND CMPT_FIM>=mes)) GROUP BY ALL),
      r AS (SELECT mes,cnes,count(DISTINCT id) tipos FROM recursos WHERE id NOT LIKE 'ST_%' AND valor>0 GROUP BY ALL)
      SELECT p.mes movimento,p.PA_CMP producao,p.cnes,p.municipio,st.municipio municipio_st,
      coalesce(g.regiao,'INDETERMINADA') regiao_at,p.PA_PROC_ID codigo,p.grupo_clinico,p.situacao,
      st.cnes IS NOT NULL cadastrado,st.municipio=p.municipio mesmo_municipio,r.tipos,
      CASE WHEN p.servico IS NULL OR trim(p.servico)='' OR st.cnes IS NULL THEN NULL ELSE list_has_any(coalesce(src.servs,[]),string_split(p.servico,' ')) END algum_servico_relacionado,
      CASE WHEN p.habilitacao IS NULL OR trim(p.habilitacao)='' OR st.cnes IS NULL THEN NULL ELSE list_has_any(coalesce(h.habs,[]),list_transform(string_split(p.habilitacao,' '),x->split_part(x,'/',1))) END alguma_habilitacao_relacionada,
      sum(p.linhas::INT) linhas,sum(p.PA_QTDAPR::BIGINT) aprovadas,sum(p.PA_QTDPRO::BIGINT) apresentadas
      FROM classificacao p LEFT JOIN ST st ON st.mes=p.PA_CMP AND st.cnes=p.cnes
      LEFT JOIN geo g ON g.municipio=p.municipio LEFT JOIN src ON src.mes=p.PA_CMP AND src.cnes=p.cnes
      LEFT JOIN h ON h.mes=p.PA_CMP AND h.cnes=p.cnes LEFT JOIN r ON r.mes=p.PA_CMP AND r.cnes=p.cnes GROUP BY ALL""")
    if db.execute("SELECT (SELECT sum(aprovadas) FROM vinculo)<>(SELECT sum(PA_QTDAPR::BIGINT) FROM classificacao)").fetchone()[0]:
        raise ValueError("Inflação na vinculação entre sistemas")
    copia(db,stage,"estrutura_producao.csv.gz","SELECT * FROM vinculo")
    copia(db,stage,"compatibilidade_regional.csv.gz","SELECT producao,regiao_at,grupo_clinico,situacao,cadastrado,mesmo_municipio,algum_servico_relacionado,alguma_habilitacao_relacionada,sum(linhas) linhas,sum(aprovadas) aprovadas,sum(apresentadas) apresentadas FROM vinculo GROUP BY ALL")
    db.execute("""CREATE TABLE pa_territorio AS SELECT PA_CMP competencia,municipio,coalesce(g.regiao,'INDETERMINADA') regiao,PA_PROC_ID codigo,grupo_clinico,situacao,PA_DOCORIG instrumento,complexidade,modalidade,sum(PA_QTDAPR::BIGINT) aprovadas,sum(PA_QTDPRO::BIGINT) apresentadas,sum(linhas::BIGINT) linhas,count(DISTINCT cnes) FILTER(WHERE PA_QTDAPR::BIGINT>0) estabelecimentos
        FROM classificacao LEFT JOIN geo g USING(municipio) GROUP BY ALL""")
    copia(db,stage,"pa_municipal.csv.gz","SELECT * FROM pa_territorio")
    db.execute("""CREATE TABLE agregado_pa AS SELECT PA_CMP competencia,coalesce(g.regiao,'INDETERMINADA') territorio,PA_PROC_ID codigo,grupo_clinico,situacao,sum(PA_QTDAPR::BIGINT) aprovadas,sum(PA_QTDPRO::BIGINT) apresentadas,sum(linhas::BIGINT) linhas,count(DISTINCT cnes) FILTER(WHERE PA_QTDAPR::BIGINT>0) unidades FROM classificacao LEFT JOIN geo g USING(municipio) GROUP BY ALL
        UNION ALL SELECT PA_CMP,'ES',PA_PROC_ID,grupo_clinico,situacao,sum(PA_QTDAPR::BIGINT),sum(PA_QTDPRO::BIGINT),sum(linhas::BIGINT),count(DISTINCT cnes) FILTER(WHERE PA_QTDAPR::BIGINT>0) FROM classificacao GROUP BY ALL""")
    copia(db,stage,"pa_regional_observado.csv.gz","SELECT * FROM agregado_pa")
    # Grade explícita. Ausência de edição, revisão clínica e APAC exclusiva sem observação não viram zero.
    db.execute("""CREATE TABLE pa_mensal AS WITH territorios AS (SELECT DISTINCT regiao territorio FROM geo UNION ALL SELECT 'ES'), obs AS
       (SELECT competencia,codigo,sum(linhas) linhas FROM agregado_pa WHERE territorio='ES' AND situacao='elegivel' GROUP BY ALL)
       SELECT p.competencia,t.territorio,p.codigo,p.descricao,p.versao_atributos,p.classe,p.grupo_clinico,p.modalidade,p.registro,
       CASE WHEN p.presente='0' THEN 'ausente_na_edicao' WHEN p.classe='D' THEN 'sob_revisao'
       WHEN NOT list_has_any(string_split(p.registro,' '),['01','02','06','07','08','09']) THEN 'instrumento_fora_do_PA'
       WHEN NOT list_has_any(string_split(p.registro,' '),['01','02']) AND coalesce(obs.linhas,0)=0 THEN 'sem_evidencia_PA_no_mes'
       ELSE 'validado' END estado,
       CASE WHEN estado='validado' THEN coalesce(a.aprovadas,0) END aprovadas,
       CASE WHEN estado='validado' THEN coalesce(a.apresentadas,0) END apresentadas,
       CASE WHEN estado='validado' THEN coalesce(a.unidades,0) END unidades
       FROM procedimentos p CROSS JOIN territorios t LEFT JOIN obs USING(competencia,codigo)
       LEFT JOIN agregado_pa a ON a.competencia=p.competencia AND a.codigo=p.codigo AND a.territorio=t.territorio AND a.situacao='elegivel'""")
    copia(db,stage,"pa_series_mensais.csv.gz","SELECT * FROM pa_mensal ORDER BY competencia,territorio,codigo")
    copia(db,stage,"pa_anuais.csv","SELECT left(competencia,4) ano,territorio,codigo,grupo_clinico,count(*) FILTER(WHERE estado='validado') meses_validos,sum(aprovadas) aprovadas_nos_meses_validos,sum(apresentadas) apresentadas_nos_meses_validos,CASE WHEN count(aprovadas)=12 THEN sum(aprovadas) END aprovadas_12_meses FROM pa_mensal GROUP BY ALL ORDER BY ALL")
    copia(db,stage,"pa_subtotais.csv","SELECT competencia,territorio,grupo_clinico,count(*) FILTER(WHERE estado='validado') codigos_elegiveis,sum(aprovadas) aprovadas,sum(apresentadas) apresentadas FROM pa_mensal WHERE classe IN ('A','B') GROUP BY ALL UNION ALL SELECT competencia,territorio,'soma_especificos_elegiveis',count(*) FILTER(WHERE estado='validado'),sum(aprovadas),sum(apresentadas) FROM pa_mensal WHERE classe='A' GROUP BY ALL ORDER BY ALL")
    copia(db,stage,"pa_instrumento_complexidade.csv.gz","SELECT PA_CMP competencia,grupo_clinico,coalesce(g.regiao,'INDETERMINADA') territorio,PA_DOCORIG instrumento,complexidade,modalidade modalidades_admitidas,sum(PA_QTDAPR::BIGINT) aprovadas,sum(PA_QTDPRO::BIGINT) apresentadas FROM classificacao LEFT JOIN geo g USING(municipio) WHERE situacao='elegivel' GROUP BY ALL ORDER BY ALL")
    copia(db,stage,"participacao_producao.csv.gz","WITH a AS (SELECT left(producao,4) ano,codigo,cnes,regiao_at,sum(aprovadas) n FROM vinculo WHERE situacao='elegivel' GROUP BY ALL) SELECT *,100*n/nullif(sum(n) OVER(PARTITION BY ano,codigo,regiao_at),0) pct_na_regiao,100*n/nullif(sum(n) OVER(PARTITION BY ano,codigo),0) pct_no_estado FROM a")
    medir_estoques(db,stage)
    controles_cnes=[]
    for fam,medidas in {"ST":["registros"],"HB":["registros"],"LT":["registros","QT_EXIST","QT_SUS","QT_NSUS"],
                        "EQ":["registros","QT_EXIST","QT_USO"],"PF":["registros","HORA_AMB","HORAHOSP","HORAOUTR"]}.items():
        filtro = " AND split_part(tipo,'/',1) IN ('225120','225210','225203')" if fam=="PF" else ""
        if fam=="LT": filtro+=" AND competencia<>'202412'"
        for medida in medidas:
            campo="linhas" if medida=="registros" else medida
            recorte = "WHERE mes<>'202412'" if fam=="LT" else ""
            q=f"""WITH a AS (SELECT mes,coalesce(regiao,'ES_IGN') reg,sum({campo}::BIGINT) n FROM {fam} LEFT JOIN geo USING(municipio) {recorte} GROUP BY ALL),
                    b AS (SELECT competencia mes,regiao reg,sum(quantidade::BIGINT) n FROM basecnes WHERE familia=? AND medida=? {filtro} GROUP BY ALL)
                    SELECT mes,reg,coalesce(a.n,0) calculado,coalesce(b.n,0) anterior FROM a FULL JOIN b USING(mes,reg)"""
            compara=db.execute(q,[fam,medida]).df()
            if not compara.calculado.eq(compara.anterior).all(): raise ValueError(f"Margens CNES divergentes em {fam} {medida}")
            controles_cnes.append(compara.assign(familia=fam,medida=medida))
    pd.concat(controles_cnes).to_csv(stage/"controles_cnes.csv.gz",index=False)
    copia(db,stage,"catalogo_clinico.csv","SELECT DISTINCT codigo,descricao,classe,grupo_clinico,CASE WHEN classe='D' THEN 'Provisório' ELSE 'Validado no escopo homologado; elegibilidade mensal no PA' END status,CASE WHEN classe='A' THEN 'Total específico apenas em competência e instrumento elegíveis' WHEN grupo_clinico='consulta_cbo' THEN 'CBO do recorte pertinência e compatibilidade no mês; motivo clínico desconhecido' WHEN classe='B' THEN 'Produção vascular contextual; fora do total específico' ELSE 'Fora do total específico e das séries definitivas' END regra FROM procedimentos WHERE presente='1' ORDER BY codigo,descricao")
    if db.execute("SELECT count(*) FROM (SELECT mes,territorio,id FROM estoque_regional GROUP BY ALL HAVING count(*)<>1)").fetchone()[0]:
        raise ValueError("Chave de estoque regional repetida")
    qa={"meses":len(MESES),"selecoes_recursos":len(catalogo),"particoes_sr":db.execute("SELECT count(DISTINCT mes) FROM SR").fetchone()[0],
        "celulas_regressao_pa":db.execute("SELECT count(*) FROM conf_pa").fetchone()[0],"divergencias_pa":desvios,"divergencias_ep":ep,
        "linhas_pa_recorte":db.execute("SELECT sum(linhas::BIGINT) FROM classificacao").fetchone()[0],
        "situacoes_pa":dict(db.execute("SELECT situacao,sum(linhas::BIGINT) FROM classificacao GROUP BY situacao").fetchall())}
    db.close()
    (stage/"trabalho.duckdb").unlink()
    return qa


def medir_estoques(db,stage):
    db.execute("""CREATE TABLE dominio_mes AS SELECT c.mes,d.*,
      CASE WHEN d.familia='HB' THEN EXISTS(SELECT 1 FROM habilitacoes h WHERE h.competencia=c.mes AND h.codigo=d.codigos)
           WHEN d.familia='PF' THEN EXISTS(SELECT 1 FROM ocupacoes h WHERE h.competencia=c.mes AND h.codigo=d.codigos)
           WHEN d.familia='SR' THEN EXISTS(SELECT 1 FROM servicos s WHERE s.competencia=c.mes AND s.servico='116' AND s.descricao_servico ILIKE '%cardio%')
           ELSE true END vigente FROM calendario c CROSS JOIN dicionario d""")
    db.execute("""CREATE TABLE estoque_municipal AS WITH a AS (SELECT mes,municipio,id,sum(valor) n FROM recursos GROUP BY ALL)
      SELECT d.mes,g.municipio,g.regiao,d.id,CASE WHEN d.vigente THEN coalesce(a.n,0) END valor
      FROM dominio_mes d CROSS JOIN geo g LEFT JOIN a ON a.mes=d.mes AND a.municipio=g.municipio AND a.id=d.id""")
    copia(db,stage,"estoques_municipais.csv.gz","SELECT * FROM estoque_municipal")
    db.execute("""CREATE TABLE estoque_regional AS WITH regioes AS (SELECT DISTINCT regiao territorio FROM geo UNION ALL SELECT 'ES'),
      regular AS (SELECT mes,coalesce(regiao,'INDETERMINADA') territorio,id,sum(valor) n FROM recursos LEFT JOIN geo USING(municipio) GROUP BY ALL
                  UNION ALL SELECT mes,'ES',id,sum(valor) FROM recursos GROUP BY ALL)
      SELECT d.mes,t.territorio,d.id,CASE WHEN d.vigente THEN coalesce(a.n,0) END valor,
       CASE WHEN NOT d.vigente THEN 'sem_dominio_historico' WHEN d.mes='202412' AND d.familia='LT' THEN 'DBC_reposto_conciliado_CP04' ELSE 'DBC' END evidencia
      FROM dominio_mes d CROSS JOIN regioes t LEFT JOIN regular a ON d.mes=a.mes AND t.territorio=a.territorio AND d.id=a.id""")
    copia(db,stage,"estoques_regionais.csv.gz","SELECT * FROM estoque_regional")
    copia(db,stage,"estoques_anuais.csv","""WITH p AS (SELECT ano,regiao territorio,sum(total::BIGINT) habitantes FROM pop JOIN geo ON datasus6=municipio GROUP BY ALL UNION ALL SELECT ano,'ES',sum(total::BIGINT) FROM pop GROUP BY ALL)
      SELECT left(mes,4) ano,e.territorio,id,count(valor) meses,avg(valor) media_mensal,min(valor) minimo,max(valor) maximo,p.habitantes,
      avg(valor)*100000/nullif(p.habitantes,0) media_por_100mil FROM estoque_regional e JOIN p ON left(e.mes,4)=p.ano AND e.territorio=p.territorio GROUP BY left(mes,4),e.territorio,id,p.habitantes ORDER BY ALL""")


def fechar(v,out):
    entradas={}
    for mes in MESES:
        for chave in ("particoes","reabilitacao"):
            entradas[chave+mes]=conferir(out/chave/mes)
    for pasta in [out/"historico",v/"assistencia-final",v/"equipes",v/"taxas-ed2"]:
        entradas[pasta.name]=conferir(pasta)
    entradas["lt_202412"]=conferir(out/"reposicao-lt/202412")
    entradas.update(pdr=territorio.TABELA,conversoes=out/"fontes/TAB_CNES.zip",informe=out/"fontes/informe_sia.pdf",
                    dezembro=v.parent/"acervo/CP04/Resultados/CNES_LT_202412_ESTOQUE_POR_CODIGO.csv")
    def medir(stage):
        return construir(v,out,stage)
    return executar(out/"etapa1",entradas,{"norma":"PA_CMP","estoque":"competência cadastral","pdr":territorio.VERSAO},medir)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("v",type=Path)
    p.add_argument("out",type=Path)
    a=p.parse_args()
    print(fechar(a.v,a.out)["controles"],flush=True)
