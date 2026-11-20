"""Concilia as AIHs de residentes e integra medidas anuais com unidades e âmbitos distintos."""
from comum import *

RECURSOS=['SR_CARD','HB_0801','LT_02_QT_EXIST','LT_02_QT_SUS','LT_32_QT_EXIST','LT_32_QT_SUS','EQ_441_QT_EXIST','PF_225120_vinculos','PF_225120_horas_amb']
def main():
    a=Acervo()
    cp=a.w/'checkpoint-B'
    dados=ler(cp/'estratos_sih.csv.gz')
    loc=dados.rename(columns={'regiao':'territorio'})
    areas=pd.concat([loc[loc.territorio.isin(REG)],loc.assign(territorio='ES'),loc[loc.territorio!='Norte'].assign(territorio=COMP),loc[loc.territorio.isin(OUTRAS)].assign(territorio=ESTRITO)])
    counts=pd.concat([areas,areas.assign(sexo='T')]).groupby(['ano','territorio','sexo','idade_inicio','grupo'],as_index=False).aih.sum()
    b5=a.tabela('B05')
    key=['ano','territorio','sexo','idade_inicio']
    extra=b5[b5.territorio.isin(OUTRAS)].groupby(['ano','sexo','idade_inicio'],as_index=False)[['habitantes','aih_residentes']].sum(min_count=3).assign(territorio=ESTRITO)
    b5=pd.concat([b5,extra],ignore_index=True)
    grid=b5[key+['habitantes','aih_residentes']].merge(pd.DataFrame({'grupo':['G0','G1','G2','G3','G4','G5']}),how='cross')
    per=grid.merge(counts,how='left',on=key+['grupo'],validate='one_to_one')
    assert len(counts.merge(grid,on=key+['grupo']))==len(counts)
    per.aih=per.aih.fillna(0).astype(int)
    g0=per[per.grupo=='G0']
    igual(g0.aih,g0.aih_residentes,'B05 G0 por estrato')
    per=per.drop(columns='aih_residentes')
    per['taxa_100mil']=per.aih*100000.0/per.habitantes
    gravar(per,cp/'T30.csv.gz')
    group=['ano','territorio','sexo','grupo']
    taxas=per.groupby(group).agg(aih=('aih','sum'),habitantes=('habitantes',lambda s:s.sum(min_count=1))).reset_index()
    taxas['bruta_100mil']=taxas.aih*100000.0/taxas.habitantes
    pesos=ler(a.v/'taxas-ed2/pesos.csv')
    sel=per[per.idade_inicio>=0].merge(pesos,on='idade_inicio')
    sel['ponderada']=sel.taxa_100mil*sel.peso_todas
    pad=sel.groupby(group+['censo']).ponderada.sum(min_count=17).unstack('censo').rename(columns={2022:'direta_2022',2010:'direta_2010'})
    taxas=taxas.join(pad,on=group)
    b9=a.tabela('B09')
    b9['ano']=b9.competencia//100
    gr=['ano','territorio','grupo']
    ref=b9.groupby(gr).aih.sum()
    ref=ref.reindex(taxas.query("sexo=='T' and territorio!=@ESTRITO").set_index(gr).index,fill_value=0)
    igual(ref,taxas.query("sexo=='T' and territorio!=@ESTRITO").aih,'B09 grupos todas UFs')
    hosp=taxas[taxas.grupo=='G0'].merge(a.tabela('B04'),on=group[:3],validate='one_to_one')
    for k,l in [('aih','aih_residentes'),('bruta_100mil','utilizacao_bruta_100mil'),('direta_2022','padronizada_censo2022_100mil'),('direta_2010','padronizada_censo2010_100mil')]: igual(hosp[k],hosp[l],l)
    gravar(taxas,cp/'T24.csv.gz')
    od=ler(cp/'T28.csv.gz')
    od['municipio_at']=od.municipio_at.astype(str)
    reses=od.municipio_res.str.startswith('32')
    ates=od.uf_atendimento.eq('ES')
    externos=od.regiao_res.eq('OUTRA_UF_CODIGO_PLAUSIVEL')
    def agrup(mask):
        return od[mask].groupby('ano').aih.sum().reindex(ANOS,fill_value=0)
    flux=[]
    for t in ['ES',*REG,COMP,ESTRITO]:
        if t=='ES':
            mora,atende=reses,ates
        elif t in REG:
            mora,atende=od.regiao_res.eq(t),ates&od.regiao_at.eq(t)
        else:
            mora=reses&(~od.regiao_res.eq('Norte') if t==COMP else od.regiao_res.isin(OUTRAS))
            atende=ates&(~od.regiao_at.eq('Norte') if t==COMP else od.regiao_at.isin(OUTRAS))
        amt=agrup(mora)
        at=agrup(atende)
        ev=agrup(mora&~ates)
        atr=agrup(atende&externos)
        inter=agrup(mora&ates&od.regiao_res.isin(REG)&od.regiao_at.isin(REG)&od.regiao_res.ne(od.regiao_at))
        flux.append(pd.DataFrame(dict(territorio=t,aih_residentes=amt,atendimento=at,evasao_aih=ev,atracao_aih=atr,interregional_es=inter,evasao_pct=100*ev/amt,atracao_pct=100*atr/at)).rename_axis('ano').reset_index())
    fl=pd.concat(flux,ignore_index=True)
    conferir=fl.query("territorio=='ES'").merge(a.tabela('T02'),on='ano')
    for k,l in [('evasao_aih_x','evasao_aih_y'),('atracao_aih_x','atracao_aih_y'),('interregional_es','interregional_intra_es')]:igual(conferir[k],conferir[l],l)
    gravar(fl,cp/'T31.csv')
    # Matriz ampla legível, com ligação às tabelas de maior granularidade.
    chave=['ano','territorio']
    mort=ler(cp/'T25.csv.gz').query("sexo_sim=='T' and censo==2022")
    sim=mort.query("grupo=='G0' and universo=='todas'")[chave+['habitantes','obitos','bruta_100mil','direta_100mil']].rename(columns={'bruta_100mil':'sim_bruta','direta_100mil':'sim_direta_2022'})
    sim=sim.merge(mort.query("universo=='30-69'")[chave+['direta_100mil']].rename(columns={'direta_100mil':'sim_prematura_direta_2022'}),on=chave)
    sim=sim.merge(mort.query("grupo!='G0' and universo=='todas'").pivot(index=chave,columns='grupo',values='bruta_100mil').add_prefix('sim_bruta_'),on=chave)
    sih=taxas.query("sexo=='T'").pivot(index=chave,columns='grupo',values='bruta_100mil').add_prefix('sih_bruta_')
    wide=sim.merge(sih,on=chave).merge(taxas.query("grupo=='G0' and sexo=='T'")[chave+['direta_2022']].rename(columns={'direta_2022':'sih_direta_2022'}),on=chave).merge(fl,on=chave)
    def local(tab):
        # Somente os municípios conhecidos entram na coluna de localização do prestador.
        return tab[tab.territorio.isin(['ES',*REG,COMP])].replace({'territorio':{COMP:ESTRITO}})
    cn=local(ler(cp/'T23.csv.gz')).query('id in @RECURSOS').pivot(index=chave,columns='id',values='media_anual_12_meses').add_prefix('cnes_media_')
    pa=local(ler(cp/'T22.csv.gz')).pivot(index=chave,columns='modalidade',values=['aprovadas','apresentadas','aprovadas_por_100mil'])
    pa.columns=['pa_'+k+'_'+m for k,m in pa.columns]
    wide=wide.merge(cn,on=chave,how='left').merge(pa,on=chave,how='left')
    assert len(wide)==77 and not wide.duplicated(chave).any()
    gravar(wide,cp/'T29.csv')
    gravar(wide.melt(id_vars=chave,var_name='indicador',value_name='valor'),cp/'T29_longa.csv.gz')
    print('T24,T30,T28,T29',len(taxas),len(per),len(od),wide.shape)
if __name__=='__main__':main()
