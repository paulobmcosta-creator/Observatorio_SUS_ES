from apoio import *
from observatorio_sus.estudos.camila.sim import GRUPOS
import json,shutil
w,root,base,out=folder("INTEGRACAO"); con=db(); ex=con.execute; e=papel("agregados_oferta"); geo(con)
assert len(list((w/"projecoes/RD").glob("*/recibo.json")))==132
for name,path in {"cadastro":e/"cadastro_estabelecimentos.csv.gz","rec":e/"recursos_estabelecimento.csv.gz","pa":e/"pa_por_estabelecimento.csv.gz","rd":w/"projecoes/RD/*/celulas.csv.gz","sr":e/"servicos_historicos_cnes.csv.gz"}.items(): materialize(con,name,path)
def put(name,sql):export(con,out/(name+".csv.gz"),sql)
for t in ["cadastro","rec","sr"]:
    assert not ex(f"SELECT count(*) FROM {t} WHERE cnes IS NULL OR NOT regexp_full_match(cnes,'[0-9]{{7}}') OR cnes='0000000'").fetchone()[0],t
assert not ex("SELECT count(*) FROM (SELECT mes,cnes FROM cadastro GROUP BY ALL HAVING count(*)<>1)").fetchone()[0]
def valid(c):return f"regexp_full_match({c},'[0-9]{{7}}') AND {c}<>'0000000'"
ex("""CREATE TABLE producao AS SELECT PA_CMP mes,pa.mes movimento,cnes,municipio,PA_PROC_ID codigo,PA_DOCORIG instrumento,classe,grupo_clinico,registro,versao_atributos,
sum(PA_QTDAPR::INT)::BIGINT aprovadas,sum(PA_QTDPRO::INT)::BIGINT apresentadas FROM pa WHERE situacao='elegivel' AND classe IN ('A','B') AND PA_CMP BETWEEN '201401' AND '202412' GROUP BY ALL""")
put("PA_detalhe_janela_original","FROM producao")
groups="CASE "+" ".join(f"WHEN substr(DIAG_PRINC,2,2)::INT BETWEEN {lo} AND {hi} THEN '{g}'" for g,(lo,hi) in GRUPOS.items())+" ELSE 'OUTRAS_I00_I99' END"
put("SIH_diagnostico_admissao_residencia",f"SELECT movimento processamento,left(movimento,4) ano_processamento,ano_admissao,CNES,MUNIC_MOV,MUNIC_RES,DIAG_PRINC,{groups} grupo,sum(linhas::INT)::BIGINT aih FROM rd GROUP BY ALL")
materialize(con,"ref",papel("referencia_sih"))
checks=ex("""WITH a AS (SELECT left(movimento,4) ano,MUNIC_RES municipio_res,MUNIC_MOV municipio_at,sum(linhas::INT) n FROM rd GROUP BY ALL),b AS (SELECT ano,municipio_res,municipio_at,sum(aih::INT) n FROM ref WHERE uf_atendimento='ES' GROUP BY ALL) SELECT count(*),sum(abs(coalesce(a.n,0)-coalesce(b.n,0))) FROM a FULL JOIN b USING(ano,municipio_res,municipio_at)""").fetchone()
assert checks[1]==0,checks
ex(f"CREATE TABLE amb AS SELECT mes,cnes,min(municipio) municipio,sum(CASE WHEN classe='A' THEN aprovadas ELSE 0 END) especificas,sum(CASE WHEN classe='A' THEN apresentadas ELSE 0 END) apresentadas,sum(CASE WHEN classe='B' THEN aprovadas ELSE 0 END) contextuais FROM producao WHERE {valid('cnes')} GROUP BY mes,cnes")
ex(f"CREATE TABLE hosp AS SELECT movimento mes,cnes,min(MUNIC_MOV) municipio,sum(linhas::INT) aih FROM rd WHERE {valid('cnes')} GROUP BY movimento,cnes")
put("chaves_inconclusivas",f"SELECT 'PA' fonte,mes,cnes,municipio,classe,sum(aprovadas) quantidade FROM producao WHERE NOT coalesce({valid('cnes')},false) GROUP BY ALL UNION ALL SELECT 'SIH',movimento,cnes,MUNIC_MOV,'G0',sum(linhas::INT) FROM rd WHERE NOT coalesce({valid('cnes')},false) GROUP BY ALL")
put("geografia_divergente_fonte","SELECT 'PA' fonte,mes,cnes,municipio,sum(aprovadas) quantidade FROM producao WHERE (mes,cnes) IN (SELECT mes,cnes FROM producao GROUP BY ALL HAVING count(DISTINCT municipio)>1) GROUP BY ALL UNION ALL SELECT 'SIH',movimento,cnes,MUNIC_MOV,sum(linhas::INT) FROM rd WHERE (movimento,cnes) IN (SELECT movimento,cnes FROM rd GROUP BY ALL HAVING count(DISTINCT MUNIC_MOV)>1) GROUP BY ALL")
# Conserve each resource measure with its unit. Specificity is not additive across families.
card="(id IN ('SR_CARD','LT_02_QT_EXIST','LT_32_QT_EXIST') OR starts_with(id,'HB_') OR (starts_with(id,'PF_') AND ends_with(id,'_vinculos')))"
hosp="(id IN ('LT_02_QT_EXIST','LT_32_QT_EXIST') OR starts_with(id,'HB_'))"
ex(f"""CREATE TABLE marks AS SELECT mes,cnes,municipio,{card} AND valor::DOUBLE>0 especifico,{hosp} AND valor::DOUBLE>0 estrutura_hosp,id='SR_CARD' AND valor::DOUBLE>0 sr,starts_with(id,'HB_') AND valor::DOUBLE>0 hab FROM rec WHERE id<>'ST_CAD' AND id<>'ST_SUS' UNION ALL SELECT mes,cnes,municipio,true,true,true,false FROM sr WHERE SERV_ESP='140' AND CLASS_SR='014' AND descricao_classe IS NOT NULL""")
ex("CREATE TABLE rsum AS SELECT mes,cnes,min(municipio) municipio,bool_or(especifico) especifico,bool_or(estrutura_hosp) estrutura_hosp,bool_or(sr) sr,bool_or(hab) hab FROM marks GROUP BY mes,cnes")
ex(((Path(__file__).resolve().parents[3]/"integracao_estabelecimentos/integracao_geral.sql")).read_text(encoding="utf8"))
ex("CREATE TABLE m AS SELECT matriz.*,coalesce(geo.regiao,'INDETERMINADA') regiao FROM matriz LEFT JOIN geo USING(municipio)")
assert ex("SELECT count(*)=count(DISTINCT (mes,cnes)) FROM m").fetchone()[0]
put("A_cadastro_ambulatorio","SELECT mes,cnes,municipio,regiao,cadastrado,VINC_SUS,recurso_especifico,servico,aprovadas,apresentadas,contextuais,tem_pa FROM m")
put("B_cadastro_hospitalar","SELECT mes,cnes,municipio,regiao,cadastrado,VINC_SUS,estrutura_hosp,habilitacao,aih,tem_sih FROM m")
put("C_cadastro_producao_integrada","FROM m")
put("recursos_vigentes","SELECT * FROM rec WHERE id NOT IN ('ST_CAD','ST_SUS')")
put("servicos_e_classes","SELECT mes,cnes,municipio,SERV_ESP,CLASS_SR,AMB_SUS,HOSP_SUS,TERCEIRO,descricao_classe FROM sr WHERE (SERV_ESP='116' OR SERV_ESP||'/'||CLASS_SR IN ('122/003','122/007','126/004','140/014','162/005')) AND descricao_classe IS NOT NULL GROUP BY ALL")
shutil.copy2(e/"dicionario_recursos.csv",out/"dicionario_recursos.csv")
put("D_evolucao","""WITH d AS (SELECT *,strftime(strptime(mes,'%Y%m')+INTERVAL 1 MONTH,'%Y%m') seguinte FROM m)
 SELECT coalesce(a.mes,b.seguinte) mes,coalesce(a.cnes,b.cnes) cnes,coalesce(a.municipio,b.municipio) municipio,
 CASE WHEN a.mes='201401' THEN 'inicio_da_observacao' WHEN a.cadastrado AND b.cadastrado THEN 'permanencia' WHEN a.cadastrado THEN 'entrada_ou_reentrada' WHEN b.cadastrado THEN 'saida' ELSE 'sem_ST' END cadastro,
 b.situacao situacao_anterior,a.situacao situacao_no_mes FROM d a FULL JOIN d b ON a.mes=b.seguinte AND a.cnes=b.cnes WHERE coalesce(a.mes,b.seguinte)<='202412'""")
levels="SELECT *, 'ES' nivel,'ES' territorio FROM m UNION ALL SELECT *,'Região',regiao FROM m UNION ALL SELECT *,'Município',municipio FROM m"
ex(f"""CREATE TABLE anos AS SELECT left(mes,4) ano,nivel,territorio,cnes,bool_or(cadastrado) st,bool_or(VINC_SUS='1') sus,bool_or(recurso_especifico) recurso,bool_or(estrutura_hosp) estrutura_hosp,bool_or(tem_pa) pa,bool_or(tem_sih) sih,bool_or(tem_pa AND tem_sih) ambos_mes FROM ({levels}) GROUP BY ALL""")
ex("""CREATE TABLE estratos AS SELECT ano,nivel,territorio,st,coalesce(sus,false) sus,recurso,estrutura_hosp,CASE WHEN pa AND sih THEN 'ambos' WHEN pa THEN 'apenas_PA' WHEN sih THEN 'apenas_SIH' ELSE 'nenhum' END situacao,count(*) estabelecimentos FROM anos GROUP BY ALL""")
put("E_territorios_anuais","SELECT *,100.*estabelecimentos/sum(estabelecimentos) OVER(PARTITION BY ano,nivel,territorio) percentual FROM estratos")
put("seis_medidas_anuais","SELECT ano,nivel,territorio,count(*) universo,count_if(st) cadastrados,count_if(sus) vinculo_sus,count_if(recurso) com_recurso,count_if(pa) com_pa,count_if(sih) com_sih,count_if(pa AND sih) ambos_no_ano,count_if(ambos_mes) ambos_no_mes FROM anos GROUP BY ALL ORDER BY ALL")
put("confronto_territorial","SELECT mes,municipio,regiao,count(*) cnes,sum(aprovadas) aprovadas,sum(contextuais) contextuais,sum(aih) aih,count_if(conflito_territorial) conflitos FROM m GROUP BY ALL")
print("T28",checks,"matriz",ex("SELECT count(*),sum(aih),sum(aprovadas),count_if(conflito_territorial) FROM m").fetchone(),flush=True)
