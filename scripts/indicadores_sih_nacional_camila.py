"""Calcule utilização e fluxos do SIH para anos completos de processamento."""
import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

from completar_sih_nacional_camila import catalogo
from observatorio_sus.estudos.camila import assistencia, sim, territorio
from observatorio_sus.estudos.camila.lote import executar, ler, produtos, salvar
from observatorio_sus.extract.envelope_datasus import UFS
from observatorio_sus.io.custodia import sha256_arquivo
from observatorio_sus.transform import padronizacao

FAIXAS = tuple(range(0, 85, 5))
REGIOES = tuple(territorio.PAGINAS)
ESCOPO = ("ES", *REGIOES, "ES sem Norte")
SEXO = ("T", "M", "F", "IGN")
UF_IBGE = dict(zip("RO AC AM RR PA AP TO MA PI CE RN PB PE AL SE BA MG ES RJ SP PR SC RS MS MT GO DF".split(),
                   "11 12 13 14 15 16 17 21 22 23 24 25 26 27 28 29 31 32 33 35 41 42 43 50 51 52 53".split()))


def tabela_cnv(conteudo):
    """Aplique a precedência da conversão TABWIN, refinando o valor residual inicial."""
    resultado = {}
    for linha in conteudo.decode("latin1").splitlines()[1:]:
        partes = linha.split()
        if not partes:
            continue
        categoria = int(partes[0])
        for item in partes[-1].split(","):
            limites = [int(s) for s in item.split("-")]
            for codigo in range(limites[0], limites[-1]+1):
                resultado[codigo] = categoria
    return resultado


def estratos(r, idades, sexos):
    """Converta código e quantidade de idade e reúna as duas classes de menores de cinco."""
    unidade, quantidade = r["unidade_idade"], r["idade"]
    faixa = None
    if re.fullmatch(r"[0-9]", unidade) and re.fullmatch(r"[0-9]{1,2}", quantidade):
        classe = idades.get(int(unidade)*100+int(quantidade))
        if classe in (1, 2):
            faixa = 0
        elif classe is not None and 3 <= classe <= 18:
            faixa = (classe-2)*5
    sexo = sexos.get(int(r["sexo_sih"])) if r["sexo_sih"].isdigit() else None
    return {1:"M", 2:"F"}.get(sexo, "IGN"), faixa if faixa is not None else -1


def territorios(regiao):
    """O comparador ES sem Norte segue o tratamento do resíduo homologado no TCC."""
    yield "ES"
    if regiao in REGIOES:
        yield regiao
    if regiao != "Norte":
        yield "ES sem Norte"


def proporcao(n, d, fator=100):
    return fator*n/d if d else None


def salvar_contagem(path, campos, contagem):
    salvar(path, [*campos.split(), "aih"], ((*k,n) for k,n in sorted(contagem.items())))


def ler_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def verificar_produtos(pasta, nomes):
    rec = ler_json(pasta/"recibo.json")
    for nome in nomes:
        if sha256_arquivo(pasta/nome) != rec["saidas"][nome]:
            raise ValueError(f"Produto prévio divergente: {pasta.name}/{nome}")


def fontes(v, out, ano):
    """Vincule cada DBC ao catálogo oficial, à aquisição e ao recibo de processamento."""
    inventario = v/"auditoria-final/originais.csv"
    if sha256_arquivo(inventario) != ler_json(inventario.with_name("verificacao.json"))["sha256_origem"]:
        raise ValueError("Inventário legado divergente")
    antigas = {Path(r["arquivo_local"]).stem:r for r in ler(inventario) if r["familia"]=="RD"}
    tamanhos = catalogo(out/"rd-lista-atual.txt")
    recibos = []
    arquivos = {}
    insumos = {"inventario":inventario, "catalogo":out/"rd-lista-atual.txt", "pdr":territorio.TABELA,
               "dicionarios":out/"dicionario/TAB_SIH.zip","reposicao":out/"reposicao-cp04.json",
               "den":v/"taxas-ed2/especificas.csv","pesos":v/"taxas-ed2/pesos.csv",
               "anterior":v/"sih-final/serie.csv", "pilotos":v/"indicadores-assistenciais/qa_sih_pilotos.csv",
               "producao_anterior":v/"indicadores-assistenciais/sih_atendimento_es_anual.csv"}
    for pasta, nomes in [(v/"taxas-ed2",["especificas.csv","pesos.csv"]), (v/"sih-final",["serie.csv"]),
                         (v/"indicadores-assistenciais",["qa_sih_pilotos.csv","sih_atendimento_es_anual.csv"])]:
        verificar_produtos(pasta, nomes)
    cp = v.parent/"acervo/CP04/Resultados"
    if ano == 2024:
        insumos.update(cp_fluxos=cp/"SIH_PILOTO_FLUXOS.csv",cp_producao=cp/"SIH_PILOTO_PRODUCAO.csv")
    pdr = sha256_arquivo(territorio.TABELA)
    for m in range(1,13):
        mes = f"{ano}{m:02d}"
        lote = out/"lotes"/(mes+".json")
        extras = {}
        if lote.exists():
            insumos["lote"+mes] = lote
            extras = {r["arquivo"]:r for r in ler_json(lote)["objetos"]}
        for uf in sorted(UFS):
            nome = "RD"+uf+mes[2:]
            base = antigas.get(nome)
            novo = extras.get(nome)
            if sum([bool(base),bool(novo),nome=="RDES2411"]) != 1:
                raise ValueError(f"Competência ainda sem cobertura validada ou sobreposta: {nome}")
            url = f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/{nome}.dbc"
            dbc = Path(base["arquivo_local"]) if base else v/"originais-assistencia/RD"/uf/mes/(nome+".dbc")
            sha = sha256_arquivo(dbc)
            pin = base or novo or ler_json(insumos["reposicao"])
            if sha != pin["sha256"] or dbc.stat().st_size != tamanhos[nome] or int(pin["bytes"]) != tamanhos[nome]:
                raise ValueError(f"Original divergente: {nome}")
            origem = "acervo v3" if base else "lote v3.1" if novo else "reposição CP04"
            evidencia = dbc.parent/"aquisicao.json"
            if evidencia.exists():
                acq = ler_json(evidencia)
                if acq["sha256"] != sha or url != acq["uri_oficial"] or acq["bytes"] != tamanhos[nome]:
                    raise ValueError(f"Recibo de aquisição incompatível: {nome}")
                insumos["aquisicao_"+nome] = evidencia
            elif not base or base["fonte"].startswith("ftp:"):
                raise ValueError(f"Recibo de aquisição ausente: {nome}")
            else:
                evidencia = inventario
            pasta = v/"sih"/nome/mes
            integral = pasta.is_dir()
            if not integral:
                pasta = v/"sih-residentes"/nome/mes
            recibo = pasta/"recibo.json"
            rec = ler_json(recibo)
            if (rec["contrato"]["entradas"] != {"dbc":sha, "pdr":pdr}
                    or rec["saidas"] != produtos(pasta) or (not integral and uf=="ES")):
                raise ValueError(f"Leitura ou domínio inválido: {nome}")
            qa = rec["controles"]["qa"]
            if qa["ativos"]+qa["excluidos"] != qa["cabecalho"] or (novo and novo["sha256_recibo"] != sha256_arquivo(recibo)):
                raise ValueError(f"Balanço DBF ou recibo divergente: {nome}")
            insumos[nome] = recibo
            arquivos[nome] = (pasta/"fluxos.csv", integral, rec["controles"])
            recibos.append((mes,uf,dbc.name,url,tamanhos[nome],sha,origem,dbc,evidencia,sha256_arquivo(evidencia),
                            recibo,sha256_arquivo(recibo),qa["cabecalho"],qa["ativos"],qa["excluidos"]))
    return insumos, arquivos, recibos


def calcular_taxas(stage, ano, insumos, idades, eventos):
    den = defaultdict(dict)
    for r in ler(insumos["den"]):
        if int(r["ano"])==ano and r["grupo"]=="G0" and r["habitantes"]:
            sexo = {"T":"T","1":"M","2":"F"}[r["sexo_sim"]]
            den[r["territorio"],sexo][int(r["idade_inicio"])] = int(r["habitantes"])
    pesos = defaultdict(dict)
    for r in ler(insumos["pesos"]):
        pesos[r["censo"]][int(r["idade_inicio"])] = float(r["peso_todas"])
    if set(pesos)!={"2010","2022"} or any(set(w)!=set(FAIXAS) for w in pesos.values()):
        raise ValueError("Pesos censitários incompletos")
    linhas, especificas = [], []
    for t in ESCOPO:
        for sexo in SEXO:
            d = den[t,sexo]
            if sexo != "IGN" and (set(d)!=set(FAIXAS) or min(d.values())<=0):
                raise ValueError(f"Denominadores incompletos: {ano} {t} {sexo}")
            n = {a:idades[t,sexo,a] for a in FAIXAS}
            fora = {a:eventos[t,sexo,a] for a in FAIXAS}
            ig = idades[t,sexo,-1]
            n_total = sum(n.values())+ig
            n_fora = sum(fora.values())+eventos[t,sexo,-1]
            if n_fora>n_total:
                raise ValueError("Evasão excede utilização")
            hab = sum(d.values())
            linhas.append((ano,t,sexo,n_total,n_total-n_fora,n_fora,proporcao(n_fora,n_total),ig,hab or None,
                           proporcao(n_total,hab,100000),padronizacao.direta(n,d,pesos["2022"]),
                           padronizacao.direta(n,d,pesos["2010"])))
            for a in (*FAIXAS,-1):
                num, ev = idades[t,sexo,a],eventos[t,sexo,a]
                especificas.append((ano,t,sexo,a,num,ev,proporcao(ev,num),d.get(a),proporcao(num,d.get(a),100000)))
        totais = [sum(idades[t,s,a] for a in (*FAIXAS,-1)) for s in SEXO]
        if totais[0] != sum(totais[1:]):
            raise ValueError("Margens por sexo inconsistentes")
    salvar(stage/"indicadores_anuais.csv","ano territorio sexo aih_residentes aih_no_es evasao_aih evasao_pct idade_ignorada habitantes utilizacao_bruta_100mil padronizada_censo2022_100mil padronizada_censo2010_100mil".split(),linhas)
    salvar(stage/"sexo_idade_anual.csv","ano territorio sexo idade_inicio aih_residentes evasao_aih evasao_pct habitantes utilizacao_100mil".split(),especificas)
    return sum(idades["ES","T",a] for a in (*FAIXAS,-1))


def calcular(v, out, ano):
    """Só produza indicadores anuais após fechar os doze meses em todas as UFs."""
    insumos, arquivos, recibos = fontes(v, out, ano)

    def medir(stage):
        with ZipFile(insumos["dicionarios"]) as z:
            idades = tabela_cnv(z.read("CNV/IDADE18.CNV"))
            sexos = tabela_cnv(z.read("CNV/SEXO.CNV"))
        mapa = territorio.mapa()
        if set(UF_IBGE)!=set(UFS):
            raise ValueError("Mapa das UFs incompleto")
        idade_total, idade_fora, mensal, municipios, adm, fluxos, grupos = (Counter() for _ in range(7))
        atendimento_grupo, novembro, codigos = Counter(), Counter(), Counter()
        for nome,(path,integral,ctrl) in arquivos.items():
            uf, mes = nome[2:4], "20"+nome[-4:]
            soma = 0
            with path.open(encoding="utf-8-sig",newline="") as f:
                for r in csv.DictReader(f):
                    n = int(r["aih"])
                    res, at = r["municipio_res"], r["municipio_atend"]
                    local = res.startswith("32")
                    reg, dest = r["regiao_res"], r["regiao_atend"]
                    if (n<=0 or r["competencia"]!=mes or r["uf_arquivo"]!=uf or reg!=assistencia.situacao(res,mapa)
                            or dest!=assistencia.situacao(at,mapa) or (not integral and not local)):
                        raise ValueError(f"Chave geográfica ou célula inválida: {nome}")
                    soma += n
                    if uf!="ES" and not local:
                        continue
                    if at[:2]!=UF_IBGE[uf]:
                        mensal[mes,"municipio_at_diverge_uf_arquivo"] += n
                    cid = r["diagnostico"]
                    if not re.fullmatch("I[0-9]{2}[A-Z0-9]?",cid):
                        raise ValueError(f"Diagnóstico fora de G0: {nome}")
                    subgrupos = ["G0",*(g for g,(lo,hi) in sim.GRUPOS.items() if lo<=int(cid[1:3])<=hi)]
                    fluxos[mes,reg,uf,dest,res[:2],at[:2]] += n
                    if uf=="ES":
                        mensal[mes,"atendimento"] += n
                        if not local:
                            classe = "atracao" if reg=="OUTRA_UF_CODIGO_PLAUSIVEL" else "origem_indeterminada"
                            mensal[mes,classe] += n
                        if mes=="202411":
                            novembro[reg if local else "RES_OUTRA_UF_OU_INDETERMINADA",dest] += n
                        for g in subgrupos:
                            atendimento_grupo[mes,"ES",g] += n
                            atendimento_grupo[mes,dest,g] += n
                    if not local:
                        continue
                    mensal[mes,"residentes"] += n
                    if uf!="ES":
                        mensal[mes,"evasao"] += n
                    if uf=="ES" and reg in REGIOES and dest in REGIOES and reg!=dest:
                        mensal[mes,"interregional_es"] += n
                    sexo, idade = estratos(r,idades,sexos)
                    codigos[r["sexo_sih"],r["unidade_idade"],r["idade"],sexo,idade] += n
                    adm[mes,r["ano_admissao"],uf] += n
                    municipios[mes,reg,res,uf] += n
                    for t in territorios(reg):
                        for s in ("T",sexo):
                            idade_total[t,s,idade] += n
                            if uf!="ES":
                                idade_fora[t,s,idade] += n
                        for g in subgrupos:
                            grupos[mes,t,g,uf] += n
            valido = ctrl["qa"]["circulatorias_ident_1"] if integral else ctrl["residentes_circulatorios"]
            if soma != valido:
                raise ValueError(f"Margem de AIHs divergente: {nome}")
        salvar(stage/"arquivos.csv","competencia uf arquivo url_catalogo bytes sha256 origem caminho_dbc evidencia_aquisicao sha256_evidencia recibo_analitico sha256_recibo registros_dbf ativos excluidos".split(),recibos)
        salvar_contagem(stage/"fluxos_mensais.csv","competencia regiao_res uf_atendimento regiao_at uf_res_ibge uf_at_municipio",fluxos)
        salvar_contagem(stage/"municipios.csv","competencia regiao_res municipio_res uf_atendimento",municipios)
        salvar_contagem(stage/"ano_admissao.csv","competencia ano_admissao uf_atendimento",adm)
        salvar_contagem(stage/"grupos.csv","competencia territorio grupo uf_atendimento",grupos)
        salvar_contagem(stage/"conversao_demografica.csv","sexo_sih unidade_idade idade_sih sexo faixa",codigos)
        total = calcular_taxas(stage,ano,insumos,idade_total,idade_fora)
        conciliar(stage,ano,insumos,mensal,atendimento_grupo,novembro,total)
        return dict(ano=ano,competencias=12,particoes=len(recibos),residentes=total,
                    evasao=sum(idade_fora["ES","T",a] for a in (*FAIXAS,-1)),ativos=sum(r[-2] for r in recibos))

    return executar(out/"anos"/str(ano),insumos,{"ano_processamento":ano,"ident":"1","capitulo":"I00-I99"},medir,
                    [Path(padronizacao.__file__),Path(assistencia.__file__),Path(sim.__file__)])


def conciliar(stage, ano, insumos, mensal, atendimento_grupo, novembro, total):
    meses = [f"{ano}{m:02d}" for m in range(1,13)]
    anterior = {r["competencia"]:r for r in ler(insumos["anterior"])}
    serie, provas = [], []
    for mes in meses:
        legado = anterior[mes]
        at, res, ev, atr, ign = (mensal[mes,c] for c in ("atendimento","residentes","evasao","atracao","origem_indeterminada"))
        if at != res-ev+atr+ign:
            raise ValueError(f"Balanço atendimento/residência inválido: {mes}")
        for campo,valor in [("atendimento_es",at),("atracao_plausivel",atr),("residentes_cobertura_nacional",res),
                            ("evasao_cobertura_nacional",ev)]:
            if legado[campo] and int(legado[campo])!=valor:
                raise ValueError(f"Checkpoint divergente: {mes} {campo}")
            provas.append((mes,campo,legado[campo],valor,"igual" if legado[campo] else "cobertura ampliada"))
        ganho = res-int(legado["residentes_observados"])
        if ganho<0 or ganho!=ev-int(legado["evasao_observada"] or 0):
            raise ValueError(f"Incremento não explicado por atendimento fora do ES: {mes}")
        serie.append((mes,27,at,res,res-ev,ev,proporcao(ev,res),atr,proporcao(atr,at),ign,
                      mensal[mes,"interregional_es"],mensal[mes,"municipio_at_diverge_uf_arquivo"]))
    if total != sum(r[3] for r in serie):
        raise ValueError("Margens mensais e etárias divergentes")
    piloto = [r for r in ler(insumos["pilotos"]) if r["competencia"][:4]==str(ano)]
    for r in piloto:
        if atendimento_grupo[r["competencia"],r["atendimento"],r["grupo"]]!=int(r["aih_anterior"]):
            raise ValueError("Grupo ou piloto estadual divergente")
    anterior_anual, = (r for r in ler(insumos["producao_anterior"]) if r["ano"]==str(ano))
    if int(anterior_anual["sum"]) != sum(r[2] for r in serie) or int(anterior_anual["count"]) != 12:
        raise ValueError("Soma anual de atendimento divergente")
    if ano==2024:
        orig = {(r["origem_residencia"],r["destino_atendimento"]):int(r["aih_g0_ident1"])
                for r in ler(insumos["cp_fluxos"]) if r["competencia_processamento"]=="202411"}
        if dict(novembro)!=orig:
            raise ValueError("Fluxos da reposição incompatíveis com CP04")
        for r in ler(insumos["cp_producao"]):
            if r["competencia_processamento"]=="202411" and int(r["aih_ident1"])!=atendimento_grupo["202411",r["atendimento"],r["grupo"]]:
                raise ValueError("Produção da reposição incompatível com CP04")
    salvar(stage/"serie_mensal.csv","competencia ufs atendimento_es residentes_es residentes_no_es evasao_aih evasao_pct atracao_aih atracao_pct origem_indeterminada_no_es interregional_intra_es uf_at_municipio_divergente".split(),serie)
    salvar(stage/"regressoes.csv","competencia indicador checkpoint_anterior calculado verificacao".split(),provas)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("custodia",type=Path)
    parser.add_argument("saida",type=Path)
    parser.add_argument("anos",nargs="+",type=int,choices=range(2014,2025))
    args = parser.parse_args()
    for ano in args.anos:
        print(calcular(args.custodia,args.saida,ano)["controles"],flush=True)
