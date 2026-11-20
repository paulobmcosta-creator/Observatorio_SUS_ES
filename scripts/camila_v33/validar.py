"""Contraprovas por SQL nas tabelas exportadas; executar após os três módulos quantitativos."""
import duckdb
from comum import *

def main():
    a=Acervo()
    cp=a.w/'checkpoint-B'
    db=duckdb.connect()
    for id in ['B01','B02','B04','B05','B06','B07','B08','B09','T01','T02','T03','T05','T07','T08','T09','T10','T11','T12','T15','T16']:
        db.register(id,a.tabela(id))
    for p in cp.glob('T*.csv*'):
        db.register(p.name.split('.')[0],ler(p))
    db.register('pesos',ler(a.v/'taxas-ed2/pesos.csv'))
    db.register('geo',ler(REPO/'metadata/territorio/pdr_es_2024_tcc_v1.csv'))
    db.register('exp',ler(a.exp))
    db.register('cad405',ler(cp/'controle_320405.csv'))
    db.register('i50',a.tabela('B03'))
    qa=[]
    def testar(nome,sql):
        n,f=db.execute('SELECT count(*),count(*) FILTER (WHERE ok IS DISTINCT FROM true) FROM ('+sql+') q').fetchone()
        qa.append(dict(controle=nome,casos=n,divergencias=f))
        if n==0 or f: raise ValueError(f'{nome}: {n} casos e {f} divergências')
    def near(x,y,tol='1e-7'):
        return f'(({x}) IS NULL AND ({y}) IS NULL OR abs(({x})-({y}))<={tol})'
    for tab,keys in {'T20':'ano,territorio','T21':'ano,territorio,codigo','T22':'ano,territorio,modalidade','T23':'ano,territorio,id','T24':'ano,territorio,sexo,grupo','T25':'ano,territorio,sexo_sim,grupo,universo,censo','T26':'ano,municipio,grupo,estrato,valor','T27':'ano,territorio,conceito','T28':'ano,municipio_res,uf_atendimento,municipio_at,regiao_at,regiao_res','T29':'ano,territorio','T30':'ano,territorio,sexo,grupo,idade_inicio','T31':'ano,territorio','T29_longa':'ano,territorio,indicador'}.items():
        testar('Unicidade '+tab,'select count(*)=1 ok from '+tab+' group by '+keys)
    testar('Cobertura SIH','select ufs_validadas=27 ok from B08')
    testar('Comparador PA e SR', 'select '+near('a.aprovadas','b.procedimentos_cardiovasculares_especificos_aprovados_local_prestador')+' and '+near('a.estabelecimentos_sr116_media','b.media_mensal_cnes_sr116')+' ok from T20 a join exp b using(ano,territorio)')
    testar('Grades municipais de produção, oferta e mortalidade',"""select count(distinct territorio)=78 ok from (
      select ano,territorio,'pa' origem from T21 union all select ano,territorio,'cnes' from T23 union all select ano,municipio,'sim' from T26
    ) where territorio in (select cast(cod_municipio_cnes as varchar) from geo) group by ano,origem""")
    testar('Validade municipal 320405','select estabelecimentos_cadastrados>0 and linhas_elegiveis=0 and codigos_vigentes>0 ok from cad405')
    for tab,col,num,den in [('T21','aprovadas_12_meses_por_100mil','aprovadas_12_meses','habitantes'),('T22','aprovadas_por_100mil','aprovadas','habitantes'),('T23','media_anual_12_meses_por_100mil','media_anual_12_meses','habitantes'),('T23','estoque_dezembro_por_100mil','estoque_dezembro','habitantes'),('T24','bruta_100mil','aih','habitantes'),('T25','bruta_100mil','obitos','habitantes'),('T26','taxa_100mil','obitos','habitantes'),('T27','taxa_100mil','obitos','habitantes'),('T30','taxa_100mil','aih','habitantes'),('T31','evasao_pct','evasao_aih','aih_residentes'),('T31','atracao_pct','atracao_aih','atendimento')]:
        mult=100 if tab=='T31' else 100000
        testar(tab+' '+col,'select '+near(col,f'{mult}.0*{num}/nullif({den},0)')+' ok from '+tab)
    testar('Vigência e parcialidade PA','select (aprovadas_12_meses is null)=(meses_validos<12) and (aprovadas is null)=(meses_validos=0) ok from T21')
    testar('Vigência CNES','select (media_anual_12_meses is null)=(meses_validos<12) ok from T23')
    testar('Quantidades PA por classe e código',"""with p as (select ano,territorio,sum(aprovadas) n,sum(apresentadas) m from T21 where grupo_clinico in ('exames_especificos','fisioterapia_especifica') group by all)
    select p.n=t.aprovadas and p.m=t.apresentadas ok from p join T22 t using(ano,territorio) where t.modalidade='especificos'""")
    testar('Média e dezembro municipal contra T15','with x as (select mes//100 ano,municipio territorio,id,avg(valor) media,max(valor) filter(where mes%100=12) dez from T15 group by all) select '+near('x.media','t.media_meses_validos')+' and '+near('x.dez','t.estoque_dezembro')+' ok from x join T23 t using(ano,territorio,id)')
    testar('G0 municipal e óbitos indeterminados','select t.obitos=b.obitos ok from T26 t join T08 b using(ano,municipio) where t.grupo=\'G0\' and t.estrato=\'total\'')
    testar('G0 por município na matriz origem e destino','with g as (select ano,municipio_res,sum(aih) n from T28 group by all) select coalesce(n,0)=aih_residentes ok from T03 left join g using(ano,municipio_res)')
    testar('Pares de origem e destino anuais contra T11',"""with g as (select ano,regiao_res,uf_atendimento,regiao_at,sum(aih) n from T28 group by all),
     h as (select ano,regiao_res,uf_atendimento,regiao_at,sum(aih) n from T11 group by all)
     select g.n=h.n ok from g full join h using(ano,regiao_res,uf_atendimento,regiao_at)""")
    testar('I50 por conceito contra as contagens de B03',"""select t.obitos=case conceito when 'i50_final' then b.i50_final when 'i50_original' then b.i50_original when 'ampliada' then b.ampliada when 'mencao_atestado' then b.mencao_atestado when 'mencao_linhas' then b.mencao_linhas else b.mencao_uniao end ok from T27 t join i50 b using(ano,territorio)""")
    # Uma segunda implementação aplica pesos aos estratos regionais somados, com os dois censos.
    testar('Padrões diretos SIM estritos','''with e as (select ano,grupo,sexo_sim,idade_inicio,sum(obitos) n,sum(habitantes) d from B02 where territorio in ('Central','Sul','Metropolitana') group by all),
      m as (select ano,grupo,sexo_sim,censo,'todas' universo,sum(100000.0*n*peso_todas/d) taxa from e join pesos using(idade_inicio) group by all
      union all select ano,grupo,sexo_sim,censo,'30-69',sum(100000.0*n*peso_30_69/d) from e join pesos using(idade_inicio) where grupo='G0' and idade_inicio between 30 and 65 group by all)
      select '''+near('t.direta_100mil','m.taxa')+" ok from T25 t join m using(ano,grupo,sexo_sim,censo,universo) where territorio='ES sem Norte estrito'")
    testar('Taxas SIH por grupo diante das 27 UFs','''with b as (select competencia//100 ano,territorio,grupo,sum(aih) n from B09 group by all) select coalesce(n,0)=t.aih ok from T24 t left join b using(ano,territorio,grupo) where sexo='T' and territorio<>'ES sem Norte estrito' ''')
    testar('Padronização SIH em todos os grupos','''with d as (select ano,territorio,grupo,sexo,censo,sum(100000.0*aih*peso_todas/habitantes) n from T30 join pesos using(idade_inicio) group by all) select '''+near('case when censo=2022 then direta_2022 else direta_2010 end','n')+' ok from T24 join d using(ano,territorio,grupo,sexo)')
    wide=ler(cp/'T29.csv')
    longa=ler(cp/'T29_longa.csv.gz').pivot(index=['ano','territorio'],columns='indicador',values='valor')
    ref=wide.set_index(['ano','territorio']).sort_index()
    igual(longa[ref.columns],ref,'matriz longa × ampla')
    qa.append(dict(controle='Células comuns das matrizes longa e ampla',casos=ref.size,divergencias=0))
    gravar(pd.DataFrame(qa),cp/'contraprovas.csv')
    json_out(cp/'recibo.json',dict(testes=len(qa),comparacoes=sum(x['casos'] for x in qa),tolerancia_absoluta=1e-7,arquivos={p.name:sha(p) for p in sorted(cp.glob('*')) if p.name!='recibo.json'}))
    print(len(qa),sum(x['casos'] for x in qa))
if __name__=='__main__':main()
