"""Coluna opcional ausente não demonstra equivalência de linhas/edições."""
from observatorio_sus.transform.validar_partes_csv import validar_partes_csv


def test_sobreposicao_potencial_em_esquemas_diferentes(tmp_path):
    a,b = tmp_path/'a.csv',tmp_path/'b.csv'
    a.write_text('id,valor,opcional\n001,x,\n');b.write_text('id,valor\n001,x\n')
    r=validar_partes_csv({'a':a,'b':b},['id','valor'],['id','valor','opcional'])
    assert r['estado']=='PENDENTE' and r['sobreposicoes']==0
    assert r['potenciais_sobreposicoes_sob_esquemas_distintos']==1
    assert r['partes'][1]['campos_opcionais_ausentes']==['opcional']
    assert r['linhas']==2  # nenhuma deduplicação ou imputação automática


def test_edicao_legitima_explicitada_sem_equivalencia_implicita(tmp_path):
    a,b = tmp_path/'a.csv',tmp_path/'b.csv'
    a.write_text('id,valor,opcional\n001,x,z\n');b.write_text('id,valor\n002,y\n')
    contrato={'id':'edicao_fixture','evidencia':'teste sintético; não layout oficial',
              'partes':{'a':{'campos':['id','valor','opcional']},'b':{'campos':['id','valor']}}}
    r=validar_partes_csv({'a':a,'b':b},['id','valor'],['id','valor','opcional'],contrato_edicao=contrato)
    assert r['estado']=='APROVADO' and r['esquemas_heterogeneos']
