"""Preparar candidato no schema v2 sem inventar vigência, códigos ou hashes de atos."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--candidato",required=True,type=Path);p.add_argument("--saida",required=True,type=Path)
    a=p.parse_args()
    schema=Path('metadata/territorio/schema_correspondencia_v2.csv')
    campos=[r['nome_campo'] for r in csv.DictReader(schema.open())]
    origem=list(csv.DictReader(a.candidato.open(encoding='utf-8-sig')))
    if len(origem)!=78 or len({r['cod_municipio_ibge'] for r in origem})!=78:raise ValueError('Candidato deve preservar os 78 municípios informados.')
    a.saida.mkdir(parents=True,exist_ok=False)
    extras=['codigo_datasus_candidato_nao_validado','estado','hash_derivado_origem_nao_e_hash_de_ato']
    hash_derivado=hashlib.sha256(a.candidato.read_bytes()).hexdigest()
    with (a.saida/'candidato_schema_v2.csv').open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=campos+extras,lineterminator='\n');w.writeheader()
        for ano in ['2020','2024']:
            for r in origem:
                row={c:'' for c in campos}
                row.update(versao_territorial='CANDIDATO_PDR_'+ano,cod_municipio_ibge=r['cod_municipio_ibge'],
                           regiao_nome=r['regiao_pdr'+ano],fonte_url=r['fonte_pdr'+ano],
                           codigo_datasus_candidato_nao_validado=r['cod_municipio_datasus_candidato'],
                           estado='PENDENTE_ATOS_VIGENCIA_CATALOGO',hash_derivado_origem_nao_e_hash_de_ato=hash_derivado)
                w.writerow(row)
    (a.saida/'limites.json').write_text(json.dumps({'linhas_candidatas':156,'empiricamente_aplicavel':False,
        'campos_propositalmente_vazios':['cod_municipio_cnes','regiao_id','vigencia_inicio','vigencia_fim','ato_referencia','sha256_fonte'],
        'motivo':'Originais integrais, eficácia e catálogo municipal não recebidos; código derivado não é correspondência oficial.'},ensure_ascii=False,indent=2)+'\n')
    print('156 linhas candidatas; aplicação empírica bloqueada por campos documentais ausentes.')
