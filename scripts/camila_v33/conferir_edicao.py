"""Contraprova célula a célula da matriz integrada, subjacentes e navegação da edição."""
import re
from xml.etree import ElementTree
from comum import *
from visuais import CODIGOS

def conferir(a,figs,inv):
    cp=a.w/'checkpoint-B'
    ts={k:ler(next(cp.glob(k+'.csv*'))) for k in ['T21','T22','T23','T24','T25','T29','T30','T31']}
    w=ts['T29']
    qs=[]
    def comparar(x,y):
        if not np.isclose(float(x),float(y),rtol=0,atol=1e-7,equal_nan=True):raise ValueError(f'Célula divergente {x}, {y}')
    cn=ts['T23'].set_index(['ano','territorio','id'])
    pa=ts['T22'].set_index(['ano','territorio','modalidade'])
    sim=ts['T25'].query("sexo_sim=='T' and censo==2022").set_index(['ano','territorio','grupo','universo'])
    sih=ts['T24'].query("sexo=='T'").set_index(['ano','territorio','grupo'])
    fl=ts['T31'].set_index(['ano','territorio'])
    for row in w.to_dict('records'):
        k=row['ano'],row['territorio']
        kl=k[0],(COMP if k[1]==ESTRITO else k[1])
        for col,num in row.items():
            if col in ['ano','territorio']:continue
            if col.startswith('cnes_media_'):
                v=np.nan if k[1]==COMP else cn.loc[(*kl,col.removeprefix('cnes_media_')),'media_anual_12_meses']
            elif col.startswith('pa_'):
                field=next(x for x in ['aprovadas_por_100mil','aprovadas','apresentadas'] if col.startswith('pa_'+x+'_'))
                mod=col.removeprefix('pa_'+field+'_')
                v=np.nan if k[1]==COMP else pa.loc[(*kl,mod),field]
            elif col in fl.columns:
                v=fl.loc[k,col]
            elif col.startswith('sih_'):
                v=sih.loc[(*k,'G0'),'direta_2022'] if col=='sih_direta_2022' else sih.loc[(*k,col[-2:]),'bruta_100mil']
            else:
                g=col[-2:] if '_G' in col else 'G0'
                u='30-69' if 'prematura' in col else 'todas'
                m='direta_100mil' if 'direta' in col else ('bruta_100mil' if 'bruta' in col else col)
                v=sim.loc[(*k,g,u),m]
            comparar(v,num)
    qs.append(('T29','células temáticas',len(w)*(len(w.columns)-2)))
    q21=ts['T21'].set_index(['ano','territorio','codigo'])
    q30=ts['T30'].set_index(['ano','territorio','sexo','idade_inicio','grupo'])
    q24=ts['T24'].set_index(['ano','territorio','sexo','grupo'])
    wide=w.set_index(['ano','territorio'])
    nomes={'Total específico':'especificos','Eletrocardiograma':'ECG','Demais exames específicos':'demais_exames','Fisioterapia cardiovascular':'fisioterapia'}
    recursos={'Leitos clínicos de cardiologia SUS':'LT_32_QT_SUS','Leitos cirúrgicos de cardiologia SUS':'LT_02_QT_SUS','Eletrocardiógrafos cadastrados':'EQ_441_QT_EXIST','Vínculos de cardiologistas':'PF_225120_vinculos'}
    for fig in figs.itertuples():
        path=a.e/fig.caminho
        df=ler(path.with_suffix('.csv'))
        svg=' '.join(ElementTree.parse(path.with_suffix('.svg')).getroot().itertext())
        for tag in [fig.id,fig.base,fig.fonte,fig.periodo,fig.unidade]:
            if tag not in svg: raise ValueError(f'{fig.id}: marcação ausente {tag}')
        for r in df.itertuples():
            fid=fig.id
            if fid in ['F26','F28']: v=pa.loc[(r.ano,r.serie,nomes[r.painel]),'aprovadas' if fid=='F26' else 'aprovadas_por_100mil']
            elif fid=='F27': v=q21.loc[(r.ano,'ES',r.painel[:10]),'aprovadas_12_meses']
            elif fid=='F29': v=cn.loc[(r.ano,'ES',recursos[r.painel]),'estoque_dezembro' if r.serie=='Dezembro' else 'media_anual_12_meses']
            elif fid=='F30': v=q30.loc[(2024,'ES',r.serie,r.idade_inicio,r.painel[:2]),'taxa_100mil']
            elif fid=='F31': v=q24.loc[(r.ano,r.serie,'T',r.painel[:2]),'bruta_100mil']
            elif fid=='F32':
                col={'Mortalidade':'sim_direta_2022','AIHs':'sih_bruta_G0','Procedimentos':'pa_aprovadas_por_100mil_especificos','Serviço':'cnes_media_SR_CARD'}[r.painel.split()[0]]
                v=wide.loc[(r.ano,r.serie),col]
            elif fid=='F33':
                col={'Evasão':'evasao_aih','Atração':'atracao_aih','Entre':'interregional_es'}[r.painel.split()[0]]
                v=fl.loc[(r.ano,r.serie),col]
            elif fid=='F34':v=cn.loc[(r.ano,r.serie,recursos[r.painel]),'media_anual_12_meses_por_100mil']
            else:v=cn.loc[(2024,r.regiao,'LT_32_QT_SUS'),'media_anual_12_meses_por_100mil']
            comparar(r.valor,v)
        qs.append((fig.id,'valores da figura',len(df)))
    for row in inv.itertuples():
        for x in [row.tabela,row.figura]:
            if isinstance(x,str) and x and not (a.e/x).is_file():raise FileNotFoundError(x)
    idx=a.e/'00_LEIA_PRIMEIRO/indice_geral.md'
    for item in re.findall(r'\]\(([^)]+)\)',idx.read_text(encoding='utf8')):
        if not (idx.parent/item).is_file():raise FileNotFoundError(item)
    qs.append(('índice','produtos com destino verificado',len(inv)))
    return pd.DataFrame(qs,columns=['produto','controle','casos'])
