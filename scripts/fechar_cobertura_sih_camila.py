"""Feche a matriz nacional do SIH e confronte as séries anuais com o leitor histórico."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from indicadores_sih_nacional_camila import REGIOES, proporcao, verificar_produtos
from observatorio_sus.estudos.camila import territorio
from observatorio_sus.estudos.camila.lote import executar, ler, produtos, salvar
from observatorio_sus.extract.envelope_datasus import UFS
from observatorio_sus.io.custodia import sha256_arquivo


def concatenar(stage, pastas, nome):
    """Concatene arquivos anuais com a mesma ordem de campos."""
    campos = None
    with (stage/nome).open("x", encoding="utf8", newline="") as dest:
        writer = csv.writer(dest)
        for pasta in pastas:
            with (pasta/nome).open(encoding="utf-8-sig", newline="") as src:
                linhas = csv.reader(src)
                header = next(linhas)
                if campos is None:
                    campos = header
                    writer.writerow(["ano",*header] if nome=="conversao_demografica.csv" else header)
                if header != campos:
                    raise ValueError(f"Esquema divergente em {pasta.name}/{nome}")
                if nome=="conversao_demografica.csv":
                    writer.writerows(([pasta.name,*linha] for linha in linhas))
                else:
                    writer.writerows(linhas)


def fluxo_regional(stage):
    """Particione os destinos e as origens do atendimento em cada região do PDR."""
    saidas, entradas, destinos, regional = (Counter() for _ in range(4))
    for r in ler(stage/"fluxos_mensais.csv"):
        ano, orig, uf, dest = r["competencia"][:4],r["regiao_res"],r["uf_atendimento"],r["regiao_at"]
        n = int(r["aih"])
        local = r["uf_res_ibge"]=="32"
        if local and orig in REGIOES:
            if uf!="ES":
                tipo, destino = "outra_uf",uf
            elif dest==orig:
                tipo, destino = "propria_regiao",dest
            elif dest in REGIOES:
                tipo, destino = "outra_regiao_es",dest
            else:
                tipo, destino = "at_es_sem_regiao",dest
            saidas[ano,orig,tipo] += n
            destinos[ano,orig,tipo,destino] += n
        if uf=="ES" and dest in REGIOES:
            if orig==dest:
                tipo = "propria_regiao"
            elif orig in REGIOES:
                tipo = "outra_regiao_es"
            elif local:
                tipo = "es_sem_regiao"
            elif orig=="OUTRA_UF_CODIGO_PLAUSIVEL":
                tipo = "outra_uf"
            else:
                tipo = "origem_indeterminada"
            entradas[ano,dest,tipo] += n
        regional[ano,orig,uf,dest,r["uf_res_ibge"]] += n
    linhas = []
    for ano in sorted({k[0] for k in regional}):
        for reg in REGIOES:
            s = [saidas[ano,reg,c] for c in ("propria_regiao","outra_regiao_es","outra_uf","at_es_sem_regiao")]
            e = [entradas[ano,reg,c] for c in ("propria_regiao","outra_regiao_es","outra_uf","es_sem_regiao","origem_indeterminada")]
            if s[0]!=e[0]:
                raise ValueError("Atendimentos da própria região divergentes nas duas margens")
            externos = [(n,d) for (a,o,c,d),n in destinos.items() if a==ano and o==reg and c in ("outra_regiao_es","outra_uf")]
            maximo = max((n for n,_ in externos),default=0)
            principais = "|".join(sorted(d for n,d in externos if n==maximo))
            linhas.append((ano,reg,sum(s),*s,proporcao(s[0],sum(s)),proporcao(s[1]+s[2],sum(s)),
                           proporcao(s[2],sum(s)),principais,maximo,sum(e),*e[1:],
                           proporcao(e[1]+e[2],sum(e)),proporcao(e[2],sum(e)),
                           sum(s[:3]),proporcao(s[1]+s[2],sum(s[:3])),
                           sum(e[:3]),proporcao(e[1]+e[2],sum(e[:3]))))
    salvar(stage/"indicadores_regionais.csv",("ano regiao residentes na_propria_regiao em_outra_regiao_es em_outra_uf "
            "at_es_sem_regiao propria_regiao_pct evasao_regional_conhecida_pct evasao_interestadual_pct destino_externo_principal "
            "aih_destino_principal atendimento_na_regiao atracao_de_outra_regiao_es atracao_de_outra_uf residentes_es_sem_regiao "
            "origem_indeterminada atracao_externa_regiao_conhecida_pct atracao_interestadual_pct "
            "destino_comparavel_aih evasao_pct_dos_destinos_comparaveis origem_comparavel_aih "
            "atracao_pct_das_origens_comparaveis").split(),linhas)
    salvar(stage/"matriz_regional_anual.csv","ano regiao_res uf_atendimento regiao_at uf_res_ibge aih".split(),
           ((*k,n) for k,n in sorted(regional.items())))


def indicadores_municipais(stage, denominadores):
    """Inclua os municípios com zero observado após validação das 27 UFs em cada mês."""
    mapa = territorio.mapa()
    habitantes = {}
    for r in ler(denominadores):
        k = (r["ano"], r["datasus6"])
        n = int(r["total"])
        if k in habitantes or n <= 0 or any(int(r[c])!=n for c in ("soma_idades","soma_sexos")):
            raise ValueError(f"Denominador municipal divergente: {k}")
        habitantes[k] = n
    if set(habitantes) != {(str(ano),m) for ano in range(2014,2025) for m in mapa}:
        raise ValueError("Cobertura dos denominadores municipais divergente")
    contagens, evasao = Counter(), Counter()
    for r in ler(stage/"municipios.csv"):
        k = r["competencia"][:4],r["municipio_res"]
        n = int(r["aih"])
        contagens[k] += n
        if r["uf_atendimento"]!="ES":
            evasao[k] += n
    for r in ler(stage/"indicadores_anuais.csv"):
        if r["territorio"]=="ES" and r["sexo"]=="T":
            ano = r["ano"]
            if (sum(n for (a,m),n in habitantes.items() if a==ano)!=int(r["habitantes"])
                    or sum(n for (a,m),n in contagens.items() if a==ano)!=int(r["aih_residentes"])
                    or sum(n for (a,m),n in evasao.items() if a==ano)!=int(r["evasao_aih"])):
                raise ValueError(f"Margens municipais de utilização divergentes: {ano}")
    linhas = []
    for k in sorted(habitantes.keys()|contagens.keys()):
        ano,m = k
        n,ev,pop = contagens[k],evasao[k],habitantes.get(k)
        linhas.append((ano,m,mapa.get(m,"ES_SEM_MUNICIPIO_VALIDO"),n,ev,proporcao(ev,n),pop,proporcao(n,pop,100000)))
    salvar(stage/"indicadores_municipais.csv","ano municipio_res regiao_res aih_residentes evasao_aih evasao_pct habitantes utilizacao_bruta_100mil".split(),linhas)


def qualidade_por_particao(stage, objetos):
    """Preserve o universo próprio dos controles do leitor integral e do leitor de residentes."""
    linhas = []
    for obj in objetos:
        arquivo = Path(obj["recibo_analitico"])
        if sha256_arquivo(arquivo)!=obj["sha256_recibo"]:
            raise ValueError(f"Recibo diverge do fechamento anual: {arquivo}")
        rec = json.loads(arquivo.read_text())["controles"]
        qa = rec["qa"]
        integral = "residentes_circulatorios" not in rec
        registros = qa.get("circulatorias_ident_1",0) if integral else rec["residentes_circulatorios"]
        universo = "G0 de todas as residências atendidas na UF" if integral else "G0 dos residentes do ES atendidos na UF"
        linhas.append((obj["competencia"],obj["uf"],universo,registros,qa.get("datas_inconsistentes",0),
                       qa.get("aih_sem_numero" if integral else "aih_ausente",0),
                       qa["repeticoes_numero_aih" if integral else "repeticoes_aih"]))
    salvar(stage/"qualidade_particoes.csv",("competencia uf universo_qa aih_principais_cardiovasculares "
            "datas_inconsistentes aih_sem_numero repeticoes_do_numero_na_particao").split(),linhas)


def figura_utilizacao(stage):
    """Apresente taxas e proporções em painéis com escalas e denominadores próprios."""
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    from matplotlib.ticker import FuncFormatter

    linhas = [r for r in ler(stage/"indicadores_anuais.csv") if r["territorio"]=="ES" and r["sexo"]=="T"]
    anos = [int(r["ano"]) for r in linhas]
    fig, (taxas, evasao) = plt.subplots(2,1,figsize=(9,6.5),sharex=True)
    for campo,legenda,cor in [("utilizacao_bruta_100mil","Bruta","#595959"),
                              ("padronizada_censo2022_100mil","Padrão Brasil 2022","#006d77"),
                              ("padronizada_censo2010_100mil","Padrão Brasil 2010","#905522")]:
        taxas.plot(anos,[float(r[campo]) for r in linhas],color=cor,marker="o",markersize=4,label=legenda)
    taxas.set_ylabel("AIHs por 100 mil habitantes")
    taxas.legend(frameon=False,ncol=3,loc="lower center",bbox_to_anchor=(.5,1.01))
    evasao.plot(anos,[float(r["evasao_pct"]) for r in linhas],color="#34538a",marker="o",markersize=4)
    evasao.set_ylabel("AIHs atendidas fora do ES (%)")
    evasao.set_xlabel("Ano da competência de processamento")
    evasao.set_ylim(bottom=0)
    evasao.yaxis.set_major_formatter(FuncFormatter(lambda n,_: f"{n:.1f}".replace(".",",")))
    for ax in (taxas,evasao):
        ax.grid(axis="y",color="#dedede",linewidth=.7)
        ax.spines[["right","top"]].set_visible(False)
    evasao.set_xticks(anos)
    fig.suptitle("Utilização hospitalar cardiovascular dos residentes do Espírito Santo",fontsize=14)
    fig.text(.08,.025,"Fonte: SIH/SUS, AIHs principais com diagnóstico principal I00–I99. Inclui atendimento em todas as UFs.",fontsize=9)
    fig.tight_layout(rect=(0,.05,1,.96))
    fig.savefig(stage/"utilizacao_e_evasao_es.png",dpi=180)
    plt.close(fig)


def conferir_taxas(stage, arquivo_pesos):
    """Recalcule em SQL a partir dos estratos e dos tamanhos das populações dos Censos."""
    import duckdb
    with duckdb.connect() as con:
        consulta = """
          WITH estratos AS (
            SELECT * FROM read_csv_auto(?)
          ), pesos AS (
            SELECT censo, idade_inicio, populacao / sum(populacao) OVER (PARTITION BY censo) AS peso
            FROM read_csv_auto(?)
          ), margens AS (
            SELECT ano, territorio, sexo, sum(aih_residentes) AS aih, sum(evasao_aih) AS ev,
                   100000.0 * sum(aih_residentes) / nullif(sum(habitantes), 0) AS bruta
            FROM estratos GROUP BY ALL
          ), diretas AS (
            SELECT ano, territorio, sexo, censo,
                   CASE WHEN count(habitantes) = 17 AND count(*) = 17
                        THEN sum(100000.0 * aih_residentes / habitantes * peso) END AS taxa
            FROM estratos JOIN pesos USING (idade_inicio) GROUP BY ALL
          )
          SELECT ano, territorio, sexo, aih, ev, bruta, censo, taxa
          FROM margens JOIN diretas USING (ano, territorio, sexo) ORDER BY ano, territorio, sexo, censo
        """
        linhas = con.execute(consulta,[str(stage/"sexo_idade_anual.csv"),str(arquivo_pesos)]).fetchall()
    referencias = {(r["ano"],r["territorio"],r["sexo"]):r for r in ler(stage/"indicadores_anuais.csv")}
    if len(linhas)!=2*len(referencias):
        raise ValueError("Cobertura divergente da contraprova de taxas")
    provas = []
    for ano,t,s,n,ev,bruta,censo,taxa in linhas:
        r = referencias[str(ano),t,s]
        if n!=int(r["aih_residentes"]) or ev!=int(r["evasao_aih"]):
            raise ValueError("Contraprova das margens etárias divergente")
        for campo,valor in [("utilizacao_bruta_100mil",bruta),(f"padronizada_censo{censo}_100mil",taxa)]:
            anterior = r[campo]
            if (valor is None)!=(anterior=="") or (valor is not None and abs(valor-float(anterior))>1e-8):
                raise ValueError(f"Contraprova de taxa divergente: {ano} {t} {s} {campo}")
        provas.append((ano,t,s,censo,n,ev,bruta,taxa,"conferido"))
    salvar(stage/"contraprova_taxas.csv","ano territorio sexo censo aih evasao taxa_bruta_sql direta_sql controle".split(),provas)


def relatorio(stage, cobertura):
    """Grave uma síntese de leitura humana junto às tabelas restritas e ao recibo."""
    def inteiro(n):
        return f"{int(n):,}".replace(",",".")

    def decimal(n):
        return f"{float(n):.2f}".replace(".",",")

    anuais = ler(stage/"utilizacao_e_evasao_es.csv")
    taxas = {(r["ano"],r["territorio"]):r for r in ler(stage/"indicadores_anuais.csv") if r["sexo"]=="T"}
    linhas = ["# SIH/SUS • Uso hospitalar cardiovascular dos residentes do Espírito Santo", "",
              f"**{cobertura['competencias']} competências de processamento, de janeiro de 2014 a dezembro de 2024.** "
              f"A conferência cobre {inteiro(cobertura['particoes'])} partições e as {cobertura['ufs']} UFs. "
              f"Os DBC somam {inteiro(cobertura['bytes'])} bytes. Cada célula igual a 1 na matriz indica um arquivo presente, "
              "conferido pelo tamanho e pelo SHA-256 e associado ao recibo analítico. "
              "[Matriz de cobertura](matriz_132_competencias.csv) · [Inventário com caminhos e evidências](arquivos.csv).", "",
              "## AIHs principais por ano de processamento", "",
              "| Ano | Residentes do ES | Atendimento no ES, todas as origens | Evasão (AIHs) | Evasão (%) | Atração (AIHs) | Taxa bruta¹ | Censo 2022¹ | Censo 2010¹ |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in anuais:
        t = taxas[r["ano"],"ES"]
        valores = [r["ano"],inteiro(r["aih_residentes"]),inteiro(r["atendimento_es"]),inteiro(r["evasao_aih"]),
                   decimal(r["evasao_pct"]),inteiro(r["atracao_aih"]),decimal(t["utilizacao_bruta_100mil"]),
                   decimal(t["padronizada_censo2022_100mil"]),decimal(t["padronizada_censo2010_100mil"])]
        linhas.append("| "+" | ".join(valores)+" |")
    linhas.extend(["", "¹ AIHs por 100 mil habitantes. As taxas brutas usam os denominadores anuais. A padronização direta usa "
                   "as mesmas faixas quinquenais, de 0–4 a 80+, e pesos comuns aos sexos. O padrão principal é o Brasil de 2022. "
                   "As tabelas preservam sexo e idade ignorados e mantêm vazias as taxas sem denominador.",
                   "", "A série conta AIHs principais ativas, IDENT=1, com diagnóstico principal I00–I99. Uma pessoa pode ter "
                   "várias AIHs. A evasão divide as AIHs de residentes atendidos em outra UF por todas as AIHs de residentes. "
                   "A atração divide as AIHs com município de residência de outra UF plausível por todas as AIHs atendidas no ES. "
                   "A UF de atendimento corresponde à UF do DBC. A conferência com o município do estabelecimento consta da série mensal.",
                   "", "A tabela clínica cruza ano de admissão com competência de processamento e UF. Admissões processadas depois "
                   "de dezembro de 2024 ficam fora da janela. Uma série por ano clínico exige considerar essa borda. "
                   "[Ano de admissão](ano_admissao.csv) · [Série por competência](serie_mensal.csv).",
                   "", "## Território e estratos", "",
                   "A matriz origem–destino segue as quatro regiões do PDR/ES 2024 em toda a série. As proporções regionais "
                   "trazem denominadores de todos os elegíveis e dos destinos ou origens comparáveis. Os campos residuais "
                   "identificam registros sem região válida. A participação interestadual usa o total elegível. O comparador "
                   "ES sem Norte segue o recorte do TCC e inclui residência estadual sem município identificado.",
                   "", "[Fluxos regionais](indicadores_regionais.csv) · [Matriz origem–destino](matriz_regional_anual.csv) · "
                   "[Utilização estadual, regional e por sexo](indicadores_anuais.csv) · [Sexo e idade](sexo_idade_anual.csv) · "
                   "[Indicadores municipais](indicadores_municipais.csv) · [Diagnóstico por grupo](grupos.csv).",
                   "", "## Controles de reprodução", "",
                   f"As {cobertura['competencias_anteriores_conciliadas']} competências nacionais anteriormente verificadas "
                   "reproduziram os valores de residentes e evasão. A série de atendimento no ES foi confrontada mês a mês e "
                   "ano a ano. A reposição autorizada do RD/ES de novembro de 2024 reproduziu o SHA-256 e o tamanho do CP04, "
                   "os fluxos regionais e os grupos de produção. O arquivo completo sustenta os estratos demográficos desse mês.",
                   "", "Os recibos de aquisição identificam a origem e a revisão do catálogo. O SHA-256 calculado na custódia "
                   "identifica os bytes preservados. Os recibos anuais vinculam esses bytes, os leitores, o PDR e os denominadores "
                   "aos produtos. Os testes em dados sintéticos e os confrontos empíricos têm registros próprios.",
                   "", "[Confrontos mensais](regressoes.csv) · [Recibos anuais](../anos/) · [Lotes adquiridos](../lotes/) · "
                   "[Recibo de reposição](../reposicao-cp04.json) · [Log de aquisição](../execucao.log).",
                   "", "As séries descrevem utilização registrada pelo SUS. Podem fundamentar as tabelas, mapas e resultados "
                   "do TCC após revisão. Interpretações sobre necessidade não atendida, resolutividade ou efeito da oferta "
                   "exigem evidência adicional."])
    (stage/"resultados_sih.md").write_text("\n".join(linhas)+"\n",encoding="utf8")


def fechar(v, out, destino=None):
    pastas = [out/"anos"/str(a) for a in range(2014,2025)]
    nacional = out/"fluxos-nacionais"
    insumos = {}
    for pasta in [*pastas,nacional]:
        recibo = pasta/"recibo.json"
        rec = json.loads(recibo.read_text())
        if rec["saidas"] != produtos(pasta):
            raise ValueError(f"Produtos alterados: {pasta}")
        insumos[pasta.name] = recibo
    nomes = ["arquivos.csv","serie_mensal.csv","indicadores_anuais.csv","sexo_idade_anual.csv","municipios.csv",
             "ano_admissao.csv","grupos.csv","fluxos_mensais.csv","regressoes.csv","conversao_demografica.csv"]
    def medir(stage):
        for nome in nomes:
            concatenar(stage,pastas,nome)
        cobertura = {(r["competencia"],r["uf"]):r for r in ler(nacional/"cobertura.csv")}
        origem = ler(stage/"arquivos.csv")
        ufs = sorted(UFS)
        meses = [f"{ano}{m:02d}" for ano in range(2014,2025) for m in range(1,13)]
        esperados = {(m,u) for m in meses for u in ufs}
        presentes = {(r["competencia"],r["uf"]) for r in origem}
        if presentes!=esperados or set(cobertura)!=esperados or len(origem)!=len(presentes):
            raise ValueError("Grade de partições incompleta ou sobreposta")
        qualidade_por_particao(stage,origem)
        for r in cobertura.values():
            if (r["objetos_catalogados"],r["dbc_reprocessados"],r["completo_fluxo_regional"],r["checkpoint_agregado"])!=("1","1","True","False"):
                raise ValueError("Cobertura sem DBC integral")
        salvar(stage/"matriz_132_competencias.csv",["ano","mes","competencia",*ufs,"ufs_validadas"],
               ((m[:4],m[4:],m,*(int((m,u) in presentes) for u in ufs),len(ufs)) for m in meses))
        fluxo_regional(stage)
        indicadores_municipais(stage,insumos["denominadores_municipais"])
        conferir_taxas(stage,insumos["populacoes_censitarias"])
        series = {r["competencia"]:r for r in ler(stage/"serie_mensal.csv")}
        indices = {r["competencia"]:r for r in ler(nacional/"serie.csv")}
        if set(indices)!=set(meses) or set(series)!=set(meses):
            raise ValueError("Série mensal incompleta")
        for mes,r in series.items():
            for a,b in [("atendimento_es","atendimento_es"),("residentes_es","residentes_cobertura_nacional"),
                        ("evasao_aih","evasao_cobertura_nacional"),("atracao_aih","atracao_plausivel")]:
                if r[a] != indices[mes][b]:
                    raise ValueError(f"Consolidações divergentes: {mes} {a}")
        uf_residentes = Counter()
        for r in ler(stage/"municipios.csv"):
            uf_residentes[r["competencia"],r["uf_atendimento"]] += int(r["aih"])
        lista_ufs = [(m,u,uf_residentes[m,u]) for m in meses for u in ufs]
        salvar(stage/"residentes_por_uf_atendimento.csv",["competencia","uf_atendimento","aih_residentes_es"],lista_ufs)
        for m in meses:
            if (sum(uf_residentes[m,u] for u in ufs)!=int(series[m]["residentes_es"])
                    or uf_residentes[m,"ES"]!=int(series[m]["residentes_no_es"])):
                raise ValueError(f"Margem municipal ou de UF divergente: {m}")
        calendario, por_competencia = Counter(), Counter()
        for r in ler(stage/"ano_admissao.csv"):
            calendario[r["competencia"][:4],r["ano_admissao"]] += int(r["aih"])
            por_competencia[r["competencia"]] += int(r["aih"])
        if any(por_competencia[m]!=int(series[m]["residentes_es"]) for m in meses):
            raise ValueError("Margem por ano de admissão divergente")
        salvar(stage/"admissao_por_ano_processamento.csv",["ano_processamento","ano_admissao","aih_residentes"],
               ((*k,n) for k,n in sorted(calendario.items())))
        anuais = []
        for ano in range(2014,2025):
            rs = [r for r in series.values() if int(r["competencia"][:4])==ano]
            def soma(k):
                return sum(int(r[k]) for r in rs)
            res, ev, at, atr, ign, inter = [soma(k) for k in ("residentes_es","evasao_aih","atendimento_es","atracao_aih",
                                                              "origem_indeterminada_no_es","interregional_intra_es")]
            if res-ev+atr+ign!=at:
                raise ValueError(f"Balanço anual divergente: {ano}")
            anuais.append((ano,len(rs),res,res-ev,ev,proporcao(ev,res),at,atr,proporcao(atr,at),ign,inter))
        salvar(stage/"utilizacao_e_evasao_es.csv",("ano competencias aih_residentes aih_residentes_no_es evasao_aih evasao_pct "
              "atendimento_es atracao_aih atracao_pct origem_indeterminada_no_es interregional_intra_es").split(),anuais)
        figura_utilizacao(stage)
        antigos = [r for r in ler(v/"sih-final/serie.csv") if r["residentes_cobertura_nacional"]]
        controles = dict(competencias=len(meses),particoes=len(origem),ufs=len(ufs),bytes=sum(int(r["bytes"]) for r in origem),
                    arquivos_por_origem=dict(Counter(r["origem"] for r in origem)),competencias_anteriores_conciliadas=len(antigos),
                    residentes=sum(r[2] for r in anuais),evasao=sum(r[4] for r in anuais),atendimento=sum(r[6] for r in anuais),
                    atracao=sum(r[7] for r in anuais),origem_indeterminada=sum(r[9] for r in anuais))
        relatorio(stage,controles)
        return controles
    insumos["serie_basal"] = v/"sih-final/serie.csv"
    insumos["pdr"] = territorio.TABELA
    nome = "RIPSA_DEM101_QA_TOTAIS.csv"
    verificar_produtos(v/"taxas-ed2",[nome,"pesos.csv"])
    insumos["denominadores_municipais"] = v/"taxas-ed2"/nome
    insumos["populacoes_censitarias"] = v/"taxas-ed2/pesos.csv"
    return executar(destino or out/"entrega",insumos,{"periodo":"201401-202412","matriz":"partição com bytes e recibo validados"},medir)


if __name__=="__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("custodia",type=Path)
    p.add_argument("saida",type=Path)
    p.add_argument("--destino",type=Path,help="Diretório externo para preservar outra edição da entrega.")
    args = p.parse_args()
    print(fechar(args.custodia,args.saida,args.destino)["controles"])
