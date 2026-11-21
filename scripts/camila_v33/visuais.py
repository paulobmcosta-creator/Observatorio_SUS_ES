"""Figuras com dados subjacentes, escalas por painel e mapa diretamente regional."""
import math
import sys
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colormaps
from matplotlib.colors import Normalize
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MPath
from matplotlib.ticker import MaxNLocator
from PIL import Image
from comum import *
PA='SIA/PA e SIGTAP histórico'
C='CNES e RIPSA'
H='SIH/RD nacional e RIPSA'
CORES=['#164e63','#bd5723','#357865','#76559a','#8c3048','#596d23']
CODIGOS={'0205010032':'Eco transtorácico','0208010025':'Perfusão em estresse','0208010033':'Perfusão em repouso','0211020010':'Cateterismo','0211020036':'Eletrocardiograma','0211020044':'Holter','0211020052':'MAPA','0211020060':'Teste ergométrico','0302040030':'Fisioterapia clínica','0302040048':'Fisioterapia cirúrgica','0302040064':'Fisioterapia em síndrome coronariana'}
def executar(a):
    cp=a.w/'checkpoint-B'
    pasta=a.e/'03_GRAFICOS/complementacao_v33'
    pasta.mkdir(parents=True,exist_ok=True)
    matplotlib.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'svg.hashsalt':'TCC33','svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
    reg=[]
    def acabar(fig,axlista,id,titulo,base,fonte,limite,pasta,pontos,unidade,periodo,ter):
        fig.suptitle(id+'  |  '+titulo,x=.06,y=.965,ha='left',fontsize=16,color='#173247')
        footer=f'{periodo} · {ter} · {unidade}\nFonte: {fonte} · Tabela {base} · Série descritiva validada no recorte indicado.\n{limite}'
        fig.text(.06,.035,footer,ha='left',va='bottom',fontsize=8,color='#273846')
        for ext in ('svg','png'):
            fig.savefig(pasta/(id+'.'+ext),dpi=146,metadata={'Date':None} if ext=='svg' else None)
        plt.close(fig)
        gravar(pontos,pasta/(id+'.csv'))
        with Image.open(pasta/(id+'.png')) as img: img.verify()
        reg.append(dict(id=id,titulo=titulo,base=base,fonte=fonte,nota=limite,unidade=unidade,periodo=periodo,territorio=ter,caminho=(pasta/id).relative_to(a.e).as_posix()))
    def painel(id,df,titulo,base,fonte,limite,unidade,ter,periodo='2014–2024',x='ano',cols=2):
        paineis=list(dict.fromkeys(df.painel))
        n=math.ceil(len(paineis)/cols)
        fig,axes=plt.subplots(n,cols,squeeze=False,figsize=(12,2.25*n+2.1))
        fig.subplots_adjust(left=.083,right=.975,top=1-.87/fig.get_figheight(),bottom=1.0/fig.get_figheight(),hspace=.85,wspace=.29)
        for ax,p in zip(axes.flat,paineis):
            d=df[df.painel==p]
            for i,(serie,linha) in enumerate(d.groupby('serie',sort=True)):
                linha=linha.sort_values(x)
                ax.plot(linha[x],linha.valor,marker='o',markersize=2.6,lw=1.7,label=serie,color=CORES[i%len(CORES)])
            ax.set_title(p,fontsize=10,loc='left',fontweight='bold')
            ax.grid(axis='y',alpha=.2)
            ax.set_ylim(bottom=0)
            ax.xaxis.set_major_locator(MaxNLocator(integer=True,nbins=6))
            if d.serie.nunique()>1: ax.legend(fontsize=7,frameon=False,ncol=min(3,d.serie.nunique()),loc='best')
        for ax in list(axes.flat)[len(paineis):]: ax.axis('off')
        acabar(fig,axes,id,titulo,base,fonte,limite,pasta,df,unidade,periodo,ter)
    t22=ler(cp/'T22.csv.gz')
    names={'especificos':'Total específico','ECG':'Eletrocardiograma','demais_exames':'Demais exames específicos','fisioterapia':'Fisioterapia cardiovascular'}
    def pa(sel,col):
        q=sel[sel.modalidade.isin(names)].copy()
        return q.assign(painel=q.modalidade.map(names),valor=q[col],serie=q.territorio)[['ano','painel','serie','valor']]
    painel('F26',pa(t22[t22.territorio=='ES'],'aprovadas'),'Produção cardiovascular aprovada por modalidade','T22',PA,'Local do prestador. O total inclui os três componentes. Cada painel tem escala própria.','procedimentos','Espírito Santo')
    t21=ler(cp/'T21.csv.gz')
    c=t21[(t21.territorio=='ES')&t21.codigo.isin(CODIGOS)].copy()
    c['painel']=c.codigo+' · '+c.codigo.map(CODIGOS)
    painel('F27',c.assign(serie='ES',valor=c.aprovadas_12_meses)[['ano','painel','serie','valor']],'Procedimentos específicos por código','T21',PA,'Somente anos com 12 competências válidas. Cada código tem sua escala.','procedimentos aprovados','Espírito Santo',cols=3)
    painel('F28',pa(t22[t22.territorio.isin(REG)],'aprovadas_por_100mil'),'Densidade territorial da produção aprovada','T22',PA+' e RIPSA','Numerador pelo município do prestador. Denominador de residentes em cada região.','procedimentos por 100 mil habitantes','quatro Regiões de Saúde')
    c=ler(cp/'T23.csv.gz')
    recursos={'LT_32_QT_SUS':'Leitos clínicos de cardiologia SUS','LT_02_QT_SUS':'Leitos cirúrgicos de cardiologia SUS','EQ_441_QT_EXIST':'Eletrocardiógrafos cadastrados','PF_225120_vinculos':'Vínculos de cardiologistas'}
    q=c[c.id.isin(recursos)&(c.territorio=='ES')].copy()
    q=q.melt(id_vars=['ano','id'],value_vars=['media_anual_12_meses','estoque_dezembro'],var_name='serie',value_name='valor')
    q['serie']=q.serie.map({'media_anual_12_meses':'Média mensal','estoque_dezembro':'Dezembro'})
    painel('F29',q.assign(painel=q.id.map(recursos))[['ano','painel','serie','valor']],'Recursos cadastrados ao longo do ano e em dezembro','T23',C,'Leitos, equipamentos e vínculos são unidades distintas. O cadastro descreve o estoque declarado.','quantidade cadastrada','Espírito Santo')
    t30=ler(cp/'T30.csv.gz')
    q=t30[(t30.ano==2024)&(t30.sexo.isin(['F','M']))&(t30.territorio=='ES')&(t30.idade_inicio>=0)]
    grupos={'G0':'G0 · Circulatórias','G1':'G1 · Isquêmicas','G2':'G2 · Insuficiência cardíaca','G3':'G3 · Cerebrovasculares','G4':'G4 · Hipertensivas','G5':'G5 · Artérias, arteríolas e capilares'}
    painel('F30',q.assign(painel=q.grupo.map(grupos),valor=q.taxa_100mil,serie=q.sexo)[['idade_inicio','painel','valor','serie']],'AIHs por diagnóstico, sexo e início da faixa etária','T30',H,'Grupos quinquenais em anos. O ponto 80 representa 80 anos ou mais. Ano de processamento.','AIHs por 100 mil do estrato','residentes do Espírito Santo','2024','idade_inicio',3)
    t24=ler(cp/'T24.csv.gz')
    q=t24[t24.territorio.isin(REG)&(t24.sexo=='T')]
    painel('F31',q.assign(painel=q.grupo.map(grupos),valor=q.bruta_100mil,serie=q.territorio)[['ano','painel','serie','valor']],'Utilização hospitalar por diagnóstico e região de residência','T24',H,'AIHs principais em todas as UFs de atendimento. G0 inclui os grupos específicos.','AIHs por 100 mil habitantes','quatro Regiões de Saúde',cols=3)
    w=ler(cp/'T29.csv')
    q=w[w.territorio.isin(['Norte',ESTRITO])]
    campos={'sim_direta_2022':'Mortalidade padronizada · por 100 mil','sih_bruta_G0':'AIHs de residentes · por 100 mil','pa_aprovadas_por_100mil_especificos':'Procedimentos locais · por 100 mil','cnes_media_SR_CARD':'Serviço 116 · média mensal de estabelecimentos'}
    q=q.melt(id_vars=['ano','territorio'],value_vars=campos,var_name='campo',value_name='valor')
    painel('F32',q.assign(painel=q.campo.map(campos),serie=q.territorio)[['ano','painel','serie','valor']],'Norte e conjunto das demais regiões com território conhecido','T29','SIM, SIH, CNES, SIA/SIGTAP e RIPSA','Censo 2022 para mortalidade. Cada painel conserva sua unidade, tempo e critério territorial.','unidade indicada no painel','Região Norte e comparador estrito')
    q=w[w.territorio.isin(REG)].melt(id_vars=['ano','territorio'],value_vars=['evasao_aih','atracao_aih','interregional_es'],var_name='medida',value_name='valor')
    painel('F33',q.assign(serie=q.territorio,painel=q.medida.map({'evasao_aih':'Evasão interestadual','atracao_aih':'Atração interestadual','interregional_es':'Entre regiões conhecidas do ES, por residência'}))[['ano','painel','serie','valor']],'Fluxos hospitalares por Região de Saúde','T31','SIH/RD nacional','Evasão por residência. Atração pela região de atendimento. AIHs por processamento.','AIHs principais','quatro Regiões de Saúde')
    q=c[c.id.isin(recursos)&c.territorio.isin(REG)]
    painel('F34',q.assign(serie=q.territorio,painel=q.id.map(recursos),valor=q.media_anual_12_meses_por_100mil)[['ano','painel','serie','valor']],'Densidade dos recursos cadastrados por região','T23',C,'Média dos 12 estoques mensais. As unidades do numerador estão indicadas nos painéis.','unidades do recurso por 100 mil habitantes','quatro Regiões de Saúde')
    # Dissolução das geometrias do IBGE. O mapa acadêmico adota o enquadramento continental anterior.
    sys.path.insert(0,str(a.w/'bibliotecas'))
    from shapely.geometry import shape, mapping
    from shapely.ops import unary_union
    from shapely import normalize
    malha=a.p/'mandato-v3.2/fontes/municipios-es.geojson'
    geo=a.tabela('T08').query('ano==2024').set_index('chave').regiao
    feats=json.loads(malha.read_text(encoding='utf8'))['features']
    assert len(feats)==78 and {str(f['properties']['codarea']) for f in feats}==set(geo.index)
    geometria={r:normalize(unary_union([shape(f['geometry']) for f in feats if geo[str(f['properties']['codarea'])]==r])) for r in REG}
    assert all(g.is_valid and g.area>0 for g in geometria.values())
    assert abs(sum(g.area for g in geometria.values())-unary_union(list(geometria.values())).area)<1e-8
    mapa=a.e/'04_MAPAS_E_FLUXOS'
    dados=c.query("id=='LT_32_QT_SUS' and ano==2024 and territorio in @REG")[['territorio','media_anual_12_meses_por_100mil']].rename(columns={'territorio':'regiao','media_anual_12_meses_por_100mil':'valor'}).sort_values('regiao')
    old=a.tabela('M02')[['regiao','valor']].drop_duplicates().sort_values('regiao')
    igual(dados.valor,old.valor,'M02 taxas regionais')
    json_out(mapa/'M02_regioes.geojson',dict(type='FeatureCollection',features=[dict(type='Feature',properties={'regiao':r},geometry=mapping(geometria[r])) for r in REG]))
    fig,axes=plt.subplots(1,2,figsize=(9,6),gridspec_kw={'width_ratios':[3,2]})
    fig.subplots_adjust(top=.85,bottom=.21,right=.93,left=.08)
    for ax in axes: ax.axis('off')
    norm=Normalize(0,dados.valor.max()*1.03)
    for i,row in enumerate(dados.itertuples()):
        color=colormaps['Blues'](.18+.74*norm(row.valor))
        geom=geometria[row.regiao]
        for poly in getattr(geom,'geoms',[geom]):
            for ring in [poly.exterior,*poly.interiors]:
                ar=np.array(ring.coords)
                axes[0].fill(ar[:,0],ar[:,1],color=color if ring==poly.exterior else 'white',edgecolor='#466077',linewidth=.4)
        axes[1].text(.08,.84-i*.18,f'{row.regiao}   {row.valor:.2f}'.replace('.',','),transform=axes[1].transAxes,fontsize=13,bbox={'facecolor':color,'alpha':.8,'edgecolor':'none','pad':5})
    axes[0].set_xlim(-42.05,-39.55);axes[0].set_ylim(-21.45,-17.82);axes[0].set_aspect(1/np.cos(np.deg2rad(20)))
    acabar(fig,axes,'M02','Leitos clínicos de cardiologia SUS por região','T23',C+' e malha IBGE','Média mensal de 2024. Polígonos regionais por dissolução da malha municipal. Enquadramento continental.',mapa,dados,'leitos por 100 mil habitantes','2024','quatro Regiões de Saúde')
    return pd.DataFrame(reg)
