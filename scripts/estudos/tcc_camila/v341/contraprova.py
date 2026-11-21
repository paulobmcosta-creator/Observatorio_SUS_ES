"""Contraprova direta nas chaves da edição certificada e leitura da persistência mensal."""
from comum import *
from temas import TEMAS
import numpy as np
w,v,base,src=paths();a=w/"A";b=w/"B";c=w/"C/Controles";c.mkdir(parents=True,exist_ok=True);(w/"C/TCC").mkdir(parents=True,exist_ok=True)
if src is None or not src.is_dir():raise ValueError("Forneça --integracao com os agregados anteriores")
con=duckdb.connect(); r=con.execute
ref=pd.read_csv(src/"seis_medidas_anuais.csv.gz").query("nivel!='Município'").copy()
ay=q(a/"pertencimento_anual.parquet"); mm=q(a/"pertencimento_mensal.parquet")
mapa=dict(universo="true",cadastrados="ST",vinculo_sus="SUS",com_recurso="COMP",com_pa="PA",com_sih="SIH",ambos_no_ano="PA AND SIH",ambos_no_mes="PA_SIH_MES")
test=[]
for name,expr in mapa.items():
    actual=r(f"SELECT ano::INT ano,territorio,count_if({expr})::INT calculado FROM {ay} GROUP BY ano,territorio").df().merge(ref[["ano","territorio",name]],on=["ano","territorio"],validate="one_to_one")
    assert len(actual)==55 and actual.calculado.eq(actual[name]).all()
    for x in actual.to_dict("records"):test.append(dict(fonte="seis_medidas_anuais_v34",ano=x["ano"],territorio=x["territorio"],medida=name,referencia=x[name],apurado=x["calculado"]))
# From the original long sources, construct V03 independently using DISTINCT intersections of provider identities.
f=lambda fname:csvrel(src/(fname+".csv.gz"))
origquery={
"A":f"SELECT DISTINCT cnes FROM {f('recursos_vigentes')} WHERE starts_with(mes,'2024') AND id='EQ_441_QT_USO' AND valor::DOUBLE>0",
"B":f"SELECT DISTINCT cnes FROM {f('servicos_e_classes')} WHERE starts_with(mes,'2024') AND SERV_ESP='122' AND CLASS_SR='003'",
"C":f"SELECT DISTINCT cnes FROM {f('PA_detalhe_janela_original')} WHERE starts_with(mes,'2024') AND classe='A' AND codigo='0211020036' AND aprovadas::BIGINT>0"}
for k,sql in origquery.items():r(f"CREATE TEMP TABLE fonte_{k} AS "+sql)
formula=pd.read_csv(b/"intersecoes_anuais.csv.gz",dtype={"padrao":str});tab=formula.query("tema=='V03' and ano==2024 and territorio=='ES'").set_index("padrao")
for pattern in tab.index:
    if pattern=="000":continue
    req=[x for x,bit in zip("ABC",pattern) if bit=="1"]
    n=r("SELECT count(*) FROM ("+" INTERSECT ".join(f"SELECT cnes FROM fonte_{k}" for k in req)+")").fetchone()[0]
    assert n==tab.loc[pattern,"inclusiva_anual"]
    test.append(dict(fonte="intersect_SQL_fontes_v34",ano=2024,territorio="ES",medida=pattern,referencia=n,apurado=tab.loc[pattern,"inclusiva_anual"]))
pd.DataFrame(test).to_csv(c/"controles_v34_e_fontes.csv",index=False)
# The change of universe for re-entry is explicit. Only compare months having a historically defined domain in both.
dom=pd.read_csv(a/"vigencia_mensal.csv",dtype={"mes":str}).pivot(index="mes",columns="conjunto",values="dominio_disponivel")
use=sorted(set().union(*(cols for _,cols in TEMAS.values()))|{"SR_CARD_SUS","SR126_004","LT_85_QT_EXIST","LT_86_QT_EXIST"})
spells=[];prior={};seen={};last=None
for m in dom.index:
    df=r("SELECT cnes,regiao,"+",".join(use)+f" FROM {mm} WHERE mes=?",[m]).df()
    for rg in ["ES","Norte","Central","Metropolitana","Sul"]:
        sub=df if rg=="ES" else df[df.regiao==rg]
        for var in use:
            key=(rg,var);curr=set(sub.loc[sub[var],"cnes"])
            if last is not None:
                prev=prior[key];historico=seen[key];valid=bool(dom.loc[m,var] and dom.loc[last,var])
                adds=curr-prev;lost=prev-curr;keep=curr&prev;back=adds&historico
                assert len(keep)+len(adds)==len(curr) and len(keep)+len(lost)==len(prev)
                spells.append((last,m,rg,var,valid,*([len(prev),len(curr),len(keep),len(adds),len(lost),len(back)] if valid else [None]*6)))
            prior[key]=curr;seen.setdefault(key,set()).update(curr)
    last=m
pd.DataFrame(spells,columns="mes_anterior mes_atual territorio conjunto dominio_comparavel anterior atual permaneceram entradas saidas reentradas_observadas".split()).to_csv(c/"persistencia_entre_competencias.csv.gz",index=False)
# All input flags observed, including the difference between actual specialized service and legacy composite flag.
service_diff=r(f"""SELECT left(mes,4) ano,count_if(SERV34 AND NOT SR_CARD) meses_cnes_servico_legado_sem_SR116,count_if(SR_CARD AND NOT SERV34) reverso FROM {mm} GROUP BY 1 ORDER BY 1""").df();service_diff.to_csv(c/"definicoes_de_servico.csv",index=False)
# A small, legible spreadsheet-compatible table with both denominator directions for named modalities.
pairs=pd.read_csv(b/"razoes_bidirecionais.csv.gz")
pick={"V01":[("COMP","PA")],"V02":[("SR_CARD","PA")],"V02S":[("SR_CARD_SUS","PA")],"V03":[("EQ_441_QT_USO","ECG"),("SR122_003","ECG")],"V03T":[("SR122_007","ECG")],"H01":[("HAB","SIH"),("LEITOS","SIH")],"F01":[("SR126_004","FISIO")],"D01":[("EQ_113_QT_USO","ECO")],"D02":[("EQ_110_QT_USO","CAT"),("SR116_005","CAT")]}
sel=[(theme,x,y) in {(t,i,j) for t,vals in pick.items() for i,j in vals} for theme,x,y in pairs[["tema","X","Y"]].itertuples(index=False,name=None)]
pairs[sel].to_csv(w/"C/TCC/modalidades_e_denominadores.csv",index=False)
save(c/"recibo_contraprova.json",dict(margens_anteriores=440,intersecoes_diretas_em_sql=7,transicoes_entre_competencias=len(spells),coincidencias_quadro=1000,perfis_nota=10))
print(len(test),"confrontos;",len(spells),"linhas de transição administrativa")
