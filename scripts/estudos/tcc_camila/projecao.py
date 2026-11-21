"""Projetar apenas agregados certificados. Todas as saídas têm esquema explícito."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
INDICADORES = (
    "habitantes obitos sim_bruta sim_direta_2022 sim_prematura_direta_2022 "
    "aih_residentes atendimento evasao_aih atracao_aih interregional_es evasao_pct "
    "sih_direta_2022 cnes_media_SR_CARD cnes_media_EQ_441_QT_EXIST "
    "cnes_media_LT_32_QT_SUS pa_aprovadas_ECG pa_aprovadas_demais_exames "
    "pa_aprovadas_fisioterapia pa_aprovadas_especificos pa_apresentadas_especificos"
).split()

def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()

def salvar(frame, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, lineterminator="\n")

def projetar(origem, saida):
    cfg = json.loads((HERE / "fontes_agregadas.json").read_text(encoding="utf8"))
    def ler(chave):
        meta = cfg[chave]
        path = origem / meta["caminho"]
        if sha(path) != meta["sha256"]:
            raise ValueError("Edição divergente em " + chave)
        return pd.read_csv(path, dtype={"padrao": str}, float_precision="round_trip")
    table = ler("T29")
    if table.duplicated(["ano", "territorio"]).any():
        raise ValueError("Duplicação de ano e território")
    salvar(table[["ano","territorio",*INDICADORES]], saida / "t29_selecao.csv")
    dictionary = ler("dicionario")
    dictionary = dictionary[dictionary.id.str.startswith("T29.")].copy()
    if len(dictionary)!=51 or dictionary.id.nunique()!=51:
        raise ValueError("Dicionário incompatível com a edição")
    dictionary["na_selecao"] = dictionary.id.str.removeprefix("T29.").isin(INDICADORES)
    salvar(dictionary[["id","nome","unidade","formula","numerador","denominador","sistema","temporalidade","limitacoes","na_selecao"]], saida / "dicionario_t29.csv")
    cols = ["tema","ano","territorio","padrao","exclusiva_anual","inclusiva_anual","inclusiva_em_algum_mes","universo","uniao"]
    venn = pd.concat([ler(k)[cols] for k in ("V01","V02","V03")], ignore_index=True)
    salvar(venn, saida / "particoes_es.csv")
    temporal = ler("T01").query("territorio == 'ES' and padrao == '111'")
    salvar(temporal[["ano","inclusiva_anual","inclusiva_em_algum_mes"]], saida / "sr116_temporal_es.csv")
    sim = ler("I50")
    if not (sim.i50_original - sim.saida + sim.entrada == sim.i50_final).all():
        raise ValueError("Balanço original/final incompatível")
    salvar(sim[["ano","i50_original","i50_final","ampliada","mencao_uniao","entrada","saida"]], saida / "i50_es.csv")
    pa = ler("PA").query("classe == 'A' and estado == 'elegível na janela delimitada'")
    if pa.duplicated(["competencia","codigo"]).any() or len(pa)!=132 or pa[["congelada","adicional","janela_estendida"]].isna().any().any():
        raise ValueError("Domínio clínico ou janela incompletos")
    pa = pa.groupby("competencia", as_index=False)[["congelada","adicional","janela_estendida"]].sum(min_count=1)
    if not np.allclose(pa.congelada+pa.adicional, pa.janela_estendida):
        raise ValueError("As duas janelas não reconciliam")
    salvar(pa, saida / "pa_janelas_es.csv")
