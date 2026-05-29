# Guia de início — Observatório SUS-ES

## 1. O que é o Observatório SUS-ES

O Observatório SUS-ES é um repositório científico e educacional voltado à organização, documentação, análise e validação de dados de saúde pública, com foco no Espírito Santo. Ele reúne documentação metodológica, contratos de dados, metadados, scripts e testes para apoiar análises reprodutíveis.

A prioridade do aluno é compreender a estrutura do projeto e produzir leitura técnica organizada antes de executar ou modificar qualquer componente.

## 2. Qual é o foco atual no CNES

O foco atual é o CNES, o Cadastro Nacional de Estabelecimentos de Saúde. O repositório contém um piloto técnico e metodológico para organizar bases, metadados, indicadores e validações relacionadas à oferta de serviços e características dos estabelecimentos de saúde.

O CNES é tratado como núcleo atual de trabalho, mas as decisões operacionais devem seguir a orientação do pesquisador.

## 3. Por que CNES é importante

O CNES descreve estabelecimentos, serviços, habilitações, vínculos e características estruturais relevantes para a análise da rede de saúde. Ele permite investigar oferta, capacidade instalada, organização territorial e dimensões da atenção especializada.

Por ser uma base complexa, com muitos campos e regras próprias, o CNES exige cuidado com identificadores, chaves, competências, preservação textual e rastreabilidade.

## 4. Papel do R

R permanece como oráculo metodológico do projeto. Isso significa que os scripts R existentes são a referência principal para comportamento esperado, validação, transformação e cálculo no piloto CNES.

O aluno não deve alterar nem substituir scripts R sem autorização. A leitura dos scripts pode ser indicada pelo orientador, mas a execução e modificação dependem de supervisão.

## 5. Papel do Python/PySUS

Python/PySUS foi investigado como alternativa ou apoio para acesso e mapeamento estrutural de dados CNES. A avaliação mostrou viabilidade parcial, com ressalvas importantes.

No estado atual do repositório, Python/PySUS é experimental e prototípico. Ele não deve ser tratado como pipeline produtivo nem usado para gerar bases sem autorização explícita.

## 6. Por que a migração Python está arquivada como histórico

A documentação da migração Python/PySUS contém muitas etapas diagnósticas, hipóteses, testes controlados e registros de instabilidade. Esses documentos foram importantes para decidir os limites da migração, mas podem confundir quem está começando.

Por isso, a documentação longa foi arquivada em `docs/arquivo_historico/migracao_python/`. O aluno deve conhecer a conclusão consolidada, mas não precisa iniciar a formação lendo todos os diagnósticos históricos.

## 7. O que o aluno deve ler primeiro

A sequência inicial recomendada é:

1. `docs/guias_aluno/README.md`
2. `docs/guias_aluno/mapa_repositorio_observatorio_sus.md`
3. `docs/guias_aluno/glossario_minimo_cnes_observatorio.md`
4. `docs/guias_aluno/plano_trabalho_aluno_cnes.md`
5. Documentos CNES indicados pelo orientador, especialmente os textos consolidados em `docs/cnes/`.

## 8. O que o aluno não deve fazer

- Não executar scripts R ou Python sem autorização.
- Não alterar código em `src/`, `scripts/` ou `python/`.
- Não alterar testes.
- Não editar metadados existentes.
- Não escrever em `data_raw/`, `data_interim/` ou `data_processed/`.
- Não gerar bases.
- Não tentar resolver `CO_UNIDADE` sem orientação.
- Não substituir o pipeline R por Python.

## 9. Produto inicial esperado: fichamento técnico

O primeiro produto esperado é um fichamento técnico curto, com linguagem própria do aluno, contendo:

- documentos lidos;
- objetivo de cada documento;
- conceitos novos aprendidos;
- dúvidas metodológicas;
- campos CNES que exigem cuidado;
- riscos de execução indevida;
- síntese de como o aluno entende o papel do CNES no Observatório.

O fichamento deve ser usado para uma conversa inicial com o orientador antes de qualquer etapa prática.

## 10. Conclusão

O aluno deve entrar no projeto pela documentação pedagógica, compreender o núcleo CNES/R, reconhecer que Python/PySUS é experimental e respeitar as áreas restritas. A primeira contribuição esperada não é código, mas leitura, síntese e formulação de dúvidas qualificadas.
