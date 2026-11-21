from pathlib import Path
import sys
from entradas import papel
import duckdb
import pandas as pd
from observatorio_sus.estudos.camila import territorio
def folder(name):
    w=papel("edicao_operacional"); out=papel("saida")/name; out.mkdir(parents=True,exist_ok=True)
    base=papel("academico_anterior")
    return w,None,base,out
def db():
    conn=duckdb.connect()
    conn.execute("SET threads=2");conn.execute("SET memory_limit='1300MB'")
    return conn
def quote(value):return "'"+str(value).replace("\\","/").replace("'","''")+"'"
def relation(path):return f"read_csv({quote(path)},header=true,all_varchar=true,sample_size=20480,null_padding=false)"
def materialize(con,name,path):con.execute(f"CREATE TABLE {name} AS SELECT * FROM {relation(path)}")
def export(con,path,query):
    con.execute(f"COPY ({query}) TO {quote(path)} (FORMAT CSV, HEADER true"+(",COMPRESSION GZIP" if path.suffix==".gz" else "")+")")
def geo(con):con.execute("CREATE TABLE geo AS SELECT cod_municipio_cnes municipio,regiao_nome regiao FROM "+relation(territorio.TABELA))
