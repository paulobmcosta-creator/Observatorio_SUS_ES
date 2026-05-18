# Fontes Normativas para Classificação de Habilitações e Referências CNES

## 1. Finalidade

Este documento registra fontes que deverão ser usadas para validar códigos, descrições e tipos de referência da classificação temática de habilitações e referências CNES. Ele apoia a revisão da tabela `metadata/cnes/classificacao_habilitacoes_cnes.csv` antes da aplicação automática da classificação em código R.

## 2. Situação atual

A tabela de classificação ainda contém códigos a confirmar e itens conceituais. Essa escolha é deliberada: códigos oficiais não devem ser inventados nem inferidos sem fonte normativa ou técnica confiável. Além disso, parte das referências pode corresponder a serviços especializados, equipamentos, leitos, tipos de estabelecimento ou componentes de rede, e não a habilitações CNES estritas.

## 3. Fontes a consultar

As fontes a consultar em ciclos futuros incluem:

- documentação oficial do CNES/DATASUS;
- manuais técnicos do SCNES;
- SIGTAP;
- portarias ministeriais de habilitação;
- portarias específicas de oncologia;
- normativas da atenção cardiovascular;
- normativas da Rede de Urgência e Emergência;
- normativas de UTI e cuidado crítico;
- normativas da Rede de Cuidados à Pessoa com Deficiência;
- documentos técnicos do Ministério da Saúde;
- bases auxiliares oficiais, quando disponíveis.

## 4. Critérios para confirmação de códigos

Um código só deve ser marcado como confirmado quando houver fonte oficial ou técnica confiável que permita rastrear o código, a descrição, a vigência e a natureza da referência. A confirmação deve registrar a fonte utilizada e, quando possível, a versão ou data de consulta da tabela normativa.

## 5. Critérios para manter `codigo_a_confirmar`

O valor `codigo_a_confirmar` deve ser mantido quando:

- não houver fonte segura;
- o item não for claramente uma habilitação;
- houver dúvida entre serviço, equipamento, leito, estabelecimento ou componente de rede;
- a classificação for apenas conceitual.

Manter `codigo_a_confirmar` é preferível a registrar código incorreto. A prioridade metodológica é preservar rastreabilidade e evitar falsa precisão.

## 6. Próximos passos

A validação normativa é pré-requisito desejável antes da aplicação automática da classificação. Os próximos ciclos devem revisar códigos, separar regras por tipo de referência CNES, atualizar a documentação metodológica e criar testes que garantam consistência entre tabela de referência, função R futura e produtos tabulares derivados.
