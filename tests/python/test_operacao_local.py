"""Caminhos com espaços, volumes compartilhados e bloqueio antes de materializar."""
import json
from pathlib import Path
from collections import namedtuple
import pytest
from observatorio_sus.io.operacao_local import ler_configuracao, preflight


def config(tmp_path):
    repo=tmp_path/'repo';repo.mkdir()
    c={k:str(tmp_path/'dados externos'/k) for k in ['data_root','cache','temporarios','saida','backup']}
    c.update(margem_livre_bytes=10,concorrencia_max=1)
    p=tmp_path/'config local.json';p.write_text(json.dumps(c))
    return ler_configuracao(p,repo)


def test_soma_no_mesmo_volume_e_margem_no_limite(tmp_path):
    c=config(tmp_path);uso=namedtuple('Uso','free')
    r=preflight(c,[{'bytes':20,'limite_bytes':25}],limite_derivados_bytes=30,limite_temporarios_bytes=5,
                backup_novo_bytes=10,medir=lambda _:uso(80))
    assert r['estado']=='APTO_NOS_LIMITES_DECLARADOS' # 25+30+5+10+10
    r=preflight(c,[{'bytes':20,'limite_bytes':25}],limite_derivados_bytes=30,limite_temporarios_bytes=5,
                backup_novo_bytes=10,medir=lambda _:uso(79))
    assert r['estado']=='BLOQUEADO_ESPACO'
    assert not (tmp_path/'dados externos').exists()


def test_fila_nominal_nao_inventa_volume(tmp_path):
    c=config(tmp_path)
    assert preflight(c,[{'nome':'RDES2401.dbc'}],limite_derivados_bytes=0,limite_temporarios_bytes=0)['estado']=='BLOQUEADO'
    assert preflight(c,[{'bytes':10}],limite_temporarios_bytes=0)['estado']=='BLOQUEADO'


def test_recusar_dados_ou_config_no_checkout(tmp_path):
    repo=tmp_path/'repo';repo.mkdir();p=repo/'config.json';p.write_text('{}')
    with pytest.raises(ValueError,match='fora do checkout'):ler_configuracao(p,repo)
