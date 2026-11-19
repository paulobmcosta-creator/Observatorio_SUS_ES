"""Controles sintéticos da cobertura por arquivo, da conversão SIH e dos fluxos."""
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts"))
from completar_sih_nacional_camila import catalogo
from consolidar_sih_camila import consolidar
from fechar_cobertura_sih_camila import fluxo_regional
from indicadores_sih_nacional_camila import estratos, tabela_cnv
from observatorio_sus.estudos.camila.lote import ler, produtos, salvar
from observatorio_sus.extract.envelope_datasus import UFS


class CoberturaNacional(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.v = self.root/"custodia"
        self.lista = self.v/"fontes/rd-lista-ftp.txt"
        self.lista.parent.mkdir(parents=True)
        self.catalogo = [f"registro 900 RD{uf}{ano:02}{mes:02}.dbc" for ano in range(14,25)
                         for mes in range(1,13) for uf in sorted(UFS)]
        self.lista.write_text("\n".join(self.catalogo))

    def test_recusa_particao_ausente_duplicada_e_adicional(self):
        self.assertEqual(len(catalogo(self.lista)),132*27)
        for linhas in (self.catalogo[:-1],self.catalogo+[self.catalogo[-1]],self.catalogo+["outro 1 RDSP1410B.dbc"]):
            self.lista.write_text("\n".join(linhas))
            with self.assertRaises(ValueError):
                catalogo(self.lista)

    def test_checkpoint_e_original_recuperado(self):
        cp04 = self.root/"acervo/CP04/Resultados"
        cp04.mkdir(parents=True)
        salvar(cp04/"SIH_PILOTO_FLUXOS.csv",["competencia_processamento","origem_residencia","destino_atendimento","aih_g0_ident1"],
               [("202411","Sul","Sul",2),("202411","RES_OUTRA_UF_OU_INDETERMINADA","Sul",1)])
        salvar(cp04/"SIH_PILOTO_PRODUCAO.csv",["competencia_processamento","atendimento","grupo","aih_ident1"],
               [("202411","ES","G0",3)])
        antigo = self.root/"anterior"
        consolidar(self.v,antigo)
        def novembro(p):
            return next(r for r in ler(p/"serie.csv") if r["competencia"]=="202411")
        self.assertEqual(novembro(antigo)["atracao_plausivel"],"")
        self.assertEqual(novembro(antigo)["residentes_observados"],"2")
        self.assertEqual(novembro(antigo)["residentes_cobertura_nacional"],"")
        part = self.v/"sih/RDES2411/202411"
        part.mkdir(parents=True)
        campos = "competencia uf_arquivo municipio_res regiao_res municipio_atend regiao_atend diagnostico sexo_sih unidade_idade idade aih"
        salvar(part/"fluxos.csv",campos.split(),[
            ("202411","ES","320120","Sul","320120","Sul","I500","3","4","72",2),
            ("202411","ES","330045","OUTRA_UF_CODIGO_PLAUSIVEL","320120","Sul","I50","1","4","63",1)])
        (part/"recibo.json").write_text(json.dumps({"saidas":produtos(part)}))
        novo = self.root/"novo"
        consolidar(self.v,novo)
        linha = novembro(novo)
        self.assertEqual((linha["atendimento_es"],linha["residentes_observados"],linha["atracao_plausivel"]),("3","2","1"))
        self.assertEqual(linha["residentes_cobertura_nacional"],"")

    def test_conversao_com_residuo_e_limite_aberto(self):
        tab = tabela_cnv(b"4 3\n 19 Ign 000-999\n 1 M0 100-312,400\n 2 A0 401-404\n 18 A80 480-599\n")
        sx = tabela_cnv(b"3 1\n 3 Ign 0-9\n 1 M 1\n 2 F 2,3\n")
        for uni,idade,sexo,esperado in [("4","04","2",("F",0)), ("2","07","3",("F",0)),
                                       ("5","01","1",("M",80)), ("9","99","0",("IGN",-1)),
                                       ("4","","3",("F",-1)), ("4","80","1",("M",80))]:
            self.assertEqual(estratos({"unidade_idade":uni,"idade":idade,"sexo_sih":sexo},tab,sx),esperado)

    def test_fluxo_regional_com_destino_desconhecido(self):
        campos = "competencia regiao_res uf_atendimento regiao_at uf_res_ibge uf_at_municipio aih"
        salvar(self.root/"fluxos_mensais.csv",campos.split(),[
            ("202001","Sul","ES","Sul","32","32",9),("202001","Sul","ES","Central","32","32",2),
            ("202001","Sul","RJ","OUTRA_UF_CODIGO_PLAUSIVEL","32","33",1),
            ("202001","Sul","ES","ES_SEM_MUNICIPIO_VALIDO","32","32",3),
            ("202001","OUTRA_UF_CODIGO_PLAUSIVEL","ES","Sul","33","32",7)])
        fluxo_regional(self.root)
        sul = next(r for r in ler(self.root/"indicadores_regionais.csv") if r["regiao"]=="Sul")
        self.assertEqual(sul["residentes"],"15")
        self.assertEqual(float(sul["evasao_regional_conhecida_pct"]),20)
        self.assertEqual(sul["destino_comparavel_aih"],"12")
        self.assertEqual(float(sul["evasao_pct_dos_destinos_comparaveis"]),25)
        self.assertEqual((sul["atendimento_na_regiao"],sul["atracao_de_outra_uf"]),("16","7"))
        self.assertEqual(sul["destino_externo_principal"],"Central")
