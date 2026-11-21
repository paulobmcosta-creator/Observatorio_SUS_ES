"""Matrizes pareadas do recorte da insuficiência cardíaca de residentes do ES."""
import json,sys
from entradas import papel
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
d=papel("saida")/"SIM";d.mkdir(parents=True,exist_ok=True)
base=papel("academico_anterior")
data=pd.concat([pd.read_csv(papel("estratos_i50")/str(y)/"insuficiencia.csv",keep_default_na=False).assign(ano=y) for y in range(2014,2025)])
a=data.i50_original;b=data.i50_final
assert (a==data.original.str.startswith("I50")).all() and (b==data.final.str.startswith("I50")).all()
for name,flag in dict(entrada=~a&b,saida=a&~b,retida=a&b,i50_original=a,i50_final=b,ampliada=data.ampliada,mencao_atestado=data.mencao_atestado,mencao_linhas=data.mencao_linhas,mencao_uniao=data.mencao_atestado|data.mencao_linhas).items(): data[name]=data.obitos*flag
keys="i50_original retida saida entrada i50_final ampliada mencao_atestado mencao_linhas mencao_uniao".split()
def tab(group):return data.groupby(group,as_index=False,dropna=False)[keys].sum()
annual=tab(["ano"]);ref=pd.read_csv(base/"01_BASES_E_INDICADORES/complementares/B03.csv").query("territorio=='ES'")
pd.testing.assert_frame_equal(annual.set_index("ano")[keys],ref.set_index("ano")[keys],check_dtype=False)
assert (annual.i50_original-annual.saida+annual.entrada==annual.i50_final).all()
annual.to_csv(d/"balanco_anual.csv",index=False)
monthly=tab(["ano","mes"]);assert len(monthly)==132;monthly.to_csv(d/"balanco_mensal.csv",index=False)
for label,group in {"regional":["ano","mes","regiao"],"demografico":["ano","regiao","sexo","idade_ampla"]}.items():
    age=pd.to_numeric(data.faixa.replace({"IGNORADA":-1,"80+":80}),errors="raise")
    data["idade_ampla"]=np.select([age<0,age<30,age<60,age<80],["Ignorada","0–29","30–59","60–79"],default="80+")
    tab(group).to_csv(d/f"balanco_{label}.csv.gz",index=False)
pairs=data[(data.i50_original>0)|(data.i50_final>0)].copy()
for label,group in {"anual":["ano"],"mensal":["ano","mes"],"territorial":["ano","mes","regiao"],"sexo_idade":["ano","sexo","idade_ampla"]}.items():
    pairs.groupby(group+["original","final"],as_index=False).obitos.sum().to_csv(d/f"pares_{label}.csv.gz",index=False)
dest=pairs[pairs.i50_original>0].groupby(["ano","final"],as_index=False).obitos.sum()
dest["pct_dos_originais"]=100*dest.obitos/dest.groupby("ano").obitos.transform("sum");dest.to_csv(d/"destinos.csv",index=False)
assert dest.query("ano==2024 and final=='I110'").obitos.sum()==266 and dest.query("ano==2024 and final=='I132'").obitos.sum()==33
fig,axes=plt.subplots(2,1,figsize=(9,6),layout="constrained")
for key,color in [("i50_original","#225381"),("i50_final","#ae5935")]:
    axes[0].plot(annual.ano,annual[key],marker="o",color=color,label=key.replace("_"," "))
    part=monthly[monthly.ano>=2022];axes[1].plot(pd.to_datetime(dict(year=part.ano,month=part.mes,day=1)),part[key],color=color)
axes[0].legend();axes[0].set_title("I50 nas declarações de residentes do Espírito Santo");axes[1].set_title("Por mês de ocorrência, 2022–2024")
for ax in axes: ax.set_ylabel("Declarações");ax.grid(axis="y",alpha=.25)
fig.savefig(d/"I50_original_final.png",dpi=175);plt.close(fig)
st=pd.read_csv(papel("estabilidade_municipal"))
assert len(st)==5148 and st.estratos.eq(17).all() and st.estratos_zero.gt(0).sum()==5145
st.groupby("grupo").agg(combinacoes=("ano","size"),com_estrato_zero=("estratos_zero",lambda s:int((s>0).sum()))).to_csv(d/"controle_estabilidade.csv")
print(annual.tail(3).to_string(index=False))
