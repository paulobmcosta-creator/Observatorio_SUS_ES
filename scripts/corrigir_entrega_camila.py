"""Gerar a edição corretiva local a partir dos produtos selados e da auditoria da v3.2."""
import argparse
import ast
import gzip
import hashlib
import json
import re
import shutil
from pathlib import Path

import pandas as pd

import figuras_academicas_camila as figuras
from corrigir_servicos_camila import DECISOES, dicionario, dominio_oficial, historico_sr
from entrega_academica_camila import DOCS, NOME, PDR, REPO, conferir
from observatorio_sus.estudos.camila.lote import executar
from observatorio_sus.io.custodia import sha256_arquivo

EDICAO = NOME+"_v3.2.1"
NOVOS = {"T17":"Classes de diagnóstico, fisioterapia e urgência cadastradas por competência",
         "T18":"Sobreposição entre classes SR e o serviço 116 por competência",
         "T19":"Cadastro da classe coronariana UCO por competência"}
SCRIPTS = [Path(__file__), Path(figuras.__file__), Path(__file__).with_name("corrigir_servicos_camila.py")]
FONTE = "CNES/SR do ES e SIGTAP da competência"


def ler_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def texto(path, conteudo):
    path.write_text(conteudo.strip()+"\n",encoding="utf8")


def sha_conteudo(path):
    with gzip.open(path,"rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()


def revisar_notas(inv):
    """Vincular o método e as notas ao estimando representado em cada produto."""
    esp = "Óbitos na faixa e sexo / habitantes do mesmo estrato × 100 mil."
    inv.loc["B02",["notas","numerador_denominador"]] = [
        "Idade conhecida, em faixas quinquenais até 80+. A contagem de idade ignorada está em B01, coluna idade_ignorada.",esp]
    inv.loc["T08",["notas","numerador_denominador"]] = [
        "Óbitos com causa básica final I00–I99 e residência municipal identificada. T09 mostra o resíduo estadual.",
        "Óbitos no município e ano / habitantes do município no mesmo ano × 100 mil. Taxa bruta."]
    inv.loc["F05",["titulo","numerador_denominador"]] = ["Mortalidade circulatória por idade e sexo no Espírito Santo, 2024",esp]
    inv.loc["F11","titulo"] = "Estabelecimentos com serviço cardiovascular 116 por região"
    inv.loc["F11","notas"] = "SR 116 com classificação histórica válida. Média dos estoques mensais de CNES distintos."
    inv.loc["F07","numerador_denominador"] = "Soma das taxas etárias de AIHs por 100 mil, ponderadas pela população-padrão Brasil 2022."
    inv.loc["F08","numerador_denominador"] = "AIHs no estrato de idade e sexo / habitantes do mesmo estrato × 100 mil."
    inv.loc["F10","numerador_denominador"] = "Evasão / AIHs dos residentes × 100. Atração / AIHs atendidas no ES × 100."
    inv.loc["B04","numerador_denominador"] += " Taxas diretas com pesos etários dos censos indicados nas colunas."
    for ident in ("T01","T02","T11"):
        inv.loc[ident,"notas"] = "AIHs principais por origem e destino. Ano de processamento. A tabela distingue a área de residência da área de atendimento."
    for i in range(11,18):
        inv.loc[f"F{i}","numerador_denominador"] = "Soma da medida nos meses válidos / número de meses válidos."
    for ident in ["F18","F19","F20","F21","F22","M03"]:
        inv.loc[ident,"numerador_denominador"] = "Soma da quantidade aprovada do recorte identificado, pela localização do prestador."
    for ident in ["F02","F03","F04","F24"]:
        inv.loc[ident,"numerador_denominador"] = "Soma das taxas específicas por idade ponderadas pelo padrão Brasil 2022 no universo indicado."
    for ident in ["F09","F10","F25","M04"]:
        inv.loc[ident,"fonte"] = "SIH/SUS, RD nacional"


def redesenhar(d, o, inv):
    figuras.iniciar()
    for ident, r in inv[inv.figura.ne("")].iterrows():
        source = d/r.tabela
        df = pd.read_csv(source, dtype={"chave":str})
        legend = r.territorio if "ES" in r.territorio or "Brasil" in r.territorio or "Espírito" in r.territorio else r.territorio+" · Espírito Santo"
        opts = dict(arquivo=(d/r.figura).with_suffix(""), titulo=r.titulo, unidade=r.unidade,
                    fonte=r.fonte, nota=r.notas, referencia={"periodo":r.periodo,"territorio":legend,"status":r.status})
        if ident.startswith("M"):
            malha = "ufs-br" if ident=="M04" else "municipios-es"
            figuras.mapa(df,o/"fontes"/(malha+".geojson"),**opts)
        elif ident=="F25":
            figuras.fluxo(df,**opts)
        else:
            etario = ident in {"F05","F08"}
            figuras.linhas(df,idades=etario,eixo="Idade em anos" if etario else "Ano",**opts)


def registrar_sr(d, inv, cont, inter):
    dados = {"T17":cont[cont.decisao.ne("Provisório")],"T18":inter,"T19":cont[cont.decisao.eq("Provisório")]}
    for ident, df in dados.items():
        path = f"02_TABELAS/oferta/{ident}.csv"
        df.to_csv(d/path,index=False)
        intersec = ident=="T18"
        inv.loc[ident] = dict(tipo="Tabela",titulo=NOVOS[ident],periodo="2014–2024",
            territorio="ES e quatro regiões" if intersec else "ES, quatro regiões e 78 municípios",
            unidade="estabelecimentos distintos",fonte=FONTE,
            numerador_denominador="CNES presentes em ambas as classes no mesmo mês." if intersec else "CNES distintos no território e competência da classe vigente.",
            notas="Zero indica ausência de cadastro da classe vigente. Valores ausentes indicam falta de domínio. Consulta por nível territorial.",
            status="Provisório para interpretação longitudinal" if ident=="T19" else "Verificado no escopo cadastral indicado",
            base="SR mensal, classificações e títulos do SIGTAP, PDR/ES 2024",tabela=path,figura="",script="scripts/corrigir_servicos_camila.py")


def funcao(path,nome):
    arvore=ast.parse(path.read_text(encoding="utf-8-sig"))
    return ast.dump(next(n for n in arvore.body if isinstance(n,ast.FunctionDef) and n.name==nome),include_attributes=False)


def proveniencia(d,o,ref,aud,edicoes):
    """Ligar os binários dos métodos às entradas e saídas dos recibos originais."""
    prov=d/"08_REPRODUTIBILIDADE/proveniencia_sigtap"
    prov.mkdir()
    script="historico_clinico_camila.py"
    caminhos={"historico":ref/"historico_clinico_edicao_recibo.py","reabilitacao":ref/"historico_complementar_em_execucao.py",
              "checkout":REPO/"scripts"/script}
    for papel,path in caminhos.items():
        shutil.copyfile(path,prov/(papel+".py"))
    met={k:sha256_arquivo(f) for k,f in caminhos.items()}
    historico=ler_json(o/"historico/recibo.json")
    if historico["contrato"]["metodo"][script]!=met["historico"]:
        raise ValueError("Revisão do catálogo sem correspondência com o recibo")
    recibos=prov/"recibos"
    recibos.mkdir()
    shutil.copyfile(o/"historico/recibo.json",recibos/"historico.json")
    saidas=[]
    insumos=[]
    for mes,arq in sorted(edicoes.items()):
        chave=sha256_arquivo(arq)
        if historico["contrato"]["entradas"].get(mes)!=chave:
            raise ValueError("Edição SIGTAP diferente da usada no histórico")
        insumos.append(("historico",mes,arq.name,chave,met["historico"],historico["id"]))
        rfile=o/"reabilitacao"/mes/"recibo.json"
        r=ler_json(rfile)
        if r["contrato"]["metodo"][script]!=met["reabilitacao"]:
            raise ValueError("Revisão da partição de reabilitação incompatível")
        shutil.copyfile(rfile,recibos/(mes+".json"))
        insumos.append(("reabilitacao",mes,"PAES"+mes[2:]+".dbc",r["contrato"]["entradas"]["PA"],met["reabilitacao"],r["id"]))
        for nome,h in r["saidas"].items():
            if sha256_arquivo(rfile.parent/nome)!=h:
                raise ValueError("Partição de reabilitação divergente")
            saidas.append((r["id"],mes,nome,h))
    for nome,h in historico["saidas"].items():
        saidas.append((historico["id"],"201401–202412",nome,h))
    pd.DataFrame(insumos,columns=["funcao","competencia","arquivo_oficial","sha256_entrada","sha256_script","id_recibo"]).to_csv(prov/"entradas.csv",index=False)
    pd.DataFrame(saidas,columns=["id_recibo","competencia","produto","sha256_produto"]).to_csv(prov/"saidas.csv",index=False)
    conf={}
    for nome in ["procedimentos","ocupacoes","servicos","habilitacoes"]:
        file=nome+".csv.gz"
        anterior=sha_conteudo(o/"historico"/file)
        if anterior!=sha_conteudo(aud/"historico"/file):
            raise ValueError("Conteúdo oficial do histórico diverge da reprodução anterior")
        conf[file]=anterior
    if not (funcao(caminhos["checkout"],"historico")==funcao(caminhos["historico"],"historico")
            and funcao(caminhos["checkout"],"adicional")==funcao(caminhos["reabilitacao"],"adicional")):
        raise ValueError("O corpo de uma função comparada mudou")
    anterior=ler_json(aud/"historico/recibo.json")
    if anterior["contrato"]["metodo"][script]!=met["checkout"]:
        raise ValueError("A revisão da reprodução anterior não é a revisão comparada")
    shutil.copyfile(aud/"historico/recibo.json",recibos/"reexecucao_historico.json")
    texto(prov/"confronto.json",json.dumps({"sha256_script":met,"conteudo_descompactado":conf,"meses_reabilitacao":len(edicoes),
        "funcao_historico_ast_igual":True,"funcao_adicional_ast_igual":True},ensure_ascii=False,indent=2))
    texto(prov/"LEIA.md","""# Revisões do método SIGTAP

historico.py é a cópia compatível com o recibo de formação do catálogo. reabilitacao.py corresponde aos 132 recibos de projeção complementar. checkout.py identifica o código da branch usado na contraprova anterior. entradas.csv liga as competências e edições aos hashes dos métodos e recibos. saidas.csv identifica cada produto. Os JSON em recibos preservam todos os parâmetros e as dependências gravadas no contrato original.

O corpo sintático da função historico coincide na revisão do primeiro lote e na atual. A auditoria anterior reexecutou a revisão atual a partir das 132 edições. Nesta correção foram conferidos a identidade dessa revisão e o conteúdo descompactado das quatro tabelas. O corpo sintático da função adicional coincide entre a revisão das partições e a atual. A conferência das partições usa seus hashes de origem, parâmetros e produtos selados. Não houve nova leitura dos microdados ambulatoriais.

A revisão do catálogo original não importa sys, necessário no caminho de execução de adicional. Uma constante de instrumentos, sem uso nas funções comparadas, foi removida da revisão atual. A evidência abrange as funções, os produtos e as entradas identificados. Não autoriza equivalência integral em outros modos ou entradas.""")


def atualizar_documentos(stage,o,inv,dominio):
    doc=stage/"07_DOCUMENTACAO_METODOLOGICA"
    nav=stage/"00_LEIA_PRIMEIRO"
    repro=stage/"08_REPRODUTIBILIDADE"
    dominio.to_csv(doc/"decisoes_sr_por_competencia.csv",index=False)
    uso=pd.read_csv(doc/"situacao_de_uso.csv")
    novos=[(decisao,"CNES/SR "+k,justificativa) for k,(decisao,justificativa) in DECISOES.items()]
    novos.append(("Não utilizável","Estabelecimentos em funcionamento efetivo",
                  "Os campos ST validados, vínculo SUS e produção aprovada em PA não comprovam abertura e continuidade de funcionamento."))
    pd.concat([uso,pd.DataFrame(novos,columns=uso.columns)],ignore_index=True).to_csv(doc/"situacao_de_uso.csv",index=False)
    campos={}
    for mes in sorted(dominio.competencia.unique()):
        st=ler_json(o/"particoes"/mes/"controles.json")["ST"]
        campos[mes]={"disponiveis":st["esquema"],"usados":st["campos"]}
    texto(doc/"campos_st_por_competencia.json",json.dumps(campos,ensure_ascii=False,indent=2))
    texto(doc/"decisao_atividade_operacional.md","""# Funcionamento operacional dos estabelecimentos

**Situação de uso: não mensurável com os campos validados neste estudo.** Foram examinados os esquemas e os campos efetivamente lidos nas 132 competências do CNES/ST. O arquivo campos_st_por_competencia.json permite consultar ambos por mês. ATIVIDAD, DT_ATUAL e os atributos cadastrais de atendimento, quando presentes, não documentam abertura física, continuidade diária ou disponibilidade efetiva de atendimento.

| Conceito | Regra no estudo | Fonte e unidade |
|---|---|---|
| Cadastro | Presença de CNES distinto na competência | ST_CAD, estabelecimentos por mês |
| Vínculo SUS | Presença e marca VINC_SUS igual a 1 | ST_SUS, estabelecimentos por mês |
| Produção observada | CNES com quantidade aprovada positiva do recorte específico, deduplicado no território e período | SIA/PA e SIGTAP; F23 por região e ano |
| Funcionamento efetivo | Medida indisponível; não há critério operacional validado nestes campos | Sem estimativa e sem imputação de zero |

O indicador de produção depende dos procedimentos selecionados e da janela de movimento. A atividade de outras especialidades e o funcionamento durante dias sem produção registrada permanecem desconhecidos.""")
    texto(doc/"leitura_chaves_historicas.md","""# Identificação das entradas do catálogo

A coluna id preserva a identidade analítica usada nas tabelas e nas figuras. Use chave_historica para identificar uma entrada do dicionário. Para PA e as cinco classes SR, a chave reúne ID, competência e SHA-256 da edição SIGTAP. A consulta retorna o título da competência, a edição e, quando aplicável, a versão dos atributos. Meses sem vigência do procedimento são preservados no histórico completo procedimentos.csv.gz.

Para as definições de recursos originais do CNES, a chave identifica a regra v3.2 e sha256_edicao remete ao dicionário de recursos que a fixou. Essas definições não afirmam vigência ininterrupta de códigos. Consulte a evidência mensal em B06 e o número de meses em T05. As colunas id e chave_historica permitem relacionar as séries existentes e as novas definições sem somar versões históricas.""")
    shutil.copyfile(DOCS/"manual_leitura_assistencial.md",stage/"05_MANUAL_DA_ESTUDANTE/manual.md")
    shutil.copyfile(DOCS/"registro_decisoes_metodologicas.md",doc/"registro_decisoes_metodologicas.md")
    for script in SCRIPTS:
        shutil.copyfile(script,repro/script.name)
    idx=nav/"indice_geral.md"
    conteudo=idx.read_text(encoding="utf8").replace("Entrega acadêmica da Camila","Edição corretiva v3.2.1 · Entrega acadêmica da Camila")
    conteudo=conteudo.replace("F05 · Mortalidade por idade e sexo no Espírito Santo","F05 · "+inv.loc["F05","titulo"])
    conteudo=conteudo.replace("F11 · Serviço cardiovascular classificado por região","F11 · "+inv.loc["F11","titulo"])
    indice=["## Serviços especializados na edição v3.2.1",""]
    for ident,titulo in NOVOS.items():
        indice.append(f"- [{ident} · {titulo}](../{inv.loc[ident,'tabela']})")
    indice+=["- [Decisões por classe e competência](../07_DOCUMENTACAO_METODOLOGICA/decisoes_sr_por_competencia.csv)",
             "- [Cadastro, produção e funcionamento](../07_DOCUMENTACAO_METODOLOGICA/decisao_atividade_operacional.md)",
             "- [Como usar as chaves históricas](../07_DOCUMENTACAO_METODOLOGICA/leitura_chaves_historicas.md)",
             "- [Proveniência das revisões SIGTAP](../08_REPRODUTIBILIDADE/proveniencia_sigtap/LEIA.md)"]
    texto(idx,conteudo+"\n\n"+"\n".join(indice))
    guia=nav/"guia_de_navegacao.md"
    texto(guia,guia.read_text(encoding="utf8")+"\n\nConsulte T17 e T19 para as cinco classes SR, e T18 para identificar sobreposições. A partir da edição v3.2.1, cada visual informa ID, período e território no próprio desenho.")
    texto(repro/"reproduzir.md","""# Reproduzir a edição corretiva

Use o ambiente do estudo, o checkout com os scripts desta edição e a custódia local. O primeiro argumento contém mandato-v3 e mandato-v3.2. O segundo aponta para o diretório da auditoria de aderência de 19/11/2026 que contém historico/ e o parecer anterior. O terceiro aponta para a pasta referencias preservada no ZIP de auditoria corretiva. O quarto é um novo diretório de saída externo ao checkout, com diretório pai existente.

```powershell
$env:PYTHONPATH=(Resolve-Path python).Path
python scripts/corrigir_entrega_camila.py $custodia $auditoriaAnterior $referencias $novoDestino
```

O gerador confere os recibos e os SHA-256 dos insumos, copia a edição acadêmica de referência e trabalha sobre a cópia. Apura somente os recortes SR adicionais e lê as definições oficiais das competências já adquiridas. Os 29 visuais são desenhados diretamente das suas tabelas originais. A comparação quantitativa e o manifesto das saídas estão na pasta 08 e no recibo da raiz. Use proveniencia_sigtap para conferir as revisões anteriores do método.""")
    inv.rename_axis("id").reset_index().to_csv(nav/"inventario_produtos.csv",index=False)


def validar(stage,base,inv,anterior):
    """Conferir cada tabela original e cada legenda contra o arquivo realmente entregue."""
    from xml.etree import ElementTree as ET
    from PIL import Image
    repro=stage/"08_REPRODUTIBILIDADE"
    comparacao=[]
    for ident,r in anterior.iterrows():
        h0=sha256_arquivo(base/r.tabela)
        h1=sha256_arquivo(stage/r.tabela)
        if h0!=h1:
            raise ValueError(f"Alteração quantitativa na tabela {ident}")
        comparacao.append((ident,r.tabela,h0,h1))
    pd.DataFrame(comparacao,columns=["id","arquivo","sha256_v32","sha256_v321"]).to_csv(repro/"confronto_tabelas.csv",index=False)
    qa=[]
    for ident,r in inv[inv.figura.ne("")].iterrows():
        arquivo=stage/r.figura
        svg=ET.parse(arquivo)
        rotulos=" ".join("".join(n.itertext()) for n in svg.iter("{http://www.w3.org/2000/svg}text"))
        termos=[ident,r.titulo,r.periodo,r.territorio,r.unidade,r.fonte,r.status,ident+".csv"]
        if not all(t in rotulos for t in termos):
            raise ValueError(f"Identificação gráfica incompleta em {ident}")
        with Image.open(arquivo.with_suffix(".png")) as im:
            im.verify()
        qa.append((ident,r.periodo,sha256_arquivo(stage/r.tabela),sha256_arquivo(arquivo),sha256_arquivo(arquivo.with_suffix(".png"))))
    if len(qa)!=29:
        raise ValueError("Inventário visual incompleto")
    pd.DataFrame(qa,columns=["id","periodo","sha256_tabela","sha256_svg","sha256_png"]).to_csv(repro/"validacao_visuais.csv",index=False)
    for f in stage.rglob("*.md"):
        for href in re.findall(r"\]\(([^)]+)\)",f.read_text(encoding="utf-8-sig")):
            if "://" in href or href.startswith("#"):
                continue
            if not (f.parent/href).is_file():
                raise ValueError(f"Link relativo sem destino em {f.name}: {href}")


def corrigir(custodia,aud,ref,destino):
    o=custodia/"mandato-v3.2"
    base=o/NOME
    etapa=o/"etapa1"
    historico=o/"historico"
    oficiais=custodia/"mandato-v3/fontes/sigtap"
    edicoes={f.name.split("_")[1][:6]:f for f in oficiais.rglob("*.zip")}
    if len(edicoes)!=132:
        raise ValueError("Edições históricas ausentes")
    entradas={"edicao_v32":conferir(base),"etapa1":conferir(etapa),"historico":conferir(historico),
              "historico_auditoria":conferir(aud/"historico"),"pdr":PDR}
    for nome in ["mandato-corretivo.md","parecer-independente.md","parecer.md","matriz_de_aderencia.csv",
                 "documentacao.json","historico_clinico_edicao_recibo.py","historico_complementar_em_execucao.py"]:
        entradas[nome]=ref/nome
    for f in [DOCS/"manual_leitura_assistencial.md",DOCS/"registro_decisoes_metodologicas.md",REPO/"scripts/historico_clinico_camila.py"]:
        entradas[f.name]=f
    for m,arq in edicoes.items():
        entradas["sigtap_"+m]=arq
        entradas["reab_"+m]=o/"reabilitacao"/m/"recibo.json"
        entradas["esquema_st_"+m]=o/"particoes"/m/"controles.json"
    for nome in ("municipios-es","ufs-br"):
        entradas[nome]=o/"fontes"/(nome+".geojson")
    def calcular(stage):
        shutil.copytree(base,stage,dirs_exist_ok=True,ignore=lambda path,names: ["controles.json","recibo.json"] if Path(path)==base else [])
        doc=stage/"07_DOCUMENTACAO_METODOLOGICA"
        nav=stage/"00_LEIA_PRIMEIRO"
        inv=pd.read_csv(nav/"inventario_produtos.csv",dtype=str,keep_default_na=False).set_index("id")
        anterior=inv.copy()
        dominio=dominio_oficial(edicoes,historico/"servicos.csv.gz")
        cont,inter,presenca=historico_sr(etapa,PDR,dominio)
        registrar_sr(stage,inv,cont,inter)
        catalogo=dicionario(doc/"catalogo_indicadores.csv",historico/"procedimentos.csv.gz",edicoes,dominio,sha256_arquivo(etapa/"dicionario_recursos.csv"))
        catalogo.to_csv(doc/"catalogo_indicadores.csv",index=False)
        proveniencia(stage,o,ref,aud,edicoes)
        revisar_notas(inv)
        inv.loc[inv.figura.ne(""),"script"]="scripts/corrigir_entrega_camila.py + scripts/figuras_academicas_camila.py"
        redesenhar(stage,o,inv)
        atualizar_documentos(stage,o,inv,dominio)
        validar(stage,base,inv,anterior)
        return {"edicao":"3.2.1","catalogo_chaves":len(catalogo),"catalogo_ids":int(catalogo.id.nunique()),
                "tabelas_originais_iguais":len(anterior),"produtos":len(inv),"graficos":25,"mapas":4,
                "meses_sr":int(presenca.mes.nunique()),"controle_116_territorios_mes":660,"linhas_intersecoes":len(inter),
                "decisoes_sr":len(DECISOES),"funcionamento_efetivo":"não mensurável"}
    return executar(destino,entradas,{"edicao":"v3.2.1","origem":"v3.2"},calcular,SCRIPTS)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    for n in ["custodia","auditoria","referencias","destino"]:
        p.add_argument(n,type=Path)
    args=p.parse_args()
    print(corrigir(args.custodia,args.auditoria,args.referencias,args.destino)["controles"])
