import unittest
from observatorio_sus.transform.padronizacao import direta, pesos


class PadronizacaoTest(unittest.TestCase):
    def test_comparacao_por_sexo_com_pesos_comuns(self):
        w = pesos({0:30,80:70},[0,80])
        self.assertEqual(direta({0:0,80:3},{0:50,80:100},w),2100)
        self.assertIsNone(direta({0:0,80:3},{0:50,80:0},w))
        self.assertIsNone(direta({0:0},{0:50,80:100},w))
        self.assertEqual(direta({0:0,80:0},{0:50,80:100},w),0)
        with self.assertRaises(ValueError):
            direta({0:1},{0:2},{0:0.9})

    def test_renormalizacao(self):
        self.assertEqual(pesos({0:10,30:40,35:60,80:90},[30,35]),{30:0.4,35:0.6})
