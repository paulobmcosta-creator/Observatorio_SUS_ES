from apoio import *
from integrar_oferta_camila import registro_pa_sql
import re,json,zipfile
w,root,base,out=folder("SIA");con=db();ex=con.execute;geo(con)
projs=sorted((w/"projecoes/PA").glob("*/recibo.json"))
assert len(projs)==144,len(projs)
inv=[]
for path in projs:
    r=json.loads(path.read_text())
    if path.parent.name[:4]=="2025":
        a=json.loads((w/"originais-assistencia/PA/ES"/path.parent.name/"aquisicao.json").read_text())
        inv.extend(dict(movimento=path.parent.name,producao=k,registros=v,arquivo=r["arquivo"],bytes=r["bytes"],sha256=r["origem"],uf="ES",url="ftp://ftp.datasus.gov.br/dissemin/publicos/SIASUS/200801_/Dados/"+r["arquivo"]) for k,v in r["competencias_producao_arquivo_2025"].items())
pd.DataFrame(inv).to_csv(out/"inventario_movimentos_2025.csv",index=False)
materialize(con,"pa",w/"projecoes/PA/*/celulas.csv.gz")
materialize(con,"s",base/"07_DOCUMENTACAO_METODOLOGICA/procedimentos.csv.gz")
assert ex("SELECT count(*)=count(DISTINCT (competencia,codigo)) FROM s").fetchone()[0]
ex(f"""CREATE TABLE elegivel AS SELECT PA_CODUNI cnes,PA_UFMUN municipio,PA_MUNPCN residencia,PA_CMP producao,movimento,PA_PROC_ID codigo,PA_DOCORIG instrumento,PA_CBOCOD cbo,s.classe,s.grupo_clinico,PA_QTDPRO::BIGINT apresentadas,PA_QTDAPR::BIGINT aprovadas,linhas::BIGINT linhas
FROM pa JOIN s ON PA_CMP=s.competencia AND PA_PROC_ID=s.codigo WHERE s.presente='1' AND s.classe IN ('A','B') AND list_contains(string_split(s.registro,' '),{registro_pa_sql('PA_DOCORIG')}) AND (PA_PROC_ID<>'0301010072' OR (PA_CBOCOD IN ('225120','225210','225203') AND list_contains(string_split(s.ocupacao,' '),PA_CBOCOD))) AND PA_QTDPRO::BIGINT>=0 AND PA_QTDAPR::BIGINT>=0""")
# Reconciliation by establishment, movement, production, code and instrument across the frozen window.
materialize(con,"frozen",papel("saida")/"INTEGRACAO/PA_detalhe_janela_original.csv.gz")
keys="mes,movimento,cnes,municipio,codigo,instrumento,classe"
ex(f"""CREATE TABLE delta AS WITH a AS (SELECT producao mes,movimento,cnes,municipio,codigo,instrumento,classe,sum(aprovadas) q,sum(apresentadas) p FROM elegivel WHERE movimento<='202412' GROUP BY ALL),
b AS (SELECT {keys},sum(aprovadas::BIGINT) q,sum(apresentadas::BIGINT) p FROM frozen GROUP BY ALL)
SELECT {keys},coalesce(a.q,0)-coalesce(b.q,0) d_aprovadas,coalesce(a.p,0)-coalesce(b.p,0) d_apresentadas FROM a FULL JOIN b USING({keys})""")
diff=ex("SELECT count(*),sum(abs(d_aprovadas)),sum(abs(d_apresentadas)) FROM delta").fetchone()
assert diff[1:]==(0,0),diff
z=zipfile.ZipFile(papel("municipios_cnes_zip"))
codes=[]
for line in z.read("CNV/BR_municip.cnv").decode("latin1").splitlines():
    m=re.match(r"^\s*\d+\s+(\d{6})\s+.*?\s+(\d{6})(?:,[^\r\n]*)?\s*$",line)
    if m and m[1]==m[2] and m[1] not in {"510183","000000"}:codes.append(m[1])
assert len(set(codes))==5570,len(set(codes))
dom=pd.DataFrame({"codigo":sorted(set(codes))});con.register("dominio_municipal",dom)
ex("CREATE TABLE medido AS "+(Path(__file__).resolve().parents[3]/"integracao_estabelecimentos/residencia_geral.sql").read_text(encoding="utf8"))
assert ex("SELECT (SELECT count(*) FROM medido)=(SELECT count(*) FROM elegivel)").fetchone()[0]
ex("CREATE VIEW m AS SELECT *,CASE WHEN movimento>'202412' THEN 'adicional_2025' ELSE 'janela_original' END janela FROM medido")
def put(n,q):export(con,out/(n+".csv.gz"),q)
put("residencia_por_competencia","SELECT janela,producao,movimento,instrumento,classe,grupo_clinico,codigo,situacao_residencia,sum(linhas) linhas,sum(aprovadas) aprovadas,sum(apresentadas) apresentadas FROM m GROUP BY ALL")
put("residencia_por_instrumento_ano","WITH a AS (SELECT janela,left(producao,4) ano,classe,instrumento,situacao_residencia,sum(aprovadas) n FROM m GROUP BY ALL) SELECT *,100.*n/nullif(sum(n) OVER(PARTITION BY janela,ano,classe,instrumento),0) pct_no_instrumento,100.*n/nullif(sum(n) OVER(PARTITION BY janela,ano,classe),0) pct_na_classe FROM a")
ex("""CREATE TABLE od AS SELECT janela,producao,classe,codigo,instrumento,residencia,municipio,coalesce(regiao_residencia,'UF_'||left(residencia,2)) origem,coalesce(regiao_destino,'INDETERMINADA') destino,sum(aprovadas) aprovadas,sum(apresentadas) apresentadas FROM m WHERE situacao_residencia='1_residencia_identificavel' GROUP BY ALL""")
put("OD_municipal","FROM od")
put("OD_regional","SELECT janela,producao,classe,instrumento,origem,destino,sum(aprovadas) aprovadas,sum(apresentadas) apresentadas FROM od GROUP BY ALL")
assert ex("SELECT (SELECT sum(aprovadas) FROM od)=(SELECT sum(aprovadas) FROM m WHERE situacao_residencia='1_residencia_identificavel')").fetchone()[0]
ex("""CREATE TABLE reconciliacao AS SELECT producao,cnes,municipio,regiao_destino,codigo,grupo_clinico,classe,instrumento,
sum(CASE WHEN movimento<='202412' THEN aprovadas ELSE 0 END) congelada,sum(CASE WHEN movimento>'202412' THEN aprovadas ELSE 0 END) adicional,
sum(CASE WHEN movimento<='202412' THEN apresentadas ELSE 0 END) apresentadas_congelada,sum(CASE WHEN movimento>'202412' THEN apresentadas ELSE 0 END) apresentadas_adicionais,
sum(aprovadas) janela_estendida,100.*adicional/nullif(congelada,0) diferenca_pct FROM m WHERE left(producao,4)='2024' GROUP BY ALL""")
put("reconciliacao_2024_detalhada","FROM reconciliacao")
put("serie_2024_por_competencia","SELECT producao,classe,sum(congelada) congelada,sum(adicional) adicional,sum(janela_estendida) janela_estendida,100.*sum(adicional)/nullif(sum(congelada),0) diferenca_pct FROM reconciliacao GROUP BY ALL ORDER BY ALL")
put("defasagens","SELECT producao,movimento,date_diff('month',strptime(producao,'%Y%m'),strptime(movimento,'%Y%m')) defasagem,codigo,instrumento,classe,sum(aprovadas) aprovadas,sum(apresentadas) apresentadas FROM m WHERE producao>='202401' GROUP BY ALL")
# Restrict exact-match audit to 2024 candidates in individual movements; includes ineligible instruments/codes within A/B candidates.
sig=w/"projecoes/PA/*/assinaturas.tsv.gz"
ex(f"""CREATE TABLE assin AS SELECT regexp_extract(replace(filename,chr(92),'/'),'/([0-9]{{6}})/assinaturas',1) mov,column0 sig,column1::BIGINT q,column2 cod,column3::BIGINT n FROM read_csv({quote(sig)},delim='\t',header=false,all_varchar=true,filename=true,columns={{'column0':'VARCHAR','column1':'VARCHAR','column2':'VARCHAR','column3':'VARCHAR'}})""")
assert ex("SELECT count(*) FROM assin WHERE mov=''").fetchone()[0]==0
put("controle_repeticoes","""WITH a AS (SELECT cod,sig,q,sum(CASE WHEN mov<'202501' THEN n ELSE 0 END) anterior,sum(CASE WHEN mov>='202501' THEN n ELSE 0 END) novo,count(DISTINCT mov) n_mov,max(n) maior FROM assin GROUP BY ALL) SELECT cod,count(*) assinaturas,sum(novo) linhas_adicionais,sum(least(anterior,novo)) correspondencias_entre_janelas,sum(q*least(anterior,novo)) qt_correspondente,sum(CASE WHEN n_mov>1 THEN anterior+novo-maior ELSE 0 END) repeticoes_entre_movimentos FROM a GROUP BY ALL""")
put("coincidencias_celulas","SELECT classe,codigo,count_if(adicional>0) celulas_com_acrescimo,count_if(adicional>0 AND congelada>0) celulas_em_ambas,sum(CASE WHEN congelada>0 THEN adicional ELSE 0 END) adicional_em_celula_anterior FROM reconciliacao GROUP BY ALL")
stats=ex("SELECT classe,sum(congelada),sum(adicional),sum(janela_estendida) FROM reconciliacao GROUP BY ALL ORDER BY ALL").fetchall()
print("confronto janela antiga",diff,"2024",stats,flush=True)
