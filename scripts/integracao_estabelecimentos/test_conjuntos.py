import unittest
import numpy as np
import pandas as pd
from conjuntos import alguma_competencia, codificar, contagens, matriz_distinta

class TestConjuntos(unittest.TestCase):
    def test_particao_completa_e_inclusivas(self):
        valores=np.arange(8)
        ex,inc=contagens(valores,3)
        np.testing.assert_array_equal(ex,np.ones(8))
        np.testing.assert_array_equal(inc,[8,4,4,2,4,2,2,1])

    def test_temporalidade_e_multiplicidade(self):
        # A unidade 0 tem A e B em meses distintos; a unidade 1 tem ambos em dois meses.
        idx=np.array([0,0,1,1]);mask=np.array([2,1,3,3])
        sem,sim=alguma_competencia(idx,mask,2,2)
        self.assertEqual(sem[3],1);self.assertEqual(sim[3],1)
        self.assertEqual(sim[2],2);self.assertEqual(sim[1],2)
        anual=np.zeros(2,dtype=int);np.bitwise_or.at(anual,idx,mask)
        self.assertEqual(contagens(anual,2)[1][3],2)

    def test_dominios_e_chaves(self):
        with self.assertRaises(ValueError):codificar(np.array([[1,2]]))
        for ids,v in [(["01","01"],["1","0"]),(["01",None],["1","0"]),(["01","02"],["1","?"])]:
            with self.assertRaises(ValueError):matriz_distinta(pd.DataFrame({"id":ids,"A":v}),"id",["A"])
        result=matriz_distinta(pd.DataFrame({"id":["01","02"],"A":["0","0"]}),"id",["A"])
        self.assertEqual(list(result.exclusiva),[2,0])

if __name__=="__main__":unittest.main()
