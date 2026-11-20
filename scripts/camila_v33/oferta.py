"""Densidades ecológicas de produção e estoques com controles mensais de elegibilidade."""
from comum import *

def somar_regioes(df,keys,valores):
    orig=df[df.territorio.isin(OUTRAS)]
    g=orig.groupby(keys,dropna=False)[valores].sum(min_count=3).reset_index()
    g['territorio']=COMP
    es=df[df.territorio=='ES'].set_index(keys)[valores].sort_index()
    norte=df[df.territorio=='Norte'].set_index(keys)[valores].sort_index()
    igual((es-norte).values,g.set_index(keys)[valores].sort_index().values,'comparador mensal por três regiões')
    return pd.concat([df,g],ignore_index=True)

def main():
    a=Acervo()
    dest=a.w/'checkpoint-B'
    t8=a.tabela('T08')
    mun=t8[['ano','municipio','regiao','habitantes']].rename(columns={'municipio':'territorio'})
    popreg=a.tabela('T10')[['ano','territorio','habitantes']]
    pop=pd.concat([mun.drop(columns='regiao'),popreg])
    geo=mun[['territorio','regiao']].drop_duplicates()
    pc=a.tabela('B07')
    pc['ano']=pc.competencia//100
    campos=['aprovadas','apresentadas']
    keys=['competencia','codigo','grupo_clinico']
    assert not pc.duplicated(keys+['territorio']).any()
    regio=somar_regioes(pc[keys+['territorio']+campos],keys,campos)
    assert pc.loc[pc.estado!='validado',campos].isna().all().all()
    eleg=pc[pc.territorio=='ES'][keys+['estado']]
    tm=pd.concat([a.tabela('T12'),a.tabela('T16')]).rename(columns={'municipio':'territorio'})
    assert not tm.duplicated(keys+['territorio']).any()
    controle=ler(a.fonte(a.et/'controle_pa_mensal.csv',a.et))
    assert len(controle)==132 and controle.filter(regex='^diferenca').eq(0).all().all()
    grade=eleg.merge(geo,how='cross').merge(tm[keys+['territorio']+campos],how='left',on=keys+['territorio'],validate='one_to_one')
    # Comprove a exaustividade por região, código, competência e pelos dois campos.
    observed=grade.groupby(keys+['regiao'])[campos].sum().sort_index()
    expected=pc[pc.territorio.isin(REG)].set_index(keys+['territorio'])[campos].sort_index()
    igual(observed.values,expected.fillna(0).values,'produção municipal vs. B07')
    assert list(observed.index)==list(expected.index)
    assert grade.loc[grade.estado!='validado',campos].isna().all().all()
    grade['tem_linha']=grade.aprovadas.notna()
    ok=grade.estado.eq('validado')
    grade.loc[ok,campos]=grade.loc[ok,campos].fillna(0)
    # Todos os municípios estão na malha e nas margens. Diferenciar ausência de linha e valor nulo registrado.
    cad=ler(a.fonte(a.et/'cadastro_estabelecimentos.csv.gz',a.et))
    cad=cad[cad.municipio=='320405'].groupby('mes').cnes.nunique().rename('estabelecimentos_cadastrados')
    privado=ler(a.fonte(a.et/'pa_municipal.csv.gz',a.et))
    espec=privado[privado.municipio=='320405'].groupby(['competencia','situacao']).size().unstack(fill_value=0)
    grade405=grade[grade.territorio=='320405'].groupby('competencia').agg(codigos_vigentes=('estado',lambda s:int((s=='validado').sum())),linhas_elegiveis=('tem_linha','sum')).join(cad).join(espec)
    assert len(grade405)==132 and grade405.estabelecimentos_cadastrados.gt(0).all()
    gravar(grade405.reset_index(),dest/'controle_320405.csv')
    regio['tem_linha']=regio.aprovadas.notna()
    allpa=pd.concat([regio,grade],ignore_index=True)
    allpa['ano']=allpa.competencia//100
    pa=allpa.groupby(['ano','territorio','codigo','grupo_clinico']).agg(meses_validos=('aprovadas','count'),meses_com_registro=('tem_linha','sum'),aprovadas=('aprovadas',lambda s:s.sum(min_count=1)),apresentadas=('apresentadas',lambda s:s.sum(min_count=1))).reset_index().merge(pop,validate='many_to_one')
    pa['aprovadas_12_meses']=pa.aprovadas.where(pa.meses_validos==12)
    pa['aprovadas_12_meses_por_100mil']=pa.aprovadas_12_meses*100000.0/pa.habitantes
    pa['situacao']=np.select([pa.meses_validos.eq(0),pa.meses_validos.lt(12),pa.aprovadas.eq(0)&pa.meses_com_registro.eq(0),pa.aprovadas.eq(0)],['não aplicável','vigência parcial','sem registro elegível na janela verificada','zero observado'],default='com produção aprovada')
    gravar(pa,dest/'T21.csv.gz')
    # Subtotais contam apenas códigos elegíveis em cada mês. A composição pode mudar dentro do ano.
    spec=allpa[allpa.grupo_clinico.isin(['exames_especificos','fisioterapia_especifica'])].copy()
    spec['modalidade']=np.select([spec.codigo.eq('0211020036'),spec.grupo_clinico.eq('fisioterapia_especifica')],['ECG','fisioterapia'],default='demais_exames')
    geral=spec.assign(modalidade='especificos')
    context=allpa[allpa.grupo_clinico.isin(['consulta_cbo','doppler_contextual'])].copy()
    context['modalidade']=context.grupo_clinico
    by=pd.concat([spec,geral,context]).groupby(['ano','competencia','territorio','modalidade'])[campos].sum(min_count=1).reset_index()
    membros=by.groupby(['ano','territorio','modalidade'])[campos].count()
    assert membros.eq(12).all().all()
    tab=by.groupby(['ano','territorio','modalidade'])[campos].sum().reset_index().merge(pop,validate='many_to_one')
    tab['aprovadas_por_100mil']=tab.aprovadas*100000.0/tab.habitantes
    chk=by[(by.modalidade=='especificos')&by.territorio.isin(['ES',*REG])].sort_values(['competencia','territorio'])
    t7=a.tabela('T07').query("grupo_clinico=='soma_especificos_elegiveis'").sort_values(['competencia','territorio'])
    igual(chk[campos],t7[campos],'660 margens específicas')
    gravar(tab,dest/'T22.csv.gz')
    # Série de estoques. Os 78 municípios preservam as lacunas do código histórico.
    b6=a.tabela('B06')
    local=a.tabela('T15').rename(columns={'municipio':'territorio'})
    resto=somar_regioes(b6,['mes','id'],['valor'])
    m=local.groupby(['mes','regiao','id']).valor.sum(min_count=1).sort_index()
    r=b6[b6.territorio.isin(REG)].set_index(['mes','territorio','id']).valor.sort_index()
    assert list(m.index)==list(r.index)
    igual(m,r,'estoques mensais municipal regional')
    cnes=pd.concat([resto,local],ignore_index=True)
    cnes['ano']=cnes.mes//100
    ch=['ano','territorio','id']
    anual=cnes.groupby(ch).valor.agg(meses_validos='count',media_meses_validos='mean').join(cnes[cnes.mes%100==12].set_index(ch).valor.rename('estoque_dezembro')).reset_index().merge(pop,validate='many_to_one')
    anual['media_anual_12_meses']=anual.media_meses_validos.where(anual.meses_validos.eq(12))
    for k in ['media_anual_12_meses','estoque_dezembro']: anual[k+'_por_100mil']=anual[k]*100000.0/anual.habitantes
    hist=anual.merge(a.tabela('T05'),on=ch)
    igual(hist.media_meses_validos,hist.media_mensal,'T05 média regional')
    gravar(anual,dest/'T23.csv.gz')
    t10=a.tabela('T10')
    n=anual.query("id=='SR_CARD'")[['ano','territorio','media_anual_12_meses','meses_validos']].merge(tab.query("modalidade=='especificos'")[['ano','territorio','aprovadas']])
    t10=t10.merge(n,on=['ano','territorio'],suffixes=('','_nova'),validate='one_to_one')
    for k,novo in [('estabelecimentos_sr116_media','media_anual_12_meses'),('meses','meses_validos'),('aprovadas','aprovadas_nova')]:
        s=t10[k].notna()
        igual(t10.loc[s,k],t10.loc[s,novo],k)
        t10[k]=t10[novo]
    t10=t10.drop(columns=['media_anual_12_meses','meses_validos','aprovadas_nova'])
    t10['sr116_por_100mil']=t10.estabelecimentos_sr116_media*100000.0/t10.habitantes
    t10['aprovadas_por_100mil']=t10.aprovadas*100000.0/t10.habitantes
    externo=ler(a.exp).sort_values(['ano','territorio'])
    t10=t10.sort_values(['ano','territorio'])
    assert list(zip(externo.ano,externo.territorio))==list(zip(t10.ano,t10.territorio))
    for k,ext in zip(['habitantes','obitos','bruta_100mil','direta_100mil','aih_residentes','utilizacao_bruta_100mil','padronizada_censo2022_100mil','estabelecimentos_sr116_media','sr116_por_100mil','aprovadas','aprovadas_por_100mil'],externo.columns[2:13]):
        igual(t10[k],externo[ext],'CSV exploratório '+ext)
    gravar(t10,dest/'T20.csv')
    gravar(pd.DataFrame([(p.name,h) for p,h in a.fontes.items()],columns=['insumo','sha256']),dest/'fontes_oferta.csv')
    print('T20–23',len(t10),len(pa),len(tab),len(anual))
if __name__=='__main__': main()
