import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from observatorio_sus.estudos.camila import populacao, sim
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
                        INVALIDA=1,AUSENTE=1,data_invalida=1,outro_ano=1,I50_com_ponto=2,I50_sem_ponto=2,
                        I50_apenas_apos_retirada_irrestrita_de_pontos=1))
                with (dst/"csv.csv").open() as f:
                    self.assertTrue(any(r["regiao"]=="RES_ES_IGNORADO" for r in csv.DictReader(f)))
                (dst/"dupla_leitura.json").write_text("{}")
                with self.assertRaises(ValueError):
                    sim.diagnosticar(z,2022,dst,True)
                z.write_bytes(b"outra edicao")
                with self.assertRaises(ValueError):
                    sim.diagnosticar(z,2022,dst)

    def test_margem_municipal_fora_dos_sete_anos_impede_promocao(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)
            dem=base/"dem.csv"
            municipios=populacao.mapa()
            campos=["co_anomes","co_ibge","co_uf","sg_granularidade","sg_categoria","ds_item_categoria","vl_indicador_calculado_mun"]
            with dem.open("w",newline="") as stream:
                w=csv.writer(stream)
                w.writerow(campos)
                for ano in range(2014,2025):
                    for municipio in municipios:
                        chave=[str(ano)+"12",municipio,"32","MN"]
                        w.writerows([*chave,"Idade",idade,1] for idade in populacao.IDADES)
                        w.writerow([*chave,"PESSOA1","Feminino",41])
                        w.writerow([*chave,"PESSOA1","Masculino",40])
                        w.writerow([*chave,"TC","Total",82 if (ano,municipio)==(2014,"320010") else 81])
            def calcular(stage):
                return populacao.conferir({"dem":dem},stage,municipios)
            with self.assertRaisesRegex(ValueError,"divergência entre total municipal"):
                executar(base/"validado",{"dem":dem},{},calcular)
            self.assertFalse((base/"validado").exists())
            self.assertFalse(list(base.rglob("MORTALIDADE*.csv")))
            self.assertEqual(len(list(base.rglob("RIPSA_DEM101_QA_TOTAIS.csv"))),1)

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
            from observatorio_sus.io.custodia import escrever_json
            def falhar_no_recibo(path,valor):
                if path.name=="recibo.json":
                    raise OSError("falha entre arquivo e recibo")
                escrever_json(path,valor)
            with patch("observatorio_sus.estudos.camila.lote.escrever_json",side_effect=falhar_no_recibo):
                with self.assertRaises(OSError):
                    executar(dst,{"entrada":entrada},{},calcular)
            self.assertFalse(dst.exists())
            a=executar(dst,{"entrada":entrada},{},calcular)
            self.assertEqual(a,executar(dst,{"entrada":entrada},{},calcular))
            entrada.write_text("v2")
            with self.assertRaises(ValueError):
                executar(dst,{"entrada":entrada},{},calcular)
            self.assertEqual(json.loads((dst/"recibo.json").read_text()),a)
