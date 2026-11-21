"""Analisar as matrizes certificadas por período e território, incluindo permanências e saídas."""
from comum import *
from conjuntos import codificar,contagens,alguma_competencia
from temas import TEMAS
from collections import Counter
import numpy as np

w,v,base,src=paths(); a=w/"A";out=w/"B";out.mkdir(exist_ok=True)
proof=json.loads((a/"checkpoint_A.json").read_text(encoding="utf8"))
for name,h in proof["arquivos"].items(): assert sha(a/name)==h
con=duckdb.connect();source=q(a/"pertencimento_mensal.parquet");year_source=q(a/"pertencimento_anual.parquet")
con.execute("SET threads=2")
labels=pd.read_csv(a/"dicionario_conjuntos.csv").set_index("conjunto").nome.to_dict()
vig=pd.read_csv(a/"vigencia_mensal.csv",dtype={"mes":str}).pivot(index="mes",columns="conjunto",values="dominio_disponivel")
temas=dict(TEMAS)
for key in labels:
    if key.startswith("SR116_"):temas[key]=("Classificação SR116 e produção", [key,"PA","SIH"])
sets=list(labels)
regions=["ES","Norte","Central","Metropolitana","Sul"]
catalog=[];parts=[];co=[];mg=[];trans=[];persistence=[];long_counts=[];cross=[];margins=[];totals=[];prev={};tests=Counter()
def ok(tag,condition):
    if not condition:raise ValueError(tag)
    tests[tag]+=1
def save_tab(name,rows,columns):
    pd.DataFrame.from_records(rows,columns=columns.split()).to_csv(out/name,index=False)
def tobits(m,k):return format(m,f"0{k}b")
for name,(title,cols) in temas.items():
    catalog.extend((name,title,j+1,id,labels[id]) for j,id in enumerate(cols))
save_tab("temas_e_ordem.csv",catalog,"tema titulo posicao conjunto definicao")
for year in range(2014,2025):
    df=con.execute(f"FROM {source} WHERE starts_with(mes,'{year}') ORDER BY mes,cnes").df()
    orig=con.execute(f"FROM {year_source} WHERE ano='{year}'").df()
    for rg in regions:
        x=df if rg=="ES" else df[df.regiao==rg];xn=x.cnes.to_numpy()
        ids,identity=np.unique(xn,return_inverse=True); n=len(ids)
        z=orig[orig.territorio==rg].set_index("cnes").loc[ids];ym=x.mes.to_numpy()
        months=sorted(set(ym)); starts=np.flatnonzero(np.r_[True,ym[1:]!=ym[:-1]]);bounds=np.r_[starts,len(x)]
        ok("12 competências territoriais",len(months)==12)
        # Independent annual direct cardinalities for all denominators; retention across adjacent years.
        for col in sets:
            flags=x[col].to_numpy(dtype=bool); present=z[col].to_numpy(dtype=bool); mult=np.bincount(identity[flags],minlength=n)
            ok("anual = presença mensal em pelo menos uma competência",np.array_equal(mult>0,present))
            count=int(present.sum()); valid=int(vig.loc[months,col].sum()); denom=n if valid else None
            long_counts.append((year,rg,col,n,valid,count if valid else None,100*count/n if valid else None))
            for k in range(1,13):persistence.append((year,rg,col,k,int((mult==k).sum()),valid))
            old=prev.get(("set",rg,col));current=set(ids[present])
            if old is not None:
                trans.append((year-1,year,rg,col,len(old&current),len(current-old),len(old-current),len(old),len(current)))
            prev[("set",rg,col)]=current
            for j,m in enumerate(months):
                cardinal=int(flags[bounds[j]:bounds[j+1]].sum());domain=bool(vig.loc[m,col])
                ok("presença exige domínio",domain or cardinal==0)
                mg.append((m,rg,col,bounds[j+1]-bounds[j],domain,cardinal if domain else None))
        for theme,(title,cols) in temas.items():
            k=len(cols); size=1<<k
            patterns=codificar(x[cols].to_numpy(dtype=bool)); annual=codificar(z[cols].to_numpy(dtype=bool))
            ex,inc=contagens(annual,k);ever,sim=alguma_competencia(identity,patterns,k,n)
            ok("partição anual, união e denominador",int(ex.sum())==n and inc[0]==n and ex[1:].sum()==n-ex[0])
            ok("inclusiva simultânea contida na anual",bool(np.all(sim<=inc)))
            # Independent exact expected counts by direct bool predicates on annual rows.
            domain_year=int(vig.loc[months,cols].all(axis=1).sum())
            for m in range(size):
                required=[j for j in range(k) if m&(1<<(k-1-j))]
                direct=int(z[cols].iloc[:,required].all(axis=1).sum()) if required else n
                ok("inclusão explícita anual em todas as combinações",direct==inc[m])
                parts.append((theme,year,rg,tobits(m,k),int(ex[m]),int(inc[m]),int(ever[m]),int(sim[m]),n,int(ex[1:].sum()),domain_year,100*ex[m]/n,100*inc[m]/n))
            totals.append((theme,year,rg,n,int(ex[1:].sum()),int(ex[0]),100*ex[1:].sum()/n))
            for j,month in enumerate(months):
                sub=patterns[bounds[j]:bounds[j+1]]; e,h=contagens(sub,k)
                ok("partição mensal e cardinalidade",int(e.sum())==len(sub) and h[0]==len(sub))
                for idx,col in enumerate(cols):
                    ok("margens mensais contra flags individuais",h[1<<(k-1-idx)]==int(x[col].iloc[bounds[j]:bounds[j+1]].sum()))
                for m in range(size):
                    co.append((theme,month,rg,tobits(m,k),int(e[m]),int(h[m]),len(sub),int(len(sub)-e[0]),bool(vig.loc[month,cols].all())))
            # Bidirectional percentages among providers, including same-month co-presence across the year.
            for l in range(k):
                for r in range(l+1,k):
                    lmask,rmask=1<<(k-1-l),1<<(k-1-r)
                    both=int(inc[lmask|rmask]);same=int(sim[lmask|rmask]);nx=int(inc[lmask]);ny=int(inc[rmask])
                    cross.append((theme,year,rg,cols[l],cols[r],nx,ny,both,same,100*both/nx if nx else None,100*both/ny if ny else None,100*same/nx if nx else None,100*same/ny if ny else None,domain_year))
            # Use an outer join so entry/exit from the territorial universe is explicit.
            key=(theme,rg); now=pd.Series(annual,index=ids,dtype="int16"); old=prev.get(key)
            if old is not None:
                paired=pd.concat([old.rename("anterior"),now.rename("atual")],axis=1).fillna(-1).astype(int)
                nb=paired.value_counts()
                ok("balanço transição universo anterior e atual",int((paired.anterior>=0).sum())==len(old) and int((paired.atual>=0).sum())==n)
                for (x0,x1),qtd in nb.items():margins.append((theme,year-1,year,rg,tobits(x0,k) if x0>=0 else "FORA",tobits(x1,k) if x1>=0 else "FORA",qtd))
            prev[key]=now
    print(year,flush=True)
save_tab("intersecoes_anuais.csv.gz",parts,"tema ano territorio padrao exclusiva_anual inclusiva_anual exata_em_algum_mes inclusiva_em_algum_mes universo uniao meses_dominio_conjunto pct_exclusiva_universo pct_inclusiva_universo")
save_tab("intersecoes_mensais.csv.gz",co,"tema mes territorio padrao exclusiva inclusiva universo uniao dominios_completos")
save_tab("unioes_anuais.csv",totals,"tema ano territorio universo uniao fora_dos_conjuntos pct_uniao_universo")
save_tab("razoes_bidirecionais.csv.gz",cross,"tema ano territorio X Y n_X n_Y ambos_ano ambos_mes pct_Y_entre_X pct_X_entre_Y pct_mes_entre_X pct_mes_entre_Y meses_dominio_conjunto")
save_tab("cardinalidades_anuais.csv.gz",long_counts,"ano territorio conjunto universo meses_dominio cnes pct_universo")
save_tab("cardinalidades_mensais.csv.gz",mg,"mes territorio conjunto universo dominio_disponivel cnes")
save_tab("transicoes_de_perfil.csv.gz",margins,"tema ano_anterior ano_atual territorio padrao_anterior padrao_atual cnes")
save_tab("entradas_saidas_dos_conjuntos.csv.gz",trans,"ano_anterior ano_atual territorio conjunto persistiram entraram sairam anterior atual")
save_tab("duracao_no_ano.csv.gz",persistence,"ano territorio conjunto meses_com_presenca cnes meses_dominio")
save_tab("controles_executados.csv",sorted(tests.items()),"controle verificacoes_aprovadas")
sello(out,"checkpoint_B.json",temas=len(temas),anos=11,territorios=5,controles=dict(tests),intersecoes_anuais=len(parts),intersecoes_mensais=len(co))
