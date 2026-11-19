"""Documentar as homologações e congelar a evidência da Etapa 1 antes do pacote acadêmico."""
import argparse
import json
from pathlib import Path
import pandas as pd
from observatorio_sus.estudos.camila.lote import executar, produtos
from observatorio_sus.io.custodia import sha256_arquivo
from integrar_oferta_camila import conferir


def fechar(out):
    etapa=out/"etapa1"
    entradas={k:conferir(p) for k,p in {"calculo":etapa,"historico":out/"historico","reposicao":out/"reposicao-lt/202412"}.items()}
    entradas["testes"]=out/"testes-etapa1.log"
    entradas["fontes"]=out/"fontes/proveniencia.json"
    def medir(stage):
        est=pd.read_csv(etapa/"estoques_anuais.csv")
        pa=pd.read_csv(etapa/"pa_subtotais.csv",dtype={"competencia":str})
        q=pd.read_csv(etapa/"controle_pa_mensal.csv")
        if len(q)!=132 or q.filter(regex="diferenca").abs().to_numpy().max()!=0:
            raise ValueError("Comparação com o PA anterior")
        if est.ano.nunique()!=11 or est.territorio.nunique()!=5:
            raise ValueError("Cobertura dos estoques anuais")
        reg=pd.read_csv(etapa/"pa_subtotais.csv",dtype={"competencia":str})
        estados=reg[reg.territorio=="ES"].set_index(["competencia","grupo_clinico"]).aprovadas
        soma=reg[reg.territorio!="ES"].groupby(["competencia","grupo_clinico"]).aprovadas.sum(min_count=1)
        # Uma produção com município inclassificável continua na margem estadual e é auditada.
        residuos=estados.sub(soma).dropna()
        if (residuos<0).any():raise ValueError("Margem regional de PA excede ES")
        residuos.rename("residuo_territorial").to_csv(stage/"residuos_pa.csv")
        defs=pd.read_csv(etapa/"dicionario_recursos.csv")
        defs["fonte"]="CNES/DATASUS"
        defs["temporalidade"]="competência cadastral; média mensal no ano"
        defs["territorio"]="município do estabelecimento; PDR/ES 2024"
        defs["teste"]="balanço DBF; regressão regional v3 ou catálogo histórico SR; confirmação de chaves"
        defs["script"]="qualificar_particoes_camila.py; integrar_oferta_camila.py"
        procs=pd.read_csv(etapa/"catalogo_clinico.csv",dtype=str)
        clin=procs.drop_duplicates(["codigo","descricao"]).copy()
        clin["id"]="PA_"+clin.codigo
        clin["familia"]="PA"
        clin["titulo"]=clin.descricao
        clin["unidade"]="quantidade de procedimentos"
        clin["codigos"]=clin.codigo
        clin["filtro"]=clin.regra
        clin["formula"]="soma separada de PA_QTDAPR e PA_QTDPRO; CNES distintos com quantidade aprovada positiva"
        clin["limitacao"]="Janela de movimento jan/2014 a dez/2024; produção apresentada depois da janela não é observada."
        clin["fonte"]="SIA/PA + SIGTAP mensal"
        clin["temporalidade"]="PA_CMP; PA_MVM identifica o arquivo de movimento"
        clin["territorio"]="prestador por PA_UFMUN; PDR/ES 2024"
        clin["teste"]="vigência, instrumento, regressão PA por código/CBO/região/competência, balanço da junção"
        clin["script"]="historico_clinico_camila.py; integrar_oferta_camila.py"
        pd.concat([defs,clin[defs.columns]],ignore_index=True).to_csv(stage/"catalogo_indicadores.csv",index=False)
        estados_uso=[
            ("Validado","ST/SR/HB","Contagem de CNES, serviços classificados e habilitações por código vigente; domínios ausentes ficam vazios."),
            ("Validado","LT 02 e 32; 03 e 33 contextuais","Códigos e títulos no domínio LFCES001, manual SCNES 2009, e na conversão oficial. Estoques cadastrados e SUS."),
            ("Provisório","LT UCO e UTI longitudinal","Conservar códigos e contagens. A Portaria SAES/MS 1.202/2023 confirma a nomenclatura UCO em parte do intervalo; a continuidade completa do significado requer revisão."),
            ("Validado","EQ/PF/EP","Equipamentos pela tabela aplicável até 202507, vínculos e horas pelos três CBO, equipes identificáveis ativas ao fim do mês."),
            ("Validado","PA A específico e B contextual","Aplicar as duas homologações que constam do registro. Subtotais por modalidade clínica e tabela por instrumento/complexidade."),
            ("Provisório","Intervenções AC, fisioterapia vascular periférica e reabilitação pós-COVID","Preservar quantidades observadas e normas. Análise fora dos produtos específicos definitivos."),
            ("Exploratório","Correspondências de serviço e habilitação","Verificação parcial das alternativas por CNES/mês da produção. Sem juízo individual sobre conformidade."),
            ("Não utilizável","Pacientes únicos, profissionais distintos, postos contratuais, demanda atendida","Essas contagens não são identificadas pelos indicadores implementados. A projeção exclui identificadores pessoais."),
            ("Não utilizável","Equivalência entre códigos sucessores","Mudanças de atributos estão enumeradas. Nenhuma equivalência substantiva entre códigos diferentes foi presumida.")]
        pd.DataFrame(estados_uso,columns=["status","produto","justificativa"]).to_csv(stage/"situacao_de_uso.csv",index=False)
        arquivos=[]
        for p in sorted((out/"originais-assistencia").rglob("aquisicao.json")):
            rec=json.loads(p.read_text()); dbc,=p.parent.glob("*.dbc")
            if sha256_arquivo(dbc)!=rec["sha256"] or dbc.stat().st_size!=rec["bytes"]:raise ValueError(dbc)
            arquivos.append((dbc.stem,rec["uri_oficial"],rec["bytes"],rec["sha256"],str(p),sha256_arquivo(p)))
        if len(arquivos)!=133:raise ValueError("Inventário incremental SR/LT")
        pd.DataFrame(arquivos,columns="objeto fonte bytes sha256 recibo sha256_recibo".split()).to_csv(stage/"inventario_incremental.csv",index=False)
        for nome in ("testes-etapa1.log","reposicao-lt-confronto.log"):
            if nome=="testes-etapa1.log" and "OK" not in (out/nome).read_text(encoding="utf-8-sig"):raise ValueError("Testes pendentes")
        notas="""# Checkpoint da Etapa 1

O catálogo identifica para cada indicador o campo, a unidade, os códigos, o filtro, o território, o status e o leitor. A tabela de situações de uso delimita o que pode integrar o material acadêmico. O diretório etapa1 guarda as tabelas por estabelecimento, os resíduos, o confronto com os agregados anteriores e as versões dos atributos do SIGTAP.

ST representa estabelecimentos cadastrados. SR contém serviços e classificações. A identificação de atuação clínica real exige evidência adicional. HB considera o intervalo de vigência e a existência no SIGTAP mensal. LT conserva os campos de quantidade e compara os tipos cirúrgico, clínico e complementar. EQ distingue existência, uso e a marcação SUS. PF preserva contagens de registros de vínculo e horas por modalidade e CBO. EP usa o identificador de equipe e o estado na competência. Recursos e pessoal gerais são contexto.

No SIA, o arquivo PA reúne registros de diferentes instrumentos. Segundo o informe técnico de julho de 2019, página 3, P e S representam procedimentos APAC principal e secundário, C e I identificam BPA consolidado e individualizado, A e B identificam RAAS. Antes de somar a produção, verifica-se a presença do instrumento na relação histórica. A soma cobre procedimentos registrados nos movimentos disponíveis. Uma APAC exclusiva sem evidência observada não gera zero. Outras bases APAC só devem ser incorporadas diante de lacuna material e reconciliação, para evitar dupla contagem.

A exposição territorial da oferta usa os habitantes do município ou da região. A produção usa a localização do prestador. As médias de estoques levam o número de competências válidas. Regras mensais ausentes ficam documentadas. O estoque registrado mede capacidade cadastrada, não produtividade nem acesso. Comparações normativas de serviços e habilitações medem correspondência descritiva entre sistemas.

Referências de domínios: Manual de Operação SCNES, fevereiro de 2009, tabela LFCES001; TAB_CNES / Equipamento.def e Leitos_Especialidade.def; Portaria SAES/MS 1.202, de dezembro de 2023; Informe Técnico SIA/SUS de julho de 2019; edições locais SIGTAP. O catálogo registra as mudanças de configuração sem atribuir equivalência automática entre procedimentos. Os recibos de cada competência documentam os campos efetivamente lidos e a verificação do original.
"""
        (stage/"criterios_de_uso.md").write_text(notas,encoding="utf8")
        return dict(etapa=1,liberadas="somente medidas validadas dos catálogos",recibo_integracao=json.loads(entradas["calculo"].read_text())["id"],
                    competencias=132,arquivos_incrementais=len(arquivos),itens_recursos=len(defs),codigos_pa=procs.codigo.nunique(),
                    comparacoes_pa=int(q.celulas_comparadas.sum()),residuo_pa_maximo=float(residuos.abs().max()))
    return executar(out/"checkpoint-etapa1",entradas,{"homologacoes":["Doppler e consulta contextuais","exames e três fisioterapias específicos","reposição LT condicionada ao CP04"]},medir)


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("out",type=Path)
    print(fechar(p.parse_args().out)["controles"])
