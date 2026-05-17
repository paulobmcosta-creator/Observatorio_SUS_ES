# Fluxo de Trabalho

Este documento descreve o fluxo mínimo recomendado para mudanças no Observatório SUS-ES. Ele complementa a governança de código e as convenções metodológicas já documentadas, sem substituir a revisão científica ou metodológica definida em `AGENTS.md`.

## 1. Definir a tarefa ou abrir issue

1. Registre a necessidade em uma issue, discussão ou tarefa interna antes de alterar o repositório.
2. Descreva o problema, a motivação, o escopo proposto, os arquivos ou módulos afetados e os critérios de aceite.
3. Para mudanças científicas, metodológicas ou de dados sensíveis, solicite validação prévia do Pesquisador Principal ou responsável designado.

## 2. Criar branch de trabalho

1. Crie uma branch a partir de `main`, evitando trabalhar diretamente na branch principal.
2. Use nomes curtos e descritivos, alinhados ao tipo de mudança:
   - `docs/tema` para documentação;
   - `feat/tema` para novas funcionalidades;
   - `fix/tema` para correções;
   - `test/tema` para testes;
   - `chore/tema` para manutenção.

## 3. Desenvolver a mudança

1. Mantenha a alteração pequena, rastreável e coerente com a issue ou tarefa definida.
2. Priorize R para scripts reprodutíveis; use Python apenas quando houver justificativa técnica explícita.
3. Use caminhos relativos e preserve a organização do repositório:
   - `src/extract/` para extração;
   - `src/transform/` para limpeza e integração;
   - `src/indicators/` para indicadores;
   - `src/validation/` ou `tests/` para validação e testes;
   - `metadata/` para dicionários, esquemas e descrições de dados;
   - `docs/` para documentação técnica e metodológica.
4. Atualize documentação, metadados ou lista de dependências somente quando a mudança exigir.

## 4. Validar localmente

1. Verifique se os arquivos esperados existem e se os caminhos documentados continuam válidos.
2. Confirme que novas dependências externas em R foram registradas em `config/dependencias_r.csv`.
3. Quando houver dados, valide consistência, completude, plausibilidade e anonimização conforme a LGPD.
4. Evite incluir dados sensíveis, arquivos temporários ou resultados grandes sem justificativa e revisão.

## 5. Executar testes e checks

1. Rode os testes automatizados afetados pela mudança antes de abrir o pull request.
2. Para scripts em R, prefira checks executáveis via `Rscript` ou ferramentas equivalentes disponíveis no ambiente.
3. Registre no pull request os comandos executados, indicando sucesso, falha ou limitação de ambiente.
4. Se um teste não puder ser executado localmente, explique a limitação de forma objetiva.

## 6. Abrir pull request

1. Abra um pull request contra `main` após organizar o diff.
2. No texto do pull request, inclua:
   - resumo do problema;
   - solução implementada;
   - arquivos principais alterados;
   - comandos de validação executados;
   - limitações conhecidas;
   - referência à issue ou tarefa, quando aplicável.
3. Use mensagens de commit no padrão Conventional Commits em português, conforme `AGENTS.md`.

## 7. Revisar

1. Solicite revisão de pelo menos uma pessoa responsável pelo escopo afetado.
2. Mudanças metodológicas, indicadores, pipelines de dados ou tratamento de dados sensíveis devem receber revisão técnica e científica compatível com o risco.
3. Responda aos comentários de revisão com ajustes pequenos e rastreáveis.
4. Reexecute os testes relevantes após alterações solicitadas na revisão.

## 8. Fazer merge

1. Faça o merge somente após aprovação e checks satisfatórios.
2. Prefira squash merge quando adequado para manter o histórico limpo.
3. Feche ou atualize a issue relacionada após o merge.
4. Quando a mudança afetar uso, metodologia, dependências ou dados publicados, atualize a documentação correspondente.
