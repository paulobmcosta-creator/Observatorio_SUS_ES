"""Empacota e confere cada membro das duas entregas, sem substituir um ZIP divergente."""
import os
import tempfile
import io
import csv
from comum import *

def empacotar(dest,membros,manifesto=False):
    # Os hashes dos originais são independentes da leitura posterior dos membros.
    dados={k:sha(v) for k,v in sorted(membros.items())}
    tabela=io.StringIO()
    out=csv.writer(tabela,lineterminator='\n')
    out.writerow(['caminho','bytes','sha256'])
    out.writerows((n,p.stat().st_size,dados[n]) for n,p in sorted(membros.items()))
    conteudo=tabela.getvalue().encode('utf8')
    with tempfile.NamedTemporaryFile(dir=dest.parent,delete=False,suffix='.parcial') as tmp: parcial=Path(tmp.name)
    try:
        with zipfile.ZipFile(parcial,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for n,p in sorted(membros.items()): z.write(p,n)
            if manifesto:z.writestr('MANIFESTO_SHA256.csv',conteudo)
        def verificar(p):
            with zipfile.ZipFile(p) as z:
                nomes=set(membros)|({'MANIFESTO_SHA256.csv'} if manifesto else set())
                assert len(z.infolist())==len(nomes) and set(z.namelist())==nomes
                for n,h in dados.items():
                    with z.open(n) as f:
                        if hashlib.file_digest(f,'sha256').hexdigest()!=h: raise ValueError(n)
                if manifesto: assert z.read('MANIFESTO_SHA256.csv')==conteudo
        verificar(parcial)
        if dest.exists(): verificar(dest)
        else: os.link(parcial,dest)
    finally:parcial.unlink(missing_ok=True)
    return dict(arquivo=dest.name,bytes=dest.stat().st_size,sha256=sha(dest),membros=len(membros)+int(manifesto))

def main():
    a=Acervo()
    man=a.r/'manifesto_sha256.csv'
    files={p.relative_to(a.e).as_posix():p for p in a.e.rglob('*') if p.is_file()}
    h=ler(man)
    assert len(files)==len(h)+1 and set(files)-set(h.caminho)=={man.relative_to(a.e).as_posix()}
    for r in h.itertuples(): assert sha(files[r.caminho])==r.sha256
    base=a.f/(a.b.name+'.zip')
    assert sha(base)=='8afd4c51ec49c2a80457d4f370afd9808729bb0c074efbc69836eefe296e634b'
    ed=a.w/(a.e.name+'.zip')
    recibos=[empacotar(ed,{a.e.name+'/'+n:p for n,p in files.items()})]
    audit={ed.name:ed}
    for pasta in ['checkpoint-A','checkpoint-B','checkpoint-C','referencias']:
        for p in (a.w/pasta).rglob('*'):
            if p.is_file():audit[p.relative_to(a.w).as_posix()]=p
    for p in [a.exp,a.parecer]:audit['referencias/'+p.name]=p
    recibos.append(empacotar(a.w/'AUDITORIA_TCC_CAMILA_v3.3.zip',audit,True))
    for r in recibos:
        nome=r['arquivo']
        nota(a.w/(nome+'.sha256'),r['sha256']+'  '+nome)
        for f in [a.w/nome,a.w/(nome+'.sha256')]:
            dest=a.docs/f.name
            if not dest.exists():
                with dest.open('xb') as writer,f.open('rb') as reader:shutil.copyfileobj(reader,writer)
            if sha(dest)!=sha(f):raise ValueError(dest)
    json_out(a.w/'recibo_empacotamento.json',recibos)
    print(json.dumps(recibos,indent=2))
if __name__=='__main__':main()
