# Plano de trabalho inicial do aluno — CNES

Este plano organiza as quatro primeiras semanas de entrada do aluno no Observatório SUS-ES. O objetivo é formar compreensão metodológica antes de qualquer execução de script, alteração de código ou geração de base.

## Semana 1 — Ambientação e leitura

### Tarefas

- Ler `README.md`.
- Ler `docs/indice_repositorio.md`.
- Ler todos os documentos em `docs/guias_aluno/`.
- Identificar as áreas que o aluno não deve alterar.
- Registrar dúvidas iniciais sobre CNES, R, Python/PySUS e dados.

### Entregáveis

- Lista dos documentos lidos.
- Fichamento técnico inicial de uma página.
- Lista de dúvidas para reunião com o orientador.

### O que não fazer

- Não executar scripts.
- Não alterar arquivos.
- Não acessar dados como área de trabalho.
- Não propor substituição de R por Python.

### Critérios de avaliação

- Clareza na distinção entre entrada pedagógica, núcleo CNES e arquivo histórico.
- Capacidade de explicar por que Python/PySUS está classificado como experimental.
- Identificação correta das áreas restritas.

## Semana 2 — CNES e documentação metodológica

### Tarefas

- Ler os documentos CNES indicados pelo orientador em `docs/cnes/`.
- Identificar objetivo, escopo e limites do piloto CNES.
- Mapear os principais campos CNES citados no glossário.
- Relacionar os documentos CNES aos metadados existentes.

### Entregáveis

- Fichamento técnico dos documentos CNES lidos.
- Tabela simples com campos CNES importantes e cuidados associados.
- Lista de pontos que precisam de explicação do orientador.

### O que não fazer

- Não editar `docs/cnes/`.
- Não editar `metadata/cnes/`.
- Não executar pipeline R.
- Não baixar dados CNES.

### Critérios de avaliação

- Compreensão do papel do CNES no Observatório.
- Reconhecimento dos limites de campos sensíveis como `CO_UNIDADE`.
- Uso correto de termos como contrato, metadado, chave e rastreabilidade.

## Semana 3 — Metadados, contratos e rastreabilidade

### Tarefas

- Ler os dicionários, schemas e contratos indicados pelo orientador.
- Comparar a documentação CNES com os metadados correspondentes.
- Identificar quais arquivos funcionam como contrato de dados.
- Descrever como a rastreabilidade é preservada no repositório.

### Entregáveis

- Fichamento técnico sobre metadados e contratos.
- Mapa conceitual simples conectando documentação, metadados, scripts e testes.
- Lista de inconsistências percebidas, se houver, sem editar arquivos.

### O que não fazer

- Não corrigir metadados diretamente.
- Não alterar schemas.
- Não modificar testes.
- Não gerar base intermediária ou final.

### Critérios de avaliação

- Capacidade de explicar a função de metadados e dicionários.
- Atenção a preservação textual e coerção de tipo.
- Separação entre observação de problema e alteração técnica.

## Semana 4 — Síntese, dúvidas e apresentação curta

### Tarefas

- Consolidar os fichamentos das semanas anteriores.
- Preparar apresentação curta para o orientador.
- Indicar dúvidas que bloqueiam avanço técnico.
- Sugerir uma possível tarefa futura de baixo risco, sem executá-la.

### Entregáveis

- Documento final de síntese com 3 a 5 páginas.
- Apresentação curta de 5 a 7 minutos.
- Lista priorizada de dúvidas.
- Proposta de próxima tarefa supervisionada.

### O que não fazer

- Não transformar a síntese em alteração de código.
- Não abrir PR técnico sem orientação.
- Não mover arquivos.
- Não mexer em dados.

### Critérios de avaliação

- Síntese fiel ao estado atual do repositório.
- Reconhecimento explícito de que R permanece oráculo metodológico.
- Compreensão de que Python/PySUS permanece experimental.
- Clareza sobre riscos de execução indevida.

## Modelo de fichamento técnico

Use o modelo abaixo para cada documento ou conjunto de documentos lidos.

```text
Título do documento:
Caminho no repositório:
Data da leitura:

1. Objetivo do documento

2. Principais conceitos ou campos citados

3. Decisões metodológicas registradas

4. Relação com CNES

5. Relação com R, Python/PySUS, metadados ou testes

6. Dúvidas do aluno

7. Cuidados operacionais identificados

8. Síntese em até cinco linhas
```
