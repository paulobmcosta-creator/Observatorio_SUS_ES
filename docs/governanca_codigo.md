# Governança de Código

A governança de código deste repositório visa garantir que o processo de desenvolvimento seja transparente, reprodutível e alinhado às melhores práticas da ciência aberta. Este documento estabelece regras para controle de versões, branchs, revisões e gestão de issues.

## Estrutura de Branches

1. **`main`**: contém o código estável e pronto para produção ou divulgação. Cada commit em `main` deve corresponder a uma versão coerente e funcional do projeto.
2. **Branches de Funcionalidade (`feature/nome-funcao`)**: usadas para desenvolver novas funcionalidades ou indicadores específicos. Devem derivar de `main` ou de um branch de desenvolvimento.
3. **Branches de Correção (`fix/nome-correção`)**: destinam-se à resolução de bugs de alta prioridade.
4. **Branches de Manutenção (`chore/nome-tarefa`)**: para tarefas menores de manutenção (atualização de dependências, limpeza de código).
5. **Branches de Documentação (`docs/tema`)**: dedicados a alterações na documentação.

Evite trabalhar diretamente na `main`. Ao iniciar uma nova tarefa, crie um branch com nome descritivo e curto.

## Pull Requests (PRs)

* **Objetivo**: todo branch deve ser integrado via pull request. Pull requests facilitam revisão colegiada, discussão e registro permanente das motivações das mudanças.
* **Descrição**: a mensagem do PR deve incluir um resumo do problema, a abordagem adotada e referências a issues associadas.
* **Revisores**: pelo menos um membro do time deve revisar o PR. Para mudanças substanciais (modelos estatísticos, novos indicadores), recomenda-se a revisão por dois especialistas.
* **Checklist para Aprovação**:
  1. Código executa sem erros? Inclua logs ou testes.
  2. A documentação foi atualizada conforme necessário?
  3. As mensagens de commit seguem o padrão estabelecido?
  4. Há novos testes cobrindo as alterações?

Após aprovação, o autor é responsável por realizar o merge. Prefira merges *squash* para manter o histórico limpo.

## Gestão de Issues

* **Tipos de Issues**:
  * **Bug**: comportamento inesperado ou erro.
  * **Feature**: sugestão de nova funcionalidade.
  * **Task**: atividade de manutenção ou documentação.
  * **Question**: dúvidas gerais.

* **Abertura de Issue**: descreva claramente o problema ou proposta. Inclua passos para reproduzir bugs, contexto relevante e possíveis soluções.
* **Triagem**: o Pesquisador Principal e o Curador de Metadados triagem semanalmente as issues, definindo prioridade e designando responsáveis.
* **Fechamento**: uma issue somente é fechada quando o PR associado é aceito e mergeado ou quando a discussão determina que não há ação necessária.

## Revisão de Código

Revisões devem focar em:

* **Legibilidade**: nomes de variáveis, funções e arquivos devem ser descritivos. Evite abreviações obscuras.
* **Documentação**: cada função deve possuir docstrings que expliquem parâmetros, retornos e referências metodológicas.
* **Conformidade Metodológica**: verifique se os cálculos estatísticos seguem critérios epidemiológicos reconhecidos.
* **Eficiência e Estilo**: avalie a eficiência dos algoritmos e aderência ao estilo (PEP 8 para Python; tidyverse para R).

## Licenciamento e Citação

Todo código deste repositório é disponibilizado sob licença MIT, salvo indicação em contrário. Ao reutilizar ou adaptar trechos deste trabalho, cite o repositório e os autores como forma de reconhecimento ao esforço coletivo.
