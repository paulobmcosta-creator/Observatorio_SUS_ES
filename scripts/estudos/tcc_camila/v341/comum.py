from pathlib import Path
import csv,hashlib,json,sys
import argparse
import duckdb
import pandas as pd
def sha(p):
    with p.open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def save(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str),encoding="utf8")
def txt(p,s):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s.strip()+"\n",encoding="utf8")
def q(v):return "'"+str(v).replace("\\","/").replace("'","''")+"'"
def csvrel(p):return f"read_csv({q(p)},all_varchar=true,header=true,sample_size=20480)"
def csvfile(p,records):
    pd.DataFrame(records).to_csv(p,index=False)
def paths():
    parser=argparse.ArgumentParser()
    parser.add_argument("--trabalho", required=True, type=Path, help="Pasta privada da execução com A, B e C")
    parser.add_argument("--integracao", type=Path, help="Agregados da integração anterior para a contraprova")
    args=parser.parse_args()
    return args.trabalho.resolve(), None, None, args.integracao
def sello(folder,filename,**meta):
    save(folder/filename,dict(**meta,arquivos={p.relative_to(folder).as_posix():sha(p) for p in sorted(folder.rglob("*")) if p.is_file() and p.name!=filename}))
