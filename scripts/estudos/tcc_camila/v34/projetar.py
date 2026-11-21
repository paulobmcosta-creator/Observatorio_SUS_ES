"""Projeções mensais dos originais já identificados. Produz somente células agregadas."""
import argparse, csv, hashlib, json, os, shutil, struct, subprocess, sys, tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd
from oferta_producao_camila import blocos
from observatorio_sus.io.custodia import sha256_arquivo

PA="PA_CODUNI PA_UFMUN PA_MUNPCN PA_CMP PA_PROC_ID PA_CBOCOD PA_DOCORIG PA_QTDAPR PA_QTDPRO PA_MVM".split()
RD="CNES MUNIC_MOV MUNIC_RES DIAG_PRINC DT_INTER IDENT ANO_CMPT MES_CMPT".split()
def process(job):
    w, path, expected, family, catalog=job
    month="20"+path.stem[-4:]; dest=w/"projecoes"/family/month
    receipt=dest/"recibo.json"
    if receipt.exists():
        meta=json.loads(receipt.read_text())
        if meta["origem"]==expected and all(sha256_arquivo(dest/n)==h for n,h in meta["saidas"].items()): return month
        raise ValueError(f"Colisão {dest}")
    dest.mkdir(parents=True,exist_ok=True)
    assert sha256_arquivo(path)==expected,path
    fields=PA if family=="PA" else RD
    with path.open("rb") as f:
        n,h,t=struct.unpack_from("<IHH",f.read(32),4)
        schema={}; offset=1
        for _ in range((h-33)//32):
            b=f.read(32); key=b[:11].split(bytes(1))[0].decode(); schema[key]=(offset,b[16]); offset+=b[16]
    assert set(fields)<=schema.keys() and shutil.disk_usage(w).free>3*(n*t+h+path.stat().st_size)+500_000_000
    codes=[s.encode() for s in catalog]; chunks=[]; hist=[]; signatures=[]; alive=deleted=0
    with tempfile.TemporaryDirectory(dir=dest) as tmp:
        tmp=Path(tmp); shutil.copyfile(path,tmp/"original.dbc")
        subprocess.run([sys.executable,"-c","from pyreaddbc.readdbc import _dbc2dbf; _dbc2dbf('original.dbc','leitura.dbf')"],cwd=tmp,check=True)
        for a,_ in blocos(tmp/"leitura.dbf",fields):
            active=a["estado"]==b" "; gone=a["estado"]==b"*"
            assert (active|gone).all()
            alive+=int(active.sum()); deleted+=int(gone.sum())
            if family=="PA":
                assert (a["PA_MVM"][active]==month.encode()).all()
                if month.startswith("2025"):
                    u,c=np.unique(a["PA_CMP"][active],return_counts=True)
                    hist.extend(zip([x.decode() for x in u],c))
                    active &= np.char.startswith(a["PA_CMP"],b"2024")
                active &= np.isin(a["PA_PROC_ID"],codes)
                active &= (a["PA_PROC_ID"]!=b"0301010072")|np.isin(a["PA_CBOCOD"],[b"225120",b"225210",b"225203"])
            else:
                assert ((a["ANO_CMPT"][active]==month[:4].encode())&(a["MES_CMPT"][active]==month[4:].encode())).all()
                active &= (a["IDENT"]==b"1") & np.char.startswith(a["DIAG_PRINC"],b"I")
            sub=a[active]
            if not len(sub): continue
            if family=="PA" and month>="202401":
                selected=active & np.char.startswith(a["PA_CMP"],b"2024")
                # Exact byte signature excluding movement, retaining multiplicity within each movement.
                low,size=schema["PA_MVM"]
                for pos in np.flatnonzero(selected):
                    record=a[pos]; raw=record.tobytes()
                    signatures.append((hashlib.sha256(raw[:low]+raw[low+size:]).digest(),int(record["PA_QTDAPR"]),record["PA_PROC_ID"]))
            df=pd.DataFrame({c:sub[c] for c in fields})
            if family=="PA":
                df.drop(columns="PA_MVM",inplace=True)
                for c in ["PA_QTDAPR","PA_QTDPRO"]: df[c]=pd.to_numeric(df[c],errors="raise")
                keys=list(df.columns[:-2]); vals=["PA_QTDAPR","PA_QTDPRO","linhas"]
            else:
                df=df[~df.DIAG_PRINC.str.decode("latin1").str.strip().str.fullmatch(r"I\d{2}[0-9A-Z]?",na=False).eq(False)].copy()
                dates=pd.to_datetime(df.pop("DT_INTER").str.decode("ascii"),format="%Y%m%d",errors="coerce")
                df["ano_admissao"]=dates.dt.year.fillna(0).astype(int)
                df.drop(columns=["IDENT","ANO_CMPT","MES_CMPT"],inplace=True)
                keys=list(df); vals=["linhas"]
            df["linhas"]=1
            chunks.append(df.groupby(keys,as_index=False,sort=False)[vals].sum())
        assert alive+deleted==n
        keynames=(PA[:7] if family=="PA" else ["CNES","MUNIC_MOV","MUNIC_RES","DIAG_PRINC","ano_admissao"])
        values=(["PA_QTDAPR","PA_QTDPRO","linhas"] if family=="PA" else ["linhas"])
        data=pd.concat(chunks,ignore_index=True).groupby(keynames,as_index=False)[values].sum() if chunks else pd.DataFrame(columns=keynames+values)
        for c in keynames:
            if c!="ano_admissao" and len(data): data[c]=data[c].str.decode("latin1").str.strip()
        data["movimento"]=month
        data.to_csv(tmp/"celulas.csv.gz",index=False)
        outputs=["celulas.csv.gz"]
        if signatures:
            from collections import Counter
            sigs=Counter(signatures)
            import gzip
            with gzip.open(tmp/"assinaturas.tsv.gz","wt",encoding="ascii") as out:
                for (s,q,c),k in sigs.items(): out.write(f"{s.hex()}\t{q}\t{c.decode()}\t{k}\n")
            outputs+=["assinaturas.tsv.gz"]
        groups={}
        for k,c in hist: groups[k]=groups.get(k,0)+int(c)
        meta=dict(arquivo=path.name,origem=expected,bytes=path.stat().st_size,esquema=schema,registros=n,ativos=alive,excluidos=deleted,selecionados=int(data.linhas.sum()),competencias_producao_arquivo_2025=groups,saidas={k:sha256_arquivo(tmp/k) for k in outputs})
        for name in outputs: os.replace(tmp/name,dest/name)
        (tmp/"recibo.json").write_text(json.dumps(meta,indent=2),encoding="utf8");os.replace(tmp/"recibo.json",receipt)
    return f"{family} {month} {meta['selecionados']}"

def main():
    p=argparse.ArgumentParser();p.add_argument("manifesto",type=Path);p.add_argument("sistema",choices=["PA","RD","2025"]);p.add_argument("--workers",type=int,default=2)
    a=p.parse_args();roles=json.loads(a.manifesto.read_text(encoding="utf-8-sig")); ref=a.manifesto.resolve().parent
    def role(n):return (ref/roles[n]).resolve()
    w=role("edicao_operacional")
    def table(path): return pd.read_csv(path,dtype=str)
    hist=table(role("catalogo_clinico")); catalog=hist[hist.classe.isin(["A","B"])].codigo.unique().tolist()
    if a.sistema=="RD":
        inv=table(role("inventario_rd")).query("uf=='ES'")
        jobs=[(w,(role("raiz_rd")/r.caminho_dbc),r.sha256,"RD",catalog) for r in inv.itertuples()]
    elif a.sistema=="PA":
        inv=table(role("inventario_pa")).query("familia=='PA'")
        jobs=[(w,(role("raiz_pa")/r.arquivo_local),r.sha256,"PA",catalog) for r in inv.itertuples()]
    else:
        jobs=[(w,f,json.loads(f.with_name("aquisicao.json").read_text())["sha256"],"PA",catalog) for f in sorted(w.glob("originais-assistencia/PA/ES/*/*.dbc"))]
        assert len(jobs)==12
    with ProcessPoolExecutor(a.workers) as pool:
        for info in pool.map(process,jobs): print(info,flush=True)
if __name__=="__main__":main()
