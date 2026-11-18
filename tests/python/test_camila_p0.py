import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from observatorio_sus.estudos.camila import sim
from observatorio_sus.estudos.camila.lote import executar
from observatorio_sus.io.custodia import sha256_arquivo


class CamilaP0(unittest.TestCase):
    def test_dupla_leitura_e_aceite(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            z=base/"edicao.zip"
            with ZipFile(z,"w") as f:
                f.writestr("m.csv","TIPOBITO;DTOBITO;CODMUNRES;CAUSABAS;IDADE\n"
                           "2;1012022;320330;I50.0;460\n2;01012022;329999;I501;599\n"
                           "2;15022022;320330;i50.9;405\n2;15022022;320330;I50;401\n"
                           "2;15022022;320330;I5.0;402\n2;15022022;320330;;402\n"
                           "2;15022022;320330;I210;420\n2;31022022;320330;I509;499\n"
                           "2;01012021;320330;I50;402\n1;01012022;320330;I50;402\n"
                           "2;01012022;330001;I50;402\n")
            fontes=base/"edicoes.csv"
            fontes.write_text(f"ano,membro,bytes,sha256\n2022,m.csv,{z.stat().st_size},{sha256_arquivo(z)}\n")
            with patch.object(sim,"FONTES",fontes):
                dst=base/"lote"
                resultado=sim.diagnosticar(z,2022,dst,True)
                self.assertEqual(resultado["controles"]["G0"],5)
                self.assertEqual(resultado["controles"]["subcategorias"],dict(I500=1,I501=1,I509=1,I50=1))
                self.assertEqual(resultado["controles"]["qa"],dict(origem=11,res_es_tipo2=9,elegiveis=7,
                        INVALIDA=1,AUSENTE=1,data_invalida=1,outro_ano=1))
                with (dst/"csv.csv").open() as f:
                    self.assertTrue(any(r["regiao"]=="RES_ES_IGNORADO" for r in csv.DictReader(f)))
                (dst/"dupla_leitura.json").write_text("{}")
                with self.assertRaises(ValueError):
                    sim.diagnosticar(z,2022,dst,True)
                z.write_bytes(b"outra edicao")
                with self.assertRaises(ValueError):
                    sim.diagnosticar(z,2022,dst)

    def test_interrupcao_e_retomada(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            dst=base/"completo"
            entrada=base/"entrada"
            entrada.write_text("v1")
            def calcular(stage):
                (stage/"arquivo").write_text("ok")
                return {"linhas":1}
            with patch("observatorio_sus.estudos.camila.lote.os.rename",side_effect=OSError("interrupcao")):
                with self.assertRaises(OSError):
                    executar(dst,{"entrada":entrada},{},calcular)
            self.assertFalse(dst.exists())
            a=executar(dst,{"entrada":entrada},{},calcular)
            self.assertEqual(a,executar(dst,{"entrada":entrada},{},calcular))
            entrada.write_text("v2")
            with self.assertRaises(ValueError):
                executar(dst,{"entrada":entrada},{},calcular)
            self.assertEqual(json.loads((dst/"recibo.json").read_text()),a)
