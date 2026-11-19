"""Controles sintéticos dos recortes clínicos e temporais do módulo do TCC."""
import sys
import unittest
from pathlib import Path

import duckdb

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts"))
from historico_clinico_camila import classe, REAB, EXAMES, DOPPLER
from integrar_oferta_camila import registro_pa_sql
from qualificar_particoes_camila import situacao_equipe
from observatorio_sus.estudos.camila.sigtap import CONSULTA


class AssistenciaQualificada(unittest.TestCase):
    def test_recortes_mutuamente_exclusivos(self):
        self.assertEqual(len(set(EXAMES)),8)
        self.assertEqual({c for c in REAB if classe(c)[0]=="A"}, {REAB[1],REAB[2],REAB[4]})
        self.assertTrue(all(classe(c)==("A","exames_especificos") for c in EXAMES))
        self.assertEqual(classe(DOPPLER),("B","doppler_contextual"))
        self.assertEqual(classe(CONSULTA),("B","consulta_cbo"))
        self.assertEqual(classe("0406030014")[0],"D")

    def test_apac_principal_secundaria_e_origem_desconhecida(self):
        with duckdb.connect() as db:
            resultado=db.execute("SELECT "+registro_pa_sql("c")+" FROM (VALUES ('P'),('S'),('I'),('C'),('A'),('B'),('?')) t(c)").fetchall()
        self.assertEqual(resultado,[("06",),("07",),("02",),("01",),("08",),("09",),(None,)])

    def test_vigencia_equipes(self):
        self.assertEqual(situacao_equipe("201901","900001","00","202012"),"ativa_ao_fim")
        self.assertEqual(situacao_equipe("201901","202012","01","202012"),"desativada_na_competencia")
        self.assertEqual(situacao_equipe("201901","201912","01","202012"),"fora_da_competencia")
        self.assertEqual(situacao_equipe("201913","900001","00","202012"),"datas_indeterminadas")
