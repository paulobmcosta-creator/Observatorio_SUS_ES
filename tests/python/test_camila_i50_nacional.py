import csv
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import investigar_i50_nacional as estudo
from observatorio_sus.estudos.camila.lote import ler


class Nacional(unittest.TestCase):
    def test_eligibilidade_mencao_e_datas(self):
        campos = list(dict.fromkeys(["TIPOBITO", "DTOBITO", "CODMUNRES", *estudo.EXAMINAR]))
        stream = io.StringIO()
        writer = csv.DictWriter(stream, [c.lower() for c in campos], delimiter=";")
        writer.writeheader()
        modelo = dict(tipobito="2", dtobito="1012024", codmunres="329999", causabas="I11.0",
                      causabas_o="I509", cb_pre="I50", atestado="I50.9/I500*I110",
                      linhaa="*I509*I500", dtcadastro="01012025", versaoscb="4,3")
        for alteracoes in ({}, {"causabas": "I500", "atestado": "XI50.9 I5000", "linhaa": ""},
                           {"dtobito": "31022024"}, {"dtobito": "01012023"},
                           {"codmunres": "999999"}, {"tipobito": "1"}):
            writer.writerow(modelo | alteracoes)
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            resultado = estudo.analisar(io.BytesIO(stream.getvalue().encode("latin1")), 2024, pasta)
            self.assertEqual(dict(resultado["qa"]), dict(origem=6, elegiveis=2, data_invalida=1,
                             outro_ano=1, sem_UF_brasileira=1, tipo_excluido=1))
            linhas = ler(pasta / "mensal.csv")
            self.assertEqual(len(linhas), 324)
            jan = next(r for r in linhas if r["uf"] == "ES" and r["mes"] == "1")
            self.assertEqual([jan[k] for k in ("G0", "I50", "I50_original", "I50_pre",
                             "mencao_atestado", "mencao_linhas", "I50_e_mencao")], list("2122110"))
            pares = ler(pasta / "matriz.csv")
            self.assertEqual(sum(int(r["n"]) for r in pares), 2)
            proc, = ler(pasta / "processamento.csv")
            self.assertEqual((proc["cadastro"], proc["scb"]), ("2025-01", "4.3"))

