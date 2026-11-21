"""Contratos de integração em dados inteiramente sintéticos."""
import unittest
from pathlib import Path
import duckdb
SQL=Path(__file__).resolve().parent
class TesteIntegracao(unittest.TestCase):
    def setUp(self):
        self.con=duckdb.connect()
    def tearDown(self):
        self.con.close()
    def test_uniao_e_sobreposicao(self):
        c=self.con
        c.execute("""CREATE TABLE cadastro AS SELECT '202401' mes,cnes,'320001' municipio,'1' VINC_SUS,'01' TP_UNID,'1' NAT_JUR,'M' TPGESTAO,'1' ATENDAMB,'1' ATENDHOS FROM (VALUES ('0000001'),('0000003')) t(cnes);
        CREATE TABLE rsum AS SELECT mes,cnes,municipio,true especifico,true estrutura_hosp,true sr,false hab FROM cadastro;
        CREATE TABLE amb AS SELECT '202401' mes,'0000001' cnes,'320001' municipio,3 especificas,4 apresentadas,5 contextuais;
        CREATE TABLE hosp AS SELECT '202401' mes,cnes,'320002' municipio,2 aih FROM (VALUES ('0000001'),('0000002')) t(cnes);""")
        c.execute((SQL/"integracao_geral.sql").read_text(encoding="utf8"))
        self.assertEqual(c.execute("SELECT cnes,cadastrado,situacao FROM matriz ORDER BY cnes").fetchall(),[("0000001",True,"ambos"),("0000002",False,"apenas_SIH"),("0000003",True,"nenhum")])
        self.assertEqual(c.execute("SELECT sum(aih),sum(aprovadas),sum(contextuais),count_if(conflito_territorial) FROM matriz").fetchone(),(4,3,5,1))
    def test_residencia_independe_de_coincidencia(self):
        c=self.con
        c.execute("""CREATE TABLE dominio_municipal AS SELECT '320001' codigo;
        CREATE TABLE geo AS SELECT '320001' municipio,'R' regiao;
        CREATE TABLE elegivel AS SELECT row_number() OVER() k,instrumento,residencia,'320001' municipio FROM (VALUES ('C','320001'),('C','999999'),('I','320001'),('P','000000'),('S',NULL),('A','320001'),('X','320001')) d(instrumento,residencia)""")
        rows=c.execute("SELECT left(situacao_residencia,1) FROM ("+(SQL/"residencia_geral.sql").read_text(encoding="utf8")+") ORDER BY k").fetchall()
        self.assertEqual([i[0] for i in rows],list("2213345"))
if __name__=="__main__":unittest.main(verbosity=2)
