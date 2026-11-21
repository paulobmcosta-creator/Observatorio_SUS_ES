from contextlib import contextmanager
from hashlib import sha256
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from observatorio_sus.estudos.camila.assistencia import estoque_medio, situacao
from observatorio_sus.estudos.camila.sigtap import CONSULTA, avaliar_pa
from observatorio_sus.extract.envelope_datasus import EnvelopeMensal, consulta

class Pilotos(unittest.TestCase):
    def test_estoque_e_residencia(self):
        s=estoque_medio({"202401":0,"202412":6})
        self.assertEqual((s["media"],s["competencias"],s["meses_ativos"]),(3,2,1))
        self.assertEqual(situacao("330001",{}),"OUTRA_UF_CODIGO_PLAUSIVEL")
        self.assertEqual(situacao("999999",{}),"INDETERMINADO_OU_EXTERIOR")
        self.assertEqual(situacao("329999",{}),"ES_SEM_MUNICIPIO_VALIDO")

    def test_pa_cbo_mensal_e_quantidade_aprovada(self):
        r=dict(PA_CMP="202412",PA_QTDAPR="0",PA_QTDPRO="2",PA_PROC_ID=CONSULTA,PA_CBOCOD="225120")
        args=("202412",{CONSULTA},{(CONSULTA,"225120")},{CONSULTA},{"225120"})
        self.assertEqual(avaliar_pa(r,*args),("elegivel",0,2))
        self.assertEqual(avaliar_pa(dict(r,PA_CBOCOD="999999"),*args)[0],"consulta_cbo_incompativel")
        with self.assertRaises(ValueError):
            avaliar_pa(dict(r,PA_CMP="202411"),*args)
        with self.assertRaises(ValueError):
            avaliar_pa(dict(r,PA_QTDAPR=""),*args)

    def test_transporte_envelope(self):
        nome="PAES2411.dbc"
        uri="ftp://ftp.datasus.gov.br/dissemin/publicos/SIASUS/200801_/Dados/"+nome
        obj=dict(familia="PA",uf="ES",competencia="202411",caminho=nome,uri_oficial=uri,
                 revisao="edicao_sintetica",limite_bytes=10)
        url="https://datasus.saude.gov.br/wp-content/zipupload/Arq_1/arquivo.zip"
        envelope=io.BytesIO()
        with ZipFile(envelope,"w") as z:
            z.writestr(nome,b"teste")
        dados=envelope.getvalue()
        class Cliente:
            @contextmanager
            def abrir(self,objeto):
                yield io.BytesIO(dados),dict(uri_efetiva=url,headers={"Content-Length":str(len(dados))})
        with tempfile.TemporaryDirectory() as temp:
            fonte=EnvelopeMensal(temp,len(dados),Cliente())
            def post(endpoint,form,limite):
                if endpoint=="/ftp.php":
                    self.assertEqual(form["uf[]"],"ES")
                    return [dict(arquivo=nome,fonte="SIASUS",endereco=uri)],"a"*64
                self.assertEqual(form["dados[0][link]"],uri)
                return [[url]],"b"*64
            with patch.object(fonte,"_post",side_effect=post):
                with fonte.abrir(obj) as (stream,meta):
                    self.assertEqual(stream.read(),b"teste")
                    self.assertEqual(meta["sha256_envelope"],sha256(dados).hexdigest())
                    self.assertEqual(meta["uri_oficial"],uri)
                    self.assertEqual(meta["headers"]["Content-Length"],"5")
                with self.assertRaises(ValueError),fonte.abrir(dict(obj,limite_bytes=3)):
                    pass
                with self.assertRaises(ValueError):
                    consulta(dict(obj,uf="RJ"))
