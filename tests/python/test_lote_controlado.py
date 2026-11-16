"""O preflight bloqueia antes da fonte; cache é por identidade/revisão/hash."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import adquirir_lote_controlado as modulo
from test_operacao_local import config
from test_custodia import contrato, Memoria


def test_lote_sem_espaco_nao_abre_fonte(tmp_path,monkeypatch):
    c=config(tmp_path)
    monkeypatch.setattr(modulo,'preflight',lambda *a,**k:{'estado':'BLOQUEADO_ESPACO'})
    class Fonte:
        def abrir(self,objeto):raise AssertionError('não deve abrir fonte')
    plano={'objetos':[contrato('a',b'ab')],'limite_derivados_bytes':0,'limite_temporarios_bytes':0,'transporte':'snapshot'}
    r=modulo.executar_lote(c,plano,True,Fonte())
    assert r['aquisicao']=='NAO_INICIADA' and not c['data_root'].exists()


def test_cache_exato_nao_reconsulta_mesmo_com_pouco_espaco(tmp_path,monkeypatch):
    c=config(tmp_path)
    plano={'objetos':[contrato('a',b'ab')],'limite_derivados_bytes':0,'limite_temporarios_bytes':0,'transporte':'snapshot'}
    r=modulo.executar_lote(c,plano,True,Memoria({'a':b'ab'}))
    monkeypatch.setattr(modulo,'preflight',lambda *a,**k:{'estado':'BLOQUEADO_ESPACO'})
    class Fonte:
        def abrir(self,objeto):raise AssertionError('cache não deve reconsultar')
    novo=modulo.executar_lote(c,plano,True,Fonte())
    assert novo['conteudo_id']==r['conteudo_id'] and novo['aquisicao']=='CACHE_VALIDADO_SEM_NOVA_CONSULTA'
