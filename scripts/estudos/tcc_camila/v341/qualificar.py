"""Verificar as fontes seladas e construir matrizes de pertencimento sem reler microdados."""
from comum import *
import argparse,zipfile
parser=argparse.ArgumentParser()
parser.add_argument("manifesto",type=Path)
manifest=parser.parse_args().manifesto.resolve()
roles=json.loads(manifest.read_text(encoding="utf-8-sig"))
def role(n):return (manifest.parent/roles[n]).resolve()
w=role("trabalho");v=role("edicao_v34");base=role("academico_v34");i=role("integracao");out=w/"A";out.mkdir(parents=True,exist_ok=True)
receipts=json.loads((v/"recibo_final_v34.json").read_text(encoding="utf8"))
sources={}
for name,r in receipts.items():
    z=v/(name+".zip");assert sha(z)==r["sha256"]
    with zipfile.ZipFile(z) as f:
        fmanifest=f.read("MANIFESTO_SHA256_v34.csv");assert fmanifest==(v/name/"MANIFESTO_SHA256_v34.csv").read_bytes()
        assert len(f.namelist())==r["arquivos_conferidos"]
        for row in csv.DictReader(fmanifest.decode("utf8").splitlines()):
            assert sha(v/name/row["arquivo"])==row["sha256"],row["arquivo"]
    sources[name]=r
for key in ("quadro_denominadores","nota_referencia","mandato_referencia"):
    sources[key]=sha(role(key))
hist=role("historico_sigtap"); hs=hist/"servicos.csv.gz"
assert json.loads((hist/"recibo.json").read_text())["saidas"][hs.name]==sha(hs)
sources["dominio_SIGTAP_servicos"]=sha(hs)
con=duckdb.connect();con.execute("SET threads=2");con.execute("SET memory_limit='1400MB'")
for name,file in {"m":i/"C_cadastro_producao_integrada.csv.gz","r":i/"recursos_vigentes.csv.gz","s":i/"servicos_e_classes.csv.gz","p":i/"PA_detalhe_janela_original.csv.gz"}.items():
    con.execute(f"CREATE TABLE {name} AS FROM {csvrel(file)}")
n,unicos,meses,invalid,fora=con.execute("""SELECT count(*),count(distinct(mes,cnes)),count(distinct mes),count_if(NOT regexp_full_match(cnes,'[0-9]{7}') OR cnes='0000000' OR cnes IS NULL),count_if(NOT cadastrado::BOOL) FROM m""").fetchone()
assert n==unicos==950730 and meses==132 and not invalid
reg=con.execute("SELECT DISTINCT regiao FROM m ORDER BY 1").fetchnumpy()["regiao"].tolist()
assert set(reg)=={"Metropolitana","Norte","Sul","Central"}
for table in ["r","s","p"]:
    orphans=con.execute(f"SELECT count(*) FROM {table} t ANTI JOIN m ON t.mes=m.mes AND t.cnes=m.cnes AND t.municipio=m.municipio").fetchone()[0];assert not orphans,table
calendar=sorted(x[0] for x in con.execute("SELECT DISTINCT mes FROM m").fetchall())
domain=pd.read_csv(hs,dtype=str)
stock=role("estoques_regionais")
assert sha(stock)==json.loads(stock.with_name("recibo.json").read_text())["saidas"][stock.name]
sources["estoques_incluindo_UCO_provisorios"]=sha(stock)
b06=pd.read_csv(stock,dtype={"mes":str});b06=b06[b06.territorio=="ES"]
catalog=pd.read_csv(i/"dicionario_recursos.csv",dtype=str,keep_default_na=False)
proced=pd.read_csv(base/"07_DOCUMENTACAO_METODOLOGICA/procedimentos.csv.gz",dtype=str,keep_default_na=False)
spec=proced[proced.classe.isin(["A","B"]) & proced.presente.eq("1")].copy()
defs={};parts={k:[] for k in ["m","r","s","p"]};vig={}
def add(id,label,table,rule,obs="",domain_months=None):
    defs[id]=dict(conjunto=id,nome=label,fonte=table,criterio=rule,limite=obs or "Presença observada no recorte homologado.")
    parts[table].append((id,rule));vig[id]=set(calendar if domain_months is None else domain_months)
for id,label,rule in [
 ("ST","Cadastro no CNES","cadastrado::BOOL"),("SUS","Vínculo SUS","VINC_SUS='1'"),("COMP","Recurso composto v3.4","recurso_especifico::BOOL"),("SERV34","Serviço no algoritmo v3.4","servico::BOOL"),("ESTH","Estrutura hospitalar v3.4","estrutura_hosp::BOOL"),("HAB","Habilitação cardiovascular selecionada","habilitacao::BOOL"),("PA","Produção PA específica","tem_pa::BOOL"),("SIH","AIHs cardiovasculares","tem_sih::BOOL"),("CTX","Produção PA contextual","contextuais::BIGINT>0")]:
    add(id,label,"m",rule)
defs["COMP"]["limite"]="União deduplicada de SR116, SR140/014, LT02/LT32 existentes, habilitações do catálogo e vínculos CBO 225120/225210/225203. Equipamentos têm conjuntos próprios."
defs["SERV34"]["limite"]="Inclui SR116 e SR140/014 no algoritmo legado. A série SR_CARD isola SR116."
for row in catalog.itertuples():
    id=row.id
    if id.startswith("HB_") or id in ("SR_CARD","SR_CARD_SUS") or (id.startswith("LT_") and id.split("_")[1] in {"02","32","85","86"}) or (id.startswith("EQ_") and (id.endswith("_QT_USO") or id=="EQ_441_SUS")) or (id.startswith("PF_") and ("vinculos" in id)):
        good=b06[b06.id.eq(id)&b06.valor.notna()].mes
        add(id,row.titulo,"r",f"id='{id}' AND valor::DOUBLE>0",row.status+". "+row.limitacao,good)
def code_set(id,label,selection,rule,limit=""):
    avail=domain.loc[selection,"competencia"];add(id,label,"s",rule,limit,avail)
for serv,cl in [("122","003"),("122","007"),("140","014"),("126","004"),("162","005")]:
    sel=domain.servico.eq(serv)&domain.classificacao.eq(cl);label=domain.loc[sel,"descricao_classe"].iloc[-1]
    code_set(f"SR{serv}_{cl}",label,sel,f"SERV_ESP='{serv}' AND CLASS_SR='{cl}'","Contextual composto" if serv=="126" else "Provisório para inferência longitudinal" if serv=="162" else "Classificação específica do serviço no cadastro.")
for cl in sorted(domain[domain.servico.eq("116")].classificacao.unique()):
    sel=domain.servico.eq("116")&domain.classificacao.eq(cl);label=domain.loc[sel,"descricao_classe"].iloc[-1]
    for suffix,pred in [("",""),("_SUS"," AND AMB_SUS='1'")]:
        code_set("SR116_"+cl+suffix,label+(" (ambulatório SUS)" if suffix else ""),sel,f"SERV_ESP='116' AND CLASS_SR='{cl}'"+pred)
for id,label,rule in [
    ("ECG","ECG aprovado","classe='A' AND codigo='0211020036'"),("OUTRO_PA","Específicos além do ECG","classe='A' AND codigo<>'0211020036'"),
    ("ECO","Ecocardiografia transtorácica aprovada","classe='A' AND codigo='0205010032'"),("CAT","Cateterismo cardíaco aprovado","classe='A' AND codigo='0211020010'"),
    ("FISIO","Fisioterapia cardiovascular específica","classe='A' AND grupo_clinico='fisioterapia_especifica'"),
    ("DOP","Doppler vascular contextual","classe='B' AND grupo_clinico='doppler_contextual'"),("CONS","Consulta por CBO contextual","classe='B' AND grupo_clinico='consulta_cbo'")]:
    add(id,label,"p",rule+" AND aprovadas::BIGINT>0")
for code in sorted(spec.codigo.unique()):
    sel=spec[spec.codigo==code];months=sel[sel.registro.str.split().map(lambda x:bool(set(x)&{"01","02","06","07","08","09"}))].competencia
    add("P"+code,sel.descricao.iloc[-1],"p",f"codigo='{code}' AND aprovadas::BIGINT>0","Código oficial, elegibilidade por competência e instrumento.",months)
for k in "CIPS":add("INSTR_"+k,"PA específico no instrumento "+k,"p",f"classe='A' AND instrumento='{k}' AND aprovadas::BIGINT>0")
for table in ["r","s","p"]:
    expr=", ".join(f"bool_or(coalesce(({rule}),false)) AS {id}" for id,rule in parts[table])
    con.execute(f"CREATE TABLE flag_{table} AS SELECT mes,cnes,{expr} FROM {table} GROUP BY mes,cnes")
expr=[f"coalesce(({rule}),false) AS {id}" for id,rule in parts["m"]]
expr += [f"coalesce(flag_{table}.{id},false) AS {id}" for table in ["r","s","p"] for id,rule in parts[table]]
con.execute("CREATE TABLE flags AS SELECT m.mes,m.cnes,m.municipio,m.regiao,"+",".join(expr)+" FROM m LEFT JOIN flag_r USING(mes,cnes) LEFT JOIN flag_s USING(mes,cnes) LEFT JOIN flag_p USING(mes,cnes)")
deriv={"LEITOS":("Leito clínico ou cirúrgico de cardiologia","LT_02_QT_EXIST OR LT_32_QT_EXIST"),"PROF":("Vínculo profissional do catálogo","PF_225120_vinculos OR PF_225210_vinculos OR PF_225203_vinculos"),"ECG_SERV":("Exame eletrocardiográfico convencional ou por telemedicina","SR122_003 OR SR122_007"),"PA_SIH_MES":("Produção nos dois sistemas no mês","PA AND SIH")}
for id,(l,rule) in deriv.items():defs[id]=dict(conjunto=id,nome=l,fonte="derivado",criterio=rule,limite="Presença na mesma competência administrativa.");vig[id]=set(calendar)
extra=",".join(f"({rule}) AS {id}" for id,(_,rule) in deriv.items())
con.execute("CREATE TABLE mes AS SELECT *,"+extra+" FROM flags")
ids=list(defs)
assert con.execute("SELECT count(*) FROM mes WHERE PA<>(ECG OR OUTRO_PA) OR (SR_CARD_SUS AND NOT SR_CARD) OR PA_SIH_MES<>(PA AND SIH)").fetchone()[0]==0
def export(table,name):
    con.execute(f"COPY ({table}) TO {q(out/(name+'.parquet'))} (FORMAT PARQUET, COMPRESSION ZSTD)")
annual=",".join(f"bool_or({id}) AS {id}" for id in ids)
# Territorial and state annual membership are calculated independently for providers changing location.
con.execute(f"""CREATE TABLE ano AS WITH loc AS (SELECT *,regiao territorio FROM mes UNION ALL SELECT *,'ES' territorio FROM mes)
 SELECT left(mes,4) ano,territorio,cnes,string_agg(DISTINCT municipio,'|' ORDER BY municipio) municipios_observados,count(*) meses_no_universo,{annual} FROM loc GROUP BY 1,2,3""")
export("SELECT * FROM mes ORDER BY mes,cnes","pertencimento_mensal")
export("SELECT * FROM ano ORDER BY ano,territorio,cnes","pertencimento_anual")
source_names={"m":"C_cadastro_producao_integrada","r":"recursos_vigentes","s":"servicos_e_classes","p":"PA_detalhe_janela_original","derivado":"pertencimento_mensal"}
for d in defs.values():d["fonte"]=source_names[d["fonte"]]
csvfile(out/"dicionario_conjuntos.csv",list(defs.values()))
csvfile(out/"vigencia_mensal.csv",[dict(mes=m,conjunto=k,dominio_disponivel=m in vs) for k,vs in vig.items() for m in calendar])
# Independent check on each reference denominator, including same-month coincidences.
ind=pd.read_csv(role("quadro_denominadores"),dtype={"universo":str})
names=list(ind[ind.regiao=="ES"].universo)
mapping=dict(zip(names[:11],["ST","SUS","COMP","SERV34","PA","CTX","ESTH","HAB","SIH","SR_CARD","SR_CARD_SUS"]))
for name in names[11:]:mapping[name]=name.replace("SR ","SR").replace("/","_")
checks=[]
for k,id in mapping.items():
    z=con.execute(f"""WITH x AS (SELECT cnes,territorio,bool_or({id}) a,bool_or(pa) b,bool_or(sih) c,bool_or({id} AND pa) ab,bool_or({id} AND sih) ac FROM (SELECT *,regiao territorio FROM mes WHERE mes>='202401' UNION ALL SELECT *,'ES' territorio FROM mes WHERE mes>='202401') GROUP BY cnes,territorio)
    SELECT territorio,count_if(a),count_if(a AND b),count_if(a AND c),count_if(a AND (b OR c)),count_if(a AND b AND c),count_if(ab),count_if(ac) FROM x GROUP BY territorio""").fetchall()
    for territory,*values in z:
        ref=ind[(ind.universo==k)&(ind.regiao==territory)].iloc[0]
        pct=round(100*values[1]/values[0],2) if values[0] else None
        for col,new in zip(ind.columns[3:],values+[pct]):
            old=ref[col];ok=(pd.isna(old) and new is None) or (pd.notna(old) and new==old)
            checks.append(dict(universo=k,regiao=territory,medida=col,independente=old,calculado=new,igual=ok))
csvfile(out/"confronto_quadro_2024.csv",checks)
assert len(checks)==1000 and all(x["igual"] for x in checks),[x for x in checks if not x["igual"]][:4]
profile={"produtores_ecg":("ECG",176),"somente_ecg":("ECG AND NOT OUTRO_PA",122),"demais_especificos":("OUTRO_PA",86),"ECG_e_demais":("ECG AND OUTRO_PA",54),"demais_sem_ECG":("OUTRO_PA AND NOT ECG",32),"ECG_com_servico":("ECG AND SR122_003",146),"ECG_com_equipamento":("ECG AND EQ_441_QT_USO",159),"PA_sem_SR116":("PA AND NOT SR_CARD",176),"PA_sem_composto":("PA AND NOT COMP",97),"PA_sem_composto_com_equipamento":("PA AND NOT COMP AND EQ_441_QT_USO",71)}
reports=[]
for k,(rule,ref) in profile.items():
    val=con.execute(f"SELECT count_if({rule}) FROM ano WHERE ano='2024' AND territorio='ES'").fetchone()[0]; reports.append(dict(medida=k,criterio=rule,nota=ref,apurado=val,igual=ref==val))
assert all(r["igual"] for r in reports);csvfile(out/"confronto_nota_2024.csv",reports)
csvfile(out/"cardinalidades_2024.csv",[dict(territorio=t,conjunto=id,cnes=int(n)) for t,*vals in con.execute("SELECT territorio,"+",".join(f"count_if({id})" for id in ids)+" FROM ano WHERE ano='2024' GROUP BY territorio ORDER BY territorio").fetchall() for id,n in zip(ids,vals)])
save(out/"proveniencia.json",dict(referencias=sources,municipios=con.execute("SELECT count(DISTINCT municipio) FROM mes").fetchone()[0],nao_cadastrados=fora))
txt(out/"viabilidade_e_escolhas.md","""# Domínios, unidade e seleção das figuras

A unidade é o estabelecimento de atendimento no Espírito Santo, identificado pelo CNES de sete dígitos. O universo é a união de chaves válidas da matriz integrada v3.4. A matriz mensal guarda município e região do prestador. A anual guarda, em cada território, todos os municípios observados. A linha estadual deduplica novamente os CNES. A competência do cadastro, a de produção do PA e a de processamento do SIH definem o encontro administrativo. Usou-se a janela congelada da matriz v3.4, incluindo para 2024.

V01 retoma o algoritmo composto. V02 isola o serviço SR116. V03 examina equipamento em uso, serviço convencional SR122/003 e ECG aprovado. A telemedicina 122/007 tem recorte paralelo e união própria. Uma inclusão comprovada no cadastro SUS admite Euler. UpSet por tema distingue especialização, recursos hospitalares, ECG e instrumentos. Séries anuais e mapas de calor preservam comparabilidade no período e dão visibilidade à Região Norte.

A tabela de vigência acompanha os indicadores booleanos. Falso significa ausência de presença positiva nos agregados elegíveis observados. Antes de interpretar um zero, conferir o domínio do mês. UCO permanece provisória. A classificação 126/004 inclui fisioterapia cardiovascular e pneumo-funcional. O Doppler colorido EQ_113 é equipamento compartilhável. A edição homologada não identifica separadamente um aparelho de uso exclusivo para ecocardiografia. Confronta-se esse recurso contextual com o procedimento específico ECO. O aparelho EQ_110 e a classificação SR116/005 têm séries próprias para hemodinâmica. Não se atribuiu especialidade por inferência. Ver dicionário e domínio histórico de cada conjunto.""")
sello(out,"checkpoint_A.json",competencias=meses,estabelecimento_meses=n,conjuntos=len(ids),linhas_quadro=125,campos_conferidos=1000,perfis_nota=len(profile))
print(n,len(ids),len(checks),"diferenças zero",flush=True)
