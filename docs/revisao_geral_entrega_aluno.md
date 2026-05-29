# Revisão geral do repositório para entrega orientada a aluno

## 1. Objetivo da revisão

Esta revisão tem finalidade de curadoria, limpeza conceitual e preparação pedagógica do repositório **Observatorio_SUS_ES** para entrega orientada a um aluno. O foco não é ampliar a implementação técnica, mas tornar explícito o que já existe, distinguir núcleo atual, legado metodológico, experimentos e documentação histórica, e reduzir o risco de interpretação equivocada por quem inicia no projeto.

Esta etapa:

- não executa pipelines;
- não altera código;
- não gera bases;
- não substitui R;
- não continua a depuração PySUS;
- apenas organiza o que existe por meio de inventário, classificação e recomendações.

Nenhum arquivo existente foi excluído, nenhum script R ou Python foi modificado, nenhum teste foi alterado, nenhum dado foi gerado e nenhuma pasta de dados foi escrita. O produto desta rodada é exclusivamente documental.

## 2. Estado geral do repositório

O Observatório SUS-ES é um repositório científico e educacional voltado ao monitoramento, análise e documentação de informações de saúde pública, com ênfase atual no piloto CNES. A proposta geral inclui pipelines reprodutíveis, indicadores, metadados, documentação metodológica, testes automatizados e produtos futuros de visualização.

O **CNES** ocupa hoje o papel mais consolidado do repositório: há documentação metodológica específica, contratos, dicionários, classificações, scripts R de extração/transformação/indicadores/validação, testes automatizados e uma trilha de investigação Python/PySUS ainda não produtiva.

O **R** permanece como linguagem principal do pipeline consolidado e como **oráculo metodológico**. Os scripts R existentes representam a referência operacional para o piloto CNES e não devem ser removidos, substituídos ou depreciados sem paridade documentada e validação humana.

O **Python/PySUS** aparece como trilha de migração controlada e prova de viabilidade. A investigação avançou em reconhecimento de API, mapeamentos estruturais, contratos intermediários e transformação em memória, mas foi encerrada na Etapa 5N com ressalvas. Essa trilha deve ser apresentada ao aluno como experimento documentado e não como pipeline produtivo.

O estágio atual da migração é: **viabilidade parcial demonstrada, mas sem autorização para geração de base, sem substituição do R e com bloqueios metodológicos relevantes**. As limitações atuais incluem ausência de resolução para `CO_UNIDADE`, falta de paridade com o R/oráculo, instabilidade/intermitência do grupo ST, impossibilidade de tratar CNES como substituto de `CO_UNIDADE` e proibição de materializar bases finais enquanto os bloqueios não forem resolvidos.

## 3. Inventário por diretório

| Diretório | Conteúdo principal | Função atual | Situação | Observação |
|---|---|---|---|---|
| `README.md` | Visão geral, estrutura do projeto, status CNES e arquitetura híbrida R-Python | Porta de entrada do repositório | NUCLEO_ATUAL | Deve ser mantido, mas pode precisar de nota pedagógica mais explícita sobre o que o aluno deve ou não executar. |
| `AGENTS.md` | Papéis, responsabilidades, linguagem principal e convenções de commit | Governança humana e automatizada | NUCLEO_ATUAL | Documento essencial para orientar responsabilidades e limites. |
| `src/` | Scripts R de extração, transformação, indicadores e validação | Pipeline CNES consolidado em R | LEGADO_ORACULO | Núcleo técnico atual e oráculo metodológico. Não alterar nesta rodada. |
| `scripts/` | Script de instalação de dependências R | Apoio operacional para ambiente R | NUCLEO_ATUAL | Útil para execução supervisionada futura; não entregar como primeira ação autônoma ao aluno. |
| `python/` | Pacote Python mínimo, módulos CNES/PySUS, extração, transformação em memória, utilitários | Trilha experimental de migração PySUS | EXPERIMENTAL | Deve ser preservado, mas não apresentado como pipeline produtivo. |
| `tests/` | Testes R, testes Python e fixtures CNES | Validação de contratos, scripts e estrutura | NUCLEO_ATUAL | Núcleo de reprodutibilidade. Não executar nesta rodada; leitura orientada pode ser útil. |
| `docs/` | Governança, convenções, fluxo, manutenção, CNES e migração Python | Documentação geral e histórica | DOCUMENTACAO_METODOLOGICA | Precisa de curadoria para entrada pedagógica, pois contém muitos documentos técnicos e históricos. |
| `docs/cnes/` | Guia CNES, bases, indicadores, contratos, decisões, metadados, roadmap | Documentação metodológica consolidada CNES | DOCUMENTACAO_METODOLOGICA | Deve compor a base de leitura do aluno, com roteiro de priorização. Não alterar nesta rodada. |
| `docs/migracao_python/` | Baseline R, governança híbrida, POC PySUS, Etapas 5N e encerramento | Histórico e diagnóstico da migração R-Python/PySUS | DOCUMENTACAO_HISTORICA | Grande volume de documentos; pode confundir se entregue sem resumo. |
| `metadata/` | Dicionários, schemas, classificações e contratos CNES | Contratos de dados e metadados | DOCUMENTACAO_METODOLOGICA | Deve ser protegido contra edição não supervisionada. |
| `config/` | Dependências R declaradas | Apoio à reprodutibilidade do ambiente R | NUCLEO_ATUAL | Útil para execução local supervisionada. |
| `.github/workflows/` | Workflow de validação do pipeline CNES em R | Integração contínua | NUCLEO_ATUAL | Não alterar; evidencia rotina de validação. |
| `data_raw/` | Pasta versionada por `.gitkeep` para dados brutos | Local reservado para dados brutos | NECESSITA_REVISAO | Não escrever nem entregar como local de uso livre ao aluno sem regras claras. |
| `data_interim/` | Pasta versionada por `.gitkeep` para dados intermediários | Local reservado para dados parcialmente tratados | NECESSITA_REVISAO | Geração de base está bloqueada; deve haver orientação explícita de não uso inicial. |
| `data_processed/` | Pasta versionada por `.gitkeep` para dados finais | Local reservado para bases finais | NECESSITA_REVISAO | Não há autorização para gerar base final enquanto bloqueios persistirem. |
| `dashboards/` | Pasta reservada por `.gitkeep` | Futuro produto visual | NAO_AVALIADO | Pode ser mencionada como escopo futuro, não como tarefa inicial. |
| `maps/` | Pasta reservada por `.gitkeep` | Futuro produto cartográfico | NAO_AVALIADO | Pode ser mencionada como escopo futuro, não como tarefa inicial. |
| `requirements-python-poc.txt` | Dependências da prova de conceito Python | Apoio à trilha experimental | EXPERIMENTAL | Pode confundir se o aluno entender Python como caminho produtivo. |
| `fluxo_trabalho.md` | Documento de fluxo na raiz | Possível duplicação com `docs/fluxo_trabalho.md` | NECESSITA_REVISAO | Recomenda-se verificar se é duplicado, divergente ou legado em etapa posterior. |

## 4. Núcleo que deve permanecer

### Núcleo metodológico

- `docs/convensoes_metodologicas.md`: base de padronização científica, documentação, rastreabilidade, LGPD e critérios metodológicos.
- `docs/convensoes_versionamento_dados.md`: referência para versionamento e governança de dados.
- `docs/fluxo_trabalho.md` e/ou `fluxo_trabalho.md`: fluxo de colaboração e execução; requerem checagem de possível duplicidade antes de entrega pedagógica.
- `docs/matriz_manutencao.md`: referência útil para manutenção e responsabilidades, caso esteja atualizada.

### Núcleo de governança

- `AGENTS.md`: papéis, responsabilidades, linguagem principal e convenções de commit.
- `docs/governanca_codigo.md`: regras de branch, commits, pull requests, revisão e qualidade.
- `.github/workflows/validar_pipeline_cnes_r.yml`: validação contínua do pipeline R, preservada como evidência de reprodutibilidade.

### Núcleo CNES

- `docs/cnes/README.md`.
- `docs/cnes/resumo_executivo_cnes.md`.
- `docs/cnes/decisoes_metodologicas_cnes.md`.
- `docs/cnes/contrato_dados_cnes_piloto.md`.
- `docs/cnes/metadados_cnes_piloto.md`.
- `docs/cnes/base_estabelecimentos_cnes.md`.
- `docs/cnes/base_habilitacoes_cnes.md`.
- `docs/cnes/classificacao_habilitacoes_cnes.md`.
- `docs/cnes/indicadores_cnes_oferta.md`.
- `docs/cnes/produtos_tabulares_cnes.md`.
- `docs/cnes/roadmap_tecnico_cnes.md`.
- `metadata/cnes/` completo, especialmente dicionários, schemas, classificações e contratos.
- `src/extract/`, `src/transform/`, `src/indicators/` e `src/validation/` enquanto implementação R consolidada.

### Núcleo de testes

- Testes R em `tests/test_*.R` e `tests/teste_pipeline_piloto_cnes.R`.
- Fixtures CNES em `tests/fixtures/cnes/`.
- Testes Python em `tests/python/`, enquanto documentação executável da trilha experimental e dos contratos mínimos.

### Núcleo de documentação para aluno

Para uma entrega pedagógica, o núcleo inicial deve ser mais curto que o repositório completo. Recomenda-se priorizar:

- `README.md`.
- `AGENTS.md`.
- `docs/convensoes_metodologicas.md`.
- `docs/governanca_codigo.md`.
- `docs/cnes/README.md`.
- `docs/cnes/resumo_executivo_cnes.md`.
- `docs/cnes/contrato_dados_cnes_piloto.md`.
- `docs/cnes/metadados_cnes_piloto.md`.
- `docs/migracao_python/05N_encerramento_viabilidade_pysus_cnes.md`, apenas como leitura de contexto e bloqueios, não como roteiro de execução.
- Este documento, `docs/revisao_geral_entrega_aluno.md`, como mapa crítico de orientação.

## 5. Legado R e oráculos

O legado R deve ser preservado integralmente como **oráculo metodológico**. Nesta revisão, nenhum script R deve ser excluído, editado ou reclassificado como obsoleto operacional sem decisão humana posterior.

Devem ser preservados como referência/oráculo:

- `src/extract/ler_arquivos_cnes.R`.
- `src/transform/padronizar_cnes_interim.R`.
- `src/transform/executar_pipeline_piloto_cnes.R`.
- `src/transform/preparar_estabelecimentos_cnes.R`.
- `src/transform/preparar_habilitacoes_cnes.R`.
- `src/transform/classificar_habilitacoes_cnes.R`.
- `src/transform/corrigir_falsos_negativos_habilitacoes_cnes.R`.
- `src/transform/auditar_fora_escopo_habilitacoes_cnes.R`.
- `src/indicators/calcular_indicadores_cnes_oferta.R`.
- `src/validation/validar_pipeline_cnes.R`.
- `scripts/instalar_dependencias_r.R`.
- Testes R em `tests/`.
- Documentação CNES que descreve decisões e contratos do pipeline R.

Registro metodológico obrigatório: **R continua como oráculo metodológico**. Nenhum script R deve ser excluído nesta revisão. Qualquer depreciação futura depende de paridade documentada, comparação explícita com resultados do R, validação de campos críticos, decisão sobre `CO_UNIDADE` e aprovação humana.

## 6. Trilha Python/PySUS

A trilha Python/PySUS deve ser entendida como uma investigação de migração controlada, não como substituição do pipeline R.

### Artefatos úteis

- `python/observatorio_sus/cnes/contratos.py`: explicita contratos mínimos e pode ajudar a entender regras de estrutura.
- `python/observatorio_sus/cnes/contrato_intermediario_pysus_cnes.py`: materializa o contrato intermediário PySUS-CNES.
- `python/observatorio_sus/utils/normalizacao.py`: concentra normalizações úteis, desde que lidas como apoio experimental.
- `metadata/cnes/contrato_intermediario_pysus_cnes.csv`: contrato intermediário documentado.
- Testes Python de contratos e CLIs em `tests/python/`: úteis como documentação executável do que foi investigado.

### Artefatos experimentais

- `python/observatorio_sus/extract/reconhecer_api_cnes_pysus.py`.
- `python/observatorio_sus/extract/testar_cnes_pysus_ambiente_isolado.py`.
- `python/observatorio_sus/extract/diagnosticar_falha_cnes_pysus.py`.
- `python/observatorio_sus/extract/inventariar_grupos_cnes_pysus.py`.
- `python/observatorio_sus/extract/mapear_estrutura_grupos_cnes_pysus.py`.
- `python/observatorio_sus/extract/mapear_multicompetencia_cnes_pysus.py`.
- `python/observatorio_sus/extract/validar_extracao_cnes_controlada.py`.
- `python/observatorio_sus/transform/transformar_memoria_multicompetencia_cnes_pysus.py`.
- `requirements-python-poc.txt`.

### Diagnósticos encerrados

A sequência `docs/migracao_python/05N*.md` documenta uma fase longa de diagnóstico e prova de viabilidade. Ela deve permanecer como histórico técnico, mas não deve ser o primeiro material de estudo do aluno. A Etapa 5N foi encerrada com ressalvas, preservando os bloqueios: ST instável/intermitente, `CO_UNIDADE` não resolvido, ausência de paridade com R, proibição de geração de base e manutenção do R como oráculo.

### Scripts que podem confundir o aluno

Os scripts de reconhecimento, diagnóstico, mapeamento e transformação em memória podem sugerir que há um pipeline Python pronto para produção. Esse entendimento seria incorreto. Para o aluno, esses arquivos devem ser apresentados como material de leitura supervisionada, não como comandos de execução inicial.

### Scripts que devem ser mantidos, mas não apresentados como pipeline produtivo

Todos os scripts Python devem ser mantidos nesta rodada, pois registram decisões, hipóteses, testes e aprendizado técnico. Entretanto, devem ser marcados em guia futuro como **experimentais** e **não autorizados para geração de base**.

## 7. Documentação de migração Python

| Documento | Função | Deve ser lido pelo aluno? | Situação | Ação recomendada |
|---|---|---|---|---|
| `docs/migracao_python/00_baseline_r_pre_migracao.md` | Registra baseline R antes da migração | Sim, em leitura orientada | DOCUMENTACAO_HISTORICA | RESUMIR_EM_GUIA |
| `docs/migracao_python/01_classificacao_legado_r.md` | Classifica legado R e prioridades | Sim, após entender CNES | DOCUMENTACAO_HISTORICA | RESUMIR_EM_GUIA |
| `docs/migracao_python/02_governanca_arquitetura_hibrida.md` | Define governança R-Python | Sim, seletivamente | DOCUMENTACAO_METODOLOGICA | MANTER |
| `docs/migracao_python/03_poc_pysus_cnes.md` | Documenta POC inicial PySUS/CNES | Não inicialmente | EXPERIMENTAL | MANTER_COMO_HISTORICO |
| `docs/migracao_python/04_contratos_extracao_cnes_python.md` | Contratos de extração Python | Não inicialmente | EXPERIMENTAL | RESUMIR_EM_GUIA |
| `docs/migracao_python/04_deliberacao_humana_pre_etapa5.md` | Deliberação antes da Etapa 5 | Não inicialmente | DOCUMENTACAO_HISTORICA | MANTER_COMO_HISTORICO |
| `docs/migracao_python/04_revisao_pos_etapa4.md` | Revisão pós-Etapa 4 | Não inicialmente | DOCUMENTACAO_HISTORICA | MANTER_COMO_HISTORICO |
| `docs/migracao_python/05N_reinicio_cnes_python_api_pysus.md` | Reinício da investigação PySUS | Não inicialmente | DOCUMENTACAO_HISTORICA | MANTER_COMO_HISTORICO |
| `docs/migracao_python/05N1_isolamento_pysus_duckdb_cnes.md` | Isolamento de ambiente PySUS/DuckDB | Não inicialmente | EXPERIMENTAL | NÃO_ENTREGAR_AO_ALUNO_INICIALMENTE |
| `docs/migracao_python/05N2_diagnostico_falha_cnes_pos_isolamento.md` | Diagnóstico de falha CNES | Não inicialmente | EXPERIMENTAL | NÃO_ENTREGAR_AO_ALUNO_INICIALMENTE |
| `docs/migracao_python/05N3_inventario_grupos_cnes_pysus.md` | Inventário de grupos CNES via PySUS | Talvez, com tutor | EXPERIMENTAL | RESUMIR_EM_GUIA |
| `docs/migracao_python/05N3R_reteste_controlado_st_cnes_pysus.md` | Reteste controlado ST | Não inicialmente | EXPERIMENTAL | MANTER_COMO_HISTORICO |
| `docs/migracao_python/05N4_mapeamento_estrutural_grupos_cnes_pysus.md` | Mapeamento estrutural de grupos | Talvez, com tutor | EXPERIMENTAL | RESUMIR_EM_GUIA |
| `docs/migracao_python/05N5_mapeamento_multicompetencia_cnes_pysus.md` | Mapeamento multi-competência | Não inicialmente | EXPERIMENTAL | MANTER_COMO_HISTORICO |
| `docs/migracao_python/05N6_contrato_intermediario_pysus_cnes.md` | Contrato intermediário PySUS-CNES | Sim, depois do contrato CNES | EXPERIMENTAL | RESUMIR_EM_GUIA |
| `docs/migracao_python/05N6R_deliberacao_humana_contrato_intermediario_pysus_cnes.md` | Deliberação humana sobre contrato intermediário | Não inicialmente | DOCUMENTACAO_HISTORICA | MANTER_COMO_HISTORICO |
| `docs/migracao_python/05N7_8_transformacao_memoria_multicompetencia_cnes_pysus.md` | Transformação em memória multi-competência | Não inicialmente | EXPERIMENTAL | NÃO_ENTREGAR_AO_ALUNO_INICIALMENTE |
| `docs/migracao_python/05N7_8A_validacao_minima_transformacao_memoria_cnes_pysus.md` | Validação mínima da transformação | Não inicialmente | EXPERIMENTAL | NÃO_ENTREGAR_AO_ALUNO_INICIALMENTE |
| `docs/migracao_python/05N7_8D_diagnostico_timeout_transformacao_memoria_cnes_pysus.md` | Diagnóstico de timeout | Não inicialmente | EXPERIMENTAL | ARQUIVAR_POSTERIORMENTE |
| `docs/migracao_python/05N7_8E_correcao_caminho_padrao_transformacao_memoria_cnes_pysus.md` | Correção de caminho padrão | Não inicialmente | EXPERIMENTAL | ARQUIVAR_POSTERIORMENTE |
| `docs/migracao_python/05N7_8F_diagnostico_st_transformacao_memoria_cnes_pysus.md` | Diagnóstico ST na transformação | Não inicialmente | EXPERIMENTAL | ARQUIVAR_POSTERIORMENTE |
| `docs/migracao_python/05N7_8G_diagnostico_acesso_st_pysus_cnes.md` | Diagnóstico de acesso ST | Não inicialmente | EXPERIMENTAL | ARQUIVAR_POSTERIORMENTE |
| `docs/migracao_python/05N_encerramento_viabilidade_pysus_cnes.md` | Encerramento da Etapa 5N com ressalvas | Sim, como síntese de limites | DOCUMENTACAO_METODOLOGICA | MANTER |

## 8. Documentação CNES

A documentação CNES é o conjunto mais consolidado do repositório e deve ser protegida como núcleo metodológico. Ela contém documentos de escopo, contratos, bases, classificações, indicadores, auditorias, fontes normativas e roadmap técnico.

### Documentos consolidados

- `docs/cnes/README.md`: índice e porta de entrada CNES.
- `docs/cnes/resumo_executivo_cnes.md`: síntese executiva do piloto.
- `docs/cnes/visao_analitica_cnes_observatorio.md`: visão analítica do CNES no Observatório.
- `docs/cnes/decisoes_metodologicas_cnes.md`: decisões metodológicas críticas.
- `docs/cnes/roadmap_tecnico_cnes.md`: planejamento técnico.
- `docs/cnes/setup_execucao_local_r.md`: execução local em R, apenas para fase supervisionada.

### Contratos

- `docs/cnes/contrato_dados_cnes_piloto.md`.
- `docs/cnes/metadados_cnes_piloto.md`.
- `metadata/cnes/schema_cnes_piloto.yml`.
- `metadata/cnes/schema_estabelecimentos_cnes.csv`.
- `metadata/cnes/schema_habilitacoes_cnes.csv`.
- `metadata/cnes/contrato_intermediario_pysus_cnes.csv`.

### Dicionários

- `metadata/cnes/dicionario_cnes_piloto.csv`.
- `metadata/cnes/dicionario_estabelecimentos_cnes.csv`.
- `metadata/cnes/dicionario_habilitacoes_cnes.csv`.
- `metadata/cnes/dicionario_indicadores_cnes_oferta.csv`.

### Classificações e auditorias

- `docs/cnes/classificacao_habilitacoes_cnes.md`.
- `metadata/cnes/classificacao_habilitacoes_cnes.csv`.
- `docs/cnes/auditoria_fora_escopo_habilitacoes_cnes.md`.
- `metadata/cnes/auditoria_fora_escopo_habilitacoes_cnes_202601.csv`.
- `metadata/cnes/auditoria_linguistica_textos_ingles.csv`.
- `metadata/cnes/matriz_revisao_produtos_cnes_observatorio.csv`.

### Arquivos que o aluno deve conhecer

O aluno deve conhecer, nessa ordem: `docs/cnes/README.md`, `docs/cnes/resumo_executivo_cnes.md`, `docs/cnes/contrato_dados_cnes_piloto.md`, `docs/cnes/metadados_cnes_piloto.md`, `docs/cnes/base_estabelecimentos_cnes.md`, `docs/cnes/base_habilitacoes_cnes.md`, `docs/cnes/indicadores_cnes_oferta.md` e os dicionários correspondentes em `metadata/cnes/`.

### Arquivos protegidos contra edição

Todos os arquivos em `metadata/cnes/`, `docs/cnes/`, scripts R em `src/` e testes em `tests/` devem ser protegidos contra edição inicial pelo aluno. Edições futuras só devem ocorrer com tarefa explícita, justificativa metodológica e revisão humana.

## 9. Arquivos que podem confundir o aluno

| Arquivo/Diretório | Motivo de confusão | Risco | Ação recomendada |
|---|---|---|---|
| `docs/migracao_python/` | Contém muitas etapas, diagnósticos e subetapas 5N | Aluno confundir histórico de investigação com roteiro de execução | Criar resumo pedagógico e arquivar subetapas posteriormente. |
| `python/observatorio_sus/extract/` | Scripts parecem comandos operacionais de extração | Execução indevida de PySUS ou tentativa de baixar dados | Marcar como experimental e não executar inicialmente. |
| `python/observatorio_sus/transform/` | Transformação em memória pode parecer pipeline válido | Geração ou interpretação indevida de base não validada | Manter como experimento; bloquear uso produtivo. |
| `requirements-python-poc.txt` | Pode sugerir instalação e uso imediato da POC | Aluno iniciar pela trilha Python em vez do núcleo CNES/R | Entregar apenas com nota de POC experimental. |
| `data_raw/`, `data_interim/`, `data_processed/` | Pastas existem, mas geração está bloqueada | Escrita indevida de dados e quebra de rastreabilidade | Criar guia explícito de não escrita inicial. |
| `fluxo_trabalho.md` e `docs/fluxo_trabalho.md` | Possível duplicidade de fluxo | Leitura divergente ou redundante | Comparar e consolidar posteriormente. |
| `src/indicators/src/validation/.gitkeep` | Caminho incomum dentro de `src/indicators` | Interpretação equivocada da estrutura | Verificar em limpeza futura; não excluir nesta rodada. |
| `tests/python/` | Testes de CLIs experimentais | Aluno inferir maturidade produtiva da trilha PySUS | Apresentar como documentação executável experimental. |
| `docs/cnes/setup_execucao_local_r.md` | Guia de execução local | Aluno executar sem supervisão e sem dados corretos | Usar apenas em fase 4 supervisionada. |
| Documentos `05N7_8*` | Diagnósticos detalhados de timeout, ST e transformação | Sobrecarga cognitiva e foco em depuração encerrada | Não entregar inicialmente; resumir no encerramento 5N. |

## 10. O que não deve ser entregue inicialmente ao aluno

Não se recomenda entregar inicialmente como material principal:

- A pasta completa `docs/migracao_python/` sem roteiro.
- Scripts Python de extração e transformação como comandos de uso.
- `requirements-python-poc.txt` como instrução de instalação inicial.
- Documentos detalhados `05N7_8*` de diagnóstico operacional.
- Pastas `data_raw/`, `data_interim/` e `data_processed/` como locais de trabalho livre.
- Workflows de CI como tarefa de edição.
- Testes como tarefa de modificação.
- `metadata/cnes/` como área editável.
- Qualquer orientação para gerar base, baixar dados ou executar PySUS.

Esses itens não devem ser excluídos. Devem ficar como referência secundária, histórica ou técnica, acessível apenas após orientação.

## 11. O que deve ser entregue ao aluno

Proposta de pacote pedagógico mínimo:

| Item | Por que entregar | Como o aluno deve usar |
|---|---|---|
| `README.md` | Apresenta finalidade, estrutura e status geral | Ler primeiro para entender o projeto, sem executar comandos. |
| `AGENTS.md` | Define papéis, responsabilidades e linguagem principal | Ler para compreender limites, governança e postura esperada. |
| `docs/convensoes_metodologicas.md` | Explica padrões científicos e reprodutibilidade | Usar como referência de escrita, metadados e cautelas metodológicas. |
| `docs/governanca_codigo.md` | Define governança de branches, commits e revisão | Consultar antes de qualquer contribuição futura. |
| `docs/cnes/README.md` | Porta de entrada para CNES | Ler como índice do módulo CNES. |
| `docs/cnes/resumo_executivo_cnes.md` | Síntese do piloto CNES | Entender escopo sem entrar de imediato nos detalhes. |
| `docs/cnes/contrato_dados_cnes_piloto.md` | Define contrato dos dados | Usar para compreender campos, chaves e limites. |
| `docs/cnes/metadados_cnes_piloto.md` | Complementa o contrato com metadados | Relacionar documentação e arquivos em `metadata/cnes/`. |
| `metadata/cnes/dicionario_cnes_piloto.csv` | Dicionário de dados do piloto | Ler em modo consulta; não editar. |
| `metadata/cnes/schema_cnes_piloto.yml` | Schema do piloto | Ler como contrato formal; não editar. |
| `docs/migracao_python/05N_encerramento_viabilidade_pysus_cnes.md` | Resume por que PySUS não virou pipeline produtivo | Ler somente após entender CNES/R, como contexto de bloqueios. |
| `src/` | Scripts R do núcleo/oráculo | Ler em modo supervisionado; não alterar. |
| `tests/` | Testes e fixtures | Ler depois para entender validação; não alterar inicialmente. |
| `docs/revisao_geral_entrega_aluno.md` | Mapa crítico desta curadoria | Usar como roteiro de orientação e limites da entrega. |

## 12. Lacunas antes da entrega ao aluno

Antes da entrega pedagógica ideal, recomenda-se criar ou melhorar:

- Guia “por onde começar”.
- Mapa do repositório com indicação de leitura obrigatória, leitura complementar e não executar.
- Glossário CNES com termos como CNES, estabelecimento, habilitação, competência, ST, LT, SR e `CO_UNIDADE`.
- Instruções explícitas do que o aluno não deve editar.
- Plano semanal de leitura e fichamento.
- Roteiro de leitura dos documentos CNES.
- Resumo pedagógico da migração Python/PySUS em uma página.
- Índice de documentos históricos e diagnósticos.
- Tabela de “pipeline produtivo” versus “experimento”.
- Nota sobre bloqueio de geração de base.
- Fichamento técnico orientado para o aluno preencher.

## 13. Recomendações de limpeza

### 13.1 Limpeza imediata segura

Itens que podem ser feitos em rodada posterior sem risco metodológico relevante:

- Criar `docs/guias_aluno/` com guia de início, roteiro de leitura e glossário.
- Criar `docs/indice_repositorio.md` com mapa dos diretórios.
- Criar uma nota curta `docs/migracao_python/README.md` explicando que a pasta é histórica/experimental, caso ainda não exista.
- Criar uma tabela de classificação dos documentos de migração por status: produtivo, histórico, experimental, encerrado.
- Marcar explicitamente scripts Python como experimentais em documentação, sem alterar os scripts.
- Criar orientação “não escrever em `data_*` sem autorização”.
- Verificar duplicidade entre `fluxo_trabalho.md` e `docs/fluxo_trabalho.md` antes de consolidar.

### 13.2 Limpeza após validação humana

Itens que dependem de decisão do pesquisador principal ou responsável metodológico:

- Mover documentos detalhados da Etapa 5N para `docs/migracao_python/arquivo/`.
- Consolidar documentos supersedidos da migração Python em um guia único.
- Definir quais documentos de migração devem ficar visíveis na entrega ao aluno.
- Reavaliar a necessidade do caminho `src/indicators/src/validation/.gitkeep`.
- Definir se `fluxo_trabalho.md` na raiz deve ser removido, redirecionado ou consolidado com `docs/fluxo_trabalho.md`.
- Deliberar sobre uma futura Etapa 6 apenas após material pedagógico mínimo.
- Definir política formal de acesso e escrita em `data_raw/`, `data_interim/` e `data_processed/`.

### 13.3 Não limpar por enquanto

Itens que devem permanecer preservados:

- Todos os scripts R em `src/` e `scripts/`.
- Todos os testes R e Python em `tests/`.
- Todos os arquivos em `metadata/cnes/`.
- Todos os documentos em `docs/cnes/`.
- Toda a trilha Python/PySUS em `python/`, até decisão posterior.
- Todos os documentos `docs/migracao_python/05N*`, até arquivamento deliberado.
- Workflows em `.github/workflows/`.
- Pastas `data_*` com `.gitkeep`, sem escrita de dados.

## 14. Proposta de reorganização sem perda histórica

Recomenda-se, em etapa futura e sem perda histórica:

- Criar `docs/arquivo_historico/` para documentos gerais supersedidos, se houver.
- Criar `docs/migracao_python/arquivo/` para diagnósticos detalhados e subetapas encerradas.
- Criar `docs/guias_aluno/` para materiais didáticos.
- Criar `docs/indice_repositorio.md` com o mapa oficial do repositório.
- Criar `docs/guia_inicio_aluno.md` com leitura em ordem, objetivos e proibições iniciais.
- Criar `docs/guias_aluno/glossario_cnes.md`.
- Criar `docs/guias_aluno/roteiro_leitura_cnes.md`.
- Criar `docs/guias_aluno/fichamento_tecnico_cnes.md`.
- Criar `docs/guias_aluno/o_que_nao_executar.md`.

Esta revisão não executa a reorganização; apenas recomenda os movimentos.

## 15. Plano de entrega ao aluno

### Fase 1 — leitura orientada

Objetivo: compreender o projeto, sua governança e o escopo CNES.

Leituras sugeridas:

1. `README.md`.
2. `AGENTS.md`.
3. `docs/convensoes_metodologicas.md`.
4. `docs/governanca_codigo.md`.
5. `docs/cnes/README.md`.
6. `docs/cnes/resumo_executivo_cnes.md`.

Produto esperado: resumo de uma página explicando o que é o Observatório SUS-ES, qual é o papel do CNES e por que o R permanece como oráculo.

### Fase 2 — compreensão dos dados CNES

Objetivo: entender contratos, campos, metadados e bases documentadas.

Leituras sugeridas:

1. `docs/cnes/contrato_dados_cnes_piloto.md`.
2. `docs/cnes/metadados_cnes_piloto.md`.
3. `docs/cnes/base_estabelecimentos_cnes.md`.
4. `docs/cnes/base_habilitacoes_cnes.md`.
5. Dicionários em `metadata/cnes/`.

Produto esperado: tabela de campos críticos, significados e cuidados de interpretação.

### Fase 3 — fichamento técnico

Objetivo: transformar leitura em material de apoio ao projeto.

Atividades:

- Fichar documentos CNES.
- Listar dúvidas metodológicas.
- Separar termos que precisam de glossário.
- Identificar documentos que parecem redundantes ou difíceis.

Produto esperado: fichamento técnico revisável pelo orientador.

### Fase 4 — execução supervisionada, se houver

Objetivo: somente após autorização, observar como o pipeline R é validado.

Limites:

- Não executar PySUS.
- Não baixar dados.
- Não gerar bases.
- Não escrever em `data_raw/`, `data_interim/` ou `data_processed/`.
- Qualquer execução deve ser orientada pelo responsável e usar dados/fixtures autorizados.

Produto esperado: relatório de aprendizado sobre validação e testes, sem alteração de código.

### Fase 5 — produção de documentação/tabelas auxiliares

Objetivo: contribuir sem risco ao núcleo técnico.

Possíveis entregas:

- Glossário CNES.
- Roteiro de leitura.
- Mapa do repositório.
- Tabela de documentos por status.
- Fichamento de contratos e dicionários.
- Lista de dúvidas para próxima reunião metodológica.

## 16. Decisão sobre Etapa 6

A Etapa 6 deve vir somente depois da limpeza/documentação pedagógica mínima. Antes de qualquer nova etapa técnica, o repositório precisa estar mais claro para leitores iniciantes, com separação visível entre núcleo R/CNES, histórico de migração, experimentos PySUS e bloqueios metodológicos.

Nome sugerido para etapa futura:

**Etapa 6 — consolidação da estratégia de migração controlada CNES R–Python/PySUS**

Essa etapa deve definir o que permanece em R, o que pode avançar em Python, o que continua bloqueado por `CO_UNIDADE`, como tratar ST instável, quais comparações com R serão obrigatórias e em que condições poderá haver primeira materialização controlada. Entretanto, a entrega ao aluno e a limpeza documental pedagógica devem ter prioridade antes de qualquer nova etapa técnica.

## 17. Checklist de revisão

- [x] Inventário de diretórios realizado.
- [x] Núcleo atual identificado.
- [x] Legado/oráculo identificado.
- [x] Experimentos identificados.
- [x] Documentos confusos identificados.
- [x] Pacote pedagógico mínimo proposto.
- [x] Limpeza imediata segura proposta.
- [x] Limpeza dependente de validação humana proposta.
- [x] Nenhum arquivo excluído.
- [x] Nenhum código alterado.
- [x] Nenhum dado alterado.

## 18. Conclusão

Classificação final: **NECESSITA_LIMPEZA_DOCUMENTAL**.

O repositório possui um núcleo técnico e metodológico robusto, especialmente no piloto CNES em R, nos metadados, nos contratos, nos testes e na documentação CNES. Contudo, ainda não está idealmente pronto para entrega direta ao aluno sem mediação, porque há grande volume de documentos de migração Python/PySUS, muitas subetapas diagnósticas, scripts experimentais que podem parecer produtivos e pastas de dados que exigem regras explícitas de não escrita.

A recomendação é entregar o repositório ao aluno apenas com guia de orientação ou após uma rodada curta de limpeza documental. O pacote inicial deve enfatizar README, governança, convenções metodológicas, documentação CNES consolidada, contratos, dicionários e o documento de encerramento da Etapa 5N como síntese de limites. A trilha Python/PySUS deve permanecer preservada, mas secundária, histórica e supervisionada.

Resumo desta revisão:

- Documento criado: `docs/revisao_geral_entrega_aluno.md`.
- Estado geral: núcleo CNES/R consolidado; Python/PySUS experimental e encerrado na Etapa 5N com ressalvas.
- Principais itens a manter: `src/`, `tests/`, `docs/cnes/`, `metadata/cnes/`, governança e workflow R.
- Principais itens a não entregar inicialmente: subetapas detalhadas de migração Python, scripts PySUS como comandos de uso, pastas `data_*` como locais livres de trabalho e diagnósticos operacionais `05N7_8*`.
- Recomendações de limpeza: criar guias do aluno, índice do repositório, glossário CNES, roteiro de leitura e eventual arquivo histórico para subetapas de migração.
- Proposta de pacote pedagógico: README, AGENTS, governança, convenções, documentação CNES consolidada, contratos, metadados, dicionários, encerramento 5N e esta revisão.
- Confirmação: nenhum código, dado, metadado existente, documento em `docs/cnes`, script R, script Python, teste ou workflow foi alterado nesta rodada.
