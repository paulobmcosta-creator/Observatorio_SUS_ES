"""Regressão de IDs analíticos com títulos diferentes entre edições oficiais."""
from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/"scripts"))
from corrigir_servicos_camila import dicionario


def test_chave_preserva_descricoes_edicoes_e_cbo(tmp_path):
    colunas = "id familia titulo unidade codigos filtro formula status limitacao fonte temporalidade territorio teste script".split()
    itens = []
    for titulo in ["Consulta anterior", "Consulta revista"]:
        row = dict.fromkeys(colunas, "sintético")
        row.update(id="PA_0301010072", familia="PA", titulo=titulo, codigos="0301010072")
        itens.append(row)
    original = tmp_path/"catalogo.csv"
    pd.DataFrame(itens).to_csv(original,index=False)
    historico = tmp_path/"historico.csv"
    meses = ["202401","202402","202403"]
    pd.DataFrame([(m,"0301010072",t,"1",i+1) for i,(m,t) in enumerate(zip(meses,["Consulta anterior","Consulta revista","Consulta anterior"]))],
                 columns=["competencia","codigo","descricao","presente","versao_atributos"]).to_csv(historico,index=False)
    edicoes = {}
    for m in meses:
        edicoes[m] = tmp_path/(m+".txt")
        edicoes[m].write_text(m,encoding="ascii")
    dominio = pd.DataFrame(columns=["competencia","classe_sr","vigente","titulo_servico","titulo_classe","decisao","justificativa"])
    dominio["vigente"] = dominio.vigente.astype(bool)
    cat = dicionario(original,historico,edicoes,dominio,"regra")
    assert cat.id.tolist() == ["PA_0301010072"]*3
    assert cat.titulo.tolist() == ["Consulta anterior","Consulta revista","Consulta anterior"]
    assert cat.chave_historica.is_unique
    assert all(cat.filtro.str.contains(cbo).all() for cbo in ["225120","225210","225203"])
