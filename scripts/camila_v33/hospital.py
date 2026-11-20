"""Reutiliza os fluxos agregados certificados, com os mesmos grupos e conversão de idade do SIH."""
import csv
from collections import Counter
from comum import *
from observatorio_sus.estudos.camila.sim import GRUPOS

def main():
    a=Acervo()
    arquivos=ler(a.fonte(a.sih/'arquivos.csv',a.sih))
    assert len(arquivos)==3564 and not arquivos.duplicated(['competencia','uf']).any()
    conv=ler(a.fonte(a.sih/'conversao_demografica.csv',a.sih)).fillna(-999)
    def norm(v):
        try: return int(v)
        except (TypeError,ValueError): return -999
    cv={(r.ano,r.sexo_sih,r.unidade_idade,r.idade_sih):(r.sexo,int(r.faixa)) for r in conv.itertuples()}
    counts=Counter()
    od=Counter()
    for row in arquivos.itertuples():
        rec=Path(row.recibo_analitico)
        if sha(rec)!=row.sha256_recibo: raise ValueError(rec)
        fonte=a.fonte(rec.with_name('fluxos.csv'),rec.parent)
        ano=int(row.competencia)//100
        with fonte.open(encoding='utf-8-sig',newline='') as fp:
            for r in csv.DictReader(fp):
                res,at=r['municipio_res'],r['municipio_atend']
                if not res.startswith('32') and row.uf!='ES': continue
                qtd=int(r['aih'])
                od[ano,res,r['regiao_res'],row.uf,at,r['regiao_atend']]+=qtd
                if not res.startswith('32'): continue
                sexo,idade=cv[ano,norm(r['sexo_sih']),norm(r['unidade_idade']),norm(r['idade'])]
                cid=int(r['diagnostico'][1:3])
                for g in ['G0']+[key for key,(lo,hi) in GRUPOS.items() if lo<=cid<=hi]:
                    counts[ano,r['regiao_res'],sexo,idade,g]+=qtd
    pasta=a.w/'checkpoint-B'
    def quadro(dic,cols):
        return pd.DataFrame([(*k,n) for k,n in sorted(dic.items())],columns=cols.split()+['aih'])
    gravar(quadro(od,'ano municipio_res regiao_res uf_atendimento municipio_at regiao_at'),pasta/'T28.csv.gz')
    gravar(quadro(counts,'ano regiao sexo idade_inicio grupo'),pasta/'estratos_sih.csv.gz')
    gravar(pd.DataFrame([(str(p.relative_to(a.p)),h) for p,h in a.fontes.items()],columns=['fonte','sha256']),pasta/'fontes_sih.csv')
    print('arquivos',len(arquivos),'origens e destinos',len(od),'estratos',len(counts))
if __name__=='__main__': main()
