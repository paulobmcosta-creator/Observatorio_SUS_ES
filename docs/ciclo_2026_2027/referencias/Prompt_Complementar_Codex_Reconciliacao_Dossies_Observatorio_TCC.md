# Prompt complementar ao Codex
## Incorporação dos Dossiês 1 e 2 ao trabalho em andamento do Observatório SUS-ES

**Este comando complementa a tarefa que você já iniciou. Não reinicie o projeto, não descarte o trabalho realizado e não repita o inventário geral sem necessidade.** Dois documentos de decisões metodológicas não haviam sido fornecidos no primeiro prompt e precisam ser incorporados agora, com avaliação do impacto sobre o que já foi produzido e sobre as próximas etapas.

Leia os documentos integralmente, incluindo quadros, apêndices, notas de status e pendências. Em seguida, reconcilie as decisões com a implementação atual e execute as correções justificadas.

## 1. Documentos agora incorporados

**Dossiê 1**
Arquivo: `Dossie_1_Metodologico_Tecnico_Observatorio_SUS_ES_2026_2027_v1_0.docx`.
Título: Dossiê Metodológico e Técnico do Observatório SUS-ES — Projeto 2026–2027.
Versão 1.0, de 3 de outubro de 2026.
Função: governança institucional reutilizável de aquisição, camadas de dados, proveniência, territorialização, denominadores, semântica dos sistemas, qualidade, indicadores e comunicação.

**Dossiê 2**
Arquivo anexado: `Dossie_2_Metodologico_TCC_Camila_Atencao_Cardiovascular_v1_0 (1).docx`.
Título: Dossiê Metodológico do TCC — Atenção Cardiovascular Especializada no Espírito Santo.
Versão 1.0, de 3 de outubro de 2026.
Função: protocolo científico e analítico específico do TCC de Camila Moreira dos Santos.

O sufixo “(1)” do arquivo é parte do nome da cópia, não uma versão metodológica diferente. Preserve os originais e registre suas versões e hashes quando os incorporar ao controle documental.

O projeto institucional em PDF continua definindo objetivos, vigência, compromissos e planos de trabalho. Os dossiês detalham sua operacionalização e o protocolo temático. O primeiro prompt continua válido nas partes compatíveis; este complemento corrige sua insuficiência documental.

**Não faça alterações no relatório 2025–2026 nem em suas figuras, tabelas, links ou referências.** Eventuais incompatibilidades históricas devem ser registradas na documentação do novo ciclo, sem reescrever o relatório encerrado.

## 2. Como reconciliar documentos e implementação

Não use uma hierarquia única que confunda decisão metodológica com comprovação de execução:

- O projeto institucional define o escopo geral de 2026–2027.
- O Dossiê 1 governa as regras compartilhadas do Observatório.
- O Dossiê 2 governa as escolhas próprias do TCC cardiovascular.
- Código, dados, manifests, testes e logs demonstram o que está efetivamente implementado.
- O relatório anterior e o arquivo de contexto documentam a situação histórica.
- O primeiro prompt é orientação operacional que deve ser ajustada às decisões agora fornecidas.

Uma decisão consolidada em dossiê não comprova implementação. Uma implementação existente não invalida automaticamente uma decisão metodológica. Se houver divergência, registre-a, avalie o impacto e proponha ou execute a adequação pertinente.

Diferencie rigorosamente:
1. decisão consolidada a operacionalizar;
2. lista/código preliminar sujeito a validação histórica;
3. pendência metodológica explicitamente aberta;
4. afirmação sobre ambiente ou estado técnico a verificar no checkout atual.

Não reabra escolhas já consolidadas apenas porque chegaram depois. Também não promova uma lista preliminar a regra definitiva por estar no apêndice.

Se surgir conflito real entre documentos, fonte oficial e código, apresente a evidência e mantenha pendente somente a decisão afetada. Continue as tarefas independentes. Não modifique instruções de acesso ou governança para contornar restrições.

## 3. Primeiro passo obrigatório: localizar o avanço já realizado

Antes de editar:

1. Identifique branch, commit de referência, alterações não commitadas e entregas realizadas desde o primeiro prompt.
2. Leia os registros de execução e continuidade que você já produziu.
3. Preserve o trabalho existente. Não faça reset, limpeza destrutiva, restauração global ou substituição indiscriminada.
4. Localize somente os arquivos potencialmente afetados pelos dossiês.
5. Construa uma matriz de impacto com:
   - decisão e localização no dossiê — seção/quadro;
   - escopo institucional, temático ou compartilhado;
   - estado da decisão;
   - implementação atual e evidência;
   - arquivos, contratos, indicadores e produtos dependentes;
   - classificação: compatível; parcialmente compatível; incompatível; não implementado; não aplicável; não verificável;
   - ação: manter; completar; corrigir; recalcular; marcar como superado; aguardar evidência;
   - verificação necessária e eventual decisão humana remanescente.

**Não presuma que houve erro.** Se um componente já estiver correto, registre sua compatibilidade e reutilize-o. Determine o que o Codex efetivamente fez nesta sessão ou branch; não use o resumo histórico como substituto dessa inspeção.

Dê prioridade às divergências que alteram numeradores, denominadores, elegibilidade, agregações, períodos, chaves ou interpretação. Depois trate contratos, testes e documentação; por último, apresentação.

## 4. Separação obrigatória entre infraestrutura institucional e estudo cardiovascular

O Observatório deve fornecer infraestrutura compartilhada para SIM, SIH/SUS, SIA/SUS, CNES, SIGTAP, população e território, com incorporação progressiva conforme as dependências do projeto.

O módulo cardiovascular consome essa infraestrutura e acrescenta suas próprias definições. **Não configure todo o Observatório com período 2014–2024, CID I00–I99, Noroeste 1 ou Prais-Winsten.**

Não replique aquisição, tabela territorial ou série populacional em uma plataforma paralela para o TCC. Reutilize componentes existentes, parametrizando o que for temático. A classificação de pertencimento territorial deve continuar centralizada; a aplicação retrospectiva de uma versão territorial será configuração do estudo.

Mantenha distinguíveis:
- matriz mínima institucional e indicadores complementares/temáticos;
- indicadores principais e de aprofundamento do TCC;
- testes de qualidade do processamento e indicadores substantivos de saúde.

Não transforme todas as medidas cardiovasculares em obrigações do núcleo institucional. O painel institucional completo não é condição de conclusão do TCC, e a engenharia integral do Observatório não é atribuição da discente.

## 5. Ajuste da orientação tecnológica do primeiro prompt

**Referência: Dossiê 1, seções 4.2–4.3 e 18.**

O primeiro prompt descrevia corretamente o R validado e o estágio experimental da trilha PySUS conhecido à época. Essa descrição histórica não deve se transformar em proibição permanente de evolução tecnológica.

Adote a orientação consolidada:
- arquitetura híbrida R–Python;
- Python preferencial para aquisição, cache, engenharia e armazenamento quando a implementação estiver operacionalmente validada;
- PySUS como ferramenta possível, sem transformá-lo em requisito científico;
- acesso direto à fonte oficial ou outro método validado como alternativa documentada quando necessário;
- R preservado como referência metodológica e de paridade nos componentes já validados;
- nenhuma retirada de componente sensível sem equivalência funcional e metodológica demonstrada.

Diferencie cobertura por sistema e família de arquivos. Uma falha de ST não prova inviabilidade de todo Python/PySUS; um download bem-sucedido não prova validade das chaves e transformações.

Python 3.12 e PySUS 2.0.4 são versões mencionadas no histórico do dossiê: examine o ambiente atual e registre a configuração utilizada, sem impor atualização ou rebaixamento automático.

Não migre por conveniência estética. Se o incremento em R já produzido for compatível com os contratos comuns, preserve-o. Quando desenvolver aquisição em Python, mantenha manifestos, schemas, interfaces e testes independentes da linguagem. Continue distinguindo o script Python da RUE da trilha PySUS.

## 6. Regras institucionais com impacto sobre produtos existentes

### 6.1 Camadas e proveniência
**Dossiê 1, seções 4.1 e 5.**

Preserve as funções RAW → INTERIM/STAGING → ANALYTIC/PROCESSED → OUTPUT. Não renomeie toda a árvore apenas para reproduzir os rótulos do dossiê: documente a correspondência com os diretórios existentes.

RAW deve permanecer imutável. Filtros substantivos, exclusões e classificações devem ser rastreáveis. Inclua nos manifestos sistema/família, abrangência, competência, arquivo original, origem oficial, data/hora, bytes, SHA-256, contagens, schema, versão do pipeline, responsável real e observações.

Uma nova execução não substitui a evidência de uma execução histórica cujo manifesto esteja ausente. Preserve snapshots e registre a linhagem dos novos derivados.

### 6.2 Território e população
**Dossiê 1, seção 7; Dossiê 2, seções 6 e 8.**

Use chave municipal canônica e tabela territorial central, com fonte e versão. Preserve código original e código harmonizado. Não converta formatos por truncamento ou preenchimento sem regra comprovada.

Mantenha separados residência, atendimento, município gestor e localização da oferta. Não impute residência a partir do estabelecimento ou CEP para contornar ausência.

Use uma série populacional harmonizada por estudo, com estratos compatíveis. Agregações regionais são derivadas dos municípios. Não insira denominadores de outra metodologia no meio da série sem decisão documentada.

A população residente total é o denominador padrão dos indicadores populacionais; **não subtraia automaticamente beneficiários de planos de saúde para estimar uma população “exclusivamente SUS”**. Indicadores de cobertura privada do primeiro ciclo permanecem históricos, sem determinar os denominadores do segundo ciclo.

### 6.3 Semântica dos sistemas
**Dossiê 1, seção 8.**

- SIM: óbitos; causa básica segundo a definição do estudo.
- SIH: internações/AIH registradas, não pessoas únicas; diagnóstico principal para morbidade; valores aprovados/reembolso não equivalem a custo econômico.
- SIA: quantidade de procedimentos, preferencialmente aprovada; quantidade apresentada preservada para auditoria; seleção por procedimento e, quando necessário, CBO.
- CNES: cadastro mensal de oferta; distinguir estabelecimento, habilitação/serviço, leito, equipamento, pessoa, vínculo e carga horária.
- Fluxos ambulatoriais dependem da qualidade da residência; ausência não significa origem externa ou evasão.

A expressão internação/AIH não dispensa explicitar o tratamento de tipos de AIH, continuidade e reapresentações conforme a pergunta e o layout. Não invente regra geral de deduplicação.

### 6.4 Estoques mensais CNES
**Dossiê 1, seção 9; Dossiê 2, seção 15.**

A competência integra a chave. A síntese anual principal de estoque quantitativo é a **média mensal das competências válidas**, acompanhada de quantidade de meses observados. Preserve última competência válida, mínimo, máximo e meses ativos quando pertinentes.

Não some estoques mensais. Não preencha mês ausente com zero automaticamente. Diferencie ausência de recurso em competência observada de ausência do arquivo/competência. Uma média de ano incompleto deve permanecer identificada como parcial, sujeita à regra de qualidade definida.

Profissionais distintos, vínculos e carga horária SUS são medidas separadas. Recalcule pessoas distintas em cada nível territorial; somar pessoas distintas dos municípios pode duplicar profissionais na região. Preserve as restrições aplicáveis a identificadores individuais e publique produtos agregados.

### 6.5 SIGTAP histórico
**Dossiê 1, seção 10; Dossiê 2, seção 14 e Apêndice A.**

Não aplique a lista atual de procedimentos a toda a série. Modele código, competência, vigência, descrição e conceito analítico, com relações históricas necessárias.

Mantenha a infraestrutura SIGTAP no núcleo comum e as whitelists cardiovasculares no módulo temático. Códigos candidatos não verificados devem conservar status preliminar. Não invente continuidade histórica, equivalência clínica ou vigência para preencher lacunas.

### 6.6 Exclusões, qualidade e validação
**Dossiê 1, seção 11; Dossiê 2, seções 20–21.**

Não use exclusão global por casos completos nem deduplicação genérica. Um registro pode ser elegível para total e inelegível para estratificação. Diferencie ausente, ignorado, inválido, não aplicável, duplicidade física comprovada e evento repetido legítimo.

No TCC, preserve os motivos EX01–EX07 definidos no Quadro 21, vinculados à análise. Se vários motivos se aplicarem à mesma linha, não some contagens sobrepostas como perdas únicas.

Meça completude, integridade temporal e territorial, rupturas e impacto das exclusões. Limiares de publicação/supressão permanecem pendentes; não invente percentuais aprovados ou corte universal de 10/20 eventos.

TABNET ou outra interface oficial serve a checagens sentinelas do processamento, não como prova independente da qualidade epidemiológica da mesma fonte. Não imponha conferência manual de cada resultado.

## 7. Decisões consolidadas exclusivas do TCC cardiovascular

**Dossiê 2, seções 2–19 e Quadro 24.** Estas decisões devem orientar o módulo, preservando as pendências do Quadro 25.

### Recorte e território
- Objeto: atenção cardiovascular especializada; não avaliação integral da linha de cuidado, resolutividade ou suficiência.
- Período empírico: **2014–2024**, onze anos.
- Preservar granularidade mensal necessária para SIH, SIA, CNES e SIGTAP; a apresentação predominante é anual.
- Comparação principal pelas quatro Regiões de Saúde **Norte, Central, Metropolitana e Sul**, segundo a versão oficial selecionada pelo protocolo.
- Aplicação retrospectiva dessa classificação à série, explicitada como harmonização territorial; não representa a governança administrativa de cada ano.
- **Noroeste 1** é recorte focal sub-regional, comparado à Região Norte e ao Espírito Santo, não uma quinta Região de Saúde.
- A composição municipal e a versão territorial precisam ser verificadas e congeladas em fonte oficial. Não deixe um pipeline mudar automaticamente as regiões de um estudo congelado quando houver atualização da tabela institucional.
- Os conjuntos focal, regional e estadual se sobrepõem; não são grupos independentes nem parcelas somáveis.

Não atualize automaticamente o término do TCC para a competência mais recente do projeto institucional. Não reutilize sem revisão o agrupamento histórico Central-Norte do primeiro ciclo.

### Universo e grupos
- G0: I00–I99.
- G1: I20–I25 — doenças isquêmicas do coração.
- G2: I50 — insuficiência cardíaca.
- G3: I60–I69 — doenças cerebrovasculares.
- G4: I10–I15 — doenças hipertensivas.
- G5: I70–I79 — doenças arteriais/arteriolares/capilares.

G0 contém os grupos específicos: não some G0 a G1–G5. Estes grupos não esgotam necessariamente todo I00–I99. Doenças cerebrovasculares não devem ser vinculadas automaticamente à oferta de cardiologistas. Hipertensão não representa exclusivamente desempenho da atenção especializada.

AVC agudo I60–I64 e seus subgrupos são aprofundamentos previstos. A definição CID final do IAM continua pendente: não escolha silenciosamente entre conjuntos possíveis.

### Mortalidade e denominadores
- Causa básica e residência como referências principais.
- Taxas brutas e padronizadas; método direto com **população brasileira de 2010** como padrão.
- Faixas quinquenais de 0–4 até 80–84 e 85 anos ou mais.
- Mortalidade prematura: **30–69 anos**, com taxa específica e padronizada no intervalo.
- Para o intervalo restrito, explicite os pesos e sua normalização, garantindo correspondência entre numerador, denominador e padrão.
- Faixas de apresentação: <30; 30–39; 40–49; 50–59; 60–69; 70–79; ≥80. Elas não substituem os estratos quinquenais usados no cálculo.
- Não denomine a taxa cardiovascular prematura como ODS 3.4.1.
- A fonte/versão da série populacional harmonizada ainda precisa ser congelada. Não confunda a população padrão de 2010 com os denominadores anuais de 2014–2024.

### Produção, oferta e fluxos
- Consultas específicas: procedimento genérico combinado ao CBO pertinente; procedimento isolado não identifica a especialidade.
- Cintilografia em esforço e repouso mantém componentes; não somar como usuários únicos.
- Alta complexidade organizada nas famílias AC1–AC7 do dossiê; respeitar relações de inclusão entre famílias, evitando dupla contagem em totais.
- CNES: habilitações, leitos SUS pertinentes, profissionais e equipamentos cardiovasculares; códigos históricos ainda sujeitos à conferência.
- Atendimento na própria região, evasão, atração e destino externo principal; não chamar permanência territorial de resolutividade.
- Explicite o denominador de cada fluxo e as perdas por origem/destino ignorados. Não produza um complemento de 100% artificial quando houver destinos não classificados.
- Verifique se a extração cobre atendimentos de residentes do ES realizados fora do estado e não residentes atendidos no ES. Uma extração limitada a arquivos por UF do prestador pode ser insuficiente para medir evasão. Documente a cobertura requerida antes de qualquer download amplo.

### Análise
- Indicador principal não significa teste estatístico obrigatório.
- Comparações territoriais por valores observados, diferenças e razões válidas; nenhum índice sintético ponderado arbitrário.
- Integrações carga × oferta × utilização × fluxos em nível territorial e temporal, sem linkage individual ou inferência causal.
- Prais-Winsten restrito a séries centrais adequadas; transformação log10 e VPA = (10^β1 − 1) × 100, com IC95%.
- Não aplique logaritmo a zeros nem acrescente constante arbitrária. Registre elegibilidade, estabilidade, comparabilidade e diagnósticos.
- Se a seleção entre versões bruta/padronizada de mortalidade prematura para tendência não estiver operacionalmente fechada, registre a decisão a resolver; não modele todas automaticamente.
- Variação entre extremos 2014/2024 não é, isoladamente, tendência.
- Não introduza Joinpoint rotineiro, bateria de correlações ou modelos causais.
- Mantenha **2020–2022** e identifique o período atípico; não exclua nem modele como intervenção causal automaticamente.

## 8. Pendências que devem continuar visíveis

Transcreva e acompanhe as pendências do Dossiê 1, Quadro 18, e Dossiê 2, Quadro 25, vinculando-as às tarefas afetadas:
- cobertura de aquisição por sistema/família e alternativas oficiais;
- paridade R–Python;
- infraestrutura histórica SIGTAP;
- composição territorial, inclusive Noroeste 1;
- fonte e versão populacional;
- lista mínima institucional;
- definição final do IAM;
- whitelists SIA e de alta complexidade;
- habilitações, CBOs, leitos/UCO e equipamentos históricos;
- qualidade da residência no SIA;
- critérios de pequenos números e publicação;
- enquadramento ético/institucional conforme o desenho efetivo.

O Apêndice A do TCC é uma especificação de trabalho. Extraia códigos como texto, preservando zeros e a descrição original, junto à normalização para processamento; não os apresente como validados sem fonte por competência.

O enquadramento registrado para o primeiro ciclo não deve ser copiado automaticamente para todo estudo futuro. Registre a verificação pertinente ao novo desenho, sem inventar aprovação ou dispensa, e sem alterar o relatório encerrado.

## 9. Correção do trabalho já feito e rastreabilidade

Após a matriz de impacto, execute as correções comprovadamente necessárias:

1. Separe parâmetros institucionais dos cardiovasculares se tiverem sido misturados.
2. Atualize contratos e testes quando necessário antes de recalcular produtos.
3. Preserve implementações válidas e adapte os componentes afetados.
4. Identifique resultados derivados de regras incompatíveis e seus consumidores.
5. Recalcule apenas os dependentes de mudanças efetivas, com nova versão e manifesto. Se faltarem insumos, marque-os como pendentes de recálculo e não como resultados atuais validados.
6. Compare versão anterior e nova em esquema, contagens, cobertura, elegibilidade e resultados pertinentes, explicando a causa das diferenças.
7. Atualize o plano de continuidade já existente, em vez de criar outro planejamento concorrente.
8. Registre decisões e provenance com localização precisa nos dossiês. Preserve os DOCX originais; crie representações operacionais em Markdown/CSV/YAML apenas quando úteis e sem perder ressalvas.

Esta rodada autoriza reconciliar e corrigir o trabalho em andamento. Não é ordem para executar, de uma só vez, todos os cálculos de onze anos, todos os procedimentos, todos os sistemas e todo o TCC.

Não faça merge na branch principal, publicação externa ou alteração de permissões. Preserve alterações de terceiros e respeite as instruções aplicáveis ao repositório.

## 10. Verificação e entregas da rodada

Selecione verificações relevantes aos componentes efetivamente alterados. Exemplos:
- síntese anual CNES não soma estoques e informa meses válidos;
- mês ausente não vira zero;
- profissional em dois municípios não é duplicado na contagem regional de pessoas;
- código fora da vigência SIGTAP não entra indevidamente na seleção;
- ausência de idade pode impedir padronização sem eliminar o registro do total elegível;
- consulta genérica sem CBO pertinente não é classificada automaticamente como cardiologia;
- Noroeste 1 é subconjunto focal, não região independente;
- taxas agregadas usam numerador/denominador agregados, não média simples de taxas;
- regras do TCC não vazam para módulos institucionais;
- fluxos tratam destinos externos e ignorados explicitamente.

Não crie testes artificiais para simplesmente reproduzir a implementação. Dados sintéticos usados em testes devem estar identificados como fixtures e separados das evidências empíricas. Se um teste não puder ser executado, informe a razão e não o classifique como aprovado.

Entregue:
1. **Matriz de impacto dos dois dossiês sobre o trabalho já realizado**, com decisões compatíveis e incompatíveis.
2. **Registro de reconciliação metodológica**, indicando o que mudou em relação ao primeiro prompt.
3. **Alterações concretas em contratos, configuração, código, testes ou documentação**, conforme os achados.
4. **Lista de produtos que precisam de recálculo**, ou confirmação fundamentada de que nenhum recálculo foi necessário.
5. **Plano de continuidade atualizado**, separando infraestrutura comum, módulo cardiovascular e pendências.
6. **Ponto exato de retomada**, incluindo branch/commit ou diff revisável e próxima tarefa.

Consolide esses itens em arquivos existentes quando apropriado. Não multiplique documentos sem função.

Na resposta final, diga objetivamente: o que já estava correto; o que foi corrigido; quais resultados foram recalculados; o que ainda depende de dados ou decisão; e qual é o próximo incremento. Não afirme que tudo foi validado apenas porque o dossiê foi incorporado.

**Comece pela leitura integral dos dois dossiês e pela inspeção do avanço já realizado. Faça a reconciliação delimitada, execute as adequações necessárias e retome o desenvolvimento a partir do estado corrigido.**

