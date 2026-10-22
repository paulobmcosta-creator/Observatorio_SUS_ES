# Prompt atualizado — revisão crítica e planejamento integral do Observatório SUS-ES
Versão: 2.0 — 22/10/2026
Finalidade: executar a revisão e o planejamento no Codex; submeter essa etapa a uma segunda revisão no ChatGPT antes da implementação ampla.

## Orientação de uso

Envie este arquivo na mesma conversa do Codex em que a branch está sendo desenvolvida. Cole a mensagem:

> Execute o prompt atualizado anexado. Nesta rodada, realize a revisão crítica e o planejamento integral do Observatório SUS-ES, considerando a agenda do relatório e todos os objetivos e produtos do projeto 2026–2027. Fundamente as decisões com os documentos, o código, os produtos existentes e testes delimitados quando necessários. Atualize o planejamento vigente e prepare uma entrega rastreável para uma segunda revisão no ChatGPT. Preserve os avanços válidos. Encerre no ponto de revisão definido no prompt, antes da implementação ampla. Não altere o relatório 2025–2026.

Este prompt substitui, para a próxima rodada, as instruções de implementação ampla do arquivo Revisao_Critica_Prompt_Continuidade_Integral_Observatorio_2026_2027.md. O parecer contido naquele arquivo continua sendo uma referência a verificar. As decisões metodológicas consolidadas dos dossiês e as evidências anteriores permanecem válidas em seus respectivos escopos.

Se o Codex já tiver avançado além do estado mencionado abaixo, examine os avanços e incorpore-os à revisão. Não faça reset, reversão ou exclusão para retornar ao ponto anterior.

---

# INÍCIO DO PROMPT EXECUTÁVEL

## 1. Objetivo e limite desta rodada

Realize uma revisão crítica integrada do trabalho existente e prepare um plano completo, justificável e executável para:

1. dar continuidade à agenda elencada no relatório encerrado de 2025–2026;
2. cumprir todos os objetivos e produtos previstos no projeto 2026–2027;
3. incorporar as decisões dos dossiês institucional e cardiovascular;
4. aproveitar os componentes adequados e identificar o que deve ser corrigido, ampliado, substituído ou preservado apenas como histórico.

O resultado desta rodada será submetido a uma segunda revisão no ChatGPT, com o coordenador, antes da implementação ampla. Você deve concluir a revisão e o planejamento e preparar a passagem de trabalho.

Estão incluídos nesta rodada:
- leitura dos documentos e inspeção do acervo acessível;
- exame do código, configurações, dados, evidências e histórico pertinente;
- comparação de alternativas suficientemente aprofundada para decidir;
- testes diagnósticos e provas de conceito delimitadas quando resolverem uma incerteza importante;
- atualização dos documentos de estado corrente e planejamento;
- correções técnicas pontuais necessárias à inspeção ou à confiabilidade da entrega, com diff e justificativa.

Ficam para depois da segunda revisão:
- migração ampla de linguagem ou arquitetura;
- substituição generalizada dos pipelines;
- aquisição histórica em grande escala;
- recálculo em massa ou promoção de novos resultados como produtos validados;
- implantação ampla de módulos e painel;
- publicação externa de produtos, merge na main e envio de mensagens a terceiros.

Se uma correção pontual não for necessária para concluir a revisão, registre-a como tarefa pronta para execução. Mantenha separadas recomendações, experimentos e alterações efetivamente realizadas.

Não altere o relatório 2025–2026 nem os documentos originais fornecidos.

## 2. Estado de partida e documentos de referência

Repositório:
https://github.com/paulobmcosta-creator/Observatorio_SUS_ES

Branch conhecida:
feat/ciclo-2026-2027-transicao

Último estado examinado nesta conversa:
937056af0af34b81d27ec38b608f5356488b46a7

Base daquela comparação:
6478f93a50d03270a78959730221f2ea5a643658

Esses commits são referências históricas. Verifique o HEAD atual, a branch efetiva, mudanças não commitadas e instruções aplicáveis antes de trabalhar. Preserve alterações de terceiros e avanços posteriores.

Fontes centrais:
- Relatório encerrado: https://docs.google.com/document/d/1gmVyMUhK3o2CtsTEaeqVgk4lj08es5TlWbklIQGekWQ/edit
- Acervo: https://drive.google.com/drive/folders/1mi6rvQeHxuCfcMJfOJtGmWRKL358WjZD
- Projeto 2026–2027: “Consolidação metodológica do Observatório SUS-ES: validação e atualização de indicadores da atenção especializada no Espírito Santo”, período setembro/2026–agosto/2027. Cópia conhecida em docs/ciclo_2026_2027/referencias/proposta_2026_2027.pdf.
- Dossiê 1 metodológico e técnico institucional, v1.0, 03/10/2026.
- Dossiê 2 metodológico do TCC cardiovascular de Camila, v1.0, 03/10/2026.
- Documentação, matrizes, configurações, código e evidências da branch.
- Parecer externo anterior, se disponível, como conjunto de constatações a conferir.

Identifique cada documento por título, período e conteúdo. O PDF do projeto original 2025–2026, também fornecido na conversa, não substitui o projeto 2026–2027.

Reutilize as leituras integrais e referências já existentes quando forem suficientes e corresponderem à mesma versão. Não recomece investigações concluídas sem mudança ou incerteza relevante.

O projeto define compromissos e cronograma; D1 define regras institucionais; D2 define o módulo cardiovascular; o relatório apresenta resultados, limites e agenda herdada. Uma afirmação documental sobre implementação deve ser conferida com evidência quando for determinante para a decisão.

## 3. Perguntas que a revisão deve responder

Para cada produto ou componente relevante:
- Que pergunta científica ou de gestão ele responde?
- Que objetivo ou entrega do projeto depende dele?
- O que foi efetivamente produzido e qual sua evidência?
- O que está metodologicamente correto e tecnicamente reutilizável?
- Quais limitações afetam o resultado, a interpretação ou a atualização?
- É melhor manter, corrigir, ampliar, substituir ou descontinuar seu uso ativo?
- Quais alternativas foram examinadas e por que a escolhida é preferível?
- Qual o custo de adaptação, reprodução e manutenção?
- Quais resultados e consumidores seriam afetados por uma mudança?
- Qual a próxima ação e qual evidência permitirá considerá-la concluída?

Não recomende conservar uma implementação apenas porque já existe. Não recomende substituí-la apenas por preferência de linguagem, novidade ou aparência de modernização.

Diferencie preservação histórica de adoção como solução vigente. Uma solução superada pode permanecer documentada sem continuar sendo a base da execução.

## 4. Completar a avaliação do acervo

A execução anterior registrou restrição de acesso ao Drive e não reinspecionou vários produtos externos. Verifique o acesso disponível agora. Se persistir uma limitação, registre exatamente o que faltou e quais decisões dependem disso.

Examine, na medida necessária:
- Oncologia: relatório, bases, tabelas, cálculos, denominadores, fontes e gráficos;
- Cardiologia: extrações e produtos anteriores, confrontados com D2;
- RUE: relatório individual, análise municipal de encerramento, script, base e nota metodológica;
- MVP principal: código, conjunto analítico, filtros, cartões, mapas, dependências e atualização;
- variante v2 não homologada: diferenças, benefícios demonstrados e problemas;
- Comunicação: diretrizes, modelo de nota técnica e materiais;
- Força de trabalho e ICSAP: requisitos e preparação efetivamente existentes;
- guias, inventários, catálogos e materiais formativos reutilizáveis.

Preserve a distinção entre produção individual, coletiva, análise de encerramento e proposta ainda não implementada.

Não classifique como inexistente um produto que apenas não está no checkout. Não reconstrua o painel antes de inspecionar o que já existe.

Use os conectores e meios autorizados disponíveis. Se faltar um arquivo essencial, reúna em uma solicitação objetiva os nomes, finalidade e decisões afetadas. Continue a revisão independente desse material. Não repita acessos recusados sem mudança legítima de condição.

## 5. Avaliação científica e metodológica

Avalie a matriz institucional e os produtos herdados pelas dimensões previstas no projeto: relevância sanitária, clareza da definição, disponibilidade, consistência, completude, comparabilidade territorial e temporal, atualização, inteligibilidade e utilidade para a gestão.

Confronte essas dimensões com evidências específicas. Não trate “potencialmente útil” como justificativa suficiente para todos os indicadores. Não invente pontuações, pesos ou limiares como se já fossem decisões aprovadas.

Identifique uma proposta de núcleo inicial e sua sequência de expansão, explicando por que determinadas medidas devem entrar antes de outras. Diferencie:
- controles técnicos;
- indicadores substantivos da matriz institucional;
- medidas complementares;
- indicadores próprios de cada módulo;
- análises exploratórias.

Não confunda as seis medidas técnicas existentes com as seis famílias analíticas futuras. Um conjunto de testes aprovado não equivale à validação documental, analítica ou gerencial.

Examine especialmente:
- adequação das unidades: estabelecimento, habilitação, profissional, vínculo, hora, internação, AIH, procedimento e óbito;
- localização física, município gestor, residência, atendimento e ocorrência;
- necessidade real das chaves em cada relacionamento;
- definições e vigências de habilitações, procedimentos e classificações;
- cobertura dos fluxos interestaduais;
- denominadores, população residente total e estratos;
- estoques mensais e síntese anual com cobertura explícita;
- ausentes, zeros, exclusões e duplicidades;
- comparabilidade entre períodos e mudanças de layout;
- limites de interpretação de cadastro, produção, acesso, suficiência e desfechos.

A orientação institucional de população total não autoriza alterar o relatório encerrado. Proponha versões novas e comparações quando regras herdadas precisarem de revisão.

CO_UNIDADE é necessário onde o relacionamento o exigir. Não o fabrique nem o imponha como requisito universal de análises independentes. Um contrato oficial com CNES público, competência e outras chaves pode atender a outra finalidade, desde que sua semântica e cardinalidade sejam demonstradas.

Preserve decisões consolidadas de D2, como período 2014–2024 e desenho territorial e analítico, em seu escopo temático. Não as transforme em padrão de todo o Observatório. Identifique separadamente escolhas consolidadas, validações operacionais pendentes e decisões metodológicas ainda abertas.

## 6. Avaliação tecnológica e alternativas

Reutilize a avaliação já produzida de PySUS, microdatasus, PyArrow, DuckDB e outros componentes. O DataHub está identificado como:
https://github.com/rafa-trindade/kaggle-datahub
Pin anteriormente examinado:
60aa9cbd82509e0595d5c99ec74794e6be1588bd

Verifique se houve atualização relevante antes de atribuir às versões atuais conclusões obtidas em versões antigas. Não atualize dependências apenas para realizar a revisão.

Compare as opções por função:
- descoberta de arquivos e cobertura;
- aquisição e preservação da fonte;
- conversão e tipos;
- tratamento e integração;
- armazenamento;
- análise;
- visualização;
- atualização e manutenção.

Python/PySUS é a direção preferencial da engenharia quando operacionalmente validado, conforme D1. R deve permanecer onde há implementação adequada e custo de manutenção justificável. Não imponha migração total.

Diferencie cobertura declarada, download demonstrado, integridade da conversão e equivalência metodológica. Dados sintéticos demonstram comportamentos específicos; não validam uma série histórica real.

As limitações identificadas no DataHub exigem decisões por uso. Não conclua que todo o projeto é inutilizável, nem adote integralmente o corpus sem avaliar proveniência, partes, campos e períodos.

Se uma prova adicional for necessária, defina antes:
1. a dúvida;
2. o material mínimo;
3. o resultado esperado;
4. a condição de aceitação ou rejeição;
5. a consequência para a escolha.

Encerre a investigação quando houver evidência suficiente para a decisão. Bloqueio de rede não prova defeito da ferramenta. Prepare a próxima ação reproduzível quando não puder executá-la.

## 7. Cobertura integral dos objetivos e da agenda herdada

Atualize o plano vigente, com correspondência explícita:

objetivo → produto → situação comprovada → lacuna → decisão → tarefa → dependências → critério de conclusão → responsável funcional → período.

O plano deve contemplar:

| Objetivo do ciclo 2026–2027 | Entrega a assegurar |
|---|---|
| O1 — sistematizar produtos anteriores | Inventário crítico completo e decisões de aproveitamento |
| O2 — selecionar e validar indicadores | Matriz mínima e fichas com evidência documental, operacional e analítica |
| O3 — atualizar e padronizar bases | Bases e recortes adequados aos indicadores, com registros de extração e dicionários |
| O4 — aprimorar o fluxo reprodutível | Rotinas, conferências, versionamento, ambiente e manual de atualização |
| O5 — qualificar o painel-piloto | Painel baseado em produtos versionados, coerente e atualizável |
| O6 — disseminar resultados | Nota técnica, resumo científico, comunicação/apresentações e novo relatório final |

Represente os três planos formativos e sua complementaridade. Use responsáveis funcionais quando a designação nominal não estiver comprovada. Não invente execução discente, reuniões, bolsas, horas ou participação de parceiros.

A agenda herdada deve receber encaminhamento explícito:
- CNES: habilitações e serviços, atualização temporal, leitos, equipamentos, profissionais e território;
- Oncologia: continuidade dos resultados e aprofundamento por estabelecimento, habilitação, equipamento e fluxos;
- Cardiovascular: implementação de D2 e integração oferta–utilização–mortalidade;
- RUE: progressão da descrição cadastral para produção e fluxos; avaliar dados necessários para distância/tempo, regulação e funcionamento;
- Força de trabalho: profissional, vínculo e carga horária com unidades e agregações corretas;
- ICSAP: SIH, lista aplicável, residência, população e comparabilidade, explicando sua função na análise da rede;
- Painel: inspeção, decisão sobre aproveitamento, evolução, atualização e usabilidade;
- Comunicação: aproveitamento dos modelos e elaboração de produtos vinculados a perguntas de gestão;
- Artigos e cooperação: encaminhamentos compatíveis com maturidade, distinguindo preparação, revisão, submissão e uso institucional.

Diferencie obrigações do projeto novo, continuidade solicitada do relatório e extensões propostas. A antiga previsão de três notas gerenciais não deve ser atribuída automaticamente ao novo projeto.

Priorizar significa ordenar e justificar. Não omita uma frente porque ela não apareceu no primeiro incremento. Se houver incompatibilidade entre escopo, capacidade e prazo, demonstre-a e apresente opções ao coordenador.

## 8. Rever o encadeamento do trabalho

Avalie se o plano atual se concentra excessivamente no snapshot 202601 e na engenharia. Identifique dependências verdadeiras e possibilidades de avanço independente.

Proponha marcos com produtos verificáveis:
1. avaliação do acervo e decisões de continuidade;
2. referências comuns suficientes para os primeiros indicadores;
3. primeiro percurso completo com dados reais, da fonte à interpretação;
4. demonstração de atualização em outra competência ou período;
5. expansão justificada dos indicadores e módulos;
6. integração e qualificação do painel;
7. manual, produtos científicos, comunicação e consolidação do ciclo.

Escolha e justifique o primeiro percurso analítico que será executado após a segunda revisão. Compare candidatos pelo valor científico, maturidade, disponibilidade e capacidade de desbloquear outras entregas. Verifique se LT/ES/202401 continua sendo o melhor passo; não o mantenha por inércia.

Não espere todos os dados para preparar requisitos do painel, estrutura do manual e critérios de comunicação. Não preencha resultados inexistentes.

Harmonize o planejamento operacional com o cronograma original, explicitando ajustes propostos. Não interprete data passada como prova de conclusão, nem antecipe ficticiamente atividades.

## 9. Verificar achados concretos da revisão anterior

Confirme se persistem no HEAD atual:
- divergência tecnológica entre AGENTS.md, README e D1;
- declaração de pipeline completo no README sem correspondência à maturidade documentada;
- arquivo_origem fixo em tbEstabelecimento202601 numa rotina parametrizada por competência;
- precedência de município gestor onde a finalidade exige localização física;
- ausência de tarefas suficientemente detalhadas para Oncologia, RUE, força de trabalho e ICSAP;
- R10 concentrada na inspeção do painel, sem decomposição da entrega de evolução e manutenção;
- documentos correntes que ainda informam CI remoto não executado;
- inventários históricos apresentados como se descrevessem o estado atual.

Os workflows R e Python foram observados com sucesso em 47bc932fe3955ac3759d4b7bc5094c016db03cd3. Consulte o estado atual; não atribua essa execução a outro commit sem evidência.

A atualização de instruções de governança deve formalizar decisões autorizadas; não serve para contornar controles. Se houver decisão substantiva não resolvida, apresente recomendação concreta.

Não repita o parecer anterior como verdade automática: corrija-o quando os arquivos atuais ou outras evidências mostrarem situação diferente.

## 10. Formato da entrega

Atualize os documentos de planejamento já existentes. Use um parecer de síntese como entrada para a segunda revisão, com links para as evidências, evitando duplicar matrizes e planos.

A entrega deve conter:

### A. Parecer crítico
Conclusões hierarquizadas, fundamentos, alternativas e consequências. Para cada achado, indique se é observado diretamente, reportado em log, inferência ou não verificável.

### B. Decisões por produto/componente
Manter, corrigir, ampliar, substituir, descontinuar uso ativo ou preservar como histórico. Registre evidência, alternativa, justificativa, impacto, dependências e condição de conclusão.

### C. Plano integral revisado
Todos os objetivos e a agenda herdada, com prioridades justificadas, sequência, entregas, dependências específicas e critérios de aceite. Distinga tarefas prontas, tarefas bloqueadas e decisões da coordenação.

### D. Primeiro percurso analítico proposto
Pergunta, indicador, fonte, recorte, implementação aproveitada, controles, produto esperado, dependências e razão da escolha. Prepare a especificação para execução posterior.

### E. Registro do que foi realizado nesta rodada
Arquivos alterados, testes/experimentos executados, resultados, correções pontuais e limites. Não confunda planejamento com implementação concluída.

### F. Passagem para a segunda revisão
Informe:
- branch e SHA exato do commit final, se houver;
- commit-base da comparação;
- arquivos modificados ainda não commitados;
- link de comparação ou PR existente;
- documentos centrais e ordem sugerida de leitura;
- fontes acessadas e materiais faltantes;
- decisões consolidadas e propostas ainda abertas;
- perguntas ao coordenador, somente quando necessárias;
- ponto exato de retomada após a revisão.

Se já houver autorização vigente para commit/push/PR, respeite seu alcance e registre o estado publicado. Este prompt, isoladamente, não autoriza merge ou publicação externa de produtos. Se não puder publicar ou não houver autorização, entregue o patch e os arquivos finais de forma identificável; não deixe a segunda revisão depender apenas de um resumo verbal.

## 11. Critério de encerramento

A rodada estará concluída quando:
- as decisões relevantes estiverem fundamentadas ou precisamente delimitadas como pendentes;
- todos os objetivos e frentes solicitadas tiverem encaminhamento explícito;
- o plano indicar produtos e critérios de conclusão, além de tarefas;
- alternativas tiverem sido examinadas na profundidade necessária;
- houver um primeiro percurso analítico justificadamente escolhido;
- os arquivos e o estado de revisão estiverem identificáveis.

Conclua toda a parte executável desta revisão antes de apresentar pedidos residuais de informação. Não prolongue a etapa com verificações repetidas sem uma dúvida concreta.

Ao atingir esse ponto, encerre a rodada e entregue o material para a segunda revisão. Aguarde a orientação resultante antes da implementação ampla. Não declare o projeto 2026–2027 concluído: esta entrega corresponde à revisão crítica e ao planejamento.

# FIM DO PROMPT EXECUTÁVEL

---

## O que trazer de volta ao ChatGPT

Após a conclusão do Codex, envie:
1. o link da comparação ou do PR, preferencialmente acompanhado do SHA final;
2. a resposta final do Codex;
3. arquivos e alterações que tenham ficado apenas locais, caso não estejam na comparação.

A segunda revisão examinará a fundamentação das decisões, a cobertura integral do projeto, a coerência metodológica, a viabilidade do plano e a suficiência dos critérios de conclusão. Depois disso, serão incorporados os ajustes e definida a continuidade da implementação, preservando os avanços válidos.

