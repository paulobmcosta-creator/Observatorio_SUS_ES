"""Confrontar somente DEPOIS de produzir os resultados dos três pilotos."""
from pathlib import Path
import argparse, csv, json, hashlib
def sha(p):
    with p.open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def table(p,rows):
    with p.open("w",encoding="utf8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
import pandas as pd
import numpy as np
from collections import Counter
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--pilotos", required=True,type=Path)
parser.add_argument("--referencias",required=True,type=Path)
parser.add_argument("--saida",required=True,type=Path)
args=parser.parse_args()
q=args.pilotos; destino=args.saida; log=[]
if destino.exists() and any(destino.iterdir()):parser.error("A saída deve ser nova ou vazia")
destino.mkdir(parents=True,exist_ok=True)
config=json.loads(args.referencias.read_text(encoding="utf-8-sig"))
def referencia(k):
    spec=config[k]; f=(args.referencias.parent/spec["caminho"]).resolve()
    if sha(f)!=spec["sha256"]:raise ValueError("Edição da referência diverge: "+k)
    return f
def compare(source,observed,expected,fields,keys,label):
    joined=observed.merge(expected,on=keys,how="outer",indicator=True,suffixes=("_piloto","_referencia"),validate="one_to_one")
    ok=joined._merge.eq("both")
    for col in fields:
        left,right=joined[col+"_piloto"],joined[col+"_referencia"]
        if col in ("participacao_no_ES","atracao_pct"):
            ok &= np.isclose(left,right,rtol=1e-12,atol=1e-10,equal_nan=True)
        else:
            ok &= left.eq(right)
    joined["igual"]=ok;joined.to_csv(destino/(label+"_confronto.csv"),index=False)
    log.append(dict(trajetoria=label,referencia=source.name,sha256_referencia=sha(source),linhas=len(joined),iguais=int(ok.sum()),divergentes=int((~ok).sum()),resultado="demonstrada" if ok.all() else "divergente"))
sim=pd.read_csv(q/"SIM/sim_2024.csv")
f=referencia("T29");t=pd.read_csv(f).query("ano==2024 and territorio in ('ES','Norte','Central','Metropolitana','Sul')")[["territorio","obitos"]].rename(columns={"obitos":"obitos_circulatorios"})
es=int(t.loc[t.territorio.eq("ES"),"obitos_circulatorios"].iloc[0]);t.loc[len(t)]=["RES_ES_IGNORADO",es-t.loc[t.territorio.ne("ES"),"obitos_circulatorios"].sum()]
t["participacao_no_ES"]=t.obitos_circulatorios/es;compare(f,sim,t,["obitos_circulatorios","participacao_no_ES"],["territorio"],"SIM")
f=referencia("fluxo");expected=pd.read_csv(f).groupby(["regiao_res","regiao_atend","ano_admissao"],as_index=False).aih.sum()
compare(f,pd.read_csv(q/"SIH/sih_fluxo.csv"),expected,["aih"],["regiao_res","regiao_atend","ano_admissao"],"SIH_fluxo")
f=referencia("mensal");monthly=pd.read_csv(f).query("competencia==202412").rename(columns={"atendimento_es":"aih_principais_circulatorias"});compare(f,pd.read_csv(q/"SIH/sih_indicador.csv"),monthly[["competencia","aih_principais_circulatorias","atracao_aih","atracao_pct"]],["aih_principais_circulatorias","atracao_aih","atracao_pct"],["competencia"],"SIH_indicador")
f=referencia("intersecoes")
expected=pd.read_csv(f,dtype={"padrao":str}).query("tema=='V03' and territorio=='ES' and mes==202412")
compare(f,pd.read_csv(q/"CNES_SIA/cnes_sia_ecg.csv",dtype={"padrao":str}),expected[["padrao","exclusiva","inclusiva","uniao","universo"]],["exclusiva","inclusiva","uniao","universo"],["padrao"],"CNES_SIA")
table(destino/"confrontos.csv",log);print([(r["trajetoria"],r["linhas"],r["divergentes"]) for r in log])

if any(r["divergentes"] for r in log):raise SystemExit(1)
