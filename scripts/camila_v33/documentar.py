"""Índice, dicionário e orientação de uso das medidas derivadas."""
from comum import *
# Tabela, pasta, nome, sistema, tempo, numerador, denominador, critério/limite.
TABELAS={
'T20':('cruzamentos_integrados','Comparador anual e confronto de T10','SIM/SIH/CNES/SIA','ocorrência, processamento, cadastro e produção','medidas de T10 e estoques/quantidades anuais','população do território','SIM e SIH residuais. CNES e PA em estabelecimentos localizados.'),
'T21':('producao_sia','Produção localizada por código','SIA/SIGTAP','competência de produção PA_CMP','quantidades aprovadas ou apresentadas em códigos elegíveis','população anual','Total anual de código exige 12 meses válidos. A soma nos meses válidos tem coluna própria.'),
'T22':('producao_sia','Produção localizada por modalidade','SIA/SIGTAP','competência de produção PA_CMP','quantidade de procedimentos de códigos elegíveis a cada mês','população anual','ECG, demais exames e fisioterapia formam o total. Doppler e consultas por CBO são contextuais.'),
'T23':('oferta_cnes','Capacidade cadastrada anual e em dezembro','CNES','competências cadastrais','média de estoques ou estoque de dezembro','população anual','SUS segundo o campo de origem. Distinga vínculos, estabelecimentos, horas e equipamentos.'),
'T24':('internacoes','Internações por diagnóstico e sexo','SIH/RD','ano de processamento','AIHs principais de residentes, todas as UFs de atendimento','habitantes no estrato territorial e demográfico','G0 contém G1–G5 e demais circulatórias. As taxas diretas usam idades conhecidas.'),
'T25':('mortalidade','Mortalidade por grupo, sexo, universo e padrão','SIM','ano do óbito','óbitos de residentes pela causa básica final','habitantes do estrato','Direta por idade. A bruta geral inclui idade ignorada no numerador.'),
'T26':('mortalidade','Mortalidade municipal por grupo e estrato','SIM','ano do óbito','óbitos pela causa básica final de residentes conhecidos','habitantes no município, no sexo ou na idade','Estratos total, sexo e idade em linhas separadas. Células pequenas geram taxas instáveis.'),
'T27':('mortalidade','Insuficiência cardíaca por conceito','SIM','ano do óbito','declarações que atendem a cada conceito separadamente','habitantes do território','Final, original, causa ampliada e menções podem coexistir. Sem denominador para residência municipal ignorada isolada.'),
'T28':('fluxos','Matriz municipal anual de origem e destino','SIH/RD','ano de processamento','AIHs principais de residentes do ES ou atendidas no ES','nenhum para contagem','Pares observados de origem e destino, com UF de atendimento. Não revela trajetórias individuais.'),
'T29':('cruzamentos_integrados','Matriz anual integrada','SIM/SIH/CNES/SIA/SIGTAP','tempo próprio de cada coluna','medida da tabela temática vinculada','denominador temático','Regionalização PDR/ES. Oferta e produção no comparador estrito. Linha residual preservada no SIM e SIH.'),
'T30':('internacoes','Utilização por idade, sexo e grupo','SIH/RD','ano de processamento','AIHs principais de residentes com diagnóstico do grupo','habitantes do estrato','Faixas quinquenais e 80+. Idade -1 ou sexo ignorado sem denominador.'),
'T31':('fluxos','Utilização, evasão, atração e deslocamento regional','SIH/RD','ano de processamento','AIHs por origem ou destino conforme campo','residentes para evasão e atendidas para atração','Interregional considera duas regiões conhecidas e distintas dentro do ES.')}
BASE={'T20':'T10/B06/T07','T21':'B07/T12/T16','T22':'B07/T07/T12/T16','T23':'B06/T15','T24':'B05/B09/T30 e pesos.csv','T25':'B01/B02 e pesos.csv','T26':'estratos anuais SIM e margens_conjuntas.csv','T27':'B03 e população anual','T28':'fluxos.csv certificados pelo SIH nacional','T29':'T22/T23/T24/T25/T31','T30':'fluxos.csv, conversao_demografica.csv e B05','T31':'T28, T01 e T02'}
def fonte_col(col):
    if col=='habitantes' or col.startswith('sim_') or col=='obitos':return 'T25'
    if col.startswith('sih_'):return 'T24'
    if col.startswith('pa_'):return 'T22'
    if col.startswith('cnes_'):return 'T23'
    return 'T31'
LIMITES="""# Limites de comparabilidade

O SIM usa ano de ocorrência e residência. A taxa bruta geral admite idade ignorada no numerador. O padrão Brasil 2022 é principal e o Brasil 2010 é complementar. Nas taxas diretas as taxas de idade conhecida recebem os pesos dos 17 estratos, com faixa final de 80 anos ou mais. Na prematura os pesos são renormalizados entre 30 e 69 anos.

T20 preserva a convenção histórica de T10. O residual estadual menos Norte inclui residentes do ES com município ignorado. Em T25 e T29 o comparador estrito soma Central, Metropolitana e Sul, inclusive os numeradores e denominadores etários antes de ponderar. As medidas de PA e CNES são localizadas pelos estabelecimentos e aparecem na linha estrita de T29. A linha residual fica em branco nessas colunas. A série SIH de T31 contém dois comparadores segundo o lado da medida, residência para evasão e destino para atração.

O SIH usa ano de processamento e conta AIHs principais. B08 documenta 27 UFs por competência. T04 mantém o ano de admissão em separado. A atração interestadual exige origem reconhecida fora do ES. Os fluxos são observados, sem informação de fila ou referência formal.

No SIA, a produção se refere à competência da realização registrada e aos movimentos disponíveis até dezembro de 2024. O mês final pode receber lançamentos posteriores. A unidade é o procedimento, com repetições possíveis entre pessoas. O denominador ecológico inclui habitantes do território onde o prestador está localizado. A composição do total específico pode variar com a vigência mensal dos códigos. Consulta por CBO e Doppler vascular são contextuais. AC, reabilitação pós-COVID e fisioterapia vascular periférica mantêm as classificações anteriores e permanecem fora do total.

A disponibilidade do CNES é cadastral. Médias de 12 competências e estoques de dezembro têm colunas diferentes. A média dos meses válidos pode existir com cobertura parcial. Consultar a unidade e a regra de cada ID no catálogo histórico. Habilitações podem coexistir no mesmo estabelecimento. Horas e vínculos preservam a unidade cadastral.

Nas tabelas municipais, um zero observado tem competência e universo verificados. A ausência de linha PA pode representar ausência de registro elegível após a reconciliação de ambos os campos de quantidade, em cada código, competência e região. A ausência de edição válida é não aplicável. Sem denominador, a taxa permanece vazia. Em 320405 foram encontrados estabelecimentos cadastrados em todas as competências. A ausência de registros elegíveis no recorte estudado não descreve a assistência total do município."""
def documentar(a,figs):
    cp=a.w/'checkpoint-B'
    doc=a.e/'07_DOCUMENTACAO_METODOLOGICA'
    ini=a.e/'00_LEIA_PRIMEIRO'
    old=ler(ini/'inventario_produtos.csv')
    novos=[]
    catalog=[]
    def verbete(id,tab,col,nome,formula,unid):
        sub,n,sist,tempo,num,den,lim=TABELAS[tab]
        figs_ids=', '.join(figs[figs.base==tab].id)
        catalog.append(dict(id=id,nome=nome,definicao_conceitual=n,definicao_operacional=f'{col} segundo os estratos de {tab}',formula=formula,numerador=num,denominador=den if ('100 mil' in unid or unid=='%' or 'direta' in col) else 'não se aplica à contagem ou conforme campo',unidade=unid,sistema=sist,periodo='2014–2024',temporalidade=tempo,territorio='conforme chave territorial da tabela',estratificacoes={'T21':'código e grupo clínico','T22':'modalidade','T23':'ID cadastral e tipo de estoque','T24':'grupo e sexo','T25':'sexo, grupo, universo e censo','T26':'município, grupo, sexo ou idade','T27':'conceito de I50','T28':'municípios de origem e destino e UF','T30':'grupo, sexo, idade','T31':'origem ou destino'}.get(tab,'ano e território'),vigencia='competência SIGTAP válida' if tab in ('T21','T22') else ('domínio cadastral no mês' if tab=='T23' else 'janela anual e cobertura da fonte'),criterio_inclusao_exclusao=lim,situacao='verificado nos controles v3.3',limitacoes=lim,tabela=tab,figuras=figs_ids,fonte=BASE[tab],script='scripts/camila_v33',recibo='08_REPRODUTIBILIDADE/recibos/checkpoint-B.json',edicao='v3.3; código clínico e série-base conforme catálogo v3.2.1'))
    def medida(c,t):
        if c=='habitantes': return 'População anual no estrato','habitantes'
        if c=='meses' or c.startswith('meses_'): return 'Contagem de competências segundo a condição da coluna','meses'
        if 'direta' in c or 'padronizada' in c:return '100 mil × soma de (eventos etários / população etária) × peso censitário','por 100 mil'
        if '100mil' in c or c.startswith(('sim_bruta','sih_bruta')):return '100 mil × numerador / habitantes no estrato','por 100 mil'
        if 'pct' in c:return '100 × AIHs do fluxo / AIHs do universo territorial correspondente','%'
        if c.startswith('media') or 'sr116_media' in c or c.startswith('cnes_media'):return 'Soma dos estoques mensais válidos / meses válidos; média anual integral exige 12 competências','unidade do recurso'
        if t=='T23':return 'Estoque registrado no mês de dezembro','unidade do recurso'
        if t in ('T21','T22') or c=='aprovadas':return 'Soma das quantidades do campo no período elegível','procedimentos'
        if t in ('T24','T28','T30','T31') or c=='aih_residentes':return 'Contagem de AIHs principais elegíveis no recorte','AIHs'
        return 'Contagem de declarações elegíveis segundo o campo','óbitos'
    for id,(sub,titulo,sist,tempo,num,den,lim) in TABELAS.items():
        path=next(cp.glob(id+'.csv*'))
        alvo=a.tab/sub/path.name
        alvo.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,alvo)
        df=ler(path)
        novos.append(dict(id=id,tipo='Tabela',titulo=titulo,periodo='2014–2024',territorio='conforme dimensão territorial',unidade='ver dicionário por campo',fonte=sist,numerador_denominador=num+' / '+den,notas=lim,status='verificado',base=BASE[id],tabela=alvo.relative_to(a.e).as_posix(),figura='',script='scripts/camila_v33'))
        campos=set('ano territorio municipio municipio_res municipio_at uf_atendimento regiao_res regiao_at regiao sexo sexo_sim idade_inicio grupo universo censo conceito codigo grupo_clinico modalidade id estrato valor situacao'.split())
        for c in [c for c in df if c not in campos]:
            orig=fonte_col(c) if id=='T29' else id
            form,un=medida(c,orig)
            verbete(id+'.'+c,orig,c,c.replace('_',' '),form,un)
            if id=='T29':
                catalog[-1]['tabela']='T29 e '+orig
                catalog[-1]['fonte']=orig
                catalog[-1]['figuras']='F32; consultar também figuras temáticas'
            if c=='idade_ignorada':
                catalog[-1]['formula']='Contagem de eventos com idade indeterminada'
            if c=='habitantes':
                catalog[-1]['numerador']='habitantes segundo a edição populacional e o estrato'
            if c in ('evasao_pct','atracao_pct'):
                catalog[-1]['numerador']='AIHs de residentes atendidos fora do ES' if c=='evasao_pct' else 'AIHs na área de atendimento com origem reconhecida em outra UF'
                catalog[-1]['denominador']='AIHs dos residentes' if c=='evasao_pct' else 'AIHs atendidas na área'
            if c in ('atendimento','interregional_es','evasao_aih','atracao_aih'):
                catalog[-1]['definicao_operacional']={'atendimento':'AIHs atendidas no território','interregional_es':'AIHs de residentes atendidos em outra região conhecida do ES','evasao_aih':'AIHs de residentes atendidos em outra UF','atracao_aih':'AIHs atendidas no território com origem reconhecida em outra UF'}[c]
    shutil.copyfile(cp/'T29_longa.csv.gz',a.tab/'cruzamentos_integrados/T29_longa.csv.gz')
    for f in ['controle_320405.csv','estabilidade_municipal.csv.gz']:
        alvo=a.tab/'indicadores_derivados'/f
        alvo.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(cp/f,alvo)
    for f in figs.itertuples():
        novos.append(dict(id=f.id,tipo='Mapa' if f.id=='M02' else 'Gráfico',titulo=f.titulo,periodo=f.periodo,territorio=f.territorio,unidade=f.unidade,fonte=f.fonte,numerador_denominador='Consultar '+f.base,notas=f.nota,status='verificado',base=f.base,tabela=f.caminho+'.csv',figura=f.caminho+'.svg',script='scripts/camila_v33/visuais.py'))
    inv=gravar(pd.concat([old[old.id!='M02'],pd.DataFrame(novos)],ignore_index=True),ini/'inventario_produtos.csv')
    candidates=ler(a.w/'checkpoint-A/matriz_suficiencia_indicadores.csv')
    candidates['situacao']=np.where(candidates.prioridade.isin(['inadequada','exploratória']),'limitação documentada','incorporado e verificado')
    gravar(candidates,ini/'matriz_suficiencia_indicadores.csv')
    gravar(candidates[['objetivo','paragrafo','trecho','dimensao','produto','situacao']],doc/'matriz_objetivos_indicadores.csv')
    gravar(pd.DataFrame(catalog),doc/'dicionario_indicadores.csv')
    shutil.copyfile(REPO/'docs/estudos/tcc_camila/registro_decisoes_metodologicas.md',doc/'registro_decisoes_metodologicas.md')
    nota(doc/'limites_de_comparabilidade.md',LIMITES)
    est=ler(cp/'estabilidade_municipal.csv.gz')
    nota(doc/'indicadores_nao_calculaveis.md',f"""# Medidas de uso limitado

A cobertura de pacientes residentes em PA carece de identificação individual e territorial adequada. As consultas por CBO tampouco identificam o motivo clínico. O funcionamento efetivo dos serviços carece de observação operacional. A correlação causal entre oferta e mortalidade extrapola o desenho ecológico.

A padronização municipal irrestrita foi classificada como exploratória. Entre {len(est)} combinações de município, ano e grupo, {int(est.estratos_zero.gt(0).sum())} têm ao menos uma faixa quinquenal sem óbitos. O arquivo de estabilidade informa também os estratos com um a quatro óbitos e o menor denominador. T26 conserva taxas brutas e específicas por sexo ou idade, sem modelo de suavização. Uma interpretação de estimativas padronizadas municipais exigiria decisão sobre precisão. O pacote é de circulação restrita.

Atribuir causa administrativa à ruptura de I50 exigiria evidência específica. T27 oferece definições independentes por declaração. É inadequado somar as colunas de causas e menções.""")
    resumo='A edição acrescenta T20–T31, nove gráficos F26–F34 e a geometria regional de M02. B01–B09 e T01–T19 conservam os dados da edição-base. T20 completa os campos assistenciais de T10. O dicionário v3.3 detalha as variáveis adicionais. O catálogo histórico mantém as definições e vigências anteriores.'
    nota(ini/'resumo_das_alteracoes_v33.md','# Alterações quantitativas v3.3\n\n'+resumo)
    linhas=['# Atenção cardiovascular no Espírito Santo, 2014–2024','', 'Edição quantitativa v3.3 · Entrega acadêmica da Camila','',resumo,'','[Matriz de suficiência](matriz_suficiencia_indicadores.csv) · [Dicionário](../07_DOCUMENTACAO_METODOLOGICA/dicionario_indicadores.csv) · [Limites](../07_DOCUMENTACAO_METODOLOGICA/limites_de_comparabilidade.md) · [Manual](../05_MANUAL_DA_ESTUDANTE/manual.md) · [Roteiro](../06_ROTEIRO_DO_ORIENTADOR/roteiro.md)','', '[Matriz em formato longo](../02_TABELAS/cruzamentos_integrados/T29_longa.csv.gz) · [Estabilidade municipal](../02_TABELAS/indicadores_derivados/estabilidade_municipal.csv.gz) · [Cobertura em 320405](../02_TABELAS/indicadores_derivados/controle_320405.csv)']
    for tipo,g in inv.groupby('tipo',sort=False):
        linhas+=['','## '+tipo,'']
        for r in g.itertuples():
            fig=r.figura if isinstance(r.figura,str) else ''
            linhas.append(f'- [{r.id} · {r.titulo}](../{fig or r.tabela})'+(f' · [Dados](../{r.tabela})' if fig else ''))
    nota(ini/'indice_geral.md','\n'.join(linhas))
    for rel,extra in [('05_MANUAL_DA_ESTUDANTE/manual.md','Comece com T29 para escolher domínio e território. Use T20 para reproduzir a antiga T10. Para a comparação territorial use a linha estrita em T25/T29 e confira o resíduo em T09. Na produção, leia F26–F28 junto com a vigência em T21. Para o município, examine o número de meses válidos e a tabela de estabilidade antes de comparar taxas. Em arquivos CSV.GZ, descompacte primeiro para abrir o CSV num editor de planilhas. O ponto decimal e a vírgula delimitadora seguem os arquivos de origem.'),('06_ROTEIRO_DO_ORIENTADOR/roteiro.md','Para os objetivos dos §§99–104, consulte a matriz objetivos × indicadores. Peça à estudante que identifique o universo e o denominador de cada painel de F32 e descreva a diferença entre o residual estadual e o comparador estrito. Na revisão do §103 e do §163, alinhe o território focal à decisão sobre a Região Norte. Atribuição causal e interpretação clínica exigem evidência própria.'),('00_LEIA_PRIMEIRO/guia_de_navegacao.md','Abra indice_geral.md para navegar na edição v3.3. T20–T31, F26–F34 e M02 constam do inventário e do índice.')]:
        p=a.e/rel
        nota(p,'# Complementação v3.3\n\n'+extra+'\n\n## Material de orientação herdado da edição v3.2.1\n\n'+p.read_text(encoding='utf8'))
    return inv
