"""Contraprovas delimitadas do TCC. A entrada contém apenas originais, hashes e território."""
import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(REPO/"python"), str(REPO/"scripts"), str(REPO/"scripts/integracao_estabelecimentos")]
from observatorio_sus.estudos.camila import sim, territorio
from oferta_producao_camila import blocos
from figuras_conjuntos import venn3

def digest(path):
    with path.open("rb") as file:return hashlib.file_digest(file,"sha256").hexdigest()

def save(df, output, name):
    df.to_csv(output/name, index=False, lineterminator="\n")

def sim_piloto(inputs, out):
    ref=inputs["SIM"]
    with zipfile.ZipFile(ref["path"]) as archive, archive.open(ref["membro"]) as stream:
        cube, qa=sim.leitor_pandas(stream,2024,territorio.mapa())
    counts=Counter()
    for (_, _, _, region, _), n in cube.items():counts[region]+=n
    total=sum(counts.values())
    rows=[(region,n,n/total) for region,n in sorted(counts.items())]+[("ES",total,1)]
    save(pd.DataFrame(rows,columns=["territorio","obitos_circulatorios","participacao_no_ES"]),out,"sim_2024.csv")
    return {**dict(qa),"circulatorios":total,"regra":"não fetal, residente ES, data do óbito em 2024 e CID final circulatória válida; sem restrição etária"}

def ler_dbc(meta, fields, qa):
    """O DBF temporário existe somente durante a leitura e não é escrito na saída."""
    with tempfile.TemporaryDirectory() as tmp:
        directory=Path(tmp)
        shutil.copyfile(meta["path"], directory/"fonte.dbc")
        subprocess.run([sys.executable,"-c","from pyreaddbc.readdbc import _dbc2dbf; _dbc2dbf('fonte.dbc','dados.dbf')"],cwd=directory,check=True)
        for block, expected in blocos(directory/"dados.dbf",fields):
            active=block["estado"]==b" "
            if not np.isin(block["estado"],[b" ",b"*"]).all():raise ValueError("Flag DBF desconhecida")
            qa.update(lidas=len(block),ativas=int(active.sum()),excluidas=int((~active).sum()))
            yield block[active]
        if qa["lidas"]!=expected:raise ValueError("Total do cabeçalho DBF divergente")

def local(code, pdr):
    if code in pdr:return pdr[code]
    if len(code)==6 and code.isdigit() and code[:2] in "11 12 13 14 15 16 17 21 22 23 24 25 26 27 28 29 31 33 35 41 42 43 50 51 52 53".split():return "OUTRA_UF_CODIGO_PLAUSIVEL"
    return "INDETERMINADA"

def sih_piloto(inputs,out):
    counts=Counter();qa=Counter();pdr=territorio.mapa()
    fields="ANO_CMPT MES_CMPT IDENT DIAG_PRINC MUNIC_RES MUNIC_MOV DT_INTER".split()
    for block in ler_dbc(inputs["RD"],fields,qa):
        if not ((block["ANO_CMPT"]==b"2024")&(block["MES_CMPT"]==b"12")).all():raise ValueError("Competência do RD")
        eligible=block[(block["IDENT"]==b"1")&np.char.startswith(block["DIAG_PRINC"],b"I")]
        for row in eligible:
            origin=row["MUNIC_RES"].decode().strip();dest=row["MUNIC_MOV"].decode().strip();admission=row["DT_INTER"].decode().strip()[:4]
            counts[(origin,local(origin,pdr),dest,local(dest,pdr),admission)]+=1
    df=pd.DataFrame([(*k,n) for k,n in sorted(counts.items())],columns=["municipio_res","regiao_res","municipio_atend","regiao_atend","ano_admissao","aih"])
    # Only regional/counting outputs leave the computation.
    flow=df.groupby(["regiao_res","regiao_atend","ano_admissao"],as_index=False).aih.sum()
    save(flow,out,"sih_fluxo.csv")
    total=int(df.aih.sum());outside=int(df.loc[df.regiao_res.eq("OUTRA_UF_CODIGO_PLAUSIVEL"),"aih"].sum())
    save(pd.DataFrame([dict(competencia="202412",uf_atendimento="ES",aih_principais_circulatorias=total,atracao_aih=outside,atracao_pct=100*outside/total)]),out,"sih_indicador.csv")
    return dict(**qa,elegiveis=total,chaves_municipais_com_admissao=len(df),regra="IDENT 1; diagnóstico principal circulatório, competência de processamento; ano de admissão próprio")

def sigtab(archive,name):
    layout=csv.DictReader(io.StringIO(archive.read(name+"_layout.txt").decode("latin1")))
    fields={r["Coluna"]:(int(r["Inicio"])-1,int(r["Fim"])) for r in layout}
    for line in archive.read(name+".txt").decode("latin1").splitlines():
        yield {k:line[i:j].strip() for k,(i,j) in fields.items()}

def selecionar_ecg(arr, competencia, codigo):
    """Campos DBF são bytes de largura fixa; movimento e produção têm papéis distintos."""
    return arr[(arr["PA_CMP"] == competencia) & (arr["PA_PROC_ID"] == codigo.encode("ascii"))]

def cnes_piloto(inputs,out):
    code="0211020036";compet=b"202412";qa={};sets={};valid=lambda c:len(c)==7 and c.isdigit() and c!="0000000"
    with zipfile.ZipFile(inputs["SIGTAP"]["path"]) as z:
        regs={r["CO_REGISTRO"] for r in sigtab(z,"rl_procedimento_registro") if r["CO_PROCEDIMENTO"]==code}
        found=[r for r in sigtab(z,"tb_procedimento") if r["CO_PROCEDIMENTO"]==code]
        sr=any(r["CO_SERVICO"]=="122" and r["CO_CLASSIFICACAO"]=="003" for r in sigtab(z,"tb_servico_classificacao"))
    if len(found)!=1 or not regs or not sr:raise ValueError("Vigência clínica ou serviço sem domínio histórico")
    instrumentos={b"C":"01",b"I":"02",b"P":"06",b"S":"07",b"A":"08",b"B":"09"}
    for fam,extra in [("ST",[]),("EQ",["TIPEQUIP","CODEQUIP","QT_USO"]),("SR",["SERV_ESP","CLASS_SR"])]:
        qa[fam]=Counter();keys=Counter()
        for arr in ler_dbc(inputs[fam],["COMPETEN","CNES",*extra],qa[fam]):
            if not (arr["COMPETEN"]==compet).all():raise ValueError(fam+" competência")
            if fam=="EQ":arr=arr[(np.char.add(arr["TIPEQUIP"],arr["CODEQUIP"])==b"441")]
            if fam=="SR":arr=arr[(arr["SERV_ESP"]==b"122")&(arr["CLASS_SR"]==b"003")]
            for r in arr:
                c=r["CNES"].decode().strip()
                if valid(c):keys[c]+=int(r["QT_USO"]) if fam=="EQ" else 1
        sets[fam]={k for k,n in keys.items() if n>0}
    qa["PA"]=Counter();cells=Counter()
    fields=["PA_MVM","PA_CMP","PA_CODUNI","PA_PROC_ID","PA_DOCORIG","PA_QTDAPR","PA_UFMUN"]
    for arr in ler_dbc(inputs["PA"],fields,qa["PA"]):
        if not (arr["PA_MVM"]==compet).all():raise ValueError("Movimento PA divergente")
        arr=selecionar_ecg(arr,compet,code)
        qa["PA"]["linhas_ecg_competencia"]+=len(arr)
        for r in arr:
            if instrumentos.get(r["PA_DOCORIG"]) not in regs:continue
            c=r["PA_CODUNI"].decode().strip()
            if valid(c):cells[(c,r["PA_UFMUN"],r["PA_DOCORIG"])]+=int(r["PA_QTDAPR"])
    sets["PA"]={k[0] for k,n in cells.items() if n>0}
    universe=sets["ST"];outside=(sets["EQ"]|sets["SR"]|sets["PA"])-universe
    masks=Counter("".join("1" if c in sets[f] else "0" for f in ["EQ","SR","PA"]) for c in universe)
    rows=[]
    for i in range(8):
        bits=f"{i:03b}";inc=sum(n for k,n in masks.items() if int(k,2)&i==i)
        rows.append(dict(padrao=bits,exclusiva=masks[bits],inclusiva=inc,universo=len(universe),uniao=len(universe)-masks["000"]))
    df=pd.DataFrame(rows);save(df,out,"cnes_sia_ecg.csv")
    matplotlib.rcParams.update({"svg.hashsalt":"v343-piloto-ECG","svg.fonttype":"none"})
    fig,ax=plt.subplots(figsize=(8,5));fig.subplots_adjust(right=.65,bottom=.13,top=.83);venn3(ax,df.exclusiva.to_numpy())
    fig.suptitle("Cadastro e produção de ECG · Espírito Santo, dezembro de 2024")
    fig.text(.64,.59,"A  Eletrocardiógrafo em uso\nB  Serviço 122/003\nC  ECG aprovado",linespacing=1.6)
    fig.text(.08,.03,"CNES/ST, EQ, SR e SIA/PA · mesma competência · contagens exclusivas de estabelecimentos")
    fig.savefig(out/"cnes_sia_ecg.svg",metadata={"Date":None});plt.close(fig)
    return dict(controles=qa,conjuntos={k:len(v) for k,v in sets.items()},selecionados_fora_ST=len(outside),instrumentos_SIGTAP=sorted(regs),codigo=code,regra="presença aprovada nas células elegíveis; competência e movimento 202412")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trajetoria",choices=["SIM","SIH","CNES_SIA"]);parser.add_argument("--manifesto",type=Path,required=True);parser.add_argument("--saida",type=Path,required=True)
    args=parser.parse_args();out=args.saida
    if out.exists() and any(out.iterdir()):parser.error("A saída deve ser nova ou vazia")
    spec=json.loads(args.manifesto.read_text(encoding="utf-8-sig"))["originais"]
    required={"SIM":["SIM"],"SIH":["RD"],"CNES_SIA":["ST","EQ","SR","PA","SIGTAP"]}[args.trajetoria]
    sources={}
    for k in required:
        r=spec[k];path=(args.manifesto.parent/r["path"]).resolve()
        if path.stat().st_size!=r["bytes"] or digest(path)!=r["sha256"]:raise ValueError("Edição divergente: "+k)
        sources[k]={**r,"path":path}
    out.mkdir(parents=True,exist_ok=True);start=time.perf_counter()
    qa={"SIM":sim_piloto,"SIH":sih_piloto,"CNES_SIA":cnes_piloto}[args.trajetoria](sources,out)
    receipt={"trajetoria":args.trajetoria,"duracao_segundos":round(time.perf_counter()-start,3),"fontes":{k:{j:r[j] for j in ("url","bytes","sha256")} for k,r in sources.items()},"codigo_sha256":digest(Path(__file__)),"territorio_sha256":digest(territorio.TABELA),"controles":qa,"saidas":{f.name:digest(f) for f in out.iterdir() if f.is_file()}}
    (out/"recibo.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding="utf8")
    print(args.trajetoria, "concluída", receipt["duracao_segundos"], "s")

if __name__=="__main__":main()
