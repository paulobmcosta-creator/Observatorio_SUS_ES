# Análise global do GitHub e do repositório Observatório SUS-ES

**Data da análise:** 2026-05-18  
**Escopo:** repositório público `paulobmcosta-creator/Observatorio_SUS_ES`, com cruzamento entre a árvore pública observada no GitHub e o checkout local disponível no ambiente de trabalho.  
**Natureza:** diagnóstico técnico, metodológico e operacional para apoiar priorização de próximos passos; não altera o escopo científico do projeto.

## 1. Fontes e comandos utilizados

A análise combinou inspeção local do repositório, consulta pública à interface/API do GitHub e leitura dos arquivos versionados relevantes.

Comandos e consultas executados:

```bash
pwd && git status --short && git log --oneline -5 && find .. -name AGENTS.md -print
find . -maxdepth 4 -type f -not -path './.git/*' -print | sort
find . -maxdepth 4 -type d -not -path './.git*' -print | sort
git remote -v
git branch --show-current
python3 /tmp/collect_analysis.py
Rscript tests/test_estrutura_repositorio.R
```

Consultas públicas utilizadas:

- `https://github.com/paulobmcosta-creator/Observatorio_SUS_ES`
- `https://api.github.com/repos/paulobmcosta-creator/Observatorio_SUS_ES`
- `https://api.github.com/repos/paulobmcosta-creator/Observatorio_SUS_ES/git/trees/main?recursive=1`
- `https://api.github.com/repos/paulobmcosta-creator/Observatorio_SUS_ES/actions/workflows`

Limitações importantes:

- O checkout local não possui remoto Git configurado no ambiente (`git remote -v` não retornou origem). Por isso, a comparação com `main` foi feita por API pública, sem `git fetch`.
- Configurações privadas de GitHub, como branch protection, secrets, regras de aprovação obrigatória e permissões internas, não são auditáveis pela API pública sem autenticação administrativa.
- A execução local de testes em R não pôde ser concluída porque `Rscript` não está instalado no ambiente.

## 2. Fotografia pública do GitHub

A API pública do GitHub indicou o seguinte estado do repositório em `main`:

| Dimensão | Observação |
| --- | --- |
| Visibilidade | Público |
| Branch padrão | `main` |
| Criado em | 2026-04-13 |
| Último push observado | 2026-05-18 |
| Estrelas | 1 |
| Forks | 0 |
| Issues abertas | 0 |
| Licença detectada pela API | `null` |
| Descrição do repositório | `null` |
| Workflow Actions público | `validar-pipeline-cnes-r`, ativo |

A árvore pública de `main` contém 30 arquivos e 22 diretórios, com predominância de Markdown e R:

| Tipo | Quantidade observada |
| --- | ---: |
| Arquivos sem extensão, principalmente `.gitkeep` | 12 |
| Markdown (`.md`) | 8 |
| R (`.R`) | 7 |
| CSV (`.csv`) | 2 |
| Workflow YAML (`.yml`) | 1 |

## 3. Diagnóstico executivo

O repositório está em estágio **inicial estruturado com piloto técnico operacional em R**, mas ainda não atingiu maturidade de produto analítico ou plataforma científica consolidada.

Pontos fortes:

1. Há uma estrutura de diretórios coerente para ciência de dados em saúde, com separação entre dados brutos, intermediários, processados, código, testes, metadados, mapas e dashboards.
2. A governança já define papéis relevantes: Pesquisador Principal, Desenvolvedor de Dados, Analista de Visualização, Curador de Metadados, Testador/Integrador e Contribuidores Externos.
3. O repositório declara R como linguagem principal para pipelines reprodutíveis e restringe Python a casos com justificativa técnica explícita.
4. O GitHub público já apresenta um workflow de CI ativo para o pipeline piloto CNES.
5. Existe um primeiro núcleo técnico CNES no `main` público, com extração, transformação, validação, fixture e teste.

Pontos críticos:

1. A licença é citada no README, mas a API pública não detecta licença e a árvore pública observada não inclui arquivo `LICENSE`.
2. O repositório público não possui descrição nem tópicos visíveis, o que reduz descobribilidade e clareza institucional.
3. Há duplicidade entre `fluxo_trabalho.md` na raiz e `docs/fluxo_trabalho.md`, criando risco de divergência documental.
4. A documentação afirma uma visão de pipeline completo, mas a implementação atual ainda é um piloto técnico localizado; a redação deve distinguir visão estratégica de capacidade implementada.
5. O CI público executa o teste do pipeline CNES, mas não executa explicitamente o teste estrutural `tests/test_estrutura_repositorio.R` observado na árvore pública.
6. O diretório público `src/indicators/src/validation/` parece anômalo, pois duplica `src` dentro de `src/indicators` e convive com `src/validation/`.
7. O checkout local usado nesta tarefa está divergente da árvore pública de `main`: localmente faltam `.github/`, `scripts/`, `src/validation/`, `docs/cnes/`, fixtures e scripts CNES observados no GitHub.

## 4. Estrutura e arquitetura do projeto

A arquitetura pretendida é adequada para um observatório de dados em saúde:

- `data_raw/`: entrada bruta preservada;
- `data_interim/`: dados parcialmente tratados;
- `data_processed/`: dados prontos para análise;
- `metadata/`: dicionários, esquemas e descrições;
- `src/extract/`: extração;
- `src/transform/`: transformação;
- `src/indicators/`: indicadores;
- `src/validation/`: validação;
- `tests/`: testes automatizados;
- `docs/`: documentação técnica e metodológica;
- `dashboards/` e `maps/`: produtos de visualização.

Avaliação:

- A separação conceitual está correta.
- A implementação ainda é assimétrica: `src/transform/` e `src/validation/` já têm atividade no `main` público; `src/indicators/`, `dashboards/`, `maps/` e `metadata/` permanecem essencialmente como placeholders.
- A presença de `src/indicators/src/validation/` deve ser tratada como dívida estrutural: provavelmente era intenção criar `src/validation/`, que já existe no `main` público.

Recomendação:

1. Remover ou migrar `src/indicators/src/validation/` após confirmar que não há dependência histórica.
2. Criar contratos mínimos de dados em `metadata/`, antes de ampliar indicadores.
3. Evitar novos módulos temáticos até estabilizar padrões de extração, transformação, validação, teste e documentação no piloto CNES.

## 5. Governança e colaboração

A governança está bem encaminhada. O arquivo `AGENTS.md` descreve responsabilidades por papel, incluindo supervisão metodológica, curadoria de metadados, integração contínua e diretrizes de commit.

Forças:

- Há responsabilidades explícitas para revisão científica, proteção ética e LGPD.
- Há diretrizes de Conventional Commits em português.
- Há separação entre governança, convenções metodológicas e fluxo de trabalho.

Lacunas:

- Não foram observados templates públicos de issue ou pull request.
- Não foi observado `CODEOWNERS`.
- Não foi possível verificar branch protection ou exigência de reviews/checks por limitação de acesso público.
- A ausência de issues abertas pode significar organização externa, mas também pode indicar que o backlog ainda não está rastreável no GitHub.

Recomendação:

1. Adicionar templates mínimos de issue e pull request.
2. Adicionar `CODEOWNERS` quando houver equipe definida.
3. Formalizar no README se o backlog será gerido no GitHub Issues ou em ferramenta externa.
4. Configurar proteção de `main` para exigir PR, CI verde e pelo menos uma revisão, se ainda não estiver configurado.

## 6. Documentação

Documentos observados no `main` público:

- `README.md`;
- `AGENTS.md`;
- `docs/governanca_codigo.md`;
- `docs/convensoes_metodologicas.md`;
- `docs/fluxo_trabalho.md`;
- `docs/cnes/README.md`;
- `docs/cnes/setup_execucao_local_r.md`;
- `fluxo_trabalho.md` na raiz.

Avaliação:

- A documentação cobre identidade do projeto, estrutura, linguagem principal, governança, convenções e fluxo.
- A documentação CNES já descreve entrada, processamento, saída, limitações e validação local.
- O README menciona licença MIT, mas a licença não é detectada pela API pública, o que sugere ausência de `LICENSE` padronizado.
- A duplicidade do fluxo de trabalho deve ser resolvida para que exista uma única fonte de verdade.

Recomendação:

1. Manter `docs/fluxo_trabalho.md` como fonte canônica.
2. Remover, redirecionar ou reduzir `fluxo_trabalho.md` da raiz a uma nota curta apontando para `docs/fluxo_trabalho.md`.
3. Adicionar `LICENSE` MIT, se esse for de fato o licenciamento pretendido.
4. Ajustar a linguagem do README para separar claramente visão do observatório e capacidades já implementadas.

## 7. Código R e pipeline CNES

O `main` público contém um piloto CNES com os seguintes componentes:

- `src/extract/ler_arquivos_cnes.R`;
- `src/transform/padronizar_cnes_interim.R`;
- `src/transform/executar_pipeline_piloto_cnes.R`;
- `src/validation/validar_pipeline_cnes.R`;
- `tests/fixtures/cnes/cnes_piloto_exemplo.csv`;
- `tests/teste_pipeline_piloto_cnes.R`.

Avaliação técnica:

- O pipeline é pequeno, compreensível e usa funções base/built-in de R.
- A orquestração por `source()` é aceitável para piloto, mas tende a fragilizar conforme o projeto crescer.
- A validação cobre existência de entrada, colunas mínimas transformadas e arquivo de saída.
- O teste com fixture é um bom primeiro passo, pois reduz dependência de dados externos.
- Ainda não há camada de schema versionado em `metadata/`, nem validações epidemiológicas ou regras específicas CNES mais robustas.

Riscos técnicos:

1. `source()` com caminhos fixos depende do diretório de execução ser a raiz do repositório.
2. A cobertura de testes é estreita e concentrada no caminho feliz.
3. Não há lint, formatação automática ou análise estática configurada.
4. Não há estratégia formal de versionamento de dados e schemas.

Recomendação:

1. Manter o piloto CNES como referência técnica inicial.
2. Adicionar testes de erro controlado: diretório ausente, arquivo sem coluna `competencia`, arquivo vazio e competência inválida.
3. Criar `metadata/cnes_schema_minimo.csv` ou equivalente antes de ampliar o pipeline.
4. Adiar empacotamento R até haver mais funções estáveis, mas preparar convenções para isso.

## 8. Dependências R

A inspeção dos scripts R públicos indica uso de pacotes built-in, especialmente `base` e `utils`. Não foram observadas dependências externas obrigatórias no piloto CNES público.

A matriz de dependências deve permanecer simples enquanto o pipeline usar apenas pacotes distribuídos com R. O formato recomendado para compatibilidade com o script público `scripts/instalar_dependencias_r.R` é:

```csv
pacote,fonte,obrigatorio,motivo
base,built-in,sim,funcionalidades básicas da linguagem R usadas nos testes e scripts
utils,built-in,sim,leitura e escrita de arquivos CSV no pipeline piloto CNES
methods,built-in,sim,pacote padrão do runtime R carregado na sessão
stats,built-in,sim,pacote padrão do runtime R carregado na sessão
```

Achado relevante desta análise: o checkout local anterior usava um schema alternativo em `config/dependencias_r.csv` (`pacote,tipo,escopo,uso_observado,observacao`), incompatível com o script público de instalação de dependências. Este ajuste foi corrigido nesta intervenção para reduzir risco de conflito com o `main` público.

## 9. Testes e integração contínua

O GitHub público informa um workflow ativo chamado `validar-pipeline-cnes-r`, localizado em `.github/workflows/validar_pipeline_cnes_r.yml`.

O workflow público:

- executa em `push` para `main`, `work` e `feature/**` quando caminhos relevantes mudam;
- executa em `pull_request` quando caminhos relevantes mudam;
- configura R 4.3;
- roda `scripts/instalar_dependencias_r.R`;
- executa `tests/teste_pipeline_piloto_cnes.R`.

Avaliação:

- O CI é apropriado para o estágio atual.
- A execução está focada no piloto CNES, o que é coerente com a maturidade inicial.
- O teste estrutural `tests/test_estrutura_repositorio.R` existe no `main` público, mas não aparece como etapa explícita do workflow observado.
- Não há evidência pública de cobertura, lint, checagem de documentação ou validação de schemas.

Recomendação:

1. Incluir `Rscript tests/test_estrutura_repositorio.R` no workflow.
2. Adicionar uma checagem leve para parsear `config/dependencias_r.csv`.
3. Manter CI pequeno até estabilizar o piloto, evitando matriz complexa prematura.
4. Registrar no PR os comandos executados e limitações de ambiente.

## 10. Dados, metadados e LGPD

O repositório usa `.gitkeep` em diretórios de dados, e `.gitignore` evita versionamento de dados brutos, intermediários e processados, preservando apenas placeholders. Isso é adequado para um projeto de saúde pública com possível sensibilidade de dados.

Forças:

- Dados gerados e brutos são ignorados por padrão.
- A governança menciona anonimização e conformidade com LGPD.
- O piloto usa fixture mínima e sintética, reduzindo risco de exposição de dados sensíveis.

Lacunas:

- `metadata/` ainda não contém dicionários ou schemas reais.
- Não há política específica de classificação de dados, níveis de agregação, retenção ou descarte.
- Não há documentação operacional para revisão de risco antes de publicar dados derivados.

Recomendação:

1. Criar um primeiro dicionário de dados para o fixture e para a saída CNES interim.
2. Definir campos obrigatórios de metadados: origem, data de coleta, unidade geográfica, granularidade temporal, nível de agregação, responsável, licença/fonte e restrições de uso.
3. Criar checklist LGPD antes de aceitar dados reais no repositório ou nos produtos derivados.

## 11. Segurança e qualidade no GitHub

Achados públicos:

- Repositório público.
- API pública informa licença `null`.
- Página pública informa ausência de descrição e tópicos.
- Não foram observados releases publicados.
- Não há fork público e há uma estrela observada.
- A aba de Security/quality existe, mas detalhes avançados não são auditáveis sem acesso autenticado.

Riscos:

1. Ausência de `LICENSE` detectável reduz clareza jurídica de reutilização.
2. Ausência de descrição/tópicos prejudica comunicação institucional.
3. Sem branch protection verificada, há risco de merge sem CI ou revisão, se ainda não configurada.
4. Sem templates de PR/issue, a qualidade das contribuições depende de memória institucional.

Recomendação:

1. Adicionar `LICENSE` se a licença MIT for confirmada.
2. Preencher descrição e tópicos no GitHub: `sus`, `espirito-santo`, `saude-publica`, `r`, `epidemiologia`, `ciencia-de-dados`.
3. Adicionar `SECURITY.md` simples para reporte de problemas, especialmente se houver dados sensíveis.
4. Configurar Dependabot apenas quando houver manifestos de dependência externos relevantes.

## 12. Divergência entre checkout local e GitHub público

O ambiente local desta tarefa contém a branch `work`, sem remoto configurado. A árvore local observada é menor que a árvore pública de `main`.

Arquivos/diretórios observados no GitHub público, mas ausentes no checkout local desta tarefa antes desta análise:

- `.github/workflows/validar_pipeline_cnes_r.yml`;
- `docs/cnes/README.md`;
- `docs/cnes/setup_execucao_local_r.md`;
- `scripts/instalar_dependencias_r.R`;
- `src/extract/ler_arquivos_cnes.R`;
- `src/transform/executar_pipeline_piloto_cnes.R`;
- `src/transform/padronizar_cnes_interim.R`;
- `src/validation/validar_pipeline_cnes.R`;
- `tests/fixtures/cnes/cnes_piloto_exemplo.csv`;
- `tests/teste_pipeline_piloto_cnes.R`.

Impacto:

- Uma PR criada a partir deste checkout precisa ser rebased/sincronizada com `main` antes de merge, ou poderá sobrescrever/colidir com arquivos mais recentes.
- A análise local isolada não é suficiente para afirmar maturidade do GitHub atual; é necessário considerar o `main` público.

Recomendação:

1. Sincronizar a branch de trabalho com `main` antes de novas mudanças funcionais.
2. Evitar alterar arquivos que já evoluíram no GitHub público sem rebase.
3. Tratar esta análise como documentação diagnóstica, não como substituto de atualização completa da branch local.

## 13. Priorização recomendada

### Prioridade alta

1. Adicionar `LICENSE` MIT ou ajustar README caso a licença não seja MIT.
2. Resolver duplicidade entre `fluxo_trabalho.md` raiz e `docs/fluxo_trabalho.md`.
3. Sincronizar branches de trabalho com `main` público antes de novos PRs.
4. Incluir o teste estrutural no CI.
5. Corrigir a anomalia `src/indicators/src/validation/`.

### Prioridade média

1. Criar templates de issue e pull request.
2. Criar primeiro schema/dicionário em `metadata/` para o pipeline CNES.
3. Ampliar testes do CNES para cenários de erro e dados malformados.
4. Ajustar README para diferenciar visão estratégica e implementação atual.
5. Preencher descrição e tópicos no GitHub.

### Prioridade baixa, mas desejável

1. Adicionar `SECURITY.md`.
2. Criar changelog simples quando houver releases.
3. Planejar lint/formatação R após estabilizar convenções de código.
4. Avaliar empacotamento R no futuro, se o número de funções crescer.

## 14. Conclusão

O Observatório SUS-ES tem uma base institucional e técnica promissora: a governança está acima da média para um repositório inicial, R foi definido como linguagem principal, e o `main` público já contém um piloto CNES com CI. O maior risco não é ausência de direção, mas sim desalinhamento entre documentação, árvore local, árvore pública e automação.

A recomendação central é consolidar antes de expandir: resolver licença, duplicidade documental, sincronização de branches, teste estrutural no CI, schema de metadados e pequenos casos de teste adicionais do CNES. Só depois disso faz sentido iniciar novos módulos temáticos, dashboards ou indicadores mais complexos.
