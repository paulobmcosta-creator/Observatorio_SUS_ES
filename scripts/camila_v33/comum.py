"""Rotinas compartilhadas da complementação incremental. Caminhos vêm da execução."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import zipfile
import pandas as pd
import numpy as np

REG = ['Central','Metropolitana','Norte','Sul']
OUTRAS = ['Central','Metropolitana','Sul']
COMP = 'ES sem Norte'
ESTRITO = 'ES sem Norte estrito'
ANOS = list(range(2014,2025))
NOME = 'ENTREGA_TCC_CAMILA_2014_2024'
REPO = Path(__file__).resolve().parents[2]

def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()

def gravar(df, path):
    path.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(path,index=False,lineterminator='\n',compression={'method':'gzip','mtime':0} if path.suffix=='.gz' else None)
    return df

def nota(path,conteudo):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(conteudo.strip()+'\n',encoding='utf8')

def json_out(path,obj):
    nota(path,json.dumps(obj,indent=2,ensure_ascii=False,default=str,allow_nan=False))

def ler(p,**kw):
    return pd.read_csv(p,dtype={'codigo':str,'municipio':str,'municipio_res':str,'sexo_sim':str,'chave':str},**kw)

def igual(a,b,rotulo,tol=1e-7):
    if not np.allclose(np.asarray(a,dtype=float),np.asarray(b,dtype=float),atol=tol,rtol=0,equal_nan=True):
        raise ValueError('Divergência em '+rotulo)

class Acervo:
    def __init__(self):
        cli=argparse.ArgumentParser()
        cli.add_argument('custodia',type=Path)
        cli.add_argument('documentos',type=Path)
        cli.add_argument('--destino',type=Path)
        args=cli.parse_args()
        self.p=args.custodia.resolve()
        self.docs=args.documentos.resolve()
        self.f=self.p/'mandato-v3.2.1'
        self.b=self.f/(NOME+'_v3.2.1')
        self.w=(args.destino or self.p/'mandato-v3.3').resolve()
        self.e=self.w/(NOME+'_v3.3')
        self.r=self.e/'08_REPRODUTIBILIDADE'
        self.tab=self.e/'02_TABELAS'
        self.v=self.p/'mandato-v3'
        self.sih=self.p/'mandato-v3.1-sih/entrega-final'
        self.et=self.p/'mandato-v3.2/etapa1'
        self.doc=self.docs/'TCC_Camila_segunda_rodada_referencial_v4.docx'
        self.exp=self.docs/'Cruzamento_exploratorio_TCC_Camila_2014_2024.csv'
        self.parecer=self.docs/'Parecer_Analitico_Indicadores_TCC_Camila_v3_2_1.md'
        self.fontes={}
    def tabela(self,id):
        return ler(next(p for p in self.b.rglob(id+'.csv*') if p.name in [id+'.csv',id+'.csv.gz']))
    def fonte(self,path,raiz=None):
        if path not in self.fontes:
            h=sha(path)
            if raiz:
                ref=json.loads((raiz/'recibo.json').read_text(encoding='utf-8-sig'))['saidas'][path.relative_to(raiz).as_posix()]
                if h!=ref: raise ValueError('Fonte alterada '+str(path))
            self.fontes[path]=h
        return path
