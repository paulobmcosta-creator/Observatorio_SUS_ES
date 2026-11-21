import io
import json
import sys
import unittest
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.error import URLError
from zipfile import ZipFile

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import confrontar_sim_camila as contraste
import obter_edicoes_sim_camila as aquisicao
from observatorio_sus.estudos.camila import sim
from observatorio_sus.estudos.camila.lote import ler, salvar
from observatorio_sus.io.custodia import sha256_arquivo


class Edicoes(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.local = self.root / "autorizado"
        self.local.mkdir()
        self.zip = self.local / "edicao_renomeada.zip"
        self.membro = "Mortalidade_Geral_2014.csv"
        with ZipFile(self.zip, "w") as z:
            z.writestr(self.membro, "TIPOBITO;DTOBITO;CODMUNRES;CAUSABAS;IDADE\n"
                "2;1012014;320330;I50.0;460\n2;02012014;329999;I509;465\n"
                "2;03012014;320330;I21;498\n1;03012014;320330;I50;400\n")
        self.fontes = self.root/"edicoes.csv"
        salvar(self.fontes,["ano","url","membro","bytes","sha256","last_modified"],
               [(2014,"https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SIM/csv/teste.zip",
                 self.membro,self.zip.stat().st_size,sha256_arquivo(self.zip),"fixture")])

    def test_custodia_prioritaria_e_retomada_https(self):
        vazio = self.root/"vazio"
        vazio.mkdir()
        destino = self.root/"dados"
        dados = self.zip.read_bytes()
        class Fonte:
            @contextmanager
            def abrir(self,obj):
                yield io.BytesIO(dados), {"uri_efetiva":obj["uri_oficial"],"headers":{"Content-Length":str(len(dados))}}
        with patch.object(aquisicao,"FONTES",self.fontes),patch.object(aquisicao,"HTTPSOficial",return_value=Fonte()):
            self.assertEqual(aquisicao.obter([vazio],destino,[2014],True),0)
        with patch.object(aquisicao,"FONTES",self.fontes),patch.object(aquisicao.HTTPSOficial,"abrir",side_effect=AssertionError):
            self.assertEqual(aquisicao.obter([vazio],destino,[2014],True),0)
            self.assertEqual(aquisicao.obter([self.local],self.root/"destino2",[2014],True),0)
        estados = {json.loads(f.read_text())["estado"] for f in destino.glob("consulta-*/2014.json")}
        self.assertEqual(estados,{"oficial_verificado","custodia_por_sha256"})

    def test_recusa_registrada_sem_objeto_promovido(self):
        pasta = self.root/"vazio"
        pasta.mkdir()
        destino = self.root/"bloqueado"
        with patch.object(aquisicao,"FONTES",self.fontes),patch.object(aquisicao.HTTPSOficial,"abrir",side_effect=URLError("teste de recusa")):
            self.assertEqual(aquisicao.obter([pasta],destino,[2014],True),1)
        self.assertEqual(json.loads(next(destino.glob("consulta-*/2014.json")).read_text())["estado"],"impedimento")
        self.assertFalse((destino/"SIM/2014/versoes").exists())

    def test_original_grupos_residuo_e_taxas(self):
        entradas={}
        def fixture(nome,campos,linhas):
            arq=self.root/(nome+".csv")
            salvar(arq,campos.split(),linhas)
            entradas[nome]=arq
        territorios=("ES",*contraste.REGIOES)
        fixture("cp02","ano territorio grupo obitos",[(2014,t,g,0) for t in territorios for g in contraste.GRUPOS])
        fixture("inicial","ano territorio grupo obitos status",[(2014,t,g,0,"teste") for t in territorios for g in contraste.GRUPOS])
        fixture("brutas","ano territorio grupo taxa_100mil",[(2014,t,g,"0.000000") for t in territorios for g in contraste.GRUPOS])
        fixture("qa_inicial","ano controle valor",[])
        fixture("taxas","ano territorio obitos_30_69 taxa_padronizada_100mil estado_padronizacao",[(2014,t,0,"","pendente") for t in territorios])
        fixture("pop","ano territorio faixa habitantes",[(2014,t,f,1000 if f=="TODAS" else 800 if f=="30_69" else 100) for t in territorios for f in ("TODAS","30_69",*contraste.PESOS)])
        fixture("pesos","idade_inicio peso_30_69",[(f,0.125) for f in contraste.PESOS])
        destino=self.root/"calculado"
        with patch.object(contraste,"fontes",return_value=entradas),patch.object(sim,"FONTES",self.fontes):
            contraste.processar(self.root,[self.local],destino,[2014])
        linha=next(r for r in ler(destino/"confronto_anual.csv") if r["territorio"]=="ES" and r["grupo"]=="G2")
        self.assertEqual((linha["original"],linha["delta_original_CP02"],float(linha["taxa_original_100mil"])),("2","2",200.0))
        estado=next(r for r in ler(destino/"prematura_desde_original.csv") if r["territorio"]=="ES")
        self.assertEqual((estado["obitos"],float(estado["taxa_padronizada_100mil"])),("2",250.0))
        self.assertTrue(any(r["territorio"]=="RES_ES_IGNORADO" and r["I50"]=="1" for r in ler(destino/"i50_por_idade.csv")))
