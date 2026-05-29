# Roteiro de revisão humana assistida — CNES / Observatório SUS-ES

## 1. Finalidade do roteiro

Este documento orienta a entrada do aluno no projeto como revisor humano assistido, não como executor autônomo. A finalidade é apoiar uma leitura cuidadosa do repositório, ajudando o aluno a compreender o Observatório SUS-ES, reconhecer os limites técnicos atuais e registrar dúvidas que possam orientar conversas com o pesquisador/orientador.

Nesta fase:

- não há prazo rígido;
- o roteiro não é cronograma obrigatório;
- as etapas são progressivas e dependem de orientação;
- o objetivo é compreender, revisar e levantar dúvidas;
- o aluno não deve executar scripts nem gerar dados.

O roteiro deve ser entendido como apoio à compreensão e à revisão documental, não como lista de tarefas técnicas a serem cumpridas de forma independente.

## 2. Papel do aluno nesta fase

O papel do aluno é:

- ler documentos orientados;
- compreender o objetivo do Observatório SUS-ES;
- identificar conceitos fundamentais do CNES;
- revisar clareza documental;
- apontar ambiguidades;
- listar dúvidas metodológicas;
- verificar se os guias são compreensíveis;
- apoiar a organização conceitual do repositório;
- produzir fichamentos e sínteses;
- discutir achados com o orientador.

O aluno não será responsável, nesta fase, por:

- programar pipelines;
- executar extrações;
- validar scripts;
- alterar metadados;
- gerar base;
- tomar decisões sobre R ou Python;
- resolver `CO_UNIDADE`.

## 3. Princípios da revisão humana assistida

1. Ler antes de executar.
2. Perguntar antes de alterar.
3. Registrar dúvidas em vez de corrigir diretamente arquivos técnicos.
4. Diferenciar documentação consolidada de documentação histórica.
5. Não tratar scripts experimentais como instrução operacional.
6. Não interpretar CNES como `CO_UNIDADE`.
7. Não modificar metadados.
8. Não gerar dados.
9. Não substituir decisões metodológicas do orientador.
10. Priorizar clareza, rastreabilidade e compreensão.

## 4. O que o aluno deve compreender

### 4.1 O projeto Observatório SUS-ES

O aluno deve compreender a finalidade geral do Observatório SUS-ES, com foco em monitoramento, análise da atenção especializada e organização de dados secundários do SUS. A entrada no projeto deve privilegiar leitura, contextualização e entendimento das regras de governança.

### 4.2 O papel do CNES

O CNES é um eixo inicial importante para compreender estabelecimentos, leitos, serviços e profissionais. Ele ajuda a organizar a leitura da oferta de saúde, mas exige cuidado com campos, códigos, identificadores e competências temporais.

### 4.3 O papel do R

R permanece oráculo metodológico do projeto. Isso significa que os scripts R existentes são referência para comportamento esperado, validação e paridade metodológica. O aluno não deve propor substituição do R nem modificar scripts sem autorização expressa.

### 4.4 O papel do Python/PySUS

Python/PySUS é uma trilha experimental/prototípica, encerrada com ressalvas na Etapa 5N. Essa trilha demonstrou viabilidade parcial para acesso e mapeamento estrutural, mas não autoriza pipeline produtivo, geração de bases ou substituição do fluxo em R.

### 4.5 A pendência `CO_UNIDADE`

`CO_UNIDADE` é uma pendência crítica. O aluno deve entender que CNES não deve ser tratado automaticamente como `CO_UNIDADE`, e que qualquer interpretação, correção ou tentativa de resolução desse ponto depende de decisão metodológica do orientador.

## 5. Roteiro progressivo de revisão

Os blocos abaixo não têm prazo rígido. Eles são momentos de revisão que podem ser retomados, reorganizados ou aprofundados conforme orientação do pesquisador/orientador.

### Bloco 1 — Ambientação

Objetivo:
Entender o que é o projeto e como o repositório está organizado.

Leituras:

- `docs/guias_aluno/README.md`
- `docs/guias_aluno/guia_inicio_observatorio_sus.md`
- `docs/guias_aluno/mapa_repositorio_observatorio_sus.md`
- `docs/indice_repositorio.md`
- `README.md`

Produto esperado:

- síntese inicial do que o aluno entendeu;
- lista de dúvidas gerais;
- identificação de termos desconhecidos.

### Bloco 2 — Compreensão do CNES

Objetivo:
Entender por que o CNES é central no projeto.

Leituras:

- `docs/guias_aluno/glossario_minimo_cnes_observatorio.md`
- documentos CNES indicados pelo orientador em `docs/cnes/`
- `metadata/cnes/` apenas como consulta, sem edição.

Produto esperado:

- fichamento técnico sobre CNES;
- quadro com termos-chave;
- dúvidas sobre campos, códigos e identificadores.

### Bloco 3 — Revisão da governança e das regras de segurança

Objetivo:
Entender o que pode e não pode ser alterado.

Leituras:

- `docs/governanca_codigo.md`
- `docs/convensoes_metodologicas.md`
- `docs/revisao_geral_entrega_aluno.md`
- `docs/migracao_python/README.md`

Produto esperado:

- lista de regras que o aluno compreendeu;
- lista de pontos que ainda parecem ambíguos;
- indicação de documentos que precisam de linguagem mais clara.

### Bloco 4 — Revisão humana dos guias

Objetivo:
Avaliar se os guias criados são compreensíveis para um aluno.

Leituras:

- todos os arquivos em `docs/guias_aluno/`.

Produto esperado:

- apontamentos sobre trechos confusos;
- sugestões de melhoria de linguagem;
- termos que precisam entrar no glossário;
- dúvidas sobre ordem de leitura.

### Bloco 5 — Síntese para reunião com orientador

Objetivo:
Preparar uma conversa qualificada com o orientador.

Produto esperado:

- síntese do que entendeu;
- lista de dúvidas priorizadas;
- lista de riscos percebidos;
- sugestões de melhorias documentais;
- indicação do que o aluno acredita que ainda não deve executar.

## 6. Modelo de fichamento técnico

| Campo                                        | Preenchimento                                     |
| -------------------------------------------- | ------------------------------------------------- |
| Documento lido                               |                                                   |
| Tipo de documento                            | guia / metodologia / histórico / metadado / outro |
| Objetivo do documento                        |                                                   |
| Conceitos principais                         |                                                   |
| Campos ou bases citadas                      |                                                   |
| Relação com CNES                             |                                                   |
| Relação com atenção especializada            |                                                   |
| O que entendi                                |                                                   |
| O que não entendi                            |                                                   |
| Dúvidas para o orientador                    |                                                   |
| Pontos de possível confusão para outro aluno |                                                   |
| Sugestões de melhoria documental             |                                                   |

## 7. Quadro de revisão humana

| Item revisado | Tipo de problema | Descrição | Gravidade | Sugestão |
| ------------- | ---------------- | --------- | --------- | -------- |
|               |                  |           |           |          |

Tipos de problema:

- termo confuso;
- orientação ambígua;
- risco de execução indevida;
- documento difícil de localizar;
- contradição aparente;
- necessidade de exemplo;
- dúvida metodológica;
- outro.

Gravidade:

- baixa;
- média;
- alta.

## 8. O que o aluno não deve fazer

- Não executar scripts.
- Não editar scripts.
- Não editar `metadata/cnes`.
- Não alterar `docs/cnes` sem autorização.
- Não mover documentos.
- Não apagar arquivos.
- Não criar bases.
- Não escrever em `data_raw`, `data_interim` ou `data_processed`.
- Não alterar workflows.
- Não tratar Python/PySUS como pipeline produtivo.
- Não tratar CNES como `CO_UNIDADE`.
- Não decidir substituição do R.

## 9. Como o aluno deve registrar dúvidas

As dúvidas devem ser registradas em documento próprio, ou em quadro separado a ser criado posteriormente pelo orientador, sem alterar arquivos técnicos. O registro deve separar dúvida, contexto, documento de origem e possível risco de interpretação.

Categorias sugeridas:

- dúvidas conceituais;
- dúvidas sobre CNES;
- dúvidas sobre repositório;
- dúvidas sobre R/Python;
- dúvidas sobre metadados;
- dúvidas sobre próximos passos;
- dúvidas sobre o que não pode ser feito.

## 10. Critérios de boa revisão humana

- Clareza na leitura.
- Capacidade de diferenciar documento pedagógico e histórico.
- Cuidado com termos técnicos.
- Identificação de ambiguidades.
- Respeito às regras de segurança.
- Organização das dúvidas.
- Prudência antes de sugerir execução.
- Atenção à rastreabilidade.

## 11. Produtos esperados da revisão

| Produto | Finalidade | Observação |
| ------- | ---------- | ---------- |
| Fichamento técnico | Registrar leitura, compreensão e dúvidas sobre documentos orientados. | Não substitui reunião com orientador. |
| Lista de dúvidas | Organizar perguntas conceituais, metodológicas e operacionais. | Deve priorizar pontos que bloqueiam entendimento. |
| Quadro de termos confusos | Identificar palavras, siglas ou campos que dificultam a leitura. | Pode alimentar melhoria futura do glossário. |
| Sugestões de melhoria documental | Apontar trechos que precisam de linguagem mais clara. | Não implica editar arquivos técnicos diretamente. |
| Síntese para reunião | Preparar conversa qualificada com o orientador. | Deve incluir limites do que o aluno não deve executar. |
| Glossário complementar, se autorizado | Registrar novos termos identificados durante a revisão. | Só deve ser criado ou incorporado com autorização. |

## 12. Conclusão

A função do aluno, nesta fase, é ajudar a qualificar a documentação e compreender os próximos passos do projeto, não executar sozinho. A revisão humana assistida deve produzir leitura crítica, dúvidas organizadas, identificação de ambiguidades e sugestões de melhoria documental para discussão com o orientador.

Nesta fase, o aluno atua como revisor humano assistido do repositório. Sua contribuição principal é ler, compreender, fichar, apontar dúvidas e identificar riscos de interpretação. Nenhuma execução técnica, alteração de código, modificação de metadados ou geração de base deve ser feita sem autorização expressa do orientador.
