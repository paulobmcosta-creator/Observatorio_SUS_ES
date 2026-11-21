"""Exportar as figuras a partir das regiões exatas, com tabela e ficha verificáveis."""
from comum import *
from figuras_conjuntos import numero,venn3,upset,euler_aninhado,INK,BLUE,TEAL,ORANGE,GRAY,inclusiva
from temas import TEMAS
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from PIL import Image
import xml.etree.ElementTree as ET

w,v,base,src=paths();a=w/"A";b=w/"B";c=w/"C";c.mkdir(exist_ok=True)
data=pd.read_csv(b/"intersecoes_anuais.csv.gz",dtype={"padrao":str})
lookup=pd.read_csv(a/"dicionario_conjuntos.csv").set_index("conjunto")
short={"COMP":"Cadastro composto v3.4","SR_CARD":"Serviço cardiovascular SR116","SR_CARD_SUS":"SR116 ambulatorial SUS","PA":"PA cardiovascular específico","SIH":"AIHs cardiovasculares","EQ_441_QT_USO":"Eletrocardiógrafo em uso","SR122_003":"Serviço de ECG convencional","SR122_007":"Serviço de ECG por telemedicina","ECG":"ECG aprovado","PROF":"Vínculo por CBO","SUS":"Vínculo SUS","HAB":"Habilitação cardiovascular","LT_32_QT_EXIST":"Leito clínico de cardiologia","LT_02_QT_EXIST":"Leito cirúrgico de cardiologia","INSTR_C":"BPA consolidado","INSTR_I":"BPA individualizado","INSTR_P":"APAC principal","INSTR_S":"APAC secundária","ST":"Cadastro ST"}
questions={"V01":"Quantos prestadores reúnem recurso cadastrado e produção em cada sistema?","V02":"Quais registros de SR116 coincidem com produção ambulatorial ou hospitalar?","V03":"Quantos prestadores com ECG aprovado têm equipamento e serviço convencional cadastrados?","E01":"A produção observada está contida nos conjuntos anuais de cadastro e vínculo SUS?","U01":"Quais combinações de serviço, profissional, vínculo e produção são observadas?","U02":"Como os cadastros convencional e por telemedicina se cruzam com equipamento e ECG?","U03":"Quais combinações de habilitação, leitos e AIHs aparecem nos mesmos prestadores?","U04":"Em quais instrumentos um mesmo prestador informa produção específica aprovada?"}
titles={"V01":"Cadastro cardiovascular e produção observada","V02":"Serviço cardiovascular especializado e produção","V03":"Equipamento, serviço e produção de ECG","E01":"Cadastro, vínculo SUS e produção cardiovascular","U01":"Serviço, vínculo profissional e produção","U02":"Modalidades de eletrocardiografia","U03":"Habilitação, leitos de cardiologia e internações","U04":"Instrumentos da produção ambulatorial específica","T01":"Interseções de SR116, PA e SIH ao longo da série","T02":"Serviço SR116 ambulatorial SUS e PA específico nas regiões"}
titles.update({"T03":"Persistência do perfil de cadastro e produção"})
plt.rcParams.update({"font.family":"DejaVu Sans","text.color":INK,"axes.labelcolor":INK,"xtick.color":GRAY,"ytick.color":GRAY,"svg.fonttype":"none","svg.hashsalt":"Observatorio-SUS-ES-v341"})
notes=[]; rendered=[]
def header(fig,id,territory,period,subtitle):
    fig.text(.055,.95,f"{id}    /    {territory}    /    {period}",fontsize=10,color=TEAL,weight="bold",va="top")
    fig.text(.055,.875,titles[id],fontsize=20,color=INK,weight="bold",va="top")
    fig.text(.055,.79,subtitle,fontsize=10.5,color=GRAY,va="top")
def finish(fig,id,group,tab,question,definition,limit,universe,period="2024",territory="Espírito Santo"):
    loc=c/group;loc.mkdir(exist_ok=True); table=loc/(id+"_tabela.csv");tab.to_csv(table,index=False)
    fig.text(.055,.075,limit,fontsize=8.5,color=GRAY)
    fig.text(.055,.038,f"Fonte: CNES, SIA/PA e SIH/RD · v3.4  |  CNES distintos  |  Tabela {id}  |  figuras.py  |  contagens conferidas",fontsize=7.8,color=GRAY)
    for suffix in ["svg","png"]:
        f=loc/(id+"."+suffix);fig.savefig(f,dpi=190,facecolor="white",metadata={"Title":titles[id]})
        if suffix=="png":
            with Image.open(f) as im:im.verify()
        else:ET.parse(f)
    plt.close(fig)
    notes.append(dict(figura=id,frente=group,titulo=titles[id],pergunta=question,conjuntos=definition,unidade="Estabelecimento distinto (CNES)",ano=period,territorio=territory,universo=universe,fonte="Matrizes certificadas v3.4",script="figuras.py; figuras_conjuntos.py",validacao="Contagens confrontadas com os padrões completos",limitacao=limit,tabela=table.name,sha256_tabela=sha(table)))
def trios(theme):
    table=data[(data.tema==theme)&(data.territorio=="ES")&(data.ano==2024)].sort_values("padrao").copy()
    return table,table.exclusiva_anual.to_numpy(dtype=int)
def tline(fig,x,y,lab,val,color=INK):
    fig.text(x,y,lab,va="center",fontsize=10,color=color);fig.text(.936,y,numero(val),ha="right",va="center",fontsize=11,weight="bold",color=color)
for theme in ["V01","V02","V03"]:
    cols=TEMAS[theme][1];tab,ex=trios(theme);U=int(sum(ex))
    fig=plt.figure(figsize=(11,6.4));header(fig,theme,"Espírito Santo","2024",questions[theme])
    ax=fig.add_axes([.055,.14,.45,.56]);venn3(ax,ex)
    for j,(l,mask) in enumerate(zip(cols,[4,2,1])):
        tline(fig,.53,.684-j*.063,chr(65+j)+"   "+short[l],inclusiva(ex,mask),[BLUE,ORANGE,TEAL][j])
    fig.text(.53,.47,"Interseções inclusivas",weight="bold",fontsize=10)
    for j,(lab,mask) in enumerate([("A ∩ B",6),("A ∩ C",5),("B ∩ C",3),("A ∩ B ∩ C",7)]):tline(fig,.53,.425-j*.043,lab,inclusiva(ex,mask))
    tline(fig,.53,.222,"União de A, B e C",U-ex[0])
    tline(fig,.53,.178,"Fora dos três conjuntos",ex[0])
    tline(fig,.53,.134,"Universo cadastral do ano",U)
    for m,n in enumerate(ex):rendered.append((theme,format(m,"03b"),int(n)))
    lim="Venn esquemático. Os números nos círculos são exclusivos. O pertencimento anual admite meses diferentes."
    finish(fig,theme,"TCC",tab,questions[theme],"; ".join(short[x] for x in cols),lim,U)
tab,ex=trios("E01");U=int(sum(ex));sus=inclusiva(ex,4);prod=sum(ex[m] for m in range(len(ex)) if m&3)
assert inclusiva(ex,8)==U and sum(ex[m] for m in range(16) if m&3 and not m&4)==0
fig=plt.figure(figsize=(11,6.4));header(fig,"E01","Espírito Santo","2024",questions["E01"])
ax=fig.add_axes([.055,.15,.61,.52]);euler_aninhado(ax,U,sus,prod)
for j,(lab,val) in enumerate([("Cadastro sem vínculo SUS",U-sus),("Vínculo sem PA/SIH",sus-prod),("Com PA ou SIH",prod)]):
    fig.text(.70,.59-j*.145,lab,fontsize=10);fig.text(.70,.528-j*.145,numero(val),fontsize=19,color=BLUE,weight="bold")
finish(fig,"E01","TCC",tab,questions["E01"],"Cadastro ST; vínculo SUS; união PA específico ou SIH cardiovascular","Euler esquemático. As inclusões foram conferidas por CNES no ano. As áreas não representam quantidades.",U)
for theme in ["U01","U02","U03","U04"]:
    cols=TEMAS[theme][1];tab,ex=trios(theme);U=int(sum(ex))
    fig=plt.figure(figsize=(max(12,4+.46*int((ex[1:]>0).sum())),7.3))
    header(fig,theme,"Espírito Santo","2024",questions[theme])
    masks=upset(fig,[short[x] for x in cols],ex)
    assert set(masks)==set(np.flatnonzero(ex))-{0}
    for m in masks:rendered.append((theme,format(m,f"0{len(cols)}b"),int(ex[m])))
    fig.text(.055,.126,f"Universo cadastral  {numero(U)}     |     União  {numero(U-ex[0])}     |     Fora dos conjuntos  {numero(ex[0])}",fontsize=10,weight="bold")
    finish(fig,theme,"Observatorio",tab,questions[theme],"; ".join(short[x] for x in cols),"Cada coluna conta uma combinação exclusiva. Pontos escuros indicam presença. Todas as combinações positivas da união estão visíveis.",U)
# Temporal views distinguish an annual intersection from three criteria in one administrative month.
df=data[(data.tema=="V02")&(data.padrao=="111")&(data.territorio.isin(["ES","Norte"]))].copy()
fig,axs=plt.subplots(1,2,figsize=(11,6.4));fig.subplots_adjust(left=.08,right=.96,bottom=.23,top=.66,wspace=.30)
header(fig,"T01","Espírito Santo e Região Norte","2014–2024","Quantos estabelecimentos reuniram SR116 e as duas produções no ano ou na mesma competência?")
for ax,rg in zip(axs,["ES","Norte"]):
    part=df[df.territorio==rg].sort_values("ano")
    for col,lab,m,cx,ls in [("inclusiva_anual","No ano","o",BLUE,"-"),("inclusiva_em_algum_mes","Na mesma competência","x",ORANGE,"--")]:
        ax.plot(part.ano,part[col],marker=m,ls=ls,color=cx,label=lab,lw=1.6)
    ax.set_title(rg);ax.set_ylabel("CNES distintos");ax.set_ylim(-.6,df.inclusiva_anual.max()+2);ax.yaxis.set_major_locator(MaxNLocator(integer=True,nbins=5));ax.grid(axis="y",alpha=.22);ax.legend(fontsize=8)
    ax.set_xticks([2014,2016,2018,2020,2022,2024])
finish(fig,"T01","TCC",df,"A coincidência anual ocorre também em algum mês?","SR116, PA específico e AIH cardiovascular","PA por produção e SIH por processamento. A coincidência administrativa mensal não comprova operação contínua.","Universos territoriais anuais na tabela","2014–2024","ES e Norte")
ra=pd.read_csv(b/"razoes_bidirecionais.csv.gz");rr=ra[(ra.tema=="V02S")&(ra.X=="SR_CARD_SUS")&(ra.Y=="PA")&(ra.territorio!="ES")].copy()
regs=["Norte","Central","Metropolitana","Sul"];rr["rotulo"]=[f"{int(n)}/{int(d)}" for n,d in zip(rr.ambos_ano,rr.n_X)]
pv=rr.pivot(index="territorio",columns="ano",values="pct_Y_entre_X").loc[regs];rrs=rr.set_index(["territorio","ano"])
fig=plt.figure(figsize=(12.8,6.3));header(fig,"T02","Quatro Regiões de Saúde do ES","2014–2024","Entre os estabelecimentos com SR116 ambulatorial SUS, quantos têm PA específico observado?")
ax=fig.add_axes([.16,.28,.76,.35]);im=ax.imshow(pv,cmap="Blues",vmin=0,vmax=100,aspect="auto")
for j,yr in enumerate(pv.columns):
    for i,rg in enumerate(regs):ax.text(j,i,rrs.loc[(rg,yr),"rotulo"],ha="center",va="center",fontsize=9,color="white" if pv.loc[rg,yr]>56 else "#172e45")
ax.set_xticks(range(len(pv.columns)),pv.columns);ax.set_yticks(range(len(regs)),regs)
cb=fig.colorbar(im,cax=fig.add_axes([.37,.18,.40,.022]),orientation="horizontal");cb.set_label("% de prestadores do denominador regional",fontsize=9)
finish(fig,"T02","TCC",rr,"Qual a interseção por território e ano?","SR116 ambulatorial SUS e PA específico","Cada célula informa interseção anual / estabelecimentos com SR116 ambulatorial SUS. A cor representa essa proporção.","SR116 ambulatorial SUS do território e ano","2014–2024","Quatro Regiões de Saúde")
# Annual transitions: one state per CNES for each year, plus explicit entry and exit from the universe.
tran=pd.read_csv(b/"transicoes_de_perfil.csv.gz",dtype={"padrao_anterior":str,"padrao_atual":str})
mt=tran[(tran.tema=="V02")&(tran.territorio=="ES")&(tran.ano_atual==2024)]
order=["FORA"]+[format(x,"03b") for x in range(8)]
mat=mt.pivot(index="padrao_anterior",columns="padrao_atual",values="cnes").reindex(index=order,columns=order).fillna(0)
fig=plt.figure(figsize=(11,7.6));header(fig,"T03","Espírito Santo","2023 → 2024","Como mudou o perfil anual SR116 (A), PA específico (B) e SIH cardiovascular (C) em cada CNES?")
ax=fig.add_axes([.12,.23,.50,.49]);im=ax.imshow(np.log1p(mat),cmap="Blues",aspect="auto")
for i in range(9):
    for j in range(9):ax.text(j,i,numero(mat.iloc[i,j]),ha="center",va="center",fontsize=8,color="white" if np.log1p(mat.iloc[i,j])>np.log1p(mat.values.max())*.58 else INK)
ax.set_xticks(range(9),order);ax.set_yticks(range(9),order);ax.set_xlabel("Perfil em 2024");ax.set_ylabel("Perfil em 2023")
fig.text(.66,.59,"Como ler o padrão",weight="bold");fig.text(.66,.54,"Da esquerda para a direita",fontsize=10,va="top")
fig.text(.66,.485,"A    Serviço SR116\nB    PA específico\nC    SIH cardiovascular",fontsize=11,linespacing=1.55,va="top")
fig.text(.66,.32,"1 = presença no ano\n0 = ausência no recorte\nFORA = ausente do universo anual",fontsize=9,linespacing=1.55,va="top")
finish(fig,"T03","Observatorio",mat.rename_axis("padrao_em_2023").reset_index(),"Quais perfis anuais persistiram ou mudaram?","Ordem de bits SR116, PA, SIH","Números são contagens exatas; a intensidade usa log(1 + contagem). Ausência no recorte não identifica encerramento de serviço.","União dos universos anuais de 2023 e 2024","2023–2024","Espírito Santo")
pd.DataFrame(notes).to_csv(c/"indice_figuras.csv",index=False)
# Validate all numeric labels of the Venn regions and UpSet columns against the source table after serialization.
for fig,mask,n in rendered:
    group="TCC" if fig.startswith("V") else "Observatorio"
    tt=pd.read_csv(c/group/(fig+"_tabela.csv"),dtype={"padrao":str}).set_index("padrao")
    assert tt.loc[mask,"exclusiva_anual"]==n
save(c/"verificacao_grafica.json",dict(figuras=len(notes),contagens_graficas_conferidas=len(rendered),formatos=["SVG","PNG"],tabelas_por_figura=len(notes)))
print(len(notes),"figuras",len(rendered),"rótulos reconciliados")
