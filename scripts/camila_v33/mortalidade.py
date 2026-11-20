"""Taxas municipais por sexo ou idade e comparador estrito padronizado pelos pesos censitários."""
from comum import *
from observatorio_sus.estudos.camila.sim import GRUPOS

def main():
    a=Acervo()
    cp=a.w/'checkpoint-B'
    t8=a.tabela('T08')
    geo=t8[['municipio','regiao']].drop_duplicates()
    partes=[]
    for ano in ANOS:
        pasta=a.v/f'estratos/{ano}'
        df=ler(a.fonte(pasta/'cardiovascular.csv',pasta))
        df['ano']=ano
        df['idade_inicio']=pd.to_numeric(df.faixa,errors='coerce').fillna(-1).astype(int)
        df['cid']=df.final.str[1:3].astype(int)
        for g,(lo,hi) in {'G0':(0,99),**GRUPOS}.items():
            linhas=df[df.cid.between(lo,hi)].groupby(['ano','municipio','sexo','idade_inicio'],as_index=False).obitos.sum()
            partes.append(linhas.assign(grupo=g))
    obs=pd.concat(partes).merge(geo,how='left',validate='many_to_one')
    obs['sexo']=obs.sexo.astype(str)
    marg=a.v/'taxas-ed2/margens_conjuntas.csv'
    den=ler(a.fonte(marg,marg.parent))
    igual(den.dem,den.popsvs,'margens demográficas')
    # Contagens por sexo e faixa separadamente, inclusive sexo/idade indeterminados, com denominador apenas nos estratos conhecidos.
    base=obs[obs.regiao.notna()].copy()
    grupo=['ano','municipio','grupo']
    tot=base.groupby(grupo,as_index=False).obitos.sum().assign(estrato='total',valor='T')
    sx=base.groupby(grupo+['sexo'],as_index=False).obitos.sum().rename(columns={'sexo':'valor'}).assign(estrato='sexo')
    age=base.groupby(grupo+['idade_inicio'],as_index=False).obitos.sum().rename(columns={'idade_inicio':'valor'}).assign(estrato='idade')
    counts=pd.concat([tot,sx,age],ignore_index=True)
    counts['valor']=counts.valor.astype(str)
    pop=den.assign(valor=np.where(den.dominio.eq('idade'),(den.estrato//5*5),den.estrato)).groupby(['ano','municipio','dominio','valor'],as_index=False).dem.sum().rename(columns={'dem':'habitantes','dominio':'estrato'})
    pop=pd.concat([pop,t8[['ano','municipio','habitantes']].assign(estrato='total',valor='T')],ignore_index=True)
    pop['valor']=pop.valor.astype(str)
    df=pop.merge(pd.DataFrame({'grupo':['G0',*GRUPOS]}),how='cross').merge(counts,on=grupo+['estrato','valor'],how='outer',validate='one_to_one')
    df.obitos=df.obitos.fillna(0).astype(int)
    df['taxa_100mil']=df.obitos*100000.0/df.habitantes.where(df.habitantes>0)
    df=df.merge(geo,validate='many_to_one')
    gravar(df.sort_values(grupo+['estrato','valor']),cp/'T26.csv.gz')
    check=df.query("grupo=='G0' and estrato=='total'").merge(t8,on=['ano','municipio'])
    igual(check.obitos_x,check.obitos_y,'mortalidade municipal G0')
    qualidade=df.query("estrato=='idade' and valor!='-1'").groupby(grupo,as_index=False).agg(estratos=('obitos','size'),estratos_zero=('obitos',lambda v:int(v.eq(0).sum())),estratos_1_a_4=('obitos',lambda v:int(v.between(1,4).sum())),menor_populacao=('habitantes','min'))
    gravar(qualidade,cp/'estabilidade_municipal.csv.gz')
    b1=a.tabela('B01')
    b2=a.tabela('B02')
    pesos=ler(a.fonte(a.v/'taxas-ed2/pesos.csv',a.v/'taxas-ed2'))
    estr=b2[b2.territorio.isin(OUTRAS)].groupby(['ano','grupo','sexo_sim','idade_inicio'])[['obitos','habitantes']].sum(min_count=3).reset_index()
    # Confronte as contagens estritas contra as causas municipais, por sexo, idade e grupo.
    prim=base[base.regiao.isin(OUTRAS)]
    prim=pd.concat([prim,prim.assign(sexo='T')])
    pi=prim[prim.idade_inicio>=0].groupby(['ano','grupo','sexo','idade_inicio']).obitos.sum()
    ix=estr.set_index(['ano','grupo','sexo_sim','idade_inicio']).sort_index()
    igual(ix.obitos,pi.reindex(ix.index,fill_value=0),'estratos estritos SIM')
    linhas=[]
    for (ano,g,s),sub in estr.groupby(['ano','grupo','sexo_sim']):
        for univ in (['todas','30-69'] if g=='G0' else ['todas']):
            e=sub if univ=='todas' else sub[sub.idade_inicio.between(30,65)]
            raw=b1[(b1.ano==ano)&(b1.grupo==g)&(b1.sexo_sim==s)&(b1.censo==2022)&(b1.universo==univ)&b1.territorio.isin(OUTRAS)]
            n=raw.obitos.sum()
            d=e.habitantes.sum(min_count=len(e))
            ig=n-e.obitos.sum()
            for c,pc in pesos.groupby('censo'):
                j=e.merge(pc,on='idade_inicio',validate='one_to_one')
                w=j['peso_todas' if univ=='todas' else 'peso_30_69']
                igual(w.sum(),1,'pesos')
                direta=(w*j.obitos/j.habitantes*100000).sum(min_count=len(j))
                linhas.append((ano,ESTRITO,s,g,univ,c,n,ig,d,n*100000.0/d if d>0 else None,direta))
    tab=pd.DataFrame(linhas,columns=b1.columns)
    out=pd.concat([b1,tab],ignore_index=True)
    gravar(out,cp/'T25.csv.gz')
    t9=a.tabela('T09').set_index('ano')
    dif=out.query("universo=='todas' and grupo=='G0' and sexo_sim=='T' and censo==2022").pivot(index='ano',columns='territorio',values='obitos')
    igual(dif[COMP]-dif[ESTRITO],t9.obitos_sem_municipio,'resíduo municipal')
    b3=a.tabela('B03')
    fatos=['i50_final','i50_original','ampliada','mencao_linhas','mencao_atestado','mencao_uniao']
    b3=pd.concat([b3,b3[b3.territorio.isin(OUTRAS)].groupby('ano',as_index=False)[fatos].sum(min_count=3).assign(territorio=ESTRITO)])
    pops=out.query("sexo_sim=='T' and grupo=='G0' and universo=='todas' and censo==2022")[['ano','territorio','habitantes']]
    ind=b3.melt(id_vars=['ano','territorio'],value_vars=fatos,var_name='conceito',value_name='obitos').merge(pops,on=['ano','territorio'],how='left',validate='many_to_one')
    ind['taxa_100mil']=ind.obitos*100000.0/ind.habitantes
    gravar(ind,cp/'T27.csv')
    gravar(pd.DataFrame([(str(p.relative_to(a.p)),h) for p,h in a.fontes.items()],columns=['fonte','sha256']),cp/'fontes_sim.csv')
    print('T25–27',len(out),len(df),len(ind))
if __name__=='__main__': main()
