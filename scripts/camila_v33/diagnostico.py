"""Checkpoint A. Verifica as edições seladas e relaciona o manuscrito aos cálculos."""
import sys
import csv
from xml.etree import ElementTree as ET
from comum import *

# objetivo, dimensão, fonte, base, medida, numerador, denominador, unidade, estratos, produto, situação inicial
MEDIDAS=[
(99,'Mortalidade geral e prematura','SIM','B01/B02; F01–F05','Taxas diretas e brutas G0–G5','óbitos de residentes','habitantes no estrato','por 100 mil','sexo, idade, 30–69, 80+','T25','essencial','falta o comparador estrito'),
(99,'Mortalidade municipal','SIM','T08; M01','Grupo e sexo por município','óbitos por causa final','população municipal por sexo','por 100 mil','sexo, grupo','T26','complementar relevante','T08 apresenta G0'),
(99,'Insuficiência cardíaca','SIM','B03; F06','Taxas por conceito independente','óbitos que cumprem cada definição','habitantes do território','por 100 mil','conceito','T27','complementar relevante','faltam taxas por conceito'),
(99,'Internações por diagnóstico','SIH','B04/B05/B09; F07/F08','Taxas por grupo e estrato','AIHs principais de residentes atendidos em qualquer UF','habitantes no estrato','por 100 mil','sexo, idade, grupo','T24/T30','essencial','B09 separa a UF de atendimento'),
(100,'Produção por procedimento','SIA/SIGTAP','B07/T06/T07/T12/T16; F18–F23','Densidade anual por código e modalidade','quantidade aprovada por prestadores locais','população do território','procedimentos por 100 mil','código, classe e modalidade','T21/T22','essencial','faltam densidades e comparador'),
(100,'Utilização ambulatorial por residência','SIA/PA','T12/T16','Cobertura de pessoas residentes','pessoas residentes atendidas','população de residentes elegíveis','%','indivíduo','limites','inadequada','localização e quantidade não identificam residentes únicos'),
(101,'Oferta cadastrada','CNES','B06/T05/T15; F11–F17/M02','Média mensal, dezembro e respectivas densidades','estoques mensais cadastrados','habitantes do território','unidade do recurso e por 100 mil','id de recurso, SUS','T23','essencial','falta anual municipal e comparador'),
(101,'Operação efetiva','CNES','T17–T19','Funcionamento do serviço','unidades efetivamente operantes','unidades cadastradas','%','estabelecimento','limites','inadequada','cadastro e produção não demonstram funcionamento integral'),
(102,'Fluxos hospitalares','SIH','T01/T02/T03/T11; F10/F25','Distribuição anual de origem e destino','AIHs por município de residência e destino','AIHs do território para proporções','AIHs e %','origem e destino','T28/T29','essencial','faltam pares municipais no pacote'),
(103,'Comparador territorial','SIM/SIH/CNES/SIA','T09/T10; F07/F23','Norte, demais regiões mapeadas e residual estadual','contagens territoriais em cada sistema','população do território','contagens e taxas por 100 mil','quatro regiões PDR/ES','T20/T25','essencial','distinguir município ignorado e completar T10'),
(104,'Integração descritiva','SIM/SIH/CNES/SIA/SIGTAP','T10','Matriz anual com dimensões próprias','medidas temáticas referenciadas','conforme indicador','unidade de cada coluna','território e ano','T29','essencial','incluir oferta, fluxos e composição da produção'),
(99,'Estabilidade municipal','SIM','T08','Padronização direta municipal irrestrita','óbitos por idade','denominador por idade','por 100 mil','município e idade','T26','exploratória','avaliar dispersão e células pequenas antes de inferência')]
def main():
    a=Acervo()
    pins={a.f/(NOME+'_v3.2.1.zip'):'8afd4c51ec49c2a80457d4f370afd9808729bb0c074efbc69836eefe296e634b',a.f/'AUDITORIA_TCC_CAMILA_v3.2.1.zip':'42c77b3be5622946c1cbf2c91784b4076a1df56711e53f4c8b3fd0ae6663010b',a.doc:'baffb7ed43290866ba525979e98e7455c905643c1a94fa72e0dcade527f6b341'}
    for path,h in pins.items():
        if sha(path)!=h: raise ValueError(path)
    hashes={p.relative_to(a.b).as_posix():sha(p) for p in a.b.rglob('*') if p.is_file()}
    with zipfile.ZipFile(next(iter(pins))) as z:
        assert len(z.namelist())==len(hashes)==295
        for n,h in hashes.items():
            with z.open(a.b.name+'/'+n) as f: assert hashlib.file_digest(f,'sha256').hexdigest()==h
    with zipfile.ZipFile(a.f/'AUDITORIA_TCC_CAMILA_v3.2.1.zip') as z:
        import io
        manifest=list(csv.DictReader(io.TextIOWrapper(z.open('MANIFESTO_SHA256.csv'),encoding='utf8')))
        assert len(manifest)+1==len(z.infolist())
        for row in manifest:
            with z.open(row['caminho']) as f: assert hashlib.file_digest(f,'sha256').hexdigest()==row['sha256']
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(a.doc) as z:
        paras=[''.join(k.text or '' for k in v.findall('.//w:t',ns)) for v in ET.fromstring(z.read('word/document.xml')).findall('w:body/w:p',ns)]
    rows=[]
    refs={99:144,100:152,101:134,102:128,103:163,104:116}
    for obj,dim,sist,exist,med,num,den,unit,est,prod,prior,lac in MEDIDAS:
        rows.append(dict(objetivo=f'OE{obj-98}',paragrafo=obj,trecho=paras[obj-1],problema_e_objetivo_geral='introdução §§93–98',referencial=f'§{refs[obj]}',metodologia='§§160–183',dimensao=dim,sistema=sist,indicador_necessario=med,indicador_disponivel=exist,definicao_operacional=med+' segundo '+est,numerador=num,denominador=den,unidade=unit,periodo='2014–2024',territorio='ES, regiões e comparador; município nos produtos municipais',estratos=est,tabela_grafico_existentes=exist,lacuna=lac,viabilidade='limitada' if prior in ['exploratória','inadequada'] else 'calculável',agregados_privados='sim' if obj in [99,102] else 'base selada e controles privados',nova_decisao='necessária para extensão' if prior in ['inadequada','exploratória'] else 'critérios vigentes',prioridade=prior,produto=prod,situacao='avaliado no checkpoint A'))
    cp=a.w/'checkpoint-A'
    gravar(pd.DataFrame(rows),cp/'matriz_suficiencia_indicadores.csv')
    gravar(pd.DataFrame(hashes.items(),columns=['caminho_v321','sha256']),cp/'preservacao_v321.csv')
    files=[*pins,a.exp,a.parecer,a.f/'evidencias/parecer_v321.md',a.b/'06_ROTEIRO_DO_ORIENTADOR/roteiro.md',REPO/'metadata/territorio/pdr_es_2024_tcc_v1.csv',REPO/'docs/estudos/tcc_camila/registro_decisoes_metodologicas.md',a.sih/'recibo.json',a.et/'recibo.json',a.v/'taxas-ed2/recibo.json',a.v/'taxas-ed2/pesos.csv']
    gravar(pd.DataFrame([(str(p),sha(p)) for p in files],columns=['arquivo','sha256']),cp/'entradas.csv')
    nota(cp/'medidas_limitadas.md','O PA identifica quantidade e localização do prestador. Faltam identificação longitudinal de pacientes, denominador clínico de cobertura e comprovação do motivo cardiovascular das consultas. O CNES mede capacidade cadastrada. A padronização municipal requer avaliação de estabilidade dos estratos. O objetivo §103 e a metodologia §163 ainda indicam Noroeste 1. A decisão territorial vigente adota a Região Norte para aprofundamento.')
    json_out(cp/'recibo.json',{'arquivos_base':len(hashes),'membros_auditados':len(manifest),'objetivos':6,'itens':len(rows),'sha256':{p.name:sha(p) for p in cp.glob('*') if p.name!='recibo.json'}})
    print(cp, len(hashes),len(rows))
if __name__=='__main__': main()
